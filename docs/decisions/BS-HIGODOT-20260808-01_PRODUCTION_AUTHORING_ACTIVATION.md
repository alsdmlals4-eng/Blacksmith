# BS-HIGODOT-20260808-01 — HiGodot Production Authoring Activation

## Decision

```text
DECISION_ID: BS-HIGODOT-20260808-01
STATUS: USER_APPROVED_PRODUCTION_AUTHORING_ACTIVATION
HIGODOT_AUTHORING_AUTHORITY: FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY
PRODUCTION_ACTIVATION: USER_APPROVED_ACTIVE
TASK2_SCOPE: TASK2_SCOPED_AUTHORING_ONLY
GENERAL_PRODUCT_IMPLEMENTATION: GENERAL_PRODUCT_IMPLEMENTATION_BLOCKED
GUT_AUTHORITY: GUT_SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY
HERA_AUTHORITY: HERA_AUTHORITY_NONE
MIXED_SURFACE_RULE: FILE_AUTHORITY_MANIFEST_REQUIRED_FOR_MIXED_SURFACE_PR
MERGE_APPROVAL: NOT_GRANTED
```

User approval was recorded on 2026-08-08 for the previously recommended next step: activate HiGodot production authoring for the already approved Task 2 MainMenu / BlacksmithApp / Workshop authoring boundary. This approval is not PR #131 merge approval and does not open general product implementation.

## Activated authority

HiGodot (`hi-godot/godot-ai`, installed at `addons/godot_ai`) is the sole production authoring authority for Godot serialization surfaces after this Decision:

- `project.godot`
- `**/*.tscn`
- `**/*.tres`
- `**/*.res`
- Godot Scene/Node graphs
- Godot project settings, plugins, autoload declarations, and InputMap serialization

The active policy role remains `SOLE_GODOT_AUTHORING_AUTHORITY`.

## Task 2 scope

This activation does not grant unrestricted product implementation. Under Decision `BS-VS-TASK2-20260807-01`, the only currently approved HiGodot production-authoring scope is:

- `scenes/vertical_slice/main_menu.tscn`
- `scenes/vertical_slice/vertical_slice_app.tscn`
- `scenes/vertical_slice/screens/vs_workshop_screen.tscn`
- the single `application/run/main_scene` migration in `project.godot`

The existing 720×1280 portrait, renderer, autoload, plugin, input, and other project settings must be preserved. No external product assets are authorized by this Decision.

## Authoring provenance requirement

Production Godot serialization surfaces must be authored through an actual HiGodot production-authoring execution path. A generic code editor, GitHub contents API, or direct text replacement must not be represented as HiGodot authoring and must not be used to bypass this ownership rule.

At approval time, the repository's existing Godot Live-Editor workflow remains a bounded pilot with `source_mutation_policy: FORBIDDEN`, scratch-scene-only mutation, and read-only GitHub permissions. Therefore:

```text
HIGODOT_PRODUCTION_AUTHORITY: ACTIVE
HIGODOT_PRODUCTION_EXECUTION_PATH: BLOCKED_UNAVAILABLE_OR_UNVERIFIED
TASK2_SCENE_PROJECT_GREEN: BLOCKED_PENDING_COMPLIANT_HIGODOT_EXECUTION_PATH
```

Authority activation and execution capability are separate facts. Until a compliant production authoring path exists and produces attributable evidence, Task 2's Scene/`project.godot` static RED remains fail-closed.

## Authority separation

- GUT 9.7.1 remains `FORMALLY_ADOPTED_ACTIVE` and the sole GDScript test framework authority.
- HiGodot must not edit `tests/gut/**`, `.gutconfig.json`, `addons/gut/**`, or JUnit success evidence.
- GUT runtime must not mutate tracked Scene/Resource/`project.godot` surfaces.
- Hera Agent Godot remains `VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE`; its authoring/mutation authority remains `NONE`.
- Same-file dual authority and unknown-authority changes remain fail-closed.

## Mixed-surface PR evidence

Before any HiGodot-owned production surface is added to PR #131, the PR must carry a file-by-file authority manifest that attributes each changed path to its authorized writer. `FILE_AUTHORITY_MANIFEST_REQUIRED_FOR_MIXED_SURFACE_PR` is mandatory once the PR contains multiple authority classes.

## Unchanged gates

```text
GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED
PRODUCT_IMAGE_RIGHTS: BLOCKED_NOT_RUN
ANDROID_DEVICE_VALIDATION: NOT_RUN
HUMAN_PLAYTEST: NOT_RUN
HERA_ACTIVATION: NOT_APPROVED
PR131_MERGE: NOT_APPROVED
BASE_MAIN_UPGRADE: DEFERRED
```

The next compliant step is to establish or expose a real HiGodot production-authoring execution path, prove its provenance and bounded write surface, then use it to drive the existing Task 2 static RED toward GREEN. Direct textual Scene/`project.godot` authoring is forbidden.