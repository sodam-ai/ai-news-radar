"""
db/database.py — AI News Radar SQLite 데이터 계층
보안: 모든 쿼리 파라미터화, foreign_keys ON, WAL 모드
"""
import json
import sqlite3
import threading
from pathlib import Path

from config import DB_PATH

# ── 스레드 로컬 커넥션 (Streamlit 멀티스레드 대응) ──────────────────────────
_local = threading.local()


def get_connection() -> sqlite3.Connection:
    """스레드당 하나의 커넥션 반환 (WAL + FK 활성화)"""
    if not hasattr(_local, "conn") or _local.conn is None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA cache_size = -8000")
        conn.execute("PRAGMA synchronous = NORMAL")
        _local.conn = conn
    return _local.conn


# ── DB 초기화 (앱 시작 시 1회 호출) ─────────────────────────────────────────
DDL = """
CREATE TABLE IF NOT EXISTS articles (
    id              TEXT PRIMARY KEY,
    source_id       TEXT DEFAULT '',
    title           TEXT NOT NULL DEFAULT '',
    url             TEXT UNIQUE NOT NULL,
    content         TEXT DEFAULT '',
    category        TEXT DEFAULT '',
    importance      INTEGER DEFAULT 0,
    sentiment       TEXT DEFAULT '',
    sentiment_reason TEXT DEFAULT '',
    tags            TEXT DEFAULT '[]',
    image_urls      TEXT DEFAULT '[]',
    image_analysis  TEXT DEFAULT '',
    cluster_id      TEXT DEFAULT '',
    is_primary      INTEGER DEFAULT 1,
    related_articles TEXT DEFAULT '[]',
    published_at    TEXT DEFAULT '',
    crawled_at      TEXT NOT NULL DEFAULT '',
    is_read         INTEGER DEFAULT 0,
    ai_processed    INTEGER DEFAULT 0,
    summary_text    TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS briefings (
    id              TEXT PRIMARY KEY,
    date            TEXT UNIQUE NOT NULL,
    summary         TEXT DEFAULT '',
    top_articles    TEXT DEFAULT '[]',
    focus_briefings TEXT DEFAULT '{}',
    created_at      TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS watchlist (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword     TEXT UNIQUE NOT NULL,
    is_active   INTEGER DEFAULT 1,
    created_at  TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS bookmarks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT NOT NULL,
    memo        TEXT DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sources (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL DEFAULT '',
    url             TEXT UNIQUE NOT NULL,
    type            TEXT DEFAULT 'rss',
    is_preset       INTEGER DEFAULT 0,
    crawl_interval  INTEGER DEFAULT 60,
    is_active       INTEGER DEFAULT 1,
    lang            TEXT DEFAULT 'en',
    last_crawled_at TEXT,
    created_at      TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS alert_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS weekly_reports (
    id          TEXT PRIMARY KEY,
    week        TEXT UNIQUE NOT NULL,
    period      TEXT DEFAULT '',
    title       TEXT DEFAULT '',
    summary     TEXT DEFAULT '',
    key_themes  TEXT DEFAULT '[]',
    top_stories TEXT DEFAULT '[]',
    created_at  TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_articles_ai_processed ON articles(ai_processed);
CREATE INDEX IF NOT EXISTS idx_articles_is_primary   ON articles(is_primary);
CREATE INDEX IF NOT EXISTS idx_articles_category     ON articles(category);
CREATE INDEX IF NOT EXISTS idx_articles_importance   ON articles(importance DESC);
CREATE INDEX IF NOT EXISTS idx_articles_crawled_at   ON articles(crawled_at DESC);
CREATE INDEX IF NOT EXISTS idx_briefings_date        ON briefings(date DESC);
CREATE INDEX IF NOT EXISTS idx_alert_log_article     ON alert_log(article_id);

CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(
    title,
    summary_text,
    tags,
    content=articles,
    content_rowid=rowid
);

CREATE TRIGGER IF NOT EXISTS articles_fts_insert AFTER INSERT ON articles BEGIN
    INSERT INTO articles_fts(rowid, title, summary_text, tags)
    VALUES (new.rowid, new.title, new.summary_text, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS articles_fts_update AFTER UPDATE ON articles BEGIN
    UPDATE articles_fts
    SET title=new.title, summary_text=new.summary_text, tags=new.tags
    WHERE rowid=old.rowid;
END;

CREATE TRIGGER IF NOT EXISTS articles_fts_delete AFTER DELETE ON articles BEGIN
    DELETE FROM articles_fts WHERE rowid=old.rowid;
END;
"""

