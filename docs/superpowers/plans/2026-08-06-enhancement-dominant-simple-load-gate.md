# Enhancement-Dominant Simple Load Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize the approved binary strength-based load gate and enhancement-dominant success preset into Blacksmith planning canon without implementing product code.

**Architecture:** Add one focused Decision that refines the previous customer-equipment and mobile-card contracts. Current authority documents use `MAXIMUM_LOAD / LOAD_STATUS`, while the older `COMFORTABLE_LOAD / BALANCE_STATE` load model remains visible only as historical superseded text. All product runtime, scenes, game data, and assets remain untouched.

**Tech Stack:** Markdown planning canon, JSON registry, Python unittest contracts, GitHub Actions, Google Sheets authority mirror.

## Global Constraints

- Decision ID: `BS-CUSTOMER-20260806-01`.
- Active batch: `R2_BATCH_005_4_OF_10`.
- Maximum load: `STRENGTH × 10 WEIGHT_POINT`.
- Load states: `WITHIN_LIMIT / OVERWEIGHT`.
- `WITHIN_LIMIT` has no weight bonus or penalty.
- `OVERWEIGHT` blocks assignment.
- Enhancement level contributes `+1 percentage point per level` to the baseline event forecast.
- Customer stat and proficiency remain small auxiliary modifiers.
- Product implementation remains `BLOCKED`.
- Do not modify runtime, scenes, game data, images, or animation HX.

---

### Task 1: RED planning contract

**Files:**
- Create: `tests/test_r2_enhancement_dominant_simple_load_gate.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: current R2 registry and authority documents at batch 3/10.
- Produces: a failing contract requiring the new Decision and simplified load/success rules.

- [x] Write tests for batch 4/10, the binary load gate, enhancement-dominant forecast, document routing, and product blocking.
- [x] Add the test module to Planning-first CI.
- [x] Run CI and observe failure because the Decision and current authority do not exist.
- [x] Record RED commit `b38562012620383da7ec442d1579ed554966f974` and Planning-first run `173`.

### Task 2: GREEN focused canon and registry

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: approved design spec and RED contract.
- Produces: Decision `BS-CUSTOMER-20260806-01` and machine-readable current rules.

- [x] Add the new Decision with `BINARY_MAXIMUM_LOAD_GATE`.
- [x] Move active batch from 3/10 to 4/10 without rewriting historical Decision counters.
- [x] Record the load formula, status model, forecast formula, small modifiers, and special-function requirement gate.
- [x] Register the canon, design, and plan documents as ACTIVE.

### Task 3: Current authority and validator refinement

**Files:**
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `tests/test_base_v942_planning_first_adoption.py`
- Modify: `tests/test_r2_artistry_generation_growth_economy.py`
- Modify: `tests/test_r2_customer_equipment_compatibility.py`
- Modify: `tests/test_r2_mobile_customer_card_progressive_disclosure.py`
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: current Decision contract.
- Produces: one current active interpretation and no stale active 3/10 or four-state load assertions.

- [x] Route current load terminology to `TOTAL_WEIGHT / MAXIMUM_LOAD / LOAD_STATUS`.
- [x] Mark `COMFORTABLE_LOAD / BALANCE_STATE` and escalating overload penalties `HISTORICAL_SUPERSEDED` for load handling.
- [x] Update mobile disclosure to show `총 중량 / 최대 중량` and binary usability.
- [x] State that enhancement is the primary controllable success modifier.
- [x] Update active batch assertions to 4/10 while preserving historical 1/10, 2/10, and 3/10 markers.
- [x] Add the new canon to project and operating audits.

### Task 4: Verification, PR, and Sheet evidence

**Files:**
- Modify after verification: PR #109 body and Google Sheet authority rows.

**Interfaces:**
- Consumes: final exact branch head and observed CI results.
- Produces: read-back evidence for the same Decision ID and commit.

- [x] Run focused Planning-first contracts and project-core alignment.
- [ ] Run Base adoption, Python full contracts, operating audit, and Godot 4.7.1 headless validation.
- [ ] Confirm protected product path changes remain zero.
- [ ] Confirm PR comments and unresolved review threads remain zero.
- [ ] Write Decision `BS-CUSTOMER-20260806-01`, batch 4/10, exact head, and CI results to the six Sheet authority locations.
- [ ] Read back all written Sheet ranges.
- [ ] Update PR #109 while keeping it Draft and unmerged.

## Intermediate GREEN evidence

- Canon synchronization commit: `12fe01e9e821146eebf8edb175750d9fda35a9f1`.
- Focused contracts: `34 tests PASS`.
- Project core alignment: `PASS`.
- One-shot synchronizer and workflow were removed from the GREEN result commit.
- This user-authored update triggers final exact-head Planning-first, Base, Python/operating-audit, and Godot validation. Sheet and PR final evidence remain pending until those runs complete.
