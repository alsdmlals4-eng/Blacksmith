# Development Gates

## 1. 판정 원칙

- 문서 승인, 기획 완전성, 구현, 자동 테스트, 실제 렌더, Android, 접근성, 성능, 사람 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.
- 과거 PoC PASS는 해당 과거 코드 HEAD의 증거이며 최신 총기획·제품·플랫폼 PASS를 대신하지 않는다.
- 제품 구현은 `PLANNING_AND_REVIEW_COMPLETE_GATE` 뒤 별도 승인 계약으로만 시작한다.
- 병합은 승인 기획을 main에 보존하는 작업이며 제품 구현·검증 완료를 의미하지 않는다.

## 2. Current Gate Summary

```yaml
CURRENT_OPERATING_DECISIONS:
  - BS-OPS-20260802-01
  - BS-OPS-20260802-02
CURRENT_WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
CANONICAL_RECOVERY_GATE: PASS
DECISION_AUTHORITY_GATE: PREMERGE_RECHECK
DECISION_SYNC_GATE: PREMERGE_RECHECK
PLANNING_COVERAGE_GATE: R1_IN_PROGRESS
GRILL_ME_DECISION_GATE: BATCH_01_APPROVED
PREMERGE_ADVERSARIAL_AUDIT_GATE: IN_PROGRESS
ADVERSARIAL_FINAL_REVIEW_GATE: NOT_STARTED
USER_PLANNING_COMPLETE_GATE: BLOCKED
USER_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
PRODUCT_MAIN_AND_SHELL_GATE: NOT_IMPLEMENTED
SAVE_AND_RESULT_RECOVERY_GATE: NOT_IMPLEMENTED
FATIGUE_DATE_RUNTIME_GATE: NOT_IMPLEMENTED
EVENT_CHRONICLE_SET_RUNTIME_GATE: NOT_IMPLEMENTED
LATEST_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
PRODUCTION_GREENLIGHT_GATE: BLOCKED
```

## 3. R0 Canonical Recovery Gate

상태: `PASS_FOR_DRAFT_PR`.

완료:

- [x] current main·branch·PR·Decision ID 고정
- [x] 사용자 승인 설계와 실행 계획 기록
- [x] Root `CURRENT_CONFIRMED_DECISIONS.md` 생성
- [x] Hub·Registry·Base Adapter·Health 복구
- [x] Google Sheet 동일 Decision ID 동기화와 bounded readback
- [x] Issue·PR 권위 정리
- [x] 보호 제품 경로 변경 0 확인

제한:

- local validator: `BLOCKED_UNVERIFIED` — container GitHub DNS 실패
- Godot runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## 4. R1 Approval Batch 01 Gate

승인된 Decision:

- [x] `BS-CORE-20260802-01`
- [x] `BS-CORE-20260802-02`
- [x] `BS-SET-20260802-01`
- [x] `BS-SET-20260802-02`
- [x] `BS-SET-20260802-03`
- [x] `BS-SET-20260802-04`
- [x] `BS-OPS-20260802-02`

이번 병합 배치의 Grill Me 질문은 5건이며, `BS-SET-20260802-01`은 질문 이전에 승인된 상위 세트 방향이다.

배치 상세:

- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`

현재 상태: `PREMERGE_AUDIT_IN_PROGRESS`.

R1 전체 Gate는 아직 닫히지 않았다.

## 5. Decision Authority Gate

`PASS` 조건:

- Root current decisions가 최신 승인 ID와 상태를 포함
- 각 상세 질문에 단일 분야 정본 존재
- Draft·승인·구현·검증 상태 분리
- supersedes와 history 관계 보존
- broad publication index와 current R1 overlay의 우선순위 명시

현재 확인:

- Root entrypoint: R1 batch 01로 갱신
- Current R1 overlay: 생성
- PR #81: `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`
- 제품 구현: `BLOCKED`

최종 판정은 병합 직전 fresh readback 후 기록한다.

## 6. Decision Sync Gate

`SYNCED` 조건:

```text
같은 Decision ID
+ 같은 의미와 상태
+ GitHub 책임 원본 경로
+ PR과 exact Draft HEAD 외부 기록
+ Google Sheet Tab·Range
+ 양쪽 재조회 성공
```

현재 대상:

- `BS-OPS-20260802-01`
- `BS-OPS-20260802-02`
- `BS-CORE-20260802-01`
- `BS-CORE-20260802-02`
- `BS-SET-20260802-01~04`

Sheet 핵심 범위:

- `02_현재_확정결정`
- `05_GDD_요약`
- `99_변경이력`
- `00_프로젝트_허브`
- `04_누락_충돌_감사`

현재 상태: `PREMERGE_RECHECK`.

## 7. Premerge Adversarial Audit Gate

병합 직전 모두 확인한다.

- [ ] PR open·mergeable이며 expected HEAD 불변
- [ ] main 뒤처짐·merge conflict 없음
- [ ] changed files 전체가 허용 범위
- [ ] `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 변경 0
- [ ] Root·Hub·R1 canon의 Decision ID·현재 단계 일치
- [ ] Sheet Decision ID·의미·GitHub 경로·Commit·상태 readback
- [ ] PR 본문 최신 Decision·Sheet 위치·검증 상한 반영
- [ ] 미해결 리뷰 스레드·REQUEST_CHANGES 0
- [ ] 필수 check 실패 0
- [ ] `NOT_RUN` 항목을 PASS로 과장하지 않음
- [ ] P0/P1 누락·충돌 0

