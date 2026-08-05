# Customer Capability and Equipment Compatibility Canon Plan

> Execute planning-only canon synchronization for approved Decision `BS-CUSTOMER-20260805-01`. Product implementation stays blocked.

## Task 1 — RED contract

- Add `tests/test_r2_customer_equipment_compatibility.py`.
- Add the test to planning-first CI.
- Verify failure while Decision ID, canon file, batch 2/10, and authority tokens are absent.

## Task 2 — GREEN authority sync

- Create the focused customer/equipment canon and design spec.
- Add the Decision to `CURRENT_R2_CANON_REGISTRY.json`.
- Move `R2_BATCH_005` from 1/10 to 2/10.
- Update Current Decisions, Current Game Bible, Active Context, Roadmap, Development Gates, Start Here, Documentation Map, and Design Document Registry.
- Mark the older customer schedule canon as retained for schedule behavior but refined for capability structure.

## Task 3 — Regression and adversarial review

- Run focused planning-first contract tests.
- Run Base adoption, Python project contract, Godot headless, and PR validation workflows.
- Confirm product paths remain unchanged.
- Check PR diff, review threads, stale authority tokens, and Sheet readback.
- Confirm the customer model improves equipment-selection judgment without becoming a separate customer-RPG progression loop.
- Confirm raw item power remains owned by the item UID and is not counted again through customer stats or proficiency.
- Resolve the inherited visitor-archetype identifier drift by refining `SKILL` to the canonical `DEXTERITY` identifier while retaining the Korean label `기량`.
- Restore batch-specific validation semantics: the first artistry Decision keeps its historical `1/10` marker while active authority documents require the current `2/10` counter, without contradictory forbidden tokens.

## Task 4 — Sheet sync

Write `BS-CUSTOMER-20260805-01` as `APPROVED_PENDING_MERGE` to current decisions, audit, GDD summary, core systems, and change history. Record the exact PR head. Do not claim `SYNCED_TO_MAIN` before merge and post-merge readback.

## Task 5 — Final exact-head evidence

- Re-run all required workflows from a user-authored exact head after structural synchronization.
- Record observed run IDs and conclusions; do not treat `action_required` from an automation-authored head as a content test result.
- Update PR evidence and Google Sheet locations only after the exact-head checks complete.
