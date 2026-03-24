"""AI 뉴스레터 이메일 발행 — SMTP로 주간/일간 뉴스레터 자동 발송

.env 설정:
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=your_email@gmail.com
  SMTP_PASSWORD=your_app_password (Gmail: 앱 비밀번호)
  NEWSLETTER_RECIPIENTS=email1@example.com,email2@example.com
  NEWSLETTER_SENDER_NAME=AI News Radar
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import DATA_DIR, CATEGORIES
from ai.weekly_report import get_latest_report, export_weekly_report_markdown
from ai.briefing import FOCUS_AREAS
from utils.helpers import safe_read_json, safe_write_json, today_str, now_iso, log

BRIEFINGS_PATH = DATA_DIR / "briefings.json"
SEND_LOG_PATH = DATA_DIR / "newsletter_log.json"


def _get_smtp_config() -> dict | None:
    """SMTP 설정 로드"""
    host = os.getenv("SMTP_HOST", "")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")

    if not all([host, user, password]):
        return None

    return {"host": host, "port": port, "user": user, "password": password}


def _get_recipients() -> list[str]:
    """수신자 목록"""
    raw = os.getenv("NEWSLETTER_RECIPIENTS", "")
    if not raw:
        return []
    return [e.strip() for e in raw.split(",") if e.strip()]


def _briefing_to_html(briefing: dict) -> str:
    """브리핑을 HTML 이메일 본문으로 변환"""
    date = briefing.get("date", today_str())

    html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto; color: #e2e8f0; background: #0f172a; padding: 32px; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 style="color: #60a5fa; font-size: 24px; margin: 0;">📡 AI News Radar</h1>
            <p style="color: #94a3b8; font-size: 14px; margin-top: 4px;">일간 AI 뉴스 브리핑 — {date}</p>
        </div>
    """

    # 총평
    summary = briefing.get("summary", "")
    if summary:
        html += f"""
        <div style="background: rgba(96,165,250,0.1); border-left: 3px solid #60a5fa; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 24px;">
            <p style="margin: 0; color: #cbd5e1; font-size: 14px;">💡 {summary}</p>
        </div>
        """

    # TOP 기사
    top = briefing.get("top_articles", [])
    if isinstance(top, list):
        for i, item in enumerate(top[:5], 1):
            if not isinstance(item, dict):
                continue
            headline = item.get("headline", item.get("title", ""))
            why = item.get("why_important", item.get("summary", ""))

            html += f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; align-items: flex-start;">
                    <span style="background: #60a5fa; color: white; font-weight: 700; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; margin-right: 12px; flex-shrink: 0;">{i}</span>
                    <div>
                        <p style="margin: 0; font-weight: 600; font-size: 15px; color: #f1f5f9;">{headline}</p>
                        {"<p style='margin: 4px 0 0; font-size: 13px; color: #94a3b8;'>→ " + why + "</p>" if why else ""}
                    </div>
                </div>
            </div>
            """

    # 분야별 브리핑
    focus = briefing.get("focus_briefings", {})
    if focus:
        html += '<div style="margin-top: 24px;"><h3 style="color: #60a5fa; font-size: 16px;">🎯 관심 분야별</h3>'
        for area_id, area_data in focus.items():
            icon = area_data.get("icon", "📌")
            name = area_data.get("name", "")
            total = area_data.get("total_count", 0)
            html += f'<p style="color: #94a3b8; font-size: 13px; margin: 8px 0 4px;">{icon} <strong>{name}</strong> — {total}건</p>'
            for art in area_data.get("top_articles", [])[:2]:
                html += f'<p style="color: #cbd5e1; font-size: 13px; margin: 2px 0 2px 20px;">• {art.get("title", "")[:60]}</p>'
        html += '</div>'

    # 푸터
    html += """
        <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.06); text-align: center;">
            <p style="color: #64748b; font-size: 12px; margin: 0;">📡 AI News Radar — SoDam AI Studio</p>
        </div>
    </div>
    """

    return html


def _weekly_report_to_html(report: dict) -> str:
    """주간 리포트를 HTML 이메일로 변환"""
    md_content = export_weekly_report_markdown(report)

    # 간단한 Markdown → HTML 변환
    html_body = md_content
    html_body = html_body.replace("# ", "<h1 style='color:#60a5fa'>").replace("\n", "</h1>\n", 1) if "# " in html_body else html_body

    lines = md_content.split("\n")
    html_lines = []
    for line in lines:
        if line.startswith("# "):
            html_lines.append(f"<h2 style='color:#60a5fa;font-size:18px'>{line[2:]}</h2>")
        elif line.startswith("## "):
            html_lines.append(f"<h3 style='color:#93c5fd;font-size:16px'>{line[3:]}</h3>")
        elif line.startswith("#### "):
            html_lines.append(f"<h4 style='color:#cbd5e1;font-size:14px'>{line[5:]}</h4>")
        elif line.startswith("- "):
            html_lines.append(f"<li style='color:#cbd5e1;font-size:13px'>{line[2:]}</li>")
        elif line.startswith("**") and line.endswith("**"):
            html_lines.append(f"<p style='color:#f1f5f9;font-weight:600'>{line[2:-2]}</p>")
        elif line.strip():
            html_lines.append(f"<p style='color:#94a3b8;font-size:13px'>{line}</p>")

    body = "\n".join(html_lines)

    return f"""
    <div style="font-family: -apple-system, sans-serif; max-width: 600px; margin: 0 auto; color: #e2e8f0; background: #0f172a; padding: 32px; border-radius: 16px;">
        {body}
        <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.06); text-align: center;">
            <p style="color: #64748b; font-size: 12px;">📡 AI News Radar 주간 인텔리전스 리포트 — SoDam AI Studio</p>
        </div>
    </div>
    """


def send_newsletter(newsletter_type: str = "daily") -> dict:
    """뉴스레터 이메일 발송

    Args:
        newsletter_type: "daily" (일간 브리핑) 또는 "weekly" (주간 리포트)

    Returns:
        {"success": bool, "sent_to": int, "error": str}
    """
    smtp_config = _get_smtp_config()
    if not smtp_config:
        return {"success": False, "sent_to": 0, "error": "SMTP 설정이 .env에 없습니다 (SMTP_HOST, SMTP_USER, SMTP_PASSWORD)"}

    recipients = _get_recipients()
    if not recipients:
        return {"success": False, "sent_to": 0, "error": "수신자가 없습니다 (NEWSLETTER_RECIPIENTS)"}

    sender_name = os.getenv("NEWSLETTER_SENDER_NAME", "AI News Radar")

    # 콘텐츠 생성
    if newsletter_type == "daily":
        briefings = safe_read_json(BRIEFINGS_PATH, [])
        today_briefing = next((b for b in briefings if b.get("date") == today_str()), None)
        if not today_briefing:
            return {"success": False, "sent_to": 0, "error": "오늘의 브리핑이 없습니다"}
        subject = f"📡 AI 뉴스 브리핑 — {today_str()}"
        html_body = _briefing_to_html(today_briefing)
    elif newsletter_type == "weekly":
        report = get_latest_report()
        if not report:
            return {"success": False, "sent_to": 0, "error": "주간 리포트가 없습니다"}
        subject = f"📊 주간 AI 인텔리전스 리포트 — {report['week_start']}~{report['week_end']}"
        html_body = _weekly_report_to_html(report)
    else:
        return {"success": False, "sent_to": 0, "error": f"지원하지 않는 유형: {newsletter_type}"}

    # 이메일 발송
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{sender_name} <{smtp_config['user']}>"
        msg["To"] = ", ".join(recipients)

        # HTML + 텍스트 fallback
        text_part = MIMEText(subject, "plain", "utf-8")
        html_part = MIMEText(html_body, "html", "utf-8")
        msg.attach(text_part)
        msg.attach(html_part)

        with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
            server.starttls()
            server.login(smtp_config["user"], smtp_config["password"])
            server.sendmail(smtp_config["user"], recipients, msg.as_string())

        # 발송 로그
        send_log = safe_read_json(SEND_LOG_PATH, [])
        send_log.append({
            "type": newsletter_type,
            "subject": subject,
            "recipients": len(recipients),
            "sent_at": now_iso(),
        })
        safe_write_json(SEND_LOG_PATH, send_log)

        log(f"[뉴스레터] {newsletter_type} 발송 완료 → {len(recipients)}명")
        return {"success": True, "sent_to": len(recipients)}

    except Exception as e:
        log(f"[뉴스레터 오류] {e}")
        return {"success": False, "sent_to": 0, "error": str(e)}


def is_smtp_configured() -> bool:
    """SMTP 설정 여부"""
    return _get_smtp_config() is not None


def get_newsletter_log(limit: int = 10) -> list[dict]:
    """발송 히스토리"""
    logs = safe_read_json(SEND_LOG_PATH, [])
    return logs[-limit:]
