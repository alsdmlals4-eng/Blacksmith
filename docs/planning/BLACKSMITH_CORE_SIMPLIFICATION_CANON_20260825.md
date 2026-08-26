# [현재 정본] Blacksmith Core Simplification Canon · 2026-08-25

- Decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03`
- Status: `USER_APPROVED / CURRENT_PLANNING_CANON`
- Work Mode: `PLAN`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Runtime implementation: `NOT_RUN / IMPLEMENTATION_DRIFT_EXISTS`
- Human/Player validation: `NOT_RUN`

## 1. Current ownership

This document owns the integrated current meaning for enhancement cadence, precision keyword, visible durability, derived damage state, Decision28 damage probability, Decision29 repair/scar model, Chronicle inclusion and art direction.

Decision-specific machine owners:

- `docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json`
- `docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json`

Historical CURRENT/MAX values, MAX bands, old repair/overhaul formulas, old DAMAGE/CRITICAL ratios and multi-precision cadence are not fallback authority.

## 2. Enhancement / Precision · `BS-ENHANCE-20260825-25`

```text
SUCCESS_LEVEL_DELTA = +1
NO_MULTI_LEVEL_SUCCESS
TARGET_LEVEL = CURRENT_LEVEL + 1
+9 -> +10 = PRECISION_ENHANCEMENT
+10 PRECISION SUCCESS -> exactly one ITEM_KEYWORD
ITEM_KEYWORD machine owner = CATALYST_AFFIX
NO_FOURTH_AFFIX_SLOT
```

+20/+30/+40/+50 do not reopen Precision. Durability modifiers never change the +1 level delta or +10 keyword cardinality.

## 3. Current durability authority · `BS-REPAIR-20260826-29`

Decision29 partially supersedes Decision26's no-numeric-authority/state-step fields. Numeric durability is now **visible and sole mechanical authority**.

```text
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
NO_HIDDEN_SECOND_DURABILITY_AUTHORITY = TRUE
BASE_MAX_DURABILITY = immutable birth durability
MAX_DURABILITY = current structural ceiling
CURRENT_DURABILITY = current durability
0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
REFERENCE_BASE_MAX_DURABILITY = 5  # reference/test item only
CURRENT_MAX_AUTHORITY = SUPERSEDED = HISTORICAL_DECISION26_ONLY
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
```

### 3.1 Effective durability ratio

A perfect CURRENT repair does not erase a permanent MAX scar. Therefore current damage and structural scar are collapsed into **one** effective ratio rather than stacked as two penalties.

```text
CURRENT_CONDITION_RATIO = CURRENT_DURABILITY / MAX_DURABILITY
STRUCTURAL_CONDITION_RATIO = MAX_DURABILITY / BASE_MAX_DURABILITY
EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)
```

State derivation:

```text
DESTROYED = CURRENT_DURABILITY == 0
NORMAL = EFFECTIVE_DURABILITY_RATIO == 1.00
MINOR = 0.50 < EFFECTIVE_DURABILITY_RATIO < 1.00
MAJOR = 0 < EFFECTIVE_DURABILITY_RATIO <= 0.50
```

Reference examples with `BASE_MAX=5`:

```text
5/5/5 -> NORMAL
4/5/5 -> MINOR
2/5/5 -> MAJOR
4/4/5 -> MINOR   # fully repaired, permanent scar remains
2/2/5 -> MAJOR   # fully repaired, severe structural scar remains
1/1/5 -> MAJOR
0/5/5 -> DESTROYED
```

This avoids both failure modes: MAX scar becoming cosmetic, and CURRENT damage + MAX scar being punished twice.

### 3.2 Damage event amount · temporary Budget

```text
DAMAGE_EVENT_CURRENT_LOSS = 1
TEMP_TEST_BUDGET = TRUE
```

A damage event lowers CURRENT by one, floored at zero; derived state is recalculated afterward. This amount is not final balance.

## 4. Enhancement-failure damage · `BS-DAMAGE-20260826-28`

Early safety gate remains:

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
```

Decision28 target-level base conditional curve remains unchanged:

```text
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
+11  = 5%
+30  = 6%
+60  = 7%
+90  = 8%
+100 = 10%
DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
DAMAGE_CURVE_ROUNDING = NONE_CANON_EXACT_UI_ROUNDING_NOT_DECIDED
```

Decision29 applies one modifier from the current **effective** durability state:

| Effective state | Success delta | New ordinary effect | Decision28 risk multiplier |
|---|---:|---:|---:|
| `NORMAL` | `0pp` | `100%` | `×1.00` |
| `MINOR` | `-3pp` | `90%` | `×1.25` |
| `MAJOR` | `-7pp` | `75%` | `×1.75` |

```text
DURABILITY_MODIFIERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, EFFECTIVE_STATE)
= Decision28_base_probability(TARGET) * Decision29_state_multiplier(EFFECTIVE_STATE)
```

Hard guarantee stays real 100%. Effect multiplier applies only to newly added ordinary enhancement effect, not existing stats, +1 level delta or keyword count.

```text
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
```

## 5. Repair / probabilistic MAX scar · `BS-REPAIR-20260826-29`

```text
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY
DESTROYED_REPAIR_ALLOWED = FALSE
FULL_DURABILITY_REPAIR_ALLOWED = FALSE
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
MAX_DURABILITY_RECOVERY = NOT_APPROVED
```

MAJOR does not force repair; player may repair, push damaged/scarred, or stop/handoff.

### 5.1 Temporary repair quality

