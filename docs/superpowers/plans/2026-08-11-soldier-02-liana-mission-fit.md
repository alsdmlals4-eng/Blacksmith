# SOLDIER_02 Liana Mission-Fit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Canonize `BS-CONTENT-20260811-07 / SOLDIER_02 / LIANA_BERG / FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY` as R3–R7 planning-only 7/10 while preserving Marek/Cassia ownership boundaries, same-UID lifecycle, and all product/Task3 blocks.

**Architecture:** Follow the established Decision01–06 pattern: add one focused Python contract test first, wire it into the existing validation workflow, verify semantic RED, then add the Liana responsibility canon and promote current registry/router state from 6/10 to 7/10. Repair only current-state consumers that are expected to follow the moving R3 pointer, run adversarial/post-change checks, and sync the final merged main plus current Base observation to Google Sheet using the same Decision ID.

**Tech Stack:** Markdown planning canon, JSON registry, Python `unittest`/`pytest`, GitHub Actions, Godot 4.7.1 validation, Google Sheets.

## Global Constraints

- Decision ID: `BS-CONTENT-20260811-07`.
- Content ID: `SOLDIER_02`.
- Customer ID: `LIANA_BERG`.
- Activity family: `FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY`.
- Current Base observed main at work start: `23d5b292f619022cdd8ab7a33fb1debc2d294861`.
- Current Blacksmith main at work start: `27365bc774508bea6a1a19221fb2a3dc2d093be5`.
- Open PR inventory at work start: PR #81 only, `REFERENCE ONLY / DO NOT MERGE`.
- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- `SAME_ITEM_UID_PRESERVED`.
- `NO_DIRECT_TACTICAL_COMBAT`.
- `NO_UNIT_MOVEMENT_OR_FORMATION_CONTROL`.
- `NO_REALTIME_LOGISTICS_CONTROL`.
- `NO_SOLDIER_CASUALTY_MICROMANAGEMENT`.
- `NO_COMMAND_POWER_SCORE / NO_HERO_SCORE / NO_LEADERSHIP_SCORE / NO_MISSION_FIT_TOTAL_SCORE`.
- `NO_HIGHEST_DEFENSE_ALWAYS_BEST / NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`.
- `NO_ITEM_AS_SOLE_CAUSE_OF_MISSION_RESULT`.
- `NO_BASELINE_PERMADEATH_FOR_LIANA`.
- `NO_DEATH_FARMING_OR_RECRUIT_REPLACEMENT_LOOP`.
- `NO_MISSION_COUNT_ARTISTRY_GROWTH`.
- `NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_SURVIVAL`.
- `NO_MISSION_FARMING_MULTIPLIER`.
- Exact mission types, thresholds, injury states, timing, economy, rewards, and result distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.
- Sheet `BS-CT-06` taxonomy ambiguity is recorded but not silently redefined in Decision07.

---

### Task 1: Add the failing Decision07 contract

**Files:**
- Create: `tests/test_r3_soldier_02_liana_content.py`
- Modify: `.github/workflows/python-validation.yml`

**Interfaces:**
- Consumes: current `CURRENT_R3_R7_CANON_REGISTRY.json`, current routers, existing Liana Sheet identity concept.
- Produces: a deterministic contract that fails until Decision07 canon, registry, and current routers exist.

- [ ] **Step 1: Write the failing test**

The test must require:

```python
registry["next_approval_counter"] == "7/10"
"BS-CONTENT-20260811-07" in decisions
contract["content_id"] == "SOLDIER_02"
contract["customer_id"] == "LIANA_BERG"
contract["activity_family"] == "FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY"
contract["result_axes"] == [
    "MISSION_DUTY_STATE",
    "COMMANDER_RETURN_STATE",
    "ITEM_UID_FIELD_LEGACY_STATE",
]
```

It must also assert all protected false/true boundaries and that routers move to Decision07/7-of-10 without opening product/Task3 implementation.

- [ ] **Step 2: Wire the test into the existing validation workflow**

Add immediately after the Soldier01 test:

```yaml
python -m unittest tests.test_r3_soldier_02_liana_content -v
```

- [ ] **Step 3: Push only test/workflow changes and open/update Draft PR**

- [ ] **Step 4: Verify semantic RED**

Expected failure cause: registry remains `6/10`, Decision07/canon does not exist, and routers still point at Decision06. Do not accept YAML syntax errors, import errors, or unrelated CI infrastructure failures as RED evidence.

---

### Task 2: Add minimal Liana planning canon and registry contract

**Files:**
- Create: `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`

**Interfaces:**
- Consumes: approved Decision07 design and R2 Soldier/customer/item authorities.
- Produces: the authoritative planning contract and current 7/10 Decision pointer.

- [ ] **Step 1: Write the minimal canon**

Canon must define the flow:

```text
Liana visit
→ disclosed duty/risk/equipment role
→ candidate UID comparison
→ one same UID handoff
→ off-screen field resolution
→ MISSION_DUTY_STATE
 + COMMANDER_RETURN_STATE
 + ITEM_UID_FIELD_LEGACY_STATE
→ repair/restore/enhance/recraft/preserve/reassign reason
```