Gate가 실패하면 병합하지 않는다.

## 8. Grill Me Batch Gate

`BS-OPS-20260802-02`:

- 이번 배치: 승인 질문 `5/5`, 사용자 즉시 병합 지시
- 병합 후 신규 카운터: `0/10`
- 다음 배치: 신규 승인 `10/10`
- 병합 방식: 원칙적으로 `SQUASH`
- 병합 전 감사: 필수
- 병합 후 main SHA·Sheet 재동기화: 필수

## 9. Planning Coverage Gate

순서:

1. R1 프로젝트 코어·플레이어 약속 — `IN_PROGRESS`
2. R2 Core·Session·Meta Loop
3. R3 제작·강화·작품 정체성·실패·저장
4. R4 고객·세계 일정·사건·장비 연대기
5. R5 경제·피로도·성장·장기 목표
6. R6 모바일 UX·접근성·아트·오디오
7. R7 버티컬 슬라이스·data·migration·검증·제작 계획
8. R8 최종 적대적 검토·사용자 검수

R1 batch 01 병합은 R1 전체 완료가 아니다.

## 10. Product Implementation Gate

다음이 모두 닫혀야 Codex 구현 계약을 만든다.

- [ ] R1~R7 기획 Coverage 완료 또는 명시적 제외
- [ ] 미해결 `MUST_FIX` 0
- [ ] 필요한 Grill Me 완료
- [ ] 주요 Decision GitHub·Sheet `SYNCED`
- [ ] 사용자 `기획 완료`
- [ ] R8 적대적 최종 검수 완료
- [ ] 사용자 `검수 완료`
- [ ] 구현 범위·수용 기준·테스트·rollback 확정

현재 상태: `BLOCKED`.

## 11. Product and Platform Validation

| Gate | 상태 | 필요한 증거 |
|---|---|---|
| current-head static/contract | `BLOCKED_UNVERIFIED` | local validator output |
| Godot import/parse | `NOT_RUN` | current approved product paths |
| Main·representative Scene | `NOT_RUN` | implemented approved Main/Shell |
| fatigue·date | `NOT_IMPLEMENTED` | runtime loop and balance evidence |
| EventChronicle·ChronicleSet | `NOT_IMPLEMENTED` | data/runtime/content pipeline |
| save/load/process-death | `NOT_RUN` | implementation and Android interruption |
| Android device | `NOT_RUN` | build·install·safe area·touch·Back·lifecycle |
| Accessibility | `NOT_RUN` | non-color channels·text·input·human review |
| Performance | `NOT_RUN` | representative/worst-scene profile |
| Human playtest | `NOT_RUN` | understanding·fatigue·choices·history feedback |
| Build/package | `NOT_RUN` | clean build·package·install·launch·exit |

## 12. Completion Rules

### 이번 병합 완료

```yaml
PREMERGE_ADVERSARIAL_AUDIT_GATE: PASS
PR_84_MERGED: true
MERGE_METHOD: SQUASH
MAIN_SHA_RECORDED: true
SHEET_POSTMERGE_READBACK: PASS
GRILL_ME_NEW_COUNTER: 0/10
PRODUCT_IMPLEMENTATION: BLOCKED
```

### 전체 기획 완료

R1~R7 Coverage, 중요 Decision, 동기화, R8 적대적 검토, 사용자 검수가 닫혀야 한다.

### Demo 완료

승인 범위 실제 구현, 자동 검증, Android, 접근성, 성능, 사람 플레이, Build·패키징 증거가 필요하다. 문서와 과거 PoC PASS만으로 Demo Ready를 선언하지 않는다.
