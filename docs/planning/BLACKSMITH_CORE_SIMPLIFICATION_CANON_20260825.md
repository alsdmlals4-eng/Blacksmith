# [현재 정본] Blacksmith Core Simplification Canon · 2026-08-25

- Decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03`
- Status: `USER_APPROVED / CURRENT_PLANNING_CANON`
- Work Mode: `PLAN`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Runtime implementation of this canon: `NOT_RUN / IMPLEMENTATION_DRIFT_EXISTS`
- Human/Player validation: `NOT_RUN`

## 1. Current priority

This document owns the current player/system meaning for:

```text
ENHANCEMENT_CADENCE
PRECISION_ENHANCEMENT_CADENCE
ITEM_KEYWORD_CREATION_GATE
DURABILITY_AUTHORITY
DAMAGE_STATE_DERIVATION
ENHANCEMENT_DAMAGE_GATE
DAMAGE_PROBABILITY_CURVE
DURABILITY_ENHANCEMENT_MODIFIERS
REPAIR_RESOLUTION
REPAIR_MAX_SCAR_RISK
MAJOR_ENHANCEMENT_ELIGIBILITY
CUSTOMER_WORLD_EVENT_DAMAGE_HOOK
PLAYER_FACING_CHRONICLE_INCLUSION
ART_DIRECTION_SELECTION
```

Decision29 changes the current durability architecture after Decision26. Historical CURRENT/MAX formulas and MAX-scar tables are not silently revived: the **new visible numeric model and its new temporary budgets** are owned by Decision29 and its machine-readable model.

## 2. `BS-ENHANCE-20260825-25` · Enhancement / Precision

### 2.1 One success = one level

```text
SUCCESS_LEVEL_DELTA = +1
NO_MULTI_LEVEL_SUCCESS
TARGET_LEVEL = CURRENT_LEVEL + 1
```

Every successful enhancement raises the item by exactly one enhancement level. Durability never changes this level delta.

### 2.2 Precision Enhancement happens only once

```text
+0 -> +1 ... +8 -> +9 = NORMAL_ENHANCEMENT
+9 -> +10 = PRECISION_ENHANCEMENT
+10 -> +11 ... +99 -> +100 = NORMAL_ENHANCEMENT
```

```text
+9 -> +10 = PRECISION_ENHANCEMENT
```

The older `+10/+20/+30/+40/+50` Precision cadence is superseded.

### 2.3 +10 creates one keyword

```text
PLAYER_FACING_NAME = ITEM_KEYWORD
MACHINE_OWNER = CATALYST_AFFIX
CARDINALITY = 0..1
CREATION_GATE = SUCCESSFUL_TARGET_+10_PRECISION
NO_FOURTH_AFFIX_SLOT
```

A failed +10 attempt creates no keyword. Decision29 durability effect multipliers do not change keyword cardinality or the +10 creation gate.

## 3. Durability / damage authority · Decisions26 + 28 + 29

### 3.1 Decision29 current override

Decision26 removed a hidden numeric durability axis in favor of four explicit labels. The user's 2026-08-26 repair/durability approval now changes that architecture again.

```text
BS-REPAIR-20260826-29
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
NO_HIDDEN_SECOND_DURABILITY_AUTHORITY = TRUE
CURRENT_MAX_AUTHORITY = SUPERSEDED = HISTORICAL_DECISION26_ONLY
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
```

The numeric axis is **not hidden**. `CURRENT / MAX` is a player-readable core state and the only mechanical durability authority.

```text
BASE_MAX_DURABILITY = immutable birth durability
MAX_DURABILITY = current structural ceiling
CURRENT_DURABILITY = current durability
0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
REFERENCE_BASE_MAX_DURABILITY = 5  # reference/test item only
```

Machine-readable owner:

`docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json`

Decision record:

`docs/decisions/BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md`

### 3.2 Derived player-facing damage state

The labels remain for mobile readability and Chronicle language, but are derived from the numeric authority:

```text
NORMAL -> MINOR -> MAJOR -> DESTROYED
NORMAL = CURRENT_DURABILITY == MAX_DURABILITY
MINOR = 0.50 < CURRENT_DURABILITY / MAX_DURABILITY < 1.00
MAJOR = 0 < CURRENT_DURABILITY / MAX_DURABILITY <= 0.50
DESTROYED = CURRENT_DURABILITY == 0
```

`DESTROYED` remains terminal for the physical UID. History/provenance survives in the archive.

### 3.3 Damage event amount · temporary Budget

```text
DAMAGE_EVENT_CURRENT_LOSS = 1
TEMP_TEST_BUDGET = TRUE
```

A damage event currently means `CURRENT_DURABILITY - 1`, floored at zero. The resulting label is derived after the numeric change. This amount is not final product balance.

### 3.4 Enhancement-failure damage gate and Decision28 base curve

The safe early gate remains unchanged:

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
MONOTONIC_NON_DECREASING_DAMAGE_RISK
```

