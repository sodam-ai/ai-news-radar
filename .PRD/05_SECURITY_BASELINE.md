# 🔐 Security Baseline — AI News Radar

> **기준:** OWASP ASVS v4.0.3 Level 1 + Secure by Design
> **범위:** 로컬 개인 앱 + GitHub Actions 자동화 + 외부 API(Gemini/Discord/Telegram)
> **생성일:** 2026-04-17
> **대응 버전:** v1.5.0+

---

## 1. 위협 모델 (STRIDE)

| 위협 | 예시 | 영향 | 기본 완화 |
|------|------|------|-----------|
| **S**poofing | Discord 봇 토큰 탈취 → 봇 계정 도용 | 상 | 토큰 회전·`.env` 격리 |
| **T**ampering | RSS 크롤 결과 조작·악성 HTML 삽입 | 중 | BS4 sanitize + iframe 금지 |
| **R**epudiation | 로그 부재로 이상 행위 추적 불가 | 중 | 구조화 로그 + 요청 ID |
| **I**nformation Disclosure | `.env` 커밋 실수 / `radar.db` 공개 | 상 | `.gitignore` + pre-commit + Turso 전환 |
| **D**enial of Service | Gemini 한도 고갈·RSS 무한 리다이렉트 | 중 | Rate limit + timeout + 재시도 제한 |
| **E**levation of Privilege | Streamlit XSS → 로컬 파일 접근 | 중 | XSRF + CSP + 파일 경로 검증 |

---

## 2. OWASP ASVS v4.0.3 Level 1 매핑

### V1 — Architecture
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V1.1.1 | SDLC에 보안 설계 포함 | 본 문서 | PR 템플릿 체크박스 | 🟡 부분 |
| V1.2.1 | 신뢰 경계 식별 | §1 위협 모델 | 코드 리뷰 | 🟢 완료 |

### V2 — Authentication
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V2.1 | 비밀번호 저장·전송 | N/A (로컬 앱, 로그인 없음) | — | ⚪ 해당없음 |
| V2.10.4 | 서비스 계정 토큰 회전 | `.env` 90일 주기 수동 회전 | `SECURITY.md` 절차 문서 | 🟡 절차만 |

### V3 — Session
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V3.2.1 | 세션 ID 암호학적 난수 | Streamlit 기본 (secrets 기반) | — | 🟢 |
| V3.3.1 | 유휴 타임아웃 | Streamlit 기본 브라우저 세션 | — | 🟢 |

### V4 — Access Control
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V4.1.1 | 신뢰 경계 밖 자원 접근 차단 | localhost:6601 바인딩 | `netstat -ano \| grep 6601` | 🟡 기본설정 |

### V5 — Input Validation
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V5.1.3 | 화이트리스트 검증 | 카테고리·감성 enum 고정 | `config.py` CATEGORIES/SENTIMENTS | 🟢 |
| V5.2.1 | Output encoding | Streamlit 기본 HTML escape | `unsafe_allow_html=False` 유지 | 🟢 |
| V5.3.4 | SQL Injection 방지 | `?` 플레이스홀더 전역 | `db/database.py` 정규식 검사 | 🟢 검증됨 |
| V5.5.2 | SSRF 방지 | `utils/security.safe_url()` | 테스트 케이스 + 로그 모니터 | 🟢 **구현 완료** |

### V6 — Cryptography
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V6.2.1 | 강한 난수 | `secrets.token_urlsafe(32)` | `grep "random\." --include="*.py"` | 🟡 점검 필요 |
| V6.2.5 | 인증된 암호화 | `.env` 평문 (OS-level 암호화 권장) | BitLocker/FileVault | ⚪ |

### V7 — Error & Logging
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V7.1.1 | 민감정보 로그 제외 | `utils/security.mask_secret()` 필터 | `logging.Formatter` 공통화 | 🟢 **구현 완료** |
| V7.4.1 | 예외는 일반 메시지만 UI 노출 | `st.error("문제 발생")` 패턴 | UI 리뷰 | 🟡 부분 |

