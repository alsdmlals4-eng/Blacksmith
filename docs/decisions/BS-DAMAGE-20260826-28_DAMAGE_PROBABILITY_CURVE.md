# BS-DAMAGE-20260826-28 · Enhancement Failure Damage Probability Curve

- Decision ID: `BS-DAMAGE-20260826-28`
- Date: `2026-08-26 KST`
- Status: `USER_APPROVED / PLANNING_CANON`
- Parent structural Decision: `BS-DAMAGE-20260825-26`
- Work Mode: `PLAN`
- Product/runtime implementation: `BLOCKED / NOT_RUN`
- User approval: recommended balanced curve approved on `2026-08-26 KST`

## 1. Decision

This Decision closes only the enhancement-failure damage-probability gate opened by Decision26.

```text
PROBABILITY_BASIS = P(DAMAGE_ADVANCE | ENHANCEMENT_FAILURE, TARGET_LEVEL)
P(DAMAGE_ADVANCE | ENHANCEMENT_FAILURE, TARGET_LEVEL <= 10) = 0
DAMAGE_CURVE_ANCHORS = +11 5% / +30 6% / +60 7% / +90 8% / +100 10%
INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
DAMAGE_ADVANCE = EXACTLY_ONE_STATE
RUNTIME_IMPLEMENTATION = BLOCKED / NOT_RUN
```

Canonical shorthand:

```text
P(DAMAGE_ADVANCE | ENHANCEMENT_FAILURE, TARGET_LEVEL)
ANCHORS = 5% / 6% / 7% / 8% / 10%
PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
```

The authoritative machine-readable copy is:

`docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json`

## 2. Exact interpolation

For a target `t` between adjacent anchors `(a, p_a)` and `(b, p_b)`:

```text
P_percent(t) = p_a + (p_b - p_a) * (t - a) / (b - a)
```

The approved segments are:

```text
+11..+30   : 5% -> 6% over 19 target intervals
+30..+60   : 6% -> 7% over 30 target intervals
+60..+90   : 7% -> 8% over 30 target intervals
+90..+100  : 8% -> 10% over 10 target intervals
```

The canonical probability is the exact piecewise-linear value. There is no hidden integer-percent table and no implicit floor/ceil/nearest-percent rule.

```text
CANONICAL_ROUNDING = NONE
UI_DISPLAY_ROUNDING = NOT_DECIDED
```

If the future UI rounds a displayed percentage, the resolver must still use the exact canonical probability unless a later approved Decision changes the numeric authority.

## 3. Scope boundary

Decision28 decides the probability of **one four-state damage advance after an enhancement attempt has already failed**. It does not silently redesign the rest of failure resolution.

```text
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED_BY_THIS_DECISION
```

In particular, this Decision does not decide whether a single failed enhancement may combine damage with DOWNGRADE, HOLD, resource loss, or another failure consequence. That composition must be resolved explicitly before runtime migration rather than inferred from the superseded `HOLD / DOWNGRADE / DAMAGE / CRITICAL` family table.

The following also remain separate gates:

```text
MINOR_MAJOR_REPAIR_MODEL = USER_APPROVAL_REQUIRED
MAJOR_ENHANCEMENT_ELIGIBILITY = USER_APPROVAL_REQUIRED
CUSTOMER_EVENT_DAMAGE_POLICY = CONTENT_OWNER_DECISION_REQUIRED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
UI_DISPLAY_ROUNDING = NOT_DECIDED
```

## 4. Player-risk interpretation

The approved values are conditional on failure, not per-attempt destruction or per-attempt damage odds.

Using the existing non-final base-success planning budget only as a diagnostic example:

```text
+11: 18% base failure × 5% conditional damage = about 0.90% damage on the first attempt
+30: 28% base failure × 6% conditional damage = about 1.68%
+60: 31% base failure × 7% conditional damage = about 2.17%
+90: about 34.7% base failure × 8% conditional damage = about 2.78%
+100: 36% base failure × 10% conditional damage = about 3.60%
```

These products are derived diagnostics only. They are not a second damage-probability authority, do not include same-target recovery/hard guarantee, and do not reapprove the older success/economy table as final product balance.

## 5. PRE_WORK_RESEARCH_GATE · 2026-08-26

Official/direct comparison sources were fresh-read before the numeric recommendation. External probabilities are `REFERENCE_ONLY / NO_NUMERIC_IMPORT`.

### MapleStory Star Force — `ADAPT`

Sources:
- https://support-maplestory.nexon.com/hc/en-us/articles/204088639-How-do-I-enhance-equips-with-Star-Force
- https://archive.maplestory.nexon.com/news/ProbabilityResult/MonthData

Adapt:
- make enhancement risk explicit before the attempt;
- allow risk to rise at upper enhancement levels;
- preserve recovery/protection concepts rather than relying only on severe RNG.

Reject:
- do not import Star Force destruction percentages or its short star-band structure into Blacksmith;
- do not collapse Blacksmith's same-UID four-state life system into a direct destruction roll.

### Black Desert — `ADAPT`

Source:
- https://www.sa.playblackdesert.com/Pt-BR/Wiki?wikiNo=48

Adapt:
- failed enhancement can create persistent item-state/workload consequences;
- repeated failure needs recovery/guarantee pressure relief;
- protection and repair workload must remain legible to the player.

Reject:
- do not restore numeric CURRENT/MAX durability as a hidden gameplay authority;
- do not import Black Desert enhancement or durability numbers.

### Lost Ark — `ADOPT / ADAPT`

Source:
- https://www.playlostark.com/en-us/game/releases/arkesia-ignited

Adopt/Adapt:
- failure recovery and eventual guarantee support a tension model that does not require extreme damage probability;
- keep Blacksmith's existing same-target recovery/hard-guarantee planning inputs separate from the damage curve.

Reject:
- do not import honing percentages, Artisan's Energy values, or upgrade economy.

### Blacksmith differentiator

```text
DIFFERENTIATOR = STOP/PUSH enhancement risk becomes a same-UID life consequence
NORMAL -> MINOR -> MAJOR -> DESTROYED
and later reconnects to repair, Chronicle, customer/world causality, archive, and successor decisions.
```

The goal is not to maximize punishment frequency. The curve supports the value of an accumulated workpiece while leaving room for the still-unresolved repair and customer/world-event risk systems.

## 6. Adversarial pre-check

1. **Double-risk check:** the curve is conditional on failure; it is not added as an independent unconditional roll.
2. **Monotonicity check:** all exact target values from +11 through +100 are positive and monotonic non-decreasing.
3. **Secondary-authority check:** old DAMAGE/CRITICAL and CURRENT/MAX tables remain historical evidence only.
4. **Scope check:** no repair cost, MAJOR eligibility, customer-event probability, or failure-composition rule is invented here.
5. **Implementation Reality Gate:** planning approval does not prove runtime behavior, Android behavior, human pacing, accessibility, or release balance.

## 7. Next planning gate

```text
NEXT = MINOR_MAJOR_REPAIR_MODEL + MAJOR_ENHANCEMENT_ELIGIBILITY
THEN = CUSTOMER_EVENT_DAMAGE_POLICY
THEN = REPRESENTATIVE_VISUAL_REGENERATION_AFTER_SYSTEM_SYNC
```

The approved curve must be used as an input to repair-workload/economy analysis, but it does not itself approve the repair economy.
