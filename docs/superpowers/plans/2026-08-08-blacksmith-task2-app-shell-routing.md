# Blacksmith Task 2 App Shell and Start-Scene Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the historical executable test scene with a save-aware MainMenu and a single `BlacksmithApp` shell that enters at `WORKSHOP`, while keeping all gameplay calculations, product assets, Android validation, and later vertical-slice screens out of Task 2.

**Architecture:** Task 2 adds engine-native Control/Container UI under the already approved vertical-slice namespace. `VSMainMenu` classifies the result of the existing `VSSaveService` without directly manipulating save files, while `VSApp` owns only a declared/implemented screen-routing boundary. The actual application entry moves through `project.godot` only after RED tests exist and the missing new-campaign initializer authority is separately resolved.

**Tech Stack:** Godot 4.7.1, GDScript 2.0, GUT 9.7.1, Python 3.11-3.13 contract tests, GitHub Actions, existing `VSSaveEnvelope` and `VSSaveService` Task 1 canon.

## Global Constraints

- Decision: `BS-VS-TASK2-20260807-01`.
- Current Blacksmith main at plan creation: `a00e864ce5de7bdf872e8093d489c8a78c058afb`.
- Current Base main observed: `fa69a77a14f923a756064f6ae151d34cadb374f7`; project operating pin remains `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e` and is not upgraded by Task 2.
- `RED → GREEN → REFACTOR` is mandatory. Observe the intended RED before any implementation code.
- General product implementation remains `BLOCKED`; only the approved scoped vertical-slice namespace may be touched.
- Allowed product paths after Entry Gate opens: `scripts/vertical_slice/ui/`, `scenes/vertical_slice/`, and `project.godot`, plus focused tests and CI routing.
- `assets/`, `addons/`, unrelated `data/`, historical POC gameplay services, and other product namespaces are out of scope.
- Do not enable Hera. Hera remains `VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE` with authoring/mutation authority `NONE`.
- HiGodot remains `PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY`; this plan does not claim production authoring authority.
- GUT 9.7.1 remains the formal GDScript test authority.
- Task 2 adds no image, audio, font, or other external product asset. Product-image generation, rights, final-screen readability, Android-device validation, and human playtest remain blocked/not run.
- Preserve the current 720×1280 portrait viewport, renderer, autoload, and plugin settings while changing only `run/main_scene` in `project.godot`.
- Every primary interactive control must have `custom_minimum_size` of at least 48×48 logical pixels.
- Enabled/disabled/error/recovery state must not be communicated by color alone.
- Save/load must never reroll already resolved facts.
- UI code must never directly delete, rename, or overwrite save files.
- A valid backup recovery returned by `VSSaveService` is loadable and must remain Continue-capable with explicit recovery status.
- No product implementation begins while the Entry Gate below is failed.

## Entry Gate — Current Verdict

```text
FAIL_CLOSED / NEW_CAMPAIGN_INITIALIZER_AUTHORITY_MISSING
```

Current canon defines that a valid `VSSaveEnvelope` must persist:

- `saved_at_utc`
- `active_run.run_id`
- `active_run.run_rng_seed`
- `active_run.current_day`
- `active_run.resolved_events`

Current canon also requires persisted run RNG and no load reroll, but no current approved source defines how a brand-new campaign creates `saved_at_utc`, `run_id`, or `run_rng_seed`. `VSSaveEnvelope.new()` is not a valid persisted campaign because `saved_at_utc` and `run_id` are empty by default. Task 2 must not invent a UUID format, clock source, or RNG seed policy.

### Required authority before Task 1 below may execute

A separate user-approved, GitHub+Sheet-synchronized Decision must define all of these items explicitly:

1. `active_run.run_id` generation rule and format.
2. `active_run.run_rng_seed` source, valid range, and whether creation is nondeterministic or externally seeded.
3. `saved_at_utc` source and serialization format/timezone.
4. The approved owner of campaign initialization: a dedicated vertical-slice service or another named current authority surface.
5. Whether New Game writes immediately before entering `BlacksmithApp`, and the exact failure behavior if that first save fails.
6. How destructive replacement interacts with the existing primary/backup rotation so an unvalidated new campaign cannot poison or destroy the prior recoverable campaign.

