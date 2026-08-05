# Mobile Customer Card Progressive Disclosure Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize the approved three-layer mobile customer card information hierarchy into Blacksmith canon without implementing product UI.

**Architecture:** Store the user-approved UX contract as a focused Decision and canon document, then route it through the current R2 Registry, Game Bible, project hub, validators, PR evidence, and Google Sheet. The mobile and future PC surfaces share one information hierarchy; platform-specific layout remains a later visual/implementation concern.

**Tech Stack:** Markdown canon and design documents, JSON registries, Python unittest contracts, GitHub Actions, Google Sheets authority mirror.

## Global Constraints

- Decision ID: `BS-UX-20260805-01`.
- Active batch: `R2_BATCH_005_3_OF_10`.
- Product implementation remains `BLOCKED`.
- Use RED → GREEN → REFACTOR evidence.
- Preserve historical 1/10 and 2/10 Decision markers; only active authority becomes 3/10.
- Do not change runtime, scenes, game data, images, or animation HX.

---

### Task 1: RED planning contract

**Files:**
- Create: `tests/test_r2_mobile_customer_card_progressive_disclosure.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: current R2 Registry and current authority documents.
- Produces: a failing contract requiring Decision `BS-UX-20260805-01` and batch 3/10.

- [x] Write the failing contract for the three layers, accessibility rules, and authority documents.
- [x] Add the test to Planning-first CI.
- [x] Run Planning-first and observe failure while the Decision is absent.
- [x] Record RED commit `e5d531417da28a12c687bfefb5cda0f624d69f40` and run `161`.

### Task 2: GREEN focused canon and registry

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`
- Create: `docs/superpowers/specs/2026-08-05-mobile-customer-card-progressive-disclosure-design.md`
- Create: `docs/superpowers/plans/2026-08-05-mobile-customer-card-progressive-disclosure.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: customer capability/equipment compatibility and success-disclosure Decisions.
- Produces: canonical three-layer UX contract and machine-readable Decision fields.

- [x] Add Decision `BS-UX-20260805-01` with `THREE_LAYER_PROGRESSIVE_DISCLOSURE`.
- [x] Move active batch from 2/10 to 3/10 without rewriting historical Decision counters.
- [x] Record default, post-equipment, detail, accessibility, and PC-adaptation contracts.
- [x] Register the canon, design, and plan documents.

### Task 3: Authority and validator synchronization

**Files:**
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `tests/test_base_v942_planning_first_adoption.py`
- Modify: `tests/test_r2_artistry_generation_growth_economy.py`
- Modify: `tests/test_r2_customer_equipment_compatibility.py`
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: focused canon and registry Decision.
- Produces: consistent active authority and no stale active 2/10 assertions.

- [x] Add current Decision summaries and core-fun protection.
- [x] Update active batch assertions to 3/10.
- [x] Keep `BS-CRAFT-20260805-02` at historical 1/10 and `BS-CUSTOMER-20260805-01` at historical 2/10.
- [x] Add focused canon assertions to project and operating audits.

### Task 4: Verification, PR, and Sheet evidence

**Files:**
- Modify after verification: PR #109 body and Google Sheet authority rows.

**Interfaces:**
- Consumes: final exact branch head and observed CI results.
- Produces: read-back evidence for the same Decision ID and commit.

- [ ] Run Planning-first, Base adoption, Python full contracts, operating audit, and Godot 4.7.1 headless.
- [ ] Confirm protected product path changes remain zero.
- [ ] Confirm PR comments and unresolved review threads remain zero.
- [ ] Write Decision `BS-UX-20260805-01`, batch 3/10, exact head, and CI results to Sheet.
- [ ] Read back all Sheet ranges.
- [ ] Update PR #109 while keeping Draft and unmerged.

## Intermediate GREEN evidence

- One-shot canon synchronization commit: `0c672f98f0c3bb25fc2c48826f215dc9b24e106f`.
- Focused contract suite: 29 tests PASS.
- Project core alignment: PASS after repairing the remaining active-batch validator tokens.
- Automation-authored-head workflows `166 / 653 / 1244` returned `action_required`; they are not content test results.
- User-authored head `b11940496e78cf8584f58420100a3d0e512f5416`: Planning-first `167` PASS and Base `654` PASS.
- PR validation `1245` exposed one remaining operating-audit assertion for `DEVELOPMENT_GATES`; this is observed RED evidence, not a product failure.
- Focused audit repair commit: `7164d7e72db77c206003e46a8e62d341441f9edb`.
- This user-authored commit triggers the final post-repair exact-head CI. Final Sheet and PR evidence remains pending until those runs complete.
