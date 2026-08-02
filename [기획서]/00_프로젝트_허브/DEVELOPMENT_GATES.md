# Development Gates

## 1. 판정 원칙

- 문서 승인, 기획 완전성, 구현, 자동 테스트, 실제 렌더, Android, 접근성, 성능, 사람 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.
- 과거 PoC PASS는 해당 과거 코드 HEAD의 증거이며 최신 총기획·제품·플랫폼 PASS를 대신하지 않는다.
- 제품 구현은 `PLANNING_AND_REVIEW_COMPLETE_GATE` 뒤 별도 승인 계약으로만 시작한다.
- 병합은 승인 기획의 main 보존이며 제품 구현·검증 완료가 아니다.

## 2. Current Gate Summary

```yaml
CURRENT_OPERATING_DECISIONS:
  - BS-OPS-20260802-01
  - BS-OPS-20260802-02
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
CANONICAL_RECOVERY_GATE: PASS
DECISION_AUTHORITY_GATE: PASS
PREMERGE_ADVERSARIAL_AUDIT_GATE: PASS
PR_84_MERGE_GATE: PASS
DECISION_SYNC_GATE: POSTMERGE_SYNC_IN_PROGRESS
PLANNING_COVERAGE_GATE: R1_IN_PROGRESS
GRILL_ME_DECISION_GATE: NEW_COUNTER_0_OF_10
USER_PLANNING_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
FATIGUE_DATE_RUNTIME_GATE: NOT_IMPLEMENTED
EVENT_CHRONICLE_SET_RUNTIME_GATE: NOT_IMPLEMENTED
LATEST_R1_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## 3. R0 Canonical Recovery Gate

상태: `PASS / MERGED_TO_MAIN`.

- [x] Root Decision 원장과 Hub 복구
- [x] Base v9.4 Adapter·Health 복구
- [x] Google Sheet 동기화와 bounded readback
- [x] PR #81·Issue 권위 정리
- [x] 보호 제품 경로 변경 0
- [x] PR #84 squash 병합

배치 01 main 병합 SHA: `bd68c2dbf20592e84c1bebfdc83c4c925d010dbf`.

## 4. R1 Approval Batch 01 Gate

- [x] `BS-CORE-20260802-01`
- [x] `BS-CORE-20260802-02`
- [x] `BS-SET-20260802-01`
- [x] `BS-SET-20260802-02`
- [x] `BS-SET-20260802-03`
- [x] `BS-SET-20260802-04`
- [x] `BS-OPS-20260802-02`
- [x] GitHub·Sheet premerge readback
- [x] Base v9 adoption check
- [x] Python contracts
- [x] Godot 4.7.1 headless contracts
- [x] 리뷰·스레드·충돌·금지 경로 감사
- [x] PR #84 squash merge

정본:

- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`

R1 전체 Gate는 아직 닫히지 않았다.

## 5. Premerge Adversarial Audit Result

- [x] PR open·mergeable, expected HEAD 불변
- [x] main behind 0, merge conflict 없음
- [x] changed files 전체 허용 범위
- [x] `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 변경 0
- [x] Root·Hub·R1 canon Decision과 단계 일치
- [x] Sheet Decision·의미·경로·Commit·상태 readback
- [x] PR 본문 최신 Decision·Sheet 위치 반영
- [x] 미해결 리뷰·REQUEST_CHANGES 0
- [x] 필수 check 실패 0
- [x] `NOT_RUN`을 PASS로 과장하지 않음
- [x] P0/P1 누락·충돌 0

감사 판정: `PASS`.

## 6. Grill Me Batch Gate

- 완료 배치: `BS-GRILL-BATCH-20260802-01`
- 완료 질문 수: `5`
- 병합 PR: `#84`
- 병합 방식: `SQUASH`
- 신규 승인 카운터: `0/10`
- 다음 배치 조건: 신규 승인 `10/10`
- 다음 병합 전 감사: 필수

## 7. Planning Coverage Gate

1. R1 프로젝트 코어·플레이어 약속 — `IN_PROGRESS`
2. R2 Core·Session·Meta Loop
3. R3 제작·강화·작품 정체성·실패·저장
4. R4 고객·세계 일정·사건·장비 연대기
5. R5 경제·피로도·성장·장기 목표
6. R6 모바일 UX·접근성·아트·오디오
7. R7 버티컬 슬라이스·data·migration·검증
8. R8 최종 적대적 검토·사용자 검수

배치 01 병합은 R1 전체 완료가 아니다.

## 8. Historical PoC and CI compatibility gates

아래 제목과 토큰은 과거 장비 생애 PoC 및 정적 검사 계약을 보존한다. 최신 R1 제품 상태로 확대하지 않는다.

### Project core confirmation

- 과거 코어 정렬 기록을 보존한다.
- 현재 R1 코어는 승인 배치 01에 기록됐으나 R1 전체는 진행 중이다.

### Equipment lifecycle PoC specification

- 역사 명세: `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
- 현재 분류: `REFERENCE_IMPLEMENTATION`.

### Equipment lifecycle PoC implementation

- 역사 계획: `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`
- 역사 결과 토큰: `PASS / IMPLEMENTATION_VALIDATED`.
- 제작 품질 단위 검증의 역사 기록: `제작 모델 7건`.
- 제작 결과·강화 연계 검증의 역사 기록: `통합 6건`.
- 과거 CI 증거: `PR validation #468`.
- PR #84 최종 CI: Base v9 adoption run #247 `SUCCESS`, PR validation run #838 `SUCCESS`.
- 최신 R1 runtime은 `NOT_RUN`이다.

## 9. Product Implementation Gate

다음이 모두 닫혀야 Codex 구현 계약을 만든다.

- [ ] R1~R7 기획 Coverage 완료 또는 명시적 제외
- [ ] 미해결 MUST_FIX 0
- [ ] 필요한 Grill Me 완료
- [ ] 주요 Decision GitHub·Sheet SYNCED
- [ ] 사용자 기획 완료
- [ ] R8 적대적 최종 검수와 사용자 검수 완료
- [ ] 구현 범위·수용 기준·테스트·rollback 확정

현재: `BLOCKED`.

## 10. Product and Platform Validation

| Gate | 상태 |
|---|---|
| PR #84 document/static contracts | `PASS` |
| existing reference Godot import·parse·smoke·model·integration | `PASS_AT_PR84_HEAD` |
| fatigue·date R1 runtime | `NOT_IMPLEMENTED` |
| EventChronicle·ChronicleSet runtime | `NOT_IMPLEMENTED` |
| Android device | `NOT_RUN` |
| Accessibility | `NOT_RUN` |
| Performance | `NOT_RUN` |
| Human playtest | `NOT_RUN` |
| Build/package | `NOT_RUN` |

## 11. Current Next Gate

```yaml
POSTMERGE_SYNC_PR: IN_PROGRESS
SHEET_POSTMERGE_READBACK: PENDING
GRILL_ME_NEW_COUNTER: 0/10
R1_NEXT_DESIGN_ACTIVITY: CONTINUE_AFTER_SYNC
PRODUCT_IMPLEMENTATION: BLOCKED
```
