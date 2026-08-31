# Blacksmith 반복 정밀강화 태그 진화 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 사용자가 확정한 규칙대로 `+9 → +10`부터 `+99 → +100`까지 모든 10단위 강화 성공에 태그 하나의 **추가 또는 강화**를 필수화한다. 하나의 `CATALYST_AFFIX` 안에서 최대 3개 태그와 각 태그의 I~IV 단계를 저장하고, 기존 +1 성공, 손상·수리, 세 affix 슬롯, 현재 Phase-1 범위 및 사람용 GDD/PDF를 일관되게 유지한다.

**Architecture:** repository-owned Decision38 및 versioned JSON catalog가 규칙의 기계 정본이 된다. `VSItem` V4는 기존 `CATALYST_AFFIX`를 versioned tag collection으로 이관하며 `used_precision_milestones`를 유일한 정밀 이정표 완료 기록으로 유지한다. `VSPrecisionResolver`는 action-local `ADD_TAG`/`UPGRADE_TAG` 선택을 검증·미리보기·성공 적용하고, `VSEnhancementResolver`/`VSEnhancementActionService`는 비용 전 차단과 저장 원자성을 보장한다. `VSWorkshopScreen`은 큰 native Control 두 단계 선택과 현재 태그 계보판만 표시한다. 사람용 GDD와 파생 PDF는 런타임 증거와 구분해 이 흐름을 설명한다.

**Tech Stack:** Godot 4.7-compatible GDScript, native Godot `Control` nodes, GUT 9.7.1, Python 3.12 document contracts, repository JSON, Poppler + PyPDF validation. PDF 발행 시 이 데스크톱의 bundled Python/runtime을 사용한다.

**Spec:** [2026-08-30-blacksmith-recurring-precision-tag-evolution-design.md](../specs/2026-08-30-blacksmith-recurring-precision-tag-evolution-design.md)

## Global Constraints

- 사용자 확정 방향은 `BS-ENHANCE-20260830-38`로 기록한다. 이전의 `+10` 단일 정밀강화, non-empty catalyst 차단, 단일 문자열 tag owner 문구는 해당 필드에서 명시적으로 `[대체됨]` 처리하고, Decision28/29/30의 확률·손상·수리 수치에는 손대지 않는다.
- Precision target은 정확히 `[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]`이며, 성공은 항상 `+1` 레벨과 정확히 하나의 tag-growth action이다. Checkpoint floors `[10, 30, 60, 90]`는 별도의 보호 규칙으로 보존한다.
- affix slot은 계속 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX` 세 개뿐이다. 신규 top-level affix, catalyst inventory, random/reroll, 기본 선택, unrelated replacement, player title을 만들지 않는다.
- `CATALYST_AFFIX` 내부 record는 최대 3개 고유 tag entry만 가진다. entry는 `tag_id`, `stage`(1~4), `created_milestone`, `last_advanced_milestone`을 보존하며, 완료 여부의 유일한 persisted owner는 `used_precision_milestones`다.
- `EDGE_REINFORCEMENT`는 `RAW_ROLE_STAT +3`, `LIGHTWEIGHTING`은 `WEIGHT_POINT -3` (minimum 0)이다. 선택한 tag의 방법 효과는 tag 추가·강화 성공 때 정확히 한 번만 적용한다. 무게가 0이면 `LIGHTWEIGHTING` 선택을 cost/roll 전에 차단한다.
- `FAILED_HOLD`, `FAILED_DAMAGE`, `BLOCKED`는 태그, stage, 효과, milestone, ledger를 전혀 변경하지 않는다. 성공 기록만 append-only ledger와 사람용 Chronicle summary의 후보가 된다.
- V3 string catalyst migration은 idempotent해야 한다. known tag는 `SEED I` + milestone 10으로, placeholder는 무료 initial-tag backfill pending으로, unknown nonempty value는 원문을 보존한 unreadable fail-closed state로 변환한다. 기존에 적용된 +3/-3은 절대 재적용하지 않는다.
- Workshop은 720×1280 portrait native controls만 사용한다. 정밀 화면의 클릭 영역은 최소 48dp이다. 2026-08-30 사용자가 메인·핵심 장면이 비어 보이지 않도록 실제 소비처가 있는 시각 자산 제작을 추가 승인했으므로, Task 6의 세 후보만 consumer-first Visual Requirement를 통과한 뒤 생성한다. 후보는 post-generation user lock 전까지 `GENERATED_CANDIDATE`이며 `assets/`·runtime·asset catalog에 승격하지 않는다. 소비처가 없는 설명용 flow-map raster, fake gameplay screenshot, 오디오, VFX, 새 scene은 계속 만들지 않는다.
- 기존 미커밋 `BLACKSMITH_HUMAN_FACING_GDD_20260828.md`, PDF, receipt, `PROJECT_AI_PRODUCTION_SPEC.md`, `.base-contract/`, `tmp/` 변경 및 PR #196은 현 작업 소유가 아니다. isolated worktree/branch에서 시작하고, user-owned 변경을 reset, stash, overwrite, commit, merge하지 않는다.
- 자동 테스트, document/PDF validation, Godot headless import, live runtime, Android, accessibility, performance, human playtest, release evidence는 서로 다른 상태다. 실제 실행하지 않은 것은 `NOT_RUN`으로만 기록한다.

---

### Task 1: Current-canon amendment and machine-readable catalog

**Files:**
- Create: `docs/decisions/BS-ENHANCE-20260830-38_RECURRING_PRECISION_TAG_EVOLUTION.md`
- Modify: `docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`
- Modify: `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- Modify: `docs/decisions/BS-ENHANCE-20260828-34_WEAPON_KEYWORD_OWNERSHIP.md`
- Modify: `docs/decisions/BS-ENHANCE-20260829-37_PRECISION_TAG_CATALOG_AND_SELECTION_GATE.md`
- Modify: `docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md`
- Modify: `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`
- Modify: `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`
- Modify: `tests/check_precision_tag_catalog_contract.py`

