# Weight Performance Budget and Lightweight Trade-off Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give heavier equipment a larger initial performance budget while allowing rare precision-enhancement lightweighting to lower current use weight without deleting previously earned performance.

**Architecture:** Add Decision `BS-ITEM-20260806-02` as a refinement of the fixed-weight and binary-load contracts. The item UID stores `CURRENT_WEIGHT` separately from monotonic `BUDGET_RECOGNIZED_WEIGHT`; customer load uses current weight, while performance budget uses the highest successfully reached weight. Lightweighting and weighting are precision-enhancement method choices available only at `+10/+20/+30/+40/+50`, so repeated adjustment consumes scarce milestone opportunities.

**Tech Stack:** Markdown planning canon, JSON authority registries, Python unittest contracts, GitHub Actions, Google Sheets authority mirror.

## Global Constraints

- Decision ID: `BS-ITEM-20260806-02`.
- Active batch: `R2_BATCH_005_6_OF_10`.
- `INITIAL_WEIGHT = equipment-group base weight at first crafting completion`.
- `CURRENT_WEIGHT = max(0, INITIAL_WEIGHT + cumulative successful precision weight adjustments)`.
- `BUDGET_RECOGNIZED_WEIGHT = max(INITIAL_WEIGHT, highest successful CURRENT_WEIGHT ever reached by the UID)`.
- `WEIGHT_PERFORMANCE_BUDGET = BUDGET_RECOGNIZED_WEIGHT / 5`.
- Each `5 WEIGHT_POINT` contributes exactly `+1 PERFORMANCE_BUDGET_POINT`.
- Initial crafting weight grants initial budget.
- Lightweighting lowers current weight by 5 and never lowers recognized weight or existing budget.
- Weighting raises current weight by 5 and grants budget only for weight above the previous recognized peak.
- Budget lanes: `ATTACK_BUDGET / DEFENSE_BUDGET / MAGIC_FUNCTION_BUDGET / UTILITY_BUDGET`.
- One budget point is allocated to one compatible lane only.
- Customer load uses `CURRENT_WEIGHT`, not `BUDGET_RECOGNIZED_WEIGHT`.
- Weight adjustment belongs to the precision-enhancement method, not `CATALYST_AFFIX`.
- Precision milestones are exactly `[10, 20, 30, 40, 50]`.
- At most one weight adjustment can be selected per milestone.
- Adjustments can accumulate across distinct milestones.
- The same milestone cannot be replayed, refunded, or repeatedly switched.
- Accessories receive no weight-derived budget or precision weight adjustment by default.
- Weight budget is not multiplied by material, grade, artistry, catalyst, chronicle, or enhancement.
- Weight budget does not directly change generic customer event success.
- Runtime, scenes, assets, images, and `data/crafting/weapon_bases.json` remain unchanged.
- Product implementation remains `BLOCKED`.

---

### Task 1: Correct the RED planning contract

**Files:**
- Modify: `tests/test_r2_weight_performance_budget_and_lightweight_tradeoff.py`
- Existing CI entry: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: RED commit `e82057b1c966294913c716b2f7849fab1d40ba5d`, Planning-first run `204`, and the revised approved design.
- Produces: a failing contract requiring monotonic budget memory, preserved budget after lightweighting, peak-only gain after weighting, and precision-milestone opportunity cost.

- [ ] **Step 1: Replace the rejected current-weight assertions**

Require:

```python
self.assertEqual("PEAK_RECOGNIZED_WEIGHT_MONOTONIC_SINGLE_SOURCE", contract["weight_performance_budget_model"])
self.assertEqual(
    "MAX_INITIAL_OR_HIGHEST_SUCCESSFUL_CURRENT_WEIGHT_DIVIDED_BY_5",
    contract["weight_performance_budget_formula"],
)
self.assertTrue(contract["initial_weight_grants_initial_budget"])
self.assertTrue(contract["lightweighting_preserves_existing_budget"])
self.assertTrue(contract["budget_recognized_weight_is_monotonic"])
self.assertTrue(contract["current_weight_drives_customer_load_gate"])
self.assertTrue(contract["weighting_grants_budget_only_above_previous_peak"])
```

