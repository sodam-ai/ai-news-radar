# AI News Radar -- 데이터 모델

> 이 문서는 앱에서 다루는 핵심 데이터의 구조를 정의합니다.
> 개발자가 아니어도 이해할 수 있는 "개념적 ERD"입니다.
> 저장 방식: JSON 파일 / SQLite (로컬 저장)

---

## 전체 구조

```
[Source] --1:N--> [Article] --1:1--> [Summary]
                     |
                     ├──N:N--> [Category]
                     |
                     ├──0:N--> [Tag]
                     |
                     ├──0:1--> [Bookmark] --0:1--> [NoteExport]
                     |
                     └──0:N--> [ReadingLog]

[NewsletterSource] --is a--> [Source] (뉴스레터 전용 확장)

[AlertSetting] -- 알림 설정 (독립)
[Watchlist] -- 키워드 워치리스트 (독립)
[DailyBriefing] --1:0..1--> [AudioBriefing] (음성 버전)
[ChatSession] --0:N--> [ChatMessage] (AI 채팅)
[TrendReport] -- 주간/월간 자동 생성 (독립)
[UserPreference] -- AI 학습 데이터 (독립)
[SourceRecommendation] -- AI가 발견한 새 소스 추천 (독립)
[SentimentTimeline] -- 감성 온도계 시계열 데이터 (독립)
[Newsletter] -- 자동 생성된 뉴스레터 (독립)
[BotConfig] -- 텔레그램/디스코드/슬랙 봇 설정 (독립)
[FactCheck] -- 뉴스 팩트체크 결과 (Article에 연결)
[Debate] -- 뉴스 디베이트 찬반 시각 (Article에 연결)
[AgentLog] -- 멀티 에이전트 실행 로그 (독립)
[SocialPost] -- 자동 소셜 포스팅 기록 (독립)
[UserGamification] -- 게이미피케이션 (스트릭, 레벨, 배지)
[Quiz] -- AI 뉴스 퀴즈 (Article에서 자동 생성)
[WeeklyReport] -- 주간 인텔리전스 리포트
[Prediction] -- AI 예측 + 검증 결과
[EcosystemEntity] --N:N--> [EcosystemEntity] (AI 생태계 맵)
[CompetitorWatch] -- 경쟁사 모니터링 추적 목록
[GlossaryTerm] -- AI 용어 사전
[PodcastEpisode] -- AI 팟캐스트 에피소드
[Plugin] -- 플러그인 등록 정보
[TeamComment] -- 팀 협업 코멘트/투표
[GeneratedContent] -- AI 자동 생성 콘텐츠
```

---

## 엔티티 상세

### Source (뉴스 소스)
내가 등록한 RSS 피드나 웹사이트. "어디서 뉴스를 가져올지" 정의.

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 고유 식별자 (자동 생성) | src_001 | O |
| name | 소스 이름 | TechCrunch AI | O |
| url | RSS 피드 또는 웹 URL | https://techcrunch.com/feed/ | O |
| type | 소스 유형 | rss / web | O |
| is_preset | 기본 프리셋 소스 여부 | true | O |
| crawl_interval | 수집 주기 (분) | 60 | O |
| is_active | 활성 여부 | true | O |
| last_crawled_at | 마지막 수집 시각 | 2026-03-22T09:00:00 | X |
| created_at | 등록 날짜 | 2026-03-22 | O |

### Article (뉴스 글)
수집된 개별 뉴스 기사. 원문 정보 + AI 처리 결과 포함.

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 고유 식별자 (자동 생성) | art_001 | O |
| source_id | 어느 소스에서 왔는지 | src_001 | O |
| title | 글 제목 | "GPT-5 출시 발표" | O |
| url | 원문 링크 | https://... | O |
| content | 원문 내용 (크롤링) | (본문 텍스트) | X |
| category | AI 분류 결과 | ai_tool | O |
| importance | AI 중요도 점수 (1~5) | 5 | O |
| sentiment | AI 감성 분석 결과 | positive / negative / neutral | O |
| sentiment_reason | 감성 판단 근거 (한 줄) | "새 모델 성능 향상에 대한 긍정적 평가" | X |
| tags | AI가 추출한 태그 | ["GPT-5", "OpenAI"] | X |
| image_urls | 뉴스 속 이미지 URL 목록 | ["https://...chart.png"] | X |
| image_analysis | Gemini 멀티모달 이미지 분석 결과 | "벤치마크 차트: 수학 95점, 코딩 92점" | X |
| embedding_id | ChromaDB 벡터 ID (시맨틱 검색용) | "emb_art_001" | X |
| fact_score | AI 팩트체크 점수 (0~1) | 0.85 | X |
| fact_sources | 교차 확인된 매체 수 | 3 | X |
| cluster_id | 중복 뉴스 그룹 ID (같은 뉴스끼리 같은 ID) | clst_001 | X |
| is_primary | 중복 그룹에서 대표 글인지 | true | O |
| related_articles | 같은 뉴스를 보도한 다른 매체 정보 (URL + 제목 + 매체명 + 요약) | [{url, title, source, summary}] | X |
| published_at | 원문 발행일 | 2026-03-21 | O |
| crawled_at | 수집 시각 | 2026-03-22T09:00:00 | O |
| is_read | 읽었는지 여부 | false | O |

