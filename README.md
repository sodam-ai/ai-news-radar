# 📡 AI News Radar

<p align="center">
  <img src="assets/icon.png" width="80" alt="AI News Radar 아이콘" />
</p>

<p align="center">
  <strong>나만의 AI 뉴스 인텔리전스 플랫폼</strong><br/>
  74개 소스에서 AI 뉴스를 자동 수집·요약·분석하는 개인용 대시보드
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
  <img src="https://img.shields.io/badge/Release-v1.5.0-blue" alt="Release"/>
  <img src="https://img.shields.io/badge/Streamlit-1.44%2B-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/LLM-35개_프로바이더-purple" alt="LLM"/>
  <img src="https://img.shields.io/badge/벡터검색-ChromaDB-orange" alt="ChromaDB"/>
</p>

<p align="center">
  <a href="README.md">한국어</a> |
  <a href="README_EN.md">English</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_ZH.md">中文</a>
</p>

---

## AI News Radar가 뭔가요?

**코딩을 한 번도 안 해봐도** 사용할 수 있는 AI 뉴스 도구입니다.

- 📰 **74개 AI 뉴스 소스**에서 자동으로 최신 뉴스를 수집합니다
- 🤖 **AI가 자동으로 요약·분류·중요도 평가**를 해줍니다
- 📋 **매일 TOP 5 브리핑**을 자동으로 만들어 줍니다
- 💬 **"이번 주 Claude 관련 뉴스 알려줘"** — AI에게 자연어로 질문하세요
- 🔍 **시맨틱 검색** — 의미 기반 AI 검색 (단어가 정확히 안 맞아도 관련 기사 찾기)
- ⭐ **북마크 + 메모** — 중요한 기사를 저장하고 메모합니다
- 📱 **텔레그램 봇** — 앱을 안 켜도 중요 뉴스가 텔레그램으로 옵니다
- 📊 **트렌드·경쟁사 분석** — AI 업계 흐름을 차트로 한눈에 파악합니다

> 내 컴퓨터에서만 실행되는 **완전 로컬** 앱입니다. 데이터가 외부로 나가지 않습니다.

---

## 빠른 시작 (코딩 경험 없어도 OK)

### 1단계: Python 설치

이미 Python이 설치되어 있다면 2단계로 건너뛰세요.