Decision28 remains the owner of the **target-level base conditional probability**:

```text
PROBABILITY_BASIS = P(DAMAGE_ADVANCE | ENHANCEMENT_FAILURE, TARGET_LEVEL)
DAMAGE_PROBABILITY_CURVE = USER_APPROVED / BS-DAMAGE-20260826-28
DAMAGE_CURVE_ANCHORS_PERCENT = [11:5, 30:6, 60:7, 90:8, 100:10]
DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
DAMAGE_CURVE_ROUNDING = NONE_CANON_EXACT_UI_ROUNDING_NOT_DECIDED
```

Decision29 does not replace the anchors. It multiplies the Decision28 base risk by a temporary durability-state multiplier.

```text
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
```

## 4. Low-durability enhancement modifiers · Decision29 temporary Budget

The structural relationship is approved: lower durability must make further enhancement less attractive. Exact numbers are delegated test budgets.

| State | Success delta | New enhancement effect | Decision28 risk multiplier |
|---|---:|---:|---:|
| `NORMAL` | `0pp` | `100%` | `×1.00` |
| `MINOR` | `-3pp` | `90%` | `×1.25` |
| `MAJOR` | `-7pp` | `75%` | `×1.75` |

```text
DURABILITY_MODIFIERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

Hard guarantee stays a real 100% guarantee. Otherwise the durability success delta applies after existing success/recovery planning input.

The effect multiplier modifies only the **newly gained ordinary enhancement effect**. It does not change `SUCCESS_LEVEL_DELTA = +1`, retroactively reduce existing item stats, or change +10 keyword cardinality.

Final enhancement-failure damage risk:

```text
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, STATE)
= Decision28_base_probability(TARGET)
* Decision29_durability_damage_risk_multiplier(STATE)
```

This remains conditional on enhancement failure.

## 5. `BS-REPAIR-20260826-29` · Repair / probabilistic MAX scar

### 5.1 Repair eligibility

```text
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY
DESTROYED_REPAIR_ALLOWED = FALSE
FULL_DURABILITY_REPAIR_ALLOWED = FALSE
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
```

MAJOR does **not** force repair. The player may repair, push while damaged, or stop/handoff.

### 5.2 Repair quality · temporary Budget

| Result | Chance | Target CURRENT after repair |
|---|---:|---:|
| `EXCELLENT` | 20% | 100% of post-scar MAX |
| `STANDARD` | 60% | 75% of post-scar MAX |
| `POOR` | 20% | 50% of post-scar MAX |

```text
REPAIR_QUALITY = TEMP_TEST_BUDGET
REPAIR_MINIMUM_CURRENT_GAIN_WHEN_POSSIBLE = 1
```

The post-repair target is calculated after any MAX scar. If recovery space exists, repair gains at least one CURRENT point.

### 5.3 Probabilistic MAX scar · temporary Budget

MAX loss is not automatic. It depends on pre-repair damage state and current enhancement band.

| State | +0~10 | +11~30 | +31~60 | +61~90 | +91~100 |
|---|---:|---:|---:|---:|---:|
| `MINOR` | 10% | 15% | 20% | 25% | 30% |
| `MAJOR` | 25% | 30% | 35% | 40% | 45% |

```text
MAX_SCAR_AMOUNT_ON_TRIGGER = -1
MAX_DURABILITY_FLOOR = 1
MAX_SCAR_CHANCE = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
MAX_DURABILITY_RECOVERY = NOT_APPROVED
```

At `MAX=1`, scar chance is forced to zero. Repair itself cannot delete the physical UID; destruction remains `CURRENT=0` from an actual damage event.

### 5.4 User reference example

```text
BASE_MAX = 5
CURRENT/MAX = 1/5  # MAJOR
repair scar roll triggers
MAX 5 -> 4

