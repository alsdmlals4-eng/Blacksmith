# Blacksmith Task 2 — HiGodot CI Authoring Bridge Design

Decision ID: `BS-HIGODOT-EXEC-20260808-01`

Status: `USER_APPROVED_DESIGN / WRITTEN_SPEC_REVIEW_PENDING / IMPLEMENTATION_NOT_STARTED`

Related Decisions:

- `BS-VS-TASK2-20260807-01` — Task 2 MainMenu → BlacksmithApp → WORKSHOP shell and start-scene migration.
- `BS-HIGODOT-20260808-01` — HiGodot is the user-approved production authoring authority for the Task 2 serialized Godot surfaces only.
- `BS-VS-INIT-20260808-01` — new-campaign initializer and safe replacement slice.
- `BS-TEST-20260806-01` — GUT 9.7.1 remains the sole GDScript test-framework authority.
- `BS-HERA-20260808-01` — Hera remains vendored, disabled, and non-authoritative.

Observed baselines at design approval:

- Blacksmith `main`: `a00e864ce5de7bdf872e8093d489c8a78c058afb`.
- PR #131 pre-spec head: `89e6fa73d9d0a4ed5cb72447189e126ea905bd3a`.
- Base `main`: `eee98a930219065e30b4d7d14d99d5ac7db44c60`.
- Project pinned Base operating source remains unchanged; this Decision does not adopt current Base main.

## 1. Problem

Task 2 script logic is GREEN, but the remaining static app-shell RED is on HiGodot-owned serialized surfaces:

```text
scenes/vertical_slice/main_menu.tscn
scenes/vertical_slice/vertical_slice_app.tscn
scenes/vertical_slice/screens/vs_workshop_screen.tscn
project.godot  # application/run/main_scene only
```

`BS-HIGODOT-20260808-01` activates HiGodot as the production authoring authority for those surfaces, but approval and execution capability are separate facts.

The existing repository Live-Editor Pilot cannot be reused as a production mutation path. Its contract is disposable-copy only, `source_mutation_policy: FORBIDDEN`, `MAIN_SCENE_READ_ONLY`, `SCRATCH_SCENE_MUTATION_ONLY`, and `SOURCE_TREE_UNCHANGED`.

Directly writing `.tscn` or `project.godot` through a generic editor or GitHub Contents API would bypass the approved authoring authority and is therefore forbidden.

## 2. Source-grounded HiGodot constraints

The vendored plugin is `Godot AI` version `3.0.5` and is an `EditorPlugin`.

The source establishes these implementation facts:

1. `addons/godot_ai/plugin.gd` disables MCP when Godot is launched in headless mode. Therefore the authoring bridge must run a real Editor process under a virtual display such as Xvfb; `godot --headless --editor` cannot be the mutation process.
2. The plugin starts or adopts an exact-version Python server and connects the Editor to it over WebSocket. The HTTP MCP endpoint is loopback-local; the configured default is `http://127.0.0.1:8000/mcp`, with the Editor WebSocket on the configured WS port.
3. In user mode, server discovery prefers an exact plugin-version `uvx` launch. For vendored `3.0.5`, the server package must remain version-locked to the compatible release; no automatic upgrade is allowed by this Decision.
4. The vendored tool catalog exposes the required authoring domains, including `scene_manage`, `node_create`, `node_manage`, `node_set_property`, `project_manage`, and `ui_manage`.
5. Scene creation is executed inside the Editor through Godot APIs (`PackedScene`, `ResourceSaver`, `EditorInterface`), not by emitting hand-written `.tscn` text.
6. Project-setting writes use `ProjectSettings.set_setting()` followed by `ProjectSettings.save()` and report the old and new values.

These facts make a project-specific CI bridge feasible without granting a generic text writer authority over Godot serialization.

## 3. Decision

Adopt **Approach B: a Task 2-scoped CI HiGodot PROVE → PUBLISH bridge**.

The bridge is a project-specific execution path. It does **not** declare Base's generic Godot production adapter ready, does not activate Hera, does not broaden HiGodot scope beyond Task 2, and does not open general product implementation.

The bridge has two separated jobs:

```text
workflow_dispatch at an exact PR #131 head
        |
        v
PROVE (contents: read)
  Xvfb + Godot 4.7.1 Editor
  + vendored HiGodot 3.0.5
  + exact-version godot-ai server
  + MCP authoring recipe
        |
        v
validated artifact bundle
  exact four output files
  + provenance/evidence manifest
        |
        v
PUBLISH (contents: write)
  verify same input head
  verify bundle hashes
  copy byte-identical proven outputs
  commit/push to PR #131 branch
        |
        v
automatic exact-head CI
```

No serialized product file may be published unless the PROVE job completed successfully and its evidence verifies the exact bytes being published.

## 4. Workflow trigger and branch binding

The authoring workflow is manual `workflow_dispatch` only.

Required inputs and preconditions:

- exact expected PR head SHA;
- target branch fixed to `feat/vertical-slice-task2-app-shell` / PR #131;
- current checkout HEAD must equal the expected SHA;
- the PR must still target `main` and remain unmerged;
- if `main` advanced in a way that makes the PR stale or the expected head no longer matches, fail closed and require a fresh authority/PR review before authoring.

The workflow must not trigger automatically on arbitrary pull requests, pushes, forks, labels, comments, or schedules.

## 5. PROVE job

### 5.1 Permissions

```yaml
permissions:
  contents: read
```

The PROVE job receives no repository write authority.

### 5.2 Runtime

- Ubuntu GitHub-hosted runner.
- Godot `4.7.1-stable` only.
- HiGodot/Godot AI plugin bytes must be the bytes already present in the exact PR head; the job must record their relevant blob/file hashes and plugin version.
- `uv` and the Python server/tooling must be version-pinned; floating `latest`, branch, or unbounded package selectors are forbidden.
- Set `GODOT_AI_MODE=user` so the server path is the user-install/exact-version path rather than an accidental unrelated development venv.
- Set `GODOT_AI_DISABLE_TELEMETRY=true` (or equivalent supported opt-out) for the CI authoring session.
- Start Godot as a non-headless Editor under Xvfb. An invocation that contains `--headless` is a contract failure because HiGodot disables MCP in that mode.

### 5.3 Readiness and identity preflight

Before the first mutation, the driver must prove all of the following:

1. the exact Git checkout path is the active Godot project;
2. the HiGodot server reports the expected compatible version;
3. the Editor-to-server WebSocket session is live;
4. the MCP client can enumerate/activate exactly the intended project session;
5. the required tool domains/operations are available;
6. the Editor reports a writable/ready state;
7. no ambiguous second Blacksmith Editor session can receive the operation;
8. the initial tracked diff contains no HiGodot-owned Task 2 serialized surface.

If any identity or capability check is ambiguous, fail before mutation.

### 5.4 MCP authoring recipe

The driver may invoke only the minimal HiGodot operations needed to materialize the already-approved Task 2 design.

Allowed serialized outputs are exactly:

```text
scenes/vertical_slice/main_menu.tscn
scenes/vertical_slice/vertical_slice_app.tscn
scenes/vertical_slice/screens/vs_workshop_screen.tscn
project.godot
```

The product recipe must:

- create the three approved scenes through HiGodot scene/node/UI operations;
- attach/use the already-GREEN `vs_main_menu.gd` and `vs_app.gd` scripts without modifying those scripts in this phase;
- use engine-native UI nodes only and add no external image/audio/font assets;
- keep MainMenu controls at the approved minimum 48×48 interaction size;
- keep Settings as an inline MainMenu overlay;
- make `BlacksmithApp` enter at `WORKSHOP` using the approved script/router behavior;
- change only `application/run/main_scene` in `project.godot` to the approved MainMenu scene;
- preserve viewport, portrait orientation, renderer, autoloads, enabled plugins, input settings, and unrelated project settings.

The bridge must not use HiGodot filesystem/script text-write tools as a shortcut for these serialized outputs when a Godot-native scene/node/project-setting operation exists.

### 5.5 Timeout and retry policy

Mutation calls are not blindly retried after a timeout or lost response.

On an uncertain result, the driver must first read back Editor state and filesystem/project-setting state. If it cannot determine whether the operation committed, fail closed and publish nothing.

### 5.6 Post-authoring diff gate

