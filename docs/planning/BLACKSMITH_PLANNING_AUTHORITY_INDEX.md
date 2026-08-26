# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX / POSTMERGE_PLANNING`
- current decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29 / BS-REPAIR-20260826-31 / BS-DAMAGE-20260826-30 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03 / BS-ART-20260826-04`
- current owner: `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. 충돌 시 우선순위

1. 사용자의 최신 지시와 승인.
2. `AGENTS.md`.
3. `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` — Decisions25~30 / Art03~04 integrated meaning.
4. `BS-DAMAGE-20260826-30_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY.md` + `BLACKSMITH_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY_20260826.json` — customer/world event damage owner.
5. `BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md` + `BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json` — current durability/repair owner.
6. `BS-DAMAGE-20260826-28_DAMAGE_PROBABILITY_CURVE.md` + `BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json` — target-level enhancement-failure base damage curve owner.
7. `BS-ART-20260826-04_ACTUAL_GAME_IMAGE_CONSUMER_GATE.md` + `BLACKSMITH_ACTUAL_GAME_IMAGE_CONSUMER_GATE_20260826.json` — project image consumer/delivery owner; Art03 remains style owner.
8. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md` current override.
9. 2026-08-20/24 개별 Canon — 새 owner와 충돌하지 않는 필드만 current; 충돌 필드는 역사/부분대체 evidence.
10. 실제 runtime/data/test evidence — 구현 사실을 증명하지만 PLAN Gate의 implementation drift가 최신 승인 기획을 덮어쓰지 않는다.
11. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장.
12. R2/R3 Game Bible·과거 PoC·구형 data/runtime.

```text
CURRENT_OWNER = docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
BS-ENHANCE-20260825-25
BS-DAMAGE-20260825-26
BS-DAMAGE-20260826-28
BS-REPAIR-20260826-29
BS-DAMAGE-20260826-30
BS-CHRONICLE-20260825-27
BS-ART-20260825-03
BS-ART-20260826-04
```

새 `기획 완료` 사용자 선언 전 제품 `data/scripts/scenes/assets/addons/project.godot` 변경은 금지한다.

## 2. Current core contract

### Enhancement / Precision

```text
SUCCESS_LEVEL_DELTA = +1
TARGET = CURRENT + 1
+9 -> +10 = PRECISION_ENHANCEMENT
+10 PRECISION SUCCESS -> exactly one ITEM_KEYWORD
ITEM_KEYWORD machine owner = CATALYST_AFFIX
NO_FOURTH_AFFIX_SLOT
```

### Durability / derived state · Decision29

```text
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
BASE_MAX_DURABILITY = immutable birth durability
0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
CURRENT_CONDITION_RATIO = CURRENT_DURABILITY / MAX_DURABILITY
STRUCTURAL_CONDITION_RATIO = MAX_DURABILITY / BASE_MAX_DURABILITY
EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)
DESTROYED = CURRENT_DURABILITY == 0
NORMAL = EFFECTIVE_DURABILITY_RATIO == 1.00
MINOR = 0.50 < EFFECTIVE_DURABILITY_RATIO < 1.00
MAJOR = 0 < EFFECTIVE_DURABILITY_RATIO <= 0.50
CURRENT_MAX_AUTHORITY = SUPERSEDED = HISTORICAL_DECISION26_ONLY
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
DAMAGE_EVENT_CURRENT_LOSS = 1 / TEMP_TEST_BUDGET
```

`CURRENT/MAX` 현재 손상과 `MAX/BASE_MAX` 구조 흉터를 별도 패널티로 중첩하지 않는다. 둘 중 더 나쁜 비율 하나가 current effective state와 enhancement modifier를 소유한다.

Reference:

```text
5/5/5 -> NORMAL
4/4/5 -> MINOR
2/2/5 -> MAJOR
1/1/5 -> MAJOR
```

### Enhancement-failure damage · Decision28 + Decision29 modifier

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
DAMAGE_CURVE_ANCHORS_PERCENT = [11:5, 30:6, 60:7, 90:8, 100:10]
DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
DAMAGE_CURVE_ROUNDING = NONE_CANON_EXACT_UI_ROUNDING_NOT_DECIDED
```

Temporary effective-state modifiers:

```text
NORMAL success 0pp / new effect ×1.00 / damage risk ×1.00
MINOR  success -3pp / new effect ×0.90 / damage risk ×1.25
MAJOR  success -7pp / new effect ×0.75 / damage risk ×1.75
DURABILITY_MODIFIERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

```text
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, EFFECTIVE_STATE)
= Decision28_base_probability(TARGET) * Decision29_state_multiplier(EFFECTIVE_STATE)
```

Hard guarantee remains 100%; modifier does not change +1 level delta, existing stats or +10 keyword cardinality.

### Repair / probabilistic structural scar + economy overlay · Decision29 + Decision31

```text
REPAIR_JOB_AVAILABLE = true after a resolved actual damage event lowers CURRENT; one boolean per UID
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY AND REPAIR_JOB_AVAILABLE
REPAIR_JOB_CONSUMED_ON_REPAIR_START = TRUE
DESTROYED_REPAIR_ALLOWED = FALSE
FULL_DURABILITY_REPAIR_ALLOWED = FALSE
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
MAX_DURABILITY_RECOVERY = NOT_APPROVED
```

Temporary repair quality:

```text
EXCELLENT 20% -> post-scar MAX 100%
STANDARD  60% -> post-scar MAX 75%
POOR      20% -> post-scar MAX 50%
REPAIR_MINIMUM_CURRENT_GAIN_WHEN_POSSIBLE = 1
```

Temporary `MAX -1` scar chance:

| Pre-repair effective state | +0~10 | +11~30 | +31~60 | +61~90 | +91~100 |
|---|---:|---:|---:|---:|---:|
| MINOR | 10% | 15% | 20% | 25% | 30% |
| MAJOR | 25% | 30% | 35% | 40% | 45% |

Decision29 quality/scar values remain `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`. Decision31 sets the temporary initial payment `ceil(R_BAND * (0.05 + 0.65 * ((MAX-CURRENT)/BASE_MAX))) + 1 common_reinforcement_material`; it forbids sell-price, next-attempt-price, MAX, and scar multipliers. A scar that would make positive recovery impossible is skipped without reroll. `R_BAND` table and final prices remain sensitivity inputs, not product balance.

### Customer/world event damage · Decision30

```text
PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE
ACTUAL_ITEM_USE_REQUIRED = TRUE
MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1
MISSION_OUTCOME_AND_ITEM_DAMAGE = INDEPENDENT_AXES
WORLD_EVENT_MAX_DURABILITY_DAMAGE = FALSE
NO_UNIVERSAL_CUSTOMER_DAMAGE_PERCENT
```

Temporary event profiles:

```text
NONE = 0%
LOW = 10%
MEDIUM = 20%
HIGH = 40%
DIRECT = 100%
PROBABILISTIC_DAMAGE_CAP = 95%
EVENT_DAMAGE_PROFILE_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

`NONE/LOW/MEDIUM/HIGH` use Decision29's effective-state damage-risk multiplier. `DIRECT` causes one deterministic Decision29 damage event. Same event + same UID rolls at most once. World events never directly reduce MAX.

### Chronicle / Art / Visual delivery

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

Decision04 current image-delivery gate:

```text
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
NEW_EXPLANATORY_GDD_SHEET_IMAGE_TARGET = FALSE
NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE
PRIMARY_USE_GATE_REQUIRED = TRUE
NO_CONSUMER = CUT_OR_DEFER
GENERATED_UI_SCREENSHOT_MOCKUP_AS_PRODUCT_ASSET = FALSE
FULL_FRAME_IMAGE_ALLOWED_ONLY_IF_RUNTIME_CONSUMES_FULL_FRAME = TRUE
```

The existing 8 Visual GDD images are `HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY`. New image candidates must map to an actual game consumer before a separate image-generation approval Gate.

## 3. Historical owner boundary

Preserved where non-conflicting:

- `BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md` — enhancement tension + DDD.
- `BLACKSMITH_ENHANCEMENT_PROGRESSION_ECONOMY_CANON_20260820.md` — +10 break-even / +100 range intent; exact economics need Decision29/30 rebase.
- `BLACKSMITH_LEVEL_TO_EXPERIENCE_BAND_CANON_20260820.md` — target bands.
- `BLACKSMITH_CHECKPOINT_CADENCE_CANON_20260820.md` — floors `[10,30,60,90]`.
- existing success/recovery/attempt-cost/common reinforcement-material values — planning inputs pending durability/economy sensitivity recheck.
- physical UID death/archive/memorial/new-UID successor principles remain current.

