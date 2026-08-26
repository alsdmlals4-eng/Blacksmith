# [현재 정본] Blacksmith Core Simplification Canon · 2026-08-25

- Decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03`
- Status: `USER_APPROVED / CURRENT_PLANNING_CANON`
- Work Mode: `PLAN`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Runtime implementation of this canon: `NOT_RUN / IMPLEMENTATION_DRIFT_EXISTS`
- Human/Player validation: `NOT_RUN`

## 1. Current priority

This document is the current owner for the fields below and overrides older 2026-08-20/24 planning material only where the same field conflicts.

```text
ENHANCEMENT_CADENCE
PRECISION_ENHANCEMENT_CADENCE
ITEM_KEYWORD_CREATION_GATE
DAMAGE_STATE_AUTHORITY
ENHANCEMENT_DAMAGE_GATE
CUSTOMER_WORLD_EVENT_DAMAGE_HOOK
PLAYER_FACING_CHRONICLE_INCLUSION
ART_DIRECTION_SELECTION
```

Older CURRENT/MAX, multi-milestone Precision Enhancement, repair/overhaul percentage formulas, structural-scar penalties, and dated per-attempt Chronicle examples remain historical/partially superseded evidence. They are not fallback authority for these fields.

## 2. `BS-ENHANCE-20260825-25` · Enhancement / Precision

### 2.1 One success = one level

```text
SUCCESS_LEVEL_DELTA = +1
NO_MULTI_LEVEL_SUCCESS
TARGET_LEVEL = CURRENT_LEVEL + 1
```

Every successful enhancement raises the item by exactly one enhancement level. Normal or special success cannot skip levels.

### 2.2 Precision Enhancement happens only once

```text
+0 -> +1 ... +8 -> +9 = NORMAL_ENHANCEMENT
+9 -> +10 = PRECISION_ENHANCEMENT
+10 -> +11 ... +99 -> +100 = NORMAL_ENHANCEMENT
```

Canonical compatibility anchor:

```text
+9 -> +10 = PRECISION_ENHANCEMENT
```

The older `+10/+20/+30/+40/+50` Precision cadence is superseded. +20/+30/+40/+50 do not reopen a Precision Enhancement screen.

### 2.3 +10 creates one keyword

Successful `+9 -> +10` Precision Enhancement creates exactly one player-facing item keyword.

```text
PLAYER_FACING_NAME = ITEM_KEYWORD
MACHINE_OWNER = CATALYST_AFFIX
CARDINALITY = 0..1
CREATION_GATE = SUCCESSFUL_TARGET_+10_PRECISION
NO_FOURTH_AFFIX_SLOT
```

The existing material context + enhancement method + one catalyst responsibilities may be reused to resolve a compatible keyword family/result at +10. A failed +10 attempt creates no keyword.

Keyword evolution/mutation after +10 is not approved by this Decision. Ordinary enhancement does not create extra keywords.

## 3. `BS-DAMAGE-20260825-26` · Four-state damage

### 3.1 One authoritative state machine

```text
NORMAL -> MINOR -> MAJOR -> DESTROYED
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = TRUE
CURRENT_MAX_AUTHORITY = SUPERSEDED
```

There is no hidden numeric CURRENT/MAX gameplay authority behind these labels. `DESTROYED` is terminal for the physical UID; history/provenance survives in the archive.

`MINOR` and `MAJOR` do not automatically inherit old MAX-based success penalties or new-effect multipliers.

### 3.2 Enhancement-failure damage gate

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
MONOTONIC_NON_DECREASING_DAMAGE_RISK
```

Damage cannot occur from enhancement failure through target +10. From target +11 onward, a failed enhancement has a non-zero conditional chance to advance one damage state. That conditional chance must be monotonic non-decreasing as target enhancement level rises.

```text
EXACT_ENHANCEMENT_DAMAGE_CURVE = TUNABLE_NOT_FINAL
DAMAGE_PROBABILITY_CURVE = USER_APPROVAL_REQUIRED
```

No exact +11~+100 probability anchors, interpolation, or caps are approved yet. Old `DAMAGE/CRITICAL` percentages are historical comparison evidence only and are not an implicit fallback.

### 3.3 Customer/world event damage

```text
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
```

When a visiting customer buys or receives the same UID item, purchase/handoff itself does not damage the item. A later eligible customer/world event that actually uses the item may resolve a one-step damage transition.

```text
CUSTOMER_HANDOFF_OR_PURCHASE
-> DELAYED_EVENT
-> EVENT_SPECIFIC_ITEM_USE_CONSEQUENCE
-> OPTIONAL_ONE_STEP_DAMAGE_ADVANCE
-> SAME_UID_NEXT_STATE
```

Not every event is damage-eligible. Exact event eligibility and event-specific probability are unresolved and remain owned by the relevant content design.

```text
CUSTOMER_EVENT_DAMAGE_POLICY = CONTENT_OWNER_DECISION_REQUIRED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
```

If an event reaches `DESTROYED`, the existing physical-death/archive/memorial/optional-successor principles continue to apply without power inheritance or same-UID revival.

## 4. Repair / overhaul status after CURRENT/MAX removal

The following old formulas are superseded and cannot be used as silent defaults:

```text
missing = MAX - CURRENT
CURRENT -> MAX
MAX unchanged
MAX + 15 / cap 60 overhaul
MAX-state success penalties
MAX-state new-effect multipliers
```

Replacement repair semantics are not invented here.

```text
MINOR_MAJOR_REPAIR_MODEL = USER_APPROVAL_REQUIRED
MAJOR_ENHANCEMENT_ELIGIBILITY = USER_APPROVAL_REQUIRED
REPAIR_MODEL = NOT_DECIDED
```

