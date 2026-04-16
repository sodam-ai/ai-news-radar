"""AI 배치 처리."""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from ai.model_router import call_gemini, call_gemini_multimodal
from config import DATA_DIR
from utils.helpers import log, safe_read_json, safe_update_json

ARTICLES_PATH = DATA_DIR / "articles.json"
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


def _merge_processed_articles(current_articles: list[dict], updated_articles: dict[str, dict]) -> list[dict]:
    merged = []
    for article in current_articles:
        updated = updated_articles.get(article.get("id"))
        if not updated or not updated.get("ai_processed"):
            merged.append(article)
            continue

        merged_article = dict(article)
        for field in ARTICLE_UPDATE_FIELDS:
            if field in updated:
                merged_article[field] = updated[field]
        merged.append(merged_article)
    return merged


def process_unprocessed(skip_images: bool = False) -> int:
    articles = safe_read_json(ARTICLES_PATH, [])
    unprocessed = [article for article in articles if not article.get("ai_processed")]

    if not unprocessed:
        log("[batch] no unprocessed articles")
        return 0

    articles_map = {article["id"]: dict(article) for article in articles}
    processed_count = 0
    batches = [unprocessed[index:index + BATCH_SIZE] for index in range(0, len(unprocessed), BATCH_SIZE)]

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_BATCHES) as executor:
        futures = {executor.submit(_process_batch, batch): batch for batch in batches}

        for future in as_completed(futures):
            try:
                results = future.result()
                for article_id, result in results:
                    target = articles_map.get(article_id)
                    if not target:
                        continue
                    target["category"] = result.get("category", "ai_other")
                    target["importance"] = result.get("importance", 3)
                    target["sentiment"] = result.get("sentiment", "neutral")
                    target["sentiment_reason"] = result.get("sentiment_reason", "")
                    target["tags"] = result.get("tags", [])
                    if "summary" in result:
                        target["summary_text"] = result["summary"]
                    target["ai_processed"] = True
                    processed_count += 1
            except Exception as e:
                log(f"[batch:error] {e}")

    if not skip_images:
        image_count = 0
        for article in unprocessed[:20]:
            target = articles_map.get(article["id"])
            if not target or not target.get("ai_processed"):
                continue

            image_urls = target.get("image_urls", [])
            if not image_urls or target.get("image_analysis"):
                continue

            try:
                analysis = call_gemini_multimodal(image_urls[0])
                if analysis and "error" not in analysis.lower():
                    target["image_analysis"] = analysis
                    image_count += 1
            except Exception:
                pass

        if image_count > 0:
            log(f"[batch:image-analysis] count={image_count}")

    safe_update_json(
        ARTICLES_PATH,
        lambda current: _merge_processed_articles(current, articles_map),
        default=articles,
    )

    # ChromaDB에 처리된 기사 벡터 추가
    try:
        from ai.vector_store import add_articles
        newly_processed = [a for a in articles_map.values() if a.get("ai_processed")]
        add_articles(newly_processed)
    except Exception as e:
        log(f"[batch:vector-error] {e}")

    log(f"[batch:done] processed={processed_count} batches={len(batches)} parallel={MAX_PARALLEL_BATCHES}")
    return processed_count
