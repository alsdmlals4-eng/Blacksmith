# BS-REPAIR-20260826-29 · Durability / Repair / Structural Scar Model

- Date: `2026-08-26 KST`
- User approval: `수리는 현재/최대 내구도 수치로 운용하고, 낮은 내구도는 강화 성공률·새 강화효과·파손 위험에 불리하게 작용하며, 수리 결과와 MAX 손실은 확률 판정으로 처리. 세부 확률은 임시 권장안으로 진행.`
- Status: `USER_APPROVED_STRUCTURAL_CANON / TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Parent: `BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28`
- Work Mode: `PLAN`
- Product runtime: `NOT_RUN / BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. Decision purpose

Decision26의 핵심 의도였던 "숨은 두 번째 내구도 권위 금지"는 유지한다. 다만 사용자의 최신 승인에 따라 **숫자 내구도 자체를 다시 보이는 단일 gameplay authority로 채택**한다.

```text
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
NO_HIDDEN_SECOND_DURABILITY_AUTHORITY = TRUE
```

`NORMAL / MINOR / MAJOR / DESTROYED`는 별도 상태머신이 아니라 숫자 내구도에서 파생되는 사람이 읽기 쉬운 상태명이다. 따라서 Decision26의 `CURRENT_MAX_AUTHORITY = SUPERSEDED`와 `ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE`는 최신 Decision29와 충돌하는 필드에서 부분 대체된다.

## 2. Numeric durability authority

```text
BASE_MAX_DURABILITY
= 작품이 태어날 때의 원래 최대 내구도
= immutable provenance value

MAX_DURABILITY
= 현재 작품이 회복할 수 있는 최대 내구도

CURRENT_DURABILITY
= 현재 남은 내구도

0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
```

Reference item only:

```text
REFERENCE_BASE_MAX_DURABILITY = 5
```

`5`는 사용자가 든 대표 예시와 첫 테스트 Budget을 위한 기준값이며 모든 아이템 family의 출시 고정값을 뜻하지 않는다. 재료/아이템 family별 birth durability 차이는 별도 데이터 Decision이 필요하다.

`BASE_MAX_DURABILITY - MAX_DURABILITY`는 작품에 남은 구조 흉터를 설명하는 provenance 값이며 별도 숨은 전투 페널티 축으로 중복 사용하지 않는다.

## 3. Derived damage states

```text
NORMAL = CURRENT_DURABILITY == MAX_DURABILITY
MINOR = 0.50 < CURRENT_DURABILITY / MAX_DURABILITY < 1.00
MAJOR = 0 < CURRENT_DURABILITY / MAX_DURABILITY <= 0.50
DESTROYED = CURRENT_DURABILITY == 0
```

Reference `MAX=5`:

| CURRENT/MAX | Derived state |
|---|---|
| `5/5` | `NORMAL` |
| `4/5`, `3/5` | `MINOR` |
| `2/5`, `1/5` | `MAJOR` |
| `0/5` | `DESTROYED` |

`DESTROYED` is terminal for the physical UID. History/archive/successor principles remain current; destroyed items cannot be repaired back into the same physical UID.

## 4. Damage event under Decision29

The old state-step resolver is superseded for current planning.

```text
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
DAMAGE_EVENT_CURRENT_LOSS = 1
```

`DAMAGE_EVENT_CURRENT_LOSS = 1` is a `TEMP_TEST_BUDGET`, not final product balance. A damage event reduces `CURRENT_DURABILITY` by one, floored at zero. The resulting player-facing state is then derived from the new `CURRENT/MAX` ratio.

Decision28 still owns the base conditional probability of an enhancement-failure damage event:

```text
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
+11  = 5%
+30  = 6%
+60  = 7%
+90  = 8%
+100 = 10%
INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
```

Decision29 does **not** replace these anchors. It applies a temporary current-durability multiplier after the Decision28 target curve is resolved.

## 5. Low durability enhancement modifiers · temporary Budget

The structure is user-approved; the exact values below are delegated temporary tuning numbers.

