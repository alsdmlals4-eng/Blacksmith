# SOLDIER_01 Marek Small-Lot Standard Order Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `BS-CONTENT-20260811-03 / SOLDIER_01 / MAREK_OLDEN / SMALL_LOT_STANDARD_ORDER` to R3–R7 planning canon at `3/10` without opening product or Task3 implementation.

**Architecture:** Add one Soldier content canon and propagate the Decision through the existing R3 registry/current-router documents. The contract keeps a roughly ten-item fixture as a small-lot planning preset while preserving per-item UID, resource, work, forging, enhancement, and lifecycle semantics.

**Tech Stack:** Markdown planning canon, JSON R3 registry, Python `unittest` contract tests, existing GitHub Actions PR validation.

## Global Constraints

- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- PR #81 remains reference-only and is not merged.
- R3 approval counter changes from `2/10` to `3/10` only for `BS-CONTENT-20260811-03`.
- `ORDER_QUANTITY = 10` is a noncanonical baseline fixture, not a universal release constant.
- No direct tactical combat, real-time logistics, worker/production-line system, free cloning, or opaque standardization score.
- Every delivered item keeps a unique UID and independent costs/results/history.

---

### Task 1: Add the failing Marek planning-contract test

**Files:**
- Create: `tests/test_r3_soldier_01_marek_content.py`

**Interfaces:**
- Consumes: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`, current router documents.
- Produces: assertions for Decision03 promotion and protected boundaries.

- [ ] **Step 1: Write the failing test** asserting `3/10`, Decision ID, `SOLDIER_01`, `MAREK_OLDEN`, `SMALL_LOT_STANDARD_ORDER`, fixture quantity 10, per-item UID/cost/result preservation, decomposed result axes, and product/Task3 blocks.
- [ ] **Step 2: Run only this test and verify RED** because Marek canon/Decision03 is not yet present.
- [ ] **Step 3: Record the RED cause** as missing approved planning canon, not workflow syntax/environment failure.

### Task 2: Materialize the minimum approved Marek canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`

**Interfaces:**
- Consumes: Decision03 design spec.
- Produces: current `3/10` planning routing and Soldier01 canon.

- [ ] **Step 1: Add the Soldier01 canon** with reference-item + independent-small-lot semantics and no product implementation.
- [ ] **Step 2: Promote registry to `3/10`** while retaining Nadia/Toren history and all protected boundaries.
- [ ] **Step 3: Update current routers** to Decision03 and `SOLDIER_01_MAREK_SMALL_LOT_STANDARD_ORDER_APPROVED`.
- [ ] **Step 4: Run the focused test and verify GREEN**.

### Task 3: Regression and authority checks

**Files:**
- Modify only if an existing current-state assertion legitimately needs current/history separation.

- [ ] **Step 1: Run project planning/document contract tests** used by prior R3 promotion PRs.
- [ ] **Step 2: Fix only stale current-state consumers**; do not weaken protected tests.
- [ ] **Step 3: Run full PR validation and exact-head CI**.
- [ ] **Step 4: Adversarially inspect the diff** for mass-production drift, item identity loss, product scope opening, or PR81 contamination.
- [ ] **Step 5: Merge after exact-head validation under inherited same-approved-scope authority**.
- [ ] **Step 6: Postmerge read back new main and synchronize the same Decision ID to Google Sheet**.
