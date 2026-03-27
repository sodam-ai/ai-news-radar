<div align="center">

# AI News Radar

**AI 뉴스를 자동으로 수집·분석·전달하는 개인용 뉴스 인텔리전스 플랫폼 — 74개 소스, 35개 LLM 지원**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLMs](https://img.shields.io/badge/LLM_플랫폼-35개-blueviolet)](#35개-llm-플랫폼)
[![Sources](https://img.shields.io/badge/뉴스_소스-74개-blue)](#74개-뉴스-소스)
[![Commits](https://img.shields.io/badge/커밋-37개-orange)](#)
[![License](https://img.shields.io/badge/라이선스-MIT-green)](./LICENSE)

**[English](./README.md) / Korean / [Japanese](./README_JA.md) / [Chinese](./README_ZH.md)**

</div>

---

## 이게 뭔가요?

AI 뉴스는 매시간 쏟아집니다. 새 모델 출시, 도구 업데이트, 논문 발표, 기업 동향 — 수십 개의 사이트에 흩어져 있습니다. **AI News Radar**는 이 소음을 없애줍니다. **74개 엄선된 소스**에서 뉴스를 지속적으로 수집하고, AI가 모든 기사를 요약·분류·중요도 평가·팩트체크한 다음, 깔끔하고 실용적인 브리핑으로 전달합니다.

**한 줄 요약:** 74개 사이트를 직접 방문하지 마세요. AI가 전부 읽고 중요한 것만 알려드립니다.

---

## 핵심 특징

- **50+ 기능** — 5개 탭 (대시보드 / 뉴스피드 / AI / 인사이트 / 공유)
- **74개 소스** — 일반 AI(26개) + 이미지·영상(20개) + 바이브코딩(19개) + 온톨로지(9개)
- **35개 LLM 플랫폼** — 대부분 무료, API 키 1개만 필요
- **9개 카테고리** — 도구, 연구, 트렌드, 튜토리얼, 비즈니스, 이미지·영상, 바이브코딩, 온톨로지, 기타
- **19개 AI 도구 추적** — 릴리즈 자동 감지
- **5개 SNS** — X, 텔레그램, 디스코드, 쓰레드, 인스타그램 + 카드뉴스 자동 생성
- **5종 콘텐츠** — 트윗, 쓰레드, 인스타 캡션, 블로그 포스트, LinkedIn 포스트
- **음성 브리핑**, AI 팩트체크, AI 용어사전, AI 토론
- **원클릭 풀 파이프라인** — 수집 > 분석 > 브리핑 > 릴리즈 감지
- **데스크톱 앱** — 시스템 트레이 + 백그라운드 알림
- **GitHub Actions** — 하루 3회 자동 수집
- **자동 한국어 번역** (영어 → 한국어)

---

## 주요 기능 (50+)

### 대시보드 탭

| 기능 | 설명 |
|------|------|
| 데일리 브리핑 | AI가 생성한 "오늘의 AI 뉴스 TOP 5" (중요도 순위 포함) |
| 포커스 브리핑 | 이미지·영상 / 바이브코딩 / 온톨로지 전용 브리핑 |
| 카테고리 퀵필터 | 9개 카테고리 원클릭 필터 |
| 감성 게이지 | 긍정/중립/부정 비율 Plotly 인터랙티브 차트 |
| 음성 브리핑 | edge-tts로 브리핑을 AI 음성으로 청취 |
| 주간 인텔리전스 리포트 | 트렌드·예측·분석이 담긴 자동 생성 주간 리포트 |
| 뉴스레터 | SMTP로 일간·주간 브리핑 이메일 발송 |

### 뉴스피드 탭

| 기능 | 설명 |
|------|------|
| 74개 소스 수집 | 15 워커 병렬 크롤링으로 빠른 집계 |
| AI 요약 | 모든 기사의 3줄 한국어 요약 |
| 9개 카테고리 분류 | AI 자동 카테고리 분류 |
| 중요도 점수 | 기사별 1–5점 중요도 평가 |
| 감성 분석 | 긍정 / 중립 / 부정 태깅 |
| AI 팩트체크 | 교차 검증 ("3개 매체 확인" vs "단독 소스") |
| 중복 기사 병합 | 동일 기사를 여러 매체에서 가져온 경우 자동 병합 |
| 키워드 관심 목록 | 추적 키워드 강조 표시 및 알림 |
| 인앱 리더 | 앱 내에서 전체 기사 읽기 (광고 없음) |
| 고급 검색 | 키워드·카테고리·감성·읽음 여부 필터 |
| 북마크 + 메모 | 개인 메모와 함께 기사 저장 |
| 페이지네이션 | 페이지당 10개 기사, 부드러운 이동 |
| 타임라인 뷰 | 오늘 / 어제 / 이번 주로 탐색 |
| 자동 한국어 번역 | 영어 기사 자동 한국어 번역 |

### AI 탭

| 기능 | 설명 |
|------|------|
| AI 뉴스 채팅 | 수집된 뉴스에 대해 자연어로 질문 |
| AI 용어사전 | 자동 추출 AI 용어 + 초보자 친화적 설명 |

### 인사이트 탭

| 기능 | 설명 |
|------|------|
| AI 도구 릴리즈 추적기 | 19개 AI 도구 자동 릴리즈 감지 |
| 트렌드 차트 | 일별 언급 빈도 Plotly 라인 차트 |
| 핫 키워드 | 전주 대비 상승률 기준 키워드 |
| AI 토론 | "Midjourney vs Flux" — 장단점·결론 AI 생성 |
| 주간 인텔리전스 리포트 | 심층 주간 분석 + 예측 |

### 공유 탭

| 기능 | 설명 |
|------|------|
| SNS 자동 게시 | X, 텔레그램, 디스코드, 쓰레드, 인스타그램에 포스팅 |
| 카드뉴스 생성기 | 1080×1080 카드 이미지 자동 생성 (다크 테마, 카테고리별 색상) |
| AI 콘텐츠 생성 | 트윗·쓰레드·인스타 캡션·블로그·LinkedIn 포스트 자동 생성 |
| 뉴스레터 이메일 | 구독자 목록에 포맷된 브리핑 발송 |
| 내보내기 | Markdown 또는 PDF 다운로드 |

### 시스템 기능

| 기능 | 설명 |
|------|------|
| 원클릭 풀 파이프라인 | 수집 > AI 처리 > 브리핑 > 릴리즈 감지를 한 번에 |
| 병렬 크롤링 | 15개 동시 워커로 빠른 수집 |
| 배치 병렬 처리 | 대량 기사 효율적인 AI 배치 처리 |
| 스마트 키워드 알림 | 감시 키워드 등장 시 데스크톱 알림 |
| 데스크톱 앱 | pywebview 네이티브 창 + 시스템 트레이 + 백그라운드 모드 |
| GitHub Actions | 하루 3회 자동 수집 (설정 가능) |
| 텔레그램 봇 | 7개 명령어로 어디서나 접근 |

---

## 74개 뉴스 소스

| 카테고리 | 수 | 예시 |
|----------|:--:|------|
| **일반 AI** | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites, Ars Technica |
| **이미지·영상** | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| **바이브코딩** | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| **온톨로지** | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35개 LLM 플랫폼

아래 플랫폼 중 **단 1개의 API 키**만 있으면 됩니다:

| 등급 | 플랫폼 |
|------|--------|
| **무료 (추천)** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **크레딧/저렴** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **프리미엄** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

> **팁:** Gemini와 Groq가 무료 할당량이 넉넉하고 설정이 가장 쉽습니다.

---

## 대시보드 구성 (5탭)

| 탭 | 내용 |
|----|------|
| **대시보드** | 데일리 브리핑, 포커스 브리핑, 카테고리 퀵필터, 감성 차트, 주간 리포트, 뉴스레터 |
| **뉴스피드** | 전체 뉴스, 고급 검색, 북마크, 타임라인 뷰, 페이지네이션 |
| **AI** | 뉴스 채팅, AI 용어사전 |
| **인사이트** | 릴리즈 추적기, 트렌드 차트, 핫 키워드, AI 토론, 주간 리포트 |
| **공유** | SNS 게시, AI 콘텐츠 생성, 카드뉴스, 뉴스레터, 내보내기 |

---

## 시작하기 — 7단계 설치 가이드

> **코딩 경험이 전혀 없어도 됩니다.** 각 단계를 차근차근 따라하세요.

### 1단계 — Python 설치

1. [python.org/downloads](https://www.python.org/downloads/) 접속
2. 노란색 **"Download Python"** 버튼 클릭
3. 다운로드된 파일 실행
4. **필수:** 설치 화면 아래쪽의 **"Add Python to PATH"** 체크박스 반드시 체크
5. **"Install Now"** 클릭

**설치 확인:** 터미널 열기 (`Win + R` → `cmd` 입력 → Enter) 후 실행:

```bash
python --version
```

`Python 3.11.x` 이상이 보이면 성공입니다.

### 2단계 — 프로젝트 다운로드

**방법 A: Git 사용 (추천)**

```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**방법 B: 직접 다운로드**

1. [GitHub 저장소](https://github.com/sodam-ai/ai-news-radar) 접속
2. 초록색 **"Code"** 버튼 → **"Download ZIP"** 클릭
3. 원하는 폴더에 ZIP 압축 해제
4. 해당 폴더에서 터미널 열기

### 3단계 — 가상환경 생성 (권장)

```bash
python -m venv venv
```

가상환경 활성화:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

터미널 앞에 `(venv)`가 표시되면 성공입니다.

### 4단계 — 패키지 설치

```bash
pip install -r requirements.txt
```

필요한 모든 패키지가 설치됩니다. 완료까지 1–2분 소요될 수 있습니다.

### 5단계 — 무료 API 키 발급

**아래 중 1개만 선택하세요.** 가장 빠른 설정은 **Groq** 추천:

1. [console.groq.com/keys](https://console.groq.com/keys) 접속
2. 구글 계정으로 회원가입 (10초)
3. **"Create API Key"** 클릭
4. 키 복사 (`gsk_`로 시작)

> 다른 무료 옵션: [Gemini](https://aistudio.google.com/apikey), [Cerebras](https://cloud.cerebras.ai/), [SambaNova](https://cloud.sambanova.ai/)

### 6단계 — API 키 설정

1. 프로젝트 폴더에서 `.env.example` 파일 찾기
2. 파일을 복사해서 이름을 `.env`로 변경
3. `.env`를 메모장 등 텍스트 편집기로 열기
4. API 키 입력:

```env
# 1개 이상 선택:
GROQ_API_KEY=gsk_실제키를여기에붙여넣기
# GEMINI_API_KEY=your_gemini_key
# OPENAI_API_KEY=sk-your_openai_key
```

5. 저장 후 닫기

> **보안 안내:** `.env` 파일은 `.gitignore`에 포함되어 GitHub에 절대 업로드되지 않습니다. 이 파일을 공개적으로 공유하지 마세요.

### 7단계 — 앱 실행

**웹 모드 (브라우저에서 열림):**

```bash
streamlit run app.py
```

브라우저에서 **http://localhost:6601** 자동 접속

**데스크톱 모드 (네이티브 창):**

```bash
python desktop.py
```

또는 Windows에서 **`AI_News_Radar.bat`** 더블클릭

### 첫 사용

1. 사이드바의 **"수집"** 클릭 — 74개 소스에서 뉴스 수집 (~1분 소요)
2. **"AI 처리"** 클릭 — AI가 모든 기사 분석·요약·분류
3. **"브리핑 생성"** 클릭 — 오늘의 TOP 5 브리핑 생성
4. 5개 탭을 탐색하며 모든 기능을 발견하세요!

---

## 사용 가이드

| 원하는 것 | 방법 |
|-----------|------|
| 오늘의 요약 읽기 | 대시보드 탭 > 브리핑 섹션 |
| 카테고리별 필터링 | 대시보드 탭 > 카테고리 퀵필터 클릭 |
| 특정 주제 검색 | 뉴스피드 탭 > 검색 뷰 > 키워드 입력 |
| AI에게 뉴스 질문 | AI 탭 > 채팅 뷰 > 질문 입력 |
| AI 용어 학습 | AI 탭 > 용어사전 뷰 > 탐색 또는 검색 |
| AI 도구 릴리즈 추적 | 인사이트 탭 > 릴리즈 추적기 |
| 트렌드 키워드 확인 | 인사이트 탭 > 트렌드 |
| AI 토론 실행 | 인사이트 탭 > AI 토론 > 도구 2개 선택 |
| SNS 콘텐츠 생성 | 공유 탭 > 콘텐츠 생성 > 기사 + 플랫폼 선택 |
| 소셜 미디어 게시 | 공유 탭 > SNS 게시 > 플랫폼 선택 > 게시 |
| 브리핑 듣기 | 대시보드 탭 > 목소리 선택 > "음성" 클릭 |
| PDF 내보내기 | 공유 탭 > 내보내기 뷰 |
| 기사 저장 | 뉴스피드 탭 > 기사의 북마크 아이콘 클릭 |
| 키워드 알림 설정 | 사이드바 > 관심 목록 > 키워드 입력 |
| 풀 파이프라인 실행 | 사이드바 > "원클릭 파이프라인" 버튼 |

---

## SNS 연동 가이드

| 플랫폼 | 설정 시간 | 난이도 | 가이드 |
|--------|:---------:|:------:|--------|
| 디스코드 | 30초 | 매우 쉬움 | 채널 설정에서 웹훅 URL 생성 |
| 텔레그램 | 2분 | 쉬움 | @BotFather로 봇 생성 |
| X (트위터) | 10분 | 중간 | 개발자 계정 신청 |
| 쓰레드 | 10분 | 중간 | Meta 개발자 포털 |
| 인스타그램 | 15분 | 복잡 | Instagram Graph API 설정 |

앱 내 **공유 탭 > SNS 게시** 섹션에서 단계별 상세 안내를 확인할 수 있습니다.

---

## 프로젝트 구조

```
ai-news-radar/
├── app.py                       # 메인 대시보드 (5탭)
├── desktop.py                   # 데스크톱 앱 (pywebview + 시스템 트레이)
├── config.py                    # 설정 (9개 카테고리, 포트, 경로)
├── requirements.txt             # 필요 패키지 목록
├── .env.example                 # API 키 템플릿
├── AI_News_Radar.bat            # Windows 실행기 (웹 모드)
├── AI_News_Radar_Silent.vbs     # 무음 실행기 (콘솔 창 없음)
│
├── ai/                          # AI 모듈 14개
│   ├── model_router.py          #   35개 LLM 프로바이더 라우팅
│   ├── briefing.py              #   일간+포커스 브리핑 생성
│   ├── chat.py                  #   자연어 뉴스 채팅
│   ├── voice_briefing.py        #   TTS 음성 출력 (edge-tts)
│   ├── factcheck.py             #   교차 소스 팩트 검증
│   ├── glossary.py              #   AI 용어사전
│   ├── weekly_report.py         #   주간 인텔리전스 리포트
│   ├── competitor.py            #   AI 도구 릴리즈 모니터링
│   ├── release_tracker.py       #   자동 릴리즈 감지
│   ├── trend.py                 #   키워드 트렌드 분석
│   ├── debate.py                #   AI 토론 모드
│   ├── smart_alert.py           #   데스크톱 키워드 알림
│   ├── translator.py            #   자동 한국어 번역
│   ├── deduplicator.py          #   중복 기사 병합
│   └── batch_processor.py       #   배치 병렬 처리
│
├── sns/                         # SNS·공유 모듈
│   ├── card_generator.py        #   1080×1080 카드뉴스 이미지 (Pillow)
│   ├── poster.py                #   5개 플랫폼 SNS 게시
│   ├── content_generator.py     #   AI 콘텐츠 (5종류)
│   └── newsletter.py            #   이메일 뉴스레터 (SMTP)
│
├── crawler/                     # 데이터 수집
│   ├── rss_crawler.py           #   RSS 크롤러 (15 병렬 워커)
│   └── scheduler.py             #   APScheduler 스케줄링
│
├── bot/                         # 텔레그램 연동
│   └── telegram_bot.py          #   텔레그램 봇 (7개 명령어)
│
├── reader/                      # 기사 읽기
│   └── article_reader.py        #   인앱 기사 리더 (광고 없음)
│
├── export/                      # 데이터 내보내기
│   └── exporter.py              #   Markdown + PDF 내보내기
│
├── utils/                       # 공유 유틸리티
│   └── helpers.py               #   공통 헬퍼 함수
│
├── scripts/                     # CLI 도구
│   ├── collect.py               #   독립 수집 스크립트
│   └── reclassify.py            #   카테고리 재분류 도구
│
├── data/                        # 로컬 데이터 저장소
│   ├── preset_sources.json      #   74개 소스 정의
│   ├── sources.json             #   활성 소스 설정
│   ├── articles.json            #   수집된 기사
│   ├── briefings.json           #   생성된 브리핑
│   ├── weekly_reports.json      #   주간 리포트 아카이브
│   ├── release_log.json         #   도구 릴리즈 이력
│   ├── audio/                   #   음성 브리핑 오디오 파일
│   └── cards/                   #   생성된 카드뉴스 이미지
│
├── .github/workflows/
│   └── collect.yml              #   GitHub Actions (하루 3회 자동 수집)
│
└── PRD/                         #   제품 설계 문서
```

**8개 디렉토리에 24개 모듈** — **37개 커밋** 진행 중.

---

## 기술 스택

| 컴포넌트 | 기술 |
|----------|------|
| **언어** | Python 3.11+ |
| **대시보드** | Streamlit 1.44+ |
| **AI 엔진** | 통합 모델 라우터를 통한 35개 LLM 플랫폼 |
| **차트** | Plotly (인터랙티브 트렌드 차트, 감성 게이지) |
| **음성** | edge-tts (Microsoft 신경망 TTS) |
| **이미지 생성** | Pillow (다크 테마 카드뉴스) |
| **데스크톱** | pywebview + pystray (네이티브 창 + 시스템 트레이) |
| **알림** | plyer (크로스 플랫폼 데스크톱 알림) |
| **RSS 파싱** | feedparser (74개 소스 피드) |
| **웹 스크래핑** | BeautifulSoup4 + requests |
| **텔레그램 봇** | python-telegram-bot |
| **SNS API** | tweepy (X), Telegram API, Discord Webhook, Threads API, Instagram Graph API |
| **이메일** | smtplib (SMTP 뉴스레터) |
| **PDF 내보내기** | fpdf2 (한국어 폰트 지원) |
| **스케줄링** | APScheduler (인앱), GitHub Actions (CI/CD) |
| **데이터 저장** | 로컬 JSON (데이터베이스 설정 불필요) |

---

## 문제 해결

| 문제 | 해결 방법 |
|------|-----------|
| `python` 명령어 없음 | **"Add to PATH"** 체크 후 Python 재설치 |
| `pip` 명령어 없음 | `python -m pip install -r requirements.txt` 사용 |
| `streamlit` 없음 | `pip install streamlit` 실행, 가상환경 활성화 확인 |
| "API 키 미설정" 경고 | `.env` 파일에 API 키 1개 이상 입력 (6단계 참고) |
| 기사가 나타나지 않음 | **"수집"** 후 **"AI 처리"** 순서로 클릭 |
| 카테고리에 기사 0개 | `python scripts/reclassify.py` 실행 |
| 포트 6601 이미 사용 중 | `streamlit run app.py --server.port 7777` |
| macOS/Linux에서 PDF 내보내기 실패 | `NanumGothic` 폰트 설치 |
| 데스크톱 모드 실행 안 됨 | `pip install pywebview` 설치 확인 |
| 수집이 느림 | 정상 — 74개 소스 15 병렬 워커로 약 60초 소요 |
| edge-tts 음성 오류 | 인터넷 연결 확인 (edge-tts는 온라인 필요) |

---

## 로드맵

| 단계 | 기능 | 상태 |
|------|------|:----:|
| **Phase 1** | 수집 + AI 요약 + 대시보드 (17기능) | ✅ 완료 |
| **Phase 2-A** | 검색 + 북마크 + 감성 + 채팅 (5기능) | ✅ 완료 |
| **Phase 2-B** | 음성 + 텔레그램 + 팩트체크 + 용어사전 + Actions (5기능) | ✅ 완료 |
| **Tier 1** | 포커스 브리핑 + 주간 리포트 + 릴리즈 추적기 (3기능) | ✅ 완료 |
| **Tier 2** | 트렌드 차트 + AI 토론 + 핫 키워드 (3기능) | ✅ 완료 |
| **S-Tier** | 스마트 알림 + 콘텐츠 생성 + 뉴스레터 + SNS (4기능) | ✅ 완료 |
| **UI/UX** | 5탭 리디자인 + 페이지네이션 + 카테고리 퀵필터 + 프리미엄 CSS | ✅ 완료 |
| **데스크톱** | pywebview + 시스템 트레이 + 백그라운드 알림 | ✅ 완료 |
| **파이프라인** | 원클릭 풀 파이프라인 + 병렬 크롤링 + 배치 처리 | ✅ 완료 |
| **번역** | 자동 한국어 번역 + 중복 제거 | ✅ 완료 |
| **다음** | ChromaDB 벡터 검색, Ollama 로컬 LLM, 게이미피케이션, 모바일 PWA | 📋 예정 |

---

## 기여

풀 리퀘스트는 환영합니다!

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 열기

---

## 라이선스

MIT 라이선스 — Copyright (c) 2026 **SoDam AI Studio**

자세한 내용은 [LICENSE](./LICENSE) 참조.

---

<div align="center">

*Streamlit + 35개 AI 플랫폼으로 제작 — SoDam AI Studio*

</div>