- [ ] **Step 2: Require precision opportunity-cost rules**

```python
self.assertEqual([10, 20, 30, 40, 50], contract["precision_milestones"])
self.assertEqual(1, contract["maximum_weight_adjustments_per_precision_milestone"])
self.assertTrue(contract["weight_adjustments_accumulate_across_distinct_milestones"])
self.assertFalse(contract["same_milestone_weight_adjustment_replay_allowed"])
self.assertFalse(contract["used_precision_milestone_refund_allowed"])
```

- [ ] **Step 3: Require exact player-facing tokens**

```text
최초 제작 중량 5당 초기 성능 예산 +1
경량화 -5 중량 / 기존 예산 유지
중량화 +5 중량 / 과거 최고 인정 중량 초과분만 예산 추가
정밀강화 +10 / +20 / +30 / +40 / +50
```

- [ ] **Step 4: Run Planning-first and verify revised RED**

Expected: the seven new tests still fail because Decision `BS-ITEM-20260806-02`, active batch 6/10, canon, and contract are absent. Existing prior tests remain green.

---

### Task 2: GREEN machine-readable canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: revised RED contract.
- Produces: Decision `BS-ITEM-20260806-02` and one machine-readable budget-memory contract.

- [ ] **Step 1: Write the focused canon**

Include:

```text
INITIAL_WEIGHT = 장비군 기본 중량
CURRENT_WEIGHT = max(0, INITIAL_WEIGHT + 누적 정밀강화 중량 조정)
BUDGET_RECOGNIZED_WEIGHT = max(INITIAL_WEIGHT, UID가 성공적으로 달성한 역대 최고 CURRENT_WEIGHT)
WEIGHT_PERFORMANCE_BUDGET = BUDGET_RECOGNIZED_WEIGHT / 5
```

- [ ] **Step 2: Store the exact contract**

```json
{
  "weight_performance_budget_model": "PEAK_RECOGNIZED_WEIGHT_MONOTONIC_SINGLE_SOURCE",
  "weight_performance_budget_formula": "MAX_INITIAL_OR_HIGHEST_SUCCESSFUL_CURRENT_WEIGHT_DIVIDED_BY_5",
  "weight_points_per_budget_point": 5,
  "initial_weight_grants_initial_budget": true,
  "lightweighting_preserves_existing_budget": true,
  "budget_recognized_weight_is_monotonic": true,
  "current_weight_drives_customer_load_gate": true,
  "weighting_grants_budget_only_above_previous_peak": true,
  "weight_adjustment_owner": "PRECISION_ENHANCEMENT_METHOD",
  "weight_delta_by_operation": {
    "LIGHTWEIGHTING": -5,
    "WEIGHTING": 5
  },
  "precision_milestones": [10, 20, 30, 40, 50],
  "maximum_weight_adjustments_per_precision_milestone": 1,
  "weight_adjustments_accumulate_across_distinct_milestones": true,
  "same_milestone_weight_adjustment_replay_allowed": false,
  "used_precision_milestone_refund_allowed": false,
  "budget_lanes": [
    "ATTACK_BUDGET",
    "DEFENSE_BUDGET",
    "MAGIC_FUNCTION_BUDGET",
    "UTILITY_BUDGET"
  ],
  "budget_point_allocates_to_exactly_one_lane": true,
  "accessory_weight_budget_enabled_by_default": false,
  "weight_budget_directly_changes_generic_success_rate": false,
  "weight_budget_multiplied_by_other_progression_axes": false,
  "exact_stat_conversion": "BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
  "product_implementation": "BLOCKED"
}
```

- [ ] **Step 3: Advance only the active batch**

