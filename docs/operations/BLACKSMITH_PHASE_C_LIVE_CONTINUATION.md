# Blacksmith Phase C Live Continuation

Decision: `BS-OPS-20260811-03`.

이 문서는 PR #158의 유효한 운영 의도만 최신 main에서 최소 계약으로 유지한다. 기존 `AGENTS.md`, `CURRENT_CONFIRMED_DECISIONS.md`, START_HERE, Active Context, Development Gates, Roadmap와 역사 테스트를 대량 삭제·재작성하지 않는다.

```text
PR158_MERGE_UNIT: CLOSED_SUPERSEDED_UNMERGED
PR158_BRANCH_ROLE: HISTORICAL_REFERENCE_ONLY
PR158_VALID_INTENT: REIMPLEMENT_MINIMALLY_FROM_LATEST_MAIN
NO_MASS_ROUTER_REWRITE
```

## 1. PR #158 정리 판정

PR #158은 live router와 역사 consumer를 동시에 바꾸고 고정된 과거 main SHA를 durable contract에 요구했다. 따라서 대량 router 삭제와 무기한 runtime `OPEN` 주장은 폐기하고 다음 원칙만 보존한다.

- latest-main 재조회
- 기존 승인 canon 내부의 분리된 작업 계약
- fresh 전용 실행환경만 재사용
- 만료·충돌·복구 시 bootstrap 재진입
- targeted Sheet write
- Task3와 신규 제품 범위 분리

`PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`는 역사·호환 locator로 계속 보존한다. persistent Godot authoring 전에는 exact Blacksmith 실행환경과 권위를 fresh하게 증명해야 한다.

## 2. P2 완료 상태

```text
P2_CONTENT_RESULT_FOUNDATION: MERGED_PR162_MAIN_CANON
P2_DECISION: BS-VS-P2-20260813-01
P2_EXACT_HEAD: b0118e980df06c641c6b19372f364fa52a94b394
P2_MERGE_MAIN: 78eeb4c442a917051b327ddc050f9337b41516b0
P2_POSTMERGE_FULL_VALIDATION_RUN: 31653614060
P2_POSTMERGE_FULL_VALIDATION: PASS
P2_LIVE_EDITOR_PILOT_RUN: 31653614171
P2_LIVE_EDITOR_PILOT: PASS
```

P2는 기존 `VSSaveEnvelope.active_run.resolved_events` 안에 `CONTENT_RESULT_V1` typed contract를 추가했다. D01–D09의 결정·고객·세 결과 축·작품 UID 참조·인과 이유 2~4개·다음 행동 하나를 검증하며, 일반 legacy event Dictionary와 save schema version 1은 유지한다.

P2는 고객·일정 결과 계산, 확률, 보상, 총점, UI, Scene, Task3 또는 Decision10을 구현하지 않았다.

## 3. 현재 Phase C 범위

```text
PHASE_C_SCOPE: APPROVED_WITHIN_EXISTING_CANON_ONLY
NEXT_PHASE_C_PACKAGE: UNSELECTED_USER_DECISION_REQUIRED
PRODUCT_WRITER_GATE: CLOSED_NO_ACTIVE_A2
TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED
IMAGE_GENERATION: DEFERRED_BY_USER
```

P2 A2 작업은 병합·검증으로 폐쇄됐다. 현재 활성 제품 Writer Lease는 없으며 다음 패키지를 자동 추론하지 않는다.

다음 단계는 두 경우 중 하나다.

1. 기존 승인 canon 안에서 다음 최소 패키지를 A0 SHADOW로 조사한 뒤 별도 A2 계약을 연다.
2. project core, 제작·강화·경제·확률, save/UID 의미, major UX/input, Task3 또는 신규 제품 범위를 바꾸려면 새 사용자 Decision을 받는다.

## 4. Runtime freshness

PR #157과 병합된 receipt는 기록 시점의 read-only 관찰 증거다.

