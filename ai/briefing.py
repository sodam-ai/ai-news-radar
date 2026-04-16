"""Daily briefing generation."""
import json

from ai.model_router import call_gemini
from config import CATEGORIES, DATA_DIR
from utils.helpers import log, now_iso, safe_read_json, safe_update_json, today_str

ARTICLES_PATH = DATA_DIR / "articles.json"
BRIEFINGS_PATH = DATA_DIR / "briefings.json"

FOCUS_AREAS = {
    "ai_image_video": {
        "name": "AI Image/Video",
        "icon": "IV",
        "keywords": [
            "midjourney", "stable diffusion", "dall-e", "flux", "sora",
            "runway", "kling", "pika", "comfyui", "lora",
            "text-to-image", "text-to-video",
        ],
        "top_count": 3,
    },
    "ai_coding": {
        "name": "AI Coding",
        "icon": "CD",
        "keywords": [
            "claude code", "cursor", "copilot", "v0", "bolt", "windsurf",
            "devin", "vibe coding", "ai coding", "agentic",
        ],
        "top_count": 3,
    },
    "ai_ontology": {
        "name": "Ontology/Knowledge Graph",
        "icon": "KG",
        "keywords": [
            "ontology", "knowledge graph", "neo4j", "rdf", "owl",
            "semantic web", "graph database",
        ],
        "top_count": 3,
    },
}


def _select_today_articles(articles: list[dict], today: str) -> list[dict]:
    selected = [
        article
        for article in articles
        if article.get("ai_processed")
        and article.get("is_primary", True)
        and article.get("crawled_at", "").startswith(today)
    ]
    if selected:
        return selected

    fallback = [
        article
        for article in articles
        if article.get("ai_processed") and article.get("is_primary", True)
    ]
    fallback.sort(key=lambda item: item.get("crawled_at", ""), reverse=True)
    return fallback[:20]


def _extract_briefing_result(result) -> tuple[list[dict], str]:
    top_articles: list[dict] = []
    summary = ""

    if isinstance(result, list):
        top_articles = result
    elif isinstance(result, dict):
        for key in ("top_articles", "top_5_news", "top_news", "articles", "top5", "news"):
            if isinstance(result.get(key), list):
                top_articles = result[key]
                break

        if not top_articles:
            for value in result.values():
                if isinstance(value, list) and value and isinstance(value[0], dict):
                    top_articles = value
                    break

        for key in ("overall_summary", "summary", "overall"):
            if isinstance(result.get(key), str):
                summary = result[key]
                break

    return top_articles, summary


def _store_briefing(briefing: dict):
    briefing_date = briefing["date"]

    def updater(current: list[dict]):
        retained = [item for item in current if item.get("date") != briefing_date]
        retained.append(briefing)
        return retained

    safe_update_json(BRIEFINGS_PATH, updater, default=[])


def generate_daily_briefing() -> dict | None:
    articles = safe_read_json(ARTICLES_PATH, [])
    today = today_str()
    today_articles = _select_today_articles(articles, today)
    if not today_articles:
        return None

    today_articles.sort(key=lambda item: item.get("importance", 0), reverse=True)
    top_candidates = today_articles[:20]
    prompt_items = []
    for article in top_candidates:
        prompt_items.append(
            f"[ID: {article['id']}] "
            f"importance={article.get('importance', 3)} "
            f"sentiment={article.get('sentiment', 'neutral')} | "
            f"{article['title']}\n"
            f"summary: {article.get('summary_text', article.get('content', '')[:200])}"
        )

    prompt = (
        f"Create a top-5 AI news daily briefing for {today}. "
        "Return JSON only with overall_summary and top_articles.\n\n"
        + "\n\n".join(prompt_items)
    )

    try:
        response_text = call_gemini(prompt, use_flash=True)
        cleaned = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        result = json.loads(cleaned)
    except Exception as e:
        log(f"[briefing:error] {e}")
        return None

    top_articles, summary = _extract_briefing_result(result)
    briefing = {
        "id": f"brf_{today.replace('-', '')}",
        "date": today,
        "top_articles": top_articles,
        "summary": summary,
        "created_at": now_iso(),
    }
    briefing["focus_briefings"] = _generate_focus_briefings(today_articles)
    _store_briefing(briefing)

    log(f"[briefing:done] date={today} focus_groups={len(briefing['focus_briefings'])}")
    return briefing


def _generate_focus_briefings(all_articles: list[dict]) -> dict:
    focus_results = {}
    for area_id, area_info in FOCUS_AREAS.items():
        matched = []
        for article in all_articles:
            score = 0
            if article.get("category") == area_id:
                score += 10

            haystack = (
                f"{article.get('title', '')} "
                f"{' '.join(article.get('tags', []))} "
                f"{article.get('summary_text', '')}"
            ).lower()
            for keyword in area_info["keywords"]:
                if keyword.lower() in haystack:
                    score += 3 if keyword.lower() in article.get("title", "").lower() else 1

            if score > 0:
                matched.append({"score": score, "article": article})

        matched.sort(key=lambda item: (-item["score"], -item["article"].get("importance", 0)))
        top_n = matched[:area_info["top_count"]]
        focus_results[area_id] = {
            "name": area_info["name"],
            "icon": area_info["icon"],
            "total_count": len(matched),
            "top_articles": [
                {
                    "title": item["article"]["title"],
                    "url": item["article"]["url"],
                    "summary": item["article"].get("summary_text", ""),
                    "importance": item["article"].get("importance", 0),
                    "sentiment": item["article"].get("sentiment", "neutral"),
                    "score": item["score"],
                }
                for item in top_n
            ],
        }

    return focus_results


def get_focus_areas() -> dict:
    return FOCUS_AREAS
