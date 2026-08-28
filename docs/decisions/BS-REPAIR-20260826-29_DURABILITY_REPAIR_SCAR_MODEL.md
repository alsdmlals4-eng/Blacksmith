# BS-REPAIR-20260826-29 · Durability / Repair / Structural Scar Model

- Date: `2026-08-26 KST`
- User approval: `수리는 현재/최대 내구도 수치로 운용하고, 낮은 내구도는 강화 성공률·새 강화효과·파손 위험에 불리하게 작용하며, 수리 결과와 MAX 손실은 확률 판정으로 처리. 세부 확률은 임시 권장안으로 진행.`
- Status: `USER_APPROVED_STRUCTURAL_CANON / TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Parent: `BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28`
- Work Mode: `IMPLEMENTATION_AND_REVIEW`
- Current execution: `CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826`
- Product runtime: `CURRENT_CANON_MVP_AUTHORIZED / EXACT_HEAD_CONTRACT_AND_TDD_REQUIRED`

## 1. Decision purpose

Decision26의 핵심 의도였던 **숨은 두 번째 내구도 권위 금지**는 유지한다. 다만 사용자의 최신 승인에 따라 숫자 내구도 자체를 다시 **보이는 단일 gameplay authority**로 채택한다.

```text
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
NO_HIDDEN_SECOND_DURABILITY_AUTHORITY = TRUE
```

`NORMAL / MINOR / MAJOR / DESTROYED`는 별도 상태머신이 아니라 같은 숫자 내구도에서 파생되는 사람이 읽기 쉬운 상태명이다. Decision26의 `CURRENT_MAX_AUTHORITY = SUPERSEDED`와 `ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE`는 Decision29와 충돌하는 필드에서 부분 대체된다.

## 2. Numeric durability authority

```text
BASE_MAX_DURABILITY
= 작품이 태어날 때의 원래 최대 내구도
= immutable provenance value

MAX_DURABILITY
= 현재 작품이 회복할 수 있는 구조적 최대 내구도

CURRENT_DURABILITY
= 현재 남은 내구도

0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
```

Reference item only:

```text
REFERENCE_BASE_MAX_DURABILITY = 5
```

`5`는 사용자가 든 대표 예시와 첫 테스트 Budget을 위한 기준값이며 모든 아이템 family의 출시 고정값이 아니다. 재료/아이템 family별 birth durability 차이는 별도 데이터 Decision이 필요하다.

### 2.1 Why MAX scars must remain mechanically relevant

수리 결과가 `1/5 -> 4/4`가 되었을 때 `CURRENT/MAX`만 보면 다시 100% 상태이지만, `MAX/BASE_MAX = 4/5`라는 영구 구조 흉터가 남는다. 이 작품을 pristine `5/5`와 완전히 같게 취급하면 MAX 감소가 이름뿐인 패널티가 된다.

따라서 같은 세 숫자에서 두 비율을 계산하고 **더 나쁜 쪽 하나만** 최종 내구도 상태 판정에 사용한다.

```text
CURRENT_CONDITION_RATIO = CURRENT_DURABILITY / MAX_DURABILITY
STRUCTURAL_CONDITION_RATIO = MAX_DURABILITY / BASE_MAX_DURABILITY
EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)
```

이 구조는 두 개의 독립 권위를 만들지 않는다. 입력은 모두 `CURRENT / MAX / BASE_MAX` 한 묶음이고, 최종 enhancement modifier owner도 `EFFECTIVE_DURABILITY_RATIO` 하나뿐이다.

금지:

```text
CURRENT state penalty + MAX scar penalty를 각각 별도 곱셈
hidden scar score
old MAX band success penalty 자동 부활
```

## 3. Derived player-facing states

`CURRENT == 0`은 다른 비율 계산보다 우선해 terminal이다.

```text
DESTROYED = CURRENT_DURABILITY == 0

