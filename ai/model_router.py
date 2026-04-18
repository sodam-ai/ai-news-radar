"""멀티 LLM 플랫폼 라우팅 + Context Caching

지원 플랫폼 (무료 할당량 있는 플랫폼 우선):
- Google Gemini: Flash-Lite 1000회/일, Flash 250회/일 (기본값)
- Groq: Llama/Gemma 무료 (분당 30회, 일 14,400회)
- Cerebras: Llama 무료 (분당 30회)
- SambaNova: Llama 무료 (분당 10회)
- Mistral: 무료 실험용 API 제공
- Cohere: Command 무료 (월 1000회)
- HuggingFace: 무료 Inference API
- Together AI: 가입 시 $5 크레딧
- OpenRouter: 일부 무료 모델
- OpenAI: GPT-4o-mini (유료, 가입 크레딧)
- Anthropic: Claude (유료)
- DeepSeek: DeepSeek-V3 저렴 (100만 토큰당 $0.27)
- Fireworks AI: 가입 시 $1 크레딧
"""
import os
import json
import time
import requests as req

from utils.helpers import log

# ── 시스템 프롬프트 ──

CLASSIFICATION_SYSTEM = """너는 AI 뉴스 분류 전문가야. 각 뉴스 기사에 대해 다음을 JSON으로 반환해:
- category: ai_tool | ai_research | ai_trend | ai_tutorial | ai_business | ai_image_video | ai_coding | ai_ontology | ai_other
- importance: 1~5 (5가 가장 중요)
- sentiment: positive | negative | neutral
- sentiment_reason: 감성 판단 이유 한 줄
- tags: 핵심 키워드 3~5개 배열
- summary: 한국어 3줄 요약

카테고리 분류 기준:
- ai_image_video: AI 이미지 생성(Midjourney, Stable Diffusion, DALL-E, Flux), AI 영상 생성(Sora, Runway, Kling, Pika), ComfyUI, LoRA 등
- ai_coding: 바이브코딩, AI 코딩 도구(Claude Code, Cursor, Copilot, v0, Bolt, Windsurf, Devin), 코드 생성, 에이전트 코딩
- ai_ontology: 온톨로지, 지식그래프, Knowledge Graph, 시맨틱웹, RDF, OWL, 네오포제이(Neo4j), 그래프DB

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


# ══════════════════════════════════════════════════════════
# 프로바이더 레지스트리: 각 플랫폼의 설정 정보
# ══════════════════════════════════════════════════════════

PROVIDERS = {
    # ── 무료 할당량 충분 (추천) ──
    "gemini": {
        "name": "Google Gemini",
        "env_key": "GEMINI_API_KEY",
        "type": "gemini",  # Google 전용 SDK
        "models": {
            "lite": "gemini-2.5-flash-lite",
            "main": "gemini-2.5-flash",
        },
        "free_tier": "Flash-Lite 1000회/일, Flash 250회/일",
        "supports_multimodal": True,
    },
    "groq": {
        "name": "Groq",
        "env_key": "GROQ_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.groq.com/openai/v1",
        "models": {
            "lite": "llama-3.3-70b-versatile",
            "main": "llama-3.3-70b-versatile",
        },
        "free_tier": "분당 30회, 일 14,400회 무료",
        "supports_multimodal": False,
    },
    "cerebras": {
        "name": "Cerebras",
        "env_key": "CEREBRAS_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.cerebras.ai/v1",
        "models": {
            "lite": "llama-3.3-70b",
            "main": "llama-3.3-70b",
        },
        "free_tier": "분당 30회 무료 (초고속 추론)",
        "supports_multimodal": False,
    },
    "sambanova": {
        "name": "SambaNova",
        "env_key": "SAMBANOVA_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.sambanova.ai/v1",
        "models": {
            "lite": "Meta-Llama-3.3-70B-Instruct",
            "main": "Meta-Llama-3.3-70B-Instruct",
        },
        "free_tier": "분당 10회 무료",
        "supports_multimodal": False,
    },
    "mistral": {
        "name": "Mistral AI",
        "env_key": "MISTRAL_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.mistral.ai/v1",
        "models": {
            "lite": "mistral-small-latest",
            "main": "mistral-medium-latest",
        },
        "free_tier": "실험용 무료 API 제공",
        "supports_multimodal": False,
    },
    "cohere": {
        "name": "Cohere",
        "env_key": "COHERE_API_KEY",
        "type": "cohere",
        "models": {
            "lite": "command-r",
            "main": "command-r-plus",
        },
        "free_tier": "월 1,000회 무료",
        "supports_multimodal": False,
    },
    "huggingface": {
        "name": "HuggingFace",
        "env_key": "HF_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api-inference.huggingface.co/v1",
        "models": {
            "lite": "meta-llama/Llama-3.3-70B-Instruct",
            "main": "meta-llama/Llama-3.3-70B-Instruct",
        },
        "free_tier": "무료 Inference API (속도 제한)",
        "supports_multimodal": False,
    },

    # ── 가입 크레딧 / 저렴 ──
    "together": {
        "name": "Together AI",
        "env_key": "TOGETHER_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.together.xyz/v1",
        "models": {
            "lite": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "main": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        },
        "free_tier": "가입 시 $5 크레딧",
        "supports_multimodal": False,
    },
    "openrouter": {
        "name": "OpenRouter",
        "env_key": "OPENROUTER_API_KEY",
        "type": "openai_compat",
        "base_url": "https://openrouter.ai/api/v1",
        "models": {
            "lite": "meta-llama/llama-3.3-70b-instruct:free",
            "main": "meta-llama/llama-3.3-70b-instruct:free",
        },
        "free_tier": "일부 모델 무료 (속도 제한)",
        "supports_multimodal": False,
    },
    "fireworks": {
        "name": "Fireworks AI",
        "env_key": "FIREWORKS_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.fireworks.ai/inference/v1",
        "models": {
            "lite": "accounts/fireworks/models/llama-v3p3-70b-instruct",
            "main": "accounts/fireworks/models/llama-v3p3-70b-instruct",
        },
        "free_tier": "가입 시 $1 크레딧",
        "supports_multimodal": False,
    },
    "deepseek": {
        "name": "DeepSeek",
        "env_key": "DEEPSEEK_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.deepseek.com/v1",
        "models": {
            "lite": "deepseek-chat",
            "main": "deepseek-chat",
        },
        "free_tier": "매우 저렴 (100만 토큰당 $0.27)",
        "supports_multimodal": False,
    },

    # ── 유료 (강력) ──
    "openai": {
        "name": "OpenAI",
        "env_key": "OPENAI_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.openai.com/v1",
        "models": {
            "lite": "gpt-4o-mini",
            "main": "gpt-4o",
        },
        "free_tier": "신규 가입 시 $5 크레딧",
        "supports_multimodal": True,
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "env_key": "ANTHROPIC_API_KEY",
        "type": "anthropic",
        "models": {
            "lite": "claude-sonnet-4-6",
            "main": "claude-sonnet-4-6",
        },
        "free_tier": "유료 (API 크레딧 필요)",
        "supports_multimodal": True,
    },

    # ── 무료 / 크레딧 추가 플랫폼 ──
    "nvidia": {
        "name": "NVIDIA NIM",
        "env_key": "NVIDIA_API_KEY",
        "type": "openai_compat",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "models": {
            "lite": "meta/llama-3.3-70b-instruct",
            "main": "meta/llama-3.3-70b-instruct",
        },
        "free_tier": "1,000 크레딧 무료 (가입 시)",
        "supports_multimodal": False,
    },
    "cloudflare": {
        "name": "Cloudflare Workers AI",
        "env_key": "CF_API_TOKEN",
        "type": "openai_compat",
        "base_url": "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
        "extra_env": "CF_ACCOUNT_ID",
        "models": {
            "lite": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
            "main": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        },
        "free_tier": "일 10,000 뉴런 무료",
        "supports_multimodal": False,
    },
    "perplexity": {
        "name": "Perplexity AI",
        "env_key": "PERPLEXITY_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.perplexity.ai",
        "models": {
            "lite": "llama-3.1-sonar-small-128k-online",
            "main": "llama-3.1-sonar-large-128k-online",
        },
        "free_tier": "가입 시 $5 크레딧 (온라인 검색 포함)",
        "supports_multimodal": False,
    },
    "xai": {
        "name": "xAI (Grok)",
        "env_key": "XAI_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.x.ai/v1",
        "models": {
            "lite": "grok-2-latest",
            "main": "grok-2-latest",
        },
        "free_tier": "매월 $25 무료 크레딧",
        "supports_multimodal": True,
    },
    "ai21": {
        "name": "AI21 Labs (Jamba)",
        "env_key": "AI21_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.ai21.com/studio/v1",
        "models": {
            "lite": "jamba-1.5-mini",
            "main": "jamba-1.5-large",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },
    "upstage": {
        "name": "Upstage (Solar)",
        "env_key": "UPSTAGE_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.upstage.ai/v1/solar",
        "models": {
            "lite": "solar-pro",
            "main": "solar-pro",
        },
        "free_tier": "가입 시 무료 크레딧 (한국 기업)",
        "supports_multimodal": False,
    },
    "deepinfra": {
        "name": "DeepInfra",
        "env_key": "DEEPINFRA_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.deepinfra.com/v1/openai",
        "models": {
            "lite": "meta-llama/Llama-3.3-70B-Instruct",
            "main": "meta-llama/Llama-3.3-70B-Instruct",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },
    "hyperbolic": {
        "name": "Hyperbolic",
        "env_key": "HYPERBOLIC_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.hyperbolic.xyz/v1",
        "models": {
            "lite": "meta-llama/Llama-3.3-70B-Instruct",
            "main": "meta-llama/Llama-3.3-70B-Instruct",
        },
        "free_tier": "무료 티어 제공",
        "supports_multimodal": False,
    },
    "lepton": {
        "name": "Lepton AI",
        "env_key": "LEPTON_API_KEY",
        "type": "openai_compat",
        "base_url": "https://llama3-3-70b.lepton.run/api/v1",
        "models": {
            "lite": "llama3-3-70b",
            "main": "llama3-3-70b",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },
    "novita": {
        "name": "Novita AI",
        "env_key": "NOVITA_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.novita.ai/v3/openai",
        "models": {
            "lite": "meta-llama/llama-3.3-70b-instruct",
            "main": "meta-llama/llama-3.3-70b-instruct",
        },
        "free_tier": "가입 시 $0.5 크레딧",
        "supports_multimodal": False,
    },
    "nebius": {
        "name": "Nebius AI",
        "env_key": "NEBIUS_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.studio.nebius.ai/v1",
        "models": {
            "lite": "meta-llama/Llama-3.3-70B-Instruct",
            "main": "meta-llama/Llama-3.3-70B-Instruct",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },
    "kluster": {
        "name": "Kluster AI",
        "env_key": "KLUSTER_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.kluster.ai/v1",
        "models": {
            "lite": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
            "main": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",
        },
        "free_tier": "무료 티어 제공",
        "supports_multimodal": False,
    },
    "glhf": {
        "name": "GLHF.chat",
        "env_key": "GLHF_API_KEY",
        "type": "openai_compat",
        "base_url": "https://glhf.chat/api/openai/v1",
        "models": {
            "lite": "hf:meta-llama/Llama-3.3-70B-Instruct",
            "main": "hf:meta-llama/Llama-3.3-70B-Instruct",
        },
        "free_tier": "무료 (커뮤니티 지원)",
        "supports_multimodal": False,
    },
    "chutes": {
        "name": "Chutes AI",
        "env_key": "CHUTES_API_KEY",
        "type": "openai_compat",
        "base_url": "https://llm.chutes.ai/v1",
        "models": {
            "lite": "meta-llama/Llama-3.3-70B-Instruct",
            "main": "meta-llama/Llama-3.3-70B-Instruct",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },
    "replicate": {
        "name": "Replicate",
        "env_key": "REPLICATE_API_KEY",
        "type": "openai_compat",
        "base_url": "https://openai-proxy.replicate.com/v1",
        "models": {
            "lite": "meta/meta-llama-3-70b-instruct",
            "main": "meta/meta-llama-3-70b-instruct",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },

    # ── 아시아 플랫폼 ──
    "alibaba": {
        "name": "Alibaba Qwen (DashScope)",
        "env_key": "DASHSCOPE_API_KEY",
        "type": "openai_compat",
        "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "models": {
            "lite": "qwen-turbo",
            "main": "qwen-plus",
        },
        "free_tier": "가입 시 무료 크레딧 (100만 토큰)",
        "supports_multimodal": True,
    },
    "zhipu": {
        "name": "Zhipu AI (GLM)",
        "env_key": "ZHIPU_API_KEY",
        "type": "openai_compat",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "models": {
            "lite": "glm-4-flash",
            "main": "glm-4-plus",
        },
        "free_tier": "Flash 모델 무료",
        "supports_multimodal": True,
    },
    "moonshot": {
        "name": "Moonshot AI (Kimi)",
        "env_key": "MOONSHOT_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.moonshot.cn/v1",
        "models": {
            "lite": "moonshot-v1-8k",
            "main": "moonshot-v1-32k",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },
    "yi": {
        "name": "01.AI (Yi)",
        "env_key": "YI_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.lingyiwanwu.com/v1",
        "models": {
            "lite": "yi-lightning",
            "main": "yi-large",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },
    "baichuan": {
        "name": "Baichuan AI",
        "env_key": "BAICHUAN_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.baichuan-ai.com/v1",
        "models": {
            "lite": "Baichuan4",
            "main": "Baichuan4",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": False,
    },

    # ── 클라우드 / 엔터프라이즈 ──
    "azure_openai": {
        "name": "Azure OpenAI",
        "env_key": "AZURE_OPENAI_API_KEY",
        "type": "openai_compat",
        "base_url": "",  # AZURE_OPENAI_ENDPOINT 환경변수에서 동적 로드
        "extra_env": "AZURE_OPENAI_ENDPOINT",
        "models": {
            "lite": "gpt-4o-mini",
            "main": "gpt-4o",
        },
        "free_tier": "Azure 무료 계정 시 $200 크레딧",
        "supports_multimodal": True,
    },
    "reka": {
        "name": "Reka AI",
        "env_key": "REKA_API_KEY",
        "type": "openai_compat",
        "base_url": "https://api.reka.ai/v1",
        "models": {
            "lite": "reka-flash",
            "main": "reka-core",
        },
        "free_tier": "가입 시 무료 크레딧",
        "supports_multimodal": True,
    },

    # ──────────────────────────────────────────────────────────
    # 🏠 로컬 LLM (OpenAI-호환 API · 오프라인 · 완전 무료)
    # base_url/model은 .env로 환경별 오버라이드 가능
    # ──────────────────────────────────────────────────────────
    "ollama": {
        "name": "Ollama (로컬)",
        "env_key": "OLLAMA_API_KEY",
        "type": "openai_compat",
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        "base_url_env": "OLLAMA_BASE_URL",
        "models": {
            "lite": os.getenv("OLLAMA_MODEL_LITE", "llama3.2:3b"),
            "main": os.getenv("OLLAMA_MODEL_MAIN", "llama3.3:70b"),
        },
        "free_tier": "완전 무료 · 오프라인 실행",
        "supports_multimodal": False,
        "is_local": True,
    },
    "lmstudio": {
        "name": "LM Studio (로컬)",
        "env_key": "LMSTUDIO_API_KEY",
        "type": "openai_compat",
        "base_url": os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
        "base_url_env": "LMSTUDIO_BASE_URL",
        "models": {
            "lite": os.getenv("LMSTUDIO_MODEL", "local-model"),
            "main": os.getenv("LMSTUDIO_MODEL", "local-model"),
        },
        "free_tier": "완전 무료 · GUI 모델 관리",
        "supports_multimodal": False,
        "is_local": True,
    },
    "llamacpp": {
        "name": "llama.cpp server (로컬)",
        "env_key": "LLAMACPP_API_KEY",
        "type": "openai_compat",
        "base_url": os.getenv("LLAMACPP_BASE_URL", "http://localhost:8080/v1"),
        "base_url_env": "LLAMACPP_BASE_URL",
        "models": {
            "lite": os.getenv("LLAMACPP_MODEL", "local-model"),
            "main": os.getenv("LLAMACPP_MODEL", "local-model"),
        },
        "free_tier": "완전 무료 · 초경량",
        "supports_multimodal": False,
        "is_local": True,
    },
    "jan": {
        "name": "Jan (로컬)",
        "env_key": "JAN_API_KEY",
        "type": "openai_compat",
        "base_url": os.getenv("JAN_BASE_URL", "http://localhost:1337/v1"),
        "base_url_env": "JAN_BASE_URL",
        "models": {
            "lite": os.getenv("JAN_MODEL", "local-model"),
            "main": os.getenv("JAN_MODEL", "local-model"),
        },
        "free_tier": "완전 무료 · 크로스플랫폼 GUI",
        "supports_multimodal": False,
        "is_local": True,
    },
}


# ══════════════════════════════════════════════════════════
# 활성 프로바이더 감지
# ══════════════════════════════════════════════════════════

def get_active_provider() -> str:
    """환경변수에서 LLM_PROVIDER를 읽거나, API 키가 있는 첫 번째 프로바이더를 자동 감지"""
    # 1. 명시적 설정
    explicit = os.getenv("LLM_PROVIDER", "").lower().strip()
    if explicit and explicit in PROVIDERS:
        env_key = PROVIDERS[explicit]["env_key"]
        if os.getenv(env_key):
            return explicit

    # 2. API 키가 있는 프로바이더 자동 감지 (우선순위: 무료 할당량 많은 순서)
    priority = [
        # 무료 할당량 충분
        "gemini", "groq", "cerebras", "sambanova", "xai",
        "mistral", "cohere", "huggingface", "nvidia", "cloudflare",
        "zhipu", "kluster", "glhf", "hyperbolic",
        # 가입 크레딧 / 저렴
        "together", "openrouter", "fireworks", "deepseek", "deepinfra",
        "perplexity", "ai21", "upstage", "lepton", "novita", "nebius",
        "chutes", "replicate", "alibaba", "moonshot", "yi", "baichuan",
        "reka",
        # 유료 (강력)
        "openai", "azure_openai", "anthropic",
    ]
    for name in priority:
        env_key = PROVIDERS[name]["env_key"]
        key = os.getenv(env_key, "")
        if key and key != f"your_{name}_api_key_here":
            return name

    return ""


def get_available_providers() -> list[dict]:
    """API 키가 설정된 모든 프로바이더 목록 반환"""
    available = []
    for name, info in PROVIDERS.items():
        key = os.getenv(info["env_key"], "")
        if key and not key.startswith("your_"):
            available.append({
                "id": name,
                "name": info["name"],
                "free_tier": info["free_tier"],
                "multimodal": info["supports_multimodal"],
            })
    return available


# ══════════════════════════════════════════════════════════
# 프로바이더별 API 호출 구현
# ══════════════════════════════════════════════════════════

def _call_gemini_api(prompt: str, system: str, use_flash: bool) -> str:
    """Google Gemini SDK로 호출"""
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY", "")
    genai.configure(api_key=api_key)

    model_name = PROVIDERS["gemini"]["models"]["main" if use_flash else "lite"]
    model = genai.GenerativeModel(model_name=model_name, system_instruction=system)

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )
    return response.text


def _call_openai_compat(provider_id: str, prompt: str, system: str, use_flash: bool) -> str:
    """OpenAI 호환 API로 호출 (Groq, Cerebras, OpenAI, Together 등 30+ 플랫폼)"""
    info = PROVIDERS[provider_id]
    api_key = os.getenv(info["env_key"], "")
    base_url = info.get("base_url", "")
    model = info["models"]["main" if use_flash else "lite"]

    # Cloudflare: {account_id} 동적 치환
    if provider_id == "cloudflare":
        account_id = os.getenv("CF_ACCOUNT_ID", "")
        base_url = base_url.replace("{account_id}", account_id)

    # Azure OpenAI: 엔드포인트 동적 로드
    if provider_id == "azure_openai":
        base_url = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/") + "/openai/deployments/" + model + "/v1"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Azure OpenAI: api-key 헤더 방식
    if provider_id == "azure_openai":
        headers = {
            "api-key": api_key,
            "Content-Type": "application/json",
        }

    # OpenRouter: 추가 헤더 필요
    if provider_id == "openrouter":
        headers["HTTP-Referer"] = "https://github.com/sodam-ai/ai-news-radar"
        headers["X-Title"] = "AI News Radar"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }

    resp = req.post(
        f"{base_url}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def _call_cohere_api(prompt: str, system: str, use_flash: bool) -> str:
    """Cohere API로 호출"""
    api_key = os.getenv("COHERE_API_KEY", "")
    model = PROVIDERS["cohere"]["models"]["main" if use_flash else "lite"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "message": prompt,
        "preamble": system,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }

    resp = req.post(
        "https://api.cohere.com/v2/chat",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["text"]


def _call_anthropic_api(prompt: str, system: str, use_flash: bool) -> str:
    """Anthropic Claude API로 호출"""
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    model = PROVIDERS["anthropic"]["models"]["main" if use_flash else "lite"]

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "max_tokens": 4096,
        "system": system,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
    }

    resp = req.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["content"][0]["text"]


# ══════════════════════════════════════════════════════════
# 통합 호출 함수 (기존 인터페이스 유지)
# ══════════════════════════════════════════════════════════

def call_gemini(prompt: str, use_flash: bool = False) -> str:
    """LLM API 호출 + 재시도 로직 (멀티 플랫폼 지원)

    기존 함수명 유지: batch_processor.py, briefing.py에서 이 함수를 호출함.
    내부적으로 활성 프로바이더에 따라 적절한 API를 호출.
    """
    provider_id = get_active_provider()
    if not provider_id:
        raise RuntimeError(
            "LLM API 키가 설정되지 않았습니다. .env 파일에 API 키를 입력하세요.\n"
            "무료 추천: GEMINI_API_KEY, GROQ_API_KEY, CEREBRAS_API_KEY"
        )

    info = PROVIDERS[provider_id]
    provider_type = info["type"]
    system = BRIEFING_SYSTEM if use_flash else CLASSIFICATION_SYSTEM

    for attempt in range(3):
        try:
            if provider_type == "gemini":
                return _call_gemini_api(prompt, system, use_flash)
            elif provider_type == "openai_compat":
                return _call_openai_compat(provider_id, prompt, system, use_flash)
            elif provider_type == "cohere":
                return _call_cohere_api(prompt, system, use_flash)
            elif provider_type == "anthropic":
                return _call_anthropic_api(prompt, system, use_flash)
            else:
                raise ValueError(f"지원하지 않는 프로바이더 타입: {provider_type}")

        except Exception as e:
            log(f"[{info['name']} 오류] 시도 {attempt + 1}/3: {e}")
            if attempt == 2:
                raise

    return ""


def call_gemini_multimodal(image_url: str) -> str:
    """이미지 멀티모달 분석 (Gemini/OpenAI만 지원, 비지원 시 스킵)"""
    provider_id = get_active_provider()
    if not provider_id:
        return "LLM 프로바이더 미설정"

    info = PROVIDERS[provider_id]

    # 멀티모달 미지원 프로바이더는 스킵
    if not info.get("supports_multimodal"):
        return ""

    if info["type"] == "gemini":
        return _call_gemini_multimodal_impl(image_url)
    elif provider_id == "openai":
        return _call_openai_multimodal_impl(image_url)
    elif provider_id == "anthropic":
        return _call_anthropic_multimodal_impl(image_url)

    return ""


def _call_gemini_multimodal_impl(image_url: str) -> str:
    """Gemini 멀티모달 이미지 분석"""
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY", "")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=PROVIDERS["gemini"]["models"]["main"],
        system_instruction=IMAGE_ANALYSIS_SYSTEM,
    )

    try:
        resp = req.get(image_url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp.raise_for_status()
    except Exception as e:
        return f"이미지 다운로드 실패: {e}"

    content_type = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
    if content_type not in ("image/jpeg", "image/png", "image/webp", "image/gif"):
        content_type = "image/jpeg"

    image_part = {"mime_type": content_type, "data": resp.content}

    for attempt in range(3):
        try:
            response = model.generate_content(
                ["이 뉴스 이미지를 분석해줘:", image_part],
                generation_config=genai.types.GenerationConfig(temperature=0.1),
            )
            return response.text
        except Exception as e:
            log(f"[Gemini 멀티모달 오류] 시도 {attempt + 1}/3: {e}")
            if attempt == 2:
                return f"이미지 분석 실패: {e}"
    return ""


def _call_openai_multimodal_impl(image_url: str) -> str:
    """OpenAI Vision 이미지 분석"""
    api_key = os.getenv("OPENAI_API_KEY", "")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": IMAGE_ANALYSIS_SYSTEM},
            {"role": "user", "content": [
                {"type": "text", "text": "이 뉴스 이미지를 분석해줘:"},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]},
        ],
        "temperature": 0.1,
        "max_tokens": 500,
    }

    try:
        resp = req.post("https://api.openai.com/v1/chat/completions",
                        headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"이미지 분석 실패: {e}"


def _call_anthropic_multimodal_impl(image_url: str) -> str:
    """Anthropic Claude Vision 이미지 분석"""
    import base64

    api_key = os.getenv("ANTHROPIC_API_KEY", "")

    try:
        img_resp = req.get(image_url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        img_resp.raise_for_status()
    except Exception as e:
        return f"이미지 다운로드 실패: {e}"

    content_type = img_resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
    b64_data = base64.b64encode(img_resp.content).decode("utf-8")

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    payload = {
        "model": PROVIDERS["anthropic"]["models"]["main"],
        "max_tokens": 500,
        "system": IMAGE_ANALYSIS_SYSTEM,
        "messages": [{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": content_type, "data": b64_data}},
            {"type": "text", "text": "이 뉴스 이미지를 분석해줘:"},
        ]}],
        "temperature": 0.1,
    }

    try:
        resp = req.post("https://api.anthropic.com/v1/messages",
                        headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]
    except Exception as e:
        return f"이미지 분석 실패: {e}"
