# GLADIATOR_02 Kyle Veteran Equipment Continuity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Canonize `BS-CONTENT-20260811-09 / GLADIATOR_02 / KYLE_VAREN / VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION` as R3–R7 planning-only 9/10 while preserving Cassia arena-fit ownership, Noble01 treatment-depth ownership, old/new UID integrity, legacy Kyle PoC history, and all product/Task3 blocks.

**Architecture:** Follow the established Decision08 pattern. First add a focused Python contract and prove semantic RED against the still-current Decision08/8/10 state. Then add the Kyle canon and promote only moving-current planning routers/registry to Decision09/9/10, keeping Decisions01–08 historical meaning intact; repair audit/test consumers that still own moving-current constants; run the Base post-change adversarial loop and exact-head CI; merge; then sync the Google Sheet with the identical Decision ID and merged-main SHA.

**Tech Stack:** Markdown planning canon, JSON registry, Python `unittest`/`pytest`, GitHub Actions, Godot 4.7.1 validation, Base/BCA/GUT/HiGodot/adapter gates, Google Sheets.

## Global Constraints

- Decision ID: `BS-CONTENT-20260811-09`.
- Content ID: `GLADIATOR_02`.
- Customer ID: `KYLE_VAREN`.
- Activity family: `VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION`.
- Work-start Base main: `23d5b292f619022cdd8ab7a33fb1debc2d294861`.
- Work-start Blacksmith main: `80b35b9fc914853428e991c4130edc87dd260083`.
- Written spec head before implementation planning: `8d2dde3c5928c33c7bca81981f49941c63f8cd33`.
- Open PR inventory at start: PR #81 only, `REFERENCE ONLY / DO NOT MERGE`; same-goal Decision09 PR: none.
- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- Kyle responsibility: `CONTINUE_IN_SERVICE_OR_RETIRE_AND_REPLACE`.
- Cassia responsibility remains current-match contextual item fit and arena contribution.
- Noble01/existing repair owner retains treatment depth; Decision09 must not create repair/restoration-depth ownership.
- Keep path preserves the old UID; replacement preserves old UID/history and uses a distinct new UID.
- `NO_UID_REWRITE / NO_HISTORY_TRANSFER_TO_REPLACEMENT / OLD_ITEM_HISTORY_PRESERVED / NEW_ITEM_GETS_NEW_UID`.
- `NO_OLD_ITEM_ALWAYS_BEST / NO_NEW_ITEM_ALWAYS_BEST / NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST / NO_HIGHEST_ARTISTRY_ALWAYS_BEST / NO_MOST_CHRONICLE_ALWAYS_BEST`.
- `NO_SENTIMENT_SCORE / NO_VETERAN_TOTAL_SCORE / NO_LINEAGE_POWER_BONUS`.
- `LEGACY_GLADIATOR_KYLE_FIXTURE_NON_AUTHORITATIVE / NO_FIXED_IRON_SWORD_CANON / NO_LEGACY_ARENA_SCORE_FORMULA_CANON`.
- No direct arena combat, roster/guild management, training/injury management, betting, or baseline permadeath.
- No comeback/replacement count Artistry growth, automatic Chronicle Affix from comeback/retirement, or comeback farming multiplier.
- Exact unlock timing, hard thresholds, visit cadence, economy/rewards and outcome distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED` remains unresolved by this Decision.
- Human playtest, Android device and accessibility remain `NOT_RUN` unless actually observed.

---

### Task 1: Prove Decision09 semantic RED

**Files:**
- Create: `tests/test_r3_gladiator_02_kyle_content.py`
- Create temporarily: `.github/workflows/decision09-semantic-red.yml`

**Interfaces:**
- Consumes: current Decision08 registry/router state and approved Decision09 written spec.
- Produces: a test contract that later materialization must satisfy.

- [ ] **Step 1: Write the failing contract.** Require registry counter `9/10`, Decisions01–09, Decision09 contract fields, the Kyle canon, three result axes, old/new UID boundaries, Cassia/Noble separation, legacy-fixture non-authority, anti-management/anti-score/anti-farming boundaries, and current routers at Decision09 while product/Task3 stay blocked.

```python
self.assertEqual("9/10", registry.get("next_approval_counter"))
self.assertIn("BS-CONTENT-20260811-09", decisions)
self.assertEqual("GLADIATOR_02", contract.get("content_id"))
self.assertEqual("KYLE_VAREN", contract.get("customer_id"))
self.assertEqual(
    ["VETERAN_RETURN_STATE", "EQUIPMENT_CONTINUITY_STATE", "ITEM_UID_LINEAGE_STATE"],
    contract.get("result_axes"),
)
self.assertTrue(contract.get("old_item_history_preserved"))
self.assertTrue(contract.get("new_item_gets_new_uid"))
self.assertFalse(contract.get("history_transfer_to_replacement"))
self.assertFalse(contract.get("legacy_arena_score_formula_canon"))
```

- [ ] **Step 2: Wire only the temporary RED runner and open a Draft PR.**

```yaml
name: Decision09 semantic RED
on:
  pull_request:
    paths:
      - 'tests/test_r3_gladiator_02_kyle_content.py'
      - 'docs/superpowers/specs/2026-08-11-gladiator-02-kyle-veteran-continuity-design.md'
      - 'docs/superpowers/plans/2026-08-11-gladiator-02-kyle-veteran-continuity.md'
