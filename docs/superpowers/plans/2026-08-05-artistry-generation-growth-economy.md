# Artistry Generation, Growth, and Valuation Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `BS-CRAFT-20260805-02` into `R2_BATCH_005 / 1/10` as the authoritative contract for artistry creation sources, post-craft growth sources, valuation diminishing returns, customer interest roles, and anti-exploit boundaries without implementing product code or exact balance values.

**Architecture:** Keep `artistry` as the persisted non-negative integer item stat established by `BS-CRAFT-20260805-01`. Add only responsibility boundaries: source-tagged changes, context-derived `artistry_value` and `customer_artistry_fit`, additive one-time value ownership, and data-driven diminishing-return tables whose exact values remain test presets. Current decisions, machine Registry, Game Bible, hub routers, validators, PR evidence, and Google Sheet must read the same Decision ID and batch counter.

**Tech Stack:** Markdown canon, JSON Registry schema 8, Python contract validators, GitHub Actions, Godot 4.7.1 headless regression suite, Google Sheets same-ID readback.

## Global Constraints

- Decision ID is exactly `BS-CRAFT-20260805-02`.
- Approved batch state is exactly `R2_BATCH_005_ACTIVE_1_OF_10`; maximum batch size remains 10.
- Product implementation remains `BLOCKED`; protected product paths remain unchanged.
- `artistry` remains `NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM` and is displayed as an integer without denominator or named tier.
- Exact initial distributions, marginal-value bands, coefficients, customer thresholds, costs, success rates, damage/restoration formulas, storage type, and overflow guards remain `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.
- TDD evidence must show an observed RED before GREEN.
- Benchmark output must preserve `ADOPT / ADAPT / REJECT / DIFFERENTIATION / REMAINING_UNCERTAINTY`.

---

### Task 1: Add the failing Batch 005 contract

**Files:**
- Modify: `tests/test_base_v942_planning_first_adoption.py`
- Create: `tests/test_r2_artistry_generation_growth_economy.py`

**Interfaces:**
- Consumes: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`, `CURRENT_CONFIRMED_DECISIONS.md`, approved design spec.
- Produces: machine-readable requirements for `BS-CRAFT-20260805-02` and `R2_BATCH_005 / 1/10`.

- [ ] **Step 1: Write the failing Planning-first assertions**

Require the Registry to contain:

```python
assert registry["stage_status"] == "R2_BATCH_005_ACTIVE_1_OF_10"
assert registry["next_approval_counter"] == "1/10"
assert registry["active_batch"]["decisions"] == ["BS-CRAFT-20260805-02"]
contract = decisions["BS-CRAFT-20260805-02"]["contract"]
assert contract["persisted_stat"] == "ARTISTRY"
assert contract["initial_sources"] == [
    "BASE_ITEM_DESIGN_AESTHETIC_TENDENCY",
    "MATERIAL_VISUAL_PROCESSING_FIT",
    "DIRECT_FORGING_AESTHETIC_RESULT",
]
assert contract["allowed_post_craft_growth_sources"] == [
    "ARTISTIC_FINISH",
    "ARTISTRY_OWNED_CATALYST_EFFECT",
    "APPROVED_FINISHING_OR_DECORATION_CONTENT",
    "MEANINGFUL_ARTISTIC_REWORK",
]
assert contract["valuation_model"] == "ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE"
assert contract["customer_interest_roles"] == ["IGNORE", "SECONDARY", "PRIMARY", "REQUIREMENT"]
assert contract["exact_values"] == "BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED"
```

- [ ] **Step 2: Add the focused contract test**

Test that automatic growth sources are forbidden, value components are counted once, repair/exhibition/appraisal loops cannot create artistry, and product implementation stays blocked.

- [ ] **Step 3: Run CI to verify RED**

Push the test-only commit to PR #109.

Expected:

```text
Planning-first: FAIL because Registry is still R2_BATCH_005_ACTIVE_0_OF_10 and BS-CRAFT-20260805-02 is absent
Base adoption: PASS
```

- [ ] **Step 4: Record RED evidence**

Record the exact commit and workflow run number in the PR body; do not claim focused standalone PASS unless directly run.

---

### Task 2: Promote the approved design into authoritative canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md`

**Interfaces:**
- Consumes: approved spec `docs/superpowers/specs/2026-08-05-artistry-generation-growth-economy-design.md`.
- Produces: one authoritative current contract and Registry entry for `BS-CRAFT-20260805-02`.

- [ ] **Step 1: Create the focused canon**

The canon must define:

```text
artistry = persisted item stat
artistry_value = context-derived market/appraisal result, not persisted as a new permanent stat
customer_artistry_fit = context-derived customer/schedule fit, not persisted as a new permanent stat
```

Initial sources:

```text
BASE_ITEM_DESIGN_AESTHETIC_TENDENCY
MATERIAL_VISUAL_PROCESSING_FIT
DIRECT_FORGING_AESTHETIC_RESULT
```

Allowed post-craft growth sources:

```text
ARTISTIC_FINISH
ARTISTRY_OWNED_CATALYST_EFFECT
APPROVED_FINISHING_OR_DECORATION_CONTENT
MEANINGFUL_ARTISTIC_REWORK
```

