# Function Recipes, Material Fit, Forging, and Playtest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Approve and synchronize `BS-ITEM-20260806-06` as `R2_BATCH_005_10_OF_10`, defining primary-material role fit, direct-forging role results, initial/rework function recipes, and the human playtest gate without changing product files.

**Architecture:** GitHub remains the authority. A focused contract test first records the missing 10/10 Decision as RED; a planning-only canon and registry synchronization then make it GREEN. Google Sheet tab `42_능력치_강화_참조표` receives four new reference sections and the standard project summary surfaces receive the same Decision ID and final exact head.

**Tech Stack:** Markdown canon/spec/plan, compact JSON registries, Python `unittest`, GitHub Actions, Google Sheets API.

## Global Constraints

- Decision ID: `BS-ITEM-20260806-06`.
- Active state after synchronization: `R2_BATCH_005_ACTIVE_10_OF_10` and counter `10/10`.
- Product implementation remains `BLOCKED`.
- Exact values remain `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`.
- Do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.
- Specifically preserve `data/crafting/materials.json`, `weapon_bases.json`, `forging_balance.json`, and `craftsmanship_grades.json` byte-for-byte.
- PR #109 remains open, Draft, and unmerged.
- GitHub canon and Google Sheet mirror must carry the same Decision ID and exact final head.

---

### Task 1: Record the RED contract

**Files:**
- Create: `tests/test_r2_function_recipe_material_fit_and_playtest.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: current compact `CURRENT_R2_CANON_REGISTRY.json` at 9/10.
- Produces: failing assertions for the exact 10/10 contract and planning documents.

- [ ] **Step 1: Write the focused contract test**

The test must assert:

```python
self.assertEqual("R2_BATCH_005_ACTIVE_10_OF_10", registry["stage_status"])
self.assertEqual("10/10", registry["next_approval_counter"])
self.assertEqual(10, registry["active_batch"]["approved_decisions"])
self.assertIn("BS-ITEM-20260806-06", decisions)
```

It must also assert the exact material matrix, role strike mapping, six initial recipes, rework catalyst-tag contract, current fire-only rework availability, 48-case solo plan, 3–5 person external plan, and protection flags.

- [ ] **Step 2: Add the test module to Planning-first CI**

Append:

```yaml
tests.test_r2_function_recipe_material_fit_and_playtest
```

without removing any existing module.

- [ ] **Step 3: Commit RED**

```bash
git add tests/test_r2_function_recipe_material_fit_and_playtest.py \
  .github/workflows/validate-base-v942-planning-first-adoption.yml
git commit -m "test: define final batch material recipe contract"
```

- [ ] **Step 4: Run Planning-first RED**

Expected result:

```text
all existing 76 tests PASS
new focused tests FAIL only because BS-ITEM-20260806-06, 10/10 state,
canon, registry contract, and sheet declaration are absent
```

Record RED head, workflow run, existing-pass count, new-fail count, and failure reasons.

---

### Task 2: Create the planning canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_FUNCTION_RECIPE_MATERIAL_FIT_AND_PLAYTEST_CANON_2026.md`

**Interfaces:**
- Consumes: approved spec `docs/superpowers/specs/2026-08-06-function-recipes-material-fit-forging-playtest-design.md`.
- Produces: authority canon cited by registries, tests, PR, and Sheet.

- [ ] **Step 1: Write the canon header and state**

Include:

```text
Decision: BS-ITEM-20260806-06
USER_APPROVED / R2_BATCH_005_10_OF_10 / APPROVED_PENDING_MERGE
BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED
Google Sheet mirror: 42_능력치_강화_참조표
제품 구현: BLOCKED
```

- [ ] **Step 2: Record the exact primary-material matrix**

Use:

```text
iron: all nine role-stat equipment groups STANDARD_ROLE_FIT
silver HIGH: SWORD, RANGED, LIGHT_ARMOR
silver STANDARD: SHIELD_SUPPORT, MEDIUM_ARMOR
silver LOW: AXE, BLUNT, POLEARM, HEAVY_ARMOR
meteor_iron HIGH: AXE, BLUNT, POLEARM, HEAVY_ARMOR
meteor_iron STANDARD: SWORD, SHIELD_SUPPORT, MEDIUM_ARMOR
meteor_iron LOW: RANGED, LIGHT_ARMOR
```

- [ ] **Step 3: Record direct-forging ownership**

```text
OUTSIDE_GOOD_ZONE -> -1
GOOD_ZONE -> 0
PERFECT_ZONE -> +1
AUTO -> 0
```

