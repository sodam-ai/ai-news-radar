"""AI 팩트체크 — 뉴스 교차 검증 (중복 병합 데이터 기반)

기존 deduplicator의 related_articles 필드를 활용하여
같은 뉴스를 보도한 매체 수로 신뢰도를 판단합니다.
"""


def get_factcheck_badge(article: dict) -> dict:
    """기사의 팩트체크 배지 정보를 반환.

    Returns:
        {
            "level": "high" | "medium" | "low" | "single",
            "label": 표시 텍스트,
            "icon": 아이콘,
            "sources_count": 보도 매체 수,
            "sources": 매체 목록,
        }
    """
    related = article.get("related_articles", [])
    count = len(related) + 1  # 본인 포함

    if count >= 4:
        return {
            "level": "high",
            "label": f"✅ {count}개 매체 확인",
            "icon": "✅",
            "sources_count": count,
            "sources": related,
        }
    elif count >= 3:
        return {
            "level": "medium",
            "label": f"✅ {count}개 매체 확인",
            "icon": "✅",
            "sources_count": count,
            "sources": related,
        }
    elif count == 2:
        return {
            "level": "low",
            "label": f"🔍 {count}개 매체 보도",
            "icon": "🔍",
            "sources_count": count,
            "sources": related,
        }
    else:
        return {
            "level": "single",
            "label": "⚠️ 단독 보도",
            "icon": "⚠️",
            "sources_count": 1,
            "sources": [],
        }


def get_factcheck_summary(articles: list[dict]) -> dict:
    """전체 기사의 팩트체크 요약 통계.

    Returns:
        {"high": N, "medium": N, "low": N, "single": N, "total": N}
    """
    stats = {"high": 0, "medium": 0, "low": 0, "single": 0, "total": 0}
    for a in articles:
        badge = get_factcheck_badge(a)
        stats[badge["level"]] += 1
        stats["total"] += 1
    return stats
