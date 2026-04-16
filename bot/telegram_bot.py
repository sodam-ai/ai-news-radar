"""텔레그램 봇 — AI News Radar 뉴스 요약+브리핑+AI 채팅

사용법:
  1. @BotFather에서 봇 생성 후 토큰 발급
  2. .env에 TELEGRAM_BOT_TOKEN=your_token 추가
  3. python -m bot.telegram_bot 으로 실행

명령어:
  /start      — 시작 메시지
  /today      — 오늘의 브리핑
  /top        — 중요도 TOP 5 뉴스
  /search 키워드 — 뉴스 검색
  /ask 질문    — AI 뉴스 채팅
  /stats      — 수집 통계
  /help       — 도움말
"""
import os
import sys
import logging

# 프로젝트 루트를 path에 추가 (bot/ 하위에서 실행해도 import 가능)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from config import DATA_DIR
from utils.helpers import safe_read_json, safe_write_json, today_str, now_iso, log
from ai.chat import chat as ai_chat
from ai.model_router import get_active_provider
from utils.bookmarks import get_bookmarks

logging.basicConfig(
    format="%(asctime)s [TG-BOT] %(levelname)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

ARTICLES_PATH = DATA_DIR / "articles.json"
BRIEFINGS_PATH = DATA_DIR / "briefings.json"

# ── 최대 메시지 길이 (텔레그램 제한 4096자) ──
MAX_MSG = 4000


def _truncate(text: str, limit: int = MAX_MSG) -> str:
    if len(text) <= limit:
        return text
    return text[:limit - 3] + "..."


# ── 명령어 핸들러 ──

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📡 *AI News Radar 봇*에 오신 걸 환영합니다!\n\n"
        "명령어:\n"
        "/today — 오늘의 AI 브리핑\n"
        "/top — 중요도 TOP 5 뉴스\n"
        "/search 키워드 — 뉴스 검색\n"
        "/ask 질문 — AI에게 뉴스 질문\n"
        "/alert — 워치리스트 조회\n"
        "/alert 키워드 — 워치리스트 추가\n"
        "/bookmark — 북마크 기사 보기\n"
        "/stats — 수집 통계\n"
        "/help — 도움말",
        parse_mode="Markdown",
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_start(update, context)


async def cmd_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """오늘의 브리핑 표시"""
    briefings = safe_read_json(BRIEFINGS_PATH, [])
    today = today_str()
    briefing = next((b for b in briefings if b.get("date") == today), None)

    if not briefing:
        # 가장 최근 브리핑
        if briefings:
            briefing = max(briefings, key=lambda b: b.get("date", ""))
        else:
            await update.message.reply_text("아직 브리핑이 없습니다. 웹 대시보드에서 브리핑을 먼저 생성해주세요.")
            return

    lines = [f"📋 *AI 브리핑* ({briefing.get('date', '')})\n"]

    summary = briefing.get("summary", "")
    if summary:
        lines.append(f"_{summary}_\n")

    top = briefing.get("top_articles", [])
    if isinstance(top, list):
        for i, item in enumerate(top, 1):
            if isinstance(item, dict):
                headline = item.get("headline", item.get("title", ""))
                why = item.get("why_important", item.get("summary", ""))
                lines.append(f"*{i}.* {headline}")
                if why:
                    lines.append(f"   → {why}")
                lines.append("")

    await update.message.reply_text(_truncate("\n".join(lines)), parse_mode="Markdown")


async def cmd_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """중요도 TOP 5 뉴스"""
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]
    processed.sort(key=lambda x: x.get("importance", 0), reverse=True)
    top5 = processed[:5]

    if not top5:
        await update.message.reply_text("아직 수집된 뉴스가 없습니다.")
        return

    lines = ["📰 *중요도 TOP 5 뉴스*\n"]
    for i, a in enumerate(top5, 1):
        stars = "⭐" * a.get("importance", 0)
        sentiment = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment", ""), "")
        lines.append(f"*{i}.* {stars} {sentiment}")
        lines.append(f"[{a['title']}]({a['url']})")
        summary = a.get("summary_text", "")
        if summary:
            lines.append(f"_{summary[:100]}_")
        lines.append("")

    await update.message.reply_text(
        _truncate("\n".join(lines)),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """뉴스 검색: /search 키워드"""
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text("사용법: /search 키워드\n예: /search Claude")
        return

    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    q = query.lower()
    results = [
        a for a in processed
        if q in a.get("title", "").lower()
        or q in a.get("summary_text", "").lower()
        or any(q in t.lower() for t in a.get("tags", []))
    ]

    if not results:
        await update.message.reply_text(f"'{query}'에 대한 검색 결과가 없습니다.")
        return

    lines = [f"🔍 *'{query}' 검색 결과* ({len(results)}개)\n"]
    for a in results[:10]:
        sentiment = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment", ""), "")
        lines.append(f"{sentiment} [{a['title']}]({a['url']})")
        lines.append("")

    await update.message.reply_text(
        _truncate("\n".join(lines)),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def cmd_ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI 뉴스 채팅: /ask 질문"""
    question = " ".join(context.args) if context.args else ""
    if not question:
        await update.message.reply_text("사용법: /ask 질문\n예: /ask 이번 주 Claude 관련 뉴스 알려줘")
        return

    if not get_active_provider():
        await update.message.reply_text("LLM API 키가 설정되지 않았습니다.")
        return

    await update.message.reply_text("🤔 뉴스를 분석하고 답변을 생성 중...")

    try:
        response = ai_chat(question)
        await update.message.reply_text(_truncate(response))
    except Exception as e:
        logger.error(f"AI 채팅 오류: {e}")
        await update.message.reply_text(f"답변 생성 중 오류: {e}")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """수집 통계"""
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed")]
    primary = [a for a in processed if a.get("is_primary", True)]

    lines = [
        "📊 *AI News Radar 통계*\n",
        f"총 기사: {len(articles)}개",
        f"AI 처리 완료: {len(processed)}개",
        f"대표 기사: {len(primary)}개",
    ]

    # 카테고리별 분포
    cat_count = {}
    for a in primary:
        cat = a.get("category", "other")
        cat_count[cat] = cat_count.get(cat, 0) + 1
    if cat_count:
        lines.append("\n*카테고리 분포:*")
        for cat, cnt in sorted(cat_count.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  {cat}: {cnt}개")

    # 감성 분포
    sent_count = {}
    for a in primary:
        s = a.get("sentiment", "neutral")
        sent_count[s] = sent_count.get(s, 0) + 1
    if sent_count:
        emojis = {"positive": "😊", "negative": "😠", "neutral": "😐"}
        lines.append("\n*감성 분포:*")
        for s, cnt in sent_count.items():
            lines.append(f"  {emojis.get(s, '')} {s}: {cnt}개")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/alert [키워드] — 워치리스트 조회 또는 키워드 추가"""
    keyword = " ".join(context.args).strip() if context.args else ""
    watchlist_path = DATA_DIR / "watchlist.json"

    if not keyword:
        watchlist = safe_read_json(watchlist_path, [])
        active = [w.get("keyword", "") for w in watchlist if w.get("is_active")]
        if active:
            items = "\n".join([f"  • `{k}`" for k in active])
            await update.message.reply_text(
                f"📋 *워치리스트* ({len(active)}개)\n{items}\n\n추가: /alert 키워드",
                parse_mode="Markdown",
            )
        else:
            await update.message.reply_text("워치리스트가 비어있습니다.\n추가: /alert 키워드\n예: /alert Claude 5")
        return

    watchlist = safe_read_json(watchlist_path, [])
    if any(w.get("keyword", "").lower() == keyword.lower() for w in watchlist):
        await update.message.reply_text(f"이미 등록된 키워드입니다: `{keyword}`", parse_mode="Markdown")
        return

    watchlist.append({"keyword": keyword, "is_active": True, "created_at": now_iso()})
    safe_write_json(watchlist_path, watchlist)
    await update.message.reply_text(f"✅ `{keyword}` 워치리스트 등록 완료!\n해당 키워드가 포함된 기사 수집 시 자동 알림됩니다.", parse_mode="Markdown")


async def cmd_bookmark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/bookmark — 북마크한 기사 목록"""
    bookmarks = get_bookmarks()
    if not bookmarks:
        await update.message.reply_text(
            "북마크한 기사가 없습니다.\n웹 대시보드 뉴스피드에서 ☆ 버튼으로 북마크하세요."
        )
        return

    arts_map = {a["id"]: a for a in safe_read_json(ARTICLES_PATH, [])}
    lines = [f"⭐ *북마크 기사* ({len(bookmarks)}개)\n"]
    for bm in reversed(bookmarks[:10]):
        a = arts_map.get(bm.get("article_id", ""))
        if not a:
            continue
        memo = bm.get("memo", "")
        lines.append(f"[{a['title']}]({a['url']})")
        if memo:
            lines.append(f"  📝 _{memo}_")
        lines.append("")

    await update.message.reply_text(
        _truncate("\n".join(lines)),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """일반 메시지 → AI 채팅으로 처리"""
    text = update.message.text
    if not text:
        return

    if not get_active_provider():
        await update.message.reply_text("LLM API 키가 설정되지 않았습니다. /help 로 명령어를 확인하세요.")
        return

    await update.message.reply_text("🤔 답변 생성 중...")
    try:
        response = ai_chat(text)
        await update.message.reply_text(_truncate(response))
    except Exception as e:
        await update.message.reply_text(f"오류: {e}")


def run_bot():
    """텔레그램 봇 실행"""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN이 .env에 설정되지 않았습니다.")
        print("   @BotFather에서 봇을 만들고 토큰을 .env에 추가하세요.")
        print("   예: TELEGRAM_BOT_TOKEN=123456:ABC-DEF...")
        return

    app = Application.builder().token(token).build()

    # 명령어 등록
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("today", cmd_today))
    app.add_handler(CommandHandler("top", cmd_top))
    app.add_handler(CommandHandler("search", cmd_search))
    app.add_handler(CommandHandler("ask", cmd_ask))
    app.add_handler(CommandHandler("alert", cmd_alert))
    app.add_handler(CommandHandler("bookmark", cmd_bookmark))
    app.add_handler(CommandHandler("stats", cmd_stats))

    # 일반 메시지 → AI 채팅
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 AI News Radar 텔레그램 봇 시작!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run_bot()