State that the role strike is deterministic, excluded from grade scoring, and not applied to items without a role raw stat.

- [ ] **Step 4: Record initial and rework recipes**

Copy the six exact initial recipes from the approved spec. Record the catalyst-tag contract and the exact mapping:

```text
fire -> element:fire
fire -> environment:fire
```

Current available bound reworks:

```text
ELEMENTAL_WARD(FIRE)
ENVIRONMENTAL_SEALING(FIRE)
```

All other named reworks are `CONTENT_NOT_AVAILABLE` until a matching catalyst tag exists.

- [ ] **Step 5: Record playtest and protection gates**

Include the 48-case solo matrix, external 3–5 player protocol, metric thresholds, `PASS / REVISE / REJECT`, and exact protected product files.

- [ ] **Step 6: Commit the canon**

```bash
git add docs/planning/BLACKSMITH_R2_FUNCTION_RECIPE_MATERIAL_FIT_AND_PLAYTEST_CANON_2026.md
git commit -m "docs: approve material fit recipes and playtest gate"
```

---

### Task 3: Synchronize authority registries and entrypoints

**Files:**
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: Task 2 canon.
- Produces: current 10/10 authority state.

- [ ] **Step 1: Add the registry Decision**

The compact registry contract must contain:

```json
{
  "id":"BS-ITEM-20260806-06",
  "status":"USER_APPROVED_R2_BATCH_005_10_OF_10_APPROVED_PENDING_MERGE",
  "canon":"docs/planning/BLACKSMITH_R2_FUNCTION_RECIPE_MATERIAL_FIT_AND_PLAYTEST_CANON_2026.md",
  "contract":{
    "material_role_fit_model":"EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP",
    "direct_forging_role_result_model":"DETERMINISTIC_ROLE_STRIKE_THREE_ZONE",
    "function_recipe_model":"ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY",
    "current_available_bound_reworks":["ELEMENTAL_WARD_FIRE","ENVIRONMENTAL_SEALING_FIRE"],
    "solo_playtest_case_count":48,
    "external_playtester_minimum":3,
    "external_playtester_maximum":5,
    "sheet_reference_tab":"42_능력치_강화_참조표",
    "product_implementation":"BLOCKED"
  }
}
```

Also update active batch decisions, approved count, counter, and stage status to 10/10 while preserving compact JSON serialization.

- [ ] **Step 2: Update current decision summaries and Game Bible**

Add the exact material matrix, three-zone result, current fire-only rework availability, and human playtest gate. Historical 1–9/10 evidence must remain historical and not be globally replaced.

- [ ] **Step 3: Update hub entrypoints**

Every current-status entrypoint must point to `R2_BATCH_005_10_OF_10`, the new canon, and the next checkpoint boundary.

- [ ] **Step 4: Validate JSON**

```bash
python -m json.tool docs/planning/CURRENT_R2_CANON_REGISTRY.json > /dev/null
python -m json.tool '[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json' > /dev/null
```

---

### Task 4: Refine prior canons and validators

**Files:**
- Modify: `docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md`
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`
- Modify: existing active batch tests whose current-state expectations are 9/10.

**Interfaces:**
- Consumes: Task 3 registry state.
- Produces: no stale current 9/10 assertions and no ambiguity about refined ownership.

- [ ] **Step 1: Add refinement markers**

Each refined canon must include:

```text
REFINED_BY_BS-ITEM-20260806-06
R2_BATCH_005_10_OF_10
```

and defer exact material/recipe/playtest details to the new canon.

- [ ] **Step 2: Update current-state tests only**

Replace active expectations of `9/10` with `10/10` only where the assertion describes current state. Preserve historical Decision-specific batch counters.

- [ ] **Step 3: Extend core alignment and operating audit**

Require the new canon, Decision ID, 10/10 state, material model, three-zone forging model, current rework availability, playtest count, and sheet tab declaration.

- [ ] **Step 4: Run focused GREEN tests**

```bash
python -m unittest \
  tests.test_base_v942_planning_first_adoption \
  tests.test_r2_artistry_generation_growth_economy \
  tests.test_r2_customer_equipment_compatibility \
  tests.test_r2_mobile_customer_card_progressive_disclosure \
  tests.test_r2_enhancement_dominant_simple_load_gate \
  tests.test_r2_equipment_base_weight_points \
  tests.test_r2_weight_performance_budget_and_lightweight_tradeoff \
  tests.test_r2_weight_budget_conversion_and_role_presets \
  tests.test_r2_item_role_stat_and_initial_function_catalog \
  tests.test_r2_initial_role_stat_preset_and_enhancement_function_ownership \
  tests.test_r2_function_recipe_material_fit_and_playtest -v
