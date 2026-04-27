# AI News Radar

<p align="center">
  <img src="assets/icon.png" width="80" alt="AI News Radar Icon" />
</p>
<p align="center">
  <strong>개인용 AI 뉴스 인텔리전스 플랫폼</strong><br/>
  74개 소스에서 AI 뉴스를 자동 수집·요약·분석합니다
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-SoDam%20AI%20Studio-green" alt="License"/>
  <img src="https://img.shields.io/badge/Release-v1.6.0-blue" alt="Release"/>
  <img src="https://img.shields.io/badge/LLM-39%20Providers%20(Local%204%20+%20Cloud%2035)-purple" alt="LLM"/>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_KO.md">한국어</a>
</p>

---

## AI News Radar란?

AI News Radar는 **내 컴퓨터에서 실행되는 AI 뉴스 비서**입니다:

- **74개 소스**에서 AI 뉴스를 한 번에 수집
- AI가 모든 기사를 **자동 요약·분류·분석**
- 매일 **TOP 5 브리핑**, 매주 **인텔리전스 리포트** 생성
- 뉴스에 대해 AI와 **대화** ("오늘 AI 분야에 무슨 일이 있었어?")
- Discord, Telegram, X 등에 **SNS 게시물 자동 생성**
- AI 도구 **릴리즈 추적**, **트렌드 분석**, **경쟁사 비교**

---

## 빠른 시작 가이드

> **코딩 경험이 전혀 필요 없습니다.** 아래 단계를 그대로 따라하세요.

### 1단계: Python 설치

이미 Python이 설치되어 있으면 2단계로 건너뛰세요.

