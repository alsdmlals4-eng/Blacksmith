# Blacksmith R2 작품 역할 원수치와 최초 기능 카탈로그 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `BS-ITEM-20260806-04`를 R2 배치 8/10 정본으로 기록하고, 단일 역할 원수치 모델과 최초 마법·유틸리티 기능 6종을 검증 가능한 계약으로 고정한다.

**Architecture:** 제품 구현 없이 기획 정본·레지스트리·현재 진입점·계약 테스트·운영 감사를 같은 Decision ID로 동기화한다. 작품은 장비군에 맞는 단일 역할 원수치만 갖고, 특수기능은 용량을 소비하는 승인 함수 인스턴스로 분리한다.

**Tech Stack:** Markdown, compact JSON, Python `unittest`, GitHub Actions, Google Sheets.

## Global Constraints

- Decision ID: `BS-ITEM-20260806-04`
- Active batch: `R2_BATCH_005_8_OF_10`
- Product implementation: `BLOCKED`
- PR #109 remains `OPEN / DRAFT / UNMERGED`
- Runtime, game data, scripts, scenes, images, assets, addons, and `project.godot` must not change.
- `data/crafting/weapon_bases.json` must remain unchanged.
- No generic event-success bonus from function tags.
- No default secondary combat-stat schema.

---

### Task 1: Add RED contract

**Files:**
- Create: `tests/test_r2_item_role_stat_and_initial_function_catalog.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Produces: Contract assertions for the new Decision and authority documents.

- [ ] **Step 1: Write the failing test**

Create a `unittest.TestCase` that asserts:

```python
self.assertEqual("R2_BATCH_005_ACTIVE_8_OF_10", registry["stage_status"])
self.assertEqual("8/10", registry["next_approval_counter"])
self.assertIn("BS-ITEM-20260806-04", decisions)
self.assertEqual(
    "SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS",
    contract["item_role_stat_model"],
)
```

The test must also assert the exact attack/defense formulas, equipment-group ownership, absence of default secondary combat stats, the six function IDs and costs, duplicate prohibition, bound-context requirements, capacity-3 separate approval, product blocking, and unchanged `weapon_bases.json`.

- [ ] **Step 2: Add the test module to Planning-first CI**

Append:

```yaml
tests.test_r2_item_role_stat_and_initial_function_catalog
```

to the focused `python -m unittest` command.

- [ ] **Step 3: Run RED**

Run the Planning-first workflow on the RED head.

Expected:

```text
Existing 57 contracts PASS.
New contract failures are limited to missing Decision, 8/10 state, canon, function catalog, and refinements.
```

- [ ] **Step 4: Commit RED evidence**

```bash
git add tests/test_r2_item_role_stat_and_initial_function_catalog.py \
  .github/workflows/validate-base-v942-planning-first-adoption.yml
git commit -m "test: define item role stat and function catalog contract"
```

### Task 2: Create authority canon and registry contract

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: `BS-ITEM-20260806-03`, design spec.
- Produces: Current authority contract used by tests and audits.

- [ ] **Step 1: Add the canon**

The canon must contain:

```text
ITEM_ROLE_STAT_MODEL = SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS
DISPLAY_ATTACK = CRAFTED_ATTACK + WEIGHT_ATTACK_OUTPUT + APPROVED_ENHANCEMENT_ATTACK_OUTPUT
DISPLAY_DEFENSE = CRAFTED_DEFENSE + WEIGHT_DEFENSE_OUTPUT + APPROVED_ENHANCEMENT_DEFENSE_OUTPUT
```

It must enumerate:

```text
ARCANE_CONDUCTION: 1
ELEMENTAL_WARD: 1
ARCANE_SENSING: 2
ENVIRONMENTAL_SEALING: 1
FIELD_SERVICEABILITY: 1
TASK_INTEGRATION: 1
```

- [ ] **Step 2: Update the compact registry**

Set:

```json
{
  "stage_status": "R2_BATCH_005_ACTIVE_8_OF_10",
  "next_approval_counter": "8/10"
}
```

Append `BS-ITEM-20260806-04` as the eighth active decision with a `contract` object containing all exact identifiers from the spec.

- [ ] **Step 3: Register the canon**

Add the canon, spec, plan, and test paths to the design document registry using the same Decision ID.

- [ ] **Step 4: Validate JSON**

```bash
python -m json.tool docs/planning/CURRENT_R2_CANON_REGISTRY.json > /dev/null
python -m json.tool '[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json' > /dev/null
```

### Task 3: Synchronize current authority entrypoints

**Files:**
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`

