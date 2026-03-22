"""인앱 리더 뷰 — 원문 추출 + 정제"""
import re
import requests
from bs4 import BeautifulSoup


def fetch_clean_content(url: str, timeout: int = 10) -> str:
    """URL에서 원문 텍스트를 추출하고 광고/사이드바를 제거하여 깨끗한 텍스트 반환"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        # 불필요한 요소 제거
        for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "iframe", "ads"]):
            tag.decompose()

        # 본문 추출 시도 (일반적인 article/main 태그 우선)
        article = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"(content|article|post|entry)"))

        if article:
            text = article.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        # 연속 빈줄 정리
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return "\n\n".join(lines[:200])  # 최대 200줄

    except Exception as e:
        return f"원문을 가져올 수 없습니다: {e}"
