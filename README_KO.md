<div align="center">

# AI News Radar

**AI 기반 뉴스 인텔리전스 플랫폼 -- 74개 소스에서 자동 수집, 분석, 브리핑. 35개 LLM 플랫폼 지원.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-SoDam%20AI%20Studio-green)](./LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.0-blue)](https://github.com/sodam-ai/ai-news-radar/releases)

[English](./README.md) | [한국어](./README_KO.md) | [日本語](./README_JA.md) | [中文](./README_ZH.md)

</div>

---

## AI News Radar란?

AI 분야는 매시간 바뀝니다. 새 모델 출시, 도구 업데이트, 논문 발표, 기업 동향 -- 수십 곳에 흩어져 있는 정보를 일일이 확인하는 건 사실상 불가능합니다. AI News Radar는 이 문제를 해결합니다. 74개의 엄선된 소스에서 뉴스를 자동으로 수집하고, AI가 모든 기사를 요약, 분류, 점수화, 팩트체크한 뒤 -- 깔끔하고 실용적인 브리핑으로 전달합니다.

**한 문장으로:** 74개 사이트를 직접 돌아다니지 마세요. AI가 전부 읽고 중요한 것만 알려줍니다.

---

## 보안 및 개인정보 -- 반드시 읽으세요

### API 키는 100% 개인 소유 -- 절대 업로드되지 않습니다

이 프로젝트를 다운로드하면 **API 키, 비밀번호, 개인 정보가 전혀 포함되어 있지 않습니다.**

작동 방식:
- 본인 컴퓨터에 `.env`라는 파일을 직접 만듭니다
- 본인이 발급받은 API 키를 그 파일에 넣습니다 (Google/Groq 등에서 무료 발급)
- 그 파일은 **절대 인터넷에 업로드되지 않습니다** -- `.gitignore`가 차단합니다
- 이 앱을 다운로드한 모든 사람은 **자신의 키**로 **자신의 할당량**을 사용합니다

### 안전하다는 증거

| 확인 항목 | 결과 |
|-----------|------|
| GitHub 저장소에 `.env` 파일 존재 | 없음 (.gitignore로 차단됨) |
| 소스 코드에 API 키 하드코딩 | 없음 -- 모든 코드가 환경변수에서 읽음 |
| 내 키가 다른 사람과 공유됨 | 불가능 -- 각자 자신의 키 설정 |
| AI 제공업체 외 서버 연결 | 뉴스 RSS 피드와 선택한 AI API에만 연결 |

### 다운로드한 사람이 해야 할 일

이 앱을 다운로드한 모든 사람은:
1. 본인의 무료 API 키를 발급받습니다 (10초, 신용카드 불필요)
2. 본인의 `.env` 파일을 만들고 키를 넣습니다
3. 끝 -- 자신의 할당량을 사용, 다른 사람의 할당량과 완전히 분리됨

---

## 기능별 API 키 필요 여부

### 즉시 사용 가능 -- API 키 불필요

앱을 다운로드하고 실행하는 즉시 사용할 수 있는 기능:

| 기능 | 방식 |
|------|------|
| **74개 소스에서 뉴스 수집** | RSS 피드 읽기 (인터넷 연결만 필요) |
| **기사 목록 보기** | 로컬 파일 읽기 |
| **북마크 및 읽기 기록** | 컴퓨터에 저장 |
| **고급 검색 및 필터** | 로컬 데이터 처리 |
| **내보내기 (PDF / 마크다운)** | 로컬 파일 생성 |
| **앱 내 기사 리더** | 웹 페이지 가져오기 |
| **타임라인 보기** | 로컬 데이터 표시 |

### API 키 필요 (무료 옵션 있음)

AI를 사용하는 기능 -- 무료 API 키 1개 필요:

| 기능 | API 키가 필요한 이유 |
|------|---------------------|
| **AI 뉴스 분류** | AI가 각 기사를 읽고 분류 |
| **3줄 한국어 요약** | AI가 각 기사 요약 |
| **일일 브리핑 (TOP 5)** | AI가 주요 뉴스 선정 및 설명 |
| **영어 -> 한국어 번역** | AI가 기사 내용 번역 |
| **AI 뉴스 챗봇** | AI가 뉴스에 대한 질문 답변 |
| **팩트체크** | AI가 소스 교차 검증 |
| **AI 토론** | AI가 두 도구의 장단점 생성 |
| **AI 용어 사전** | AI가 전문 용어 설명 |
| **주간 인텔리전스 리포트** | AI가 주간 분석 생성 |
| **원클릭 풀 파이프라인** | 모든 AI 기능 한 번에 실행 |

> **무료 Gemini API 키** (Google 제공)는 하루 1,000회 AI 호출이 가능합니다 -- 개인 일상 사용에 충분한 양입니다.

---

## 주요 특징

- **50개 이상의 기능** -- 5개 탭
- **74개 소스** -- 일반 AI (26) + 이미지/영상 (20) + 바이브코딩 (19) + 온톨로지 (9)
- **35개 LLM 플랫폼** -- 대부분 무료 티어, API 키 1개만 필요
- **9개 카테고리** -- 도구, 연구, 트렌드, 튜토리얼, 비즈니스, 이미지/영상, 바이브코딩, 온톨로지, 기타
- **19개 AI 도구** 자동 릴리즈 감지
- **5개 SNS 플랫폼** -- X, 텔레그램, 디스코드, 스레드, 인스타그램 + 카드 뉴스 자동 생성
- **음성 브리핑**, AI 팩트체크, AI 용어 사전, AI 토론
- **원클릭 풀 파이프라인** -- 수집 > 분석 > 브리핑 > 릴리즈 감지
- **데스크톱 앱** -- 시스템 트레이 + 백그라운드 알림
- **GitHub Actions** -- 하루 3회 자동 수집

---

## 기능 목록 (50개 이상)

### 대시보드 탭

| 기능 | 설명 |
|------|------|
| 일일 브리핑 | AI가 생성한 "오늘의 AI 뉴스 TOP 5" (중요도 순) |
| 포커스 브리핑 | 이미지/영상, 바이브코딩, 온톨로지 전용 브리핑 |
| 카테고리 퀵필터 | 9개 카테고리 원클릭 필터 |
| 감성 게이지 | 긍정/중립/부정 비율 인터랙티브 Plotly 차트 |
| 음성 브리핑 | edge-tts로 브리핑을 음성으로 듣기 |
| 주간 인텔리전스 리포트 | 트렌드, 예측, 분석 포함 주간 리포트 자동 생성 |
| 뉴스레터 | 이메일로 일일/주간 브리핑 발송 (SMTP) |

### 뉴스 피드 탭

| 기능 | 설명 |
|------|------|
| 74개 소스 수집 | 15개 병렬 워커로 빠른 수집 |
| AI 요약 | 모든 기사 한국어 3줄 요약 |
| 9개 카테고리 분류 | AI 자동 분류 |
| 중요도 점수 | 기사별 1~5점 평가 |
| 감성 분석 | 긍정/중립/부정 태깅 |
| AI 팩트체크 | 소스 교차 검증 |
| 중복 병합 | 동일 기사 자동 병합 |
| 키워드 워치리스트 | 추적 키워드 하이라이트 및 알림 |
| 앱 내 리더 | 광고 없이 앱 내에서 기사 전체 읽기 |
| 고급 검색 | 키워드, 카테고리, 감성, 읽음 여부 필터 |
| 북마크 + 메모 | 개인 메모와 함께 기사 저장 |
| 페이지네이션 | 페이지당 10개 기사 |
| 타임라인 보기 | 오늘 / 어제 / 이번 주 탐색 |
| 자동 한국어 번역 | 영어 기사 자동 번역 |

### AI 탭

| 기능 | 설명 |
|------|------|
| AI 뉴스 채팅 | 수집된 뉴스에 대해 자연어로 질문 |
| AI 용어 사전 | 자동 추출된 AI 용어와 초보자 친화적 설명 |

### 인사이트 탭

| 기능 | 설명 |
|------|------|
| AI 도구 릴리즈 트래커 | 19개 AI 도구 자동 릴리즈 감지 |
| 트렌드 차트 | 인터랙티브 일별 언급 빈도 Plotly 차트 |
| 핫 키워드 | 전주 대비 상승 키워드 |
| AI 토론 | 두 AI 도구의 장단점과 판정 생성 |
| 주간 인텔리전스 리포트 | 예측 포함 심층 주간 분석 |

### 공유 탭

| 기능 | 설명 |
|------|------|
| SNS 자동 게시 | X, 텔레그램, 디스코드, 스레드, 인스타그램 게시 |
| 카드 뉴스 생성 | 1080x1080 카드 이미지 자동 생성 (다크 테마) |
| AI 콘텐츠 생성 | 트윗, 스레드, 인스타그램 캡션, 블로그, 링크드인 자동 생성 |
| 뉴스레터 이메일 | 구독자 목록에 브리핑 발송 |
| 내보내기 | 마크다운 또는 PDF 다운로드 |

### 시스템 기능

| 기능 | 설명 |
|------|------|
| 원클릭 풀 파이프라인 | 수집 > AI 처리 > 브리핑 > 릴리즈 감지를 한 번에 |
| 병렬 크롤링 | 15개 동시 워커로 빠른 수집 |
| 스마트 키워드 알림 | 감시 키워드 등장 시 데스크톱 알림 |
| 데스크톱 앱 | pywebview 기반 네이티브 창 + 시스템 트레이 + 백그라운드 모드 |
| GitHub Actions | 하루 3회 자동 수집 (설정 가능) |
| 텔레그램 봇 | 7개 명령어로 외출 중에도 접근 |

---

## 74개 뉴스 소스

| 카테고리 | 개수 | 예시 |
|----------|:----:|------|
| **일반 AI** | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites, Ars Technica |
| **이미지/영상** | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| **바이브코딩** | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| **온톨로지** | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35개 LLM 플랫폼

아래 중 **하나의 API 키**만 있으면 됩니다:

| 등급 | 플랫폼 |
|------|--------|
| **무료 (추천)** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **크레딧 / 저렴** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **프리미엄** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

> **초보자 추천:** Gemini (하루 1,000회 무료)와 Groq (하루 14,400회 무료) -- 신용카드 불필요.

---

## 시작하기 -- 완전 초보자 가이드 (단계별)

> **코딩 경험이 전혀 없어도 됩니다.** 복사 붙여넣기만 할 수 있으면 설정할 수 있습니다. 각 단계를 천천히 따라하세요.

### 1단계 -- Python 설치

Python은 이 앱이 만들어진 프로그래밍 언어입니다. 한 번만 설치하면 됩니다.

1. 브라우저 주소창에 입력: **https://www.python.org/downloads/**
2. 큰 노란색 **"Download Python"** 버튼 클릭
3. 다운로드된 파일 실행 (Windows에서 `.exe` 파일을 더블클릭)
4. **매우 중요:** 설치 화면 하단의 **"Add Python to PATH"** 체크박스를 반드시 체크하세요
5. **"Install Now"** 클릭
6. 완료될 때까지 기다린 후 "Close" 클릭

**설치 확인 방법:** 키보드에서 `Win + R` 키를 동시에 누르고, `cmd`를 입력한 뒤 Enter를 누르세요. 검은 창이 열리면 다음을 입력합니다:
```
python --version
```
`Python 3.11.9` 같은 결과가 나오면 설치 성공입니다.

---

### 2단계 -- 프로젝트 다운로드

**방법 A: ZIP 다운로드 (가장 쉬움)**
1. 브라우저에서 **https://github.com/sodam-ai/ai-news-radar** 접속
2. 초록색 **"Code"** 버튼 클릭
3. **"Download ZIP"** 클릭
4. 다운로드된 ZIP 파일 찾기 (보통 "다운로드" 폴더에 있습니다)
5. ZIP 파일을 우클릭 > **"모두 압축 풀기"** > 원하는 폴더 선택 > "압축 풀기" 클릭
6. `ai-news-radar-main` 폴더가 생성됩니다

**방법 B: Git Clone (Git이 설치되어 있는 경우)**
```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

---

### 3단계 -- 프로젝트 폴더에서 터미널 열기

1. 압축 해제된 폴더를 열어주세요 (`app.py` 파일이 보이는 폴더)
2. 파일 탐색기 상단의 주소창을 클릭합니다
3. `cmd`를 입력하고 Enter를 누릅니다
4. 검은 터미널 창이 올바른 폴더 위치에서 자동으로 열립니다

---

### 4단계 -- 필수 패키지 설치

터미널 창에 아래 명령어를 그대로 입력하고 Enter를 누르세요:
```bash
pip install -r requirements.txt
```
설치가 완료될 때까지 기다립니다 (1~3분 소요). 화면에 많은 텍스트가 빠르게 스크롤되는데, 이것은 정상입니다.

---

### 5단계 -- 무료 API 키 발급

AI 기능을 사용하려면 무료 API 키가 필요합니다. 가장 빠른 방법 두 가지:

**방법 A: Google Gemini (추천 -- 하루 1,000회 무료)**
1. 브라우저에서 **https://aistudio.google.com/apikey** 접속
2. Google 계정으로 로그인
3. **"Create API Key"** 클릭
4. **"Create API key in new project"** 클릭
5. 화면에 나타나는 키를 복사합니다 (`AIzaSy...`로 시작하는 긴 문자열)

**방법 B: Groq (역시 무료 -- 하루 14,400회, 더 빠름)**
1. 브라우저에서 **https://console.groq.com/keys** 접속
2. Google 계정으로 가입 (10초면 됩니다)
3. **"Create API Key"** 클릭
4. 키를 복사합니다 (`gsk_`로 시작)

> 두 방법 모두 **신용카드가 필요 없습니다.** 요금이 부과되지 않습니다.

---

### 6단계 -- API 키 설정 (.env 파일)

1. 프로젝트 폴더에서 **`.env.example`** 파일을 찾습니다
2. 그 파일을 복사한 뒤 이름을 **`.env`**로 변경합니다 (`.example` 부분을 지웁니다)
   - Windows: 파일을 우클릭 > 복사 > 같은 폴더에 붙여넣기 > 이름 변경
3. `.env` 파일을 메모장으로 엽니다 (우클릭 > 연결 프로그램 > 메모장)
4. 본인이 발급받은 플랫폼에 해당하는 줄을 찾아 키를 입력합니다:

**Gemini 키를 받은 경우:**
```
GEMINI_API_KEY=AIzaSy_여기에_본인_키_붙여넣기
```

**Groq 키를 받은 경우:**
```
GROQ_API_KEY=gsk_여기에_본인_키_붙여넣기
```

5. 메모장에서 `Ctrl + S`로 저장한 뒤 닫습니다

> **키는 안전합니다.** 이 `.env` 파일은 본인 컴퓨터에만 존재합니다. GitHub이나 다른 곳에 절대 업로드되지 않습니다.

---

### 7단계 -- 앱 실행 (3가지 방법)

**방법 1: 웹 모드 (브라우저에서 열림)**
```bash
streamlit run app.py
```
브라우저가 자동으로 **http://localhost:6601** 을 엽니다.

**방법 2: 데스크톱 모드 (독립 창)**
```bash
python desktop.py
```
시스템 트레이에 아이콘이 생기며 백그라운드에서 동작합니다.

**방법 3: EXE 실행파일 (설치 없이 바로 실행)**

PyInstaller로 빌드된 `.exe` 파일이 있다면, `dist` 폴더 안의 실행파일을 더블클릭하면 됩니다. Python 설치 없이도 실행 가능합니다.

**Windows 바로가기:** 프로젝트 폴더의 **`AI_News_Radar.bat`** 파일을 더블클릭해도 웹 모드로 실행됩니다.

---

### 첫 사용 -- 실행 후 할 일

1. 사이드바(왼쪽 패널)에서 **"Collect"** 클릭 -- 74개 소스에서 뉴스 수집 (약 1분 소요)
2. **"AI Process"** 클릭 -- AI가 모든 기사를 분석합니다 (API 키 필요)
3. **"Briefing"** 클릭 -- 오늘의 TOP 5 요약이 생성됩니다
4. 5개 탭을 탐색해 보세요: 대시보드 / 뉴스 피드 / AI / 인사이트 / 공유

> **팁:** API 키가 아직 없어도 "Collect"를 클릭하면 뉴스 목록은 볼 수 있습니다. AI 요약이나 분류 없이 기사 제목과 링크만 표시됩니다. 나중에 API 키를 추가하면 모든 AI 기능이 활성화됩니다.

---

## 사용 가이드

| 원하는 것 | 방법 |
|----------|------|
| 오늘 요약 읽기 | 대시보드 탭 > 브리핑 섹션 |
| 카테고리별 필터 | 대시보드 탭 > 카테고리 퀵필터 클릭 |
| 주제 검색 | 뉴스 피드 탭 > 검색 보기 > 키워드 입력 |
| AI에게 뉴스 질문 | AI 탭 > 채팅 보기 > 질문 입력 |
| AI 용어 학습 | AI 탭 > 용어 사전 > 검색 또는 탐색 |
| AI 도구 릴리즈 추적 | 인사이트 탭 > 릴리즈 트래커 |
| 트렌드 키워드 확인 | 인사이트 탭 > 트렌드 |
| AI 토론 실행 | 인사이트 탭 > AI 토론 > 두 도구 선택 |
| SNS 콘텐츠 생성 | 공유 탭 > 콘텐츠 생성 |
| SNS에 게시 | 공유 탭 > SNS 게시 |
| 브리핑 음성으로 듣기 | 대시보드 탭 > 음성 선택 > "Voice" 클릭 |
| PDF로 내보내기 | 공유 탭 > 내보내기 |
| 기사 저장 | 뉴스 피드 탭 > 북마크 아이콘 클릭 |
| 키워드 알림 설정 | 사이드바 > 워치리스트 > 키워드 입력 |
| 풀 파이프라인 실행 | 사이드바 > "원클릭 전체 실행" 버튼 |

---

## SNS 플랫폼 연결 가이드

| 플랫폼 | 소요 시간 | 난이도 | 설정 방법 |
|--------|:---------:|:------:|-----------|
| Discord | 30초 | 매우 쉬움 | 채널 설정에서 웹훅 URL 생성 |
| Telegram | 2분 | 쉬움 | @BotFather로 봇 생성 |
| X (Twitter) | 10분 | 보통 | 개발자 계정 신청 |
| Threads | 10분 | 보통 | Meta 개발자 포털 |
| Instagram | 15분 | 복잡 | Instagram Graph API 설정 |

각 플랫폼별 상세 연결 방법은 앱 내 **공유 탭 > SNS 게시** 섹션에서 확인할 수 있습니다.

---

## 프로젝트 구조

```
ai-news-radar/
├── app.py                       # 메인 대시보드 (5개 탭)
├── desktop.py                   # 데스크톱 앱 (pywebview + 시스템 트레이)
├── config.py                    # 설정 (9개 카테고리, 포트, 경로)
├── requirements.txt             # 필수 패키지 목록
├── .env.example                 # API 키 템플릿 (공유해도 안전)
├── .env                         # 본인의 API 키 (로컬 전용, 절대 업로드 안 됨)
├── .gitignore                   # .env 업로드 차단
├── AI_News_Radar.bat            # Windows 실행기 (웹 모드)
├── AI_News_Radar_Silent.vbs     # 콘솔 창 없는 실행기
│
├── ai/                          # AI 모듈 14개
│   ├── model_router.py          #   35개 LLM 플랫폼 라우팅
│   ├── briefing.py              #   일일 + 포커스 브리핑 생성
│   ├── chat.py                  #   자연어 뉴스 채팅
│   ├── voice_briefing.py        #   TTS 음성 출력 (edge-tts)
│   ├── factcheck.py             #   소스 교차 팩트 검증
│   ├── glossary.py              #   AI 용어 사전
│   ├── weekly_report.py         #   주간 인텔리전스 리포트
│   ├── release_tracker.py       #   자동 릴리즈 감지
│   ├── trend.py                 #   키워드 트렌드 분석
│   ├── debate.py                #   AI 토론 모드
│   ├── smart_alert.py           #   데스크톱 키워드 알림
│   ├── translator.py            #   자동 한국어 번역
│   ├── deduplicator.py          #   중복 기사 병합
│   └── batch_processor.py       #   배치 병렬 처리
│
├── sns/                         # SNS 및 공유 모듈
│   ├── card_generator.py        #   1080x1080 카드 뉴스 이미지
│   ├── poster.py                #   5개 플랫폼 SNS 게시
│   ├── content_generator.py     #   AI 콘텐츠 (5종류)
│   └── newsletter.py            #   이메일 뉴스레터 (SMTP)
│
├── crawler/                     # 데이터 수집
│   ├── rss_crawler.py           #   RSS 피드 크롤러 (15개 병렬 워커)
│   └── scheduler.py             #   APScheduler 기반 스케줄링
│
├── bot/                         # 텔레그램 연동
│   └── telegram_bot.py          #   텔레그램 봇 (7개 명령어)
│
├── reader/                      # 기사 읽기
│   └── article_reader.py        #   광고 없는 앱 내 기사 리더
│
├── export/                      # 데이터 내보내기
│   └── exporter.py              #   마크다운 + PDF 내보내기
│
├── utils/                       # 공용 유틸리티
│   └── helpers.py               #   공통 헬퍼 함수
│
├── scripts/                     # CLI 도구
│   ├── collect.py               #   독립 실행 수집 스크립트
│   └── reclassify.py            #   카테고리 재분류 도구
│
├── data/                        # 로컬 데이터 저장소 (절대 업로드 안 됨)
│   ├── preset_sources.json      #   74개 소스 정의
│   ├── articles.json            #   수집된 기사
│   ├── briefings.json           #   생성된 브리핑
│   └── ...
│
└── .github/workflows/
    └── collect.yml              #   GitHub Actions (하루 3회 자동 수집)
```

---

## 기술 스택

| 구성 요소 | 기술 |
|-----------|------|
| **언어** | Python 3.11+ |
| **대시보드** | Streamlit 1.44+ |
| **AI 엔진** | 35개 LLM 플랫폼 통합 모델 라우터 |
| **차트** | Plotly |
| **음성** | edge-tts (Microsoft 신경망 TTS) |
| **이미지 생성** | Pillow |
| **데스크톱** | pywebview + pystray |
| **알림** | plyer |
| **RSS 파싱** | feedparser (74개 소스 피드) |
| **웹 스크래핑** | BeautifulSoup4 + requests |
| **텔레그램 봇** | python-telegram-bot |
| **PDF 내보내기** | fpdf2 |
| **스케줄링** | APScheduler + GitHub Actions |
| **데이터 저장** | 로컬 JSON (데이터베이스 설정 불필요) |

---

## EXE 빌드 (소스에서 빌드하기)

Python 환경 없이 실행 가능한 `.exe` 파일을 직접 만들 수 있습니다.

**사전 준비:**
```bash
pip install pyinstaller
```

**빌드 실행:**
```bash
python build_installer.py
```

빌드가 완료되면 `dist` 폴더에 실행파일이 생성됩니다. 이 파일을 더블클릭하면 Python이 설치되지 않은 컴퓨터에서도 AI News Radar를 실행할 수 있습니다.

---

## 자주 묻는 질문 (FAQ)

| 문제 | 해결 방법 |
|------|----------|
| `python` 명령어를 찾을 수 없음 | **"Add to PATH"** 체크 후 Python 재설치 |
| `pip` 명령어를 찾을 수 없음 | `python -m pip install -r requirements.txt` 시도 |
| `streamlit` 명령어를 찾을 수 없음 | `pip install streamlit` 실행 |
| "API 키 미설정" 경고 | 6단계에 따라 API 키가 있는 `.env` 파일 생성 |
| 기사가 나타나지 않음 | "Collect" 먼저 클릭, 1분 기다린 후 "AI Process" 클릭 |
| AI 기능이 작동하지 않음 | `.env` 파일이 존재하고 유효한 API 키가 있는지 확인 |
| 카테고리에 기사가 0개 | `python scripts/reclassify.py` 실행 |
| 포트 6601이 이미 사용 중 | `streamlit run app.py --server.port 7777` 사용 |
| 수집이 느림 | 정상입니다 -- 74개 소스 수집에 약 60초 소요 |

**API 키 관련 자주 하는 실수:**
- 키 앞뒤에 공백이 포함된 경우 -- 공백을 모두 제거하세요
- 만료된 키를 사용하는 경우 -- 새로운 키를 발급받으세요
- `.env` 파일 저장을 잊은 경우 -- 메모장에서 `Ctrl + S`로 반드시 저장하세요

---

## 로드맵

| 단계 | 기능 | 상태 |
|------|------|:----:|
| **Phase 1** | 수집 + AI 요약 + 대시보드 | 완료 |
| **Phase 2** | 검색 + 북마크 + 채팅 + 음성 + 팩트체크 | 완료 |
| **Phase 3** | 인사이트 + SNS + 파이프라인 + 데스크톱 | 완료 |
| **다음** | ChromaDB 벡터 검색, Ollama 로컬 LLM, 모바일 PWA | 계획 중 |

---

## 기여하기

기여를 환영합니다. Pull Request를 자유롭게 제출해 주세요.

1. 저장소 Fork
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

---

## 라이선스

Copyright (c) 2026 **SoDam AI Studio**

이 소프트웨어는 개인 및 교육 목적으로 제공됩니다. 상업적 사용은 퍼블리셔에게 문의하세요. 자세한 내용은 [LICENSE](./LICENSE)를 참조하세요.

---

<div align="center">

*Streamlit + 35개 AI 플랫폼으로 제작 -- SoDam AI Studio*

</div>
