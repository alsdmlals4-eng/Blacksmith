# Blacksmith Save·Continue·ResultEnvelope Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Execution Gate:** 이 계획은 사용자 `기획 완료`와 `검수 완료` 전에는 실행하지 않는다.

**Goal:** 단일 캠페인·자동 백업 2개·안전한 이어하기·손상 복구·AttemptIntent·ResultEnvelope를 Godot 4.7.1 프로젝트에 구현해 앱 종료와 프로세스 종료 후에도 결과 재추첨·이중 적용·자원 손실 없이 같은 캠페인을 복구한다.

**Architecture:** `AppStateCoordinator`가 한 캠페인의 도메인 객체를 소유하고, `SaveCoordinator`가 Snapshot 수집·검증·마이그레이션·원자 저장·백업 복구를 단독 책임진다. 비가역 행동은 `AttemptIntent PREPARED` 저장 뒤 실행하며, 도메인 변경과 `ResultEnvelope APPLIED`를 같은 save revision에 확정한 뒤 결과 UI를 표시한다.

**Tech Stack:** Godot 4.7.1 stable, GDScript, JSON, ConfigFile, FileAccess, SHA-256 payload hash, Godot headless SceneTree tests, Python data validators, Android portrait 720×1280.

## Global Constraints

- Decision ID: `BS-SAVE-20260801-01`.
- 캠페인 슬롯은 1개다.
- 자동 백업은 2개다.
- 수동 저장·수동 불러오기·백업 선택 UI는 금지한다.
- 정상 검증된 primary만 backup으로 회전한다.
- 저장 공간 부족·쓰기 불가 상태에서 비가역 행동을 시작하지 않는다.
- `APPLIED` 저장 전 결과 화면을 열지 않는다.
- 앱 재실행·화면 전환·뒤로가기로 결과를 재추첨하거나 이중 적용하지 않는다.
- 새 게임은 신규 캠페인 파일 검증 성공 후 기존 캠페인을 교체한다.
- 마이그레이션 실패 시 원본 바이트를 덮어쓰지 않는다.
- 제품 구현과 실행은 전체 기획·최종 검수 승인 뒤에만 수행한다.

---

## File Map

### Create

- `scripts/application/app_state_coordinator.gd`
- `scripts/application/save/save_paths.gd`
- `scripts/application/save/save_status.gd`
- `scripts/application/save/campaign_serializer.gd`
- `scripts/application/save/campaign_validator.gd`
- `scripts/application/save/atomic_save_writer.gd`
- `scripts/application/save/save_inspector.gd`
- `scripts/application/save/save_migrator.gd`
- `scripts/application/save/recovery_coordinator.gd`
- `scripts/application/save/save_coordinator.gd`
- `scripts/application/transactions/attempt_intent.gd`
- `scripts/application/results/result_envelope.gd`
- `scripts/application/results/result_envelope_queue.gd`
- `scripts/application/settings/settings_store.gd`
- `scripts/ui/main_menu_controller.gd`
- `scripts/ui/result_envelope_overlay.gd`
- `scenes/application/boot.tscn`
- `scenes/application/blacksmith_app.tscn`
- `scenes/ui/main_menu.tscn`
- `scenes/ui/result_envelope_overlay.tscn`
- `tests/unit/test_campaign_validator.gd`
- `tests/unit/test_atomic_save_writer.gd`
- `tests/unit/test_save_inspector.gd`
- `tests/unit/test_save_migrator.gd`
- `tests/unit/test_attempt_intent.gd`
- `tests/unit/test_result_envelope_queue.gd`
- `tests/unit/test_settings_store.gd`
- `tests/integration/test_save_coordinator.gd`
- `tests/integration/test_continue_recovery_flow.gd`
- `tests/integration/test_irreversible_action_recovery.gd`
- `tests/integration/test_new_game_replacement.gd`
- `tools/validate_save_contract.py`
- `tests/test_save_contract.py`

### Modify

