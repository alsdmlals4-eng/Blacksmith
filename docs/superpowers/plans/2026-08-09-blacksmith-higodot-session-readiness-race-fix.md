# Blacksmith HiGodot Session Readiness Race Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the pre-mutation startup session-registration race in the PR #131 HiGodot Task 2 PROVE bridge without weakening identity, authority, mutation, provenance, or publish gates.

**Architecture:** Keep `preflight_mcp()` as the public entry point and add one internal read-only discovery helper that polls `session_manage(list)` only while zero exact-project matches exist. The production default performs 41 list attempts with 0.5 second delays between attempts, which yields at most 20 seconds of waiting; tests inject a zero delay and small attempt count. As soon as one session appears, all existing strict version/readiness/activation/readback checks continue unchanged. Ambiguity and malformed payloads fail immediately.

**Tech Stack:** Python 3.12, asyncio, pytest, FastMCP, Godot 4.7.1-stable, Godot AI/HiGodot 3.1.3, GitHub Actions.

## Global Constraints

- Decision ID: `BS-HIGODOT-EXEC-20260808-01`.
- Target PR: `#131`; branch: `feat/vertical-slice-task2-app-shell`.
- Godot: exact `4.7.1-stable`.
- HiGodot/Godot AI: exact `3.1.3`.
- Retry is permitted only for read-only `session_manage(list)` while the exact normalized project path has zero matches.
- Production discovery budget: 41 attempts, 0.5 seconds between zero-match attempts; maximum sleep time 20 seconds.
- Two or more exact-project sessions fail immediately; no retry on ambiguity.
- Invalid session payload, plugin/server/Godot drift, readiness drift, activation failure, editor-state failure, hierarchy/readback failure all fail immediately.
- Mutation timeout/connection handling remains readback-once then fail closed; no blind mutation retry.
- No workflow-trigger broadening and no fixed workflow `sleep` replacement.
- No direct `.tscn` or `project.godot` write.
- Serialized allowlist remains exactly `project.godot`, `scenes/vertical_slice/main_menu.tscn`, `scenes/vertical_slice/vertical_slice_app.tscn`, and `scenes/vertical_slice/screens/vs_workshop_screen.tscn`.
- PR #131 remains Draft/unmerged; merge requires separate approval.

---

### Task 1: TDD RED for bounded session discovery

**Files:**
- Modify: `tests/test_higodot_task2_mcp_driver.py`

**Interfaces:**
- Consumes existing `FakeClient`, `_session()`, `_required_tools()`.
- Defines required future helper interface: `async _discover_project_session(client, expected_project_path, *, attempts: int, delay_seconds: float) -> dict`.

- [ ] **Step 1: Make preflight fixture preserve explicit empty session lists**

Change `_preflight_responses()` so `sessions=[]` is not replaced by the default session. Use `sessions is None`, not truthiness, when selecting the default list.

- [ ] **Step 2: Add retry-success RED**

Add a test that supplies two `session_manage` responses in order: first `{"sessions": [], "count": 0}`, then one exact `_session()`. Call `_discover_project_session(..., attempts=2, delay_seconds=0)`. Assert the returned `session_id` is `SESSION_ID` and the client made exactly two `session_manage` calls and no activation/mutation call.

- [ ] **Step 3: Add retry-exhaustion RED**

Add a test with two empty `session_manage` responses. Call `_discover_project_session(..., attempts=2, delay_seconds=0)` and require `ValueError` matching `expected exactly one Blacksmith project session, found 0`. Assert only two `session_manage` calls occurred.

- [ ] **Step 4: Run focused test to verify RED**

Run:

```bash
python -m pytest tests/test_higodot_task2_mcp_driver.py -q
```

Expected: the two new tests fail because `_discover_project_session` does not exist. Existing tests remain otherwise stable.

- [ ] **Step 5: Commit RED only**

Commit only `tests/test_higodot_task2_mcp_driver.py` with message:

```text
test: cover delayed HiGodot session registration
```

---

### Task 2: Minimal bounded read-only discovery implementation

**Files:**
- Modify: `tools/higodot_task2_bridge.py`