1. 브라우저에서 **[python.org/downloads](https://www.python.org/downloads/)** 접속
2. 노란 **"Download Python 3.xx"** 버튼 클릭
3. 다운로드된 파일 실행
4. **반드시 체크 필수**: 설치 화면 맨 아래 **"Add Python to PATH"** 체크박스를 반드시 체크하세요!
5. **"Install Now"** 클릭 → 완료되면 "Close"

### 2단계: 프로그램 다운로드

**방법 A — GitHub Releases (권장):**
1. [Releases 페이지](https://github.com/sodam-ai/ai-news-radar/releases) 접속
2. **`Source code (zip)`** 다운로드
3. ZIP 파일 우클릭 → "모두 압축 풀기" → 폴더 선택 → "압축 풀기"

**방법 B — 이 페이지에서:**
1. 상단 초록색 **"Code"** 버튼 클릭
2. **"Download ZIP"** 클릭
3. ZIP을 원하는 폴더에 압축 해제

### 3단계: 무료 API 키 발급 (30초)

AI News Radar는 AI로 뉴스를 분석합니다. 무료 API 키가 필요합니다.

1. **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)** 접속
2. Google 계정으로 로그인
3. **"Create API Key"** 클릭
4. 키를 복사 (`AIzaSy...` 형태)

> **정말 무료인가요?** 네! Google이 하루 1,000회 무료 제공합니다. 개인 뉴스 추적에는 충분합니다. 신용카드 불필요.

### 4단계: 설정 파일 만들기

다운로드한 폴더 안에서:

1. `.env.example` 파일을 찾아 복사
2. 복사한 파일 이름을 `.env` 로 변경
3. 메모장으로 `.env` 열기
4. `GEMINI_API_KEY=` 뒤에 복사한 API 키 붙여넣기

```
GEMINI_API_KEY=AIzaSy여기에붙여넣기
```

저장하고 닫기.

### 5단계: 실행

**더블클릭으로 실행:**
- `AI_News_Radar.exe` 파일을 더블클릭하면 자동으로 설치 후 실행됩니다
- 처음 실행 시 패키지 설치로 2~3분 걸릴 수 있습니다
- 실행되면 자동으로 브라우저에서 `http://localhost:6601` 이 열립니다

**또는 bat 파일로 실행:**
- `AI_News_Radar.bat` 더블클릭

---

## 주요 기능 전체 목록

| 기능 | 설명 |
|------|------|
| 📡 자동 수집 | 74개 RSS 소스 병렬 수집 (15개 스레드) |
| 🤖 AI 배치 처리 | 요약·분류·중요도·감성·키워드 한 번에 |
| 🔍 시맨틱 검색 | ChromaDB + ONNX 로컬 임베딩 (v1.3.0 신규) |
| 💬 AI 채팅 | 수집된 뉴스로 자연어 대화 |
| 📋 일일 브리핑 | TOP 5 자동 생성 |
| 📊 주간 리포트 | 트렌드·예측 PDF 자동 생성 |
| ⭐ 북마크+메모 | 기사 저장 및 메모 |
| 🔔 스마트 알림 | 워치리스트 키워드 감지 시 알림 |
| 📱 텔레그램 봇 | `/today`, `/ask`, `/alert`, `/bookmark` |
| 🌐 번역 | AI 영→한 자동 번역 |
| 🎙️ 음성 브리핑 | edge-tts AI 음성으로 읽어주기 |
| 📈 트렌드 차트 | 키워드별 시계열 언급량 분석 |
| 🏢 경쟁사 모니터링 | AI 기업·제품 추적 |
| ✅ 팩트체크 배지 | 보도 매체 수 기반 신뢰도 |
| 🗣️ 디베이트 모드 | AI가 찬성/반대 시각 자동 생성 |
| 📚 AI 용어 사전 | 뉴스 속 전문용어 자동 추출·설명 |
| 🚀 릴리즈 트래커 | AI 도구 새 버전 자동 감지 |
| 📤 내보내기 | Markdown·PDF |
| 📲 SNS 카드 | 뉴스 카드 자동 생성 |
| 🤖 35개 LLM | Gemini, Claude, GPT, Groq 등 자동 전환 |

---

## 환경 변수 설정 (.env)

`.env` 파일에서 설정합니다. 필수 항목 하나만 설정해도 동작합니다.

```env
# ── 필수 (하나만 있으면 됩니다) ──────────────────────
GEMINI_API_KEY=AIzaSy...          # Google AI Studio (무료 1000회/일)

# ── 선택: 다른 LLM 프로바이더 ────────────────────────
GROQ_API_KEY=gsk_...              # Groq (무료 14400회/일, 초고속)
OPENAI_API_KEY=sk-...             # OpenAI GPT
ANTHROPIC_API_KEY=sk-ant-...      # Anthropic Claude

# ── 선택: 텔레그램 봇 ────────────────────────────────
TELEGRAM_BOT_TOKEN=123456:ABC...  # @BotFather에서 발급
TELEGRAM_CHAT_ID=123456789        # @userinfobot에서 확인

# ── 선택: 수집 주기 ──────────────────────────────────
CRAWL_INTERVAL_MINUTES=60         # 기본값: 60분마다 자동 수집
```

> **보안 주의**: `.env` 파일은 절대 GitHub에 올리면 안 됩니다. `.gitignore`에 이미 등록되어 있어 자동으로 제외됩니다.

---

## 텔레그램 봇 설정 방법

1. 텔레그램에서 **@BotFather** 검색
2. `/newbot` 입력 → 봇 이름 설정 → 토큰 복사
3. `.env`에 `TELEGRAM_BOT_TOKEN=발급받은토큰` 입력
4. 텔레그램에서 **@userinfobot** 검색 → `/start` → 숫자 ID 복사
5. `.env`에 `TELEGRAM_CHAT_ID=숫자ID` 입력
6. 터미널에서: `python -m bot.telegram_bot`

**봇 명령어:**
| 명령어 | 설명 |
|--------|------|
| `/today` | 오늘의 AI 브리핑 |
| `/top` | 중요도 TOP 5 뉴스 |
| `/search 키워드` | 뉴스 검색 |
| `/ask 질문` | AI에게 뉴스 질문 |
| `/alert` | 워치리스트 조회 |
| `/alert 키워드` | 워치리스트 추가 |
| `/bookmark` | 북마크 기사 목록 |
| `/stats` | 수집 통계 |

---

## 시맨틱 검색 초기 설정 (v1.3.0 신규)

처음 실행 후 사이드바에서 **"🧠 벡터 동기화"** 버튼을 한 번 클릭하세요.  
기존에 수집된 기사들이 AI 검색 DB에 등록됩니다. (이후에는 자동)

---

## 폴더 구조

```
ai-news-radar/
├── app.py                  # 메인 Streamlit 대시보드 (1400줄)
├── config.py               # 설정 (포트, 카테고리, API 키 로드)
├── requirements.txt        # 필요 패키지 목록
├── .env                    # API 키 설정 (직접 생성, GitHub에 올리지 마세요)
├── .env.example            # 환경 변수 예시 파일
│
├── ai/                     # AI 처리 모듈
│   ├── model_router.py     # 35개 LLM 멀티 프로바이더 라우팅
│   ├── batch_processor.py  # 기사 일괄 AI 분석
│   ├── vector_store.py     # ChromaDB 시맨틱 검색 (v1.3.0)
│   ├── chat.py             # AI 뉴스 채팅
│   ├── briefing.py         # 일일 브리핑 생성
│   ├── weekly_report.py    # 주간 리포트
│   ├── trend.py            # 트렌드 분석
│   ├── competitor.py       # 경쟁사 모니터링
│   ├── smart_alert.py      # 스마트 알림 (텔레그램 연동)
│   ├── factcheck.py        # 팩트체크 배지
│   ├── debate.py           # 디베이트 모드
│   ├── glossary.py         # AI 용어 사전
│   ├── release_tracker.py  # 릴리즈 감지
│   ├── translator.py       # 영→한 자동 번역
│   ├── voice_briefing.py   # 음성 브리핑
│   └── deduplicator.py     # 중복 뉴스 병합
│
├── crawler/                # 뉴스 수집
│   ├── rss_crawler.py      # RSS 멀티스레드 수집 (74개 소스)
│   └── scheduler.py        # 자동 수집 스케줄러
│
├── bot/                    # 텔레그램 봇
│   └── telegram_bot.py     # 봇 명령어 처리
│
├── sns/                    # 소셜 미디어
│   ├── card_generator.py   # 뉴스 카드 생성
│   ├── content_generator.py
│   ├── newsletter.py       # 이메일 뉴스레터
│   └── poster.py           # 소셜 포스팅
│
├── reader/                 # 아티클 리더
│   └── article_reader.py   # 원문 클린 뷰
│
├── export/                 # 내보내기
│   └── exporter.py         # Markdown/PDF 내보내기
│
├── utils/                  # 공통 유틸
│   ├── helpers.py          # JSON 읽기/쓰기, 로그 등
│   └── bookmarks.py        # 북마크 관리 (v1.3.0)
│
└── data/                   # 런타임 데이터 (자동 생성, Git 제외)
    ├── articles.json        # 수집된 기사
    ├── sources.json         # 등록된 소스
    ├── briefings.json       # 생성된 브리핑
    ├── chroma/              # 벡터 검색 DB
    └── audio/               # 음성 브리핑 파일
```

---

## 운영 시 주의사항

| 항목 | 내용 |
|------|------|
| **API 키** | `.env` 파일에만 보관. 절대 GitHub, 카카오톡, 이메일로 공유 금지 |
| **API 한도** | Gemini Flash 무료: 250회/일. 초과 시 Groq 등 다른 프로바이더 자동 전환 |
| **data/ 폴더** | 기사가 쌓이면 용량이 커질 수 있습니다. 주기적으로 정리 권장 |
| **포트 충돌** | `6601` 포트를 다른 프로그램이 사용 중이면 `.env`에서 변경 가능 |
| **벡터 동기화** | `data/chroma/` 삭제 후 재동기화하면 초기화됩니다 |
| **텔레그램 알림** | `.env`에 `TELEGRAM_CHAT_ID` 없으면 데스크톱 알림만 작동 |

---

## 버전 히스토리

| 버전 | 주요 변경 |
|------|----------|
| v1.3.0 | ChromaDB 시맨틱 검색, 텔레그램 봇 고도화(`/alert`, `/bookmark`), 스마트 알림 텔레그램 연동 |
| v1.2.1 | 멀티 LLM 35개 프로바이더 지원 확장 |
| v1.2.0 | 경량 exe 런처 (7.8MB), 다중 해상도 아이콘 |
| v1.0.0 | MVP 출시 — 수집·요약·분류·브리핑·채팅 |

---

## 라이선스

MIT License © 2026 [SoDam AI Studio](https://github.com/sodam-ai)

자유롭게 사용, 수정, 배포 가능합니다.  
상업적 이용 시 원 저작자 표기를 유지해 주세요.