Until those six items exist in current authority, **stop after planning/review; do not add Task 2 product code, RED implementation commits, or `project.godot` changes.**

---

## File Structure After the Entry Gate Opens

### Runtime UI

- Create `scripts/vertical_slice/ui/vs_main_menu.gd`: save-status presentation, Continue/New Game/Settings UI coordination, no gameplay math and no direct file operations.
- Create `scripts/vertical_slice/ui/vs_app.gd`: declared-state graph, implemented-destination registry, fail-closed transition results, no gameplay math.
- Create `scenes/vertical_slice/main_menu.tscn`: separate application-entry scene using only engine-native UI controls.
- Create `scenes/vertical_slice/vertical_slice_app.tscn`: persistent campaign shell.
- Create `scenes/vertical_slice/screens/vs_workshop_screen.tscn`: minimal implemented `WORKSHOP` destination only.

### Tests

- Create `tests/test_vertical_slice_task2_app_shell_contract.py`: static scope/start-scene/mobile/no-asset/no-Hera contracts.
- Create `tests/gut/unit/vertical_slice/test_vs_main_menu.gd`: real `VSSaveService` temporary-path integration for missing, valid primary, valid backup recovery, and unrecoverable states.
- Create `tests/gut/unit/vertical_slice/test_vs_app.gd`: declared/implemented routing behavior.

### CI

- Modify `.github/workflows/python-validation.yml`: run the Task 2 Python contract in code scope.
- Modify `.github/workflows/godot-validation.yml`: smoke `main_menu.tscn` and `vertical_slice_app.tscn` while retaining historical scene smokes.
- GUT workflow already recursively runs `tests/gut/unit` and is triggered by GUT tests, `project.godot`, and scenes, so do not create a second GUT workflow.

### Project configuration

- Modify `project.godot`: only change `run/main_scene` to `res://scenes/vertical_slice/main_menu.tscn`; preserve all other application/display/autoload/editor-plugin/rendering settings.

---

### Task 0: Resolve New-Campaign Initializer Authority

**Files:**
- No product files may change in this task.
- Update current Decision/canon and Google Sheet using the separately approved initializer Decision.
- Update this plan/spec only after the Decision exists.

**Interfaces:**
- Produces an approved initializer contract consumed by Task 3.
- Must define exact creation semantics for `saved_at_utc`, `run_id`, and `run_rng_seed`.

- [ ] **Step 1: Record the six authority requirements above in the Decision proposal**

The proposal must state exact algorithms/formats rather than examples or optional alternatives.

- [ ] **Step 2: Obtain explicit user approval for that Decision**

Expected gate state before approval:

```text
NEW_CAMPAIGN_INITIALIZER_AUTHORITY_MISSING
```

No code is permitted while that state is true.

- [ ] **Step 3: Synchronize the same Decision ID to GitHub canon and Google Sheet**

Read both surfaces back after write. Any mismatch keeps the Entry Gate failed.

- [ ] **Step 4: Re-run the project Entry Gate**

Required result before Task 1:

```text
NEW_CAMPAIGN_INITIALIZER_AUTHORITY_RESOLVED
TASK2_SCOPE_CURRENT
PR131_SPEC_CURRENT
```

If any of these are absent, stop.

---

### Task 1: Define Task 2 Static Contracts — RED

**Files:**
- Create: `tests/test_vertical_slice_task2_app_shell_contract.py`
- Modify: `.github/workflows/python-validation.yml`

**Interfaces:**
- Consumes current design spec and current `project.godot`.
- Produces a focused Python contract that prevents scope expansion and proves the intended RED on current main.

