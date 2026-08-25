# Blacksmith Damage Source Amendment Design

- Date: 2026-08-25 KST
- Classification: ARCHITECTURAL AMENDMENT
- Parent spec: `docs/superpowers/specs/2026-08-25-blacksmith-enhancement-damage-chronicle-simplification-design.md`
- Decision owner: `BS-DAMAGE-20260825-26`
- User approval: explicit 2026-08-25 KST approval after parent-spec review
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. Approved amendment

The four-state damage model remains:

```text
NORMAL -> MINOR -> MAJOR -> DESTROYED
```

Every accepted damage event advances exactly one state. `DESTROYED` is terminal for the physical item; UID/history provenance remains.

Two damage sources are now approved.

### A. Enhancement-failure damage

Damage from enhancement failure is locked until the item has secured +10.

```text
TARGET <= +10
P(DAMAGE_ADVANCE | ENHANCEMENT_FAILURE) = 0

TARGET >= +11
P(DAMAGE_ADVANCE | ENHANCEMENT_FAILURE) > 0
```

For `TARGET >= +11`, the conditional damage probability must be monotonic non-decreasing as target enhancement level rises.

```text
for a < b and a,b >= 11:
P(DAMAGE_ADVANCE | FAILURE, target=b)
>= P(DAMAGE_ADVANCE | FAILURE, target=a)
```

This is a structural rule, not a numeric balance approval. Exact anchors, interpolation, caps, and band-level values are `TUNABLE / USER_APPROVAL_REQUIRED / NOT_FINAL_PRODUCT_BALANCE`.

A failed attempt still resolves only one failure consequence path. If the damage roll triggers, advance one damage state. Do not resurrect the old `CURRENT/MAX`, `FAIL_CRITICAL_DAMAGE`, hidden scar roll, or separate destroy roll.

### B. Customer/world-event damage

After a visiting customer buys or receives an item, the same UID can be exposed to real use in the customer's delayed event/content lifecycle. An eligible resolved event may advance the item's damage state by one step.

```text
CUSTOMER_HANDOFF_OR_PURCHASE
-> delayed customer/world event
-> event-specific item-use consequence
-> optional DAMAGE_ADVANCE
-> same UID next state / Chronicle consequence
```

Rules:

- purchase/handoff itself does not automatically damage the item;
- not every customer/world event must be damage-eligible;
- an eligible event can advance at most one damage state unless a later explicit decision says otherwise;
- exact event eligibility and probabilities are `TUNABLE / CONTENT_OWNER_DECISION_REQUIRED`;
- the result must be causally attributable to the actual event and same item UID;
- a world-event damage transition is a meaningful Chronicle event;
- if the transition reaches `DESTROYED`, the existing physical-death/archive/successor principles remain.

This reuses the existing delayed `VSContentResultRecord` / item-UID lifecycle concept rather than creating a second customer-history system.

## 2. Supersession impact

The parent spec's temporary idea of directly aggregating old `DAMAGE + CRITICAL` percentages into a final migration table is no longer an approved numeric migration. Those old values can be historical comparison evidence only.

Current structural damage contract is now:

```text
ENHANCEMENT_SUCCESS_OR_FAILURE
-> if failure and target >= 11: conditional damage roll from NEW curve
-> if roll triggers: advance one state

CUSTOMER_WORLD_EVENT
-> if event is damage-eligible: event-specific damage roll
-> if roll triggers: advance one state
```

The new curve must be designed separately. Do not use the old CURRENT/MAX severity table or old failure-family ratios as an implicit fallback.

## 3. Player-facing disclosure

Before an enhancement attempt:

- at `TARGET <= +10`, the screen must not imply enhancement-failure item damage;
- at `TARGET >= +11`, the screen must disclose that failure can damage the item;
- the exact percent is shown only after a numeric curve is approved and implemented;
- higher enhancement should communicate higher damage risk without requiring color alone.

For customer/world events, the player does not need a universal damage percent on every customer card. The relevant content result should explain the actual event cause if damage occurred.

## 4. Chronicle interaction

Routine enhancement attempts remain excluded from the player-facing Chronicle.

Chronicle-worthy damage events include:

```text
DAMAGE_STATE_CHANGED_BY_ENHANCEMENT
DAMAGE_STATE_CHANGED_BY_CUSTOMER_WORLD_EVENT
DESTROYED_BY_ENHANCEMENT
DESTROYED_BY_CUSTOMER_WORLD_EVENT
```

Internal sequence/day provenance may remain for causality, while the player-facing Chronicle does not need `N days ago` rows for routine enhancement attempts.

## 5. Follow-up gates before runtime migration

Runtime code must not be migrated until these remaining decisions are closed:

1. enhancement-failure damage probability curve for +11~+100;
2. customer/world content event eligibility and event-specific damage probability policy;
3. `MINOR` and `MAJOR` repair results/costs, including whether MAJOR needs a special overhaul action;
4. whether MAJOR blocks further enhancement or merely carries destruction risk.

No legacy numeric durability formula may be used as a silent default while these gates are open.

## 6. Acceptance

Planning sync is correct only if current authority clearly states all of the following:

```text
DAMAGE_STATE_AUTHORITY = NORMAL / MINOR / MAJOR / DESTROYED
ENHANCEMENT_DAMAGE_BEFORE_PLUS_11 = IMPOSSIBLE
ENHANCEMENT_DAMAGE_FROM_PLUS_11 = POSSIBLE_AND_MONOTONICALLY_RISING
EXACT_ENHANCEMENT_DAMAGE_CURVE = NOT_FINAL
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = TRUE
CURRENT_MAX_AUTHORITY = SUPERSEDED
```