It must explicitly separate Marek batch-standardization ownership and Cassia arena-contribution ownership.

- [ ] **Step 2: Add Decision07 to the current registry**

Use a contract containing the approved identifiers, result axes, same-UID rule, no-direct-control rules, no-score rules, no-permadeath baseline, no-progression-farming rules, product block, Task3 block, and `human_playtest: NOT_RUN`.

- [ ] **Step 3: Move current confirmed decisions to 7/10**

Preserve Decisions01–06 as history and set the current Decision to `BS-CONTENT-20260811-07`.

- [ ] **Step 4: Run the focused Decision07 contract**

Expected: the canon/registry portions pass; router assertions may still fail until Task 3.

---

### Task 3: Promote the four current routers and current-state consumers

**Files:**
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify only if required by failing current-state regression: `tests/check_project_core_alignment_current.py`, `tests/test_r3_*`, `tests/test_auto_enhancement_cap_unlock.py`, `tests/test_hera_postmerge_closure_contract.py`, `tests/test_project_operating_system_audit_runner.py`, `tools/run_project_operating_system_audit.py`, `docs/PROJECT_OPERATING_HEALTH.json`.

**Interfaces:**
- Consumes: Decision07 current registry.
- Produces: one coherent current 7/10 pointer across human-readable routers and audit consumers.

- [ ] **Step 1: Replace only moving current-state assertions**

Move `6/10 / Decision06 / Noble01 resume locator` to `7/10 / Decision07 / Soldier02 Liana resume locator`. Do not rewrite Decision01–06 historical assertions.

- [ ] **Step 2: Refresh observed Base main only where the field is explicitly current observation**

Use `23d5b292f619022cdd8ab7a33fb1debc2d294861`. Do not change `PROJECT_BASE_ADAPTER_PIN` merely because Base main advanced.

- [ ] **Step 3: Re-run focused current-state tests**

Fix only failures caused by the intentional current pointer move.

---

### Task 4: Adversarial/post-change verification and PR closure

**Files:**
- No new product files.
- Add receipts only when they record real RED/GREEN/repair evidence and follow existing repository practice.

**Interfaces:**
- Consumes: exact PR head after Tasks 1–3.
- Produces: exact-head validation evidence and post-change classification.

- [ ] **Step 1: Attack the diff**

Classify findings using `OMISSION / CONFLICT / COMPLEMENT_GAP / DUPLICATE_WORK / NO_MATERIAL_FOLLOWUP` plus severity. Mandatory attacks: Marek duplication, Cassia reskin, direct-combat drift, hidden total score, highest-stat dominance, item-only causality, baseline permadeath, UID replacement, progression farming, untouched current consumers.

- [ ] **Step 2: Check open/recent same-goal PRs**

PR #81 remains reference-only; verify no new Liana/Decision07 PR appeared.

- [ ] **Step 3: Run exact-head validation**

Require the repository's current PR validation set including Python contracts and Godot 4.7.1 headless validation, plus Base/BCA/GUT/HiGodot/adapter workflows used by the current project gate. Do not claim human/Android/accessibility evidence.

- [ ] **Step 4: Mark Ready and merge only if the exact approved scope is green**

Use squash merge with expected head SHA. Do not re-ask merge approval for the same approved scope.

- [ ] **Step 5: Post-merge main readback**

Verify new main contains Decision07/7-of-10, product/Task3 blocks, and only intended current-state changes.

---

### Task 5: Same-ID Google Sheet sync and readback

**Files:**
- Google Sheet only; no product files.

**Interfaces:**
- Consumes: final merged main SHA and fresh Base main observation.
- Produces: same Decision ID across GitHub and Sheet with postmerge readback PASS.

- [ ] **Step 1: Re-read target ranges immediately before write**

Target current ranges: `00_프로젝트_허브`, `01_작업순서`, next row in `02_현재_확정결정`, `13_주요인물` Liana row, next content row in `50_메인콘텐츠`, next row in `99_변경이력`, and `10_제품방향` only if a current derived field needs final-main refresh.

- [ ] **Step 2: Sync Decision07**

Set current to 7/10, add Liana responsibility canon/status, add `SOLDIER_02`, and record exact PR heads/merged main.

- [ ] **Step 3: Repair only objective derived drift**

Refresh Sheet Base current main from `7ce96181...` to `23d5b292...` if Base has not advanced again. Preserve adapter pin. Do not silently redefine `BS-CT-06` taxonomy ambiguity.

- [ ] **Step 4: Exact readback**

Verify Decision ID, final main SHA, 7/10, Base observation, `PRODUCT_IMPLEMENTATION_BLOCKED`, `TASK3_NOT_APPROVED`, and change-history status.

- [ ] **Step 5: Close with `POSTMERGE_READBACK_PASS`**

Report human playtest, Android device, and accessibility as `NOT_RUN` unless actual evidence exists.
