# Weight Performance Budget and Lightweight Trade-off Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make equipment weight a readable performance-versus-usability trade-off by deriving one performance-budget point from every five final weight points and making lightweighting reduce both weight and budget.

**Architecture:** Add Decision `BS-ITEM-20260806-02` as a focused refinement of the current fixed-weight and binary-load contracts. Weight contributes one small, derived budget source that is allocated to exactly one compatible performance lane per point. `LIGHTWEIGHT / NONE / WEIGHTED` is owned by the precision-enhancement method, replaces rather than stacks, and never changes generic customer success directly.

**Tech Stack:** Markdown planning canon, JSON authority registries, Python unittest contracts, GitHub Actions, Google Sheets authority mirror.

## Global Constraints

- Decision ID: `BS-ITEM-20260806-02`.
- Active batch: `R2_BATCH_005_6_OF_10`.
- `EFFECTIVE_WEIGHT = max(0, BASE_WEIGHT + STRUCTURAL_WEIGHT_DELTA)`.
- `WEIGHT_PERFORMANCE_BUDGET = EFFECTIVE_WEIGHT / 5`.
- Each `5 WEIGHT_POINT` contributes exactly `+1 PERFORMANCE_BUDGET_POINT`.
- Budget lanes: `ATTACK_BUDGET / DEFENSE_BUDGET / MAGIC_FUNCTION_BUDGET / UTILITY_BUDGET`.
- One budget point is allocated to one compatible lane only.
- `LIGHTWEIGHT = -5 weight and -1 budget`, `NONE = 0`, `WEIGHTED = +5 weight and +1 budget`.
- Structural weight treatment belongs to the precision-enhancement method, not `CATALYST_AFFIX`.
- One item has at most one active structural treatment; rework replaces and recalculates it.
- Accessories receive no weight-derived budget and no structural weight treatment by default.
- Weight budget is not multiplied by material, grade, artistry, catalyst, chronicle, or enhancement.
- Weight budget does not directly change generic customer event success.
- Runtime, scenes, assets, images, and `data/crafting/weapon_bases.json` remain unchanged.
- Product implementation remains `BLOCKED`.

---

### Task 1: RED planning contract

