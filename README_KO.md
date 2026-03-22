# AI News Radar

> **AI 뉴스를 자동으로 수집하고, 요약하고, 분류해주는 나만의 AI 뉴스 대시보드**

**[English](./README.md) / Korean / [Japanese](./README_JA.md) / [Chinese](./README_ZH.md)**

---

## AI News Radar가 뭔가요?

AI News Radar는 전 세계 AI 관련 뉴스를 **자동으로 모아서**, Google Gemini AI가 **요약하고, 분류하고, 중요도를 매겨주는** 개인용 대시보드입니다.

**쉽게 말하면:** 매일 15개 이상의 뉴스 사이트를 돌아다니는 대신, 이 앱이 대신 해주고 중요한 것만 보여줍니다.

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| 자동 수집 | 15개 프리셋 소스에서 자동으로 뉴스 수집 (TechCrunch, The Verge, MIT Tech Review 등) |
| AI 요약 | 각 기사를 한국어 3줄로 요약 |
| 스마트 분류 | 도구/연구/트렌드/튜토리얼/비즈니스 카테고리로 자동 분류 |
| 중요도 점수 | 각 기사에 1~5개 별점 부여 |
| 감성 분석 | 각 기사를 긍정/중립/부정으로 분류 |
| 오늘의 브리핑 | 매일 "오늘의 AI 뉴스 TOP 5" 자동 생성 |
| 중복 병합 | 같은 뉴스를 여러 매체가 보도하면 1개로 합침 |
| 키워드 워치리스트 | 추적 키워드가 포함된 뉴스 하이라이트 (예: "Claude", "GPT") |
| 인앱 리더 | 광고 없이 대시보드 안에서 원문 읽기 |
| 다크모드 | 다크/라이트 테마 전환 |
| 내보내기 | 브리핑과 기사를 Markdown 또는 PDF로 다운로드 |
| 이미지 분석 | 뉴스 속 차트/인포그래픽을 AI가 분석 |
| 실시간 갱신 | 대시보드가 5분마다 자동으로 새로고침 |
| 타임라인 뷰 | 시간순으로 뉴스 보기 (오늘/어제/이번 주) |
| Context Caching | 시스템 프롬프트 캐싱으로 API 토큰 비용 최대 90% 절감 |
| 스마트 라우팅 | 단순 작업은 Flash-Lite, 고품질 작업은 Flash 자동 분기 |

---

## 화면 미리보기

앱을 실행하면 브라우저에서 `http://localhost:6601` 로 접속합니다:

- **브리핑 탭** - 오늘의 TOP 5 AI 뉴스 한눈에 보기
- **뉴스 목록 탭** - 수집된 모든 기사 + 필터 + 정렬
- **타임라인 탭** - 시간 기반 뉴스 흐름
- **소스 관리 탭** - 뉴스 소스 관리

---

## 시작하기 (완전 초보자용 단계별 가이드)

> **코딩 경험이 전혀 없어도 됩니다.** 각 단계를 차근차근 따라하세요.

### 1단계: Python 설치하기

Python은 이 앱을 실행하는 데 필요한 프로그래밍 언어입니다.