if CURRENT_DURABILITY > 0:
    CURRENT_CONDITION_RATIO = CURRENT_DURABILITY / MAX_DURABILITY
    STRUCTURAL_CONDITION_RATIO = MAX_DURABILITY / BASE_MAX_DURABILITY
    EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)

NORMAL = EFFECTIVE_DURABILITY_RATIO == 1.00
MINOR = 0.50 < EFFECTIVE_DURABILITY_RATIO < 1.00
MAJOR = 0 < EFFECTIVE_DURABILITY_RATIO <= 0.50
```

Reference `BASE_MAX = 5`:

| CURRENT/MAX/BASE_MAX | Effective ratio | Derived state | Meaning |
|---|---:|---|---|
| `5/5/5` | 1.00 | `NORMAL` | pristine |
| `4/5/5` | 0.80 | `MINOR` | current damage |
| `3/5/5` | 0.60 | `MINOR` | current damage |
| `2/5/5` | 0.40 | `MAJOR` | severe current damage |
| `1/5/5` | 0.20 | `MAJOR` | severe current damage |
| `4/4/5` | 0.80 | `MINOR` | fully repaired but permanent MAX scar remains |
| `2/2/5` | 0.40 | `MAJOR` | fully repaired but severe structural scar remains |
| `1/1/5` | 0.20 | `MAJOR` | floor-level structural life remains |
| `0/5/5` | 0.00 | `DESTROYED` | physical UID terminal |

Compatibility anchors required by tests/docs:

```text
4/4 with BASE_MAX 5 = MINOR
2/2 with BASE_MAX 5 = MAJOR
```

`DESTROYED` is terminal for the physical UID. History/archive/successor principles remain current; destroyed items cannot be repaired back into the same physical UID.

## 4. Damage event under Decision29

The old state-step resolver is superseded for current planning.

```text
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
DAMAGE_EVENT_CURRENT_LOSS = 1
```

`DAMAGE_EVENT_CURRENT_LOSS = 1` is a `TEMP_TEST_BUDGET`, not final product balance. A damage event reduces `CURRENT_DURABILITY` by one, floored at zero. The derived state is recalculated afterward from the numeric authority.

Decision28 still owns the target-level base conditional probability of an enhancement-failure damage event:

```text
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
+11  = 5%
+30  = 6%
+60  = 7%
+90  = 8%
+100 = 10%
INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
```

Decision29 does **not** replace these anchors. It applies one temporary modifier selected from the derived effective durability state.

## 5. Low effective durability enhancement modifiers · temporary Budget

The structural relationship is user-approved; the exact values below are delegated temporary tuning numbers.

| Derived state | Success delta | New enhancement effect | Decision28 damage-risk multiplier |
|---|---:|---:|---:|
| `NORMAL` | `0pp` | `100%` | `×1.00` |
| `MINOR` | `-3pp` | `90%` | `×1.25` |
| `MAJOR` | `-7pp` | `75%` | `×1.75` |

```text
TEMP_TEST_BUDGET = TRUE
FINAL_PRODUCT_BALANCE = NOT_APPROVED
```

The state is derived from `EFFECTIVE_DURABILITY_RATIO`, so both short-term CURRENT loss and permanent MAX scar can keep an item in MINOR/MAJOR. They do not stack as separate penalties.

### 5.1 Success probability

```text
if HARD_GUARANTEE_ACTIVE:
    FINAL_SUCCESS = 100%
else:
    FINAL_SUCCESS = existing_success_and_recovery_result + durability_success_delta_pp