**Files:**
- Create: `tests/test_r2_weight_performance_budget_and_lightweight_tradeoff.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: current batch `R2_BATCH_005_5_OF_10`, Decision `BS-ITEM-20260806-01`, and the written design spec.
- Produces: a failing contract requiring Decision `BS-ITEM-20260806-02`, active batch 6/10, the exact formulas, lane rules, ownership, replacement semantics, and product blocking.

- [ ] **Step 1: Write the failing contract**

Create tests that assert:

```python
self.assertEqual("R2_BATCH_005_ACTIVE_6_OF_10", registry["stage_status"])
self.assertEqual("6/10", registry["next_approval_counter"])
self.assertIn("BS-ITEM-20260806-02", decisions)
self.assertEqual("EFFECTIVE_WEIGHT_DIVIDED_BY_5", contract["weight_performance_budget_formula"])
self.assertEqual(5, contract["weight_points_per_budget_point"])
self.assertEqual(
    ["ATTACK_BUDGET", "DEFENSE_BUDGET", "MAGIC_FUNCTION_BUDGET", "UTILITY_BUDGET"],
    contract["budget_lanes"],
)
self.assertEqual("PRECISION_ENHANCEMENT_METHOD", contract["structural_weight_treatment_owner"])
self.assertEqual({"LIGHTWEIGHT": -1, "NONE": 0, "WEIGHTED": 1}, contract["budget_delta_by_treatment"])
self.assertEqual(1, contract["maximum_active_structural_weight_treatments_per_item"])
self.assertFalse(contract["structural_weight_treatments_stack"])
self.assertFalse(contract["weight_budget_directly_changes_generic_success_rate"])
self.assertFalse(contract["accessory_weight_budget_enabled_by_default"])
self.assertEqual("BLOCKED", contract["product_implementation"])
```

Authority-document tests must require:

```text
BS-ITEM-20260806-02
R2_BATCH_005_6_OF_10
최종 중량 5당 성능 예산 +1
경량화 -5 중량 / -1 예산
중량화 +5 중량 / +1 예산
PRECISION_ENHANCEMENT_METHOD
제품 구현: `BLOCKED`
```

- [ ] **Step 2: Add the test to Planning-first CI**

Add the new test path to workflow triggers and the module to the unittest invocation.

- [ ] **Step 3: Run Planning-first and verify RED**

Expected failure reasons:

```text
Decision BS-ITEM-20260806-02 absent
active batch remains 5/10
new canon absent
weight budget contract absent
```

- [ ] **Step 4: Record RED evidence**

Record the exact RED commit SHA and Planning-first run number in this plan and the later PR body.

---

### Task 2: GREEN machine-readable canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: design spec and RED contract.
- Produces: current Decision `BS-ITEM-20260806-02` and one machine-readable performance-budget contract.

- [ ] **Step 1: Write the focused canon**

The canon must include:

```text
EFFECTIVE_WEIGHT = max(0, BASE_WEIGHT + STRUCTURAL_WEIGHT_DELTA)
WEIGHT_PERFORMANCE_BUDGET = EFFECTIVE_WEIGHT / 5
TOTAL_PERFORMANCE_BUDGET = NON_WEIGHT_BASE_BUDGET + WEIGHT_PERFORMANCE_BUDGET
```

It must preserve the current base-weight table and state that weight budget is counted once.

- [ ] **Step 2: Store the exact contract**

Add this contract shape:

```json
{
  "weight_performance_budget_model": "FINAL_WEIGHT_LINEAR_SINGLE_SOURCE",
  "weight_performance_budget_formula": "EFFECTIVE_WEIGHT_DIVIDED_BY_5",
  "weight_points_per_budget_point": 5,
  "budget_lanes": [
    "ATTACK_BUDGET",
    "DEFENSE_BUDGET",
    "MAGIC_FUNCTION_BUDGET",
    "UTILITY_BUDGET"
  ],
  "budget_point_allocates_to_exactly_one_lane": true,
  "structural_weight_treatment_owner": "PRECISION_ENHANCEMENT_METHOD",
  "weight_delta_by_treatment": {
    "LIGHTWEIGHT": -5,
    "NONE": 0,
    "WEIGHTED": 5
  },
  "budget_delta_by_treatment": {
    "LIGHTWEIGHT": -1,
    "NONE": 0,
    "WEIGHTED": 1
  },
  "maximum_active_structural_weight_treatments_per_item": 1,
  "structural_weight_treatments_stack": false,
  "rework_semantics": "REPLACE_AND_RECALCULATE_DERIVED_BUDGET",
  "accessory_weight_budget_enabled_by_default": false,
  "weight_budget_directly_changes_generic_success_rate": false,
  "weight_budget_multiplied_by_other_progression_axes": false,
  "exact_stat_conversion": "BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
  "product_implementation": "BLOCKED"
}
```

- [ ] **Step 3: Advance only the active batch**

Set the active batch to six approved decisions without rewriting historical 1/10–5/10 approval evidence.

- [ ] **Step 4: Register canon, spec, and plan**

Mark all three documents as current planning authority for this Decision.

---

### Task 3: Refine current authority documents

**Files:**
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: new registry contract.
- Produces: one current interpretation of weight as both assignment cost and performance capacity.

- [ ] **Step 1: Supersede the pure-disadvantage rule**

Replace current statements equivalent to:

```text
높은 중량 자체를 품질·희귀도·공격력으로 취급하지 않는다
중량화에는 자동 보상을 붙이지 않는다
```

with:

```text
높은 최종 중량은 5포인트당 성능 예산 +1을 제공한다
한 예산점은 한 호환 성능 축에만 배분한다
중량은 모든 능력치를 동시에 올리지 않는다
```

Preserve the binary load gate and no-overload-penalty rule.

- [ ] **Step 2: Assign ownership to precision enhancement**

State that `LIGHTWEIGHT / NONE / WEIGHTED` is a structural precision-enhancement method and not a catalyst-affix family.

- [ ] **Step 3: Add rework and anti-farming guards**

State that structural treatment replacement recalculates the derived budget and cannot create cumulative gains.

- [ ] **Step 4: Add player preview requirements**

The precision-enhancement preview must show:

```text
final weight
weight budget before and after
lane allocation before and after
customers newly eligible or no longer eligible
exact displayed-stat changes
```

- [ ] **Step 5: Keep enhancement dominant**

State that weight budget affects item stats and specific requirements only; it does not directly add to generic event success.

---

### Task 4: Update validators and historical batch assertions

**Files:**
- Modify: `tests/test_base_v942_planning_first_adoption.py`
- Modify: `tests/test_r2_artistry_generation_growth_economy.py`
- Modify: `tests/test_r2_customer_equipment_compatibility.py`
- Modify: `tests/test_r2_mobile_customer_card_progressive_disclosure.py`
- Modify: `tests/test_r2_enhancement_dominant_simple_load_gate.py`
- Modify: `tests/test_r2_equipment_base_weight_points.py`
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: current authority text and registry.
- Produces: validators that recognize 6/10 as current while preserving older Decision-local approval counters.

- [ ] **Step 1: Update active-batch assertions**

Current-state assertions must require:

```text
R2_BATCH_005_ACTIVE_6_OF_10
R2_BATCH_005_6_OF_10
현재 승인 카운터: `6/10`
```

Decision-local status strings such as `R2_BATCH_005_5_OF_10` remain valid history inside the prior Decision records.

- [ ] **Step 2: Add the new canon to audits**

Require the Decision ID, formulas, treatment owner, lane list, and blocked product state.

- [ ] **Step 3: Detect stale active interpretation**

Reject active entry points that still say weighted treatment has no compensation or that high weight has no performance meaning.

- [ ] **Step 4: Run focused GREEN tests**

Run the six prior focused modules plus the new module and project-core alignment. Expected: all pass with zero failures.

---

### Task 5: Full verification and evidence synchronization

**Files:**
- Modify after verification: `docs/superpowers/plans/2026-08-06-weight-performance-budget-and-lightweight-tradeoff.md`
- Modify after verification: PR #109 body
- Modify after verification: Google Sheet authority rows

**Interfaces:**
- Consumes: final exact branch head and observed CI evidence.
- Produces: synchronized GitHub and Sheet authority evidence for Decision `BS-ITEM-20260806-02`.

- [ ] **Step 1: Run exact-head validation**

Require successful results for:

```text
Planning-first
Base adoption
PR validation
Python full contracts
project operating audit
Godot 4.7.1 import and parse
scene smoke
Godot model and integration suites
```

- [ ] **Step 2: Verify protected paths**

Compare the PR base against the final head and assert no changes under runtime, scenes, assets, images, or `data/crafting/weapon_bases.json`.

- [ ] **Step 3: Verify review state**

Require PR comments `0` and unresolved inline review threads `0`, unless new actionable feedback exists and is addressed first.

- [ ] **Step 4: Synchronize Google Sheet**

Write the same Decision ID, batch `6/10`, exact head, formulas, budget lanes, treatment ownership, validation evidence, Draft/unmerged state, and product block to:

```text
00_프로젝트_허브!H2:J2
02_현재_확정결정 next empty row
04_누락_충돌_감사 next empty row
05_GDD_요약 next empty row
40_핵심시스템_메인콘텐츠 next empty row
99_변경이력 next empty row
```

- [ ] **Step 5: Read back every written range**

Confirm all six locations contain `BS-ITEM-20260806-02`, `R2_BATCH_005_6_OF_10`, and the same exact head.

- [ ] **Step 6: Update PR #109 without merging**

Keep the PR `OPEN / DRAFT / UNMERGED` and record the final rules, RED/GREEN evidence, protected-path result, Sheet ranges, and remaining `NOT_RUN` balance playtest.