| Result | Chance | Target CURRENT after repair |
|---|---:|---:|
| EXCELLENT | 20% | 100% of post-scar MAX |
| STANDARD | 60% | 75% of post-scar MAX |
| POOR | 20% | 50% of post-scar MAX |

```text
REPAIR_MINIMUM_CURRENT_GAIN_WHEN_POSSIBLE = 1
REPAIR_QUALITY = TEMP_TEST_BUDGET
```

### 5.2 Temporary MAX -1 scar chance

| Pre-repair effective state | +0~10 | +11~30 | +31~60 | +61~90 | +91~100 |
|---|---:|---:|---:|---:|---:|
| MINOR | 10% | 15% | 20% | 25% | 30% |
| MAJOR | 25% | 30% | 35% | 40% | 45% |

```text
MAX_SCAR_AMOUNT_ON_TRIGGER = -1
MAX_DURABILITY_FLOOR = 1
MAX_SCAR_CHANCE = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

At MAX=1 scar chance becomes zero. Repair itself cannot destroy the item. A scarred full item cannot reroll MAX recovery because full-durability repair is ineligible and MAX recovery is not approved.

User reference:

```text
BASE_MAX=5, CURRENT/MAX=1/5
scar triggers -> MAX 5->4
EXCELLENT -> 4/4/5 -> MINOR
STANDARD  -> 3/4/5 -> MINOR
POOR      -> 2/4/5 -> MAJOR
```

Without scar: EXCELLENT `5/5/5 NORMAL`, STANDARD `4/5/5 MINOR`, POOR `3/5/5 MINOR`.

Repair gold/material/fatigue economy is still `NOT_FINAL / FOLLOWUP_REBASE_REQUIRED`. Old CURRENT→MAX price formulas and old `MAX +15 / cap60` overhaul are historical only.

## 6. Customer/world event damage

```text
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
CUSTOMER_EVENT_DAMAGE_POLICY = CONTENT_OWNER_DECISION_REQUIRED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
```

Later event damage must feed the same numeric durability resolver; it must not create a second damage state machine.

## 7. Chronicle · `BS-CHRONICLE-20260825-27`

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY
```

Player Chronicle may retain creation, +10 keyword, durability damage, meaningful repair, MAX scar, handoff, world consequence, destruction, memorial/successor. Routine attempt clicks remain internal provenance/telemetry.

## 8. Preserved product thesis

```text
PRIMARY_CORE = ENHANCEMENT_TENSION + DDD
PLAYER_QUESTION = STOP_OR_PUSH
ITEM_UID_IDENTITY = PRESERVED
RECOVERY_OWNER = ITEM_UID + TARGET_LEVEL
CHECKPOINT_FLOORS = [10,30,60,90]
+10 = FIRST_ECONOMIC_SECURED_BREAK_EVEN_STATE
+11 = FIRST_SALIENT_STOP_PUSH_RISK_DECISION
+100 = MAX_ENHANCEMENT_TERMINAL
CUSTOMER_WORLD_RESULT = DELAYED_SAME_UID_CAUSALITY
```

Decision29 adds a repair/push/stop choice inside the same core rather than creating a maintenance game as a second core.

Existing success/recovery/attempt-cost/resource/economic values remain planning inputs and require Decision29 sensitivity revalidation.

## 9. First-session interpretation

```text
NEW_GAME
-> FIRST_ITEM
-> ordinary +1 enhancement through +9
-> +9 -> +10 Precision
-> +10 success creates one keyword
-> +10 secured state
-> +11 first damage-eligible STOP/PUSH
-> if damaged/scarred: show CURRENT/MAX/BASE_MAX + effective state
-> REPAIR / PUSH DAMAGED / STOP
-> HANDOFF / DELAYED SAME-UID RESULT
```

Do not teach obsolete hidden MAX bands; teach current visible numeric durability.

## 10. Art direction · `BS-ART-20260825-03`

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

Representative regeneration after system sync: Main Menu; Enhancement Main with visible durability; +9→+10 Precision Keyword; Durability/Repair/Structural Scar; event-only Chronicle. Old boards are information-architecture reference only where system semantics conflict.

## 11. Supersession boundary

- Decision26 no-numeric-authority and one-state-per-event fields: `PARTIALLY_SUPERSEDED_BY_BS-REPAIR-20260826-29`.
- Historical 0~100 CURRENT/MAX scale, old MAX bands/success/effect penalties: historical only.
- Old repair formulas and `MAX +15 / cap60` overhaul: historical/superseded; not fallback.
- Old DAMAGE/CRITICAL family ratios: historical; not Decision28/29 authority.
- Old multi-precision cadence: partially superseded; +10-only current.
- Old Visual GDD numeric durability values: `SYSTEM_SEMANTICS_STALE`.

## 12. Implementation Reality Gate

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

V2 runtime field-name similarity is not Decision29 implementation proof. Protected product paths remain untouched while PLAN gate is closed.

## 13. Next planning order

```text
1. CUSTOMER_WORLD_EVENT_DAMAGE_POLICY
2. REPAIR_ECONOMY_REBASE + durability/economy sensitivity simulation
3. FAILURE_CONSEQUENCE_COMPOSITION + UI_DAMAGE_PERCENT_ROUNDING if needed
4. REPRESENTATIVE_VISUAL_REGENERATION_AFTER_SYSTEM_SYNC
5. full planning adversarial review
6. CURRENT_PLANNING_COMPLETE user declaration
7. runtime implementation plan refresh and TDD migration
```
