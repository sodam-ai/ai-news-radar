"""AI News Radar — Streamlit 대시보드 (Simplified UI v2)"""
import os
import streamlit as st
from datetime import datetime, timedelta

from config import DATA_DIR, CATEGORIES, SENTIMENTS
from utils.helpers import today_str, log
from db.database import (
    init_db, get_articles, get_primary_articles, search_articles,
    get_article_by_id, update_article_fields,
    get_briefings, get_sources, upsert_source,
    get_watchlist, add_watchlist_keyword, get_active_keywords,
    get_bookmarks, add_bookmark, remove_bookmark, update_bookmark_memo,
    get_bookmark_ids, get_article_count, get_processed_count,
    get_weekly_reports,
)
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
from ai.release_tracker import detect_releases, get_release_history, get_tracked_tools
from ai.translator import translate_articles, get_translation_stats
from sns.card_generator import generate_single_card, generate_briefing_card
from sns.poster import get_available_platforms, post_article, post_briefing, PLATFORM_ADAPTERS
from sns.content_generator import generate_content, generate_multi_content, get_content_templates
from sns.newsletter import send_newsletter, is_smtp_configured, get_newsletter_log

# ── 페이지 설정 ──
st.set_page_config(page_title="AI News Radar", page_icon="📡", layout="wide", initial_sidebar_state="expanded")

