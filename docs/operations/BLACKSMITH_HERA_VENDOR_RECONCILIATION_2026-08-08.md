# Blacksmith Hera Vendor Reconciliation — 2026-08-08

```yaml
decision_id: BS-HERA-20260808-01
status: USER_APPROVED_RECONCILIATION_DRAFT_PR_PENDING_MERGE
observed_main: ddb914f7e70e0deb62f5840fb990eb471eb7f441
hera_introduced_main_commit: a5126d8a2091ce2350e50713eac614a045cc6ef2
hera_state: VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE
hera_project_plugin_enabled: false
hera_authoring_authority: NONE
gut_state: FORMALLY_ADOPTED_ACTIVE
higodot_state: PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY
task2: IMPLEMENTATION_BLOCKED_PENDING_RECONCILIATION_MERGE_AND_REVIEW
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

현재 reconciliation 기준 main은 `ddb914f7e70e0deb62f5840fb990eb471eb7f441`이다.

- `bd7e97ec49b2fac67f619c9bbe5e2c6e53c48d6f → a5126d8a2091ce2350e50713eac614a045cc6ef2`: 변경은 `addons/hera_agent_godot/**` vendor tree 추가에 한정된다.
- `a5126d8a2091ce2350e50713eac614a045cc6ef2 → ddb914f7e70e0deb62f5840fb990eb471eb7f441`: 후속 1 commit은 `.gitignore`와 `tools/watch_asset_downloads.ps1`만 변경한다. Hera 권위 또는 활성화 상태를 추가로 변경하지 않는다.

따라서 Sheet의 `GitHub main a5126d8...` 표기는 현재 main보다 한 commit 뒤처진 상태지만, 별도의 Hera 채택 증거는 아니다.

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

## 5. Task 2 gate

PR #131의 `BS-VS-TASK2-20260807-01` 설계 승인은 유지한다. 그러나 이 reconciliation Draft가 존재한다는 이유만으로 Task 2 implementation을 `READY`로 올리지 않는다.

순서는 다음과 같다.

1. PR #132에서 `BS-HERA-20260808-01` exact-head 검증 및 Sheet same-ID readback
2. 별도 명시적 사용자 승인 뒤 PR #132 merge
3. merge된 current main을 다시 읽어 Sheet main SHA 동기화
4. PR #131을 최신 main에 rebase/update하고 설계·changed files·CI를 재검토
5. 필요한 written spec / implementation plan 및 Entry Gate 통과 뒤에만 Task 2 구현 진입 재판정

현재 판정: `TASK2_DESIGN_APPROVED_IMPLEMENTATION_BLOCKED`.

## 6. Unchanged blockers

이번 reconciliation으로 다음 상태는 바뀌지 않는다.

- `GENERAL_PRODUCT_BLOCKED`
- 이미지 생성·권리·제품 적용 Gate
- Android 실기기 검증 `NOT_RUN`
- 사람 플레이 검증 `NOT_RUN`
- 로컬 Windows/Godot 실행 증거 미확인

## 7. Change boundary

이 PR은 운영 정본·계약·CI 연결만 다룬다. 다음 경로는 변경하지 않는다.

```text
addons/
assets/
data/
scenes/
scripts/
project.godot
```

특히 `addons/hera_agent_godot/**` vendor byte와 `project.godot` 활성화 상태는 그대로 보존한다.
