# Blacksmith Godot Vertical Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Godot 4.7.1 vertical slice where one sword is forged, receives a persistent UID and birth facts, is enhanced through +10, assigned to a customer and schedule, gains damage or chronicle history, is saved and loaded, and returns as the same item.

**Architecture:** Add an isolated `vertical_slice` namespace instead of extending the historical POC model. Domain objects are plain typed GDScript classes, data comes from versioned JSON presets, and one SaveEnvelope persists item identity, RNG seeds, schedule state, and append-only ledgers. UI scenes consume services through explicit interfaces and never own canonical calculations.

**Tech Stack:** Godot 4.7.1, GDScript 2.0, JSON, `FileAccess`, `DirAccess`, existing headless test runner patterns, Python contract tests, GitHub Actions.

## Global Constraints

- `RED → GREEN → REFACTOR` is required for every task.
- Current approved R2 canon remains authoritative.
- `PRODUCT_IMPLEMENTATION: BLOCKED` until the Batch 006 proposal is explicitly approved and merged.
- `HUMAN_PLAYTEST: NOT_RUN` until real external testers complete the protocol.
- New production files live under `scripts/vertical_slice/`, `data/vertical_slice/`, `scenes/vertical_slice/`, and `tests/vertical_slice/`.
- Do not import the historical `STANDARD / GOOD / PERFECT` quality model into the new namespace.
- Do not expose or store a secondary-material slot.
- Do not use a generic `affixes` array; use `grade_affix`, `catalyst_affix`, and `chronicle_affix` fields.
- Exact values come from preset `VS-2026.08.06-A` and are not final balance.
- Save/load must not reroll crafting grade, customer result, schedule result, or any already resolved RNG event.
- Every mutation of a work item appends an item-ledger entry.
- Mobile interaction targets are at least 48dp and information is never conveyed by color alone.

---

## File Structure

### Data

- Create `data/vertical_slice/vertical_slice_preset.json`: exact representative materials, grade rolls, enhancement values, customers, schedules, and acceptance metadata.
- Create `data/vertical_slice/vertical_slice_schema.json`: allowed field names, enums, and version identifiers used by Python and GDScript validators.

### Domain and services

- Create `scripts/vertical_slice/domain/vs_item.gd`: typed item state and serialization.
- Create `scripts/vertical_slice/domain/vs_ledger_entry.gd`: append-only ledger entry.
- Create `scripts/vertical_slice/domain/vs_save_envelope.gd`: versioned run state.
- Create `scripts/vertical_slice/services/vs_uid_service.gd`: 32-lower-hex UID generation and collision checks.
- Create `scripts/vertical_slice/services/vs_save_service.gd`: atomic JSON save/load.
- Create `scripts/vertical_slice/services/vs_forge_service.gd`: three-zone input, grade roll, birth facts.
- Create `scripts/vertical_slice/services/vs_enhancement_service.gd`: +0~+10 attempts, pity, +10 precision result.
- Create `scripts/vertical_slice/services/vs_customer_service.gd`: maximum-load gate and explainable success estimate.
- Create `scripts/vertical_slice/services/vs_schedule_service.gd`: personal/world schedule resolution.
- Create `scripts/vertical_slice/services/vs_chronicle_service.gd`: damage, repair, chronicle-affix selection.

### UI and scenes

- Create `scripts/vertical_slice/ui/vs_app.gd`: explicit screen-state router.
- Create `scripts/vertical_slice/ui/vs_forge_screen.gd`.
- Create `scripts/vertical_slice/ui/vs_enhancement_screen.gd`.
- Create `scripts/vertical_slice/ui/vs_customer_screen.gd`.
- Create `scripts/vertical_slice/ui/vs_result_screen.gd`.
- Create `scripts/vertical_slice/ui/vs_item_detail_panel.gd`.
- Create `scenes/vertical_slice/vertical_slice_app.tscn`.
- Create one focused scene per screen under `scenes/vertical_slice/screens/`.

### Tests

- Create unit tests under `tests/vertical_slice/unit/`.
- Create integration tests under `tests/vertical_slice/integration/`.
- Create `tests/vertical_slice/run_vertical_slice_suite.gd` as the headless suite entry.
- Create `tests/test_vertical_slice_data_contract.py` for JSON and namespace governance.

---

### Task 1: Vertical Slice Schema and Save Envelope

