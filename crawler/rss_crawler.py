"""RSS ë‰´ìŠ¤ ìˆ˜ì§‘."""
import feedparser
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from time import mktime

from config import DATA_DIR, MAX_ARTICLES_PER_SOURCE
from utils.helpers import generate_id, log, now_iso, safe_read_json, safe_update_json, safe_write_json

SOURCES_PATH = DATA_DIR / "sources.json"
ARTICLES_PATH = DATA_DIR / "articles.json"
MAX_WORKERS = 15
REQUEST_HEADERS = {"User-Agent": "AI-News-Radar/1.0"}


def load_sources() -> list[dict]:
    sources = safe_read_json(SOURCES_PATH, [])
    if not sources:
        preset = safe_read_json(DATA_DIR / "preset_sources.json", [])
        for source in preset:
            source["last_crawled_at"] = None
            source["created_at"] = now_iso()
        safe_write_json(SOURCES_PATH, preset)
        return preset
    return sources


def parse_published(entry) -> str:
    for attr in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, attr, None)
        if parsed:
            dt = datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
            return dt.isoformat()
    return now_iso()


def _crawl_single(source: dict, existing_urls: set[str]) -> tuple[dict, list[dict]]:
    """단일 소스 수집 후 갱신된 source metadata 와 신규 기사 목록을 반환."""
    if not source.get("is_active", True):
        return source, []

    try:
        feed = feedparser.parse(source["url"], request_headers=REQUEST_HEADERS)
    except Exception as e:
        log(f"[crawl:error] {source['name']}: {e}")
        return source, []

    source["last_crawled_at"] = now_iso()
    new_articles: list[dict] = []
    for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
        url = getattr(entry, "link", "")
        if not url or url in existing_urls:
            continue

        title = getattr(entry, "title", "Untitled")
        content = ""
        if hasattr(entry, "summary"):
            content = entry.summary
        elif hasattr(entry, "content"):
            content = entry.content[0].value if entry.content else ""

        image_urls = []
        if hasattr(entry, "media_content"):
            for media in entry.media_content:
                media_url = media.get("url", "")
                if media.get("medium") == "image" or media_url.endswith((".jpg", ".png", ".webp")):
                    image_urls.append(media_url)

        new_articles.append(
            {
                "id": generate_id("art"),
                "source_id": source["id"],
                "title": title,
                "url": url,
                "content": content[:5000],
                "category": "",
                "importance": 0,
                "sentiment": "",
                "sentiment_reason": "",
                "tags": [],
                "image_urls": image_urls,
                "image_analysis": "",
                "cluster_id": "",
                "is_primary": True,
                "related_articles": [],
                "published_at": parse_published(entry),
                "crawled_at": now_iso(),
                "is_read": False,
                "ai_processed": False,
            }
        )

    return source, new_articles


def _merge_articles(current: list[dict], new_articles: list[dict]) -> list[dict]:
    by_url = {article["url"]: article for article in current if article.get("url")}
    for article in new_articles:
        by_url.setdefault(article["url"], article)
    return list(by_url.values())


def _merge_sources(current: list[dict], updated_sources: list[dict]) -> list[dict]:
    updated_by_id = {source["id"]: source for source in updated_sources if source.get("id")}
    merged = []
    seen_ids = set()

    for source in current:
        source_id = source.get("id")
        latest = updated_by_id.get(source_id)
        if latest:
            merged.append({**source, **latest})
            seen_ids.add(source_id)
        else:
            merged.append(source)

    for source_id, source in updated_by_id.items():
        if source_id not in seen_ids:
            merged.append(source)

    return merged


def crawl_all() -> int:
    """모든 활성 소스를 수집하고 신규 기사 수를 반환."""
    sources = load_sources()
    existing = safe_read_json(ARTICLES_PATH, [])
    existing_urls = {article["url"] for article in existing if article.get("url")}

    total_new = 0
    aggregated_new_articles: list[dict] = []
    active_sources = [source for source in sources if source.get("is_active", True)]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(_crawl_single, source, existing_urls): source
            for source in active_sources
        }

        for future in as_completed(futures):
            try:
                _, new_articles = future.result()
                if new_articles:
                    aggregated_new_articles.extend(new_articles)
                    for article in new_articles:
                        existing_urls.add(article["url"])
                    total_new += len(new_articles)
            except Exception as e:
                log(f"[crawl:error] {e}")

    if aggregated_new_articles:
        safe_update_json(
            ARTICLES_PATH,
            lambda current: _merge_articles(current, aggregated_new_articles),
            default=[],
        )

    safe_update_json(
        SOURCES_PATH,
        lambda current: _merge_sources(current, sources),
        default=sources,
    )

    log(f"[crawl:done] sources={len(active_sources)} new_articles={total_new}")
    return total_new


def crawl_source(source: dict) -> list[dict]:
    existing_urls = {article["url"] for article in safe_read_json(ARTICLES_PATH, []) if article.get("url")}
    _, articles = _crawl_single(source, existing_urls)
    return articles