1. [python.org/downloads](https://www.python.org/downloads/) 에 접속
2. 큰 노란색 **"Download Python 3.xx"** 버튼 클릭
3. 다운로드된 파일 실행
4. **중요:** 설치 화면 하단의 **"Add Python to PATH"** 체크박스를 반드시 체크
5. **"Install Now"** 클릭

**설치 확인 방법:** 명령 프롬프트를 열고 (키보드에서 `Win + R` → `cmd` 입력 → Enter) 다음을 입력:
```
python --version
```
`Python 3.13.x` 같은 문구가 나오면 성공!

### 2단계: 프로젝트 다운로드

**방법 A: Git 사용 (추천)**

Git이 설치되어 있다면:
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**방법 B: 직접 다운로드**

1. [GitHub 저장소 페이지](https://github.com/sodam-ai/ai-news-radar) 접속
2. 초록색 **"Code"** 버튼 클릭
3. **"Download ZIP"** 클릭
4. ZIP 파일을 원하는 폴더에 압축 해제

### 3단계: 필요한 패키지 설치

명령 프롬프트를 열고, 프로젝트 폴더로 이동한 후 실행:
```
cd 프로젝트폴더경로\ai-news-radar
pip install -r requirements.txt
```

> **이게 뭐 하는 건가요?** 앱이 실행되는 데 필요한 도구(라이브러리)들을 자동으로 다운로드합니다. 약 1~2분 소요됩니다.

### 4단계: Gemini API 키 발급 (무료)

AI 기능을 사용하려면 Google Gemini API 키가 필요합니다. **완전 무료**입니다.

1. [aistudio.google.com/apikey](https://aistudio.google.com/apikey) 접속
2. Google 계정으로 로그인
3. **"Create API Key"** (API 키 만들기) 클릭
4. 생성된 키를 복사 (`AIzaSy...` 형태)

### 5단계: API 키 설정

1. 프로젝트 폴더에서 `.env.example` 파일을 찾으세요
2. 이 파일을 복사해서 이름을 `.env`로 변경하세요
3. `.env` 파일을 메모장 등 텍스트 편집기로 열어주세요
4. `your_gemini_api_key_here` 부분을 실제 API 키로 교체:

```
GEMINI_API_KEY=AIzaSy여기에실제키입력
```

5. 파일 저장

> **보안 주의:** `.env` 파일에는 비밀 API 키가 들어있습니다. 이 파일은 자동으로 GitHub 업로드에서 제외됩니다. 절대 다른 사람과 공유하지 마세요.

### 6단계: 앱 실행

```
streamlit run app.py
```

브라우저가 자동으로 **http://localhost:6601** 을 열어줍니다.

끝! AI News Radar가 실행되었습니다!

---

## 사용 방법

### 처음 사용할 때

1. 사이드바에서 **"수집"** 버튼 클릭 → 뉴스 수집
2. **"AI 처리"** 버튼 클릭 → 수집된 기사 AI 분석
3. **"브리핑 생성"** 클릭 → 오늘의 TOP 5 요약 생성

### 매일 사용할 때

앱은 60분마다 자동으로 뉴스를 수집합니다. 대시보드를 열고:

- **브리핑 탭**에서 빠르게 훑어보기
- **뉴스 목록**에서 자세히 읽기
- 사이드바 **필터**로 관심 카테고리/감성만 보기

### 기능별 가이드

| 하고 싶은 것 | 방법 |
|-------------|------|
| 뉴스 소스 추가 | 사이드바 > 소스 관리 > 이름과 RSS URL 입력 > "소스 추가" 클릭 |
| 키워드 추적 | 사이드바 > 키워드 워치리스트 > 키워드 입력 > "추가" 클릭 |
| 원문 읽기 | 기사 제목 클릭(새 탭) 또는 "자세히 보기" > "원문 가져오기" |
| PDF로 내보내기 | 브리핑 탭 또는 뉴스 탭 > "내보내기" > PDF 선택 |
| Markdown으로 내보내기 | 브리핑 탭 또는 뉴스 탭 > "내보내기" > Markdown 선택 |
| 다크/라이트 전환 | 사이드바 상단 토글 |
| 카테고리 필터 | 사이드바 > 필터 섹션 > 카테고리 선택 |
| 감성 필터 | 사이드바 > 필터 섹션 > 감성 선택 |
| 중요도 필터 | 사이드바 > 필터 섹션 > 슬라이더 조절 |

---

## 프로젝트 구조

```
ai-news-radar/
├── app.py                  # 메인 대시보드 (브라우저에 보이는 화면)
├── config.py               # 설정 (API 키, 수집 주기 등)
├── requirements.txt        # 필요한 패키지 목록
├── .env.example            # API 키 설정 템플릿
├── .env                    # 실제 API 키 (GitHub에 올라가지 않음)
├── LICENSE                 # MIT 라이선스 (SoDam AI Studio)
├── .streamlit/
│   └── config.toml         # 테마 및 포트 설정
├── crawler/                # 뉴스 수집
│   ├── rss_crawler.py      # RSS 피드에서 기사 수집
│   └── scheduler.py        # 자동 수집 스케줄러
├── ai/                     # AI 처리
│   ├── model_router.py     # 스마트 라우팅 + Context Caching
│   ├── batch_processor.py  # 배치 AI 처리 + 이미지 분석
│   ├── deduplicator.py     # 중복 뉴스 병합
│   └── briefing.py         # 오늘의 브리핑 TOP 5 생성
├── reader/
│   └── article_reader.py   # 광고 없는 원문 리더
├── export/
│   └── exporter.py         # Markdown/PDF 내보내기
├── data/
│   └── preset_sources.json # 15개 프리셋 뉴스 소스
├── utils/
│   └── helpers.py          # 유틸리티 함수
└── PRD/                    # 디자인 문서 (4개 파일)
```

---

## 문제 해결

| 문제 | 해결 방법 |
|------|----------|
| `pip` 명령어를 찾을 수 없음 | Python 재설치 시 "Add Python to PATH" 체크 |
| `streamlit` 명령어를 찾을 수 없음 | 실행: `pip install streamlit` |
| "GEMINI_API_KEY가 설정되지 않았습니다" 경고 | `.env` 파일을 만들었는지 확인 (`.env.example`이 아님) |
| 기사가 안 나옴 | "수집" 먼저 클릭, 그 다음 "AI 처리" 클릭 |
| 포트 6601이 이미 사용 중 | 다른 Streamlit을 종료하거나 `.streamlit/config.toml`에서 포트 변경 |
| PDF 내보내기 실패 | Windows 환경에서만 동작 (한글 지원을 위해 Windows 폰트 사용) |
| 기사 수집은 되는데 AI 분석 안 됨 | `.env` 파일의 GEMINI_API_KEY가 올바른지 확인 |
| 앱 시작 시 에러 | `pip install -r requirements.txt` 다시 실행하여 누락된 패키지 확인 |

---

## 무료 API 한도

AI News Radar는 Gemini 무료 티어로 **완전 무료** 운영 가능합니다:

| 모델 | 무료 한도 | 용도 |
|------|----------|------|
| Gemini Flash-Lite | 1,000회/일 | 분류, 태그, 감성 분석 |
| Gemini Flash | 250회/일 | 요약, 브리핑, 이미지 분석 |

스마트 라우팅 시스템이 단순 작업은 저렴한 모델로, 복잡한 작업은 고성능 모델로 자동 분배합니다.

---

## 로드맵

| Phase | 주요 기능 | 상태 |
|-------|----------|------|
| Phase 1 (MVP) | 수집 + AI 요약 + 대시보드 (17개 기능) | 완료 |
| Phase 2 | 채팅 + 음성 + 봇 + 팩트체크 + 게이미피케이션 (35개 기능) | 예정 |
| Phase 3 | 에이전트 + 예측 + 팟캐스트 + 플러그인 + 팀 모드 (19개 기능) | 예정 |

상세 로드맵은 [PRD/03_PHASES.md](./PRD/03_PHASES.md)를 참고하세요.

---

## 기술 스택

| 구성 요소 | 기술 | 선택 이유 |
|----------|------|----------|
| 언어 | Python 3.11+ | AI와 웹 크롤링에 최적의 생태계 |
| 대시보드 | Streamlit 2026 | Python만으로 웹 UI 구현 |
| AI | Google Gemini (Flash + Flash-Lite) | 무료 티어, 스마트 라우팅, Context Caching |
| 데이터 | 로컬 JSON 파일 | DB 서버 불필요 |
| 스케줄링 | APScheduler | cron 없이 앱 안에서 자동 수집 |
| PDF 내보내기 | fpdf2 | 경량 PDF 생성, 한글 폰트 지원 |

---

## 라이선스

MIT License - Copyright (c) 2026 **SoDam AI Studio**

자세한 내용은 [LICENSE](./LICENSE) 파일을 참고하세요.

---

*Streamlit + Google Gemini AI로 만들었습니다 — SoDam AI Studio*