- `project.godot`
- `scripts/forging/forging_session.gd`
- `scripts/enhancement/enhancement_session.gd`
- `scripts/economy/workshop_resources.gd`
- `scripts/progression/workshop_calendar.gd`
- `scripts/world/equipment_world_registry.gd`
- `scripts/poc/equipment_lifecycle_poc_controller.gd`
- `scripts/ui/game_flow_screen.gd`
- `scripts/ui/enhancement_screen.gd`
- `tests/README.md`
- `.github/workflows/godot-validation.yml`
- `docs/CI_EXECUTION_POLICY.md`

---

### Task 1: Save contracts and path constants

**Files:**
- Create: `scripts/application/save/save_paths.gd`
- Create: `scripts/application/save/save_status.gd`
- Create: `scripts/application/transactions/attempt_intent.gd`
- Create: `scripts/application/results/result_envelope.gd`
- Test: `tests/unit/test_attempt_intent.gd`
- Test: `tests/unit/test_result_envelope_queue.gd`

**Interfaces:**
- Produces: `SavePaths`, `SaveStatus`, `AttemptIntent`, `ResultEnvelope` constants and constructors.

- [ ] **Step 1: Write failing contract tests**

```gdscript
extends SceneTree

const AttemptIntentScript = preload("res://scripts/application/transactions/attempt_intent.gd")
const ResultEnvelopeScript = preload("res://scripts/application/results/result_envelope.gd")

var failures: Array[String] = []

func _initialize() -> void:
    var intent := AttemptIntentScript.create_prepared(
        "intent:enhance:eq_1:11",
        "ENHANCE",
        "eq_1",
        11,
        {"gold": 1000, "equipment_level": 10},
        150,
        {"whetstone": 1},
        {"seed": 29029, "draw_index": 12},
        7
    )
    _expect(intent["state"] == "PREPARED", "신규 intent는 PREPARED여야 합니다.")
    _expect(intent["created_revision"] == 7, "생성 revision을 보존해야 합니다.")

    var envelope := ResultEnvelopeScript.create_applied(
        "result:intent:enhance:eq_1:11",
        intent["intent_id"],
        "ENHANCEMENT_RESULT",
        "EQUIPMENT",
        "eq_1",
        "ENHANCE",
        "before_hash",
        "after_hash",
        {"outcome": "SUCCESS"},
        8,
        "RESULT_ENVELOPE_OVERLAY"
    )
    _expect(envelope["state"] == "APPLIED", "도메인 반영 결과는 APPLIED여야 합니다.")
    _expect(envelope["applied_revision"] == 8, "APPLIED revision을 보존해야 합니다.")
    quit(0 if failures.is_empty() else 1)

func _expect(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
```

- [ ] **Step 2: Run tests and verify failure**

```bash
godot --headless --path . --script res://tests/unit/test_attempt_intent.gd
godot --headless --path . --script res://tests/unit/test_result_envelope_queue.gd
```

Expected: preload failure because contract scripts do not exist.

- [ ] **Step 3: Implement exact constants and constructors**

```gdscript
# scripts/application/save/save_paths.gd
class_name SavePaths
extends RefCounted

const PRIMARY := "user://campaign.save"
const BACKUP_1 := "user://campaign.backup1"
const BACKUP_2 := "user://campaign.backup2"
const TEMPORARY := "user://campaign.save.tmp"
const SETTINGS := "user://settings.cfg"

static func corrupt_path(timestamp_token: String) -> String:
    return "user://campaign.corrupt.%s" % timestamp_token
```

```gdscript
# scripts/application/save/save_status.gd
class_name SaveStatus
extends RefCounted

enum Code {
    NO_SAVE,
    VALID_PRIMARY,
    RECOVERABLE_BACKUP,
    MIGRATION_REQUIRED,
    MIGRATION_FAILED,
    UNSUPPORTED_VERSION,
    UNRECOVERABLE_CORRUPTION,
}
```

`AttemptIntent.create_prepared()`와 `ResultEnvelope.create_applied()`는 모든 필수 필드를 deep copy하며 빈 ID와 음수 revision을 거부한다.

