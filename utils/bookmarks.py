"""북마크 관리 — app.py와 동일한 포맷 사용

포맷: [{"article_id": "...", "memo": "", "created_at": "YYYY-MM-DD"}, ...]
텔레그램 봇 등 외부 모듈에서 북마크 읽기용으로 사용.
"""
from config import DATA_DIR
from utils.helpers import safe_read_json, safe_write_json, today_str

BOOKMARKS_PATH = DATA_DIR / "bookmarks.json"


def get_bookmarks() -> list[dict]:
    """북마크 목록 반환 (앱과 동일한 포맷)"""
    return safe_read_json(BOOKMARKS_PATH, [])


def get_bookmark_ids() -> set[str]:
    """북마크된 article_id set 반환"""
    return {b["article_id"] for b in get_bookmarks() if b.get("article_id")}


def is_bookmarked(article_id: str) -> bool:
    """해당 기사가 북마크되어 있는지 확인"""
    return article_id in get_bookmark_ids()
