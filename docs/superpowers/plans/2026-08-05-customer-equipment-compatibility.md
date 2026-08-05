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

## Task 4 — Sheet sync

Write `BS-CUSTOMER-20260805-01` as `APPROVED_PENDING_MERGE` to current decisions, audit, GDD summary, core systems, and change history. Record the exact PR head. Do not claim `SYNCED_TO_MAIN` before merge and post-merge readback.
