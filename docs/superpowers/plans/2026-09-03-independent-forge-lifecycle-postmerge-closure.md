# Independent Forge Lifecycle Post-Merge Closure Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` task by task. This is an operational closure, not a new product feature.

**Goal:** Retire the consumed protected-change approval from merged PR #366 and advance Blacksmith's protected baseline to its actual merge commit `c31e550fc8d5b27d4377aeb542fde3cbfe228c06`, without changing gameplay, UI behavior, save data, Godot scenes, or assets.

**Authority and scope:** `AGENTS.md`; `docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md`; [PR #366](https://github.com/alsdmlals4-eng/Blacksmith/pull/366); `skills/PROJECT_BASE_ADAPTER.json`; `docs/operations/receipts/2026-09-03-independent-forge-lifecycle-design.json`.

## Boundaries

- `BENCHMARK_NOT_APPLICABLE`: This is a Base-adapted L0/L1 operational retirement of a consumed approval. It adds no game content, UX, economy, visual, engine, or platform decision; the established Phase 1 closure pattern is the directly relevant repository precedent.
- Base current `850204b3e5de81a4045111b4a050c46c5a292b59` was fresh-read only for drift. The project-adopted Base v9.4.4 lock remains unchanged.
- Do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`, user saves, existing runtime captures, or PRs #196/#359.
- Delete only `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json` after verifying the #366 exact-head CI and `origin/main` merge readback. The deletion is git-recoverable and has zero active consumers after the baseline advances.
- Regenerate compatibility views only through `Base/tools/project_operating_contract.py::write_or_check_artifacts`; do not hand-edit generated files.
- Keep Android, accessibility, performance, human-play, rights, and release evidence at `NOT_RUN`.

## Task 1 — RED: Make stale closure evidence fail

**Files:**

- Modify: `tests/test_equipment_v2_postmerge_approval_retirement.py`
- Modify: `tests/test_project_adapter_long_lived_pr_baseline.py`

- [x] Require the canonical adapter baseline to equal `c31e550fc8d5b27d4377aeb542fde3cbfe228c06`.
- [x] Require the consumed manifest to be absent.
- [x] Require the independent-loop receipt to record PR #366 exact CI head `1713b64d22e0f830b6e980aa451df73158fcb2e4`, all-green CI, merge readback, retirement, and the rebased adapter baseline.
- [x] Observe focused RED: two stale-baseline failures, one lingering-manifest failure, and one missing-delivery-record error.

## Task 2 — GREEN: Retire approval and synchronize derivatives

**Files:**

- Delete: `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json`
- Modify: `skills/PROJECT_BASE_ADAPTER.json`
- Modify generated if content changes: `skills/BASE_V9_ADAPTER.json`, `skills/PROJECT_BASE_SKILL_ADAPTER.json`, `skills/PROJECT_SKILL_SNAPSHOT.json`, `docs/PROJECT_OPERATING_DASHBOARD.html`
- Modify: `docs/operations/receipts/2026-09-03-independent-forge-lifecycle-design.json`
- Modify: `docs/superpowers/plans/2026-09-03-independent-forge-lifecycle.md`

- [x] Change only `protected_baseline.commit` to the actual #366 merge commit.
- [x] Record the exact CI head, all-green result, protected GitHub merge, main readback, and the consumed approval's retirement in the receipt. The delivery work item uses exact CI head `1713b64d22e0f830b6e980aa451df73158fcb2e4`; `remote_delivery` retains the distinct product merge SHA.
- [x] Remove the one-shot manifest with a recoverable repository deletion.
- [x] Run the Base-owned artifact builder and review its generated-file list.
- [x] Re-run focused closure contracts until GREEN.

## Task 3 — Exact-head operational delivery

- [x] Run Python discovery, receipt closeout validation against the independent PR #366 CI subject head `1713b64d22e0f830b6e980aa451df73158fcb2e4`, normal operating-contract validation, generated-artifact check, whitespace audit, and protected-path audit. Python: 350 passed, 2 skipped; all closure contracts passed.
- [ ] Commit only the closure files, push a separate PR, inspect exact-head GitHub CI, merge normally, and read `origin/main` back.
- [ ] Remove only task-created, untracked closure-temporary files after the remote readback; preserve product evidence, source history, and every unrelated worktree.

## Adversarial review

- A stale baseline could let a later protected diff inherit a consumed approval. Two independent tests prevent that.
- Leaving the manifest after its approved diff is merged would make a future protected change look approved. The closure contract requires file absence.
- Hand-editing generated compatibility views could desynchronize hashes. The Base-owned generator plus ordinary validator must be the only Green route.
- A local merge claim is insufficient. The receipt records GitHub's exact CI head, merge commit, and `origin/main` readback, while unrun product gates remain unpromoted.
