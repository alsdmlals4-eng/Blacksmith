# Development Gates

## 판정 원칙

- 사용자 승인, 기획 완전성, 구현, 자동 테스트, Android, 접근성, 성능, 사람 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN`이다.
- 과거 PoC PASS는 최신 제품 PASS를 대신하지 않는다.
- 제품 구현은 전체 기획과 사용자 최종 검수 뒤 별도 승인으로만 시작한다.
- 미검증 정확한 숫자는 제품 정본이 아니라 버전형 테스트 프리셋이다.

## Current Gate Summary

```yaml
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
LATEST_MAIN_SHA: b3a852cbb35de73a4b2da32151f845ddd61e1921
LATEST_MERGED_PR: 93
CURRENT_AUTHORITY_PR: 94
BATCH_001_TO_004: PASS / MERGED
CORE_DIRECTION_GATE: PASS
CORE_CONFLICT_DECISION_GATE: PASS
AUTHORITY_CONSISTENCY_GATE: ALIGNMENT_IN_PROGRESS
SHEET_CANON_ALIGNMENT_GATE: ALIGNMENT_IN_PROGRESS
HALL_OF_FAME_GATE: FUTURE_CONTENT_HOLD_NONCOMPETITIVE_ARCHIVE
USER_R1_FINAL_REVIEW_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
LATEST_R1_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## R1 Core Gate

확정 코어:

- 직접 단조와 영구 출생 품질
- 한 입력 한 결과의 강화와 멈춤·추가 도전 판단
- 현재 검증 상한 `+50`
- `+10/+20/+30/+40/+50` 정밀 이정표
- 일반 수식어 A·B
- 활성 사건·연대기 수식어 한 개와 진화 이력
- UID 기반 작품 생애·손상·복원·계승
- 방문 고객 인계와 즉시 인과 결과
- 지연된 생애 업데이트·재방문
- 피로도·날짜 우선순위
- 경제 구조 정본과 수치 테스트 프리셋 분리

판정: `PASS / USER_APPROVED`.

## Core Vertical Slice Gate

확정 범위:

```text
플레이어가 선택한 작품 한 점 제작
→ +10/+20/+30/+40/+50 정밀 이정표
→ 방문 고객 납품
→ 즉시 인과 결과
→ 피로도·날짜·세계일정
→ 같은 UID 재방문
→ 손상·복원·재강화·후속 판단
```

- `+50` 도달만으로 완료하지 않음
- 다른 작품군은 제한된 비플레이 미리보기
- 검증 작품을 별도 대표작 시스템으로 승격하지 않음

판정: `PASS / SCOPE_APPROVED / IMPLEMENTATION_NOT_STARTED`.

## Core Fun Validation Gate

필수 행동 증거:

- 강화 지속·중단 고민
- 일반 수식어 A·B와 주요 선택 기억
- 납품 결과 인과 설명
- 같은 UID 재방문 후 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 생애 의미 이해

필수 확인:

- 플레이 직후 중립적 회상 인터뷰
- 진행자 개입·UI 오류·성능 문제 분리 기록
- 행동과 인터뷰 일치도

행동과 인터뷰가 충돌하면 통과를 보류하고 최소 수정 후 재검증한다.

정확한 표본 수·통과 비율·반복 횟수: `TEST_VALUE`.

현재 판정: `CONTRACT_APPROVED / EXECUTION_NOT_RUN`.

## Numeric Authority Gate

정본:

- 자원 종류
- 소비 시점·반환 여부
- 정보 공개
- 실패·손상·복원·파괴 상태 전이
- 피로도·날짜 역할

테스트 프리셋:

- 비용·확률
- 피로도 소비·이월
- 보상량
- 재료·촉매 수량
- 날짜·재방문 간격

상태 분류:

- `LEGACY_IMPLEMENTED_VALUE`
- `BASELINE_TEST_PRESET`
- `EXPERIMENT_VARIANT`
- `CURRENT_VALIDATED`
- `DEPRECATED_PRESET`

판정: `PASS / STRUCTURE_APPROVED / EXACT_VALUES_UNVALIDATED`.

## Damage·Restoration Gate

- 일반 실패와 대파는 UID·생애·연대기를 유지
- 강화 단계 하락 가능
- 수식어는 삭제보다 잠금·복원
- 이정표 보상 중복 지급 금지
- 대파가 흉터·변형·새 연대기를 만들 수 있음
- 완전 파괴는 명시적이고 정보가 제공된 선택만 허용
- 완전 파괴 후에도 역사 기록 보존