**Interfaces:**
- The catalog exposes `precision_targets`, `max_active_tags`, `max_tag_stage`, canonical `lineages`, `methods`, `tags`, and `compatible_tag_ids`.
- `selection_flow` accepts attempt-local dictionaries of one of these exact forms:

```gdscript
{ "action": "ADD_TAG", "lineage_id": "EMBER_LINEAGE", "method_id": "EDGE_REINFORCEMENT" }
{ "action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE" }
```

- Decision38 alone owns the recurring cadence, collection cardinality/stages, V3→V4 migration disposition, and tag-growth effect timing. Decision34/37 retain only unaffected historical evidence and explicit supersession links.

- [ ] **Step 1: Turn the Python contract into an intended failing amendment test (RED).**

Add assertions before changing the owners. Cover exact ten precision targets, max 3 active tags, stage 4, four current tags, action-local persistence, `CATALYST_AFFIX` ownership, effect boundaries, no default/random/reroll, and the three V3 migration dispositions.

```python
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
assert catalog["schema_version"] == 2
assert catalog["precision_targets"] == list(range(10, 101, 10))
assert catalog["tag_growth"]["max_active_tags"] == 3
assert catalog["tag_growth"]["max_stage"] == 4
assert catalog["selection_flow"]["actions"] == ["ADD_TAG", "UPGRADE_TAG"]
```

Run: `python tests/check_precision_tag_catalog_contract.py`

Expected: FAIL because the current decision/catalog declares only `9 → 10`, schema version 1, and one resolved string Tag.

- [ ] **Step 2: Create Decision38 and update the catalog (GREEN).**

Write the decision in Korean with a replacement table for Decision25/34/37 fields, retained Decision28/29/30 boundaries, action truth table, migration table, forbidden behavior, research `ADOPT / ADAPT / REJECT`, and evidence ceilings. Upgrade the JSON to schema 2 while retaining the approved first four tags/method effects. Its relevant shape is:

```json
{
  "schema_version": 2,
  "source_decision_id": "BS-ENHANCE-20260830-38",
  "machine_owner": "CATALYST_AFFIX",
  "precision_targets": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
  "tag_growth": { "max_active_tags": 3, "max_stage": 4 },
  "selection_flow": { "actions": ["ADD_TAG", "UPGRADE_TAG"], "persistence": "ATTEMPT_LOCAL_ONLY" }
}
```

For all existing owner documents, replace conflicting text with a link to Decision38 and `[대체됨]`; do not duplicate a competing current owner. Update the handoff only with current amendment status, not unverified runtime claims.

- [ ] **Step 3: Make the static contract GREEN and protect catalog integrity.**

Extend the contract test to reject duplicate tag IDs, invalid compatibility references, nonzero durability deltas, tag effects outside the two approved axes, a fourth affix slot, or a catalog that omits a target. Include all amended current owners in its readback list.

Run: `python tests/check_precision_tag_catalog_contract.py`

Expected: PASS only when all current owner links and catalog fields agree.

- [ ] **Step 4: Refactor ownership wording and commit only the canon slice.**

Read all changed documents back, scan for stale claims such as `only +9`, `only +10`, `one Tag`, `new stored field is forbidden`, and make each remaining hit explicitly historical or semantically correct. Commit only the files above on the isolated branch:

```powershell
git add docs/decisions/BS-ENHANCE-20260830-38_RECURRING_PRECISION_TAG_EVOLUTION.md `
  docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json `
  docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md `
  docs/decisions/BS-ENHANCE-20260828-34_WEAPON_KEYWORD_OWNERSHIP.md `
  docs/decisions/BS-ENHANCE-20260829-37_PRECISION_TAG_CATALOG_AND_SELECTION_GATE.md `
  docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md `
  docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md `
  docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md `
  tests/check_precision_tag_catalog_contract.py
git commit -m "docs: define recurring precision tag evolution"
```

### Task 2: V4 `VSItem` catalyst collection and migration boundary

