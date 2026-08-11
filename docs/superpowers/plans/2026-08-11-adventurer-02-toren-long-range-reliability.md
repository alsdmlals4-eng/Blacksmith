# ADVENTURER_02 Toren Long-Range Reliability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote the user-approved `BS-CONTENT-20260811-02 / ADVENTURER_02 / TOREN_MARCH` planning design to current R3–R7 canon, synchronize the same Decision ID to Google Sheet, and prove the change without opening product implementation.

**Architecture:** This is a planning-only delivery. A focused Python contract first defines the required Toren decision and protection boundaries; the canon document, R3–R7 registry, current routers, and operating-health evidence then satisfy that contract. Google Sheet consumes the same Decision ID after GitHub exact-head validation, and merge is allowed only after current-main/review/CI readback.

**Tech Stack:** Markdown, JSON, Python `unittest`, GitHub Actions, Google Sheets API, Godot 4.7.1 headless as unchanged regression surface.

## Global Constraints

- `PRODUCT_IMPLEMENTATION: BLOCKED`
- `TASK3_IMPLEMENTATION: NOT_APPROVED`
- `R3_R7_APPROVAL_COUNTER: 2/10`
- Decision ID: `BS-CONTENT-20260811-02`
- Content ID: `ADVENTURER_02`
- Customer ID: `TOREN_MARCH`
- Content goal: `JOURNEY_CONTINUITY_AND_RELIABILITY`
- Player remains `BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_TRAVEL_CONTROLLER`.
- No direct travel, map-route, combat, or survival minigame.
- No new raw stats for reliability, portability, or repairability.
- Consume existing `WEIGHT`, `DURABILITY`, enhancement, `ENVIRONMENTAL_SEALING`, `FIELD_SERVICEABILITY`, and only actually relevant approved functions.
- `OVERWEIGHT` remains assignment-blocking before success forecast.
- Enhancement remains the primary general-event success owner.
- No universal fixed day count.
- No routine automatic wear tax; wear/damage requires a causal event/exposure.
- Same item UID lifecycle is preserved.
- Routine completion does not auto-grant chronicle affix or artistry growth.
- Exact duration, probabilities, wear amounts, repair amounts, rewards, and costs remain `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.
- Human playtest, Android device, and accessibility execution remain `NOT_RUN`.
- PR #81 remains `REFERENCE_ONLY_DO_NOT_MERGE`.

---

### Task 1: Lock the Toren planning contract with RED

**Files:**
- Create: `tests/test_r3_adventurer_02_toren_content.py`
- Read: `tests/test_r3_adventurer_01_nadia_content.py`
- Read: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`

**Interfaces:**
- Consumes: current R3 registry schema and stable hub entrypoints.
- Produces: failing assertions that define the complete `BS-CONTENT-20260811-02` planning contract.

- [ ] **Step 1: Write the failing test**

The test must assert all of the following exact contract tokens before implementation:

```python
self.assertEqual("2/10", registry.get("next_approval_counter"))
self.assertIn("BS-CONTENT-20260811-02", decisions)
self.assertEqual("ADVENTURER_02", contract.get("content_id"))
self.assertEqual("TOREN_MARCH", contract.get("customer_id"))
self.assertEqual("JOURNEY_CONTINUITY_AND_RELIABILITY", contract.get("content_goal"))
self.assertFalse(contract.get("direct_travel_or_route_minigame"))
self.assertFalse(contract.get("new_reliability_or_repairability_raw_stat"))
self.assertFalse(contract.get("routine_automatic_wear_tax"))
self.assertEqual(
    ["JOURNEY_ARRIVAL_STATE", "ROUTE_EXPOSURE_STATE", "ITEM_UID_LIFECYCLE_STATE"],
    contract.get("result_axes"),
)
self.assertEqual("NON_CANONICAL_BASELINE_TEST_FIXTURE", contract.get("test_fixture_status"))
self.assertEqual("OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL", contract.get("playtest_evidence"))
```

The canon token assertions must include:

```python
for token in (
    "BS-CONTENT-20260811-02",
    "ADVENTURER_02",
    "TOREN_MARCH",
    "JOURNEY_CONTINUITY_AND_RELIABILITY",
    "ENVIRONMENTAL_SEALING",
    "FIELD_SERVICEABILITY",
    "FIELD_MAINTAINED_UID_PRESERVED",
    "직접 이동·지도 경로 선택·실시간 생존 조작을 요구하지 않는다",
    "자동 매일 내구도 감소 금지",
    "OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL",
):
    self.assertIn(token, canon)
```

Stable entrypoint assertions must require `R3_R7_APPROVAL_COUNTER: 2/10`, `R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-02`, `PRODUCT_IMPLEMENTATION: BLOCKED`, and `TASK3_IMPLEMENTATION: NOT_APPROVED` in current routing docs.

- [ ] **Step 2: Run the focused contract to verify RED**

Run:

```bash
python -m unittest tests.test_r3_adventurer_02_toren_content -v
```

