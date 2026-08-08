# BS-HIGODOT-EXEC-20260808-01 — Task 2 HiGodot CI Authoring Bridge

Status: `USER_APPROVED_DESIGN / WRITTEN_SPEC_REVIEW_PENDING / IMPLEMENTATION_NOT_STARTED`

Approved at: `2026-08-08 KST`

## Decision

Adopt a project-specific CI execution bridge for the remaining Task 2 HiGodot-owned serialized surfaces.

The bridge uses a separated `PROVE → PUBLISH` model:

- **PROVE** runs with `contents: read`, starts a real Godot 4.7.1 Editor under Xvfb, uses the vendored HiGodot/Godot AI 3.0.5 MCP authoring path, validates the resulting working tree, and emits a provenance bundle.
- **PUBLISH** is the only `contents: write` job. It does not run Godot or HiGodot; it verifies and publishes only the byte-identical serialized outputs that PROVE already authored and validated.

Approved serialized output scope is exactly:

```text
scenes/vertical_slice/main_menu.tscn
scenes/vertical_slice/vertical_slice_app.tscn
scenes/vertical_slice/screens/vs_workshop_screen.tscn
project.godot  # application/run/main_scene only
```

## Authority boundary

This Decision consumes `BS-HIGODOT-20260808-01` and does not broaden its authority beyond Task 2.

- HiGodot remains the sole Godot Scene/Resource/project-settings production authoring authority for the approved scope.
- GUT 9.7.1 remains the sole GDScript test-framework authority.
- Hera remains vendored, disabled, non-authoritative, authority `NONE`.
- General product implementation remains blocked outside the approved vertical-slice scope.
- Base current main is not adopted by this Decision.
- Base generic Godot production adapter remains `NOT_READY`; this project bridge must not claim otherwise.

## Mandatory provenance constraints

- No `--headless` mutation session: vendored HiGodot disables MCP in headless mode.
- Mutation must occur through the live Godot Editor + HiGodot MCP path.
- Exact PR/branch/head/project/session identity must be proven before mutation.
- Exact compatible plugin/server versions must be proven; no floating upgrade is allowed.
- Direct generic text/GitHub API authoring of `.tscn` or `project.godot` is forbidden.
- No filesystem/script text-write fallback may impersonate Godot-native Scene/Node/project-setting operations.
- Any mutation timeout or ambiguous result requires readback before retry; unresolved ambiguity fails closed.
- Any tracked diff outside the exact four-file allowlist fails closed.
- PUBLISH must verify artifact hashes and branch head freshness and must never regenerate or modify the proven bytes.

## Evidence and validation

Before publication, PROVE must produce a self-contained provenance manifest that binds:

- Decision IDs;
- repository/PR/input head;
- Godot and HiGodot/server versions;
- active MCP session/project identity;
- ordered operation names and canonical input/result status hashes;
- exact changed-file list;
- serialized file hashes;
- focused Task 2, Godot 4.7.1, GUT, and required regression validation evidence.

After publication, automatic PR validation and Full validation must pass on the exact merge-candidate head before merge readiness.

## Current state

```text
DESIGN = USER_APPROVED
WRITTEN_SPEC = docs/superpowers/specs/2026-08-08-blacksmith-higodot-ci-authoring-bridge-design.md
WRITTEN_SPEC_REVIEW = PENDING
IMPLEMENTATION_PLAN = NOT_STARTED
BRIDGE_TDD = NOT_STARTED
TASK2_STATIC_APP_SHELL = EXPECTED_RED
SCENE_PROJECT_MUTATION = 0
PR131 = DRAFT_UNMERGED
```

## Merge gate

This Decision is not merge approval. PR #131 must remain unmerged until a separate explicit user approval after exact-head validation.