jobs:
  semantic-red:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m unittest tests.test_r3_gladiator_02_kyle_content -v
```

- [ ] **Step 3: Verify RED.** Accept failure only when Python executes normally and failures are caused by Decision09/9/10/canon/current-router absence. Reject syntax/import/YAML/infrastructure failures as fake RED.

- [ ] **Step 4: Commit the RED evidence state.** Preserve the exact RED head and workflow/job identifiers for the later receipt.

---

### Task 2: Materialize the planning-only Kyle canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`

**Interfaces:**
- Consumes: approved written spec and Task 1 contract.
- Produces: canonical Decision09 plus current 9/10 routing without product implementation.

- [ ] **Step 1: Create the canon from the approved spec.** Canon flow must be:

```text
KYLE_VAREN revisit
-> real prior Kyle item record
-> disclosed comeback purpose/current role
-> old UID current state + real lifecycle evidence
-> hard serviceability/eligibility gate
-> KEEP_IN_SERVICE or RETIRE_AND_REPLACE
-> off-screen comeback/arena world event
-> VETERAN_RETURN_STATE
 + EQUIPMENT_CONTINUITY_STATE
 + ITEM_UID_LINEAGE_STATE
-> 2-4 actual reasons
-> one primary next action
```

- [ ] **Step 2: Add Decision09 to the registry without deleting Decisions01–08.** Set `next_approval_counter` to `9/10`. The Decision09 contract must explicitly model keep-path same UID, replace-path old-history preservation/new UID, no history transfer, Cassia/Noble separation, non-authoritative legacy fixture, anti-score/anti-management/anti-farming boundaries, P1 taxonomy defer, and planning-only blocks.

- [ ] **Step 3: Move only current router state from D08/8/10 to D09/9/10.** Keep D08 as the eighth historical section; Roadmap order must remain `... 7/10 -> 8/10 -> 9/10`.

- [ ] **Step 4: Commit the minimal materialization.** No scripts/scenes/resources/runtime data or `data/customers/gladiator_poc.json`/`data/world/gladiator_match_poc.json` changes are allowed.

---

### Task 3: Repair moving-current consumers and prove GREEN

**Files:**
- Modify: `.github/workflows/python-validation.yml` to run `tests/test_r3_gladiator_02_kyle_content.py` permanently.
- Modify only moving-current assertions discovered by search in prior R3 content tests, `tests/check_project_core_alignment_current.py`, `tests/test_auto_enhancement_cap_unlock.py`, `tests/test_hera_postmerge_closure_contract.py`, `tests/test_project_operating_system_audit_runner.py`, and `tools/run_project_operating_system_audit.py`.
- Refresh `docs/PROJECT_OPERATING_HEALTH.json` only when the existing audit contract requires the changed current-decision hash/evidence.
- Remove `.github/workflows/decision09-semantic-red.yml` once permanent validation owns the test.