- [ ] **Step 4: Run tests and verify pass**

```bash
godot --headless --path . --script res://tests/unit/test_attempt_intent.gd
godot --headless --path . --script res://tests/unit/test_result_envelope_queue.gd
```

Expected: exit 0.

- [ ] **Step 5: Commit**

```bash
git add scripts/application/save scripts/application/transactions scripts/application/results tests/unit/test_attempt_intent.gd tests/unit/test_result_envelope_queue.gd
git commit -m "feat: define save transaction and result contracts"
```

---

### Task 2: Campaign serializer and validator

**Files:**
- Create: `scripts/application/save/campaign_serializer.gd`
- Create: `scripts/application/save/campaign_validator.gd`
- Create: `tools/validate_save_contract.py`
- Create: `tests/test_save_contract.py`
- Test: `tests/unit/test_campaign_validator.gd`

**Interfaces:**
- Produces: `CampaignSerializer.encode(snapshot) -> String`, `decode(text) -> Dictionary`.
- Produces: `CampaignValidator.validate(snapshot) -> Dictionary` with `ok`, `errors`, `payload_hash`.

- [ ] **Step 1: Write failing tests for required fields, duplicate IDs, dangling references and hash mismatch**

```python
VALID = {
    "schema_version": 1,
    "save_revision": 8,
    "campaign_id": "campaign-1",
    "created_at_utc": "2026-08-01T00:00:00Z",
    "saved_at_utc": "2026-08-01T00:01:00Z",
    "game_day": 3,
    "current_route": "FORGE_HUB",
    "last_safe_view": "FORGE_HUB",
    "workshop_resources": {"gold": 1000, "material_stock": {}},
    "workshop_calendar": {"day": 3},
    "equipment_storage": {"records": {}},
    "active_forging": {},
    "active_enhancement": {},
    "active_attempt_intent": {},
    "customers_and_contracts": {"contracts": {}},
    "customer_relationships": {"records": {}},
    "equipment_world_registry": {"records": {}},
    "pending_result_envelopes": [],
    "integrity_metadata": {"writer_version": "1.0.0", "payload_hash": ""},
}
```

Tests must reject:
- missing `campaign_id`
- negative `save_revision`
- duplicate `equipment_uid`
- envelope subject pointing to missing equipment
- `APPLIED` envelope with `applied_revision` greater than save revision
- hash mismatch

- [ ] **Step 2: Run and verify failure**

```bash
python -m unittest tests/test_save_contract.py
godot --headless --path . --script res://tests/unit/test_campaign_validator.gd
```

- [ ] **Step 3: Implement canonical JSON and SHA-256**

Serializer must recursively sort dictionary keys before JSON encoding. `payload_hash` is calculated from the snapshot with `integrity_metadata.payload_hash` temporarily set to an empty string.

```gdscript
static func compute_payload_hash(snapshot: Dictionary) -> String:
    var canonical := _canonicalize(snapshot.duplicate(true))
    canonical["integrity_metadata"]["payload_hash"] = ""
    return canonical_json(canonical).sha256_text()
```

- [ ] **Step 4: Validate cross references**

Validator must verify:
- every stored equipment key matches `equipment_uid`
- every `AttemptIntent.equipment_uid` exists unless action type is campaign-global
- every unacknowledged envelope has unique `envelope_id`
- `intent_id` may be empty only for non-random informational results
- `save_revision >= applied_revision >= created_revision`

- [ ] **Step 5: Run tests**

