# Blacksmith HiGodot Validated Main Scene Command Design

Decision: `BS-HIGODOT-EXEC-20260808-01`

Date: `2026-08-09 KST`

Status: `USER_APPROVED_DESIGN / WRITTEN_SPEC_REVIEW_APPROVED`

## Problem

Manual HiGodot Task 2 PROVE attempt #2 ran on PR #131 at exact input head `467d1e2eab3c7de707ba83b3c79fef1f0a62b55f` as GitHub Actions run `31314172410`.

The run proved that the prior editor-session readiness race was fixed. A live Blacksmith Godot 4.7.1 editor session registered, HiGodot/Godot AI 3.1.3 activated the exact project session, and the approved Task 2 recipe successfully authored and saved the three approved scenes inside the ephemeral Actions runner.

The final recipe operation then failed before provenance and guarded PUBLISH:

```text
project_manage(op="settings_set", key="application/run/main_scene")
VALUE_OUT_OF_RANGE: Refusing to set 'application/run/main_scene' — this key controls what the engine loads or executes at project startup.
```

The runner-authored scenes were not published to the PR branch. `project.godot` and the three Task 2 `.tscn` outputs remain unpublished on PR #131.

## Upstream safety contract

Pinned HiGodot/Godot AI `v3.1.3` deliberately treats `application/run/main_scene` as a protected startup-execution setting. The generic `set_project_setting` path must continue to reject this key.

The same upstream design uses dedicated validated commands for protected startup surfaces when a legitimate authoring route exists, for example `autoload_manage(op="add")` rather than relaxing generic settings writes.

The pinned Python MCP server `v3.1.3` does not expose a dedicated persistent main-scene setter. It does expose `batch_execute`, whose sub-commands are raw plugin command names dispatched by the connected Godot plugin.

## Approved approach

Preserve the generic startup-execution denylist and add one narrowly scoped **plugin command** for persistent main-scene selection.

The command will be named:

```text
set_main_scene
```

It will live in the existing project handler and be registered with the plugin dispatcher. The pinned Python MCP server remains byte-for-byte upstream-compatible at `3.1.3`; no server package fork or tool-schema expansion is required.

The Task 2 recipe will invoke the new plugin command through the already-existing upstream MCP tool:

```text
batch_execute(
  commands=[
    {
      "command": "set_main_scene",
      "params": {"scene": "res://scenes/vertical_slice/main_menu.tscn"}
    }
  ],
  undo=false
)
```

Using a single-command `batch_execute` keeps the MCP surface pinned to the official 3.1.3 server while still routing the mutation through the live HiGodot editor plugin.

## Security and validation contract

`set_main_scene` must fail closed unless every condition below is true:

1. `scene` is present and is a non-empty string.
2. The path is a confined `res://` project path. `uid://`, `user://`, absolute paths, traversal (`..`), null bytes, and paths outside the project are rejected.
3. The path extension is exactly `.tscn` case-insensitively.
4. The target file/resource exists as a loadable scene before any ProjectSettings mutation.
5. The command may mutate only `application/run/main_scene`.
6. The existing `STARTUP_EXECUTION_KEYS_EXACT` denylist entry for `application/run/main_scene` remains unchanged, so generic `set_project_setting` continues to reject it.
7. `ProjectSettings.save()` failure restores the previous in-memory value and returns an error.
8. The response reports the exact key, old value, new value, `undoable=false`, and a reason identifying the dedicated validated route.
9. No direct text/filesystem write to `project.godot` is introduced.
10. No workflow trigger broadening, force push/rebase, blind mutation retry, or PR #131 merge is authorized.

## Bridge and recipe contract

`tools/higodot_task2_bridge.py` must recognize exactly one main-scene authoring operation in the executable recipe, and that operation must have the exact shape:

```text
tool = batch_execute
undo = false
commands = [
  {
    command = set_main_scene
    params.scene = res://scenes/vertical_slice/main_menu.tscn
  }
]
```

No other raw plugin sub-command is approved through `batch_execute` for Task 2.

The prior generic `project_manage(settings_set)` recipe route becomes invalid for Task 2. `project_manage(settings_get)` remains the read-only preflight/readback authority.

If the `batch_execute(set_main_scene)` call ends in timeout/connection ambiguity, the bridge must perform exactly one read-only `project_manage(settings_get)` readback for `application/run/main_scene` and then fail closed with `AmbiguousMutationError`. It must never blindly retry the mutation.

The existing four-file serialized allowlist remains exactly:

```text
project.godot
scenes/vertical_slice/main_menu.tscn
scenes/vertical_slice/vertical_slice_app.tscn
scenes/vertical_slice/screens/vs_workshop_screen.tscn
```

`verify_project_setting_delta()` remains the final guard that proves `project.godot` changed only at `run/main_scene` and that the resulting value points to the approved MainMenu.

## TDD contract

Implementation must follow RED -> GREEN.

### Plugin command tests

Add focused coverage that proves:

- generic `set_project_setting` still rejects `application/run/main_scene`;
- valid confined existing `.tscn` is accepted by the dedicated route;
- missing `scene` is rejected;
- non-`res://` paths are rejected;
- traversal is rejected;
- non-`.tscn` paths are rejected;
- missing/non-loadable scene is rejected;
- save failure restores the old ProjectSettings value;
- dispatcher registration exposes `set_main_scene` as a plugin command without adding a new MCP tool to the catalog.

### Task 2 bridge tests

Add or update focused Python tests that prove:

- the approved recipe uses only the exact one-command `batch_execute(set_main_scene)` shape;
- `batch_execute` is otherwise rejected as a generic escape hatch;
- the old `project_manage(settings_set)` recipe shape is rejected;
- required MCP tools include `batch_execute` and retain read-only `project_manage` for preflight/readback;
- ambiguity after `set_main_scene` performs one main-scene readback and raises without retry;
- existing serialized allowlist, provenance, and exact-head contracts remain unchanged.

## Validation before another manual PROVE

Before asking the user to dispatch again:

1. focused plugin command/security tests GREEN;
2. focused Task 2 MCP driver/bridge tests GREEN;
3. approved editor-plugin synchronization/toolchain contracts GREEN;
4. exact branch head read back from GitHub;
5. all applicable remote CI read back on that exact head;
6. Google Sheet synchronized under `BS-HIGODOT-EXEC-20260808-01`;
7. only then provide one new exact `expected_head_sha` for manual `HiGodot Task 2 Authoring Bridge` dispatch.

A successful PROVE must still pass exact serialized diff validation, Godot import/smoke, GUT 9.7.1, Task 1 regressions, model/integration checks, provenance creation/upload, exact-head race check, and guarded byte-identical PUBLISH.

## Non-goals

This change does not:

- remove or weaken the upstream generic startup-execution denylist;
- make Hera an authoring authority;
- change HiGodot `3.1.3`, Godot `4.7.1-stable`, GUT `9.7.1`, or toolchain pins;
- directly edit `project.godot` or Task 2 `.tscn` product files outside live HiGodot authoring;
- add a general arbitrary ProjectSettings write escape hatch;
- broaden authoring permissions beyond the approved Task 2 main scene;
- publish any serialized output before real PROVE succeeds;
- merge PR #131.

## Rollback

If the dedicated command or bridge integration fails validation, revert only the command/dispatcher/bridge/recipe/test changes. The generic denylist remains intact, the manual workflow stays fail-closed, and PR #131 remains Draft and unmerged.