- [ ] **Step 1: Write the failing contract**

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "project.godot"
MAIN_MENU = ROOT / "scenes/vertical_slice/main_menu.tscn"
APP_SCENE = ROOT / "scenes/vertical_slice/vertical_slice_app.tscn"
WORKSHOP = ROOT / "scenes/vertical_slice/screens/vs_workshop_screen.tscn"
MENU_SCRIPT = ROOT / "scripts/vertical_slice/ui/vs_main_menu.gd"
APP_SCRIPT = ROOT / "scripts/vertical_slice/ui/vs_app.gd"


class VerticalSliceTask2AppShellContractTests(unittest.TestCase):
    def test_application_entry_is_vertical_slice_main_menu(self) -> None:
        text = PROJECT.read_text(encoding="utf-8")
        self.assertIn('run/main_scene="res://scenes/vertical_slice/main_menu.tscn"', text)

    def test_required_task2_runtime_files_exist(self) -> None:
        for path in [MAIN_MENU, APP_SCENE, WORKSHOP, MENU_SCRIPT, APP_SCRIPT]:
            self.assertTrue(path.is_file(), str(path))

    def test_task2_does_not_enable_hera(self) -> None:
        text = PROJECT.read_text(encoding="utf-8")
        self.assertNotIn("addons/hera_agent_godot/plugin.cfg", text)

    def test_task2_uses_no_external_product_assets(self) -> None:
        for path in [MAIN_MENU, APP_SCENE, WORKSHOP]:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("res://assets/", text)

    def test_project_mobile_baseline_is_preserved(self) -> None:
        text = PROJECT.read_text(encoding="utf-8")
        self.assertIn("window/size/viewport_width=720", text)
        self.assertIn("window/size/viewport_height=1280", text)
        self.assertIn("window/handheld/orientation=1", text)
```

- [ ] **Step 2: Wire only this contract into code-scope Python validation**

Add after the existing Task 1 canon command in `.github/workflows/python-validation.yml`:

```yaml
      - name: Validate vertical slice Task 2 app shell contract
        if: inputs.scope == 'code'
        working-directory: project
        run: python -m unittest tests.test_vertical_slice_task2_app_shell_contract -v
```

- [ ] **Step 3: Run the contract and observe RED**

Run:

```bash
python -m unittest tests.test_vertical_slice_task2_app_shell_contract -v
```

Expected: FAIL because current main still points to `res://scenes/test/enhancement_test.tscn` and Task 2 runtime files do not exist.

Record the exact RED commit SHA. Do not add implementation in the RED commit.

- [ ] **Step 4: Commit the RED contract**

```bash
git add tests/test_vertical_slice_task2_app_shell_contract.py .github/workflows/python-validation.yml
git commit -m "test: define Task 2 app shell contract"
```

---

### Task 2: Define App Router Behavior — RED then GREEN

**Files:**
- Create: `tests/gut/unit/vertical_slice/test_vs_app.gd`
- Create: `scripts/vertical_slice/ui/vs_app.gd`

**Interfaces:**
- Produces: `VSApp.can_transition(previous_state: String, next_state: String) -> bool`
- Produces: `VSApp.transition_to(next_state: String, payload: Dictionary = {}) -> String`
- Produces: `VSApp.register_destination(state: String, scene: PackedScene) -> void`
- Produces signal: `state_changed(previous_state: String, current_state: String)`
- Result constants: `OK_TRANSITION`, `INVALID_TRANSITION`, `MISSING_DESTINATION`, `INVALID_PAYLOAD`.

- [ ] **Step 1: Write failing GUT tests**

```gdscript
extends "res://addons/gut/test.gd"

const AppScript = preload("res://scripts/vertical_slice/ui/vs_app.gd")

func test_workshop_is_initial_state() -> void:
    var app = AppScript.new()
    assert_eq(app.current_state, "WORKSHOP")

func test_declared_edge_is_distinct_from_implemented_destination() -> void:
    var app = AppScript.new()
    assert_true(app.can_transition("WORKSHOP", "FORGE"))
    assert_eq(app.transition_to("FORGE"), app.MISSING_DESTINATION)
    assert_eq(app.current_state, "WORKSHOP")

func test_undeclared_edge_fails_closed() -> void:
    var app = AppScript.new()
    assert_false(app.can_transition("WORKSHOP", "RESULT"))
    assert_eq(app.transition_to("RESULT"), app.INVALID_TRANSITION)
    assert_eq(app.current_state, "WORKSHOP")
```

