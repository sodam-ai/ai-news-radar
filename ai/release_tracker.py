"""Detect tool and model release announcements from processed articles."""

from config import DATA_DIR
from utils.helpers import log, now_iso, safe_read_json, safe_update_json

ARTICLES_PATH = DATA_DIR / "articles.json"
RELEASE_LOG_PATH = DATA_DIR / "release_log.json"

RELEASE_KEYWORDS = [
    "released",
    "launches",
    "launched",
    "announces",
    "announced",
    "introduces",
    "introduced",
    "unveils",
    "unveiled",
    "rolls out",
    "now available",
    "general availability",
    "public beta",
    "open beta",
    "version",
    "v2",
    "v3",
    "v4",
    "v5",
    "v6",
    "update",
    "upgrade",
    "new feature",
]

TRACKED_TOOLS = {
    "midjourney": {"name": "Midjourney", "icon": "IV", "keywords": ["midjourney"]},
    "stable_diffusion": {
        "name": "Stable Diffusion",
        "icon": "IV",
        "keywords": ["stable diffusion", "stability ai", "sdxl", "sd3", "sd 3"],
    },
    "flux": {"name": "Flux", "icon": "IV", "keywords": ["flux", "black forest"]},
    "sora": {"name": "Sora", "icon": "IV", "keywords": ["sora"]},
    "runway": {"name": "Runway", "icon": "IV", "keywords": ["runway", "gen-3", "gen-4"]},
    "kling": {"name": "Kling", "icon": "IV", "keywords": ["kling"]},
    "comfyui": {"name": "ComfyUI", "icon": "IV", "keywords": ["comfyui", "comfy ui"]},
    "dalle": {"name": "DALL-E", "icon": "IV", "keywords": ["dall-e", "dalle"]},
    "claude_code": {"name": "Claude Code", "icon": "CD", "keywords": ["claude code"]},
    "cursor": {"name": "Cursor", "icon": "CD", "keywords": ["cursor"]},
    "copilot": {"name": "GitHub Copilot", "icon": "CD", "keywords": ["copilot"]},
    "v0": {"name": "v0", "icon": "CD", "keywords": ["v0.dev", "v0 by vercel"]},
    "windsurf": {"name": "Windsurf", "icon": "CD", "keywords": ["windsurf", "codeium"]},
    "devin": {"name": "Devin", "icon": "CD", "keywords": ["devin"]},
    "bolt": {"name": "Bolt", "icon": "CD", "keywords": ["bolt.new"]},
    "neo4j": {"name": "Neo4j", "icon": "KG", "keywords": ["neo4j"]},
    "openai": {"name": "OpenAI", "icon": "LLM", "keywords": ["openai", "gpt-5", "gpt-4", "chatgpt"]},
    "anthropic": {"name": "Anthropic", "icon": "LLM", "keywords": ["anthropic", "claude"]},
    "google_ai": {"name": "Google AI", "icon": "LLM", "keywords": ["gemini", "google ai"]},
}

MAX_RELEASE_LOG_ENTRIES = 200


def detect_releases(articles: list[dict] = None) -> list[dict]:
    """Return newly detected release announcements."""
    if articles is None:
        articles = safe_read_json(ARTICLES_PATH, [])

    processed = [item for item in articles if item.get("ai_processed") and item.get("is_primary", True)]

    release_log = safe_read_json(RELEASE_LOG_PATH, [])
    logged_ids = {entry.get("article_id") for entry in release_log}
    new_releases = []

    for article in processed:
        article_id = article.get("id")
        if not article_id or article_id in logged_ids:
            continue

        text = f"{article.get('title', '')} {article.get('summary_text', '')}".lower()
        if not any(keyword in text for keyword in RELEASE_KEYWORDS):
            continue

        for tool_id, tool_info in TRACKED_TOOLS.items():
            if not any(keyword.lower() in text for keyword in tool_info["keywords"]):
                continue

            release_entry = {
                "tool_id": tool_id,
                "tool_name": tool_info["name"],
                "tool_icon": tool_info["icon"],
                "article_id": article_id,
                "article_title": article.get("title", ""),
                "article_url": article.get("url", ""),
                "importance": article.get("importance", 0),
                "detected_at": now_iso(),
            }
            new_releases.append(release_entry)
            logged_ids.add(article_id)
            break

    if new_releases:
        def updater(current: list[dict]):
            by_article_id = {
                entry.get("article_id"): entry
                for entry in current
                if entry.get("article_id")
            }
            for entry in new_releases:
                by_article_id[entry["article_id"]] = entry

            merged = list(by_article_id.values())
            merged.sort(key=lambda item: item.get("detected_at", ""))
            if len(merged) > MAX_RELEASE_LOG_ENTRIES:
                merged = merged[-MAX_RELEASE_LOG_ENTRIES:]
            return merged

        safe_update_json(RELEASE_LOG_PATH, updater, default=[])
        log(f"[release-tracker] detected={len(new_releases)}")

    return new_releases


def get_release_history(limit: int = 20) -> list[dict]:
    log_data = safe_read_json(RELEASE_LOG_PATH, [])
    return list(reversed(log_data[-limit:]))


def get_tracked_tools() -> dict:
    return TRACKED_TOOLS