**Files:**
- Create: `data/vertical_slice/vertical_slice_preset.json`
- Create: `data/vertical_slice/vertical_slice_schema.json`
- Create: `scripts/vertical_slice/domain/vs_ledger_entry.gd`
- Create: `scripts/vertical_slice/domain/vs_item.gd`
- Create: `scripts/vertical_slice/domain/vs_save_envelope.gd`
- Create: `scripts/vertical_slice/services/vs_uid_service.gd`
- Create: `scripts/vertical_slice/services/vs_save_service.gd`
- Create: `tests/vertical_slice/unit/test_vs_item.gd`
- Create: `tests/vertical_slice/unit/test_vs_save_service.gd`
- Create: `tests/test_vertical_slice_data_contract.py`

**Interfaces:**
- Produces: `VSItem.from_dict(value: Dictionary) -> VSItem`
- Produces: `VSItem.to_dict() -> Dictionary`
- Produces: `VSLedgerEntry.create(sequence: int, event_id: String, event_type: String, source_decision_id: String, before_digest: String, after_digest: String, game_day: int, payload: Dictionary) -> VSLedgerEntry`
- Produces: `VSUidService.create_uid(existing_ids: Dictionary) -> String`
- Produces: `VSSaveService.save_envelope(envelope: VSSaveEnvelope) -> Error`
- Produces: `VSSaveService.load_envelope() -> VSSaveEnvelope`

- [ ] **Step 1: Write failing Python and GDScript schema tests**

```python
class VerticalSliceDataContractTests(unittest.TestCase):
    def test_preset_and_schema_versions_match(self) -> None:
        preset = json.loads(PRESET.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(preset["schema_version"], 1)
        self.assertEqual(preset["preset_version"], "VS-2026.08.06-A")
        self.assertEqual(schema["schema_version"], 1)
        self.assertFalse(preset["is_final_balance"])

    def test_no_historical_fields_enter_new_namespace(self) -> None:
        for path in NEW_NAMESPACE_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn("secondary_material", source)
            self.assertNotIn('"affixes"', source)
            self.assertNotIn("STANDARD", source)
            self.assertNotIn("GOOD", source)
            self.assertNotIn("PERFECT", source)
```

```gdscript
func _test_round_trip_preserves_birth_facts() -> void:
    var item := VSItem.new()
    item.uid = "BSI-0123456789abcdef0123456789abcdef"
    item.birth_rng_seed = 712345
    item.crafting_grade = "MASTERWORK"
    item.artistry = 7
    var restored := VSItem.from_dict(item.to_dict())
    _expect(restored.uid == item.uid, "UID changed during round trip")
    _expect(restored.birth_rng_seed == item.birth_rng_seed, "seed changed")
    _expect(restored.crafting_grade == item.crafting_grade, "grade changed")
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python -m unittest tests.test_vertical_slice_data_contract -v
Godot_v4.7.1 --headless --path . --script tests/vertical_slice/unit/test_vs_item.gd
Godot_v4.7.1 --headless --path . --script tests/vertical_slice/unit/test_vs_save_service.gd
```

Expected: FAIL because data and classes do not exist.

- [ ] **Step 3: Implement typed item and ledger serialization**

```gdscript
class_name VSItem
extends RefCounted

var uid: String = ""
var birth_rng_seed: int = 0
var primary_material_id: String = ""
var equipment_group: String = "SWORD"
var role_profile: String = "PHYSICAL_WEAPON_ATTACK"
var crafting_grade: String = "NORMAL"
var artistry: int = 0
var raw_role_stat: int = 0
var weight_point: int = 0
var function_capacity: int = 0
var functions: Array[String] = []
var grade_affix: String = ""
var catalyst_affix: String = ""
var chronicle_affix: String = ""
var enhancement_level: int = 0
var enhancement_failure_streak: int = 0
var used_precision_milestones: Array[int] = []
var damage_state: String = "INTACT"
var owner_id: String = "PLAYER"
var ledger: Array[Dictionary] = []
```

`to_dict()` must emit every field explicitly. `from_dict()` must reject an unsupported `schema_version`, clamp no values silently, and return an error result through `VSSaveEnvelope.validation_errors` rather than inventing defaults for required birth facts.

- [ ] **Step 4: Implement atomic save service**

