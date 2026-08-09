# Blacksmith HiGodot Validated Main Scene Command Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the incompatible Task 2 generic `project_manage(settings_set)` main-scene write with one fail-closed HiGodot plugin command, while preserving the upstream 3.1.3 startup-execution denylist, the official Python MCP server surface, exact four-file serialized allowlist, provenance/race guards, and PR #131 Draft/unmerged state.

**Architecture:** Add a raw Godot-plugin command `set_main_scene` to the existing project handler and dispatcher. The command validates a confined existing `res://... .tscn`, persists only `application/run/main_scene`, and rolls back the in-memory ProjectSettings value if persistence fails. The Task 2 bridge invokes that raw command only through the already-pinned upstream `batch_execute` MCP tool using one exact approved command shape with `undo=false`; all other `batch_execute` shapes remain rejected. Read-only `project_manage(settings_get)` remains the preflight and ambiguity-readback path.

**Tech Stack:** Godot 4.7.1 stable, GDScript editor plugin, HiGodot/Godot AI 3.1.3, Python 3.12 bridge/tests, pytest, GUT 9.7.1 project test authority, GitHub Actions, Google Sheets project canon.

**Decision:** `BS-HIGODOT-EXEC-20260808-01`

**Approved spec:** `docs/superpowers/specs/2026-08-09-blacksmith-higodot-main-scene-command-design.md`

**Protected constraints:**

- Do not remove `application/run/main_scene` from `STARTUP_EXECUTION_KEYS_EXACT`.
- Do not add a new Python MCP tool or fork the pinned 3.1.3 server.
- Do not directly write `project.godot` or Task 2 `.tscn` product files outside live HiGodot authoring.
- Do not broaden workflow triggers.
- Do not force-push/rebase the PR branch.
- Do not merge PR #131 without separate explicit approval.
- Keep PR head SHA and GitHub test-merge SHA as separate evidence values.

---

## Task 1: Write the plugin-command/security RED

**Files:**
- Create: `tests/unit/test_higodot_main_scene_command.gd`
- Modify: `.github/workflows/godot-validation.yml`
- Modify: `tests/test_user_approved_editor_plugin_runtime_contract.py`

### Step 1: Add the focused GDScript RED

Create a SceneTree-style headless test matching the repository's existing `tests/unit/*.gd` pattern. The test must load `addons/godot_ai/handlers/project_handler.gd` and prove the following contract before production code exists:

1. `ProjectHandler.startup_execution_key_refusal("application/run/main_scene")` remains non-empty.
2. The new `set_main_scene` method is expected to exist.
3. missing/empty `scene` fails closed;
4. `uid://`, `user://`, absolute paths, and `res://../...` traversal fail closed;
5. non-`.tscn` paths fail closed;
6. missing or non-`PackedScene` resources fail closed;
7. an existing confined `.tscn` can be accepted through the dedicated route;
8. an injected save failure restores the old `application/run/main_scene` in memory.

The test must restore any ProjectSettings value it temporarily changes before quitting. It must not rely on a real `project.godot` disk mutation to prove save-failure rollback.

### Step 2: Add a test-only persistence seam expectation

The RED should instantiate the handler with an optional `Callable` used only for ProjectSettings persistence in tests. Production construction with the existing three arguments must remain valid.

Target production seam expected by the test:

```gdscript
var _project_settings_save: Callable = Callable()

func _save_project_settings() -> int:
    if _project_settings_save.is_valid():
        return int(_project_settings_save.call())
    return ProjectSettings.save()
```

Do not implement this in Task 1.

### Step 3: Wire the new headless test into the existing Godot workflow

Add a run step to `.github/workflows/godot-validation.yml` that executes only the new test script with the already-downloaded Godot 4.7.1 binary. Do not change `on:` triggers, permissions, or any authoring workflow.

Expected command shape in CI:

```bash
./Godot_v4.7.1-stable_linux.x86_64 --headless --path . --script res://tests/unit/test_higodot_main_scene_command.gd
```

### Step 4: Extend the static editor-plugin contract

Update `tests/test_user_approved_editor_plugin_runtime_contract.py` so the desired raw dispatcher registration is required, while the tool catalog is required to remain without a new `set_main_scene` MCP tool.

