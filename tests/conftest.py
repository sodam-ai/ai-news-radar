"""pytest 공용 fixture.

- 각 테스트마다 독립된 임시 SQLite DB 사용 (운영 DB 무오염)
- 실제 네트워크/.env 미의존 (CI 격리)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """각 테스트별 임시 SQLite DB.

    - db.database.DB_PATH를 임시 경로로 치환
    - 스레드 로컬 커넥션 리셋 후 init_db 호출
    """
    from db import database

    test_db_path = tmp_path / "test_radar.db"
    monkeypatch.setattr(database, "DB_PATH", test_db_path)

    if hasattr(database._local, "conn") and database._local.conn is not None:
        try:
            database._local.conn.close()
        except Exception:
            pass
        database._local.conn = None

    database.init_db()
    yield test_db_path

    if hasattr(database._local, "conn") and database._local.conn is not None:
        try:
            database._local.conn.close()
        except Exception:
            pass
        database._local.conn = None


@pytest.fixture
def sample_article():
    """테스트용 합성 기사 (운영 데이터 아님)."""
    return {
        "id": "art_test001",
        "source_id": "src_test",
        "title": "AI Breakthrough in Testing",
        "url": "https://example.com/news/ai-testing",
        "content": "An AI system demonstrated new capabilities.",
        "category": "ai_research",
        "importance": 4,
        "sentiment": "positive",
        "sentiment_reason": "novel capability",
        "tags": ["ai", "research", "testing"],
        "image_urls": [],
        "image_analysis": "",
        "cluster_id": "",
        "is_primary": True,
        "related_articles": [],
        "published_at": "2026-04-17T00:00:00+00:00",
        "crawled_at": "2026-04-17T00:05:00+00:00",
        "is_read": False,
        "ai_processed": True,
        "summary_text": "AI system shows new testing abilities.",
    }


@pytest.fixture
def sample_source():
    """테스트용 합성 소스 (운영 데이터 아님)."""
    return {
        "id": "src_test",
        "name": "Test RSS Feed",
        "url": "https://example.com/feed.xml",
        "type": "rss",
        "is_preset": True,
        "crawl_interval": 60,
        "is_active": True,
        "lang": "en",
        "last_crawled_at": None,
        "created_at": "2026-04-17T00:00:00+00:00",
    }
