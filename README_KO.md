# AI News Radar

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-SoDam%20AI%20Studio-green)
![Release](https://img.shields.io/badge/Release-v1.1.0-blue)

[English](README.md) | [한국어](README_KO.md) | [日本語](README_JA.md) | [中文](README_ZH.md)

---

**AI News Radar**는 **74개 뉴스 소스**에서 AI 관련 뉴스를 자동으로 수집하고, AI가 요약·분류·분석해주는 개인용 뉴스 플랫폼입니다.

---

## 실행 방법 (3단계)

> **코딩 경험이 전혀 없어도 됩니다.** 아래 3단계만 따라하세요.

### 1단계: 다운로드

이 페이지 위쪽의 초록색 **"Code"** 버튼을 클릭하고, **"Download ZIP"**을 클릭합니다.

다운로드된 ZIP 파일을 원하는 폴더에 압축 해제합니다.

### 2단계: Python 설치

이미 Python이 설치되어 있다면 이 단계를 건너뛰세요.

1. **[python.org/downloads](https://www.python.org/downloads/)** 에 접속합니다
2. 노란색 **"Download Python"** 버튼을 클릭합니다
3. 다운로드된 파일을 실행합니다
4. **중요: 화면 아래쪽의 "Add Python to PATH" 체크박스를 반드시 체크하세요!**
5. **"Install Now"**를 클릭합니다

### 3단계: 앱 실행

압축 해제한 폴더를 열고, 아래 파일을 **더블클릭**합니다:

| 파일 | 설명 |
|------|------|
| **`install_and_run.bat`** | **처음 실행할 때 사용.** 모든 것을 자동으로 설치하고 API 키 설정을 도와줍니다. |
| **`start.bat`** | **두 번째부터 사용.** 빠르게 실행합니다. |

끝! 브라우저에 AI News Radar가 열립니다.

---

## 무료 API 키 발급

AI News Radar가 뉴스를 분석하려면 AI 서비스가 필요합니다. **Google Gemini**를 추천합니다 (무료).

1. **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)** 에 접속
2. Google 계정으로 로그인
3. **"Create API Key"** 클릭
4. 키를 복사

`install_and_run.bat`을 실행하면 자동으로 키를 입력하라고 안내합니다.

> **35개 AI 서비스를 지원합니다.** `.env.example` 파일에서 전체 목록을 확인할 수 있습니다. 1개의 키만 있으면 됩니다.

---

## 주요 기능 (45+)

### 뉴스 수집
- **74개 RSS 소스**에서 자동 수집 (영어 + 한국어)
- 중복 뉴스 자동 병합
- 키워드 워치리스트 (관심 키워드 하이라이트)
- 영어 기사 자동 한국어 번역

### AI 분석
- **원클릭 파이프라인**: 수집 → 분석 → 브리핑을 한 번에
- 매일 TOP 5 브리핑 자동 생성
- 주간 인텔리전스 리포트
- AI 채팅 (뉴스에 대해 질문하기)
- 트렌드 분석 + 차트
- AI 도구 릴리즈 추적
- 경쟁 도구 비교
- AI 토론 모드 (찬반 분석)
- AI 용어 사전 (전문 용어 쉽게 설명)
- 팩트체크 (여러 매체 교차 검증)
- 스마트 알림

### 콘텐츠 & 공유
- 음성 브리핑 (TTS)
- Markdown / PDF 내보내기
- Discord, Telegram, X, Threads, Instagram 게시
- AI 콘텐츠 자동 생성 (SNS용 글 자동 작성)
- 이메일 뉴스레터 발행

---

## 프로젝트 구조

```
ai-news-radar/
├── install_and_run.bat    ← 더블클릭으로 설치 + 실행 (처음)
├── start.bat              ← 더블클릭으로 실행 (이후)
├── desktop.bat            ← 데스크톱 앱 모드 (선택)
├── app.py                 ← 메인 앱
├── config.py              ← 설정
├── requirements.txt       ← 의존성 목록
├── .env                   ← API 키 (직접 생성)
├── .env.example           ← .env 템플릿
│
├── ai/                    ← AI 분석 모듈
├── crawler/               ← 뉴스 수집
├── reader/                ← 기사 리더
├── export/                ← 내보내기
├── sns/                   ← SNS 게시
├── bot/                   ← 텔레그램 봇
├── utils/                 ← 유틸리티
└── data/                  ← 수집된 데이터 (자동 생성)
```

---

## 환경 변수

모든 설정은 `.env` 파일에 저장됩니다. 최소 1개의 API 키만 있으면 됩니다.

| 변수 | 필수 | 설명 |
|------|------|------|
| `GEMINI_API_KEY` | 추천 | Google Gemini (무료: 1000회/일) |
| `GROQ_API_KEY` | 대안 | Groq (무료: 14,400회/일) |
| `OPENAI_API_KEY` | 대안 | OpenAI GPT (유료) |

35개 AI 서비스 전체 목록은 `.env.example`을 참고하세요.

---

## 자주 묻는 질문

**Q: "API key not configured"라고 나옵니다**
A: `.env` 파일을 메모장으로 열어 API 키가 올바르게 입력되었는지 확인하세요. 따옴표는 필요 없습니다.

**Q: .bat 파일을 더블클릭해도 아무 일도 안 일어납니다**
A: .bat 파일을 마우스 오른쪽 버튼으로 클릭 → "관리자 권한으로 실행"을 선택하세요. 그래도 안 되면 Python 설치 시 "Add to PATH"를 체크했는지 확인하세요.

**Q: Mac이나 Linux에서도 쓸 수 있나요?**
A: 네! 터미널에서 아래 명령어를 실행하세요:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 6601
```

**Q: Gemini API가 정말 무료인가요?**
A: 네. Google이 Flash-Lite 1000회/일, Flash 250회/일을 무료로 제공합니다. 개인 사용에 충분합니다.

---

## 라이선스

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

이 소프트웨어는 개인 및 교육 목적으로 제공됩니다. 상업적 사용은 퍼블리셔에게 문의하세요.
