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
expected_platform: ANDROID
PRODUCTION_ADAPTER_READY: NOT_READY
```

This repository adopts the immutable Base C0.1 Pilot commit `2b595570bd237174b2b962a1eb54588b5ecc508d` through four adoption files only.

## Legacy coexistence boundary

`LEGACY_GODOT_AI_SOURCE_PRESERVED` means the source repository keeps `res://addons/godot_ai/plugin.cfg`, the Godot AI addon bytes, and `_mcp_game_helper` unchanged.

`LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY` means the Base runner copies the project to a temporary workspace and disables only the declared Plugin and Autoload entries in that copy. The source `project.godot` remains byte-identical.

`DUAL_MUTATION_AUTHORITY_FORBIDDEN` means Godot AI and the Base transaction adapter are never active together in the Pilot workspace.

## Pilot execution

The workflow creates and prepares a disposable project copy, imports and parses it with Godot 4.7.1, then runs the same fourteen model and integration GDScript checks used by the authoritative Godot validation workflow.

The configured main Scene `res://scenes/test/enhancement_test.tscn` is opened only under `MAIN_SCENE_READ_ONLY`.

Rename, Editor Undo, save, ledger recording, and physical SHA-256 verification occur only in the runner-owned `res://.godot-live-editor-pilot/scratch.tscn` under `SCRATCH_SCENE_MUTATION_ONLY`.

The source Git-tracked bytes are inventoried before and after execution. Any source change violates `SOURCE_TREE_UNCHANGED` and fails the Pilot.

## Evidence bundle

`SELF_CONTAINED_EVIDENCE_BUNDLE` requires the downloaded artifact to contain:

```text
project-pilot-evidence.json
runtime-result.json
scratch.tscn
```

The runtime result and saved scratch Scene must be independently rehashed after download and match the SHA-256 values recorded in the evidence JSON.

## Protected product and planning boundary

The Pilot does not change crafting, enhancement, economy, customer, lifecycle, save, UI, data, assets, planning Decisions, Registry, or Google Sheets. Product Scenes, Resources, and GDScript remain unchanged.

`expected_platform: ANDROID` records the intended platform only. This Pilot does not execute an Android device, APK, AAB, touch, safe-area, accessibility, performance, or human playtest.

The Pilot does not install a permanent addon, open a network listener, create an MCP server, or provide arbitrary property, script, shell, or project mutation.

## Program exclusions

Program B authenticated local STDIO MCP transport and Program C opt-in runtime debugger are not implemented. Both require separate design, approval, TDD, adversarial review, and merge gates.

```yaml
android_device: NOT_RUN
physical_input: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
windows_production_operation: NOT_RUN
PRODUCTION_ADAPTER_READY: NOT_READY
```

## Removal

Rollback is one revert of the four adoption files:

```text
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION.md
tests/test_godot_live_editor_adoption.py
.github/workflows/validate-godot-live-editor-pilot.yml
```

No product or planning file must be edited to remove this Pilot.
