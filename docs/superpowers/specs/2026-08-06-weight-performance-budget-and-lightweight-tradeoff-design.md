# Weight Performance Budget and Lightweight Trade-off Design

- Decision ID: `BS-ITEM-20260806-02`
- Approval status: `USER_APPROVED / R2_BATCH_005_6_OF_10 / APPROVED_PENDING_MERGE`
- Refines: `BS-ITEM-20260806-01 / BS-CRAFT-20260804-04 / BS-CUSTOMER-20260806-01`
- Product implementation: `BLOCKED`

## 1. Purpose

Equipment weight must not be a pure disadvantage. A heavier work can support more attack, defense, magical function, or utility capacity, while a lightweighting operation trades part of that capacity for broader customer usability.

```text
heavier structure
→ larger performance budget
→ higher Strength customer can use it without alteration

lightweighting work
→ lower final weight and lower performance budget
→ lower Strength customer can use it
```

Weight remains a supporting system. General enhancement success/failure and stop-or-push decisions remain the core progression loop.

## 2. Rejected alternatives

### Base-weight-only budget

Budget would remain unchanged after lightweighting. This makes lightweighting almost always optimal because it removes the assignment restriction without paying a performance cost. Rejected.

### Weight tiers

Separate bonus tables for light, medium, and heavy thresholds would create breakpoints, exception handling, and hidden optimization. Rejected.

### Direct automatic bonus to every stat

Adding weight-derived points simultaneously to attack, defense, magic, durability, and handling would multiply the same cause across several outputs. Rejected as double counting.

## 3. Adopted model

All current weights are multiples of five, so final weight converts linearly into one small budget source.

```text
EFFECTIVE_WEIGHT = max(0, BASE_WEIGHT + STRUCTURAL_WEIGHT_DELTA)
WEIGHT_PERFORMANCE_BUDGET = EFFECTIVE_WEIGHT / 5
TOTAL_PERFORMANCE_BUDGET = NON_WEIGHT_BASE_BUDGET + WEIGHT_PERFORMANCE_BUDGET
```

- `WEIGHT_PERFORMANCE_BUDGET` is an integer.
- Each `5 WEIGHT_POINT` contributes `+1 PERFORMANCE_BUDGET_POINT`.
- This contribution is included exactly once.
- The equipment-group preset must not secretly add a second heavy-item bonus.
- Weight budget does not multiply material, craftsmanship grade, artistry, catalyst, chronicle, or enhancement values.
- Weight budget does not directly change the generic customer event success forecast.

## 4. Current examples

| Equipment | Effective weight | Weight budget |
|---|---:|---:|
| Accessory | 0 | 0 |
| Tool or clothing | 5 | 1 |
| Sword, ranged weapon, light armor, shield/support | 10 | 2 |
| Axe or blunt weapon | 15 | 3 |
| Polearm or medium armor | 20 | 4 |
| Heavy armor | 30 | 6 |

A weighted treatment can raise a compatible item by one row step, and a lightweight treatment can lower it by one row step.

## 5. Budget lanes

Weight budget is capacity, not a direct bonus to every displayed stat. Each budget point is assigned to one item-compatible lane.

```text
ATTACK_BUDGET
DEFENSE_BUDGET
MAGIC_FUNCTION_BUDGET
UTILITY_BUDGET
```

Suggested compatibility:

| Equipment category | Allowed lanes |
|---|---|
| Weapon | `ATTACK_BUDGET / MAGIC_FUNCTION_BUDGET / UTILITY_BUDGET` |
| Armor | `DEFENSE_BUDGET / MAGIC_FUNCTION_BUDGET / UTILITY_BUDGET` |
| Shield or offhand | `DEFENSE_BUDGET / MAGIC_FUNCTION_BUDGET / UTILITY_BUDGET` |
| Tool | `MAGIC_FUNCTION_BUDGET / UTILITY_BUDGET` |
| Accessory | no weight-derived budget by default |

`MAGIC_FUNCTION_BUDGET` feeds approved magical or special-function outputs. It does not create a universal mana stat or automatically improve every magical property.

The exact conversion from one budget point to displayed attack, defense, magical-function, durability, handling, or special-function values remains a `BASELINE_TEST_PRESET`. The preview must show the exact resulting stat changes before the operation.

## 6. Structural weight treatment ownership

`LIGHTWEIGHT / NONE / WEIGHTED` belongs to the **precision-enhancement method**, not the catalyst affix.

```text
LIGHTWEIGHT = -5 WEIGHT_POINT and -1 weight budget
NONE = 0
WEIGHTED = +5 WEIGHT_POINT and +1 weight budget
```

Reasons:

