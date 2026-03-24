"""AI News Radar — Streamlit 대시보드 (Simplified UI v2)"""
import os
import streamlit as st
from datetime import datetime, timedelta

from config import DATA_DIR, CATEGORIES, SENTIMENTS
from utils.helpers import safe_read_json, safe_write_json, today_str, log
from crawler.rss_crawler import crawl_all, load_sources
from crawler.scheduler import start_scheduler
from ai.batch_processor import process_unprocessed
from ai.deduplicator import deduplicate
from ai.briefing import generate_daily_briefing, FOCUS_AREAS
from ai.model_router import get_active_provider, get_available_providers, PROVIDERS
from export.exporter import (
    export_briefing_markdown, export_articles_markdown,
    export_briefing_pdf, export_articles_pdf,
)
from reader.article_reader import fetch_clean_content
from ai.chat import chat as ai_chat
from ai.voice_briefing import generate_voice_briefing, get_available_voices
from ai.factcheck import get_factcheck_badge
from ai.glossary import get_glossary, extract_terms_from_articles, search_glossary
from ai.weekly_report import generate_weekly_report, get_latest_report, export_weekly_report_markdown
from ai.competitor import get_competitor_analysis, COMPETITOR_GROUPS
from ai.trend import get_trend_data, get_keyword_trend, get_hot_keywords
from ai.debate import generate_debate, get_debate_pairs
from ai.smart_alert import check_and_alert
from sns.card_generator import generate_single_card, generate_briefing_card
from sns.poster import get_available_platforms, post_article, post_briefing, PLATFORM_ADAPTERS
from sns.content_generator import generate_content, generate_multi_content, get_content_templates
from sns.newsletter import send_newsletter, is_smtp_configured, get_newsletter_log

# ── 페이지 설정 ──
st.set_page_config(page_title="AI News Radar", page_icon="📡", layout="wide", initial_sidebar_state="expanded")

# ── CSS ──
st.markdown("""<style>
* { transition: all 0.18s cubic-bezier(0.4,0,0.2,1); }
[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 14px 18px;
}
[data-testid="stMetricValue"] { font-size: 1.9rem !important; font-weight: 800 !important; letter-spacing: -0.5px !important; }
[data-testid="stMetricLabel"] { font-size: 0.78rem !important; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.5px; }
button[data-baseweb="tab"] { font-size: 0.9rem !important; font-weight: 500 !important; padding: 10px 16px !important; border-radius: 0 !important; border-bottom: 2px solid transparent !important; background: transparent !important; }
button[data-baseweb="tab"][aria-selected="true"] { font-weight: 700 !important; border-bottom: 2px solid #60a5fa !important; color: #60a5fa !important; }
[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] { border-radius: 14px !important; border: 1px solid rgba(255,255,255,0.06) !important; }
[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.2); border-color: rgba(96,165,250,0.15) !important; }
[data-testid="stChatMessage"] { border-radius: 18px !important; }
.stButton > button { border-radius: 10px !important; font-weight: 600 !important; border: 1px solid rgba(255,255,255,0.08) !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important; }
[data-testid="stExpander"] { border-radius: 12px !important; }
.sentiment-bar { height: 3px; border-radius: 2px; margin-bottom: 10px; opacity: 0.8; }
.sentiment-positive { background: linear-gradient(90deg, #34d399, #10b981); }
.sentiment-neutral { background: linear-gradient(90deg, #fbbf24, #f59e0b); }
.sentiment-negative { background: linear-gradient(90deg, #f87171, #ef4444); }
.cat-pill { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; margin-right: 6px; border: 1px solid transparent; }
.cat-ai_tool { background: rgba(59,130,246,0.12); color: #60a5fa; } .cat-ai_research { background: rgba(168,85,247,0.12); color: #a78bfa; }
.cat-ai_trend { background: rgba(251,146,60,0.12); color: #fb923c; } .cat-ai_tutorial { background: rgba(52,211,153,0.12); color: #34d399; }
.cat-ai_business { background: rgba(244,114,182,0.12); color: #f472b6; } .cat-ai_image_video { background: rgba(251,113,133,0.12); color: #fb7185; }
.cat-ai_coding { background: rgba(52,211,153,0.12); color: #2dd4bf; } .cat-ai_ontology { background: rgba(139,92,246,0.12); color: #a78bfa; }
.cat-ai_other { background: rgba(148,163,184,0.1); color: #94a3b8; }
.fc-badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.68rem; font-weight: 600; }
.fc-high,.fc-medium { background: rgba(52,211,153,0.12); color: #34d399; } .fc-low { background: rgba(251,191,36,0.12); color: #fbbf24; } .fc-single { background: rgba(248,113,113,0.08); color: #fca5a5; }
.page-info { text-align: center; padding: 8px 0; color: #94a3b8; font-size: 0.85rem; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.main .block-container { animation: fadeIn 0.25s ease; }
@media (max-width: 768px) { [data-testid="stMetricValue"] { font-size: 1.3rem !important; } button[data-baseweb="tab"] { font-size: 0.78rem !important; padding: 6px 8px !important; } }
::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: rgba(148,163,184,0.2); border-radius: 3px; }
a { color: #60a5fa !important; text-decoration: none !important; } a:hover { color: #93c5fd !important; }
hr { border-color: rgba(255,255,255,0.04) !important; }
</style>""", unsafe_allow_html=True)

# ── 초기화 ──
_active_provider = get_active_provider()
if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

ARTICLES_PATH = DATA_DIR / "articles.json"
SOURCES_PATH = DATA_DIR / "sources.json"
WATCHLIST_PATH = DATA_DIR / "watchlist.json"
BRIEFINGS_PATH = DATA_DIR / "briefings.json"
BOOKMARKS_PATH = DATA_DIR / "bookmarks.json"
CAT_NAMES = {"ai_tool": "도구", "ai_research": "연구", "ai_trend": "트렌드", "ai_tutorial": "튜토리얼", "ai_business": "비즈니스", "ai_image_video": "이미지/영상", "ai_coding": "바이브코딩", "ai_ontology": "온톨로지", "ai_other": "기타"}


def load_articles():
    return safe_read_json(ARTICLES_PATH, [])


def load_primary_articles():
    return [a for a in load_articles() if a.get("is_primary", True) and a.get("ai_processed")]


