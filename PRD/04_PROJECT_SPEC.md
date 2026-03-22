# AI News Radar -- 프로젝트 스펙

> AI가 코드를 짤 때 지켜야 할 규칙과 절대 하면 안 되는 것.
> 이 문서를 AI에게 항상 함께 공유하세요.

---

## 기술 스택

| 영역 | 선택 | 이유 |
|------|------|------|
| 언어 | Python 3.11+ | 크롤링·AI 라이브러리가 가장 풍부 (feedparser, BeautifulSoup, LangChain 등) |
| 대시보드 | Streamlit (2026) | Python만으로 웹 UI 구현 가능, 2026 동적 컨테이너·위젯 바인딩 활용, 무료 호스팅 |
| 데이터 저장 | JSON 파일 → SQLite | 외부 DB 서버 불필요, 혼자 쓰니까 로컬 파일로 충분 |
| AI 요약 (고품질) | Gemini 2.5 Flash | 요약·브리핑·채팅 등 고품질 작업 (250회/일 무료) |
| AI 분류 (경량) | Gemini 2.5 Flash-Lite | 분류·태그·감성 등 단순 작업 (1000회/일 무료, 15 RPM) |
| AI 비용 최적화 | Gemini Context Caching | 시스템 프롬프트 캐싱으로 토큰 비용 90% 절감 |
| 크롤링 | feedparser + BeautifulSoup | RSS 파싱 + 웹 스크래핑 표준 라이브러리 |
| 스케줄러 | APScheduler | Python 내장 스케줄러, cron 없이 앱 안에서 동작 |
| 벡터 검색 | ChromaDB + Gemini Embedding 2 | 시맨틱 검색으로 AI 채팅 품질 대폭 향상 (Phase 2) |
| 뉴스레터 파싱 | imaplib + email (표준 라이브러리) | Gmail IMAP으로 뉴스레터 이메일 자동 수신·파싱 (Phase 2) |
| 노트 연동 | notion-client / obsidiantools | Notion API / Obsidian 폴더 직접 쓰기 (Phase 2) |
| 멀티 플랫폼 봇 | python-telegram-bot / discord.py / slack-bolt | 텔레그램·디스코드·슬랙에서 뉴스 소비 (Phase 2) |
| 뉴스레터 발행 | Resend API (무료 100통/일) | 수집된 뉴스로 자동 뉴스레터 생성·발송 (Phase 2) |
| 서버리스 자동화 | GitHub Actions (무료 2000분/월) | cron으로 수집+처리 자동화, 24시간 가동 불필요 (Phase 2) |
| 로컬 LLM | Ollama + Llama 3.3 | 오프라인 AI 처리, 무제한 요청, 데이터 외부 유출 제로 (Phase 2) |
| 팩트체크 | 자체 교차 검증 로직 | 중복 병합 데이터 활용한 뉴스 정확성 자동 검증 (Phase 2) |
| 에이전트 프레임워크 | MCP (Model Context Protocol) | 멀티 에이전트 자율 운영 표준 프로토콜 (Phase 3) |
| 소셜 포스팅 | tweepy / linkedin-api | X/LinkedIn 자동 게시 (Phase 3) |
| PWA | Service Worker + Manifest | Streamlit → PWA 변환, 모바일 앱 경험 (Phase 3) |
| 크롬 확장 | Manifest V3 + TypeScript | 웹 브라우징 중 글 수집 (Phase 3, 별도 프로젝트) |
| API 서버 (추후) | FastAPI + st.App (ASGI) | Streamlit 2026 실험적 ASGI로 하이브리드 구성 (Phase 3) |
| 배포 (추후) | Streamlit Cloud | GitHub 연결만으로 무료 배포 |

---

## 프로젝트 구조