### V8 — Data Protection
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V8.1.1 | 민감 데이터 분류 | `.env` 최상위, `radar.db` 2차 | — | 🟢 |
| V8.2.1 | 클라이언트 캐싱 제한 | `@st.cache_data(ttl=60)` 적정 | — | 🟢 |

### V9 — Communication
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V9.1.1 | TLS 1.2+ | 모든 외부 호출 HTTPS | `requirements.txt` 버전 | 🟢 |

### V10 — Malicious Code
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V10.3.2 | 의존성 취약점 점검 | `pip-audit --strict` | CI 주간 스케줄 | 🟢 도구 도입 |
| V10.3.3 | 미서명 코드 차단 | N/A (개인 프로젝트) | — | ⚪ |

### V11 — Business Logic
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V11.1.2 | Rate limit / throttle | Gemini 배치 + 15 RPM 준수 | `ai/model_router.py` | 🟢 |

### V12 — Files & Resources
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V12.3.1 | 경로 순회 방지 | `utils/security.safe_join()` | 테스트 + grep 사용처 | 🟢 **구현 완료** |
| V12.5.1 | 파일 다운로드는 신뢰 확장자만 | 오디오 `.mp3`/PDF만 | — | 🟢 |

### V13 — API
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V13.2.1 | 외부 API 요청 timeout | `httpx(timeout=30.0)` 일관 적용 | grep 필요 | 🟡 점검 필요 |

### V14 — Configuration
| ID | 요구사항 | 구현 | 검증 | 상태 |
|----|----------|------|------|------|
| V14.1.1 | 빌드·배포 자동화 + 재현 | GitHub Actions | `crawl.yml` | 🟢 |
| V14.2.1 | 최소 권한 컨테이너/워커 | Actions `permissions: contents: write` | workflow 스캔 | 🟡 점검 필요 |
| V14.3.2 | 기본 자격증명 제거 | `.env.example`은 placeholder만 | — | 🟢 |
| V14.4.1 | 시크릿 스캔 | `detect-secrets` pre-commit | `.pre-commit-config.yaml` | 🟢 **구현 완료** |

---

## 3. 암호학적 난수 / 토큰 정책

### 3.1 강한 PRNG만 사용
```python
# ✅ 권장
import secrets
nonce = secrets.token_urlsafe(32)
session_id = secrets.token_hex(16)

# ❌ 금지
import random
token = ''.join(random.choices(...))   # 예측 가능
```

### 3.2 토큰 만료 정책
| 토큰 | 만료 | 회전 주기 | 저장 |
|------|------|-----------|------|
| Gemini API Key | N/A (정적) | 90일 | `.env` + GitHub Secrets |
| Discord Bot Token | 영구 (Discord 관리) | 90일 | `.env` |
| Telegram Bot Token | 영구 | 180일 | `.env` |
| Streamlit 세션 | 브라우저 종료 | 즉시 | 메모리 |
| CSRF/XSRF 토큰 | 요청별 | 즉시 | Streamlit 기본 |

### 3.3 Nonce / 일회성 값
- 중복 감지 해시: `hashlib.sha256(url + published_at)` — 결정적, 충돌 저항
- 로그 상관관계 ID: `secrets.token_urlsafe(8)`

---

## 4. 구현 체크리스트 (Dev)

- [x] **V5.5.2** `utils/security.safe_url()` — SSRF 차단
- [x] **V12.3.1** `utils/security.safe_join()` — 경로 탈출 차단
- [x] **V7.1.1** `utils/security.mask_secret()` — 로그 마스킹
- [x] **V14.4.1** `.pre-commit-config.yaml` — detect-secrets + pip-audit
- [x] **V10.3.2** `pip-audit --strict` — 의존성 CVE 스캔 도구 도입
- [ ] **V13.2.1** `grep -rn "httpx\|requests" --include="*.py"` → 모든 호출 timeout ≤ 30s 강제
- [ ] **V6.2.1** `grep -rn "random\." --include="*.py"` → 약한 난수 치환
- [ ] **V14.2.1** Actions `crawl.yml` `permissions:` 블록 최소화 감사