- [ ] **Step 2: Run GUT and verify RED**

Run with the repository's formal GUT CLI:

```bash
./godot --headless -d -s --path "$PWD" addons/gut/gut_cmdln.gd \
  -gdir=res://tests/gut/unit/vertical_slice \
  -ginclude_subdirs \
  -gexit
```

Expected: FAIL because `vs_app.gd` does not exist.

- [ ] **Step 3: Implement the minimal router**

```gdscript
class_name VSApp
extends Control

signal state_changed(previous_state: String, current_state: String)

const OK_TRANSITION := "OK"
const INVALID_TRANSITION := "INVALID_TRANSITION"
const MISSING_DESTINATION := "MISSING_DESTINATION"
const INVALID_PAYLOAD := "INVALID_PAYLOAD"

const DECLARED_TRANSITIONS := {
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

var current_state := "WORKSHOP"
var _destinations: Dictionary = {}

func can_transition(previous_state: String, next_state: String) -> bool:
    return next_state in DECLARED_TRANSITIONS.get(previous_state, [])

func register_destination(state: String, scene: PackedScene) -> void:
    if scene != null:
        _destinations[state] = scene

func transition_to(next_state: String, payload: Dictionary = {}) -> String:
    if not can_transition(current_state, next_state):
        return INVALID_TRANSITION
    if not _destinations.has(next_state):
        return MISSING_DESTINATION
    var previous := current_state
    current_state = next_state
    state_changed.emit(previous, current_state)
    return OK_TRANSITION
```

Do not add gameplay calculations, RNG, customer logic, forge logic, or placeholder future scenes.

- [ ] **Step 4: Run focused GUT tests and verify GREEN**

Expected: router tests PASS; existing Task 1 GUT tests also remain PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/gut/unit/vertical_slice/test_vs_app.gd scripts/vertical_slice/ui/vs_app.gd
git commit -m "feat: add bounded vertical slice app router"
```

---

### Task 3: Define MainMenu Save-State Behavior — RED then GREEN

**Hard prerequisite:** Task 0 is resolved. This task must consume the approved initializer authority; it must not invent initializer semantics inside UI code.

**Files:**
- Create: `tests/gut/unit/vertical_slice/test_vs_main_menu.gd`
- Create: `scripts/vertical_slice/ui/vs_main_menu.gd`
- Consume: `scripts/vertical_slice/services/vs_save_service.gd`
- Consume: the separately approved campaign-initializer authority from Task 0.

**Interfaces:**
- Produces status constants: `MISSING`, `LOADABLE`, `RECOVERED`, `UNRECOVERABLE_OR_UNSUPPORTED`.
- Produces: `VSMainMenu.refresh_save_status() -> String`
- Produces: `VSMainMenu.request_new_game() -> String`
- Produces: `VSMainMenu.confirm_new_game_overwrite() -> Error`
- Produces signal: `campaign_ready(envelope)` only after valid Continue or successfully persisted New Game.

- [ ] **Step 1: Write real-file GUT tests against temporary save paths**

Use the existing Task 1 pattern with a dedicated path such as:

```gdscript
const TEST_SAVE_PATH := "user://blacksmith_vertical_slice_task2_menu_gut.json"
```

Cover exactly these cases:

```gdscript
func test_missing_save_disables_continue() -> void:
    # No primary and no backup.
    # Expected status MISSING and Continue disabled.
    pass

func test_valid_primary_enables_continue() -> void:
    # Save a valid envelope through VSSaveService.
    # Expected LOADABLE and Continue enabled.
    pass

func test_corrupt_primary_with_valid_backup_enables_continue_as_recovered() -> void:
    # Save two valid envelopes, corrupt primary, let VSSaveService recover backup.
    # Expected RECOVERED, Continue enabled, recovered_from_backup true.
    pass

