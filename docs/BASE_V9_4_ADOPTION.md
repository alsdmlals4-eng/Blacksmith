# Blacksmith Base v9.4 Adoption State

- Current operating Decision: `BS-OPS-20260802-01`
- Base repository: `alsdmlals4-eng/Base`
- Released version: `9.4.0`
- Release commit: `a728712cb776ec98f4875914a580fcf7d0156593`
- Release evidence commit: `ef1fba11167e4da0b298123b0c85ebd268191a42`
- Blacksmith recovery base: `main@ac120fb146cea29bb5f8876682809f76779d86ad`

## Status Separation

```yaml
BASE_RELEASE_ADOPTION: COMPLETE
PROJECT_CANONICAL_RECOVERY: IN_PROGRESS
GDD_SHEET_BINDING: SYNC_IN_PROGRESS_BS-OPS-20260802-01
PROJECT_SKILL_ROUTING: UPDATED / STATIC_VALIDATION_NOT_RUN
GENERATED_COMPATIBILITY_VIEWS: BLOCKED_UNVERIFIED
LATEST_PLANNING_RUNTIME_VALIDATION: NOT_RUN
ANDROID_DEVICE_VALIDATION: NOT_RUN
ACCESSIBILITY_HUMAN_REVIEW: NOT_RUN
PERFORMANCE_PROFILE: NOT_RUN
HUMAN_PLAYTEST: NOT_RUN
```

Base v9.4 adoption means the released Base payload and project adapter structure were merged into Blacksmith. It does not mean Blacksmith's active planning entrypoints, Google Sheet, product scenes, Android behavior, accessibility, performance, or player experience are complete.

## Current Canonical Inputs

- `skills/PROJECT_BASE_ADAPTER.json`
- `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`
- `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`
- `CURRENT_CONFIRMED_DECISIONS.md`
- `AGENTS.md`
- `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`

## Sheet Binding

- Spreadsheet: `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`
- Role: `USER_FACING_GDD_WORKSPACE`
- Authority: GitHub canon
- Current sync Decision: `BS-OPS-20260802-01`
- Target tabs: `00`, `01`, `02`, `04`, `05`, `90`, `99`
- Current status: `WRITE_AND_READBACK_PENDING`

Sheet values that still route through Base v9.3, PR #61/#62, or PR #81 as the active work path are stale operating references and must be corrected. Historical evidence remains in `99_변경이력`.

## Selective Skill Routing

- `load_all_skills=false`
- `default_selection=automatic-trigger-match`
- one primary discipline Skill per step
- common Base foundation routes are selected by current responsibility
- Blacksmith-specific game-design, engineering, and QA skills retain project paths and terminology
- engineering implementation is currently blocked by planning gates

No new recovery-specific project Skill is required. The work is covered by existing operating, game-design, QA, and Superpowers contracts.

## Compatibility Views

`skills/BASE_V9_ADAPTER.json` and `skills/PROJECT_BASE_SKILL_ADAPTER.json` are compatibility views with archived legacy inputs. This connector-only session did not run the approved generator or local validators.

Therefore:

```yaml
COMPATIBILITY_VIEW_GENERATION: NOT_RUN
COMPATIBILITY_VIEW_FRESHNESS: BLOCKED_UNVERIFIED
MANUAL_VIEW_EDIT: PROHIBITED
```

This state must not be reported as full adapter synchronization.

## Protected Product Baseline

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

The recovery branch may inspect these paths but must not modify them. Current `project.godot` still starts `res://scenes/test/enhancement_test.tscn`; that implementation fact is separate from the approved future main-menu and app-shell contracts.

## Validators

Configured commands:

```bash
python tools/check_archive_governance.py
python -m unittest tests.test_archive_retention_governance -v
python tools/audit_project_operating_system.py
```

Current execution status: `NOT_RUN_IN_CONNECTOR_ONLY_SESSION`.

Manual validation lanes remain:

- Godot project parse and runtime
- Android device and safe area
- UX/UI human understanding and accessibility
- representative and worst-scene performance
- external human play

All remain `NOT_RUN`.

## Completion Boundary

Base adoption can remain `COMPLETE` while project canonical recovery is `IN_PROGRESS`. R0 recovery closes only after:

1. current entrypoints, registries, adapter, and health agree;
2. `BS-OPS-20260802-01` is written to and read back from the Sheet;
3. Issue #60/#79 and PR #81/#84 authority is unambiguous;
4. final branch diff changes no protected product paths;
5. operating adversarial review has no unresolved `MUST_FIX`;
6. exact final HEAD evidence is recorded.

Even after R0 closes, product implementation and product validation remain blocked until the full planning and review gate is approved.
