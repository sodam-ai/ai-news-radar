"""ChromaDB 벡터 저장소 — 시맨틱 검색

기사 AI 처리 완료 시 자동으로 임베딩 저장.
ai/chat.py에서 자연어 질문으로 관련 기사 시맨틱 검색.
"""
import os

from config import DATA_DIR
from utils.helpers import log

CHROMA_PATH = DATA_DIR / "chroma"


def _get_collection():
    """ChromaDB 컬렉션 반환 (없으면 생성)

    ONNX 로컬 all-MiniLM-L6-v2 모델로 임베딩.
    API 키 불필요, 완전 오프라인 동작.
    """
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    try:
        from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2
        ef = ONNXMiniLM_L6_V2()
    except Exception:
        # onnxruntime 미설치 시 None → chromadb 내장 처리
        ef = None

    try:
        kwargs = {"name": "articles"}
        if ef is not None:
            kwargs["embedding_function"] = ef
        return client.get_or_create_collection(**kwargs)
    except Exception as e:
        log(f"[vector:collection-error] {e}")
        return None


def add_articles(articles: list[dict]) -> int:
    """처리된 기사들을 벡터 DB에 추가. 추가된 수 반환."""
    col = _get_collection()
    if col is None:
        return 0

    try:
        existing_ids = set(col.get(include=[])["ids"])
    except Exception:
        existing_ids = set()

    new = [
        a for a in articles
        if a.get("id") not in existing_ids and a.get("ai_processed")
    ]
    if not new:
        return 0

    docs, ids, metas = [], [], []
    for a in new:
        text = (
            f"{a.get('title', '')} "
            f"{a.get('summary_text', '')[:300]} "
            f"{' '.join(a.get('tags', []))}"
        ).strip()
        if not text:
            continue
        docs.append(text)
        ids.append(a["id"])
        metas.append({
            "title": a.get("title", ""),
            "url": a.get("url", ""),
            "category": a.get("category", ""),
            "importance": int(a.get("importance", 0)),
            "sentiment": a.get("sentiment", ""),
        })

    if not ids:
        return 0

    try:
        col.add(documents=docs, ids=ids, metadatas=metas)
        log(f"[vector:add] {len(ids)}개 추가 (총 {col.count()}개)")
        return len(ids)
    except Exception as e:
        log(f"[vector:add-error] {e}")
        return 0


def search(query: str, n_results: int = 10) -> list[str]:
    """쿼리와 의미론적으로 유사한 기사 ID 목록 반환"""
    col = _get_collection()
    if col is None:
        return []

    try:
        total = col.count()
        if total == 0:
            return []
        results = col.query(
            query_texts=[query],
            n_results=min(n_results, total),
        )
        return results["ids"][0] if results.get("ids") else []
    except Exception as e:
        log(f"[vector:search-error] {e}")
        return []


def get_count() -> int:
    """벡터 DB에 저장된 기사 수"""
    try:
        col = _get_collection()
        return col.count() if col else 0
    except Exception:
        return 0


def sync_existing_articles(articles: list[dict]) -> int:
    """기존 처리된 기사를 벡터 DB에 일괄 동기화 (최초 1회용)"""
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]
    if not processed:
        return 0
    added = add_articles(processed)
    log(f"[vector:sync] 기존 기사 {added}개 동기화 완료")
    return added
