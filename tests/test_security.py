"""utils/security.py — OWASP ASVS L1 보안 유틸 회귀 테스트.

검증 항목:
- V5.5.2 safe_url — SSRF 차단 (프라이빗 IP / 메타데이터 / 비표준 포트 / 스킴)
- V12.3.1 safe_join — 경로 탈출 차단
- V7.1.1 mask_secret — 알려진 시크릿 패턴 마스킹
- V6.2.1 secure_token — 암호학적 난수 최소 엔트로피
"""
from __future__ import annotations

import logging

import pytest

from utils.security import (
    SecretMaskingFilter,
    SecurityError,
    install_secret_mask,
    mask_secret,
    safe_join,
    safe_url,
    secure_token,
)


class TestSafeUrl:
    """V5.5.2 — 외부 URL이 안전한 요청 대상인지 검증."""

    @pytest.mark.parametrize("url", [
        "https://example.com/feed.xml",
        "https://news.ycombinator.com/rss",
        "http://blog.example.org/feed",
        "https://sub.domain.example/path?query=1",
    ])
    def test_safe_public_urls_pass(self, url):
        assert safe_url(url) == url

    @pytest.mark.parametrize("url", [
        "http://localhost/admin",
        "http://localhost:8080/",
        "https://LOCALHOST/x",
    ])
    def test_localhost_blocked(self, url):
        assert safe_url(url) is None

    @pytest.mark.parametrize("url", [
        "http://127.0.0.1/",
        "http://127.0.0.1:6601/secret",
        "http://10.0.0.1/internal",
        "http://192.168.1.1/",
        "http://172.16.0.1/",
        "http://::1/",
        "http://0.0.0.0/",
    ])
    def test_private_ips_blocked(self, url):
        assert safe_url(url) is None, f"private IP should be blocked: {url}"

    @pytest.mark.parametrize("url", [
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/",
        "http://metadata.google.internal/computeMetadata/v1/",
        "http://100.100.100.200/",
    ])
    def test_cloud_metadata_blocked(self, url):
        assert safe_url(url) is None, f"cloud metadata should be blocked: {url}"

    @pytest.mark.parametrize("url", [
        "file:///etc/passwd",
        "ftp://example.com/",
        "javascript:alert(1)",
        "data:text/html,<script>",
        "gopher://example.com/",
    ])
    def test_non_http_schemes_blocked(self, url):
        assert safe_url(url) is None

    def test_https_only_mode(self):
        assert safe_url("http://example.com/", allow_http=False) is None
        assert safe_url("https://example.com/", allow_http=False) == "https://example.com/"

    @pytest.mark.parametrize("url", [
        "https://example.com:22/",
        "https://example.com:3306/",
        "https://example.com:6379/",
        "https://example.com:25/",
    ])
    def test_non_standard_ports_blocked(self, url):
        assert safe_url(url) is None

    @pytest.mark.parametrize("url", [
        "https://example.com:80/",
        "https://example.com:443/",
        "https://example.com:8080/",
        "https://example.com:8443/",
    ])
    def test_standard_ports_allowed(self, url):
        assert safe_url(url) == url

    @pytest.mark.parametrize("url", [
        "",
        None,
        "   ",
        "not a url",
        "https://",
    ])
    def test_invalid_inputs_rejected(self, url):
        assert safe_url(url) is None

    def test_excessively_long_url_rejected(self):
        long_url = "https://example.com/" + ("a" * 2100)
        assert safe_url(long_url) is None

    def test_non_string_type_rejected(self):
        assert safe_url(12345) is None
        assert safe_url(["https://example.com"]) is None


class TestSafeJoin:
    """V12.3.1 — 결합된 경로가 base 하위인지 검증."""

    def test_valid_subpath(self, tmp_path):
        result = safe_join(tmp_path, "subdir", "file.txt")
        assert str(result).startswith(str(tmp_path.resolve()))

    def test_single_file(self, tmp_path):
        result = safe_join(tmp_path, "file.txt")
        assert result.name == "file.txt"

    @pytest.mark.parametrize("attempt", [
        ("..", "etc", "passwd"),
        ("..", "..", "secret"),
        ("subdir", "..", "..", "secret"),
    ])
    def test_path_traversal_blocked(self, tmp_path, attempt):
        with pytest.raises(SecurityError):
            safe_join(tmp_path, *attempt)

    def test_absolute_path_escape_blocked(self, tmp_path):
        with pytest.raises(SecurityError):
            safe_join(tmp_path, "/etc/passwd")

    def test_base_as_string_works(self, tmp_path):
        result = safe_join(str(tmp_path), "ok.txt")
        assert result.name == "ok.txt"


