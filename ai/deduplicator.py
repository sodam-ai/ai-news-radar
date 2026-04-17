"""유사 기사 묶기."""
from difflib import SequenceMatcher

from config import DATA_DIR
from utils.helpers import generate_id, log, safe_read_json, safe_update_json

ARTICLES_PATH = DATA_DIR / "articles.json"
SIMILARITY_THRESHOLD = 0.6
DEDUP_FIELDS = ("cluster_id", "is_primary", "related_articles")


def _title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _merge_cluster_updates(current_articles: list[dict], updated_articles: dict[str, dict]) -> list[dict]:
    merged = []
    for article in current_articles:
        updated = updated_articles.get(article.get("id"))
        if not updated or not updated.get("cluster_id"):
            merged.append(article)
            continue

        merged_article = dict(article)
        for field in DEDUP_FIELDS:
            merged_article[field] = updated.get(field, merged_article.get(field))
        merged.append(merged_article)
    return merged


def deduplicate() -> int:
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [article for article in articles if article.get("ai_processed") and not article.get("cluster_id")]

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
        updated_articles = {article["id"]: article for article in processed if article.get("cluster_id")}
        safe_update_json(
            ARTICLES_PATH,
            lambda current: _merge_cluster_updates(current, updated_articles),
            default=articles,
        )

    log(f"[dedup:done] clusters={clusters_found}")
    return clusters_found
