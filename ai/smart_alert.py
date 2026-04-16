"""Desktop alerts for watchlist hits and high-importance articles."""

from config import DATA_DIR
from utils.helpers import log, now_iso, safe_read_json, safe_update_json

WATCHLIST_PATH = DATA_DIR / "watchlist.json"
ARTICLES_PATH = DATA_DIR / "articles.json"
ALERT_LOG_PATH = DATA_DIR / "alert_log.json"

IMPORTANCE_ALERT_THRESHOLD = 5
MAX_ALERT_LOG_ENTRIES = 500


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
    alert_log = safe_read_json(ALERT_LOG_PATH, [])
    return article_id in alert_log


def _mark_alerted(article_id: str):
    def updater(current: list[str]):
        updated = [item for item in current if item != article_id]
        updated.append(article_id)
        if len(updated) > MAX_ALERT_LOG_ENTRIES:
            updated = updated[-MAX_ALERT_LOG_ENTRIES:]
        return updated

    safe_update_json(ALERT_LOG_PATH, updater, default=[])


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
    """Show alerts for matching keywords or highly important articles."""
    if articles is None:
        articles = safe_read_json(ARTICLES_PATH, [])

    watchlist = safe_read_json(WATCHLIST_PATH, [])
    active_keywords = [
        item["keyword"].lower()
        for item in watchlist
        if item.get("is_active") and item.get("keyword")
    ]
    if not active_keywords:
        return []

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
    alert_log = safe_read_json(ALERT_LOG_PATH, [])
    return alert_log[-limit:]
