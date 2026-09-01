# Godot Warning Hygiene Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the currently reproducible invalid Script UID and source-level GDScript warning causes without changing Blacksmith gameplay, save data, visual direction, or runtime asset scope.

**Architecture:** A small Python contract owns the stable file-to-UID and warning-source expectations, while existing GUT suites retain behavior coverage. The sole scene serialization change is performed through the approved Godot editor authoring surface; ordinary GDScript and test-source edits remain minimal identifier or numeric-expression corrections.

**Tech Stack:** Godot 4.7.1, GDScript, GUT 9.7.1, Python `unittest`, Godot AI editor authoring surface.

**Spec:** `AGENTS.md`; `docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md`; `docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json`; `.github/validation/higodot-task2-authoring-recipe.json`; `docs/operations/receipts/2026-09-01-phase1-workshop-blueprint.json`.

## Global Constraints

- Scope is current-canon implementation correction only; no feature, balance, save-schema, UI-flow, art-direction, asset, or Android-device claim changes.
- Change `scenes/vertical_slice/vertical_slice_app.tscn` only through the current Godot editor authoring surface; do not text-edit its serialization.
- GUT is the sole GDScript test authority. It must not be used to mutate tracked authoring surfaces.
- This protected-path correction requires a one-shot `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json` for exactly the six runtime paths and the GitHub `approved-protected-change` label before exact-head CI.
- Preserve PR #196 as `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`.
- The `ILLUSTRATED_WORKSHOP_BOOK` assets are already consumed; no new raster image is required by this maintenance work.
- Human play, Android, accessibility, performance, asset-rights release approval, and release evidence remain `NOT_RUN`.

---

### Task 1: Lock the reproducible warning sources (RED)

**Files:**

- Create: `tests/test_godot_warning_hygiene.py`
- Create: `docs/superpowers/plans/2026-09-01-godot-warning-hygiene.md`

**Interfaces:**

- Consumes: `vertical_slice_app.tscn` script ExtResource, `vs_app.gd.uid`, five current production scripts, and the precision catalog GUT file.
- Produces: a failing machine contract that detects the stale app-shell Script UID and every currently recorded warning-source expression.

- [x] **Step 1: Write the failing test**

```python
def test_vertical_slice_app_script_uid_matches_the_script_sidecar() -> None:
    scene_uid = _script_uid_from_scene(APP_SCENE, "res://scripts/vertical_slice/ui/vs_app.gd")
    assert scene_uid == APP_SCRIPT_UID.read_text(encoding="utf-8").strip()


def test_known_gdscript_warning_sources_are_absent() -> None:
    for path, forbidden in WARNING_SOURCE_FRAGMENTS.items():
        text = path.read_text(encoding="utf-8")
        for fragment in forbidden:
            assert fragment not in text, f"{path.relative_to(ROOT)} still contains {fragment!r}"
```

- [x] **Step 2: Run the focused test to verify RED**

Run:

```powershell
& 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_godot_warning_hygiene -v
```

Expected: failure for `uid://b327lccqh1dps` versus `uid://bo1yb0vtangvj`, followed by failures for the recorded shadowing and integer-division sources.

### Task 2: Repair the persisted scene reference (GREEN)

**Files:**

- Modify through Godot editor only: `scenes/vertical_slice/vertical_slice_app.tscn`

**Interfaces:**

- Consumes: the scene root `/BlacksmithApp`, its script path `res://scripts/vertical_slice/ui/vs_app.gd`, and the sidecar UID.
- Produces: the same app-root script binding, serialized with the current script UID rather than a text-path fallback.

- [x] **Step 1: Open the exact task worktree in the Godot editor**

Start an editor only for `C:/Users/user/Documents/GitHub/Ninza/Blacksmith-worktrees/codex-godot-warning-audit-20260901`, enumerate sessions, and select it by exact project path. Do not touch the already-running GRIMOIRE editor.

- [x] **Step 2: Rebind the root script through the editor**

Open `res://scenes/vertical_slice/vertical_slice_app.tscn`, attach `res://scripts/vertical_slice/ui/vs_app.gd` to `/BlacksmithApp`, and save the scene through the editor. Confirm the binding path is unchanged.

