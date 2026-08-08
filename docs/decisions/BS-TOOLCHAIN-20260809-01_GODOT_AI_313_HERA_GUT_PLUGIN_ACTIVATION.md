# BS-TOOLCHAIN-20260809-01 — Godot AI 3.1.3 and Editor Plugin Activation

Status: `USER_APPROVED_TARGET_STATE / GITHUB_SYNC_PENDING`

Approved: `2026-08-09 KST`

## Decision

The user approved the following project toolchain target state:

```text
GODOT_AI_TARGET_VERSION = 3.1.3
GODOT_AI_RUNTIME_MIGRATION = USER_APPROVED
HERA_EDITOR_PLUGIN_ENABLEMENT = USER_APPROVED
GUT_EDITOR_PLUGIN_ENABLEMENT = USER_APPROVED
GUT_TEST_AUTHORITY = FORMALLY_ADOPTED_ACTIVE / SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY
HERA_AUTHORING_AUTHORITY = NONE_UNLESS_SEPARATELY_SCOPED
GENERAL_PRODUCT_IMPLEMENTATION = BLOCKED
```

This Decision acknowledges plugin enablement approval without silently expanding writer authority. HiGodot remains the sole Godot Scene/Resource/project-settings production authoring authority for the currently approved Task 2 serialized scope. GUT remains the sole GDScript test-framework authority. Hera may be enabled as an editor plugin, but this Decision alone does not grant Hera authority to author or mutate HiGodot-owned serialized product surfaces.

## Live GitHub readback at approval processing

The authoritative repository had not yet received the reported local/editor state when this Decision was recorded:

```text
BLACKSMITH_MAIN = f02619ad8603318015017a0c9ab9ac76bd703384
PR131_HEAD = 52ace3f4df07ab9fccc4d375c4ee58b260d15084
GITHUB_GODOT_AI_PLUGIN_VERSION = 3.0.5
GITHUB_EDITOR_PLUGINS = GODOT_AI_ONLY
HERA_PLUGIN_PRESENT = 1.0.0
GUT_PLUGIN_PRESENT = 9.7.1
GITHUB_SYNC = PENDING
```

Therefore the user's reported local/editor update and the GitHub repository state are intentionally distinguished. No repository claim of `3.1.3 installed` or `Hera/GUT enabled` is valid until a later exact GitHub readback proves those bytes/settings are present.

## Godot AI 3.1.3 bridge migration

The approved Task 2 HiGodot CI bridge may migrate its runtime identity from 3.0.5 to exact 3.1.3 under TDD. The runtime remains version-pinned and fail-closed:

```text
GODOT_AI_SERVER = godot-ai==3.1.3
FASTMCP = 3.4.2
UV = 0.12.3
GODOT = 4.7.1-stable
```

The existing Task 2 operation family must remain compatible before live authoring is permitted. No floating package selector or automatic vendor upgrade is allowed.

## Repository synchronization boundary

The following reported local changes remain pending GitHub synchronization:

- `addons/godot_ai/plugin.cfg` / vendor tree reflecting version 3.1.3;
- `project.godot` editor-plugin enablement containing Godot AI, Hera Agent Godot, and GUT.

`project.godot` is a HiGodot-owned serialized/project-settings surface. ChatGPT must not simulate this local activation by generic text replacement or GitHub Contents API writes. The exact project setting must arrive through the approved Godot/HiGodot authoring path or be pushed from the user's already-performed local Godot editor change and then independently verified.

The Godot AI vendor update is also not recreated from memory or a floating upstream snapshot. Exact repository bytes/provenance must be read after synchronization.

## Task 8 gate

Actual Task 2 real PROVE remains fail-closed until all of these are true on one exact PR head:

1. bridge runtime contracts are GREEN for exact Godot AI 3.1.3;
2. the default-branch manual-dispatch workflow is synchronized to the same 3.1.3 runtime contract;
3. GitHub readback proves the intended Godot AI 3.1.3 vendor/plugin state;
4. GitHub readback proves Hera and GUT editor-plugin enablement;
5. same Decision ID is synchronized to the Google Sheet;
6. no unexpected authoring-authority expansion or serialized diff is present.

Until then:

```text
LIVE_HIGODOT_PROVE = BLOCKED_PENDING_313_AND_PLUGIN_STATE_SYNC
PRODUCT_SERIALIZED_MUTATION = 0
PR131 = DRAFT_UNMERGED
```

## Relationship to existing Decisions

- `BS-HIGODOT-20260808-01`: HiGodot Task 2 scoped production authoring authority remains active.
- `BS-HIGODOT-EXEC-20260808-01`: PROVE → PUBLISH bridge architecture remains active; only exact toolchain identity is migrated after TDD.
- `BS-HERA-20260808-01`: prior disabled-state record remains historical evidence. This Decision supersedes only the editor-plugin activation state once GitHub synchronization is proven; it does not grant Hera serialized authoring authority.
- `BS-TEST-20260806-01`: GUT 9.7.1 formal test authority is unchanged; editor-plugin enablement is an additional approved runtime/editor state, not a replacement test authority.