# ── CSS ──
st.markdown("""<style>
/* ═══ Design System — AI News Radar v3 ═══ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --surface-0: #09090b;
    --surface-1: #0f0f12;
    --surface-2: #17171c;
    --surface-3: #23232a;
    --surface-4: #2e2e38;
    --border-subtle: rgba(255,255,255,0.05);
    --border-default: rgba(255,255,255,0.08);
    --border-hover: rgba(99,102,241,0.22);
    --text-primary: #ececef;
    --text-secondary: #9d9da7;
    --text-muted: #636370;
    --accent: #6366f1;
    --accent-hover: #818cf8;
    --accent-soft: rgba(99,102,241,0.12);
    --positive: #34d399;
    --neutral-tone: #fbbf24;
    --negative: #f87171;
    --radius-sm: 8px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --transition: 0.16s cubic-bezier(0.25, 0.1, 0.25, 1);
    --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
}

/* ═══ Typography ═══ */
html, body, [class*="css"] { font-family: var(--font) !important; -webkit-font-smoothing: antialiased; }

/* ═══ Global transitions ═══ */
.stButton > button, [data-testid="stVerticalBlock"] > div[data-testid="stContainer"],
[data-testid="stExpander"], [data-testid="stMetric"] {
    transition: all var(--transition);
}

/* ═══ Sidebar ═══ */
[data-testid="stSidebar"] {
    background: var(--surface-1) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdown"] h2 {
    font-size: 0.95rem !important; font-weight: 700 !important; letter-spacing: -0.2px;
}

.brand-header {
    padding: 2px 0 14px; margin-bottom: 10px;
    border-bottom: 1px solid var(--border-subtle);
}
.brand-header h2 {
    margin: 0; font-size: 1rem; font-weight: 700; color: var(--text-primary);
    letter-spacing: -0.3px;
}
.brand-sub {
    font-size: 0.62rem; color: var(--text-muted); letter-spacing: 0.8px;
    text-transform: uppercase; margin-top: 3px;
}

/* ═══ Metrics ═══ */
[data-testid="stMetric"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-lg) !important;
    padding: 18px 20px;
    position: relative; overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent); opacity: 0.5;
}
[data-testid="stMetric"]:hover {
    border-color: var(--border-hover) !important;
    box-shadow: 0 0 0 1px var(--accent-soft);
}
[data-testid="stMetricValue"] {
    font-size: 1.75rem !important; font-weight: 800 !important;
    letter-spacing: -0.5px !important; color: var(--text-primary) !important;
    font-variant-numeric: tabular-nums;
}
[data-testid="stMetricLabel"] {
    font-size: 0.65rem !important; color: var(--text-muted) !important;
    text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600 !important;
}

/* ═══ Tabs ═══ */
[data-baseweb="tab-list"] {
    gap: 0 !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    background: transparent !important;
}
button[data-baseweb="tab"] {
    font-size: 0.8rem !important; font-weight: 500 !important;
    padding: 11px 18px !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    color: var(--text-muted) !important;
    transition: all var(--transition) !important;
}
button[data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
    background: rgba(255,255,255,0.015) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    font-weight: 700 !important;
    border-bottom-color: var(--accent) !important;
    color: var(--text-primary) !important;
}

/* ═══ Cards ═══ */
[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-subtle) !important;
    background: var(--surface-2) !important;
}
[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:hover {
    border-color: var(--border-hover) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.18);
}

/* ═══ Chat ═══ */
[data-testid="stChatMessage"] {
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--border-subtle) !important;
    background: var(--surface-2) !important;
}

/* ═══ Buttons ═══ */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    border: 1px solid var(--border-default) !important;
    letter-spacing: 0.1px; font-size: 0.8rem !important;
    background: var(--surface-2) !important;
    color: var(--text-primary) !important;
}
.stButton > button:hover {
    border-color: var(--border-hover) !important;
    background: var(--surface-3) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}
.stButton > button:active {
    transform: scale(0.98) !important;
}
.stButton > button[kind="primary"] {
    background: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    color: white !important;
    font-weight: 700 !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--accent-hover) !important;
    border-color: var(--accent-hover) !important;
    box-shadow: 0 4px 14px var(--accent-soft) !important;
}

/* ═══ Expander ═══ */
[data-testid="stExpander"] {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-subtle) !important;
    background: var(--surface-1) !important;
}

/* ═══ Inputs ═══ */
[data-testid="stTextInput"] input, [data-testid="stSelectbox"] > div > div {
    border-radius: var(--radius-sm) !important;
    border-color: var(--border-default) !important;
    font-family: var(--font) !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-soft) !important;
}

/* ═══ Sentiment Bars ═══ */
.sentiment-bar { height: 2px; border-radius: 1px; margin-bottom: 10px; opacity: 0.8; }
.sentiment-positive { background: var(--positive); }
.sentiment-neutral { background: var(--neutral-tone); }
.sentiment-negative { background: var(--negative); }

/* ═══ Category Pills ═══ */
.cat-pill {
    display: inline-block; padding: 2px 10px; border-radius: 100px;
    font-size: 0.65rem; font-weight: 600; margin-right: 4px;
    border: 1px solid transparent; letter-spacing: 0.15px;
    vertical-align: middle;
}
.cat-ai_tool { background: rgba(99,102,241,0.1); color: #818cf8; border-color: rgba(99,102,241,0.15); }
.cat-ai_research { background: rgba(168,85,247,0.1); color: #c084fc; border-color: rgba(168,85,247,0.12); }
.cat-ai_trend { background: rgba(251,146,60,0.08); color: #fb923c; border-color: rgba(251,146,60,0.1); }
.cat-ai_tutorial { background: rgba(52,211,153,0.08); color: #34d399; border-color: rgba(52,211,153,0.1); }
.cat-ai_business { background: rgba(244,114,182,0.08); color: #f472b6; border-color: rgba(244,114,182,0.1); }
.cat-ai_image_video { background: rgba(251,113,133,0.08); color: #fb7185; border-color: rgba(251,113,133,0.1); }
.cat-ai_coding { background: rgba(45,212,191,0.08); color: #2dd4bf; border-color: rgba(45,212,191,0.1); }
.cat-ai_ontology { background: rgba(139,92,246,0.1); color: #a78bfa; border-color: rgba(139,92,246,0.12); }
.cat-ai_other { background: rgba(148,163,184,0.05); color: #94a3b8; border-color: rgba(148,163,184,0.06); }

/* ═══ Badges ═══ */
.fc-badge {
    display: inline-block; padding: 2px 9px; border-radius: 100px;
    font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1px; vertical-align: middle;
    margin-left: 4px;
}
.fc-high,.fc-medium { background: rgba(52,211,153,0.08); color: var(--positive); }
.fc-low { background: rgba(251,191,36,0.08); color: var(--neutral-tone); }
.fc-single { background: rgba(248,113,113,0.05); color: #fca5a5; }

/* ═══ Pagination ═══ */
.page-info {
    text-align: center; padding: 10px 0;
    color: var(--text-secondary); font-size: 0.8rem;
    font-weight: 600; font-variant-numeric: tabular-nums;
}

/* ═══ Section headers ═══ */
.section-header {
    font-size: 1.1rem; font-weight: 700; color: var(--text-primary);
    letter-spacing: -0.3px; margin: 0 0 4px;
}
.section-sub {
    font-size: 0.7rem; color: var(--text-muted); letter-spacing: 0.3px; margin-bottom: 14px;
}

/* ═══ Animation ═══ */
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
.main .block-container { animation: fadeIn 0.2s ease-out; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.5; } }
.live-dot {
    display: inline-block; width: 5px; height: 5px; border-radius: 50%;
    background: var(--positive); animation: pulse 2.5s ease-in-out infinite;
    margin-right: 6px; vertical-align: middle;
}

/* ═══ Responsive ═══ */
@media (max-width: 1200px) {
    [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
}
@media (max-width: 768px) {
    [data-testid="stMetricValue"] { font-size: 1.15rem !important; }
    [data-testid="stMetricLabel"] { font-size: 0.58rem !important; }
    button[data-baseweb="tab"] { font-size: 0.7rem !important; padding: 8px 10px !important; }
    .cat-pill { font-size: 0.58rem; padding: 2px 7px; }
}

/* ═══ Scrollbar ═══ */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(148,163,184,0.12); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(148,163,184,0.24); }

/* ═══ Links ═══ */
a { color: var(--accent-hover) !important; text-decoration: none !important; transition: color var(--transition); }
a:hover { color: #a5b4fc !important; }
hr { border-color: var(--border-subtle) !important; }

/* ═══ Empty state ═══ */
.empty-state { text-align: center; padding: 48px 24px; color: var(--text-muted); }
.empty-state-icon { font-size: 2rem; margin-bottom: 10px; opacity: 0.4; }

/* ═══ Progress Bar ═══ */
[data-testid="stProgress"] > div > div > div { background: var(--accent) !important; }

/* ═══ Toast / Status ═══ */
[data-testid="stToast"] { border-radius: var(--radius-md) !important; }

/* ═══ Radio pills (horizontal) ═══ */
[data-testid="stRadio"] > div { gap: 0 !important; }
[data-testid="stRadio"] label {
    font-size: 0.76rem !important; font-weight: 500 !important;
}

/* ═══ Download buttons ═══ */
[data-testid="stDownloadButton"] button {
    font-size: 0.76rem !important;
}

/* ═══ Selectbox ═══ */
[data-testid="stSelectbox"] label { font-size: 0.76rem !important; }

/* ═══ Main container padding ═══ */
.main .block-container { padding-top: 1.5rem !important; }
</style>""", unsafe_allow_html=True)