| Derived state | Success delta | New enhancement effect | Decision28 damage-risk multiplier |
|---|---:|---:|---:|
| `NORMAL` | `0pp` | `100%` | `×1.00` |
| `MINOR` | `-3pp` | `90%` | `×1.25` |
| `MAJOR` | `-7pp` | `75%` | `×1.75` |

```text
TEMP_TEST_BUDGET = TRUE
FINAL_PRODUCT_BALANCE = NOT_APPROVED
```

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

A damaged item can still succeed and gains exactly one enhancement level. Durability only reduces the newly added ordinary enhancement effect magnitude under this temporary Budget; it does not retroactively erase existing power or change the +10 keyword count.

### 5.3 Damage risk

```text
P(FINAL_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET, STATE)
= Decision28_base_probability(TARGET)
* durability_damage_risk_multiplier(STATE)
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

A MAJOR item may still be pushed. This deliberately preserves the player's risky choice instead of turning repair into a mandatory gate. The cost of pushing is the lower success chance, lower new-effect quality, higher damage-event probability, and shorter remaining durability buffer.

## 7. Repair resolution

Repair is available only while the physical item still exists.

```text
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY
DESTROYED_REPAIR_ALLOWED = FALSE
FULL_DURABILITY_REPAIR_ALLOWED = FALSE
```

A repair resolves two related but distinct outputs:

1. CURRENT recovery quality;
2. probability of a permanent `MAX_DURABILITY - 1` structural scar.

The player should see both the expected recovery band and the structural-scar risk before confirmation. Hidden MAX loss is forbidden.

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

This prevents a repair from randomly doing zero healing when there is still room to recover. If a MAX scar itself lowers the new MAX to the old CURRENT, the item can become full at the lower structural ceiling.

Exact quality odds may later incorporate blacksmith skill/tools/material condition. They are intentionally not final here.

## 9. Probabilistic MAX structural scar · temporary Budget

`MAX_DURABILITY` does not drop on every repair. A successful repair job independently exposes a structural-scar chance based on **pre-repair damage state + current enhancement level band**.

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

When `MAX_DURABILITY == 1`, structural-scar probability is forced to zero because repair cannot reduce MAX below the approved floor. Physical destruction remains owned by `CURRENT_DURABILITY == 0`, not by a repair reducing MAX to zero.

The exact table is deliberately temporary. The approved structural rule is only that worse damage state and higher enhancement level must not make repair scar risk lower.

## 10. Reference examples

### 10.1 User example

```text
BASE_MAX = 5
CURRENT/MAX = 1/5  # MAJOR
repair at a band whose structural-scar roll triggers
MAX 5 -> 4
```

Then repair quality resolves against `POST_SCAR_MAX = 4`:

```text
EXCELLENT -> 4/4
STANDARD  -> 3/4
POOR      -> 2/4
```

This preserves the user's intended `1/5 -> repair -> possible 4/4` outcome without making `MAX -1` automatic on every repair.

### 10.2 Repair without scar

```text
1/5 MAJOR
MAX scar roll does not trigger
EXCELLENT -> 5/5
STANDARD  -> 4/5
POOR      -> 3/5
```

## 11. Repair economy boundary

This Decision closes the **structural repair behavior and MAJOR enhancement eligibility** gate. It does not silently restore old CURRENT/MAX repair-price formulas.

```text
REPAIR_GOLD_COST = NOT_FINAL / FOLLOWUP_REBASE_REQUIRED
REPAIR_MATERIAL_COST = NOT_FINAL / FOLLOWUP_REBASE_REQUIRED
MAX_DURABILITY_RECOVERY = NOT_APPROVED
OLD_MAX_OVERHAUL_PLUS15_CAP60 = SUPERSEDED / HISTORICAL_ONLY
```

The historical repair-cost documents remain comparison evidence only. A later economy pass must test whether repair cost plus probabilistic structural scar makes repair neither an automatic answer nor a trap.

## 12. Benchmark disposition · fresh 2026-08-26

### Stars Reach — ADAPT

Official update text states that repair has a chance to reduce maximum durability and that this chance rises with damage/wear and lower current max durability.

ADAPT:
- probabilistic permanent repair scar;
- damage condition influences scar risk;
- warn players before broken state.

REJECT:
- copy its exact `10%` max-durability reduction amount/probability.

Source: `https://starsreach.com/home/?query-8-page=3`

