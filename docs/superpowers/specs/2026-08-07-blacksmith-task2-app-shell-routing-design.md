# Blacksmith Task 2 — App Shell and Start-Scene Routing Design

Decision ID: `BS-VS-TASK2-20260807-01`

Status: `USER_APPROVED_DESIGN / AUTHORITY_REFRESHED_ON_MAIN_a00e864 / IMPLEMENTATION_NOT_STARTED / ENTRY_GATE_REVIEW_PENDING`

Base project main at design approval: `bd7e97ec49b2fac67f619c9bbe5e2c6e53c48d6f`

Current project main at authority refresh: `a00e864ce5de7bdf872e8093d489c8a78c058afb`

## Authority

This design consumes and does not replace the following approved decisions:

- `BS-MAIN-20260801-01` — separate main menu before the game shell; required actions are Continue, New Game, Settings; Continue is disabled when no loadable save exists.
- `BS-SHELL-20260801-01` — after the separate main menu, campaign views run inside one `BlacksmithApp` shell with view/overlay separation and shared campaign state.
- `BS-VS-20260806-01` — scoped vertical-slice implementation is approved while general product implementation remains blocked.
- `BS-SAVE-20260806-01` — save/load must preserve already resolved facts and must not reroll them.
- `BS-TEST-20260806-01` — GUT 9.7.1 is the formal GDScript test authority.
- `BS-HERA-20260808-01` — Hera Agent Godot is `VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE`; authoring/mutation authority remains `NONE` unless a separate adoption is approved.

Current authority evidence at refresh:

- PR #133 postmerge Hera closure is main canon.
- PR #134 cross-platform hash regression fix is main canon at `a00e864ce5de7bdf872e8093d489c8a78c058afb`.
- Full validation #113 is PASS, including Windows Python 3.11/3.12/3.13, Ubuntu Python 3.11/3.12/3.13, Godot 4.7.1, and pinned Base governance.
- Godot Live-Editor Pilot #22 is PASS.
- the standalone HiGodot/GUT authority workflow still has the separately tracked pre-existing zero-job startup failure; this does not grant production authoring authority or open a product gate.

The approved implementation approach is **B**: Task 2 changes the actual Godot application start scene, rather than leaving the historical test scene as the executable entry point.

## Goal

Replace the historical test-scene application entry with the smallest production-shaped vertical-slice shell that satisfies the approved main-menu and app-shell contracts without implementing later gameplay systems.

The executable flow for Task 2 is:

```text
Godot application start
→ MainMenu
→ Continue / New Game / Settings
→ BlacksmithApp
→ Workshop
```

Task 2 proves real application entry, save-aware main-menu behavior, safe transition into one persistent app shell, bounded screen routing, and minimum mobile interaction constraints.

## Scope

### New runtime surfaces

- `scripts/vertical_slice/ui/vs_main_menu.gd`
- `scripts/vertical_slice/ui/vs_app.gd`
- `scenes/vertical_slice/main_menu.tscn`
- `scenes/vertical_slice/vertical_slice_app.tscn`
- `scenes/vertical_slice/screens/vs_workshop_screen.tscn`

The Task 2 Settings overlay is an inline child of `main_menu.tscn`; no standalone settings scene or persistent settings subsystem is introduced in this task.

Task 2 uses engine-native Control/Container/Label/Button-style UI only. It creates no new image, audio, font, or other external product asset files and does not claim that blocked product-image or rights gates are complete.

### Validation surfaces

- focused GUT 9.7.1 tests for main-menu and app routing
- focused Python contract tests for Task 2 file boundaries, start-scene routing, and mobile target requirements
- CI routing/gate changes only when required to admit this approved Task 2 scope

### Existing file intentionally changed

- `project.godot`
  - change `run/main_scene` from the historical enhancement test scene to `res://scenes/vertical_slice/main_menu.tscn`
  - preserve existing 720×1280 viewport, portrait orientation, renderer, autoload, and plugin settings unless a separate approved issue is discovered
  - do not enable Hera or add another authoring plugin

## Out of scope

Task 2 does not implement:

- forge gameplay or forging calculations
- enhancement gameplay or probabilities
- customer assignment or customer success calculations
- schedule/world-event resolution
- result-generation logic
- item birth logic beyond consuming existing Task 1 save state
- archive, sales, economy, monetization, advertising, localization, final art, or final audio
- product image generation or asset-rights completion
- Android release-quality validation
- human playtest approval
- Base main adoption
- replacement or expansion of the current HiGodot/plugin authority model
- Hera activation, adoption, authoring, or mutation

No fake gameplay screen is added merely to satisfy the transition graph.

## Architecture

### 1. MainMenu is an application-entry boundary

`MainMenu` is a separate scene and is not a state inside `BlacksmithApp`.

Responsibilities:

- inspect save availability through a narrow status classification backed by `VSSaveService.load_envelope()`
- enable Continue whenever `VSSaveService` returns a loadable envelope, including a valid backup recovery
- expose New Game and Settings
- require overwrite confirmation before replacing any existing but resumable or non-resumable campaign state
- display explicit error/status text for no-save, recovered-backup, and unrecoverable/unsupported-save states
- launch `BlacksmithApp` only after a valid Continue or confirmed New Game action

