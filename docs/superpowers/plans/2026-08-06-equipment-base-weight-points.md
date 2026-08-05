# Equipment Base Weight Points Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize a 5-point equipment-group base-weight table and one explicit ±5 weight modifier into Blacksmith planning canon without changing product data or runtime code.

**Architecture:** Add Decision `BS-ITEM-20260806-01` as a focused refinement of the binary maximum-load gate. Base weight comes only from the existing equipment group, while an approved weight-specific enhancement can apply one additive `-5`, `0`, or `+5` modifier. The current product implementation remains blocked.

**Tech Stack:** Markdown planning canon, JSON registry, Python unittest contracts, GitHub Actions, Google Sheets authority mirror.

## Global Constraints

- Decision ID: `BS-ITEM-20260806-01`.
- Active batch: `R2_BATCH_005_5_OF_10`.
- Weight unit: integer `WEIGHT_POINT`.
- Base weights use only multiples of 5, including 0.
- Accessory 0; tool 5; clothing/robe 5; light armor 10; medium armor 20; heavy armor 30.
- Sword 10; axe 15; blunt 15; polearm 20; ranged 10; shield/support 10.
- `ITEM_WEIGHT = BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER` with final minimum 0.
- Explicit modifier values: `LIGHTWEIGHT -5`, `NONE 0`, `WEIGHTED +5`.
- At most one explicit weight modifier is active per item.
- Material, craftsmanship grade, artistry, attack, defense, handling, durability, and general enhancement level do not automatically change weight.
- Runtime, `data/crafting/weapon_bases.json`, scenes, images, and assets remain unchanged.
- Product implementation remains `BLOCKED`.

---

### Task 1: RED planning contract

**Files:**
- Create: `tests/test_r2_equipment_base_weight_points.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: current registry at batch 4/10 and the current simple-load canon.
- Produces: a failing contract requiring Decision `BS-ITEM-20260806-01`, batch 5/10, the exact table, and the explicit modifier guardrails.

- [x] Write tests for the active batch, exact base-weight table, additive modifier, no automatic material/stat/general-enhancement scaling, authority routing, and product blocking.
- [x] Add the test module to Planning-first workflow paths and unittest invocation.
- [x] Run Planning-first CI and verify failure because the Decision and canon do not exist.
- [x] Record the RED commit `eca4f5d5ec203db9e83fbe7d47f4b5bb8e3b3fff` and Planning-first run `190`.

### Task 2: GREEN focused canon and registry

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: the approved design spec and RED contract.
- Produces: machine-readable Decision `BS-ITEM-20260806-01` and the current base-weight mapping.

- [x] Add the new Decision and move the active batch from 4/10 to 5/10 without rewriting historical counters.
- [x] Store all twelve equipment-group base values exactly.
- [x] Store the modifier values, one-modifier limit, final minimum zero, and excluded automatic weight sources.
- [x] Register canon, spec, and plan as active authority documents.

### Task 3: Current authority and validator refinement

**Files:**
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `tests/test_base_v942_planning_first_adoption.py`
- Modify: existing R2 focused tests that assert the active batch.
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: the registry contract.
- Produces: one current 5/10 authority interpretation with older 1/10–4/10 markers retained as history.

- [x] Route total weight to base group weight plus one explicit modifier.
- [x] State that general enhancement levels and unrelated item stats do not change weight.
- [x] Add the player-facing `중량 N` and optional `경량화 -5` or `중량화 +5` reason-chip contract.
- [x] Update active-batch validators to 5/10 while retaining prior historical evidence.
- [x] Add the new canon to project and operating audits.

### Task 4: Verification, PR, and Sheet evidence

**Files:**
- Modify after verification: PR #109 body and Google Sheet authority rows.

**Interfaces:**
- Consumes: the final exact branch head and observed CI results.
- Produces: read-back evidence for the same Decision ID, table, exact head, and verification status.

- [ ] Run focused contracts and project-core alignment.
- [ ] Run Planning-first, Base adoption, Python full contracts, operating audit, and Godot 4.7.1 headless validation.
- [ ] Confirm `data/crafting/weapon_bases.json` and all protected product paths are unchanged.
- [ ] Confirm PR comments and unresolved review threads remain zero.
- [ ] Write the Decision and exact head to the six Sheet authority locations.
- [ ] Read back every written range.
- [ ] Update PR #109 while keeping it Draft and unmerged.
