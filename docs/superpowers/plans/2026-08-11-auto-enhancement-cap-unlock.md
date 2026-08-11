# Progressive Auto-Enhancement Cap Unlock Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Canonize `BS-CORE-20260811-01 / AUTO_ENHANCEMENT_CAP_UNLOCK` as a planning refinement of the existing low-risk continuous-enhancement rule without automating the current risk frontier.

**Architecture:** Keep the existing sequential enhancement attempt owner unchanged. Add planning authority that derives a category-specific automatic target cap from already-completed manual breakthrough milestones, one 10-level band behind the frontier, while preserving normal per-attempt risk/cost/history and explicit manual stop points.

**Tech Stack:** Markdown planning canon, current decision/router documents, Python `unittest` contract tests, existing GitHub Actions PR validation.

## Global Constraints

- Preserve the existing initial `15 manual attempts → AUTO_CAP +20` rule.
- Later cap ownership is category-specific.
- `AUTO_CAP = highest completed category breakthrough - 10`, with the initial +20 early-game exception.
- Player selects `TARGET_ENHANCEMENT <= AUTO_CAP`.
- `HIGH / VERY_HIGH`, precision enhancement, technical breakthrough, and permanent-risk branches remain manual.
- Auto attempts use normal chance, cost, resources, fatigue/work, UID history, and telemetry.
- No new pity gauge, success bonus, discount, resource bypass, or unprotected automatic destruction.
- Product implementation and Task3 remain blocked.
- This core/system Decision does not increment the R3 content approval counter.

---

### Task 1: Add the failing auto-cap planning-contract test

**Files:**
- Create: `tests/test_auto_enhancement_cap_unlock.py`

**Interfaces:**
- Consumes: existing continuous-enhancement authority and growth-breakthrough authority.
- Produces: assertions for Decision `BS-CORE-20260811-01` and its protected boundaries.

- [ ] **Step 1: Write the failing test** asserting the existing +20 unlock remains, later category breakthrough mapping trails by one band, target is player-selected, attempts preserve normal semantics, and manual-only stop points remain.
- [ ] **Step 2: Run only this test and verify RED** because the new Decision/canon is absent.
- [ ] **Step 3: Confirm the RED is semantic absence rather than a test harness error**.

### Task 2: Materialize the planning refinement

**Files:**
- Create: `docs/planning/BLACKSMITH_AUTO_ENHANCEMENT_CAP_UNLOCK_CANON_2026.md`
- Create: `docs/decisions/BS-CORE-20260811-01_AUTO_ENHANCEMENT_CAP_UNLOCK.md`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify current router/gate documents only where the new core Decision must be discoverable.

**Interfaces:**
- Consumes: `BLACKSMITH_DECISION_LEDGER_ADDENDUM_07.md`, `BLACKSMITH_GROWTH_SYSTEM_ADDENDUM_02.md`, `BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026.md`.
- Produces: one authoritative refinement that does not duplicate probability or breakthrough ownership.

- [ ] **Step 1: Add the auto-cap canon and Decision record** with explicit refinement/inheritance links.
- [ ] **Step 2: Add discoverability to current confirmed decisions and relevant routing docs** without changing R3 counter ownership.
- [ ] **Step 3: Run focused auto-cap test and verify GREEN**.

### Task 3: Combined regression and postmerge sync

**Files:**
- Modify only stale current-state consumers or operating-health derivative evidence proven necessary by tests.

- [ ] **Step 1: Run Marek and auto-cap focused tests together**.
- [ ] **Step 2: Run existing enhancement, growth, R3 router, and operating-audit tests**.
- [ ] **Step 3: Confirm no test was weakened to obtain GREEN**.
- [ ] **Step 4: Run full exact-head PR CI**.
- [ ] **Step 5: Adversarially inspect the final diff** for frontier automation, silent destruction, UID merging, duplicate probability authority, or accidental content-counter increments.
- [ ] **Step 6: Merge within the already-approved scope after exact-head validation**.
- [ ] **Step 7: Postmerge read back GitHub main and synchronize `BS-CORE-20260811-01` to Google Sheet separately from Marek's `3/10` content Decision**.
