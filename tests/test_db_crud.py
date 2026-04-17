"""db/database.py — SQLite CRUD 계약 회귀 테스트.

목적:
- 공개 함수의 기본 계약(입력/반환/부작용) 고정
- 빈 입력·최대 길이·충돌·JSON 역직렬화 경계값 검증
- 실제 네트워크 미의존, 임시 DB만 사용
"""
from __future__ import annotations

from db import database as db


class TestArticles:
    def test_upsert_and_get_single(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        got = db.get_article_by_id(sample_article["id"])
        assert got is not None
        assert got["title"] == sample_article["title"]
        assert got["tags"] == ["ai", "research", "testing"]
        assert got["is_primary"] is True
        assert got["ai_processed"] is True

    def test_upsert_articles_batch(self, temp_db, sample_article):
        batch = [
            {**sample_article, "id": f"art_{i}", "url": f"https://ex.com/{i}"}
            for i in range(5)
        ]
        inserted = db.upsert_articles(batch)
        assert inserted == 5
        assert db.get_article_count() == 5

    def test_upsert_articles_empty_list(self, temp_db):
        """빈 리스트는 예외 없이 0 반환."""
        assert db.upsert_articles([]) == 0
        assert db.get_article_count() == 0

    def test_url_unique_conflict_updates(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        updated = {**sample_article, "title": "UPDATED TITLE", "ai_processed": True}
        db.upsert_article(updated)
        got = db.get_article_by_id(sample_article["id"])
        assert got["title"] == "UPDATED TITLE"
        assert db.get_article_count() == 1

    def test_get_article_by_invalid_id(self, temp_db):
        assert db.get_article_by_id("") is None
        assert db.get_article_by_id(None) is None
        assert db.get_article_by_id("x" * 100) is None
        assert db.get_article_by_id("nonexistent") is None

    def test_get_primary_articles_filters(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        secondary = {**sample_article, "id": "art_sec", "url": "https://ex.com/sec", "is_primary": False}
        db.upsert_article(secondary)
        unproc = {**sample_article, "id": "art_unp", "url": "https://ex.com/unp", "ai_processed": False}
        db.upsert_article(unproc)

        primaries = db.get_primary_articles()
        assert len(primaries) == 1
        assert primaries[0]["id"] == sample_article["id"]

    def test_get_unprocessed_articles(self, temp_db, sample_article):
        unproc = {**sample_article, "id": "art_u", "url": "https://ex.com/u", "ai_processed": False}
        db.upsert_article(sample_article)
        db.upsert_article(unproc)
        unprocessed = db.get_unprocessed_articles()
        assert len(unprocessed) == 1
        assert unprocessed[0]["id"] == "art_u"

    def test_update_article_fields_whitelist(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        db.update_article_fields(sample_article["id"], {"category": "ai_tool", "importance": 5})
        got = db.get_article_by_id(sample_article["id"])
        assert got["category"] == "ai_tool"
        assert got["importance"] == 5

    def test_update_article_fields_blocks_unknown(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        db.update_article_fields(sample_article["id"], {"url": "https://evil.com"})
        got = db.get_article_by_id(sample_article["id"])
        assert got["url"] == sample_article["url"]

    def test_update_article_fields_invalid_id(self, temp_db):
        db.update_article_fields("", {"category": "x"})
        db.update_article_fields("x" * 100, {"category": "x"})

    def test_counts(self, temp_db, sample_article):
        assert db.get_article_count() == 0
        assert db.get_processed_count() == 0
        db.upsert_article(sample_article)
        assert db.get_article_count() == 1
        assert db.get_processed_count() == 1


class TestSources:
    def test_upsert_and_get(self, temp_db, sample_source):
        db.upsert_source(sample_source)
        sources = db.get_sources()
        assert len(sources) == 1
        assert sources[0]["name"] == "Test RSS Feed"
        assert sources[0]["is_active"] is True

    def test_update_source_crawled(self, temp_db, sample_source):
        db.upsert_source(sample_source)
        db.update_source_crawled(sample_source["id"], "2026-04-17T01:00:00+00:00")
        sources = db.get_sources()
        assert sources[0]["last_crawled_at"] == "2026-04-17T01:00:00+00:00"


class TestWatchlist:
    def test_add_and_list(self, temp_db):
        assert db.add_watchlist_keyword("Claude", "2026-04-17T00:00:00+00:00") is True
        assert db.add_watchlist_keyword("Gemini", "2026-04-17T00:00:00+00:00") is True
        wl = db.get_watchlist()
        assert len(wl) == 2

    def test_duplicate_returns_false(self, temp_db):
        db.add_watchlist_keyword("Claude", "2026-04-17T00:00:00+00:00")
        assert db.add_watchlist_keyword("Claude", "2026-04-17T00:00:00+00:00") is False

    def test_empty_keyword_rejected(self, temp_db):
        assert db.add_watchlist_keyword("", "2026-04-17T00:00:00+00:00") is False
        assert db.add_watchlist_keyword("   ", "2026-04-17T00:00:00+00:00") is False

    def test_keyword_length_capped(self, temp_db):
        long_kw = "A" * 200
        db.add_watchlist_keyword(long_kw, "2026-04-17T00:00:00+00:00")
        wl = db.get_watchlist()
        assert len(wl[0]["keyword"]) <= 100

    def test_active_keywords_lowercase(self, temp_db):
        db.add_watchlist_keyword("Claude", "2026-04-17T00:00:00+00:00")
        db.add_watchlist_keyword("GPT", "2026-04-17T00:00:00+00:00")
        active = db.get_active_keywords()
        assert "claude" in active
        assert "gpt" in active

    def test_set_active(self, temp_db):
        db.add_watchlist_keyword("Claude", "2026-04-17T00:00:00+00:00")
        db.set_watchlist_active("Claude", False)
        assert "claude" not in db.get_active_keywords()


class TestBookmarks:
    def test_add_remove(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        assert db.add_bookmark(sample_article["id"], "좋은 기사", "2026-04-17T00:00:00+00:00") is True
        bookmarks = db.get_bookmarks()
        assert len(bookmarks) == 1
        assert bookmarks[0]["memo"] == "좋은 기사"

        db.remove_bookmark(sample_article["id"])
        assert len(db.get_bookmarks()) == 0

    def test_duplicate_bookmark_returns_false(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        db.add_bookmark(sample_article["id"], "first", "2026-04-17T00:00:00+00:00")
        assert db.add_bookmark(sample_article["id"], "dup", "2026-04-17T00:00:00+00:00") is False

    def test_invalid_article_id_rejected(self, temp_db):
        assert db.add_bookmark("", "m", "2026-04-17T00:00:00+00:00") is False
        assert db.add_bookmark("x" * 100, "m", "2026-04-17T00:00:00+00:00") is False

    def test_update_memo(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        db.add_bookmark(sample_article["id"], "initial", "2026-04-17T00:00:00+00:00")
        db.update_bookmark_memo(sample_article["id"], "updated")
        bms = db.get_bookmarks()
        assert bms[0]["memo"] == "updated"

    def test_memo_length_capped(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        db.add_bookmark(sample_article["id"], "x" * 1000, "2026-04-17T00:00:00+00:00")
        bms = db.get_bookmarks()
        assert len(bms[0]["memo"]) <= 500

    def test_bookmark_ids(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        db.add_bookmark(sample_article["id"], "", "2026-04-17T00:00:00+00:00")
        ids = db.get_bookmark_ids()
        assert sample_article["id"] in ids


class TestAlertLog:
    def test_mark_and_get(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        db.mark_alerted(sample_article["id"], "2026-04-17T00:00:00+00:00")
        log = db.get_alert_log()
        assert sample_article["id"] in log

    def test_duplicate_mark_no_error(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        db.mark_alerted(sample_article["id"], "2026-04-17T00:00:00+00:00")
        db.mark_alerted(sample_article["id"], "2026-04-17T01:00:00+00:00")
        log = db.get_alert_log()
        assert log.count(sample_article["id"]) == 1


class TestBriefings:
    def test_upsert_and_get(self, temp_db):
        briefing = {
            "id": "brief_001",
            "date": "2026-04-17",
            "summary": "오늘의 AI 뉴스 요약",
            "top_articles": ["art_1", "art_2"],
            "focus_briefings": {"research": "연구 요약"},
            "created_at": "2026-04-17T00:00:00+00:00",
        }
        db.upsert_briefing(briefing)
        briefings = db.get_briefings()
        assert len(briefings) == 1
        assert briefings[0]["top_articles"] == ["art_1", "art_2"]
        assert briefings[0]["focus_briefings"] == {"research": "연구 요약"}


class TestWeeklyReports:
    def test_upsert_and_get(self, temp_db):
        report = {
            "id": "wk_001",
            "week": "2026-W16",
            "period": "2026-04-13 ~ 2026-04-19",
            "title": "주간 AI 뉴스",
            "summary": "주간 요약",
            "key_themes": ["LLM", "RAG"],
            "top_stories": [{"id": "art_1", "title": "X"}],
            "created_at": "2026-04-17T00:00:00+00:00",
        }
        db.upsert_weekly_report(report)
        reports = db.get_weekly_reports()
        assert len(reports) == 1
        assert reports[0]["key_themes"] == ["LLM", "RAG"]
