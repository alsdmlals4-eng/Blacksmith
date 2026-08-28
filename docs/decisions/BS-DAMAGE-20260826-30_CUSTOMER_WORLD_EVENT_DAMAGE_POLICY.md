# BS-DAMAGE-20260826-30 · Customer / World Event Damage Policy

- Date: `2026-08-26 KST`
- User approval: `권장안 B 승인`
- Status: `USER_APPROVED_STRUCTURAL_CANON / TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Parent: `BS-LINK-20260824-24 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29`
- Work Mode: `IMPLEMENTATION_AND_REVIEW`
- Current execution: `CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826`
- Product runtime: `CURRENT_CANON_MVP_AUTHORIZED / EXACT_HEAD_CONTRACT_AND_TDD_REQUIRED`

## 1. Purpose

고객에게 작품을 인계한 뒤 세계에서 실제로 사용된 결과가 같은 UID의 작품 생애로 돌아오게 하되, 단순 소유·판매·일정 진행 자체가 내구도 세금이 되지 않도록 한다.

```text
PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE
ACTUAL_ITEM_USE_REQUIRED = TRUE
CUSTOMER_WORLD_EVENT_DAMAGE = EVENT_SPECIFIC_CAUSAL_RESULT_ONLY
MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1
```

손상은 임무의 성공/실패와 별도 축이다.

```text
MISSION_OUTCOME_AND_ITEM_DAMAGE = INDEPENDENT_AXES
```

성공적으로 귀환했더라도 실제 충격 때문에 작품이 손상될 수 있고, 임무가 실패했더라도 작품에 손상 원인이 없었다면 내구도는 그대로일 수 있다.

## 2. Eligibility gate

고객/세계 이벤트가 damage 후보가 되려면 모두 만족해야 한다.

```text
SAME_PHYSICAL_UID_PRESENT = TRUE
ACTUAL_ITEM_USE_REQUIRED = TRUE
EVENT_DAMAGE_PROFILE is authored
EVENT_CAUSAL_REASON is authored
```

다음은 손상 판정 자체를 만들지 않는다.

```text
purchase
handoff
ownership duration
mission turn-in
customer relation change
UI/menu interaction
schedule tick without actual use
```

이 규칙은 Stars Reach가 2026-08 실제 Early Access에서 mission turn-in/UI 같은 비사용 durability 호출을 제거한 사례와 같은 방향으로, **실제 사용 원인과 시스템 bookkeeping을 분리**한다.

## 3. Event damage profiles · temporary Budget

첫 시뮬레이션 Budget:

```text
NONE = 0%
LOW = 10%
MEDIUM = 20%
HIGH = 40%
DIRECT = 100%
```

상태:

```text
EVENT_DAMAGE_PROFILE_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

의미:

- `NONE`: 작품에 실제 손상 원인이 없는 이벤트.
- `LOW`: 통상보다 분명한 위험이 있지만 큰 충격은 아닌 실제 사용.
- `MEDIUM`: 작품이 눈에 띄는 충격/부하/환경 위험에 노출된 사용.
- `HIGH`: 강한 충격·극한 환경·위험한 사용이 사건의 중요한 원인인 경우.
- `DIRECT`: 콘텐츠가 작품에 직접 손상이 일어나는 사건을 명시한 경우. 확률형 위험을 숨겨 100%로 올리는 용도가 아니다.

프로필은 customer success score에서 자동 도출하지 않는다. content/event owner가 실제 사건 원인과 함께 명시한다.

## 4. Decision29 effective durability composition

`NONE/LOW/MEDIUM/HIGH` 중 확률형 프로필은 Decision29의 **기존 effective durability 상태**를 재사용한다.

```text
DURABILITY_MULTIPLIER_OWNER = BS-REPAIR-20260826-29

P(EVENT_DAMAGE | PROFILE, EFFECTIVE_STATE)
= min(
    PROBABILISTIC_DAMAGE_CAP,
    PROFILE_BASE_DAMAGE_PERCENT * Decision29_damage_risk_multiplier(EFFECTIVE_STATE)
  )

PROBABILISTIC_DAMAGE_CAP = 95%
```