```

Existing recovery soft-cap/hard-guarantee safety remains separate. A hard guarantee stays a real guarantee and is not secretly cancelled by durability.

### 5.2 Enhancement effect

```text
SUCCESS_LEVEL_DELTA = +1  # unchanged
NEW_ENHANCEMENT_EFFECT_ONLY *= durability_new_effect_multiplier
EXISTING_ITEM_STATS = unchanged by this multiplier
ITEM_KEYWORD_CARDINALITY / +10 CREATION_GATE = unchanged
```

A damaged/scarred item can still succeed and gains exactly one enhancement level. Durability only reduces the newly added ordinary enhancement effect magnitude under this temporary Budget; it does not retroactively erase existing power or change +10 keyword count.

### 5.3 Damage risk

```text
P(FINAL_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET, EFFECTIVE_STATE)
= Decision28_base_probability(TARGET)
* durability_damage_risk_multiplier(EFFECTIVE_STATE)
```

Examples:

| Target | NORMAL | MINOR | MAJOR |
|---:|---:|---:|---:|
| +11 | 5.00% | 6.25% | 8.75% |
| +30 | 6.00% | 7.50% | 10.50% |
| +60 | 7.00% | 8.75% | 12.25% |
| +90 | 8.00% | 10.00% | 14.00% |
| +100 | 10.00% | 12.50% | 17.50% |

These remain conditional on enhancement failure. They are not unconditional per-attempt percentages.

## 6. MAJOR enhancement eligibility

```text
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
DESTROYED_ENHANCEMENT_ELIGIBILITY = FALSE
```

A MAJOR item may still be pushed. This deliberately preserves the player's risky choice instead of turning repair into a mandatory gate. The cost of pushing is lower success chance, lower new-effect quality, higher damage-event probability, and shorter remaining CURRENT buffer. A structurally scarred full item can also remain MAJOR if `MAX/BASE_MAX <= 50%`.

## 7. Repair resolution

Repair is available only while the physical item still exists and CURRENT is below MAX.

```text
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY
DESTROYED_REPAIR_ALLOWED = FALSE
FULL_DURABILITY_REPAIR_ALLOWED = FALSE
```

A repair resolves two related outputs:

1. CURRENT recovery quality;
2. probability of a permanent `MAX_DURABILITY - 1` structural scar.

The player should see both the expected recovery band and structural-scar risk before confirmation. Hidden MAX loss is forbidden.

A fully repaired but already scarred item (`CURRENT == MAX < BASE_MAX`) cannot spam repair to reroll MAX because full-durability repair is not eligible and MAX recovery is not approved.

## 8. Repair quality · temporary Budget

First tuning table:

| Result | Probability | Target CURRENT ratio after repair |
|---|---:|---:|
| `EXCELLENT` | 20% | 100% of post-scar MAX |
| `STANDARD` | 60% | 75% of post-scar MAX |
| `POOR` | 20% | 50% of post-scar MAX |

```text
REPAIR_QUALITY = TEMP_TEST_BUDGET
REPAIR_MINIMUM_CURRENT_GAIN_WHEN_POSSIBLE = 1
```

Resolution after the optional MAX scar:

```text
quality_target = ceil(POST_SCAR_MAX * quality_ratio)
NEW_CURRENT = min(POST_SCAR_MAX, max(min(OLD_CURRENT + 1, POST_SCAR_MAX), quality_target))
```

This prevents a repair from randomly doing zero healing when recovery space remains. If a MAX scar lowers the new MAX to old CURRENT, the item can become full at the lower structural ceiling — but its derived state still reflects `MAX/BASE_MAX`.

Exact quality odds may later incorporate blacksmith skill/tools/material condition. They are intentionally not final here.

## 9. Probabilistic MAX structural scar · temporary Budget

`MAX_DURABILITY` does not drop on every repair. A repair job exposes structural-scar chance based on **pre-repair effective damage state + current enhancement level band**.

### 9.1 Enhancement bands for repair scar risk

```text
PLUS_0_10   = enhancement +0..+10
PLUS_11_30  = +11..+30
PLUS_31_60  = +31..+60
PLUS_61_90  = +61..+90
PLUS_91_100 = +91..+100
```

### 9.2 First temporary probability table

| Pre-repair state | +0~10 | +11~30 | +31~60 | +61~90 | +91~100 |
|---|---:|---:|---:|---:|---:|
| `MINOR` | 10% | 15% | 20% | 25% | 30% |
| `MAJOR` | 25% | 30% | 35% | 40% | 45% |

```text
MAX_SCAR_AMOUNT_ON_TRIGGER = -1
MAX_DURABILITY_FLOOR = 1
MAX_SCAR_CHANCE = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