Set current active state to `R2_BATCH_005_ACTIVE_6_OF_10` and append the new Decision while preserving historical 1/10–5/10 status strings.

- [ ] **Step 4: Register canon, spec, and plan**

Add the three documents as current authority for `BS-ITEM-20260806-02`.

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
- Consumes: registry contract.
- Produces: one current interpretation of weight memory, customer eligibility, and milestone opportunity cost.

- [ ] **Step 1: Supersede pure-disadvantage language**

Replace active statements that high weight has no performance meaning with:

```text
최초 제작 중량 5당 초기 성능 예산 +1
한 예산점은 한 호환 성능 축에만 배분
중량은 모든 능력치를 동시에 올리지 않음
```

- [ ] **Step 2: Preserve performance through lightweighting**

State explicitly that lightweighting reduces `CURRENT_WEIGHT` but never reduces `BUDGET_RECOGNIZED_WEIGHT`, existing budget, or already allocated stats.

- [ ] **Step 3: Add peak-only weighting gain**

State that weighting grants new budget only when the new current weight exceeds the UID's previous recognized peak.

- [ ] **Step 4: Replace one-active-modifier language**

Refine prior `maximum one modifier per item` wording into:

```text
one weight adjustment per distinct precision milestone
adjustments accumulate across milestones
same milestone replay/refund forbidden
```

- [ ] **Step 5: Add preview requirements**

Show before execution:

```text
current weight before/after
recognized budget weight
weight budget and newly gained budget
lane allocation changes only when new budget is gained
customers newly eligible or no longer eligible
```

- [ ] **Step 6: Preserve binary load and enhancement dominance**

No overload speed, fatigue, accuracy, or evasion penalties. Weight budget affects item stats only and never directly adds to the generic success forecast.

---

### Task 4: Update validators

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
- Produces: validators recognizing 6/10 while retaining Decision-local historical counters.

- [ ] **Step 1: Update only active-state assertions**

Require `R2_BATCH_005_ACTIVE_6_OF_10`, `R2_BATCH_005_6_OF_10`, and `현재 승인 카운터: 6/10` in current entry points.

- [ ] **Step 2: Require the new budget-memory contract**

Validate initial budget, lightweight preservation, monotonic recognized weight, peak-only gain, exact milestone list, and no same-milestone replay/refund.

- [ ] **Step 3: Detect stale active interpretation**

Reject active text that says lightweighting removes budget, weighting always grants budget, or weight adjustments are available outside precision milestones.

- [ ] **Step 4: Run focused GREEN tests**

Run all seven focused modules plus project-core alignment. Expected: all pass.

---

### Task 5: Full verification and evidence synchronization

**Files:**
- Modify after verification: this plan
- Modify after verification: PR #109 body
- Modify after verification: Google Sheet authority rows

**Interfaces:**
- Consumes: final exact branch head and observed CI evidence.
- Produces: synchronized GitHub and Sheet authority evidence.

- [ ] **Step 1: Run exact-head validation**

Require successful Planning-first, Base adoption, PR validation, Python full contracts, operating audit, Godot 4.7.1 import/parse, scene smoke, and Godot model/integration suites.

- [ ] **Step 2: Verify protected paths**

Assert no runtime, scene, asset, image, or `data/crafting/weapon_bases.json` changes.

- [ ] **Step 3: Verify review state**

Require no actionable PR comments or unresolved review threads.

- [ ] **Step 4: Synchronize and read back Google Sheet**

Write the same Decision ID, 6/10 batch, exact head, formulas, opportunity-cost rules, validation evidence, Draft/unmerged status, and product block to the hub and next empty rows of the decision, audit, GDD, core-system, and history tabs. Read all six ranges back.

- [ ] **Step 5: Update PR #109 without merging**

Keep `OPEN / DRAFT / UNMERGED`; record the final rules, corrected RED/GREEN evidence, protected-path result, Sheet ranges, and `NOT_RUN` balance playtest.
