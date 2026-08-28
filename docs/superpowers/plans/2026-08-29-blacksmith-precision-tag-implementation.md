# Blacksmith Precision Tag Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement GitHub Issue #326: the approved `+9 → +10` 2×2 catalyst-lineage and precision-method Tag selection in the current Vertical Slice.

**Architecture:** `VSPrecisionResolver` becomes the sole runtime adapter for the repository-owned Decision37 JSON catalog. `VSEnhancementResolver` validates a transient selection at target `10` and applies it only on success. `VSEnhancementActionService` validates before resources are staged and owns atomic saved backfill; `VSWorkshopScreen` owns transient `OptionButton` state and Korean preview/copy.

**Tech Stack:** Godot 4.7-compatible GDScript, native `Control`/`OptionButton`, GUT 9.7.1, Python contract checks.

**Spec:** `docs/decisions/BS-ENHANCE-20260829-37_PRECISION_TAG_CATALOG_AND_SELECTION_GATE.md`, `docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`, `docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md`, GitHub Issue #326.

## Global Constraints

- `+9 → +10` is the only Precision Enhancement; target `<= 10` must never yield `FAILED_DAMAGE`.
- Only the existing weapon-owned `CATALYST_AFFIX` stores the resolved Tag. No schema field, fourth affix, player title, catalyst inventory, default lineage, random Tag, or reroll may be added.
- The first catalog is exactly `EMBER_LINEAGE` / `ANVIL_LINEAGE` × `EDGE_REINFORCEMENT` / `LIGHTWEIGHTING`.
- `EDGE_REINFORCEMENT` changes `raw_role_stat` by `+3`; `LIGHTWEIGHTING` changes `weight_point` by `-3`, minimum `0`; catalog durability delta is `0`.
- Grade and Event affixes remain byte-for-byte unchanged. No function/artistry/environmental/customer-universal effect is allowed.
- Selection is attempt-local: a missing/invalid pair blocks before cost/material/roll; `FAILED_HOLD` persists no choice, Tag, or method effect.
- A `PRECISION_KEYWORD_PENDING_CONTENT` V3 `+10+` item gets one no-cost/no-roll backfill with a valid pair; known Tag or unknown nonempty affix fails closed.
- UI is Korean, 720×1280 portrait `Control` layout, native controls only, and no new raster/audio/VFX asset.
- Human play, Android, accessibility, and release evidence remain `DEFERRED_BY_USER / NOT_RUN` unless actually run.

---

### Task 1: Runtime catalog adapter and selection invariants — IN PROGRESS

**Files:**
- Modify: `scripts/vertical_slice/resolvers/vs_precision_resolver.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_precision_customer_context_runtime.gd`
- Create: `tests/gut/unit/vertical_slice/test_vs_precision_tag_catalog.gd`

**Interfaces:**
- Consumes: `res://docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`, `VSItem`.
- Produces: `VSPrecisionResolver.selection_preview(item, target_level, selection) -> Dictionary`; `apply_selection_success(item, selection) -> Dictionary`; `backfill_placeholder(item, selection) -> Dictionary`.
- `selection` is only `{ "lineage_id": String, "method_id": String }`; it is never written to `VSItem`.

- [ ] **Step 1: Write failing catalog tests**

```gdscript
func test_catalog_resolves_each_approved_pair_and_blocks_missing_input() -> void:
    var resolver = PrecisionResolverScript.new()
    var missing = resolver.selection_preview(_item(9), 10, {})
    assert_false(bool(missing.get("allowed", true)))
    assert_eq(missing.get("reason", ""), "MISSING_CATALYST_LINEAGE")
    var valid = resolver.selection_preview(_item(9), 10, {
        "lineage_id": "EMBER_LINEAGE", "method_id": "EDGE_REINFORCEMENT"
    })
    assert_true(bool(valid.get("allowed", false)))
    assert_eq(valid.get("tag_id", ""), "TAG_EMBER_EDGE")
    assert_eq(valid.get("method_delta", 0), 3)
```

- [ ] **Step 2: Run the focused GUT file and observe RED**

Run: `godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -ginclude_subdirs -gselect=test_vs_precision_tag_catalog.gd -gexit`

Expected: FAIL because Decision37 catalog functions do not exist and the legacy resolver permits obsolete methods.

- [ ] **Step 3: Implement the catalog adapter minimally**

```gdscript
func selection_preview(item, target_level: int, selection: Dictionary) -> Dictionary:
    if str(selection.get("lineage_id", "")).is_empty():
        return _blocked("MISSING_CATALYST_LINEAGE")
    if str(selection.get("method_id", "")).is_empty():
        return _blocked("MISSING_PRECISION_METHOD")
    # Read the current JSON, resolve its exact 2×2 Tag, and expose before/after values.
```

