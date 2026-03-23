"""키워드 트렌드 분석 — 도구/키워드별 시계열 언급량 분석

56개 소스에서 수집한 기사의 날짜별 언급 빈도를 계산하여
Plotly 시계열 차트 데이터를 생성합니다.
"""
from datetime import datetime, timedelta
from collections import defaultdict

from config import DATA_DIR
from ai.competitor import COMPETITOR_GROUPS
from utils.helpers import safe_read_json

ARTICLES_PATH = DATA_DIR / "articles.json"


def _match_keyword(article: dict, keywords: list[str]) -> bool:
    """기사가 키워드 목록 중 하나라도 포함하는지 확인"""
    text = f"{article.get('title', '')} {article.get('summary_text', '')} {' '.join(article.get('tags', []))}".lower()
    return any(kw.lower() in text for kw in keywords)


def get_trend_data(group_id: str, days: int = 30) -> dict:
    """특정 경쟁 그룹의 일별 트렌드 데이터 반환

    Returns:
        {
            "dates": ["2026-03-01", "2026-03-02", ...],
            "tools": [
                {"name": "Midjourney", "color": "#5865F2", "counts": [3, 1, 0, ...]},
                ...
            ]
        }
    """
    group = COMPETITOR_GROUPS.get(group_id)
    if not group:
        return {"dates": [], "tools": []}

    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    # 날짜 범위 생성
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days - 1)
    date_range = []
    current = start_date
    while current <= end_date:
        date_range.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    # 도구별 일별 카운트
    tool_data = []
    for tool in group["tools"]:
        daily_counts = defaultdict(int)
        for a in processed:
            pub = a.get("published_at", a.get("crawled_at", ""))[:10]
            if pub and start_date.strftime("%Y-%m-%d") <= pub <= end_date.strftime("%Y-%m-%d"):
                if _match_keyword(a, tool["keywords"]):
                    daily_counts[pub] += 1

        counts = [daily_counts.get(d, 0) for d in date_range]
        total = sum(counts)
        if total > 0:  # 언급이 있는 도구만 포함
            tool_data.append({
                "name": tool["name"],
                "color": tool["color"],
                "counts": counts,
                "total": total,
            })

    # 총 언급량 순 정렬
    tool_data.sort(key=lambda x: x["total"], reverse=True)

    return {"dates": date_range, "tools": tool_data}


def get_keyword_trend(keyword: str, days: int = 30) -> dict:
    """커스텀 키워드의 일별 트렌드 데이터

    Returns:
        {"dates": [...], "counts": [...], "total": N}
    """
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days - 1)
    date_range = []
    current = start_date
    while current <= end_date:
        date_range.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    daily_counts = defaultdict(int)
    kw_lower = keyword.lower()
    for a in processed:
        pub = a.get("published_at", a.get("crawled_at", ""))[:10]
        if pub and start_date.strftime("%Y-%m-%d") <= pub <= end_date.strftime("%Y-%m-%d"):
            text = f"{a.get('title', '')} {a.get('summary_text', '')} {' '.join(a.get('tags', []))}".lower()
            if kw_lower in text:
                daily_counts[pub] += 1

    counts = [daily_counts.get(d, 0) for d in date_range]
    return {"dates": date_range, "counts": counts, "total": sum(counts)}


def get_hot_keywords(top_n: int = 10, days: int = 7) -> list[dict]:
    """최근 N일간 급상승 키워드 (태그 기반)

    Returns:
        [{"keyword": "...", "count": N, "change_pct": float}, ...]
    """
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    end_date = datetime.now()
    this_week_start = (end_date - timedelta(days=days)).strftime("%Y-%m-%d")
    last_week_start = (end_date - timedelta(days=days * 2)).strftime("%Y-%m-%d")
    last_week_end = this_week_start

    # 이번 주 태그 카운트
    this_week_tags = defaultdict(int)
    last_week_tags = defaultdict(int)

    for a in processed:
        pub = a.get("published_at", a.get("crawled_at", ""))[:10]
        tags = a.get("tags", [])
        for tag in tags:
            tag_lower = tag.lower().strip()
            if not tag_lower:
                continue
            if pub >= this_week_start:
                this_week_tags[tag_lower] += 1
            elif pub >= last_week_start:
                last_week_tags[tag_lower] += 1

    # 변화율 계산
    hot = []
    for tag, count in this_week_tags.items():
        prev = last_week_tags.get(tag, 0)
        if prev > 0:
            change = round((count - prev) / prev * 100)
        elif count > 0:
            change = 999  # 신규 등장
        else:
            change = 0
        hot.append({"keyword": tag, "count": count, "prev_count": prev, "change_pct": change})

    # 언급량 + 변화율 종합 정렬
    hot.sort(key=lambda x: (x["count"] * 2 + max(x["change_pct"], 0)), reverse=True)
    return hot[:top_n]