Decision29 current temporary multipliers are read from its owner, not re-owned here:

```text
NORMAL x1.00
MINOR  x1.25
MAJOR  x1.75
```

Reference examples under the current temporary Decision29 modifiers:

| Profile | NORMAL | MINOR | MAJOR |
|---|---:|---:|---:|
| `LOW` | 10% | 12.5% | 17.5% |
| `MEDIUM` | 20% | 25% | 35% |
| `HIGH` | 40% | 50% | 70% |

`DIRECT = 100%` is deterministic and does not pass through the probabilistic 95% cap or durability multiplier.

This Decision does not create a second durability modifier table. If Decision29 temporary multipliers change, these derived examples must be recalculated from Decision29.

## 5. Damage resolution owner

If an event damage result triggers, Decision29 remains the mechanical durability resolver.

```text
DAMAGE_RESOLUTION_OWNER = BS-REPAIR-20260826-29
WORLD_EVENT_MAX_DURABILITY_DAMAGE = FALSE
```

Current Decision29 temporary damage amount is used:

```text
DAMAGE_EVENT_CURRENT_LOSS = 1 / TEMP_TEST_BUDGET
```

Therefore:

```text
triggered world event damage
-> CURRENT_DURABILITY decreases by Decision29 damage-event amount
-> EFFECTIVE_DURABILITY recalculated
-> NORMAL / MINOR / MAJOR / DESTROYED derived
```

World/customer events do **not** directly reduce `MAX_DURABILITY`. `MAX -1` structural scar remains owned by the Decision29 repair process.

## 6. One event, one UID, at most one damage roll

A delayed event may summarize several narrative beats, but one resolved event can expose the same physical UID to at most one damage roll.

```text
MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1
NO_PER_ATTACK_WORLD_EVENT_ROLL_SPAM
NO_PER_SCENE_MULTI_ROLL_FOR_SAME_RESOLVED_EVENT
```

If content genuinely needs multiple independent damaging incidents, they must be represented as separate resolved events with separate causal records rather than silently multiplying rolls inside one result.

## 7. Relevant protection / keyword interaction

A relevant item keyword or explicit function may mitigate a **probabilistic** event profile only when the event author declares the causal relation.

```text
EXPLICIT_RELEVANT_PROTECTION_PROFILE_SHIFT = ENABLED
MAX_PROFILE_SHIFT = -1 STEP
EVENT_SPECIFIC_RELEVANCE_REQUIRED = TRUE
UNIVERSAL_KEYWORD_DAMAGE_BONUS = FORBIDDEN
DIRECT_PROFILE_MITIGATED_BY_GENERIC_KEYWORD = FALSE
```

Example meaning only:

```text
ENVIRONMENTAL_TREATMENT
+ explicitly related corrosive/exposure event
-> HIGH may become MEDIUM
```

This is not a universal item-quality score and not a hidden customer bonus. Exact keyword-to-hazard mappings remain content-owned and require their own explicit data when authored.

## 8. Separation from customer outcome model

Decision24 customer outcome axes remain separate:

```text
EXPEDITION_RETURN_STATE
RECOVERY_STATE
ITEM_UID_LIFECYCLE_STATE
```

The historical/test-budget `ENHANCEMENT_EVENT_BONUS_PP` does not set damage probability.

```text
CUSTOMER_EVENT_SUCCESS_SCORE != ITEM_DAMAGE_PROBABILITY
NO_OPAQUE_COMBINED_FIT_DAMAGE_SCORE
NO_UNIVERSAL_CUSTOMER_DAMAGE_PERCENT
```

## 9. Player information

Before handoff/event:

- Do not add one universal damage percentage to every customer card.
- If a known event/hazard is disclosed, present qualitative risk and the causal reason in player-readable terms.
- Hidden risk may exist only when the fiction/content genuinely keeps the hazard unknown; resolver odds still come from authored event data, not AI improvisation.

After event resolution, if damage occurs, show:

```text
same item UID
actual event cause
before CURRENT/MAX/BASE_MAX or derived state
actual damage result
after CURRENT/MAX/BASE_MAX or derived state
primary next action
```