**Interfaces:**
- Consumes: Decision09 materialized current state.
- Produces: one coherent `D09 current / D01–D08 history` repository state.

- [ ] **Step 1: Run the focused Decision09 contract.**

```bash
python -m unittest tests.test_r3_gladiator_02_kyle_content -v
```

Expected after materialization: PASS.

- [ ] **Step 2: Search stale moving-current tokens.** Search for `R3_R7_APPROVAL_COUNTER: 8/10`, `R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08`, and tests/audit constants that semantically mean *current*. Do not rewrite D08 historical assertions or immutable merge SHAs.

- [ ] **Step 3: Run focused history/current regressions.** At minimum run D05 Cassia, D06 Noble01, D07 Liana, D08 Sedric, project-core current alignment, auto-enhancement current routing, Hera current/history, and project operating audit wrapper.

- [ ] **Step 4: Repair only semantic current-pointer failures.** If a test owns historical Decision08 semantics, keep D08. If it owns the current pointer, update it to D09/9/10.

- [ ] **Step 5: Remove the temporary RED workflow and commit GREEN.**

---

### Task 4: Adversarial/post-change review and exact-head closure

**Files:**
- Create: `docs/superpowers/receipts/2026-08-11-bs-content-20260811-09-red-green.md`
- Create/update only if current project convention requires it: Decision09 adversarial/audit receipt.

**Interfaces:**
- Consumes: fully GREEN planning diff.
- Produces: exact-head evidence suitable for merge.

- [ ] **Step 1: Attack the retained diff.** Check for Cassia reskin, Noble01 treatment overlap, old/new UID overwrite, fake Kyle history, legacy score resurrection, direct combat/roster/training/injury drift, lineage stat creep, sentimental/new-item auto-best, result collapse, progression farming, taxonomy scope hijack, product/Task3 leakage, stale untouched consumers, and unintended generated/gitlink artifacts.

- [ ] **Step 2: Validate critiques and classify findings.** Use `OMISSION / CONFLICT / COMPLEMENT_GAP / DUPLICATE_WORK / NO_MATERIAL_FOLLOWUP`; only validated in-scope findings get minimal fixes.

- [ ] **Step 3: Recheck same-goal open/recent PRs.** PR #81 remains reference-only; no concurrent Decision09 owner may exist.

- [ ] **Step 4: Validate one exact head.** Require the repository's current full PR workflow set on one SHA, including Python contracts, Godot 4.7.1 headless, Base v9/planning-first, BCA, Project Base Adapter, Thin Adapter, GUT and HiGodot/GUT authority gates.

- [ ] **Step 5: Mark Ready and merge only after exact-head GREEN.** Re-run any Ready-triggered adapter gate on that same head if the repository does so.

- [ ] **Step 6: Postmerge readback.** Re-read `main`, D09 canon/registry/current routers, Base current main, open/recent PRs, and complete the Base `POST_CHANGE_MONITOR_LOOP`.

---

### Task 5: Same-ID Google Sheet sync and readback

**Files/data:**
- Google Sheet `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`.
- Re-discover exact empty/target rows immediately before write; do not hardcode from stale state.

**Interfaces:**
- Consumes: final merged Blacksmith main SHA and Decision09 canon.
- Produces: GitHub/Sheet same-ID synchronized authority.

- [ ] **Step 1: Re-read hub/current-decision/product-direction/Kyle/main-content/change-history target ranges.** Ensure no concurrent Sheet edit has occupied the intended rows.

- [ ] **Step 2: Sync exact Decision ID `BS-CONTENT-20260811-09`.** Update current hub/work-order/product-direction, append D09 current-decision row, expand Kyle character row, add `GLADIATOR_02` main-content row, and append change history. Preserve P1 taxonomy defer and all implementation/NOT_RUN blocks.

- [ ] **Step 3: Exact readback.** Require D09, `9/10`, final merged main SHA, Kyle/`GLADIATOR_02`, next `10/10` planning decision required, `PRODUCT_IMPLEMENTATION_BLOCKED`, `TASK3_NOT_APPROVED`, and `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`.

- [ ] **Step 4: Final report.** Report before -> changes -> RED/GREEN/evidence -> after -> expected player/product effect -> remaining risks/NOT_RUN.