### Summary (AI 요약)
AI가 생성한 글 요약. 글 1개당 요약 1개.

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| article_id | 어떤 글의 요약인지 | art_001 | O |
| short_summary | 핵심 3줄 요약 | "OpenAI가 GPT-5를 발표..." | O |
| key_points | 핵심 포인트 목록 | ["성능 2배 향상", "가격 30% 인하"] | X |
| language | 요약 언어 | ko | O |
| created_at | 요약 생성 시각 | 2026-03-22T09:01:00 | O |

### Category (카테고리)
뉴스 분류 기준. 미리 정의된 카테고리 목록.

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 카테고리 ID | ai_tool | O |
| name | 표시 이름 | AI 도구/제품 | O |
| description | 설명 | 새 AI 도구 출시, 업데이트 소식 | O |

**기본 카테고리:**
- `ai_tool` — AI 도구/제품 (ChatGPT, Claude, Midjourney 등)
- `ai_research` — AI 논문/연구
- `ai_trend` — 업계 트렌드/동향
- `ai_tutorial` — 활용법/튜토리얼
- `ai_business` — AI 비즈니스/투자
- `ai_other` — 기타

### Bookmark (북마크)
중요한 글을 저장하고 메모를 추가. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| article_id | 북마크한 글 | art_001 | O |
| memo | 메모 | "팀에 공유할 것" | X |
| created_at | 북마크 시각 | 2026-03-22 | O |

### AlertSetting (알림 설정)
어떤 알림을 언제 받을지 설정. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| type | 알림 유형 | realtime / daily / weekly | O |
| categories | 알림 받을 카테고리 | ["ai_tool", "ai_trend"] | O |
| time | 정기 알림 시각 | 08:00 | X |
| is_active | 활성 여부 | true | O |

### Watchlist (키워드 워치리스트)
내가 추적하는 관심 키워드. 해당 키워드가 포함된 뉴스가 하이라이트 표시됨.

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| keyword | 추적 키워드 | Claude | O |
| is_active | 활성 여부 | true | O |
| created_at | 등록 시각 | 2026-03-22 | O |

### DailyBriefing (오늘의 브리핑)
매일 자동 생성되는 "오늘 꼭 봐야 할 AI 뉴스 TOP 5" 요약.

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 브리핑 ID | brf_20260322 | O |
| date | 브리핑 날짜 | 2026-03-22 | O |
| top_articles | TOP 5 기사 ID + 한줄 요약 | [{id: "art_001", headline: "..."}] | O |
| summary | 오늘의 AI 동향 총평 | "오늘은 LLM 신모델 발표가..." | O |
| created_at | 생성 시각 | 2026-03-22T07:00:00 | O |

### TrendReport (트렌드 리포트)
주간/월간 자동 생성되는 AI 트렌드 분석. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 리포트 ID | rpt_001 | O |
| period | 분석 기간 | weekly / monthly | O |
| start_date | 시작일 | 2026-03-15 | O |
| end_date | 종료일 | 2026-03-22 | O |
| top_keywords | 상위 키워드 | ["GPT-5", "Agent", "MCP"] | O |
| top_articles | 주요 기사 ID 목록 | ["art_001", "art_015"] | O |
| insights | AI 분석 요약 | "이번 주 AI 에이전트 관련 논문이..." | O |
| created_at | 생성 시각 | 2026-03-22 | O |

