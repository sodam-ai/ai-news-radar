"""유사 기사 묶기."""
from difflib import SequenceMatcher

from db.database import get_articles, update_article_fields
from utils.helpers import generate_id, log

SIMILARITY_THRESHOLD = 0.6


def _title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate() -> int:
    articles = get_articles(limit=5000)
    processed = [a for a in articles if a.get("ai_processed") and not a.get("cluster_id")]

    if len(processed) < 2:
        return 0

    clusters_found = 0
    for index, article in enumerate(processed):
        if article.get("cluster_id"):
            continue

        cluster_id = generate_id("clst")
        group = [article]

        for compare_index in range(index + 1, len(processed)):
            candidate = processed[compare_index]
            if candidate.get("cluster_id"):
                continue
            if _title_similarity(article["title"], candidate["title"]) >= SIMILARITY_THRESHOLD:
                group.append(candidate)

        if len(group) <= 1:
            continue

        group.sort(key=lambda item: item.get("importance", 0), reverse=True)
        primary = group[0]
        primary["cluster_id"] = cluster_id
        primary["is_primary"] = True
        primary["related_articles"] = [
            {"url": item["url"], "title": item["title"], "source_id": item["source_id"]}
            for item in group[1:]
        ]

        for item in group[1:]:
            item["cluster_id"] = cluster_id
            item["is_primary"] = False

        clusters_found += 1

    if clusters_found > 0:
        for article in processed:
            if article.get("cluster_id"):
                update_article_fields(article["id"], {
                    "cluster_id": article["cluster_id"],
                    "is_primary": article["is_primary"],
                    "related_articles": article["related_articles"],
                })

    log(f"[dedup:done] clusters={clusters_found}")
    return clusters_found