def render_cat_pill(cat):
    return f'<span class="cat-pill cat-{cat}">{CAT_NAMES.get(cat, "기타")}</span>'


def render_fc_badge(article):
    fc = get_factcheck_badge(article)
    return f'<span class="fc-badge fc-{fc["level"]}">{fc["label"]}</span>'


def render_sentiment_bar(s):
    cls = f"sentiment-{s}" if s in ("positive", "neutral", "negative") else "sentiment-neutral"
    return f'<div class="sentiment-bar {cls}"></div>'


# ══════════════════════════════════════════════
# 사이드바
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📡 AI News Radar")

    if _active_provider:
        st.caption(f"🤖 **{PROVIDERS[_active_provider]['name']}**")
    else:
        st.error("⚠️ API 키 미설정")

    st.divider()

    # 액션 버튼
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 수집", use_container_width=True):
            try:
                with st.spinner("📡 수집 중..."):
                    count = crawl_all()
                st.success(f"✅ {count}개!")
            except Exception as e:
                st.error("수집 오류")
                log(f"[수집 오류] {e}")
    with c2:
        if st.button("🤖 AI 처리", use_container_width=True):
            if not _active_provider:
                st.error("API 키 필요")
            else:
                try:
                    with st.spinner("🧠 분석 중..."):
                        processed = process_unprocessed()
                        deduplicate()
                    st.success(f"✅ {processed}개!")
                    alerted = check_and_alert()
                    if alerted:
                        st.info(f"🔔 {len(alerted)}건 알림!")
                except Exception as e:
                    st.error("AI 처리 오류")
                    log(f"[AI 처리 오류] {e}")

    if st.button("📋 브리핑 생성", use_container_width=True):
        if not _active_provider:
            st.error("API 키 필요")
        else:
            try:
                with st.spinner("📝 생성 중..."):
                    generate_daily_briefing()
                st.success("✅ 완료!")
            except Exception as e:
                st.error("브리핑 오류")
                log(f"[브리핑 오류] {e}")

    st.divider()

    with st.expander("🔍 필터"):
        category_filter = st.multiselect("카테고리", list(CATEGORIES.keys()), format_func=lambda x: CATEGORIES[x])
        sentiment_filter = st.multiselect("감성", list(SENTIMENTS.keys()), format_func=lambda x: SENTIMENTS[x])
        importance_filter = st.slider("최소 중요도", 1, 5, 1)

    with st.expander("👀 워치리스트"):
        watchlist = safe_read_json(WATCHLIST_PATH, [])
        watchlist_keywords = [w["keyword"] for w in watchlist if w.get("is_active")]
        new_kw = st.text_input("키워드", placeholder="예: Claude, Flux", label_visibility="collapsed")
        if new_kw and st.button("➕ 추가", key="add_kw", use_container_width=True):
            watchlist.append({"keyword": new_kw, "is_active": True, "created_at": today_str()})
            safe_write_json(WATCHLIST_PATH, watchlist)
            st.rerun()
        if watchlist_keywords:
            st.markdown(" ".join([f"`{k}`" for k in watchlist_keywords]))

    with st.expander("📰 소스 관리"):
        sources = load_sources()
        for s in sources:
            s["is_active"] = st.checkbox(s["name"], value=s.get("is_active", True), key=f"src_{s['id']}")
        if st.button("💾 저장", use_container_width=True, key="save_src"):
            safe_write_json(SOURCES_PATH, sources)
            st.success("저장됨!")

    @st.fragment(run_every=300)
    def sidebar_stats():
        all_a = load_articles()
        proc = [a for a in all_a if a.get("ai_processed")]
        st.divider()
        st.caption(f"📊 {len(all_a)}개 수집 | {len(proc)}개 분석")
    sidebar_stats()


# ── 실시간 알림 ──
@st.fragment(run_every=300)
def new_articles_banner():
    total = len(load_articles())
    if "last_count" not in st.session_state:
        st.session_state.last_count = total
    elif total > st.session_state.last_count:
        st.toast(f"📡 새 글 {total - st.session_state.last_count}개!", icon="🆕")
        st.session_state.last_count = total
    else:
        st.session_state.last_count = total
new_articles_banner()


# ── 데이터 준비 ──
articles = load_primary_articles()
if category_filter:
    articles = [a for a in articles if a.get("category") in category_filter]
if sentiment_filter:
    articles = [a for a in articles if a.get("sentiment") in sentiment_filter]
articles = [a for a in articles if a.get("importance", 0) >= importance_filter]


def is_watchlisted(article):
    text = f"{article.get('title', '')} {' '.join(article.get('tags', []))}".lower()
    return any(k.lower() in text for k in watchlist_keywords)


# ── 히어로 메트릭 ──
all_for_m = load_articles()
proc_for_m = [a for a in all_for_m if a.get("ai_processed")]
pri_for_m = [a for a in proc_for_m if a.get("is_primary", True)]
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("📰 기사", f"{len(all_for_m)}")
with m2:
    p_cnt = len([a for a in pri_for_m if a.get("sentiment") == "positive"])
    st.metric("😊 긍정", f"{round(p_cnt / max(len(pri_for_m), 1) * 100)}%")
with m3:
    st.metric("⭐ 북마크", f"{len(safe_read_json(BOOKMARKS_PATH, []))}")
with m4:
    st.metric("📡 소스", f"{len([s for s in load_sources() if s.get('is_active')])}")

# ══════════════════════════════════════════════
# 5탭 구성
# ══════════════════════════════════════════════
tab_dash, tab_news, tab_ai, tab_insight, tab_share = st.tabs(
    ["🏠 대시보드", "📰 뉴스피드", "💬 AI", "📊 인사이트", "📢 공유"]
)