Required assertions after GREEN should include:

```text
plugin.gd registers raw command set_main_scene -> project handler
project_handler.gd keeps application/run/main_scene in startup denylist
tool_catalog.gd project domain remains project_manage + project_run only
```

### Step 5: Run/observe RED

Focused commands:

```bash
python -m pytest tests/test_user_approved_editor_plugin_runtime_contract.py -q
```

and the new Godot script in `godot-validation.yml`.

**Expected RED:** failures must be attributable to the absent `set_main_scene` handler/dispatcher/persistence seam, not to unrelated Task 2 serialized files.

### Step 6: Commit RED only

```bash
git add tests/unit/test_higodot_main_scene_command.gd .github/workflows/godot-validation.yml tests/test_user_approved_editor_plugin_runtime_contract.py
git commit -m "test: cover validated HiGodot main-scene command"
```

Do not modify `project_handler.gd`, `plugin.gd`, bridge code, recipe, or product serialized files in this commit.

---

## Task 2: Implement the narrow plugin command GREEN

**Files:**
- Modify: `addons/godot_ai/handlers/project_handler.gd`
- Modify: `addons/godot_ai/plugin.gd`
- Test: `tests/unit/test_higodot_main_scene_command.gd`
- Test: `tests/test_user_approved_editor_plugin_runtime_contract.py`

### Step 1: Add the optional save seam without changing production behavior

Extend the existing project-handler constructor with one optional `Callable = Callable()` argument. Existing three-argument production construction must remain source-compatible.

Route both the existing generic setting writer and the new dedicated writer through `_save_project_settings()` so failure rollback can be deterministically tested. With no injected callable, `_save_project_settings()` must call `ProjectSettings.save()` exactly as before.

### Step 2: Implement `set_main_scene(params)`

The command must validate before mutation, in this order:

```text
scene param exists and TYPE_STRING
→ strip edges and require non-empty
→ McpPathValidator.path_error(scene, "scene") == null
→ extension lowercased == "tscn"
→ ResourceLoader.exists(scene)
→ ResourceLoader.load(scene, "PackedScene") returns PackedScene
→ capture old main_scene value
→ set only application/run/main_scene
→ persist through _save_project_settings()
→ on failure restore old value/clear new value and return INTERNAL_ERROR
→ on success return exact old/new/key/undoable=false/reason data
```

The method must not call `set_project_setting()`, because that generic method must continue refusing `application/run/main_scene` by design.

Recommended success payload shape:

```gdscript
{
    "data": {
        "key": "application/run/main_scene",
        "old_value": NodeHandler._serialize_value(old_value),
        "value": scene,
        "type": "String",
        "undoable": false,
        "reason": "Dedicated validated main-scene route",
    }
}
```

### Step 3: Register only a raw dispatcher command

In `addons/godot_ai/plugin.gd` add:

```gdscript
_dispatcher.register_lazy("set_main_scene", "project", &"set_main_scene")
```

Do not add it to `addons/godot_ai/tool_catalog.gd`. Do not add a Python `@mcp.tool`.

### Step 4: Run focused GREEN

Run/observe:

```bash
python -m pytest tests/test_user_approved_editor_plugin_runtime_contract.py -q
./Godot_v4.7.1-stable_linux.x86_64 --headless --path . --script res://tests/unit/test_higodot_main_scene_command.gd
```

Then run the pre-existing Godot headless scripts from `godot-validation.yml` to ensure the new handler constructor and dispatcher registration do not regress existing engine tests.

**Expected GREEN:** all focused plugin/security tests pass; generic main-scene settings write is still refused.

### Step 5: Commit GREEN

```bash
git add addons/godot_ai/handlers/project_handler.gd addons/godot_ai/plugin.gd
git commit -m "feat: add validated HiGodot main-scene command"
```

---

## Task 3: Write bridge/recipe exact-shape RED

**Files:**
- Modify: `tests/test_higodot_task2_mcp_driver.py`

### Step 1: Require the new final recipe shape

Add tests that require exactly one main-scene write represented as:

