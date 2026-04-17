"""보안 유틸리티 — OWASP ASVS v4.0.3 Level 1 대응.

이 모듈은 외부 입력 처리 시 발생할 수 있는 주요 위협을 선제적으로 차단합니다.
- safe_url(): V5.5.2 SSRF 차단 — RSS 피드 URL 검증
- safe_join(): V12.3.1 경로 탈출 차단 — 파일 저장 경로 검증
- mask_secret(): V7.1.1 로그 마스킹 — API 키 누출 방지
- secure_token(): V3.2.1 / V6.2.1 암호학적 난수 — 세션/nonce용
"""
from __future__ import annotations

import ipaddress
import logging
import re
import secrets
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

__all__ = [
    "safe_url",
    "safe_join",
    "mask_secret",
    "secure_token",
    "SecurityError",
    "SecretMaskingFilter",
    "install_secret_mask",
]


class SecurityError(ValueError):
    """보안 검증 실패 시 발생하는 예외."""


# ---------------------------------------------------------------------------
# V5.5.2 — SSRF 차단
# ---------------------------------------------------------------------------

_ALLOWED_SCHEMES = frozenset({"http", "https"})

_BLOCKED_HOSTS = frozenset({
    "localhost",
    "metadata.google.internal",
    "metadata.aws",
    "169.254.169.254",   # AWS/GCP/Azure IMDS
    "100.100.100.200",   # Alibaba Cloud ECS
})

_ALLOWED_PORTS = frozenset({80, 443, 8080, 8443})


def _is_private_ip(host: str) -> bool:
    """호스트가 프라이빗·예약·루프백 IP인지 판정."""
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_reserved
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_unspecified
    )


def safe_url(url: str, *, allow_http: bool = True) -> Optional[str]:
    """URL이 안전한 외부 요청 대상인지 검증.

    - 허용 스킴: http / https (allow_http=False면 https만)
    - 차단: localhost, 프라이빗/링크로컬/루프백 IP, 클라우드 메타데이터, 비표준 포트
    - 반환: 안전하면 원본 URL, 아니면 None
    """
    if not url or not isinstance(url, str):
        return None
    if len(url) > 2048:
        return None

    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return None

    scheme = (parsed.scheme or "").lower()
    if scheme not in _ALLOWED_SCHEMES:
        return None
    if not allow_http and scheme != "https":
        return None

    host = (parsed.hostname or "").lower()
    if not host:
        return None
    if host in _BLOCKED_HOSTS:
        return None
    if _is_private_ip(host):
        return None

    if parsed.port is not None and parsed.port not in _ALLOWED_PORTS:
        return None

    return url


# ---------------------------------------------------------------------------
# V12.3.1 — 경로 탈출 차단
# ---------------------------------------------------------------------------

def safe_join(base: Path | str, *paths: str) -> Path:
    """base 디렉토리 하위 경로를 안전하게 결합.

    - 결합 후 resolve된 경로가 base 하위인지 검증 (심볼릭 링크 포함)
    - 탈출 시도 시 SecurityError 발생
    """
    base_path = Path(base).resolve()
    joined = base_path.joinpath(*paths).resolve()
    try:
        joined.relative_to(base_path)
    except ValueError as exc:
        raise SecurityError(
            f"Path traversal attempt: {joined} is outside {base_path}"
        ) from exc
    return joined


# ---------------------------------------------------------------------------
# V7.1.1 — 로그 마스킹
# ---------------------------------------------------------------------------

def _kv_mask(match: re.Match) -> str:
    return f"{match.group(1)}=***"


_SECRET_PATTERNS: tuple[tuple[re.Pattern, object], ...] = (
    (re.compile(r"AIza[A-Za-z0-9_-]{35,}"), "AIza***"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "sk-***"),
    (re.compile(r"ghp_[A-Za-z0-9]{30,}"), "ghp_***"),
    (re.compile(r"gho_[A-Za-z0-9]{30,}"), "gho_***"),
    (re.compile(r"xoxb-[A-Za-z0-9-]{20,}"), "xoxb-***"),
    (re.compile(r"xoxp-[A-Za-z0-9-]{20,}"), "xoxp-***"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AKIA***"),
    (re.compile(r"\b[0-9]{9,10}:[A-Za-z0-9_-]{35}\b"), "tg:***"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"), "Bearer ***"),
    (re.compile(
        r"(?i)(api[-_]?key|auth[-_]?token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9._-]{16,}['\"]?"
    ), _kv_mask),
)


def mask_secret(text: str) -> str:
    """문자열 내 알려진 패턴의 비밀값을 마스킹.

    - 로그/에러 메시지 출력 직전에 호출
    - 짧은 값(< 16자)은 대체로 원본 유지 (false positive 방지)
    - 알 수 없는 포맷은 마스킹하지 않음
    """
    if not text or not isinstance(text, str):
        return text
    out = text
    for pattern, repl in _SECRET_PATTERNS:
        out = pattern.sub(repl, out)
    return out


class SecretMaskingFilter(logging.Filter):
    """logging 파이프라인에 부착하여 메시지·args 자동 마스킹."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            if isinstance(record.msg, str):
                record.msg = mask_secret(record.msg)
            if record.args:
                if isinstance(record.args, dict):
                    record.args = {k: mask_secret(str(v)) for k, v in record.args.items()}
                else:
                    record.args = tuple(mask_secret(str(a)) for a in record.args)
        except Exception:
            pass
        return True


def install_secret_mask(logger: Optional[logging.Logger] = None) -> None:
    """지정 logger(없으면 root)에 SecretMaskingFilter를 idempotent하게 부착."""
    target = logger or logging.getLogger()
    for existing in target.filters:
        if isinstance(existing, SecretMaskingFilter):
            return
    target.addFilter(SecretMaskingFilter())


# ---------------------------------------------------------------------------
# V3.2.1 / V6.2.1 — 암호학적 난수
# ---------------------------------------------------------------------------

def secure_token(nbytes: int = 32) -> str:
    """URL-safe 암호학적 난수 토큰 생성.

    - secrets.token_urlsafe 기반 (CSPRNG)
    - 기본 32 bytes → 약 43자 Base64URL
    - nonce·일회성 값·상관관계 ID에 사용
    """
    if nbytes < 16:
        raise SecurityError("nbytes must be >= 16 bytes of entropy")
    return secrets.token_urlsafe(nbytes)
