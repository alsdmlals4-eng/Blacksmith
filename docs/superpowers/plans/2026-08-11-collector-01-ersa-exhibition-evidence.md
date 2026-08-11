# COLLECTOR_01 Ersa Exhibition Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `BS-CONTENT-20260811-04 / COLLECTOR_01 / ERSA_ROEN / EXHIBITION_EVIDENCE_AND_PROVENANCE` to R3–R7 planning canon at `4/10` without opening product or Task3 implementation.

**Architecture:** Add one Collector content canon and propagate the Decision through the existing R3 registry/current-router documents. The contract reuses the existing item UID, Artistry, provenance, Chronicle, ownership, damage/recovery/repair history, and explanatory customer-result layers; it adds no new raw score and keeps exhibition execution off-screen.

**Tech Stack:** Markdown planning canon, JSON R3 registry, Python `unittest` contract tests, existing GitHub Actions PR validation.

## Global Constraints

- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- PR #81 remains reference-only and is not merged.
- R3 approval counter changes from `3/10` to `4/10` only for `BS-CONTENT-20260811-04`.
- `CRAFTSMANSHIP_EVIDENCE` and `LIVED_HISTORY_EVIDENCE` are exhibition-context families, not new item types or raw stats.
- No `RARITY_SCORE`, `PRESTIGE_SCORE`, `COLLECTOR_SCORE`, `EXHIBITION_SCORE`, Chronicle-count optimization, or oldest/highest-Artistry/highest-enhancement universal answer.
- Exhibition count/display alone cannot grow `ARTISTRY` or automatically grant `CHRONICLE_AFFIX`.
- Same item UID remains authoritative before, during, and after exhibition.
- No direct exhibition minigame, gallery decoration core, visitor management, auction management, or curator-control expansion.

---

### Task 1: Add the failing Ersa planning-contract test

**Files:**
- Create: `tests/test_r3_collector_01_ersa_content.py`

**Interfaces:**
- Consumes: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`, current router documents.
- Produces: assertions for Decision04 promotion, evidence families, decomposed result axes, same-UID lifecycle, and protected boundaries.

- [ ] **Step 1: Write the failing test** asserting `4/10`, Decision ID, `COLLECTOR_01`, `ERSA_ROEN`, `EXHIBITION_EVIDENCE_AND_PROVENANCE`, the two context families, no opaque score, no automatic Artistry/Chronicle growth, same UID preservation, decomposed result axes, and product/Task3 blocks.
- [ ] **Step 2: Run only this test and verify RED** because Ersa canon/Decision04 is not yet present.
- [ ] **Step 3: Record the RED cause** as missing approved planning canon/current routing, not workflow syntax or environment failure.

### Task 2: Materialize the minimum approved Ersa canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`

**Interfaces:**
- Consumes: Decision04 design spec.
- Produces: current `4/10` planning routing and Collector01 canon.

- [ ] **Step 1: Add the Collector01 canon** with exhibition intent, existing-evidence comparison, maker-statement explanation layer, off-screen resolution, and same-UID public-history consequence.
- [ ] **Step 2: Promote registry to `4/10`** while retaining Nadia/Toren/Marek history and all protected boundaries.
- [ ] **Step 3: Update current routers** to Decision04 and `COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED`.
- [ ] **Step 4: Run the focused test and verify GREEN**.

### Task 3: Regression and authority checks

**Files:**
- Modify only if an existing current-state assertion legitimately needs current/history separation.

- [ ] **Step 1: Run project planning/document contract tests** used by prior R3 promotion PRs.
- [ ] **Step 2: Fix only stale current-state consumers**; do not weaken protected tests.
- [ ] **Step 3: Run full PR validation and exact-head CI**.
- [ ] **Step 4: Adversarially inspect the diff** for hidden score drift, lore-quiz drift, Chronicle-count optimization, free Artistry/Chronicle progression, curator-control expansion, item UID identity loss, product scope opening, or PR81 contamination.
- [ ] **Step 5: Merge after exact-head validation under inherited same-approved-scope authority**.
- [ ] **Step 6: Postmerge read back new main and synchronize the same Decision ID to Google Sheet**.