**Files:**
- Modify: `scripts/vertical_slice/domain/vs_item.gd`
- Modify: `scripts/vertical_slice/domain/vs_save_envelope.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_item.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_item_v2_contract.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_save_service.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_v2_save_boundary.gd`

**Interfaces:**
- `VSItem.SCHEMA_VERSION` advances from 3 to 4. `catalyst_affix` changes from a plain `String` to the following canonical dictionary while remaining the existing affix owner:

```gdscript
{
    "schema_version": 1,
    "tag_entries": [
        {
            "tag_id": "TAG_EMBER_EDGE",
            "stage": 1,
            "created_milestone": 10,
            "last_advanced_milestone": 10,
        }
    ],
    "initial_tag_backfill_pending": false,
    "unreadable_legacy_affix": "",
}
```

- Required `VSItem` helpers use one normalized collection representation:

```gdscript
static func empty_catalyst_affix() -> Dictionary
func catalyst_tag_entries() -> Array[Dictionary]
func has_initial_tag_backfill_pending() -> bool
func has_unreadable_catalyst_affix() -> bool
func precision_milestone_is_resolved(target_level: int) -> bool
```

- `VSSaveEnvelope` remains its current envelope schema unless an envelope-level field truly changes. It must stop treating a string placeholder or the old `legacy_v3_precision_backfill_uids` side map as the source of truth; pending state resides inside the migrated `VSItem` record.

- [ ] **Step 1: Add V4 serialization and migration tests before implementation (RED).**

Cover fresh empty record round trip; a valid multi-tag V4 record; duplicate tag/stage 0/stage 5/non-precision milestone rejection; known V3 tag migration without reapplying stats; placeholder migration to pending; unknown string to a non-destructive unreadable state; and load-save-load idempotence.

```gdscript
func test_v3_known_tag_migrates_to_seed_without_reapplying_legacy_effect() -> void:
    var item = VSItem.from_dict(_v3_item("TAG_EMBER_EDGE", 10, []))
    assert_eq(item.schema_version, 4)
    assert_eq(item.catalyst_tag_entries()[0]["stage"], 1)
    assert_eq(item.used_precision_milestones, [10])
    assert_eq(item.raw_role_stat, _v3_raw_role_stat)
```

Run the focused files:

```powershell
godot --headless -d -s --path . addons/gut/gut_cmdln.gd `
  -gdir=res://tests/gut/unit/vertical_slice -ginclude_subdirs `
  -gselect=test_vs_item.gd,test_vs_item_v2_contract.gd,test_vs_save_service.gd,test_vs_v2_save_boundary.gd -gexit
```

Expected: FAIL because V3 accepts only string `catalyst_affix` and validates `[10]` as the only precision milestone.

- [ ] **Step 2: Implement the smallest self-validating V4 record (GREEN).**

Implement a V3 migration branch in `VSItem.from_dict`; normalize incoming nested arrays/dictionaries; deep-copy to `to_dict`; and validate record shape against catalog invariants. Normalize a known historic string to one `SEED` entry, append `10` only when absent, preserve old stats/ledger/Grade/Chronicle byte-for-byte, and reject unavailable catalog IDs without silently deleting their source string. Validate each creation/last-advance milestone is in `used_precision_milestones` and no tag entry appears twice.

Make `VSSaveEnvelope.from_dict` delegate item migration and delete or replace the old V3 placeholder map only after tests prove an old envelope can still open deterministically.

- [ ] **Step 3: Verify reruns and failure paths.**

Add save-service tests that a second deserialize/save causes no new stage, stat, milestone, ledger entry, or backfill. Assert malformed V4 payloads remain validation errors and never become a playable empty collection. Run the Task 2 focused GUT command until GREEN.

- [ ] **Step 4: Commit the isolated data migration task.**

```powershell
git add scripts/vertical_slice/domain/vs_item.gd scripts/vertical_slice/domain/vs_save_envelope.gd `
  tests/gut/unit/vertical_slice/test_vs_item.gd tests/gut/unit/vertical_slice/test_vs_item_v2_contract.gd `
  tests/gut/unit/vertical_slice/test_vs_save_service.gd tests/gut/unit/vertical_slice/test_vs_v2_save_boundary.gd