**Interfaces:**
- Produces `SESSION_DISCOVERY_ATTEMPTS = 41`.
- Produces `SESSION_DISCOVERY_DELAY_SECONDS = 0.5`.
- Produces `_discover_project_session(client, expected_project_path, *, attempts=SESSION_DISCOVERY_ATTEMPTS, delay_seconds=SESSION_DISCOVERY_DELAY_SECONDS) -> dict[str, Any]`.
- `preflight_mcp()` consumes the helper and performs all existing strict checks after it returns.

- [ ] **Step 1: Add `asyncio` import and timing constants**

Add `import asyncio`, `SESSION_DISCOVERY_ATTEMPTS = 41`, and `SESSION_DISCOVERY_DELAY_SECONDS = 0.5` near the existing bridge constants.

- [ ] **Step 2: Implement `_discover_project_session()`**

The helper must:

```python
if attempts < 1:
    raise ValueError("session discovery attempts must be at least 1")
if delay_seconds < 0:
    raise ValueError("session discovery delay must be non-negative")
```

For each attempt, call only:

```python
listing = await client.call("session_manage", {"op": "list", "params": {}})
```

Reject non-list `sessions` immediately. Filter exact normalized `project_path` matches. Return immediately on one match. Raise immediately on more than one match. On zero matches, `await asyncio.sleep(delay_seconds)` only if another attempt remains. After the budget, raise the existing zero-match error text.

- [ ] **Step 3: Replace the one-shot discovery block in `preflight_mcp()`**

After required-tool validation, call:

```python
session = await _discover_project_session(client, expected_project_path)
```

Then leave `_require_session_identity`, session ID extraction, `session_activate`, `editor_state`, hierarchy, and `project_manage(settings_get)` behavior unchanged.

- [ ] **Step 4: Run focused GREEN**

Run:

```bash
python -m pytest tests/test_higodot_task2_mcp_driver.py -q
```

Expected: all MCP driver tests pass, including immediate ambiguous-session and version/readiness failure behavior.

- [ ] **Step 5: Commit implementation**

Commit only `tools/higodot_task2_bridge.py` with message:

```text
fix: wait for HiGodot project session readiness
```

---

### Task 3: Regression and exact-head remote validation

**Files:**
- No new product files.
- Read/validate existing bridge, workflow, tests, PR metadata, and Sheet.

**Interfaces:**
- Produces one exact new PR #131 head suitable for a second manual PROVE only if all non-serialized gates are current and acceptable.

- [ ] **Step 1: Run focused/static regression suites**

Require GREEN for:

```text
tests/test_higodot_task2_mcp_driver.py
tests/test_higodot_task2_ci_authoring_bridge_contract.py
tests/test_higodot_task2_real_prove_contract.py
tests/test_higodot_task2_toolchain_pin.py
tests/test_higodot_task2_313_runtime_contract.py
tests/test_higodot_task2_post_authoring_gate.py
tests/test_higodot_task2_provenance_artifact.py
tests/test_higodot_task2_publish_guard.py
```

Do not reinterpret the existing Task 2 serialized app-shell RED as a bridge regression while the approved four outputs remain unmaterialized.

- [ ] **Step 2: Read exact PR #131 head and merge-candidate SHA separately**

Record the branch head as the future `expected_head_sha`. Record GitHub's test-merge/merge candidate SHA separately; never substitute it for the branch head.

- [ ] **Step 3: Read all applicable GitHub Actions on that exact head**

Do not reuse checks from `9a748570...`, `5839d49d...`, or intermediate RED commits as final proof. Investigate any new failure before asking the user to dispatch.

- [ ] **Step 4: Recheck PR review state**

Read reviews/comments/unresolved threads. PR #131 remains Draft and unmerged.

- [ ] **Step 5: Synchronize Google Sheet under the same Decision ID**

Update `BS-HIGODOT-EXEC-20260808-01` to record written-spec approval, TDD RED evidence, implementation head, validation state, and the new exact manual-PROVE SHA. Do not mark live authoring/provenance/PUBLISH as complete.

- [ ] **Step 6: Hand off one new manual dispatch**

Only after the exact-head checks are current, instruct the user to run `HiGodot Task 2 Authoring Bridge` on `feat/vertical-slice-task2-app-shell` with the new exact branch HEAD. Never reuse `9a74857079aa101227ee34efe30989e05b190400`.
