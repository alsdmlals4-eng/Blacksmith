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
