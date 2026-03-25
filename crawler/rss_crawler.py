"""RSS 피드 수집 (병렬 처리)"""
import ssl
import urllib.request
import feedparser
from datetime import datetime, timezone
from time import mktime
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import DATA_DIR, MAX_ARTICLES_PER_SOURCE
from utils.helpers import generate_id, now_iso, safe_read_json, safe_write_json, log

SOURCES_PATH = DATA_DIR / "sources.json"
ARTICLES_PATH = DATA_DIR / "articles.json"

# 병렬 크롤링 동시 작업 수 (네트워크 I/O 대기이므로 높여도 됨)
MAX_WORKERS = 15


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


# SSL 컨텍스트 캐싱 (재생성 방지)
_SSL_CTX = None


def _get_ssl_ctx():
    global _SSL_CTX
    if _SSL_CTX is None:
        _SSL_CTX = ssl.create_default_context()
        _SSL_CTX.check_hostname = False
        _SSL_CTX.verify_mode = ssl.CERT_NONE
    return _SSL_CTX


def _crawl_single(source: dict, existing_urls: set) -> tuple[dict, list[dict]]:
    """단일 소스 크롤링 (병렬 실행용). (source, new_articles) 반환."""
    if not source.get("is_active", True):
        return source, []

    try:
        if "arxiv.org" in source["url"]:
            handlers = [urllib.request.HTTPSHandler(context=_get_ssl_ctx())]
            feed = feedparser.parse(source["url"], handlers=handlers)
        else:
            feed = feedparser.parse(source["url"], request_headers={"User-Agent": "AI-News-Radar/1.0"})
    except Exception as e:
        log(f"[크롤링 실패] {source['name']}: {e}")
        return source, []

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

    if new_articles:
        source["last_crawled_at"] = now_iso()

    return source, new_articles


def crawl_all() -> int:
    """모든 활성 소스를 병렬 수집. 새 글 수 반환."""
    sources = load_sources()
    existing = safe_read_json(ARTICLES_PATH, [])
    existing_urls = {a["url"] for a in existing}

    total_new = 0
    active_sources = [s for s in sources if s.get("is_active", True)]

    # 병렬 크롤링
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(_crawl_single, source, existing_urls): source
            for source in active_sources
        }

        for future in as_completed(futures):
            try:
                source, new_articles = future.result()
                if new_articles:
                    existing.extend(new_articles)
                    # existing_urls도 업데이트 (중복 방지)
                    for a in new_articles:
                        existing_urls.add(a["url"])
                    total_new += len(new_articles)
            except Exception as e:
                log(f"[크롤링 오류] {e}")

    if total_new > 0:
        safe_write_json(ARTICLES_PATH, existing)
        safe_write_json(SOURCES_PATH, sources)

    log(f"[크롤링 완료] {len(active_sources)}개 소스 병렬 수집 → 새 글 {total_new}개")
    return total_new


# 하위 호환: 단일 소스 크롤링 (테스트용)
def crawl_source(source: dict) -> list[dict]:
    existing_urls = {a["url"] for a in safe_read_json(ARTICLES_PATH, [])}
    _, articles = _crawl_single(source, existing_urls)
    return articles
