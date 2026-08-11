# GLADIATOR_01 Cassia Arena Signature Weapon Implementation Plan

**Goal:** Promote `BS-CONTENT-20260811-05 / GLADIATOR_01 / CASSIA_BELLAN / ARENA_SIGNATURE_WEAPON_AND_LEGACY` to R3–R7 planning canon at `5/10` without opening product or Task3 implementation.

**Architecture:** Add one gladiator content canon and propagate Decision05 through the existing R3 registry/current-router documents. Reuse current item UID, item properties, provenance, Artistry, Chronicle, customer result, and world-result explanation authority. Arena resolution stays off-screen and decomposes match outcome from equipment contribution and same-UID legacy.

**Tech Stack:** Markdown planning canon, JSON R3 registry, Python `unittest` contract tests, existing GitHub Actions PR validation.

## Global Constraints

- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- PR #81 remains reference-only and is not merged.
- R3 approval counter changes from `4/10` to `5/10` only for `BS-CONTENT-20260811-05`.
- No direct arena combat, fighter positioning/behavior orders, team/guild management, or betting.
- No `ARENA_SCORE`, `FAME_SCORE`, `GLADIATOR_SCORE`, `SIGNATURE_SCORE`, or other opaque aggregate raw stat.
- Match outcome and item contribution remain separate.
- Highest enhancement is not automatically best.
- Same item UID remains authoritative before, during, and after the event.
- Match/win count does not automatically grow `ARTISTRY` or grant `CHRONICLE_AFFIX`.
- Historical Kyle/iron_sword PoC fixed values remain non-authoritative for Decision05.
- Exact timing, thresholds, economy, rewards, and result distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.

---

### Task 1: Establish semantic RED for Decision05

**Files:**
- Create: `tests/test_r3_gladiator_01_cassia_content.py`
- Modify: `.github/workflows/python-validation.yml`

- Write the focused contract for `5/10`, Decision05, Cassia IDs, player-role boundary, decomposed result axes, same UID, legacy-PoC non-authority, no aggregate score/direct combat/automatic progression, and product/Task3 blocks.
- Wire the test into the existing Python validation entrypoint in the same commit series so the test cannot exist unexecuted.
- Verify RED because Decision05/canon/current routing are absent; record the semantic cause rather than treating workflow/environment failure as RED.

### Task 2: Materialize approved planning canon

**Files:**
- Create: `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify current-health or current-state tests only when they legitimately consume the current Decision/counter.

- Add Cassia canon from the approved design spec.
- Promote registry/current routers to `5/10`, preserving Decisions01–04 as history.
- Keep all product/Task3 gates blocked.
- Run focused test to GREEN.

### Task 3: Regression, adversarial review, merge, and sync

- Run the planning/document contract suite used by recent R3 promotions and the project operating audit.
- Fix only stale current-state consumers; do not weaken historical tests or product gates.
- Attack for direct-combat drift, opaque score drift, win=item-quality collapse, highest-enhancement dominance, progression farming, UID loss, legacy PoC resurrection, or scope opening.
- Run exact-head GitHub Actions validation.
- Inspect PR diff and review/thread/comment state.
- Merge under inherited same-approved-scope authority only after exact-head technical validation.
- Postmerge read back main/current canon and synchronize the same `BS-CONTENT-20260811-05` to the live Google Sheet with independent readback.

## TDD evidence

- Semantic RED head: `9a262945191cf87e2b992b0f402daaa81b95093f`.
- RED cause: the newly CI-wired Cassia contract failed only because the Decision05 canon/current routing was absent; prior R3 contracts and infrastructure reached the new test successfully.
- Materialized GREEN head: `ac8cabe55ce5a190dd532c0efb39be6c3cf4aa16`.
- Focused GREEN at materialization: Cassia `4/4`, Ersa `4/4`, Marek `4/4`, and project-core current alignment all passed.
- Temporary materializer, count-fix helper, and materializer workflow self-deleted before the materialized commit; none are part of the resulting planning diff.
- Exact-head `c1b3336206104ab447e7b3e2ff79de5c3545850f` advanced all R3/Cassia/Hera current-router contracts and the Godot 4.7.1 suite, then exposed one regression introduced by the planning-gate rewrite: the Decision01 first-approved-history sentence had been dropped from `DEVELOPMENT_GATES.md`.
- Gate-history repair run `31461497303` restored that Decision01 history marker and advanced the remaining product-gate current pointer from Decision04 to Decision05; affected initializer and Cassia contracts passed before commit.
- Repaired planning head: `500e7c94a544561ff8d12da795a8d2c9a85c68c6`; its temporary repair script/workflow are absent from the resulting tree.
- Exact-head `98b229a465e6c14d3a9d430e4e052a59b14ab152` then passed the full document/CI contract phase and exposed the operating-audit wrapper's stale current-state model: it still treated Ersa 4/10 as `R3_CURRENT_DECISION` while tests correctly expected Cassia 5/10.
- Operating-audit repair run `31461697006` separated `R3_FOURTH_DECISION=BS-CONTENT-20260811-04` from `R3_CURRENT_DECISION=BS-CONTENT-20260811-05`, added the Cassia canon to active audit authority, advanced registry/router assertions to `5/10`, and passed the operating-audit runner plus Cassia focused contract before commit.
- Repaired audit head: `de3c789932503f824d90c827e43d22cd65778a0b`; its temporary repair script/workflow are absent from the resulting tree.
- This evidence commit is the fresh exact-head CI trigger. Merge remains blocked until every workflow on this exact head is green and PR review/diff readback is clean.