Remove obsolete `ARTISTIC_FINISH`, environmental/function, customer-context, weighting, and post-`+10` Precision behavior from this current Vertical Slice resolver. Preserve no behavior from it as a fallback.

- [ ] **Step 4: Add success/backfill boundary tests and make them GREEN**

```gdscript
func test_success_and_backfill_apply_one_tag_and_one_delta_once() -> void:
    var item = _item(9)
    item.grade_affix = "GRADE_KEEP"
    item.chronicle_affix = "EVENT_KEEP"
    var result = resolver.apply_selection_success(item, _ember_edge())
    assert_eq(item.catalyst_affix, "TAG_EMBER_EDGE")
    assert_eq(item.raw_role_stat, _raw_before + 3)
    assert_eq(item.grade_affix, "GRADE_KEEP")
    assert_eq(item.chronicle_affix, "EVENT_KEEP")
```

Run the Task 1 focused GUT command until it passes.

- [ ] **Step 5: Commit the isolated catalog adapter task**

```bash
git add scripts/vertical_slice/resolvers/vs_precision_resolver.gd \
  tests/gut/unit/vertical_slice/test_vs_precision_customer_context_runtime.gd \
  tests/gut/unit/vertical_slice/test_vs_precision_tag_catalog.gd
git commit -m "feat: add precision tag catalog resolver"
```

### Task 2: Atomic enhancement and save boundary

**Files:**
- Modify: `scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd`
- Modify: `scripts/vertical_slice/services/vs_enhancement_action_service.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_resolver.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_action_archive.gd`

**Interfaces:**
- Consumes: the Task 1 selection interface.
- Produces: optional `selection: Dictionary = {}` parameter on preview/resolve/save APIs and `backfill_precision_tag_and_save(...) -> Dictionary`.
- Existing callers targeting levels other than `10` remain valid without a selection argument.

- [ ] **Step 1: Write failing atomicity tests**

```gdscript
func test_target_ten_missing_selection_blocks_before_resource_or_roll() -> void:
    var before_resources = resources.snapshot()
    var result = service.resolve_and_save_with_rolls(envelope, item.uid, 10, {}, _rolls(), 1, resources, save)
    assert_eq(result.get("outcome", ""), "BLOCKED")
    assert_eq(result.get("reason", ""), "MISSING_CATALYST_LINEAGE")
    assert_eq(resources.snapshot(), before_resources)
    assert_null(save.saved_envelope)
```

- [ ] **Step 2: Run focused resolver/action GUT files and observe RED**

Run: `godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -ginclude_subdirs -gselect=test_vs_enhancement_resolver.gd,test_vs_enhancement_action_archive.gd -gexit`

Expected: FAIL because target ten presently writes `PRECISION_KEYWORD_PENDING_CONTENT` and resource staging has no selection gate.

- [ ] **Step 3: Gate before resources and apply only on successful target ten**

```gdscript
var preview := EnhancementResolverScript.new().preview(source_item, target_level, selection)
if not bool(preview.get("allowed", false)):
    return _blocked(str(preview.get("reason", "INVALID_ATTEMPT")))
# Only after that line may resource validation/staging begin.
```

On a hold, preserve no choice or method change. On a target-ten success, call Task 1's `apply_selection_success` inside the cloned candidate item; commit `raw_role_stat`, `weight_point`, `catalyst_affix`, and existing fields atomically. Remove the placeholder write from `_apply_success`.

- [ ] **Step 4: Implement and test saved placeholder backfill**

```gdscript
var result = service.backfill_precision_tag_and_save(envelope, item_uid, selection, save_service)
assert_eq(result.get("status", ""), "APPLIED")
assert_eq(result.get("gold_cost", -1), 0)
assert_eq(result.get("reinforcement_units", -1), 0)
```

Verify a known Tag and unknown nonempty affix both fail closed without save or mutation; verify a second call cannot double-apply.

- [ ] **Step 5: Run focused GUT files until GREEN and commit**

```bash
git add scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd \
  scripts/vertical_slice/services/vs_enhancement_action_service.gd \
  tests/gut/unit/vertical_slice/test_vs_enhancement_resolver.gd \
  tests/gut/unit/vertical_slice/test_vs_enhancement_action_archive.gd
git commit -m "feat: apply precision tag selections atomically"
```

### Task 3: Workshop selection, preview, and backfill UI

**Files:**
- Modify: `scripts/vertical_slice/ui/vs_workshop_screen.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_app.gd`

**Interfaces:**
- Consumes: Task 1 catalog preview, Task 2 optional selection/save/backfill APIs.
- Produces: `set_precision_selection(lineage_id, method_id) -> void`, `request_precision_backfill() -> Dictionary`, and `view_state()` keys for selected Tag, stat before/after, `내구도 변화 없음`, and block reason.

- [ ] **Step 1: Write failing UI tests**

