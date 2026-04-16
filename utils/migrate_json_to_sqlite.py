"""
utils/migrate_json_to_sqlite.py — JSON → SQLite 1회성 마이그레이션
실행: .venv/Scripts/python -m utils.migrate_json_to_sqlite
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DATA_DIR
from db.database import (
    init_db,
    upsert_articles,
    upsert_source,
    upsert_briefing,
    add_watchlist_keyword,
    add_bookmark,
    mark_alerted,
    upsert_weekly_report,
)
from utils.helpers import safe_read_json, now_iso


def _load(filename: str, default=None):
    path = DATA_DIR / filename
    return safe_read_json(path, default if default is not None else [])


def migrate():
    print("🗄️  AI News Radar JSON → SQLite 마이그레이션 시작")
    init_db()

    # 1. articles.json
    articles = _load("articles.json")
    if articles:
        count = upsert_articles(articles)
        print(f"  ✅ articles: {len(articles)}개 로드, {count}개 신규 삽입")
    else:
        print("  ⚠️  articles.json 없음 — 건너뜀")

    # 2. sources.json
    sources = _load("sources.json")
    for s in sources:
        upsert_source(s)
    print(f"  ✅ sources: {len(sources)}개 삽입")

    # 3. briefings.json
    briefings = _load("briefings.json")
    for b in briefings:
        upsert_briefing(b)
    print(f"  ✅ briefings: {len(briefings)}개 삽입")

    # 4. watchlist.json
    watchlist = _load("watchlist.json")
    for w in watchlist:
        add_watchlist_keyword(w.get("keyword", ""), w.get("created_at", now_iso()))
    print(f"  ✅ watchlist: {len(watchlist)}개 삽입")

    # 5. bookmarks.json
    bookmarks = _load("bookmarks.json")
    for bm in bookmarks:
        add_bookmark(
            bm.get("article_id", ""),
            bm.get("memo", ""),
            bm.get("created_at", now_iso()),
        )
    print(f"  ✅ bookmarks: {len(bookmarks)}개 삽입")

    # 6. alert_log.json
    alert_log = _load("alert_log.json")
    ts = now_iso()
    for article_id in alert_log:
        if isinstance(article_id, str):
            mark_alerted(article_id, ts)
    print(f"  ✅ alert_log: {len(alert_log)}개 삽입")

    # 7. weekly_reports.json
    reports = _load("weekly_reports.json")
    for r in reports:
        upsert_weekly_report(r)
    print(f"  ✅ weekly_reports: {len(reports)}개 삽입")

    print(f"\n🎉 마이그레이션 완료! radar.db 생성됨")
    print(f"   경로: {DATA_DIR / 'radar.db'}")


if __name__ == "__main__":
    migrate()
