"""RSS 뉴스 수집."""
import feedparser
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from time import mktime

from config import DATA_DIR, MAX_ARTICLES_PER_SOURCE
from db.database import (
    init_db,
    get_sources,
    upsert_source,
    upsert_articles,
    update_source_crawled,
    get_connection,
)
from utils.helpers import generate_id, log, now_iso, safe_read_json

MAX_WORKERS = 15
REQUEST_HEADERS = {"User-Agent": "AI-News-Radar/1.0"}


def load_sources() -> list[dict]:
    """소스 목록 반환 — DB 우선, 없으면 preset_sources.json으로 초기화"""
    init_db()
    sources = get_sources()
    if not sources:
        preset = safe_read_json(DATA_DIR / "preset_sources.json", [])
        for source in preset:
            source.setdefault("last_crawled_at", None)
            source.setdefault("created_at", now_iso())
            upsert_source(source)
        sources = get_sources()
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


def crawl_all() -> int:
    """모든 활성 소스를 수집하고 신규 기사 수를 반환."""
    sources = load_sources()

    # DB에서 기존 URL 조회 (중복 방지) — JSON 5MB 파싱 불필요
    conn = get_connection()
    existing_urls: set[str] = {
        r[0] for r in conn.execute("SELECT url FROM articles WHERE url != ''").fetchall()
    }

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
                updated_src, new_articles = future.result()
                if new_articles:
                    aggregated_new_articles.extend(new_articles)
                    for article in new_articles:
                        existing_urls.add(article["url"])
                    total_new += len(new_articles)
                # 소스 마지막 수집 시각 업데이트
                if updated_src.get("last_crawled_at"):
                    update_source_crawled(updated_src["id"], updated_src["last_crawled_at"])
            except Exception as e:
                log(f"[crawl:error] {e}")

    if aggregated_new_articles:
        upsert_articles(aggregated_new_articles)

    log(f"[crawl:done] sources={len(active_sources)} new_articles={total_new}")
    return total_new


def crawl_source(source: dict) -> list[dict]:
    """단일 소스 수집 (앱 UI에서 수동 수집 시 호출)"""
    conn = get_connection()
    existing_urls: set[str] = {
        r[0] for r in conn.execute("SELECT url FROM articles WHERE url != ''").fetchall()
    }
    updated_src, new_articles = _crawl_single(source, existing_urls)
    if new_articles:
        upsert_articles(new_articles)
    if updated_src.get("last_crawled_at"):
        update_source_crawled(updated_src["id"], updated_src["last_crawled_at"])
    return new_articles
