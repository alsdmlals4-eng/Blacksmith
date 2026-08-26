# BS-REPAIR-20260826-31 — Repair Economy Rebase and Sensitivity Contract

- Status: `USER_APPROVED_PLANNING_CANON`
- Scope: planning and deterministic balance-contract work only
- Owner: repair economy overlay for Decision 29
- Supersedes: only the Decision 29 fields named in “Precedence”; does not replace its durability, scar-band, or repair-quality structure
- Runtime status: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Numeric status: `TEMPORARY_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE`

## Decision

Repair is a paid, player-chosen recovery action. Its price is driven only by the item’s secured enhancement-band reference and normalized missing durability. A completed repair is one job per eligible actual-damage cycle, never a reroll loop.

A repair job becomes available when a resolved **actual** damage event reduces an item’s Current durability. The job is stored as a boolean per item UID:

```text
REPAIR_JOB_AVAILABLE = true
```

Further actual damage before repair leaves the flag true; it does not create additional tickets or stacked benefits. Starting a repair consumes the flag whether the outcome is excellent, standard, poor, or scarred. The next repair needs a later actual damage event.

## Eligibility and payment

```text
REPAIR_ELIGIBLE =
  0 < CURRENT < MAX
  AND REPAIR_JOB_AVAILABLE

LOSS_RATIO = (MAX - CURRENT) / BASE_MAX
GOLD = ceil(R_BAND * (0.05 + 0.65 * LOSS_RATIO))
REPAIR_PAYMENT = GOLD + 1 common_reinforcement_material
```

Definitions:

- `R_BAND` is the authored, secured enhancement-band reference for the item. It is an explicit simulation input, not the current sell price, a forecast next-attempt price, or a MAX/scar multiplier.
- `R_BAND` now uses the approved **mutable test baseline** below. It is a fixed gold-only normal-enhancement reference by primary material and secured band; it may change after human playtesting or new balance evidence. It is not a shipping price table.
- `BASE_MAX` remains the Decision 29 base maximum (the test reference is 5 until a later rebase). The denominator never moves after a scar.
- `common_reinforcement_material` is the always-available common resource defined by the common-resource supply canon. It grants no repair-price discount.
- The initial sensitivity sweep holds setup at `0.05` and tests loss coefficients `0.50 / 0.65 / 0.80` under identical deterministic inputs. The `0.65` curve is the approved initial test baseline, not a shipping price table.

| Secured band | Iron | Silver | Meteor iron |
|---|---:|---:|---:|
| `+0~10` | 125 | 145 | 170 |
| `+11~30` | 160 | 185 | 215 |
| `+31~60` | 220 | 255 | 295 |
| `+61~90` | 300 | 345 | 405 |
| `+91~100` | 400 | 460 | 540 |

The earlier `R_BAND = 100` sweep remains historical normalized sensitivity evidence only. It does not override this mutable test baseline.

Destroyed items (`CURRENT = 0`) and full items (`CURRENT = MAX`) are ineligible for repair. A major-damage item remains eligible for enhancement under Decision 29; this decision does not make repair mandatory.

## Scar and rounding safety

Decision 29 quality and scar probabilities remain authoritative. This overlay changes the repair-resolution guard and rounding order:

```text
candidate_post_scar_max = MAX after the selected Decision 29 scar result

if candidate_post_scar_max <= OLD_CURRENT:
    skip the scar; do not reroll quality or scar

POST_SCAR_MAX = candidate_post_scar_max (or unchanged MAX when skipped)
QUALITY_TARGET = ceil(POST_SCAR_MAX * QUALITY_RATIO)
NEW_CURRENT = min(
  POST_SCAR_MAX,
  max(OLD_CURRENT + 1, QUALITY_TARGET)
)
```

Therefore a paid, eligible repair always gives at least one Current-durability point. The guard does not refund, add a second quality roll, add a scar reroll, or remove the future MAX-risk system. It only rejects a scar outcome that would make positive recovery impossible at the five-point reference scale.

The formula can fully restore a one-point minor-damage item. That is an intentional discrete-scale result to test, not evidence that repeated maintenance is the desired product loop.

## Player-facing contract for later implementation

Before confirming repair, the UI must state:

1. Current / Max / Base Max and repair eligibility;
2. the quoted gold and one common material payment;
3. expected recovery by quality result;
4. whether the current item state is exposed to a possible MAX scar; and
5. that a repair consumes the current repair job and another actual damage event is needed for another repair.

No UI, save-state, economy, scene, asset, or runtime implementation is authorized by this planning decision.

## Sensitivity and acceptance contract

Every sweep must:

- use the same deterministic event sequence, item UID, quality/scar stream, and `R_BAND` input across compared curves;
- vary one economic variable at a time;
- report gold, material use, recovery, scar skips, repair-job consumption, and player decision outcome separately;
- include `b = 0.50, 0.65, 0.80` for `GOLD = ceil(R_BAND * (0.05 + b * LOSS_RATIO))`;
- verify no eligible repair returns zero Current gain;
- verify no repair can be repeated without a later resolved actual damage event; and
- preserve Decision 29’s damage, quality, scar-band, rare-scar, and enhancement-gate invariants.

The first sweep must keep `R_BAND` as an explicit normalized input. Choosing a live band-price table, a final gold target, or a product-ready material recipe is deferred until evidence and a user-approved balance interpretation exist.

## Precedence

This decision supersedes Decision 29 only for:

- repair-job availability and consumption;
- repair eligibility;
- repair payment formula and one-common-material payment;
- the source restrictions on `R_BAND`;
- scar guard and post-scar rounding order; and
- the sensitivity/acceptance requirements above.

Decision 29 remains the structural owner of Current / Max / Base Max, damage severities, repair-quality probabilities, scar bands, rare-scar behavior, destroyed/full state meaning, and enhancement eligibility.

## Evidence boundary

External references are adaptation principles only:

- Stars Reach demonstrates that repair can visibly couple damage with a MAX-durability risk; it is not a copied probability, economy, or item-scale model. [Source](https://starsreach.com/before-the-frontier/)
- Black Desert distinguishes ordinary durability recovery from MAX-durability restoration; it is not a price or resource benchmark. [Source](https://www.naeu.playblackdesert.com/en-US/Wiki?wikiNo=172)
- Diablo IV’s material simplification informs the “one common material” complexity cap only; it does not set the gold curve. [Source](https://news.blizzard.com/en-us/article/24244466/diablo-iv-patch-notes-2-5)

## Adversarial closure

Five full-scope planning review loops closed the following valid risks:

1. repair rerolls after a bad result → one boolean job per actual-damage cycle;
2. five-point scars that erase recovery → skip only the blocking scar, without rerolls;
3. scar plus cost multiplier as a double tax → no MAX/scar price multiplier;
4. sell price or next-attempt price dominating repair → `R_BAND` only; and
5. historical simulations or benchmark games being mistaken for product truth → temporary parameters, deterministic sensitivity, and ADAPT-only evidence labels.

No runtime claim, human play-simulation result, final price table, or implementation approval is created by this decision.