```text
LAST_OBSERVED_RUNTIME_RECEIPT: PASS_AT_RECORDED_RECEIPT
OBSERVED_AT_LOCAL: 2026-08-12T01:08:11+09:00
CURRENT_RUNTIME_FRESHNESS: NOT_RECHECKED_IN_THIS_GITHUB_SESSION
PERSISTENT_MUTATION_GATE: RECHECK_REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING
```

GitHub 문서만으로 현재 Godot/Codex/HiGodot process·session·port의 freshness를 증명할 수 없다. 다음 조건이 fresh하게 확인된 경우에만 live dedicated session을 재사용한다.

```text
exact Blacksmith project path
+ dedicated Godot 4.7.1
+ Godot-AI 3.1.4
+ dedicated CODEX_HOME
+ HTTP 8006 / WS 9506 exact identity
+ one exact Blacksmith session
+ editor_state / hierarchy / project settings fresh receipt
```

만료·충돌·identity 불명·복구 필요 상태에서는 전용 bootstrap으로 재진입한다.

## 5. 보호면과 Base 후속

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

새 제품 작업은 별도 A2 계약에 Task lease, resource lock, 정확 허용 경로, acceptance criteria, RED/GREEN, runtime evidence, rollback을 기록해야 한다.

P2 수행 중 현재 Base validator의 `data/`, `scripts/` 같은 디렉터리 패턴이 하위 경로를 재귀적으로 보호하지 못하는 결함을 확인했다. 프로젝트 제품 PR에서 어댑터나 workflow를 임의 수정하지 않고 Base 후속 이슈로 분리했다.

```text
BASE_PROTECTED_PATH_FOLLOW_UP: alsdmlals4-eng/Base#314
```

이 결함이 해결되기 전 다음 보호 제품 패키지는 현행 validator의 실제 동작을 먼저 재확인해야 한다.

## 6. Sheet 정책

```text
SHEET_SYNC_WRITE_POLICY: TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE
TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE
```

- GitHub current canon과 같은 Decision ID를 사용한다.
- current mirror만 정확한 range로 갱신한다.
- broad find/replace로 과거 PR·SHA·상태를 바꾸지 않는다.
- write 뒤 current landmark와 historical landmark를 모두 readback한다.
- P2 구현과 이번 폐쇄 작업에서는 Sheet write를 실행하지 않았다.

## 7. 다음 진입 순서

```text
latest main + open PR 재조회
→ 기존 승인 canon의 미구현 owner inventory
→ 다음 후보를 A0 SHADOW로 분리
→ 사용자 승인 범위 확인
→ 별도 A2 contract
→ semantic RED
→ 최소 GREEN
→ affected regression + 필요한 GUT/Godot/HiGodot
→ exact-head PR
→ postmerge readback
```

현재 상태는 `NEXT_PHASE_C_PACKAGE: UNSELECTED_USER_DECISION_REQUIRED`이며 제품 변경 권한은 열려 있지 않다.

## 8. Evidence와 비주장

확인:

- PR #158: `CLOSED_SUPERSEDED_UNMERGED`
- PR #162: P2 `MERGED_MAIN_CANON`
- P2 exact-head CI: PASS
- P2 postmerge Full Validation: PASS
- P2 postmerge Live-Editor Pilot: PASS
- Base adapter pin 변경: 없음
- repository workflow/ruleset 변경: 없음

미확인:

```text
CURRENT_LOCAL_RUNTIME: NOT_RECHECKED
PERSISTENT_GODOT_AUTHORING_AFTER_P2: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY: NOT_RUN
PERFORMANCE: NOT_RUN
HUMAN_PLAYTEST: NOT_RUN
SHEET_SYNC: NOT_RUN
```

## 9. 롤백

이번 폐쇄 작업은 continuation 상태·가이드·AI 라우팅·A2/설계 상태·회귀 테스트만 되돌린다. PR #162 제품 구현을 되돌리려면 PR #162의 squash merge를 별도로 revert한다. Save schema는 version 1이므로 migration rollback은 필요하지 않다.
