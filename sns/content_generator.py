"""AI 콘텐츠 자동 생성 — 뉴스 기반 SNS 콘텐츠 초안 작성

플랫폼별 최적화된 콘텐츠를 LLM으로 자동 생성합니다:
- X (Twitter): 280자 트윗 + 해시태그
- Threads: 500자 쓰레드 포스트
- Instagram: 캡션 + 해시태그 30개
- 블로그: 800~1500자 블로그 포스트
- LinkedIn: 전문적 톤의 인사이트 포스트
"""
import json

from config import CATEGORIES
from ai.model_router import call_gemini, get_active_provider
from utils.helpers import log

# 플랫폼별 프롬프트 템플릿
CONTENT_TEMPLATES = {
    "tweet": {
        "name": "X (트윗)",
        "icon": "🐦",
        "max_length": 280,
        "prompt": """다음 AI 뉴스를 기반으로 X(트위터) 트윗을 작성해줘.

규칙:
- 280자 이내 (필수)
- 핵심만 간결하게
- 해시태그 2~3개 포함
- 이모지 1~2개 자연스럽게
- AI 봇이 쓴 느낌이 나지 않도록 사람처럼 자연스럽게
- 한국어로 작성

뉴스: {title}
요약: {summary}
카테고리: {category}

트윗만 출력해. 다른 설명 없이.""",
    },
    "thread": {
        "name": "Threads",
        "icon": "🧵",
        "max_length": 500,
        "prompt": """다음 AI 뉴스를 기반으로 Threads 포스트를 작성해줘.

규칙:
- 500자 이내
- 인사이트 중심 (단순 뉴스 전달 X)
- 내 생각/의견 포함하는 톤
- 해시태그 3~5개
- 대화체로 편하게
- AI 봇이 쓴 느낌 X, 실제 사용자가 쓴 것처럼
- 한국어로 작성

뉴스: {title}
요약: {summary}
카테고리: {category}

포스트만 출력해.""",
    },
    "instagram": {
        "name": "Instagram 캡션",
        "icon": "📸",
        "max_length": 2200,
        "prompt": """다음 AI 뉴스를 기반으로 Instagram 캡션을 작성해줘.

규칙:
- 첫 줄에 훅 (관심을 끄는 한 줄)
- 본문 3~5줄 (핵심 인사이트)
- 줄바꿈으로 가독성 확보
- CTA (댓글/저장 유도) 한 줄
- 해시태그 15~20개 (관련성 높은 것만)
- 이모지 적절히 사용하되 과하지 않게
- AI가 쓴 느낌 X
- 한국어로 작성

뉴스: {title}
요약: {summary}
카테고리: {category}
태그: {tags}

캡션만 출력해.""",
    },
    "blog": {
        "name": "블로그 포스트",
        "icon": "📝",
        "max_length": 3000,
        "prompt": """다음 AI 뉴스를 기반으로 블로그 포스트를 작성해줘.

규칙:
- 800~1500자
- 제목 (매력적으로) + 본문
- 서론 (왜 이 뉴스가 중요한지)
- 본론 (핵심 내용 + 의미 분석)
- 결론 (앞으로의 전망 / 내 생각)
- 마크다운 포맷
- 전문적이지만 읽기 쉬운 톤
- AI가 쓴 느낌 X, 블로거가 직접 분석한 것처럼
- 한국어로 작성

뉴스: {title}
요약: {summary}
카테고리: {category}
태그: {tags}
원문 URL: {url}

블로그 포스트만 출력해.""",
    },
    "linkedin": {
        "name": "LinkedIn",
        "icon": "💼",
        "max_length": 3000,
        "prompt": """다음 AI 뉴스를 기반으로 LinkedIn 포스트를 작성해줘.

규칙:
- 500~1000자
- 전문적이고 인사이트 있는 톤
- 첫 줄 훅 (스크롤 멈추게)
- 업계 동향 분석 관점
- 실무에 적용 가능한 인사이트 포함
- CTA (의견 물어보기)
- 해시태그 5~8개
- AI 느낌 X, 현업 전문가가 쓴 것처럼
- 한국어로 작성

뉴스: {title}
요약: {summary}
카테고리: {category}

포스트만 출력해.""",
    },
}


def generate_content(article: dict, platform: str) -> dict:
    """기사 기반 SNS 콘텐츠 생성

    Args:
        article: 뉴스 기사 dict
        platform: 플랫폼 키 (tweet, thread, instagram, blog, linkedin)

    Returns:
        {"platform": str, "content": str, "success": bool, "error": str}
    """
    if not get_active_provider():
        return {"platform": platform, "content": "", "success": False, "error": "LLM API 키 미설정"}

    template = CONTENT_TEMPLATES.get(platform)
    if not template:
        return {"platform": platform, "content": "", "success": False, "error": f"지원하지 않는 플랫폼: {platform}"}

    prompt = template["prompt"].format(
        title=article.get("title", ""),
        summary=article.get("summary_text", ""),
        category=CATEGORIES.get(article.get("category", ""), "AI"),
        tags=", ".join(article.get("tags", [])),
        url=article.get("url", ""),
    )

    try:
        content = call_gemini(prompt, use_flash=True)
        content = content.strip()
        # 길이 제한
        if len(content) > template["max_length"]:
            content = content[:template["max_length"] - 3] + "..."

        log(f"[콘텐츠 생성] {platform}: {len(content)}자")
        return {"platform": platform, "content": content, "success": True}

    except Exception as e:
        log(f"[콘텐츠 생성 오류] {platform}: {e}")
        return {"platform": platform, "content": "", "success": False, "error": str(e)}


def generate_multi_content(article: dict, platforms: list[str]) -> list[dict]:
    """여러 플랫폼용 콘텐츠 일괄 생성"""
    results = []
    for p in platforms:
        result = generate_content(article, p)
        results.append(result)
    return results


def get_content_templates() -> dict:
    """사용 가능한 콘텐츠 템플릿 목록"""
    return {k: {"name": v["name"], "icon": v["icon"], "max_length": v["max_length"]} for k, v in CONTENT_TEMPLATES.items()}