```gdscript
const SAVE_PATH := "user://blacksmith_vertical_slice_v1.json"
const TEMP_PATH := "user://blacksmith_vertical_slice_v1.tmp"

func save_envelope(envelope: VSSaveEnvelope) -> Error:
    var file := FileAccess.open(TEMP_PATH, FileAccess.WRITE)
    if file == null:
        return FileAccess.get_open_error()
    file.store_string(JSON.stringify(envelope.to_dict(), "  "))
    file.flush()
    file.close()
    if FileAccess.file_exists(SAVE_PATH):
        var remove_error := DirAccess.remove_absolute(ProjectSettings.globalize_path(SAVE_PATH))
        if remove_error != OK:
            return remove_error
    return DirAccess.rename_absolute(
        ProjectSettings.globalize_path(TEMP_PATH),
        ProjectSettings.globalize_path(SAVE_PATH),
    )
```

`load_envelope()` must return the previously saved grade, RNG seed, result events, and ledger without invoking any roll service.

- [ ] **Step 5: Run tests and verify GREEN**

Expected: all schema, UID-format, round-trip, atomic-path, and no-reroll tests PASS.

- [ ] **Step 6: Commit**

```bash
git add data/vertical_slice scripts/vertical_slice/domain scripts/vertical_slice/services/vs_uid_service.gd scripts/vertical_slice/services/vs_save_service.gd tests/vertical_slice/unit tests/test_vertical_slice_data_contract.py
git commit -m "feat: add vertical slice item and save schema"
```

---

### Task 2: App Shell and Screen Routing

**Files:**
- Create: `scripts/vertical_slice/ui/vs_app.gd`
- Create: `scenes/vertical_slice/vertical_slice_app.tscn`
- Create: `scenes/vertical_slice/screens/vs_title_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_workshop_screen.tscn`
- Create: `tests/vertical_slice/unit/test_vs_app_state.gd`

**Interfaces:**
- Consumes: `VSSaveService.load_envelope()`
- Produces: `VSApp.transition_to(next_state: String, payload: Dictionary = {}) -> void`
- Produces signals: `state_changed(previous: String, current: String)` and `item_selected(uid: String)`

- [ ] **Step 1: Write the failing state-transition test**

```gdscript
func _test_only_declared_transitions_are_allowed() -> void:
    var app := VSApp.new()
    _expect(app.current_state == "TITLE", "initial state must be TITLE")
    _expect(app.can_transition("TITLE", "WORKSHOP"), "TITLE to WORKSHOP missing")
    _expect(not app.can_transition("TITLE", "RESULT"), "TITLE must not skip to RESULT")
```

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because `VSApp` does not exist.

- [ ] **Step 3: Implement explicit state graph**

```gdscript
const ALLOWED_TRANSITIONS := {
    "TITLE": ["WORKSHOP"],
    "WORKSHOP": ["FORGE", "ITEM_DETAIL"],
    "FORGE": ["ITEM_BIRTH"],
    "ITEM_BIRTH": ["ENHANCEMENT", "WORKSHOP"],
    "ENHANCEMENT": ["PRECISION", "CUSTOMER", "WORKSHOP"],
    "PRECISION": ["CUSTOMER", "WORKSHOP"],
    "CUSTOMER": ["RESULT"],
    "RESULT": ["REPAIR", "ITEM_DETAIL"],
    "REPAIR": ["ITEM_DETAIL"],
    "ITEM_DETAIL": ["WORKSHOP"],
}
```

The router owns screen changes only. It must not calculate grade, enhancement, customer chance, or schedule outcomes.

- [ ] **Step 4: Build 720×1280 root scene**

Use a root `Control`, safe-area margins, one content container, one persistent item-summary header, and a minimum custom control size of 48×48 for every interactive button.

- [ ] **Step 5: Run scene smoke and unit tests**

```bash
Godot_v4.7.1 --headless --path . --editor --quit
Godot_v4.7.1 --headless --path . scenes/vertical_slice/vertical_slice_app.tscn --quit-after 2
Godot_v4.7.1 --headless --path . --script tests/vertical_slice/unit/test_vs_app_state.gd
```

- [ ] **Step 6: Commit**

```bash
git add scripts/vertical_slice/ui/vs_app.gd scenes/vertical_slice tests/vertical_slice/unit/test_vs_app_state.gd
git commit -m "feat: add vertical slice app shell"
```

---

### Task 3: Direct Forging and Item Birth

