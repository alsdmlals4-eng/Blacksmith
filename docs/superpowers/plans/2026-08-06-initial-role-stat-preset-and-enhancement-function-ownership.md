# Initial Role Stat Preset and Enhancement Function Ownership Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Canonize `BS-ITEM-20260806-05` as the ninth approval in `R2_BATCH_005`, define test-role-stat values and exclusive enhancement/function change ownership, and mirror the approved contract in a new `42_능력치_강화_참조표` Google Sheet tab.

**Architecture:** GitHub planning canon remains authoritative. A new contract test drives registry and document changes from RED to GREEN, while product paths remain untouched. After exact-head validation, Google Sheets receives one formatted reference tab and standard decision/readback rows using the same Decision ID and exact head.

**Tech Stack:** Markdown canon, JSON registries, Python `unittest`, GitHub Actions, GitHub connector, Google Sheets API connector.

## Global Constraints

- Active branch: `agent/r2-artistry-generation-growth-economy-design`.
- Active PR: `#109`, which must remain `OPEN / DRAFT / UNMERGED`.
- Target status: `R2_BATCH_005_ACTIVE_9_OF_10` and `9/10`.
- Product implementation remains `BLOCKED`.
- Do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.
- `data/crafting/weapon_bases.json` must remain unchanged.
- Exact balance values are `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`.
- General enhancement owns enhancement level and generic event-success bonus only.
- Precision output lanes `STAT_METHOD` and `FUNCTION_REWORK` are mutually exclusive per milestone.
- Google Sheet is a mirror; GitHub canon is authority.

---

### Task 1: Add the failing approval contract