```

Expected: all focused contracts PASS.

- [ ] **Step 5: Run core and Base audit**

```bash
python tests/check_project_core_alignment.py
python tools/run_project_operating_system_audit.py \
  --base-root base-src \
  --report /tmp/blacksmith-base-adoption-report.json
```

Expected: both PASS.

---

### Task 5: Protect product scope and record TDD evidence

**Files:**
- Modify: `tests/test_r2_function_recipe_material_fit_and_playtest.py`

**Interfaces:**
- Consumes: RED and GREEN workflow evidence.
- Produces: permanent exact evidence assertions.

- [ ] **Step 1: Compare against main**

```bash
git diff --name-only origin/main...HEAD
```

Fail if any changed path starts with:

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

- [ ] **Step 2: Verify protected files**

Confirm these file SHAs remain unchanged from the prior exact head:

```text
data/crafting/materials.json
data/crafting/weapon_bases.json
data/crafting/forging_balance.json
data/crafting/craftsmanship_grades.json
```

- [ ] **Step 3: Add TDD evidence assertion**

Record exact RED head/run/counts, GREEN sync head/run/counts, and protected-path result in the new test file.

- [ ] **Step 4: Commit final user head**

```bash
git add tests/test_r2_function_recipe_material_fit_and_playtest.py
git commit -m "test: record final batch material recipe evidence"
```

---

### Task 6: Run final exact-head CI

**Files:** none.

**Interfaces:**
- Consumes: final user head from Task 5.
- Produces: exact verification evidence.

- [ ] **Step 1: Run Planning-first workflow**

Expected: all focused contract tests PASS.

- [ ] **Step 2: Run Base adoption workflow**

Expected: CI gate and adversarial gate PASS.

- [ ] **Step 3: Run PR validation**

Expected:

```text
Python contracts PASS
project operating audit PASS
game/lifecycle data PASS
forging quality PASS
enhancement failure PASS
balance simulator PASS
Godot 4.7.1 import/parse PASS
scene smoke PASS
model/integration PASS
```

---

### Task 7: Extend Google Sheet reference tables

**Files:** Google Spreadsheet `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`.

**Interfaces:**
- Consumes: final exact head and canon.
- Produces: same-Decision reference mirror.

- [ ] **Step 1: Append four sections to `42_능력치_강화_참조표`**

Append after the current used range:

```text
5. 주재료 역할 적합표 — PRIMARY_MATERIAL_ROLE_FIT
6. 직접 단조 역할 결과 — DIRECT_FORGING_ROLE_RESULT
7. 최초 제작·재작업 기능 레시피 — FUNCTION_RECIPE_CATALOG
8. 사람 플레이테스트 계획 — HUMAN_PLAYTEST_PLAN
```

- [ ] **Step 2: Populate exact tables**

Include all 27 material-fit cells, three role-strike results plus AUTO, six initial recipes, six rework tag requirements and availability, Stage A/Stage B counts, and PASS/REVISE/REJECT thresholds.

- [ ] **Step 3: Apply existing sheet style**

Use the same dark section bars, gray headers, wrapped body cells, borders, and column widths already used by sections 1–4.

- [ ] **Step 4: Update standard surfaces**

Append the same Decision ID and exact head to:

```text
00_프로젝트_허브
02_현재_확정결정
04_누락_충돌_감사
05_GDD_요약
40_핵심시스템_메인콘텐츠
99_변경이력
```

- [ ] **Step 5: Read back values and formatting**

Verify the new sections, standard rows, Decision ID, 10/10 state, exact head, and Draft/unmerged/product-blocked status.

---

### Task 8: Update PR #109 and final review boundary

**Files:** PR #109 metadata.

**Interfaces:**
- Consumes: final exact head and Sheet readback.
- Produces: complete 10/10 Draft PR description.

- [ ] **Step 1: Update title and body**

The PR body must report all 10 Decisions, exact material matrix, direct-forging mapping, function recipes, playtest gate, RED/GREEN/final CI, Sheet ranges, protected scope, and next checkpoint action.

- [ ] **Step 2: Verify review state**

Confirm:

```text
state = open
draft = true
merged = false
mergeable = true
comments = 0 unless new comments exist
unresolved review threads = 0 unless new threads exist
```

- [ ] **Step 3: Do not merge**

At 10/10, stop at the checkpoint boundary and report that explicit user approval is required before merging or starting the next batch.
