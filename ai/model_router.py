"""Gemini 스마트 모델 라우팅 + Context Caching"""
import time
import google.generativeai as genai
from google.generativeai import caching

from config import GEMINI_API_KEY, GEMINI_FLASH_MODEL, GEMINI_FLASH_LITE_MODEL
from utils.helpers import log

# API 초기화
genai.configure(api_key=GEMINI_API_KEY)

# 시스템 프롬프트 (캐싱 대상)
CLASSIFICATION_SYSTEM = """너는 AI 뉴스 분류 전문가야. 각 뉴스 기사에 대해 다음을 JSON으로 반환해:
- category: ai_tool | ai_research | ai_trend | ai_tutorial | ai_business | ai_other
- importance: 1~5 (5가 가장 중요)
- sentiment: positive | negative | neutral
- sentiment_reason: 감성 판단 이유 한 줄
- tags: 핵심 키워드 3~5개 배열
- summary: 한국어 3줄 요약

반드시 유효한 JSON 배열로만 응답해. 다른 텍스트 없이."""

BRIEFING_SYSTEM = """너는 AI 뉴스 브리핑 작성 전문가야.
주어진 뉴스 목록에서 가장 중요한 TOP 5를 선정하고, 각각에 대해:
- headline: 한 줄 헤드라인
- why_important: 왜 중요한지 한 줄
- article_id: 해당 기사 ID

그리고 마지막에:
- overall_summary: 오늘의 AI 동향 총평 2~3줄

반드시 유효한 JSON으로만 응답해."""

IMAGE_ANALYSIS_SYSTEM = """너는 뉴스 이미지 분석 전문가야.
이미지를 분석해서 다음 정보를 한국어로 추출해:
- 이미지 유형 (차트/그래프/인포그래픽/사진/스크린샷 등)
- 핵심 수치나 데이터 (벤치마크 점수, 비교 수치 등)
- 이미지가 전달하는 핵심 메시지 한 줄

2~3줄로 간결하게 요약해. JSON이 아닌 일반 텍스트로 응답해."""


# ── Context Caching: 모델 인스턴스 재사용 ──
# system_instruction으로 시스템 프롬프트를 바인딩한 모델 인스턴스를 캐싱합니다.
# 이렇게 하면 매 요청마다 시스템 프롬프트 토큰을 중복 전송하지 않습니다.

_cached_models = {}


def _get_cached_model(model_name: str, system_prompt: str):
    """시스템 프롬프트가 바인딩된 모델 인스턴스를 캐싱하여 반환"""
    cache_key = f"{model_name}:{hash(system_prompt)}"
    if cache_key not in _cached_models:
        _cached_models[cache_key] = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt,
        )
    return _cached_models[cache_key]


# ── 서버 측 Context Caching (Gemini Caching API) ──
# 서버 캐시는 최소 토큰 요구사항이 있어 실패할 수 있으므로 graceful fallback

_server_cache = {}  # {cache_key: (cached_content, expire_time)}
CACHE_TTL_MINUTES = 60


def _try_server_cache(model_name: str, system_prompt: str):
    """서버 측 캐시 생성 시도. 실패 시 None 반환."""
    cache_key = f"server:{model_name}:{hash(system_prompt)}"

    # 기존 캐시 확인
    if cache_key in _server_cache:
        cached, expire_time = _server_cache[cache_key]
        if time.time() < expire_time:
            try:
                return genai.GenerativeModel.from_cached_content(cached)
            except Exception:
                del _server_cache[cache_key]

    # 새 서버 캐시 생성 시도
    try:
        import datetime
        cached_content = caching.CachedContent.create(
            model=model_name,
            system_instruction=system_prompt,
            ttl=datetime.timedelta(minutes=CACHE_TTL_MINUTES),
        )
        _server_cache[cache_key] = (cached_content, time.time() + CACHE_TTL_MINUTES * 60)
        log(f"[Context Cache] 서버 캐시 생성 성공: {model_name}")
        return genai.GenerativeModel.from_cached_content(cached_content)
    except Exception as e:
        # 최소 토큰 미달 등으로 실패 시 무시
        log(f"[Context Cache] 서버 캐시 불가 (정상 — 클라이언트 캐시 사용): {e}")
        return None


def get_lite_model():
    """경량 작업용 (분류/태그/감성) — Flash-Lite (1000회/일) + Context Caching"""
    server_model = _try_server_cache(GEMINI_FLASH_LITE_MODEL, CLASSIFICATION_SYSTEM)
    if server_model:
        return server_model
    return _get_cached_model(GEMINI_FLASH_LITE_MODEL, CLASSIFICATION_SYSTEM)


def get_flash_model():
    """고품질 작업용 (요약/브리핑) — Flash (250회/일) + Context Caching"""
    server_model = _try_server_cache(GEMINI_FLASH_MODEL, BRIEFING_SYSTEM)
    if server_model:
        return server_model
    return _get_cached_model(GEMINI_FLASH_MODEL, BRIEFING_SYSTEM)


def get_image_model():
    """이미지 분석용 — Flash (멀티모달) + Context Caching"""
    server_model = _try_server_cache(GEMINI_FLASH_MODEL, IMAGE_ANALYSIS_SYSTEM)
    if server_model:
        return server_model
    return _get_cached_model(GEMINI_FLASH_MODEL, IMAGE_ANALYSIS_SYSTEM)


def call_gemini(prompt: str, use_flash: bool = False) -> str:
    """Gemini API 호출 + 재시도 로직 (Context Caching 적용)"""
    model = get_flash_model() if use_flash else get_lite_model()

    for attempt in range(3):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )
            return response.text
        except Exception as e:
            log(f"[Gemini 오류] 시도 {attempt + 1}/3: {e}")
            if attempt == 2:
                raise
    return ""


def call_gemini_multimodal(image_url: str) -> str:
    """이미지 URL로 멀티모달 분석 + 재시도"""
    import requests as req

    model = get_image_model()

    # 이미지 다운로드
    try:
        resp = req.get(image_url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp.raise_for_status()
    except Exception as e:
        return f"이미지 다운로드 실패: {e}"

    # Content-Type에서 MIME 타입 추출
    content_type = resp.headers.get("Content-Type", "image/jpeg")
    if ";" in content_type:
        content_type = content_type.split(";")[0].strip()
    if content_type not in ("image/jpeg", "image/png", "image/webp", "image/gif"):
        content_type = "image/jpeg"

    image_part = {
        "mime_type": content_type,
        "data": resp.content,
    }

    for attempt in range(3):
        try:
            response = model.generate_content(
                ["이 뉴스 이미지를 분석해줘:", image_part],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                ),
            )
            return response.text
        except Exception as e:
            log(f"[멀티모달 오류] 시도 {attempt + 1}/3: {e}")
            if attempt == 2:
                return f"이미지 분석 실패: {e}"
    return ""
