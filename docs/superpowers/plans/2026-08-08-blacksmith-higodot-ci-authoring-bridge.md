# Blacksmith Task 2 HiGodot CI Authoring Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and prove the PR #131-scoped HiGodot CI `PROVE → PUBLISH` bridge that authors exactly three approved Task 2 scenes plus the `application/run/main_scene` setting through the live Godot Editor/HiGodot path, then publishes only byte-identical validated outputs.

**Architecture:** A manual-only GitHub Actions workflow binds to one expected PR #131 head. `PROVE` has read-only repository permission, runs a non-headless Godot 4.7.1 Editor under Xvfb, drives vendored Godot AI 3.0.5 through its local MCP endpoint, validates an exact four-file serialized diff, and emits a provenance artifact. `PUBLISH` is the only write-capable job; it never runs Godot or HiGodot and can only copy the hash-verified bytes produced by `PROVE` if the PR branch is still at the expected head.

**Tech Stack:** GitHub Actions, Python 3.12, pytest 8.3.5, FastMCP programmatic client, Godot 4.7.1-stable, vendored Godot AI/HiGodot 3.0.5, Xvfb, GUT 9.7.1, SHA-256 evidence.

## Global Constraints

- Decision ID: `BS-HIGODOT-EXEC-20260808-01`.
- Related authority: `BS-HIGODOT-20260808-01`, `BS-VS-TASK2-20260807-01`, `BS-VS-INIT-20260808-01`.
- Target PR: `#131`; target branch: `feat/vertical-slice-task2-app-shell`.
- Blacksmith main baseline at review: `a00e864ce5de7bdf872e8093d489c8a78c058afb`.
- Project pinned Base remains `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`; current Base main is not adopted.
- Godot mutation process: `4.7.1-stable`, non-headless Editor under Xvfb.
- Vendored HiGodot/Godot AI plugin: exact `3.0.5`; no plugin upgrade in this plan.
- Server package: exact `godot-ai==3.0.5`; telemetry disabled with `GODOT_AI_DISABLE_TELEMETRY=true`.
- MCP endpoint: loopback `http://127.0.0.1:8000/mcp` after server/editor readiness is proven.
- Mutation must use HiGodot Scene/Node/UI/ProjectSettings operations; direct generic text/GitHub API authoring of `.tscn` or `project.godot` is forbidden.
- Serialized output allowlist is exactly:
  - `scenes/vertical_slice/main_menu.tscn`
  - `scenes/vertical_slice/vertical_slice_app.tscn`
  - `scenes/vertical_slice/screens/vs_workshop_screen.tscn`
  - `project.godot`, with only `application/run/main_scene` semantically changed.
- `PROVE` has `contents: read`; `PUBLISH` is the only job with `contents: write`.
- `PUBLISH` does not run Godot, HiGodot, MCP, or any scene generator.
- Branch movement, project/session ambiguity, missing required tools, uncertain mutation result, unexpected tracked diff, failed validation, provenance mismatch, or byte mismatch fails closed.
- Existing `.godot-live-editor` pilot remains scratch-only/source-mutation-forbidden and is not converted into this production path.
- Base generic `PRODUCTION_ADAPTER_READY` remains `NOT_READY`.
- General product implementation, product image/rights completion, Android-device validation, human playtest, Hera activation, and PR #131 merge remain outside this plan.
- No Scene or `project.godot` product mutation occurs until a real `PROVE` run in Task 8.

---

## File Structure

- Create: `tests/test_higodot_task2_ci_authoring_bridge_contract.py` — repository-level bridge policy and fail-closed contract.
- Modify: `.github/workflows/python-validation.yml` — execute the bridge contract in centralized Python validation.
- Create: `.github/validation/higodot-task2-authoring-recipe.json` — declarative allowlisted authoring recipe and expected scene structure.
- Create: `.github/validation/higodot-task2-provenance-schema.json` — required evidence fields and exact output set.
- Create: `tools/higodot_task2_bridge.py` — deterministic MCP driver, diff/provenance validator, and artifact packager.
- Create: `.github/workflows/higodot-task2-authoring-bridge.yml` — manual `PROVE → PUBLISH` workflow.
- Modify after successful real publish only: the four approved serialized outputs, exclusively through the PROVE artifact bytes.

