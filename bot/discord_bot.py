"""Discord 봇 — AI News Radar
보안: 토큰 환경변수 전용, 입력 길이 제한
실행: .venv/Scripts/python -m bot.discord_bot
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

import discord
from discord.ext import commands

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
if not DISCORD_BOT_TOKEN:
    print("DISCORD_BOT_TOKEN not set in .env")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Discord bot ready: {bot.user}")


@bot.hybrid_command(name="top", description="중요도 TOP 5 AI 뉴스")
async def cmd_top(ctx: commands.Context):
    from db.database import init_db, get_primary_articles
    init_db()
    articles = get_primary_articles(limit=100)
    top5 = sorted(articles, key=lambda x: x.get("importance", 0), reverse=True)[:5]
    if not top5:
        await ctx.reply("아직 수집된 뉴스가 없습니다.")
        return
    lines = ["**TOP 5 AI 뉴스**\n"]
    for i, a in enumerate(top5, 1):
        stars = "★" * a.get("importance", 0)
        lines.append(f"**{i}.** {stars} [{a['title']}]({a['url']})")
        if a.get("summary_text"):
            lines.append(f"> {a['summary_text'][:100]}...")
    await ctx.reply("\n".join(lines)[:2000])


@bot.hybrid_command(name="today", description="오늘의 AI 브리핑")
async def cmd_today(ctx: commands.Context):
    from db.database import init_db, get_briefings
    from utils.helpers import today_str
    init_db()
    briefings = get_briefings(limit=10)
    today = today_str()
    b = next((x for x in briefings if x.get("date") == today), None)
    if not b and briefings:
        b = max(briefings, key=lambda x: x.get("date", ""))
    if not b:
        await ctx.reply("오늘 브리핑이 아직 없습니다.")
        return
    msg = f"**{b.get('date', '')} AI 브리핑**\n\n{b.get('summary', '')}"
    await ctx.reply(msg[:2000])


@bot.hybrid_command(name="search", description="AI 뉴스 검색 (예: !search Claude)")
async def cmd_search(ctx: commands.Context, *, query: str):
    query = query.strip()[:100]
    if not query:
        await ctx.reply("검색어를 입력하세요.")
        return
    from db.database import init_db, search_articles
    init_db()
    results = search_articles(query, limit=5)
    if not results:
        await ctx.reply(f"'{query}' 검색 결과가 없습니다.")
        return
    lines = [f"**'{query}' 검색 결과**\n"]
    for a in results:
        lines.append(f"• [{a['title']}]({a['url']})")
    await ctx.reply("\n".join(lines)[:2000])


@bot.hybrid_command(name="alert", description="워치리스트 키워드 추가 (예: !alert Claude)")
async def cmd_alert(ctx: commands.Context, *, keyword: str):
    keyword = keyword.strip()[:50]
    if not keyword:
        await ctx.reply("키워드를 입력하세요.")
        return
    from db.database import init_db, add_watchlist_keyword
    from utils.helpers import now_iso
    init_db()
    success = add_watchlist_keyword(keyword, now_iso())
    if success:
        await ctx.reply(f"`{keyword}` 워치리스트에 추가되었습니다.")
    else:
        await ctx.reply(f"`{keyword}` 는 이미 등록된 키워드입니다.")


@bot.hybrid_command(name="stats", description="수집 통계")
async def cmd_stats(ctx: commands.Context):
    from db.database import init_db, get_article_count, get_processed_count
    init_db()
    total = get_article_count()
    processed = get_processed_count()
    pct = round(processed / max(total, 1) * 100)
    await ctx.reply(f"**AI News Radar 통계**\n총 기사: {total:,}개\nAI 처리: {processed:,}개 ({pct}%)")


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
