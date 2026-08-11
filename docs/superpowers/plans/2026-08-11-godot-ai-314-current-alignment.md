# Godot AI 3.1.4 Current Alignment Implementation Plan

**Goal:** make Blacksmith current toolchain authority match the already-vendored exact upstream Godot AI `3.1.4` payload, restore GREEN current validation, and preserve completed Task2 `3.1.3` provenance as history.

**Architecture:** keep `addons/godot_ai` byte-identical to official v3.1.4. Repair current policy/tests/docs rather than recreating a Blacksmith vendor fork. Treat the old Task2-only `set_main_scene` overlay as historical completed-task evidence. No product serialization changes.

## Constraints

- Base observed: `7a49390bd840f5f5dc80fe661b44ad45e9ebeb7f`.
- Blacksmith base: `eb5a43d3293290372a0ca2fe6ec107feef4cc6e5`.
- Only open PR #81 is reference-only / do not merge.
- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- R3–R7 remains `4/10`.
- Do not edit `project.godot`, scenes/resources, GUT vendor, or Hera vendor.
- Preserve historical Task2 3.1.3 bridge/prove files without blanket version replacement.

### Task 1 — RED current-version contract

- [ ] Add `tests/test_godot_ai_314_current_alignment.py` first.
- [ ] Assert current plugin version `3.1.4`, official identity metadata, new Decision presence, current policy version `3.1.4`, preserved Task2 historical `3.1.3`, generic main-scene guard, current already-finalized MainMenu path, and no current raw `set_main_scene` registration.
- [ ] Wire the focused test into Python validation.
- [ ] Run PR CI and verify RED for missing Decision/current policy plus existing stale runtime test expectation.

### Task 2 — GREEN authority alignment

- [ ] Add `docs/decisions/BS-TOOLCHAIN-20260811-02_GODOT_AI_314_CURRENT_VENDOR_ALIGNMENT.md`.
- [ ] Update `docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json` current Godot AI version/official identity while retaining historical Task2 evidence.
- [ ] Update current editor-plugin sync/runtime contracts to current 3.1.4 semantics and keep GUT/Hera authority unchanged.
- [ ] Update active current-router/gate text that still states 3.1.3 as current, without rewriting historical evidence.
- [ ] If `CURRENT_CONFIRMED_DECISIONS.md` changes, repair only the derived operating-health SHA evidence.

### Task 3 — regression and adversarial verification

- [ ] Run focused current alignment tests.
- [ ] Run full PR validation and Godot 4.7.1 suite.
- [ ] Confirm the exact upstream addon tree remains `69010571e11123dfc4e09483f80cb9e6ca93511a`.
- [ ] Confirm generic `application/run/main_scene` write remains denied in upstream current handler.
- [ ] Confirm no product serialized surface is changed by this repair PR.
- [ ] Confirm PR #81 untouched and review/thread state clear.
- [ ] Merge exact-head after all applicable workflows are GREEN under inherited same-approved-scope authority.

### Task 4 — same-ID Sheet synchronization

- [ ] Postmerge read back main and current policy/Decision.
- [ ] Add `BS-TOOLCHAIN-20260811-02` to live Sheet without overwriting historical 3.1.3 rows.
- [ ] Update current hub status with 3.1.4 toolchain alignment while retaining R3 4/10 and product/Task3 blocks.
- [ ] Add audit/change-history rows with RED→GREEN and exact-head evidence.
- [ ] Independently read back all written cells and close as `POSTMERGE_READBACK_PASS`.
