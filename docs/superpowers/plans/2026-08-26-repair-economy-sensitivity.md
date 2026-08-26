# Repair Economy Sensitivity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute Decision31's reproducible normalized repair-economy sensitivity sweep and publish only a planning interpretation.

**Architecture:** One JSON fixture fixes one UID, five actual-damage/repair cycles, `R_BAND=100`, and the three approved loss coefficients. A standalone Python tool emits structured rows and invariant evidence; a report retains `TEST_IN_PLAY`, not a final price conclusion.

**Tech Stack:** Python standard library, JSON, `unittest`, Markdown.

**Spec:** `docs/superpowers/specs/2026-08-26-repair-economy-sensitivity-design.md`

## Global Constraints

- GitHub Issue: `#216`.
- `BS-REPAIR-20260826-31` owns economy and `BS-REPAIR-20260826-29` retains quality/scar semantics.
- `R_BAND=100` is normalized input only; no live price table is authored.
- Do not change `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.
- Do not use `tools/simulate_enhancement_balance.py` as current durability evidence.
- Runtime, Android, accessibility, performance, and human play remain `NOT_RUN`.
- Future approved-image receipts require both a Notion record and exact project-local binary path; no image file is created here.

---

### Task 1: Freeze deterministic analysis input

**Files:**
- Create: `docs/planning/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_INPUT_20260826.json`
- Create: `tests/test_repair_economy_sensitivity.py`

**Interfaces:**
- Consumes: Decision31 formula and Decision29 five-point semantics.
- Produces: `load_input(path: Path) -> dict` with one UID, `base_max=5`, `r_band_normalized=100`, and five events.

- [ ] **Step 1: Write the failing test**

```python
def test_input_fixes_one_uid_and_one_variable_sweep() -> None:
    payload = load_input(INPUT)
    assert payload["item_uid"] == "BS-REPAIR-SENS-001"
    assert payload["r_band_normalized"] == 100
    assert payload["loss_coefficients"] == [0.5, 0.65, 0.8]
    assert len(payload["events"]) == 5
    assert all(event["base_max"] == 5 for event in payload["events"])
```

- [ ] **Step 2: Run RED**

Run: `py -3 -m unittest tests.test_repair_economy_sensitivity -v`

Expected: FAIL because input and loader do not exist.

- [ ] **Step 3: Add the immutable JSON input**

Use five eligible events with `CURRENT = 4, 3, 2, 1, 4`, `MAX=5`, quality ratios `1.00, 0.50, 0.75, 1.00, 0.50`, and last-event `candidate_post_scar_max=4`. Every event is a resolved actual-damage event with a repair job.

- [ ] **Step 4: Run GREEN**

Run: `py -3 -m unittest tests.test_repair_economy_sensitivity -v`

Expected: PASS for fixed UID, normalized input, one-variable sweep, and five-point coverage.

- [ ] **Step 5: Commit**

Run:

```powershell
git add docs/planning/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_INPUT_20260826.json tests/test_repair_economy_sensitivity.py
git commit -m "test: define repair economy sensitivity input contract"
```

### Task 2: Implement planning-only analyzer

**Files:**
- Create: `tools/run_repair_economy_sensitivity.py`
- Modify: `tests/test_repair_economy_sensitivity.py`

**Interfaces:**
- Consumes: fixed JSON input.
- Produces: `resolve_repair(event: dict) -> dict`, `analyze(payload: dict) -> dict`, and rows with Gold, material use, recovery, scar skip, job consumption, repeat outcome, and decision outcome.

- [ ] **Step 1: Write failing arithmetic and guard tests**

```python
def test_cost_changes_only_with_loss_coefficient() -> None:
    result = analyze(load_input(INPUT))
    first = [row for row in result["rows"] if row["event_id"] == "E1"]
    assert [row["gold"] for row in first] == [15, 18, 21]
    assert len({row["new_current"] for row in first}) == 1