git commit -m "feat: migrate catalyst affix to tag collection"
```

### Task 3: Action-aware precision resolver and exact success semantics

**Files:**
- Modify: `scripts/vertical_slice/resolvers/vs_precision_resolver.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_precision_tag_catalog.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_precision_customer_context_runtime.gd`

**Interfaces:**
- `VSPrecisionResolver.selection_preview(item, target_level, selection) -> Dictionary` supports every catalog precision target.
- `apply_selection_success(item, target_level, selection) -> Dictionary` is the sole tag record/effect mutation point; it returns `tag_id`, `action`, `stage_before`, `stage_after`, `effect_axis`, `effect_delta`, `before_value`, `after_value`.
- `backfill_placeholder(item, selection)` is replaced with `backfill_initial_tag(item, selection)` and only permits the migrated pending-state `ADD_TAG` at milestone 10, with zero cost/roll.

- [ ] **Step 1: Write target/action matrix tests (RED).**

Test all 10 targets and adjacent ordinary targets, first target ADD-only, later add below cap, duplicate/add-at-cap rejections, stage I→II→III→IV upgrade, mastered rejection, zero-weight lightweight rejection, and no catalog/selection mutation during preview.

```gdscript
func test_upgrade_applies_the_resolved_method_once_and_marks_only_target_twenty() -> void:
    var item := _item_with_seed("TAG_EMBER_EDGE", 19)
    var preview := resolver.selection_preview(item, 20, {"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
    assert_true(preview["allowed"])
    var result := resolver.apply_selection_success(item, 20, {"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
    assert_eq(result["stage_before"], 1)
    assert_eq(result["stage_after"], 2)
    assert_eq(item.raw_role_stat, _raw_before + 3)
    assert_eq(item.used_precision_milestones, [10, 20])
```

Run:

```powershell
godot --headless -d -s --path . addons/gut/gut_cmdln.gd `
  -gdir=res://tests/gut/unit/vertical_slice -ginclude_subdirs `
  -gselect=test_vs_precision_tag_catalog.gd,test_vs_precision_customer_context_runtime.gd -gexit
```

Expected: FAIL because the resolver accepts only level 9/target 10 and writes a single tag string.

- [ ] **Step 2: Implement a fail-closed catalog adapter (GREEN).**

Read schema-2 catalog data, validate all tag/method/compatibility relationships, derive candidates according to the selected action, and return stable Korean display data. Validate `target_level` against `precision_targets`, current level against `target - 1`, all stored tags/cap/stages, exact action fields, available next effect, and resolved-milestone uniqueness before an effect is applied.

```gdscript
func _apply_growth(item, preview: Dictionary) -> void:
    if str(preview["action"]) == "ADD_TAG":
        item.catalyst_affix["tag_entries"].append(_seed_entry(preview))
    else:
        _advance_entry(item.catalyst_affix["tag_entries"], str(preview["tag_id"]), int(preview["stage_after"]), int(preview["target_level"]))
    _apply_method_effect_once(item, preview)
    item.used_precision_milestones.append(int(preview["target_level"]))
```

- [ ] **Step 3: Prove success-only mutation and legacy backfill safety.**

Test that blocked/malformed/repeated calls preserve the entire item snapshot, and that pending backfill transitions exactly once to a seed entry with milestone 10. Test Grade/Chronicle preservation and durable probability fields unchanged. Run the focused files until they pass.

- [ ] **Step 4: Commit the resolver task.**

```powershell
git add scripts/vertical_slice/resolvers/vs_precision_resolver.gd `
  tests/gut/unit/vertical_slice/test_vs_precision_tag_catalog.gd `
  tests/gut/unit/vertical_slice/test_vs_precision_customer_context_runtime.gd
git commit -m "feat: resolve recurring precision tag growth"
```

### Task 4: Atomic enhancement, action service, ledger, and Chronicle integration

**Files:**
- Modify: `scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd`
- Modify: `scripts/vertical_slice/services/vs_enhancement_action_service.gd`
- Modify: `scripts/vertical_slice/domain/vs_ledger_entry.gd` only if its allowed event enum/schema needs an explicit tag-growth event
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_resolver.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_action_archive.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_resolution.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_content_result_record.gd` only if the existing player Chronicle projection requires its dedicated tag-growth summary

**Interfaces:**
- `VSEnhancementResolver.preview/resolve_with_rolls(..., precision_selection)` calls precision validation for any target in the catalog’s `precision_targets`, never for ordinary targets.
- `VSEnhancementActionService._commit_enhancement_state` deep-copies `catalyst_affix` and `used_precision_milestones` from the staged item.
- A successful tag growth uses a clear decision source (`BS-ENHANCE-20260830-38`) and an append-only payload containing target, action, tag ID, stage before/after, and applied method axis/delta. It must not turn routine ordinary enhancements into Chronicle entries.

- [ ] **Step 1: Add atomic success/failure tests first (RED).**

Test level 19 without action blocks before resources/save/roll; a +20 hold and damage leave tag data untouched; +20 success applies exactly once inside the cloned candidate; and multiple candidate/save calls cannot duplicate. Preserve the exact current `+10` damage zero guarantee and Decision28 damage for target ≥11.

```gdscript
func test_precision_hold_charges_the_normal_attempt_but_writes_no_tag_growth() -> void:
    var before := envelope.get_item(item.uid).to_dict()
    var result := service.resolve_and_save_with_rolls(envelope, item.uid, 20, _hold_rolls(), 1, resources, save, _upgrade_edge())
    assert_eq(result["outcome"], "FAILED_HOLD")
    assert_eq(save.saved_envelope.get_item(item.uid).catalyst_affix, before["catalyst_affix"])
    assert_eq(save.saved_envelope.get_item(item.uid).used_precision_milestones, before["used_precision_milestones"])
```

Run:

```powershell
godot --headless -d -s --path . addons/gut/gut_cmdln.gd `
  -gdir=res://tests/gut/unit/vertical_slice -ginclude_subdirs `
  -gselect=test_vs_enhancement_resolver.gd,test_vs_enhancement_action_archive.gd,test_vs_enhancement_resolution.gd -gexit
```

Expected: FAIL because the resolver invokes precision only for target 10 and the action service string-casts `catalyst_affix`.

- [ ] **Step 2: Generalize only the precision hook and keep core probability math unchanged (GREEN).**

Replace `if target_level == 10` hooks with catalog-target membership. Call `apply_selection_success(staged_item, target_level, selection)` only after success rolls. Keep `_apply_success` responsible for one level/checkpoint update and do not modify damage anchors, durability modifiers, price calculation, hard guarantee, or repair fields. Deep-copy nested catalyst data/milestones in `_commit_enhancement_state`.

- [ ] **Step 3: Make the success event traceable but bounded.**

Use existing ledger sequencing and current Chronicle projection conventions. Add a precise event only when the tag collection changed successfully, never for hold/damage/blocked/clicks. Validate the payload through save/reload and check known old ledger entries remain valid.

- [ ] **Step 4: Update free initial backfill atomically.**

Replace the old source-envelope boolean with migrated item pending state; enforce `ADD_TAG` and target 10; save no resources/roll; clear pending only after candidate save succeeds. Unknown migrated values and known resolved tags must remain fail closed.

- [ ] **Step 5: Run the focused GUT suite and commit.**

```powershell
git add scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd `
  scripts/vertical_slice/services/vs_enhancement_action_service.gd `
  scripts/vertical_slice/domain/vs_ledger_entry.gd `
  tests/gut/unit/vertical_slice/test_vs_enhancement_resolver.gd `
  tests/gut/unit/vertical_slice/test_vs_enhancement_action_archive.gd `
  tests/gut/unit/vertical_slice/test_vs_enhancement_resolution.gd `
  tests/gut/unit/vertical_slice/test_vs_content_result_record.gd
git commit -m "feat: commit precision tag growth atomically"
```

If the ledger/Chronicle files require no code change, omit them from the commit rather than creating a non-functional abstraction.

### Task 5: Workshop tag-growth UI and input flow

**Files:**
- Modify: `scripts/vertical_slice/ui/vs_workshop_screen.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_app.gd`

**Interfaces:**
- `VSWorkshopScreen.set_precision_selection(selection: Dictionary) -> void` replaces the two-string helper; a compatibility wrapper may remain temporarily inside test code only if all production callers use the action-aware shape.
- `view_state()` exposes `precision_target`, `precision_mode`, `precision_tag_entries`, `precision_action`, `precision_candidates`, `precision_preview_summary`, and `enhancement_allowed`.
- UI node family is native and explicit: `PrecisionActionAddButton`, `PrecisionActionUpgradeButton`, `PrecisionTagOption`, `PrecisionLineageOption`, `PrecisionMethodOption`, `PrecisionPreviewLabel`, and `PrecisionBackfillButton` only for migrated pending state.

- [ ] **Step 1: Write failing UI state/interaction tests (RED).**

Test that +9 requires ADD and two tag source choices; level 19 offers large ADD/UPGRADE actions and only valid candidates; a level with three tags hides/disables ADD; a stage IV tag cannot be selected for upgrade; zero-weight candidates are absent; ordinary target controls remain hidden; and all action buttons are at least 48dp tall.

```gdscript
func test_plus_nineteen_shows_existing_tag_stages_then_requires_one_growth_action() -> void:
    var screen := _configured_precision_screen(19, _seed_edge_collection())
    assert_true(screen.view_state()["precision_visible"])
    assert_true(screen.get_node("WorkshopLayout/PrecisionActionAddButton").visible)
    assert_true(screen.get_node("WorkshopLayout/PrecisionActionUpgradeButton").visible)
    assert_true(screen.get_node("WorkshopLayout/EnhancementButton").disabled)
    screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
    assert_false(screen.get_node("WorkshopLayout/EnhancementButton").disabled)
```

Run:

```powershell
godot --headless -d -s --path . addons/gut/gut_cmdln.gd `
  -gdir=res://tests/gut/unit/vertical_slice -ginclude_subdirs `
  -gselect=test_vs_workshop_screen.gd,test_vs_app.gd -gexit
```

Expected: FAIL because the present screen is fixed to a lineage/method pair at `+9 → +10` and identifies a string placeholder.

- [ ] **Step 2: Implement the minimal two-step native UI (GREEN).**

Do not edit `.tscn` or add raster assets. Extend the dynamically created native controls to display a readable tag line (name, lineage, I~IV, next effect) and large ADD/UPGRADE action buttons. After ADD, populate only compatible unseen tags through lineage/method controls; after UPGRADE, populate active I~III tags. Use action-local selection only, render preview from the resolver, pass it into normal enhancement request, and clear it after every completed attempt or backfill.

- [ ] **Step 3: Add visual/integration guardrails.**

Verify Korean labels avoid implementation identifiers; state contains the exact target such as `+19 → +20`; selection omission disables confirm; save failure does not visually adopt the staged collection; and old free pending backfill remains a distinct zero-cost action.

- [ ] **Step 4: Run focused UI tests and commit.**

```powershell
git add scripts/vertical_slice/ui/vs_workshop_screen.gd `
  tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd `
  tests/gut/unit/vertical_slice/test_vs_app.gd
git commit -m "feat: show recurring precision tag choices"
```

### Task 6: Consumer-first scene art requirements, candidate generation, and lock gate

**Files:**
- Create: `docs/planning/BLACKSMITH_RECURRING_PRECISION_VISUAL_REQUIREMENTS_20260830.json`
- Modify: `docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json`
- Modify: `docs/planning/PROJECT_CORE_SCENE_VISUAL_BOARD_20260828.md`
- Create: `tests/check_recurring_precision_visual_requirements_contract.py`
- Candidate-only output outside `assets/`: `artifacts/visual_candidates/20260830/` (only if the image tool provides a local candidate file; no generated fallback artwork)

**Interfaces:**
- `VIS-REC-20260830-01` is a `941x1672` portrait `SCREEN_BACKGROUND` candidate for the existing `MAIN_MENU` slot `res://scenes/vertical_slice/main_menu.tscn#MenuIllustratedBackground`; its post-lock binding owner is `VSMainMenu.MainMenuBackgroundTexture` and its fallback is the already approved `ASSET-WORKSHOP-BACKGROUND-V2`.
- `VIS-REC-20260830-02` is a `941x1672` portrait `SCREEN_BACKGROUND` candidate for the exact recurring precision state inside `res://scripts/vertical_slice/ui/vs_workshop_screen.gd`; its post-lock binding owner is a precision-only `TextureRect` layer created by the Task 5 screen owner. Its fallback is the current `ASSET-WORKSHOP-BACKGROUND-V2`. It is a background only: tag names, stages, controls, odds, and all other decision text stay in native Godot controls.
- `VIS-REC-20260830-03` is a `941x1672` portrait `EVENT_ILLUSTRATION` candidate for `res://scenes/vertical_slice/screens/vs_customer_result_screen.tscn`; its post-lock binding owner is `VSCustomerResultScreen` using a dynamic background layer. Its fallback is the existing ColorRect/Label result surface.
- Every requirement records all Decision04 mandatory fields: `consumer_id`, `consumer_surface`, `runtime_asset_role`, `primary_use`, `implementation_owner_or_path`, `target_aspect_resolution`, `state_family_requirement`, and `fallback_if_unconsumed`, as well as candidate status, prompt version, rights/provenance placeholder, and post-lock promotion steps. A candidate stays `GENERATED_CANDIDATE`/`REVIEWED` until the user locks it; an unlocked candidate must never be called a project/runtime asset.
- The human flow map remains text-native Mermaid/table content that links the three real scene consumers. It is not a generated raster asset.

- [ ] **Step 1: Establish the failing consumer-requirement contract (RED).**

Add a focused Python contract test requiring exactly the three records above, complete consumer metadata, `941x1672` portrait constraints, `GENERATED_CANDIDATE` lifecycle handling, explicit existing fallbacks, and the prohibition on standalone flow-map/fake-screen generation. It must also reject an asset catalog/runtime-consumption claim before `USER_LOCKED` status.

Run: `python tests/check_recurring_precision_visual_requirements_contract.py`

Expected: FAIL because no current requirement record ties the requested main, recurring precision, and customer-result art to actual runtime slots.

- [ ] **Step 2: Record the requirements and revise the current scene-flow board (GREEN).**

Write the three requirements with the exact runtime locators verified from current source. Update visual coverage to show a user-approved **candidate-production scope** without overwriting the prior approved assets or treating candidates as canonical. Amend the visual board from stale `+10`-only wording to all ten Precision gates and make its flow map a compact, human-readable path through Main Menu → First Forge → Workshop / every ten-level Tag decision → Customer Result / Repair. It must identify illustration layers separately from native UI controls.

- [ ] **Step 3: Generate and inspect the three constrained candidate illustrations.**

Use the image-generation model rather than procedural drawing, SVG, Canvas, Godot primitives, or generated UI screenshots. Every prompt must preserve `ILLUSTRATED_WORKSHOP_BOOK`: warm handmade workshop-book ink and watercolor/paper materials; no dark-forge gold/black direction; no logo, readable text, UI controls, watermarks, people/characters whose identity would invent content, or in-image probability/gameplay claims. Compose a quiet upper/middle readability field for native controls and an art focal point away from the primary text stack:

1. **Main Menu** — a dawn-lit blacksmith workshop entrance, forge, worn bench, and a single unfinished workpiece silhouette; invitation and ownership, not a menu screenshot.
2. **Recurring Precision** — close portrait workshop workbench with an anvil, tag-shaped metal blanks/etched tokens, restrained ember and anvil motifs, and an intentionally clear central decision field; recurrence is implied by multiple stages of craft material, not text or repeated UI.
3. **Customer Result** — workshop threshold / return table with a travelled same-workpiece silhouette, folded use report and subtle road/weather traces; reflective consequence without depicting an identified customer, combat, or forced damage.

Inspect each candidate against its requirement, aspect/crop safety, no-text/no-fake-UI rule, art-direction consistency, and native-control readability. Place a local copy in the candidate-only location only when available; otherwise preserve the image tool reference in the requirement record. Show each candidate to the user for post-generation direction lock. Do not promote, bind, or hash a final `assets/` file in this step.

- [ ] **Step 4: Stop only the promotion path at the post-generation user lock.**

Continue non-asset runtime/document work while the user considers the candidates, but keep asset status `PENDING_USER_LOCK`. On a clear lock, create a narrowly scoped follow-up implementation slice: copy only locked files into `assets/ui/workshop/`, record SHA-256/provenance/approved runtime consumer in the existing coverage/rights owner, bind the Main Menu and Customer Result dynamic layers, add the precision-only layer without serializing a scene, write RED/GREEN GUT coverage for each binding and fallback, and complete Godot runtime verification if an approved live-editor session is available. On a rejection, retain no generated candidate as a runtime/GDD substitute; `REBRIEF` or `CUT` it.

- [ ] **Step 5: Commit the requirements/candidate-evidence slice only.**

Stage requirements, board, coverage record, and contract test. Do not stage a candidate binary, `assets/` file, scene, or runtime binding before a clear post-generation user lock.

### Task 7: Human-facing GDD, technical trace, and reproducible Blueprint PDF

**Files:**
- Modify: `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md`
- Modify: `docs/design/PROJECT_AI_PRODUCTION_SPEC.md`
- Modify: `tests/check_human_facing_gdd_and_review_loop_contract.py`
- Modify: `exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf`
- Modify: `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json`
- Create: `tools/publish_human_facing_gdd_pdf.py`

**Interfaces:**
- Human GDD conveys the player journey, all ten precision gates, `ADD_TAG`/`UPGRADE_TAG`, three-tag/I~IV board, success/hold/damage/recovery branches, and Phase-1 evidence ceiling in Korean without exposing code/test or internal issue jargon as player-facing content.
- Technical trace links current Decision38, catalog schema 2, V4 migration, runtime consumers, exact test evidence, and unrun evidence ceilings.
- PDF receipt hashes normalized-LF Markdown and exact PDF bytes, includes readable page count/A4 metadata/render inspection, and never claims runtime/player evidence.

- [ ] **Step 1: Add intended failing human-document/PDF contract tests (RED).**

Replace stale Decision37-only runtime claims with requirements for Korean player-facing terms: `정밀 강화`, `태그 추가`, `태그 강화`, `최대 세 개`, `씨앗/성장/진화/완성`, `+9 → +10`, `+19 → +20`, and failure/recovery explanation. Assert the PDF text contains the same conceptual content, its receipt SHA-256 matches both artifacts, and no existing user-owned accidental diff becomes test evidence.

Run: `python tests/check_human_facing_gdd_and_review_loop_contract.py`

Expected: FAIL because the current GDD/PDF describe only the first +10 tag selection.

- [ ] **Step 2: Revise the two source documents using the confirmed Blueprint structure.**

Keep the supplied PDF as layout-density reference only; do not copy its dark visual styling or treat it as project content. Expand the Korean GDD with a compact tag growth board, ten-gate journey/flow table, Workshop screen contract, save/recovery behavior, scope map, and an evidence table. Use Markdown tables and a text-native Mermaid flow only where it improves reading; do not manufacture explanatory raster images. Update the technical trace with the machine owner and migration/consumer map.


- [ ] **Step 3: Produce and inspect the replacement PDF and receipt (GREEN).**

No project publisher currently exists, so create the smallest deterministic ReportLab publisher at `tools/publish_human_facing_gdd_pdf.py`. It reads the human GDD Markdown, lays out the approved Korean title/sections/tables/flow in A4 using the locally available Malgun Gothic font (`C:\Windows\Fonts\malgun.ttf`), sets the `Human-facing Korean GDD` PDF subject, writes `exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf`, and emits the normalized-LF source hash/PDF hash/page count receipt. Render the revised GDD, inspect text/metadata with `pypdf`, render all pages with Poppler, visually inspect every rendered page, then write exact normalized source/PDF SHA-256 and page count to the receipt.

```powershell
& 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools/publish_human_facing_gdd_pdf.py
python tests/check_human_facing_gdd_and_review_loop_contract.py
```

Expected: PASS only after source, PDF, receipt, textual content, metadata, and readable layout agree.

- [ ] **Step 4: Commit the documentation/PDF delivery slice.**

Stage only files generated from this worktree’s revised source; do not stage pre-existing user edits that collide with them. If the current main worktree contains overlapping user changes, resolve by rebuilding the same approved content in the isolated worktree rather than copying over them.

```powershell
git add docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md `
  docs/design/PROJECT_AI_PRODUCTION_SPEC.md `
  tools/publish_human_facing_gdd_pdf.py `
  tests/check_human_facing_gdd_and_review_loop_contract.py `
  exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf `
  docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json
git commit -m "docs: publish recurring precision game blueprint"
```

### Task 8: Full regression, adversarial review, runtime evidence, and safe delivery

**Files:**
- Modify only verified evidence/status fields when the exact observed result requires it: `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`
- Do not modify: `data/`, `scenes/`, `addons/`, `project.godot`. `assets/` and the three verified dynamic binding scripts may change only in the separate Task 6 post-generation user-lock follow-up described above; without that lock, their state remains untouched.

**Interfaces:**
- Consumes the exact implementation head and repository current owners.
- Produces machine verification evidence and a precise `NOT_RUN` statement for all checks not actually run.

- [ ] **Step 1: Execute full static and GUT regression at the implementation head.**

```powershell
python tests/check_precision_tag_catalog_contract.py
python tests/check_phase1_unified_implementation_contract.py
python tests/check_core_simplification_current_contract.py
python tests/check_human_facing_gdd_and_review_loop_contract.py
python -m unittest tests/test_gut_formal_adoption_contract.py -v
python -m unittest tests/test_higodot_gut_authority_gate.py -v
godot --headless --editor --path . --quit
godot --headless -d -s --path . addons/gut/gut_cmdln.gd `
  -gdir=res://tests/gut/unit -gdir=res://tests/gut/integration `
  -ginclude_subdirs -gexit -gjunit_xml_file=res://artifacts/gut/recurring-precision-tag-junit.xml
python tools/validate_gut_junit.py artifacts/gut/recurring-precision-tag-junit.xml --minimum-tests 1
```

Record actual counts and failures; never reuse the old 180-test count.

- [ ] **Step 2: Run the adversarial acceptance matrix.**

Verify from exact code/tests: every 10 target gates pre-cost; ordinary targets do not; each add/upgrade has exactly one effect; capacity/duplicate/mastered/zero-weight all block pre-roll; failed hold/damage cannot mutate collection; V3 migration is idempotent/fail-closed; `+10` remains no-damage; target ≥11 still uses current exact damage curve; Grade/Chronicle/durability/repair/checkpoints are preserved; all UI actions are 48dp+ native controls; PDF/GDD evidence does not claim runtime validation.

- [ ] **Step 3: Collect runtime evidence only if a current live editor is available.**

Use the project-authoritative live-editor process and inspect a level-9 ADD plus a prepared level-19 UPGRADE flow without mutating unrelated scenes/resources. If unavailable, do not substitute screenshots, fake mockups, or static tests; record `RUNTIME_VERIFIED = NOT_RUN`, along with Android/accessibility/performance/human-play `NOT_RUN`.

- [ ] **Step 4: Audit scope and delivery.**

Confirm expected `HEAD`, `git diff --check`, protected-path status, source/PDF receipt hashes, and no user-owned main-worktree diff is staged. Push only the task branch, create/update a narrow PR against `main`, wait for exact-HEAD required checks, and merge only through the normal green path. Do not touch PR #196. After merge, read back `origin/main` SHA and current owner files; update handoff with only verified merge/validation evidence.

```powershell
git diff --check
git status --short
git diff --name-only origin/main...HEAD
git push -u origin codex/recurring-precision-tag-evolution-20260830
```

## Plan self-review

- **Spec coverage:** Tasks 1–2 establish the new current owners and lossless data boundary; Tasks 3–4 cover all ten targets, action rules, single application, failures, saving, and traceability; Task 5 covers the Android-oriented Workshop consumer; Task 6 fills the user-identified visual gap with three consumer-first art candidates and a no-raster flow map; Task 7 makes the requested human Blueprint GDD/PDF match the new system and visual evidence status; Task 8 separates machine/runtime/human evidence and delivery.
- **Dependency order:** current canon/canonical catalog → V4 migration → resolver → atomic action service → UI → visual requirements/candidates → human GDD/PDF → exact-head validation. A candidate is deliberately not a runtime dependency until a user lock authorizes its narrow promotion slice.
- **Placeholder scan:** No implementation behavior is left as TODO/TBD. Runtime/Android/accessibility/performance/human-play are deliberately evidence states and remain `NOT_RUN` until an actual corresponding verification is run.
- **Type consistency:** Every runtime task consumes the same action dictionary (`ADD_TAG` with `lineage_id`/`method_id`; `UPGRADE_TAG` with `tag_id`), stores stages as 1–4, and treats `used_precision_milestones` as the only completion list. `CATALYST_AFFIX` is a `Dictionary` at V4 and must always be deep-copied at save/action boundaries.
- **Scope safety:** This plan changes GDScript/docs/tests/PDF and, after the existing post-generation user lock, at most three actual-consumer PNGs plus their dynamic script bindings. It deliberately avoids scene serialization, project settings, external services, pricing/risk/durability economy, fake UI screenshot assets, standalone explanatory flow-map rasters, and legacy user files.