```bash
python tools/validate_save_contract.py
python -m unittest tests/test_save_contract.py
godot --headless --path . --script res://tests/unit/test_campaign_validator.gd
```

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/application/save/campaign_serializer.gd scripts/application/save/campaign_validator.gd tools/validate_save_contract.py tests/test_save_contract.py tests/unit/test_campaign_validator.gd
git commit -m "feat: add canonical campaign serialization and validation"
```

---

### Task 3: Atomic writer and safe backup rotation

**Files:**
- Create: `scripts/application/save/atomic_save_writer.gd`
- Test: `tests/unit/test_atomic_save_writer.gd`

**Interfaces:**
- Consumes: serializer and validator from Task 2.
- Produces: `write_verified(snapshot) -> Dictionary` and `restore_verified(source_path) -> Dictionary`.

- [ ] **Step 1: Write failing filesystem tests with an isolated user-data directory**

Required cases:
1. valid tmp replaces primary
2. invalid tmp leaves primary byte-identical
3. corrupt primary never becomes backup1
4. backup1 moves to backup2 only after validation
5. simulated rename failure preserves at least one valid file
6. repeated same revision is rejected

```gdscript
var result := writer.write_verified(snapshot)
_expect(result["ok"], "정상 snapshot 저장은 성공해야 합니다.")
_expect(_read(primary_path) != "", "primary가 생성되어야 합니다.")
_expect(_read(backup_1_path) == old_primary_bytes, "직전 정상 primary만 backup1이어야 합니다.")
```

- [ ] **Step 2: Run and verify failure**

```bash
godot --headless --path . --script res://tests/unit/test_atomic_save_writer.gd
```

- [ ] **Step 3: Implement write sequence**

```text
serialize → validate → write tmp → close → read tmp → validate again
→ inspect existing primary
→ rotate only verified primary/backups
→ rename tmp to primary
→ final read-back validation
```

Use `FileAccess`, `DirAccess.rename_absolute`, and dependency-injected file operations for failure simulation. Do not delete the last known valid file.

- [ ] **Step 4: Add storage-space preflight**

`write_verified()` returns `STORAGE_UNAVAILABLE` before domain mutation when temp file creation or flush is unavailable.

- [ ] **Step 5: Run tests and commit**

```bash
godot --headless --path . --script res://tests/unit/test_atomic_save_writer.gd
git add scripts/application/save/atomic_save_writer.gd tests/unit/test_atomic_save_writer.gd
git commit -m "feat: add verified atomic save and backup rotation"
```

---

### Task 4: Save inspection, migration dispatch and recovery

**Files:**
- Create: `scripts/application/save/save_inspector.gd`
- Create: `scripts/application/save/save_migrator.gd`
- Create: `scripts/application/save/recovery_coordinator.gd`
- Test: `tests/unit/test_save_inspector.gd`
- Test: `tests/unit/test_save_migrator.gd`
- Test: `tests/integration/test_continue_recovery_flow.gd`

**Interfaces:**
- Produces: `SaveInspector.inspect_all() -> Dictionary` with `status`, `selected_path`, `metadata`, `recovery_impact`.
- Produces: `SaveMigrator.migrate(snapshot, target_version) -> Dictionary`.
- Produces: `RecoveryCoordinator.restore_selected_candidate(inspect_result) -> Dictionary`.

- [ ] **Step 1: Write failing status matrix tests**

Cases:
- no files → `NO_SAVE`
- valid primary → `VALID_PRIMARY`
- corrupt primary + valid backup1 → `RECOVERABLE_BACKUP`
- corrupt primary and backup1 + valid backup2 → `RECOVERABLE_BACKUP`
- all corrupt → `UNRECOVERABLE_CORRUPTION`
- older supported schema → `MIGRATION_REQUIRED`
- newer unsupported schema → `UNSUPPORTED_VERSION`

- [ ] **Step 2: Implement newest-valid-candidate selection**

Candidates are sorted by `save_revision`, then `saved_at_utc`. The user never chooses between backup files.

- [ ] **Step 3: Implement migration isolation**

```text
read source bytes
→ decode and validate old schema
→ deep-copy migration in memory
→ validate target schema
→ write migrated tmp
→ verify tmp
→ preserve original bytes in quarantine/backup
→ promote migrated primary
```

Migration failures return `MIGRATION_FAILED` and do not change source bytes.

- [ ] **Step 4: Implement recovery-impact metadata**

Return:
- selected save time
- selected game day
- revision difference
- whether unacknowledged envelopes remain
- corrupt path quarantined

- [ ] **Step 5: Run tests and commit**

```bash
godot --headless --path . --script res://tests/unit/test_save_inspector.gd
godot --headless --path . --script res://tests/unit/test_save_migrator.gd
godot --headless --path . --script res://tests/integration/test_continue_recovery_flow.gd
git add scripts/application/save tests/unit/test_save_inspector.gd tests/unit/test_save_migrator.gd tests/integration/test_continue_recovery_flow.gd
git commit -m "feat: inspect migrate and recover campaign saves"
```

---

### Task 5: AppStateCoordinator snapshot and restore boundary

**Files:**
- Create: `scripts/application/app_state_coordinator.gd`
- Modify: `scripts/forging/forging_session.gd`
- Modify: `scripts/enhancement/enhancement_session.gd`
- Modify: `scripts/economy/workshop_resources.gd`
- Modify: `scripts/progression/workshop_calendar.gd`
- Modify: `scripts/world/equipment_world_registry.gd`
- Modify: `scripts/poc/equipment_lifecycle_poc_controller.gd`
- Test: `tests/integration/test_save_coordinator.gd`

**Interfaces:**
- Produces: `AppStateCoordinator.snapshot() -> Dictionary`.
- Produces: `AppStateCoordinator.restore(snapshot) -> Dictionary`.
- Each domain produces `snapshot()` and `restore_from_snapshot(data) -> Dictionary`.

- [ ] **Step 1: Write round-trip tests**

Create one campaign containing:
- gold and materials
- day and fatigue
- one stored equipment
- active forging progress
- active enhancement at READY
- one customer contract and relationship
- one world registry record
- one pending ResultEnvelope

Assert `restore(snapshot).snapshot()` equals the canonicalized original snapshot except volatile timestamps.

- [ ] **Step 2: Add explicit restore methods**

Do not assign raw dictionaries directly from UI code. Each domain validates ranges and IDs.

```gdscript
func restore_from_snapshot(data: Dictionary) -> Dictionary:
    if int(data.get("gold", -1)) < 0:
        return {"ok": false, "error": "INVALID_GOLD"}
    gold = int(data["gold"])
    material_stock = Dictionary(data.get("material_stock", {})).duplicate(true)
    _normalize_stock()
    return {"ok": true}
