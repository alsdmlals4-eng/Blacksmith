# Godot Live-Editor Pilot Adoption

## Status

```yaml
adoption_mode: TEMPORARY_COPY_ONLY
legacy_source_policy: LEGACY_GODOT_AI_SOURCE_PRESERVED
legacy_workspace_policy: LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY
mutation_authority_policy: DUAL_MUTATION_AUTHORITY_FORBIDDEN
main_scene_policy: MAIN_SCENE_READ_ONLY
mutation_policy: SCRATCH_SCENE_MUTATION_ONLY
source_integrity: SOURCE_TREE_UNCHANGED
base_pilot_commit: 2b595570bd237174b2b962a1eb54588b5ecc508d
evidence_bundle: SELF_CONTAINED_EVIDENCE_BUNDLE
PRODUCTION_ADAPTER_READY: NOT_READY
```

This repository adopts the immutable Base C0.1 Pilot commit `2b595570bd237174b2b962a1eb54588b5ecc508d` through four adoption files only.

## Legacy coexistence boundary

The source repository keeps `res://addons/godot_ai/plugin.cfg`, the Godot AI addon bytes, and `_mcp_game_helper` unchanged. The Base runner disables only those declared entries in a disposable copy before activating its own Pilot addon. Godot AI and the Base transaction adapter are never granted mutation authority together.

## Pilot behavior

The Pilot copies the project, disables the declared legacy Plugin and Autoload in the copy, imports and parses Godot 4.7.1, runs the existing merge-conflict contract, and opens `res://scenes/test/enhancement_test.tscn` only under `MAIN_SCENE_READ_ONLY`.

Rename, Editor Undo, save, ledger recording, and physical SHA-256 verification occur only in `res://.godot-live-editor-pilot/scratch.tscn`. The Git-tracked source bytes are inventoried before and after execution; any source mutation fails the Pilot.

## Evidence bundle

The downloaded artifact must contain:

```text
project-pilot-evidence.json
runtime-result.json
scratch.tscn
```

The runtime result and scratch Scene must be independently rehashed after download and match the SHA-256 values recorded in the evidence JSON.

## Protected product boundary

The Pilot does not modify forging, enhancement, economy, save behavior, UI, data, assets, planning Decisions, Google Sheets, `project.godot`, product Scenes, Resources, or GDScript. It does not install a permanent addon, open a listener, create an MCP server, or provide arbitrary shell or project mutation.

Program B authenticated local STDIO transport and Program C opt-in debugger remain unimplemented. No physical-input, accessibility, performance, Android device, Windows production-operation, or human-editor-usability PASS is claimed.

## Removal

Rollback is one revert of these four files:

```text
.github/workflows/validate-godot-live-editor-pilot.yml
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION.md
tests/test_godot_live_editor_adoption.py
```
