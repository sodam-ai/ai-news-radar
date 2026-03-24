"""AI 도구 릴리즈 추적 — 버전 업데이트/출시 자동 감지 + 알림

수집된 뉴스에서 릴리즈/업데이트/출시 관련 키워드를 감지하여
사용자가 추적하는 도구의 새 버전 소식을 빠르게 알려줍니다.
"""
from config import DATA_DIR
from utils.helpers import safe_read_json, safe_write_json, now_iso, log

ARTICLES_PATH = DATA_DIR / "articles.json"
RELEASE_LOG_PATH = DATA_DIR / "release_log.json"

# 릴리즈 감지 키워드
RELEASE_KEYWORDS = [
    "released", "launches", "launched", "announces", "announced",
    "introduces", "introduced", "unveils", "unveiled", "rolls out",
    "now available", "general availability", "public beta", "open beta",
    "version", "v2", "v3", "v4", "v5", "v6",
    "update", "upgrade", "new feature",
    "출시", "발표", "공개", "업데이트", "릴리즈", "베타",
    "새로운 버전", "새 기능", "정식 출시",
]

# 추적 대상 도구 (사용자 관심 분야 기반)
TRACKED_TOOLS = {
    # 이미지/영상
    "midjourney": {"name": "Midjourney", "icon": "🎨", "keywords": ["midjourney"]},
    "stable_diffusion": {"name": "Stable Diffusion", "icon": "🎨", "keywords": ["stable diffusion", "stability ai", "sdxl", "sd3", "sd 3"]},
    "flux": {"name": "Flux", "icon": "🎨", "keywords": ["flux", "black forest"]},
    "sora": {"name": "Sora", "icon": "🎬", "keywords": ["sora"]},
    "runway": {"name": "Runway", "icon": "🎬", "keywords": ["runway", "gen-3", "gen-4"]},
    "kling": {"name": "Kling", "icon": "🎬", "keywords": ["kling"]},
    "comfyui": {"name": "ComfyUI", "icon": "🖼️", "keywords": ["comfyui", "comfy ui"]},
    "dalle": {"name": "DALL-E", "icon": "🎨", "keywords": ["dall-e", "dalle"]},
    # 바이브코딩
    "claude_code": {"name": "Claude Code", "icon": "💻", "keywords": ["claude code"]},
    "cursor": {"name": "Cursor", "icon": "💻", "keywords": ["cursor"]},
    "copilot": {"name": "GitHub Copilot", "icon": "💻", "keywords": ["copilot"]},
    "v0": {"name": "v0", "icon": "💻", "keywords": ["v0.dev", "v0 by vercel"]},
    "windsurf": {"name": "Windsurf", "icon": "💻", "keywords": ["windsurf", "codeium"]},
    "devin": {"name": "Devin", "icon": "💻", "keywords": ["devin"]},
    "bolt": {"name": "Bolt", "icon": "💻", "keywords": ["bolt.new"]},
    # 온톨로지
    "neo4j": {"name": "Neo4j", "icon": "🔮", "keywords": ["neo4j"]},
    # LLM 플랫폼
    "openai": {"name": "OpenAI", "icon": "🤖", "keywords": ["openai", "gpt-5", "gpt-4", "chatgpt"]},
    "anthropic": {"name": "Anthropic", "icon": "🤖", "keywords": ["anthropic", "claude"]},
    "google_ai": {"name": "Google AI", "icon": "🤖", "keywords": ["gemini", "google ai"]},
}


def detect_releases(articles: list[dict] = None) -> list[dict]:
    """수집된 기사에서 릴리즈/업데이트 소식 감지.

    Returns:
        [{"tool_id", "tool_name", "tool_icon", "article_title", "article_url", "detected_at"}, ...]
    """
    if articles is None:
        articles = safe_read_json(ARTICLES_PATH, [])

    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    # 이미 감지한 기사 ID
    release_log = safe_read_json(RELEASE_LOG_PATH, [])
    logged_ids = {r.get("article_id") for r in release_log}

    new_releases = []

    for article in processed:
        if article.get("id") in logged_ids:
            continue

        title = article.get("title", "").lower()
        summary = article.get("summary_text", "").lower()
        text = f"{title} {summary}"

        # 릴리즈 키워드 매칭
        has_release_keyword = any(rk in text for rk in RELEASE_KEYWORDS)
        if not has_release_keyword:
            continue

        # 추적 도구 매칭
        for tool_id, tool_info in TRACKED_TOOLS.items():
            tool_matched = any(tk.lower() in text for tk in tool_info["keywords"])
            if tool_matched:
                release_entry = {
                    "tool_id": tool_id,
                    "tool_name": tool_info["name"],
                    "tool_icon": tool_info["icon"],
                    "article_id": article.get("id"),
                    "article_title": article.get("title", ""),
                    "article_url": article.get("url", ""),
                    "importance": article.get("importance", 0),
                    "detected_at": now_iso(),
                }
                new_releases.append(release_entry)
                release_log.append(release_entry)

    # 저장 (최근 200개만 유지)
    if new_releases:
        if len(release_log) > 200:
            release_log = release_log[-200:]
        safe_write_json(RELEASE_LOG_PATH, release_log)
        log(f"[릴리즈 추적] {len(new_releases)}건 감지")

    return new_releases


def get_release_history(limit: int = 20) -> list[dict]:
    """최근 릴리즈 히스토리"""
    log_data = safe_read_json(RELEASE_LOG_PATH, [])
    return list(reversed(log_data[-limit:]))


def get_tracked_tools() -> dict:
    """추적 중인 도구 목록"""
    return TRACKED_TOOLS