# ── 초기화 ──
init_db()
_active_provider = get_active_provider()
if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

CAT_NAMES = {"ai_tool": "도구", "ai_research": "연구", "ai_trend": "트렌드", "ai_tutorial": "튜토리얼", "ai_business": "비즈니스", "ai_image_video": "이미지/영상", "ai_coding": "바이브코딩", "ai_ontology": "온톨로지", "ai_other": "기타"}


@st.cache_data(ttl=60)
def load_articles():
    return get_articles(limit=5000)


@st.cache_data(ttl=60)
def load_primary_articles():
    return get_primary_articles(limit=2000)


def _toggle_bookmark(article_id: str) -> None:
    ids = get_bookmark_ids()
    if article_id in ids:
        remove_bookmark(article_id)
    else:
        add_bookmark(article_id, "", today_str())
    st.cache_data.clear()


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
    st.markdown("""<div class="brand-header">
        <h2>📡 AI News Radar</h2>
        <div class="brand-sub"><span class="live-dot"></span>AI-Powered News Intelligence</div>
    </div>""", unsafe_allow_html=True)

    if _active_provider:
        st.caption(f"**{PROVIDERS[_active_provider]['name']}** connected")
    else:
        st.error("API key not configured")

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
                st.error(f"수집 오류: {str(e)[:60]}")
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
                    st.error(f"AI 처리 오류: {str(e)[:60]}")
                    log(f"[AI 처리 오류] {e}")

    c3, c4 = st.columns(2)
    with c3:
        if st.button("📋 브리핑", use_container_width=True):
            if not _active_provider:
                st.error("API 키 필요")
            else:
                try:
                    with st.spinner("📝 생성 중..."):
                        generate_daily_briefing()
                    st.success("✅ 완료!")
                except Exception as e:
                    st.error(f"브리핑 오류: {str(e)[:60]}")
                    log(f"[브리핑 오류] {e}")
    with c4:
        if st.button("🌐 번역", use_container_width=True):
            if not _active_provider:
                st.error("API 키 필요")
            else:
                try:
                    with st.spinner("🌐 영→한 번역 중..."):
                        t_count = translate_articles(max_batch=10)
                    if t_count > 0:
                        st.success(f"✅ {t_count}개 번역!")
                    else:
                        st.caption("번역할 기사 없음")
                except Exception as e:
                    st.error(f"번역 오류: {e}")

    # ── 원클릭 풀 파이프라인 ──
    if st.button("⚡ 원클릭 전체 실행", use_container_width=True, type="primary"):
        if not _active_provider:
            st.error("API 키를 먼저 설정하세요.")
        else:
            progress = st.progress(0, text="⚡ 파이프라인 시작...")
            pipeline_ok = True

            # 1. 수집
            try:
                progress.progress(10, text="📡 1/4 — RSS 수집 중...")
                count = crawl_all()
                progress.progress(30, text=f"📡 {count}개 수집 완료")
            except Exception as e:
                st.error(f"수집 오류: {e}")
                pipeline_ok = False
                log(f"[파이프라인 수집 오류] {e}")

            # 2. AI 처리
            if pipeline_ok:
                try:
                    progress.progress(35, text="🧠 2/4 — AI 분석 중 (고속 모드)...")
                    processed = process_unprocessed(skip_images=True)
                    deduplicate()
                    progress.progress(60, text=f"🧠 {processed}개 분석 완료")
                    alerted = check_and_alert()
                except Exception as e:
                    st.error(f"AI 처리 오류: {e}")
                    pipeline_ok = False
                    log(f"[파이프라인 AI 오류] {e}")

            # 3. 브리핑
            if pipeline_ok:
                try:
                    progress.progress(65, text="📋 3/4 — 브리핑 생성 중...")
                    generate_daily_briefing()
                    progress.progress(85, text="📋 브리핑 완료")
                except Exception as e:
                    st.warning(f"브리핑 오류 (계속 진행): {e}")
                    log(f"[파이프라인 브리핑 오류] {e}")

            # 4. 릴리즈 감지
            if pipeline_ok:
                progress.progress(90, text="🔍 4/4 — 릴리즈 감지 중...")
                releases = detect_releases()
                if releases:
                    progress.progress(95, text=f"🚀 {len(releases)}건 릴리즈 감지!")

            # 5. 완료
            progress.progress(100, text="✅ 파이프라인 완료!")
            if pipeline_ok:
                st.success("⚡ 수집 → 분석 → 브리핑 완료!")
                if alerted:
                    st.info(f"🔔 {len(alerted)}건 키워드 알림")
                if releases:
                    st.info(f"🚀 {len(releases)}건 릴리즈 감지!")
            import time
            time.sleep(1.5)
            progress.empty()

    # ── ChromaDB 벡터 동기화 ──
    try:
        from ai.vector_store import get_count
        _vec_count = get_count()
    except Exception:
        _vec_count = 0
    if st.button(f"🧠 벡터 동기화 ({_vec_count}개)", use_container_width=True, help="기존 기사를 시맨틱 검색 DB에 동기화 (최초 1회)"):
        try:
            with st.spinner("🧠 동기화 중..."):
                from ai.vector_store import sync_existing_articles
                synced = sync_existing_articles(get_articles(limit=5000))
            if synced > 0:
                st.success(f"✅ {synced}개 동기화!")
            else:
                st.caption("이미 최신 상태")
        except Exception as e:
            st.error(f"동기화 오류: {str(e)[:60]}")

    st.divider()

    with st.expander("🔍 필터"):
        category_filter = st.multiselect("카테고리", list(CATEGORIES.keys()), format_func=lambda x: CATEGORIES[x], key="cf")
        sentiment_filter = st.multiselect("감성", list(SENTIMENTS.keys()), format_func=lambda x: SENTIMENTS[x], key="sf")
        importance_filter = st.slider("최소 중요도", 1, 5, 1, key="if")
        # 필터 변경 시 페이지 리셋
        _filter_key = f"{category_filter}_{sentiment_filter}_{importance_filter}"
        if st.session_state.get("_last_filter_key") != _filter_key:
            st.session_state["_last_filter_key"] = _filter_key
            st.session_state["page"] = 1

    with st.expander("👀 워치리스트"):
        watchlist_keywords = get_active_keywords()
        new_kw = st.text_input("키워드", placeholder="예: Claude, Flux", label_visibility="collapsed")
        if new_kw and st.button("➕ 추가", key="add_kw", use_container_width=True):
            kw_clean = new_kw.strip()[:50]
            from utils.helpers import now_iso
            add_watchlist_keyword(kw_clean, now_iso())
            st.rerun()
        if watchlist_keywords:
            st.markdown(" ".join([f"`{k}`" for k in watchlist_keywords]))

    with st.expander("📰 소스 관리"):
        sources = load_sources()
        for s in sources:
            s["is_active"] = st.checkbox(s["name"], value=s.get("is_active", True), key=f"src_{s['id']}")
        if st.button("💾 저장", use_container_width=True, key="save_src"):
            for s in sources:
                upsert_source(s)
            st.success("저장됨!")

    @st.fragment(run_every=300)
    def sidebar_stats():
        total = get_article_count()
        processed = get_processed_count()
        st.divider()
        st.caption(f"📊 {total:,}개 수집 | {processed:,}개 분석")
        if total > 0:
            st.progress(processed / total, text=f"AI 처리율 {processed / total:.0%}")
    sidebar_stats()


