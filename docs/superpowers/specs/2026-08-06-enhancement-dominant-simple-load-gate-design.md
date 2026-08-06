# Enhancement-Dominant Simple Load Gate Design

- Decision: `BS-CUSTOMER-20260806-01`
- Status: `USER_APPROVED / R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE`
- Refines: `BS-CUSTOMER-20260805-01 / BS-UX-20260805-01 / BS-CUSTOMER-20260803-02`
- Product implementation: `BLOCKED`

## Goal

Keep enhancement as Blacksmith's main decision system while reducing customer and equipment compatibility to a small, readable support rule.

## Adopted approach

Use a binary maximum-load gate.

```text
MAXIMUM_LOAD = STRENGTH × 10 WEIGHT_POINT
TOTAL_WEIGHT ≤ MAXIMUM_LOAD → WITHIN_LIMIT
TOTAL_WEIGHT > MAXIMUM_LOAD → OVERWEIGHT / assignment blocked
```

Within the limit there is no weight bonus, exact-match bonus, stamina drain, handling penalty, or hidden efficiency tier. Constitution and dexterity do not alter maximum load.

### Rejected alternatives

- Tiered overload penalties: rejected because they add secondary optimization and explanation cost.
- Four balance states (`UNSUITABLE / UNSTABLE / STABLE / SKILLED`): superseded for load handling.
- Removing weight completely: rejected because strength still needs a clear equipment-use role.

## Enhancement-dominant success preset

The internal baseline forecast is intentionally small and linear.

```text
risk_base = clamp(100 - event_risk × 10, 5, 90)
final_success = clamp(
  risk_base
  + enhancement_level
  + relevant_stat_bonus
  + proficiency_bonus,
  5,
  95
)
```

- Enhancement level: `+1 level = +1 percentage point`.
- Relevant customer stat: if the relevant stat is at least the event risk, `+5 percentage points`; otherwise `0`.
- Proficiency `0 / 1 / 2 / 3`: `-10 / 0 / +5 / +10 percentage points`.
- Player display remains rounded to the nearest `10%`, with a `5~95%` display range.
- Raw item `ATTACK / DEFENSE / HANDLING / ARTISTRY` do not feed the general customer-success formula. They retain their item identity, sale, requirement, and content-specific roles.

This keeps enhancement as the largest controllable modifier. Customer stats and proficiency help choose a recipient but do not become a second main progression loop.

## Special functions

Special-function suitability becomes a requirement check rather than a general weighted score.

- If an event explicitly requires a special function, the customer must meet its approved activation requirements.
- Failing the required activation check blocks that assignment or marks the required function unavailable.
- If the event does not require the function, failure to activate it does not reduce the ordinary success forecast.

## Mobile disclosure

Replace `BALANCE_STATE` with `LOAD_STATUS`.

- Show `총 중량 / 최대 중량`, for example `32 / 50`.
- Show `사용 가능` for `WITHIN_LIMIT`.
- Show `중량 초과 · 배정 불가` for `OVERWEIGHT`.
- Do not show four load-quality tiers or percentage penalties.
- Success reasons prioritize enhancement level first, then the one relevant stat and relevant proficiency.

## Examples

### Load

- Strength `4` → maximum load `40`.
- Total weight `40` → usable, no bonus or penalty.
- Total weight `41` → assignment blocked.

### Forecast

Event risk `6`, item enhancement `+20`, relevant stat meets risk, proficiency `2`:

```text
risk_base 40 + enhancement 20 + stat 5 + proficiency 5 = 70%
```

The player sees approximately `70%`.

## Adversarial review

- Risk: enhancement may dominate easy events and hit the cap early.
  - Accepted. Easy events are not intended to justify deep customer-stat optimization.
- Risk: an overweight item becomes a hard block.
  - Accepted. A clear hard limit is simpler than hidden partial penalties and gives lightweight enhancement a readable purpose.
- Risk: proficiency and stat bonuses may feel small.
  - Intentional. They are supporting selection signals, not the main progression engine.
- Risk: existing four-state language may remain in authority documents or validators.
  - Required correction: mark the old load-state contract `HISTORICAL_SUPERSEDED` and route current UI to `LOAD_STATUS`.

## Testing boundary

The planning contract must verify:

- active batch `4/10` and Decision `BS-CUSTOMER-20260806-01`;
- `STRENGTH × 10` maximum load;
- `WITHIN_LIMIT / OVERWEIGHT` only;
- no escalating overload penalty or four-state load balance;
- enhancement `+1 level = +1%p`;
- small stat and proficiency modifiers;
- binary special-function requirement;
- current authority and mobile disclosure refinement;
- product implementation remains `BLOCKED`.