# ══════════════════════════════════════════════
# 탭 1: 대시보드
# ══════════════════════════════════════════════
with tab_dash:
    # 브리핑
    briefings = safe_read_json(BRIEFINGS_PATH, [])
    today_briefing = next((b for b in briefings if b.get("date") == today_str()), None)

    # 카테고리 퀵필터 (건수 표시)
    def _cat_label_with_count(x):
        if x == "전체":
            return f"전체 ({len(articles)})"
        cnt = len([a for a in articles if a.get("category") == x])
        return f"{CATEGORIES[x]} ({cnt})" if cnt > 0 else f"{CATEGORIES[x]}"

    dash_cat = st.radio("", ["전체"] + list(CATEGORIES.keys()), horizontal=True, key="dash_cat", format_func=_cat_label_with_count, label_visibility="collapsed")

    # 카테고리 필터 적용
    dash_articles = articles if dash_cat == "전체" else [a for a in articles if a.get("category") == dash_cat]

    if dash_cat == "전체":
        # ── "전체" 모드: 브리핑 + 관심 분야 표시 ──
        if today_briefing:
            st.markdown(f"### 📋 오늘의 브리핑 — {today_str()}")
            if today_briefing.get("summary"):
                st.info(f"💡 {today_briefing['summary']}")

            all_arts_map = {a["id"]: a for a in load_articles()}
            title_url_map = {a.get("title", "").lower(): a.get("url", "") for a in load_articles() if a.get("url")}

            top = today_briefing.get("top_articles", [])
            if isinstance(top, list):
                for i, item in enumerate(top, 1):
                    if isinstance(item, dict):
                        headline = item.get("headline", item.get("title", ""))
                        why = item.get("why_important", item.get("summary", ""))
                        url = item.get("url", "")
                        if not url and item.get("article_id"):
                            m = all_arts_map.get(item["article_id"])
                            if m:
                                url = m.get("url", "")
                        if not url:
                            url = title_url_map.get(headline.lower(), "")
                        with st.container(border=True):
                            if url:
                                st.markdown(f"**#{i}** &nbsp; [{headline}]({url})")
                            else:
                                st.markdown(f"**#{i}** &nbsp; {headline}")
                            if why:
                                st.caption(f"→ {why}")

            # 내보내기 + 음성
            ec1, ec2, ec3, ec4 = st.columns(4)
            with ec1:
                st.download_button("📥 MD", data=export_briefing_markdown(), file_name=f"briefing_{today_str()}.md", mime="text/markdown", use_container_width=True)
            with ec2:
                try:
                    st.download_button("📥 PDF", data=export_briefing_pdf(), file_name=f"briefing_{today_str()}.pdf", mime="application/pdf", use_container_width=True)
                except Exception:
                    st.caption("PDF 불가")
            with ec3:
                voices = get_available_voices()
                vc = st.selectbox("음성", [v["id"] for v in voices], format_func=lambda x: next(v["name"] for v in voices if v["id"] == x), key="vc", label_visibility="collapsed")
            with ec4:
                if st.button("🎙️ 음성", use_container_width=True, key="gv"):
                    try:
                        with st.spinner("🎵 생성 중..."):
                            ap = generate_voice_briefing(today_briefing, voice=vc)
                        if ap:
                            st.session_state.voice_path = ap
                            st.rerun()
                    except Exception as e:
                        st.error(str(e)[:50])

            vp = st.session_state.get("voice_path")
            if vp and os.path.exists(vp):
                with open(vp, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
        else:
            st.markdown("### 📋 브리핑")
            st.caption("사이드바에서 🔄 수집 → 🤖 AI 처리 → 📋 브리핑 생성 순서로 진행하세요.")

        # 분야별 맞춤 브리핑
        if today_briefing and today_briefing.get("focus_briefings"):
            st.divider()
            st.markdown("### 🎯 관심 분야")
            focus = today_briefing["focus_briefings"]
            fcols = st.columns(len(focus))
            for idx, (aid, ad) in enumerate(focus.items()):
                with fcols[idx]:
                    st.markdown(f"**{ad.get('icon', '')} {ad.get('name', '')}** ({ad.get('total_count', 0)}건)")
                    for i, item in enumerate(ad.get("top_articles", []), 1):
                        st.caption(f"{i}. [{item['title'][:40]}...]({item.get('url', '')})")
        elif articles:
            st.divider()
            st.markdown("### 🎯 관심 분야")
            fcols = st.columns(len(FOCUS_AREAS))
            for idx, (aid, ai) in enumerate(FOCUS_AREAS.items()):
                with fcols[idx]:
                    cnt = len([a for a in articles if a.get("category") == aid])
                    st.metric(f"{ai['icon']} {ai['name']}", f"{cnt}건")

    else:
        # ── 특정 카테고리 선택 모드: 해당 카테고리 기사만 표시 ──
        cat_label = CATEGORIES.get(dash_cat, dash_cat)
        st.markdown(f"### {cat_label} ({len(dash_articles)}개)")

        if not dash_articles:
            st.caption(f"'{cat_label}' 카테고리에 분류된 기사가 없습니다.")
            st.caption("🔄 수집 → 🤖 AI 처리를 실행하면 새 기사가 분류됩니다.")
        else:
            for a in sorted(dash_articles, key=lambda x: x.get("importance", 0), reverse=True)[:10]:
                with st.container(border=True):
                    st.markdown(render_sentiment_bar(a.get("sentiment", "neutral")), unsafe_allow_html=True)
                    st.markdown(f"{'⭐' * a.get('importance', 0)} [{a['title']}]({a['url']})")
                    st.markdown(render_cat_pill(a.get("category", "ai_other")) + " " + render_fc_badge(a), unsafe_allow_html=True)
                    if a.get("summary_text"):
                        st.caption(a["summary_text"][:150])
                    tags = a.get("tags", [])
                    if tags:
                        st.caption(" ".join([f"`{t}`" for t in tags[:4]]))

    # 감성 온도계
    if dash_articles:
        import plotly.graph_objects as go
        st.divider()
        pos = len([a for a in dash_articles if a.get("sentiment") == "positive"])
        neu = len([a for a in dash_articles if a.get("sentiment") == "neutral"])
        neg = len([a for a in dash_articles if a.get("sentiment") == "negative"])
        total = pos + neu + neg
        pos_pct = round(pos / total * 100) if total else 0

        gc1, gc2 = st.columns(2)
        with gc1:
            fg = go.Figure(go.Indicator(mode="gauge+number", value=pos_pct, number={"suffix": "%", "font": {"size": 36}}, title={"text": "긍정 비율", "font": {"size": 14}},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#60a5fa", "thickness": 0.75},
                       "steps": [{"range": [0, 33], "color": "rgba(248,113,113,0.15)"}, {"range": [33, 66], "color": "rgba(251,191,36,0.15)"}, {"range": [66, 100], "color": "rgba(52,211,153,0.15)"}]}))
            fg.update_layout(height=220, margin=dict(t=40, b=0, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", font={"color": "gray"})
            st.plotly_chart(fg, use_container_width=True)
        with gc2:
            fd = go.Figure(go.Pie(labels=["😊 긍정", "😐 중립", "😠 부정"], values=[pos, neu, neg], hole=0.6, marker=dict(colors=["#34d399", "#fbbf24", "#f87171"]), textinfo="label+percent", textfont=dict(size=11)))
            fd.update_layout(height=220, margin=dict(t=20, b=0, l=0, r=0), showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font={"color": "gray"})
            st.plotly_chart(fd, use_container_width=True)

# ══════════════════════════════════════════════
# 탭 2: 뉴스피드 (뉴스 + 검색 + 북마크 통합)
# ══════════════════════════════════════════════
with tab_news:
    # 뷰 전환
    view_mode = st.radio("", ["📰 전체 뉴스", "🔍 검색", "⭐ 북마크", "⏰ 타임라인"], horizontal=True, key="view_mode", label_visibility="collapsed")

    if view_mode == "📰 전체 뉴스":
        # 카테고리 퀵필터 (건수 표시)
        def _news_cat_label(x):
            if x == "전체":
                return f"전체 ({len(articles)})"
            cnt = len([a for a in articles if a.get("category") == x])
            return f"{CATEGORIES[x]} ({cnt})" if cnt > 0 else f"{CATEGORIES[x]}"

        news_cat = st.radio("카테고리", ["전체"] + list(CATEGORIES.keys()), horizontal=True, key="news_cat", format_func=_news_cat_label, label_visibility="collapsed")
        filtered_articles = articles if news_cat == "전체" else [a for a in articles if a.get("category") == news_cat]
        st.markdown(f"### 📰 뉴스 ({len(filtered_articles)}개)")
        sort_opt = st.selectbox("정렬", ["중요도순", "최신순", "긍정 먼저"], label_visibility="collapsed")
        if sort_opt == "중요도순":
            filtered_articles.sort(key=lambda x: x.get("importance", 0), reverse=True)
        elif sort_opt == "최신순":
            filtered_articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)
        else:
            filtered_articles.sort(key=lambda x: {"positive": 0, "neutral": 1, "negative": 2}.get(x.get("sentiment", "neutral"), 1))

        # 페이지네이션
        PER_PAGE = 10
        total_pages = max(1, -(-len(filtered_articles) // PER_PAGE))
        if "page" not in st.session_state:
            st.session_state.page = 1
        pg = min(st.session_state.page, total_pages)
        start = (pg - 1) * PER_PAGE
        page_arts = filtered_articles[start:start + PER_PAGE]

        if total_pages > 1:
            nc = st.columns([1, 1, 2, 1, 1])
            with nc[0]:
                if st.button("⏮", key="f1", use_container_width=True, disabled=pg <= 1): st.session_state.page = 1; st.rerun()
            with nc[1]:
                if st.button("◀", key="p1", use_container_width=True, disabled=pg <= 1): st.session_state.page = pg - 1; st.rerun()
            with nc[2]:
                st.markdown(f'<div class="page-info">{pg} / {total_pages}</div>', unsafe_allow_html=True)
            with nc[3]:
                if st.button("▶", key="n1", use_container_width=True, disabled=pg >= total_pages): st.session_state.page = pg + 1; st.rerun()
            with nc[4]:
                if st.button("⏭", key="l1", use_container_width=True, disabled=pg >= total_pages): st.session_state.page = total_pages; st.rerun()

        if not page_arts:
            st.caption("사이드바에서 '🔄 수집' → '🤖 AI 처리'를 실행하세요.")
        for article in page_arts:
            watched = is_watchlisted(article)
            prefix = "👀 " if watched else ""
            sentiment = article.get("sentiment", "neutral")
            category = article.get("category", "ai_other")
            with st.container(border=True):
                st.markdown(render_sentiment_bar(sentiment), unsafe_allow_html=True)
                cm, cr = st.columns([4, 1])
                with cm:
                    st.markdown(f"#### {prefix}[{article['title']}]({article['url']})")
                    st.markdown(render_cat_pill(category) + " " + render_fc_badge(article), unsafe_allow_html=True)
                    summary = article.get("summary_text", "")
                    if summary:
                        st.write(summary)
                    with st.expander("📖 더보기"):
                        if article.get("content"):
                            st.write(article["content"][:1500])
                        st.markdown(f"[🔗 원문]({article['url']})")
                    tags = article.get("tags", [])
                    if tags:
                        st.caption(" ".join([f"`{t}`" for t in tags]))
                with cr:
                    st.markdown(f"**{'⭐' * article.get('importance', 0)}**")
                    pub = article.get("published_at", "")[:10]
                    if pub:
                        st.caption(pub)
                    bookmarks = safe_read_json(BOOKMARKS_PATH, [])
                    bm_ids = {b["article_id"] for b in bookmarks}
                    is_bm = article["id"] in bm_ids
                    if st.button("⭐" if is_bm else "☆", key=f"bm_{article['id']}", use_container_width=True):
                        if is_bm:
                            bookmarks = [b for b in bookmarks if b["article_id"] != article["id"]]
                        else:
                            bookmarks.append({"article_id": article["id"], "memo": "", "created_at": today_str()})
                        safe_write_json(BOOKMARKS_PATH, bookmarks)
                        st.rerun()
                    if not article.get("is_read"):
                        if st.button("📖", key=f"rd_{article['id']}", use_container_width=True, help="읽음"):
                            all_a = safe_read_json(ARTICLES_PATH, [])
                            for a in all_a:
                                if a["id"] == article["id"]:
                                    a["is_read"] = True
                                    break
                            safe_write_json(ARTICLES_PATH, all_a)
                            st.rerun()
                    else:
                        st.caption("✅")

    elif view_mode == "🔍 검색":
        st.markdown("### 🔍 검색")
        sq = st.text_input("🔍", placeholder="키워드 입력 (예: Claude, Flux, ComfyUI)", label_visibility="collapsed")
        sc1, sc2 = st.columns(2)
        with sc1:
            s_cat = st.selectbox("카테고리", ["전체"] + list(CATEGORIES.keys()), format_func=lambda x: "전체" if x == "전체" else CATEGORIES[x], key="sc")
        with sc2:
            s_sent = st.selectbox("감성", ["전체", "positive", "neutral", "negative"], format_func=lambda x: "전체" if x == "전체" else SENTIMENTS.get(x, x), key="ss")

        if sq or s_cat != "전체" or s_sent != "전체":
            results = load_primary_articles()
            if sq:
                q = sq.lower()
                results = [a for a in results if q in a.get("title", "").lower() or q in a.get("summary_text", "").lower() or any(q in t.lower() for t in a.get("tags", []))]
            if s_cat != "전체":
                results = [a for a in results if a.get("category") == s_cat]
            if s_sent != "전체":
                results = [a for a in results if a.get("sentiment") == s_sent]
            st.caption(f"🔎 {len(results)}개 결과")
            for a in results[:30]:
                with st.container(border=True):
                    st.markdown(render_sentiment_bar(a.get("sentiment", "neutral")), unsafe_allow_html=True)
                    st.markdown(f"{'⭐' * a.get('importance', 0)} [{a['title']}]({a['url']})")
                    st.markdown(render_cat_pill(a.get("category", "ai_other")), unsafe_allow_html=True)
                    if a.get("summary_text"):
                        st.caption(a["summary_text"][:120])

    elif view_mode == "⭐ 북마크":
        st.markdown("### ⭐ 북마크")
        bookmarks = safe_read_json(BOOKMARKS_PATH, [])
        if not bookmarks:
            st.caption("뉴스에서 ☆를 클릭하면 여기에 저장됩니다.")
        else:
            arts_map = {a["id"]: a for a in load_articles()}
            for bm in reversed(bookmarks):
                a = arts_map.get(bm["article_id"])
                if not a:
                    continue
                with st.container(border=True):
                    st.markdown(render_sentiment_bar(a.get("sentiment", "neutral")), unsafe_allow_html=True)
                    bc1, bc2 = st.columns([5, 1])
                    with bc1:
                        st.markdown(f"{'⭐' * a.get('importance', 0)} [{a['title']}]({a['url']})")
                        memo = st.text_input("메모", value=bm.get("memo", ""), key=f"m_{bm['article_id']}", placeholder="메모...", label_visibility="collapsed")
                        if memo != bm.get("memo", ""):
                            for b in bookmarks:
                                if b["article_id"] == bm["article_id"]:
                                    b["memo"] = memo
                                    break
                            safe_write_json(BOOKMARKS_PATH, bookmarks)
                    with bc2:
                        st.caption(bm.get("created_at", "")[:10])
                        if st.button("🗑️", key=f"db_{bm['article_id']}"):
                            bookmarks = [b for b in bookmarks if b["article_id"] != bm["article_id"]]
                            safe_write_json(BOOKMARKS_PATH, bookmarks)
                            st.rerun()

    elif view_mode == "⏰ 타임라인":
        st.markdown("### ⏰ 타임라인")
        now = datetime.now()
        today_d = now.strftime("%Y-%m-%d")
        yest_d = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        groups = {"🔵 오늘": [], "🟢 어제": [], "🟠 이번 주": [], "⚪ 이전": []}
        for a in articles:
            pub = a.get("published_at", "")[:10]
            if pub == today_d:
                groups["🔵 오늘"].append(a)
            elif pub == yest_d:
                groups["🟢 어제"].append(a)
            elif pub >= (now - timedelta(days=7)).strftime("%Y-%m-%d"):
                groups["🟠 이번 주"].append(a)
            else:
                groups["⚪ 이전"].append(a)
        for period, items in groups.items():
            if items:
                st.markdown(f"#### {period} ({len(items)}개)")
                for a in items:
                    se = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment"), "")
                    with st.container(border=True):
                        st.markdown(f"{se} [{a['title']}]({a['url']})")

# ══════════════════════════════════════════════
# 탭 3: AI (채팅 + 용어 사전)
# ══════════════════════════════════════════════
with tab_ai:
    ai_mode = st.radio("", ["💬 뉴스 채팅", "📚 용어 사전"], horizontal=True, key="ai_mode", label_visibility="collapsed")

    if ai_mode == "💬 뉴스 채팅":
        if not _active_provider:
            st.warning("API 키를 먼저 설정하세요.")
        else:
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            for msg in st.session_state.chat_history:
                with st.chat_message("user" if msg["role"] == "user" else "assistant", avatar="🙋" if msg["role"] == "user" else "🤖"):
                    st.write(msg["content"])
            user_input = st.chat_input("AI 뉴스에 대해 질문하세요...")
            if user_input:
                with st.chat_message("user", avatar="🙋"):
                    st.write(user_input)
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("🤔 분석 중..."):
                        response = ai_chat(user_input, st.session_state.chat_history)
                    st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            if st.session_state.chat_history:
                if st.button("🗑️ 초기화", key="cc"):
                    st.session_state.chat_history = []
                    st.rerun()
            if not st.session_state.chat_history:
                st.caption("💡 추천:")
                suggestions = ["오늘 중요한 AI 뉴스 3가지", "Flux 관련 최신 뉴스", "바이브코딩 도구 비교", "부정적 AI 뉴스는?"]
                scols = st.columns(2)
                for i, s in enumerate(suggestions):
                    with scols[i % 2]:
                        if st.button(f"💬 {s}", key=f"sg_{i}", use_container_width=True):
                            st.session_state.chat_history.append({"role": "user", "content": s})
                            r = ai_chat(s)
                            st.session_state.chat_history.append({"role": "assistant", "content": r})
                            st.rerun()

    elif ai_mode == "📚 용어 사전":
        gc1, gc2 = st.columns([3, 1])
        with gc1:
            gs = st.text_input("🔍", placeholder="용어 검색 (예: LLM, RAG)", key="gs", label_visibility="collapsed")
        with gc2:
            if st.button("🔄 추출", use_container_width=True, key="et"):
                if _active_provider:
                    with st.spinner("🧠 추출 중..."):
                        extract_terms_from_articles()
                    st.success("✅")
                    st.rerun()
        terms = search_glossary(gs) if gs else get_glossary()
        if not terms:
            st.caption("'🔄 추출' 버튼으로 뉴스에서 AI 용어를 자동 추출하세요.")
        else:
            st.caption(f"📖 {len(terms)}개 용어")
            tcols = st.columns(2)
            cat_labels = {"model": "🤖", "technique": "⚙️", "concept": "💡", "product": "📦", "company": "🏢", "other": "📌"}
            for idx, t in enumerate(terms):
                with tcols[idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"**{t.get('term', '')}** ({t.get('term_ko', '')})")
                        st.caption(f"{cat_labels.get(t.get('category', ''), '📌')} {'⭐' * t.get('difficulty', 1)} · {t.get('short_desc', '')}")
                        st.write(t.get("full_desc", ""))
                        if t.get("example"):
                            st.info(f"💡 {t['example']}")

# ══════════════════════════════════════════════
# 탭 4: 인사이트 (도구 비교 + 트렌드 + 주간 리포트)
# ══════════════════════════════════════════════
with tab_insight:
    ins_mode = st.radio("", ["🏆 도구 비교", "📈 트렌드", "🎭 AI 토론", "📊 주간 리포트"], horizontal=True, key="ins_mode", label_visibility="collapsed")

    if ins_mode == "🏆 도구 비교":
        comp_group = st.selectbox("분야", list(COMPETITOR_GROUPS.keys()), format_func=lambda x: f"{COMPETITOR_GROUPS[x]['icon']} {COMPETITOR_GROUPS[x]['name']}", key="cg", label_visibility="collapsed")
        analysis = get_competitor_analysis(comp_group)
        tools = analysis.get(comp_group, {}).get("tools", [])
        active_tools = [t for t in tools if t["mention_count"] > 0]

        if not active_tools:
            st.caption("아직 비교 데이터가 없습니다. 뉴스를 먼저 수집하세요.")
        else:
            import plotly.graph_objects as go
            names = [t["name"] for t in active_tools]
            counts = [t["mention_count"] for t in active_tools]
            colors = [t["color"] for t in active_tools]
            fig = go.Figure(go.Bar(x=counts, y=names, orientation="h", marker_color=colors, marker_cornerradius=6, text=counts, textposition="outside"))
            fig.update_layout(height=max(180, len(names) * 40), margin=dict(t=0, b=0, l=0, r=40), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "gray"}, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)

            ccols = st.columns(min(len(active_tools), 3))
            for idx, tool in enumerate(active_tools[:6]):
                with ccols[idx % min(len(active_tools), 3)]:
                    with st.container(border=True):
                        ts = sum(tool["sentiment"].values()) or 1
                        pp = round(tool["sentiment"]["positive"] / ts * 100)
                        st.markdown(f"**{tool['name']}**")
                        st.caption(f"📰 {tool['mention_count']}건 · ⭐ {tool['avg_importance']} · 😊 {pp}%")
                        for a in tool["top_articles"][:2]:
                            st.caption(f"• [{a['title'][:35]}...]({a['url']})")

    elif ins_mode == "📈 트렌드":
        comp_group = st.selectbox("분야", list(COMPETITOR_GROUPS.keys()), format_func=lambda x: f"{COMPETITOR_GROUPS[x]['icon']} {COMPETITOR_GROUPS[x]['name']}", key="tg", label_visibility="collapsed")
        days = st.selectbox("기간", [7, 14, 30], index=1, format_func=lambda x: f"{x}일", key="td", label_visibility="collapsed")
        td = get_trend_data(comp_group, days)
        if td["tools"]:
            import plotly.graph_objects as go
            fig = go.Figure()
            for t in td["tools"]:
                fig.add_trace(go.Scatter(x=td["dates"], y=t["counts"], name=f"{t['name']} ({t['total']})", line=dict(color=t["color"], width=2), mode="lines+markers", marker=dict(size=3)))
            fig.update_layout(height=320, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "gray"}, legend=dict(orientation="h", yanchor="bottom", y=1.02), hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("트렌드 데이터가 아직 부족합니다.")

        # 급상승
        hot = get_hot_keywords(8, 7)
        if hot:
            st.markdown("#### 🔥 급상승 키워드")
            hcols = st.columns(4)
            for idx, h in enumerate(hot[:8]):
                with hcols[idx % 4]:
                    ch = h["change_pct"]
                    badge = "🆕" if ch >= 999 else (f"🔺{ch}%" if ch > 0 else f"🔻{abs(ch)}%" if ch < 0 else "➡️")
                    with st.container(border=True):
                        st.markdown(f"**`{h['keyword']}`**")
                        st.caption(f"{h['count']}건 {badge}")

    elif ins_mode == "🎭 AI 토론":
        comp_group = st.selectbox("분야", list(COMPETITOR_GROUPS.keys()), format_func=lambda x: f"{COMPETITOR_GROUPS[x]['icon']} {COMPETITOR_GROUPS[x]['name']}", key="dg", label_visibility="collapsed")
        gt = COMPETITOR_GROUPS.get(comp_group, {}).get("tools", [])
        tn = [t["name"] for t in gt]
        d1, d2, d3 = st.columns([2, 2, 1])
        with d1:
            ta = st.selectbox("도구 A", range(len(tn)), format_func=lambda i: tn[i], key="da")
        with d2:
            tb = st.selectbox("도구 B", range(len(tn)), index=min(1, len(tn) - 1), format_func=lambda i: tn[i], key="db_sel")
        with d3:
            go_debate = st.button("⚔️ 토론", use_container_width=True, key="rd")

        if go_debate:
            if ta == tb:
                st.warning("다른 도구를 선택하세요.")
            elif not _active_provider:
                st.error("API 키 필요")
            else:
                with st.spinner(f"🎭 {tn[ta]} vs {tn[tb]} 분석 중..."):
                    debate = generate_debate(tn[ta], tn[tb], gt[ta]["keywords"], gt[tb]["keywords"])
                if debate:
                    st.session_state.last_debate = debate

        debate = st.session_state.get("last_debate")
        if debate:
            da_d = debate.get("tool_a", {})
            db_d = debate.get("tool_b", {})
            dc1, dc2 = st.columns(2)
            with dc1:
                with st.container(border=True):
                    st.markdown(f"### 🔵 {da_d.get('name', '')}")
                    for p in da_d.get("pros", []): st.markdown(f"✅ {p}")
                    for c in da_d.get("cons", []): st.markdown(f"⚠️ {c}")
            with dc2:
                with st.container(border=True):
                    st.markdown(f"### 🔴 {db_d.get('name', '')}")
                    for p in db_d.get("pros", []): st.markdown(f"✅ {p}")
                    for c in db_d.get("cons", []): st.markdown(f"⚠️ {c}")
            if debate.get("verdict"):
                st.info(f"🏆 {debate['verdict']}")
            if debate.get("recommendation"):
                st.success(f"💡 {debate['recommendation']}")

    elif ins_mode == "📊 주간 리포트":
        rc1, rc2 = st.columns([3, 1])
        with rc2:
            if st.button("📊 생성", use_container_width=True, key="gwr"):
                if _active_provider:
                    with st.spinner("📊 생성 중..."):
                        generate_weekly_report()
                    st.success("✅")
                    st.rerun()
        report = get_latest_report()
        if report:
            with rc1:
                st.caption(f"📅 {report['week_start']} ~ {report['week_end']}")
            stats = report.get("stats", {})
            trends = report.get("trends")
            rm = st.columns(3)
            with rm[0]:
                st.metric("기사", f"{stats.get('total', 0)}")
            with rm[1]:
                st.metric("중요도", f"{stats.get('avg_importance', 0)}")
            with rm[2]:
                st.metric("관심 분야", f"{sum(stats.get('focus_counts', {}).values())}건")

            if trends:
                for i, t in enumerate(trends.get("key_trends", []), 1):
                    st.markdown(f"**{i}.** {t}")
                if trends.get("outlook"):
                    st.info(f"🔭 {trends['outlook']}")

            md_r = export_weekly_report_markdown(report)
            st.download_button("📥 리포트 MD", data=md_r, file_name=f"weekly_{report['week_start']}.md", mime="text/markdown", use_container_width=True)
        else:
            with rc1:
                st.caption("'📊 생성' 버튼을 클릭하세요.")

        # 뉴스레터
        st.divider()
        st.markdown("#### 📧 뉴스레터")
        if is_smtp_configured():
            nl1, nl2 = st.columns(2)
            with nl1:
                if st.button("📧 일간 발송", use_container_width=True, key="sdnl"):
                    r = send_newsletter("daily")
                    st.success(f"✅ {r['sent_to']}명") if r["success"] else st.error(r["error"])
            with nl2:
                if st.button("📊 주간 발송", use_container_width=True, key="swnl"):
                    r = send_newsletter("weekly")
                    st.success(f"✅ {r['sent_to']}명") if r["success"] else st.error(r["error"])
        else:
            with st.expander("⚙️ 이메일 설정"):
                st.markdown("`.env`에 `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `NEWSLETTER_RECIPIENTS` 추가")

# ══════════════════════════════════════════════
# 탭 5: 공유 (SNS + 콘텐츠 + 내보내기)
# ══════════════════════════════════════════════
with tab_share:
    share_mode = st.radio("", ["📢 SNS 게시", "✍️ 콘텐츠 생성", "📥 내보내기"], horizontal=True, key="share_mode", label_visibility="collapsed")

    if share_mode == "📢 SNS 게시":
        platforms = get_available_platforms()
        configured = [p for p in platforms if p["configured"]]

        # 플랫폼 상태
        pcols = st.columns(len(platforms))
        for idx, p in enumerate(platforms):
            with pcols[idx]:
                st.caption(f"{p['icon']} {'🟢' if p['configured'] else '⚪'}")

        # 미연결 플랫폼 가이드 (연결된 것이 있어도 보여줌)
        unconfigured = [p for p in platforms if not p["configured"]]
        if unconfigured:
            with st.expander(f"⚙️ SNS 연결 가이드 ({len(unconfigured)}개 미연결)", expanded=not configured):
                st.markdown("`.env` 파일을 메모장으로 열어 아래 내용을 추가하세요.")

                st.markdown("---")
                st.markdown("""
### 💬 Discord — 가장 쉬움 (30초)

> 별도 가입이나 개발자 등록 없이 URL 하나만 복사하면 됩니다.

**설정 방법:**
1. Discord 앱 또는 웹에서 내 서버 열기
2. 왼쪽 채널 목록에서 게시할 채널의 **⚙️ 톱니바퀴** (채널 편집) 클릭
3. **연동** 탭 클릭
4. **웹훅 만들기** 클릭
5. 이름을 "AI News Radar"로 변경 (선택사항)
6. **웹훅 URL 복사** 클릭
7. `.env` 파일에 붙여넣기:

```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/여기에복사한URL
```

---

### 📨 Telegram — 쉬움 (2분)

> 텔레그램 앱에서 봇을 만들고 채널에 연결합니다.

**설정 방법:**
1. 텔레그램 앱에서 **@BotFather** 검색 → 대화 시작
2. `/newbot` 입력 → 봇 이름 입력 (예: `AI News Radar`)
3. 유저네임 입력 (예: `my_ai_news_bot`) — 반드시 `_bot`으로 끝나야 함
4. **토큰이 표시됨** → 복사 (예: `7123456789:AAH...`)
5. 텔레그램에서 **채널 만들기** (또는 기존 채널 사용)
6. 채널 설정 → **관리자** → 방금 만든 봇을 관리자로 추가
7. 채널의 **@아이디** 확인 (예: `@my_ai_news_channel`)
8. `.env` 파일에 추가:

```
TELEGRAM_BOT_TOKEN=7123456789:AAHxxxxxx
TELEGRAM_CHANNEL_ID=@my_ai_news_channel
```

---

### 🐦 X (Twitter) — 보통 (10분)

> 개발자 포털에서 앱을 만들고 키 4개를 발급받습니다.

**설정 방법:**
1. [developer.x.com](https://developer.x.com/) 접속 → 로그인
2. **Developer Portal** → **Projects & Apps** → **+ Create App**
3. 앱 이름 입력 (예: `AI-News-Radar`)
4. **App Settings** → **Keys and Tokens** 탭
5. **API Key and Secret** → Generate → **2개 키 복사**
6. **Access Token and Secret** → Generate → **2개 키 복사**
7. **User authentication settings** → Edit → Read and Write 권한 설정
8. `.env` 파일에 추가:

```
X_API_KEY=발급받은_API_Key
X_API_SECRET=발급받은_API_Key_Secret
X_ACCESS_TOKEN=발급받은_Access_Token
X_ACCESS_SECRET=발급받은_Access_Token_Secret
```

---

### 🧵 Threads — 보통 (10분)

> Meta 개발자 포털에서 Threads API를 활성화합니다.

**설정 방법:**
1. [developers.facebook.com](https://developers.facebook.com/) 접속 → 로그인
2. **내 앱** → **앱 만들기** → 사용 사례: **"기타"** 선택
3. 앱 이름 입력 → 만들기
4. 왼쪽 메뉴 → **제품 추가** → **Threads API** 선택
5. **API 설정** → `threads_manage_posts` 권한 추가
6. **토큰 생성** → 액세스 토큰 복사
7. 사용자 ID 확인:
   - 그래프 API 탐색기 → GET `/me` 실행 → `id` 값 복사
8. `.env` 파일에 추가:

```
THREADS_ACCESS_TOKEN=발급받은_액세스_토큰
THREADS_USER_ID=발급받은_사용자_ID
```

---

### 📸 Instagram — 복잡 (15분)

> Facebook 페이지와 Instagram 비즈니스 계정 연결이 필요합니다.

**사전 준비:**
- Instagram 계정을 **비즈니스** 또는 **크리에이터** 계정으로 전환
- Facebook 페이지를 만들고 Instagram 계정과 연결

**설정 방법:**
1. Instagram 앱 → 설정 → 계정 → **프로페셔널 계정으로 전환** → 비즈니스 선택
2. Facebook 페이지 만들기 (없는 경우) → Instagram 계정 연결
3. [developers.facebook.com](https://developers.facebook.com/) → 앱 만들기
4. **제품 추가** → **Instagram Graph API** 선택
5. 권한 추가: `instagram_basic`, `instagram_content_publish`
6. **액세스 토큰 생성** → 복사
7. **계정 ID 확인**:
   - 그래프 API 탐색기 → GET `/me/accounts` → `instagram_business_account` → `id` 복사
8. 이미지 호스팅용 Imgur 등록:
   - [api.imgur.com/oauth2/addclient](https://api.imgur.com/oauth2/addclient) → 앱 등록 → Client ID 복사
9. `.env` 파일에 추가:

```
INSTAGRAM_ACCESS_TOKEN=발급받은_액세스_토큰
INSTAGRAM_ACCOUNT_ID=발급받은_계정_ID
IMGUR_CLIENT_ID=발급받은_Imgur_Client_ID
```
""")

        if not configured:
            pass  # 가이드만 표시
        else:
            # 카테고리 선택
            sns_cats = st.multiselect("카테고리", list(CATEGORIES.keys()), default=["ai_image_video", "ai_coding", "ai_ontology"], format_func=lambda x: CATEGORIES[x], key="snsc")
            sns_arts = [a for a in articles if a.get("category") in sns_cats]
            sns_arts.sort(key=lambda x: x.get("importance", 0), reverse=True)

            sel_plats = [p["id"] for p in configured]
            max_posts = st.slider("게시 수", 1, min(10, max(len(sns_arts), 1)), min(3, max(len(sns_arts), 1)), key="snsp")

            if sns_arts:
                for a in sns_arts[:max_posts]:
                    st.caption(f"{'⭐' * a.get('importance', 0)} {a['title'][:50]}")

                if st.button(f"📢 {min(max_posts, len(sns_arts))}개 → {len(sel_plats)}개 플랫폼", use_container_width=True, key="snsgo", type="primary"):
                    prog = st.progress(0)
                    for i, a in enumerate(sns_arts[:max_posts]):
                        prog.progress((i + 1) / max_posts)
                        card = generate_single_card(a)
                        post_article(a, sel_plats, card)
                    prog.empty()
                    st.success("✅ 게시 완료!")

    elif share_mode == "✍️ 콘텐츠 생성":
        st.markdown("### ✍️ AI 콘텐츠 생성")
        target = articles[:20]
        if target:
            titles = [a.get("title", "")[:50] for a in target]
            si = st.selectbox("기사", range(len(titles)), format_func=lambda i: titles[i], key="ca")
            templates = get_content_templates()
            cps = st.multiselect("유형", list(templates.keys()), default=["tweet", "thread"], format_func=lambda x: f"{templates[x]['icon']} {templates[x]['name']}", key="cp")

            if st.button("✍️ 생성", use_container_width=True, key="gc", type="primary"):
                if _active_provider and cps:
                    with st.spinner("✍️ 작성 중..."):
                        results = generate_multi_content(target[si], cps)
                    for r in results:
                        if r["success"]:
                            with st.expander(f"{templates[r['platform']]['icon']} {templates[r['platform']]['name']}", expanded=True):
                                st.text_area("", value=r["content"], height=180, key=f"ct_{r['platform']}", label_visibility="collapsed")
                                st.download_button("📥 저장", data=r["content"], file_name=f"{r['platform']}.txt", mime="text/plain", use_container_width=True, key=f"dc_{r['platform']}")
        else:
            st.caption("기사를 먼저 수집하세요.")

    elif share_mode == "📥 내보내기":
        st.markdown("### 📥 내보내기")
        if articles:
            e1, e2 = st.columns(2)
            with e1:
                st.download_button("📥 뉴스 Markdown", data=export_articles_markdown(articles), file_name=f"news_{today_str()}.md", mime="text/markdown", use_container_width=True)
            with e2:
                try:
                    st.download_button("📥 뉴스 PDF", data=export_articles_pdf(articles), file_name=f"news_{today_str()}.pdf", mime="application/pdf", use_container_width=True)
                except Exception:
                    st.caption("PDF 불가")

            # 카드 이미지
            if st.button("🖼️ 카드 이미지 생성", use_container_width=True, key="gcards"):
                with st.spinner("🖼️ 생성 중..."):
                    paths = [generate_single_card(a) for a in articles[:5]]
                    paths = [p for p in paths if p]
                if paths:
                    icols = st.columns(min(len(paths), 3))
                    for idx, p in enumerate(paths[:3]):
                        with icols[idx]:
                            st.image(p, use_container_width=True)
                            with open(p, "rb") as f:
                                st.download_button("📥", data=f.read(), file_name=os.path.basename(p), mime="image/png", key=f"dci_{idx}", use_container_width=True)
        else:
            st.caption("내보낼 기사가 없습니다.")