```python
{
    "tool": "batch_execute",
    "arguments": {
        "commands": [
            {
                "command": "set_main_scene",
                "params": {"scene": EXPECTED_MAIN_SCENE},
            }
        ],
        "undo": False,
    },
}
```

### Step 2: Lock `batch_execute` against generic escape-hatch use

Add negative cases for:

- two commands instead of one;
- a raw command other than `set_main_scene`;
- extra fields in the command or params;
- wrong scene path;
- `undo=true`;
- missing `undo`;
- the old `project_manage(settings_set)` route.

Each must fail recipe validation before any MCP call.

### Step 3: Lock required tool/readback behavior

Require:

- `batch_execute` appears in required MCP tools only because the approved recipe uses it;
- read-only `project_manage` remains required for preflight/readback;
- timeout/connection ambiguity from the approved batch operation performs exactly one `project_manage(settings_get)` readback for `application/run/main_scene`;
- the mutation itself is called exactly once;
- `AmbiguousMutationError` is still raised after readback.

### Step 4: Preserve previous contracts

Keep existing tests proving:

- exact four serialized output paths;
- session discovery bounded retry;
- exact session/toolchain identity;
- provenance schema/head/hash constraints;
- no forbidden filesystem/script writer route.

### Step 5: Run RED

```bash
python -m pytest tests/test_higodot_task2_mcp_driver.py -q
```

**Expected RED:** failures must identify the old final `project_manage(settings_set)` recipe/bridge assumptions and absent approved-batch ambiguity handling.

### Step 6: Commit RED only

```bash
git add tests/test_higodot_task2_mcp_driver.py
git commit -m "test: require guarded Task2 main-scene batch route"
```

Do not change the recipe or bridge in this commit.

---

## Task 4: Route Task 2 through the validated command GREEN

**Files:**
- Modify: `tools/higodot_task2_bridge.py`
- Modify: `.github/validation/higodot-task2-authoring-recipe.json`
- Test: `tests/test_higodot_task2_mcp_driver.py`

### Step 1: Add one exact approved-batch predicate

Add a pure helper that returns true only for the exact pre-session recipe shape:

```python
def _is_approved_main_scene_batch(tool: str, arguments: dict[str, Any]) -> bool:
    return tool == "batch_execute" and arguments == {
        "commands": [
            {
                "command": "set_main_scene",
                "params": {"scene": EXPECTED_MAIN_SCENE},
            }
        ],
        "undo": False,
    }
```

Do not make `batch_execute` generally allowlisted.

### Step 2: Replace the executable main-scene validation rule

Update `validate_executable_recipe()` so:

- the one approved batch shape counts as the single main-scene write;
- arbitrary `batch_execute` fails;
- `project_manage(settings_set)` fails;
- `project_manage(settings_get)` remains permitted only as a read-only project operation if ever present;
- exactly one approved main-scene write remains mandatory.

Keep `ALLOWED_SERIALIZED_PATHS`, `EXPECTED_MAIN_SCENE`, exact session identity, and provenance fields unchanged.

### Step 3: Change only the final recipe operation

In `.github/validation/higodot-task2-authoring-recipe.json`, replace the old final `project_manage(settings_set)` operation with the exact approved `batch_execute(set_main_scene)` operation. Leave all three scene-authoring operation sequences unchanged.

### Step 4: Make ambiguity readback explicit

Update `_readback_after_ambiguous()` so the approved main-scene batch route performs exactly:

```python
await client.call(
    "project_manage",
    {
        "op": "settings_get",
        "params": {"key": "application/run/main_scene"},
        "session_id": session_id,
    },
)
```

Then `execute_recipe_operations()` must continue raising `AmbiguousMutationError`; do not retry `batch_execute`.

All other mutation ambiguity behavior remains unchanged.

### Step 5: Run focused GREEN

```bash
python -m pytest tests/test_higodot_task2_mcp_driver.py -q
```

Then run the repository's existing bridge/toolchain/provenance/publish static-contract tests that are part of PR validation.

**Expected GREEN:** all non-serialized HiGodot bridge contracts pass; Task 2 product static tests may still remain at the existing expected serialized RED because live PUBLISH has not occurred yet.

### Step 6: Commit GREEN

