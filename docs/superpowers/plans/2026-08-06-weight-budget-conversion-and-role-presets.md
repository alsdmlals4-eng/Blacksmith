# Weight Budget Conversion and Role Presets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Canonize exact weight-budget point conversion and automatic immutable equipment-role presets without changing product runtime data.

**Architecture:** Add Decision `BS-ITEM-20260806-03` as a refinement of the monotonic weight-budget contract. One base-item role profile selects one lane at first crafting, every budget point converts through an exact table, and later weighting follows the same profile while lightweighting preserves allocated output.

**Tech Stack:** Markdown planning canon, compact JSON authority registry, Python unittest contracts, GitHub Actions, Google Sheets authority mirror.

## Global Constraints

- Decision ID: `BS-ITEM-20260806-03`.
- Active batch: `R2_BATCH_005_7_OF_10`.
- `1 ATTACK_BUDGET = ATTACK +5`.
- `1 DEFENSE_BUDGET = DEFENSE +5`.
- `1 MAGIC_FUNCTION_BUDGET = MAGIC_FUNCTION_CAPACITY +1`.
- `1 UTILITY_BUDGET = UTILITY_CAPACITY +1`.
- The base item definition selects one immutable role profile at first crafting completion.
- Player free allocation and post-craft free reallocation are forbidden.
- New peak-weight budget follows the existing profile.
- Lightweighting preserves allocated output.
- Generic event-success calculation does not consume attack, defense, magic capacity, or utility capacity automatically.
- `data/crafting/weapon_bases.json`, runtime, scenes, assets, and images remain unchanged.
- Product implementation remains `BLOCKED`.

---

### Task 1: Observe the RED contract

**Files:**
- Create: `tests/test_r2_weight_budget_conversion_and_role_presets.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: `CURRENT_R2_CANON_REGISTRY.json` and the existing weight-budget Decision.
- Produces: eight failing assertions for the missing conversion Decision.

- [ ] **Step 1: Add exact contract assertions**

Assert batch 7/10, the four conversion entries, immutable automatic profiles, default equipment mapping, function-capacity costs, weighting/lightweighting rules, authority documents, and unchanged product data.

- [ ] **Step 2: Run the focused suite**

```bash
python -m unittest \
  tests.test_base_v942_planning_first_adoption \
  tests.test_r2_artistry_generation_growth_economy \
  tests.test_r2_customer_equipment_compatibility \
  tests.test_r2_mobile_customer_card_progressive_disclosure \
  tests.test_r2_enhancement_dominant_simple_load_gate \
  tests.test_r2_equipment_base_weight_points \
  tests.test_r2_weight_performance_budget_and_lightweight_tradeoff \
  tests.test_r2_weight_budget_conversion_and_role_presets -v
```

Expected: the existing 48 tests pass and the new eight tests fail because Decision `BS-ITEM-20260806-03` and its authority documents do not exist.

- [ ] **Step 3: Record RED evidence**

Record commit `447031d98aefcfa10abb0ead7b85df745db4b0c0`, Planning-first run `221`, `56 tests`, and `8 expected failures`.

### Task 2: Add the authority contract

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md`
- Create: `docs/superpowers/specs/2026-08-06-weight-budget-conversion-and-role-presets-design.md`
- Create: `docs/superpowers/plans/2026-08-06-weight-budget-conversion-and-role-presets.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: monotonic `BUDGET_RECOGNIZED_WEIGHT / 5`.
- Produces: `ROLE_PRESET_AUTOMATIC_SINGLE_LANE` and exact conversion/profile tables.

- [ ] **Step 1: Register Decision 7/10**

Set stage status to `R2_BATCH_005_ACTIVE_7_OF_10`, counter to `7/10`, append `BS-ITEM-20260806-03`, and preserve compact JSON serialization required by the operating audit.

- [ ] **Step 2: Add exact conversion**

Store the four conversion entries, profile mapping, baseline examples, function-capacity costs, and all anti-double-counting flags.

- [ ] **Step 3: Register the three authority documents**

Add canon, design, and plan records to the design-document registry.

### Task 3: Synchronize current authority entrypoints

**Files:**
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: Decision 7/10.
- Produces: current routing and next-gate descriptions.

- [ ] **Step 1: Advance all active counters**

Change only active batch state to 7/10. Preserve historical Decision-specific batch markers.

- [ ] **Step 2: Add the conversion summary**

Record exact point conversion, automatic profile selection, no free reallocation, and product implementation blocked.

- [ ] **Step 3: Set the next gate**

The next planning gate is content-specific attack/defense composition and the first approved magic/utility function catalog, not another weight formula.

### Task 4: Refine dependent canons

**Files:**
- Modify: `docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`

**Interfaces:**
- Consumes: exact conversion and profile rules.
- Produces: one-way refinement markers without rewriting historical approvals.

- [ ] **Step 1: Add `REFINED_BY_BS-ITEM-20260806-03` blocks**

State that point conversion is now exact, profile selection is immutable, and generic success remains unchanged.

- [ ] **Step 2: Add preview rules**

Show `weight +5 / attack +5`, `weight +5 / defense +5`, or one function capacity. Lightweighting shows weight reduction with output retained.

### Task 5: Update validators and make GREEN

**Files:**
- Modify: `tests/test_base_v942_planning_first_adoption.py`
- Modify: existing R2 batch contract tests
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: all synchronized authority documents.
- Produces: focused, core-alignment, and operating-audit PASS.

- [ ] **Step 1: Advance active-batch assertions to seven**

Append the new Decision to every active-batch list while leaving earlier Decision status markers unchanged.

- [ ] **Step 2: Register the new canon in validators**

Require the exact four conversion lines, Decision ID, 7/10 marker, automatic profile model, and blocked product status.

- [ ] **Step 3: Run focused contracts**

Run the Task 1 command. Expected: `56 tests`, all PASS.

- [ ] **Step 4: Run project core alignment**

```bash
python tests/check_project_core_alignment.py
```

Expected: PASS.

- [ ] **Step 5: Run operating audit**

```bash
python tools/run_project_operating_system_audit.py \
  --base-root base-src \
  --report /tmp/blacksmith-base-adoption-report.json
```

Expected: zero errors and zero warnings.

### Task 6: Final verification and synchronization

**Files:**
- Modify: PR #109 description
- Modify: Google Sheet authority rows

**Interfaces:**
- Consumes: exact final head and green CI.
- Produces: matching GitHub and Sheet evidence.

- [ ] **Step 1: Run full CI on the exact head**

Require Planning-first, Base adoption, PR validation, Python operating audit, and Godot 4.7.1 suites to pass.

- [ ] **Step 2: Verify protected paths**

Confirm zero changes under `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, and `project.godot`; confirm `weapon_bases.json` unchanged.

- [ ] **Step 3: Sync the Sheet**

Write the same Decision ID, 7/10 state, exact head, CI evidence, Draft/unmerged state, and product-blocked status to the next empty rows of the authority tabs.

- [ ] **Step 4: Preserve the Draft boundary**

Do not merge PR #109 without explicit user merge approval.
