# COLLECTOR_02 Sedric Archival Accession Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Canonize `BS-CONTENT-20260811-08 / COLLECTOR_02 / SEDRIC_VAEL / ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY` as R3–R7 planning-only 8/10 while preserving Ersa exhibition ownership, Noble01 treatment-depth ownership, same-UID lifecycle, and all product/Task3 blocks.

**Architecture:** Follow the established Decision01–07 pattern. Add one focused Python contract first and prove semantic RED against the still-current 7/10 state. Then materialize the Sedric canon, promote the current registry/router state to 8/10, repair only moving-current consumers, run adversarial/post-change checks, validate one exact PR head, merge, and sync Google Sheet with the same Decision ID.

**Tech Stack:** Markdown planning canon, JSON registry, Python `unittest`/`pytest`, GitHub Actions, Godot 4.7.1 validation, Google Sheets.

## Global Constraints

- Decision ID: `BS-CONTENT-20260811-08`.
- Content ID: `COLLECTOR_02`.
- Customer ID: `SEDRIC_VAEL`.
- Activity family: `ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY`.
- Work-start Base main: `23d5b292f619022cdd8ab7a33fb1debc2d294861`.
- Work-start Blacksmith main: `7005a939e003f7248e7d2546c4266bb5d144f90a`.
- Open PR inventory at start: PR #81 only, `REFERENCE ONLY / DO NOT MERGE`.
- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- `SAME_ITEM_UID_PRESERVED`.
- `ERSA_EXHIBITION_RESPONSIBILITY_PRESERVED`.
- `NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED`.
- `NO_AUTHENTICITY_TOTAL_SCORE / NO_PROVENANCE_COMPLETENESS_SCORE / NO_ARCHIVE_PRESTIGE_SCORE`.
- `NO_HIGHEST_ARTISTRY_ALWAYS_BEST / NO_OLDEST_ITEM_ALWAYS_BEST / NO_MOST_CHRONICLE_EVENTS_ALWAYS_BEST / NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`.
- `NO_DOCUMENT_FABRICATION / NO_UNRECORDED_HISTORY_AUTOFILL`.
- `NO_ACCESSION_COUNT_ARTISTRY_GROWTH / NO_APPRAISAL_OR_REVIEW_COUNT_ARTISTRY_GROWTH`.
- `NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_ARCHIVING`.
- `NO_ARCHIVE_STORAGE_MANAGEMENT / NO_MUSEUM_MANAGEMENT_SIM / NO_VISITOR_MANAGEMENT / NO_LOAN_LOGISTICS_MANAGEMENT`.
- Exact thresholds, archive-purpose mixes, timing, rewards and outcome distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED` remains unresolved by this Decision.

---

### Task 1: Prove semantic RED

**Files:**
- Create: `tests/test_r3_collector_02_sedric_content.py`
- Create temporarily: `.github/workflows/decision08-semantic-red.yml`

- [ ] Write a focused contract requiring registry `8/10`, Decision08, the Sedric canon, the three result axes, protected boundaries, and current routers at Decision08 while product/Task3 stay blocked.
- [ ] Open a Draft PR with only spec/plan/test/temporary RED runner.
- [ ] Accept RED only when the test executes normally and fails because current registry/router state is still Decision07/7/10 and Sedric canon is absent.

### Task 2: Materialize Decision08 canon and current state

**Files:**
- Create: `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`

- [ ] Add the canonical flow: Sedric visit → disclosed archival purpose → inspect real UID evidence → one same-UID handoff → off-screen accession → `ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE` → follow-up reason.
- [ ] Add Decision08 to the registry without deleting Decisions01–07.
- [ ] Move only current pointers from 7/10 Decision07 to 8/10 Decision08.

### Task 3: Repair moving-current consumers and prove GREEN

**Files:**
- Modify: `.github/workflows/python-validation.yml` to run the permanent Sedric test.
- Modify only moving-current assertions in `tests/check_project_core_alignment_current.py`, prior R3 content tests, `tests/test_auto_enhancement_cap_unlock.py`, `tests/test_hera_postmerge_closure_contract.py`, `tests/test_project_operating_system_audit_runner.py`, and `tools/run_project_operating_system_audit.py` when they still pin Decision07/7/10.
- Refresh `docs/PROJECT_OPERATING_HEALTH.json` only for the changed `CURRENT_CONFIRMED_DECISIONS.md` hash.
- Remove temporary RED-only workflow after the permanent validation path owns the test.

- [ ] Re-run focused Decision08 and all moving-current regressions.
- [ ] Repair only failures caused by the current pointer move; preserve historical meanings and immutable prior SHAs.

### Task 4: Post-change adversarial and exact-head closure

- [ ] Attack for Ersa reskin, Noble01 overlap, hidden score, oldest/highest-stat dominance, fabricated provenance, archive-management drift, UID cloning, progression farming, product/Task3 leakage, and untouched current consumers.
- [ ] Recheck same-goal open/recent PRs; PR #81 must remain reference-only.
- [ ] Require the repository's current PR validation set at one exact head, including Python contracts, Godot headless, Base/BCA/GUT/HiGodot/adapter gates.
- [ ] Mark Ready and merge the already approved planning scope only after exact-head GREEN.
- [ ] Re-read merged `main` and classify the Base `POST_CHANGE_MONITOR_LOOP` result.

### Task 5: Same-ID Sheet sync and readback

- [ ] Re-read target Sheet ranges immediately before write.
- [ ] Sync `BS-CONTENT-20260811-08` to hub, work-order/current-decision, product-direction, Sedric character row, main-content row and change-history row using final merged main SHA.
- [ ] Preserve adapter pin, P1 taxonomy ambiguity, product/Task3 blocks, and `HUMAN_PLAYTEST / ANDROID_DEVICE / ACCESSIBILITY = NOT_RUN` unless actually observed.
- [ ] Exact readback must show Decision08, 8/10, final main SHA, same Decision ID, and `POSTMERGE_READBACK_PASS`.