func test_unrecoverable_save_disables_continue() -> void:
    # Corrupt primary with no valid backup.
    # Expected UNRECOVERABLE_OR_UNSUPPORTED and Continue disabled.
    pass
```

Replace the `pass` bodies with the same real `FileAccess`/`VSSaveService` fixture pattern already used in `test_vs_save_service.gd`; do not mock the save service.

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because `VSMainMenu` does not exist.

- [ ] **Step 3: Implement status classification only**

```gdscript
func refresh_save_status() -> String:
    var envelope = _save_service.load_envelope()
    if envelope.validation_errors.is_empty():
        if envelope.recovered_from_backup:
            _set_recovered_status(envelope)
            return RECOVERED
        _set_loadable_status(envelope)
        return LOADABLE
    if envelope.validation_errors.has("SAVE_NOT_FOUND"):
        _set_missing_status()
        return MISSING
    _set_unrecoverable_status(envelope.validation_errors)
    return UNRECOVERABLE_OR_UNSUPPORTED
```

The UI must not use `FileAccess` or `DirAccess` in production code.

- [ ] **Step 4: Add New Game tests only using the approved initializer contract**

Required behaviors:

- `MISSING`: no overwrite dialog; create through approved initializer; persist through save service; emit `campaign_ready` only after save returns `OK`.
- `LOADABLE` or `RECOVERED`: require explicit overwrite confirmation.
- `UNRECOVERABLE_OR_UNSUPPORTED`: require explicit overwrite confirmation; never auto-repair or auto-start.
- save failure: keep MainMenu active, show explicit error, do not emit `campaign_ready`.

- [ ] **Step 5: Run focused GUT tests and verify GREEN**

Also rerun `test_vs_save_service.gd` to prove backup semantics were not changed.

- [ ] **Step 6: Commit**

```bash
git add tests/gut/unit/vertical_slice/test_vs_main_menu.gd scripts/vertical_slice/ui/vs_main_menu.gd
git commit -m "feat: add save-aware vertical slice main menu"
```

---

### Task 4: Build Native MainMenu and Workshop Scenes — GREEN

**Files:**
- Create: `scenes/vertical_slice/main_menu.tscn`
- Create: `scenes/vertical_slice/vertical_slice_app.tscn`
- Create: `scenes/vertical_slice/screens/vs_workshop_screen.tscn`

**Interfaces:**
- `main_menu.tscn` root script: `VSMainMenu`.
- `vertical_slice_app.tscn` root script: `VSApp`.
- `vs_workshop_screen.tscn` is the only implemented screen destination in Task 2.

- [ ] **Step 1: Add scene-structure assertions to the Python contract**

Parse scene text and assert:

```python
self.assertIn('custom_minimum_size = Vector2(48, 48)', main_menu_text)
self.assertIn('text = "Continue"', main_menu_text)
self.assertIn('text = "New Game"', main_menu_text)
self.assertIn('text = "Settings"', main_menu_text)
```

Also assert all three scenes avoid `res://assets/`.

- [ ] **Step 2: Run Python contract and observe the intended scene RED**

Expected: FAIL until scenes exist.

- [ ] **Step 3: Build `main_menu.tscn` with engine-native containers**

Use:

```text
Control
└─ MarginContainer
   └─ VBoxContainer
      ├─ Label            (title)
      ├─ Label            (save/recovery/error status)
      ├─ Button           (Continue, min 48×48)
      ├─ Button           (New Game, min 48×48)
      ├─ Button           (Settings, min 48×48)
      ├─ ConfirmationDialog (overwrite)
      └─ PanelContainer   (inline Settings overlay, initially hidden)
```

Settings overlay contains a text label and Close button only. No persistent settings subsystem is added.

- [ ] **Step 4: Build the app shell and minimal Workshop**

`vertical_slice_app.tscn`:

```text
Control (VSApp)
└─ MarginContainer
   └─ Control (screen host)
```

`vs_workshop_screen.tscn`:

