# AI News Radar

> **AI 뉴스를 자동으로 수집하고, 요약하고, 분류해주는 나만의 AI 뉴스 대시보드 — 35개 LLM 플랫폼 지원**

**[English](./README.md) / Korean / [Japanese](./README_JA.md) / [Chinese](./README_ZH.md)**

---

## AI News Radar가 뭔가요?

AI News Radar는 전 세계 AI 관련 뉴스를 **자동으로 모아서**, AI가 **요약하고, 분류하고, 중요도를 매겨주는** 개인용 대시보드입니다. OpenAI, Gemini, Groq, Claude 등 **35개 LLM 플랫폼**을 지원하며, 대부분 무료로 사용할 수 있습니다.

**쉽게 말하면:** 매일 15개 이상의 뉴스 사이트를 돌아다니는 대신, 이 앱이 대신 해주고 중요한 것만 보여줍니다.

---

## 주요 기능 (27개)

### Phase 1 — 핵심 (17개)

| 기능 | 설명 |
|------|------|
| 자동 수집 | 15개 프리셋 소스에서 자동으로 뉴스 수집 (TechCrunch, The Verge, MIT Tech Review 등) |
| AI 요약 | 각 기사를 한국어 3줄로 요약 |
| 스마트 분류 | 6개 카테고리로 자동 분류: 도구, 연구, 트렌드, 튜토리얼, 비즈니스, 기타 |
| 중요도 점수 | 각 기사에 1~5개 별점 부여 |
| 감성 분석 | 각 기사를 긍정/중립/부정으로 분류 |
| 오늘의 브리핑 | 매일 "오늘의 AI 뉴스 TOP 5" 자동 생성 |
| 중복 병합 | 같은 뉴스를 여러 매체가 보도하면 1개로 합침 |
| 키워드 워치리스트 | 추적 키워드가 포함된 뉴스 하이라이트 (예: "Claude", "GPT") |
| 인앱 리더 | 광고 없이 대시보드 안에서 원문 읽기 |
| 다크모드 | 다크/라이트 테마 전환 |
| 내보내기 (Markdown) | 브리핑과 기사를 Markdown으로 다운로드 |
| 내보내기 (PDF) | 브리핑과 기사를 한글 지원 PDF로 다운로드 |
| 이미지 분석 | 뉴스 속 차트/인포그래픽을 AI가 분석 |
| 실시간 갱신 | 대시보드가 5분마다 자동 새로고침 |
| 타임라인 뷰 | 시간순으로 뉴스 보기 (오늘/어제/이번 주) |
| Context Caching | 시스템 프롬프트 캐싱으로 API 비용 절감 |
| 스마트 라우팅 | 단순 작업은 경량 모델, 복잡한 작업은 고성능 모델 자동 분기 |

### Phase 2-A — 확장 (5개)

| 기능 | 설명 |
|------|------|
| 검색 | 키워드 + 카테고리 + 감성 + 읽음 상태로 기사 검색 |
| 북마크 + 메모 | 중요한 기사를 저장하고 메모 추가 |
| 읽은 글 히스토리 | 읽음 표시 + 안 읽은 글 필터 |
| 감성 온도계 | Plotly 차트: 게이지(긍정 비율) + 도넛(분포) + 스택 바(카테고리별) |
| AI 채팅 | 수집된 뉴스에 대해 자연어로 질문 |

### Phase 2-B — 고급 (5개)

| 기능 | 설명 |
|------|------|
| 음성 브리핑 | 오늘의 브리핑을 AI 음성으로 듣기 (edge-tts, 여성/남성 음성 선택) |
| AI 팩트체크 | 교차 매체 검증 배지: "✅ N개 매체 확인" vs "⚠️ 단독 보도" |
| AI 용어 사전 | 뉴스 속 AI 전문 용어 자동 추출 + 초보자 쉬운 설명 (난이도/카테고리 필터) |
| 텔레그램 봇 | `/today` 브리핑, `/top` 뉴스, `/search` 검색, `/ask` AI 채팅 — 텔레그램에서 바로 |
| GitHub Actions | 하루 3회 자동 수집 (06/12/18시 KST), 수동 실행 지원, CLI 스크립트 |

---

## 35개 LLM 플랫폼 지원

아래 플랫폼 중 **아무거나 1개**의 API 키만 있으면 됩니다:

### 무료 할당량 충분 (추천)

