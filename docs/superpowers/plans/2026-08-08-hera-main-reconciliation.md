# Hera Main Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile the untracked Hera Agent Godot vendor tree already present on `main` without granting it production authoring authority, restore the already-formal GUT 9.7.1 authority state in active canon, and move Task 2 from an ambiguous Hera conflict to an explicit merge/review gate.

**Architecture:** Treat `addons/hera_agent_godot/**` as an acknowledged but disabled, non-authoritative vendor baseline. Record one new same-ID decision (`BS-HERA-20260808-01`) in repository canon and Google Sheet, while preserving HiGodot's pending production activation and GUT's active GDScript test authority. Product paths, `project.godot`, Hera vendor bytes, and Task 2 implementation remain unchanged.

**Tech Stack:** Markdown/JSON canon, Python `pytest` contract tests, GitHub Actions, Google Sheets operational mirror.

## Global Constraints

- Current Blacksmith base for this reconciliation: `ddb914f7e70e0deb62f5840fb990eb471eb7f441`.
- Hera vendor introduction commit: `a5126d8a2091ce2350e50713eac614a045cc6ef2` from base `bd7e97ec49b2fac67f619c9bbe5e2c6e53c48d6f`.
- Hera manifest: `addons/hera_agent_godot/plugin.cfg`, version `1.0.0`.
- `project.godot` must not enable `res://addons/hera_agent_godot/plugin.cfg` in this change.
- HiGodot remains `PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY` with production activation requiring separate approval.
- GUT 9.7.1 remains `FORMALLY_ADOPTED_ACTIVE` / `SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY`.
- General product implementation remains `BLOCKED`; image, Android-device, and human-play gates remain unresolved/`NOT_RUN` as already recorded.
- PR #131 remains design-only and is not modified by this reconciliation branch.
- No changes under `addons/`, `scenes/`, `scripts/`, `data/`, `assets/`, or `project.godot`.
- Merge requires separate explicit user approval after exact-head validation and Sheet readback.

---

### Task 1: Contract the reconciled authority state

**Files:**
- Create: `tests/test_hera_vendor_reconciliation_contract.py`
- Read: `project.godot`
- Read: `addons/hera_agent_godot/plugin.cfg`
- Read: `docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json`
- Read: `AGENTS.md`
- Read: `CURRENT_CONFIRMED_DECISIONS.md`
- Read: `docs/operations/BLACKSMITH_HERA_VENDOR_RECONCILIATION_2026-08-08.md`

**Interfaces:**
- Consumes: current repository paths and authority markers.
- Produces: a fail-closed Python contract for Decision `BS-HERA-20260808-01`.

- [ ] **Step 1: Write the failing test**

Create tests asserting all of the following:

```python
DECISION_ID = "BS-HERA-20260808-01"
HERA_STATE = "VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE"

# Required canonical surfaces contain the same decision ID.
assert DECISION_ID in CURRENT_CONFIRMED_DECISIONS
assert DECISION_ID in RECONCILIATION_DOC

# Machine-readable policy acknowledges Hera but does not activate it.
assert policy["hera"]["status"] == HERA_STATE
assert policy["hera"]["project_plugin_enabled"] is False
assert policy["hera"]["authoring_authority"] == "NONE"

# Existing authorities remain intact.
assert policy["higodot"]["current_state"] == "PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY"
assert policy["gut"]["status"] == "FORMALLY_ADOPTED_ACTIVE"

# Godot project activation is unchanged.
assert 'res://addons/godot_ai/plugin.cfg' in project
assert 'res://addons/hera_agent_godot/plugin.cfg' not in project

# Hera vendor identity is pinned.
assert 'version="1.0.0"' in hera_manifest
```

Also assert that active `AGENTS.md` no longer claims GUT is `VENDORED_PRESENT_FORMAL_ADOPTION_PENDING`.

- [ ] **Step 2: Run test to verify it fails**

Run in GitHub Actions after opening the Draft PR from the RED commit. Expected: `tests/test_hera_vendor_reconciliation_contract.py` fails because the new Decision, Hera policy block, and reconciliation document do not yet exist.

- [ ] **Step 3: Commit RED**

Commit only the new contract test (plus this already-committed plan). Do not alter canon yet.

### Task 2: Apply the minimum canonical reconciliation

**Files:**
- Modify: `docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json`
- Modify: `AGENTS.md`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Create: `docs/operations/BLACKSMITH_HERA_VENDOR_RECONCILIATION_2026-08-08.md`
- Test: `tests/test_hera_vendor_reconciliation_contract.py`

**Interfaces:**
- Consumes: failing contract from Task 1.
- Produces: repository canon for `BS-HERA-20260808-01`.

- [ ] **Step 1: Add machine-readable Hera state**

