# Development Gates

## 판정 원칙

- 사용자 승인, 기획 완전성, 구현, 자동 테스트, Android, 접근성, 성능, 사람 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN`이다.
- 과거 PoC PASS는 최신 제품 PASS를 대신하지 않는다.
- 미검증 정확한 숫자는 버전형 테스트 프리셋이다.
- 제품 구현은 R1~R8 전체 기획과 최종 사용자 검수 뒤 별도 승인으로만 시작한다.

## Current Gate Summary

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R1_STATUS: USER_APPROVED / CANON_COMPLETE
R2_STATUS: PLANNING_ACTIVE
R1_FINAL_APPROVAL_DECISION: BS-OPS-20260803-05
WORLD_SCHEDULE_DECISION: BS-WORLD-20260803-01
CANON_BASELINE_PR: 94
CANON_BASELINE_SHA: 8a0956d6c8b4cf3db545a17d0bd002ba8354d568
POST_MERGE_FINALIZATION_PR: 96
SHEET_SYNC_CLOSURE_PR: 97
CORE_DIRECTION_GATE: PASS
CORE_CONFLICT_DECISION_GATE: PASS
AUTHORITY_CONSISTENCY_GATE: PASS
R1_ADVERSARIAL_AUDIT_GATE: PASS_P0_0_P1_0
SHEET_CANON_ALIGNMENT_GATE: PASS / BS-OPS-20260803-04 / READBACK_PASS
USER_R1_FINAL_REVIEW_GATE: PASS / BS-OPS-20260803-05
WORLD_SCHEDULE_STRUCTURE_GATE: PASS / DAILY_STAGED_PROGRESS
R2_PLANNING_GATE: OPEN
CODEX_IMPLEMENTATION_GATE: BLOCKED
LATEST_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## R1 Core Gate

- 현재 검증 상한 `+50`
- 정밀 이정표 `+10/+20/+30/+40/+50`
- 일반 수식어 A·B
- 활성 사건·연대기 수식어 한 개와 진화 이력
- UID 기반 작품 생애·손상·복원·계승
- 방문 고객 인계와 즉시·지연 결과
- 세계일정의 날짜별 단계 진행과 규모별 기간 증가
- 피로도·날짜 우선순위
- 구조 정본과 수치 테스트 프리셋 분리

판정: `PASS / USER_APPROVED / CANON_COMPLETE`.

## World Schedule Gate

필수 불변 규칙:

- 발생·납품 당일에 최종 세계 결과까지 해결하지 않음
- 첫 날짜 진행 한 번만으로 최종 해결하지 않음
- 하루 종료 한 번당 최대 한 단계 또는 한 개 진행 단위 전진
- 최종 결과 전에 최소 하나의 중간 상태 제공
- 규모가 클수록 필요한 단계와 게임 날짜 증가
- 날짜별 진행은 작품 기여·위험·조건·대응 가능성을 갱신
- 날짜 경과만으로 사건 수식어 자동 성장 금지
- 빈 대기 로그·필수 장문 대화·날짜 스킵 최적화 금지

상대 기간:

```text
LOCAL/PERSONAL
< REGIONAL/FACTION
< REALM/NATIONAL
< WAR/CATASTROPHE
```

정확한 기간·단계·동시 진행 수·분기 수는 `BASELINE_TEST_PRESET`이다.

판정: `STRUCTURE_APPROVED / EXACT_DURATION_UNVALIDATED`.

## Core Vertical Slice Gate

```text
플레이어 선택 작품 한 점 제작
→ +10/+20/+30/+40/+50
→ 방문 고객 납품
→ 즉시 사용 계획·초기 인과 피드백
→ 날짜 1: 준비·초기 진행
→ 날짜 2+: 중간 변화·전환점
→ 별도 날짜: 최종 세계 결과
→ 같은 UID 재방문
→ 손상·복원·재강화·후속 판단
```

`+50` 도달만으로 완료하지 않으며 세계일정은 최소 하나의 중간 상태를 거친다. 다른 작품군은 제한된 비플레이 미리보기로만 제시한다.

판정: `SCOPE_APPROVED / IMPLEMENTATION_NOT_STARTED`.

## Core Fun Validation Gate

필수 행동 증거:

- 강화 지속·중단 고민
- 일반 수식어 A·B와 주요 선택 기억
- 납품 결과 인과 설명
- 세계일정 현재 단계와 다음 진행 이해
- 재방문 후 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 생애 의미 이해

중립적 회상 인터뷰가 행동과 충돌하면 통과를 보류한다.

판정: `CONTRACT_APPROVED / EXECUTION_NOT_RUN`.

## Numeric Authority Gate

정본은 자원 종류·소비 시점·반환 여부·정보 공개·상태 전이·피로도와 날짜 역할·세계일정 규모와 기간의 상대 관계를 소유한다. 정확한 비용·확률·소비량·보상량·세계일정 기간·재방문 간격은 `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET / EXPERIMENT_VARIANT / CURRENT_VALIDATED / DEPRECATED_PRESET`으로 관리한다.

판정: `STRUCTURE_APPROVED / EXACT_VALUES_UNVALIDATED`.

## Damage·Restoration Gate

- 일반 실패와 대파는 UID·생애·연대기 유지
- 강화 단계 하락 가능
- 수식어 잠금·복원
- 이정표 보상 중복 지급 금지
- 완전 파괴는 명시적이고 정보가 제공된 선택만 허용
- 완전 파괴 후에도 역사 기록 보존

과거 `+30 즉시 영구 파괴`는 `LEGACY_IMPLEMENTED_VALUE / HISTORICAL_POC`다.

판정: `PASS / USER_APPROVED`.

## Hall of Fame Gate

경쟁·랭킹·점수·시즌 보상 없는 비경쟁 작품 아카이브이며 현재 `FUTURE_CONTENT_HOLD`다.

## Historical Forging Baseline Gate

- `POC v0.6.4 · main · 2026.07.23.1`
- `제작 모델 7건`, `통합 6건`
- `REFERENCE_IMPLEMENTATION / HISTORICAL_POC`

## R1 Authority·Audit Gate

- [x] 핵심 충돌 해소
- [x] Game Bible·Roadmap·MVP·Root Decision·Registry·Hub 정렬
- [x] Sheet 역사 Decision 재분류
- [x] PR #94 적대적 감사 P0 0 / P1 0
- [x] PR #94·#96·#97 최종 CI 통과
- [x] expected-head squash merge
- [x] 병합 SHA Sheet 최종화·readback
- [x] 사용자 R1 정본 최종 검수

## PR Gate

- PR #94: `MERGED_CANON_BASELINE`
- PR #96: `MERGED_POST_MERGE_FINALIZATION`
- PR #97: `MERGED_SHEET_SYNC_GATE_CLOSURE`
- PR #81: `REFERENCE_ASSET / OPEN_DRAFT / DO_NOT_MERGE_AS_UNIT`
- PR #95·#86·#61: 종료 또는 역사 전용

## Product Implementation Gate

R1~R8 기획·검수, 테스트 프리셋·rollback 계약과 최종 사용자 승인이 완료되기 전까지 `BLOCKED`다.

## Current Next Gate

```yaml
NEXT_ACTIVITY: PLAN_R2_CORE_SESSION_META_LOOP
R2_FIRST_DECISION_AREA: WORLD_SCHEDULE_SCALE_DURATION_DAILY_UPDATE_AND_PLAYER_INTERVENTION
PRODUCT_IMPLEMENTATION: BLOCKED
```