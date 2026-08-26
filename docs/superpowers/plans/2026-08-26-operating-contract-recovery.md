# Operating Contract Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore Blacksmith's current-Base operating-contract validation without changing any Godot product path or altering the approved repair-economy design.

**Architecture:** Advance the protected-path baseline to the verified current `main` commit, then make every operating-health evidence hash use the validator's raw-byte rule. Pin the adapter/CI to the released Base v9.4.4 identity and current fetched Base validator commit, regenerate the derived route snapshot, and protect those facts with a focused regression test.

**Tech Stack:** Python `unittest`, JSON contracts, GitHub Actions, Base project-operating-contract validator.

**Spec:** `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`, `AGENTS.md`, and Base `docs/operations/BASE_V9_4_4_RELEASE_CONTRACT.md`.

## Global Constraints

- Product implementation stays `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`.
- Do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.
- Preserve PR #196 as read-only.
- The repair-economy decision and all `TEMP_TEST_BUDGET` values are out of scope.
- `BENCHMARK_NOT_APPLICABLE`: this is a deterministic maintenance correction; current Project canon, current Base release contract, GitHub current main/PR state, Notion current readback, and the migration-only Sheet are the relevant evidence.

---

### Task 1: Lock the recovered operating facts with a RED regression

**Files:**
- Modify: `tests/test_project_adapter_long_lived_pr_baseline.py`

**Interfaces:**
- Consumes: `skills/PROJECT_BASE_ADAPTER.json`, `docs/PROJECT_OPERATING_HEALTH.json`.
- Produces: a regression that rejects the obsolete `fa9595...` protected baseline and non-raw evidence hashes.

- [ ] **Step 1: Write the failing test**

Add assertions requiring the protected baseline `1bdf5f4b436b114253e86d897c7ef15514103f8f`, Base release `9.4.4`, and SHA-256 hashes computed from every health-evidence file's exact raw bytes.

- [ ] **Step 2: Run test to verify it fails**

Run: `py -3 -m unittest tests.test_project_adapter_long_lived_pr_baseline -v`

Expected: FAIL because the adapter still pins `fa9595...`, Base `9.4.3`, and health evidence contains obsolete hashes.

### Task 2: Apply the smallest current-Base metadata repair

**Files:**
- Modify: `skills/PROJECT_BASE_ADAPTER.json`
- Modify: `docs/PROJECT_OPERATING_HEALTH.json`
- Modify: `skills/PROJECT_SKILL_SNAPSHOT.json`
- Modify: `docs/PROJECT_OPERATING_DASHBOARD.html`
- Modify: `skills/BASE_V9_ADAPTER.json`
- Modify: `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- Modify: `.github/workflows/validate-project-base-adapter.yml`

**Interfaces:**
- Consumes: Base v9.4.4 lock/release index and Base current commit `43b3ffb2c5b026e3d4a38dab2338585894d36f61`.
- Produces: a current protected baseline, raw-byte evidence records, a v9.4.4 adapter identity, and a generated route snapshot matching the adapter.

- [ ] **Step 1: Advance the protected baseline**

Set `protected_baseline.commit` to `1bdf5f4b436b114253e86d897c7ef15514103f8f`, which is the fresh-read `origin/main` and contains all prior protected-path changes.

- [ ] **Step 2: Adopt Base v9.4.4 exactly**

Set Base release fields to `version: 9.4.4`, `release_commit: 210ec78292fa12ed7563ba743b322dd36103ae4a`, `release_evidence_commit: bb61e68dc3028421b60c11b87ba2abd297ee6f78`, `finalization_commit: 5adc196c0185951f50e49ab5e51586eff8d60886`, and Base Registry raw SHA-256 `08f882d0c77339e8f7ff187c35b79501e0a2958ab1ff1c7aaa1c0ef8dbee45d6`.

- [ ] **Step 3: Repair health evidence only from exact bytes**

Replace each of the five stale SHA-256 fields with the exact raw-byte SHA-256 of its existing source file. Do not alter maturity or any `NOT_RUN` gate.

- [ ] **Step 4: Update the validator checkout and regenerate all derived views**

Point the Actions Base checkout to `43b3ffb2c5b026e3d4a38dab2338585894d36f61`, then use the Base artifact builder rather than hand-editing `PROJECT_SKILL_SNAPSHOT.json`, the dashboard, or the legacy compatibility views.

- [ ] **Step 5: Run the focused regression**

Run: `py -3 -m unittest tests.test_project_adapter_long_lived_pr_baseline tests.test_project_base_adapter_thin_migration -v`

Expected: PASS.

### Task 3: Validate the actual operating boundary and record the repair

**Files:**
- Modify: `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`

**Interfaces:**
- Consumes: current main, Base current validator, and current Notion/System Record readback.
- Produces: a concise durable record that the contract gate was recovered without product-path mutation.

- [ ] **Step 1: Run the current Base validator**

Run: `py -3 C:\\Users\\user\\Documents\\GitHub\\Base\\tools\\check_project_operating_contract.py --project-root . --base-repository C:\\Users\\user\\Documents\\GitHub\\Base --check`

Expected: PASS with no protected-path error because the baseline is the exact current main before this metadata-only branch.

- [ ] **Step 2: Add the handoff receipt**

Record the current Base commit, validated Blacksmith main, scope exclusion, and the fact that Google Sheet remains migration-only. Do not claim runtime, Android, accessibility, performance, or human-play validation.

- [ ] **Step 3: Run the focused contracts again**

Run: `py -3 -m unittest tests.test_project_adapter_long_lived_pr_baseline tests.test_project_base_adapter_thin_migration -v`

Expected: PASS.

- [ ] **Step 4: Commit**

```powershell
git add .github/workflows/validate-project-base-adapter.yml docs/PROJECT_OPERATING_DASHBOARD.html docs/PROJECT_OPERATING_HEALTH.json docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md docs/superpowers/plans/2026-08-26-operating-contract-recovery.md skills/BASE_V9_ADAPTER.json skills/PROJECT_BASE_ADAPTER.json skills/PROJECT_BASE_SKILL_ADAPTER.json skills/PROJECT_SKILL_SNAPSHOT.json tests/test_project_adapter_long_lived_pr_baseline.py
git commit -m "ops: restore current Base operating contract"
```

## Plan Self-Review

- Coverage: baseline ancestry, Base release identity, evidence hashes, generated snapshot, CI validator source, and durable handoff receipt are each mapped to a task.
- No protected product path is listed for modification.
- No repair-economy behavior, runtime claim, or Sheet write is introduced.
