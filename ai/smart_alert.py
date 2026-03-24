"""스마트 키워드 알림 — 중요 뉴스 감지 시 즉시 데스크톱 알림

워치리스트 키워드 + 커스텀 알림 규칙에 매칭되는 기사가 수집되면
Windows 네이티브 토스트 알림을 표시합니다.
"""
import os
from config import DATA_DIR
from utils.helpers import safe_read_json, safe_write_json, now_iso, log

WATCHLIST_PATH = DATA_DIR / "watchlist.json"
ARTICLES_PATH = DATA_DIR / "articles.json"
ALERT_LOG_PATH = DATA_DIR / "alert_log.json"

# 중요도 기반 알림 (별도 키워드 없이 중요도 높으면 알림)
IMPORTANCE_ALERT_THRESHOLD = 5


def _show_desktop_notification(title: str, message: str):
    """데스크톱 알림 표시"""
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message[:256],
            app_name="AI News Radar",
            timeout=8,
        )
    except Exception as e:
        log(f"[알림 오류] {e}")


def _already_alerted(article_id: str) -> bool:
    """이미 알림을 보낸 기사인지 확인"""
    alert_log = safe_read_json(ALERT_LOG_PATH, [])
    return article_id in alert_log


def _mark_alerted(article_id: str):
    """알림 보낸 기사 기록"""
    alert_log = safe_read_json(ALERT_LOG_PATH, [])
    alert_log.append(article_id)
    # 최근 500개만 유지
    if len(alert_log) > 500:
        alert_log = alert_log[-500:]
    safe_write_json(ALERT_LOG_PATH, alert_log)


def check_and_alert(articles: list[dict] = None) -> list[dict]:
    """새 기사에서 알림 조건 확인 → 매칭되면 데스크톱 알림.

    Returns:
        알림이 발생한 기사 목록
    """
    if articles is None:
        articles = safe_read_json(ARTICLES_PATH, [])

    # 워치리스트 키워드 로드
    watchlist = safe_read_json(WATCHLIST_PATH, [])
    active_keywords = [w["keyword"].lower() for w in watchlist if w.get("is_active")]

    if not active_keywords:
        return []

    alerted = []

    for article in articles:
        if not article.get("ai_processed"):
            continue
        if _already_alerted(article.get("id", "")):
            continue

        title = article.get("title", "").lower()
        summary = article.get("summary_text", "").lower()
        tags = " ".join(article.get("tags", [])).lower()
        text = f"{title} {summary} {tags}"

        matched_keywords = []
        for kw in active_keywords:
            if kw in text:
                matched_keywords.append(kw)

        # 중요도 5 기사는 키워드 무관하게 알림
        is_high_importance = article.get("importance", 0) >= IMPORTANCE_ALERT_THRESHOLD

        if matched_keywords or is_high_importance:
            # 알림 메시지 구성
            importance = "⭐" * article.get("importance", 0)
            if matched_keywords:
                kw_text = ", ".join(matched_keywords)
                notify_title = f"📡 키워드 감지: {kw_text}"
            else:
                notify_title = f"📡 중요 뉴스 감지 {importance}"

            notify_message = article.get("title", "")[:200]

            _show_desktop_notification(notify_title, notify_message)
            _mark_alerted(article.get("id", ""))

            alerted.append({
                "article_id": article.get("id"),
                "title": article.get("title"),
                "matched_keywords": matched_keywords,
                "importance": article.get("importance", 0),
                "alerted_at": now_iso(),
            })

            log(f"[스마트 알림] {notify_title}: {article.get('title', '')[:50]}")

    return alerted


def get_alert_history(limit: int = 20) -> list[dict]:
    """최근 알림 히스토리"""
    alert_log = safe_read_json(ALERT_LOG_PATH, [])
    return alert_log[-limit:]