After the MCP recipe finishes, the working tree must satisfy all of these conditions:

- exactly the four approved serialized files are changed/created;
- no file under `addons/`, `assets/`, `data/`, unrelated `scenes/`, or unrelated project settings changed;
- no existing GDScript implementation or test file was modified by the authoring runtime;
- transient `.godot/`, logs, MCP process files, editor settings, caches, and evidence working files are not part of the product diff.

Any unexpected tracked path blocks publication.

### 5.7 Validation before artifact creation

The PROVE job must run validation against the HiGodot-authored working tree before publishing any bytes:

- focused Task 2 static app-shell contract;
- Godot 4.7.1 import/parse;
- smoke of `main_menu.tscn`;
- smoke of `vertical_slice_app.tscn`;
- smoke of the Workshop screen or equivalent load/instantiate check;
- GUT 9.7.1 formal suite, including existing Task 2 script tests;
- existing Task 1 and model/integration regression checks required by the current PR router;
- focused diff/authority/provenance contract.

The Editor used for normal post-authoring validation may be headless because authoring has already completed; the non-headless requirement applies to the HiGodot mutation session.

### 5.8 Evidence bundle

A successful PROVE job uploads a self-contained artifact containing:

```text
higodot-task2-provenance.json
product/
  project.godot
  scenes/vertical_slice/main_menu.tscn
  scenes/vertical_slice/vertical_slice_app.tscn
  scenes/vertical_slice/screens/vs_workshop_screen.tscn
validation/
  focused contract results
  Godot import/smoke results
  GUT JUnit/result evidence
```

The provenance manifest records at minimum:

- Decision IDs;
- repository and PR number;
- input head SHA;
- Godot version;
- HiGodot plugin version and reviewed file hashes;
- server launch/version evidence;
- active MCP session/project identity;
- ordered operation names plus canonical input hashes and success/error status;
- pre/post SHA-256 for every approved serialized output;
- exact tracked diff path list;
- validation result summary and evidence hashes;
- artifact content hashes.

Do not store secrets, auth tokens, environment dumps, or unrelated source contents in the provenance manifest.

## 6. PUBLISH job

### 6.1 Permission separation

The PUBLISH job is the only job with repository write authority and runs only after successful PROVE.

```yaml
permissions:
  contents: write
```

It does not start Godot, does not call HiGodot, and does not regenerate the scenes.

### 6.2 Byte-identical publication

PUBLISH must:

1. check out the same expected PR head SHA;
2. verify the remote PR branch still points at that SHA;
3. download the PROVE artifact;
4. verify the provenance manifest and every serialized-file hash;
5. copy only the four proven files into the checkout;
6. verify the resulting Git diff is exactly the four-file allowlist;
7. verify each checkout file hash equals its PROVE artifact hash;
8. commit the exact proven bytes;
9. push only if the branch has not moved.

Copying already-proven bytes is a publication/transport operation, not a second authoring authority. Any byte change between PROVE and PUBLISH is forbidden.

If the branch moves, the job fails. It must not rebase, force-push, regenerate, or silently replay against the new head.

## 7. Post-publish validation and completion boundary

Publication does not itself make Task 2 GREEN.

After PUBLISH creates a new PR #131 head:

- all automatic PR workflows must complete on that exact head;
- the previously RED Task 2 static contract must become GREEN;
- Godot 4.7.1 and GUT must remain GREEN;
- changed-file scope must remain approved;
- reviews, unresolved review threads, and comments must be reread;
- Full validation must run on the exact merge-candidate head before merge readiness;
- Google Sheet and GitHub must be synchronized/read back under the same Decision IDs.

PR #131 remains Draft and unmerged until a separate explicit merge approval.

## 8. Base and authority compatibility

This project-specific bridge deliberately does not claim:

```text
BASE_PRODUCTION_ADAPTER_READY = READY
```

Base's current generic production-adapter readiness remains `NOT_READY`. This Decision proves, at most:

```text
BLACKSMITH_TASK2_HIGODOT_EXECUTION_PATH = VERIFIED_FOR_APPROVED_TASK2_SURFACES
```

It is not evidence for a reusable multi-project production adapter, Windows production operation, Android-device validation, physical input, human editor usability, or human playtest.