Save-status classification is based on the service result, not direct UI file mutation:

```text
validation_errors empty
→ LOADABLE
→ Continue enabled
→ recovered_from_backup=true is still LOADABLE and is surfaced as recovery status

SAVE_NOT_FOUND
→ MISSING
→ Continue disabled
→ New Game may proceed without overwrite confirmation

any other validation error after VSSaveService recovery attempts
→ UNRECOVERABLE_OR_UNSUPPORTED
→ Continue disabled
→ New Game requires explicit overwrite confirmation
```

Non-responsibilities:

- no crafting, enhancement, customer, schedule, result, or RNG calculation
- no mutation of item facts except through an explicitly approved new-run initialization path
- no silent repair, replacement, or reroll of an unrecoverable save
- no direct UI deletion, rename, or overwrite of save files

### 2. BlacksmithApp is the persistent campaign shell

`BlacksmithApp` owns only application navigation and shared campaign-session references.

Initial in-shell state:

```text
WORKSHOP
```

It must not own canonical game calculations.

The shell exposes a bounded transition interface such as:

```text
transition_to(next_state, payload = {})
can_transition(previous_state, next_state)
```

and emits routing events such as:

```text
state_changed(previous, current)
item_selected(uid)
```

### 3. Declared state graph

Task 2 implements only `WORKSHOP` visually, but declares the approved future routing graph so later tasks cannot bypass expected flow accidentally.

```text
WORKSHOP → FORGE | ITEM_DETAIL
FORGE → ITEM_BIRTH
ITEM_BIRTH → ENHANCEMENT | WORKSHOP
ENHANCEMENT → PRECISION | CUSTOMER | WORKSHOP
PRECISION → CUSTOMER | WORKSHOP
CUSTOMER → RESULT
RESULT → REPAIR | ITEM_DETAIL
REPAIR → ITEM_DETAIL
ITEM_DETAIL → WORKSHOP
```

The router distinguishes **declared states** from **implemented destinations**:

- `can_transition(previous, next)` checks only whether the edge exists in the declared graph.
- `transition_to(next, payload)` additionally requires the destination to be implemented and registered.
- a declared-but-not-yet-implemented destination returns a fail-closed `MISSING_DESTINATION` result, leaves current state unchanged, and emits no `state_changed` event.
- an undeclared state or undeclared edge returns a fail-closed `INVALID_TRANSITION` result and likewise leaves state unchanged.

Task 2 must not instantiate placeholder gameplay scenes for future states. Future state names are routing contracts only until their task supplies a real consumer.

### 4. Settings is an overlay boundary

Settings is modeled as an inline overlay child of `MainMenu` for Task 2, not as a standalone scene or full settings system.

Task 2 proves only:

- open overlay
- focus moves into overlay
- close/back returns to MainMenu
- no campaign state is created or changed by opening Settings

Persistent settings fields, audio controls, accessibility presets, and platform-specific behavior remain later scope unless already required by an executable contract.

## Main-menu behavior

### No save

- Continue disabled
- explicit text communicates that no resumable game exists
- New Game enabled without overwrite confirmation
- Settings enabled

### Valid primary save

- Continue enabled
- Continue loads the existing envelope and enters `BlacksmithApp` without rerolling or replacing resolved data
- New Game requests overwrite confirmation before replacing the save through the save-service authority

### Valid backup recovery

- Continue enabled
- recovered envelope is used exactly as returned by `VSSaveService`
- explicit recovery status is visible so backup recovery is not silent
- no reroll or synthesized replacement is performed
- New Game still requires overwrite confirmation

### Unrecoverable or unsupported save

This state means `VSSaveService` has already exhausted its current primary/backup recovery behavior and still returns validation errors other than `SAVE_NOT_FOUND`.

- Continue disabled
- explicit error/status text shown
- no automatic new game
- no silent fallback that can overwrite the existing file
- no reroll or synthesized result to make the save appear valid
- New Game requires explicit overwrite confirmation before a replacement envelope is saved

## New-game boundary

If `VSSaveService` reports `SAVE_NOT_FOUND`, New Game may enter the Task 2 shell with the minimum valid empty campaign envelope required by the existing Task 1 schema.

If a loadable recovered/primary envelope or an unrecoverable/unsupported existing campaign is reported, destructive replacement requires an explicit confirmation action.

Replacement persists only through the existing save-service authority. UI code must not directly delete, rename, or overwrite save files.

## Mobile and accessibility constraints

The design viewport remains 720×1280 portrait.

For Task 2 scenes:

- every primary interactive control has minimum custom size of at least 48×48 logical pixels
- enabled/disabled/error information is not conveyed by color alone
- Continue disabled state has textual or semantic status in addition to appearance
- backup-recovery state has textual status in addition to appearance
- controls use container-based layout rather than fixed absolute positioning for primary structure
- text must not require final art assets to remain legible
- keyboard focus behavior must remain deterministic enough for headless/desktop validation even though Android touch is the target interaction