Until those gates close, human pages must show repair as unresolved rather than showing legacy percentage formulas as current rules.

## 5. `BS-CHRONICLE-20260825-27` · Meaningful events only

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY
```

Do not create player-facing Chronicle rows for routine attempt logs such as `+7 success / N days ago` or ordinary failure-by-failure records.

Player-facing Chronicle can retain meaningful item-life events such as:

```text
ITEM_CREATED
PRECISION_KEYWORD_CREATED
DAMAGE_STATE_CHANGED_BY_ENHANCEMENT
DAMAGE_STATE_CHANGED_BY_CUSTOMER_WORLD_EVENT
SIGNIFICANT_REPAIR_OR_OVERHAUL
OWNER_OR_CUSTOMER_HANDOFF
CUSTOMER_WORLD_CONSEQUENCE
DESTROYED
MEMORIAL_OR_SUCCESSOR_LINK
```

Internal ledger sequence IDs / game-day timestamps may remain for causal replay, save diagnostics, tests, or delayed content scheduling. Internal provenance does not require dated routine rows in the player UI.

## 6. Preserved product thesis

Unless a future approved Decision changes them, these remain current:

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

The current success curve, attempt cost, reinforcement-material supply, checkpoint floors, and recovery rules remain planning inputs only where they do not depend on CURRENT/MAX or the old damage-family semantics. Their numeric status remains whatever their owner already declares; this Decision does not promote test budgets to final balance.

## 7. First-session interpretation

```text
NEW_GAME
-> FIRST_ITEM
-> ORDINARY +1 ENHANCEMENT THROUGH +9
-> +9 -> +10 PRECISION_ENHANCEMENT
-> SUCCESS CREATES ONE ITEM KEYWORD
-> +10 SECURED / BREAK-EVEN STATE
-> +11 FIRST DAMAGE-ELIGIBLE STOP/PUSH RISK
-> STOP OR PUSH
-> HANDOFF / DELAYED SAME-UID RESULT
```

Do not teach CURRENT/MAX. At +11, disclose that failure can damage the item; do not display an invented exact damage probability until the new curve is approved.

## 8. `BS-ART-20260825-03` · Current art direction

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

Current visual language:

```text
hand-drawn workshop notebook
paper / leather / iron / wood material cues
warm workshop atmosphere
modern readable interaction hierarchy
item/workpiece as visual hero
non-color redundant state signals
```

The earlier black/gold generated boards remain information-architecture references only. The selected Illustrated Workshop Book comparison/Main Menu board proves style preference, but any pre-change system text inside it is non-canonical where it shows CURRENT/MAX, five structural states, old precision milestones, MAX penalties, or routine dated enhancement history.

Representative regeneration after this mechanic sync should cover:

```text
Main Menu
Enhancement Main (+1 only)
+9 -> +10 Precision Keyword
Four-state Damage / Repair decision surface
Event-only Item Chronicle
```

## 9. Supersession map

| Older owner | Current disposition |
|---|---|
| `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` | `SUPERSEDED_FOR_CURRENT_DAMAGE_AUTHORITY / HISTORICAL_EVIDENCE` |
| durability parts of `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` | `PARTIALLY_SUPERSEDED`; checkpoint-floor parts remain |
| `BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md` damage/critical split | `SUPERSEDED_FOR_CURRENT_DAMAGE_RESOLUTION`; historical budget only |
| CURRENT/MAX repair owners and `BLACKSMITH_MAX_OVERHAUL_CANON_20260824.md` | `SUPERSEDED_PENDING_NEW_REPAIR_MODEL` |
| `BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md` precision cadence | `PARTIALLY_SUPERSEDED`; method/material/catalyst responsibilities reusable at +10 only |
| `BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md` CURRENT/MAX teaching | `PARTIALLY_SUPERSEDED`; pacing and STOP/PUSH thesis retained |
| `BLACKSMITH_PRECISION_CUSTOMER_LINK_CANON_20260824.md` multi-milestone precision wording | `PARTIALLY_SUPERSEDED`; customer context and delayed same-UID causality retained |
| Visual GDD 06/08 CURRENT/MAX semantics | `SYSTEM_SEMANTICS_STALE`; information-layout reference only |

Historical documents are not rewritten to erase prior decisions. Current entrypoints must route here whenever the same field conflicts.

## 10. Implementation Reality Gate

```text
PLANNING_DESIGN = USER_APPROVED
GITHUB_CURRENT_CANON_SYNC = SYNCED / MAIN_5c29af1_POSTMERGE_READBACK_PASS
NOTION_CURRENT_CANON_SYNC = SYNCED
SHEET_SAME_ID_COMPATIBILITY = MIGRATION_ONLY / POSTMERGE_READBACK_PASS
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = NOT_RUN / BLOCKED
DAMAGE_CURVE_NUMBERS = NOT_FINAL / USER_APPROVAL_REQUIRED
REPAIR_MODEL = NOT_DECIDED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_GEOMETRY = NOT_RUN
```

`MAIN_5c29af1_POSTMERGE_READBACK_PASS` records the completed Decisions25~27/Art03 migration checkpoint; it is not a permanent current-head pointer. Live repository state must always be fresh-read. Google Sheet remains migration compatibility evidence, not a default planning or runtime authority.

Existing V2 runtime files that still encode CURRENT/MAX and old precision milestones are implementation drift/historical runtime truth after this planning Decision; they must not be mistaken for current desired product canon while the product implementation gate is closed.
