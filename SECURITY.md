# 🔐 Security Policy — AI News Radar

본 프로젝트는 **OWASP ASVS v4.0.3 Level 1** 및 **Secure by Design** 원칙을 기준으로 운영됩니다. 보안은 선택이 아닌 핵심 요구사항입니다.

---

## 지원 버전

| 버전 | 상태 | 보안 패치 |
|------|------|-----------|
| v1.5.0 | ✅ 현재 | ✅ |
| v1.4.0 | ⚠️ 권장 안 됨 | ❌ — v1.5.0로 업그레이드 |
| v1.3.0 이하 | 🛑 지원 종료 | ❌ |

---

## 취약점 신고

보안 취약점을 발견하셨다면 **공개 이슈로 등록하지 마시고** 아래 경로로 신고해 주세요:

- **이메일:** startmxk@gmail.com
- **제목:** `[Security] AI News Radar - <간단 요약>`
- **포함 내용:** 재현 단계, 영향도, 제안 해결책 (선택)
- **응답 기한:** 72시간 내 초기 확인, 30일 내 수정 배포 목표

**책임 공개 (Responsible Disclosure):** 수정 배포 전까지 세부 내용을 공개하지 말아 주세요.

---

## 보안 원칙 (요약)

### 1. 인증 / 인가
- 로컬 개인 앱이므로 사용자 인증 없음 (혼자 사용 전제)
- 외부 서비스 연동은 **최소권한 원칙** (Discord `Send Messages` + `Read Message History`, Telegram `Bot` 스코프만)

### 2. 비밀정보 관리
- 모든 API 키는 `.env` 파일로만 관리 (Git 제외)
- GitHub Actions는 `secrets.*` 참조만 허용
- 코드·로그·README에 키 평문 금지

### 3. 입력값 검증
- RSS/웹 크롤링 URL은 `utils.security.safe_url()` 통과 필수 (SSRF 차단)
- 파일 시스템 경로는 `utils.security.safe_join()` (경로 탈출 차단)
- 모든 DB 쿼리는 `?` 플레이스홀더 (SQL Injection 차단)
- FTS5 MATCH 구문은 화이트리스트 이스케이프

### 4. 세션 / 토큰
- Streamlit 세션: 로컬 단일 사용자 가정 (멀티유저 배포 시 재평가 필요)
- 외부 API 토큰은 90일 주기 회전 권장
- 토큰/nonce는 `secrets.token_urlsafe(32)` — 암호학적 PRNG만 사용

### 5. 보안 로그
- 모든 외부 API 호출 실패는 로그(비식별화된 메타만)
- 로그에 토큰·키·사용자 식별정보 기록 금지 — `utils.security.mask_secret()` 필터 필수

### 6. 보안 설정
- Streamlit `server.enableXsrfProtection=true` (기본값 유지)
- `.gitignore`에 `.env`, `data/*.db`, `data/chroma/`, `data/audio/` 포함
- GitHub Actions 권한: `contents: write` 최소한

### 7. 의존성 점검
- `pip-audit --strict`로 주 1회 CVE 스캔 (CI 주간 스케줄)
- `detect-secrets`로 커밋 전 시크릿 검사 (pre-commit hook)
- 외부 라이브러리 최신 보안 패치 유지 (Dependabot 활성화 권장)

### 8. 암호학적 난수
- 토큰·nonce·세션 ID는 **`secrets` 모듈만** 사용
- `random` 모듈 사용 금지 (약한 PRNG)

---

## 위협 모델 / 체크리스트

상세 위협 모델과 검증 체크리스트는 내부 문서 `.PRD/05_SECURITY_BASELINE.md`를 참조하세요.

---

## 보안 검증 이력

| 날짜 | 버전 | 검증 항목 | 결과 |
|------|------|-----------|------|
| 2026-04-17 | v1.5.0 | SQL Injection (파라미터화 쿼리) | ✅ PASS |
| 2026-04-17 | v1.5.0 | 동시성 (20 스레드 병렬 읽기) | ✅ PASS |
| 2026-04-17 | v1.5.0 | FTS5 성능 (0.3ms/쿼리) | ✅ PASS |
| 2026-04-17 | v1.5.0 | 비밀정보 스캔 (grep 기반) | ✅ PASS |
| 2026-04-17 | v1.5.0 | pip-audit 의존성 CVE 스캔 | 🟡 **3패키지 패치 진행 중** |

---

## License

본 프로젝트는 MIT License (또는 SoDam AI Studio License)를 따릅니다.
