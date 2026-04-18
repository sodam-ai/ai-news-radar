"""AI News Radar 설정"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Windows 콘솔 UTF-8 인코딩 강제 (CP949 오류 방지)
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

load_dotenv(override=True)  # .env 우선 — 셸 환경변수의 만료/잘못된 키 차단

# 경로
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "radar.db"

# LLM 프로바이더 (자동 감지 또는 명시적 설정)
# .env에 LLM_PROVIDER=groq 처럼 설정하거나, API 키만 넣으면 자동 감지
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "")

# Gemini API (하위 호환)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_FLASH_MODEL = "gemini-2.5-flash"
GEMINI_FLASH_LITE_MODEL = "gemini-2.5-flash-lite"

# 크롤링
CRAWL_INTERVAL_MINUTES = int(os.getenv("CRAWL_INTERVAL_MINUTES", "60"))
MAX_ARTICLES_PER_SOURCE = 20

# 서버
STREAMLIT_PORT = 6601

# 카테고리
CATEGORIES = {
    "ai_tool": "AI 도구/제품",
    "ai_research": "AI 논문/연구",
    "ai_trend": "업계 트렌드/동향",
    "ai_tutorial": "활용법/튜토리얼",
    "ai_business": "AI 비즈니스/투자",
    "ai_image_video": "AI 이미지/영상",
    "ai_coding": "바이브코딩/AI코딩",
    "ai_ontology": "온톨로지/지식그래프",
    "ai_other": "기타",
}

# 감성
SENTIMENTS = {
    "positive": "😊 긍정",
    "negative": "😠 부정",
    "neutral": "😐 중립",
}
