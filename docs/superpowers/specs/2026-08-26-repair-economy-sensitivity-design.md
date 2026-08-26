# Repair Economy Sensitivity Design

## Status

- Decision owner: `BS-REPAIR-20260826-31`
- Scope: planning-only deterministic analysis
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Approved analysis approach: normalized `R_BAND = 100`, with no live band-price table

## Goal

Produce a reproducible, decision-only sensitivity result for the approved
repair-cost loss coefficients `b = 0.50 / 0.65 / 0.80`.  The result must
verify Decision31's repair-job and scar-safety invariants without borrowing
the historical 0--100 durability simulator or choosing shipping prices.

## Boundaries

- Create a planning analysis tool, its JSON input, machine-readable result,
  report, and contract test only under `tools/`, `docs/`, and `tests/`.
- Do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or
  `project.godot`.
- Do not use sale price, forecast enhancement cost, MAX multiplier, or scar
  multiplier as `R_BAND`.
- Do not use the historical `tools/simulate_enhancement_balance.py` as a
  source of current durability semantics.  Its structural pattern may be
  adapted only as a reproducible batch-analysis interface.
- Do not declare a final gold table, product material recipe, runtime result,
  Android result, accessibility result, or human-play result.

## Inputs

The new input JSON has one immutable analysis setup:

```text
item_uid = BS-REPAIR-SENS-001
base_max = 5
r_band_normalized = 100
setup_coefficient = 0.05
loss_coefficients = [0.50, 0.65, 0.80]
material = common_reinforcement_material x1
```

`R_BAND = 100` is a normalized measuring unit, not an authored live price.
It lets each coefficient be compared as a percentage of the same secured
band reference.  The Decision18 `50G` material shadow value remains separate
and is reported only as one consumed material; it is never added to Gold or
used to select `R_BAND`.

The deterministic stream contains five resolved actual-damage cycles on the
same UID.  It covers Current values `4, 3, 2, 1, 4` at `MAX / BASE_MAX = 5 / 5`
and fixes each quality ratio and candidate post-scar MAX.  The fifth cycle
uses `OLD_CURRENT = 4` and `candidate_post_scar_max = 4`, requiring the
Decision31 scar skip.  Every coefficient consumes the identical stream.

## Analysis behavior

For every event and each coefficient, the tool must calculate:

```text
loss_ratio = (max - current) / base_max
gold = ceil(r_band_normalized * (setup_coefficient + b * loss_ratio))
post_scar_max = max when candidate_post_scar_max <= old_current else candidate_post_scar_max
quality_target = ceil(post_scar_max * quality_ratio)
new_current = min(post_scar_max, max(old_current + 1, quality_target))
```

It then consumes the one repair job.  A second repair attempt is recorded as
`BLOCKED_NO_REPAIR_JOB`; a later actual-damage event reopens exactly one job.
The report keeps Gold, material use, Current recovery, scar skips, job state,
and player decision outcome as separate fields.

## Acceptance rules

1. All 15 coefficient/event rows use the same UID and event stream.
2. Each eligible paid repair has positive Current gain.
3. The blocking scar is skipped without reroll and does not prevent recovery.
4. A completed repair cannot be repeated before another actual damage event.
5. Cost varies only with `b`; recovery, scar handling, material quantity, and
   repair-job state are identical across the three coefficients.
6. The report labels all results `TEMP_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE`
   and finishes with `TEST_IN_PLAY`, not a shipping-economy verdict.

## Decision interpretation

The expected mechanical result is `KEEP` for the one-job gate, scar guard,
and single material; `TEST_IN_PLAY` for all three `b` values.  The sweep can
show whether the arithmetic is monotonic and legible, but cannot determine
whether a poor repair result feels appropriately tense rather than frustrating.
No coefficient is promoted to a final price table.

## Approved-image dual storage policy

For every future image that has both user approval and an approved actual-game
consumer, preserve the exact approved binary in two places:

1. its Notion asset/consumer record; and
2. the approved project-local file path for that consumer.

The approval receipt must record `consumer_id`, `notion_page_or_record`,
`local_path`, binary SHA-256, target resolution, state family, and approval
date.  This policy does not authorize creating an image or writing under
`assets/` while the current product-implementation gate remains blocked.
