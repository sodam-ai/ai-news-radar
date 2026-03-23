"""AI 용어 사전 — 뉴스 속 AI 전문 용어 자동 추출 + 쉬운 설명"""
import json

from config import DATA_DIR
from ai.model_router import call_gemini
from utils.helpers import safe_read_json, safe_write_json, now_iso, log

ARTICLES_PATH = DATA_DIR / "articles.json"
GLOSSARY_PATH = DATA_DIR / "glossary.json"

GLOSSARY_SYSTEM = """너는 AI 기술 용어 사전 전문가야.
뉴스 기사의 태그와 내용에서 AI 전문 용어를 추출하고,
완전 초보자(비개발자, 비전문가)가 이해할 수 있게 쉽게 설명해.

각 용어에 대해 다음 JSON 배열을 반환해:
[
  {
    "term": "용어 (영문)",
    "term_ko": "용어 (한국어, 없으면 영문 그대로)",
    "category": "model | technique | concept | product | company | other",
    "difficulty": 1~3 (1=쉬움, 2=보통, 3=어려움),
    "short_desc": "한 줄 설명 (20자 이내)",
    "full_desc": "쉬운 설명 (비유 포함, 2~3문장)",
    "example": "실생활 예시 한 줄"
  }
]

규칙:
- 이미 알려진 용어도 초보자 관점에서 설명
- 비유를 적극 활용 (예: "LLM은 엄청나게 많은 책을 읽은 AI 두뇌")
- 반드시 유효한 JSON 배열로만 응답
- 중복 용어 제거
- 최대 15개"""


def extract_terms_from_articles(max_articles: int = 30) -> list[dict]:
    """최근 기사에서 AI 용어를 추출하고 설명을 생성."""
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]
    processed.sort(key=lambda x: x.get("crawled_at", ""), reverse=True)
    target = processed[:max_articles]

    if not target:
        return []

    # 태그 + 제목에서 용어 후보 수집
    all_tags = set()
    titles = []
    for a in target:
        for t in a.get("tags", []):
            all_tags.add(t)
        titles.append(a.get("title", ""))

    # 기존 용어 로드 (중복 방지)
    existing = safe_read_json(GLOSSARY_PATH, [])
    existing_terms = {g["term"].lower() for g in existing}

    # 새 용어 후보만 필터
    new_tags = [t for t in all_tags if t.lower() not in existing_terms]
    if not new_tags:
        log("[용어 사전] 새 용어 없음")
        return existing

    prompt = f"""다음 AI 뉴스 태그 목록에서 AI 전문 용어를 추출하고 쉽게 설명해줘.

태그: {', '.join(new_tags[:50])}

참고 뉴스 제목:
{chr(10).join(titles[:10])}

이미 등록된 용어 (제외): {', '.join(list(existing_terms)[:30])}"""

    try:
        response_text = call_gemini(prompt, use_flash=True)
        cleaned = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        new_terms = json.loads(cleaned)
    except Exception as e:
        log(f"[용어 사전 오류] {e}")
        return existing

    if not isinstance(new_terms, list):
        return existing

    # 중복 제거 후 병합
    for term in new_terms:
        if not isinstance(term, dict) or "term" not in term:
            continue
        if term["term"].lower() not in existing_terms:
            term["added_at"] = now_iso()
            existing.append(term)
            existing_terms.add(term["term"].lower())

    # 저장
    safe_write_json(GLOSSARY_PATH, existing)
    log(f"[용어 사전] {len(new_terms)}개 새 용어 추가 (총 {len(existing)}개)")
    return existing


def get_glossary() -> list[dict]:
    """저장된 용어 사전 전체 반환 (가나다/알파벳 순)."""
    terms = safe_read_json(GLOSSARY_PATH, [])
    terms.sort(key=lambda x: x.get("term", "").lower())
    return terms


def search_glossary(query: str) -> list[dict]:
    """용어 검색."""
    terms = safe_read_json(GLOSSARY_PATH, [])
    q = query.lower()
    return [
        t for t in terms
        if q in t.get("term", "").lower()
        or q in t.get("term_ko", "").lower()
        or q in t.get("short_desc", "").lower()
    ]
