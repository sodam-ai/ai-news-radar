"""뉴스 디베이트 모드 — AI가 두 도구를 찬반 근거로 비교 분석

"Midjourney vs Flux" 같은 대결 주제에 대해
AI가 각 도구의 장점 3개 + 단점 3개 + 최종 결론을 생성합니다.
"""
import json

from config import DATA_DIR
from ai.model_router import call_gemini, get_active_provider
from ai.competitor import COMPETITOR_GROUPS
from utils.helpers import safe_read_json, log

ARTICLES_PATH = DATA_DIR / "articles.json"

DEBATE_SYSTEM = """너는 AI 도구 비교 분석 전문가야.
두 AI 도구를 뉴스 기사를 근거로 공정하게 비교 분석해.

다음 JSON으로 응답해:
{
  "tool_a": {
    "name": "도구A 이름",
    "pros": ["장점1", "장점2", "장점3"],
    "cons": ["단점1", "단점2", "단점3"]
  },
  "tool_b": {
    "name": "도구B 이름",
    "pros": ["장점1", "장점2", "장점3"],
    "cons": ["단점1", "단점2", "단점3"]
  },
  "verdict": "최종 결론 (어떤 상황에서 어떤 도구가 적합한지 2~3줄)",
  "recommendation": "입문자에게 추천하는 도구 1개 + 이유 한 줄"
}

규칙:
- 제공된 뉴스 기사를 근거로 분석 (추측 X)
- 한국어로 작성
- 공정하고 균형 잡힌 비교
- 반드시 유효한 JSON으로만 응답"""


def _find_tool_articles(tool_keywords: list[str], max_articles: int = 10) -> list[dict]:
    """도구 관련 기사 검색"""
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    matched = []
    for a in processed:
        text = f"{a.get('title', '')} {a.get('summary_text', '')} {' '.join(a.get('tags', []))}".lower()
        for kw in tool_keywords:
            if kw.lower() in text:
                matched.append(a)
                break

    matched.sort(key=lambda x: x.get("importance", 0), reverse=True)
    return matched[:max_articles]


def generate_debate(tool_a_name: str, tool_b_name: str, tool_a_keywords: list[str], tool_b_keywords: list[str]) -> dict | None:
    """두 도구의 디베이트(찬반 비교) 생성"""
    if not get_active_provider():
        return None

    # 관련 기사 수집
    articles_a = _find_tool_articles(tool_a_keywords)
    articles_b = _find_tool_articles(tool_b_keywords)

    # 프롬프트 구성
    context_a = "\n".join([
        f"- {a['title']}: {a.get('summary_text', '')[:100]}"
        for a in articles_a[:5]
    ]) or "(관련 기사 없음)"

    context_b = "\n".join([
        f"- {a['title']}: {a.get('summary_text', '')[:100]}"
        for a in articles_b[:5]
    ]) or "(관련 기사 없음)"

    prompt = f"""{tool_a_name} vs {tool_b_name} 비교 분석을 해줘.

{tool_a_name} 관련 뉴스 ({len(articles_a)}건):
{context_a}

{tool_b_name} 관련 뉴스 ({len(articles_b)}건):
{context_b}

두 도구의 장단점을 뉴스 기반으로 비교하고 결론을 내줘."""

    try:
        response_text = call_gemini(prompt, use_flash=True)
        cleaned = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        result = json.loads(cleaned)
        log(f"[디베이트] {tool_a_name} vs {tool_b_name} 생성 완료")
        return result
    except Exception as e:
        log(f"[디베이트 오류] {e}")
        return None


def get_debate_pairs(group_id: str) -> list[tuple[dict, dict]]:
    """추천 대결 쌍 생성 (언급량 상위 도구끼리)"""
    group = COMPETITOR_GROUPS.get(group_id)
    if not group:
        return []

    tools = group["tools"]
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    # 언급량 계산
    tool_counts = []
    for tool in tools:
        count = 0
        for a in processed:
            text = f"{a.get('title', '')} {a.get('summary_text', '')} {' '.join(a.get('tags', []))}".lower()
            if any(kw.lower() in text for kw in tool["keywords"]):
                count += 1
        if count > 0:
            tool_counts.append({"tool": tool, "count": count})

    tool_counts.sort(key=lambda x: x["count"], reverse=True)

    # 상위 도구끼리 쌍 만들기
    pairs = []
    used = set()
    for i in range(len(tool_counts)):
        for j in range(i + 1, len(tool_counts)):
            a_id = tool_counts[i]["tool"]["id"]
            b_id = tool_counts[j]["tool"]["id"]
            if a_id not in used or b_id not in used:
                pairs.append((tool_counts[i]["tool"], tool_counts[j]["tool"]))
                used.add(a_id)
                used.add(b_id)
            if len(pairs) >= 5:
                break
        if len(pairs) >= 5:
            break

    return pairs
