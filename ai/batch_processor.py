"""배치 처리 — 글 N개를 1회 API로 요약+분류+중요도+감성+키워드 (최적화)"""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import DATA_DIR
from ai.model_router import call_gemini, call_gemini_multimodal
from utils.helpers import safe_read_json, safe_write_json, log

ARTICLES_PATH = DATA_DIR / "articles.json"
BATCH_SIZE = 8  # 5→8로 증가 (API 호출 횟수 감소)
MAX_PARALLEL_BATCHES = 2  # 동시 배치 처리 수 (API 레이트 리밋 고려)


def _build_batch_prompt(articles: list[dict]) -> str:
    items = []
    for a in articles:
        items.append(
            f"[ID: {a['id']}]\n제목: {a['title']}\n내용: {a['content'][:800]}"
        )
    joined = "\n\n---\n\n".join(items)
    return f"다음 {len(articles)}개 AI 뉴스 기사를 분석해줘:\n\n{joined}"


def _parse_response(text: str) -> list[dict]:
    """LLM 응답을 파싱하여 분석 결과 리스트 반환."""
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
            for v in parsed.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    return v
        return []
    except json.JSONDecodeError:
        log(f"[배치 파싱 실패] 응답: {text[:200]}")
        return []


def _process_batch(batch: list[dict]) -> list[tuple[str, dict]]:
    """단일 배치 처리 (병렬 실행용). [(article_id, result_dict), ...] 반환."""
    prompt = _build_batch_prompt(batch)
    try:
        response_text = call_gemini(prompt, use_flash=False)
        results = _parse_response(response_text)
        if not results:
            return []

        matched = []
        for idx, result in enumerate(results):
            art_id = result.get("id", "")
            if not art_id and idx < len(batch):
                art_id = batch[idx]["id"]
            if art_id:
                matched.append((art_id, result))
        return matched
    except Exception as e:
        log(f"[배치 처리 오류] {e}")
        return []


def process_unprocessed(skip_images: bool = False) -> int:
    """아직 AI 처리되지 않은 기사를 배치로 처리. 처리된 수 반환.

    Args:
        skip_images: True이면 이미지 분석 건너뜀 (속도 우선)
    """
    articles = safe_read_json(ARTICLES_PATH, [])
    unprocessed = [a for a in articles if not a.get("ai_processed")]

    if not unprocessed:
        log("[배치] 처리할 새 기사 없음")
        return 0

    articles_map = {a["id"]: a for a in articles}
    processed_count = 0

    # 배치 분할
    batches = [unprocessed[i:i + BATCH_SIZE] for i in range(0, len(unprocessed), BATCH_SIZE)]

    # 병렬 배치 처리
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_BATCHES) as executor:
        futures = {executor.submit(_process_batch, batch): batch for batch in batches}

        for future in as_completed(futures):
            try:
                results = future.result()
                for art_id, result in results:
                    target = articles_map.get(art_id)
                    if target:
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
                log(f"[배치 병렬 오류] {e}")

    # ── 멀티모달 이미지 분석 (선택적) ──
    if not skip_images:
        image_count = 0
        for a in unprocessed[:20]:  # 최대 20개만 (속도 제한)
            target = articles_map.get(a["id"])
            if not target or not target.get("ai_processed"):
                continue
            image_urls = target.get("image_urls", [])
            if not image_urls or target.get("image_analysis"):
                continue
            try:
                analysis = call_gemini_multimodal(image_urls[0])
                if analysis and "실패" not in analysis:
                    target["image_analysis"] = analysis
                    image_count += 1
            except Exception:
                pass
        if image_count > 0:
            log(f"[멀티모달] {image_count}개 이미지 분석")

    safe_write_json(ARTICLES_PATH, list(articles_map.values()))
    log(f"[배치 완료] {processed_count}개 AI 처리 ({len(batches)}배치, 병렬{MAX_PARALLEL_BATCHES})")
    return processed_count