### Stable driver interfaces

`tools/higodot_task2_bridge.py` must expose these testable interfaces:

```python
ALLOWED_SERIALIZED_PATHS: tuple[str, ...]
MCP_URL = "http://127.0.0.1:8000/mcp"
TARGET_REPOSITORY = "alsdmlals4-eng/Blacksmith"
TARGET_PR = 131
TARGET_BRANCH = "feat/vertical-slice-task2-app-shell"

def load_recipe(path: Path) -> dict: ...
def validate_recipe(recipe: dict) -> None: ...
def sha256_file(path: Path) -> str: ...
def git_changed_paths(repo: Path) -> list[str]: ...
def verify_project_setting_delta(before: str, after: str) -> None: ...
def verify_serialized_diff(repo: Path, before_project_text: str) -> dict[str, str]: ...
def build_provenance(context: dict, operations: list[dict], hashes: dict[str, str], validations: dict) -> dict: ...
def validate_provenance(payload: dict, expected_head: str) -> None: ...
async def run_prove(recipe_path: Path, output_dir: Path, expected_head: str) -> None: ...
def run_publish_verify(artifact_dir: Path, repo: Path, expected_head: str) -> None: ...
```

The MCP client implementation is deterministic and programmatic:

```python
from fastmcp import Client

async with Client(MCP_URL) as client:
    tools = await client.list_tools()
    result = await client.call_tool(tool_name, arguments)
```

Every write call includes the activated `session_id` when the tool schema supports it. Tool names and operation payloads come only from the checked-in recipe.

---

### Task 1: Bridge Contract RED and CI Routing

**Files:**
- Create: `tests/test_higodot_task2_ci_authoring_bridge_contract.py`
- Modify: `.github/workflows/python-validation.yml`

**Interfaces:**
- Consumes: approved bridge spec and Decision `BS-HIGODOT-EXEC-20260808-01`.
- Produces: an exact remote RED proving bridge workflow/driver/recipe/schema do not yet exist.

- [ ] **Step 1: Write the failing repository contract**

Create tests with these exact path constants and first-order assertions:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/higodot-task2-authoring-bridge.yml"
DRIVER = ROOT / "tools/higodot_task2_bridge.py"
RECIPE = ROOT / ".github/validation/higodot-task2-authoring-recipe.json"
SCHEMA = ROOT / ".github/validation/higodot-task2-provenance-schema.json"
DECISION_ID = "BS-HIGODOT-EXEC-20260808-01"
ALLOWED = {
    "project.godot",
    "scenes/vertical_slice/main_menu.tscn",
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
}


def required_text(path: Path) -> str:
    assert path.is_file(), f"missing bridge surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def test_bridge_surfaces_exist() -> None:
    for path in (WORKFLOW, DRIVER, RECIPE, SCHEMA):
        assert path.is_file(), f"missing bridge surface: {path.relative_to(ROOT)}"