**Files:**
- Create: `tests/test_r2_initial_role_stat_preset_and_enhancement_function_ownership.py`
- Modify later: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`.
- Produces: exact assertions for Decision `BS-ITEM-20260806-05`, 9/10 state, canon tokens, refinement markers, and protected product paths.

- [ ] **Step 1: Write the failing test**

Create a `unittest.TestCase` with these methods:

```python
def test_batch_005_contains_nine_approved_decisions(): ...
def test_initial_role_stat_formula_and_values_are_exact(): ...
def test_general_enhancement_owns_no_item_raw_stat_delta(): ...
def test_precision_method_delta_table_is_exact(): ...
def test_function_rework_is_exclusive_owner(): ...
def test_item_change_ledger_fields_are_exact(): ...
def test_customer_user_stat_reference_contract_is_preserved(): ...
def test_authority_documents_and_refinements_exist(): ...
def test_sheet_reference_contract_is_declared(): ...
```

Assert exact values:

```python
BASE_ITEM_ROLE_BASE = {
    "SWORD": 5,
    "RANGED": 5,
    "AXE": 10,
    "BLUNT": 10,
    "POLEARM": 15,
    "SHIELD_SUPPORT": 5,
    "LIGHT_ARMOR": 5,
    "MEDIUM_ARMOR": 10,
    "HEAVY_ARMOR": 15,
    "TOOL": None,
    "CLOTHING_OR_ROBE": None,
    "ACCESSORY": None,
}
PRIMARY_MATERIAL_ROLE_FIT_MODIFIER = {
    "LOW_ROLE_FIT": -2,
    "STANDARD_ROLE_FIT": 0,
    "HIGH_ROLE_FIT": 2,
}
DIRECT_FORGING_ROLE_MODIFIER = {
    "BELOW_EXPECTED_DIRECT_FORGING": -1,
    "EXPECTED_DIRECT_FORGING": 0,
    "ABOVE_EXPECTED_DIRECT_FORGING": 1,
}
```

Assert general-enhancement non-owned fields:

```python
[
    "ATTACK",
    "DEFENSE",
    "WEIGHT",
    "DURABILITY",
    "HANDLING",
    "ARTISTRY",
    "MAGIC_FUNCTION_CAPACITY",
    "UTILITY_CAPACITY",
    "SPECIAL_FUNCTIONS",
]
```

Assert precision outputs:

```python
EDGE_REINFORCEMENT -> STAT_METHOD / ATTACK +5
SHOCK_ABSORPTION -> STAT_METHOD / DEFENSE +5
BALANCE_TUNING -> STAT_METHOD / HANDLING +5
ARTISTIC_FINISH -> STAT_METHOD / ARTISTRY +5
LIGHTWEIGHTING -> STAT_METHOD / CURRENT_WEIGHT -5 / allocated output preserved
WEIGHTING -> STAT_METHOD / CURRENT_WEIGHT +5 / peak-only role output
ENVIRONMENTAL_TREATMENT -> FUNCTION_REWORK / approved environment function operation
```

Assert function actions `ADD / REPLACE / REBIND / REMOVE`, no milestone refund, failed rework preservation, no duplicate function ID, no hidden function level, and product implementation `BLOCKED`.

- [ ] **Step 2: Run the focused contract to verify RED**

Run through a temporary user-authored workflow or the existing planning-first workflow after registering the test.

Expected:

```text
Existing 66 tests PASS.
New tests FAIL only because BS-ITEM-20260806-05, 9/10 registry state, canon, and refinements do not exist.
```

- [ ] **Step 3: Record RED evidence**

Capture:

```text
red_head
planning_first_run
existing_pass_count
expected_new_failure_count
```

- [ ] **Step 4: Commit the failing contract**

Commit message:

```text
test: define initial stat and enhancement ownership contract
```

### Task 2: Create the canonical Decision and registry contract

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: the design spec and failing tests from Task 1.
- Produces: `BS-ITEM-20260806-05` contract fields read by tests and current entrypoints.

- [ ] **Step 1: Write the canon document**

Include exact sections:

```text
Decision and 9/10 status
CRAFTED_ROLE_STAT formula
BASE_ITEM_ROLE_BASE table
PRIMARY_MATERIAL_ROLE_FIT_MODIFIER table
DIRECT_FORGING_ROLE_MODIFIER table
DISPLAY_ATTACK / DISPLAY_DEFENSE sources
GENERAL_ENHANCEMENT ownership and non-owned field list
seven precision method outputs with output lane
FUNCTION_REWORK acquisition and four operations
ITEM_CHANGE_LEDGER_ENTRY fields
customer/user reference table
Google Sheet mirror contract
protection conditions
playtest and product gates
```

- [ ] **Step 2: Add the registry Decision**

Set:

```json
{
  "id": "BS-ITEM-20260806-05",
  "status": "USER_APPROVED_R2_BATCH_005_9_OF_10_APPROVED_PENDING_MERGE",
  "canon": "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md",
  "spec": "docs/superpowers/specs/2026-08-06-initial-role-stat-preset-and-enhancement-function-ownership-design.md",
  "plan": "docs/superpowers/plans/2026-08-06-initial-role-stat-preset-and-enhancement-function-ownership.md"
}
```

Set active batch:

```text
stage_status = R2_BATCH_005_ACTIVE_9_OF_10
next_approval_counter = 9/10
approved_decisions = 9
counter = 9/10
append BS-ITEM-20260806-05
```

- [ ] **Step 3: Register the canon in the design registry**

Add the exact path and active status without deleting historical entries.

- [ ] **Step 4: Validate both JSON files**

Run:

```bash
python -m json.tool docs/planning/CURRENT_R2_CANON_REGISTRY.json > /dev/null
python -m json.tool '[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json' > /dev/null
```

Expected: both commands exit `0`.

- [ ] **Step 5: Commit the Decision and registry**

Commit message:

```text
docs: canonize initial stat and enhancement ownership
```

### Task 3: Synchronize current authority entrypoints and refinements

**Files:**
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md`

**Interfaces:**
- Consumes: Decision contract from Task 2.
- Produces: truthful 9/10 entrypoints and explicit `REFINED_BY_BS-ITEM-20260806-05` markers.

- [ ] **Step 1: Change only active batch assertions from 8/10 to 9/10**

Preserve historical 1/10 through 8/10 evidence. Update active status and next gate only.

- [ ] **Step 2: Add current Decision summary**

Summarize:

```text
first craft role base + material fit + direct forging result
normal enhancement changes no item raw stats
precision methods own explicit deltas
function rework owns function-list mutations
change ledger required
```

- [ ] **Step 3: Add refinement markers**

Each refined canon receives:

```markdown
<!-- REFINED_BY_BS-ITEM-20260806-05 -->
```

and a short section preserving the prior contract while delegating exact current ownership to the new canon.

- [ ] **Step 4: Update the next gate**

Set next gate to:

```text
작품별 특수기능 제작·재작업 레시피와 테스트 프리셋 플레이테스트 계획
```

- [ ] **Step 5: Commit authority synchronization**

Commit message:

```text
docs: sync stat and enhancement ownership authority
```

### Task 4: Make all planning and audit contracts GREEN

**Files:**
- Modify: `tests/test_base_v942_planning_first_adoption.py`
- Modify: existing R2 contract tests that assert the active approval counter
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`
- Modify: `tests/test_r2_initial_role_stat_preset_and_enhancement_function_ownership.py`

**Interfaces:**
- Consumes: 9/10 canon and refinements.
- Produces: focused and full exact-head validation evidence.

- [ ] **Step 1: Update active counter assertions**

Replace only assertions representing current state:

```text
8/10 -> 9/10
R2_BATCH_005_ACTIVE_8_OF_10 -> R2_BATCH_005_ACTIVE_9_OF_10
approved_decisions 8 -> 9
```

Do not replace immutable historical strings.

- [ ] **Step 2: Register the new test in planning-first CI**

Append:

```text
tests.test_r2_initial_role_stat_preset_and_enhancement_function_ownership
```

- [ ] **Step 3: Register canon and required assertions in core alignment and operating audit**

Require:

```text
BS-ITEM-20260806-05
R2_BATCH_005_9_OF_10
42_능력치_강화_참조표
제품 구현: `BLOCKED`
```

- [ ] **Step 4: Run focused GREEN verification**

Run all planning-first modules through the same command used by the workflow.

Expected: all focused tests PASS with zero failures.

- [ ] **Step 5: Run project core alignment and Base operating audit**

Run:

```bash
python tests/check_project_core_alignment.py
python tools/run_project_operating_system_audit.py --base-root base-src --report /tmp/blacksmith-base-adoption-report.json
```

Expected: both PASS.

- [ ] **Step 6: Verify protected product paths**

Compare against base main `476ddc380079dd61d67cda4c065a80819355292f`.

Expected:

```text
product protected paths changed = 0
data/crafting/weapon_bases.json unchanged
```

- [ ] **Step 7: Remove temporary one-shot files and commit GREEN synchronization**

Commit message:

```text
docs: synchronize initial stat and enhancement ownership canon
```

- [ ] **Step 8: Record RED/GREEN evidence in the new test**

Add exact heads, run IDs, pass/failure counts, audit result, and protected path count.

Commit message:

```text
test: record stat and enhancement ownership evidence
```

### Task 5: Run exact-head project validation

**Files:**
- No intended file changes unless validation exposes an exact defect.

**Interfaces:**
- Consumes: final user-authored branch head from Task 4.
- Produces: exact-head CI evidence for PR and Sheet readback.

- [ ] **Step 1: Run Planning-first workflow**

Expected: completed with `success` and all contract tests PASS.

- [ ] **Step 2: Run Base adoption workflow**

Expected: completed with `success`.

- [ ] **Step 3: Run PR validation workflow**

Expected:

```text
Python code contracts PASS
project operating audit PASS
game/lifecycle data PASS
forging quality PASS
enhancement failure PASS
balance simulator PASS
Godot 4.7.1 import/parse PASS
scene smoke PASS
model/integration PASS
```

- [ ] **Step 4: Verify PR review state**

Expected:

```text
comments = 0 or addressed
unresolved review threads = 0
Draft = true
merged = false
```

### Task 6: Create and format the Google Sheet reference tab

**Files:**
- Google Sheet: `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`
- Create tab: `42_능력치_강화_참조표`

**Interfaces:**
- Consumes: exact final GitHub head and Decision contract.
- Produces: one readable reference tab containing four tables.

- [ ] **Step 1: Add the new sheet**

Use `addSheet` with:

```json
{
  "title": "42_능력치_강화_참조표",
  "index": 16,
  "gridProperties": {
    "rowCount": 120,
    "columnCount": 10,
    "frozenRowCount": 3
  }
}
```

- [ ] **Step 2: Write title and status rows**

Rows 1–3 contain:

```text
Blacksmith 능력치·강화 참조표
BS-ITEM-20260806-05 / R2_BATCH_005_9_OF_10 / exact head
PLANNING_CANON_ONLY / BASELINE_TEST_PRESET / USER_PLAYTEST_NOT_RUN / PRODUCT_BLOCKED
```

Merge `A1:J1`, `A2:J2`, and `A3:J3`.

- [ ] **Step 3: Write Table 1 — item/weapon stats**

Place section title on row 5, header on row 6, and data rows 7–18.

Headers:

```text
분류 | 장비군 | 필수 역할 수치 | 장비군 기준값 | 주재료 보정 | 직접 단조 보정 | 기본 중량 | 초기 중량 출력 | 표시 공식 | 상태·비고
```

Include all twelve equipment groups and exact test values.

- [ ] **Step 4: Write Table 2 — customer/user stats**

Place section title on row 21, header on row 22, and data rows 23–29.

Headers:

```text
능력 ID | 한글명 | 범위 | 장비 판정 역할 | 성공률 영향 | 작품 원수치 영향 | 표시 조건 | 소유 주체 | 상태 | 비고
```

- [ ] **Step 5: Write Table 3 — enhancement changes**

Place section title on row 32, header on row 33, and data rows 34–42.

Headers:

```text
강화 유형 | 방식 | 시점 | 출력 차선 | 변경 필드 | 테스트 변동 | 보존 값 | 동시 획득 금지 | 상태 | 비고
```

Include general enhancement and seven precision methods.

- [ ] **Step 6: Write Table 4 — special functions and rework**

Place section title on row 45, header on row 46, function rows 47–52, then rework action rows 54–57.

Headers:

```text
종류 | ID/행동 | 용량 비용 | 결속 필요 | 획득 시점 | 변경 결과 | 용량 검사 | 실패 시 | 상태 | 비고
```

- [ ] **Step 7: Apply formatting**

Use:

```text
Title rows: dark gray background, white bold font, centered
Section rows: medium gray background, white bold font
Header rows: RGB 0.898/0.898/0.898, bold, centered, wrapped
Body: white background, Arial 10, top aligned, wrapped
```

Set column widths approximately:

```text
A 145, B 170, C 135, D 170, E 170,
F 210, G 190, H 190, I 230, J 280 pixels
```

- [ ] **Step 8: Read back the tab**

Read:

```text
42_능력치_강화_참조표!A1:J18
42_능력치_강화_참조표!A21:J29
42_능력치_강화_참조표!A32:J42
42_능력치_강화_참조표!A45:J57
```

Verify values and formatting metadata.

### Task 7: Synchronize standard Sheet decision surfaces

**Files:**
- Existing Google Sheet tabs.

**Interfaces:**
- Consumes: exact head and new tab readback.
- Produces: standard project tracking rows for Decision 9/10.

- [ ] **Step 1: Write project hub status**

Update:

```text
00_프로젝트_허브!H2:J2
```

- [ ] **Step 2: Append Decision and audit rows**

Write:

```text
02_현재_확정결정!A101:M101
04_누락_충돌_감사!A90:H90
05_GDD_요약!A86:J86
40_핵심시스템_메인콘텐츠!A22:J22
99_변경이력!A109:H109
```

Use system ID `BS-S-21` in the system table.

- [ ] **Step 3: Read back every written range**

Expected: every range contains `BS-ITEM-20260806-05`, `9/10`, exact head, Draft/unmerged, product blocked, and exact CI evidence.

### Task 8: Update PR #109 and perform final verification

**Files:**
- PR #109 metadata only.

**Interfaces:**
- Consumes: GitHub and Sheet readback evidence.
- Produces: final Draft PR summary for nine Decisions.

- [ ] **Step 1: Update PR title and body**

Add:

```text
BS-ITEM-20260806-05
initial role stat formula and values
general enhancement no-auto-raw-stat rule
seven precision method outputs
function rework ownership
new Sheet tab and readback ranges
RED/GREEN and exact-head CI evidence
```

- [ ] **Step 2: Verify PR remains Draft and unmerged**

Freshly read PR metadata and exact head.

- [ ] **Step 3: Verify exact-head workflows again**

Freshly read all three workflow conclusions. Do not rely on earlier output.

- [ ] **Step 4: Verify canon and Sheet readback again**

Read the first canon section and the four new tab ranges.

- [ ] **Step 5: Report completion without merging**

Report the Decision, exact numbers, file/sheet locations, CI runs, protected path count, playtest status, and next gate.
