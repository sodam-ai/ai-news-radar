"""SNS 자동 포스터 — 어댑터 패턴으로 각 플랫폼에 카드 뉴스 업로드

지원 플랫폼:
  - X (Twitter): tweepy 라이브러리
  - Telegram: python-telegram-bot (기존 봇 활용)
  - Discord: Webhook URL (간단, 인증 불필요)

.env 설정:
  # X (Twitter)
  X_API_KEY=...
  X_API_SECRET=...
  X_ACCESS_TOKEN=...
  X_ACCESS_SECRET=...

  # Telegram (기존 설정 재사용)
  TELEGRAM_BOT_TOKEN=...
  TELEGRAM_CHANNEL_ID=@your_channel_or_chat_id

  # Discord
  DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
"""
import os
import json
import requests as req
from pathlib import Path

from config import CATEGORIES
from utils.helpers import log

# ── 포스트 텍스트 생성 ──

def _make_post_text(article: dict, max_length: int = 280) -> str:
    """SNS 포스트 텍스트 생성 (플랫폼별 길이 제한 대응)"""
    title = article.get("title", "")
    url = article.get("url", "")
    category = CATEGORIES.get(article.get("category", ""), "AI")
    sentiment = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(article.get("sentiment", ""), "")
    importance = "⭐" * article.get("importance", 0)
    tags = article.get("tags", [])[:3]
    hashtags = " ".join([f"#{t.replace(' ', '_')}" for t in tags])

    text = f"{importance} {sentiment} [{category}]\n{title}\n\n{hashtags}\n\n{url}\n\n📡 AI News Radar"

    if len(text) > max_length:
        # 요약 없이 제목+URL만
        text = f"{importance} [{category}]\n{title[:100]}...\n{url}\n\n📡 AI News Radar"

    return text[:max_length]


def _make_briefing_text(briefing: dict) -> str:
    """브리핑 포스트 텍스트"""
    date = briefing.get("date", "")
    lines = [f"📡 AI 뉴스 브리핑 — {date}\n"]

    summary = briefing.get("summary", "")
    if summary:
        lines.append(f"💡 {summary[:100]}\n")

    top = briefing.get("top_articles", [])
    for i, item in enumerate(top[:5], 1):
        if isinstance(item, dict):
            headline = item.get("headline", item.get("title", ""))
            lines.append(f"{i}. {headline}")

    lines.append("\n#AI뉴스 #AINews #인공지능\n📡 AI News Radar")
    return "\n".join(lines)


# ═══════════════════════════════════════════════
# X (Twitter) 어댑터
# ═══════════════════════════════════════════════

def post_to_x(text: str, image_path: str = None) -> dict:
    """X (Twitter)에 포스트 업로드"""
    try:
        import tweepy
    except ImportError:
        return {"success": False, "error": "tweepy 미설치. pip install tweepy"}

    api_key = os.getenv("X_API_KEY", "")
    api_secret = os.getenv("X_API_SECRET", "")
    access_token = os.getenv("X_ACCESS_TOKEN", "")
    access_secret = os.getenv("X_ACCESS_SECRET", "")

    if not all([api_key, api_secret, access_token, access_secret]):
        return {"success": False, "error": "X API 키가 .env에 설정되지 않았습니다"}

    try:
        # v1.1 API for media upload
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
        api_v1 = tweepy.API(auth)

        # v2 Client for tweet
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )

        media_id = None
        if image_path and os.path.exists(image_path):
            media = api_v1.media_upload(image_path)
            media_id = media.media_id

        response = client.create_tweet(
            text=text[:280],
            media_ids=[media_id] if media_id else None,
        )
        tweet_id = response.data["id"]
        log(f"[X] 포스트 성공: {tweet_id}")
        return {"success": True, "platform": "X", "post_id": tweet_id}

    except Exception as e:
        log(f"[X 오류] {e}")
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════
# Telegram 어댑터
# ═══════════════════════════════════════════════

