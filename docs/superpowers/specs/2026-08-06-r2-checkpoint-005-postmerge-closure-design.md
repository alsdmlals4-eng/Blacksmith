# R2 Checkpoint 005 Postmerge Closure Design

## Goal

Close the planning checkpoint created by PR #109 without changing any game design, balance preset, runtime file, or protected product path.

## Authority transition

PR #109 already merged the ten `R2_BATCH_005` Decisions into `main`.

```text
planning PR: #109
source exact head: 77eba15415bc9ede661639b45bb526d5ce4410a5
squash merge: 31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9
status: MERGED_MAIN_CANON
```

The closure PR must replace current-authority premerge labels with immutable merge evidence while preserving historical documents unchanged.

## Files in scope

Current authority only:

- `CURRENT_CONFIRMED_DECISIONS.md`
- `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- `[기획서]/00_프로젝트_허브/ROADMAP.md`
- `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- new closure document and regression test

Historical, superseded, runtime, data, scripts, scenes, images, assets, addons, and `project.godot` remain untouched.

## State model

```text
R2_BATCH_005_ACTIVE_10_OF_10
→ R2_BATCH_005_CLOSED_10_OF_10 / PLANNING_MERGED_PR109
→ R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING
```

The next approval counter resets to `0/10`, but `R2_BATCH_006` is `NOT_STARTED`; this does not select the next game-design topic.

All ten batch Decisions become:

```text
MERGED_PR109 / MAIN_CANON
```

The closure PR itself remains draft and unmerged until explicit user approval.

## Preserved gates

- product implementation: `BLOCKED`
- human playtest: `NOT_RUN`
- exact balance values: `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`
- protected product path changes: `0`
- no new Decision ID

## Validation

A focused unittest must fail on the pre-closure main state and pass only when:

1. registry merge evidence matches PR #109 exactly;
2. all current-authority documents route to Checkpoint 005 closure;
3. current-authority documents contain no premerge labels;
4. the closure document preserves implementation and playtest gates.

## Conflict review

No game-design conflict is introduced. The only semantic choice is operational: `0/10` means the next batch is available but not started. This follows the Checkpoint 004 closure pattern and does not authorize a new design Decision.