def test_blocking_scar_skips_and_job_cannot_repeat() -> None:
    row = next(row for row in analyze(load_input(INPUT))["rows"] if row["event_id"] == "E5" and row["b"] == 0.65)
    assert row["scar_skipped"] is True
    assert row["new_current"] > row["old_current"]
    assert row["repeat_repair_outcome"] == "BLOCKED_NO_REPAIR_JOB"
```

- [ ] **Step 2: Run RED**

Run: `py -3 -m unittest tests.test_repair_economy_sensitivity -v`

Expected: FAIL because `analyze` does not exist.

- [ ] **Step 3: Add minimal analyzer**

Use `Decimal` plus `ROUND_CEILING` for Gold and quality targets. Apply the Decision31 blocking condition exactly without reroll. Emit three rows per event, one common material and one consumed job per row; set `player_decision_outcome="REPAIR_NOW"` and repeat outcome to `BLOCKED_NO_REPAIR_JOB`.

- [ ] **Step 4: Run GREEN**

Run:

```powershell
py -3 tools/run_repair_economy_sensitivity.py --input docs/planning/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_INPUT_20260826.json --output docs/research/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_RESULT_20260826.json
py -3 -m unittest tests.test_repair_economy_sensitivity -v
```

Expected: 15 rows, all positive Current gain, and all tests PASS.

- [ ] **Step 5: Commit**

Run:

```powershell
git add tools/run_repair_economy_sensitivity.py tests/test_repair_economy_sensitivity.py docs/research/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_RESULT_20260826.json
git commit -m "feat: add deterministic repair economy sensitivity analyzer"
```

### Task 3: Publish interpretation and handoff

**Files:**
- Create: `docs/research/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_REPORT_20260826.md`
- Modify: `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`
- Modify: `tests/check_repair_economy_rebase_current_contract.py`

**Interfaces:**
- Consumes: generated result and Decision31.
- Produces: source-backed `KEEP / TEST_IN_PLAY` interpretation and next-decision locator.

- [ ] **Step 1: Write failing report assertions**

```python
assert "R_BAND = 100" in report
assert "b = 0.50 / 0.65 / 0.80" in report
assert "TEST_IN_PLAY" in report
assert "NOT_FINAL_PRODUCT_BALANCE" in report
assert "final price table" not in report.lower()
```

- [ ] **Step 2: Run RED**

Run: `py -3 tests/check_repair_economy_rebase_current_contract.py`

Expected: FAIL because report does not exist.

- [ ] **Step 3: Add report and receipt**

Report 15 rows compactly. Identify normalized Gold bands `15/18/21`, `25/31/37`, `35/44/53`, and `45/57/69` for Current `4/3/2/1`; record `KEEP` for job gate, scar guard, and one material, `TEST_IN_PLAY` for all coefficients, and `R_BAND` live pricing as `NOT_DECIDED`.

- [ ] **Step 4: Validate**

Run:

```powershell
py -3 -m unittest tests.test_repair_economy_sensitivity tests.test_project_adapter_long_lived_pr_baseline -v
py -3 tests/check_repair_economy_rebase_current_contract.py
py -3 tests/check_durability_repair_model_current_contract.py
py -3 tests/check_core_simplification_current_contract.py
```

Expected: PASS; runtime and human-play stay `NOT_RUN`.

- [ ] **Step 5: Commit**

Run:

```powershell
git add docs/research/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_REPORT_20260826.md docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md tests/check_repair_economy_rebase_current_contract.py
git commit -m "docs: record repair economy sensitivity result"
```

## Plan Self-Review

- Coverage: fixed input, single-variable arithmetic, positive recovery, scar skip, one-job gate, material separation, generated evidence, and `TEST_IN_PLAY` each have a task.
- Scope: no product path, live price table, asset, or runtime change appears.
- Type consistency: Task 2 defines `analyze` and `resolve_repair`; Task 3 consumes its result JSON only.