### NewsletterSource (뉴스레터 소스)
RSS가 없는 AI 뉴스레터를 이메일로 받아 자동 수집. Source의 확장. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| source_id | 연결된 Source ID | src_016 | O |
| email_address | 뉴스레터 수신용 이메일 | radar-inbox@gmail.com | O |
| sender_filter | 발신자 이메일 필터 | newsletter@deeplearning.ai | O |
| subject_pattern | 제목 패턴 (정규식) | "The Batch.*" | X |
| parse_method | 파싱 방식 | html / text / auto | O |
| last_parsed_at | 마지막 파싱 시각 | 2026-03-22T09:00:00 | X |

### NoteExport (노트 앱 내보내기)
북마크한 글을 Notion/Obsidian으로 내보낸 기록. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 내보내기 ID | exp_001 | O |
| article_id | 내보낸 기사 | art_001 | O |
| target | 내보내기 대상 | notion / obsidian / markdown | O |
| target_url | 내보낸 위치 (Notion 페이지 URL 등) | https://notion.so/... | X |
| exported_at | 내보낸 시각 | 2026-03-22T10:00:00 | O |

### ReadingLog (읽기 로그)
사용자의 읽기 패턴을 기록. AI 학습 필터링의 기반 데이터. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| article_id | 읽은/무시한 기사 | art_001 | O |
| action | 사용자 행동 | read / skipped / bookmarked / exported | O |
| time_spent | 읽은 시간 (초) | 45 | X |
| scroll_depth | 스크롤 깊이 (%) | 80 | X |
| timestamp | 행동 시각 | 2026-03-22T08:30:00 | O |

### UserPreference (AI 학습 데이터)
읽기 로그를 기반으로 AI가 학습한 사용자 선호도. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| preferred_categories | 선호 카테고리 가중치 | {"ai_tool": 0.8, "ai_research": 0.6} | O |
| preferred_sources | 선호 소스 가중치 | {"src_001": 0.9, "src_003": 0.7} | O |
| preferred_keywords | 관심 키워드 가중치 | {"Claude": 0.95, "Agent": 0.8} | O |
| disliked_patterns | 무시 패턴 | ["sponsored", "listicle"] | X |
| model_version | 학습 모델 버전 | v1 | O |
| last_updated | 마지막 학습 시각 | 2026-03-22T00:00:00 | O |

### ChatSession (AI 채팅 세션)
수집된 뉴스에 대해 AI와 대화한 기록. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 세션 ID | chat_001 | O |
| title | 대화 제목 (자동 생성) | "Claude 관련 뉴스 요약" | O |
| created_at | 세션 시작 시각 | 2026-03-22T10:00:00 | O |

### ChatMessage (채팅 메시지)
AI 채팅 세션의 개별 메시지. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| session_id | 속한 세션 | chat_001 | O |
| role | 발신자 | user / assistant | O |
| content | 메시지 내용 | "이번 주 Claude 관련 뉴스 요약해줘" | O |
| referenced_articles | 참조된 기사 ID 목록 | ["art_001", "art_015"] | X |
| timestamp | 메시지 시각 | 2026-03-22T10:00:05 | O |

### AudioBriefing (음성 브리핑)
매일 브리핑을 AI 음성으로 변환한 오디오 파일. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| briefing_id | 연결된 DailyBriefing ID | brf_20260322 | O |
| audio_path | 음성 파일 경로 | data/audio/brf_20260322.mp3 | O |
| duration | 재생 시간 (초) | 120 | O |
| voice | 사용된 음성 | ko-KR-SunHiNeural | O |
| created_at | 생성 시각 | 2026-03-22T07:01:00 | O |

### SourceRecommendation (소스 자동 추천)
AI가 사용자 관심사 기반으로 발견한 새로운 뉴스 소스 추천. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 추천 ID | rec_001 | O |
| name | 추천 소스 이름 | "Simon Willison's Weblog" | O |
| url | 소스 URL | https://simonwillison.net/atom/everything/ | O |
| reason | 추천 이유 | "Claude, LLM 관련 글이 자주 올라오는 블로그" | O |
| match_score | 관심사 매칭 점수 (0~1) | 0.92 | O |
| status | 상태 | pending / accepted / dismissed | O |
| created_at | 추천 생성 시각 | 2026-03-22T00:00:00 | O |