```

- [ ] **Step 3: Separate resumable and non-resumable runtime fields**

Persist:
- forging state/progress/fever counters
- enhancement equipment state, selections, pity and histories

Do not persist:
- active Tween
- Signal connections
- Node references
- current frame delta
- precision direction if the contract resets gauge position

- [ ] **Step 4: Run tests and commit**

```bash
godot --headless --path . --script res://tests/integration/test_save_coordinator.gd
git add scripts/application/app_state_coordinator.gd scripts/forging scripts/enhancement scripts/economy scripts/progression scripts/world scripts/poc tests/integration/test_save_coordinator.gd
git commit -m "feat: unify campaign snapshot and restore ownership"
```

---

### Task 6: SaveCoordinator orchestration

**Files:**
- Create: `scripts/application/save/save_coordinator.gd`
- Test: `tests/integration/test_save_coordinator.gd`

**Interfaces:**
- Produces:
  - `create_new_campaign() -> Dictionary`
  - `inspect_continue_status() -> Dictionary`
  - `load_campaign() -> Dictionary`
  - `save_checkpoint(reason: String) -> Dictionary`
  - `prepare_irreversible_action(intent: Dictionary) -> Dictionary`
  - `commit_resolved_action(intent_id: String, envelope: Dictionary) -> Dictionary`
  - `acknowledge_result(envelope_id: String) -> Dictionary`

- [ ] **Step 1: Write failing orchestration tests**

Assert:
- save revision increases exactly once per successful commit
- failed write does not mutate committed app state
- overlapping checkpoint requests serialize
- duplicate `intent_id` is rejected
- duplicate `envelope_id` is rejected

- [ ] **Step 2: Implement copy-on-commit transaction**

For irreversible actions, mutate a working copy or reversible transaction state. Only replace committed AppState after `commit_resolved_action()` writes a verified snapshot.

- [ ] **Step 3: Add save reasons**

Allowed reason constants:
`NEW_CAMPAIGN_CREATED`, `FORGING_COMPLETED`, `ATTEMPT_PREPARED`, `ATTEMPT_RESOLVED`, `SALE_OR_DELIVERY_COMPLETED`, `WORLD_RESULT_APPLIED`, `DAY_ENDED`, `RESULT_ACKNOWLEDGED`, `RETURN_TO_MAIN_MENU`, `APPLICATION_PAUSED`, `ACTIVE_WORK_CHECKPOINT`.

- [ ] **Step 4: Run and commit**

```bash
godot --headless --path . --script res://tests/integration/test_save_coordinator.gd
git add scripts/application/save/save_coordinator.gd tests/integration/test_save_coordinator.gd
git commit -m "feat: coordinate campaign save transactions"
```

---

### Task 7: Enhancement AttemptIntent and no-reroll recovery

**Files:**
- Modify: `scripts/enhancement/enhancement_session.gd`
- Modify: `scripts/economy/workshop_resources.gd`
- Modify: `scripts/ui/enhancement_screen.gd`
- Create: `tests/integration/test_irreversible_action_recovery.gd`

**Interfaces:**
- Consumes: `SaveCoordinator.prepare_irreversible_action()` and `commit_resolved_action()`.
- Produces: deterministic attempt resolution from stored RNG commitment.

- [ ] **Step 1: Write crash-boundary tests**

1. exit after PREPARED before resource consumption → restore before snapshot
2. exit after resource consumption before result commit → restore before snapshot
3. exit after RESOLVED commit before UI → same stored result
4. reopen result overlay repeatedly → RNG call count remains zero
5. duplicate intent retry → no additional gold/material deduction

- [ ] **Step 2: Replace randomize-at-construction dependency for committed attempts**

At PREPARED time store a deterministic RNG commitment:

```gdscript
{
    "seed": campaign_rng_seed,
    "draw_index": campaign_rng_draw_index,
    "roll": committed_roll,
    "leap_roll": committed_leap_roll
}
```

Resolution consumes stored values. It never calls `rng.randf()` when commitment exists.

- [ ] **Step 3: Enforce order**

```text
preview conditions
→ PREPARED save
→ consume cost/materials in transaction
→ resolve from commitment
→ build envelope
→ RESOLVED/APPLIED save
→ emit UI signal
```

- [ ] **Step 4: Run and commit**

```bash
godot --headless --path . --script res://tests/integration/test_irreversible_action_recovery.gd
git add scripts/enhancement/enhancement_session.gd scripts/economy/workshop_resources.gd scripts/ui/enhancement_screen.gd tests/integration/test_irreversible_action_recovery.gd
git commit -m "feat: make enhancement attempts crash-safe and deterministic"
```

---

### Task 8: ResultEnvelope queue and overlay

**Files:**
- Create: `scripts/application/results/result_envelope_queue.gd`
- Create: `scripts/ui/result_envelope_overlay.gd`
- Create: `scenes/ui/result_envelope_overlay.tscn`
- Test: `tests/unit/test_result_envelope_queue.gd`
- Modify: existing forging, delivery and world-result controllers to enqueue envelopes.

**Interfaces:**
- Produces: `enqueue_applied(envelope)`, `next_unacknowledged()`, `mark_presented(id)`, `acknowledge(id)`.

- [ ] **Step 1: Write queue-order and idempotency tests**

- order by `applied_revision`, then `envelope_id`
- `ACKNOWLEDGED` excluded from active queue
- duplicate envelope ID rejected
- `PRESENTED` after restart remains displayable
- acknowledgement save failure keeps envelope unacknowledged

- [ ] **Step 2: Implement generic overlay rendering**

Overlay consumes fields only; it must not recompute outcomes. It renders:
- result title and outcome
- subject equipment
- resource changes
- ownership/relationship/fate changes
- chronology entries
- one explicit acknowledgement button

- [ ] **Step 3: Route all irreversible results**

At minimum:
- forging completion
- enhancement result
- customer sale/delivery
- world result
- permanent destruction or fate change

- [ ] **Step 4: Run and commit**

```bash
godot --headless --path . --script res://tests/unit/test_result_envelope_queue.gd
godot --headless --path . --script res://tests/integration/test_irreversible_action_recovery.gd
git add scripts/application/results scripts/ui/result_envelope_overlay.gd scenes/ui/result_envelope_overlay.tscn tests
git commit -m "feat: persist and present irreversible result envelopes"
```

---

### Task 9: Main menu continue, recovery and new-game replacement

**Files:**
- Create: `scripts/ui/main_menu_controller.gd`
- Create: `scenes/ui/main_menu.tscn`
- Create: `scenes/application/boot.tscn`
- Create: `scenes/application/blacksmith_app.tscn`
- Modify: `project.godot`
- Create: `tests/integration/test_new_game_replacement.gd`
- Extend: `tests/integration/test_continue_recovery_flow.gd`

**Interfaces:**
- Consumes: `SaveCoordinator.inspect_continue_status()`, `load_campaign()`, `create_new_campaign()`.

- [ ] **Step 1: Write status-to-UI tests**

Assert exact behavior for all seven SaveStatus values. `RECOVERABLE_BACKUP` button text must be `복구 후 이어하기`.

- [ ] **Step 2: Implement save metadata panel**

Display only:
- last saved time
- game day
- last safe view
- equipment count
- unacknowledged-result notice
- schema version

Do not reveal pending outcome details.

- [ ] **Step 3: Implement recovery confirmation**

Display selected backup time, rollback duration, game day, pending-result preservation and quarantine notice. Do not display backup filename or allow candidate selection.

- [ ] **Step 4: Implement new-game replacement transaction**

Button label: `기존 기록을 교체하고 새 게임`.

Create and validate new campaign temporary save first. Simulated first-save failure must preserve every existing campaign file byte-for-byte.

- [ ] **Step 5: Set product boot scene**

Only after menu and boot tests pass:

```ini
[application]
run/main_scene="res://scenes/application/boot.tscn"
```

- [ ] **Step 6: Run and commit**

```bash
godot --headless --editor --path . --quit
godot --headless --path . --script res://tests/integration/test_continue_recovery_flow.gd
godot --headless --path . --script res://tests/integration/test_new_game_replacement.gd
git add scenes/application scenes/ui/main_menu.tscn scripts/ui/main_menu_controller.gd project.godot tests/integration
git commit -m "feat: add save-aware main menu and recovery flow"
```

---

### Task 10: Settings and Android lifecycle save hooks

**Files:**
- Create: `scripts/application/settings/settings_store.gd`
- Test: `tests/unit/test_settings_store.gd`
- Modify: `scripts/application/app_state_coordinator.gd` or root app controller for notifications.

**Interfaces:**
- Produces: `SettingsStore.load_or_defaults()`, `save(settings)`.

- [ ] **Step 1: Write settings corruption tests**

A corrupt `settings.cfg` must recreate defaults without reading, deleting or rewriting campaign files.

- [ ] **Step 2: Implement exact settings keys**

```ini
[audio]
music_volume=1.0
sfx_volume=1.0