# ── 실시간 알림 ──
@st.fragment(run_every=300)
def new_articles_banner():
    total = get_article_count()
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
_total_count = get_article_count()
_proc_count = get_processed_count()
pri_for_m = load_primary_articles()
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("ARTICLES", f"{_total_count:,}", delta=f"{_proc_count} analyzed" if _proc_count else None)
with m2:
    p_cnt = len([a for a in pri_for_m if a.get("sentiment") == "positive"])
    pct = round(p_cnt / max(len(pri_for_m), 1) * 100)
    st.metric("POSITIVE", f"{pct}%", delta=f"{p_cnt} articles")
with m3:
    bm_count = len(get_bookmarks())
    st.metric("BOOKMARKS", f"{bm_count}")
with m4:
    active_src = len([s for s in load_sources() if s.get("is_active")])
    st.metric("SOURCES", f"{active_src}", delta="active")

# ══════════════════════════════════════════════
# 5탭 구성
# ══════════════════════════════════════════════
tab_dash, tab_news, tab_ai, tab_insight, tab_share, tab_graph = st.tabs(
    ["🏠 대시보드", "📰 뉴스피드", "💬 AI", "📊 인사이트", "📢 공유", "🕸️ 그래프"]
)

# ══════════════════════════════════════════════
# 탭 1: 대시보드
# ══════════════════════════════════════════════
with tab_dash:
    # 브리핑
    briefings = get_briefings(limit=10)
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
        # 카테고리 변경 시 페이지 리셋
        if st.session_state.get("_last_news_cat") != news_cat:
            st.session_state["_last_news_cat"] = news_cat
            st.session_state["page"] = 1
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
                    display_title = article.get("title_ko") or article["title"]
                    st.markdown(f"#### {prefix}[{display_title}]({article['url']})")
                    if article.get("title_ko") and article.get("title_ko") != article["title"]:
                        st.caption(f"🌐 {article['title'][:80]}")
                    st.markdown(render_cat_pill(category) + " " + render_fc_badge(article), unsafe_allow_html=True)
                    summary = article.get("summary_ko") or article.get("summary_text", "")
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
                    bm_ids = get_bookmark_ids()
                    is_bm = article["id"] in bm_ids
                    if st.button("⭐" if is_bm else "☆", key=f"bm_{article['id']}", use_container_width=True):
                        _toggle_bookmark(article["id"])
                        st.rerun()
                    if not article.get("is_read"):
                        if st.button("📖", key=f"rd_{article['id']}", use_container_width=True, help="읽음"):
                            update_article_fields(article["id"], {"is_read": True})
                            st.cache_data.clear()
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
            if sq:
                results = search_articles(sq.strip()[:200], limit=200)
            else:
                results = load_primary_articles()
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
        bookmarks = get_bookmarks()
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
                        memo = st.text_input("메모", value=bm.get("memo", ""), key=f"m_{bm['article_id']}", placeholder="메모 추가...", label_visibility="collapsed")
                        if memo != bm.get("memo", ""):
                            update_bookmark_memo(bm["article_id"], memo)
                            st.cache_data.clear()
                    with bc2:
                        st.caption(bm.get("created_at", "")[:10])
                        if st.button("🗑️", key=f"db_{bm['article_id']}"):
                            remove_bookmark(bm["article_id"])
                            st.cache_data.clear()
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
    ins_mode = st.radio("", ["🏆 도구 비교", "📈 트렌드", "🚀 릴리즈", "🎭 AI 토론", "📊 주간 리포트"], horizontal=True, key="ins_mode", label_visibility="collapsed")

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

    elif ins_mode == "🚀 릴리즈":
        st.markdown("### 🚀 AI 도구 릴리즈 추적")
        st.caption(f"추적 중: {len(get_tracked_tools())}개 도구")

        # 릴리즈 감지 실행
        if st.button("🔍 릴리즈 스캔", use_container_width=True, key="scan_rel"):
            with st.spinner("🔍 릴리즈 감지 중..."):
                new_rels = detect_releases()
            if new_rels:
                st.success(f"🚀 {len(new_rels)}건 새 릴리즈 감지!")
                st.rerun()
            else:
                st.caption("새 릴리즈가 감지되지 않았습니다.")

        # 히스토리
        history = get_release_history(20)
        if history:
            for rel in history:
                with st.container(border=True):
                    st.markdown(f"{rel.get('tool_icon', '📦')} **{rel.get('tool_name', '')}** — [{rel.get('article_title', '')}]({rel.get('article_url', '')})")
                    st.caption(f"감지: {rel.get('detected_at', '')[:16]} · ⭐ {rel.get('importance', 0)}")
        else:
            st.caption("아직 감지된 릴리즈가 없습니다. '🔍 릴리즈 스캔'을 클릭하거나 뉴스를 수집하세요.")

        # 추적 도구 목록
        with st.expander(f"📋 추적 중인 도구 ({len(get_tracked_tools())}개)"):
            tracked = get_tracked_tools()
            tcols = st.columns(3)
            for idx, (tid, tinfo) in enumerate(tracked.items()):
                with tcols[idx % 3]:
                    st.caption(f"{tinfo['icon']} {tinfo['name']}")

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
            st.session_state.pop("last_debate", None)
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

