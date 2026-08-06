# Weight Performance Budget and Lightweight Trade-off Design

- Decision ID: `BS-ITEM-20260806-02`
- Approval status: `USER_APPROVED / R2_BATCH_005_6_OF_10 / APPROVED_PENDING_MERGE`
- Refines: `BS-ITEM-20260806-01 / BS-CRAFT-20260804-04 / BS-CUSTOMER-20260806-01`
- Product implementation: `BLOCKED`

## 1. Purpose

Equipment weight must not be a pure disadvantage. A heavier work begins with more attack, defense, magical-function, or utility capacity. Later lightweighting lowers the weight customers must carry but does not erase performance budget already established in the work.

```text
initial crafting weight
→ initial performance budget is fixed

later lightweighting
→ current weight decreases
→ previously earned performance budget remains
→ lower-Strength customers become eligible

later weighting
→ current weight increases
→ new budget is gained only when a new highest budget-recognized weight is reached
```

Weight remains a supporting system. General enhancement success/failure and stop-or-push decisions remain the core progression loop.

## 2. Rejected alternatives

### Current-weight budget recalculation

Reducing budget whenever lightweighting lowers current weight contradicts the intended fantasy: the smith preserves the work's established performance while spending a rare precision-enhancement opportunity to make it easier to use. Rejected.

### Unconditional budget on every weighting action

Alternating lightweighting and weighting could repeatedly grant budget at the same weight. Rejected.

### Weight tiers

Separate bonus tables for light, medium, and heavy thresholds create breakpoints and hidden optimization. Rejected.

### Direct automatic bonus to every stat

Adding one weight-derived point simultaneously to attack, defense, magic, durability, and handling multiplies the same cause across several outputs. Rejected as double counting.

## 3. Adopted budget memory model

All current weights use five-point steps.

```text
INITIAL_WEIGHT = equipment-group base weight at first crafting completion
CURRENT_WEIGHT = max(0, INITIAL_WEIGHT + cumulative successful precision weight adjustments)
BUDGET_RECOGNIZED_WEIGHT = max(INITIAL_WEIGHT, highest successful CURRENT_WEIGHT ever reached by this UID)
WEIGHT_PERFORMANCE_BUDGET = BUDGET_RECOGNIZED_WEIGHT / 5
TOTAL_PERFORMANCE_BUDGET = NON_WEIGHT_BASE_BUDGET + WEIGHT_PERFORMANCE_BUDGET
```

- Each `5 WEIGHT_POINT` of `BUDGET_RECOGNIZED_WEIGHT` contributes `+1 PERFORMANCE_BUDGET_POINT`.
- Initial crafting weight grants the initial weight budget immediately.
- Decreasing `CURRENT_WEIGHT` never decreases `BUDGET_RECOGNIZED_WEIGHT` or already allocated budget.
- Increasing weight grants new budget only for the portion that exceeds the UID's previous `BUDGET_RECOGNIZED_WEIGHT`.
- Budget recognition is monotonic for the same UID.
- Current customer load checks use `CURRENT_WEIGHT`, never `BUDGET_RECOGNIZED_WEIGHT`.
- The contribution is counted exactly once.
- Equipment-group presets must not secretly add a second heavy-item bonus.
- Weight budget does not multiply material, craftsmanship grade, artistry, catalyst, chronicle, or general-enhancement values.
- Weight budget does not directly change the generic customer event success forecast.

## 4. Initial examples

| Equipment | Initial weight | Initial weight budget |
|---|---:|---:|
| Accessory | 0 | 0 |
| Tool or clothing | 5 | 1 |
| Sword, ranged weapon, light armor, shield/support | 10 | 2 |
| Axe or blunt weapon | 15 | 3 |
| Polearm or medium armor | 20 | 4 |
| Heavy armor | 30 | 6 |

## 5. Budget lanes

Weight budget is capacity, not a direct bonus to every displayed stat. Each budget point is allocated to one item-compatible lane.

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

The exact conversion from one budget point to displayed attack, defense, magical-function, durability, handling, or special-function values remains a `BASELINE_TEST_PRESET`. The preview must show exact resulting stat changes before the operation.

## 6. Precision-enhancement ownership and opportunity cost

Weight adjustment belongs to the **precision-enhancement method**, not the catalyst affix.

```text
precision milestones = +10 / +20 / +30 / +40 / +50
LIGHTWEIGHTING = CURRENT_WEIGHT -5 / existing budget preserved
WEIGHTING = CURRENT_WEIGHT +5 / budget added only above previous recognized peak
```

- A precision milestone can apply at most one weight adjustment.
- Adjustments from different precision milestones can accumulate.
- The same milestone cannot be replayed, refunded, or repeatedly switched for weight gain.
- Selecting lightweighting or weighting consumes that milestone's enhancement-method opportunity instead of attack, defense, magic, artistic, or other precision directions.
- Catalyst remains responsible for `CATALYST_AFFIX` lineage, mutation, and specialized effects.
- No new affix slot is created.