_ARTICLE_FIELDS = (
    "id, source_id, title, url, content, category, importance, sentiment, "
    "sentiment_reason, tags, image_urls, image_analysis, cluster_id, "
    "is_primary, related_articles, published_at, crawled_at, is_read, "
    "ai_processed, summary_text"
)


def repair_fts() -> bool:
    """FTS5 인덱스 강제 재구축. 손상 복구 또는 UI 수동 호출용."""
    try:
        conn = get_connection()
        conn.execute("INSERT INTO articles_fts(articles_fts) VALUES('rebuild')")
        conn.commit()
        return True
    except Exception:
        return False


def init_db() -> None:
    conn = get_connection()
    conn.executescript(DDL)
    conn.commit()
    # FTS5 무결성 검사 — 손상 감지 시 자동 재구축
    try:
        conn.execute("INSERT INTO articles_fts(articles_fts) VALUES('integrity-check')")
    except Exception:
        repair_fts()


# ── JSON 직렬화 헬퍼 ─────────────────────────────────────────────────────────
def _j(value) -> str:
    return json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value


def _pj(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return value


def _row_to_article(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["tags"] = _pj(d.get("tags", "[]"))
    d["image_urls"] = _pj(d.get("image_urls", "[]"))
    d["related_articles"] = _pj(d.get("related_articles", "[]"))
    d["is_primary"] = bool(d.get("is_primary", 1))
    d["is_read"] = bool(d.get("is_read", 0))
    d["ai_processed"] = bool(d.get("ai_processed", 0))
    return d


def _row_to_source(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["is_preset"] = bool(d.get("is_preset", 0))
    d["is_active"] = bool(d.get("is_active", 1))
    return d


def _row_to_briefing(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["top_articles"] = _pj(d.get("top_articles", "[]"))
    d["focus_briefings"] = _pj(d.get("focus_briefings", "{}"))
    return d


def _row_to_watchlist(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["is_active"] = bool(d.get("is_active", 1))
    return d


# ── ARTICLES ─────────────────────────────────────────────────────────────────
def get_articles(limit: int = 5000) -> list[dict]:
    """전체 기사 반환 (최신순, 최대 limit)"""
    limit = min(limit, 5000)
    conn = get_connection()
    rows = conn.execute(
        f"SELECT {_ARTICLE_FIELDS} FROM articles ORDER BY crawled_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [_row_to_article(r) for r in rows]


def get_primary_articles(limit: int = 2000) -> list[dict]:
    """is_primary=1 AND ai_processed=1 기사 반환"""
    limit = min(limit, 2000)
    conn = get_connection()
    rows = conn.execute(
        f"SELECT {_ARTICLE_FIELDS} FROM articles "
        "WHERE is_primary=1 AND ai_processed=1 "
        "ORDER BY crawled_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [_row_to_article(r) for r in rows]


def get_unprocessed_articles(limit: int = 200) -> list[dict]:
    """AI 미처리 기사 반환"""
    conn = get_connection()
    rows = conn.execute(
        f"SELECT {_ARTICLE_FIELDS} FROM articles "
        "WHERE ai_processed=0 ORDER BY crawled_at ASC LIMIT ?",
        (min(limit, 200),),
    ).fetchall()
    return [_row_to_article(r) for r in rows]


def get_article_by_id(article_id: str) -> dict | None:
    """ID로 단일 기사 조회"""
    if not article_id or len(article_id) > 50:
        return None
    conn = get_connection()
    row = conn.execute(
        f"SELECT {_ARTICLE_FIELDS} FROM articles WHERE id=?",
        (article_id,),
    ).fetchone()
    return _row_to_article(row) if row else None


def search_articles(query: str, limit: int = 50) -> list[dict]:
    """FTS5 전문 검색 (보안: 길이 제한 + 파라미터화)"""
    query = query.strip()[:200]
    if not query:
        return []
    limit = min(limit, 200)
    conn = get_connection()
    try:
        rows = conn.execute(
            f"""
            SELECT a.{(', a.').join(_ARTICLE_FIELDS.split(', '))}
            FROM articles a
            JOIN articles_fts f ON a.rowid = f.rowid
            WHERE articles_fts MATCH ? AND a.ai_processed=1
            ORDER BY rank
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()
        return [_row_to_article(r) for r in rows]
    except sqlite3.OperationalError:
        # FTS 쿼리 오류 시 LIKE fallback (와일드카드 이스케이프)
        safe_q = f"%{query.replace('%', '').replace('_', '')}%"
        rows = conn.execute(
            f"SELECT {_ARTICLE_FIELDS} FROM articles "
            "WHERE (title LIKE ? OR summary_text LIKE ?) AND ai_processed=1 "
            "ORDER BY crawled_at DESC LIMIT ?",
            (safe_q, safe_q, limit),
        ).fetchall()
        return [_row_to_article(r) for r in rows]


def upsert_article(article: dict) -> None:
    """기사 삽입 또는 URL 충돌 시 업데이트"""
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO articles
            (id, source_id, title, url, content, category, importance,
             sentiment, sentiment_reason, tags, image_urls, image_analysis,
             cluster_id, is_primary, related_articles, published_at,
             crawled_at, is_read, ai_processed, summary_text)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(url) DO UPDATE SET
            title            = excluded.title,
            content          = excluded.content,
            category         = CASE WHEN excluded.category != '' THEN excluded.category ELSE category END,
            importance       = CASE WHEN excluded.importance > 0  THEN excluded.importance ELSE importance END,
            sentiment        = CASE WHEN excluded.sentiment != '' THEN excluded.sentiment ELSE sentiment END,
            sentiment_reason = CASE WHEN excluded.sentiment_reason != '' THEN excluded.sentiment_reason ELSE sentiment_reason END,
            tags             = CASE WHEN excluded.tags != '[]' THEN excluded.tags ELSE tags END,
            image_urls       = excluded.image_urls,
            image_analysis   = CASE WHEN excluded.image_analysis != '' THEN excluded.image_analysis ELSE image_analysis END,
            summary_text     = CASE WHEN excluded.summary_text != '' THEN excluded.summary_text ELSE summary_text END,
            ai_processed     = CASE WHEN excluded.ai_processed=1 THEN 1 ELSE ai_processed END
        """,
        (
            article.get("id", ""),
            article.get("source_id", ""),
            article.get("title", ""),
            article.get("url", ""),
            article.get("content", "")[:5000],
            article.get("category", ""),
            article.get("importance", 0),
            article.get("sentiment", ""),
            article.get("sentiment_reason", ""),
            _j(article.get("tags", [])),
            _j(article.get("image_urls", [])),
            article.get("image_analysis", ""),
            article.get("cluster_id", ""),
            1 if article.get("is_primary", True) else 0,
            _j(article.get("related_articles", [])),
            article.get("published_at", ""),
            article.get("crawled_at", ""),
            1 if article.get("is_read", False) else 0,
            1 if article.get("ai_processed", False) else 0,
            article.get("summary_text", ""),
        ),
    )
    conn.commit()


def upsert_articles(articles: list[dict]) -> int:
    """여러 기사 일괄 삽입 (트랜잭션 1회)"""
    if not articles:
        return 0
    conn = get_connection()
    count = 0
    with conn:
        for article in articles:
            conn.execute(
                """
                INSERT INTO articles
                    (id, source_id, title, url, content, category, importance,
                     sentiment, sentiment_reason, tags, image_urls, image_analysis,
                     cluster_id, is_primary, related_articles, published_at,
                     crawled_at, is_read, ai_processed, summary_text)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(url) DO NOTHING
                """,
                (
                    article.get("id", ""),
                    article.get("source_id", ""),
                    article.get("title", ""),
                    article.get("url", ""),
                    article.get("content", "")[:5000],
                    article.get("category", ""),
                    article.get("importance", 0),
                    article.get("sentiment", ""),
                    article.get("sentiment_reason", ""),
                    _j(article.get("tags", [])),
                    _j(article.get("image_urls", [])),
                    article.get("image_analysis", ""),
                    article.get("cluster_id", ""),
                    1 if article.get("is_primary", True) else 0,
                    _j(article.get("related_articles", [])),
                    article.get("published_at", ""),
                    article.get("crawled_at", ""),
                    1 if article.get("is_read", False) else 0,
                    1 if article.get("ai_processed", False) else 0,
                    article.get("summary_text", ""),
                ),
            )
            count += conn.execute("SELECT changes()").fetchone()[0]
    return count


def update_article_fields(article_id: str, fields: dict) -> None:
    """특정 필드만 업데이트 (화이트리스트 검증 + 파라미터화)"""
    ALLOWED = {
        "category", "importance", "sentiment", "sentiment_reason",
        "tags", "image_analysis", "summary_text", "ai_processed",
        "is_read", "is_primary", "cluster_id", "related_articles",
    }
    safe = {k: v for k, v in fields.items() if k in ALLOWED}
    if not safe or not article_id or len(article_id) > 50:
        return
    for k in ("tags", "related_articles"):
        if k in safe and not isinstance(safe[k], str):
            safe[k] = _j(safe[k])
    for k in ("ai_processed", "is_read", "is_primary"):
        if k in safe:
            safe[k] = 1 if safe[k] else 0
    set_clause = ", ".join(f"{k}=?" for k in safe)
    values = list(safe.values()) + [article_id]
    conn = get_connection()
    conn.execute(f"UPDATE articles SET {set_clause} WHERE id=?", values)
    conn.commit()


def get_article_count() -> int:
    conn = get_connection()
    return conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]


def get_processed_count() -> int:
    conn = get_connection()
    return conn.execute("SELECT COUNT(*) FROM articles WHERE ai_processed=1").fetchone()[0]


# ── SOURCES ──────────────────────────────────────────────────────────────────
def get_sources() -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, url, type, is_preset, crawl_interval, "
        "is_active, lang, last_crawled_at, created_at FROM sources ORDER BY created_at"
    ).fetchall()
    return [_row_to_source(r) for r in rows]


def upsert_source(source: dict) -> None:
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO sources
            (id, name, url, type, is_preset, crawl_interval, is_active, lang, last_crawled_at, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(url) DO UPDATE SET
            name            = excluded.name,
            is_active       = excluded.is_active,
            crawl_interval  = excluded.crawl_interval,
            last_crawled_at = excluded.last_crawled_at
        """,
        (
            source.get("id", ""),
            source.get("name", ""),
            source.get("url", ""),
            source.get("type", "rss"),
            1 if source.get("is_preset", False) else 0,
            source.get("crawl_interval", 60),
            1 if source.get("is_active", True) else 0,
            source.get("lang", "en"),
            source.get("last_crawled_at"),
            source.get("created_at", ""),
        ),
    )
    conn.commit()


def update_source_crawled(source_id: str, crawled_at: str) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE sources SET last_crawled_at=? WHERE id=?",
        (crawled_at, source_id),
    )
    conn.commit()


# ── BRIEFINGS ────────────────────────────────────────────────────────────────
def get_briefings(limit: int = 30) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, date, summary, top_articles, focus_briefings, created_at "
        "FROM briefings ORDER BY date DESC LIMIT ?",
        (min(limit, 30),),
    ).fetchall()
    return [_row_to_briefing(r) for r in rows]


def upsert_briefing(briefing: dict) -> None:
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO briefings (id, date, summary, top_articles, focus_briefings, created_at)
        VALUES (?,?,?,?,?,?)
        ON CONFLICT(date) DO UPDATE SET
            summary         = excluded.summary,
            top_articles    = excluded.top_articles,
            focus_briefings = excluded.focus_briefings,
            created_at      = excluded.created_at
        """,
        (
            briefing.get("id", ""),
            briefing.get("date", ""),
            briefing.get("summary", ""),
            _j(briefing.get("top_articles", [])),
            _j(briefing.get("focus_briefings", {})),
            briefing.get("created_at", ""),
        ),
    )
    conn.commit()


# ── WATCHLIST ─────────────────────────────────────────────────────────────────
def get_watchlist() -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, keyword, is_active, created_at FROM watchlist ORDER BY created_at"
    ).fetchall()
    return [_row_to_watchlist(r) for r in rows]


def add_watchlist_keyword(keyword: str, created_at: str) -> bool:
    """키워드 추가. 중복 시 False 반환."""
    keyword = keyword.strip()[:100]
    if not keyword:
        return False
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO watchlist (keyword, is_active, created_at) VALUES (?,1,?)",
            (keyword, created_at),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_active_keywords() -> list[str]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT keyword FROM watchlist WHERE is_active=1"
    ).fetchall()
    return [r["keyword"].lower() for r in rows]


def set_watchlist_active(keyword: str, is_active: bool) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE watchlist SET is_active=? WHERE keyword=?",
        (1 if is_active else 0, keyword),
    )
    conn.commit()


# ── BOOKMARKS ─────────────────────────────────────────────────────────────────
def get_bookmarks() -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, article_id, memo, created_at FROM bookmarks ORDER BY created_at DESC"
    ).fetchall()
    return [dict(r) for r in rows]


def add_bookmark(article_id: str, memo: str, created_at: str) -> bool:
    """북마크 추가. article_id 중복 시 False."""
    if not article_id or len(article_id) > 50:
        return False
    memo = (memo or "")[:500]
    conn = get_connection()
    existing = conn.execute(
        "SELECT id FROM bookmarks WHERE article_id=?", (article_id,)
    ).fetchone()
    if existing:
        return False
    conn.execute(
        "INSERT INTO bookmarks (article_id, memo, created_at) VALUES (?,?,?)",
        (article_id, memo, created_at),
    )
    conn.commit()
    return True


def remove_bookmark(article_id: str) -> None:
    if not article_id or len(article_id) > 50:
        return
    conn = get_connection()
    conn.execute("DELETE FROM bookmarks WHERE article_id=?", (article_id,))
    conn.commit()


def update_bookmark_memo(article_id: str, memo: str) -> None:
    if not article_id or len(article_id) > 50:
        return
    memo = (memo or "")[:500]
    conn = get_connection()
    conn.execute(
        "UPDATE bookmarks SET memo=? WHERE article_id=?",
        (memo, article_id),
    )
    conn.commit()


def get_bookmark_ids() -> set[str]:
    conn = get_connection()
    rows = conn.execute("SELECT article_id FROM bookmarks").fetchall()
    return {r["article_id"] for r in rows}


# ── ALERT LOG ─────────────────────────────────────────────────────────────────
def get_alert_log(limit: int = 500) -> list[str]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT article_id FROM alert_log ORDER BY created_at DESC LIMIT ?",
        (min(limit, 500),),
    ).fetchall()
    return [r["article_id"] for r in rows]