The Chronicle may record a meaningful world-event damage or destruction event under Decision27.

## 10. Destruction boundary

If Decision29 resolution moves `CURRENT_DURABILITY` to zero:

```text
ITEM_UID = DESTROYED
CUSTOMER_IDENTITY = PRESERVED
CUSTOMER_RELATION = PRESERVED
PHYSICAL_UID_REVIVAL = FORBIDDEN
```

Archive/Memorial/optional new-UID successor principles continue to apply.

## 11. Benchmark disposition · fresh 2026-08-26

### FINAL FANTASY XIV official UI guide — ADAPT

Official guidance states combat activity and being KO'd reduce equipment durability.

ADAPT:
- durability consequence should follow actual use/combat events;
- state should remain visible and repairable.

REJECT:
- continuous generic battle wear as Blacksmith's primary world-result loop.

Source: `https://na.finalfantasyxiv.com/uiguide/equipment/equipment-repair/equipment_condition_low.html`

### Stars Reach official · Before the Frontier / current hotfix notes — ADAPT

Official notes distinguish use-based wear from combat damage, and current 2026-08 hotfix notes explicitly remove durability loss calls from non-use actions such as mission turn-in and UI/loadout interactions.

ADAPT:
- actual use/hazard is the cause owner;
- combat/use event type can have different risk semantics;
- non-use bookkeeping should not damage equipment.

REJECT:
- damage every successful use/action in Blacksmith;
- importing Stars Reach repair/durability numbers.

Sources:
- `https://starsreach.com/before-the-frontier/`
- `https://starsreach.com/home/`

### Monster Hunter official web manual — ADAPT

Official manuals state melee weapon sharpness decreases with use and lower sharpness reduces performance.

ADAPT:
- actual weapon use can create a meaningful equipment-condition consequence;
- condition should feed performance/readability.

REJECT:
- per-attack sharpness maintenance loop as Blacksmith's customer/world result model.

Source: `https://game.capcom.com/manual/MH_Gen/en/page-24.html`

## 12. Adversarial review contract

### Loop 1 — Is ownership itself punished?
No. Purchase, handoff, schedule ticks and mission turn-in do not damage items.

### Loop 2 — Does every world event become durability tax?
No. Events must opt into an authored profile and actual item use. `NONE` is valid and expected.

### Loop 3 — Can one event secretly roll repeatedly?
No. One resolved event has at most one damage roll per physical UID.

### Loop 4 — Are customer success and damage conflated?
No. They are independent axes; damage is not derived from universal fit/success score.

### Loop 5 — Does this duplicate Decision29?
No. Decision29 owns effective durability multiplier and damage resolution; Decision30 owns event eligibility/profile/cap/composition only.

### Loop 6 — Can world events erase MAX through another route?
No. World events affect CURRENT only through Decision29. MAX structural scar remains repair-owned.

### Loop 7 — Do item keywords become universal protection stats?
No. At most one profile tier mitigation requires explicit event-specific relevance. Generic keywords do not reduce DIRECT.

## 13. Evidence ceiling / next work

```text
CUSTOMER_WORLD_EVENT_DAMAGE_POLICY = USER_APPROVED / BS-DAMAGE-20260826-30
EVENT_DAMAGE_PROFILE_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
RUNTIME_IMPLEMENTATION = CURRENT_CANON_MVP_AUTHORIZED / EXACT_HEAD_CONTRACT_AND_TDD_REQUIRED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_DEVICE = NOT_RUN
ACCESSIBILITY = NOT_RUN
PERFORMANCE = NOT_RUN
REPAIR_ECONOMY = NOT_FINAL
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
```

Next safe planning order:

```text
1. REPAIR_ECONOMY_REBASE + DURABILITY_ECONOMY_SENSITIVITY
2. FAILURE_CONSEQUENCE_COMPOSITION + UI_DAMAGE_PERCENT_ROUNDING if required
3. ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS
4. full planning adversarial review
5. explicit user CURRENT_PLANNING_COMPLETE declaration
6. runtime implementation-plan refresh + TDD migration
```
