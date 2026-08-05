# Customer Capability and Equipment Compatibility Design

**Decision:** `BS-CUSTOMER-20260805-01`  
**Status:** USER_APPROVED  
**Batch:** `R2_BATCH_005_2_OF_10`

## Goal

Make customer–item matching legible and consequential without turning Blacksmith into a customer-RPG or duplicating item power.

## Approved model

1. Persist Strength, Dexterity, Constitution, and Judgment at 1–10.
2. Persist sparse weapon and armor proficiencies at 0–3: one primary and at most one secondary each.
3. Persist magic aptitude at 0–10 and at most two optional affinity tags for magic-relevant customers.
4. Derive total weight, comfortable load, balance state, and special-function fit from the equipped loadout.
5. Classify items as weapon, shield/offhand, armor, or accessory/tool and omit non-applicable stats.
6. Keep raw attack, defense, and other values owned by the item UID; customer capability changes utilization and risk, not raw item stats.
7. Preserve the existing 1–10 risk disclosure and 5–95% approximate success forecast.

## Core-fun guard

The feature must improve the decision “which work should I entrust to this customer?” and feed the result back into forging, enhancement, repair, and the item’s UID history. It must not create a separate customer-build optimization loop.

## Open values

Load conversion, utilization coefficients, forecast contribution caps, and named-customer presets remain `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.
