# Development Gates

## 판정 원칙

- 승인, 기획 완전성, 구현, 자동 테스트, Android, 접근성, 성능, 사람 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN`이다.
- 과거 PoC PASS는 최신 제품 PASS를 대신하지 않는다.
- 제품 구현은 전체 기획과 사용자 검수 뒤 별도 승인으로만 시작한다.

## Current Gate Summary

```yaml
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
LATEST_MAIN_SHA: b3a852cbb35de73a4b2da32151f845ddd61e1921
LATEST_MERGED_PR: 93
BATCH_001_TO_004: PASS / MERGED
CORE_DIRECTION_GATE: PASS_WITH_SCOPE_FINDINGS
AUTHORITY_CONSISTENCY_GATE: REPAIR_IN_PROGRESS
SHEET_CANON_ALIGNMENT_GATE: CORRECTED_IN_PR94
HALL_OF_FAME_GATE: FUTURE_CONTENT_HOLD
USER_PLANNING_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
LATEST_R1_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## 현재 코어 증명 Gate

확정 코어:

- 직접 단조와 영구 출생 품질
- 한 입력 한 결과의 강화와 멈춤·도전 판단
- `+10/+20/+30/+40/+50` 작품 정체성
- UID 기반 작품 생애·손상·복원·계승
- 방문 고객 인계와 즉시 인과 결과
- 지연된 생애 업데이트·재방문
- 피로도·날짜 우선순위

권장 첫 검증 범위는 `한 작품 +50 생애 버티컬 슬라이스`이며 상태는 `RECOMMENDED / USER_APPROVAL_REQUIRED`다.

## Authority Repair Gate

- [x] 핵심 시스템·PR 적대적 검토 보고서
- [x] 루트 Decision·R1 Registry·Hub 갱신
- [x] Sheet `+5/+10`, 파괴 종료, Hall 랭킹, Legacy 경제 상태 교정
- [x] PR #86·#61 병합 없이 종료
- [x] PR #81 참고 자산 분류
- [ ] PR #94 CI·changed files·리뷰 최종 확인
- [ ] 사용자 검토 후 병합

## Open PR Gate

- PR #86: `SUPERSEDED / CLOSED_WITHOUT_MERGE`
- PR #61: `HISTORY_ONLY / CLOSED_WITHOUT_MERGE`
- PR #81: `REFERENCE_ASSET / DO_NOT_MERGE_AS_UNIT`
- PR #94: `AUTHORITY_REPAIR / DRAFT`

## Planning Coverage Gate

1. R1 프로젝트 코어·플레이어 약속 — `IN_PROGRESS / CORE_REVIEW`
2. R2 Core·Session·Meta Loop
3. R3 제작·강화·작품 정체성·실패·저장
4. R4 고객·세계 일정·사건·작품 연대기
5. R5 경제·피로도·성장·장기 목표
6. R6 모바일 UX·접근성·아트·오디오
7. R7 버티컬 슬라이스·data·migration·검증
8. R8 최종 적대적 검토·사용자 검수

## Historical PoC and CI compatibility gates

아래는 과거 장비 생애 PoC 증거이며 최신 R1 제품 PASS가 아니다.

- `Project core confirmation`
- `Equipment lifecycle PoC specification`
- `Equipment lifecycle PoC implementation`
- `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
- `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`
- `PASS / IMPLEMENTATION_VALIDATED`
- `PR validation #468`
- `제작 모델 7건`
- `통합 6건`

## Product Implementation Gate

다음이 모두 닫혀야 구현 계약을 만든다.

- [ ] R1~R7 완료 또는 명시적 제외
- [ ] 미해결 MUST_FIX 0
- [ ] 주요 Decision GitHub·Sheet 동기화
- [ ] 사용자 기획 완료
- [ ] R8 적대적 최종 검수·사용자 검수 완료
- [ ] 범위·수용 기준·테스트·rollback 확정

현재: `BLOCKED`.

## Current Next Gate

```yaml
AUTHORITY_REPAIR_PR: PR94
NEXT_USER_DECISION: ONE_WORK_PLUS50_LIFECYCLE_VERTICAL_SLICE
PRODUCT_IMPLEMENTATION: BLOCKED
```
