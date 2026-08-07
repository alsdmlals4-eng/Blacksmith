# Blacksmith Hera Vendor Reconciliation — 2026-08-08

```yaml
decision_id: BS-HERA-20260808-01
status: USER_APPROVED_RECONCILIATION_MERGED_PR132_MAIN_CANON
observed_main: ddb914f7e70e0deb62f5840fb990eb471eb7f441
merge_main: 29b06e323185e436d709fcdf638f445b9099266e
hera_introduced_main_commit: a5126d8a2091ce2350e50713eac614a045cc6ef2
hera_state: VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE
hera_project_plugin_enabled: false
hera_authoring_authority: NONE
gut_state: FORMALLY_ADOPTED_ACTIVE
higodot_state: PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY
postmerge_full_validation_run: 111
postmerge_full_validation: PASS
authority_workflow_startup_failure: PREEXISTING_ZERO_JOB_FAILURE_NOT_INTRODUCED_BY_PR132
task2: TASK2_DESIGN_APPROVED_IMPLEMENTATION_BLOCKED_PENDING_PR131_REBASE_REVIEW_PLAN_AND_ENTRY_GATE
general_product: BLOCKED
android_device_validation: NOT_RUN
human_playtest: NOT_RUN
```

## 1. Decision

`BS-HERA-20260808-01`은 현재 `main`에 이미 들어와 있는 Hera Agent Godot vendor tree의 존재를 사실대로 정본화하되, 그 존재를 채택·활성화·저작 권위 부여로 해석하지 않는 reconciliation Decision이다.

- 설치 경로: `addons/hera_agent_godot/**`
- 관측 Plugin: Hera Agent Godot `1.0.0`
- 현재 판정: `VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE`
- authoring/mutation authority: `NONE`
- Production activation: `REQUIRES_SEPARATE_USER_APPROVED_ADOPTION`

이 Decision은 Hera vendor byte 자체를 변경하거나 활성화하지 않는다.

## 2. Main history evidence

reconciliation 설계·검증 기준 main은 `ddb914f7e70e0deb62f5840fb990eb471eb7f441`이었고, 사용자 병합 승인 뒤 PR #132가 squash merge되어 현재 reconciliation main canon은 `29b06e323185e436d709fcdf638f445b9099266e`이다.

- `bd7e97ec49b2fac67f619c9bbe5e2c6e53c48d6f → a5126d8a2091ce2350e50713eac614a045cc6ef2`: 변경은 `addons/hera_agent_godot/**` vendor tree 추가에 한정된다.
- `a5126d8a2091ce2350e50713eac614a045cc6ef2 → ddb914f7e70e0deb62f5840fb990eb471eb7f441`: 후속 1 commit은 `.gitignore`와 `tools/watch_asset_downloads.ps1`만 변경한다. Hera 권위 또는 활성화 상태를 추가로 변경하지 않는다.
- PR #132 merge `29b06e323185e436d709fcdf638f445b9099266e`: Hera vendor byte·제품 경로·`project.godot`을 변경하지 않고 권위·Gate·evidence 정합화만 main canon으로 반영한다.

## 3. Runtime/editor activation evidence

현재 `project.godot`의 Editor Plugin 활성 목록에는 `res://addons/godot_ai/plugin.cfg`만 존재하며 `res://addons/hera_agent_godot/plugin.cfg`는 포함되지 않는다.

따라서 Hera vendor 존재를 Godot Project 활성화 또는 저작 권위로 승격하지 않는다.

## 4. Existing authority preservation

### HiGodot

HiGodot은 계속 `PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY`다. Production 저작 권위 활성화는 별도 승인 전까지 `PENDING_SEPARATE_APPROVAL`이다.

### GUT 9.7.1

GUT은 `BS-TEST-20260806-01`에 따라 이미 `FORMALLY_ADOPTED_ACTIVE`이며 `SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY`다.

- formal adoption main: `2c4ae7eb244f1e6e01fd0392b747f8ffc3cee7eb` / PR #125
- postmerge closure: `8a37499afd454574dcc8407e07f6b07dff9301e8` / PR #126
- `.gutconfig.json` 존재
- `tests/gut/**` consumer 존재
- formal GUT CI 존재

이 reconciliation은 GUT 채택을 재개방하거나 권위를 변경하지 않는다.

## 5. Postmerge validation evidence

PR #132 merge main `29b06e323185e436d709fcdf638f445b9099266e`에서 Full validation #111은 PASS했다. 같은 main push에서 HiGodot/GUT authority workflow가 job 0건으로 즉시 실패했지만, 직전 main `ddb914f7e70e0deb62f5840fb990eb471eb7f441`에도 같은 zero-job startup failure가 존재한 기존 workflow 문제이며 PR #132가 도입한 회귀로 판정하지 않는다.

따라서 기록은 다음처럼 분리한다.

- postmerge Full validation #111: `PASS`
- postmerge platform/기타 실행 검증: `PASS`가 관측된 항목만 PASS로 기록
- authority workflow zero-job startup failure: `PREEXISTING_ZERO_JOB_FAILURE_NOT_INTRODUCED_BY_PR132`
- 위 기존 workflow 문제를 근거로 Hera 권위나 Task 2 Gate를 임의 개방하지 않는다.

## 6. Task 2 gate

PR #131의 `BS-VS-TASK2-20260807-01` 설계 승인은 유지한다. PR #132 병합은 Hera reconciliation Gate 하나를 폐쇄했을 뿐 Task 2 implementation을 자동으로 `READY`로 올리지 않는다.

다음 순서가 남아 있다.

1. PR #132 postmerge current-main 및 Sheet same-ID closure readback
2. PR #133 postmerge closure Draft의 exact-head 검증 및 별도 병합 승인
3. closure가 main canon이 된 뒤 PR #131을 최신 main에 rebase/update
4. PR #131 written spec·changed files·CI를 재검토하고 implementation plan을 최신화
5. Entry Gate 통과 뒤에만 Task 2 RED → GREEN 구현 진입을 재판정

현재 판정: `TASK2_DESIGN_APPROVED_IMPLEMENTATION_BLOCKED`.

## 7. Unchanged blockers

이번 reconciliation으로 다음 상태는 바뀌지 않는다.

- `GENERAL_PRODUCT_BLOCKED`
- 이미지 생성·권리·제품 적용 Gate
- Android 실기기 검증 `NOT_RUN`
- 사람 플레이 검증 `NOT_RUN`
- 로컬 Windows/Godot 실행 증거 미확인

## 8. Change boundary

reconciliation과 postmerge closure는 운영 정본·계약·CI 연결만 다룬다. 다음 경로는 변경하지 않는다.

```text
addons/
assets/
data/
scenes/
scripts/
project.godot
```

특히 `addons/hera_agent_godot/**` vendor byte와 `project.godot` 활성화 상태는 그대로 보존한다.
