"""RSS 피드 수집"""
import ssl
import urllib.request
import feedparser
from datetime import datetime, timezone
from time import mktime

from config import DATA_DIR, MAX_ARTICLES_PER_SOURCE
from utils.helpers import generate_id, now_iso, safe_read_json, safe_write_json, log

SOURCES_PATH = DATA_DIR / "sources.json"
ARTICLES_PATH = DATA_DIR / "articles.json"


def load_sources() -> list[dict]:
    sources = safe_read_json(SOURCES_PATH, [])
    if not sources:
        preset = safe_read_json(DATA_DIR / "preset_sources.json", [])
        for s in preset:
            s["last_crawled_at"] = None
            s["created_at"] = now_iso()
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


def crawl_source(source: dict) -> list[dict]:
    """단일 소스에서 새 글을 수집하여 Article 객체 리스트로 반환"""
    if not source.get("is_active", True):
        return []

    try:
        # SSL 인증서 검증 실패하는 사이트(arXiv 등) 대응
        if "arxiv.org" in source["url"]:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            handlers = [urllib.request.HTTPSHandler(context=ctx)]
            feed = feedparser.parse(source["url"], handlers=handlers)
        else:
            feed = feedparser.parse(source["url"])
    except Exception as e:
        log(f"[크롤링 실패] {source['name']}: {e}")
        return []

    existing_articles = safe_read_json(ARTICLES_PATH, [])
    existing_urls = {a["url"] for a in existing_articles}

    new_articles = []
    for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
        url = getattr(entry, "link", "")
        if not url or url in existing_urls:
            continue

        title = getattr(entry, "title", "제목 없음")
        content = ""
        if hasattr(entry, "summary"):
            content = entry.summary
        elif hasattr(entry, "content"):
            content = entry.content[0].value if entry.content else ""

        # 이미지 URL 추출
        image_urls = []
        if hasattr(entry, "media_content"):
            for media in entry.media_content:
                if media.get("medium") == "image" or media.get("url", "").endswith((".jpg", ".png", ".webp")):
                    image_urls.append(media["url"])

        article = {
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
        new_articles.append(article)

    return new_articles


def crawl_all() -> int:
    """모든 활성 소스를 수집하고 articles.json에 저장. 새 글 수 반환."""
    sources = load_sources()
    existing = safe_read_json(ARTICLES_PATH, [])
    total_new = 0

    for source in sources:
        new_articles = crawl_source(source)
        if new_articles:
            existing.extend(new_articles)
            total_new += len(new_articles)
            source["last_crawled_at"] = now_iso()

    if total_new > 0:
        safe_write_json(ARTICLES_PATH, existing)
        safe_write_json(SOURCES_PATH, sources)

    log(f"[크롤링 완료] 새 글 {total_new}개 수집")
    return total_new