### UserGamification (게이미피케이션)
사용자의 뉴스 읽기 습관 게임화 데이터. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| level | 현재 레벨 | 7 | O |
| xp | 경험치 | 1250 | O |
| streak_days | 연속 읽기 일수 | 14 | O |
| longest_streak | 최장 연속 기록 | 21 | O |
| badges | 획득한 배지 목록 | ["first_read", "7day_streak", "quiz_master"] | O |
| quiz_correct | 퀴즈 정답 수 | 45 | O |
| quiz_total | 퀴즈 총 문제 수 | 60 | O |
| last_active | 마지막 활동일 | 2026-03-22 | O |

### Quiz (AI 뉴스 퀴즈)
AI가 뉴스에서 자동 생성한 퀴즈. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 퀴즈 ID | quiz_001 | O |
| article_id | 출처 기사 | art_001 | O |
| question | 질문 | "GPT-5의 수학 벤치마크 점수는?" | O |
| options | 보기 4개 | ["85점", "90점", "95점", "99점"] | O |
| answer | 정답 인덱스 | 2 | O |
| difficulty | 난이도 | easy / medium / hard | O |
| created_at | 생성 시각 | 2026-03-22T07:00:00 | O |

### WeeklyReport (주간 인텔리전스 리포트)
매주 자동 생성되는 AI 업계 인텔리전스 리포트. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 리포트 ID | wr_20260322 | O |
| week_start | 주 시작일 | 2026-03-16 | O |
| week_end | 주 종료일 | 2026-03-22 | O |
| top_trends | 핵심 트렌드 3개 | [{topic, summary, articles}] | O |
| predictions | 다음 주 예측 | ["에이전트 관련 발표 예상", ...] | O |
| action_items | 행동 제안 | ["Claude 4 업데이트 주시", ...] | O |
| pdf_path | PDF 파일 경로 | data/reports/wr_20260322.pdf | O |
| created_at | 생성 시각 | 2026-03-22T06:00:00 | O |

### Prediction (AI 예측)
AI가 트렌드 분석으로 생성한 예측 + 검증 결과. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 예측 ID | pred_001 | O |
| topic | 예측 주제 | "MCP가 2주 내 주요 프레임워크에 통합될 것" | O |
| confidence | 확신도 (0~1) | 0.75 | O |
| predicted_at | 예측 시각 | 2026-03-22 | O |
| verify_by | 검증 예정일 | 2026-04-05 | O |
| result | 검증 결과 | correct / partially / wrong / pending | O |
| evidence | 검증 근거 기사 ID | ["art_120", "art_135"] | X |

### EcosystemEntity (AI 생태계 엔티티)
AI 생태계 맵의 노드 — 기업/기술/인물. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 엔티티 ID | eco_001 | O |
| name | 이름 | OpenAI | O |
| type | 유형 | company / technology / person / product | O |
| description | 한 줄 설명 | "GPT 시리즈 개발사" | O |
| related_entities | 관련 엔티티 ID + 관계 유형 | [{id: "eco_002", relation: "투자"}] | X |
| mention_count | 뉴스 언급 횟수 | 142 | O |
| last_mentioned | 마지막 언급일 | 2026-03-22 | O |

### CompetitorWatch (경쟁사 모니터링)
추적 중인 AI 기업/제품 목록. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 추적 ID | cw_001 | O |
| name | 기업/제품명 | OpenAI | O |
| keywords | 추적 키워드 | ["OpenAI", "GPT-5", "Sam Altman"] | O |
| summary_schedule | 요약 주기 | daily / weekly | O |
| last_summary | 마지막 요약 내용 | "이번 주 GPT-5 베타 출시..." | X |
| is_active | 활성 여부 | true | O |

### GlossaryTerm (AI 용어 사전)
뉴스에서 자동 추출된 AI 전문 용어와 설명. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| term | 용어 | MCP | O |
| definition | 쉬운 설명 | "AI 앱들이 데이터에 접근하는 표준 방식 (USB-C처럼)" | O |
| category | 분류 | protocol / model / technique / company | O |
| first_seen | 처음 등장일 | 2026-03-15 | O |
| mention_count | 뉴스 언급 횟수 | 28 | O |
| related_articles | 관련 기사 ID | ["art_001", "art_015"] | X |

### PodcastEpisode (AI 팟캐스트 에피소드)
AI 호스트 2명이 뉴스를 토론하는 팟캐스트 에피소드. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 에피소드 ID | pod_20260322 | O |
| title | 에피소드 제목 | "오늘의 AI 뉴스: GPT-5 발표의 의미" | O |
| script | 대화 스크립트 | [{host: "A", text: "오늘 큰 뉴스가..."}, ...] | O |
| audio_path | 오디오 파일 경로 | data/podcast/pod_20260322.mp3 | O |
| duration | 재생 시간 (초) | 300 | O |
| article_ids | 다룬 기사 ID 목록 | ["art_001", "art_015"] | O |
| created_at | 생성 시각 | 2026-03-22T07:00:00 | O |