```
ai-news-radar/
├── app.py                 # Streamlit 메인 앱 (대시보드)
├── config.py              # 설정 (API 키, 크롤링 주기 등)
├── crawler/
│   ├── __init__.py
│   ├── rss_crawler.py     # RSS 피드 수집
│   ├── web_crawler.py     # 웹 스크래핑 수집
│   └── scheduler.py       # 크롤링 스케줄러
├── ai/
│   ├── __init__.py
│   ├── batch_processor.py # Gemini 배치 처리 (요약+분류+중요도+감성+키워드 한번에)
│   ├── model_router.py    # 스마트 모델 라우팅 (Flash-Lite/Flash 분기) + Context Caching
│   ├── deduplicator.py    # 중복 뉴스 감지 + 병합
│   ├── briefing.py        # "오늘의 브리핑" TOP 5 자동 생성
│   ├── chat.py            # AI 뉴스 채팅 (ChromaDB 벡터 검색 기반 RAG) (Phase 2)
│   ├── vector_store.py    # ChromaDB + Gemini Embedding 2 관리 (Phase 2)
│   ├── learning.py        # AI 학습 필터링 (읽기 패턴 학습) (Phase 2)
│   ├── source_discover.py # 뉴스 소스 자동 발견 + 추천 (Phase 2)
│   ├── sentiment_agg.py   # 감성 온도계 시계열 집계 (Phase 2)
│   ├── fact_checker.py    # AI 팩트체크 교차 검증 (Phase 2)
│   ├── debate.py          # 뉴스 디베이트 찬반 시각 생성 (Phase 2)
│   ├── ollama_client.py   # Ollama 로컬 LLM 연동 (Phase 2)
│   ├── hybrid_router.py   # 하이브리드 LLM 3단계 라우팅 (Phase 2)
│   ├── quiz_generator.py  # AI 뉴스 퀴즈 자동 생성 (Phase 2)
│   ├── weekly_report.py   # 주간 인텔리전스 리포트 생성 (Phase 2)
│   ├── smart_alert.py     # 스마트 알림 (개인화 이유 포함) (Phase 2)
│   ├── competitor.py      # 경쟁사 모니터링 (Phase 2)
│   ├── glossary.py        # AI 용어 사전 자동 생성 (Phase 2)
│   ├── prediction.py      # AI 예측 엔진 + 검증 (Phase 3)
│   ├── ecosystem_map.py   # AI 생태계 맵 생성 (Phase 3)
│   ├── knowledge_graph.py # 뉴스 연결 지도 생성 (Phase 3)
│   ├── agent_system.py    # 멀티 에이전트 자율 운영 (MCP) (Phase 3)
│   ├── podcast_gen.py     # AI 팟캐스트 2인 토론 자동 생성 (Phase 3)
│   └── content_gen.py     # 뉴스 기반 블로그/소셜 콘텐츠 자동 생성 (Phase 3)
├── reader/
│   ├── __init__.py
│   └── article_reader.py  # 인앱 리더 뷰 (원문 추출 + 정제)
├── newsletter/
│   ├── __init__.py
│   └── email_parser.py    # 뉴스레터 이메일 수신 + 파싱 (Phase 2)
├── voice/
│   ├── __init__.py
│   └── tts_generator.py   # 음성 브리핑 생성 (edge-tts) (Phase 2)
├── bots/
│   ├── __init__.py
│   ├── telegram_bot.py    # 텔레그램 봇 (Phase 2)
│   ├── discord_bot.py     # 디스코드 봇 (Phase 2)
│   ├── slack_bot.py       # 슬랙 봇 (Phase 2)
│   ├── bot_core.py        # 봇 공통 로직 (명령 처리, 응답 포맷팅)
│   └── social_poster.py   # X/LinkedIn 자동 소셜 포스팅 (Phase 3)
├── export/
│   ├── __init__.py
│   ├── exporter.py        # Markdown/PDF 내보내기
│   ├── notion_export.py   # Notion DB 내보내기 + AI 자동 태깅 (Phase 2)
│   └── obsidian_export.py # Obsidian 폴더 내보내기 + 관련 노트 연결 (Phase 2)
├── data/
│   ├── preset_sources.json # 기본 프리셋 소스 15개 (읽기 전용)
│   ├── sources.json       # 등록된 뉴스 소스 목록
│   ├── articles.json      # 수집된 기사 데이터
│   ├── watchlist.json     # 키워드 워치리스트
│   ├── bookmarks.json     # 북마크 데이터 (Phase 2)
│   ├── reading_log.json   # 읽기 로그 (Phase 2)
│   ├── user_pref.json     # AI 학습 데이터 (Phase 2)
│   ├── chat_sessions.json # AI 채팅 기록 (Phase 2)
│   ├── source_recs.json   # 소스 추천 목록 (Phase 2)
│   ├── sentiment_timeline.json # 감성 온도계 시계열 (Phase 2)
│   ├── newsletters.json   # 발행된 뉴스레터 기록 (Phase 2)
│   ├── bot_config.json    # 봇 설정 (텔레그램/디스코드/슬랙) (Phase 2)
│   ├── chroma/            # ChromaDB 벡터 저장소 (Phase 2)
│   ├── gamification.json  # 게이미피케이션 데이터 (Phase 2)
│   ├── quizzes.json       # AI 뉴스 퀴즈 (Phase 2)
│   ├── weekly_reports/    # 주간 인텔리전스 리포트 PDF (Phase 2)
│   ├── competitors.json   # 경쟁사 추적 목록 (Phase 2)
│   ├── glossary.json      # AI 용어 사전 (Phase 2)
│   ├── predictions.json   # AI 예측 기록 (Phase 3)
│   ├── ecosystem.json     # AI 생태계 맵 데이터 (Phase 3)
│   ├── team_comments.json # 팀 코멘트/투표 (Phase 3)
│   ├── generated/         # AI 자동 생성 콘텐츠 (Phase 3)
│   ├── podcast/           # AI 팟캐스트 에피소드 (Phase 3)
│   ├── plugins/           # 커뮤니티 플러그인 폴더 (Phase 3)
│   └── audio/             # 음성 브리핑 파일 폴더 (Phase 2)
├── utils/
│   ├── __init__.py
│   └── helpers.py         # 유틸리티 함수
├── .env                   # 환경변수 (API 키)
├── requirements.txt       # 의존성 목록
└── README.md              # 프로젝트 설명
```

