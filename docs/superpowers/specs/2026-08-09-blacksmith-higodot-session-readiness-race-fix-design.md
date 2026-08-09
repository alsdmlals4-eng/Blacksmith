# Blacksmith HiGodot Session Readiness Race Fix Design

Decision: `BS-HIGODOT-EXEC-20260808-01`

Date: `2026-08-09 KST`

Status: `USER_APPROVED_DESIGN / WRITTEN_SPEC_REVIEW_APPROVED`

## Problem

The first real manual Task 2 HiGodot PROVE attempt ran on PR #131 at exact input head `9a74857079aa101227ee34efe30989e05b190400` as GitHub Actions run `31312062437`.

The run proved repository/PR/head identity, installed the pinned toolchain, launched Godot 4.7.1 under Xvfb, started the HiGodot/Godot AI MCP server, and observed TCP port 8000 as reachable. The immediately following authoring preflight then failed before any mutation:

```text
ValueError: expected exactly one Blacksmith project session, found 0
```

The editor log from the same run shows that the MCP server became reachable while the Godot plugin was still in its WebSocket connection/retry sequence. Therefore TCP/MCP server readiness can precede registration of the live Godot editor project session.

No approved serialized product file was authored by the failed run. Provenance upload and guarded PUBLISH did not start.

## Root cause

The bridge currently treats one `session_manage(list)` result as final. This is too strict at the startup boundary because the MCP HTTP server and the editor-session registry do not become ready atomically.

The failure is a startup-readiness race, not an authorization, PR identity, Godot version, HiGodot version, recipe, serialized-diff, or merge problem.

## Approved approach

Keep the existing strict fail-closed identity contract, but make only the pre-mutation project-session discovery tolerant of the bounded startup delay.

`preflight_mcp()` will wait for the expected Blacksmith session through a small bounded sequence of read-only `session_manage(list)` calls.

Rules:

1. Retry only when there are **zero matching sessions for the exact normalized project path**.
2. Stop waiting as soon as exactly one matching session appears, then run all existing session identity checks unchanged.
3. If two or more matching sessions are observed, fail immediately as ambiguous. Do not wait for ambiguity to disappear.
4. Invalid `session_manage` payloads fail immediately.
5. Plugin/server/Godot version drift, readiness drift, project-path drift after selection, or activation/readback failures fail immediately.
6. Required MCP tool absence fails before session discovery, as today.
7. No Scene/Node/project-setting mutation may occur until exact session identity and editor readiness are proven.
8. Mutation timeout/connection ambiguity behavior remains unchanged: read back once and fail closed; never blind-retry a mutation.
9. Do not broaden the workflow trigger, do not add push-trigger authoring, and do not replace this with a fixed workflow `sleep`.
10. The approved four-file serialized allowlist and guarded PUBLISH byte-identity rules remain unchanged.

## Timing bound

Use a bounded discovery window of **20 seconds**, polling the read-only session list every **0.5 seconds**. The implementation should keep these values internal to the session-discovery helper so unit tests can exercise retry behavior with a zero delay without waiting in real time.

This window is deliberately separate from the workflow's existing TCP-port wait. The TCP check proves that the server accepts connections; the new session wait proves that the editor has registered the exact project session.

## Code shape

Keep `preflight_mcp()` as the public preflight entry point. Add one small internal helper responsible only for session discovery, for example:

```text
_discover_project_session(client, expected_project_path, attempts, delay_seconds)
```

The helper returns exactly one matching session or raises. It must not activate the session and must not perform any authoring operation.

`preflight_mcp()` then continues with the existing sequence:

```text
required tool check
→ bounded read-only exact-project session discovery
→ strict session version/readiness identity check
→ session_activate
→ editor_state
→ scene_get_hierarchy
→ project_manage(settings_get)
→ only then authoring recipe execution
```

## TDD contract

Implementation must follow RED → GREEN.

Add focused tests to `tests/test_higodot_task2_mcp_driver.py` before changing bridge production code:

- zero matching sessions followed by one exact session is retried and then accepted;
- zero matching sessions through the complete retry budget fails closed without activation;
- the existing ambiguous-session test continues to prove immediate failure with no activation;
- existing version/readiness drift tests continue to fail before activation.

The new retry tests must use a zero poll delay so the unit suite remains deterministic and fast.

## Validation after implementation

Before requesting another real manual PROVE attempt:

1. focused MCP driver tests GREEN;
2. HiGodot bridge/real-PROVE/toolchain/provenance/publish static contracts GREEN;
3. exact new PR #131 head read back from GitHub;
4. all applicable remote CI read back on that exact head;
5. Google Sheet synchronized under `BS-HIGODOT-EXEC-20260808-01`;
6. only then provide the new exact `expected_head_sha` for one new manual workflow dispatch.

A successful second PROVE must still pass the existing serialized diff, Godot import/smoke, GUT, Task 1 regression, model/integration, provenance, race-check, and guarded PUBLISH gates.

## Non-goals

This fix does not:

- author or hand-edit `project.godot` or `.tscn` files;
- change the Task 2 scene design;
- change HiGodot/GUT/Hera authority;
- change Godot 4.7.1 or Godot AI/HiGodot 3.1.3 pins;
- relax exact PR/head identity;
- retry mutations;
- merge PR #131;
- authorize general product implementation.

## Rollback

If the bounded session-discovery change produces unexpected behavior, revert only the focused bridge/test fix. The manual PROVE workflow remains fail-closed and PR #131 remains Draft/unmerged.