### Black Desert — ADAPT / REJECT NUMERIC IMPORT

Official Black Desert guides separate current durability from maximum durability, document maximum-durability loss from enhancement, and provide explicit maximum-durability recovery systems.

ADAPT:
- visible current/max durability distinction;
- structural durability matters to enhancement lifecycle.

REJECT:
- importing its exact durability scale or same-item/Memory Fragment recovery economy;
- making repeat MAX recovery a default Blacksmith maintenance loop;
- silently locking MAJOR enhancement merely because another game has a low-max enhancement gate.

Sources:
- `https://www.kr.playblackdesert.com/ko-KR/Wiki?wikiNo=20`
- `https://www.kr.playblackdesert.com/ko-KR/Wiki?wikiNo=234`

### FINAL FANTASY XIV — REFERENCE / REJECT

Official FFXIV repair guidance emphasizes highly accessible repair and self-repair can restore +100 durability up to 199%.

ADAPT:
- repair state should be visible and understandable;
- avoid needless multi-click maintenance friction.

REJECT:
- over-repair/full reversibility as Blacksmith's structural-scar baseline, because it erases the intended lifetime tension of a specific UID workpiece.

Source: `https://na.finalfantasyxiv.com/uiguide/equipment/equipment-repair/equipment_repair_myself.html`

## 13. Adversarial review

### Loop 1 — Is numeric durability a hidden second authority?

No. Decision29 makes `CURRENT/MAX/BASE_MAX` visible and mechanically authoritative; state labels are derived only. No independent state transition table may override the numbers.

### Loop 2 — Are low-durability penalties triple-punishing the same fact?

The three penalties serve different player questions: success chance = whether the push works, new-effect multiplier = quality of the new gain, damage multiplier = risk of worsening the item's life. Initial values are intentionally modest and temporary. `MAX/BASE_MAX` does not add a fourth hidden success/effect penalty.

### Loop 3 — Does repair become mandatory?

No. `MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES`. The player can repair, push damaged, or stop/handoff. Repair itself has structural-scar risk, so it is not an automatic dominant action.

### Loop 4 — Can repair itself destroy the physical UID?

No under this first model. MAX cannot fall below 1 and destroyed repair is forbidden. Physical destruction is still `CURRENT == 0` from an actual damage event.

### Loop 5 — Does Decision29 silently replace Decision28 probability authority?

No. Decision28 remains the target-level base conditional curve. Decision29 provides a temporary multiplicative state modifier. UI rounding remains unresolved and cannot change resolver odds.

### Loop 6 — Does temporary tuning masquerade as final balance?

No. Success penalties, effect multipliers, damage multipliers, repair quality probabilities, `DAMAGE_EVENT_CURRENT_LOSS=1`, and repair MAX-scar table are all explicitly `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`. They require simulation and human playtest before final balance.

## 14. Evidence ceiling and next gates

```text
PLANNING_STRUCTURE = USER_APPROVED
TEMP_DURABILITY_TUNING = USER_DELEGATED_TEST_BUDGET / NOT_FINAL
RUNTIME_IMPLEMENTATION = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_DEVICE = NOT_RUN
ACCESSIBILITY = NOT_RUN
PERFORMANCE = NOT_RUN
REPAIR_ECONOMY = NOT_FINAL
CUSTOMER_EVENT_DAMAGE_POLICY = NOT_FINAL
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
```

Next safe planning work after synchronization:

```text
1. CUSTOMER_WORLD_EVENT_DAMAGE_POLICY
2. REPAIR_ECONOMY_REBASE + durability/economy sensitivity simulation
3. FAILURE_CONSEQUENCE_COMPOSITION + UI rounding if needed
4. REPRESENTATIVE_VISUAL_REGENERATION_AFTER_SYSTEM_SYNC
5. full planning adversarial review
6. explicit user planning-complete declaration
7. runtime TDD migration
```