---

## 절대 하지 마 (DO NOT)

> AI에게 코드를 시킬 때 이 목록을 반드시 함께 공유하세요.

- [ ] API 키를 코드에 직접 쓰지 마 (.env 파일 사용, python-dotenv로 로드)
- [ ] 외부 DB 서버(Supabase, PostgreSQL 등)를 연결하지 마 — 로컬 JSON/SQLite만 사용
- [ ] 로그인/인증 기능을 추가하지 마 — 개인용이라 불필요
- [ ] 목업/하드코딩 데이터로 완성이라고 하지 마 — 실제 RSS 피드와 실제 Gemini API 연동
- [ ] requirements.txt의 기존 의존성 버전을 임의로 변경하지 마
- [ ] data/ 폴더의 JSON 파일 구조를 사전 협의 없이 변경하지 마
- [ ] 불필요한 외부 라이브러리를 추가하지 마 — 표준 라이브러리로 가능하면 표준 사용
- [ ] Streamlit 외의 프론트엔드 프레임워크를 도입하지 마 (React, Vue 등)

---

## 항상 해 (ALWAYS DO)

- [ ] 변경하기 전에 계획을 먼저 보여줘
- [ ] 환경변수는 .env 파일에 저장하고 python-dotenv로 로드
- [ ] 에러가 발생하면 사용자에게 친절한 메시지 표시 (트레이스백 그대로 보여주지 마)
- [ ] 크롤링 시 rate limiting 존중 (서버에 부담 주지 않기)
- [ ] JSON 파일 읽기/쓰기 시 파일 깨짐 방지 (임시 파일 → rename 패턴)
- [ ] 중복 글 체크 (같은 URL의 글을 다시 수집하지 않기)
- [ ] Gemini API 호출 실패 시 재시도 로직 (최대 3회)
- [ ] 수집한 데이터의 인코딩 처리 (UTF-8 통일)
- [ ] Gemini Context Caching 활성화 (시스템 프롬프트 캐싱으로 비용 절감)
- [ ] 모델 라우팅: 단순 작업은 Flash-Lite, 고품질 작업은 Flash로 분기