When `MAX_DURABILITY == 1`, structural-scar probability is forced to zero because repair cannot reduce MAX below the floor. Physical destruction remains `CURRENT_DURABILITY == 0`, not repair reducing MAX to zero.

The exact table is deliberately temporary. The approved structural rule is that worse effective state and higher enhancement band must not make repair scar risk lower.

## 10. Reference examples

### 10.1 User example · scar triggers

```text
BASE_MAX = 5
CURRENT/MAX = 1/5  # effective MAJOR
repair at a band whose structural-scar roll triggers
MAX 5 -> 4
```

Then repair quality resolves against `POST_SCAR_MAX = 4`:

```text
EXCELLENT -> 4/4
STANDARD  -> 3/4
POOR      -> 2/4
```

The important follow-up is that `4/4/5` is **not pristine**:

```text
CURRENT_CONDITION_RATIO = 4/4 = 1.00
STRUCTURAL_CONDITION_RATIO = 4/5 = 0.80
EFFECTIVE_DURABILITY_RATIO = 0.80
4/4 with BASE_MAX 5 = MINOR
```

So MAX scar remains a real future enhancement penalty even after excellent repair.

### 10.2 Repair without scar

```text
1/5 MAJOR
MAX scar roll does not trigger
EXCELLENT -> 5/5/5 = NORMAL
STANDARD  -> 4/5/5 = MINOR
POOR      -> 3/5/5 = MINOR
```

### 10.3 Deep structural scar

```text
CURRENT/MAX/BASE_MAX = 2/2/5
CURRENT_CONDITION_RATIO = 1.00
STRUCTURAL_CONDITION_RATIO = 0.40
EFFECTIVE_DURABILITY_RATIO = 0.40
2/2 with BASE_MAX 5 = MAJOR
```

A heavily scarred item can be fully repaired and still remain a risky MAJOR workpiece. This is intentional.

## 11. Repair economy boundary

Decision29 closes structural repair behavior and MAJOR enhancement eligibility. It does not silently restore old CURRENT/MAX repair-price formulas.

```text
REPAIR_GOLD_COST = NOT_FINAL / FOLLOWUP_REBASE_REQUIRED
REPAIR_MATERIAL_COST = NOT_FINAL / FOLLOWUP_REBASE_REQUIRED
MAX_DURABILITY_RECOVERY = NOT_APPROVED
OLD_MAX_OVERHAUL_PLUS15_CAP60 = SUPERSEDED / HISTORICAL_ONLY
```

A later economy pass must test whether repair cost + scar risk makes repair neither an automatic answer nor a trap.

## 12. Benchmark disposition · fresh 2026-08-26

### Stars Reach — ADAPT

Official update text states repair has a chance to reduce maximum durability and that chance rises with damage/wear and lower current max durability.

ADAPT:
- probabilistic permanent repair scar;
- condition influences scar risk;
- max-durability loss remains meaningful after repair;
- warn players before high-risk repair.

REJECT:
- copying its exact durability-loss values/probability.

Source: `https://starsreach.com/home/?query-8-page=3`

### Black Desert — ADAPT / REJECT NUMERIC IMPORT

Official Black Desert guides separate current durability from maximum durability, document maximum-durability loss from enhancement, and provide explicit maximum-durability recovery systems.

ADAPT:
- visible current/max distinction;
- structural durability matters to item lifecycle.

REJECT:
- importing its exact durability scale or same-item/Memory Fragment recovery economy;
- making repeat MAX recovery a default Blacksmith maintenance loop;
- importing exact low-max enhancement rules.