```text
Control
└─ VBoxContainer
   ├─ Label ("Workshop")
   └─ Label (explicit vertical-slice shell/status text)
```

Do not add Forge, Item Detail, Enhancement, Customer, Result, or other placeholder scenes.

- [ ] **Step 5: Run Python + GUT tests and verify GREEN**

Run focused Task 2 contracts plus all existing GUT unit vertical-slice tests.

- [ ] **Step 6: Commit**

```bash
git add scenes/vertical_slice tests/test_vertical_slice_task2_app_shell_contract.py
git commit -m "feat: add native Task 2 shell scenes"
```

---

### Task 5: Migrate Application Entry — RED then GREEN

**Files:**
- Modify: `project.godot`
- Test: `tests/test_vertical_slice_task2_app_shell_contract.py`

**Interfaces:**
- Changes only `application/run/main_scene`.

- [ ] **Step 1: Confirm the existing RED evidence still proves old entry**

Before changing the file, verify current branch still contains:

```text
run/main_scene="res://scenes/test/enhancement_test.tscn"
```

and the Task 2 Python contract fails its start-scene assertion.

- [ ] **Step 2: Change exactly one project setting**

Replace only:

```text
run/main_scene="res://scenes/test/enhancement_test.tscn"
```

with:

```text
run/main_scene="res://scenes/vertical_slice/main_menu.tscn"
```

Do not modify autoload, viewport, renderer, input, or editor plugin lists. Hera must remain disabled.

- [ ] **Step 3: Run the Python contract and verify GREEN**

Also compare `project.godot` against the pre-change version and confirm the start-scene line is the only changed setting.

- [ ] **Step 4: Commit**

```bash
git add project.godot tests/test_vertical_slice_task2_app_shell_contract.py
git commit -m "feat: route Blacksmith startup through Task 2 main menu"
```

---

### Task 6: Extend Godot Scene Smoke Coverage

**Files:**
- Modify: `.github/workflows/godot-validation.yml`

**Interfaces:**
- Reuses existing Godot 4.7.1 reusable validation workflow.

- [ ] **Step 1: Add the two Task 2 root scenes to the existing smoke list**

Preserve all historical scene smokes and add:

```yaml
            res://scenes/vertical_slice/main_menu.tscn \
            res://scenes/vertical_slice/vertical_slice_app.tscn \
```

- [ ] **Step 2: Validate workflow structure and focused Python contracts**

Run:

```bash
python -m unittest tests/test_ci_workflow_structure.py
python -m unittest tests.test_vertical_slice_task2_app_shell_contract -v
```

- [ ] **Step 3: Run Godot 4.7.1 import and scene smokes**

Run the same commands used by `.github/workflows/godot-validation.yml`:

```bash
./godot --headless --editor --path . --quit
./godot --headless --path . res://scenes/vertical_slice/main_menu.tscn --quit-after 2
./godot --headless --path . res://scenes/vertical_slice/vertical_slice_app.tscn --quit-after 2
```