---

## 테스트 방법

```bash
# 로컬 실행
streamlit run app.py --server.port 6601

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일에 GEMINI_API_KEY 입력
```

---

## 배포 방법 (Phase 1에서는 로컬만)

```bash
# 로컬 실행
streamlit run app.py --server.port 6601

# 추후 공개 시: Streamlit Cloud
# 1. GitHub에 코드 push
# 2. share.streamlit.io에서 연결
# 3. Secrets에 API 키 등록
```

---

## 환경변수

| 변수명 | 설명 | 어디서 발급 |
|--------|------|------------|
| GEMINI_API_KEY | Google Gemini API 키 (Flash + Flash-Lite 공용) | https://aistudio.google.com/apikey |
| IMAP_EMAIL | 뉴스레터 수신용 이메일 (Phase 2) | Gmail 계정 |
| IMAP_PASSWORD | 이메일 앱 비밀번호 (Phase 2) | Google 앱 비밀번호 설정 |
| NOTION_API_KEY | Notion 연동 API 키 (Phase 2) | https://www.notion.so/my-integrations |
| NOTION_DATABASE_ID | Notion 내보내기 대상 DB ID (Phase 2) | Notion DB URL에서 추출 |
| OBSIDIAN_VAULT_PATH | Obsidian 볼트 경로 (Phase 2) | 로컬 경로 직접 입력 |
| TELEGRAM_BOT_TOKEN | 텔레그램 봇 토큰 (Phase 2) | @BotFather에서 발급 |
| TELEGRAM_CHAT_ID | 텔레그램 알림 수신 채팅 ID (Phase 2) | @userinfobot에서 확인 |
| DISCORD_BOT_TOKEN | 디스코드 봇 토큰 (Phase 2) | Discord Developer Portal |
| DISCORD_CHANNEL_ID | 디스코드 알림 채널 ID (Phase 2) | 서버 설정에서 확인 |
| SLACK_BOT_TOKEN | 슬랙 봇 토큰 (Phase 2) | Slack API에서 발급 |
| SLACK_CHANNEL_ID | 슬랙 알림 채널 ID (Phase 2) | 채널 설정에서 확인 |
| RESEND_API_KEY | 뉴스레터 발송 API 키 (Phase 2) | https://resend.com |
| OLLAMA_HOST | Ollama 서버 주소 (Phase 2, 기본: localhost:11434) | 로컬 설치 |
| OLLAMA_MODEL | 사용할 로컬 모델 (Phase 2, 기본: llama3.3) | Ollama 모델 목록 |
| X_API_KEY | X/Twitter API 키 (Phase 3) | https://developer.x.com |
| X_API_SECRET | X/Twitter API Secret (Phase 3) | https://developer.x.com |
| LINKEDIN_ACCESS_TOKEN | LinkedIn API 토큰 (Phase 3) | LinkedIn Developer |

> .env 파일에 저장. 절대 GitHub에 올리지 마세요.
> .gitignore에 .env 추가 필수.

---

## [NEEDS CLARIFICATION]

- [ ] Streamlit Cloud 배포 시 APScheduler가 정상 동작하는지 확인 필요
- [ ] JSON 파일 크기가 커지면 SQLite 전환 시점 결정 필요
- [ ] st.App (ASGI) 실험적 기능의 안정성 확인 필요 (Phase 3)
- [ ] Gmail IMAP 접근을 위한 앱 비밀번호 설정 방법 문서화 필요 (Phase 2)
- [ ] Notion API 무료 한도 확인 필요 (Phase 2)
- [ ] Gemini Context Caching TTL(유효기간) 최적값 결정 필요
- [ ] edge-tts 한국어 음성 품질 테스트 필요 (Phase 2)
- [ ] AI 채팅에서 참조할 뉴스 검색 범위 (최근 7일? 30일?) 결정 필요 (Phase 2)
- [ ] Plotly/Pyvis Knowledge Graph 렌더링 성능 한계 테스트 필요 (Phase 3)
