"""AI News Radar — Streamlit 메인 대시보드"""
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

# ── 페이지 설정 ──
st.set_page_config(
    page_title="AI News Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── LLM 프로바이더 체크 ──
_active_provider = get_active_provider()
if not _active_provider:
    st.warning("⚠️ LLM API 키가 설정되지 않았습니다. `.env` 파일에 API 키를 최소 1개 입력하세요. RSS 수집은 가능하지만 AI 처리는 불가합니다.")

# ── 자동 스케줄러 시작 (세션당 1회) ──
if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

ARTICLES_PATH = DATA_DIR / "articles.json"
SOURCES_PATH = DATA_DIR / "sources.json"
WATCHLIST_PATH = DATA_DIR / "watchlist.json"
BRIEFINGS_PATH = DATA_DIR / "briefings.json"


# ── 데이터 로드 ──
def load_articles():
    return safe_read_json(ARTICLES_PATH, [])


def load_primary_articles():
    """중복 제거된 대표 글만 반환"""
    articles = load_articles()
    return [a for a in articles if a.get("is_primary", True) and a.get("ai_processed")]


# ── 다크모드 CSS ──
LIGHT_CSS = """
<style>
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"],
    [data-testid="stHeader"], .main {
        background-color: #FFFFFF !important;
        color: #1E1E1E !important;
    }
    [data-testid="stSidebar"] {
        background-color: #F0F2F6 !important;
    }
    [data-testid="stSidebar"] * {
        color: #1E1E1E !important;
    }
    .main * { color: #1E1E1E !important; }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 { color: #1E1E1E !important; }
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stTextInput label, .stCheckbox label { color: #1E1E1E !important; }
    div[data-testid="stExpander"] { border-color: #D0D0D0 !important; }
    div[data-baseweb="select"] { background-color: #FFFFFF !important; }
</style>
"""

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if not st.session_state.dark_mode:
    st.markdown(LIGHT_CSS, unsafe_allow_html=True)

# ── 사이드바 ──
with st.sidebar:
    st.title("📡 AI News Radar")
    st.caption("AI 뉴스를 자동으로 수집·요약·분류")

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

    # LLM 프로바이더 상태 표시
    if _active_provider:
        provider_info = PROVIDERS[_active_provider]
        st.caption(f"🤖 AI: **{provider_info['name']}**")
        available = get_available_providers()
        if len(available) > 1:
            with st.expander(f"🔌 프로바이더 ({len(available)}개 사용 가능)"):
                for p in available:
                    icon = "✅" if p["id"] == _active_provider else "⚪"
                    multi = "🖼️" if p["multimodal"] else ""
                    st.caption(f"{icon} **{p['name']}** {multi} — {p['free_tier']}")
                st.caption("💡 `.env`의 `LLM_PROVIDER=이름`으로 변경 가능")

    st.divider()

    # 수동 수집 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 수집", use_container_width=True):
            try:
                with st.spinner("RSS 수집 중..."):
                    count = crawl_all()
                st.success(f"{count}개 새 글 수집!")
            except Exception as e:
                st.error("수집 중 오류가 발생했습니다. 인터넷 연결을 확인해주세요.")
                log(f"[수집 오류] {e}")
    with col2:
        if st.button("🤖 AI 처리", use_container_width=True):
            if not _active_provider:
                st.error("LLM API 키를 먼저 설정해주세요. (.env 파일)")
            else:
                try:
                    with st.spinner(f"AI 분석 중 ({PROVIDERS[_active_provider]['name']})..."):
                        processed = process_unprocessed()
                        deduplicate()
                    st.success(f"{processed}개 처리 완료!")
                except Exception as e:
                    st.error("AI 분석 중 오류가 발생했습니다. 나중에 다시 시도해주세요.")
                    log(f"[AI 처리 오류] {e}")

    if st.button("📋 브리핑 생성", use_container_width=True):
        if not _active_provider:
            st.error("LLM API 키를 먼저 설정해주세요. (.env 파일)")
        else:
            try:
                with st.spinner("오늘의 브리핑 생성 중..."):
                    briefing = generate_daily_briefing()
                if briefing:
                    st.success("브리핑 생성 완료!")
                else:
                    st.warning("브리핑 생성에 필요한 기사가 부족합니다.")
            except Exception as e:
                st.error("브리핑 생성 중 오류가 발생했습니다.")
                log(f"[브리핑 오류] {e}")

    st.divider()

    # 필터
    st.subheader("🔍 필터")

    category_filter = st.multiselect(
        "카테고리",
        options=list(CATEGORIES.keys()),
        format_func=lambda x: CATEGORIES[x],
    )

    sentiment_filter = st.multiselect(
        "감성",
        options=list(SENTIMENTS.keys()),
        format_func=lambda x: SENTIMENTS[x],
    )

    importance_filter = st.slider("최소 중요도", 1, 5, 1)

    st.divider()

    # 워치리스트
    st.subheader("👀 키워드 워치리스트")
    watchlist = safe_read_json(WATCHLIST_PATH, [])
    watchlist_keywords = [w["keyword"] for w in watchlist if w.get("is_active")]

    new_keyword = st.text_input("키워드 추가", placeholder="예: Claude, MCP")
    if new_keyword and st.button("추가", key="add_kw"):
        watchlist.append({"keyword": new_keyword, "is_active": True, "created_at": today_str()})
        safe_write_json(WATCHLIST_PATH, watchlist)
        st.rerun()

    if watchlist_keywords:
        st.write(" ".join([f"`{k}`" for k in watchlist_keywords]))

    st.divider()

    # 소스 관리
    with st.expander("📰 소스 관리"):
        sources = load_sources()
        for s in sources:
            s["is_active"] = st.checkbox(s["name"], value=s.get("is_active", True), key=f"src_{s['id']}")
        if st.button("소스 저장"):
            safe_write_json(SOURCES_PATH, sources)
            st.success("저장됨!")

        new_name = st.text_input("새 소스 이름")
        new_url = st.text_input("RSS URL")
        if new_name and new_url and st.button("소스 추가"):
            from utils.helpers import generate_id, now_iso
            sources.append({
                "id": generate_id("src"),
                "name": new_name,
                "url": new_url,
                "type": "rss",
                "is_preset": False,
                "crawl_interval": 60,
                "is_active": True,
                "lang": "en",
                "last_crawled_at": None,
                "created_at": now_iso(),
            })
            safe_write_json(SOURCES_PATH, sources)
            st.success(f"'{new_name}' 추가됨!")
            st.rerun()

    # 통계 (자동 갱신 — 5분마다 데이터 리로드)
    @st.fragment(run_every=300)
    def sidebar_stats():
        all_arts = load_articles()
        processed_arts = [a for a in all_arts if a.get("ai_processed")]
        st.caption(f"총 {len(all_arts)}개 기사 | AI 처리: {len(processed_arts)}개")
        # 마지막 수집 시각
        if all_arts:
            latest = max((a.get("crawled_at", "") for a in all_arts), default="")
            if latest:
                st.caption(f"마지막 수집: {latest[:16]}")

    sidebar_stats()


# ── 실시간 갱신: 새 글 알림 배너 (5분마다 자동 체크) ──
@st.fragment(run_every=300)
def new_articles_banner():
    """새 글이 수집되면 알림 배너 표시"""
    all_arts = load_articles()
    total = len(all_arts)
    if "last_article_count" not in st.session_state:
        st.session_state.last_article_count = total
    elif total > st.session_state.last_article_count:
        new_count = total - st.session_state.last_article_count
        st.toast(f"📡 새 글 {new_count}개가 수집되었습니다!", icon="🆕")
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

# 워치리스트 하이라이트
def is_watchlisted(article):
    text = f"{article.get('title', '')} {' '.join(article.get('tags', []))}".lower()
    return any(k.lower() in text for k in watchlist_keywords)


BOOKMARKS_PATH = DATA_DIR / "bookmarks.json"

# 탭 구성
tab_briefing, tab_list, tab_search, tab_timeline, tab_bookmarks, tab_sources = st.tabs(
    ["📋 브리핑", "📰 뉴스", "🔍 검색", "⏰ 타임라인", "⭐ 북마크", "📡 소스"]
)

# ── 탭 1: 오늘의 브리핑 ──
with tab_briefing:
    briefings = safe_read_json(BRIEFINGS_PATH, [])
    today_briefing = next((b for b in briefings if b.get("date") == today_str()), None)

    if today_briefing:
        st.header(f"📋 오늘의 AI 브리핑 ({today_str()})")

        if today_briefing.get("summary"):
            st.info(today_briefing["summary"])

        top = today_briefing.get("top_articles", [])
        if isinstance(top, list):
            for i, item in enumerate(top, 1):
                if isinstance(item, dict):
                    headline = item.get("headline", item.get("title", ""))
                    why = item.get("why_important", item.get("summary", ""))
                    st.markdown(f"**{i}. {headline}**")
                    if why:
                        st.caption(why)
        # 내보내기 버튼
        st.divider()
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            md_content = export_briefing_markdown()
            st.download_button(
                "📥 Markdown",
                data=md_content,
                file_name=f"ai_briefing_{today_str()}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with exp_col2:
            try:
                pdf_content = export_briefing_pdf()
                st.download_button(
                    "📥 PDF",
                    data=pdf_content,
                    file_name=f"ai_briefing_{today_str()}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.caption(f"PDF 생성 불가: {e}")
    else:
        st.info("아직 오늘의 브리핑이 없습니다. 사이드바에서 '📋 브리핑 생성'을 클릭하세요.")

# ── 탭 2: 뉴스 목록 ──
with tab_list:
    col_header, col_export = st.columns([3, 1])
    with col_header:
        st.header(f"📰 AI 뉴스 ({len(articles)}개)")
    with col_export:
        if articles:
            exp_fmt = st.selectbox("형식", ["Markdown", "PDF"], label_visibility="collapsed", key="export_fmt")
            if exp_fmt == "Markdown":
                md_articles = export_articles_markdown(articles)
                st.download_button(
                    "📥 내보내기",
                    data=md_articles,
                    file_name=f"ai_news_{today_str()}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            else:
                try:
                    pdf_articles = export_articles_pdf(articles)
                    st.download_button(
                        "📥 내보내기",
                        data=pdf_articles,
                        file_name=f"ai_news_{today_str()}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.caption(f"PDF 생성 불가: {e}")

    # 정렬
    sort_option = st.selectbox("정렬", ["중요도 높은 순", "최신순", "긍정 뉴스 먼저"], label_visibility="collapsed")
    if sort_option == "중요도 높은 순":
        articles.sort(key=lambda x: x.get("importance", 0), reverse=True)
    elif sort_option == "최신순":
        articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    elif sort_option == "긍정 뉴스 먼저":
        order = {"positive": 0, "neutral": 1, "negative": 2}
        articles.sort(key=lambda x: order.get(x.get("sentiment", "neutral"), 1))

    for article in articles:
        watched = is_watchlisted(article)
        prefix = "👀 " if watched else ""
        importance = "⭐" * article.get("importance", 0)
        sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(article.get("sentiment"), "")
        category_name = CATEGORIES.get(article.get("category", ""), "")

        # 카드 스타일
        with st.container(border=True):
            col_main, col_meta = st.columns([4, 1])

            with col_main:
                st.markdown(f"### {prefix}[{article['title']}]({article['url']})")

                # 3줄 요약
                summary = article.get("summary_text", "")
                if summary:
                    st.write(summary)

                # 자세히 보기 (expander) + 인앱 리더 뷰
                with st.expander("📖 자세히 보기"):
                    if article.get("content"):
                        st.write(article["content"][:2000])
                    if st.button("📰 원문 가져오기 (리더 뷰)", key=f"reader_{article['id']}"):
                        with st.spinner("원문 로딩 중..."):
                            clean = fetch_clean_content(article["url"])
                        st.markdown(clean[:3000])
                    st.markdown(f"[🔗 원문 바로가기 (새 탭)]({article['url']})")

                # 이미지 분석 결과
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
                    st.caption(f"▶ {len(related)}개 매체 추가 보도")

            with col_meta:
                st.write(f"{importance}")
                st.write(f"{sentiment_emoji} {category_name}")
                pub = article.get("published_at", "")[:10]
                if pub:
                    st.caption(pub)

                # 북마크 버튼
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

                # 읽음 표시
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

# ── 탭 3: 검색 ──
with tab_search:
    st.header("🔍 뉴스 검색")

    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input("검색어", placeholder="키워드를 입력하세요 (예: Claude, GPT, 삼성)", label_visibility="collapsed")
    with search_col2:
        search_category = st.selectbox("카테고리", ["전체"] + list(CATEGORIES.keys()), format_func=lambda x: "전체" if x == "전체" else CATEGORIES[x], key="search_cat")

    search_col3, search_col4 = st.columns(2)
    with search_col3:
        search_sentiment = st.selectbox("감성", ["전체", "positive", "negative", "neutral"], format_func=lambda x: "전체" if x == "전체" else SENTIMENTS.get(x, x), key="search_sent")
    with search_col4:
        show_read = st.selectbox("읽음 상태", ["전체", "안 읽은 글만", "읽은 글만"], key="search_read")

    if search_query or search_category != "전체" or search_sentiment != "전체" or show_read != "전체":
        all_for_search = load_primary_articles()
        results = all_for_search

        # 키워드 검색 (제목 + 요약 + 태그)
        if search_query:
            q = search_query.lower()
            results = [
                a for a in results
                if q in a.get("title", "").lower()
                or q in a.get("summary_text", "").lower()
                or any(q in t.lower() for t in a.get("tags", []))
            ]

        # 카테고리 필터
        if search_category != "전체":
            results = [a for a in results if a.get("category") == search_category]

        # 감성 필터
        if search_sentiment != "전체":
            results = [a for a in results if a.get("sentiment") == search_sentiment]

        # 읽음 상태 필터
        if show_read == "안 읽은 글만":
            results = [a for a in results if not a.get("is_read")]
        elif show_read == "읽은 글만":
            results = [a for a in results if a.get("is_read")]

        st.caption(f"검색 결과: {len(results)}개")

        for a in results[:50]:  # 최대 50개 표시
            sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment"), "")
            importance = "⭐" * a.get("importance", 0)
            read_mark = "✅" if a.get("is_read") else ""
            with st.container(border=True):
                st.markdown(f"{importance} {sentiment_emoji} {read_mark} [{a['title']}]({a['url']})")
                summary = a.get("summary_text", "")
                if summary:
                    st.caption(summary[:150])
                tags = a.get("tags", [])
                if tags:
                    st.caption(" ".join([f"`{t}`" for t in tags]))
    else:
        st.info("검색어를 입력하거나 필터를 선택하세요.")

# ── 탭 4: 타임라인 ──
with tab_timeline:
    st.header("⏰ 타임라인")

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    # 시간대별 그룹핑
    groups = {"오늘": [], "어제": [], "이번 주": [], "이전": []}
    for a in articles:
        pub = a.get("published_at", "")[:10]
        if pub == today:
            groups["오늘"].append(a)
        elif pub == yesterday:
            groups["어제"].append(a)
        elif pub >= (now - timedelta(days=7)).strftime("%Y-%m-%d"):
            groups["이번 주"].append(a)
        else:
            groups["이전"].append(a)

    for period, items in groups.items():
        if items:
            st.subheader(f"{period} ({len(items)}개)")
            for a in items:
                sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment"), "")
                importance = "⭐" * a.get("importance", 0)
                st.markdown(f"- {importance} {sentiment_emoji} [{a['title']}]({a['url']})")

# ── 탭 5: 북마크 ──
with tab_bookmarks:
    st.header("⭐ 북마크")
    bookmarks = safe_read_json(BOOKMARKS_PATH, [])

    if not bookmarks:
        st.info("북마크한 기사가 없습니다. 뉴스 목록에서 ☆ 버튼을 클릭하세요.")
    else:
        all_arts = load_articles()
        arts_map = {a["id"]: a for a in all_arts}
        st.caption(f"총 {len(bookmarks)}개 북마크")

        for bm in reversed(bookmarks):  # 최신 북마크 먼저
            a = arts_map.get(bm["article_id"])
            if not a:
                continue

            with st.container(border=True):
                col_bm_main, col_bm_action = st.columns([5, 1])

                with col_bm_main:
                    importance = "⭐" * a.get("importance", 0)
                    sentiment_emoji = {"positive": "😊", "negative": "😠", "neutral": "😐"}.get(a.get("sentiment"), "")
                    st.markdown(f"{importance} {sentiment_emoji} [{a['title']}]({a['url']})")

                    summary = a.get("summary_text", "")
                    if summary:
                        st.caption(summary[:150])

                    # 메모 입력/편집
                    memo = st.text_input(
                        "메모",
                        value=bm.get("memo", ""),
                        key=f"memo_{bm['article_id']}",
                        placeholder="메모 추가...",
                        label_visibility="collapsed",
                    )
                    if memo != bm.get("memo", ""):
                        for b in bookmarks:
                            if b["article_id"] == bm["article_id"]:
                                b["memo"] = memo
                                break
                        safe_write_json(BOOKMARKS_PATH, bookmarks)

                with col_bm_action:
                    st.caption(bm.get("created_at", "")[:10])
                    if st.button("🗑️", key=f"del_bm_{bm['article_id']}", help="북마크 삭제"):
                        bookmarks = [b for b in bookmarks if b["article_id"] != bm["article_id"]]
                        safe_write_json(BOOKMARKS_PATH, bookmarks)
                        st.rerun()

# ── 탭 6: 소스 관리 ──
with tab_sources:
    st.header("📡 뉴스 소스")
    sources = load_sources()

    for s in sources:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            status = "🟢" if s.get("is_active") else "🔴"
            preset = " (프리셋)" if s.get("is_preset") else ""
            st.write(f"{status} **{s['name']}**{preset}")
        with col2:
            st.caption(s.get("lang", "en"))
        with col3:
            last = s.get("last_crawled_at", "")
            st.caption(last[:16] if last else "미수집")
