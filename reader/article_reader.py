"""기사 본문 정리."""
import ipaddress
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

MAX_DOWNLOAD_BYTES = 1_500_000
ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_HOSTS = {"localhost"}


def fetch_clean_content(url: str, timeout: int = 10) -> str:
    """공개 웹 문서만 가져와 본문 텍스트로 정리."""
    try:
        _validate_public_url(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()

        content_length = int(response.headers.get("Content-Length", "0") or "0")
        if content_length and content_length > MAX_DOWNLOAD_BYTES:
            return "본문 로드 실패: 응답이 너무 큽니다."

        raw_chunks: list[bytes] = []
        total_bytes = 0
        for chunk in response.iter_content(chunk_size=8192):
            if not chunk:
                continue
            total_bytes += len(chunk)
            if total_bytes > MAX_DOWNLOAD_BYTES:
                return "본문 로드 실패: 응답이 너무 큽니다."
            raw_chunks.append(chunk)

        raw_body = b"".join(raw_chunks)
        response.encoding = response.apparent_encoding or "utf-8"
        text_body = raw_body.decode(response.encoding, errors="replace")
        soup = BeautifulSoup(text_body, "html.parser")

        for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
            tag.decompose()

        article = (
            soup.find("article")
            or soup.find("main")
            or soup.find("div", class_=re.compile(r"(content|article|post|entry)"))
        )

        if article:
            text = article.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return "\n\n".join(lines[:200])
    except Exception as e:
        return f"본문 로드 실패: {e}"


def _validate_public_url(url: str):
    parsed = urlparse(url)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError("http/https URL만 허용됩니다.")

    hostname = (parsed.hostname or "").strip().lower()
    if not hostname:
        raise ValueError("호스트가 없는 URL입니다.")
    if hostname in BLOCKED_HOSTS or hostname.endswith(".local"):
        raise ValueError("로컬 주소는 허용되지 않습니다.")

    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        return

    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
        raise ValueError("사설/로컬 IP는 허용되지 않습니다.")
