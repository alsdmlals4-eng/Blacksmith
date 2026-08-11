# SOLDIER_02 Liana Berg Mission-Fit Design

## Status

- Decision: `BS-CONTENT-20260811-07`
- R3–R7 slot: `7/10`
- Scope: planning canon only
- Content ID: `SOLDIER_02`
- Customer ID: `LIANA_BERG`
- Activity Family: `FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY`
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`
- User direction: approved the recommended Liana frontline-commander direction after coverage comparison, benchmarking, and adversarial review.

## Goal

Promote existing `LIANA_BERG` into the second detailed Soldier content and prove a different Soldier question from Marek: not whether several items meet one standard, but whether one real item is appropriate for one commander's disclosed duty and risk.

## PRE_WORK_RESEARCH_PACKET

```yaml
PRE_WORK_RESEARCH_PACKET:
  checked_at_kst: 2026-08-11
  base_main_sha: 23d5b292f619022cdd8ab7a33fb1debc2d294861
  project_main_sha: 27365bc774508bea6a1a19221fb2a3dc2d093be5
  open_pr_inventory: "PR #81 only; REFERENCE ONLY / DO NOT MERGE"
  google_sheet_state: "R3_R7_DESIGN_ACTIVE / 6_OF_10; Decision06 synced; product BLOCKED; Task3 NOT_APPROVED; Sheet Base SHA still 7ce96181... and therefore stale"
  work_type: "game content design / Soldier individual duty fit / same-UID field consequence"
  benchmark_sources:
    - "Battle Brothers official features/presskit"
    - "Wartales Steam product page"
    - "The Banner Saga Steam product page"
  adopt:
    - "equipment choice materially changes a character's ability to face a dangerous situation"
    - "preparation matters before off-screen consequence is resolved"
    - "choices can leave persistent consequences on a named character and the continuing story"
  adapt:
    - "character/equipment consequence becomes a blacksmith handoff decision rather than tactical combat control"
    - "persistent consequence is split into mission duty, commander return, and the same item's field lifecycle"
  reject:
    - "direct tactical combat, company/camp management, formation control, or commander RPG progression"
    - "permadeath as a baseline content requirement"
    - "new command power, hero, leadership, or battle total score"
  differentiator: "Marek tests batch consistency across many UIDs; Liana tests responsibility for one disclosed mission and one selected UID, with mission outcome, commander return, and item legacy remaining separable."
  canon_conflict_check: "Marek/Soldier01 retains SMALL_LOT_STANDARD_ORDER and batch-standardization ownership. Cassia/Gladiator01 retains arena performance-contribution ownership. Liana owns single-commander duty fit and protective responsibility."
  adversarial_precheck: "Marek duplicate, Cassia reskin, direct-combat drift, highest-defense dominance, item-as-sole-cause simplification, commander death farming, UID replacement, hidden hero score"
  remaining_uncertainty: "exact mission types, risk thresholds, equipment thresholds, injury states, timing, economy, rewards, and distributions remain NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED"