Automatic growth forbidden from general enhancement level, sale, gift, exhibition count, appraisal count, ownership transfer, fame, chronicle event, and low-cost repetition.

- [ ] **Step 2: Define valuation ownership**

Use additive one-time components:

```text
final_value
= functional_value
+ crafting_grade_value
+ diminishing_artistry_value
+ catalyst_affix_value
+ chronicle_value
+ customer_or_market_demand_adjustment
```

Require monotonic but diminishing artistry marginal value, with piecewise data tables preferred over a hard-coded logarithm or square-root formula.

- [ ] **Step 3: Define customer interest roles**

```text
IGNORE / SECONDARY / PRIMARY / REQUIREMENT
```

High artistry must not create a penalty for uninterested customers; it may exceed their willingness to pay without improving fit.

- [ ] **Step 4: Define anti-exploit and provenance rules**

Every artistry change must record source category and item UID context. Forbid repair, damage, sale, exhibition, appraisal, gift, and repeated low-cost loops from producing net artistry. A catalyst event cannot both add the same artistry and multiply that same contribution again through price or affix valuation.

- [ ] **Step 5: Update current authorities**

Advance the active batch from `0/10` to `1/10`; preserve checkpoint 004 immutable evidence and all existing Decision contracts.

- [ ] **Step 6: Commit minimal GREEN canon**

Use a commit message such as:

```bash
git commit -m "canon: approve artistry generation growth and valuation boundaries"
```

---

### Task 3: Align cold-start routers and governance

**Files:**
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`
- Modify: `docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md`

**Interfaces:**
- Consumes: focused canon and Registry entry.
- Produces: deterministic routing to the new current canon and `R2_BATCH_005 / 1/10` state.

- [ ] **Step 1: Update current session and roadmap**

Set current Decision to `BS-CRAFT-20260805-02`, counter `1/10`, and next candidate to exact artistry balance presets or the next approved design topic. Keep product implementation blocked.

- [ ] **Step 2: Add gates**

Add an `Artistry Generation·Growth·Valuation Gate` requiring allowed sources, forbidden automatic sources, additive ownership, piecewise diminishing value, customer roles, anti-loop protection, and exact values remaining test presets.

- [ ] **Step 3: Route documents**

Register the approved spec, implementation plan, and focused canon. Mark the design spec as approved input and the focused canon as current authority.

- [ ] **Step 4: Extend benchmark record**

Preserve the benchmark conclusions and state explicitly that item quality/decoration separation and source-specific anti-repeat restrictions are adopted or adapted, while multiplicative total-value stacking and invisible global diminishing returns are rejected.

---

### Task 4: Make validators GREEN and refactor stale assertions

**Files:**
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`
- Modify: `tests/test_r2_artistry_generation_growth_economy.py`

**Interfaces:**
- Consumes: final canon and Registry schema.
- Produces: full automated validation of the new contract without weakening historical implementation regressions.

- [ ] **Step 1: Update core alignment assertions**

Require Decision `BS-CRAFT-20260805-02`, `R2_BATCH_005_ACTIVE_1_OF_10`, focused canon routing, and protected product implementation state.

- [ ] **Step 2: Update operating audit assertions**

Preserve Base skill mapping, broken-reference scan, legacy status checks, PR #81 rejection, runtime path checks, and historical forging/enhancement regressions. Replace only current batch and artistry responsibility assertions.

- [ ] **Step 3: Run complete GREEN validation**

Required results on one exact HEAD:

```text
Planning-first: PASS
Validate Base v9 adoption: PASS
PR validation Python full contracts: PASS
Godot 4.7.1 headless: PASS
```

- [ ] **Step 4: Refactor only after GREEN**

Remove duplicated prose or stale `0/10` active-state assertions. Do not change product code, data, scenes, assets, addons, or `project.godot`.

---

### Task 5: Synchronize evidence and leave the Draft PR unmerged

**Files:**
- Modify: PR #109 description
- Modify: Google Sheet ranges already used by current Blacksmith governance

**Interfaces:**
- Consumes: final exact HEAD and workflow runs.
- Produces: same-ID GitHub and Sheet readback for `BS-CRAFT-20260805-02`.

- [ ] **Step 1: Check changed-file boundary and review state**

Verify protected product path count is zero, PR comments are zero or resolved, and inline review threads are zero or resolved.

- [ ] **Step 2: Write Sheet evidence**

Update:

```text
00_프로젝트_허브!H2:J2
02_현재_확정결정
04_누락_충돌_감사
05_GDD_요약
99_변경이력
```

Use the same Decision ID, exact HEAD, batch `1/10`, CI evidence, and `PRODUCT_BLOCKED` status.

- [ ] **Step 3: Read back Sheet values**

Read the exact updated bounded ranges and verify all five locations agree.

- [ ] **Step 4: Update PR #109 body**

Record benchmark decisions, RED commit/run, GREEN exact HEAD/runs, changed files, protected path count, comments/threads, Sheet ranges, and all `NOT_RUN` boundaries.

- [ ] **Step 5: Preserve approval boundary**

Keep PR #109 `OPEN / DRAFT / UNMERGED`. It is the first approved Decision in Batch 005 and must not be merged without explicit user approval or a later approved checkpoint.
