"""오늘의 브리핑 TOP 5 자동 생성"""
import json
from datetime import datetime

from config import DATA_DIR
from ai.model_router import call_gemini
from utils.helpers import safe_read_json, safe_write_json, today_str, now_iso, log

ARTICLES_PATH = DATA_DIR / "articles.json"
BRIEFINGS_PATH = DATA_DIR / "briefings.json"


def generate_daily_briefing() -> dict | None:
    """오늘의 브리핑을 생성하고 저장. 브리핑 dict 반환."""
    articles = safe_read_json(ARTICLES_PATH, [])
    today = today_str()

    # 오늘 수집된 AI 처리 완료 기사 중 대표 글만
    today_articles = [
        a for a in articles
        if a.get("ai_processed")
        and a.get("is_primary", True)
        and a.get("crawled_at", "").startswith(today)
    ]

    if not today_articles:
        # 오늘 글이 없으면 최근 글 사용
        today_articles = [
            a for a in articles
            if a.get("ai_processed") and a.get("is_primary", True)
        ]
        today_articles.sort(key=lambda x: x.get("crawled_at", ""), reverse=True)
        today_articles = today_articles[:20]

    if not today_articles:
        return None

    # 중요도 순으로 상위 20개만 프롬프트에 포함
    today_articles.sort(key=lambda x: x.get("importance", 0), reverse=True)
    top_articles = today_articles[:20]

    prompt_items = []
    for a in top_articles:
        prompt_items.append(
            f"[ID: {a['id']}] ⭐{a.get('importance', 3)} "
            f"{a.get('sentiment', '😐')} | {a['title']}\n"
            f"요약: {a.get('summary_text', a['content'][:200])}"
        )

    prompt = f"오늘({today})의 AI 뉴스 중 TOP 5를 선정하고 브리핑을 작성해줘:\n\n" + "\n\n".join(prompt_items)

    try:
        response_text = call_gemini(prompt, use_flash=True)
        result = json.loads(response_text.strip().removeprefix("```json").removesuffix("```"))
    except Exception as e:
        log(f"[브리핑 생성 오류] {e}")
        return None

    # 다양한 LLM 응답 형식 유연하게 처리
    top = []
    summary = ""

    if isinstance(result, list):
        top = result
    elif isinstance(result, dict):
        # top_articles 키 유연 검색
        for key in ("top_articles", "top_5_news", "top_news", "articles", "top5", "news"):
            if key in result and isinstance(result[key], list):
                top = result[key]
                break
        # 키를 못 찾으면 첫 번째 배열 사용
        if not top:
            for v in result.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    top = v
                    break
        # overall_summary 키 유연 검색
        for key in ("overall_summary", "summary", "총평", "overall"):
            if key in result and isinstance(result[key], str):
                summary = result[key]
                break

    briefing = {
        "id": f"brf_{today.replace('-', '')}",
        "date": today,
        "top_articles": top,
        "summary": summary,
        "created_at": now_iso(),
    }

    briefings = safe_read_json(BRIEFINGS_PATH, [])
    # 같은 날짜 브리핑 교체
    briefings = [b for b in briefings if b.get("date") != today]
    briefings.append(briefing)
    safe_write_json(BRIEFINGS_PATH, briefings)

    log(f"[브리핑] {today} 브리핑 생성 완료")
    return briefing
