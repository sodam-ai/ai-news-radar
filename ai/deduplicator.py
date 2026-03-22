"""중복 뉴스 감지 + 병합"""
from difflib import SequenceMatcher

from config import DATA_DIR
from utils.helpers import generate_id, safe_read_json, safe_write_json

ARTICLES_PATH = DATA_DIR / "articles.json"
SIMILARITY_THRESHOLD = 0.6


def _title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate() -> int:
    """제목 유사도 기반 중복 감지. 병합된 그룹 수 반환."""
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and not a.get("cluster_id")]

    if len(processed) < 2:
        return 0

    clusters_found = 0

    for i, a in enumerate(processed):
        if a.get("cluster_id"):
            continue

        cluster_id = generate_id("clst")
        group = [a]

        for j in range(i + 1, len(processed)):
            b = processed[j]
            if b.get("cluster_id"):
                continue
            if _title_similarity(a["title"], b["title"]) >= SIMILARITY_THRESHOLD:
                group.append(b)

        if len(group) > 1:
            # 가장 중요도가 높은 글을 대표로
            group.sort(key=lambda x: x.get("importance", 0), reverse=True)
            primary = group[0]
            primary["cluster_id"] = cluster_id
            primary["is_primary"] = True
            primary["related_articles"] = [
                {"url": g["url"], "title": g["title"], "source_id": g["source_id"]}
                for g in group[1:]
            ]

            for g in group[1:]:
                g["cluster_id"] = cluster_id
                g["is_primary"] = False

            clusters_found += 1

    if clusters_found > 0:
        articles_map = {a["id"]: a for a in articles}
        for p in processed:
            articles_map[p["id"]] = p
        safe_write_json(ARTICLES_PATH, list(articles_map.values()))

    print(f"[중복 제거] {clusters_found}개 그룹 병합")
    return clusters_found