Any `SCRIPT ERROR`, `Parse Error`, `Compile Error`, or `ERROR:` is blocking.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/godot-validation.yml
git commit -m "test: smoke Task 2 app shell scenes"
```

---

### Task 7: REFACTOR Without Scope Expansion

**Files:**
- Modify only Task 2 files already introduced if duplication exists.

- [ ] **Step 1: Re-run all focused tests before refactor**

Required GREEN baseline:

```text
Task 2 Python contract: PASS
GUT main-menu: PASS
GUT app-router: PASS
Task 1 save-service GUT: PASS
```

- [ ] **Step 2: Remove only duplication or clarify names**

Allowed examples:

- extract repeated status-label updates into one private `VSMainMenu` method;
- centralize route result strings as constants;
- remove duplicate scene-node lookups.

Forbidden during refactor:

- new gameplay states;
- new service/domain rules;
- new external assets;
- Hera/HiGodot authority changes;
- save initializer policy changes.

- [ ] **Step 3: Re-run focused tests after each refactor commit**

- [ ] **Step 4: Commit only if tests remain GREEN**

```bash
git commit -am "refactor: tighten Task 2 app shell boundaries"
```

Skip this commit entirely if no useful refactor is required.

---

### Task 8: Exact-Head Validation and Review Gate

**Files:**
- No new product scope.
- Update PR body/evidence and Google Sheet only after exact-head results are known.

- [ ] **Step 1: Record the exact implementation candidate HEAD**

Do not use a merge ref or an older workflow result.

- [ ] **Step 2: Require all applicable PR workflows PASS on that exact HEAD**

At minimum verify:

- PR validation
- Validate Thin Adapter Migration
- Validate Base v9 adoption
- Validate Blacksmith BCA Adoption if routed
- Validate Project Base Adapter
- Validate GUT 9.7.1 Formal Adoption

- [ ] **Step 3: Require Full validation on the exact candidate HEAD before merge readiness**

Full validation must prove:

- Windows Python 3.11 / 3.12 / 3.13 PASS
- Ubuntu Python 3.11 / 3.12 / 3.13 PASS
- Godot 4.7.1 full suite PASS
- pinned Base governance PASS

If Full validation cannot be run against the exact PR HEAD, do not claim merge readiness; create the project-approved exact-head validation path first rather than substituting a different SHA.

- [ ] **Step 4: Review the final diff boundary**

Allowed product paths:

```text
scripts/vertical_slice/ui/
scenes/vertical_slice/
project.godot
```

Allowed non-product paths:

```text
tests/test_vertical_slice_task2_app_shell_contract.py
tests/gut/unit/vertical_slice/
.github/workflows/python-validation.yml
.github/workflows/godot-validation.yml
docs/superpowers/...
```

The final diff must contain zero changes under:

```text
assets/
addons/
unrelated data/
unrelated scripts/
unrelated scenes/
```

- [ ] **Step 5: Read all PR reviews, inline threads, and comments**

Unresolved actionable feedback blocks readiness.

- [ ] **Step 6: Synchronize Decision `BS-VS-TASK2-20260807-01` to Sheet and read back**

Record exact head, RED head, GREEN/full-validation evidence, changed-file boundary, Android `NOT_RUN`, human playtest `NOT_RUN`, product image/rights gates unchanged.

- [ ] **Step 7: Keep PR Draft or unmerged until separate explicit merge approval**

Task 2 implementation completion and merge are separate approvals. Never merge automatically from this plan.

---

## Self-Review

### Spec coverage

- Separate MainMenu: covered by Tasks 3-5.
- Continue with missing/valid/recovered/unrecoverable save: Task 3.
- Safe New Game replacement: blocked by Task 0, then Task 3 consumes the approved initializer.
- Inline Settings overlay: Task 4.
- Single BlacksmithApp at WORKSHOP: Tasks 2 and 4.
- Declared versus implemented routing: Task 2.
- No placeholder gameplay scenes: Tasks 2 and 4.
- 720×1280 and 48×48: Tasks 1 and 4.
- No color-only status: Task 4 plus GUT/UI assertions added when implementing.
- No external product assets / no image-rights claim: Tasks 1 and 4.
- Actual start-scene migration: Task 5.
- GUT authority and scene smoke: Tasks 2, 3, 6, 8.
- Exact-head PR and Full validation: Task 8.
- Android/human validation remain `NOT_RUN`: Global Constraints and Task 8.
- Hera remains disabled/non-authoritative: Global Constraints, Tasks 1 and 5.

### Known intentional blocker

The plan is **not executable yet** because Task 0 has no approved initializer Decision. That is a governance dependency, not an implementation placeholder. No code should be written to guess around it.

### Type/interface consistency

- MainMenu consumes `VSSaveService.load_envelope()` exactly as implemented in Task 1 canon.
- Backup recovery uses `VSSaveEnvelope.recovered_from_backup` exactly as implemented.
- Router methods consistently use `String` state/result values and `Dictionary` payloads.
- No planned UI method owns gameplay calculations or direct save-file operations.
