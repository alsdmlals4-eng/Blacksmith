# BS-HIGODOT-EXEC-20260808-01 — Task 2 HiGodot CI Authoring Bridge

Status: `USER_APPROVED / PROVE_SUCCESS / PUBLISH_SUCCESS / TASK2_MAIN_MERGED / POSTMERGE_CI_CLOSURE_COMPLETE`

Approved at: `2026-08-08 KST`
Written-spec review approved at: `2026-08-08 21:11 KST`
Closure refreshed at: `2026-08-10 KST`

## Decision

Adopt a project-specific CI execution bridge for the remaining Task 2 HiGodot-owned serialized surfaces.

The bridge uses a separated `PROVE → PUBLISH` model:

- **PROVE** runs with read-only repository authority, starts a real Godot 4.7.1 Editor under Xvfb, uses the vendored HiGodot/Godot AI production authoring path, validates the resulting working tree, and emits a provenance bundle.
- **PUBLISH** is the only repository-write stage. It does not re-author Godot content; it verifies and publishes only the byte-identical serialized outputs already authored and validated by PROVE.

Approved serialized output scope was exactly:

```text
scenes/vertical_slice/main_menu.tscn
scenes/vertical_slice/vertical_slice_app.tscn
scenes/vertical_slice/screens/vs_workshop_screen.tscn
project.godot  # application/run/main_scene only
```

## Authority boundary

This Decision consumed `BS-HIGODOT-20260808-01` and did not broaden its authority beyond Task 2.

- HiGodot was the sole Godot Scene/Resource/project-settings production authoring authority for the approved Task2 serialized scope.
- GUT 9.7.1 remained the sole GDScript test-framework authority.
- Hera remained non-authoritative with authoring/mutation authority `NONE`.
- General product implementation remained blocked outside the approved vertical-slice scope.
- Base current main was not adopted merely by running this bridge.
- Direct generic text/GitHub API authoring of `.tscn` or `project.godot` was forbidden.

## Provenance constraints applied

- No headless mutation impersonation: mutation occurred through the live Godot Editor + HiGodot path.
- Exact repository/PR/input-head/project/session identity was bound before mutation.
- Exact compatible plugin/server identity was recorded.
- No filesystem/script text-write fallback impersonated Scene/Node/project-setting operations.
- Ambiguous mutation results required readback and fail-closed handling.
- Tracked diff outside the exact four-file allowlist was forbidden.
- PUBLISH verified artifact hashes and branch-head freshness and did not regenerate the proven bytes.

## Task2 publication evidence

```yaml
PROVE_INPUT_HEAD: 02420ebd3bcdd86776c4ab70824738aa4071a168
PROVE_RUN: 31341840236
PROVENANCE_ARTIFACT_ID: 9046072682
PROVENANCE_DIGEST: sha256:0ce5d8cf8333f8910c64c6b25cf54cc4e7d3354fa6249e0e56c65ba55a70dabd
SERIALIZED_PUBLISH_COMMIT: 8afb9a439df46eec3568a75d7f2536b89e1edaba
APPROVED_PR_HEAD: 345cf339e2af754d447099dd8e1b278b80b849d5
PREMERGE_TEST_MERGE: 70ff7bb00ebd70e5bf48b8e55b39da8463a67eca
TASK2_MERGE_MAIN: a61a0bceec4254c4b78350980275cc9a903f9042
```

`PROVE_INPUT_HEAD`, `SERIALIZED_PUBLISH_COMMIT`, approved PR head, premerge test-merge SHA, and actual merge-main SHA are separate evidence identities and must not be conflated.

## Same-scope postmerge CI recovery

Task2 merge exposed two independent operational regressions. Both were repaired without re-authoring the four serialized Task2 product files.

- PR #139 aligned the Live-Editor Pilot with the source-configured `application/run/main_scene`, preserved read-only main-scene/source-authority boundaries, and merged at `7ccee408cf5c936ae9302a986fa0c786e0247078`.
- PR #140 repaired the literal `[기획서]` path-filter parsing defect in the HiGodot/GUT authority workflow and merged at `fa9595b2df95897c915331a1cb5d9b1a583611f0`.

Fresh postmerge evidence on `fa9595b2df95897c915331a1cb5d9b1a583611f0`:

```yaml
FULL_VALIDATION_RUN: 31344872151
FULL_VALIDATION: SUCCESS
LIVE_EDITOR_PILOT_RUN: 31344872263
LIVE_EDITOR_PILOT: SUCCESS
PR140_AUTHORITY_RUN: 31344719243
PR140_AUTHORITY_WORKFLOW: SUCCESS
```

## Written-spec review and implementation plan

The approved written-spec review is:

`docs/operations/BLACKSMITH_HIGODOT_EXEC_SPEC_REVIEW_2026-08-08.md`

The approved implementation plan is:

`docs/superpowers/plans/2026-08-08-blacksmith-higodot-ci-authoring-bridge.md`

Those files preserve the pre-execution design/TDD staging history. Their old staging language is historical evidence and does not override this Decision's current closure section.

## Historical pre-execution state

The following values are retained only as immutable staging evidence from before the bridge implementation ran:

```text
WRITTEN_SPEC_REVIEW = APPROVED
BRIDGE_TDD = RED_NEXT
SCENE_PROJECT_MUTATION = 0
```

At that time, the Base generic Godot production adapter remains `NOT_READY`, and **This Decision is not merge approval** was the applicable pre-merge gate. Those statements are historical and are superseded for current status by `Current closure` below.

## Current closure

```text
DESIGN = USER_APPROVED
WRITTEN_SPEC_REVIEW = APPROVED
IMPLEMENTATION_PLAN = EXECUTED
BRIDGE_TDD = COMPLETE
TASK2_STATIC_APP_SHELL = GREEN_AND_MERGED
SCENE_PROJECT_MUTATION = HIGODOT_PROVEN_PUBLISHED
PR131 = MERGED
TASK2 = TASK2_MAIN_MERGED
POSTMERGE = POSTMERGE_CI_CLOSURE_COMPLETE
CURRENT_TECHNICAL_BASELINE = fa9595b2df95897c915331a1cb5d9b1a583611f0
GENERAL_PRODUCT_IMPLEMENTATION = BLOCKED
NEW_PRODUCT_SCOPE = USER_DECISION_REQUIRED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_DEVICE = NOT_RUN
```

Task2 완료는 새로운 Task3/R3 제품 범위 승인으로 확대되지 않는다.

## Historical merge gate

실행 전 이 Decision은 별도 PR #131 merge approval을 요구했다. 그 과거 gate는 실제 승인·검증·병합으로 충족되었으며, 현재 상태는 위 `Current closure`가 우선한다.
