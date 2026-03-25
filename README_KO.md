<p align="center">
  <h1 align="center">AI News Radar</h1>
  <p align="center">
    <strong>AI 뉴스를 자동으로 수집 · 요약 · 분류하는 올인원 뉴스 인텔리전스 대시보드</strong><br/>
    74개 소스 · 35개 LLM · 50+ 기능 · 5개 SNS · 데스크톱 앱
  </p>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License" /></a>
  <img src="https://img.shields.io/badge/python-3.11+-3776AB.svg?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/streamlit-1.44+-FF4B4B.svg?logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/LLM-35%20platforms-8A2BE2" alt="LLM" />
  <img src="https://img.shields.io/badge/sources-74-green" alt="Sources" />
  <img src="https://img.shields.io/badge/commits-36-orange" alt="Commits" />
</p>

**[English](./README.md) / Korean / [Japanese](./README_JA.md) / [Chinese](./README_ZH.md)**

---

## 목차

- [이게 뭔가요?](#이게-뭔가요)
- [주요 기능 50+](#주요-기능-50)
- [74개 뉴스 소스](#74개-뉴스-소스)
- [35개 LLM 플랫폼](#35개-llm-플랫폼)
- [대시보드 구성 (5탭)](#대시보드-구성-5탭)
- [시작하기 — 7단계 설치 가이드](#시작하기--7단계-설치-가이드)
- [사용 가이드](#사용-가이드)
- [SNS 연동 가이드](#sns-연동-가이드)
- [프로젝트 구조](#프로젝트-구조)
- [기술 스택](#기술-스택)
- [문제 해결](#문제-해결)
- [로드맵](#로드맵)
- [라이선스](#라이선스)

---

## 이게 뭔가요?

AI News Radar는 전 세계 **74개 AI 뉴스 소스**에서 기사를 **자동으로 수집**하고, **35개 LLM 플랫폼** 중 원하는 것으로 **요약 · 분류 · 중요도 평가 · 팩트체크**까지 처리하는 **개인용 AI 뉴스 인텔리전스 대시보드**입니다.

**쉽게 말하면:** 매일 수십 개 AI 뉴스 사이트를 돌아다니는 대신, 이 앱이 전부 대신 해주고 중요한 것만 보여줍니다.

**핵심 가치:**

- **시간 절약** — 74개 소스를 원클릭으로 수집, AI가 자동 분석
- **무료 사용** — 35개 LLM 중 14개가 완전 무료 (API 키 1개만 필요)
- **완전 자동화** — GitHub Actions로 하루 3회 자동 수집, 병렬 크롤링
- **멀티플랫폼** — 웹 브라우저 + 네이티브 데스크톱 앱 동시 지원
- **SNS 연동** — 5개 플랫폼에 카드뉴스 자동 게시 + AI 콘텐츠 생성

---

## 주요 기능 (50+)

### 대시보드 탭

| # | 기능 | 설명 |
|---|------|------|
| 1 | 오늘의 브리핑 | AI가 매일 "오늘의 AI 뉴스 TOP 5" 자동 생성 |
| 2 | 관심 분야 브리핑 | 이미지/영상, 바이브코딩, 온톨로지 분야별 맞춤 브리핑 |
| 3 | 카테고리 퀵필터 | 9개 카테고리 클릭 한 번에 필터링 (건수 실시간 표시) |
| 4 | 감성 온도계 | 긍정/중립/부정 비율 Plotly 인터랙티브 차트 |
| 5 | 음성 브리핑 | 브리핑을 한국어 AI 음성으로 듣기 (여성/남성 선택) |
| 6 | 주간 인텔리전스 리포트 | 핵심 트렌드 + 분야별 동향 + 전망 자동 생성 |
| 7 | 뉴스레터 이메일 발송 | 일간/주간 브리핑을 이메일로 자동 발송 (SMTP) |

### 뉴스피드 탭

| # | 기능 | 설명 |
|---|------|------|
| 8 | 74개 소스 수집 | 전 세계 74개 RSS 소스에서 병렬 자동 수집 |
| 9 | AI 요약 | 각 기사를 한국어 3줄로 자동 요약 |
| 10 | 자동 한국어 번역 | 영문 기사 제목 + 본문 자동 번역 |
| 11 | 9개 카테고리 자동분류 | 도구 / 연구 / 트렌드 / 튜토리얼 / 비즈니스 / 이미지영상 / 바이브코딩 / 온톨로지 / 기타 |
| 12 | 중요도 점수 | 1~5성 자동 평가 |
| 13 | 감성 분석 | 긍정 / 중립 / 부정 자동 태깅 |
| 14 | AI 팩트체크 | 교차 검증 배지 ("3개 매체 확인" vs "단독 보도") |
| 15 | 중복 기사 병합 | 같은 뉴스 자동 합침 (유사도 기반) |
| 16 | 키워드 워치리스트 | 추적 키워드 포함 기사 하이라이트 |
| 17 | 인앱 리더 | 앱 내에서 원문 읽기 (광고 없음) |
| 18 | 검색 + 필터 | 키워드 + 카테고리 + 감성 + 읽음 상태 복합 필터 |
| 19 | 북마크 + 메모 | 중요 기사 저장 + 개인 메모 추가 |
| 20 | 페이지네이션 | 10개씩 페이지 넘김 (대량 기사 대응) |
| 21 | 타임라인 뷰 | 오늘 / 어제 / 이번 주 기간별 탐색 |

### AI 탭

| # | 기능 | 설명 |
|---|------|------|
| 22 | AI 채팅 | 수집된 뉴스에 대해 자연어로 질문하고 답변 |
| 23 | AI 용어 사전 | 뉴스 속 전문 용어를 초보자도 이해할 수 있게 설명 |
| 24 | AI 토론 | "Midjourney vs Flux" — AI가 찬반 근거 + 결론 생성 |
| 25 | AI 콘텐츠 자동생성 | 트윗 / 쓰레드 / 인스타 캡션 / 블로그 / LinkedIn 5종 |

### 인사이트 탭

| # | 기능 | 설명 |
|---|------|------|
| 26 | 도구 비교 차트 | 19개 AI 도구 뉴스 언급량 + 감성 비교 |
| 27 | 트렌드 차트 | 키워드별 시계열 언급량 인터랙티브 차트 |
| 28 | 급상승 키워드 | 전주 대비 상승률 기반 핫 키워드 |
| 29 | 릴리즈 추적 | 19개 AI 도구 신규 릴리즈 자동 감지 |
| 30 | 주간 리포트 | 핵심 트렌드 + 분야별 동향 + 전망 |

### 공유 탭

| # | 기능 | 설명 |
|---|------|------|
| 31 | SNS 자동 게시 | X / Telegram / Discord / Threads / Instagram 5개 플랫폼 |
| 32 | 카드뉴스 생성 | 1080x1080 카드 이미지 자동 생성 (카테고리별 컬러) |
| 33 | 내보내기 | Markdown / PDF 다운로드 |

### 시스템 + 자동화

| # | 기능 | 설명 |
|---|------|------|
| 34 | 원클릭 파이프라인 | 수집 > AI 처리 > 브리핑 한 번에 실행 |
| 35 | 병렬 크롤링 | 74개 소스 동시 수집 (속도 극대화) |
| 36 | 배치 병렬 처리 | 대량 기사 AI 분석 동시 처리 |
| 37 | GitHub Actions | 하루 3회 자동 수집 (06:00 / 12:00 / 18:00 KST) |
| 38 | 데스크톱 앱 | pywebview 네이티브 윈도우 + 시스템 트레이 |
| 39 | 스마트 알림 | 워치리스트 키워드 감지 시 데스크톱 알림 |
| 40 | Telegram 봇 | 7개 명령어로 텔레그램에서 바로 사용 |

> 이외에도 10개 이상의 세부 기능이 포함되어 있습니다.

---

## 74개 뉴스 소스

| 분류 | 개수 | 주요 소스 |
|------|------|-----------|
| **일반 AI** | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ars Technica, Ben's Bites, VentureBeat, The Decoder |
| **AI 이미지/영상** | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui, deforum) |
| **바이브코딩** | 19 | Cursor, GitHub Blog, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor, CopilotAI) |
| **온톨로지** | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs, ontology) |

---

## 35개 LLM 플랫폼

**API 키 1개만 있으면 됩니다.** 아래 중 아무 플랫폼이나 하나 선택하세요.

| 등급 | 플랫폼 |
|------|--------|
| **무료 (추천)** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **크레딧 / 저렴** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **프리미엄** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

---

## 대시보드 구성 (5탭)

| 탭 | 포함 기능 |
|----|-----------|
| **대시보드** | 오늘의 브리핑 + 관심 분야 브리핑 + 카테고리 퀵필터 + 감성 차트 + 음성 브리핑 + 주간 리포트 + 뉴스레터 |
| **뉴스피드** | 전체 뉴스 / 검색 / 북마크 / 타임라인 (라디오 버튼으로 전환) |
| **AI** | AI 채팅 / AI 용어 사전 |
| **인사이트** | 도구 비교 / 트렌드 차트 / AI 토론 / 주간 리포트 / 릴리즈 추적 |
| **공유** | SNS 게시 / AI 콘텐츠 생성 / 카드뉴스 / 내보내기 |

---

## 시작하기 — 7단계 설치 가이드

> **코딩 경험이 전혀 없어도 됩니다.** 아래를 차근차근 따라하면 10분 안에 실행할 수 있습니다.

### 1단계: Python 설치

1. [python.org/downloads](https://www.python.org/downloads/) 에 접속합니다
2. 큰 노란색 **"Download Python"** 버튼을 클릭합니다
3. 다운로드된 파일을 실행합니다
4. **반드시** 하단의 **"Add Python to PATH"** 를 체크합니다
5. **"Install Now"** 를 클릭합니다

**설치 확인:** 명령 프롬프트를 열어서 확인합니다.
```
Win + R → cmd 입력 → Enter
```
```bash
python --version
# Python 3.13.x 같은 버전이 나오면 성공
```

### 2단계: 프로젝트 다운로드

**방법 A: Git 사용 (추천)**
```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**방법 B: ZIP 직접 다운로드**
1. [GitHub 저장소](https://github.com/sodam-ai/ai-news-radar) 에 접속합니다
2. 초록색 **"Code"** 버튼 > **"Download ZIP"** 을 클릭합니다
3. ZIP 파일 압축을 해제합니다
4. 해제된 폴더를 열어둡니다

### 3단계: 패키지 설치

프로젝트 폴더에서 명령 프롬프트를 열고 아래 명령어를 입력합니다:
```bash
pip install -r requirements.txt
```
16개 패키지가 자동 설치됩니다. 완료될 때까지 기다려 주세요 (약 1~3분).

### 4단계: API 키 발급 (무료)

35개 플랫폼 중 아무거나 1개만 선택하면 됩니다. **Groq** 이 가장 쉽습니다:

1. [console.groq.com/keys](https://console.groq.com/keys) 에 접속합니다
2. Google 계정으로 가입합니다
3. **"Create API Key"** 를 클릭합니다
4. 생성된 키를 복사합니다 (`gsk_`로 시작)

> **다른 무료 옵션:** [Gemini](https://aistudio.google.com/apikey) (Google 계정), [Cerebras](https://cloud.cerebras.ai/) (가장 빠름), [SambaNova](https://cloud.sambanova.ai/) (대용량)

### 5단계: API 키 설정

1. 프로젝트 폴더에서 `.env.example` 파일을 찾습니다
2. 이 파일을 복사해서 이름을 `.env`로 변경합니다
3. `.env` 파일을 메모장으로 열어 키를 입력합니다:
```dotenv
# Groq를 선택한 경우
GROQ_API_KEY=gsk_여기에실제키입력

# Gemini를 선택한 경우
GEMINI_API_KEY=여기에실제키입력
```
4. 저장(`Ctrl + S`)하고 닫습니다

> **보안 안내:** `.env` 파일은 `.gitignore`에 의해 GitHub에 자동 제외됩니다. 이 파일을 절대 타인과 공유하지 마세요.

### 6단계: 앱 실행

**웹 모드 (브라우저에서 사용):**
```bash
streamlit run app.py
```
브라우저가 자동으로 **http://localhost:6601** 을 엽니다.

**데스크톱 모드 (네이티브 윈도우):**
```bash
python desktop.py
```
또는 `AI_News_Radar.bat` 파일을 더블클릭합니다.

### 7단계: 첫 번째 사용

1. 사이드바에서 **"수집"** 클릭 — 74개 소스에서 뉴스를 가져옵니다
2. **"AI 처리"** 클릭 — 모든 기사를 AI가 요약 + 분류 + 감성 분석합니다
3. **"브리핑 생성"** 클릭 — 오늘의 AI 뉴스 TOP 5가 만들어집니다
4. 대시보드에서 카테고리별로 자유롭게 탐색하세요!

> **팁:** 원클릭 파이프라인을 사용하면 위 3단계를 한 번에 실행할 수 있습니다.

---

## 사용 가이드

| 하고 싶은 것 | 방법 |
|-------------|------|
| 오늘의 요약 보기 | 대시보드 탭 > 브리핑 섹션 |
| 이미지/영상 뉴스만 보기 | 대시보드 탭 > "AI 이미지/영상" 카테고리 클릭 |
| 바이브코딩 뉴스만 보기 | 대시보드 탭 > "바이브코딩/AI코딩" 카테고리 클릭 |
| 특정 주제 검색 | 뉴스피드 탭 > 검색 뷰 > 키워드 입력 |
| AI에게 질문 | AI 탭 > 채팅 뷰 > 질문 입력 |
| AI 용어 확인 | AI 탭 > 용어 사전 뷰 |
| AI 도구 비교 | 인사이트 탭 > 도구 비교 |
| 트렌드 확인 | 인사이트 탭 > 트렌드 차트 |
| AI 토론 시작 | 인사이트 탭 > AI 토론 > 주제 입력 |
| SNS 콘텐츠 생성 | 공유 탭 > 콘텐츠 생성 > 기사 + 플랫폼 선택 |
| SNS에 게시 | 공유 탭 > SNS 게시 > 플랫폼 선택 > 게시 |
| 음성으로 듣기 | 대시보드 탭 > 음성 선택 (여성/남성) > "음성" 클릭 |
| PDF로 내보내기 | 공유 탭 > 내보내기 > PDF 다운로드 |
| 기사 저장 | 뉴스피드 탭 > 기사의 별표 클릭 |
| 메모 추가 | 뉴스피드 탭 > 북마크 뷰 > 메모 입력 |
| 키워드 추적 | 사이드바 > 워치리스트 > 키워드 입력 |
| 주간 리포트 생성 | 인사이트 탭 > 주간 리포트 |
| 뉴스레터 발송 | 대시보드 탭 > 뉴스레터 > 이메일 입력 > 발송 |

---

## SNS 연동 가이드

| 플랫폼 | 소요 시간 | 난이도 | 필요한 것 |
|--------|----------|--------|-----------|
| Discord | 30초 | 매우 쉬움 | Webhook URL |
| Telegram | 2분 | 쉬움 | Bot Token + Chat ID |
| X (Twitter) | 10분 | 보통 | API Key + Secret + Access Token |
| Threads | 10분 | 보통 | Meta Developer 앱 |
| Instagram | 15분 | 어려움 | Meta Business 계정 + Graph API |

> 각 플랫폼의 상세 설정 방법은 **공유 탭 > SNS 게시** 섹션에서 확인할 수 있습니다.

---

## 프로젝트 구조

```
ai-news-radar/                       # 루트 (24개 모듈, 36커밋)
├── app.py                           # 메인 대시보드 (5탭 UI)
├── desktop.py                       # 데스크톱 앱 (pywebview + 트레이)
├── config.py                        # 설정 (9카테고리, 포트, LLM)
├── requirements.txt                 # 16개 패키지
├── AI_News_Radar.bat                # 원클릭 실행 (데스크톱)
├── AI_News_Radar_Silent.vbs         # 무음 실행
├── AI_News_Radar_Web.bat            # 웹 모드 실행
├── .env.example                     # API 키 템플릿
│
├── ai/                              # AI 모듈 (15개)
│   ├── model_router.py              #   35개 LLM 프로바이더 라우팅
│   ├── briefing.py                  #   일간 + 관심 분야 브리핑
│   ├── chat.py                      #   AI 뉴스 채팅
│   ├── voice_briefing.py            #   음성 브리핑 (edge-tts)
│   ├── factcheck.py                 #   교차 검증 팩트체크
│   ├── glossary.py                  #   AI 용어 사전
│   ├── weekly_report.py             #   주간 인텔리전스 리포트
│   ├── competitor.py                #   AI 도구 모니터링
│   ├── trend.py                     #   키워드 트렌드 분석
│   ├── debate.py                    #   AI 토론 모드
│   ├── smart_alert.py               #   데스크톱 스마트 알림
│   ├── translator.py                #   자동 한국어 번역
│   ├── release_tracker.py           #   릴리즈 자동 감지
│   ├── deduplicator.py              #   중복 기사 병합
│   └── batch_processor.py           #   배치 병렬 처리
│
├── sns/                             # SNS 모듈 (4개)
│   ├── poster.py                    #   5개 플랫폼 어댑터
│   ├── card_generator.py            #   카드뉴스 이미지 생성 (Pillow)
│   ├── content_generator.py         #   AI 콘텐츠 5종 생성
│   └── newsletter.py               #   이메일 뉴스레터 (SMTP)
│
├── bot/                             # 봇
│   └── telegram_bot.py              #   텔레그램 봇 (7개 명령어)
│
├── crawler/                         # 크롤러
│   ├── rss_crawler.py               #   RSS 병렬 수집 엔진
│   └── scheduler.py                 #   수집 스케줄러
│
├── reader/                          # 리더
│   └── article_reader.py            #   인앱 기사 리더
│
├── export/                          # 내보내기
│   └── exporter.py                  #   Markdown + PDF 변환
│
├── utils/                           # 유틸리티
│   └── helpers.py                   #   공통 헬퍼 함수
│
├── scripts/                         # CLI 도구
│   ├── collect.py                   #   자동 수집 스크립트
│   └── reclassify.py                #   카테고리 재분류
│
├── data/                            # 데이터 저장소
│   ├── preset_sources.json          #   74개 프리셋 소스
│   ├── sources.json                 #   사용자 소스 설정
│   ├── articles.json                #   수집된 기사
│   ├── briefings.json               #   생성된 브리핑
│   ├── weekly_reports.json          #   주간 리포트
│   ├── release_log.json             #   릴리즈 추적 로그
│   ├── audio/                       #   음성 브리핑 파일
│   └── cards/                       #   카드뉴스 이미지
│
├── .github/workflows/
│   └── collect.yml                  #   GitHub Actions (하루 3회)
│
└── PRD/                             #   기획 문서
```

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| **언어** | Python 3.11+ |
| **대시보드** | Streamlit 1.44+ |
| **AI / LLM** | 35개 플랫폼 (model_router.py 통합 라우팅) |
| **차트** | Plotly (인터랙티브 시각화) |
| **음성** | edge-tts (Microsoft TTS, 한국어 여성/남성) |
| **이미지** | Pillow (카드뉴스 1080x1080 생성) |
| **데스크톱** | pywebview + pystray (네이티브 윈도우 + 시스템 트레이) |
| **알림** | plyer (데스크톱 푸시 알림) |
| **봇** | python-telegram-bot (7개 명령어) |
| **SNS** | tweepy (X) / Telegram API / Discord Webhook / Threads API / Instagram Graph API |
| **크롤링** | feedparser + BeautifulSoup4 (RSS 파싱 + 본문 추출) |
| **PDF** | fpdf2 (한글 폰트 지원) |
| **CI/CD** | GitHub Actions (하루 3회 자동 수집) |
| **데이터** | 로컬 JSON (외부 DB 불필요) |

---

## 문제 해결

| 문제 | 원인 | 해결 방법 |
|------|------|-----------|
| `python` 명령어를 찾을 수 없음 | PATH 미등록 | Python 재설치 시 **"Add Python to PATH"** 반드시 체크 |
| `pip` 명령어를 찾을 수 없음 | PATH 미등록 | 위와 동일. 또는 `python -m pip install -r requirements.txt` 시도 |
| `streamlit` 명령어를 찾을 수 없음 | 패키지 미설치 | `pip install streamlit` 실행 |
| "API 키가 설정되지 않았습니다" | `.env` 파일 없거나 키 미입력 | 5단계 참고하여 `.env` 파일 생성 후 API 키 입력 |
| 기사가 하나도 안 나옴 | 수집 미실행 | 사이드바 "수집" 클릭 후 "AI 처리" 순서대로 실행 |
| 카테고리 필터에 기사 없음 | 이전 기사 미분류 | `python scripts/reclassify.py` 실행하여 재분류 |
| 포트가 이미 사용 중 | 다른 프로그램이 6601 포트 사용 | `streamlit run app.py --server.port 7429` 로 포트 변경 |
| PDF 내보내기 실패 | 한글 폰트 미포함 | Windows 환경에서만 지원 (맑은 고딕 폰트 필요) |
| 수집 시 일부 소스 오류 | RSS 소스 일시 장애 | 정상 동작 — 오류 소스는 건너뛰고 나머지 정상 수집 |
| 데스크톱 모드 안 열림 | pywebview 미설치 | `pip install pywebview pystray` 실행 |

---

## 로드맵

| Phase | 기능 | 상태 |
|-------|------|------|
| Phase 1 | 수집 + AI 요약 + 대시보드 (17개) | **완료** |
| Phase 2-A | 검색 + 북마크 + 감성 분석 + 채팅 (5개) | **완료** |
| Phase 2-B | 음성 + 텔레그램 + 팩트체크 + 용어사전 + Actions (5개) | **완료** |
| Tier 1 | 관심 분야 브리핑 + 주간 리포트 + 도구 비교 (3개) | **완료** |
| Tier 2 | 트렌드 차트 + AI 토론 (2개) | **완료** |
| S-Tier | 스마트 알림 + 콘텐츠 생성 + 뉴스레터 + SNS (4개) | **완료** |
| UI/UX | 5탭 리디자인 + 페이지네이션 + 프리미엄 CSS (3개) | **완료** |
| Desktop | pywebview + 시스템 트레이 + 백그라운드 알림 | **완료** |
| Expand | 릴리즈 추적 + 자동 번역 + 배치 처리 + 병렬 크롤링 | **완료** |
| Next | ChromaDB RAG, Ollama 로컬 LLM, 게이미피케이션, 플러그인 | 예정 |

---

## 라이선스

MIT License - Copyright (c) 2026 **SoDam AI Studio**

자세한 내용은 [LICENSE](./LICENSE) 파일을 참고하세요.

---

*Streamlit + 35개 AI 플랫폼으로 만들었습니다 — SoDam AI Studio*