```gdscript
func test_plus_nine_requires_two_visible_precision_choices_before_button_enables() -> void:
    var screen = _configured_level_nine_screen()
    assert_true(screen.has_node("WorkshopLayout/PrecisionLineageOption"))
    assert_true(screen.has_node("WorkshopLayout/PrecisionMethodOption"))
    assert_true(screen.get_node("WorkshopLayout/EnhancementButton").disabled)
    screen.set_precision_selection("EMBER_LINEAGE", "LIGHTWEIGHTING")
    assert_false(screen.get_node("WorkshopLayout/EnhancementButton").disabled)
    assert_true(screen.get_node("WorkshopLayout/PrecisionPreviewLabel").text.contains("불씨의 가벼움"))
```

- [ ] **Step 2: Run focused UI GUT files and observe RED**

Run: `godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -ginclude_subdirs -gselect=test_vs_workshop_screen.gd,test_vs_app.gd -gexit`

Expected: FAIL because current Workshop has no lineage/method controls and does not forward selection data.

- [ ] **Step 3: Add native Korean controls dynamically, without a scene or asset change**

```gdscript
var lineage := OptionButton.new()
lineage.name = "PrecisionLineageOption"
lineage.add_item("촉매 계보를 고르세요")
lineage.add_item("불씨 계보")
lineage.set_item_metadata(1, "EMBER_LINEAGE")
# Mirror for 모루 계보 and the two methods, then connect item_selected.
```

Show the selector only for level `9 → 10` and placeholder-backfill state. It must show selection result Tag, allowed stat before/after, `내구도 변화 없음`, ordinary outcome/cost preview, and Korean block reasons. Do not add a new image, full-frame mockup, or persisted UI state.

- [ ] **Step 4: Connect execute and backfill actions and make tests GREEN**

Forward `_precision_selection()` into `request_enhancement_with_rolls`; clear the transient options after a hold and after success. For placeholder state, display `정밀 태그 정정` and call the no-cost action, then refresh only after saved candidate adoption.

- [ ] **Step 5: Commit the UI task**

```bash
git add scripts/vertical_slice/ui/vs_workshop_screen.gd \
  tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd \
  tests/gut/unit/vertical_slice/test_vs_app.gd
git commit -m "feat: show precision tag selection in workshop"
```

### Task 4: Regression gates, runtime evidence, and delivery

**Files:**
- Modify: `tests/check_precision_tag_catalog_contract.py` only if an implementation invariant needs a new static guard.
- Modify: `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md` only with verified implementation evidence and explicit `NOT_RUN` ceilings.

**Interfaces:**
- Consumes: completed Tasks 1–3.
- Produces: exact-head automated evidence; no claim of human-play, Android, accessibility, performance, or release verification.

- [ ] **Step 1: Run complete local verification**

```bash
godot --headless --editor --path . --quit
godot --headless -d -s --path "$PWD" addons/gut/gut_cmdln.gd \
  -gdir=res://tests/gut/unit -gdir=res://tests/gut/integration \
  -ginclude_subdirs -gexit -gjunit_xml_file=res://artifacts/gut/precision-tag-junit.xml
python tests/check_precision_tag_catalog_contract.py
python tests/check_phase1_unified_implementation_contract.py
python tests/check_core_simplification_current_contract.py
```

- [ ] **Step 2: Use the live editor only if available and collect runtime evidence**

Run `hera status`; if an editor is available, use `hera guidance ui`, then inspect the Workshop’s controls and a level-nine selection attempt. If no live editor is available, record runtime UI as `NOT_RUN`; do not infer its state.

- [ ] **Step 3: Perform adversarial review**

Confirm all of the following against exact code/tests: missing inputs cannot charge; hold cannot tag; success cannot double-apply; placeholder cannot re-roll/charge; Grade/Event never mutate; `+10` cannot damage; no obsolete method can be selected; new UI is native and Korean; no protected scope expands.

- [ ] **Step 4: Commit verified evidence and deliver through GitHub**

```bash
git add <only-verified-evidence-files>
git commit -m "test: verify precision tag vertical slice"
git push -u origin codex/precision-tag-implementation-20260829
gh pr create --base main --title "feat: implement precision tag catalog selection" --body-file <prepared-body>
```

Wait for exact-head required checks, squash merge only after green, read `origin/main` back, and keep PR #196 read-only.

## Plan self-review

- **Spec coverage:** Tasks 1–3 cover catalog ownership, explicit selection, atomic success/hold, backfill, UI presentation, and forbidden effects. Task 4 covers exact-head, runtime evidence ceiling, and delivery.
- **Placeholder scan:** No TBD/TODO or deferred implementation step remains; intentionally unrun evidence is labelled `NOT_RUN` rather than treated as a future requirement.
- **Type consistency:** All cross-task values use the same `selection` dictionary keys (`lineage_id`, `method_id`) and same known Tag IDs. The action service owns saves; the Workshop never mutates persisted selection state directly.
