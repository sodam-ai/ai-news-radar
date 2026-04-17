"""Desktop alerts for watchlist hits and high-importance articles."""

from db.database import get_active_keywords, get_primary_articles, mark_alerted, get_alert_log
from utils.helpers import log, now_iso

IMPORTANCE_ALERT_THRESHOLD = 5


def _show_desktop_notification(title: str, message: str):
    """Best-effort desktop notification."""
    try:
        from plyer import notification

        notification.notify(
            title=title,
            message=message[:256],
            app_name="AI News Radar",
            timeout=8,
        )
    except Exception as exc:
        log(f"[alert:notify-error] {exc}")


def _already_alerted(article_id: str) -> bool:
    return article_id in get_alert_log(limit=500)


def _mark_alerted(article_id: str):
    mark_alerted(article_id, now_iso())


def _send_telegram_notification(article: dict, matched_keywords: list[str]):
    """텔레그램으로 알림 전송 (TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID 필요)"""
    import os
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return

    try:
        import httpx
        importance = article.get("importance", 0)
        stars = "⭐" * importance
        if matched_keywords:
            header = f"🔔 *워치리스트 알림*: `{', '.join(matched_keywords)}`"
        else:
            header = f"🚨 *중요 AI 뉴스* {stars}"
        summary = article.get("summary_text", "")[:150]
        text = (
            f"{header}\n\n"
            f"[{article.get('title', '')}]({article.get('url', '')})\n"
            + (f"\n_{summary}_" if summary else "")
        )
        httpx.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text[:4000],
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            },
            timeout=10,
        )
    except Exception as exc:
        log(f"[alert:telegram-error] {exc}")


def check_and_alert(articles: list[dict] = None) -> list[dict]:
    """워치리스트 키워드 매칭 또는 고중요도 기사에 알림."""
    active_keywords = get_active_keywords()
    if not active_keywords:
        return []

    if articles is None:
        articles = get_primary_articles(limit=500)

    alerted = []

    for article in articles:
        article_id = article.get("id", "")
        if not article.get("ai_processed") or not article_id or _already_alerted(article_id):
            continue

        title = article.get("title", "").lower()
        summary = article.get("summary_text", "").lower()
        tags = " ".join(article.get("tags", [])).lower()
        text = f"{title} {summary} {tags}"

        matched_keywords = [keyword for keyword in active_keywords if keyword in text]
        is_high_importance = article.get("importance", 0) >= IMPORTANCE_ALERT_THRESHOLD

        if not matched_keywords and not is_high_importance:
            continue

        importance_marks = "*" * article.get("importance", 0)
        if matched_keywords:
            notify_title = f"AI News Alert: {', '.join(matched_keywords)}"
        else:
            notify_title = f"AI News Alert {importance_marks}"

        notify_message = article.get("title", "")[:200]
        _show_desktop_notification(notify_title, notify_message)
        _send_telegram_notification(article, matched_keywords)
        _mark_alerted(article_id)

        alert_entry = {
            "article_id": article_id,
            "title": article.get("title"),
            "matched_keywords": matched_keywords,
            "importance": article.get("importance", 0),
            "alerted_at": now_iso(),
        }
        alerted.append(alert_entry)
        log(f"[alert:sent] {notify_title}: {article.get('title', '')[:50]}")

    return alerted


def get_alert_history(limit: int = 20) -> list[str]:
    return get_alert_log(limit=limit)
