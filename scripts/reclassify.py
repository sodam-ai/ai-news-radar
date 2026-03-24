"""기존 기사 카테고리 재분류 — 새 3개 카테고리에 키워드 기반 재배정

신규 카테고리:
  ai_image_video: AI 이미지/영상 생성
  ai_coding: 바이브코딩/AI 코딩
  ai_ontology: 온톨로지/지식그래프

기존에 ai_tool, ai_other 등으로 분류된 기사 중
새 카테고리 키워드에 매칭되는 것을 재배정합니다.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_DIR
from utils.helpers import safe_read_json, safe_write_json

ARTICLES_PATH = DATA_DIR / "articles.json"

# 재분류 키워드 (제목 + 태그 + 요약에서 매칭)
RECLASSIFY_RULES = {
    "ai_image_video": {
        "keywords": [
            "midjourney", "stable diffusion", "dall-e", "dalle", "dall·e",
            "flux", "sora", "runway", "kling", "pika", "comfyui", "comfy ui",
            "lora", "text-to-image", "text-to-video", "image generation",
            "video generation", "ai art", "ai image", "ai video",
            "이미지 생성", "영상 생성", "텍스트 투 이미지",
            "생성형 이미지", "생성형 영상", "sd3", "sdxl",
            "diffusion", "img2img", "controlnet", "inpainting",
            "replicate", "fal.ai", "elevenlabs", "luma ai",
            "stability ai", "civitai", "deforum",
            "imagen", "firefly", "adobe firefly",
            "generative ai art", "ai 그림", "ai 사진",
        ],
        "title_boost": True,  # 제목 매칭 시 우선
    },
    "ai_coding": {
        "keywords": [
            "claude code", "cursor", "copilot", "github copilot",
            "v0", "v0.dev", "bolt", "bolt.new", "windsurf", "codeium",
            "devin", "cognition", "replit agent", "replit ai",
            "vibe coding", "vibecoding", "바이브코딩", "바이브 코딩",
            "ai coding", "ai 코딩", "code generation", "코드 생성",
            "agentic coding", "aider", "continue.dev",
            "sourcegraph", "tabnine", "cody",
            "code assistant", "코드 어시스턴트",
            "ai ide", "ai editor", "ai 에디터",
            "programming assistant", "코딩 도구", "개발 도구",
        ],
        "title_boost": True,
    },
    "ai_ontology": {
        "keywords": [
            "ontology", "온톨로지", "knowledge graph", "지식그래프", "지식 그래프",
            "neo4j", "네오포제이", "rdf", "owl", "sparql",
            "semantic web", "시맨틱 웹", "시맨틱웹",
            "graph database", "그래프 데이터베이스", "graphdb",
            "linked data", "triple store", "knowledge base",
            "entity resolution", "relation extraction",
            "graph rag", "graphrag", "graph neural",
            "protege", "stardog",
        ],
        "title_boost": True,
    },
}


def reclassify_articles():
    """기존 기사를 새 카테고리 키워드로 재분류"""
    articles = safe_read_json(ARTICLES_PATH, [])
    if not articles:
        print("기사 없음")
        return

    reclassified = 0
    for article in articles:
        if not article.get("ai_processed"):
            continue

        title = article.get("title", "").lower()
        summary = article.get("summary_text", "").lower()
        tags = " ".join(article.get("tags", [])).lower()
        text = f"{title} {summary} {tags}"

        # 각 새 카테고리에 대해 매칭 점수 계산
        best_cat = None
        best_score = 0

        for cat_id, rule in RECLASSIFY_RULES.items():
            score = 0
            for kw in rule["keywords"]:
                if kw.lower() in text:
                    if rule.get("title_boost") and kw.lower() in title:
                        score += 5  # 제목 매칭 가중치
                    else:
                        score += 1

            if score > best_score:
                best_score = score
                best_cat = cat_id

        # 점수 2 이상이면 재분류 (오분류 방지)
        if best_cat and best_score >= 2:
            old_cat = article.get("category", "")
            if old_cat != best_cat:
                article["category"] = best_cat
                article["_reclassified_from"] = old_cat
                reclassified += 1

    if reclassified > 0:
        safe_write_json(ARTICLES_PATH, articles)

    print(f"재분류 완료: {reclassified}개 기사")

    # 결과 확인
    from collections import Counter
    processed = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]
    cats = Counter(a.get("category", "NONE") for a in processed)
    print("\n카테고리 분포:")
    from config import CATEGORIES
    for cat, count in cats.most_common():
        label = CATEGORIES.get(cat, f"[{cat}]")
        print(f"  {cat}: {count}개 ({label})")


if __name__ == "__main__":
    reclassify_articles()