EXCELLENT -> 4/4
STANDARD  -> 3/4
POOR      -> 2/4
```

If the scar roll does not trigger:

```text
EXCELLENT -> 5/5
STANDARD  -> 4/5
POOR      -> 3/5
```

### 5.5 Repair economy boundary

Decision29 closes structural repair behavior and MAJOR enhancement eligibility, but not final repair economy.

```text
REPAIR_GOLD_COST = NOT_FINAL / FOLLOWUP_REBASE_REQUIRED
REPAIR_MATERIAL_COST = NOT_FINAL / FOLLOWUP_REBASE_REQUIRED
OLD_CURRENT_TO_MAX_REPAIR_FORMULA = HISTORICAL_ONLY
OLD_MAX_OVERHAUL_PLUS15_CAP60 = HISTORICAL_ONLY
```

## 6. Customer/world event damage

```text
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
```

Purchase/handoff itself does not damage an item. A later eligible world/customer event may produce a damage event on the same UID. Decision29 means such a damage event will eventually use the same numeric durability authority; exact customer-event probability/eligibility remains unresolved.

```text
CUSTOMER_EVENT_DAMAGE_POLICY = CONTENT_OWNER_DECISION_REQUIRED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
```

## 7. `BS-CHRONICLE-20260825-27` · Meaningful events only

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY
```

Player-facing Chronicle may retain:

```text
ITEM_CREATED
PRECISION_KEYWORD_CREATED
DURABILITY_DAMAGE_EVENT
MAX_DURABILITY_SCAR_FROM_REPAIR
SIGNIFICANT_REPAIR
OWNER_OR_CUSTOMER_HANDOFF
CUSTOMER_WORLD_CONSEQUENCE
DESTROYED
MEMORIAL_OR_SUCCESSOR_LINK
```

Routine enhancement attempts remain internal telemetry/provenance rather than dated Chronicle rows.

## 8. Preserved product thesis

```text
PRIMARY_CORE = ENHANCEMENT_TENSION + DDD
PLAYER_QUESTION = STOP_OR_PUSH
ITEM_UID_IDENTITY = PRESERVED
ONE_INPUT_ONE_ATTEMPT_RESULT
RECOVERY_OWNER = ITEM_UID + TARGET_LEVEL
CHECKPOINT_FLOORS = [10, 30, 60, 90]
+10 = FIRST_ECONOMIC_SECURED_BREAK_EVEN_STATE
+11 = FIRST_SALIENT_STOP_PUSH_RISK_DECISION
+100 = MAX_ENHANCEMENT_TERMINAL
CUSTOMER_WORLD_RESULT = DELAYED_SAME_UID_CAUSALITY
```

Decision29 adds a second STOP/PUSH dimension without replacing enhancement as the primary core:

```text
DAMAGED ITEM
-> REPAIR and risk structural scar
OR PUSH and accept worse enhancement odds/effect/risk
OR STOP / HANDOFF
```

Existing success curve, recovery, attempt cost and resource supply are planning inputs, not final product balance, and must be revalidated against Decision29.

## 9. First-session interpretation

```text
NEW_GAME
-> FIRST_ITEM
-> ORDINARY +1 ENHANCEMENT THROUGH +9
-> +9 -> +10 PRECISION_ENHANCEMENT
-> SUCCESS CREATES ONE ITEM KEYWORD
-> +10 SECURED / BREAK-EVEN STATE
-> +11 FIRST DAMAGE-ELIGIBLE STOP/PUSH RISK
-> if durability drops: show CURRENT/MAX and derived state
-> repair / push damaged / stop
-> HANDOFF / DELAYED SAME-UID RESULT
```

