# Base 적용·가지치기 감사

## 기준

- Base: `alsdmlals4-eng/Base@ee265576da7f67d3278f8099dd97d4e714ef0651`
- 대상: `alsdmlals4-eng/Blacksmith`
- 전략: Base 기능을 복제하지 않고 프로젝트 운영 문서와 Skill 3개로 통합
- 기능 매핑: `docs/BASE_ADOPTION_PROFILE.json`
- 자동 감사: `tools/audit_project_operating_system.py`

## 읽기·검증 범위

CI가 Base 고정 커밋 전체를 checkout하고 다음을 실행한다.

1. 의존성 설치 전 Base 원본의 텍스트형 파일을 전수 스캔한다.
2. Base Skill Registry의 13개 ACTIVE Skill과 패키지 경로를 확인한다.
3. Base 공식 Linux 운영체계 회귀 테스트 전체를 실행한다.
4. 13개 기능이 Blacksmith Profile에 빠짐없이 매핑됐는지 확인한다.
5. Blacksmith의 Registry·Skill Mode·책임 원본·로컬 경로·stale 활성 설명·런타임 필수 경로를 검사한다.

최종 자동 감사 결과:

- Base 텍스트형 파일: 223개 스캔
- Base ACTIVE Skill: 13개
- Blacksmith 프로젝트 Skill: 3개
- Blacksmith 텍스트형 파일: 59개 스캔
- 오류: 0
- 경고: 0

## 가지치기 결과

| 구분 | 결과 |
|---|---|
| 프로젝트 Skill 수 | 3개 유지 |
| 게임 디자인 | 조사·DDD·밸런스·플레이테스트·PoC·Vertical Slice·아트 방향 통합 |
| 엔지니어링 | Godot·데이터·Android·저장·자동화 통합 |
| QA | 계약·외부 결과·reference-freshness·정적·런타임·접근성·성능·UI·회귀 통합 |
| Foundation | Work Mode·작업 계약·문서·Context·운영 감사는 프로젝트 허브 문서가 담당 |
| 외부 AI | 필요할 때만 격리 작업 공간으로 라우팅하고 결과를 QA가 검수 |
| Base 환류 | 반복 검증된 공용 교훈만 별도 제안·승인·구현 PR로 처리 |

삭제한 기능은 없다. 독립 패키지가 불필요한 기능만 Mode 또는 운영 문서로 통합했다.

## 정본 동기화

당시 `POC v0.6.0`과 어긋난 활성 설명을 교정했다.

- +5 중심 강화 설명 → +100 일반·특수 강화
- 전 구간 파괴 없음 → +11 하락, +30 파괴
- 5개 테스트 기준 → 최신 강화 모델 검증
- 폭주 성장 증폭 → 낮은 확률 총 2단계 도약과 이정표 차단
- 자동 단조 없음 → 목표·자동 보관·반복·재료 fallback·중지 조건
- 수동 Skill 선택 → trigger 기반 자동 선택
- 미확정 Base 버전 → 고정 commit과 재동기화 조건
- 검투사 경기 관람·베팅 삭제 오해 → 후속 기능으로 명시적 보존

게임 코드·데이터·Scene 동작은 운영체계 PR에서 변경하지 않았다.

## 안전 정리

- 완료된 일회성 `.github/workflows/materialize-auto-forge.yml`: `DELETE_APPROVED`
- `project.godot`의 일회성 검증 주석: 제거
- 과거 Changelog·Learning Log의 역사 기록: 보존
- PDF·DOCX·다이어그램·Asset Manifest: 파이프라인·승인 근거가 없어 `NOT_RUN`
- Android 실기기·AAB·사람 시각·접근성·성능: 증거 전까지 `NOT_RUN`

## 적대적 개선 루프 결과

1. Base 테스트 의존성 누락을 발견해 고정 requirements·LibreOffice·Poppler·pnpm 설치를 추가했다.
2. Base와 Blacksmith checkout을 형제 디렉터리로 격리해 스캔 오염을 차단했다.
3. 의존성의 `node_modules`가 파일 수를 부풀리는 문제를 발견해 원본 감사를 설치 전으로 이동했다.
4. 변경 목록 밖의 stale 소비자인 `tests/README.md`, `scripts/README.md`, `scenes/README.md`, `tests/SPECIAL_ENHANCEMENT_VALIDATION.md`를 갱신했다.
5. 경기 베팅이 영구 삭제처럼 보이는 기능 손실 위험을 발견해 Game Bible과 Decision Log에 후속 기능으로 보존했다.
6. 감사 실패 시에도 JSON 보고서를 업로드하도록 CI를 구성했다.

## 최종 판정

- [x] Base 고정본 공식 Linux 회귀 테스트 전체 PASS
- [x] Base 13개 기능 매핑 1:1 PASS
- [x] Blacksmith Skill 3개와 Registry Mode 일치 PASS
- [x] 로컬 경로·책임 원본·stale 활성 설명 감사 PASS
- [x] JSON 데이터 검증 PASS
- [x] Godot 4.7.1 import·parse PASS
- [x] 강화 Scene 스모크 PASS
- [x] 제작·강화 모델 테스트 PASS
- [x] changed files 30개 patch 전수 검토 PASS
- [x] untouched 소비자·삭제 참조 검토 PASS
- [x] 감사 보고서 오류 0·경고 0
- [x] PR #16 최종 리뷰와 미해결 스레드 확인
- [x] PR #16 squash 병합: `41d6dad7c2e91a9eb21c543d73b323e07251e02c`
- [x] main의 Profile·CI Workflow·Game Bible 핵심 내용 재확인
- [x] Android·AAB·시각·접근성·성능·브랜치 보호는 `NOT_RUN` 또는 `UNVERIFIED`로 분리

차단 finding은 없으며 Base 적용·가지치기·기능 보존 작업은 완료됐다.

## 최신 main 재확인 — 2026-07-23

- 확인 기준: `main` 커밋 `210a43c6ad1f34b8af15aa5938196a8f9fe24526` (PR #27 상태 동기화 포함)
- Base 기준: 고정 커밋 `ee265576da7f67d3278f8099dd97d4e714ef0651`
- 재실행: 데이터 의미 검증, 제작 결과·강화 실패 정적 계약, Base 적용·로컬 참조 감사
- 결과: 오류 0, 경고 0. 현재 제품 상태와 다음 작업은 `ACTIVE_CONTEXT.md`, `ROADMAP.md`, `DEVELOPMENT_GATES.md`가 책임진다.
- 경계: 이 문서의 PR #16·POC v0.6.0 표기는 Base 적용 당시의 이력이며, 현행 제품 버전이나 미완료 작업의 정본이 아니다.
