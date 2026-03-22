"""AI 뉴스 채팅 — 수집된 뉴스에 대해 자연어 대화"""
import json

import os
import requests as req

from config import DATA_DIR
from ai.model_router import get_active_provider, PROVIDERS, BRIEFING_SYSTEM
from utils.helpers import safe_read_json, safe_write_json, log

ARTICLES_PATH = DATA_DIR / "articles.json"
CHAT_PATH = DATA_DIR / "chat_sessions.json"

CHAT_SYSTEM = """너는 AI 뉴스 전문 어시스턴트야.
사용자가 AI 뉴스에 대해 질문하면, 아래 제공된 뉴스 기사 목록을 참고하여 정확하고 유용하게 답변해.

답변 규칙:
- 한국어로 답변
- 제공된 기사에 근거하여 답변 (근거 없는 추측 금지)
- 관련 기사의 제목을 언급하여 출처 표시
- 간결하고 핵심적으로 답변 (3~5문장)
- 관련 기사가 없으면 솔직하게 "수집된 뉴스에서 관련 내용을 찾지 못했습니다"라고 답변"""


def _find_relevant_articles(query: str, max_articles: int = 10) -> list[dict]:
    """질문과 관련된 기사를 키워드 매칭으로 검색"""
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    if not processed:
        return []

    query_lower = query.lower()
    query_words = [w.strip() for w in query_lower.split() if len(w.strip()) >= 2]

    scored = []
    for a in processed:
        text = f"{a.get('title', '')} {a.get('summary_text', '')} {' '.join(a.get('tags', []))}".lower()
        score = 0
        for word in query_words:
            if word in text:
                # 제목 매칭은 가중치 3배
                if word in a.get("title", "").lower():
                    score += 3
                else:
                    score += 1
        if score > 0:
            scored.append((score, a))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [a for _, a in scored[:max_articles]]


def chat(user_message: str, history: list[dict] = None) -> str:
    """사용자 질문에 대해 뉴스 기반으로 답변"""
    if history is None:
        history = []

    # 관련 기사 검색
    relevant = _find_relevant_articles(user_message)

    # 컨텍스트 구성
    if relevant:
        context_lines = []
        for i, a in enumerate(relevant, 1):
            context_lines.append(
                f"[{i}] {a['title']}\n"
                f"    카테고리: {a.get('category', '?')} | 감성: {a.get('sentiment', '?')} | 중요도: {a.get('importance', 0)}\n"
                f"    요약: {a.get('summary_text', a.get('content', '')[:200])}"
            )
        context = "\n\n".join(context_lines)
    else:
        context = "(관련 기사 없음)"

    # 최근 대화 히스토리 (최대 3턴)
    history_text = ""
    if history:
        recent = history[-6:]  # 최근 3턴 (Q+A × 3)
        for h in recent:
            role = "사용자" if h["role"] == "user" else "AI"
            history_text += f"{role}: {h['content']}\n"

    prompt = f"""참고할 뉴스 기사 ({len(relevant)}개):

{context}

{f'이전 대화:{chr(10)}{history_text}' if history_text else ''}
사용자 질문: {user_message}

위 뉴스 기사를 참고하여 답변해줘."""

    try:
        response = _call_chat_llm(CHAT_SYSTEM, prompt)
        return response
    except Exception as e:
        log(f"[채팅 오류] {e}")
        return f"죄송합니다, 답변 생성 중 오류가 발생했습니다: {e}"


def _call_chat_llm(system: str, prompt: str) -> str:
    """채팅용 LLM 호출 (JSON 모드 OFF — 일반 텍스트 응답)"""
    provider_id = get_active_provider()
    if not provider_id:
        return "LLM API 키가 설정되지 않았습니다."

    info = PROVIDERS[provider_id]

    # Gemini
    if info["type"] == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
        model = genai.GenerativeModel(
            model_name=info["models"]["main"],
            system_instruction=system,
        )
        response = model.generate_content(prompt)
        return response.text

    # OpenAI 호환 (대부분의 플랫폼)
    if info["type"] in ("openai_compat",):
        api_key = os.getenv(info["env_key"], "")
        base_url = info.get("base_url", "")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        payload = {
            "model": info["models"]["main"],
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
        resp = req.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    # Anthropic
    if info["type"] == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
        payload = {
            "model": info["models"]["main"],
            "max_tokens": 2048,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
        resp = req.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]

    # Cohere
    if info["type"] == "cohere":
        api_key = os.getenv("COHERE_API_KEY", "")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": info["models"]["main"], "message": prompt, "preamble": system, "temperature": 0.3}
        resp = req.post("https://api.cohere.com/v2/chat", headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["text"]

    return "지원하지 않는 프로바이더입니다."