Actual Android device validation remains `NOT_RUN` and is not inferred from desktop/headless tests.

## Error handling

Routing errors fail closed:

- undeclared transition → `INVALID_TRANSITION`, state unchanged
- declared but unimplemented destination → `MISSING_DESTINATION`, state unchanged
- invalid payload → state unchanged

Save-status errors fail closed:

- missing save after service recovery rules → Continue disabled
- unrecoverable parse/validation failure → Continue disabled with explicit status
- unsupported schema after recovery rules → Continue disabled with explicit status
- valid backup recovery → Continue enabled with explicit recovery status

No error path may trigger gameplay RNG, item creation, or destructive save replacement as a fallback.

## TDD strategy

Implementation must follow `RED → GREEN → REFACTOR`.

### RED contract

The first implementation commit must add tests/contracts that fail on current main because:

- `project.godot` still points to `res://scenes/test/enhancement_test.tscn`
- `MainMenu`, `BlacksmithApp`, and Workshop vertical-slice scene do not exist
- save-aware Continue behavior does not exist
- backup-recovery UI status does not exist
- overwrite confirmation does not exist
- bounded app routing does not exist
- Task 2 48×48 interaction-size contract does not exist

RED evidence must be recorded from the exact commit that contains tests but not the implementation.

### GREEN contract

GREEN requires, at minimum:

- Python Task 2 contract tests PASS
- GUT main-menu tests PASS
- GUT app-routing tests PASS
- Godot 4.7.1 project import/parse PASS
- `main_menu.tscn` headless smoke PASS
- `vertical_slice_app.tscn` headless smoke PASS
- existing Task 1 tests remain PASS
- existing GUT formal suite remains PASS
- automatic PR workflows PASS on one exact HEAD
- Full validation runs on that same exact HEAD before merge readiness

### REFACTOR constraints

Refactor only after GREEN. Refactor may remove duplication or clarify routing interfaces but must not expand Task 2 into later gameplay screens.

## CI and product-boundary policy

Current product gates must be widened only as narrowly as required for this approved task.

Allowed Task 2 product changes are limited to:

```text
scripts/vertical_slice/ui/
scenes/vertical_slice/
project.godot
```

plus focused tests and CI contract routing.

No Task 2 implementation change may add or modify `assets/`, `addons/`, unrelated gameplay services, historical POC models, or external visual/audio/font assets unless a separate Decision explicitly opens that scope.

Changes to unrelated scenes, resources, assets, addons, gameplay services, or historical POC models are out of scope and must fail the focused contract unless separately approved.

## Start-scene migration

Before Task 2:

```text
run/main_scene="res://scenes/test/enhancement_test.tscn"
```

After Task 2 GREEN:

```text
run/main_scene="res://scenes/vertical_slice/main_menu.tscn"
```

The historical enhancement test scene may remain as a test fixture, but it is no longer the application entry point.

## Acceptance criteria

Task 2 B is complete only when all of the following are true on one exact implementation HEAD:

1. Godot starts at the vertical-slice MainMenu.
2. Continue is unavailable when no loadable save exists.
3. Continue is available for a valid primary save and preserves the loaded envelope.
4. A valid backup recovery remains Continue-capable, surfaces recovery status, and preserves the recovered envelope.
5. Unrecoverable/unsupported save cannot silently continue or overwrite itself.
6. New Game requires overwrite confirmation whenever existing campaign state is not `SAVE_NOT_FOUND`.
7. Settings opens and returns as an inline MainMenu overlay without creating campaign state.
8. Entering a campaign loads `BlacksmithApp` at `WORKSHOP`.
9. Undeclared state transitions fail closed with state unchanged.
10. Declared-but-unimplemented destinations fail closed with state unchanged and no placeholder scene.
11. Router code contains no gameplay outcome calculation or RNG authority.
12. Primary interactive controls satisfy the 48×48 minimum contract.
13. Task 2 adds no external product image/audio/font assets and does not claim image-rights completion.
14. Godot import and both new scene smokes PASS.
15. GUT 9.7.1 formal tests and existing Task 1 tests remain GREEN.
16. Automatic PR checks and Full validation PASS on the exact merge candidate HEAD.
17. Product-scope diff is limited to the approved Task 2 paths.
18. Android device and human playtest remain explicitly `NOT_RUN` rather than being inferred from CI.

## Current authority boundary after refresh

- Current Blacksmith main: `a00e864ce5de7bdf872e8093d489c8a78c058afb`.
- Current Base main observed at refresh: `fa69a77a14f923a756064f6ae151d34cadb374f7`.
- The project's pinned Base operating source remains `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`; this Task 2 design does not adopt current Base main.
- Hera remains vendored, disabled, and non-authoritative; this task does not activate it.
- HiGodot remains `PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY`; this task does not claim production authoring authority.
- GUT 9.7.1 remains the formal GDScript test authority.
- Product image generation, rights review, Android-device validation, and human playtest remain blocked/not run and are not inferred from Task 2 CI.

General product implementation remains blocked outside the approved scoped vertical-slice implementation.
