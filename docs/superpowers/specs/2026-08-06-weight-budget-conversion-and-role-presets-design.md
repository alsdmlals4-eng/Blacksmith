# Weight Budget Conversion and Role Presets Design

- Decision: `BS-ITEM-20260806-03`
- Batch: `R2_BATCH_005_7_OF_10`
- Status: `USER_APPROVED / APPROVED_PENDING_MERGE`
- Product implementation: `BLOCKED`

## Purpose

Convert the already approved monotonic weight performance budget into understandable item outputs without adding a separate point-allocation game. The conversion must make weighting meaningful, preserve lightweighting's value, and keep normal enhancement as the dominant event-success control.

## Considered approaches

### A. Player freely allocates every budget point

This offers maximum build freedom but requires a dedicated allocation UI, invites dominant split optimization, and turns weight into a second progression game. Rejected.

### B. Every equipment group uses one automatic role profile

The base item definition chooses one immutable role profile at first crafting. Initial and later weight-derived budget follows that profile. This is the approved approach because it is explainable, mobile-friendly, and prevents post-craft reallocation exploits.

### C. Universal hybrid ratios

Every item divides budget between two or more lanes. This creates rounding rules and obscures why a specific item gained a stat. Rejected as a baseline. A future content family may define an explicit hybrid profile only through a separate approved design.

## Approved conversion

```text
1 ATTACK_BUDGET = ATTACK +5
1 DEFENSE_BUDGET = DEFENSE +5
1 MAGIC_FUNCTION_BUDGET = MAGIC_FUNCTION_CAPACITY +1
1 UTILITY_BUDGET = UTILITY_CAPACITY +1
```

The physical conversion uses five points because weight itself advances in five-point steps. One new peak-weight step therefore produces one clearly previewable result: `weight +5 / attack +5`, `weight +5 / defense +5`, or one function-capacity point.

## Profile architecture

A UID stores one immutable `PERFORMANCE_PROFILE` selected by the base item definition at first crafting completion.

```text
PHYSICAL_WEAPON
PROTECTIVE_GEAR
MAGIC_IMPLEMENT
UTILITY_IMPLEMENT
UTILITY_GARMENT
NONE
```

The profile maps to exactly one budget lane. The player does not receive a free allocation screen, and post-craft free reallocation is prohibited. New budget from a higher recognized weight follows the existing profile automatically.

## Default mapping

```text
SWORD / AXE / BLUNT / POLEARM / RANGED -> PHYSICAL_WEAPON
LIGHT_ARMOR / MEDIUM_ARMOR / HEAVY_ARMOR / SHIELD_SUPPORT -> PROTECTIVE_GEAR
TOOL -> UTILITY_IMPLEMENT
CLOTHING_OR_ROBE -> UTILITY_GARMENT
ACCESSORY -> NONE
```

A magic implement is an explicit base-item-design override. It is not a player toggle. Clothing and robes default to utility because the combined equipment group includes nonmagical garments.

## Function capacity

Magic and utility effects declare positive integer capacity costs.

```text
standard approved function: 1
strong or multi-context function: 2
transformative or rule-bypass function: 3
```

A cost-3 function also requires a separate design approval. Capacity is a budget constraint, not permission to create unapproved content.

## Data flow

```text
base equipment group
-> base item PERFORMANCE_PROFILE
-> INITIAL_WEIGHT / 5
-> initial lane budget
-> converted item output
-> weighting above historical peak adds one budget point to same lane
-> lightweighting lowers CURRENT_WEIGHT but preserves recognized budget and output
```

Customer load checks continue to use `CURRENT_WEIGHT`. Performance output continues to use monotonic recognized weight.

## Display

The normal item surface shows final attack, defense, or functions. A detail view may show one source line such as `중량 기반 공격 +10`. Precision-enhancement preview shows the current and resulting weight plus the exact output change. No allocation matrix is added.

## Compatibility boundaries

- Weight-derived output is owned by the item UID.
- Customer stats do not duplicate item attack or defense.
- Weight-derived attack and defense do not enter the generic event-success formula automatically.
- `base_progress` remains crafting progress and `base_value` remains value input.
- The same weight source cannot be counted both in a base stat table and again through the budget conversion.
- Material, grade, artistry, catalyst, chronicle, and enhancement do not multiply the conversion automatically.
- Runtime and product data remain unchanged in this Decision.

## Testing

The planning contract must verify exact conversion, immutable profile selection, default equipment mapping, capacity costs, weighting/lightweighting behavior, active batch 7/10, authority-document registration, and unchanged protected product data.