| 플랫폼 | 무료 한도 | 키 발급 |
|--------|----------|---------|
| Google Gemini | Flash-Lite 1,000회/일, Flash 250회/일 | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| Groq | 분당 30회, 일 14,400회 | [console.groq.com/keys](https://console.groq.com/keys) |
| Cerebras | 분당 30회 (초고속) | [cloud.cerebras.ai](https://cloud.cerebras.ai/) |
| SambaNova | 분당 10회 | [cloud.sambanova.ai](https://cloud.sambanova.ai/) |
| xAI (Grok) | 월 $25 크레딧 | [console.x.ai](https://console.x.ai/) |
| Mistral AI | 실험용 무료 | [console.mistral.ai](https://console.mistral.ai/api-keys) |
| Cohere | 월 1,000회 | [dashboard.cohere.com](https://dashboard.cohere.com/api-keys) |
| HuggingFace | 무료 (속도 제한) | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| NVIDIA NIM | 1,000 크레딧 | [build.nvidia.com](https://build.nvidia.com/) |
| Cloudflare | 일 10,000 뉴런 | [dash.cloudflare.com](https://dash.cloudflare.com/) |
| + 4개 더 | .env.example 참고 | 각 사이트 |

### 가입 크레딧 / 저렴 (17개)

Together AI($5), OpenRouter(무료 모델), Fireworks($1), DeepSeek(초저가), DeepInfra, Perplexity($5), AI21, Upstage(한국), Lepton, Novita, Nebius, Chutes, Replicate, Alibaba/Qwen, Moonshot, Yi, Baichuan

### 유료 (4개)

OpenAI($5 크레딧), Azure OpenAI($200 크레딧), Anthropic Claude, Reka AI

---

## 대시보드 (8개 탭)

| 탭 | 기능 |
|----|------|
| **📋 브리핑** | 오늘의 TOP 5 + 감성 온도계 + 음성 브리핑 (MP3) |
| **📰 뉴스** | 전체 기사 + 필터 + 북마크/읽음 + 팩트체크 배지 |
| **🔍 검색** | 키워드 + 카테고리 + 감성 + 읽음 상태 필터 |
| **💬 AI 채팅** | 뉴스에 대해 자연어로 질문 |
| **📚 용어 사전** | AI 전문 용어 초보자용 설명 (난이도/카테고리 필터) |
| **⏰ 타임라인** | 시간순 뉴스 흐름 (오늘/어제/이번 주) |
| **⭐ 북마크** | 저장한 기사 + 메모 편집 |
| **📡 소스** | 15개 뉴스 소스 관리 |

---

## 시작하기 (완전 초보자용 단계별 가이드)

> **코딩 경험이 전혀 없어도 됩니다.** 각 단계를 차근차근 따라하세요.

### 1단계: Python 설치

1. [python.org/downloads](https://www.python.org/downloads/) 접속
2. 큰 노란색 **"Download Python 3.xx"** 버튼 클릭
3. 다운로드된 파일 실행
4. **중요:** 하단의 **"Add Python to PATH"** 반드시 체크
5. **"Install Now"** 클릭

**확인:** 명령 프롬프트(`Win + R` → `cmd` → Enter)에서: `python --version`

### 2단계: 프로젝트 다운로드

**방법 A: Git**
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**방법 B: 직접 다운로드** — [GitHub 페이지](https://github.com/sodam-ai/ai-news-radar) → Code → Download ZIP → 압축 해제

### 3단계: 패키지 설치

```
cd 프로젝트폴더\ai-news-radar
pip install -r requirements.txt
```

### 4단계: API 키 발급 (무료)

위 테이블에서 **아무거나 1개** 선택. Groq 추천 (가장 쉬움):

1. [console.groq.com/keys](https://console.groq.com/keys) 접속
2. 가입 후 API 키 생성
3. 키 복사

### 5단계: API 키 설정

1. `.env.example`을 복사하여 `.env`로 이름 변경
2. 메모장으로 `.env` 열기
3. 키 입력:

```
GROQ_API_KEY=gsk_여기에실제키입력
```

> **보안:** `.env` 파일은 자동으로 GitHub에서 제외됩니다. 절대 공유하지 마세요.

### 6단계: 앱 실행

```
streamlit run app.py
```

브라우저가 **http://localhost:6601** 을 자동으로 엽니다 — 완료!

---

## 사용 방법

### 처음 사용

1. 사이드바 **"수집"** 클릭 → 15개 소스에서 뉴스 수집
2. **"AI 처리"** 클릭 → 모든 기사 AI 분석
3. **"브리핑 생성"** 클릭 → 오늘의 TOP 5 생성

### 매일 사용

- **브리핑 탭** — 빠른 요약 + 감성 차트
- **뉴스 탭** — 필터로 관심 기사만, 중요한 건 북마크
- **검색 탭** — 특정 주제 검색
- **AI 채팅 탭** — "오늘 중요한 AI 뉴스 알려줘"
- **북마크 탭** — 저장한 기사에 메모 추가

### 기능 가이드

| 하고 싶은 것 | 방법 |
|-------------|------|
| 뉴스 소스 추가 | 사이드바 → 소스 관리 → 이름+RSS URL 입력 |
| 키워드 추적 | 사이드바 → 워치리스트 → 키워드 입력 |
| 기사 북마크 | 뉴스 탭 → 카드의 ☆ 클릭 |
| 메모 추가 | 북마크 탭 → 메모 필드에 입력 |
| 읽음 표시 | 뉴스 탭 → 카드의 📖 클릭 |
| 기사 검색 | 검색 탭 → 키워드 + 필터 선택 |
| AI에게 질문 | AI 채팅 탭 → 질문 입력 |
| 음성 브리핑 듣기 | 브리핑 탭 → 음성 선택 → "음성 생성" 클릭 |
| AI 용어 검색 | 용어 사전 탭 → 검색 또는 탐색 |
| 텔레그램 봇 사용 | `.env`에 `TELEGRAM_BOT_TOKEN` 설정 → `python -m bot.telegram_bot` 실행 |
| PDF 내보내기 | 브리핑/뉴스 탭 → PDF 선택 → 다운로드 |
| 다크/라이트 전환 | 사이드바 상단 토글 |
| LLM 변경 | `.env`에서 `LLM_PROVIDER=groq` 설정 |

---

## 프로젝트 구조

```
ai-news-radar/
├── app.py                  # 메인 대시보드 (8탭)
├── config.py               # 설정
├── requirements.txt        # 의존성 (10개 패키지)
├── .env.example            # API 키 템플릿 (35개 플랫폼 + 텔레그램)
├── LICENSE                 # MIT 라이선스 (SoDam AI Studio)
├── .streamlit/config.toml  # 테마 + 포트 설정
├── crawler/                # 뉴스 수집
├── ai/                     # AI 처리 (라우팅, 배치, 채팅, 음성, 팩트체크, 용어 사전)
├── bot/                    # 텔레그램 봇 (7개 명령어)
├── scripts/                # CLI 수집 스크립트 (cron/Actions용)
├── .github/workflows/      # GitHub Actions 자동 수집
├── reader/                 # 원문 리더
├── export/                 # Markdown/PDF 내보내기
├── data/                   # 프리셋 소스
├── utils/                  # 유틸리티
└── PRD/                    # 디자인 문서
```

---

## 문제 해결

| 문제 | 해결 |
|------|------|
| `pip` 못 찾음 | Python 재설치, "Add to PATH" 체크 |
| `streamlit` 못 찾음 | `pip install streamlit` 실행 |
| "LLM API 키 미설정" 경고 | `.env` 파일에 API 키 최소 1개 입력 |
| 기사 안 나옴 | "수집" 먼저 → "AI 처리" |
| 포트 사용 중 | `--server.port 6602` 옵션 사용 |
| PDF 실패 | Windows 전용 (한글 폰트 사용) |
| AI 분석 안 됨 | API 키 정확한지, 만료 안 됐는지 확인 |

---

## 로드맵

| Phase | 기능 | 상태 |
|-------|------|------|
| Phase 1 | 수집 + AI 요약 + 대시보드 (17개) | **완료** |
| Phase 2-A | 검색 + 북마크 + 읽은글 + 감성차트 + AI채팅 (5개) | **완료** |
| Phase 2-B | 음성 + 텔레그램봇 + 팩트체크 + 용어사전 + GitHub Actions (5개) | **완료** |
| Phase 3 | 에이전트 + 예측 + 팟캐스트 + 플러그인 + 팀 모드 | 예정 |

---

## 기술 스택

| 구성 | 기술 |
|------|------|
| 언어 | Python 3.11+ |
| 대시보드 | Streamlit 2026 |
| AI | 35개 LLM 플랫폼 (OpenAI, Gemini, Groq, Claude 등) |
| 차트 | Plotly (게이지, 도넛, 스택 바) |
| 데이터 | 로컬 JSON |
| 스케줄링 | APScheduler |
| PDF | fpdf2 (한글 지원) |
| 음성 | edge-tts (Microsoft TTS, 한국어) |
| 봇 | python-telegram-bot (텔레그램 연동) |
| CI/CD | GitHub Actions (하루 3회 자동 수집) |

---

## 라이선스

MIT License - Copyright (c) 2026 **SoDam AI Studio**

자세한 내용은 [LICENSE](./LICENSE) 참고.

---

*Streamlit + 35개 AI 플랫폼으로 만들었습니다 — SoDam AI Studio*
