"""AI News Radar — Streamlit 메인 대시보드 (UI/UX Enhanced)"""
import os
import streamlit as st
from datetime import datetime, timedelta

from config import DATA_DIR, CATEGORIES, SENTIMENTS
from utils.helpers import safe_read_json, safe_write_json, today_str, log
from crawler.rss_crawler import crawl_all, load_sources
from crawler.scheduler import start_scheduler
from ai.batch_processor import process_unprocessed
from ai.deduplicator import deduplicate
from ai.briefing import generate_daily_briefing
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
from sns.card_generator import generate_single_card, generate_briefing_card, generate_category_cards
from sns.poster import get_available_platforms, post_article, post_briefing, PLATFORM_ADAPTERS

# ── 페이지 설정 ──
st.set_page_config(
    page_title="AI News Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 글로벌 CSS (향상된 UI) ──
ENHANCED_CSS = """
<style>
/* 글로벌 폰트 + 부드러운 전환 */
* { transition: all 0.15s ease; }

/* 메트릭 카드 스타일 */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(79,195,247,0.08) 0%, rgba(129,212,250,0.04) 100%);
    border: 1px solid rgba(79,195,247,0.15);
    border-radius: 12px;
    padding: 12px 16px;
}
[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; }

/* 탭 스타일 개선 */
button[data-baseweb="tab"] {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    border-radius: 8px 8px 0 0 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4FC3F7 0%, #29B6F6 100%) !important;
    color: white !important;
}

/* 카드 컨테이너 호버 */
[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
    border-radius: 12px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(79,195,247,0.12);
}

/* 챗 메시지 둥글게 */
[data-testid="stChatMessage"] { border-radius: 16px !important; }

/* 버튼 스타일 */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* Expander 둥글게 */
[data-testid="stExpander"] { border-radius: 10px !important; }

/* 감성 컬러 바 */
.sentiment-bar {
    height: 4px;
    border-radius: 2px;
    margin-bottom: 8px;
}
.sentiment-positive { background: linear-gradient(90deg, #6bcb77, #4caf50); }
.sentiment-neutral { background: linear-gradient(90deg, #ffd93d, #ffc107); }
.sentiment-negative { background: linear-gradient(90deg, #ff6b6b, #f44336); }

/* 카테고리 pill 배지 */
.cat-pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 4px;
}
.cat-ai_tool { background: rgba(33,150,243,0.15); color: #2196F3; }
.cat-ai_research { background: rgba(156,39,176,0.15); color: #9C27B0; }
.cat-ai_trend { background: rgba(255,152,0,0.15); color: #FF9800; }
.cat-ai_tutorial { background: rgba(76,175,80,0.15); color: #4CAF50; }
.cat-ai_business { background: rgba(233,30,99,0.15); color: #E91E63; }
.cat-ai_image_video { background: rgba(255,64,129,0.15); color: #FF4081; }
.cat-ai_coding { background: rgba(0,230,118,0.15); color: #00E676; }
.cat-ai_ontology { background: rgba(124,77,255,0.15); color: #7C4DFF; }
.cat-ai_other { background: rgba(158,158,158,0.15); color: #9E9E9E; }

/* 팩트체크 배지 */
.fc-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 600;
}
.fc-high { background: rgba(76,175,80,0.15); color: #4CAF50; }
.fc-medium { background: rgba(76,175,80,0.10); color: #66BB6A; }
.fc-low { background: rgba(255,152,0,0.15); color: #FF9800; }
.fc-single { background: rgba(244,67,54,0.10); color: #EF5350; }

/* 타임라인 스타일 */
.timeline-dot {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
}
.timeline-dot-today { background: #4FC3F7; }
.timeline-dot-yesterday { background: #81C784; }
.timeline-dot-week { background: #FFB74D; }
.timeline-dot-old { background: #90A4AE; }

/* 페이드인 애니메이션 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
.main .block-container { animation: fadeIn 0.3s ease; }

/* 히어로 그라데이션 헤더 */
.hero-header {
    background: linear-gradient(135deg, #1a237e 0%, #0d47a1 40%, #01579b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.1rem;
    font-weight: 700;
}

/* ── 반응형 (모바일/태블릿) ── */
@media (max-width: 768px) {
    [data-testid="stMetric"] { padding: 8px 10px; }
    [data-testid="stMetricValue"] { font-size: 1.3rem !important; }
    button[data-baseweb="tab"] { font-size: 0.8rem !important; padding: 6px 8px !important; }
    .cat-pill { font-size: 0.65rem; padding: 1px 6px; }
    .fc-badge { font-size: 0.6rem; padding: 1px 5px; }
}

/* ── 데스크톱 와이드 (1600px+) ── */
@media (min-width: 1600px) {
    .main .block-container { max-width: 1400px; }
}

/* 스크롤바 커스텀 (다크모드) */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.05); }
::-webkit-scrollbar-thumb { background: rgba(79,195,247,0.3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(79,195,247,0.5); }

/* 선택 텍스트 하이라이트 */
::selection { background: rgba(79,195,247,0.3); }
</style>
"""
st.markdown(ENHANCED_CSS, unsafe_allow_html=True)

# ── 라이트모드 추가 CSS ──
LIGHT_CSS = """
<style>
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"],
    [data-testid="stHeader"], .main {
        background-color: #FFFFFF !important;
        color: #1E1E1E !important;
    }
    [data-testid="stSidebar"] { background-color: #F5F7FA !important; }
    [data-testid="stSidebar"] * { color: #1E1E1E !important; }
    .main * { color: #1E1E1E !important; }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 { color: #1E1E1E !important; }
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stTextInput label, .stCheckbox label { color: #1E1E1E !important; }
    div[data-testid="stExpander"] { border-color: #E0E0E0 !important; }
    div[data-baseweb="select"] { background-color: #FFFFFF !important; }
</style>
"""

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if not st.session_state.dark_mode:
    st.markdown(LIGHT_CSS, unsafe_allow_html=True)

# ── LLM 프로바이더 체크 ──
_active_provider = get_active_provider()

# ── 자동 스케줄러 시작 (세션당 1회) ──
if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

ARTICLES_PATH = DATA_DIR / "articles.json"
SOURCES_PATH = DATA_DIR / "sources.json"
WATCHLIST_PATH = DATA_DIR / "watchlist.json"
BRIEFINGS_PATH = DATA_DIR / "briefings.json"
BOOKMARKS_PATH = DATA_DIR / "bookmarks.json"

SENTIMENT_COLORS = {"positive": "#6bcb77", "neutral": "#ffd93d", "negative": "#ff6b6b"}
CAT_NAMES = {"ai_tool": "도구", "ai_research": "연구", "ai_trend": "트렌드", "ai_tutorial": "튜토리얼", "ai_business": "비즈니스", "ai_image_video": "이미지/영상", "ai_coding": "바이브코딩", "ai_ontology": "온톨로지", "ai_other": "기타"}


# ── 데이터 로드 ──
def load_articles():
    return safe_read_json(ARTICLES_PATH, [])


def load_primary_articles():
    articles = load_articles()
    return [a for a in articles if a.get("is_primary", True) and a.get("ai_processed")]


# ── 유틸리티 ──
def render_cat_pill(category):
    name = CAT_NAMES.get(category, "기타")
    return f'<span class="cat-pill cat-{category}">{name}</span>'


def render_fc_badge(article):
    fc = get_factcheck_badge(article)
    return f'<span class="fc-badge fc-{fc["level"]}">{fc["label"]}</span>'


def render_sentiment_bar(sentiment):
    cls = f"sentiment-{sentiment}" if sentiment in SENTIMENT_COLORS else "sentiment-neutral"
    return f'<div class="sentiment-bar {cls}"></div>'


# ── 사이드바 ──
with st.sidebar:
    st.markdown("## 📡 AI News Radar")
    st.caption("AI 뉴스 자동 수집 · 요약 · 분류")

    # 다크/라이트 토글
    theme_label = "🌙 다크모드" if st.session_state.dark_mode else "☀️ 라이트모드"
    if st.toggle(theme_label, value=st.session_state.dark_mode, key="theme_toggle"):
        if not st.session_state.dark_mode:
            st.session_state.dark_mode = True
            st.rerun()
    else:
        if st.session_state.dark_mode:
            st.session_state.dark_mode = False
            st.rerun()

    st.divider()

    # LLM 상태 (컴팩트)
    if _active_provider:
        provider_info = PROVIDERS[_active_provider]
        st.caption(f"🤖 **{provider_info['name']}** 활성")
        available = get_available_providers()
        if len(available) > 1:
            with st.expander(f"🔌 {len(available)}개 프로바이더"):
                for p in available:
                    icon = "✅" if p["id"] == _active_provider else "⚪"
                    multi = " 🖼️" if p["multimodal"] else ""
                    st.caption(f"{icon} {p['name']}{multi}")
    else:
        st.error("⚠️ API 키 미설정 — `.env` 파일 확인")

    st.divider()

    # 액션 버튼 (아이콘 + 라벨)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 수집", use_container_width=True):
            try:
                with st.spinner("📡 RSS 수집 중..."):
                    count = crawl_all()
                st.success(f"✅ {count}개 새 글!")
            except Exception as e:
                st.error("수집 오류")
                log(f"[수집 오류] {e}")
    with col2:
        if st.button("🤖 AI 처리", use_container_width=True):
            if not _active_provider:
                st.error("API 키 필요")
            else:
                try:
                    with st.spinner("🧠 AI 분석 중..."):
                        processed = process_unprocessed()
                        deduplicate()
                    st.success(f"✅ {processed}개 완료!")
                except Exception as e:
                    st.error("AI 처리 오류")
                    log(f"[AI 처리 오류] {e}")

    if st.button("📋 브리핑 생성", use_container_width=True):
        if not _active_provider:
            st.error("API 키 필요")
        else:
            try:
                with st.spinner("📝 브리핑 생성 중..."):
                    briefing = generate_daily_briefing()
                if briefing:
                    st.success("✅ 브리핑 완료!")
                else:
                    st.warning("기사 부족")
            except Exception as e:
                st.error("브리핑 오류")
                log(f"[브리핑 오류] {e}")

    st.divider()

    # 필터
    with st.expander("🔍 필터", expanded=False):
        category_filter = st.multiselect(
            "카테고리", options=list(CATEGORIES.keys()),
            format_func=lambda x: CATEGORIES[x],
        )
        sentiment_filter = st.multiselect(
            "감성", options=list(SENTIMENTS.keys()),
            format_func=lambda x: SENTIMENTS[x],
        )
        importance_filter = st.slider("최소 중요도", 1, 5, 1)

    # 워치리스트
    with st.expander("👀 워치리스트"):
        watchlist = safe_read_json(WATCHLIST_PATH, [])
        watchlist_keywords = [w["keyword"] for w in watchlist if w.get("is_active")]
        new_keyword = st.text_input("키워드 추가", placeholder="예: Claude, MCP", label_visibility="collapsed")
        if new_keyword and st.button("➕ 추가", key="add_kw", use_container_width=True):
            watchlist.append({"keyword": new_keyword, "is_active": True, "created_at": today_str()})
            safe_write_json(WATCHLIST_PATH, watchlist)
            st.rerun()
        if watchlist_keywords:
            st.markdown(" ".join([f"`{k}`" for k in watchlist_keywords]))

    # 소스 관리
    with st.expander("📰 소스 관리"):
        sources = load_sources()
        for s in sources:
            s["is_active"] = st.checkbox(s["name"], value=s.get("is_active", True), key=f"src_{s['id']}")
        if st.button("💾 소스 저장", use_container_width=True):
            safe_write_json(SOURCES_PATH, sources)
            st.success("저장됨!")
        new_name = st.text_input("새 소스 이름")
        new_url = st.text_input("RSS URL")
        if new_name and new_url and st.button("➕ 소스 추가", use_container_width=True):
            from utils.helpers import generate_id, now_iso
            sources.append({
                "id": generate_id("src"), "name": new_name, "url": new_url,
                "type": "rss", "is_preset": False, "crawl_interval": 60,
                "is_active": True, "lang": "en", "last_crawled_at": None, "created_at": now_iso(),
            })
            safe_write_json(SOURCES_PATH, sources)
            st.success(f"'{new_name}' 추가됨!")
            st.rerun()

    # 통계 (자동 갱신)
    @st.fragment(run_every=300)
    def sidebar_stats():
        all_arts = load_articles()
        processed_arts = [a for a in all_arts if a.get("ai_processed")]
        st.divider()
        st.caption(f"📊 총 {len(all_arts)}개 | AI {len(processed_arts)}개")
        if all_arts:
            latest = max((a.get("crawled_at", "") for a in all_arts), default="")
            if latest:
                st.caption(f"🕐 {latest[:16]}")

    sidebar_stats()


# ── 실시간 갱신 ──
@st.fragment(run_every=300)
def new_articles_banner():
    all_arts = load_articles()
    total = len(all_arts)
    if "last_article_count" not in st.session_state:
        st.session_state.last_article_count = total
    elif total > st.session_state.last_article_count:
        new_count = total - st.session_state.last_article_count
        st.toast(f"📡 새 글 {new_count}개 수집!", icon="🆕")
        st.session_state.last_article_count = total
    else:
        st.session_state.last_article_count = total

new_articles_banner()


# ── 메인 영역 ──
articles = load_primary_articles()

# 필터 적용
if category_filter:
    articles = [a for a in articles if a.get("category") in category_filter]
if sentiment_filter:
    articles = [a for a in articles if a.get("sentiment") in sentiment_filter]
articles = [a for a in articles if a.get("importance", 0) >= importance_filter]


def is_watchlisted(article):
    text = f"{article.get('title', '')} {' '.join(article.get('tags', []))}".lower()
    return any(k.lower() in text for k in watchlist_keywords)


# ── 히어로 메트릭 (상단 통계 카드) ──
all_arts_for_metrics = load_articles()
processed_for_metrics = [a for a in all_arts_for_metrics if a.get("ai_processed")]
primary_for_metrics = [a for a in processed_for_metrics if a.get("is_primary", True)]

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("📰 총 기사", f"{len(all_arts_for_metrics)}개")
with m2:
    pos_count = len([a for a in primary_for_metrics if a.get("sentiment") == "positive"])
    total_p = len(primary_for_metrics) or 1
    st.metric("😊 긍정 비율", f"{round(pos_count / total_p * 100)}%")
with m3:
    bm_count = len(safe_read_json(BOOKMARKS_PATH, []))
    st.metric("⭐ 북마크", f"{bm_count}개")
with m4:
    sources_active = len([s for s in load_sources() if s.get("is_active")])
    st.metric("📡 활성 소스", f"{sources_active}개")

st.markdown("")  # spacer

# ── 탭 구성 ──
tab_briefing, tab_list, tab_search, tab_chat, tab_glossary, tab_competitor, tab_sns, tab_timeline, tab_bookmarks, tab_sources = st.tabs(
    ["📋 브리핑", "📰 뉴스", "🔍 검색", "💬 AI 채팅", "📚 용어 사전", "🏆 도구 비교", "📢 SNS", "⏰ 타임라인", "⭐ 북마크", "📡 소스"]
)

# ═══════════════════════════════════════════════
# 탭 1: 오늘의 브리핑
# ═══════════════════════════════════════════════
with tab_briefing:
    briefings = safe_read_json(BRIEFINGS_PATH, [])
    today_briefing = next((b for b in briefings if b.get("date") == today_str()), None)

    if today_briefing:
        st.markdown(f"### 📋 오늘의 AI 브리핑 — {today_str()}")

        # 총평 (강조 박스)
        if today_briefing.get("summary"):
            st.info(f"💡 **총평:** {today_briefing['summary']}")

        # TOP 기사 (넘버 배지 + 카드)
        top = today_briefing.get("top_articles", [])
        if isinstance(top, list):
            for i, item in enumerate(top, 1):
                if isinstance(item, dict):
                    headline = item.get("headline", item.get("title", ""))
                    why = item.get("why_important", item.get("summary", ""))
                    with st.container(border=True):
                        st.markdown(f"**#{i}** &nbsp; {headline}")
                        if why:
                            st.caption(f"→ {why}")

        # 내보내기 + 음성
        st.divider()
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        with exp_col1:
            md_content = export_briefing_markdown()
            st.download_button("📥 Markdown", data=md_content, file_name=f"ai_briefing_{today_str()}.md", mime="text/markdown", use_container_width=True)
        with exp_col2:
            try:
                pdf_content = export_briefing_pdf()
                st.download_button("📥 PDF", data=pdf_content, file_name=f"ai_briefing_{today_str()}.pdf", mime="application/pdf", use_container_width=True)
            except Exception as e:
                st.caption(f"PDF 불가: {e}")
        with exp_col3:
            voices = get_available_voices()
            voice_choice = st.selectbox("🔊 음성", options=[v["id"] for v in voices], format_func=lambda x: next(v["name"] for v in voices if v["id"] == x), key="voice_select", label_visibility="collapsed")

        if st.button("🎙️ 음성 브리핑 생성", use_container_width=True, key="gen_voice"):
            try:
                with st.spinner("🎵 음성 생성 중... (10~20초)"):
                    audio_path = generate_voice_briefing(today_briefing, voice=voice_choice)
                if audio_path:
                    st.session_state.voice_audio_path = audio_path
                    st.rerun()
                else:
                    st.warning("음성 생성 실패")
            except ImportError:
                st.error("`pip install edge-tts` 필요")
            except Exception as e:
                st.error(f"오류: {e}")

        audio_path = st.session_state.get("voice_audio_path")
        if audio_path and os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button("📥 MP3 다운로드", data=audio_bytes, file_name=f"ai_briefing_{today_str()}.mp3", mime="audio/mpeg", use_container_width=True)
    else:
        st.markdown("### 📋 브리핑")
        st.markdown("")
        st.markdown("아직 오늘의 브리핑이 없습니다.")
        st.markdown("사이드바에서 **📋 브리핑 생성**을 클릭하세요.")
        st.markdown("")
        st.caption("💡 먼저 '🔄 수집' → '🤖 AI 처리' → '📋 브리핑 생성' 순서로 진행하세요.")

    # ── 관심 분야별 맞춤 브리핑 ──
    if today_briefing and today_briefing.get("focus_briefings"):
        st.divider()
        st.markdown("### 🎯 관심 분야별 맞춤 브리핑")
        focus = today_briefing["focus_briefings"]

        focus_cols = st.columns(len(focus))
        for idx, (area_id, area_data) in enumerate(focus.items()):
            with focus_cols[idx]:
                icon = area_data.get("icon", "📌")
                name = area_data.get("name", area_id)
                total = area_data.get("total_count", 0)
                st.markdown(f"#### {icon} {name}")
                st.caption(f"관련 뉴스 {total}건")

                top_arts = area_data.get("top_articles", [])
                if top_arts:
                    for i, item in enumerate(top_arts, 1):
                        sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(item.get("sentiment", ""), "")
                        stars = "⭐" * item.get("importance", 0)
                        with st.container(border=True):
                            st.markdown(f"**#{i}** [{item['title']}]({item['url']})")
                            if item.get("summary"):
                                st.caption(item["summary"][:100])
                            st.caption(f"{stars} {sentiment_emoji}")
                else:
                    st.caption("관련 뉴스 없음")
    elif articles:
        # 브리핑 없어도 기사가 있으면 분야별 카운트만 표시
        from ai.briefing import FOCUS_AREAS
        st.divider()
        st.markdown("### 🎯 관심 분야 현황")
        fc_cols = st.columns(len(FOCUS_AREAS))
        for idx, (area_id, area_info) in enumerate(FOCUS_AREAS.items()):
            with fc_cols[idx]:
                count = len([a for a in articles if a.get("category") == area_id])
                st.metric(f"{area_info['icon']} {area_info['name']}", f"{count}건")

    # ── 감성 온도계 ──
    if articles:
        import plotly.graph_objects as go

        st.divider()
        st.markdown("### 🌡️ AI 뉴스 감성 온도계")

        pos = len([a for a in articles if a.get("sentiment") == "positive"])
        neu = len([a for a in articles if a.get("sentiment") == "neutral"])
        neg = len([a for a in articles if a.get("sentiment") == "negative"])
        total = pos + neu + neg
        pos_pct = round(pos / total * 100) if total else 0

        chart_col1, chart_col2 = st.columns([1, 1])

        with chart_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pos_pct,
                number={"suffix": "%", "font": {"size": 36}},
                title={"text": "긍정 뉴스 비율", "font": {"size": 14}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar": {"color": "#4FC3F7", "thickness": 0.75},
                    "steps": [
                        {"range": [0, 33], "color": "rgba(255,107,107,0.2)"},
                        {"range": [33, 66], "color": "rgba(255,217,61,0.2)"},
                        {"range": [66, 100], "color": "rgba(107,203,119,0.2)"},
                    ],
                    "threshold": {"line": {"color": "#4FC3F7", "width": 3}, "thickness": 0.8, "value": pos_pct},
                },
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=50, b=10, l=30, r=30), paper_bgcolor="rgba(0,0,0,0)", font={"color": "gray"})
            st.plotly_chart(fig_gauge, use_container_width=True)

        with chart_col2:
            fig_donut = go.Figure(go.Pie(
                labels=["😊 긍정", "😐 중립", "😠 부정"],
                values=[pos, neu, neg],
                hole=0.6,
                marker=dict(colors=["#6bcb77", "#ffd93d", "#ff6b6b"]),
                textinfo="label+percent",
                textfont=dict(size=12),
                hoverinfo="label+value+percent",
            ))
            fig_donut.update_layout(height=250, margin=dict(t=30, b=10, l=0, r=0), showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font={"color": "gray"})
            st.plotly_chart(fig_donut, use_container_width=True)

        # 카테고리별 감성
        cat_data = {}
        for a in articles:
            cat = CATEGORIES.get(a.get("category", ""), a.get("category", "기타"))
            sent = a.get("sentiment", "neutral")
            if cat not in cat_data:
                cat_data[cat] = {"positive": 0, "neutral": 0, "negative": 0}
            cat_data[cat][sent] = cat_data[cat].get(sent, 0) + 1

        if cat_data:
            cats_sorted = sorted(cat_data.keys())
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(name="😊 긍정", x=cats_sorted, y=[cat_data[c]["positive"] for c in cats_sorted], marker_color="#6bcb77", marker_cornerradius=4))
            fig_bar.add_trace(go.Bar(name="😐 중립", x=cats_sorted, y=[cat_data[c]["neutral"] for c in cats_sorted], marker_color="#ffd93d", marker_cornerradius=4))
            fig_bar.add_trace(go.Bar(name="😠 부정", x=cats_sorted, y=[cat_data[c]["negative"] for c in cats_sorted], marker_color="#ff6b6b", marker_cornerradius=4))
            fig_bar.update_layout(barmode="stack", height=280, margin=dict(t=30, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.02), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "gray"})
            fig_bar.update_xaxes(showgrid=False)
            fig_bar.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.1)")
            st.plotly_chart(fig_bar, use_container_width=True)

    # ── 주간 인텔리전스 리포트 ──
    st.divider()
    st.markdown("### 📊 주간 AI 인텔리전스 리포트")

    wr_col1, wr_col2 = st.columns([3, 1])
    with wr_col2:
        if st.button("📊 리포트 생성", use_container_width=True, key="gen_weekly"):
            if not _active_provider:
                st.error("API 키 필요")
            else:
                try:
                    with st.spinner("📊 주간 리포트 생성 중..."):
                        report = generate_weekly_report()
                    if report:
                        st.success("✅ 주간 리포트 완료!")
                        st.rerun()
                    else:
                        st.warning("기사 부족")
                except Exception as e:
                    st.error(f"오류: {e}")

    latest_report = get_latest_report()
    if latest_report:
        with wr_col1:
            st.caption(f"📅 {latest_report['week_start']} ~ {latest_report['week_end']}")

        stats = latest_report.get("stats", {})
        trends = latest_report.get("trends")

        # 통계 메트릭
        wr_m1, wr_m2, wr_m3, wr_m4 = st.columns(4)
        with wr_m1:
            st.metric("총 기사", f"{stats.get('total', 0)}개")
        with wr_m2:
            st.metric("평균 중요도", f"{stats.get('avg_importance', 0)}")
        with wr_m3:
            focus_c = stats.get("focus_counts", {})
            total_focus = sum(focus_c.values())
            st.metric("관심 분야", f"{total_focus}건")
        with wr_m4:
            pos = stats.get("sentiment", {}).get("positive", 0)
            total_s = stats.get("total", 1) or 1
            st.metric("긍정 비율", f"{round(pos / total_s * 100)}%")

        # 트렌드
        if trends:
            st.markdown("#### 🔥 핵심 트렌드")
            for i, t in enumerate(trends.get("key_trends", []), 1):
                st.markdown(f"**{i}.** {t}")

            # 분야별 동향
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                with st.container(border=True):
                    st.markdown(f"**🎨 이미지/영상**")
                    st.caption(trends.get("image_video_trend", "-"))
            with fc2:
                with st.container(border=True):
                    st.markdown(f"**💻 바이브코딩**")
                    st.caption(trends.get("coding_trend", "-"))
            with fc3:
                with st.container(border=True):
                    st.markdown(f"**🔮 온톨로지**")
                    st.caption(trends.get("ontology_trend", "-"))

            # 전망 + 실천 제안
            if trends.get("outlook"):
                st.markdown("#### 🔭 다음 주 전망")
                st.info(trends["outlook"])

            actions = trends.get("action_items", [])
            if actions:
                st.markdown("#### ✅ 실천 제안")
                for a in actions:
                    st.markdown(f"- {a}")

        # TOP 10 + 내보내기
        top_arts = latest_report.get("top_articles", [])
        if top_arts:
            with st.expander(f"📰 주목할 뉴스 TOP {len(top_arts)}"):
                for i, a in enumerate(top_arts, 1):
                    stars = "⭐" * a.get("importance", 0)
                    st.markdown(f"{i}. {stars} [{a['title']}]({a['url']})")
                    if a.get("summary"):
                        st.caption(f"   {a['summary']}")

        # Markdown 내보내기
        md_report = export_weekly_report_markdown(latest_report)
        st.download_button(
            "📥 주간 리포트 Markdown",
            data=md_report,
            file_name=f"weekly_report_{latest_report['week_start']}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        with wr_col1:
            st.caption("아직 주간 리포트가 없습니다. '📊 리포트 생성' 버튼을 클릭하세요.")

# ═══════════════════════════════════════════════
# 탭 2: 뉴스 목록
# ═══════════════════════════════════════════════
with tab_list:
    col_header, col_sort, col_export = st.columns([2, 1, 1])
    with col_header:
        st.markdown(f"### 📰 AI 뉴스 ({len(articles)}개)")
    with col_sort:
        sort_option = st.selectbox("정렬", ["중요도 높은 순", "최신순", "긍정 먼저"], label_visibility="collapsed")
    with col_export:
        if articles:
            exp_fmt = st.selectbox("형식", ["Markdown", "PDF"], label_visibility="collapsed", key="export_fmt")

    if sort_option == "중요도 높은 순":
        articles.sort(key=lambda x: x.get("importance", 0), reverse=True)
    elif sort_option == "최신순":
        articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    elif sort_option == "긍정 먼저":
        order = {"positive": 0, "neutral": 1, "negative": 2}
        articles.sort(key=lambda x: order.get(x.get("sentiment", "neutral"), 1))

    if articles and exp_fmt == "Markdown":
        md_articles = export_articles_markdown(articles)
        st.download_button("📥 내보내기", data=md_articles, file_name=f"ai_news_{today_str()}.md", mime="text/markdown", use_container_width=True, key="dl_md")
    elif articles and exp_fmt == "PDF":
        try:
            pdf_articles = export_articles_pdf(articles)
            st.download_button("📥 내보내기", data=pdf_articles, file_name=f"ai_news_{today_str()}.pdf", mime="application/pdf", use_container_width=True, key="dl_pdf")
        except Exception:
            pass

    if not articles:
        st.markdown("")
        st.markdown("아직 뉴스가 없습니다.")
        st.caption("사이드바에서 '🔄 수집' → '🤖 AI 처리'를 순서대로 실행하세요.")
    else:
        for article in articles:
            watched = is_watchlisted(article)
            prefix = "👀 " if watched else ""
            importance = "⭐" * article.get("importance", 0)
            sentiment = article.get("sentiment", "neutral")
            sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(sentiment, "")
            category = article.get("category", "ai_other")

            with st.container(border=True):
                # 감성 컬러 바
                st.markdown(render_sentiment_bar(sentiment), unsafe_allow_html=True)

                col_main, col_meta = st.columns([4, 1])

                with col_main:
                    # 제목 + 카테고리 pill + 팩트체크 배지
                    st.markdown(f"#### {prefix}[{article['title']}]({article['url']})")

                    # 메타 라인: 카테고리 + 팩트체크
                    meta_html = render_cat_pill(category) + " " + render_fc_badge(article)
                    st.markdown(meta_html, unsafe_allow_html=True)

                    # 3줄 요약
                    summary = article.get("summary_text", "")
                    if summary:
                        st.write(summary)

                    # 자세히 보기
                    with st.expander("📖 자세히 보기"):
                        if article.get("content"):
                            st.write(article["content"][:2000])
                        if st.button("📰 원문 가져오기", key=f"reader_{article['id']}"):
                            with st.spinner("로딩 중..."):
                                clean = fetch_clean_content(article["url"])
                            st.markdown(clean[:3000])
                        st.markdown(f"[🔗 원문 바로가기]({article['url']})")

                    # 이미지 분석
                    image_analysis = article.get("image_analysis", "")
                    if image_analysis:
                        st.caption(f"🖼️ {image_analysis}")

                    # 태그
                    tags = article.get("tags", [])
                    if tags:
                        st.caption(" ".join([f"`{t}`" for t in tags]))

                    # 중복 매체
                    related = article.get("related_articles", [])
                    if related:
                        with st.expander(f"▶ {len(related)}개 매체 추가 보도"):
                            for rel in related:
                                st.caption(f"• [{rel.get('title', '')}]({rel.get('url', '')})")

                with col_meta:
                    st.markdown(f"**{importance}**")
                    st.write(f"{sentiment_emoji}")
                    pub = article.get("published_at", "")[:10]
                    if pub:
                        st.caption(pub)

                    # 북마크
                    bookmarks = safe_read_json(BOOKMARKS_PATH, [])
                    bm_ids = {b["article_id"] for b in bookmarks}
                    is_bm = article["id"] in bm_ids
                    bm_label = "⭐" if is_bm else "☆"
                    if st.button(bm_label, key=f"bm_{article['id']}", use_container_width=True):
                        if is_bm:
                            bookmarks = [b for b in bookmarks if b["article_id"] != article["id"]]
                        else:
                            bookmarks.append({"article_id": article["id"], "memo": "", "created_at": today_str()})
                        safe_write_json(BOOKMARKS_PATH, bookmarks)
                        st.rerun()

                    # 읽음
                    if not article.get("is_read"):
                        if st.button("📖", key=f"read_{article['id']}", help="읽음 표시", use_container_width=True):
                            all_arts = safe_read_json(ARTICLES_PATH, [])
                            for a in all_arts:
                                if a["id"] == article["id"]:
                                    a["is_read"] = True
                                    break
                            safe_write_json(ARTICLES_PATH, all_arts)
                            st.rerun()
                    else:
                        st.caption("✅ 읽음")

# ═══════════════════════════════════════════════
# 탭 3: 검색
# ═══════════════════════════════════════════════
with tab_search:
    st.markdown("### 🔍 뉴스 검색")

    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input("🔍", placeholder="키워드를 입력하세요 (예: Claude, GPT, 삼성)", label_visibility="collapsed")
    with search_col2:
        search_category = st.selectbox("카테고리", ["전체"] + list(CATEGORIES.keys()), format_func=lambda x: "전체" if x == "전체" else CATEGORIES[x], key="search_cat")

    search_col3, search_col4 = st.columns(2)
    with search_col3:
        search_sentiment = st.selectbox("감성", ["전체", "positive", "negative", "neutral"], format_func=lambda x: "전체" if x == "전체" else SENTIMENTS.get(x, x), key="search_sent")
    with search_col4:
        show_read = st.selectbox("읽음", ["전체", "안 읽은 글만", "읽은 글만"], key="search_read")

    if search_query or search_category != "전체" or search_sentiment != "전체" or show_read != "전체":
        all_for_search = load_primary_articles()
        results = all_for_search

        if search_query:
            q = search_query.lower()
            results = [
                a for a in results
                if q in a.get("title", "").lower()
                or q in a.get("summary_text", "").lower()
                or any(q in t.lower() for t in a.get("tags", []))
            ]

        if search_category != "전체":
            results = [a for a in results if a.get("category") == search_category]
        if search_sentiment != "전체":
            results = [a for a in results if a.get("sentiment") == search_sentiment]
        if show_read == "안 읽은 글만":
            results = [a for a in results if not a.get("is_read")]
        elif show_read == "읽은 글만":
            results = [a for a in results if a.get("is_read")]

        st.caption(f"🔎 {len(results)}개 결과")

        for a in results[:50]:
            sentiment = a.get("sentiment", "neutral")
            sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(sentiment, "")
            importance = "⭐" * a.get("importance", 0)
            read_mark = "✅ " if a.get("is_read") else ""
            category = a.get("category", "ai_other")
            with st.container(border=True):
                st.markdown(render_sentiment_bar(sentiment), unsafe_allow_html=True)
                meta_html = render_cat_pill(category) + " " + render_fc_badge(a)
                st.markdown(f"{importance} {sentiment_emoji} {read_mark}[{a['title']}]({a['url']})")
                st.markdown(meta_html, unsafe_allow_html=True)
                summary = a.get("summary_text", "")
                if summary:
                    st.caption(summary[:150])
                tags = a.get("tags", [])
                if tags:
                    st.caption(" ".join([f"`{t}`" for t in tags]))
    else:
        st.markdown("")
        st.caption("검색어를 입력하거나 필터를 선택하세요.")

# ═══════════════════════════════════════════════
# 탭 4: AI 채팅
# ═══════════════════════════════════════════════
with tab_chat:
    st.markdown("### 💬 AI 뉴스 채팅")

    if not _active_provider:
        st.warning("LLM API 키를 먼저 설정해야 채팅을 사용할 수 있습니다.")
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
            if st.button("🗑️ 대화 초기화", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

        # 추천 질문 (클릭 가능 버튼)
        if not st.session_state.chat_history:
            st.divider()
            st.caption("💡 추천 질문을 클릭하세요:")
            suggestions = [
                "오늘 가장 중요한 AI 뉴스 3가지",
                "OpenAI 관련 최신 뉴스",
                "AI 비즈니스 뉴스 정리",
                "부정적인 AI 뉴스는?",
                "삼성 AI 관련 뉴스",
            ]
            cols = st.columns(3)
            for i, s in enumerate(suggestions):
                with cols[i % 3]:
                    if st.button(f"💬 {s}", key=f"sug_{i}", use_container_width=True):
                        st.session_state.chat_suggestion = s
                        st.rerun()

            # 클릭된 추천 질문 처리
            if "chat_suggestion" in st.session_state:
                suggestion = st.session_state.pop("chat_suggestion")
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                response = ai_chat(suggestion)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

# ═══════════════════════════════════════════════
# 탭 5: AI 용어 사전
# ═══════════════════════════════════════════════
with tab_glossary:
    st.markdown("### 📚 AI 용어 사전")
    st.caption("뉴스에 등장하는 AI 전문 용어를 초보자도 이해할 수 있게 설명합니다.")

    gl_col1, gl_col2, gl_col3 = st.columns([3, 1, 1])
    with gl_col1:
        gl_search = st.text_input("🔍 용어 검색", placeholder="예: LLM, RAG, Transformer", key="gl_search", label_visibility="collapsed")
    with gl_col2:
        diff_filter = st.selectbox("난이도", ["전체", "⭐", "⭐⭐", "⭐⭐⭐"], key="gl_diff", label_visibility="collapsed")
    with gl_col3:
        if st.button("🔄 추출", use_container_width=True, key="extract_terms"):
            if not _active_provider:
                st.error("API 키 필요")
            else:
                try:
                    with st.spinner("🧠 용어 추출 중..."):
                        extract_terms_from_articles()
                    st.success("✅ 완료!")
                    st.rerun()
                except Exception as e:
                    st.error(f"오류: {e}")

    terms = search_glossary(gl_search) if gl_search else get_glossary()
    if diff_filter != "전체":
        diff_map = {"⭐": 1, "⭐⭐": 2, "⭐⭐⭐": 3}
        target_diff = diff_map.get(diff_filter, 0)
        terms = [t for t in terms if t.get("difficulty") == target_diff]

    if not terms:
        st.markdown("")
        st.markdown("아직 추출된 용어가 없습니다.")
        st.caption("'🔄 추출' 버튼을 클릭하면 수집된 뉴스에서 AI 용어를 자동으로 찾아냅니다.")
    else:
        st.caption(f"📖 {len(terms)}개 용어")
        cat_labels = {
            "model": "🤖 모델", "technique": "⚙️ 기술", "concept": "💡 개념",
            "product": "📦 제품", "company": "🏢 기업", "other": "📌 기타",
        }

        # 2열 그리드
        cols = st.columns(2)
        for idx, term in enumerate(terms):
            with cols[idx % 2]:
                diff_stars = "⭐" * term.get("difficulty", 1)
                cat = cat_labels.get(term.get("category", "other"), "📌 기타")
                with st.container(border=True):
                    st.markdown(f"**{term.get('term', '')}** ({term.get('term_ko', '')})")
                    st.caption(f"{cat} · {diff_stars} · {term.get('short_desc', '')}")
                    st.write(term.get("full_desc", ""))
                    example = term.get("example", "")
                    if example:
                        st.info(f"💡 {example}")

# ═══════════════════════════════════════════════
# 탭 6: 경쟁 도구 모니터링
# ═══════════════════════════════════════════════
with tab_competitor:
    st.markdown("### 🏆 경쟁 도구 모니터링")
    st.caption("AI 도구별 뉴스 언급량, 감성, 트렌드를 비교합니다.")

    # 분야 선택
    comp_group = st.selectbox(
        "분야 선택",
        options=list(COMPETITOR_GROUPS.keys()),
        format_func=lambda x: f"{COMPETITOR_GROUPS[x]['icon']} {COMPETITOR_GROUPS[x]['name']}",
        key="comp_group",
        label_visibility="collapsed",
    )

    analysis = get_competitor_analysis(comp_group)
    group_data = analysis.get(comp_group, {})
    tools = group_data.get("tools", [])

    if not tools or all(t["mention_count"] == 0 for t in tools):
        st.markdown("")
        st.markdown("아직 비교할 데이터가 없습니다.")
        st.caption("'🔄 수집' → '🤖 AI 처리'를 실행하면 도구별 뉴스가 자동 분류됩니다.")
    else:
        # 언급량 바 차트
        import plotly.graph_objects as go

        tool_names = [t["name"] for t in tools if t["mention_count"] > 0]
        tool_counts = [t["mention_count"] for t in tools if t["mention_count"] > 0]
        tool_colors = [t["color"] for t in tools if t["mention_count"] > 0]

        if tool_names:
            fig_comp = go.Figure(go.Bar(
                x=tool_counts,
                y=tool_names,
                orientation="h",
                marker_color=tool_colors,
                marker_cornerradius=6,
                text=tool_counts,
                textposition="outside",
            ))
            fig_comp.update_layout(
                height=max(200, len(tool_names) * 45),
                margin=dict(t=10, b=10, l=0, r=40),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "gray"},
                yaxis=dict(autorange="reversed"),
                xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        # 도구별 상세 카드
        active_tools = [t for t in tools if t["mention_count"] > 0]
        if active_tools:
            card_cols = st.columns(min(len(active_tools), 3))
            for idx, tool in enumerate(active_tools[:6]):
                with card_cols[idx % min(len(active_tools), 3)]:
                    with st.container(border=True):
                        # 감성 비율 계산
                        total_s = sum(tool["sentiment"].values()) or 1
                        pos_pct = round(tool["sentiment"]["positive"] / total_s * 100)
                        neg_pct = round(tool["sentiment"]["negative"] / total_s * 100)

                        st.markdown(f"**{tool['name']}**")
                        st.caption(f"📰 {tool['mention_count']}건 · ⭐ {tool['avg_importance']} · 😊 {pos_pct}%")

                        # 감성 미니 바
                        pos_w = max(pos_pct, 2)
                        neu_w = max(100 - pos_pct - neg_pct, 2)
                        neg_w = max(neg_pct, 2)
                        st.markdown(
                            f'<div style="display:flex;height:6px;border-radius:3px;overflow:hidden">'
                            f'<div style="width:{pos_w}%;background:#6bcb77"></div>'
                            f'<div style="width:{neu_w}%;background:#ffd93d"></div>'
                            f'<div style="width:{neg_w}%;background:#ff6b6b"></div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                        # TOP 기사
                        for a in tool["top_articles"][:3]:
                            emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment", ""), "")
                            st.caption(f"{emoji} [{a['title'][:40]}...]({a['url']})")

        # ── 트렌드 차트 ──
        st.divider()
        st.markdown("#### 📈 언급량 트렌드")

        trend_days = st.selectbox("기간", [7, 14, 30], index=1, format_func=lambda x: f"최근 {x}일", key="trend_days", label_visibility="collapsed")

        trend_data = get_trend_data(comp_group, days=trend_days)
        if trend_data["tools"]:
            import plotly.graph_objects as go

            fig_trend = go.Figure()
            for tool in trend_data["tools"]:
                fig_trend.add_trace(go.Scatter(
                    x=trend_data["dates"],
                    y=tool["counts"],
                    name=f"{tool['name']} ({tool['total']})",
                    line=dict(color=tool["color"], width=2),
                    mode="lines+markers",
                    marker=dict(size=4),
                    hovertemplate=f"<b>{tool['name']}</b><br>%{{x}}: %{{y}}건<extra></extra>",
                ))
            fig_trend.update_layout(
                height=350,
                margin=dict(t=10, b=10, l=0, r=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "gray"},
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)", title="언급 수"),
                hovermode="x unified",
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.caption("트렌드 데이터가 아직 충분하지 않습니다. 며칠간 수집하면 차트가 나타납니다.")

        # ── 커스텀 키워드 트렌드 ──
        st.markdown("#### 🔍 키워드 트렌드 검색")
        kw_input = st.text_input("키워드", placeholder="예: Flux, ComfyUI, Claude Code", key="trend_kw", label_visibility="collapsed")
        if kw_input:
            kw_trend = get_keyword_trend(kw_input, days=trend_days)
            if kw_trend["total"] > 0:
                import plotly.graph_objects as go

                fig_kw = go.Figure(go.Bar(
                    x=kw_trend["dates"],
                    y=kw_trend["counts"],
                    marker_color="#4FC3F7",
                    marker_cornerradius=4,
                    hovertemplate=f"<b>{kw_input}</b><br>%{{x}}: %{{y}}건<extra></extra>",
                ))
                fig_kw.update_layout(
                    height=250,
                    margin=dict(t=10, b=10, l=0, r=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "gray"},
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
                )
                st.plotly_chart(fig_kw, use_container_width=True)
                st.caption(f"'{kw_input}' 최근 {trend_days}일간 총 {kw_trend['total']}건 언급")
            else:
                st.caption(f"'{kw_input}' — 최근 {trend_days}일간 언급 없음")

        # ── 급상승 키워드 ──
        st.markdown("#### 🔥 급상승 키워드")
        hot = get_hot_keywords(top_n=10, days=7)
        if hot:
            hot_cols = st.columns(5)
            for idx, h in enumerate(hot[:10]):
                with hot_cols[idx % 5]:
                    change = h["change_pct"]
                    if change >= 999:
                        badge = "🆕"
                    elif change > 0:
                        badge = f"🔺{change}%"
                    elif change < 0:
                        badge = f"🔻{abs(change)}%"
                    else:
                        badge = "➡️"
                    with st.container(border=True):
                        st.markdown(f"**`{h['keyword']}`**")
                        st.caption(f"{h['count']}건 {badge}")
        else:
            st.caption("급상승 키워드를 분석할 데이터가 아직 부족합니다.")

        # ── 디베이트 모드 ──
        st.divider()
        st.markdown("#### 🎭 AI 토론 — 도구 비교 디베이트")

        # 추천 대결 쌍 또는 수동 선택
        pairs = get_debate_pairs(comp_group)
        group_tools = COMPETITOR_GROUPS.get(comp_group, {}).get("tools", [])
        tool_names = [t["name"] for t in group_tools]

        db_col1, db_col2, db_col3 = st.columns([2, 2, 1])
        with db_col1:
            tool_a_idx = st.selectbox("도구 A", range(len(tool_names)), format_func=lambda i: tool_names[i], key="debate_a")
        with db_col2:
            default_b = min(1, len(tool_names) - 1)
            tool_b_idx = st.selectbox("도구 B", range(len(tool_names)), index=default_b, format_func=lambda i: tool_names[i], key="debate_b")
        with db_col3:
            run_debate = st.button("⚔️ 토론 시작", use_container_width=True, key="run_debate")

        if run_debate:
            if tool_a_idx == tool_b_idx:
                st.warning("다른 도구를 선택하세요.")
            elif not _active_provider:
                st.error("API 키 필요")
            else:
                tool_a = group_tools[tool_a_idx]
                tool_b = group_tools[tool_b_idx]
                with st.spinner(f"🎭 {tool_a['name']} vs {tool_b['name']} 분석 중..."):
                    debate = generate_debate(
                        tool_a["name"], tool_b["name"],
                        tool_a["keywords"], tool_b["keywords"],
                    )
                if debate:
                    st.session_state.last_debate = debate
                else:
                    st.warning("토론 생성에 실패했습니다. 관련 기사가 부족할 수 있습니다.")

        # 토론 결과 표시
        debate = st.session_state.get("last_debate")
        if debate:
            da = debate.get("tool_a", {})
            db = debate.get("tool_b", {})

            dcol1, dcol2 = st.columns(2)
            with dcol1:
                with st.container(border=True):
                    st.markdown(f"### 🔵 {da.get('name', '도구 A')}")
                    st.markdown("**장점:**")
                    for p in da.get("pros", []):
                        st.markdown(f"✅ {p}")
                    st.markdown("**단점:**")
                    for c in da.get("cons", []):
                        st.markdown(f"⚠️ {c}")

            with dcol2:
                with st.container(border=True):
                    st.markdown(f"### 🔴 {db.get('name', '도구 B')}")
                    st.markdown("**장점:**")
                    for p in db.get("pros", []):
                        st.markdown(f"✅ {p}")
                    st.markdown("**단점:**")
                    for c in db.get("cons", []):
                        st.markdown(f"⚠️ {c}")

            # 결론
            verdict = debate.get("verdict", "")
            rec = debate.get("recommendation", "")
            if verdict:
                st.info(f"🏆 **결론:** {verdict}")
            if rec:
                st.success(f"💡 **추천:** {rec}")

        # 추천 대결 쌍 표시
        if pairs and not debate:
            st.caption("💡 추천 대결:")
            pair_cols = st.columns(min(len(pairs), 3))
            for idx, (pa, pb) in enumerate(pairs[:3]):
                with pair_cols[idx]:
                    st.caption(f"⚔️ {pa['name']} vs {pb['name']}")

# ═══════════════════════════════════════════════
# 탭 7: SNS 카드 뉴스
# ═══════════════════════════════════════════════
with tab_sns:
    st.markdown("### 📢 SNS 카드 뉴스 자동 업로드")
    st.caption("원하는 카테고리의 뉴스를 카드 이미지로 만들어 SNS에 자동 게시합니다.")

    # ── 플랫폼 상태 표시 ──
    platforms = get_available_platforms()
    st.markdown("#### 📱 연결된 플랫폼")
    plat_cols = st.columns(len(platforms))
    for idx, p in enumerate(platforms):
        with plat_cols[idx]:
            status = "🟢 연결됨" if p["configured"] else "⚪ 미설정"
            with st.container(border=True):
                st.markdown(f"**{p['icon']} {p['name']}**")
                st.caption(status)

    configured_platforms = [p for p in platforms if p["configured"]]

    # 설정 가이드 (미연결 플랫폼 있으면 항상 표시)
    unconfigured = [p for p in platforms if not p["configured"]]
    if unconfigured:
        with st.expander(f"⚙️ SNS 연결 설정 가이드 ({len(unconfigured)}개 미연결)", expanded=not configured_platforms):
            st.markdown("`.env` 파일에 아래 키를 추가하세요:")

            st.markdown("""
**🐦 X (Twitter)** — [developer.x.com](https://developer.x.com/) 에서 앱 생성
```
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_SECRET=your_access_secret
```
> 1) developer.x.com → 앱 만들기 → Keys and Tokens 탭 → 4개 키 복사

---

**📨 Telegram** — @BotFather 에서 봇 생성
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=@your_channel_id
```
> 1) 텔레그램에서 @BotFather 검색 → /newbot → 토큰 복사
> 2) 채널 만들고 봇을 관리자로 추가 → 채널 @아이디 입력

---

**💬 Discord** — 서버 설정에서 웹훅 생성 (가장 쉬움, 30초)
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```
> 1) Discord 서버 → 설정 → 연동 → 웹훅 → 새 웹훅 → URL 복사

---

**🧵 Threads** — [developers.facebook.com](https://developers.facebook.com/) 에서 앱 생성
```
THREADS_ACCESS_TOKEN=your_threads_access_token
THREADS_USER_ID=your_threads_user_id
```
> 1) developers.facebook.com → 앱 만들기 → "사용 사례: 기타"
> 2) 제품 추가 → "Threads API" 선택
> 3) API 설정 → "threads_manage_posts" 권한 추가
> 4) 액세스 토큰 생성 → 복사
> 5) 사용자 ID 확인: 그래프 API 탐색기에서 GET /me 실행

---

**📸 Instagram** — Facebook 페이지 + 비즈니스 계정 필요
```
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id
IMGUR_CLIENT_ID=your_imgur_client_id
```
> 1) Instagram 앱 → 설정 → 계정 → "비즈니스 계정으로 전환"
> 2) Facebook 페이지 만들기 → Instagram 계정 연결
> 3) developers.facebook.com → 앱 → Instagram Graph API 추가
> 4) "instagram_basic", "instagram_content_publish" 권한 추가
> 5) 액세스 토큰 생성 → 복사
> 6) 계정 ID: 그래프 API 탐색기에서 GET /me/accounts → instagram_business_account.id
> 7) [api.imgur.com](https://api.imgur.com/oauth2/addclient) → 앱 등록 → Client ID 복사 (이미지 호스팅용)
""")

    if not configured_platforms:
        pass  # 가이드만 표시
    else:
        st.divider()

        # ── 모드 선택 ──
        sns_mode = st.radio("포스트 유형", ["📰 개별 기사", "📋 오늘의 브리핑"], horizontal=True, key="sns_mode")

        # ── 플랫폼 선택 ──
        selected_platforms = []
        sp_cols = st.columns(len(configured_platforms))
        for idx, p in enumerate(configured_platforms):
            with sp_cols[idx]:
                if st.checkbox(f"{p['icon']} {p['name']}", value=True, key=f"sns_plat_{p['id']}"):
                    selected_platforms.append(p["id"])

        if sns_mode == "📰 개별 기사":
            # ── 카테고리 필터 ──
            st.markdown("#### 🏷️ 카테고리 선택")
            sns_categories = st.multiselect(
                "게시할 카테고리",
                options=list(CATEGORIES.keys()),
                default=["ai_image_video", "ai_coding", "ai_ontology"],
                format_func=lambda x: CATEGORIES[x],
                key="sns_cat",
            )

            # 해당 카테고리 기사 필터
            sns_articles = [a for a in articles if a.get("category") in sns_categories]
            sns_articles.sort(key=lambda x: x.get("importance", 0), reverse=True)

            if not sns_articles:
                st.info("선택한 카테고리에 기사가 없습니다. 다른 카테고리를 선택하거나 뉴스를 먼저 수집하세요.")
            else:
                st.caption(f"📰 {len(sns_articles)}개 기사 발견")

                # 기사 선택
                max_posts = st.slider("게시할 기사 수", 1, min(10, len(sns_articles)), min(3, len(sns_articles)), key="sns_max")

                # 미리보기
                st.markdown("#### 👀 미리보기")
                preview_articles = sns_articles[:max_posts]
                for i, a in enumerate(preview_articles):
                    cat_name = CATEGORIES.get(a.get("category", ""), "기타")
                    sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment", ""), "")
                    stars = "⭐" * a.get("importance", 0)
                    with st.container(border=True):
                        st.markdown(f"{stars} {sentiment_emoji} **[{cat_name}]** {a['title']}")
                        tags = a.get("tags", [])[:3]
                        if tags:
                            st.caption(" ".join([f"#{t}" for t in tags]))

                # 게시 버튼
                st.divider()
                if st.button(f"📢 {len(preview_articles)}개 기사 → {len(selected_platforms)}개 플랫폼 게시", use_container_width=True, key="sns_post", type="primary"):
                    if not selected_platforms:
                        st.error("플랫폼을 선택하세요.")
                    else:
                        progress = st.progress(0, text="카드 뉴스 생성 중...")
                        total = len(preview_articles)
                        all_results = []

                        for i, a in enumerate(preview_articles):
                            progress.progress((i + 1) / total, text=f"📢 게시 중... ({i + 1}/{total})")

                            # 카드 이미지 생성
                            card_path = generate_single_card(a)

                            # 선택한 플랫폼에 업로드
                            results = post_article(a, selected_platforms, card_path)
                            all_results.extend(results)

                        progress.empty()

                        # 결과 표시
                        success_count = sum(1 for r in all_results if r.get("success"))
                        fail_count = len(all_results) - success_count

                        if success_count > 0:
                            st.success(f"✅ {success_count}건 게시 성공!")
                        if fail_count > 0:
                            st.warning(f"⚠️ {fail_count}건 실패")
                            for r in all_results:
                                if not r.get("success"):
                                    st.caption(f"❌ {r.get('platform', '?')}: {r.get('error', '')}")

        else:  # 브리핑 모드
            st.markdown("#### 📋 오늘의 브리핑 카드 뉴스")
            briefings = safe_read_json(BRIEFINGS_PATH, [])
            today_br = next((b for b in briefings if b.get("date") == today_str()), None)

            if not today_br:
                st.info("오늘의 브리핑이 없습니다. 먼저 브리핑을 생성하세요.")
            else:
                st.caption(f"📅 {today_br.get('date', '')}")

                # 미리보기
                top = today_br.get("top_articles", [])
                for i, item in enumerate(top[:5], 1):
                    if isinstance(item, dict):
                        headline = item.get("headline", item.get("title", ""))
                        st.markdown(f"**#{i}** {headline}")

                st.divider()
                if st.button(f"📢 브리핑 → {len(selected_platforms)}개 플랫폼 게시", use_container_width=True, key="sns_post_br", type="primary"):
                    if not selected_platforms:
                        st.error("플랫폼을 선택하세요.")
                    else:
                        with st.spinner("📸 브리핑 카드 생성 중..."):
                            card_path = generate_briefing_card(today_br)

                        with st.spinner("📢 게시 중..."):
                            results = post_briefing(today_br, selected_platforms, card_path)

                        success_count = sum(1 for r in results if r.get("success"))
                        if success_count > 0:
                            st.success(f"✅ {success_count}개 플랫폼에 게시 완료!")
                        for r in results:
                            if not r.get("success"):
                                st.caption(f"❌ {r.get('platform', '?')}: {r.get('error', '')}")

        # ── 카드 이미지 미리보기 (생성만) ──
        st.divider()
        st.markdown("#### 🖼️ 카드 이미지 생성 (다운로드용)")
        if st.button("🖼️ 선택 카테고리 카드 생성", use_container_width=True, key="gen_cards_only"):
            with st.spinner("카드 이미지 생성 중..."):
                card_paths = []
                for a in (sns_articles if sns_mode == "📰 개별 기사" else articles)[:5]:
                    path = generate_single_card(a)
                    if path:
                        card_paths.append(path)

            if card_paths:
                st.success(f"✅ {len(card_paths)}개 카드 생성!")
                # 이미지 미리보기
                preview_cols = st.columns(min(len(card_paths), 3))
                for idx, cp in enumerate(card_paths[:3]):
                    with preview_cols[idx]:
                        st.image(cp, use_container_width=True)
                        with open(cp, "rb") as f:
                            st.download_button(
                                f"📥 다운로드",
                                data=f.read(),
                                file_name=os.path.basename(cp),
                                mime="image/png",
                                key=f"dl_card_{idx}",
                                use_container_width=True,
                            )

# ═══════════════════════════════════════════════
# 탭 8: 타임라인
# ═══════════════════════════════════════════════
with tab_timeline:
    st.markdown("### ⏰ 뉴스 타임라인")

    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    yesterday_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    period_config = {
        "오늘": {"color": "timeline-dot-today", "icon": "🔵"},
        "어제": {"color": "timeline-dot-yesterday", "icon": "🟢"},
        "이번 주": {"color": "timeline-dot-week", "icon": "🟠"},
        "이전": {"color": "timeline-dot-old", "icon": "⚪"},
    }

    groups = {"오늘": [], "어제": [], "이번 주": [], "이전": []}
    for a in articles:
        pub = a.get("published_at", "")[:10]
        if pub == today_date:
            groups["오늘"].append(a)
        elif pub == yesterday_date:
            groups["어제"].append(a)
        elif pub >= (now - timedelta(days=7)).strftime("%Y-%m-%d"):
            groups["이번 주"].append(a)
        else:
            groups["이전"].append(a)

    if not any(groups.values()):
        st.markdown("")
        st.markdown("타임라인에 표시할 뉴스가 없습니다.")
        st.caption("먼저 뉴스를 수집하고 AI 처리를 실행하세요.")
    else:
        for period, items in groups.items():
            if items:
                cfg = period_config[period]
                st.markdown(f"#### {cfg['icon']} {period} ({len(items)}개)")
                for a in items:
                    sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment"), "")
                    importance = "⭐" * a.get("importance", 0)
                    time_str = a.get("published_at", "")[:16]
                    with st.container(border=True):
                        tc1, tc2 = st.columns([5, 1])
                        with tc1:
                            st.markdown(f"{sentiment_emoji} [{a['title']}]({a['url']})")
                            tags = a.get("tags", [])
                            if tags:
                                st.caption(" ".join([f"`{t}`" for t in tags[:3]]))
                        with tc2:
                            st.caption(f"{importance}")
                            st.caption(time_str[-5:] if len(time_str) > 10 else "")
                st.markdown("")

# ═══════════════════════════════════════════════
# 탭 7: 북마크
# ═══════════════════════════════════════════════
with tab_bookmarks:
    st.markdown("### ⭐ 북마크")
    bookmarks = safe_read_json(BOOKMARKS_PATH, [])

    if not bookmarks:
        st.markdown("")
        st.markdown("북마크한 기사가 없습니다.")
        st.caption("뉴스 탭에서 ☆ 버튼을 클릭하면 여기에 저장됩니다.")
    else:
        all_arts = load_articles()
        arts_map = {a["id"]: a for a in all_arts}
        st.caption(f"📌 {len(bookmarks)}개 북마크")

        for bm in reversed(bookmarks):
            a = arts_map.get(bm["article_id"])
            if not a:
                continue

            sentiment = a.get("sentiment", "neutral")
            with st.container(border=True):
                st.markdown(render_sentiment_bar(sentiment), unsafe_allow_html=True)
                col_bm_main, col_bm_action = st.columns([5, 1])

                with col_bm_main:
                    importance = "⭐" * a.get("importance", 0)
                    sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(sentiment, "")
                    category = a.get("category", "ai_other")
                    st.markdown(f"{importance} {sentiment_emoji} [{a['title']}]({a['url']})")
                    st.markdown(render_cat_pill(category), unsafe_allow_html=True)

                    summary = a.get("summary_text", "")
                    if summary:
                        st.caption(summary[:150])

                    memo = st.text_input(
                        "메모", value=bm.get("memo", ""), key=f"memo_{bm['article_id']}",
                        placeholder="💬 메모를 입력하세요...", label_visibility="collapsed",
                    )
                    if memo != bm.get("memo", ""):
                        for b in bookmarks:
                            if b["article_id"] == bm["article_id"]:
                                b["memo"] = memo
                                break
                        safe_write_json(BOOKMARKS_PATH, bookmarks)

                with col_bm_action:
                    st.caption(bm.get("created_at", "")[:10])
                    if st.button("🗑️", key=f"del_bm_{bm['article_id']}", help="삭제"):
                        bookmarks = [b for b in bookmarks if b["article_id"] != bm["article_id"]]
                        safe_write_json(BOOKMARKS_PATH, bookmarks)
                        st.rerun()

# ═══════════════════════════════════════════════
# 탭 8: 소스 관리
# ═══════════════════════════════════════════════
with tab_sources:
    st.markdown("### 📡 뉴스 소스")
    sources = load_sources()

    active_count = len([s for s in sources if s.get("is_active")])
    st.caption(f"🟢 {active_count}개 활성 / 총 {len(sources)}개")

    for s in sources:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                status = "🟢" if s.get("is_active") else "🔴"
                preset = " `프리셋`" if s.get("is_preset") else ""
                st.markdown(f"{status} **{s['name']}**{preset}")
            with col2:
                lang_flag = "🇺🇸" if s.get("lang") == "en" else "🇰🇷"
                st.caption(f"{lang_flag} {s.get('lang', 'en')}")
            with col3:
                last = s.get("last_crawled_at", "")
                st.caption(last[:16] if last else "미수집")
            with col4:
                st.caption(s.get("type", "rss").upper())
