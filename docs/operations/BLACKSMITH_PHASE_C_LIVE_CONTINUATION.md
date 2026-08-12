# Blacksmith Phase C Live Continuation

Decision: `BS-OPS-20260811-03`.

이 문서는 PR #158을 그대로 병합하지 않고, 최신 main에서 유효한 운영 의도만 최소 계약으로 다시 만든다. 기존 `AGENTS.md`, `CURRENT_CONFIRMED_DECISIONS.md`, START_HERE, Active Context, Development Gates, Roadmap와 역사 테스트를 대량 삭제·재작성하지 않는다.

```text
PR158_MERGE_UNIT: CLOSED_SUPERSEDED_UNMERGED
PR158_BRANCH_ROLE: HISTORICAL_REFERENCE_ONLY
PR158_VALID_INTENT: REIMPLEMENT_MINIMALLY_FROM_LATEST_MAIN
NO_MASS_ROUTER_REWRITE
```

## 1. 정리 판정

PR #158은 28개 커밋과 14개 파일에 걸쳐 live router와 역사 consumer를 동시에 바꿨다. `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` 같은 기존 실행환경 compatibility locator를 삭제해 실제 회귀 테스트를 깨뜨렸고, 고정된 과거 main SHA를 durable contract에 요구했다.

따라서 다음을 분리한다.

- **보존:** latest-main 재조회, 기존 승인 canon만 구현, fresh 전용 실행환경 재사용, 만료·충돌·복구 시 bootstrap 재진입, targeted Sheet write, Task3 분리.
- **폐기:** 대량 router 삭제, 역사 테스트의 일괄 기대값 변경, 과거 SHA를 현재 truth로 고정, local runtime을 영구 `OPEN`으로 간주.

`PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`는 역사·호환 locator로 계속 보존한다. 이는 매 작업마다 PowerShell을 무조건 반복하라는 뜻이 아니라, persistent Godot authoring 전에 exact Blacksmith 실행환경과 권위를 fresh하게 증명하라는 fail-closed 원칙이다.

## 2. 현재 Phase C 범위

```text
PHASE_C_SCOPE: APPROVED_WITHIN_EXISTING_CANON_ONLY
PHASE_C_NEXT_PACKAGE: P2_FOUNDATION_DATA_AND_STATE_CONTRACTS
PRODUCT_WRITER_GATE: SEPARATE_A2_CONTRACT_REQUIRED
TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED
IMAGE_GENERATION: DEFERRED_BY_USER
```

이 문서는 제품 writer lease를 만들지 않는다. P2는 먼저 현재 code/data/save/lifecycle/event/customer/item UID owner를 읽고, 이미 승인된 D01–D09가 공유하는 가장 작은 foundation gap을 찾는 기술 package다.

P2가 다음 중 하나를 요구하면 해당 항목만 별도 사용자 Decision으로 격리한다.

- project core 또는 플레이어 핵심 경험 변경
- 제작·강화·경제·확률 권위 변경
- save compatibility 또는 UID/history 의미 변경
- major UX/input meaning 변경
- Task3, Decision10 또는 새 제품 범위

## 3. Runtime freshness

PR #157과 병합된 receipt는 다음 시점의 read-only 관찰 증거다.

```text
LAST_OBSERVED_RUNTIME_RECEIPT: PASS_AT_RECORDED_RECEIPT
OBSERVED_AT_LOCAL: 2026-08-12T01:08:11+09:00
CURRENT_RUNTIME_FRESHNESS: NOT_RECHECKED_IN_THIS_GITHUB_SESSION
PERSISTENT_MUTATION_GATE: RECHECK_REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING
```

GitHub 문서만으로 사용자의 현재 Godot/Codex/HiGodot process·session·port가 아직 fresh하다고 증명할 수 없다. 따라서 PR #158의 무기한 `PERSISTENT_MUTATION_GATE: OPEN` 주장은 채택하지 않는다.

재사용 조건:

```text
exact Blacksmith project path
+ dedicated Godot 4.7.1
+ Godot-AI 3.1.4
+ dedicated CODEX_HOME
+ HTTP 8006 / WS 9506 exact identity
+ one exact Blacksmith session
+ editor_state / hierarchy / project settings fresh receipt
```

이 조건이 fresh하게 확인된 경우에만 live dedicated session을 재사용한다. 만료·충돌·identity 불명·복구 필요 상태에서는 전용 bootstrap으로 재진입한다.

## 4. 보호면

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

현재 continuation 계약은 위 경로를 수정하지 않는다. 별도 A2 계약에는 Task lease, resource lock, 허용 경로, acceptance criteria, RED/GREEN, runtime evidence, rollback이 있어야 한다.

의미적 보호:

- project core
- crafting/enhancement meaning
- economy/probability authority
- item UID/lifecycle/history
- save compatibility
- major UX/input meaning
- approved content causality

## 5. Sheet 정책

```text
SHEET_SYNC_WRITE_POLICY: TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE
TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE
```

- GitHub current canon과 같은 Decision ID를 사용한다.
- current mirror만 정확한 range로 갱신한다.
- broad find/replace로 과거 PR·SHA·상태를 바꾸지 않는다.
- write 뒤 current landmark와 historical landmark를 모두 readback한다.
- 이번 계약에서는 Sheet write를 실행하지 않는다.

## 6. P2 진입 순서

```text
latest main + open PR 재조회
→ actual code/data/Scene/tests owner inventory
→ 기존 solution REUSE / ABSORB / REFACTOR / BUILD_NEW 판정
→ 가장 작은 foundation gap 1개
→ 별도 A2 contract
→ semantic RED
→ 최소 GREEN
→ affected regression + 필요한 GUT/Godot/HiGodot
→ exact-head PR
→ postmerge readback
```

현재 단계는 P2의 **read-only owner inventory와 별도 A2 계약 작성**까지다. 이 문서 자체는 persistent 제품 구현 승인이 아니다.

## 7. Evidence와 비주장

현재 확인:

- PR #158: `CLOSED_SUPERSEDED_UNMERGED`
- PR #157 runtime receipt: 기록 시점 PASS
- 기존 제품 root 변경: 없음
- Base adapter pin 변경: 없음
- repository workflow/ruleset 변경: 없음

미확인:

```text
CURRENT_LOCAL_RUNTIME: NOT_RECHECKED
PERSISTENT_GODOT_AUTHORING: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY: NOT_RUN
PERFORMANCE: NOT_RUN
HUMAN_PLAYTEST: NOT_RUN
```

## 8. 롤백

이 대체 작업은 새 운영 상태 파일·가이드·AI 라우팅·회귀 테스트만 되돌리면 된다. 제품 data/save/Scene/Resource/runtime rollback은 필요하지 않다.
