# Base 적용·가지치기 감사

## 기준

- Base: `alsdmlals4-eng/Base@41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- 대상: `alsdmlals4-eng/Blacksmith`
- 동기화일: 2026-07-23
- 전략: Base 기능을 복제하지 않고 프로젝트 운영 문서와 Skill 3개로 통합
- 기능 매핑: `docs/BASE_ADOPTION_PROFILE.json`
- 자동 감사: `tools/audit_project_operating_system.py`

## 읽기·검증 범위

CI가 Base 고정 커밋 전체를 checkout하고 다음을 실행한다.

1. 의존성 설치 전 Base 원본의 텍스트형 파일을 전수 스캔한다.
2. Base Skill Registry의 25개 ACTIVE Skill과 패키지 경로를 확인한다.
3. Base 공식 Linux 운영체계 회귀와 `test_skill_system_coverage.py`를 실행한다.
4. 25개 기능이 Blacksmith Profile에 빠짐없이 매핑됐는지 확인한다.
5. Blacksmith의 Registry·Skill Mode·책임 원본·로컬 경로·stale 활성 설명·런타임 필수 경로를 검사한다.
6. 저장소 전체 텍스트에서 미해결 Git 충돌 블록을 검사한다.

현재 PR 자동 감사 상태:

- Base ACTIVE Skill: 25개 매핑 완료
- Blacksmith 프로젝트 Skill: 3개 유지
- 최신 Base CI: PR 실행 결과 확인 전 `NOT_RUN`
- Android·AAB·실기기·사람 시각·접근성·성능: `NOT_RUN`

과거 13개 Skill 기준의 오류 0·경고 0 결과는 역사적 증거로만 취급하며, 최신 25개 기준 PASS를 대신하지 않는다.

## 가지치기 결과

| 구분 | 결과 |
|---|---|
| 프로젝트 Skill 수 | 3개 유지 |
| 게임 디자인 | 프로젝트 코어·조사·GUR·DDD·밸런스·플레이테스트·PoC·Vertical Slice·명시 요청 아트 방향 통합 |
| 엔지니어링 | Godot·데이터·Android·저장·자동화·계약 보존 리팩터링·런타임 진단 통합 |
| QA | 계약·적대적 검토·비판 검증·reference-freshness·충돌 블록·정적·런타임·접근성·성능·UI·회귀 통합 |
| Foundation | Work Mode·작업 계약·문서·Context·운영 감사·Skill 간소화·가지치기·장기 작업 연속성은 프로젝트 허브 문서가 담당 |
| 외부 AI | 필요할 때만 격리 작업 공간으로 라우팅하고 결과를 QA가 검수 |
| Base 환류 | 반복 검증된 공용 교훈만 별도 제안·승인·구현 PR로 처리 |

삭제한 기능은 없다. 독립 패키지가 불필요한 기능만 Mode 또는 운영 문서로 통합했다.

## 최신 Base 기능 흡수

- 프로젝트 코어: `identifying-project-core`와 `establishing-project-core`를 판정·사용자 승인 단계로 분리
- 검토: `running-adversarial-review-and-refinement`를 QA의 공격·검증·최소 개선·회귀 루프로 통합
- 구조: `refactoring-with-contract-preservation`을 Engineering에 통합
- Skill 최적화: `simplifying-skill-bodies`를 Registry·콜드 스타트 계약으로 흡수
- 저장소 정리: `pruning-stale-and-nonfunctional-material`을 기능·복구 경계 보존 감사로 흡수
- Git 상태: `synchronizing-local-and-github-state`를 Work Mode 라우팅에 흡수
- 장기 작업: `maintaining-long-running-task-continuity`를 Active Context checkpoint에 흡수
- 연구: `governing-game-user-research-coverage`를 Game Design에 흡수
- 학습·대시보드: 사용자 학습 노트와 정본 연결 시각화는 Hub·Design Registry로 라우팅
- 런타임: `diagnosing-game-engine-runtime-failures`를 Engineering의 재현·원인 격리·최소 수정·재검증으로 통합

## 정본 동기화

과거와 어긋난 활성 설명을 교정했다.

- Base 13개 활성 기능 → 25개 활성 기능
- 구형 Base commit → `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- 시뮬레이터 준비 상태 → 기준선 15개 조합 × 1,000회 실행 완료
- 분석 Scope와 분석 Report의 책임 혼합 → `analysis_scope`와 `analysis_result`로 분리
- 수동 Skill 선택 → trigger 기반 자동 선택
- 검투사 경기 관람·베팅 삭제 오해 → 후속 기능으로 명시적 보존

게임 코드·데이터·Scene 동작은 운영체계 PR에서 변경하지 않았다.

## 안전 정리

- 완료된 일회성 `.github/workflows/materialize-auto-forge.yml`: `DELETE_APPROVED`
- 과거 Changelog·Learning Log의 역사 기록: 보존
- PDF·DOCX·다이어그램·Asset Manifest: 파이프라인·승인 근거가 없어 `NOT_RUN`
- Android 실기기·AAB·사람 시각·접근성·성능: 증거 전까지 `NOT_RUN`
- 프로젝트 Skill 신규 패키지: 생성하지 않음

## 적대적 개선 루프 결과

1. 완료 상태 뒤 구형 준비 상태가 충돌 마커와 함께 반영된 운영 정본 손상을 확인했다.
2. 손상된 Markdown 5개와 JSON Registry 1개를 완료 상태로 복구했다.
3. JSON 파싱만으로 Markdown 충돌을 차단할 수 없어 전체 텍스트 충돌 블록 검사와 회귀 테스트를 추가했다.
4. Scope 문서가 Report까지 소유하던 책임 혼합을 발견해 Design Document Registry에서 별도 문서로 분리했다.
5. 최신 Base 25개 기능을 3개 프로젝트 Skill과 Hub 문서에 누락 없이 매핑했다.
6. Workflow 존재·실행·Required Check 강제를 별도 상태로 유지한다.

## 현재 판정

- [x] Base 기준 커밋을 최신 `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`로 고정
- [x] Base 25개 ACTIVE Skill을 Profile에 1:1 매핑
- [x] Blacksmith Skill 3개 유지
- [x] Registry Mode와 Skill 본문 동기화
- [x] 충돌 정본 복구와 재발 방지 검사 추가
- [x] 분석 Scope·Report 책임 분리
- [x] 제품 Script·Scene·게임 데이터 비변경
- [ ] 최신 Base 전체 회귀와 프로젝트 감사 CI 결과 확인
- [ ] 새 작업자 또는 별도 AI의 실제 콜드 스타트 재현
- [ ] Branch protection에서 Required Check 강제 여부 확인

최종 PASS는 PR Workflow가 완료된 뒤에만 선언한다.

## 역사 기록

- PR #16 당시 Base 13개 기능 적용과 오류 0·경고 0 결과는 당시 기준에서 유효하다.
- PR #26 강화 실패 정책과 Data #352·Godot #310 PASS는 제품 정합성 이력이다.
- 현행 제품 상태와 다음 작업은 `ACTIVE_CONTEXT.md`, `ROADMAP.md`, `DEVELOPMENT_GATES.md`가 책임진다.
