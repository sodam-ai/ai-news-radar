"""주간 AI 인텔리전스 리포트 자동 생성

매주 자동 PDF/Markdown:
- 이번 주 핵심 트렌드 3개
- 분야별 동향 (이미지/영상, 바이브코딩, 온톨로지)
- 주간 통계 (기사 수, 감성 분포, 카테고리 분포)
- 주목할 뉴스 TOP 10
- 다음 주 예측/전망
"""
import json
from datetime import datetime, timedelta

from config import DATA_DIR, CATEGORIES
from ai.model_router import call_gemini, get_active_provider
from ai.briefing import FOCUS_AREAS
from utils.helpers import safe_read_json, safe_write_json, now_iso, log

ARTICLES_PATH = DATA_DIR / "articles.json"
REPORTS_PATH = DATA_DIR / "weekly_reports.json"


def _get_week_range() -> tuple[str, str]:
    """이번 주 월요일~일요일 날짜 범위"""
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def _get_week_articles(start: str, end: str) -> list[dict]:
    """해당 주간의 기사 필터링"""
    articles = safe_read_json(ARTICLES_PATH, [])
    return [
        a for a in articles
        if a.get("ai_processed")
        and a.get("is_primary", True)
        and start <= a.get("crawled_at", "")[:10] <= end
    ]


def _compute_stats(articles: list[dict]) -> dict:
    """주간 통계 계산"""
    total = len(articles)
    if total == 0:
        return {"total": 0}

    # 감성 분포
    sentiment_dist = {}
    for a in articles:
        s = a.get("sentiment", "neutral")
        sentiment_dist[s] = sentiment_dist.get(s, 0) + 1

    # 카테고리 분포
    category_dist = {}
    for a in articles:
        c = a.get("category", "ai_other")
        label = CATEGORIES.get(c, c)
        category_dist[label] = category_dist.get(label, 0) + 1

    # 평균 중요도
    avg_importance = round(sum(a.get("importance", 0) for a in articles) / total, 1)

    # 관심 분야별 카운트
    focus_counts = {}
    for area_id, area_info in FOCUS_AREAS.items():
        count = len([a for a in articles if a.get("category") == area_id])
        # 키워드 매칭 추가
        for a in articles:
            if a.get("category") != area_id:
                text = f"{a.get('title', '')} {' '.join(a.get('tags', []))}".lower()
                if any(kw.lower() in text for kw in area_info["keywords"]):
                    count += 1
        focus_counts[area_info["name"]] = count

    return {
        "total": total,
        "sentiment": sentiment_dist,
        "categories": category_dist,
        "avg_importance": avg_importance,
        "focus_counts": focus_counts,
    }


def generate_weekly_report() -> dict | None:
    """주간 인텔리전스 리포트 생성"""
    start, end = _get_week_range()
    articles = _get_week_articles(start, end)

    if not articles:
        log("[주간 리포트] 기사 없음")
        return None

    stats = _compute_stats(articles)

    # TOP 10 뉴스
    articles_sorted = sorted(articles, key=lambda x: x.get("importance", 0), reverse=True)
    top10 = articles_sorted[:10]

    # LLM으로 트렌드 분석 + 전망 생성
    trends = None
    if get_active_provider():
        trends = _generate_trends_with_llm(articles, start, end)

    report = {
        "id": f"weekly_{start.replace('-', '')}",
        "week_start": start,
        "week_end": end,
        "stats": stats,
        "top_articles": [
            {
                "title": a["title"],
                "url": a["url"],
                "category": CATEGORIES.get(a.get("category", ""), a.get("category", "")),
                "importance": a.get("importance", 0),
                "sentiment": a.get("sentiment", "neutral"),
                "summary": a.get("summary_text", "")[:100],
            }
            for a in top10
        ],
        "trends": trends,
        "created_at": now_iso(),
    }

    # 저장
    reports = safe_read_json(REPORTS_PATH, [])
    reports = [r for r in reports if r.get("week_start") != start]
    reports.append(report)
    safe_write_json(REPORTS_PATH, reports)

    log(f"[주간 리포트] {start}~{end} 생성 완료 ({stats['total']}개 기사)")
    return report