Sources:
- `https://www.kr.playblackdesert.com/ko-KR/Wiki?wikiNo=20`
- `https://www.kr.playblackdesert.com/ko-KR/Wiki?wikiNo=234`

### FINAL FANTASY XIV — REFERENCE / REJECT

Official FFXIV repair guidance emphasizes highly accessible repair and self-repair can restore +100 durability up to 199%.

ADAPT:
- repair state should be visible and understandable;
- avoid needless multi-click maintenance friction.

REJECT:
- over-repair/full reversibility as Blacksmith's structural-scar baseline because it erases the intended lifetime tension of a specific UID workpiece.

Source: `https://na.finalfantasyxiv.com/uiguide/equipment/equipment-repair/equipment_repair_myself.html`

## 13. Adversarial review

### Loop 1 — Is numeric durability a hidden second authority?

No. Decision29 makes `CURRENT/MAX/BASE_MAX` visible and mechanically authoritative. State labels are derived only. No independent state transition table may override the numbers.

### Loop 2 — Did MAX scar become cosmetic after a perfect repair?

Initial candidate failed this attack: `4/4` would have returned to NORMAL if only `CURRENT/MAX` were used. Refined model uses `min(CURRENT/MAX, MAX/BASE_MAX)`, so `4/4/5 = MINOR` and `2/2/5 = MAJOR`. MAX scars remain mechanically meaningful without adding a second penalty stack.

### Loop 3 — Are low-durability penalties triple-punishing the same fact?

The three modifiers serve different questions: success chance = whether push works, new-effect multiplier = quality of new gain, damage multiplier = risk of worsening life. They all come from **one effective state**, not separate current/scar penalties. Initial values are modest and temporary.

### Loop 4 — Does repair become mandatory?

No. `MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES`. Player can repair, push damaged/scarred, or stop/handoff. Repair itself has structural-scar risk.

### Loop 5 — Can repair destroy the physical UID or reroll MAX recovery?

No under this model. MAX cannot fall below 1, destroyed repair is forbidden, full-durability repair is ineligible, and MAX recovery is not approved. Physical destruction remains `CURRENT == 0` from a damage event.

### Loop 6 — Does Decision29 silently replace Decision28 probability authority?

No. Decision28 remains target-level base conditional curve. Decision29 provides one temporary multiplier from effective durability state. UI rounding remains unresolved and cannot change resolver odds.

### Loop 7 — Does temporary tuning masquerade as final balance?

No. Success penalties, effect multipliers, damage multipliers, repair quality odds, `DAMAGE_EVENT_CURRENT_LOSS=1`, and MAX-scar table are all `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`; simulation and human playtest are required before final balance.

## 14. Evidence ceiling and next gates

```text
PLANNING_STRUCTURE = USER_APPROVED
TEMP_DURABILITY_TUNING = USER_DELEGATED_TEST_BUDGET / NOT_FINAL
RUNTIME_IMPLEMENTATION = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_DEVICE = NOT_RUN
ACCESSIBILITY = NOT_RUN
PERFORMANCE = NOT_RUN
REPAIR_ECONOMY = USER_APPROVED_TEST_CONTRACT / BS-REPAIR-20260826-31
CUSTOMER_EVENT_DAMAGE_POLICY = USER_APPROVED_POLICY / BS-DAMAGE-20260826-30
FAILURE_CONSEQUENCE_COMPOSITION = USER_APPROVED_EXCLUSIVE_HOLD_OR_DAMAGE / BS-ENHANCE-20260826-32
UI_DAMAGE_PERCENT_ROUNDING = USER_APPROVED_FINAL_OUTCOME_ONE_DECIMAL_HALF_UP / BS-ENHANCE-20260826-32
```

Next safe planning work after synchronization:

```text
1. REPAIR_ECONOMY_HUMAN_PLAYTEST + MUTABLE_R_BAND_BASELINE_REVIEW
2. ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS
3. full planning adversarial review
4. explicit user planning-complete declaration
5. runtime TDD migration
```