Do not teach the obsolete hidden MAX-scar model. Teach the **current visible CURRENT/MAX** model owned by Decision29.

## 10. `BS-ART-20260825-03` · Current art direction

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

Current visual language remains hand-drawn workshop notebook, paper/leather/iron/wood material cues, warm workshop atmosphere, modern readable interaction hierarchy, workpiece as visual hero, and non-color redundant state signals.

Existing black/gold boards remain information-architecture references only. Their old CURRENT/MAX values, old MAX penalties, old precision milestones, and routine dated enhancement history are not current numeric authority.

Representative regeneration after system sync should cover:

```text
Main Menu
Enhancement Main (+1 only + visible durability)
+9 -> +10 Precision Keyword
Durability / Repair / Structural Scar decision surface
Event-only Item Chronicle
```

## 11. Supersession map

| Older owner | Current disposition |
|---|---|
| Decision26 `CURRENT_MAX_AUTHORITY = SUPERSEDED` field | `PARTIALLY_SUPERSEDED_BY_BS-REPAIR-20260826-29`; numeric durability is current again, but visible and sole authority |
| Decision26 `ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE` | `SUPERSEDED_BY_BS-REPAIR-20260826-29`; temp event amount is CURRENT -1 and labels derive afterward |
| `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` | `HISTORICAL_EVIDENCE`; old numbers/formulas are not Decision29 |
| durability parts of `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` | `HISTORICAL/PARTIAL`; checkpoint-floor parts remain |
| `BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md` | `HISTORICAL`; not Decision28/29 probability authority |
| old CURRENT/MAX repair owners | `HISTORICAL_EVIDENCE`; old pricing/formulas not fallback |
| `BLACKSMITH_MAX_OVERHAUL_CANON_20260824.md` | `SUPERSEDED / NO CURRENT MAX RECOVERY APPROVED` |
| old multi-milestone Precision docs | `PARTIALLY_SUPERSEDED`; +10 method/material responsibilities reusable only where non-conflicting |
| old Visual GDD CURRENT/MAX values | `SYSTEM_SEMANTICS_STALE`; information-layout reference only |

Historical documents are retained for provenance rather than rewritten to pretend Decision29 always existed.

## 12. Benchmark disposition

Decision29 research compares three adjacent systems without importing their numbers:

- Stars Reach: `ADAPT` probabilistic MAX loss on repair influenced by wear/damage; exact values rejected.
- Black Desert: `ADAPT` visible current/max distinction; repeat MAX-recovery economy and exact values rejected.
- FINAL FANTASY XIV: `REFERENCE / REJECT` highly reversible over-repair as Blacksmith baseline.

Full source/disposition record is in `docs/decisions/BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md`.

## 13. Implementation Reality Gate

```text
PLANNING_DESIGN = USER_APPROVED
DAMAGE_CURVE_NUMBERS = USER_APPROVED / BS-DAMAGE-20260826-28
DURABILITY_REPAIR_STRUCTURE = USER_APPROVED / BS-REPAIR-20260826-29
DURABILITY_REPAIR_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
REPAIR_ECONOMY = NOT_FINAL
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_GEOMETRY = NOT_RUN
```

Existing V2 runtime files contain old numeric durability code, but field-name similarity is **not implementation proof** of Decision29. Runtime remains implementation drift until the later planning-complete gate and TDD migration.

## 14. Next planning order

```text
1. CUSTOMER_WORLD_EVENT_DAMAGE_POLICY
2. REPAIR_ECONOMY_REBASE + durability/economy sensitivity simulation
3. FAILURE_CONSEQUENCE_COMPOSITION + UI_DAMAGE_PERCENT_ROUNDING if needed
4. REPRESENTATIVE_VISUAL_REGENERATION_AFTER_SYSTEM_SYNC
5. full planning adversarial review
6. CURRENT_PLANNING_COMPLETE user declaration
7. runtime implementation plan refresh and TDD migration
```