Expected: FAIL only because the new Toren canon/registry/router state does not exist yet. Existing Nadia and R2 contracts are not modified in this step.

- [ ] **Step 3: Commit RED only**

```bash
git add tests/test_r3_adventurer_02_toren_content.py
git commit -m "test: define Toren adventurer 02 planning contract"
```

---

### Task 2: Materialize the approved Toren canon and current routers

**Files:**
- Create: `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `docs/PROJECT_OPERATING_HEALTH.json`
- Test: `tests/test_r3_adventurer_02_toren_content.py`

**Interfaces:**
- Consumes: approved design `docs/superpowers/specs/2026-08-11-adventurer-02-toren-long-range-reliability-design.md` and current R2/R3 contracts.
- Produces: current canon for Decision `BS-CONTENT-20260811-02` and current-router state `2/10`.

- [ ] **Step 1: Create the Toren canon from the approved design**

The canon must preserve these exact structural states:

```text
PREP_AND_DEPARTURE
→ EXPOSURE_AND_ROUTE_ADAPTATION
→ ARRIVAL_AND_ITEM_ASSESSMENT
```

and result axes:

```text
JOURNEY_ARRIVAL_STATE
ROUTE_EXPOSURE_STATE
ITEM_UID_LIFECYCLE_STATE
```

It must explicitly retain `UNIVERSAL_FIXED_DAY_COUNT: false`, `PRODUCT_IMPLEMENTATION: BLOCKED`, `TASK3_IMPLEMENTATION: NOT_APPROVED`, no direct travel controls, no new reliability/repairability raw stat, and no routine automatic wear tax.

- [ ] **Step 2: Add Decision 02 to the R3–R7 registry**

Keep Decision 01 unchanged. Set top-level counter to:

```json
"next_approval_counter": "2/10"
```

Add a second `current_decisions` entry with:

```json
{
  "id": "BS-CONTENT-20260811-02",
  "title": "모험가 02 토렌 마치 장거리 여정 지속성·신뢰성 콘텐츠",
  "status": "USER_APPROVED_R3_R7_2_OF_10",
  "canon": "docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md"
}
```

Its contract must include the exact values required by Task 1 and protected boundaries for no product implementation, no direct travel, no new raw stat, no routine wear tax, and same-UID preservation.

- [ ] **Step 3: Update current routing docs**

`CURRENT_CONFIRMED_DECISIONS.md` must gain one concise Decision 02 line without altering Decision 01.

`ACTIVE_CONTEXT.md`, `START_HERE.md`, and `ROADMAP.md` must set:

```yaml
R3_R7_APPROVAL_COUNTER: 2/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-02
R3_R7_RESUME_LOCATOR: ADVENTURER_02_TOREN_LONG_RANGE_RELIABILITY_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

They must retain Nadia as `1/10` completed history and point the next-read sequence to both R3 canon documents.

- [ ] **Step 4: Run focused GREEN**

```bash
python -m unittest tests.test_r3_adventurer_02_toren_content -v
```

Expected: PASS.

- [ ] **Step 5: Refresh the current-decisions operating-health digest**

Because `CURRENT_CONFIRMED_DECISIONS.md` changes, calculate:

```bash
python - <<'PY'
from pathlib import Path
import hashlib
p = Path('CURRENT_CONFIRMED_DECISIONS.md')
print(hashlib.sha256(p.read_bytes()).hexdigest())
PY
```

Replace only `docs/PROJECT_OPERATING_HEALTH.json -> evidence.operating[id=BS-CURRENT-DECISIONS].sha256` with that exact digest.

- [ ] **Step 6: Run the planning-first compatibility suite**

```bash
python -m unittest \
  tests.test_project_total_instruction_v45_r2_canon \
  tests.test_base_v942_planning_first_adoption \
  tests.test_project_adapter_long_lived_pr_baseline \
  tests.test_r3_adventurer_01_nadia_content \
  tests.test_r3_adventurer_02_toren_content -v
```

Expected: PASS with Nadia unchanged and Toren added as 2/10.

- [ ] **Step 7: Commit canon GREEN**

```bash
git add \
  CURRENT_CONFIRMED_DECISIONS.md \
  docs/PROJECT_OPERATING_HEALTH.json \
  docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json \
  docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md \
  '[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md' \
  '[기획서]/00_프로젝트_허브/START_HERE.md' \
  '[기획서]/00_프로젝트_허브/ROADMAP.md' \
  tests/test_r3_adventurer_02_toren_content.py
git commit -m "docs: canonize Toren adventurer 02 reliability content"
```

---

### Task 3: Adversarial review the Toren delta

**Files:**
- Review: all files changed by Tasks 1–2
- Modify only when a concrete regression is found.

**Interfaces:**
- Consumes: complete planning diff.
- Produces: `P0_0 / P1_0_AFTER_MITIGATION` or a new RED→GREEN regression fix.

- [ ] **Step 1: Check Nadia differentiation**

