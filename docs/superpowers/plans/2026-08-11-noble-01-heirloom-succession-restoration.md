# NOBLE_01 Heirloom Succession Restoration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `BS-CONTENT-20260811-06 / NOBLE_01 / CEREMONIAL_NOBLE / HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY` to R3–R7 planning canon at `6/10` without opening product or Task3 implementation.

**Architecture:** Reuse the existing `CEREMONIAL_NOBLE` vertical-slice representative ID and current item UID, damage/repair/restoration, provenance, Artistry, Chronicle, customer-result, and world-result authorities. The new content asks how far the smith should intervene on one existing heirloom before a succession ceremony; it does not create a noble-house simulator, diplomacy layer, or aggregate prestige/authenticity score. Results remain decomposed into ceremony readiness, treatment fit, and the same UID's dynastic legacy.

**Tech Stack:** Markdown planning canon, JSON R3 registry, Python `unittest` contract tests, existing GitHub Actions PR validation, Google Sheet same-ID synchronization.

## Global Constraints

- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- PR #81 remains `REFERENCE ONLY / DO NOT MERGE`.
- R3 approval counter changes from `5/10` to `6/10` only for `BS-CONTENT-20260811-06`.
- Reuse `CEREMONIAL_NOBLE`; do not invent a new named noble or family canon in this Decision.
- Preserve the same item UID before, during, and after restoration and ceremony.
- No `HOUSE_PRESTIGE_SCORE`, `AUTHENTICITY_SCORE`, `SUCCESSION_SCORE`, or other opaque aggregate raw stat.
- Full restoration is not automatically best; highest Artistry is not automatically best.
- Do not erase meaningful prior damage/repair/provenance merely to maximize a cosmetic outcome.
- Ceremony/restoration count does not automatically grow `ARTISTRY` or grant `CHRONICLE_AFFIX`.
- No direct ceremony minigame, noble-house management, court/diplomacy management, or inheritance strategy game.
- Exact treatment thresholds, economy, timing, rewards, and result distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.
- Sheet drift in `00_프로젝트_허브` and `10_제품방향` is repaired as derived-state maintenance, not as a new product-scope Decision.

---

### Task 1: Establish semantic RED for Decision06

**Files:**
- Create: `tests/test_r3_noble_01_heirloom_succession_content.py`
- Modify: `.github/workflows/python-validation.yml`

**Interfaces:**
- Consumes: current R3 registry/current-router documents and the existing `data/vertical_slice/vertical_slice_preset.json` customer ID.
- Produces: an executable contract proving the exact `6/10` planning behavior and protected boundaries.

- [ ] **Step 1: Write the failing contract test**
  - Assert `BS-CONTENT-20260811-06`, `NOBLE_01`, `CEREMONIAL_NOBLE`, `NOBLE`, and `HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY`.
  - Assert result axes `CEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE`.
  - Assert same UID, no full-restoration/highest-Artistry universal answer, no opaque score, no history erasure, no progression farming, no direct ceremony/house/diplomacy control, and blocked product/Task3 gates.
  - Assert the existing vertical-slice preset already contains `ceremonial_noble` so the Decision does not invent a parallel representative fixture.

- [ ] **Step 2: Wire the test into CI**
  - Add `python -m unittest tests.test_r3_noble_01_heirloom_succession_content -v` beside the current R3 content contracts.

- [ ] **Step 3: Verify semantic RED**
  - Open the PR with only plan/spec/test/CI wiring as needed.
  - Expected failure: Decision06 canon/registry/current routers are absent. Infrastructure/workflow errors do not count as semantic RED.

### Task 2: Materialize the approved planning canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify current-health/current-state tests and audit owners only when they legitimately consume the current Decision/counter.

**Interfaces:**
- Consumes: Decisions01–05, `BS-CONTENT-20260804-02`, existing item lifecycle/restoration/provenance/Artistry/Chronicle authorities, and `CEREMONIAL_NOBLE` representative fixture.
- Produces: current R3 `6/10` canon while preserving Decisions01–05 as approved history.

- [ ] **Step 1: Add the Decision06 canon**
  - Define the player-facing flow: existing heirloom UID + succession purpose → inspect actual condition/history → choose justified intervention depth → same UID handoff → off-screen ceremony → decomposed result → repair/preservation/reuse/future succession feedback.
  - Keep treatment approaches contextual and evidence-driven rather than fixed score optimization.

- [ ] **Step 2: Promote current registry and routers**
  - Advance current pointers to `6/10 / BS-CONTENT-20260811-06` only.
  - Preserve all prior approved Decision IDs and product/Task3 blocks.

- [ ] **Step 3: Verify GREEN**
  - Run the focused Decision06 contract and prior R3 contracts through GitHub Actions.
  - Fix only actual current-state consumers; never weaken historical assertions or protected gates.

### Task 3: Adversarial review, full regression, merge, and synchronization

**Interfaces:**
- Consumes: exact reviewed PR head and live Sheet state.
- Produces: merged main canon and same-ID Sheet readback with derived-state drift repaired.

- [ ] **Step 1: Attack the design**
  - Check for prestige/authenticity score drift, cosmetic-maximization dominance, history erasure, restoration farming, UID replacement, curator/house/diplomacy drift, and Ersa Collector overlap.
  - Require that Ersa still owns exhibition evidence/provenance selection while Noble01 owns intervention-depth/restoration judgment for a pre-existing heirloom.

- [ ] **Step 2: Run exact-head regression and operating audit**
  - Require all PR checks on the exact reviewed head to succeed.
  - Inspect diff, review state, comments, and mergeability before merge.

- [ ] **Step 3: Merge and postmerge readback**
  - Squash-merge only after exact-head validation.
  - Re-read `main`, current registry/current routers, and relevant Sheet rows.

- [ ] **Step 4: Synchronize Google Sheet with the same Decision ID**
  - Append/update `BS-CONTENT-20260811-06` in `02_현재_확정결정`.
  - Advance `01_작업순서`, `00_프로젝트_허브`, relevant content/character rows, and derived `10_제품방향` state without opening product implementation.
  - Use the final merged main SHA, then perform independent readback.

## Verification ledger

- Preflight Base main: `7ce96181d0a97930300fcc6d383dacc75ad08f6a`.
- Preflight Blacksmith main: `42469f6e2058efea464755ac44bec8bcd1154f0b`.
- Open PR inventory at start: PR #81 only, `REFERENCE ONLY / DO NOT MERGE`.
- Sheet current authority at start: Decision05 / `5/10`; product blocked; Task3 not approved.
- Derived Sheet drift at start: `00_프로젝트_허브` carries stale Base/Blacksmith SHA fields and `10_제품방향` still says `PLANNING_REMEDIATION_IN_PROGRESS / CURRENT_NOT_READY`.
- Semantic RED head: pending.
- Materialized GREEN head: pending.
- Exact reviewed head: pending.
- Merge main: pending.
- Sheet same-ID/final-head readback: pending.