---

## 5. 검증 체크리스트 (QA / 릴리스 전)

### 자동 검증 (CI 권장)
- [ ] `pip-audit --strict` → 0 critical/high
- [ ] `detect-secrets scan --baseline .secrets.baseline` → 신규 시크릿 0건
- [ ] `pytest tests/test_security.py` → safe_url / safe_join / mask_secret 전 케이스 PASS

### 수동 검증
- [ ] `.env.example`에 실제 키 포맷 없음 — `grep -E "AIza|ghp_|xoxb-|AKIA"`
- [ ] GitHub 리포 → Settings → Secrets → 모든 시크릿 존재 확인
- [ ] `git log --all -p | grep -iE "AIza[A-Za-z0-9_-]{35,}"` → 과거 노출 0건
- [ ] GitHub Actions 로그 → 토큰 마스킹(`***`) 정상
- [ ] Discord/Telegram 봇 권한 → 최소 스코프만
- [ ] `data/radar.db` Git 추적 여부 (`git ls-files | grep radar.db` → 빈 결과)

---

## 6. 운영 체크리스트 (Ops)

- [ ] `.env` 파일은 OS-level 디스크 암호화 볼륨에 위치 (BitLocker/FileVault)
- [ ] GitHub 리포 → Settings → Code security & analysis → Secret scanning + Dependabot alerts ON
- [ ] 외부 API 한도 80% 도달 시 텔레그램 알림 (`ai/model_router.py` 임계치 훅)
- [ ] 월 1회 `.env` 백업 암호화 (age 또는 7-Zip AES-256)
- [ ] `SECURITY.md` 취약점 신고 이메일 월 1회 확인

---

## 7. 리스크 우선순위 (2026-04-17 기준)

| ID | 상태 | 리스크 | 우선순위 |
|----|------|--------|----------|
| V5.5.2 | ✅ 해결 | SSRF | P0 → 완료 |
| V7.1.1 | ✅ 해결 | 토큰 로그 기록 | P0 → 완료 |
| V14.4.1 | ✅ 해결 | 커밋 전 시크릿 감지 | P0 → 완료 |
| V12.3.1 | ✅ 해결 | 경로 탈출 | P1 → 완료 |
| V6.2.1 | 🟡 진행 | 약한 난수 사용처 조사 | P1 |
| V13.2.1 | 🟡 진행 | timeout 누락 | P1 |
| V2.10.4 | 🟡 절차만 | 토큰 회전 자동화 | P2 |
| V14.2.1 | 🟡 점검 | Actions 권한 과다 | P2 |

---

## 8. pip-audit 스캔 기록

### 2026-04-17 — 초기 스캔
| 패키지 | CVE | Fix | 상태 |
|--------|-----|-----|------|
| cryptography 46.0.6 | CVE-2026-39892 | 46.0.7 | 🟡 패치 진행 |
| pillow 12.1.1 | CVE-2026-40192 | 12.2.0 | 🟡 패치 진행 |
| pip 25.2 | CVE-2025-8869, CVE-2026-1703 | 26.0+ | 🟡 패치 진행 |

---

## 9. 참조

- OWASP ASVS v4.0.3 — https://owasp.org/www-project-application-security-verification-standard/
- CWE Top 25 (2024) — https://cwe.mitre.org/top25/
- Python secrets — https://docs.python.org/3/library/secrets.html
- pip-audit — https://pypi.org/project/pip-audit/
- detect-secrets — https://github.com/Yelp/detect-secrets
