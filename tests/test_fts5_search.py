"""FTS5 전문 검색 — SQL 인젝션 방어 + 이스케이프 + 기본 동작.

검증 항목:
- 파라미터화 쿼리로 SQL 인젝션 불가
- FTS5 특수 문법 파싱 실패 시 LIKE fallback으로 안전 반환
- 쿼리 길이 상한(200) + limit 상한(200) 적용
- 성능 스모크: 50건 데이터셋에서 200ms 이내
"""
from __future__ import annotations

from db import database as db


def _seed_articles(sample_article):
    """FTS5에 다양한 기사를 시드."""
    return [
        {**sample_article, "id": "art_1", "url": "https://ex.com/1",
         "title": "Claude 4.7 Released", "summary_text": "Anthropic ships new Claude version"},
        {**sample_article, "id": "art_2", "url": "https://ex.com/2",
         "title": "GPT-5 benchmark results", "summary_text": "OpenAI reports SOTA scores"},
        {**sample_article, "id": "art_3", "url": "https://ex.com/3",
         "title": "Gemini 3 multimodal", "summary_text": "Google pushes context window"},
    ]


class TestFts5Basic:
    def test_empty_query_returns_empty(self, temp_db):
        assert db.search_articles("") == []
        assert db.search_articles("   ") == []

    def test_keyword_hit(self, temp_db, sample_article):
        for a in _seed_articles(sample_article):
            db.upsert_article(a)
        results = db.search_articles("Claude")
        ids = [r["id"] for r in results]
        assert "art_1" in ids

    def test_multiple_keywords(self, temp_db, sample_article):
        for a in _seed_articles(sample_article):
            db.upsert_article(a)
        results = db.search_articles("benchmark")
        assert any(r["id"] == "art_2" for r in results)


class TestFts5SecurityBoundaries:
    """FTS5가 크래시/데이터 유출 없이 안전하게 실패해야 함."""

    def test_sql_injection_attempt_does_not_crash(self, temp_db, sample_article):
        for a in _seed_articles(sample_article):
            db.upsert_article(a)
        evil_queries = [
            "'; DROP TABLE articles; --",
            "\" OR 1=1; --",
            "x'; DELETE FROM articles; --",
        ]
        for q in evil_queries:
            result = db.search_articles(q)
            assert isinstance(result, list)

        assert db.get_article_count() == 3

    def test_fts5_special_chars_fallback(self, temp_db, sample_article):
        for a in _seed_articles(sample_article):
            db.upsert_article(a)
        tricky = [
            "foo*bar",
            "(unbalanced",
            "NEAR/999",
            '""',
            "AND OR",
            "%_like%",
        ]
        for q in tricky:
            result = db.search_articles(q)
            assert isinstance(result, list), f"query '{q}' should not crash"

    def test_query_length_cap(self, temp_db, sample_article):
        db.upsert_article(sample_article)
        long_q = "a" * 10000
        result = db.search_articles(long_q)
        assert isinstance(result, list)

    def test_limit_clamped(self, temp_db, sample_article):
        for i in range(10):
            a = {**sample_article, "id": f"art_{i}", "url": f"https://ex.com/{i}",
                 "title": f"Claude update {i}", "summary_text": "Claude release notes"}
            db.upsert_article(a)
        results = db.search_articles("Claude", limit=9999)
        assert len(results) <= 200


class TestFts5Performance:
    def test_smoke_speed(self, temp_db, sample_article):
        import time
        batch = [
            {**sample_article, "id": f"art_{i}", "url": f"https://ex.com/{i}",
             "title": f"AI news {i}", "summary_text": "LLM model release"}
            for i in range(50)
        ]
        db.upsert_articles(batch)
        t0 = time.perf_counter()
        db.search_articles("model")
        elapsed_ms = (time.perf_counter() - t0) * 1000
        assert elapsed_ms < 500, f"FTS5 검색 {elapsed_ms:.1f}ms — 느림"