1. 웹 브라우저에서 **[python.org/downloads](https://www.python.org/downloads/)** 열기
2. 노란색 **"Download Python 3.xx"** 버튼 클릭
3. 다운로드된 파일 실행
4. **매우 중요**: 설치 화면 아래쪽에 **"Add Python to PATH"** 체크박스가 있습니다. **반드시 체크하세요!** 이걸 안 하면 앱이 Python을 찾지 못합니다.
5. **"Install Now"** 클릭하고 완료까지 대기
6. **"Close"** 클릭

### 2단계: AI News Radar 다운로드

**방법 A — GitHub Releases에서 다운로드 (추천):**
1. [릴리즈 페이지](https://github.com/sodam-ai/ai-news-radar/releases)로 이동
2. **`AI_News_Radar_v1.2.0.zip`** 다운로드
3. ZIP 파일 우클릭 → **"압축 풀기"** → 원하는 폴더 선택 (예: 바탕화면)

**방법 B — 이 페이지에서 다운로드:**
1. 이 페이지 위쪽의 초록색 **"Code"** 버튼 클릭
2. **"Download ZIP"** 클릭
3. 원하는 폴더에 압축 해제

### 3단계: 무료 API 키 발급

AI News Radar가 뉴스를 분석하려면 AI 서비스 키가 필요합니다 (30초면 됩니다):

1. **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)** 접속
2. Google 계정으로 로그인
3. **"Create API Key"** 클릭
4. **키를 복사** (`AIzaSy...` 형태)
5. 이 페이지를 열어두세요 — 다음 단계에서 붙여넣기합니다

> **정말 무료인가요?** 네! Google이 하루 1,000회 무료 API 호출을 제공합니다. 개인 뉴스 추적에 충분합니다. 신용카드 불필요.

### 4단계: 앱 실행

압축 해제한 폴더를 열고 **`AI_News_Radar.exe`** 를 **더블클릭**하세요.

**처음 실행할 때:**
- 앱이 **자동으로 가상환경을 생성**하고 **모든 의존성을 설치**합니다
- **3~5분 정도 걸립니다** (인터넷 속도에 따라, 약 200MB 다운로드)
- 텍스트 편집기가 열리면 — 3단계에서 복사한 **API 키를 붙여넣기**하고, 파일을 저장하고 닫으세요
- 브라우저에 AI News Radar가 열립니다!

**두 번째 실행부터:**
- exe를 더블클릭하면 — 몇 초 안에 시작됩니다

> **Windows SmartScreen 경고?** 새로운 앱이라 파란색 경고 화면이 나올 수 있습니다. **"추가 정보"** → **"실행"** 을 클릭하세요. 모든 새 소프트웨어에 나타나는 정상적인 현상입니다.

---

## 주요 기능 (45개 이상)

### 뉴스 수집 & 관리
| 기능 | 설명 |
|------|------|
| 원클릭 파이프라인 | 수집 → 분석 → 브리핑을 버튼 하나로 |
| 74개 RSS 소스 | TechCrunch, MIT Tech Review, 한국 기술 매체 등 |
| 스마트 중복 제거 | 여러 매체의 같은 뉴스를 자동 병합 |
| 키워드 워치리스트 | 관심 키워드 하이라이트 |
| 북마크 | 기사 저장 및 빠른 접근 |
| 자동 번역 | 영어 기사를 한국어로 자동 번역 |
| 카테고리 필터 | AI 도구, 연구, 트렌드, 튜토리얼, 비즈니스 등 8개 |

### AI 분석 & 인텔리전스
| 기능 | 설명 |
|------|------|
| 매일 TOP 5 브리핑 | AI가 가장 중요한 5개 뉴스를 선별·요약 |
| 주간 리포트 | 트렌드, 예측, 핵심 시사점을 포함한 종합 분석 |
| AI 채팅 | "최근 LLM 발전은?", "오늘 중요한 뉴스는?" 등 질문 |
| 트렌드 분석 | 시간에 따른 주제 변화를 차트로 시각화 |
| 릴리즈 트래커 | 50+ AI 도구의 새 버전 모니터링 |
| 경쟁사 분석 | AI 기업/도구 비교 |
| AI 토론 | 논쟁적 AI 주제의 찬반 분석 |
| 용어 사전 | 전문 용어를 쉬운 말로 설명 |
| 팩트체크 | 여러 매체 교차 검증 |
| 스마트 알림 | 관심사와 매칭되는 뉴스 알림 |

### 콘텐츠 생성 & 공유
| 기능 | 설명 |
|------|------|
| 음성 브리핑 | TTS로 브리핑 듣기 (20+ 음성) |
| Markdown 내보내기 | 블로그, Notion, Obsidian용 |
| PDF 내보내기 | 표지와 목차가 있는 PDF |
| Discord/Telegram/X/Threads/Instagram | 5개 SNS 플랫폼 게시 |
| AI 콘텐츠 생성 | 플랫폼별 최적화된 게시물 자동 작성 |
| 이메일 뉴스레터 | 주간 요약을 이메일로 발송 |

---

## 환경 변수

모든 설정은 `.env` 파일에 저장됩니다. **최소 1개의 API 키만 있으면 됩니다.**

### 필수 (1개만 선택)

| 변수 | 제공자 | 무료 한도 | 발급 방법 |
|------|--------|-----------|----------|
| `GEMINI_API_KEY` | Google Gemini | 1,000회/일 | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| `GROQ_API_KEY` | Groq | 14,400회/일 | [console.groq.com](https://console.groq.com) |
| `OPENAI_API_KEY` | OpenAI | 유료 ($0.002/회) | [platform.openai.com](https://platform.openai.com) |

35개 AI 서비스 전체 목록은 `.env.example`을 참고하세요.

---

## 자주 묻는 질문

### "API key not configured"라고 나옵니다
`.env` 파일을 메모장으로 열어 API 키가 올바르게 입력되었는지 확인하세요:
```
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxx
```
따옴표 없이, `=` 주위에 공백 없이 입력합니다.

### exe를 더블클릭해도 아무 반응이 없습니다
1. Python이 설치되었는지 확인: 명령 프롬프트에서 `python --version` 입력
2. "인식되지 않는 명령"이 나오면, Python을 **"Add to PATH"** 체크하고 재설치
3. exe 우클릭 → **"관리자 권한으로 실행"** 시도

### 처음 실행이 오래 걸립니다
정상입니다! 첫 실행 시 약 200MB의 Python 패키지를 다운로드합니다. **3~5분** 걸리며, 이후에는 몇 초 안에 시작됩니다.

### Mac이나 Linux에서도 쓸 수 있나요?
네! `.exe` 파일은 Windows 전용이지만, 핵심 앱은 모든 OS에서 작동합니다:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 6601
```

---

## 기여자

이 프로젝트에 도움을 주신 분들께 감사드립니다.

| 기여자 | 기여 내용 |
|--------|----------|
| [@dimlose](https://github.com/dimlose) | 🐛 FTS5 DB 손상 버그 리포트 ([#11](https://github.com/sodam-ai/ai-news-radar/issues/11)) |

---

## 라이선스

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

이 소프트웨어는 개인 및 교육 목적으로 제공됩니다.
상업적 사용은 퍼블리셔에게 문의하세요.

자세한 내용은 [LICENSE](LICENSE)를 참조하세요.
