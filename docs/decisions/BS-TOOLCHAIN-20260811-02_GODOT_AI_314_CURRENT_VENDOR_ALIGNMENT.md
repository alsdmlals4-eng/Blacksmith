# BS-TOOLCHAIN-20260811-02 — Godot AI 3.1.4 Current Vendor Alignment

## Decision

`BS-TOOLCHAIN-20260811-02 / GODOT_AI_314_CURRENT_VENDOR_ALIGNMENT`

User-approved current toolchain alignment:

```text
CURRENT_GODOT_AI_VERSION: 3.1.4
UPSTREAM_TAG: v3.1.4
UPSTREAM_TAG_COMMIT: 96cc8b8c3d25ce487e24801d01d5214fea150349
UPSTREAM_VENDOR_TREE_SHA: 69010571e11123dfc4e09483f80cb9e6ca93511a
VENDOR_ALIGNMENT: EXACT_UPSTREAM_V3_1_4
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
R3_R7_APPROVAL_COUNTER: 4/10
```

The Blacksmith `addons/godot_ai` tree observed on main `eb5a43d3293290372a0ca2fe6ec107feef4cc6e5` is byte-identical to the official v3.1.4 `plugin/addons/godot_ai` tree. The direct vendor update is therefore accepted as the current vendor payload rather than reverted or re-patched.

## Refines, does not rewrite

This Decision refines current version authority after:

- `BS-TOOLCHAIN-20260809-01` — Godot AI 3.1.3 + GUT/Hera editor-plugin activation baseline.
- `BS-HIGODOT-EXEC-20260808-01` — completed Task2 production authoring/provenance, including the Task2-only validated `set_main_scene` adapter that existed on the 3.1.3 vendor.

Those Decisions remain truthful historical evidence. Task2 actually ran on the 3.1.3 execution stack and is not relabeled as a 3.1.4 execution.

## Current-vs-history split

### Current

- Godot AI vendor: `3.1.4`.
- Vendor posture: exact official upstream v3.1.4 addon tree.
- Generic upstream startup-execution guard remains active for `application/run/main_scene`.
- Current project main scene is already `res://scenes/vertical_slice/main_menu.tscn`.
- No current raw `set_main_scene` Blacksmith overlay is exposed.

### Historical Task2

- Historical Task2 toolchain version remains `3.1.3`.
- Historical Task2 bridge/workflow/recipe/provenance remain frozen evidence.
- The project-only `set_main_scene` vendor overlay is `HISTORICAL_PROVEN_RETIRED_FROM_CURRENT_VENDOR` after Task2 completion.
- This retirement does not invalidate already-published Task2 serialized bytes or provenance.

A future persistent main-scene mutation is not inferred from the old Task2 permission. It is `NEW_SCOPE_DECISION_REQUIRED`.

## Upstream 3.1.4 changes adopted

The official v3.1.4 payload includes:

- GridMap authoring support;
- CSG authoring support;
- Antigravity Windows launcher correction;
- startup handshake worker-slot correction.

Presence of these capabilities in the vendor does not itself authorize Blacksmith product mutation. Project authoring authority and product gates still control whether a capability may be used.

## Authority invariants

- HiGodot/Godot AI remains the sole scoped Godot serialized authoring authority.
- Existing Task2 scope is complete; no new production authoring task is inferred.
- GUT remains `9.7.1` and `SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY`.
- Hera remains enabled non-authoritative with authoring/mutation authority `NONE` unless separately scoped.
- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- R3–R7 remains `4/10`; this technical Decision does not consume a content approval slot.
- PR #81 remains `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT`.

## TDD and regression evidence target

RED was established on PR #149 at head `083acaaec3e2dfdb554639f75035206be9d79e82`:

- the new 3.1.4 contract proved the plugin itself was already `3.1.4`;
- it failed because this Decision did not yet exist;
- it failed because current authority policy did not yet contain this Decision/current 3.1.4 metadata;
- existing main validation independently failed because stale runtime contracts still required the removed Task2-only raw `set_main_scene` overlay.

GREEN must update current policy/current consumers without rewriting historical Task2 3.1.3 evidence and without modifying product serialized surfaces.

## Research disposition

- `ADOPT`: exact official v3.1.4 vendor payload and official tag/tree identity.
- `ADAPT`: separate current vendor version from historical Task2 execution version.
- `REJECT`: revert to 3.1.3, blanket-rewrite historical evidence, or re-fork v3.1.4 only to preserve a completed-task-only command.
- `DIFFERENTIATOR`: Blacksmith records current vendor identity and historical authoring provenance independently, so upgrades do not falsify prior execution evidence.

## Scope closure

This Decision authorizes only the current toolchain alignment requested by the user. It does not authorize product code/content implementation, Task3, new serialized authoring, new GridMap/CSG product work, or R3–R7 Decision 5/10.
