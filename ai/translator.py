"""기사 제목/요약 번역."""
import json

from ai.model_router import call_gemini, get_active_provider
from config import DATA_DIR
from utils.helpers import log, safe_read_json, safe_update_json

ARTICLES_PATH = DATA_DIR / "articles.json"

TRANSLATE_SYSTEM = """Translate AI news titles and summaries into natural Korean.
Keep product names and technical terms in their original form where needed.
Return JSON only in the form:
[{"id": "...", "title_ko": "...", "summary_ko": "..."}, ...]
"""


def _merge_translations(current_articles: list[dict], translations: dict[str, dict]) -> list[dict]:
    merged = []
    for article in current_articles:
        translated = translations.get(article.get("id"))
        if not translated:
            merged.append(article)
            continue

        merged_article = dict(article)
        merged_article["title_ko"] = translated.get("title_ko", merged_article.get("title_ko", ""))
        merged_article["summary_ko"] = translated.get("summary_ko", merged_article.get("summary_ko", ""))
        merged.append(merged_article)
    return merged


def translate_articles(max_batch: int = 10) -> int:
    if not get_active_provider():
        return 0

    articles = safe_read_json(ARTICLES_PATH, [])
    untranslated = [
        article
        for article in articles
        if article.get("ai_processed")
        and article.get("is_primary", True)
        and not article.get("title_ko")
        and _is_english(article.get("title", ""))
    ]

    if not untranslated:
        return 0

    batch = untranslated[:max_batch]
    prompt_items = [
        {
            "id": article["id"],
            "title": article.get("title", ""),
            "summary": article.get("summary_text", "")[:200],
        }
        for article in batch
    ]
    prompt = f"Translate these AI news items into Korean:\n\n{json.dumps(prompt_items, ensure_ascii=False)}"

    try:
        response_text = call_gemini(prompt, use_flash=True)
        cleaned = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        parsed = json.loads(cleaned)
    except Exception as e:
        log(f"[translate:error] {e}")
        return 0

    if not isinstance(parsed, list):
        return 0

    translations = {
        item["id"]: item
        for item in parsed
        if isinstance(item, dict) and item.get("id")
    }
    if not translations:
        return 0

    safe_update_json(
        ARTICLES_PATH,
        lambda current: _merge_translations(current, translations),
        default=articles,
    )
    log(f"[translate:done] translated={len(translations)}")
    return len(translations)


def _is_english(text: str) -> bool:
    if not text:
        return False
    ascii_count = sum(1 for char in text if char.isascii())
    return ascii_count / max(len(text), 1) > 0.7


def get_translation_stats() -> dict:
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [article for article in articles if article.get("ai_processed") and article.get("is_primary", True)]
    english = [article for article in processed if _is_english(article.get("title", ""))]
    translated = [article for article in english if article.get("title_ko")]

    return {
        "total": len(processed),
        "english": len(english),
        "translated": len(translated),
        "untranslated": len(english) - len(translated),
    }
