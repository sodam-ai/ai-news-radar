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
# Threads 어댑터 (Meta Threads API)
# ═══════════════════════════════════════════════

def post_to_threads(text: str, image_path: str = None) -> dict:
    """Threads에 포스트 (Meta Threads Publishing API)

    필요 설정:
      THREADS_ACCESS_TOKEN — Meta 개발자 포털에서 발급
      THREADS_USER_ID — Threads 사용자 ID

    발급 방법:
      1. developers.facebook.com → 앱 만들기 → Threads API 추가
      2. Access Token 발급 (threads_manage_posts 권한)
      3. 사용자 ID 확인: GET https://graph.threads.net/v1.0/me
    """
    access_token = os.getenv("THREADS_ACCESS_TOKEN", "")
    user_id = os.getenv("THREADS_USER_ID", "")

    if not access_token or not user_id:
        return {"success": False, "error": "THREADS_ACCESS_TOKEN 또는 THREADS_USER_ID가 .env에 설정되지 않았습니다"}

    base_url = "https://graph.threads.net/v1.0"

    try:
        # Step 1: 미디어 컨테이너 생성
        create_params = {
            "text": text[:500],
            "access_token": access_token,
        }

        if image_path and os.path.exists(image_path):
            # 이미지 포스트: 이미지 URL 필요 (로컬 파일 직접 업로드 불가)
            # 로컬 파일은 텍스트 전용으로 게시
            create_params["media_type"] = "TEXT"
        else:
            create_params["media_type"] = "TEXT"

        resp = req.post(
            f"{base_url}/{user_id}/threads",
            data=create_params,
            timeout=30,
        )
        result = resp.json()

        if "id" not in result:
            return {"success": False, "error": result.get("error", {}).get("message", str(result))}

        container_id = result["id"]

        # Step 2: 게시
        publish_resp = req.post(
            f"{base_url}/{user_id}/threads_publish",
            data={"creation_id": container_id, "access_token": access_token},
            timeout=30,
        )
        publish_result = publish_resp.json()

        if "id" in publish_result:
            post_id = publish_result["id"]
            log(f"[Threads] 포스트 성공: {post_id}")
            return {"success": True, "platform": "Threads", "post_id": post_id}
        else:
            return {"success": False, "error": publish_result.get("error", {}).get("message", str(publish_result))}

    except Exception as e:
        log(f"[Threads 오류] {e}")
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════
# Instagram 어댑터 (Meta Graph API)
# ═══════════════════════════════════════════════

def post_to_instagram(text: str, image_path: str = None) -> dict:
    """Instagram에 이미지 포스트 (Meta Graph API)

    필요 설정:
      INSTAGRAM_ACCESS_TOKEN — Meta 개발자 포털에서 발급
      INSTAGRAM_ACCOUNT_ID — Instagram 비즈니스/크리에이터 계정 ID
      INSTAGRAM_IMAGE_HOST — 이미지를 호스팅할 공개 URL 베이스 (선택)

    발급 방법:
      1. Facebook 페이지 + Instagram 비즈니스 계정 연결
      2. developers.facebook.com → 앱 만들기 → Instagram Graph API 추가
      3. Access Token 발급 (instagram_basic, instagram_content_publish 권한)
      4. 계정 ID: GET /me/accounts → instagram_business_account.id

    주의: Instagram API는 공개 URL의 이미지만 업로드 가능.
    로컬 파일은 별도 호스팅(예: Imgur, Cloudinary)이 필요합니다.
    """
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "")

    if not access_token or not account_id:
        return {"success": False, "error": "INSTAGRAM_ACCESS_TOKEN 또는 INSTAGRAM_ACCOUNT_ID가 .env에 설정되지 않았습니다"}

    base_url = "https://graph.facebook.com/v21.0"

    try:
        # Instagram은 이미지 필수 (텍스트 전용 포스트 불가)
        if not image_path or not os.path.exists(image_path):
            return {"success": False, "error": "Instagram은 이미지가 필수입니다"}

        # 이미지를 공개 URL로 호스팅 (간이 방법: Imgur 업로드)
        image_url = _upload_image_for_instagram(image_path)
        if not image_url:
            return {"success": False, "error": "이미지 호스팅 실패. IMGUR_CLIENT_ID를 .env에 설정하세요"}

        # Step 1: 미디어 컨테이너 생성
        create_resp = req.post(
            f"{base_url}/{account_id}/media",
            data={
                "image_url": image_url,
                "caption": text[:2200],
                "access_token": access_token,
            },
            timeout=30,
        )
        create_result = create_resp.json()

        if "id" not in create_result:
            return {"success": False, "error": create_result.get("error", {}).get("message", str(create_result))}

        container_id = create_result["id"]

        # Step 2: 게시
        import time
        time.sleep(5)  # Meta 서버 이미지 처리 대기

        publish_resp = req.post(
            f"{base_url}/{account_id}/media_publish",
            data={"creation_id": container_id, "access_token": access_token},
            timeout=30,
        )
        publish_result = publish_resp.json()

        if "id" in publish_result:
            post_id = publish_result["id"]
            log(f"[Instagram] 포스트 성공: {post_id}")
            return {"success": True, "platform": "Instagram", "post_id": post_id}
        else:
            return {"success": False, "error": publish_result.get("error", {}).get("message", str(publish_result))}

    except Exception as e:
        log(f"[Instagram 오류] {e}")
        return {"success": False, "error": str(e)}


def _upload_image_for_instagram(image_path: str) -> str | None:
    """이미지를 Imgur에 업로드하여 공개 URL 반환 (Instagram API용)"""
    client_id = os.getenv("IMGUR_CLIENT_ID", "")
    if not client_id:
        return None

    try:
        with open(image_path, "rb") as f:
            resp = req.post(
                "https://api.imgur.com/3/image",
                headers={"Authorization": f"Client-ID {client_id}"},
                files={"image": f},
                timeout=30,
            )
        result = resp.json()
        if result.get("success"):
            return result["data"]["link"]
    except Exception as e:
        log(f"[Imgur 업로드 오류] {e}")
    return None


# ═══════════════════════════════════════════════
# 통합 포스터
# ═══════════════════════════════════════════════

PLATFORM_ADAPTERS = {
    "x": {"name": "X (Twitter)", "icon": "🐦", "func": post_to_x, "max_text": 280, "env_keys": ["X_API_KEY"]},
    "telegram": {"name": "Telegram", "icon": "📨", "func": post_to_telegram, "max_text": 1024, "env_keys": ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHANNEL_ID"]},
    "discord": {"name": "Discord", "icon": "💬", "func": post_to_discord, "max_text": 2000, "env_keys": ["DISCORD_WEBHOOK_URL"]},
    "threads": {"name": "Threads", "icon": "🧵", "func": post_to_threads, "max_text": 500, "env_keys": ["THREADS_ACCESS_TOKEN", "THREADS_USER_ID"]},
    "instagram": {"name": "Instagram", "icon": "📸", "func": post_to_instagram, "max_text": 2200, "env_keys": ["INSTAGRAM_ACCESS_TOKEN", "INSTAGRAM_ACCOUNT_ID"]},
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
