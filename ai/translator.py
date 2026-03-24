"""자동 한국어 번역 — 영어 기사 제목+요약을 한국어로 번역

LLM을 활용하여 영어 기사의 제목과 요약을 자연스러운 한국어로 번역합니다.
배치 처리로 API 호출을 최소화합니다.
"""
import json

from config import DATA_DIR
from ai.model_router import call_gemini, get_active_provider
from utils.helpers import safe_read_json, safe_write_json, log

ARTICLES_PATH = DATA_DIR / "articles.json"

TRANSLATE_SYSTEM = """너는 AI 뉴스 번역 전문가야.
영어 기사의 제목과 요약을 자연스러운 한국어로 번역해.

규칙:
- AI/기술 용어는 원문 유지 (예: Claude Code, Stable Diffusion, GPT)
- 브랜드명, 제품명은 번역하지 않음
- 자연스럽고 읽기 쉬운 한국어
- 의역 가능 (직역보다 의미 전달 우선)
- 반드시 JSON으로만 응답

입력 형식: [{"id": "...", "title": "...", "summary": "..."}, ...]
출력 형식: [{"id": "...", "title_ko": "...", "summary_ko": "..."}, ...]"""


def translate_articles(max_batch: int = 10) -> int:
    """미번역 영어 기사를 한국어로 번역. 번역된 기사 수 반환."""
    if not get_active_provider():
        return 0

    articles = safe_read_json(ARTICLES_PATH, [])

    # 미번역 영어 기사 필터 (ai_processed + 한국어 제목 없음)
    untranslated = [
        a for a in articles
        if a.get("ai_processed")
        and a.get("is_primary", True)
        and not a.get("title_ko")
        and _is_english(a.get("title", ""))
    ]

    if not untranslated:
        return 0

    # 배치 처리 (max_batch개씩)
    batch = untranslated[:max_batch]

    prompt_items = [
        {"id": a["id"], "title": a.get("title", ""), "summary": a.get("summary_text", "")[:200]}
        for a in batch
    ]

    prompt = f"다음 영어 AI 뉴스를 한국어로 번역해줘:\n\n{json.dumps(prompt_items, ensure_ascii=False)}"

    try:
        response_text = call_gemini(prompt, use_flash=True)
        cleaned = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        translations = json.loads(cleaned)
    except Exception as e:
        log(f"[번역 오류] {e}")
        return 0

    if not isinstance(translations, list):
        return 0

    # 번역 결과 적용
    trans_map = {t["id"]: t for t in translations if isinstance(t, dict) and "id" in t}
    translated_count = 0

    for a in articles:
        t = trans_map.get(a.get("id"))
        if t:
            a["title_ko"] = t.get("title_ko", "")
            a["summary_ko"] = t.get("summary_ko", "")
            translated_count += 1

    if translated_count > 0:
        safe_write_json(ARTICLES_PATH, articles)
        log(f"[번역] {translated_count}개 기사 한국어 번역 완료")

    return translated_count


def _is_english(text: str) -> bool:
    """텍스트가 주로 영어인지 판단 (간단한 휴리스틱)"""
    if not text:
        return False
    ascii_count = sum(1 for c in text if c.isascii())
    return ascii_count / max(len(text), 1) > 0.7


def get_translation_stats() -> dict:
    """번역 통계"""
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]
    english = [a for a in processed if _is_english(a.get("title", ""))]
    translated = [a for a in english if a.get("title_ko")]

    return {
        "total": len(processed),
        "english": len(english),
        "translated": len(translated),
        "untranslated": len(english) - len(translated),
    }