**Interfaces:**
- Consumes: New canon and registry state.
- Produces: Truthful human-readable current context.

- [ ] **Step 1: Advance all active counters to 8/10**

Replace only active batch references. Historical batch counters must remain unchanged.

- [ ] **Step 2: Add the new Decision summary**

Record the single-stat model, formulas, function list, capacity behavior, and product block.

- [ ] **Step 3: Update next gate**

Set the next planning gate to function acquisition/upgrade ownership and exact baseline distributions, without authorizing implementation.

### Task 4: Refine dependent canons

**Files:**
- Modify: `docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`

**Interfaces:**
- Consumes: `BS-ITEM-20260806-04` canon.
- Produces: Explicit refinement links and no contradictory ownership.

- [ ] **Step 1: Add refinement markers**

Each file must contain:

```text
REFINED_BY_BS-ITEM-20260806-04
R2_BATCH_005_8_OF_10
```

- [ ] **Step 2: Clarify ownership**

State that functions consume capacity but do not automatically appear from weight gain, do not replace customer fit, and do not alter generic success.

### Task 5: Update contract validators and reach GREEN

**Files:**
- Modify: `tests/check_project_core_alignment.py`
- Modify: existing active-batch tests with stale 7/10 assertions
- Modify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: Synchronized authority state.
- Produces: Whole-project consistency verification.

- [ ] **Step 1: Update exact active-batch expectations**

Core alignment must expect eight decisions in this exact order:

```python
[
    "BS-CRAFT-20260805-02",
    "BS-CUSTOMER-20260805-01",
    "BS-UX-20260805-01",
    "BS-CUSTOMER-20260806-01",
    "BS-ITEM-20260806-01",
    "BS-ITEM-20260806-02",
    "BS-ITEM-20260806-03",
    "BS-ITEM-20260806-04",
]
```

- [ ] **Step 2: Register the new canon in the operating audit**

Require the Decision ID, 8/10 status, model ID, six function IDs, and product block.

- [ ] **Step 3: Run focused GREEN**

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
  tests.test_r2_item_role_stat_and_initial_function_catalog -v
```

Expected: all focused tests PASS.

- [ ] **Step 4: Run alignment and operating audit**

```bash
python tests/check_project_core_alignment.py
python tools/run_project_operating_system_audit.py --base-root base-src --report /tmp/blacksmith-base-adoption-report.json
```

Expected: PASS.

### Task 6: Remove one-shot artifacts and verify final exact head

**Files:**
- Delete any one-shot synchronizer, temporary workflow, temporary Base checkout, and generated report from the branch.
- Modify one permanent contract test only if a user-authored evidence commit is required to trigger PR workflows.

**Interfaces:**
- Consumes: GREEN authority state.
- Produces: Clean exact head with complete CI evidence.

- [ ] **Step 1: Confirm protected paths are unchanged**

Compare against base `476ddc380079dd61d67cda4c065a80819355292f` and require zero changes under product paths.

- [ ] **Step 2: Run exact-head workflows**

Require PASS for:

```text
Planning-first
Base adoption
PR validation
Python full contracts
Project operating audit
Godot 4.7.1 import, parse, scene smoke, model and integration
```

- [ ] **Step 3: Review PR comments and threads**

Require zero unresolved P0/P1 issues before final reporting.

### Task 7: Synchronize Google Sheet and PR body

**Files:**
- Google Sheet: `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`
- PR: `#109`

**Interfaces:**
- Consumes: Final exact head and CI evidence.
- Produces: Same Decision ID and status across GitHub and Sheet.

- [ ] **Step 1: Write the next empty rows**

Update hub, current decisions, audit, GDD summary, core systems, and change history with `BS-ITEM-20260806-04`, `8/10`, exact head, Draft/unmerged, and product blocked status.

- [ ] **Step 2: Read back all written ranges**

Verify the Decision ID, counter, exact head, and CI evidence in every range.

- [ ] **Step 3: Update PR #109**

List eight decisions, formulas, six functions, test evidence, changed-file boundary, Sheet readback, and merge boundary. Keep Draft and unmerged.

## Self-Review

- Spec coverage: all sections have a corresponding task.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation step remains.
- Type consistency: Decision ID, batch counter, model ID, function IDs, and authority paths are identical across tasks.