```

Add separate tests that, once the files exist, require manual-only trigger, permission separation, Xvfb/non-headless authoring, exact version strings, exact branch/PR/head binding, exact four-file allowlist, provenance hashes, validation-before-publish, byte-identical publish, no force-push/rebase/regeneration, no Base READY claim, and no text-serialization fallback.

- [ ] **Step 2: Route the contract through centralized validation**

In `.github/workflows/python-validation.yml`, inside `Validate document and CI contracts`, add before the existing Task 2 app-shell step:

```yaml
python -m pytest tests/test_higodot_task2_ci_authoring_bridge_contract.py -q
```

Do not add the bridge workflow or driver in this commit.

- [ ] **Step 3: Commit the RED**

```bash
git add tests/test_higodot_task2_ci_authoring_bridge_contract.py .github/workflows/python-validation.yml
git commit -m "test: define HiGodot Task 2 authoring bridge contract"
```

- [ ] **Step 4: Verify remote RED on the exact commit**

Expected: PR validation fails in `Validate document and CI contracts` because the four bridge surfaces are absent. Other automatic governance/GUT jobs must still start normally. Inspect the failed job log and record the exact missing paths; a YAML parse error, import error, or unrelated regression is not valid RED evidence.

- [ ] **Step 5: Record RED evidence without changing product surfaces**

Update PR description and same-ID Sheet evidence with the RED SHA and exact failure reason. Confirm `project.godot` and `scenes/vertical_slice/**` are unchanged.

---

### Task 2: Recipe, Provenance Schema, and Pure Validation Helpers

**Files:**
- Create: `.github/validation/higodot-task2-authoring-recipe.json`
- Create: `.github/validation/higodot-task2-provenance-schema.json`
- Create: `tools/higodot_task2_bridge.py`
- Test: `tests/test_higodot_task2_ci_authoring_bridge_contract.py`

**Interfaces:**
- Produces: exact recipe structure, provenance vocabulary, pure fail-closed validation helpers.
- Does not connect to MCP or mutate Godot files.

- [ ] **Step 1: Add failing tests for recipe and schema**

Require recipe identity:

```json
{
  "decision_id": "BS-HIGODOT-EXEC-20260808-01",
  "repository": "alsdmlals4-eng/Blacksmith",
  "pr_number": 131,
  "branch": "feat/vertical-slice-task2-app-shell",
  "godot_version": "4.7.1-stable",
  "higodot_version": "3.0.5"
}
```

Require the recipe output list to equal `ALLOWED` exactly and require no operation named `filesystem_manage`, `script_create`, `script_patch`, or equivalent serialized-text writer.

Require provenance schema fields for Decision IDs, repository/PR/head, Godot/plugin/server identity, session/project identity, ordered operations, changed paths, per-file SHA-256, validation evidence hashes, and artifact hashes.

- [ ] **Step 2: Run focused tests and verify failure**

```bash
python -m pytest tests/test_higodot_task2_ci_authoring_bridge_contract.py -q
```

Expected: failures identify missing recipe/schema/driver.

- [ ] **Step 3: Implement recipe and schema**

Recipe operations must be declarative and restricted to native Godot operations: scene create/open/save, node creation/property assignment, UI layout/property operations, script attachment to the already-GREEN scripts, and `project_manage` setting write for `application/run/main_scene` only.

The schema must use JSON Schema draft 2020-12 and set `additionalProperties: false` for top-level provenance records.

- [ ] **Step 4: Implement pure helpers only**

Implement `load_recipe`, `validate_recipe`, `sha256_file`, `git_changed_paths`, `verify_project_setting_delta`, `verify_serialized_diff`, `build_provenance`, and `validate_provenance`. `verify_project_setting_delta` must compare normalized `project.godot` lines after replacing only the `run/main_scene=` line and reject any other textual delta.

- [ ] **Step 5: Run focused tests to GREEN and commit**

```bash
python -m pytest tests/test_higodot_task2_ci_authoring_bridge_contract.py -q
python -m unittest tests/test_ci_workflow_structure.py -v
git add .github/validation/higodot-task2-authoring-recipe.json .github/validation/higodot-task2-provenance-schema.json tools/higodot_task2_bridge.py tests/test_higodot_task2_ci_authoring_bridge_contract.py
git commit -m "feat: add HiGodot bridge recipe and provenance contracts"
```

---

### Task 3: Manual Workflow Permission and Identity Skeleton

**Files:**
- Create: `.github/workflows/higodot-task2-authoring-bridge.yml`
- Modify: `tests/test_higodot_task2_ci_authoring_bridge_contract.py`

**Interfaces:**
- Consumes pure validation helpers.
- Produces manual workflow skeleton with `prove` and `publish` jobs; it is not yet authorized to publish because real PROVE remains unexecuted.

- [ ] **Step 1: Add failing workflow-structure tests**

Require:

```yaml
on:
  workflow_dispatch:
    inputs:
      expected_head_sha:
```

and reject `pull_request:`, `push:`, `schedule:`, `repository_dispatch:`, and comment/label triggers.

Require `prove` to have only `contents: read`, `publish` to have `contents: write`, and no top-level `contents: write`.

- [ ] **Step 2: Verify RED**

Run the focused pytest and confirm failures are only missing workflow markers.

- [ ] **Step 3: Add workflow skeleton**

Use Ubuntu, Python 3.12, checkout with `fetch-depth: 0`, `persist-credentials: false` in PROVE, exact expected-head equality check, exact branch `feat/vertical-slice-task2-app-shell`, repository `alsdmlals4-eng/Blacksmith`, and PR #131 metadata check before any mutation.

Download Godot 4.7.1 using the same project archive source and verify the existing expected archive SHA-256 `c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba` before extraction.

Install Xvfb and an exact Python client environment. Use `godot-ai==3.0.5`; the server identity must be read back as 3.0.5 before mutation. Set:

```yaml
env:
  GODOT_AI_MODE: user
  GODOT_AI_DISABLE_TELEMETRY: "true"
```

The mutation Editor command must use `xvfb-run` and must not contain `--headless`.

- [ ] **Step 4: GREEN focused workflow contract and commit**

Run focused pytest and CI structure tests, then commit the workflow skeleton.

---

### Task 4: Deterministic MCP Preflight and Authoring Driver

**Files:**
- Modify: `tools/higodot_task2_bridge.py`
- Modify: `.github/validation/higodot-task2-authoring-recipe.json`
- Modify: `tests/test_higodot_task2_ci_authoring_bridge_contract.py`

**Interfaces:**
- Produces: `run_prove(...)` that connects only after Editor/server readiness and fails before the first write on ambiguous identity.

- [ ] **Step 1: Add failing tests for preflight sequencing**

Test a fake client adapter that records calls and assert read-only operations happen before the first mutation:

```text
list_tools
session_manage(list)
session_activate
editor_state
scene_get_hierarchy / project_manage(settings_get)
[first allowed mutation]
```

Require exactly one active session whose reported project path resolves to the checked-out repository root. Require required tools/ops to be present before mutation.

- [ ] **Step 2: Verify RED**

Run the focused test and confirm `run_prove`/preflight behavior is missing rather than a fixture failure.

- [ ] **Step 3: Implement MCP client wrapper**

Use `fastmcp.Client(MCP_URL)` inside an async context. Call `list_tools()` and `call_tool(name, arguments)`. Normalize every result into a JSON-serializable `{tool, arguments_sha256, success, result_sha256, error}` evidence record without storing auth tokens or unrelated content.

- [ ] **Step 4: Implement exact-session preflight**

List sessions, select exactly one whose project identity/path matches this checkout, activate it, then check `editor_state` writable/ready status and required tool availability. Zero or multiple matching sessions fail closed.

- [ ] **Step 5: Implement recipe execution**

Execute recipe operations in order. On timeout/transport loss, perform readback of current scene/project setting before deciding whether the operation committed. If commit state is still ambiguous, raise and stop; do not blindly retry.

- [ ] **Step 6: GREEN driver tests and commit**

Run focused pytest plus existing HiGodot authority contracts and commit.

---

### Task 5: Post-Authoring Diff Gate and Validation

**Files:**
- Modify: `tools/higodot_task2_bridge.py`
- Modify: `.github/workflows/higodot-task2-authoring-bridge.yml`
- Modify: `tests/test_higodot_task2_ci_authoring_bridge_contract.py`

**Interfaces:**
- Produces: validated four-file working tree before artifact creation.

- [ ] **Step 1: Add failing tests for unexpected-path and project-setting changes**

Create temporary git repositories in tests and verify any fifth tracked path is rejected. Verify changes to viewport, renderer, autoload, plugin, input, or any `project.godot` line other than `run/main_scene` are rejected.

- [ ] **Step 2: Implement diff gate**

After authoring, call `verify_serialized_diff`. Require changed paths equal the four-file allowlist exactly; not a subset and not a superset.

- [ ] **Step 3: Add validation commands before artifact upload**

Workflow PROVE runs, against the authored working tree:

```bash
python -m unittest tests.test_vertical_slice_task2_app_shell_contract -v
./godot --headless --editor --path . --quit
./godot --headless --path . res://scenes/vertical_slice/main_menu.tscn --quit-after 2
./godot --headless --path . res://scenes/vertical_slice/vertical_slice_app.tscn --quit-after 2
./godot --headless --path . res://scenes/vertical_slice/screens/vs_workshop_screen.tscn --quit-after 2
```

Also run the repository’s formal GUT workflow command set or its reusable validation script, Task 1 contract, and model/integration regressions equivalent to current PR validation. Any failure prevents artifact creation.

- [ ] **Step 4: Run contract tests and commit**

The normal checked-in branch is still static RED until real PROVE; bridge-specific contract tests must be GREEN.

---

### Task 6: Provenance Artifact Construction and Verification

**Files:**
- Modify: `tools/higodot_task2_bridge.py`
- Modify: `.github/workflows/higodot-task2-authoring-bridge.yml`
- Modify: `tests/test_higodot_task2_ci_authoring_bridge_contract.py`

**Interfaces:**
- Produces artifact directory:

```text
higodot-task2-provenance.json
product/project.godot
product/scenes/vertical_slice/main_menu.tscn
product/scenes/vertical_slice/vertical_slice_app.tscn
product/scenes/vertical_slice/screens/vs_workshop_screen.tscn
validation/
```

- [ ] **Step 1: Add failing provenance tests**

Require deterministic sorted changed paths, lowercase 64-hex SHA-256 values, input head binding, versions, session identity, operation evidence hashes, validation evidence hashes, and artifact file hashes. Explicitly reject token-like fields and arbitrary environment dumps.

- [ ] **Step 2: Implement `build_provenance` and artifact copy**

Copy only the exact four product files after validation passes. Hash after copy and ensure artifact hash equals working-tree hash.

- [ ] **Step 3: Implement `validate_provenance`**

Before upload and again in PUBLISH, validate schema, expected head, exact allowlist, and all content hashes.

- [ ] **Step 4: GREEN tests and commit**

Run bridge pytest and existing document/CI contract suite.

---

### Task 7: Byte-Identical PUBLISH With Branch Race Protection

**Files:**
- Modify: `.github/workflows/higodot-task2-authoring-bridge.yml`
- Modify: `tools/higodot_task2_bridge.py`
- Modify: `tests/test_higodot_task2_ci_authoring_bridge_contract.py`

**Interfaces:**
- Consumes only a successful PROVE artifact.
- Produces one normal fast-forward commit on PR #131 branch containing exactly the four proven bytes.

- [ ] **Step 1: Add failing tests for publish invariants**

Require `publish` needs `prove`, downloads the exact artifact, verifies remote branch SHA equals `expected_head_sha`, validates provenance before copy, and rejects `--force`, `rebase`, `merge`, Godot invocation, HiGodot invocation, MCP invocation, or regeneration commands in PUBLISH.

- [ ] **Step 2: Implement `run_publish_verify`**

Before any commit, verify artifact hashes, expected head, exact output allowlist, and resulting checkout hashes. No semantic editing occurs in PUBLISH.

- [ ] **Step 3: Implement guarded commit/push**

Use a normal commit and push only after a second remote branch-head check. If the remote branch moved, exit non-zero without commit push. Do not force-push.

- [ ] **Step 4: GREEN contract tests and commit**

Run focused bridge contract, CI structure tests, authority tests, and automatic PR checks.

---

### Task 8: Real PROVE → PUBLISH Execution and Task 2 Static GREEN

**Files:**
- Runtime outputs only through the bridge artifact:
  - `scenes/vertical_slice/main_menu.tscn`
  - `scenes/vertical_slice/vertical_slice_app.tscn`
  - `scenes/vertical_slice/screens/vs_workshop_screen.tscn`
  - `project.godot`
- Evidence: GitHub Actions artifact and PR/Sheet status records.

**Interfaces:**
- Consumes: GREEN bridge contract and exact PR head.
- Produces: one exact PR head whose serialized files are attributable to HiGodot PROVE and whose automatic validation is GREEN.

- [ ] **Step 1: Re-read authority immediately before dispatch**

Confirm Blacksmith main/head, PR #131 branch/base/draft/unmerged status, zero unresolved review threads, same-ID Sheet state, and unchanged four-file serialized baseline. If any authority conflict appears, stop before dispatch.

- [ ] **Step 2: Manually dispatch PROVE with exact head**

Pass the current PR head as `expected_head_sha`. Require successful non-headless Xvfb Editor startup, HiGodot/server 3.0.5 identity, unique project session identity, native authoring operations, exact four-file diff, and all pre-artifact validations GREEN.

- [ ] **Step 3: Inspect PROVE artifact before allowing PUBLISH**

Verify provenance, operation sequence, changed-path list, and every SHA-256. Any mismatch blocks PUBLISH.

- [ ] **Step 4: Let PUBLISH copy only the proven bytes**

PUBLISH rechecks remote head, validates hashes, commits the exact four files, and fast-forward pushes. No regeneration occurs.

- [ ] **Step 5: Verify new exact PR head**

Require:

```text
Task 2 static app-shell contract = PASS
Godot 4.7.1 import/parse = PASS
new scene smokes = PASS
GUT 9.7.1 = PASS
Task 1/model/integration regressions = PASS
automatic PR workflows = PASS
changed serialized files = exact four-file allowlist
```

- [ ] **Step 6: Run Full validation on the exact merge-candidate head**

Do not infer Full validation from PR checks. Record its exact run/head/result.

- [ ] **Step 7: Synchronize GitHub and Google Sheet**

Under `BS-HIGODOT-EXEC-20260808-01`, record PROVE run/artifact, PUBLISH commit, exact-head validation, static GREEN, and remaining Android/human/image/general-product gates. Read back the written Sheet cells.

- [ ] **Step 8: Keep PR #131 Draft/unmerged until explicit merge approval**

No merge or Ready-for-Review transition is implied by bridge success.

---

## Self-Review Record

### Spec coverage

- Manual-only trigger and exact branch/head binding: Tasks 3 and 7.
- PROVE read-only vs PUBLISH write separation: Tasks 3 and 7.
- Xvfb non-headless authoring: Task 3; real evidence Task 8.
- Exact Godot/HiGodot/server identity: Tasks 3, 4, 8.
- Unique session/project identity and readback-before-retry: Task 4.
- Godot-native authoring recipe and no serialized-text fallback: Tasks 2 and 4.
- Exact four-file diff and only run/main_scene semantic change: Task 5.
- Validation before artifact: Task 5.
- Provenance and per-file hashes: Task 6.
- Byte-identical publish and branch race protection: Task 7.
- Exact-head automatic CI + Full validation + Sheet readback: Task 8.
- Base generic adapter NOT_READY, Hera NONE, general product blocked, no merge: Global Constraints and Task 8.

### Placeholder scan

The plan contains no unresolved placeholder markers and every task names concrete files, interfaces, commands, expected failures, and completion evidence.

### Type and naming consistency

The driver interfaces are declared once in `Stable driver interfaces` and reused with the same names throughout Tasks 2–7. `expected_head_sha`, `ALLOWED_SERIALIZED_PATHS`, `MCP_URL`, PR #131, target branch, and Decision ID remain consistent across workflow, driver, tests, provenance, and Sheet evidence.

## Execution Boundary For This Review Approval

The approved immediate execution after this plan is **Task 1 only: create and remotely verify the bridge contract RED**. Tasks 2–8 require the observed Task 1 RED as their TDD predecessor. No serialized Godot product file is modified in Task 1.