- [x] **Step 3: Re-run the focused test**

Run the Task 1 command. Expected: the UID assertion becomes green while warning-source assertions remain red.

### Task 3: Remove source-level warning causes without behavior change (GREEN)

**Files:**

- Modify: `scripts/vertical_slice/ui/vs_customer_result_screen.gd:145`
- Modify: `scripts/vertical_slice/resolvers/vs_repair_resolver.gd:22-26`
- Modify: `scripts/vertical_slice/ui/vs_workshop_screen.gd:1169-1173,1324-1325`
- Modify: `scripts/vertical_slice/ui/vs_app.gd:472-480`
- Modify: `scripts/vertical_slice/ui/vs_main_menu.gd:253-262`
- Modify: `tests/gut/unit/vertical_slice/test_vs_precision_tag_catalog.gd:96-98,184-186`
- Modify: `tests/test_godot_warning_hygiene.py`

**Interfaces:**

- Consumes: existing GUT behavior tests and the Task 1 static warning contract.
- Produces: semantic-equivalent local names and explicit float-then-truncate atlas-cell division, with no current warning source left in the specified files.

- [x] **Step 1: Apply only local, semantics-preserving replacements**

Use `should_show`, `should_show_handoff`, `r_band_reference`, and `duplicate_result` names that cannot shadow Godot base members. Compute each atlas cell as `int(float(texture_dimension) / 2.0)` so the prior positive-dimension truncation result is explicit.

- [x] **Step 2: Run the focused test to verify GREEN**

Run:

```powershell
& 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_godot_warning_hygiene -v
```

Expected: pass.

- [x] **Step 3: Run the directly affected GUT suites**

Run:

```powershell
& 'C:\Users\user\Downloads\Godot_v4.7.1-stable_win64.exe\Godot_v4.7.1-stable_win64_console.exe' --headless -d -s --path (Get-Location) addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -ginclude_subdirs -gexit
```

Expected: affected vertical-slice tests pass and no invalid Script UID, shadowing, or atlas integer-division warning originates from the corrected files.

### Task 4: Adversarial verification, delivery, and cleanup

**Files:**

- Verify: changed source, scene, test, and plan files only.
- Do not modify: `data/`, `assets/`, `addons/`, `project.godot`, current product decisions, or Base.

**Interfaces:**

- Consumes: Tasks 1–3 green results and the exact branch diff.
- Produces: a narrow corrective PR with machine evidence and a truthful boundary for GUT's remaining process-exit orphan/RID reports.

- [x] **Step 1: Reproduce import and full GUT after the corrections**

Run the CI-equivalent editor import and full GUT command. Record source warning absence separately from any remaining GUT orphan/RID exit report; do not call remaining process-exit reports fixed without a dedicated root-cause test.

- [x] **Step 2: Validate non-Godot contracts and changed-path boundaries**

Create a one-shot exact-path approval manifest and run Python discovery, the approved project operating-contract validator with the manifest plus external approval, the warning-hygiene test, and an exact `git diff --check`. Confirm that no new image, Base change, PR #196 edit, or uncontrolled authoring file exists.

- [ ] **Step 3: Commit, push, and create a pull request**

Use a narrow maintenance commit. After exact-head checks are green, use the normal protected GitHub path, then fetch `origin/main` and read back the merged commit and warning contract.

- [ ] **Step 4: Remove only task-owned temporary artifacts**

After main readback, remove this worktree's `artifacts/godot-warning-audit-20260901`, then remove the exact audit worktree and its branch. Preserve all unrelated worktrees, source assets, user data, and Git history.

## Plan self-review

- **Scope coverage:** the scene UID mismatch, seven recorded source warning locations, regression contract, behavior suites, CI-equivalent import, exact remote delivery, and task-only cleanup are individually covered.
- **Adversarial checks:** the static contract fails independently for stale UID and source patterns; editor import proves the loader no longer falls back to text path; existing GUT covers behavior; remaining process-exit lifecycle reports are intentionally not overstated.
- **No image expansion:** no runtime consumer gap exists in this repair, so the user-approved automatic image route is correctly unused.