# ══════════════════════════════════════════════
# 탭 6: 지식 그래프 (Knowledge Graph)
# ══════════════════════════════════════════════
with tab_graph:
    st.markdown("### 🕸️ 지식 그래프 — 태그 공동 출현 네트워크")
    st.caption("같은 기사에 함께 등장한 태그들을 엣지로 연결합니다. 노드 크기 = 기사 수, 색상 = 주요 카테고리.")

    from ai.knowledge_graph import (
        build_graph, build_plotly_figure,
        get_top_connected_tags, get_related_articles,
    )

    gc1, gc2, gc3, gc4 = st.columns([2, 1, 1, 1])
    with gc1:
        graph_cats = st.multiselect(
            "카테고리 필터", list(CATEGORIES.keys()),
            default=list(CATEGORIES.keys()),
            format_func=lambda x: CATEGORIES[x], key="gcat",
        )
    with gc2:
        top_n = st.slider("상위 노드 수", 20, 120, 60, 10, key="gtn")
    with gc3:
        min_w = st.slider("최소 엣지 가중치", 1, 5, 2, 1, key="gmw")
    with gc4:
        highlight = st.text_input("🔦 강조할 태그", placeholder="예: claude", key="ghl", label_visibility="visible")

    graph_source = [a for a in pri_for_m if a.get("category") in graph_cats]

    if not graph_source:
        st.caption("선택한 카테고리에 기사가 없습니다. 필터를 넓혀 보세요.")
    else:
        @st.cache_data(ttl=120)
        def _compute_graph(cats_key: tuple, top_n: int, min_w: int):
            source = [a for a in load_primary_articles() if a.get("category") in cats_key]
            return build_graph(source, top_n=top_n, min_edge_weight=min_w)

        gdata = _compute_graph(tuple(sorted(graph_cats)), top_n, min_w)

        gm1, gm2, gm3 = st.columns(3)
        gm1.metric("🔵 노드", len(gdata["nodes"]))
        gm2.metric("🔗 엣지", len(gdata["edges"]))
        gm3.metric("📰 분석 기사", gdata["total_articles"])

        left, right = st.columns([3, 1])
        with left:
            fig = build_plotly_figure(gdata, highlight_tag=highlight)
            if fig is None:
                st.info("💡 연결된 태그가 없습니다. 최소 엣지 가중치를 1로 낮춰 보세요.")
            else:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with right:
            st.markdown("**🔗 허브 태그 TOP 10**")
            top_hubs = get_top_connected_tags(gdata, n=10)
            if not top_hubs:
                st.caption("허브 태그가 없습니다.")
            else:
                for h in top_hubs:
                    with st.expander(f"**{h['id']}** · {h['count']}기사 (연결 {h['degree']})"):
                        rel = get_related_articles(h["id"], graph_source, limit=5)
                        for a in rel:
                            importance_marks = "⭐" * a.get("importance", 0)
                            st.markdown(f"{importance_marks} [{a['title'][:70]}]({a['url']})")
                            if a.get("summary_text"):
                                st.caption(a["summary_text"][:120])