def mark_alerted(article_id: str, created_at: str) -> None:
    if not article_id or len(article_id) > 50:
        return
    conn = get_connection()
    already = conn.execute(
        "SELECT id FROM alert_log WHERE article_id=?", (article_id,)
    ).fetchone()
    if not already:
        conn.execute(
            "INSERT INTO alert_log (article_id, created_at) VALUES (?,?)",
            (article_id, created_at),
        )
        conn.execute(
            "DELETE FROM alert_log WHERE id NOT IN "
            "(SELECT id FROM alert_log ORDER BY created_at DESC LIMIT 500)"
        )
        conn.commit()


# ── WEEKLY REPORTS ────────────────────────────────────────────────────────────
def get_weekly_reports(limit: int = 10) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, week, period, title, summary, key_themes, top_stories, created_at "
        "FROM weekly_reports ORDER BY week DESC LIMIT ?",
        (min(limit, 10),),
    ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["key_themes"] = _pj(d.get("key_themes", "[]"))
        d["top_stories"] = _pj(d.get("top_stories", "[]"))
        result.append(d)
    return result


def upsert_weekly_report(report: dict) -> None:
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO weekly_reports
            (id, week, period, title, summary, key_themes, top_stories, created_at)
        VALUES (?,?,?,?,?,?,?,?)
        ON CONFLICT(week) DO UPDATE SET
            summary     = excluded.summary,
            key_themes  = excluded.key_themes,
            top_stories = excluded.top_stories,
            created_at  = excluded.created_at
        """,
        (
            report.get("id", ""),
            report.get("week", ""),
            report.get("period", ""),
            report.get("title", ""),
            report.get("summary", ""),
            _j(report.get("key_themes", [])),
            _j(report.get("top_stories", [])),
            report.get("created_at", ""),
        ),
    )
    conn.commit()
