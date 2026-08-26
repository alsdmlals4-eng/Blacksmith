# [현재 우선 Overlay] Blacksmith Confirmed Decisions

- 상태: `CURRENT_PRIORITY_OVERLAY`
- current owner: `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- current override Decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03`
- historical/partial basis: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~13 / BS-PROGRESSION-20260820-14~17 / BS-RESOURCE-20260824-18 / BS-REPAIR-20260824-19 / BS-OVERHAUL-20260824-20 / BS-DESTRUCTION-20260824-21 / BS-MAX-20260824-22 / BS-ONBOARD-20260824-23 / BS-LINK-20260824-24`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Human/Player validation: `NOT_RUN`

## -2. CURRENT OVERRIDE · Decision29

Decision29은 사용자의 최신 승인에 따라 Decision26의 내구도 architecture 일부를 바꾼다. 과거 CURRENT/MAX 모델을 그대로 되살리는 것이 아니라 **새 보이는 숫자 내구도 + 새 수리/흉터 규칙**을 current authority로 둔다.

Required current routing tokens:

```text
BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
BS-ENHANCE-20260825-25
BS-DAMAGE-20260825-26
BS-DAMAGE-20260826-28
BS-REPAIR-20260826-29
BS-CHRONICLE-20260825-27
BS-ART-20260825-03
```

Current durability contract:

```text
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
BASE_MAX_DURABILITY = immutable birth durability
0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
NORMAL = CURRENT_DURABILITY == MAX_DURABILITY
MINOR = 0.50 < CURRENT_DURABILITY / MAX_DURABILITY < 1.00
MAJOR = 0 < CURRENT_DURABILITY / MAX_DURABILITY <= 0.50
DESTROYED = CURRENT_DURABILITY == 0
CURRENT_MAX_AUTHORITY = SUPERSEDED = HISTORICAL_DECISION26_ONLY
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
DAMAGE_EVENT_CURRENT_LOSS = 1 / TEMP_TEST_BUDGET
```

Decision29 temporary enhancement modifiers:

```text
NORMAL: success 0pp / new effect ×1.00 / damage risk ×1.00
MINOR:  success -3pp / new effect ×0.90 / damage risk ×1.25
MAJOR:  success -7pp / new effect ×0.75 / damage risk ×1.75
```

Decision29 temporary repair quality:

```text
EXCELLENT 20% -> post-scar MAX 100%
STANDARD 60% -> post-scar MAX 75%
POOR 20% -> post-scar MAX 50%
REPAIR_MINIMUM_CURRENT_GAIN_WHEN_POSSIBLE = 1
```

Decision29 temporary MAX scar chance:

```text
            +0~10  +11~30  +31~60  +61~90  +91~100
MINOR         10%      15%      20%      25%       30%
MAJOR         25%      30%      35%      40%       45%
MAX_SCAR_AMOUNT_ON_TRIGGER = -1
MAX_DURABILITY_FLOOR = 1
MAX_DURABILITY_RECOVERY = NOT_APPROVED
```

All detailed Decision29 probabilities/modifiers/`CURRENT -1` event amount are `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`. Structural direction is user-approved; final tuning requires simulation and human playtest.

```text
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
DESTROYED_REPAIR_ALLOWED = FALSE
REPAIR_ECONOMY = NOT_FINAL / FOLLOWUP_REBASE_REQUIRED
```

## -1. CURRENT OVERRIDE · Decisions25~29 / Art03

Current simplified contract:

```text
SUCCESS_LEVEL_DELTA = +1
+9 -> +10 = PRECISION_ENHANCEMENT
+10 PRECISION SUCCESS -> exactly one ITEM_KEYWORD
ITEM_KEYWORD machine owner = CATALYST_AFFIX
NO_FOURTH_AFFIX_SLOT

TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
DAMAGE_CURVE_ANCHORS_PERCENT = [11:5, 30:6, 60:7, 90:8, 100:10]
DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
DAMAGE_CURVE_ROUNDING = NONE_CANON_EXACT_UI_ROUNDING_NOT_DECIDED
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, STATE) = Decision28_base * Decision29_state_multiplier
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED

CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE

ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY

ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

Decision28 target anchors stay user-approved. Decision29 modifies current damage risk only through the current-durability multiplier and does not create a second target-level curve.

Preserved where not conflicting:

```text
PRIMARY CORE = 강화 긴장감 + DDD / STOP vs PUSH
same UID lifecycle and delayed customer/world causality
same-target recovery
CHECKPOINT_FLOORS = [10,30,60,90]
+10 secured/break-even role
+11 first salient risk decision
+100 terminal
existing success / attempt-cost / resource test budgets pending Decision29 sensitivity recheck
```

Open gates:

```text
CUSTOMER_EVENT_DAMAGE_POLICY = CONTENT_OWNER_DECISION_REQUIRED
REPAIR_ECONOMY_REBASE = REQUIRED
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
```

## 0. 운영 동기화 규칙

Meaningful planning changes update GitHub current owner/index/handoff, Notion Human current surfaces and AI/System operational metadata. Google Sheet remains migration-only and receives a same-ID compatibility row only when required.

## Historical ledger boundary

2026-08-20/24 sections and `CURRENT_CONFIRMED_DECISIONS.md` remain historical evidence. In particular, the following do **not** become current merely because Decision29 restores a visible CURRENT/MAX axis:

- old 0~100 durability scale;
- old STABLE/STRESSED/DAMAGED/FRACTURED/CRITICAL MAX bands;
- old MAX success/effect penalties;
- old CURRENT→MAX repair price formulas;
- old MAX +15/cap60 overhaul;
- old DAMAGE/CRITICAL failure-family ratios;
- old multi-precision milestones;
- routine dated Chronicle rows.

The current owner + Decision29/28 specific owners always win on conflicting fields.
