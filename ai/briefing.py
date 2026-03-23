"""오늘의 브리핑 TOP 5 + 분야별 맞춤 브리핑 자동 생성"""
import json
from datetime import datetime

from config import DATA_DIR, CATEGORIES
from ai.model_router import call_gemini
from utils.helpers import safe_read_json, safe_write_json, today_str, now_iso, log

ARTICLES_PATH = DATA_DIR / "articles.json"
BRIEFINGS_PATH = DATA_DIR / "briefings.json"

# 관심 분야 정의 (맞춤 브리핑 대상)
FOCUS_AREAS = {
    "ai_image_video": {
        "name": "AI 이미지/영상",
        "icon": "🎨",
        "keywords": ["midjourney", "stable diffusion", "dall-e", "flux", "sora", "runway", "kling", "pika", "comfyui", "lora", "이미지 생성", "영상 생성", "text-to-image", "text-to-video"],
        "top_count": 3,
    },
    "ai_coding": {
        "name": "바이브코딩/AI코딩",
        "icon": "💻",
        "keywords": ["claude code", "cursor", "copilot", "v0", "bolt", "windsurf", "devin", "vibe coding", "바이브코딩", "코드 생성", "ai coding", "agentic", "코파일럿"],
        "top_count": 3,
    },
    "ai_ontology": {
        "name": "온톨로지/지식그래프",
        "icon": "🔮",
        "keywords": ["ontology", "knowledge graph", "neo4j", "rdf", "owl", "semantic web", "그래프db", "지식그래프", "온톨로지", "graph database"],
        "top_count": 3,
    },
}


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

    # 분야별 맞춤 브리핑도 함께 생성
    focus_briefings = _generate_focus_briefings(today_articles)
    briefing["focus_briefings"] = focus_briefings

    # 다시 저장 (focus 포함)
    briefings = safe_read_json(BRIEFINGS_PATH, [])
    briefings = [b for b in briefings if b.get("date") != today]
    briefings.append(briefing)
    safe_write_json(BRIEFINGS_PATH, briefings)

    log(f"[브리핑] {today} 브리핑 생성 완료 (분야별 {len(focus_briefings)}개)")
    return briefing


def _generate_focus_briefings(all_articles: list[dict]) -> dict:
    """관심 분야별 맞춤 브리핑 생성 (LLM 호출 없이 기존 데이터 활용)"""
    focus_results = {}

    for area_id, area_info in FOCUS_AREAS.items():
        # 카테고리 매칭 + 키워드 매칭
        matched = []
        for a in all_articles:
            score = 0
            # 카테고리 직접 매칭 (가중치 높음)
            if a.get("category") == area_id:
                score += 10

            # 키워드 매칭 (제목 + 태그 + 요약)
            text = f"{a.get('title', '')} {' '.join(a.get('tags', []))} {a.get('summary_text', '')}".lower()
            for kw in area_info["keywords"]:
                if kw.lower() in text:
                    score += 3 if kw.lower() in a.get("title", "").lower() else 1

            if score > 0:
                matched.append({"score": score, "article": a})

        # 스코어 순 정렬 → top_count개 선택
        matched.sort(key=lambda x: (-x["score"], -x["article"].get("importance", 0)))
        top_n = matched[:area_info["top_count"]]

        focus_results[area_id] = {
            "name": area_info["name"],
            "icon": area_info["icon"],
            "total_count": len(matched),
            "top_articles": [
                {
                    "title": item["article"]["title"],
                    "url": item["article"]["url"],
                    "summary": item["article"].get("summary_text", ""),
                    "importance": item["article"].get("importance", 0),
                    "sentiment": item["article"].get("sentiment", "neutral"),
                    "score": item["score"],
                }
                for item in top_n
            ],
        }

    return focus_results


def get_focus_areas() -> dict:
    """등록된 관심 분야 정보 반환"""
    return FOCUS_AREAS
