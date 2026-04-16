"""AI 배치 처리."""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from ai.model_router import call_gemini, call_gemini_multimodal
from db.database import get_unprocessed_articles, update_article_fields
from utils.helpers import log

BATCH_SIZE = 8
MAX_PARALLEL_BATCHES = 2
ARTICLE_UPDATE_FIELDS = (
    "category",
    "importance",
    "sentiment",
    "sentiment_reason",
    "tags",
    "summary_text",
    "ai_processed",
    "image_analysis",
)


def _build_batch_prompt(articles: list[dict]) -> str:
    items = []
    for article in articles:
        items.append(
            f"[ID: {article['id']}]\n"
            f"title: {article['title']}\n"
            f"content: {article['content'][:800]}"
        )
    joined = "\n\n---\n\n".join(items)
    return f"Analyze these {len(articles)} AI news articles and return JSON only.\n\n{joined}"


def _parse_response(text: str) -> list[dict]:
    try:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        parsed = json.loads(text)

        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict):
            for key in ("articles", "results", "data", "items", "analysis"):
                if key in parsed and isinstance(parsed[key], list):
                    return parsed[key]
            for value in parsed.values():
                if isinstance(value, list) and value and isinstance(value[0], dict):
                    return value
        return []
    except json.JSONDecodeError:
        log(f"[batch:parse-error] raw={text[:200]}")
        return []


def _process_batch(batch: list[dict]) -> list[tuple[str, dict]]:
    prompt = _build_batch_prompt(batch)
    try:
        response_text = call_gemini(prompt, use_flash=False)
        results = _parse_response(response_text)
        if not results:
            return []

        matched = []
        for index, result in enumerate(results):
            article_id = result.get("id", "")
            if not article_id and index < len(batch):
                article_id = batch[index]["id"]
            if article_id:
                matched.append((article_id, result))
        return matched
    except Exception as e:
        log(f"[batch:error] {e}")
        return []


def process_unprocessed(skip_images: bool = False) -> int:
    # DB에서 미처리 기사 조회 (JSON 전체 로드 불필요)
    unprocessed = get_unprocessed_articles(limit=200)

    if not unprocessed:
        log("[batch] no unprocessed articles")
        return 0

    # 배치 처리 결과를 모아 일괄 DB 업데이트
    processed_results: dict[str, dict] = {}
    batches = [unprocessed[i:i + BATCH_SIZE] for i in range(0, len(unprocessed), BATCH_SIZE)]
    processed_count = 0

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_BATCHES) as executor:
        futures = {executor.submit(_process_batch, batch): batch for batch in batches}

        for future in as_completed(futures):
            try:
                results = future.result()
                for article_id, result in results:
                    processed_results[article_id] = {
                        "category": result.get("category", "ai_other"),
                        "importance": result.get("importance", 3),
                        "sentiment": result.get("sentiment", "neutral"),
                        "sentiment_reason": result.get("sentiment_reason", ""),
                        "tags": result.get("tags", []),
                        "summary_text": result.get("summary", result.get("summary_text", "")),
                        "ai_processed": True,
                    }
                    processed_count += 1
            except Exception as e:
                log(f"[batch:error] {e}")

    # 이미지 분석 (상위 20개)
    if not skip_images:
        image_count = 0
        for article in unprocessed[:20]:
            art_id = article["id"]
            if art_id not in processed_results:
                continue
            image_urls = article.get("image_urls", [])
            if not image_urls or article.get("image_analysis"):
                continue
            try:
                analysis = call_gemini_multimodal(image_urls[0])
                if analysis and "error" not in analysis.lower():
                    processed_results[art_id]["image_analysis"] = analysis
                    image_count += 1
            except Exception:
                pass
        if image_count > 0:
            log(f"[batch:image-analysis] count={image_count}")

    # DB에 필드별 업데이트 (파라미터화 쿼리)
    for article_id, fields in processed_results.items():
        update_article_fields(article_id, fields)

    # ChromaDB에 처리된 기사 벡터 추가
    try:
        from ai.vector_store import add_articles
        newly_processed = [a for a in unprocessed if a["id"] in processed_results]
        add_articles(newly_processed)
    except Exception as e:
        log(f"[batch:vector-error] {e}")

    log(f"[batch:done] processed={processed_count} batches={len(batches)} parallel={MAX_PARALLEL_BATCHES}")
    return processed_count
