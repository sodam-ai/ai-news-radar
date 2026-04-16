"""북마크 관리 — DB 기반

포맷: [{"article_id": "...", "memo": "", "created_at": "YYYY-MM-DD"}, ...]
텔레그램 봇 등 외부 모듈에서 북마크 읽기/쓰기용.
"""
from db.database import (
    get_bookmarks as _get_bookmarks,
    get_bookmark_ids as _get_bookmark_ids,
    add_bookmark as _add_bookmark,
    remove_bookmark as _remove_bookmark,
    update_bookmark_memo as _update_bookmark_memo,
)
from utils.helpers import today_str


def get_bookmarks() -> list[dict]:
    """북마크 목록 반환"""
    return _get_bookmarks()


def get_bookmark_ids() -> set[str]:
    """북마크된 article_id set 반환"""
    return _get_bookmark_ids()


def is_bookmarked(article_id: str) -> bool:
    """해당 기사가 북마크되어 있는지 확인"""
    return article_id in get_bookmark_ids()


def add_bookmark(article_id: str, memo: str = "") -> bool:
    """북마크 추가. 중복 시 False 반환."""
    return _add_bookmark(article_id, memo, today_str())


def remove_bookmark(article_id: str) -> None:
    """북마크 제거."""
    _remove_bookmark(article_id)


def update_memo(article_id: str, memo: str) -> None:
    """북마크 메모 수정."""
    _update_bookmark_memo(article_id, memo)