class TestMaskSecret:
    """V7.1.1 — 알려진 시크릿 패턴 자동 마스킹."""

    def test_gemini_api_key_masked(self):
        fake_key = "AIzaSy" + "A" * 35
        result = mask_secret(f"Calling Gemini with key={fake_key}")
        assert fake_key not in result
        assert "AIza***" in result

    def test_openai_key_masked(self):
        fake = "sk-" + "x" * 40
        out = mask_secret(f"token: {fake}")
        assert fake not in out
        assert "sk-***" in out

    def test_github_pat_masked(self):
        fake = "ghp_" + "a" * 36
        out = mask_secret(f"auth {fake}")
        assert fake not in out
        assert "ghp_***" in out

    def test_slack_bot_token_masked(self):
        fake = "xoxb-12345-67890-" + "a" * 24
        out = mask_secret(fake)
        assert fake not in out

    def test_aws_access_key_masked(self):
        fake = "AKIA" + "ABCDEFGHIJ123456"
        out = mask_secret(f"AWS {fake}")
        assert fake not in out
        assert "AKIA***" in out

    def test_telegram_bot_token_masked(self):
        fake = "123456789:" + "A" * 35
        out = mask_secret(f"bot {fake}")
        assert fake not in out

    def test_bearer_token_masked(self):
        fake = "Bearer " + "x" * 30
        out = mask_secret(fake)
        assert "Bearer ***" in out

    def test_plain_text_not_masked(self):
        msg = "Crawled 42 articles from 10 sources"
        assert mask_secret(msg) == msg

    def test_short_value_not_masked(self):
        assert "id=12345" in mask_secret("user id=12345")

    def test_none_input_returns_none(self):
        assert mask_secret(None) is None
        assert mask_secret("") == ""

    def test_api_key_kv_pattern(self):
        msg = 'api_key="' + "a" * 40 + '"'
        out = mask_secret(msg)
        assert "a" * 40 not in out
        assert "api_key=***" in out

    def test_multiple_secrets_in_one_line(self):
        fake1 = "AIzaSy" + "A" * 35
        fake2 = "sk-" + "b" * 40
        msg = f"{fake1} and {fake2}"
        out = mask_secret(msg)
        assert fake1 not in out
        assert fake2 not in out


class TestSecretMaskingFilter:
    """logging 파이프라인 통합 검증."""

    def test_filter_masks_log_message(self, caplog):
        logger = logging.getLogger("test_mask_log")
        logger.addFilter(SecretMaskingFilter())
        fake_key = "AIzaSy" + "B" * 35
        with caplog.at_level(logging.INFO, logger="test_mask_log"):
            logger.info(f"secret={fake_key}")
        assert fake_key not in caplog.text
        assert "AIza***" in caplog.text

    def test_install_secret_mask_idempotent(self):
        logger = logging.getLogger("test_idempotent")
        install_secret_mask(logger)
        install_secret_mask(logger)
        filter_count = sum(1 for f in logger.filters if isinstance(f, SecretMaskingFilter))
        assert filter_count == 1, "install_secret_mask는 중복 설치 금지"


class TestSecureToken:
    """V6.2.1 / V3.2.1 — CSPRNG 기반 토큰 생성."""

    def test_default_token_length(self):
        tok = secure_token()
        assert len(tok) >= 40

    def test_custom_length(self):
        tok = secure_token(64)
        assert len(tok) >= 80

    def test_low_entropy_rejected(self):
        with pytest.raises(SecurityError):
            secure_token(8)
        with pytest.raises(SecurityError):
            secure_token(0)

    def test_tokens_are_unique(self):
        tokens = {secure_token() for _ in range(100)}
        assert len(tokens) == 100

    def test_token_is_urlsafe(self):
        import string
        valid = set(string.ascii_letters + string.digits + "-_")
        for _ in range(20):
            tok = secure_token()
            assert set(tok).issubset(valid), f"비-URLsafe 문자 포함: {tok}"