[feedback]
vibration=true
reduced_motion=false

[accessibility]
precision_assist=false
text_size="NORMAL"
extra_status_labels=true
```

- [ ] **Step 3: Handle application notifications**

On `NOTIFICATION_APPLICATION_PAUSED` and `NOTIFICATION_WM_CLOSE_REQUEST`, request a serialized save. Do not claim guaranteed completion when the OS kills the process; correctness depends on the previous event-level commits.

- [ ] **Step 4: Add back-button rule**

Android back closes top overlay first, then asks to return to main. It must not dismiss an unacknowledged irreversible result without storing its state.

- [ ] **Step 5: Run and commit**

```bash
godot --headless --path . --script res://tests/unit/test_settings_store.gd
git add scripts/application/settings scripts/application/app_state_coordinator.gd tests/unit/test_settings_store.gd
git commit -m "feat: persist settings and handle mobile lifecycle saves"
```

---

### Task 11: CI, validators and end-to-end gates

**Files:**
- Modify: `tests/README.md`
- Modify: `.github/workflows/godot-validation.yml`
- Modify: `docs/CI_EXECUTION_POLICY.md`
- Test: all new tests.

**Interfaces:**
- Produces: mandatory save-contract CI lane and explicit external validation checklist.

- [ ] **Step 1: Add CI commands**

```bash
python tools/validate_save_contract.py
python -m unittest tests/test_save_contract.py
godot --headless --path . --script res://tests/unit/test_campaign_validator.gd
godot --headless --path . --script res://tests/unit/test_atomic_save_writer.gd
godot --headless --path . --script res://tests/unit/test_save_inspector.gd
godot --headless --path . --script res://tests/unit/test_save_migrator.gd
godot --headless --path . --script res://tests/unit/test_attempt_intent.gd
godot --headless --path . --script res://tests/unit/test_result_envelope_queue.gd
godot --headless --path . --script res://tests/unit/test_settings_store.gd
godot --headless --path . --script res://tests/integration/test_save_coordinator.gd
godot --headless --path . --script res://tests/integration/test_continue_recovery_flow.gd
godot --headless --path . --script res://tests/integration/test_irreversible_action_recovery.gd
godot --headless --path . --script res://tests/integration/test_new_game_replacement.gd
```

- [ ] **Step 2: Add zero-tolerance assertions**

The CI summary must report zero for:
- save state duplication
- result reroll on restart
- result double apply
- resource loss without result
- corrupt-primary backup poisoning
- new-game failure data loss
- migration source overwrite

- [ ] **Step 3: Preserve manual gates**

Do not mark PASS for:
- Android process-death testing
- device storage-full simulation
- safe-area and back-button behavior
- minimum six-person comprehension test

- [ ] **Step 4: Run full existing and new suites**

```bash
python tools/validate_game_data.py
python tools/validate_save_contract.py
python -m unittest discover tests
godot --headless --editor --path . --quit
# Run every command listed in tests/README.md and all new save tests.
```

Expected: all automated tests exit 0; external gates remain `NOT_RUN` until executed.

- [ ] **Step 5: Commit**

```bash
git add tests/README.md .github/workflows/godot-validation.yml docs/CI_EXECUTION_POLICY.md
git commit -m "ci: enforce save recovery and result idempotency contracts"
```

---

## Spec Coverage Self-Review

- Single campaign and two backups: Tasks 1, 3, 4.
- SaveStatus and continue: Tasks 4, 9.
- Corruption recovery and quarantine: Tasks 3, 4, 9.
- New-game replacement safety: Task 9.
- Campaign Snapshot ownership: Tasks 2, 5, 6.
- AttemptIntent PREPARED/RESOLVED: Tasks 1, 6, 7.
- ResultEnvelope lifecycle and queue: Tasks 1, 7, 8.
- Settings separation: Task 10.
- Android pause/process death: Tasks 7, 10, 11.
- Migration source preservation: Tasks 4, 11.
- Automated, device and human gates: Task 11.

## Placeholder Scan

- `TBD`, `TODO`, `implement later`, unspecified error handling: none.
- Exact filenames, interfaces, test commands and failure expectations: present.
- Runtime execution authorization: explicitly blocked until user gates complete.

## Execution Status

```text
PLAN_STATUS: COMPLETE
IMPLEMENTATION_EXECUTION: BLOCKED
REQUIRED_NEXT_PROJECT_WORK: Base analysis and full Blacksmith planning re-audit
```