This opportunity cost is the primary balance constraint. Repeated lightweighting and weighting is allowed across later milestones, but it is normally inefficient because only five precision milestones exist.

## 7. Budget-gain rules

```text
old_peak = BUDGET_RECOGNIZED_WEIGHT
new_current = max(0, CURRENT_WEIGHT + WEIGHT_ADJUSTMENT)
new_peak = max(old_peak, new_current)
new_budget_gain = (new_peak - old_peak) / 5
```

### Lightweighting

```text
CURRENT_WEIGHT -5
BUDGET_RECOGNIZED_WEIGHT unchanged
WEIGHT_PERFORMANCE_BUDGET unchanged
```

Lightweighting never removes already allocated attack, defense, magical-function, or utility budget.

### Weighting below or at the old peak

```text
CURRENT_WEIGHT +5
new current weight <= old peak
new budget gain = 0
```

This prevents lightweighting–weighting loops from duplicating budget.

### Weighting above the old peak

```text
CURRENT_WEIGHT +5
new current weight > old peak
new budget gain = (new current weight - old peak) / 5
```

Each newly gained point is allocated to one compatible lane.

## 8. Player-facing examples

### Heavy polearm made lighter

```text
initial polearm weight 20
recognized weight 20
weight budget 4
allocation: attack 3 / utility 1

+10 precision: lightweighting
current weight 15
recognized weight 20
weight budget remains 4
lower-Strength customer eligibility improves
```

### Reversing the lightweighting

```text
+20 precision: weighting
current weight 20
old recognized weight 20
new budget gain 0
```

Returning to a previously reached weight does not duplicate budget.

### Reaching a new high

```text
+30 precision: weighting
current weight 25
old recognized weight 20
new recognized weight 25
new budget gain +1
```

### Repeated lightweighting

```text
initial heavy armor weight 30 / budget 6
+10 lightweighting → current 25 / budget 6
+20 lightweighting → current 20 / budget 6
```

The item keeps its established performance but spends two of only five precision-enhancement opportunities to broaden usability.

## 9. Core-fun protection

```text
강화 성공·실패와 멈춤 판단
→ 정밀강화 기회를 성능 강화 또는 중량 조정에 사용
→ 고객 최대 중량과 작품 성능을 함께 비교
→ 사건과 같은 UID 작품의 생애 환류
→ 다음 강화·복원·제작 판단
```

- Heavy equipment is not automatically superior because fewer customers can use it without later work.
- Lightweighting is valuable but not free because it consumes a rare precision milestone.
- Performance already forged into an item is not erased by later lightweighting.
- Weighting can add performance budget, but only by reaching a genuinely new weight peak.
- Customer Strength becomes a meaningful matching axis without becoming a customer-RPG progression system.
- General enhancement level remains separate and does not automatically change weight.
- Weight budget affects item performance only through explicit allocation, not generic event success.

## 10. Benchmark interpretation

D&D 2024 equipment rules pair heavier armor with stronger protection and Strength requirements. Blacksmith adopts the readable benefit-versus-user-requirement relationship, but rejects movement, stealth, and spellcasting penalty layers.

- Adopt: heavier equipment can begin with stronger protection or capability.
- Adapt: later smithing can reduce use weight without deleting already forged capacity.
- Reject: speed, accuracy, fatigue, stealth, and casting penalties.
- Source: https://www.dndbeyond.com/sources/dnd/br-2024/equipment

## 11. Adversarial review

### Budget-loss contradiction

If lightweighting deletes budget, the operation weakens the established item rather than representing skilled weight reduction. Prevented by monotonic budget recognition.

### Loop duplication

If every weighting grants budget, alternating adjustments farms power. Prevented by granting budget only above the UID's historical recognized-weight peak.

### Free optimization

If weight adjustment is available at any time, every item can become light without meaningful cost. Prevented by limiting adjustments to one selection per distinct `+10` precision milestone.

### Universal-stat inflation

If one budget point improves all stats, heavy items scale multiplicatively. Prevented by lane allocation: one budget point goes to one compatible lane.

### Hidden load mismatch

If customer load checks use recognized peak weight, lightweighting would not improve eligibility. Prevented by using `CURRENT_WEIGHT` for load and `BUDGET_RECOGNIZED_WEIGHT` only for performance budget.

### Accessory exploit

Weight-zero accessories could gain cheap power through weighting. Accessories are excluded from weight-derived budget and precision weight adjustment by default.

### Enhancement displacement

Weight can become the main optimization system if its contribution is multiplied by grade or enhancement. Prevented by a small linear contribution, no multipliers, limited milestones, and no generic success-rate effect.

Adversarial result: `P0 0 / P1 0`.

## 12. Implementation boundary

- Update planning canon, registry, authority entry points, tests, audits, PR evidence, and Google Sheet only.
- Do not modify runtime, scenes, assets, images, or `data/crafting/weapon_bases.json`.
- Exact stat-conversion values and human balance testing remain `NOT_RUN / BASELINE_TEST_PRESET`.
- Product implementation remains `BLOCKED`.