Add a `hera` object to `HIGODOT_GUT_AUTHORITY_POLICY.json` with the exact factual baseline:

```json
{
  "decision_id": "BS-HERA-20260808-01",
  "product": "Hera Agent Godot",
  "installed_path": "addons/hera_agent_godot",
  "installed_plugin_version": "1.0.0",
  "introduced_main_commit": "a5126d8a2091ce2350e50713eac614a045cc6ef2",
  "observed_current_main": "ddb914f7e70e0deb62f5840fb990eb471eb7f441",
  "status": "VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE",
  "project_plugin_enabled": false,
  "authoring_authority": "NONE",
  "production_activation": "REQUIRES_SEPARATE_USER_APPROVED_ADOPTION",
  "mutation_permission": "NONE_UNTIL_SEPARATE_ADOPTION"
}
```

Append the Decision ID to the policy `decision_ids`. Do not change the existing HiGodot or GUT authority values.

- [ ] **Step 2: Correct active human-readable canon**

In `AGENTS.md`, replace the stale GUT-pending sentence with the formal postmerge state: GUT 9.7.1 is active test authority; HiGodot production authoring remains pending. Add Hera as vendored, disabled, and non-authoritative under `BS-HERA-20260808-01`.

In `CURRENT_CONFIRMED_DECISIONS.md`, add one concise active decision entry for `BS-HERA-20260808-01` and reference the already-adopted `BS-TEST-20260806-01` GUT state without changing product design decisions.

- [ ] **Step 3: Create reconciliation evidence document**

Create `docs/operations/BLACKSMITH_HERA_VENDOR_RECONCILIATION_2026-08-08.md` recording:

```text
Decision: BS-HERA-20260808-01
Observed main: ddb914f7e70e0deb62f5840fb990eb471eb7f441
Hera vendor introduction: a5126d8a2091ce2350e50713eac614a045cc6ef2
Hera activation: DISABLED
Hera authority: NONE
GUT authority: FORMALLY_ADOPTED_ACTIVE
HiGodot production activation: PENDING_SEPARATE_APPROVAL
Task 2: implementation remains blocked until this reconciliation is merged, PR #131 is rebased/re-reviewed, and exact-head gates pass
General product: BLOCKED
Android/human play: NOT_RUN
```

- [ ] **Step 4: Run the focused contract**

Run: `python -m pytest tests/test_hera_vendor_reconciliation_contract.py -q`
Expected: PASS.

- [ ] **Step 5: Run existing authority contracts**

Run:

```bash
python -m pytest tests/test_higodot_gut_authority_gate.py tests/test_gut_formal_adoption_contract.py -q
```

Expected: PASS, proving the reconciliation did not regress GUT or HiGodot boundaries.

- [ ] **Step 6: Commit GREEN**

Commit only the four canon/evidence surfaces above. No product or vendor changes.

### Task 3: Mirror the approved Decision into Google Sheet

**Files:**
- External source: Google Sheet `블랙스미스(Blacksmith)`.

**Interfaces:**
- Consumes: Draft PR number/head SHA from Tasks 1–2.
- Produces: same-ID operational mirror with readback.

- [ ] **Step 1: Re-read exact Sheet targets and validation metadata**

Read the current rows/cells in:

```text
00_프로젝트_허브
01_작업순서
02_현재_확정결정
04_누락_충돌_감사
99_변경이력
```

- [ ] **Step 2: Write same-ID draft reconciliation state**

Use `BS-HERA-20260808-01` in `02_현재_확정결정` and the corresponding audit/change-history rows. Update stale current-main references from `a5126d8...` to `ddb914f...`.

Until the reconciliation PR is merged, use a pending state equivalent to:

```text
HERA_RECONCILIATION_DRAFT_PENDING_MERGE
```

Do not mark Task 2 implementation READY and do not remove global product/visual/Android blockers.

- [ ] **Step 3: Read back all edited ranges**

Verify the exact Decision ID, current main SHA, Draft PR number/head, and pending merge status are present and column alignment/data validation are preserved.

### Task 4: Exact-head review and handoff

**Files:**
- No new production files.

**Interfaces:**
- Consumes: Draft PR exact head plus Sheet readback.
- Produces: merge-ready evidence, not a merge.

- [ ] **Step 1: Review changed file set**

Confirm changes are limited to plan/test/canon/evidence files and exclude protected product/vendor paths.

- [ ] **Step 2: Inspect PR review threads and CI**

Require no unresolved actionable review threads and successful relevant checks at the exact PR head.

- [ ] **Step 3: Report remaining gates**

Report `GENERAL_PRODUCT_BLOCKED`, visual/rights gates, Android device validation, human play, and local Windows/Godot execution as unresolved where not actually run.

- [ ] **Step 4: Stop before merge**

Present the validated Draft PR and Sheet same-ID readback. Merge only after a separate explicit user approval.