# Godot AI 3.1.4 Current Vendor Alignment Design

## Status

- Decision: `BS-TOOLCHAIN-20260811-02`
- Scope: current toolchain/vendor authority alignment only
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`
- R3–R7 content counter: unchanged at `4/10`
- User direction: update the repository to Godot AI `3.1.4` and continue work.

## PRE_WORK_RESEARCH_PACKET

```yaml
checked_at_kst: 2026-08-11
base_main_sha: 7a49390bd840f5f5dc80fe661b44ad45e9ebeb7f
project_main_sha: eb5a43d3293290372a0ca2fe6ec107feef4cc6e5
open_pr_inventory: PR81_REFERENCE_ONLY_DO_NOT_MERGE
sheet_state: R3_R7_4_OF_10 / BS-CONTENT-20260811-04 / PRODUCT_IMPLEMENTATION_BLOCKED / TASK3_NOT_APPROVED
work_type: TECHNICAL_TOOLCHAIN_AUTHORITY_ALIGNMENT
benchmark_sources:
  - hi-godot/godot-ai official v3.1.4 release/tag
professional_or_official_sources:
  - official v3.1.4 tag commit 96cc8b8c3d25ce487e24801d01d5214fea150349
  - official plugin/addons/godot_ai tree 69010571e11123dfc4e09483f80cb9e6ca93511a
adopt:
  - exact official v3.1.4 vendor payload
  - release/tag/tree identity as version evidence
adapt:
  - current authority moves to 3.1.4 while completed Task2 execution history remains 3.1.3
  - retire the Task2-only Blacksmith set_main_scene vendor overlay from current upstream-exact vendor state
reject:
  - reverting the vendor to 3.1.3
  - blanket rewriting historical 3.1.3 Task2 evidence
  - re-forking official v3.1.4 solely to keep a completed-Task2-only mutation command alive
  - changing GUT or Hera authority
  - opening product or Task3 scope
differentiator:
  - current vendor identity and historical authoring-execution identity are recorded separately and mechanically validated
canon_conflict_check: CURRENT_CONFLICT_FOUND / payload=3.1.4 while policy/current tests/docs still assert 3.1.3
adversarial_precheck:
  - stale current-vs-history assertions
  - accidental vendor fork drift
  - loss of generic startup-execution denylist
  - accidental new authoring permission
  - direct-main update generated UID side effects
remaining_uncertainty:
  - no new persistent main-scene mutation route is authorized; future need requires a separate scoped Decision
```

## Fresh facts

The current Blacksmith `addons/godot_ai` subtree is byte-identical to the official Godot AI `v3.1.4` addon tree: both resolve to Git tree `69010571e11123dfc4e09483f80cb9e6ca93511a`.

The official `v3.1.4` release adds GridMap/CSG authoring, an Antigravity Windows launcher correction, and a startup handshake worker-slot fix. The Blacksmith direct-main update already contains those upstream bytes.

However, current project authority still records `3.1.3`, and the direct upstream sync removed a Blacksmith-only `set_main_scene` raw plugin command that had existed solely to complete Task2. Current main CI therefore fails old tests that treated that completed Task2 overlay as a permanent current-vendor requirement.

## Root cause

The failure is not a malformed 3.1.4 vendor update. The vendor payload itself is exact upstream.

The failure is a current/history contract mismatch:

1. `BS-TOOLCHAIN-20260809-01` and Task2 evidence correctly describe the historical 3.1.3 activation/execution baseline.
2. Task2 later added a narrow Blacksmith-only `set_main_scene` overlay on that vendor so `application/run/main_scene` could be set through a validated raw command while the generic settings route stayed denied.
3. Task2 is now proven complete and `project.godot` already points to `res://scenes/vertical_slice/main_menu.tscn`.
4. Official v3.1.4 replaced the vendor tree and therefore removed the project-only overlay.
5. Active tests still interpreted the historical overlay as a permanent current-vendor obligation.

## Approved current architecture

### Current vendor

```text
Godot AI current version: 3.1.4
upstream tag: v3.1.4
upstream tag commit: 96cc8b8c3d25ce487e24801d01d5214fea150349
upstream/current addon tree: 69010571e11123dfc4e09483f80cb9e6ca93511a
vendor alignment: EXACT_UPSTREAM_V3_1_4
```

The current vendor remains exact upstream. No Blacksmith patch is reapplied inside `addons/godot_ai` as part of this Decision.

### Historical Task2 authority

`BS-TOOLCHAIN-20260809-01`, `BS-HIGODOT-EXEC-20260808-01`, the Task2 bridge, its `3.1.3` runtime pin, and its `set_main_scene` proof remain historical evidence of the toolchain that actually authored/published Task2. They are not rewritten to pretend Task2 ran on 3.1.4.

### Main-scene posture

The current project already has:

```text
run/main_scene="res://scenes/vertical_slice/main_menu.tscn"
```

The generic upstream guard for `application/run/main_scene` must remain fail-closed. The retired Task2-only raw `set_main_scene` overlay is not reintroduced merely to keep an inactive historical mutation route alive.

If a future approved product task needs to mutate the persistent main scene again, that is a new authoring scope and requires its own scoped Decision/validation route.

## Authority invariants

- HiGodot remains the sole scoped Godot serialized authoring authority.
- Current production authoring scope remains closed beyond already completed Task2; no new Task is inferred.
- GUT remains `9.7.1` and sole GDScript test framework authority.
- Hera remains enabled but non-authoritative; authoring/mutation authority remains `NONE` unless separately scoped.
- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- R3–R7 remains `4/10`; this technical Decision does not increment content approval count.
- PR #81 remains reference-only and must not be merged.

## TDD contract

RED must prove the repository is in a split state: plugin bytes/version are already 3.1.4 while current policy/Decision surfaces still claim 3.1.3, and existing current runtime tests still demand the removed Task2-only overlay.

GREEN must:

- create `BS-TOOLCHAIN-20260811-02`;
- record `3.1.4` as the current installed vendor version;
- record official tag/commit/tree identity;
- preserve the historical 3.1.3 Task2 execution identity;
- update current runtime/sync contracts to distinguish current upstream vendor from historical Task2 overlay;
- prove generic startup-execution protection remains present;
- prove current `project.godot` already points to the approved MainMenu;
- keep all product/Task3 gates closed.

## Non-goals

This change does not:

- edit `project.godot`, `.tscn`, `.tres`, or `.res` product serialization;
- re-run or rewrite historical Task2 PROVE evidence;
- reopen the Task2 authoring bridge as a new current authoring workflow;
- add a new MCP tool or raw command;
- alter GUT/Hera authority;
- advance R3–R7 content beyond `4/10`;
- authorize Task3 or general product implementation.
