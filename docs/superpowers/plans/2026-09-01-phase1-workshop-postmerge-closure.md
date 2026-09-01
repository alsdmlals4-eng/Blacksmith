# Phase 1 Workshop Post-Merge Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire the consumed Phase 1 Workshop protected-change approval and rebase the project operating baseline to the already-merged PR #352 commit without changing product behavior.

**Architecture:** The merged product commit `48c73c37f5d8b7f3a436a51aeb96d78febd0fe02` becomes the adapter's protected baseline. A small Python contract proves the approval manifest is absent and the canonical adapter plus its generated compatibility views agree. The Base-owned artifact builder regenerates only derivative views; neither it nor this closure changes a Godot product path.

**Tech Stack:** GitHub pull requests, Base v9.4.4 project-operating-contract artifact builder, Python `unittest`, existing Blacksmith operating contracts.

**Spec:** `AGENTS.md`; `docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md`; merged [PR #352](https://github.com/alsdmlals4-eng/Blacksmith/pull/352).

## Global Constraints

- `BENCHMARK_NOT_APPLICABLE`: this is an L0/L1 operational cleanup with no game, UI, economy, content, asset, or platform decision; reuse the exact prior post-merge closure pattern from commit `91bd0f3b`.
- Do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.
- Do not reopen or alter PR #196.
- `PROJECT_PROTECTED_CHANGE_APPROVAL.json` is one-shot: remove it only after PR #352 exact-head CI and GitHub merge readback are confirmed.
- Preserve the established evidence ceiling: runtime capture is not Android, accessibility, performance, human-play, or release acceptance.
- Update generated compatibility views only through `Base/tools/project_operating_contract.py::write_or_check_artifacts`.

---

### Task 1: Define the post-merge closure contract (RED)

**Files:**

- Modify: `tests/test_equipment_v2_postmerge_approval_retirement.py`
- Modify: `tests/test_project_adapter_long_lived_pr_baseline.py`
- Modify: `tests/check_phase1_workshop_blueprint_contract.py`
- Create: `docs/superpowers/plans/2026-09-01-phase1-workshop-postmerge-closure.md`

**Interfaces:**

- Consumes: PR #352 merge commit `48c73c37f5d8b7f3a436a51aeb96d78febd0fe02`, canonical adapter baseline, receipt's protected-change gate.
- Produces: failing contracts proving a stale baseline, a present manifest, or a pending/non-factual receipt cannot pass.

- [x] **Step 1: Write the failing tests**

Set the expected baseline literal in both Python test files to the PR #352 merge SHA. Change the one-shot approval test to require `APPROVAL.exists()` to be false. Extend the Phase 1 receipt check to require the exact merged PR number, merge SHA, and user-delegated external-label disposition.

- [x] **Step 2: Run the focused RED verification**

Run:

```powershell
& 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_equipment_v2_postmerge_approval_retirement tests.test_project_adapter_long_lived_pr_baseline -v
& 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tests/check_phase1_workshop_blueprint_contract.py
```

Expected: failures because the current baseline is `5560d8f0...`, the one-shot manifest is still present, and the receipt still says the external label is pending.

### Task 2: Retire the manifest and regenerate operating derivatives (GREEN)

**Files:**

- Delete: `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json`
- Modify: `skills/PROJECT_BASE_ADAPTER.json`
- Modify (generated): `skills/BASE_V9_ADAPTER.json`
- Modify (generated): `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- Modify (generated): `skills/PROJECT_SKILL_SNAPSHOT.json`
- Modify (generated only if content changes): `docs/PROJECT_OPERATING_DASHBOARD.html`
- Modify: `docs/operations/receipts/2026-09-01-phase1-workshop-blueprint.json`
- Modify: tests from Task 1

**Interfaces:**

- Consumes: the accepted merge SHA and user instruction to proceed directly.
- Produces: a canonical adapter whose protected baseline is the merged product commit, a removed one-shot manifest, generated views whose raw-byte hash matches the adapter, and a receipt that accurately records PR #352's label/CI/merge readback.

- [x] **Step 1: Apply the minimal canonical updates**

Update only `skills/PROJECT_BASE_ADAPTER.json#/protected_baseline/commit` to `48c73c37f5d8b7f3a436a51aeb96d78febd0fe02`. Delete the consumed approval manifest. Update the receipt with the GitHub label disposition, exact synchronized head `c258c198a7f7008fbe9ed15090b39c815688aa65`, merge SHA, and all-green exact-head CI readback; keep all human/device/release gates unchanged.

- [x] **Step 2: Regenerate derivative artifacts**

Run the Base-owned builder with the existing canonical adapter:

```powershell
$env:PYTHONPATH = 'C:\Users\user\Documents\GitHub\Base\tools'
& 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "from pathlib import Path; import project_operating_contract as c; from base_release_index import install_release_lock_paths; install_release_lock_paths(c); c.write_or_check_artifacts(Path('.').resolve(), Path('C:/Users/user/Documents/GitHub/Base').resolve(), check=False)"
```

Expected: only generated dashboard/snapshot/compatibility views change their adapter hash; no protected product path changes.

- [x] **Step 3: Run focused GREEN verification**

Re-run Task 1's tests, then run:

```powershell
& 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\user\Documents\GitHub\Base\tools\check_project_operating_contract.py' --project-root . --base-repository 'C:\Users\user\Documents\GitHub\Base' --check
```

Expected: all pass and the ordinary operating validator no longer detects a protected-path delta.

### Task 3: Exact-head delivery and cleanup

**Files:**

- Verify only: no new product source or asset files.

**Interfaces:**

- Consumes: the GREEN closure artifacts.
- Produces: a documentation/operating-only PR whose exact head passes project checks, merges through GitHub, and is read back from `origin/main`.

- [x] **Step 1: Run exact-head validation**

Run Python discovery, the project operating-contract validator, whitespace audit, and changed-path audit. Do not reclassify historical Godot warnings as new feature failures.

- [ ] **Step 2: Commit, push, and create a PR**

Use a concise operational commit and PR. The diff must not contain a protected product path, PR #196, a Base mutation, or a generated consumerless image.

- [ ] **Step 3: Read exact-head remote CI and merge**

Only after the PR's exact head is green, use the normal GitHub merge path, fetch `origin/main`, and verify its merge SHA and receipt fields. No direct `main` push or force push.

- [ ] **Step 4: Remove local temporary evidence copies**

After remote merge readback, remove only the known untracked GUT and runtime-capture folders from the completed Phase 1 worktree. Preserve repository receipts, hashes, and Git history; never remove user save data or product assets.

## Plan self-review

- **Scope coverage:** covers manifest retirement, baseline promotion, generated derivative synchronization, factual receipt update, exact-head CI, main readback, and temporary-file cleanup.
- **Adversarial checks:** a stale baseline fails two independent tests; a lingering approval file fails the one-shot contract; generated-view hash drift fails the operating validator; receipt evidence cannot still claim a pending label after a merged PR.
- **No product expansion:** no gameplay, UI behavior, scene, image, schema, economy, or runtime acceptance state is added.