```

## Existing-solution-first boundary

`LIANA_BERG` already exists in the current Google Sheet as the Soldier additional customer/frontline commander. Decision07 promotes that existing identity; it does not invent a parallel commander customer.

```text
EXISTING_LIANA_BERG_CUSTOMER_REUSED
NO_NEW_PARALLEL_SOLDIER_COMMANDER
```

R2 already owns Soldier protection/responsibility and Kingdom Crisis demand for both supply equipment and commander-grade works. Marek already owns the supply/standardization side. Liana fills the missing single-commander side before a future world-event composition attempts to combine them.

## Player promise

Liana arrives with a disclosed frontline duty, risk context, and required equipment role. The player compares real candidate items using current Blacksmith authority, selects one same UID, hands it over, and later receives a short non-interactive field result.

The player remains:

`BLACKSMITH_COMMANDER_EQUIPMENT_DECISION_MAKER_NOT_TACTICAL_OR_UNIT_CONTROLLER`.

The player may:

- read Liana's disclosed duty, risk, role, and relevant load/compatibility constraints;
- compare one or more existing item UIDs using only currently owned item/customer evidence;
- select one item and understand 2–4 supporting/conflicting reasons;
- hand the same UID to Liana;
- receive an off-screen mission result;
- see mission duty, commander return, and item field legacy separately;
- use the result to decide repair, restoration, follow-up enhancement, replacement craft, preservation, or reassignment.

The player does not control movement, formations, targets, individual soldiers, tactical skills, casualties, battlefield positioning, or command orders.

## Mission-fit evidence contract

Decision07 creates no new Soldier raw stat or aggregate battle score. Fit may only use evidence current Blacksmith authority already owns and only when relevant to the disclosed duty, such as:

- equipment category/role eligibility;
- `WEIGHT` and customer load/compatibility gate;
- current `DURABILITY`;
- enhancement level;
- approved attack/defense/handling values when the duty actually calls for them;
- approved special-function fit when explicitly relevant;
- Liana's existing customer capability/aptitude information;
- same-UID damage, repair, provenance, and lifecycle history where it materially affects confidence or follow-up.

The system does not create `COMMAND_POWER`, `HERO_SCORE`, `LEADERSHIP_SCORE`, `MISSION_FIT_TOTAL`, or an opaque all-purpose battle rating.

## Multiple defensible equipment choices

- Highest defense is not automatically best.
- Highest enhancement is not automatically best.
- Lowest weight is not automatically best.
- A historically important item is not automatically best or worst.
- A successful mission does not prove the selected item was the only correct choice.
- A damaged returned item does not automatically mean the equipment choice was poor if the item meaningfully fulfilled the disclosed responsibility.

The decision must remain explainable through the disclosed duty plus 2–4 concrete reasons from actual customer/item evidence.

## Result contract

```text
MISSION_DUTY_STATE
COMMANDER_RETURN_STATE
ITEM_UID_FIELD_LEGACY_STATE
```

- `MISSION_DUTY_STATE`: whether and how the disclosed duty was fulfilled in the off-screen field event.
- `COMMANDER_RETURN_STATE`: Liana's return/condition consequence as a separate named-customer result, without baseline permadeath.
- `ITEM_UID_FIELD_LEGACY_STATE`: what happened to the same selected UID in field use and what it now carries forward.

These axes must remain separable. Mission success must not collapse commander condition or item contribution into one score. Commander return must not prove mission success. Item survival must not prove the item was the best choice.

## Same-UID lifecycle

`SAME_ITEM_UID_PRESERVED`.

The handed-off item and returned/recovered item remain the same UID. Field damage, protection events, repairs, recovery, provenance, and later Chronicle-relevant events attach to that UID rather than replacing it with a generic battle-result item.

## Commander consequence boundary

Liana is a named recurring customer. Decision07 may expose nonfatal return/condition consequences, but baseline permanent death is not added here.

```text
NO_BASELINE_PERMADEATH_FOR_LIANA
NO_DEATH_FARMING_OR_RECRUIT_REPLACEMENT_LOOP
```

A future explicit high-risk narrative decision may revisit permanent loss, but that is a separate approval boundary.

## Progression boundaries

- Mission count does not automatically raise `ARTISTRY`.
- Commander survival count does not automatically raise `ARTISTRY`.
- Victory or safe return does not automatically grant `CHRONICLE_AFFIX`.
- No mission/win/survival farming multiplier is added.
- Existing Chronicle authority may recognize a specific meaningful event only through its own rules.

## Information contract

Before handoff, show Liana's duty/role, key risk, selected UID, hard eligibility/load issues, and 2–4 relevant fit reasons. Do not display an automatic `BEST` item.

After resolution, show the three result axes, 2–4 causal reasons, the same UID's field state, and one primary next-action reason. Essential state cannot rely on color alone.

Exact copy, thresholds, mission duration, injury categories, economy values, rewards, and result distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.

## Ownership separation

### Marek / SOLDIER_01

Owns `SMALL_LOT_STANDARD_ORDER`: reference item, repeated production, public standard compliance, batch summary, and per-item UID preservation across a small lot.

### Liana / SOLDIER_02

Owns `FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY`: one commander, one disclosed duty, one selected UID, and separated duty/return/item-lifecycle consequence.

### Cassia / GLADIATOR_01

Owns arena context and `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`. Liana must not be “Cassia in a war skin”; public fame/signature-weapon performance is not her content goal.

## Protected boundaries

- `EXISTING_LIANA_BERG_CUSTOMER_REUSED`
- `NO_NEW_PARALLEL_SOLDIER_COMMANDER`
- `SAME_ITEM_UID_PRESERVED`
- `NO_DIRECT_TACTICAL_COMBAT`
- `NO_UNIT_MOVEMENT_OR_FORMATION_CONTROL`
- `NO_REALTIME_LOGISTICS_CONTROL`
- `NO_SOLDIER_CASUALTY_MICROMANAGEMENT`
- `NO_COMMAND_POWER_SCORE`
- `NO_HERO_SCORE`
- `NO_LEADERSHIP_SCORE`
- `NO_MISSION_FIT_TOTAL_SCORE`
- `NO_HIGHEST_DEFENSE_ALWAYS_BEST`
- `NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`
- `NO_ITEM_AS_SOLE_CAUSE_OF_MISSION_RESULT`
- `NO_BASELINE_PERMADEATH_FOR_LIANA`
- `NO_DEATH_FARMING_OR_RECRUIT_REPLACEMENT_LOOP`
- `NO_MISSION_COUNT_ARTISTRY_GROWTH`
- `NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_SURVIVAL`
- `NO_MISSION_FARMING_MULTIPLIER`
- `BLACKSMITH_COMMANDER_EQUIPMENT_DECISION_MAKER_NOT_TACTICAL_OR_UNIT_CONTROLLER`
- `PRODUCT_IMPLEMENTATION_BLOCKED`
- `TASK3_IMPLEMENTATION_NOT_APPROVED`

## Adversarial review

### Attack

1. Liana can duplicate Marek and add nothing but a named face.
2. Liana can become Cassia with “arena” renamed to “battlefield.”
3. Direct combat/formation/unit control can swallow the smithing loop.
4. Highest defense or enhancement can become the hidden universal answer.
5. The item can be treated as the sole cause of mission success/failure.
6. Named-character injury/death can turn into melodramatic farming or roster management.
7. Field result can replace the original item with a new result object/UID.
8. A hidden hero/leadership score can collapse the decision.

### Validated response

- `MUST_FIX`: Marek owns multi-UID standardization; Liana owns single-commander duty fit.
- `MUST_FIX`: Cassia owns arena contribution/public legacy; Liana owns responsibility, return consequence, and field legacy.
- `MUST_FIX`: combat resolves off-screen and remains non-interactive.
- `MUST_FIX`: actual duty/context and existing item/customer evidence must support several defensible choices.
- `MUST_FIX`: mission outcome has causes beyond the item; the result UI must not claim deterministic item causality.
- `MUST_FIX`: baseline Liana permadeath and replacement-loop management are excluded.
- `MUST_FIX`: same UID persists through handoff/result/recovery.
- `MUST_FIX`: no opaque command/hero/leadership/mission-fit score.
- `REJECTED_CRITIQUE`: adding tactical combat, party management, or commander progression would broaden scope and weaken the established smith/item-lifecycle core.

## Acceptance criteria

- `BS-CONTENT-20260811-07 / SOLDIER_02 / LIANA_BERG / FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY` becomes current R3–R7 `7/10` planning canon.
- Decisions01–06 remain approved history.
- Existing `LIANA_BERG` identity is reused; no parallel Soldier commander is created.
- Marek's batch-standardization ownership and Cassia's arena-contribution ownership remain intact.
- Result uses `MISSION_DUTY_STATE`, `COMMANDER_RETURN_STATE`, and `ITEM_UID_FIELD_LEGACY_STATE`.
- Same item UID remains authoritative through handoff and result.
- No direct tactical/unit/logistics control, aggregate hero/command/mission-fit score, highest-defense/highest-enhancement automatic answer, item-only causality, baseline permadeath, or progression farming is added.
- Product implementation and Task3 remain blocked.