def _generate_trends_with_llm(articles: list[dict], start: str, end: str) -> dict | None:
    """LLM으로 트렌드 분석"""
    # 상위 기사 요약을 프롬프트에 포함
    top_items = sorted(articles, key=lambda x: x.get("importance", 0), reverse=True)[:15]
    items_text = "\n".join([
        f"- [{CATEGORIES.get(a.get('category', ''), '기타')}] {a['title']} (⭐{a.get('importance', 0)}, {a.get('sentiment', '중립')})"
        for a in top_items
    ])

    prompt = f"""이번 주({start} ~ {end}) AI 뉴스 {len(articles)}개를 분석해줘.

주요 기사:
{items_text}

다음 JSON으로 응답해:
{{
  "key_trends": ["핵심 트렌드 1", "핵심 트렌드 2", "핵심 트렌드 3"],
  "image_video_trend": "AI 이미지/영상 분야 동향 한 줄",
  "coding_trend": "바이브코딩/AI코딩 분야 동향 한 줄",
  "ontology_trend": "온톨로지/지식그래프 분야 동향 한 줄",
  "outlook": "다음 주 전망/예측 2~3줄",
  "action_items": ["실천 제안 1", "실천 제안 2", "실천 제안 3"]
}}

반드시 유효한 JSON으로만 응답해."""

    try:
        response_text = call_gemini(prompt, use_flash=True)
        cleaned = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(cleaned)
    except Exception as e:
        log(f"[주간 리포트 LLM 오류] {e}")
        return None


def export_weekly_report_markdown(report: dict) -> str:
    """주간 리포트를 Markdown으로 변환"""
    lines = [
        f"# 📊 주간 AI 인텔리전스 리포트",
        f"**{report['week_start']} ~ {report['week_end']}**",
        f"생성일: {report['created_at'][:10]}",
        "",
    ]

    stats = report.get("stats", {})
    lines.append(f"## 📈 주간 통계")
    lines.append(f"- 총 기사: {stats.get('total', 0)}개")
    lines.append(f"- 평균 중요도: {stats.get('avg_importance', 0)}")
    lines.append("")

    # 감성 분포
    sentiment = stats.get("sentiment", {})
    if sentiment:
        lines.append("**감성 분포:**")
        emojis = {"positive": "😊", "negative": "😠", "neutral": "😐"}
        for s, count in sentiment.items():
            lines.append(f"- {emojis.get(s, '')} {s}: {count}개")
        lines.append("")

    # 관심 분야
    focus = stats.get("focus_counts", {})
    if focus:
        lines.append("**관심 분야:**")
        for name, count in focus.items():
            lines.append(f"- {name}: {count}건")
        lines.append("")

    # 트렌드
    trends = report.get("trends")
    if trends:
        lines.append("## 🔥 핵심 트렌드")
        for i, t in enumerate(trends.get("key_trends", []), 1):
            lines.append(f"{i}. {t}")
        lines.append("")

        lines.append("## 🎯 분야별 동향")
        lines.append(f"- 🎨 이미지/영상: {trends.get('image_video_trend', '-')}")
        lines.append(f"- 💻 바이브코딩: {trends.get('coding_trend', '-')}")
        lines.append(f"- 🔮 온톨로지: {trends.get('ontology_trend', '-')}")
        lines.append("")

        lines.append("## 🔭 다음 주 전망")
        lines.append(trends.get("outlook", ""))
        lines.append("")

        actions = trends.get("action_items", [])
        if actions:
            lines.append("## ✅ 실천 제안")
            for a in actions:
                lines.append(f"- {a}")
            lines.append("")

    # TOP 10
    lines.append("## 📰 주목할 뉴스 TOP 10")
    for i, a in enumerate(report.get("top_articles", []), 1):
        stars = "⭐" * a.get("importance", 0)
        lines.append(f"{i}. {stars} [{a['title']}]({a['url']})")
        if a.get("summary"):
            lines.append(f"   > {a['summary']}")
    lines.append("")

    lines.append("---")
    lines.append("*AI News Radar 주간 인텔리전스 리포트 — SoDam AI Studio*")
    return "\n".join(lines)


def get_latest_report() -> dict | None:
    """가장 최근 주간 리포트 반환"""
    reports = safe_read_json(REPORTS_PATH, [])
    if not reports:
        return None
    return max(reports, key=lambda r: r.get("week_start", ""))
