"""Weekly AI report generation."""
import json
from datetime import datetime, timedelta

from ai.briefing import FOCUS_AREAS
from ai.model_router import call_gemini, get_active_provider
from config import CATEGORIES, DATA_DIR
from utils.helpers import log, now_iso, safe_read_json, safe_update_json

ARTICLES_PATH = DATA_DIR / "articles.json"
REPORTS_PATH = DATA_DIR / "weekly_reports.json"


def _get_week_range() -> tuple[str, str]:
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def _get_week_articles(start: str, end: str) -> list[dict]:
    articles = safe_read_json(ARTICLES_PATH, [])
    return [
        article
        for article in articles
        if article.get("ai_processed")
        and article.get("is_primary", True)
        and start <= article.get("crawled_at", "")[:10] <= end
    ]


def _compute_stats(articles: list[dict]) -> dict:
    total = len(articles)
    if total == 0:
        return {"total": 0}

    sentiment_dist = {}
    category_dist = {}
    focus_counts = {}

    for article in articles:
        sentiment = article.get("sentiment", "neutral")
        sentiment_dist[sentiment] = sentiment_dist.get(sentiment, 0) + 1

        category = article.get("category", "ai_other")
        label = CATEGORIES.get(category, category)
        category_dist[label] = category_dist.get(label, 0) + 1

    avg_importance = round(sum(article.get("importance", 0) for article in articles) / total, 1)

    for area_id, area_info in FOCUS_AREAS.items():
        count = len([article for article in articles if article.get("category") == area_id])
        for article in articles:
            if article.get("category") == area_id:
                continue
            text = f"{article.get('title', '')} {' '.join(article.get('tags', []))}".lower()
            if any(keyword.lower() in text for keyword in area_info["keywords"]):
                count += 1
        focus_counts[area_info["name"]] = count

    return {
        "total": total,
        "sentiment": sentiment_dist,
        "categories": category_dist,
        "avg_importance": avg_importance,
        "focus_counts": focus_counts,
    }


def _generate_trends_with_llm(articles: list[dict], start: str, end: str) -> dict | None:
    top_items = sorted(articles, key=lambda item: item.get("importance", 0), reverse=True)[:15]
    items_text = "\n".join(
        [
            f"- [{CATEGORIES.get(article.get('category', ''), 'Other')}] "
            f"{article['title']} "
            f"(importance={article.get('importance', 0)}, sentiment={article.get('sentiment', 'neutral')})"
            for article in top_items
        ]
    )

    prompt = f"""Analyze AI news for the week {start} to {end}.
Return JSON only with keys:
- key_trends
- image_video_trend
- coding_trend
- ontology_trend
- outlook
- action_items

Articles:
{items_text}
"""

    try:
        response_text = call_gemini(prompt, use_flash=True)
        cleaned = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(cleaned)
    except Exception as e:
        log(f"[weekly-report:llm-error] {e}")
        return None


def _store_report(report: dict):
    week_start = report["week_start"]

    def updater(current: list[dict]):
        retained = [item for item in current if item.get("week_start") != week_start]
        retained.append(report)
        return retained

    safe_update_json(REPORTS_PATH, updater, default=[])


def generate_weekly_report() -> dict | None:
    start, end = _get_week_range()
    articles = _get_week_articles(start, end)
    if not articles:
        log("[weekly-report] no articles")
        return None

    stats = _compute_stats(articles)
    top_articles = sorted(articles, key=lambda item: item.get("importance", 0), reverse=True)[:10]
    trends = _generate_trends_with_llm(articles, start, end) if get_active_provider() else None

    report = {
        "id": f"weekly_{start.replace('-', '')}",
        "week_start": start,
        "week_end": end,
        "stats": stats,
        "top_articles": [
            {
                "title": article["title"],
                "url": article["url"],
                "category": CATEGORIES.get(article.get("category", ""), article.get("category", "")),
                "importance": article.get("importance", 0),
                "sentiment": article.get("sentiment", "neutral"),
                "summary": article.get("summary_text", "")[:100],
            }
            for article in top_articles
        ],
        "trends": trends,
        "created_at": now_iso(),
    }
    _store_report(report)

    log(f"[weekly-report:done] week={start}~{end} articles={stats['total']}")
    return report


def export_weekly_report_markdown(report: dict) -> str:
    lines = [
        "# Weekly AI Report",
        f"**{report['week_start']} ~ {report['week_end']}**",
        f"Generated: {report['created_at'][:10]}",
        "",
    ]

    stats = report.get("stats", {})
    lines.append("## Weekly Stats")
    lines.append(f"- Articles: {stats.get('total', 0)}")
    lines.append(f"- Average importance: {stats.get('avg_importance', 0)}")
    lines.append("")

    sentiment = stats.get("sentiment", {})
    if sentiment:
        lines.append("**Sentiment**")
        for label, count in sentiment.items():
            lines.append(f"- {label}: {count}")
        lines.append("")

    focus = stats.get("focus_counts", {})
    if focus:
        lines.append("**Focus Areas**")
        for label, count in focus.items():
            lines.append(f"- {label}: {count}")
        lines.append("")

    trends = report.get("trends")
    if trends:
        lines.append("## Key Trends")
        for index, trend in enumerate(trends.get("key_trends", []), 1):
            lines.append(f"{index}. {trend}")
        lines.append("")

        lines.append("## Focus Commentary")
        lines.append(f"- Image/Video: {trends.get('image_video_trend', '-')}")
        lines.append(f"- Coding: {trends.get('coding_trend', '-')}")
        lines.append(f"- Ontology: {trends.get('ontology_trend', '-')}")
        lines.append("")

        lines.append("## Outlook")
        lines.append(trends.get("outlook", ""))
        lines.append("")

        actions = trends.get("action_items", [])
        if actions:
            lines.append("## Action Items")
            for item in actions:
                lines.append(f"- {item}")
            lines.append("")

    lines.append("## Top 10 Articles")
    for index, article in enumerate(report.get("top_articles", []), 1):
        stars = "*" * article.get("importance", 0)
        lines.append(f"{index}. {stars} [{article['title']}]({article['url']})")
        if article.get("summary"):
            lines.append(f"   > {article['summary']}")
    lines.append("")

    lines.append("---")
    lines.append("*Generated by AI News Radar*")
    return "\n".join(lines)


def get_latest_report() -> dict | None:
    reports = safe_read_json(REPORTS_PATH, [])
    if not reports:
        return None
    return max(reports, key=lambda item: item.get("week_start", ""))
