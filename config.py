"""AI News Radar 설정"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 경로
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Gemini API
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
    "ai_other": "기타",
}

# 감성
SENTIMENTS = {
    "positive": "😊 긍정",
    "negative": "😠 부정",
    "neutral": "😐 중립",
}