과거 `+30 즉시 영구 파괴`는 `LEGACY_IMPLEMENTED_VALUE / HISTORICAL_POC`로만 유지한다.

판정: `PASS / USER_APPROVED`.

## Hall of Fame Gate

- 경쟁·랭킹·점수·상위 퍼센트·시즌 보상 없음
- 플레이어·외부 작품 비경쟁 아카이브
- 테마 전시관·검색·필터
- 현재 `FUTURE_CONTENT_HOLD`
- 현재 코어 버티컬 슬라이스·제품 구현 범위에서 제외

판정: `DIRECTION_APPROVED / IMPLEMENTATION_DEFERRED`.

## Historical Forging Baseline Gate

- 역사 구현 기준선: `POC v0.6.4 · main · 2026.07.23.1`
- 자동 검증 기록: `제작 모델 7건`, `통합 6건`
- 위 수치와 테스트 개수는 현재 제품 재미 Gate가 아니라 `REFERENCE_IMPLEMENTATION / HISTORICAL_POC` 증거다.
- 정확한 피버·품질 수치는 `LEGACY_IMPLEMENTED_VALUE`이며 새 버티컬 슬라이스에서 재사용하면 별도 `BASELINE_TEST_PRESET` 버전이 필요하다.

판정: `HISTORICAL_AUTOMATED_EVIDENCE_PRESERVED / LATEST_HUMAN_VALIDATION_NOT_RUN`.

## Authority Repair Gate

- [x] 핵심 시스템·PR 적대적 검토 보고서
- [x] 사용자 판단이 필요한 핵심 충돌 Decision 해소
- [x] Game Bible 최신 정본화
- [x] Roadmap 최신화
- [x] MVP-003 역사 PoC 재분류
- [x] 루트 Decision·R1 Registry 갱신
- [x] START_HERE·ACTIVE_CONTEXT 갱신
- [x] DEVELOPMENT_GATES readback
- [x] Google Sheet 구형 표현 정렬
- [ ] PR #94 changed files·리뷰·스레드·댓글·CI·금지 경로·no-op·드리프트 감사
- [ ] expected HEAD squash merge
- [ ] main SHA·Sheet 최종 동기화
- [ ] 사용자 R1 정본 최종 검수

## Open PR Gate

- PR #94: `CURRENT_AUTHORITY_REPAIR / DRAFT`
- PR #95: `SUPERSEDED / CLOSED_WITHOUT_MERGE`
- PR #86: `SUPERSEDED / CLOSE_WITHOUT_MERGE`
- PR #61: `HISTORY_ONLY / CLOSE_WITHOUT_MERGE`
- PR #81: `REFERENCE_ASSET / DO_NOT_MERGE_AS_UNIT`

## Planning Coverage Gate

1. R1 프로젝트 코어·플레이어 약속 — `CORE_APPROVED / CANON_ALIGNMENT`
2. R2 Core·Session·Meta Loop
3. R3 제작·강화·작품 정체성·실패·저장
4. R4 고객·세계 일정·사건·작품 연대기
5. R5 경제·피로도·성장·장기 목표
6. R6 모바일 UX·접근성·아트·오디오
7. R7 버티컬 슬라이스·data·migration·검증
8. R8 최종 적대적 검토·사용자 검수

## Historical PoC Gate

MVP-001·002·003과 과거 CI 증거는 현재 다음으로 분류한다.

- `REFERENCE_IMPLEMENTATION`
- `HISTORICAL_POC`
- `LEGACY_IMPLEMENTED_VALUE`

MVP-003의 `+5/+10` 흐름과 과거 표본·통과 비율은 최신 `+50` 슬라이스나 현재 검증 Gate를 덮어쓰지 않는다.

## Product Implementation Gate

다음이 모두 닫혀야 구현 계약을 만든다.

- [ ] R1~R7 완료 또는 명시적 제외
- [ ] 미해결 MUST_FIX 0
- [ ] 주요 Decision GitHub·Sheet 동기화
- [ ] 사용자 기획 완료
- [ ] R8 적대적 최종 검수·사용자 검수 완료
- [ ] 범위·수용 기준·테스트 프리셋·rollback 확정

현재: `BLOCKED`.

## Current Next Gate

```yaml
AUTHORITY_REPAIR_PR: PR94
NEXT_ACTIVITY: PR94_ADVERSARIAL_AUDIT_AND_EXPECTED_HEAD_MERGE
PRODUCT_IMPLEMENTATION: BLOCKED
```