### Plugin (플러그인)
커뮤니티가 개발한 확장 플러그인 등록 정보. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 플러그인 ID | plg_001 | O |
| name | 플러그인 이름 | "Reddit AI 소스 어댑터" | O |
| type | 유형 | source_adapter / analyzer / exporter / ui_widget | O |
| version | 버전 | 1.0.0 | O |
| author | 개발자 | "community_dev" | O |
| entry_point | 진입점 파일 | plugins/reddit_adapter.py | O |
| is_active | 활성 여부 | true | O |
| installed_at | 설치 시각 | 2026-03-22 | O |

### TeamComment (팀 협업 코멘트)
팀원이 뉴스에 남긴 코멘트/태그/투표. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 코멘트 ID | tc_001 | O |
| article_id | 대상 기사 | art_001 | O |
| user_name | 작성자 | "김개발" | O |
| type | 유형 | comment / tag / upvote / downvote | O |
| content | 내용 | "팀 미팅에서 공유할 것!" | X |
| created_at | 작성 시각 | 2026-03-22T10:00:00 | O |

### GeneratedContent (AI 자동 생성 콘텐츠)
뉴스 기반으로 AI가 자동 작성한 블로그/소셜 콘텐츠. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 콘텐츠 ID | gc_001 | O |
| type | 유형 | blog_post / tweet_thread / linkedin_post | O |
| title | 제목 | "이번 주 AI 트렌드 3가지" | O |
| content | 본문 | (마크다운 또는 텍스트) | O |
| source_articles | 기반 기사 ID | ["art_001", "art_015", "art_023"] | O |
| tone | 톤앤매너 | professional / casual / technical | O |
| status | 상태 | draft / reviewed / published | O |
| created_at | 생성 시각 | 2026-03-22T11:00:00 | O |

### FactCheck (팩트체크 결과)
AI가 뉴스의 정확성을 교차 검증한 결과. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| article_id | 검증한 기사 | art_001 | O |
| claims | 추출된 주요 주장 목록 | ["GPT-5는 수학 95점 달성"] | O |
| verified_claims | 다른 매체에서 확인된 주장 | ["GPT-5는 수학 95점 달성 ✅ (3개 매체)"] | O |
| unverified_claims | 미확인 주장 | ["가격이 50% 인하될 예정 ⚠️ (1개 매체)"] | X |
| overall_score | 전체 신뢰도 점수 (0~1) | 0.85 | O |
| created_at | 검증 시각 | 2026-03-22T09:05:00 | O |

### Debate (뉴스 디베이트)
AI가 뉴스에 대해 생성한 찬반 시각. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| article_id | 디베이트 대상 기사 | art_001 | O |
| topic | 논쟁 주제 | "AI 규제가 혁신을 저해하는가?" | O |
| pro_arguments | 찬성 근거 목록 (3개) | ["안전성 확보", "사회적 합의", ...] | O |
| con_arguments | 반대 근거 목록 (3개) | ["혁신 속도 저하", "경쟁력 약화", ...] | O |
| created_at | 생성 시각 | 2026-03-22T09:06:00 | O |

### AgentLog (에이전트 실행 로그)
멀티 에이전트 시스템의 실행 기록. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 로그 ID | log_001 | O |
| agent_name | 에이전트 이름 | collector / analyzer / judge / distributor | O |
| action | 수행한 작업 | "RSS 수집 완료 (15개 소스, 42개 새 글)" | O |
| status | 상태 | success / failed / retrying | O |
| duration | 소요 시간 (초) | 12.5 | O |
| timestamp | 실행 시각 | 2026-03-22T09:00:00 | O |

### SocialPost (소셜 포스팅 기록)
자동 생성된 소셜 미디어 포스트 기록. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 포스트 ID | sp_001 | O |
| article_id | 원본 기사 | art_001 | O |
| platform | 플랫폼 | x / linkedin / blog | O |
| content | 포스트 내용 | "🔥 GPT-5 출시! 주요 변경점..." | O |
| posted_at | 게시 시각 | 2026-03-22T10:00:00 | X |
| status | 상태 | draft / posted / failed | O |

