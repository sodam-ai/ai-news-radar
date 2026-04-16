"""Chat helper backed by the configured LLM provider."""

import os

import requests as req

from ai.model_router import PROVIDERS, get_active_provider
from db.database import get_primary_articles, search_articles
from utils.helpers import log

CHAT_SYSTEM = """You are the AI News Radar assistant.
Answer using the provided AI news context when relevant.
Keep answers concise, practical, and grounded in the retrieved articles.
If the retrieved context is insufficient, say that clearly.
"""


def _find_relevant_articles(query: str, max_articles: int = 10) -> list[dict]:
    # ChromaDB 시맨틱 검색 우선 시도
    try:
        from ai.vector_store import search, get_count
        if get_count() > 0:
            ids = search(query, n_results=max_articles)
            if ids:
                # DB에서 해당 ID의 기사 조회
                from db.database import get_article_by_id
                results = [a for a in (get_article_by_id(i) for i in ids) if a]
                if results:
                    return results
    except Exception:
        pass

    # FTS5 전문 검색 fallback
    results = search_articles(query, limit=max_articles)
    if results:
        return results

    # 키워드 매칭 fallback (FTS5 실패 시)
    articles = get_primary_articles(limit=500)
    query_words = [w.strip().lower() for w in query.split() if len(w.strip()) >= 2]
    scored = []
    for article in articles:
        text = (
            f"{article.get('title', '')} "
            f"{article.get('summary_text', '')} "
            f"{' '.join(article.get('tags', []))}"
        ).lower()
        score = sum(
            3 if word in article.get("title", "").lower() else 1
            for word in query_words if word in text
        )
        if score > 0:
            scored.append((score, article))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [article for _, article in scored[:max_articles]]


def chat(user_message: str, history: list[dict] = None) -> str:
    if history is None:
        history = []

    relevant = _find_relevant_articles(user_message)

    if relevant:
        context_lines = []
        for index, article in enumerate(relevant, 1):
            context_lines.append(
                f"[{index}] {article['title']}\n"
                f"    category: {article.get('category', '?')} | "
                f"sentiment: {article.get('sentiment', '?')} | "
                f"importance: {article.get('importance', 0)}\n"
                f"    summary: {article.get('summary_text', article.get('content', '')[:200])}"
            )
        context = "\n\n".join(context_lines)
    else:
        context = "(no directly relevant AI news articles found)"

    history_text = ""
    if history:
        for item in history[-6:]:
            role = "User" if item.get("role") == "user" else "AI"
            history_text += f"{role}: {item.get('content', '')}\n"

    prompt = f"""Relevant articles ({len(relevant)}):

{context}

{f"Recent conversation:\n{history_text}" if history_text else ""}
User question: {user_message}

Answer as the AI News Radar assistant."""

    try:
        return _call_chat_llm(CHAT_SYSTEM, prompt)
    except Exception as exc:
        log(f"[chat:error] {exc}")
        return f"응답 생성 중 오류가 발생했습니다: {exc}"


def _resolve_openai_compat_endpoint(provider_id: str, info: dict) -> tuple[str, dict]:
    api_key = os.getenv(info["env_key"], "")
    base_url = info.get("base_url", "")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    if provider_id == "cloudflare":
        account_id = os.getenv("CF_ACCOUNT_ID", "")
        base_url = base_url.replace("{account_id}", account_id)

    if provider_id == "azure_openai":
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        base_url = f"{endpoint}/openai/deployments/{info['models']['main']}/v1"
        headers = {"api-key": api_key, "Content-Type": "application/json"}

    if provider_id == "openrouter":
        headers["HTTP-Referer"] = "https://github.com/sodam-ai/ai-news-radar"
        headers["X-Title"] = "AI News Radar"

    return f"{base_url}/chat/completions", headers


def _call_chat_llm(system: str, prompt: str) -> str:
    provider_id = get_active_provider()
    if not provider_id:
        return "LLM API 키가 설정되지 않았습니다."

    info = PROVIDERS[provider_id]

    if info["type"] == "gemini":
        import google.generativeai as genai

        genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
        model = genai.GenerativeModel(
            model_name=info["models"]["main"],
            system_instruction=system,
        )
        response = model.generate_content(prompt)
        return response.text

    if info["type"] == "openai_compat":
        url, headers = _resolve_openai_compat_endpoint(provider_id, info)
        payload = {
            "model": info["models"]["main"],
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
        response = req.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    if info["type"] == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": info["models"]["main"],
            "max_tokens": 2048,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
        response = req.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["content"][0]["text"]

    if info["type"] == "cohere":
        api_key = os.getenv("COHERE_API_KEY", "")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": info["models"]["main"],
            "message": prompt,
            "preamble": system,
            "temperature": 0.3,
        }
        response = req.post("https://api.cohere.com/v2/chat", headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["text"]

    return "지원되지 않는 LLM provider입니다."
