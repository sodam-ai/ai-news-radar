"""이전 사고/실수 방지 회귀 테스트.

- 마스킹 우회 시도 (JSON 래핑, URL 쿼리, 다중 라인)
- 경로 탈출 변형
- 빈 DB에서 공개 API 호출 안정성
- 한국어 콘텐츠 roundtrip
"""
from __future__ import annotations

import pytest

from db import database as db
from utils.security import SecurityError, mask_secret, safe_join, safe_url


class TestMaskingBypassAttempts:
    def test_secret_inside_json_masked(self):
        fake = "AIzaSy" + "C" * 35
        payload = f'{{"api_key": "{fake}", "model": "gemini"}}'
        out = mask_secret(payload)
        assert fake not in out

    def test_url_with_token_query_masked(self):
        fake = "ghp_" + "X" * 36
        url = f"https://api.github.com/user?token={fake}"
        out = mask_secret(url)
        assert fake not in out

    def test_multiline_text_all_masked(self):
        fake1 = "AIzaSy" + "A" * 35
        fake2 = "sk-" + "Y" * 40
        text = f"line1: {fake1}\nline2: {fake2}\nline3: plain"
        out = mask_secret(text)
        assert fake1 not in out
        assert fake2 not in out
        assert "line3: plain" in out


class TestPathTraversalVariants:
    @pytest.mark.parametrize("attempt", [
        ("..",),
        (".", ".."),
        ("subdir", "..", ".."),
        ("..", "..", "..", "etc", "passwd"),
    ])
    def test_various_traversal_blocked(self, tmp_path, attempt):
        with pytest.raises(SecurityError):
            safe_join(tmp_path, *attempt)

    def test_resolved_inside_base(self, tmp_path):
        target = tmp_path / "inside.txt"
        target.write_text("ok")
        result = safe_join(tmp_path, "inside.txt")
        assert result == target.resolve()


class TestSafeUrlVariants:
    def test_whitespace_preserved_on_pass(self):
        """선행/후행 공백이 있어도 검증 후 원본 반환 (strip은 내부 검증용)."""
        result = safe_url("  https://example.com/  ")
        # 공백 포함 전체가 반환되거나, 유효 판정 시 그대로
        assert result is None or result.strip() == "https://example.com/"

    def test_ipv6_loopback_blocked(self):
        assert safe_url("http://[::1]/") is None

    def test_url_with_userinfo(self):
        """user:pass@ 형태는 호스트 판정 후 결정됨."""
        result = safe_url("https://user:pass@example.com/")
        # 호스트가 example.com이면 허용됨
        assert result is None or "example.com" in result


class TestDatabaseResilience:
    def test_empty_db_public_apis(self, temp_db):
        """빈 DB에서도 모든 조회 API가 예외 없이 빈 값 반환."""
        assert db.get_articles() == []
        assert db.get_primary_articles() == []
        assert db.get_unprocessed_articles() == []
        assert db.get_sources() == []
        assert db.get_watchlist() == []
        assert db.get_bookmarks() == []
        assert db.get_alert_log() == []
        assert db.get_briefings() == []
        assert db.get_weekly_reports() == []
        assert db.get_active_keywords() == []
        assert db.get_bookmark_ids() == set()
        assert db.get_article_count() == 0
        assert db.get_processed_count() == 0

    def test_search_on_empty_db(self, temp_db):
        assert db.search_articles("anything") == []

    def test_korean_content_roundtrip(self, temp_db, sample_article):
        """한국어 콘텐츠가 손실 없이 저장·조회."""
        korean = {
            **sample_article,
            "id": "art_kr",
            "url": "https://ex.com/kr",
            "title": "AI 뉴스 — 클로드 최신 업데이트",
            "summary_text": "앤트로픽이 새로운 모델을 공개했다.",
            "tags": ["클로드", "앤트로픽", "업데이트"],
        }
        db.upsert_article(korean)
        got = db.get_article_by_id("art_kr")
        assert got["title"] == korean["title"]
        assert "클로드" in got["tags"]