- Lightweighting is a deliberate smithing operation that reshapes the work.
- Catalyst remains responsible for `CATALYST_AFFIX` lineage, mutation, and specialized effects.
- No new affix slot is needed.
- The operation remains inside the enhancement-centered player loop.

One item has at most one active structural weight treatment. Repeating the same treatment does not stack. Reworking it replaces the current treatment and recalculates budget from the new effective weight.

## 7. Allocation and rework

When weight changes, the budget difference must be explicitly allocated or removed from compatible lanes.

```text
NONE → WEIGHTED
weight +5 / budget +1
player assigns +1 to one compatible lane

NONE → LIGHTWEIGHT
weight -5 / budget -1
player selects one compatible lane that can lose 1

WEIGHTED → LIGHTWEIGHT
weight -10 / budget -2
player removes a total of 2 from compatible lanes
```

- A lane cannot fall below zero.
- The operation is unavailable when the required budget cannot be removed legally.
- Before execution, display final weight, customer assignment change, and exact stat changes.
- Rework replaces the structural state; it does not add historical budget deltas.
- Repeated switching cannot create net budget or duplicate stat gains.

## 8. Player-facing examples

### Heavy polearm

```text
장병기 기본 중량 20
중량 성능 예산 4
배분: 공격 3 / 유틸리티 1
근력 2 고객 최대 중량 20 → 사용 가능
```

### Lightweight polearm

```text
경량화 -5
최종 중량 15
중량 성능 예산 3
배분 조정: 공격 2 / 유틸리티 1
근력 2 고객 최대 중량 20 → 사용 가능
근력 1 고객 최대 중량 10 → 사용 불가
```

### Weighted sword

```text
검 기본 중량 10
중량화 +5
최종 중량 15
중량 성능 예산 3
추가 예산 +1을 공격 또는 마법 기능 등에 배분
근력 1 고객 최대 중량 10 → 사용 불가
근력 2 고객 최대 중량 20 → 사용 가능
```

## 9. Core-fun protection

```text
강화 성공·실패와 멈춤 판단
→ 작품 성능 방향과 구조 중량 선택
→ 적합한 고객에게 배정
→ 사건과 같은 UID 작품의 생애 환류
→ 다음 강화·복원·제작 판단
```

- Heavy equipment is not automatically superior because it restricts eligible customers.
- Lightweight equipment is not automatically superior because it gives up budget.
- Customer Strength becomes a meaningful matching axis without becoming a customer-RPG progression system.
- General enhancement level remains separate and does not automatically change weight.
- Weight budget affects item performance only through explicit allocation, not generic event success.

## 10. Benchmark interpretation

D&D 2024 equipment rules pair heavier armor with stronger protection and Strength requirements. Blacksmith adopts the readable benefit-versus-user-requirement relationship, but rejects movement, stealth, and spellcasting penalty layers.

- Adopt: heavier equipment can provide stronger protection or capability.
- Adapt: use one binary Strength load gate and one linear budget source.
- Reject: speed, accuracy, fatigue, stealth, and casting penalties.
- Source: https://www.dndbeyond.com/sources/dnd/br-2024/equipment

## 11. Adversarial review

### Mandatory lightweighting risk

If lightweighting preserves the original weight budget, it becomes a dominant no-cost choice. Prevented by deriving budget from effective weight.

### Heavy stacking risk

If the heavy equipment preset and weight formula both grant performance, the same cause is counted twice. Prevented by one explicit `WEIGHT_PERFORMANCE_BUDGET` component.

### Universal-stat inflation risk

If one weight point improves all stats, heavy items scale multiplicatively. Prevented by lane allocation: one budget point goes to one compatible lane.

### Rework farming risk

If each rework adds a historical bonus, players can alternate lightweight and weighted treatments to farm stats. Prevented by derived-state recalculation and replacement semantics.

### Accessory exploit risk

Weight-zero accessories could gain cheap power by becoming weighted while avoiding the intended equipment structure. Accessories are excluded from weight-derived budget and structural weight treatments by default.

### Enhancement displacement risk

Weight can become the main optimization system if its contribution is multiplied by grade or enhancement. Prevented by a small linear contribution, no multipliers, and no generic success-rate effect.

Adversarial result: `P0 0 / P1 0`.

## 12. Implementation boundary

- Update planning canon, registry, authority entry points, tests, audits, PR evidence, and Google Sheet only.
- Do not modify runtime, scenes, assets, images, or `data/crafting/weapon_bases.json`.
- Exact stat-conversion values and human balance testing remain `NOT_RUN / BASELINE_TEST_PRESET`.
- Product implementation remains `BLOCKED`.