Historical only where conflicting:

- old 0~100 CURRENT/MAX scale and STABLE/STRESSED/DAMAGED/FRACTURED/CRITICAL MAX bands;
- old MAX success/effect penalties;
- old DAMAGE/CRITICAL family ratios;
- old CURRENT→MAX repair pricing/material/fatigue formulas;
- old MAX +15/cap60 overhaul;
- old multi-precision cadence;
- old Visual GDD system numbers;
- existing explanatory Visual GDD images as future image-batch templates.

Decision29 does not resurrect those historical values simply because numeric durability is current again. Decision30 does not copy enhancement-failure damage probabilities into customer events. Decision04 does not revoke Art03; it narrows what new images are worth producing.

## 4. Preserved progression anchors

```text
MIN_LEVEL = +0
MAX_LEVEL = +100
+0~+9 = INVESTMENT_RECOVERY_ZONE
+10 = BREAK_EVEN_RECOVERY_POINT
+11~+100 = PROFITABLE_ENHANCEMENT_ZONE
CHECKPOINT_FLOORS = [10,30,60,90]
```

Experience bands remain LEARN / BUILD_CONFIDENCE / FIRST_STOP_POINT / TENSION / HIGH_STAKES / MASTERY.

Existing planning success/recovery inputs:

```text
+1 100%
+2 97%
+3~+10 95% -> 86%
+11 82%
+12~+30 81% -> 72%
+31~+60 73% -> 69%
+61~+100 69% -> 64%
recovery = +6pp / same-target failure
soft cap 95%
hard guarantee = LEARN2 / BUILD4 / FIRST4 / TENSION5 / HIGH6 / MASTERY7
```

These are not final product balance after Decision29/30.

## 5. Current unresolved gates

```text
REPAIR_ECONOMY_HUMAN_PLAYTEST + MUTABLE_R_BAND_BASELINE_REVIEW
FAILURE_CONSEQUENCE_COMPOSITION
UI_DAMAGE_PERCENT_ROUNDING
ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS
```

Decision29 closes structural repair behavior and MAJOR enhancement eligibility; exact detailed tuning remains temporary. Decision30 closes the customer/world event damage policy structure; exact profile numbers remain temporary.

## 6. Current work order

```text
1. REPAIR_ECONOMY_HUMAN_PLAYTEST + MUTABLE_R_BAND_BASELINE_REVIEW
2. FAILURE_CONSEQUENCE_COMPOSITION + UI_DAMAGE_PERCENT_ROUNDING if needed
3. ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS
4. full planning adversarial review
5. CURRENT_PLANNING_COMPLETE user declaration
6. runtime implementation plan refresh and TDD migration
```

## 7. Runtime reality / drift

Current V2 runtime contains similar durability/customer fields but old semantics. Field-name overlap is not Decision29/30 implementation evidence.

```text
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = NOT_RUN / BLOCKED
OLD_V2_RUNTIME = IMPLEMENTATION_DRIFT / HISTORICAL_RUNTIME_TRUTH
```

## 8. Operational sync / evidence ceiling

Meaningful planning changes update GitHub current owner/index/handoff, Notion Human current surfaces and AI/System metadata. Google Sheet remains migration-only same-ID compatibility.

PR #196 remains `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`.

```text
PLANNING_DESIGN = USER_APPROVED
DAMAGE_CURVE_NUMBERS = USER_APPROVED / BS-DAMAGE-20260826-28
DURABILITY_REPAIR_STRUCTURE = USER_APPROVED / BS-REPAIR-20260826-29
DURABILITY_REPAIR_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
CUSTOMER_WORLD_EVENT_DAMAGE_POLICY = USER_APPROVED / BS-DAMAGE-20260826-30
CUSTOMER_EVENT_DAMAGE_PROFILE_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
VISUAL_DELIVERY_POLICY = USER_APPROVED / BS-ART-20260826-04
IMAGE_GENERATION = NOT_RUN
ACTUAL_RUNTIME_IMAGE_CONSUMPTION = NOT_RUN
REPAIR_ECONOMY = USER_APPROVED_TEST_CONTRACT / B65_DEFAULT_PLAYTEST_REQUIRED
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
RUNTIME_IMPLEMENTATION = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_GEOMETRY = NOT_RUN
```