**Files:**
- Create: `scripts/vertical_slice/services/vs_forge_service.gd`
- Create: `scripts/vertical_slice/ui/vs_forge_screen.gd`
- Create: `scenes/vertical_slice/screens/vs_forge_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_item_birth_screen.tscn`
- Create: `tests/vertical_slice/unit/test_vs_forge_service.gd`
- Create: `tests/vertical_slice/integration/test_vs_forge_birth_flow.gd`

**Interfaces:**
- Consumes: material preset and `VSUidService`
- Produces: `VSForgeService.create_item(material_id: String, zone_results: Array[int], rng_seed: int, existing_ids: Dictionary) -> VSItem`

- [ ] **Step 1: Write failing deterministic birth tests**

```gdscript
func _test_same_seed_and_inputs_create_same_birth_facts() -> void:
    var first := forge.create_item("silver", [2, 2, 2], 44221, {})
    var second := forge.create_item("silver", [2, 2, 2], 44221, {})
    _expect(first.crafting_grade == second.crafting_grade, "grade rerolled")
    _expect(first.raw_role_stat == 10, "silver high attack must be 10")
    _expect(first.artistry == 10, "silver high artistry must be 10")
    _expect(first.weight_point == 10, "silver weight must be 10")
    _expect(first.function_capacity == 1, "silver capacity must be 1")
```

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because forge service is absent.

- [ ] **Step 3: Implement three-zone validation and formulas**

```gdscript
func _zone_tier(zone_results: Array[int]) -> String:
    var total := 0
    for value in zone_results:
        assert(value >= 0 and value <= 2)
        total += value
    if total <= 2:
        return "low"
    if total <= 4:
        return "mid"
    return "high"
```

Attack uses `maxi(0, material.attack_material_fit + [5, 10, 15][tier_index])`. Artistry uses `material.artistry_tendency + [0, 3, 6][tier_index]`. Grade roll uses one seeded `RandomNumberGenerator`, persists the seed and final grade, and never runs during `from_dict()`.

- [ ] **Step 4: Implement forge screen**

The screen exposes exactly:

- primary material selection: iron, silver, meteor iron
- three zone controls with values 0, 1, 2
- pre-forge comparison showing likely attack range, artistry tendency, weight, and function capacity
- forge confirmation

It exposes no secondary-material input.

- [ ] **Step 5: Verify GREEN and scene smoke**

Expected: deterministic item birth, five-grade mapping, three explicit affix fields, and item-birth summary all PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/vertical_slice/services/vs_forge_service.gd scripts/vertical_slice/ui/vs_forge_screen.gd scenes/vertical_slice/screens tests/vertical_slice
git commit -m "feat: add vertical slice direct forging"
```

---

### Task 4: General and Precision Enhancement

**Files:**
- Create: `scripts/vertical_slice/services/vs_enhancement_service.gd`
- Create: `scripts/vertical_slice/ui/vs_enhancement_screen.gd`
- Create: `scenes/vertical_slice/screens/vs_enhancement_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_precision_screen.tscn`
- Create: `tests/vertical_slice/unit/test_vs_enhancement_service.gd`
- Create: `tests/vertical_slice/integration/test_vs_enhancement_to_precision.gd`

**Interfaces:**
- Produces: `attempt(item: VSItem, rng_seed: int) -> Dictionary`
- Produces: `apply_precision_choice(item: VSItem, choice: String, catalyst_id: String = "") -> Error`

- [ ] **Step 1: Write failing attempt and pity tests**

```gdscript
func _test_failure_adds_pity_without_changing_artistry() -> void:
    var item := fixture_item(9)
    item.artistry = 10
    var result := service.attempt_with_forced_roll(item, 99.0, 10.0)
    _expect(result.outcome == "HOLD" or result.outcome == "DOWNGRADE", "invalid failure")
    _expect(item.enhancement_failure_streak == 1, "pity missing")
    _expect(item.artistry == 10, "general enhancement changed artistry")
```

- [ ] **Step 2: Run and verify RED**

- [ ] **Step 3: Implement +0~+10 rules**

Base success: `100/80/65/50`, pity `+5%p`, cap `95%`. On success increment one level and reset pity. On hold retain level. On downgrade subtract one level with floor 0. Destruction is disabled in preset A. Every attempt appends exactly one ledger entry.

- [ ] **Step 4: Implement +10 exclusive choice**

```gdscript
match choice:
    "ATTACK_PACKAGE":
        item.raw_role_stat += 5
    "LIGHTWEIGHT":
        item.weight_point = maxi(0, item.weight_point - 5)
    "FUNCTION_REWORK":
        pass
    _:
        return ERR_INVALID_PARAMETER
