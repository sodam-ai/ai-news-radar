"""Gemini 배치 처리 — 글 5~10개를 1회 API로 요약+분류+중요도+감성+키워드"""
import json

from config import DATA_DIR
from ai.model_router import call_gemini, call_gemini_multimodal
from utils.helpers import safe_read_json, safe_write_json

ARTICLES_PATH = DATA_DIR / "articles.json"
BATCH_SIZE = 5


def _build_batch_prompt(articles: list[dict]) -> str:
    items = []
    for a in articles:
        items.append(
            f"[ID: {a['id']}]\n제목: {a['title']}\n내용: {a['content'][:1000]}"
        )
    joined = "\n\n---\n\n".join(items)
    return f"다음 {len(articles)}개 AI 뉴스 기사를 분석해줘:\n\n{joined}"


def _parse_response(text: str) -> list[dict]:
    try:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"[배치 파싱 실패] 응답: {text[:200]}")
        return []


def process_unprocessed() -> int:
    """아직 AI 처리되지 않은 기사를 배치로 처리. 처리된 수 반환."""
    articles = safe_read_json(ARTICLES_PATH, [])
    unprocessed = [a for a in articles if not a.get("ai_processed")]

    if not unprocessed:
        print("[배치] 처리할 새 기사 없음")
        return 0

    articles_map = {a["id"]: a for a in articles}
    processed_count = 0

    for i in range(0, len(unprocessed), BATCH_SIZE):
        batch = unprocessed[i : i + BATCH_SIZE]
        prompt = _build_batch_prompt(batch)

        try:
            response_text = call_gemini(prompt, use_flash=False)
            results = _parse_response(response_text)

            if not results:
                continue

            for result in results:
                art_id = result.get("id", "")
                # ID 매칭: 응답에서 ID를 찾거나 순서대로 매칭
                target = articles_map.get(art_id)
                if not target:
                    idx = results.index(result)
                    if idx < len(batch):
                        target = articles_map.get(batch[idx]["id"])

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
            print(f"[배치 처리 오류] {e}")
            continue

    # ── 멀티모달 이미지 분석 (이미지가 있는 기사만) ──
    image_count = 0
    for a in unprocessed:
        target = articles_map.get(a["id"])
        if not target or not target.get("ai_processed"):
            continue
        image_urls = target.get("image_urls", [])
        if not image_urls or target.get("image_analysis"):
            continue

        # 첫 번째 이미지만 분석 (API 한도 절약)
        try:
            analysis = call_gemini_multimodal(image_urls[0])
            if analysis and "실패" not in analysis:
                target["image_analysis"] = analysis
                image_count += 1
        except Exception as e:
            print(f"[이미지 분석 오류] {target['id']}: {e}")

    if image_count > 0:
        print(f"[멀티모달] {image_count}개 이미지 분석 완료")

    safe_write_json(ARTICLES_PATH, list(articles_map.values()))
    print(f"[배치 완료] {processed_count}개 기사 AI 처리됨")
    return processed_count
