"""crawler/rss_crawler.py — SSRF 방어 회귀 테스트.

원칙:
- 실제 네트워크 호출 금지 (feedparser.parse를 mock 처리)
- safe_url 통과 실패 시 feedparser 호출조차 일어나지 않아야 함
"""
from __future__ import annotations

from unittest.mock import patch

from crawler import rss_crawler
from utils.security import safe_url


class TestCrawlerUsesSafeUrl:
    """크롤러가 safe_url 검증을 통과하지 못한 URL은 건너뛰는지 확인."""

    def test_crawl_single_rejects_private_ip_source(self):
        source = {
            "id": "src_evil",
            "name": "evil",
            "url": "http://169.254.169.254/latest/meta-data/",
            "is_active": True,
        }
        with patch("crawler.rss_crawler.feedparser") as mock_fp:
            updated, new = rss_crawler._crawl_single(source, set())
            assert new == []
            mock_fp.parse.assert_not_called()

    def test_crawl_single_rejects_localhost(self):
        source = {
            "id": "src_local",
            "name": "local",
            "url": "http://localhost:6601/feed",
            "is_active": True,
        }
        with patch("crawler.rss_crawler.feedparser") as mock_fp:
            _, new = rss_crawler._crawl_single(source, set())
            assert new == []
            mock_fp.parse.assert_not_called()

    def test_crawl_single_rejects_file_scheme(self):
        source = {
            "id": "src_file",
            "name": "file",
            "url": "file:///etc/passwd",
            "is_active": True,
        }
        with patch("crawler.rss_crawler.feedparser") as mock_fp:
            _, new = rss_crawler._crawl_single(source, set())
            assert new == []
            mock_fp.parse.assert_not_called()

    def test_inactive_source_skipped(self):
        source = {
            "id": "src_inactive",
            "name": "inactive",
            "url": "https://example.com/feed",
            "is_active": False,
        }
        with patch("crawler.rss_crawler.feedparser") as mock_fp:
            _, new = rss_crawler._crawl_single(source, set())
            assert new == []
            mock_fp.parse.assert_not_called()

    def test_article_url_filtered_by_safe_url(self):
        """피드 내 악성 article URL도 safe_url이 거부해야 함."""

        class FakeEntry:
            def __init__(self, link, title="t"):
                self.link = link
                self.title = title
                self.summary = ""

        class FakeFeed:
            entries = [
                FakeEntry("http://127.0.0.1/internal"),
                FakeEntry("https://valid.example.com/article-1"),
                FakeEntry("http://169.254.169.254/imds"),
            ]

        source = {
            "id": "src_mix",
            "name": "mix",
            "url": "https://example.com/feed",
            "is_active": True,
        }

        with patch("crawler.rss_crawler.feedparser.parse", return_value=FakeFeed()):
            _, new = rss_crawler._crawl_single(source, set())
            assert len(new) == 1
            assert new[0]["url"] == "https://valid.example.com/article-1"


class TestSafeUrlDirectly:
    def test_blocks_imds(self):
        assert safe_url("http://169.254.169.254/latest/meta-data/") is None

    def test_allows_valid_rss(self):
        assert safe_url("https://example.com/feed.xml") == "https://example.com/feed.xml"