item.used_precision_milestones.append(10)
```

Reject a second +10 call. If `salamander_core` is selected, set `catalyst_affix = "EMBER_TOUCHED"`. Add `ELEMENTAL_WARD(FIRE)` only when function capacity is available and the player selected the function-rework lane or an empty capacity slot is valid under the canonical recipe.

- [ ] **Step 5: Run GREEN tests and integration flow**

Verify one-input-one-result, no grade/artistry reroll, mutually exclusive output, catalyst seed persistence, and same-milestone rejection.

- [ ] **Step 6: Commit**

```bash
git add scripts/vertical_slice/services/vs_enhancement_service.gd scripts/vertical_slice/ui/vs_enhancement_screen.gd scenes/vertical_slice/screens tests/vertical_slice
git commit -m "feat: add vertical slice enhancement decisions"
```

---

### Task 5: Customer, Schedule, and Explainable Fit

**Files:**
- Create: `scripts/vertical_slice/services/vs_customer_service.gd`
- Create: `scripts/vertical_slice/services/vs_schedule_service.gd`
- Create: `scripts/vertical_slice/ui/vs_customer_screen.gd`
- Create: `scenes/vertical_slice/screens/vs_customer_screen.tscn`
- Create: `tests/vertical_slice/unit/test_vs_customer_service.gd`
- Create: `tests/vertical_slice/unit/test_vs_schedule_service.gd`
- Create: `tests/vertical_slice/integration/test_vs_customer_assignment.gd`

**Interfaces:**
- Produces: `evaluate(item: VSItem, customer_id: String) -> Dictionary`
- Produces: `assign(item: VSItem, customer_id: String) -> Error`
- Produces: `resolve_personal_schedule(item: VSItem, customer_id: String, rng_seed: int) -> Dictionary`
- Produces: `resolve_world_schedule(item: VSItem, event_id: String, rng_seed: int) -> Dictionary`

- [ ] **Step 1: Write failing load-gate and reason tests**

```gdscript
func _test_noble_blocks_iron_but_accepts_silver() -> void:
    var iron := fixture_item("iron", 15)
    var silver := fixture_item("silver", 10)
    _expect(service.evaluate(iron, "ceremonial_noble").assignable == false, "iron must be overweight")
    _expect(service.evaluate(silver, "ceremonial_noble").assignable == true, "silver must fit")
```

```gdscript
func _test_summary_contains_two_to_four_reasons() -> void:
    var evaluation := service.evaluate(fixture_item("silver", 10), "ceremonial_noble")
    _expect(evaluation.summary_reasons.size() >= 2, "too few reasons")
    _expect(evaluation.summary_reasons.size() <= 4, "too many reasons")