def post_to_telegram(text: str, image_path: str = None) -> dict:
    """Telegram 채널/그룹에 포스트"""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID", "")

    if not token or not chat_id:
        return {"success": False, "error": "TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHANNEL_ID가 .env에 설정되지 않았습니다"}

    base_url = f"https://api.telegram.org/bot{token}"

    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                resp = req.post(
                    f"{base_url}/sendPhoto",
                    data={"chat_id": chat_id, "caption": text[:1024], "parse_mode": "HTML"},
                    files={"photo": photo},
                    timeout=30,
                )
        else:
            resp = req.post(
                f"{base_url}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                timeout=30,
            )

        result = resp.json()
        if result.get("ok"):
            msg_id = result["result"]["message_id"]
            log(f"[Telegram] 포스트 성공: {msg_id}")
            return {"success": True, "platform": "Telegram", "post_id": msg_id}
        else:
            return {"success": False, "error": result.get("description", "Unknown error")}

    except Exception as e:
        log(f"[Telegram 오류] {e}")
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════
# Discord 어댑터
# ═══════════════════════════════════════════════

def post_to_discord(text: str, image_path: str = None) -> dict:
    """Discord Webhook으로 포스트"""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "")

    if not webhook_url:
        return {"success": False, "error": "DISCORD_WEBHOOK_URL이 .env에 설정되지 않았습니다"}

    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                resp = req.post(
                    webhook_url,
                    data={"content": text[:2000]},
                    files={"file": (os.path.basename(image_path), f, "image/png")},
                    timeout=30,
                )
        else:
            resp = req.post(
                webhook_url,
                json={"content": text[:2000]},
                timeout=30,
            )

        if resp.status_code in (200, 204):
            log(f"[Discord] 포스트 성공")
            return {"success": True, "platform": "Discord"}
        else:
            return {"success": False, "error": f"HTTP {resp.status_code}: {resp.text[:100]}"}

    except Exception as e:
        log(f"[Discord 오류] {e}")
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════
# 통합 포스터
# ═══════════════════════════════════════════════

PLATFORM_ADAPTERS = {
    "x": {"name": "X (Twitter)", "icon": "🐦", "func": post_to_x, "max_text": 280, "env_keys": ["X_API_KEY"]},
    "telegram": {"name": "Telegram", "icon": "📨", "func": post_to_telegram, "max_text": 1024, "env_keys": ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHANNEL_ID"]},
    "discord": {"name": "Discord", "icon": "💬", "func": post_to_discord, "max_text": 2000, "env_keys": ["DISCORD_WEBHOOK_URL"]},
}


def get_available_platforms() -> list[dict]:
    """설정된 (사용 가능한) SNS 플랫폼 목록"""
    result = []
    for pid, info in PLATFORM_ADAPTERS.items():
        configured = all(os.getenv(k, "") for k in info["env_keys"])
        result.append({
            "id": pid,
            "name": info["name"],
            "icon": info["icon"],
            "configured": configured,
        })
    return result


def post_article(article: dict, platforms: list[str], image_path: str = None) -> list[dict]:
    """기사를 선택한 플랫폼들에 동시 포스트"""
    results = []
    for pid in platforms:
        adapter = PLATFORM_ADAPTERS.get(pid)
        if not adapter:
            results.append({"platform": pid, "success": False, "error": "Unknown platform"})
            continue

        text = _make_post_text(article, adapter["max_text"])
        result = adapter["func"](text, image_path)
        results.append(result)

    return results


def post_briefing(briefing: dict, platforms: list[str], image_path: str = None) -> list[dict]:
    """브리핑을 선택한 플랫폼들에 포스트"""
    results = []
    text = _make_briefing_text(briefing)

    for pid in platforms:
        adapter = PLATFORM_ADAPTERS.get(pid)
        if not adapter:
            continue

        post_text = text[:adapter["max_text"]]
        result = adapter["func"](post_text, image_path)
        results.append(result)

    return results