### SentimentTimeline (감성 온도계)
시간별 감성 분석 집계. "AI 업계 분위기" 시각화 데이터. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| date | 집계 날짜 | 2026-03-22 | O |
| hour | 집계 시간 (0~23) | 9 | X |
| positive_count | 긍정 뉴스 수 | 15 | O |
| negative_count | 부정 뉴스 수 | 5 | O |
| neutral_count | 중립 뉴스 수 | 10 | O |
| score | 감성 점수 (-1 ~ +1) | 0.33 | O |
| top_positive_keyword | 가장 긍정적인 키워드 | "성능 향상" | X |
| top_negative_keyword | 가장 부정적인 키워드 | "일자리 대체" | X |

### Newsletter (자동 뉴스레터)
수집된 뉴스로 자동 생성된 주간 AI 뉴스레터. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| id | 뉴스레터 ID | nl_20260322 | O |
| title | 뉴스레터 제목 | "이번 주 AI 소식 TOP 10" | O |
| html_content | HTML 본문 | (렌더링된 이메일 본문) | O |
| article_ids | 포함된 기사 ID 목록 | ["art_001", "art_015"] | O |
| sent_to | 수신자 이메일 목록 | ["team@example.com"] | X |
| sent_at | 발송 시각 | 2026-03-22T08:00:00 | X |
| created_at | 생성 시각 | 2026-03-22T07:30:00 | O |

### BotConfig (멀티 플랫폼 봇 설정)
텔레그램/디스코드/슬랙 봇 연동 설정. (Phase 2)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| platform | 플랫폼 | telegram / discord / slack | O |
| token | 봇 토큰 | (암호화 저장) | O |
| chat_id | 알림 수신 채널/채팅 ID | -1001234567890 | O |
| features | 활성화된 기능 | ["briefing", "chat", "alert"] | O |
| schedule | 자동 브리핑 스케줄 | "08:00" | X |
| is_active | 활성 여부 | true | O |

### NewsGraph (뉴스 연결 관계)
뉴스 간의 관계를 저장. Knowledge Graph의 기반 데이터. (Phase 3)

| 필드 | 설명 | 예시 | 필수 |
|------|------|------|------|
| source_article_id | 출발 기사 | art_001 | O |
| target_article_id | 도착 기사 | art_015 | O |
| relation_type | 관계 유형 | causes / follows / related / contradicts | O |
| strength | 관계 강도 (0~1) | 0.85 | O |
| created_at | 생성 시각 | 2026-03-22T09:00:00 | O |

---

## 관계

- Source 1개에 여러 Article이 수집될 수 있음
- NewsletterSource는 Source를 확장 (뉴스레터 전용 필드 추가)
- Article 1개에 Summary 1개가 생성됨
- Article 1개는 Category 1개에 속함
- Article 1개에 여러 Tag가 붙을 수 있음
- Article 1개에 Bookmark이 0개 또는 1개 있을 수 있음
- Bookmark 1개에 NoteExport가 0개 또는 여러 개 있을 수 있음 (여러 곳에 내보내기 가능)
- Article 1개에 여러 ReadingLog가 쌓일 수 있음 (읽기/스킵/북마크 등 행동별)
- ReadingLog 데이터가 UserPreference 학습의 입력 데이터로 사용됨
- DailyBriefing 1개에 AudioBriefing이 0개 또는 1개 있을 수 있음
- ChatSession 1개에 여러 ChatMessage가 포함됨
- ChatMessage는 여러 Article을 참조할 수 있음
- NewsGraph는 Article 간의 관계를 저장 (양방향 그래프)

---

## 왜 이 구조인가

- **로컬 JSON/SQLite 중심**: 혼자 쓰는 앱이라 외부 DB 서버가 불필요. JSON 파일이면 시작하기 쉽고, 데이터가 많아지면 SQLite로 전환 가능
- **확장성**: Source-Article-Summary 구조가 유지되므로 Phase 2(알림), Phase 3(트렌드 분석) 추가 시 기존 데이터 구조를 깨지 않고 확장 가능
- **단순성**: 로그인이 없으므로 User 테이블 불필요. 북마크·읽음 표시도 단일 사용자 기준

---

## [NEEDS CLARIFICATION]

- [ ] JSON → SQLite 전환 시점 기준 (글 몇 개 이상이면 전환할지)
- [ ] 크롤링한 원문 content의 저장 범위 (전체 vs 앞부분만)