```bash
git add tools/higodot_task2_bridge.py .github/validation/higodot-task2-authoring-recipe.json
git commit -m "fix: route Task2 main scene through validated HiGodot command"
```

---

## Task 5: Exact-head verification and handoff for one new manual PROVE

**Files:**
- No product/code changes after the final GREEN commit unless verification exposes a real defect.
- Metadata-only synchronization: PR #131 body and Google Sheet rows under `BS-HIGODOT-EXEC-20260808-01`.

### Step 1: Read back exact branch head and test-merge separately

After Task 4, fetch PR #131 and record:

```text
exact branch head = <HEAD_SHA>
GitHub test-merge = <TEST_MERGE_SHA>
```

Never substitute the test-merge SHA for the manual workflow `expected_head_sha`.

### Step 2: Verify applicable remote CI on the exact head

Required evidence includes, as applicable:

- Godot 4.7.1 headless suite including `test_higodot_main_scene_command.gd`;
- focused/static HiGodot bridge contract;
- MCP driver tests;
- Godot AI 3.1.3 runtime/toolchain pin contract;
- approved editor-plugin synchronization contract;
- post-authoring/provenance/publish guard static contracts;
- GUT 9.7.1 formal adoption/regressions;
- Task 1 canon regressions.

The expected pre-PUBLISH Task 2 product state is still:

```text
three serialized-scene/main_scene assertions may remain RED because the live authoring outputs are not yet published
```

Do not call that state fully green. Distinguish non-serialized gates from intentional serialized RED.

### Step 3: Inspect review/conversation state

Freshly read:

- PR reviews;
- unresolved review threads;
- conversation comments;
- mergeability/draft/open state.

Any blocking review finding must be resolved before another manual PROVE request.

### Step 4: Synchronize Google Sheet and PR body without moving HEAD

Under `BS-HIGODOT-EXEC-20260808-01`, update current state to include:

```text
WRITTEN_SPEC_REVIEW = USER_APPROVED
IMPLEMENTATION_PLAN = COMMITTED
PLUGIN_MAIN_SCENE_COMMAND = GREEN
TASK2_BATCH_ROUTE = GREEN
EXACT_HEAD_NON_SERIALIZED_CI = <observed state>
PROVE_ATTEMPT3 = NOT_RUN / READY_FOR_MANUAL_DISPATCH
PUBLISHED_PROVENANCE = 0
PUBLISH = 0
PR131 = DRAFT / OPEN / UNMERGED
```

Do not make a post-verification documentation commit merely to record status; that would move the exact HEAD and invalidate the evidence. Use PR metadata and Sheet state for the final checkpoint.

### Step 5: Give the user exactly one new manual dispatch SHA

Only if all applicable non-serialized gates are green, provide:

```text
Actions → HiGodot Task 2 Authoring Bridge → Run workflow
branch: feat/vertical-slice-task2-app-shell
expected_head_sha: <exact branch HEAD, not test-merge>
```

Do not rerun `467d1e2e...`, `02279371...`, or any earlier SHA.

### Step 6: Post-dispatch acceptance criteria

A successful third PROVE must demonstrate, in order:

```text
exact PR/head identity
→ live Godot 4.7.1 + HiGodot 3.1.3 session
→ three approved scenes authored/saved
→ set_main_scene via exact one-command batch_execute
→ exact four-file serialized diff only
→ project.godot delta only at run/main_scene
→ Godot import/smoke + GUT + Task1/model/integration PASS
→ provenance generated/uploaded
→ exact-head race check PASS
→ guarded byte-identical PUBLISH
→ new branch HEAD readback
→ fresh CI/test-merge/review readback
```

PR #131 must remain unmerged until a separate explicit merge approval is given.

---

## Plan completion checkpoint

Before implementation starts, the authoritative state must read:

```text
WRITTEN_SPEC_REVIEW = USER_APPROVED
IMPLEMENTATION_PLAN = COMMITTED
IMPLEMENTATION = 0
PRODUCT_SERIALIZED_MUTATION = 0
PUBLISH = 0
PR131 = DRAFT / OPEN / UNMERGED
```

Implementation then proceeds strictly Task 1 RED → Task 2 GREEN → Task 3 RED → Task 4 GREEN → Task 5 exact-head verification/handoff.