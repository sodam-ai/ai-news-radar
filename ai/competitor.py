"""경쟁 도구 모니터링 — AI 도구별 뉴스 자동 추적 비교

3개 분야의 주요 도구/제품을 추적하고, 뉴스 언급량/감성/트렌드를 비교합니다.
"""
from config import DATA_DIR
from utils.helpers import safe_read_json

ARTICLES_PATH = DATA_DIR / "articles.json"

# ── 추적 대상 도구 정의 ──
COMPETITOR_GROUPS = {
    "ai_image_video": {
        "name": "AI 이미지/영상 도구",
        "icon": "🎨",
        "tools": [
            {"id": "midjourney", "name": "Midjourney", "keywords": ["midjourney"], "color": "#5865F2"},
            {"id": "stable_diffusion", "name": "Stable Diffusion", "keywords": ["stable diffusion", "stability ai", "sdxl", "sd3"], "color": "#A855F7"},
            {"id": "flux", "name": "Flux", "keywords": ["flux", "black forest labs"], "color": "#F97316"},
            {"id": "dalle", "name": "DALL-E", "keywords": ["dall-e", "dalle", "dall·e"], "color": "#10B981"},
            {"id": "sora", "name": "Sora", "keywords": ["sora"], "color": "#EF4444"},
            {"id": "runway", "name": "Runway", "keywords": ["runway", "gen-3", "gen-4"], "color": "#3B82F6"},
            {"id": "kling", "name": "Kling", "keywords": ["kling", "클링"], "color": "#EC4899"},
            {"id": "comfyui", "name": "ComfyUI", "keywords": ["comfyui", "comfy ui"], "color": "#8B5CF6"},
        ],
    },
    "ai_coding": {
        "name": "바이브코딩/AI코딩 도구",
        "icon": "💻",
        "tools": [
            {"id": "claude_code", "name": "Claude Code", "keywords": ["claude code", "클로드 코드"], "color": "#D97706"},
            {"id": "cursor", "name": "Cursor", "keywords": ["cursor", "커서"], "color": "#7C3AED"},
            {"id": "copilot", "name": "GitHub Copilot", "keywords": ["copilot", "코파일럿"], "color": "#2563EB"},
            {"id": "v0", "name": "v0", "keywords": ["v0.dev", "v0 by vercel"], "color": "#000000"},
            {"id": "bolt", "name": "Bolt", "keywords": ["bolt.new", "bolt"], "color": "#F59E0B"},
            {"id": "windsurf", "name": "Windsurf", "keywords": ["windsurf", "codeium"], "color": "#06B6D4"},
            {"id": "devin", "name": "Devin", "keywords": ["devin", "cognition"], "color": "#DC2626"},
            {"id": "replit", "name": "Replit Agent", "keywords": ["replit agent", "replit ai"], "color": "#F97316"},
        ],
    },
    "ai_ontology": {
        "name": "온톨로지/지식그래프 도구",
        "icon": "🔮",
        "tools": [
            {"id": "neo4j", "name": "Neo4j", "keywords": ["neo4j", "네오포제이"], "color": "#008CC1"},
            {"id": "protege", "name": "Protege", "keywords": ["protege", "프로테제"], "color": "#7C3AED"},
            {"id": "graphdb", "name": "GraphDB", "keywords": ["graphdb", "ontotext"], "color": "#059669"},
            {"id": "stardog", "name": "Stardog", "keywords": ["stardog"], "color": "#2563EB"},
            {"id": "kg_llm", "name": "Knowledge Graph + LLM", "keywords": ["knowledge graph", "지식그래프", "graph rag", "graphrag"], "color": "#D97706"},
        ],
    },
}


def _match_tool(article: dict, tool: dict) -> int:
    """기사와 도구의 매칭 스코어"""
    text = f"{article.get('title', '')} {article.get('summary_text', '')} {' '.join(article.get('tags', []))}".lower()
    score = 0
    for kw in tool["keywords"]:
        if kw.lower() in text:
            # 제목 매칭은 가중치 3배
            if kw.lower() in article.get("title", "").lower():
                score += 3
            else:
                score += 1
    return score


def get_competitor_analysis(group_id: str = None) -> dict:
    """경쟁 도구 분석 결과 반환

    Returns:
        {
            "group_id": {
                "name": "...",
                "icon": "...",
                "tools": [
                    {
                        "id": "...", "name": "...", "color": "...",
                        "mention_count": N,
                        "sentiment": {"positive": N, "neutral": N, "negative": N},
                        "avg_importance": float,
                        "top_articles": [...],
                    }
                ]
            }
        }
    """
    articles = safe_read_json(ARTICLES_PATH, [])
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]

    groups = COMPETITOR_GROUPS if group_id is None else {group_id: COMPETITOR_GROUPS.get(group_id, {})}
    result = {}

    for gid, group in groups.items():
        if not group:
            continue
        tool_results = []

        for tool in group.get("tools", []):
            matched_articles = []
            for a in processed:
                score = _match_tool(a, tool)
                if score > 0:
                    matched_articles.append({"score": score, "article": a})

            matched_articles.sort(key=lambda x: (-x["score"], -x["article"].get("importance", 0)))

            # 감성 분포
            sentiments = {"positive": 0, "neutral": 0, "negative": 0}
            total_importance = 0
            for m in matched_articles:
                s = m["article"].get("sentiment", "neutral")
                sentiments[s] = sentiments.get(s, 0) + 1
                total_importance += m["article"].get("importance", 0)

            count = len(matched_articles)
            tool_results.append({
                "id": tool["id"],
                "name": tool["name"],
                "color": tool["color"],
                "mention_count": count,
                "sentiment": sentiments,
                "avg_importance": round(total_importance / count, 1) if count > 0 else 0,
                "top_articles": [
                    {
                        "title": m["article"]["title"],
                        "url": m["article"]["url"],
                        "sentiment": m["article"].get("sentiment", "neutral"),
                        "importance": m["article"].get("importance", 0),
                    }
                    for m in matched_articles[:5]
                ],
            })

        # 언급 횟수 순 정렬
        tool_results.sort(key=lambda x: x["mention_count"], reverse=True)

        result[gid] = {
            "name": group["name"],
            "icon": group["icon"],
            "tools": tool_results,
        }

    return result