Reject the diff if Toren's goal or result axes collapse back to `SURVIVAL_AND_RECOVERY` / recovery-target gameplay.

- [ ] **Step 2: Check product-role drift**

Reject any direct map routing, travel movement, survival controls, combat, or player-controlled field repair.

- [ ] **Step 3: Check stat/function ownership**

Reject new `RELIABILITY`, `PORTABILITY`, or `REPAIRABILITY` raw stats. Reject `ENVIRONMENTAL_SEALING` or `FIELD_SERVICEABILITY` as unconditional general-success bonuses.

- [ ] **Step 4: Check maintenance-tax regression**

Reject automatic wear on every day or every routine completion. Wear/damage must be causally tied to exposure/event results.

- [ ] **Step 5: Check item lifecycle and routine-reward boundaries**

Require same UID through wear/field maintenance/damage/loss/recovery and forbid automatic chronicle-affix/artistry growth from routine completion.

- [ ] **Step 6: If any P1 is found, add a failing regression assertion first**

Run the focused test to observe RED, apply the smallest canon correction, then rerun to GREEN before continuing.

---

### Task 4: Validate exact PR head and merge the planning-only scope

**Files:**
- No additional product files.
- PR metadata records evidence.

**Interfaces:**
- Consumes: reviewed branch head.
- Produces: merged Blacksmith main containing Decision 02 planning canon.

- [ ] **Step 1: Confirm final changed-file inventory**

Expected scope is limited to the design/plan, one Toren contract test, one Toren canon, current registry/current routers, and operating-health digest. No `project.godot`, `.tscn`, runtime data, addons, scripts, images, or assets.

- [ ] **Step 2: Confirm exact-head CI**

Require all PR-triggered workflows to complete `SUCCESS`. In PR validation, require Python contracts and Godot 4.7.1 headless import/parse, scene smoke, HiGodot main-scene contract, and model/integration suites to remain green.

- [ ] **Step 3: Confirm review surface**

Require unresolved inline review threads = `0` and no requested changes.

- [ ] **Step 4: Re-read main before merge**

Main must still equal the PR base or the PR must be revalidated against the new main before merge.

- [ ] **Step 5: Merge with expected-head protection**

Use squash merge only after Steps 1–4 pass. Do not request a second merge approval because this is the already user-approved `BS-CONTENT-20260811-02` planning scope.

- [ ] **Step 6: Post-merge readback**

Re-read main, Toren canon, R3 registry, current decisions, Active Context, Start Here, and Roadmap. Confirm `2/10`, Decision 02 current, Decision 01 preserved, product blocked, Task3 not approved.

---

### Task 5: Synchronize Google Sheet with the same Decision ID

**Files / Sheet ranges:**
- Modify: `00_프로젝트_허브!E2:F2`
- Modify: `01_작업순서!D5:H5`
- Append or update: `02_현재_확정결정` with `BS-CONTENT-20260811-02`
- Append: `04_누락_충돌_감사` adversarial/validation row
- Update: `13_주요인물` Toren row authority/status
- Append: `50_메인콘텐츠` `ADVENTURER_02`
- Append: `60_UX_UI_접근성` same-Decision consumer mirror only if useful; never separate authority
- Append: `99_변경이력` with Decision 02 delivery evidence

**Interfaces:**
- Consumes: merged main SHA and exact-head validation evidence.
- Produces: Sheet consumer state synchronized to GitHub under `BS-CONTENT-20260811-02`.

- [ ] **Step 1: Write Decision 02 planning state**

Sheet must state `USER_APPROVED / R3_R7_2_OF_10 / PLANNING_ONLY`, merged main SHA, PR number/head evidence, `PRODUCT_IMPLEMENTATION_BLOCKED`, `TASK3_NOT_APPROVED`, `HUMAN_PLAYTEST_NOT_RUN`, and `ANDROID_DEVICE_NOT_RUN`.

- [ ] **Step 2: Update Toren and content rows**

Toren's character row must point to the new canon and Decision ID. `ADVENTURER_02` content must describe long-range journey continuity/reliability, no direct travel, and same UID wear/serviceability feedback.

- [ ] **Step 3: Add audit/history evidence**

Record benchmark adaptation, P0/P1 adversarial verdict, TDD RED→GREEN evidence, exact-head CI, merge SHA, and postmerge readback.

- [ ] **Step 4: Live readback**

Read every written range and confirm Decision ID, counter `2/10`, merge SHA, product/Task3 blocks, and human/Android `NOT_RUN` values exactly.

---

## Plan self-review

- Spec coverage: all approved Toren design sections map to Tasks 1–5.
- Placeholder scan: no `TBD`, `TODO`, or unspecified product behavior; intentionally unknown balance values are explicitly `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.
- Type/token consistency: `BS-CONTENT-20260811-02`, `ADVENTURER_02`, `TOREN_MARCH`, `JOURNEY_CONTINUITY_AND_RELIABILITY`, `2/10`, and all three result-axis identifiers are consistent across tasks.
- Scope check: one planning subsystem only; no product implementation is included.