```

- [ ] **Step 2: Run and verify RED**

- [ ] **Step 3: Implement customer formula**

```gdscript
var raw_percent := 35 + item.enhancement_level * 4
raw_percent += role_fit_modifier
raw_percent += material_or_function_modifier
raw_percent += artistry_modifier
raw_percent += judgment_risk_modifier
var exact_percent := clampi(raw_percent, 5, 95)
var displayed_percent := int(round(exact_percent / 10.0) * 10.0)
```

Return `assignable`, `load_status`, `exact_percent`, `displayed_percent`, `summary_reasons`, and `all_reasons`. Overweight returns `assignable = false` before success calculation.

- [ ] **Step 4: Implement personal and world schedule records**

Personal: `ARENA_BOUT_DAY_2`. World: `GRANARY_FIRE_DAY_4`. Store announced day, resolved day, selected item UID, persisted RNG seed, outcome, and reason list. A resolved schedule rejects a second resolution request.

- [ ] **Step 5: Implement progressive-disclosure customer screen**

Layer 1: identity, deadline, demand, selected item.

Layer 2: assignable status, rounded success estimate, 2~4 reasons.

Layer 3: exact internal percentage, all modifiers, item fields, schedule details.

Every status uses text plus icon; buttons meet 48dp.

- [ ] **Step 6: Verify GREEN and commit**

```bash
git add scripts/vertical_slice/services/vs_customer_service.gd scripts/vertical_slice/services/vs_schedule_service.gd scripts/vertical_slice/ui/vs_customer_screen.gd scenes/vertical_slice/screens tests/vertical_slice
git commit -m "feat: add explainable customer and schedule flow"
```

---

### Task 6: Chronicle, Repair, and Same-UID Return

**Files:**
- Create: `scripts/vertical_slice/services/vs_chronicle_service.gd`
- Create: `scripts/vertical_slice/ui/vs_result_screen.gd`
- Create: `scripts/vertical_slice/ui/vs_item_detail_panel.gd`
- Create: `scenes/vertical_slice/screens/vs_result_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_repair_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_item_detail_screen.tscn`
- Create: `tests/vertical_slice/unit/test_vs_chronicle_service.gd`
- Create: `tests/vertical_slice/integration/test_vs_same_uid_return.gd`

**Interfaces:**
- Produces: `apply_schedule_result(item: VSItem, result: Dictionary) -> void`
- Produces: `repair(item: VSItem, game_day: int, resource_state: Dictionary) -> Error`
- Produces: `select_display_chronicle_affix(item: VSItem) -> String`

- [ ] **Step 1: Write failing same-UID and no-reroll integration test**

```gdscript
func _test_result_repair_save_load_returns_same_item() -> void:
    var original := fixture_item("BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    chronicle.apply_schedule_result(original, forced_failure_result())
    _expect(original.damage_state == "DAMAGED", "failure must damage item")
    var grade_before := original.crafting_grade
    var artistry_before := original.artistry
    _expect(chronicle.repair(original, 5, {"repair_kit": 1}) == OK, "repair failed")
    save_service.save_envelope(envelope_with(original))
    var loaded := save_service.load_envelope().items_by_uid[original.uid]
    _expect(loaded.uid == original.uid, "UID changed")
    _expect(loaded.crafting_grade == grade_before, "repair/load changed grade")
    _expect(loaded.artistry == artistry_before, "repair/load changed artistry")
    _expect(loaded.ledger.size() >= 3, "birth/result/repair ledger missing")
```

- [ ] **Step 2: Run and verify RED**

- [ ] **Step 3: Implement damage and repair**

Outcome mapping: success keeps `INTACT`, partial success sets `WORN`, failure sets `DAMAGED`. Repair consumes one `repair_kit`, advances one game day, sets `INTACT`, preserves birth grade and artistry, and appends a `REPAIR` ledger event. It never deletes the failure event.

- [ ] **Step 4: Implement chronicle-affix priority**

```text
RESTORED_AFTER_FAILURE > FIRE_SAVED > ARENA_TESTED
```

The selected display affix is derived from ledger events but cached as `chronicle_affix` after each relevant event. Item details always show the full history even when only one affix is displayed.

- [ ] **Step 5: Implement result and item-detail UI**

Show outcome, changed fields, unchanged birth facts, reason list, ownership, damage state, repair action, and chronological ledger. The return button routes to workshop with the same selected UID.

- [ ] **Step 6: Verify GREEN and commit**

```bash
git add scripts/vertical_slice/services/vs_chronicle_service.gd scripts/vertical_slice/ui scenes/vertical_slice/screens tests/vertical_slice
git commit -m "feat: add vertical slice chronicle and repair return"
```

---

### Task 7: End-to-End Validation and Playtest Build

**Files:**
- Create: `tests/vertical_slice/run_vertical_slice_suite.gd`
- Create: `tests/vertical_slice/integration/test_vs_end_to_end.gd`
- Create: `docs/BLACKSMITH_VERTICAL_SLICE_PLAYTEST.md`
- Modify: `.github/workflows/godot-validation.yml`
- Modify: `.github/workflows/python-validation.yml`
- Modify: `project.godot` only after the new scene passes direct scene smoke
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md` only after implementation approval and evidence exist

**Interfaces:**
- Consumes all services and screens from Tasks 1–6.
- Produces one deterministic headless path and one manual Android playtest build path.

- [ ] **Step 1: Write failing end-to-end test**

```gdscript
func _run_end_to_end() -> void:
    var item := forge.create_item("silver", [2, 2, 2], 44221, {})
    while item.enhancement_level < 10:
        enhancement.attempt_with_scripted_result(item, "SUCCESS")
    _expect(enhancement.apply_precision_choice(item, "FUNCTION_REWORK", "salamander_core") == OK, "precision failed")
    var evaluation := customer.evaluate(item, "ceremonial_noble")
    _expect(evaluation.assignable, "silver item should fit noble")
    var result := schedule.resolve_world_schedule_with_scripted_result(item, "GRANARY_FIRE_DAY_4", "SUCCESS")
    chronicle.apply_schedule_result(item, result)
    save.save_envelope(envelope_with(item))
    var loaded := save.load_envelope().items_by_uid[item.uid]
    _expect(loaded.uid == item.uid, "same UID return failed")
    _expect(loaded.chronicle_affix == "FIRE_SAVED", "chronicle missing")
```

- [ ] **Step 2: Run and verify RED**

- [ ] **Step 3: Add vertical-slice suite to CI**

The Godot workflow must import and parse, smoke `vertical_slice_app.tscn`, and run `tests/vertical_slice/run_vertical_slice_suite.gd`. The Python workflow must run `tests/test_vertical_slice_data_contract.py`. Preserve existing workflow-call structure and pinned actions.

- [ ] **Step 4: Run complete GREEN validation**

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
Godot_v4.7.1 --headless --path . --editor --quit
Godot_v4.7.1 --headless --path . scenes/vertical_slice/vertical_slice_app.tscn --quit-after 2
Godot_v4.7.1 --headless --path . --script tests/vertical_slice/run_vertical_slice_suite.gd
```

Expected: all existing historical POC tests and all new vertical-slice tests PASS.

- [ ] **Step 5: Switch main scene only after scene smoke PASS**

Change:

```ini
run/main_scene="res://scenes/vertical_slice/vertical_slice_app.tscn"
```

Retain direct test-scene paths for historical regression tests. Run import, scene smoke, model, integration, save round trip, and project restart again after this change.

- [ ] **Step 6: Produce manual playtest protocol**

`docs/BLACKSMITH_VERTICAL_SLICE_PLAYTEST.md` must instruct testers to:

1. create one item without guidance;
2. explain material choice;
3. decide whether to continue at +7 or later;
4. select a +10 precision path;
5. compare three customers;
6. resolve one schedule;
7. inspect damage or chronicle;
8. close and reload the application;
9. identify the same item and explain what changed;
10. report confusion, boredom, and unexpected results.

Record automated evidence separately from 3~5 external human sessions. For five testers, the proposal threshold is 3 completions, 3 correct system explanations, 3 observed stop-or-continue reasons, and 0 critical save corruption.

- [ ] **Step 7: Commit**

```bash
git add tests/vertical_slice docs/BLACKSMITH_VERTICAL_SLICE_PLAYTEST.md .github/workflows project.godot '[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md'
git commit -m "test: validate vertical slice end to end"
```

---

## Final Verification Checklist

- [ ] All current R2 canon contracts have a corresponding test or data assertion.
- [ ] No new namespace file contains secondary-material or generic-affix ownership.
- [ ] Same seed and input produce the same birth facts.
- [ ] Save/load performs no roll.
- [ ] Every mutation appends one ledger event.
- [ ] General enhancement never changes grade or artistry.
- [ ] +10 precision choice is exclusive and non-repeatable.
- [ ] Overweight customer assignment is blocked before probability calculation.
- [ ] Customer summary has 2~4 reasons and details retain exact values.
- [ ] Repair preserves grade, artistry, UID, and history.
- [ ] UI buttons meet 48dp and statuses are not color-only.
- [ ] Existing POC regression suites still pass.
- [ ] Godot 4.7.1 import, scene smoke, model, and integration suites pass.
- [ ] Human playtest remains `NOT_RUN` until performed.
- [ ] No main-scene switch occurs before the vertical-slice scene passes direct smoke.

## Self-Review

- Spec coverage: all ten Batch 006 proposal Decisions map to Tasks 1–7.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation step remains.
- Type consistency: `VSItem`, `VSSaveEnvelope`, service signatures, field names, preset version, save paths, and UID format are consistent across tasks.
- Scope: only one sword family, three primary materials, one +10 milestone, one catalyst seed, three customers, and two schedule examples are included.

Plan status: `READY_FOR_REVIEW / EXECUTION_BLOCKED_UNTIL_CANON_APPROVAL`.