The existing Base C0/Blacksmith Live-Editor Pilot remains unchanged and read-only with respect to source product files.

## 9. Fail-closed conditions

Do not publish if any of the following is true:

- expected SHA mismatch;
- wrong branch or wrong PR;
- wrong project/session identity;
- MCP endpoint/server unavailable;
- plugin/server version mismatch;
- Godot launched headless for the mutation session;
- required HiGodot operations missing;
- ambiguous mutation timeout/readback;
- unexpected tracked diff;
- asset/addon/script mutation outside the approved recipe;
- project setting other than `application/run/main_scene` changed;
- provenance hash mismatch;
- any required focused/Godot/GUT regression validation fails;
- branch moves before publish;
- publish bytes differ from PROVE bytes.

There is no generic text-writing fallback for serialized Godot files.

## 10. TDD strategy for the bridge

Implementation begins only after written-spec review approval.

### RED

First add contract tests that fail because the bridge does not yet exist. Tests must require:

- manual-only trigger;
- PROVE `contents: read` and PUBLISH-only `contents: write` separation;
- Xvfb/non-headless authoring process;
- exact HiGodot/server version binding;
- exact branch/head binding;
- four-file serialized allowlist;
- session/project identity preflight;
- provenance manifest and per-file hashes;
- validation-before-publish;
- byte-identical artifact publication;
- fail-closed branch race handling;
- no Base production-ready claim;
- no direct serialized-text fallback.

Record remote RED evidence from the exact test-only commit.

### GREEN

Implement the minimum workflow/driver/evidence surfaces necessary to make those contracts pass, then run one real PROVE session against the current PR head. PUBLISH remains blocked until the real PROVE artifact passes all validation.

### REFACTOR

Refactor only after the bridge contract and real Task 2 authoring path are GREEN. Refactor must not broaden tool domains, output paths, target PR, or HiGodot authority.

## 11. Out of scope

- generic multi-project HiGodot production bridge;
- Base main adoption or Base contract changes;
- HiGodot vendor upgrade;
- Hera activation/adoption;
- arbitrary Scene/Resource/project-setting mutation;
- new gameplay logic;
- new product image/audio/font assets;
- product image-rights completion;
- Android device validation;
- human editor usability claim;
- human playtest;
- PR #131 merge.

## 12. Acceptance criteria

This bridge design is successfully implemented only when all of the following are true:

1. A contract RED is observed before bridge implementation.
2. PROVE runs a real Godot 4.7.1 Editor under Xvfb and HiGodot MCP is live.
3. HiGodot 3.0.5/exact compatible server identity is verified.
4. The active MCP session is proven to be the exact PR #131 checkout.
5. HiGodot authors exactly the three approved scenes and only the approved start-scene project setting.
6. The working-tree diff contains exactly the four serialized outputs.
7. Focused static, Godot, GUT, and required regression checks pass before artifact creation.
8. Provenance records operation/evidence/file hashes without secrets.
9. PUBLISH copies only byte-identical PROVE outputs and fails on branch movement.
10. The published exact head turns the existing static app-shell RED GREEN without new authority violations.
11. Exact-head PR workflows and Full validation pass before merge readiness.
12. GitHub and Google Sheet readback agree under the same Decision IDs.
13. Base generic production adapter remains explicitly `NOT_READY`.
14. PR #131 remains unmerged until a separate explicit merge approval.

## 13. Current gate after design approval

```text
BS-HIGODOT-EXEC-20260808-01 = USER_APPROVED_DESIGN
WRITTEN_SPEC_REVIEW = PENDING
IMPLEMENTATION_PLAN = NOT_STARTED
BRIDGE_TDD = NOT_STARTED
TASK2_STATIC_APP_SHELL = EXPECTED_RED
SCENE_PROJECT_MUTATION = 0
PR131 = DRAFT_UNMERGED
GENERAL_PRODUCT = BLOCKED
```

This document supersedes older Task 2 authority wording that described HiGodot as pilot-only. Product behavior requirements in the earlier Task 2 design remain applicable; current authoring authority and execution-path state are governed by `BS-HIGODOT-20260808-01` and this Decision.