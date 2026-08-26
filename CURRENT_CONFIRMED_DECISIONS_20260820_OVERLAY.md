# [현재 우선 Overlay] Blacksmith Confirmed Decisions

- 상태: `CURRENT_PRIORITY_OVERLAY`
- current owner: `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- current override Decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29 / BS-REPAIR-20260826-31 / BS-DAMAGE-20260826-30 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03 / BS-ART-20260826-04`
- historical/partial basis: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~13 / BS-PROGRESSION-20260820-14~17 / BS-RESOURCE-20260824-18 / BS-REPAIR-20260824-19 / BS-OVERHAUL-20260824-20 / BS-DESTRUCTION-20260824-21 / BS-MAX-20260824-22 / BS-ONBOARD-20260824-23 / BS-LINK-20260824-24`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Human/Player validation: `NOT_RUN`

## -4. CURRENT OVERRIDE · Decision31 repair economy overlay

Decision31 closes the approved **planning test contract** for repair economics while keeping product prices and runtime work open.

```text
BS-REPAIR-20260826-31
REPAIR_JOB_AVAILABLE = boolean_per_item_uid_after_resolved_actual_damage_reduces_CURRENT
REPAIR_ELIGIBLE = 0 < CURRENT < MAX AND REPAIR_JOB_AVAILABLE
REPAIR_JOB_CONSUMED_ON_REPAIR_START = TRUE
GOLD = ceil(R_BAND * (0.05 + 0.65 * ((MAX-CURRENT)/BASE_MAX)))
REPAIR_PAYMENT = GOLD + 1 common_reinforcement_material
R_BAND != sell_price / next_attempt_price / MAX_multiplier / scar_multiplier
NO_ZERO_RECOVERY_SCAR = skip_without_reroll
SENSITIVITY = b 0.50 / 0.65 / 0.80 with identical deterministic inputs
```

Decision29 remains owner of numeric durability, quality probabilities, scar-band chance, and derived state. Decision31 owns only job gating, economy source/formula, safety rounding, and sensitivity contract. All numeric economics are temporary test budgets, not final product balance.

## -3. CURRENT OVERRIDE · Decision30 + Art04

Decision30은 Decision26의 고객/세계 손상 hook을 실제 사용 원인 기반 정책으로 닫는다. Art04는 Art03의 스타일을 바꾸지 않고 신규 이미지 제작 대상을 **실제 게임 consumer가 있는 이미지**로 제한한다.

```text
BS-DAMAGE-20260826-30
PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE
ACTUAL_ITEM_USE_REQUIRED = TRUE
MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1
MISSION_OUTCOME_AND_ITEM_DAMAGE = INDEPENDENT_AXES
WORLD_EVENT_MAX_DURABILITY_DAMAGE = FALSE
NO_UNIVERSAL_CUSTOMER_DAMAGE_PERCENT

NONE = 0%
LOW = 10%
MEDIUM = 20%
HIGH = 40%
DIRECT = 100%
PROBABILISTIC_DAMAGE_CAP = 95%
EVENT_DAMAGE_PROFILE_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

`NONE/LOW/MEDIUM/HIGH`는 Decision29의 effective-state damage-risk multiplier를 재사용한다. `DIRECT`는 Decision29 damage event 1회를 확정한다. world/customer event는 MAX를 직접 손상시키지 않는다.

```text
BS-ART-20260826-04
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
NEW_EXPLANATORY_GDD_SHEET_IMAGE_TARGET = FALSE
NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE
GENERATED_UI_SCREENSHOT_MOCKUP_AS_PRODUCT_ASSET = FALSE
FULL_FRAME_IMAGE_ALLOWED_ONLY_IF_RUNTIME_CONSUMES_FULL_FRAME = TRUE
PRIMARY_USE_GATE_REQUIRED = TRUE
NO_CONSUMER = CUT_OR_DEFER
EXISTING_VISUAL_GDD_8 = HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY
```

새 이미지 후보는 actual consumer metadata + Visual Requirement/Delete Test + 별도 Image Conversation Approval Gate를 통과해야 한다. consumer 후보 화면명은 자동 생성 목록이 아니다.

## -2. CURRENT OVERRIDE · Decision29

Decision29은 Decision26의 내구도 architecture 일부를 바꾼다. 과거 CURRENT/MAX 모델을 그대로 되살리는 것이 아니라 **새 보이는 숫자 내구도 + 새 수리/흉터 규칙**을 current authority로 둔다.

Required current routing tokens:

```text
BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
BS-ENHANCE-20260825-25
BS-DAMAGE-20260825-26
BS-DAMAGE-20260826-28
BS-REPAIR-20260826-29
BS-REPAIR-20260826-31
BS-DAMAGE-20260826-30
BS-CHRONICLE-20260825-27
BS-ART-20260825-03
BS-ART-20260826-04
```

Current durability contract:

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

`CURRENT/MAX`의 현재 손상과 `MAX/BASE_MAX`의 영구 흉터는 별도 보정으로 중첩하지 않는다. 둘 중 더 나쁜 비율 하나가 effective state를 소유한다.

```text
5/5/5 -> NORMAL
4/4/5 -> MINOR
2/2/5 -> MAJOR
1/1/5 -> MAJOR
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

Decision29 temporary MAX scar chance, using **pre-repair effective state + enhancement band**:

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
FULL_DURABILITY_REPAIR_ALLOWED = FALSE
REPAIR_ECONOMY = USER_APPROVED_TEST_CONTRACT / SENSITIVITY_REQUIRED
```

## -1. CURRENT OVERRIDE · Decisions25~31 / Art03~04

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
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, EFFECTIVE_STATE) = Decision28_base * Decision29_effective_state_multiplier
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED

CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE
ACTUAL_ITEM_USE_REQUIRED = TRUE
MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1

ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY

ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE
PRIMARY_USE_GATE_REQUIRED = TRUE
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

Decision28 target anchors remain approved. Decision29 owns the effective durability modifier and structural repair resolution; Decision31 owns the repair-economy overlay and its test-only sensitivity. Decision30 owns customer/world eligibility/profile/composition without copying Decision28 target odds. Art04 makes explanatory Visual GDD sheets historical references, not future image-production targets.

Preserved where not conflicting:

```text
PRIMARY CORE = 강화 긴장감 + DDD / STOP vs PUSH
same UID lifecycle and delayed customer/world causality
same-target recovery
CHECKPOINT_FLOORS = [10,30,60,90]
+10 secured/break-even role
+11 first salient risk decision
+100 terminal
existing success / attempt-cost / resource test budgets pending durability/economy sensitivity recheck
```

Open gates:

```text
REPAIR_ECONOMY_REBASE + DURABILITY_ECONOMY_SENSITIVITY = REQUIRED
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS = REQUIRED_BEFORE_IMAGE_GENERATION
```

## 0. 운영 동기화 규칙

Meaningful planning changes update GitHub current owner/index/handoff, Notion Human current surfaces and AI/System operational metadata. Google Sheet remains migration-only and receives a same-ID compatibility row only when required.

## Historical ledger boundary

아래 `## 1`~`## 21`은 2026-08-20/24와 Decision28 시점의 **frozen historical/provenance ledger**를 원문 보존한다. 아래에 `current`라고 쓰인 문장도 해당 시점의 표현이며, Decisions29~30/Art04와 충돌하는 경우 위 `CURRENT OVERRIDE`와 current owner가 항상 우선한다. 역사 섹션의 숫자·수리식·MAX band·`한 damage event = 한 상태`·설명용 Visual GDD 생산 표현을 최신 fallback으로 사용하지 않는다.

## 1. 제품 계층 — 01

```text
PRIMARY CORE
강화의 긴장감 + DDD
= 지금 멈춤 / 한 번 더 도전

SUPPORT
작품 UID·생애
정밀제작
고객/세계 생애주기
경제·하루 작업량
```

DDD는 `행동 → 기대 → anticipation → 즉시 결과 → 보상/손실 → 다음 질문`의 밀도를 높이는 것이며 반복 클릭·자극량 자체를 의미하지 않는다.

## 2. 실패·회복·정보 공개 — 02~04 · `PARTIALLY_SUPERSEDED`

- 기본 골격: `RISK_PLUS_RECOVERY_PROGRESS`.
- 모든 실패는 실제 비용/손실과 같은 작품 UID의 recovery를 남긴다.
- account-wide transferable failstack은 기본 게임에서 금지.
- 과거 강화 전 정보에는 CURRENT/MAX 위험이 포함됐으나, current damage disclosure는 4단계 damage state와 Decision28의 +11~+100 conditional damage curve를 사용한다.
- 숨은 위험 보정으로 긴장감을 만들지 않는다.
- Decision28 수치는 `P(damage advance | enhancement failure, target)`이며 per-attempt unconditional damage 확률로 잘못 표시하지 않는다.

## 3. Checkpoint·CURRENT/MAX·파괴 — 05~09 · `HISTORICAL_DURABILITY_EVIDENCE`

아래 수치 이중 내구 계약은 Decision26 이후 current gameplay authority가 아니다.

```text
0 <= CURRENT <= MAX <= 100
new item = 100 / 100
normal repair = CURRENT -> MAX
MAX unchanged
CURRENT == 0 or MAX == 0 -> physical DESTROYED
```

- DOWNGRADE는 최대 1단계, 최근 checkpoint floor 아래로 내려가지 않음 — 이 checkpoint 원리는 유지.
- `FAIL_DAMAGE`/`FAIL_CRITICAL_DAMAGE`와 MAX 구조 흉터 구분은 current damage resolution에서 대체됨.
- 물리 파괴 후 UID·이름·강화/소유/사건/파괴 원인·Chronicle 기록을 보존한다는 생애 원리는 유지.

과거 MAX 상태 테스트:

```text
81~100: success  0pp / new effect 100%
61~80 : success -3pp / new effect 100%
41~60 : success -6pp / new effect 95%
21~40 : success -10pp / new effect 90%
1~20  : success -15pp / new effect 80%
```

현재는 `HISTORICAL_TEST_BUDGET`; MINOR/MAJOR에 자동 이식하지 않는다.

## 4. 일반 CURRENT 수리 — 10~12 + 18~19 · `SUPERSEDED_PENDING_NEW_REPAIR_MODEL`

과거 공식:

```text
missing = MAX - CURRENT

R
= SWORD_BASE_R 800
× MATERIAL_STRUCTURE_MULTIPLIER
× SECURED_BAND_MULTIPLIER

gold_cost
= R × (0.05 + 0.65 × missing / 100)

required_common_material
= max(1, ceil(missing / 25))

PAYMENT = GOLD + REQUIRED_COMMON_MATERIAL
CURRENT -> MAX
MAX unchanged
recovery unchanged
REPAIR_JOB_FATIGUE_COST = 2
```

과거 구조 배율:

```text
material: iron 1.00 / silver 1.20 / meteor_iron 1.50
secured: LEARN·BUILD 1.00 / FIRST 1.10 / TENSION 1.25 / HIGH 2.25 / MASTERY 3.00
```

이 수리 공식과 배율은 새 `MINOR_MAJOR_REPAIR_MODEL` 승인 전 current 구현 fallback으로 사용하지 않는다. 일반 강화용 공통 보강재 공급 계약은 별도 유지 가능하다.

## 5. 실패 결과군 정확 비율 — 13 · `HISTORICAL_DAMAGE_BUDGET`

과거 실패가 이미 확정된 뒤의 조건부 비율:

```text
order = HOLD / DOWNGRADE / DAMAGE / CRITICAL

LEARN             100 /  0 /  0 /  0
BUILD_CONFIDENCE   90 /  0 / 10 /  0
FIRST_STOP_POINT   65 / 10 / 23 /  2
TENSION            45 / 10 / 35 / 10
HIGH_STAKES        30 / 15 / 39 / 16
MASTERY            20 / 20 / 40 / 20
```

Decision26 이후 이 DAMAGE/CRITICAL 비율은 current damage resolution에서 대체됐고 Decision28의 새 curve도 이 표에서 도출하지 않았다. 현재 `TARGET <= +10` 강화 손상은 0, +11 이후 conditional damage 확률은 `5% / 6% / 7% / 8% / 10%` 앵커와 exact piecewise-linear interpolation이 소유한다. 이 역사 표는 damage와 downgrade의 동시/배타 composition도 결정하지 않는다.

## 6. 강화 범위·경제 전환점 — 14

```text
MIN_LEVEL = +0
MAX_LEVEL = +100

+0~+9      INVESTMENT_RECOVERY_ZONE
+10        BREAK_EVEN_RECOVERY_POINT
+11~+100   PROFITABLE_ENHANCEMENT_ZONE
```

+10 경제 확보 역할은 유지하되, 과거 기대원가가 CURRENT/MAX 수리·파괴 비용을 포함했다는 점 때문에 숫자 anchor는 새 damage/repair 모델 후 재검산 대상이다.

정밀제작·수식어·Chronicle·특수 고객/거래 채널 프리미엄은 별도 가치축이다.

## 7. Target level → 경험 밴드 — 15

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

밴드는 `current_level`이 아니라 **target_level** 기준.

```text
CURRENT +10 = FIRST_ECONOMIC_STOP_STATE
TARGET +11  = FIRST_STOP_POINT ATTEMPT
```

경험 밴드는 유지하지만 과거 밴드별 DAMAGE/CRITICAL 비율은 Decision26/28에 의해 대체됐다.

## 8. Checkpoint cadence — 16

```text
CHECKPOINT_FLOORS = [10, 30, 60, 90]
```

역할:

```text
+10 경제 본전 확보
+30 TENSION 완료
+60 HIGH_STAKES 완료
+90 FINAL MASTERY PUSH staging
+100 MAX terminal
```

Checkpoint는 오직 DOWNGRADE floor다. recovery/시도비/강화비를 리셋하지 않는다. 구형 CURRENT/MAX/수리비 리셋 언급은 더 이상 적용 대상이 아니다.

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

## 9. 성공률·회복·강화비 — 17

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

기본 성공률:

```text
+1       100%
+2        97%
+3~+10    95% -> 86%
+11       82%
+12~+30   81% -> 72%
+31~+60   73% -> 69%
+61~+100  69% -> 64%
```

Recovery:

```text
+6%p / same-target failure
soft cap 95%
owner = ITEM_UID + TARGET_LEVEL
hard guarantee = LEARN2 / BUILD4 / FIRST4 / TENSION5 / HIGH6 / MASTERY7
```

강화 시도비:

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)

ordinary material balance unit
= ceil(target / 20)
shadow = 50G/unit
```

대표 골드:

```text
+10 830 / +30 6,270 / +60 22,440 / +90 47,310 / +100 57,440
```

과거 MASTERY CURRENT/MAX 손상 Budget은 `HISTORICAL_NUMERIC_EVIDENCE`이며 Decision28 또는 새 4단계 repair에 자동 이식하지 않는다.

## 10. 누적 기대원가·기본 판매가 — 17

20,000-run planning Monte Carlo와 독립 seed 재검산을 사용한 과거 anchor다. 새 damage/repair 모델이 경제에 영향을 주므로 release/current balance 재검산 전까지 `PRE_SIMPLIFICATION_ECONOMIC_EVIDENCE`로 취급한다.

| Level | Mean Expected Cost Anchor | Base Market Value |
|---:|---:|---:|
| +0 | 1,500 | 1,000 |
| +5 | 2,322 | 1,900 |
| +9 | 4,759 | 4,600 |
| +10 | **5,779** | **5,800** |
| +11 | 7,023 | 7,400 |
| +20 | 30,713 | 34,400 |
| +30 | 96,006 | 117,100 |
| +40 | 219,565 | 285,400 |
| +50 | 419,230 | 578,500 |
| +60 | 712,986 | 1,055,200 |
| +70 | 1,168,898 | 1,846,900 |
| +80 | 1,907,274 | 3,204,200 |
| +90 | 3,235,853 | 5,824,500 |
| +100 | **5,632,657** | **11,265,300** |

+10 break-even / +11 이후 profit-zone이라는 구조 의도는 유지하지만, 정확 숫자는 Decision28 + 새 repair model 반영 뒤 재검산한다.

## 11. 일반 강화·수리 Resource Supply — 18 · `PARTIALLY_PRESERVED`

```text
CANONICAL_ID = common_reinforcement_material
PLAYER_NAME_KO = 보강재
UNIT_PRICE = 50G
SUPPLY = WORKSHOP_MATERIAL_VENDOR / ALWAYS_AVAILABLE / NO_CAP
```

강화 recipe는 current planning input으로 유지:

```text
+1~+20   보강재 1
+21~+40  보강재 2
+41~+60  보강재 3
+61~+80  보강재 4
+81~+100 보강재 5
```

구형 CURRENT 결손 기반 **수리** 보강재 recipe는 `SUPERSEDED_PENDING_NEW_REPAIR_MODEL`이다.

- 보강재는 새 화폐가 아니라 공통 공방 재료.
- 골드와 보강재를 모두 지불하며 상호 대체/할인하지 않음 — 강화 recipe에 적용.
- `iron / silver / meteor_iron`을 일반 보강재로 직접 소비하지 않음.
- RNG·희귀 드롭·일일 cap·채굴/전투·고객 완료를 기본 공급 Gate로 사용하지 않음.
- salvage/customer/world-event 보너스 공급은 future hook이며 아직 제품 승인 아님.

책임 원본: `docs/planning/BLACKSMITH_COMMON_RESOURCE_SUPPLY_CANON_20260824.md`.

## 12. 후기 일반 CURRENT 수리 경제 — 19 · `HISTORICAL_PRE_SIMPLIFICATION_EVIDENCE`

Decision19의 배율과 20,000-run은 구형 CURRENT/MAX 수리 정책의 민감도 증거로 보존한다. 새 MINOR/MAJOR 수리 모델의 숫자로 자동 이식하지 않는다.

책임 원본: `docs/planning/BLACKSMITH_LATE_REPAIR_ECONOMY_CANON_20260824.md`.

## 13. MAX 생애 1회 부분 대수선 — 20 · `SUPERSEDED_PENDING_NEW_REPAIR_MODEL`

과거 MAX +15 / ceiling 60 / 750k×material + 보강재20 + fatigue5 구조는 CURRENT/MAX 삭제와 함께 current repair authority에서 내려간다. 생애 1회 특별 복구라는 설계 원리는 후속 MAJOR repair/overhaul 비교 후보가 될 수 있지만 자동 채택하지 않는다.

책임 원본: `docs/planning/BLACKSMITH_MAX_OVERHAUL_CANON_20260824.md`.

## 14. DESTROYED 기록·추모·후계 UX — 21 · `PARTIALLY_PRESERVED`

유지되는 핵심:

```text
PHYSICAL_ITEM_DIES
HISTORY_DOES_NOT_DIE
IMMUTABLE_HISTORY_ARCHIVE
CURATED_MEMORIAL
OPTIONAL_NEW_UID_SUCCESSOR
ZERO_POWER_INHERITANCE
```

구형 CURRENT/MAX 0 도달 축·직전 퍼센트 표시는 current destruction trigger가 아니다. 이제 `MAJOR -> DESTROYED` 한 단계 transition 또는 eligible customer/world event damage가 terminal state에 도달할 수 있다.

- DESTROYED는 같은 physical UID의 영구 종료이며 강화·수리·판매·정상 인계로 부활하지 않는다.
- Archive는 age-based FIFO 삭제 금지.
- successor는 새 UID, predecessor relation만 허용하며 gameplay power/history를 상속하지 않는다.
- 고객 작품 파괴 시 고객 identity/관계 기록은 유지한다.

책임 원본: `docs/planning/BLACKSMITH_DESTRUCTION_UX_CANON_20260824.md` — CURRENT/MAX-specific 필드는 historical evidence.

## 15. +100 최대 강화 완료 Payoff — 22

사용자 승인 구조를 유지한다.

```text
MAX_ENHANCEMENT_COMPLETE
```

- +100은 기본 강화 terminal이고 +101/Prestige/reset형 후속 강화는 별도 승인 없이는 만들지 않는다.
- 같은 UID에 완료 사실을 기록하고 별도 완료 연출/표식을 제공할 수 있다.
- completion 자체로 추가 power multiplier나 damage heal을 주지 않는다.
- +100 이후에도 고객/세계 인계와 4단계 damage/DESTROYED 규칙을 적용받는다.

책임 원본: `docs/planning/BLACKSMITH_MAX_LEVEL_PAYOFF_CANON_20260824.md`.

## 16. 첫 10분 Core Thesis 온보딩 — 23 · `PARTIALLY_SUPERSEDED`

Current interpretation:

```text
New Game
→ 짧은 첫 작품 제작
→ +1/+2 LEARN
→ +3~+9 ordinary BUILD
→ +9 -> +10 Precision Enhancement
→ +10 성공 시 ITEM_KEYWORD 1개 생성 + checkpoint + break-even state
→ +11 첫 damage-eligible risk Preview
→ STOP vs PUSH
→ same UID payoff
```

- 첫 강화 input 약 3분/첫 STOP-PUSH 약 10분은 Human pacing 목표.
- tutorial-only scripted failure, hidden success boost, 별도 tutorial odds 금지.
- +10 이전 강화 실패 손상은 0.
- +11 실패의 conditional damage chance는 Decision28에 따라 **5%**다. 이후 +30 6%, +60 7%, +90 8%, +100 10% 앵커 사이 exact linear interpolation으로 상승한다.
- CURRENT/MAX teaching과 MAX/CRITICAL structural-scar teaching은 current onboarding에서 제거된다.
- +11을 튜토리얼 진행 조건으로 강제하지 않는다.

책임 원본: `docs/planning/BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md` — 위 current override가 동일 필드에서 우선.

## 17. 정밀강화·고객/세계 인과 연결 — 24 · `PARTIALLY_SUPERSEDED`

유지:

```text
DISCLOSED_CONTEXT_FIT_AND_CAUSAL_MULTI_AXIS_RESULT
NADIA_VENN / ADVENTURER_01 starter
목적 / 제약 / 알려진 상황
NO_UNIVERSAL_FIT_SCORE
NO_BEST_BADGE
same UID delayed result
```

정밀강화 cadence만 current Decision25로 교정:

```text
+9 -> +10 only Precision Enhancement
+10 success -> ITEM_KEYWORD
```

고객 구매/인계 뒤 실제 delayed event에서:

```text
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
```

eligible event는 same UID damage를 최대 한 단계 진행시킬 수 있고, 실제 발생했다면 causal reason/Chronicle에 남긴다. event eligibility와 확률은 후속 content Decision이다.

구형 `0.30pp/level`은 계속 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`이며 이번 Decision이 바꾸지 않는다.

책임 원본: `docs/planning/BLACKSMITH_PRECISION_CUSTOMER_LINK_CANON_20260824.md` — old multi-precision wording은 부분 대체.

## 18. 과거 숫자의 지위

다음은 current numeric authority가 아니다.

```text
+5 최초 흑자
+60 마지막 가격 앵커
old decade success pattern
old MASTERY 25~40% working range
old multi-step downgrade
old destroy RNG
pre-19 HIGH repair multiplier 1.50
pre-19 MASTERY repair multiplier 1.80
pre-24 customer enhancement contribution +1.00pp / level
all CURRENT/MAX loss and structural-scar tables as current damage authority
old DAMAGE/CRITICAL family ratios as the new +11~+100 damage curve
```

상태: `HISTORICAL_NUMERIC_EVIDENCE / RECALIBRATION_INPUT`.

## 19. 현재 승인사항 요약

```text
01     PRIMARY CORE = 강화 긴장감 + DDD
14     +10 break-even role / +100 max structure intent
15     target-level experience bands; old damage ratios superseded
16     checkpoint [10,30,60,90]
17     success / recovery / attempt cost test budgets; durability-dependent economics need recheck
18     common reinforcement material enhancement supply preserved; old repair mapping stale
21     physical destruction/archive/memorial/new-UID successor principles preserved
22     +100 terminal identity preserved
23     onboarding pacing preserved; CURRENT/MAX teaching replaced
24     Nadia/customer causal structure preserved; precision cadence replaced; world-event damage hook added
25     +1 success only / +9→+10 only Precision / one keyword
26     NORMAL→MINOR→MAJOR→DESTROYED / +11+ enhancement-failure damage gate / eligible world-event damage
28     P(damage advance | enhancement failure, target): +11 5% / +30 6% / +60 7% / +90 8% / +100 10%; exact piecewise-linear interpolation
27     player Chronicle = meaningful events only, no routine dated attempt log
Art03  ILLUSTRATED_WORKSHOP_BOOK = USER_APPROVED_DIRECTION
```

Decision28 damage curve는 `USER_APPROVED_PLANNING_CANON`. MINOR/MAJOR repair, MAJOR enhancement eligibility, customer-event damage numbers, failure consequence composition, UI rounding은 `NOT_FINAL / FOLLOW_UP_DECISION_REQUIRED`. 제품 data/runtime은 아직 변경하지 않는다.

## 20. 현재 작업 순서

1. `MINOR_MAJOR_REPAIR_MODEL` + `MAJOR_ENHANCEMENT_ELIGIBILITY`.
2. `CUSTOMER_EVENT_DAMAGE_POLICY`.
3. `FAILURE_CONSEQUENCE_COMPOSITION` + `UI_DAMAGE_PERCENT_ROUNDING` — implementation-safe spec에 필요할 경우 명시적으로 확정.
4. `REPRESENTATIVE_VISUAL_REGENERATION_AFTER_SYSTEM_SYNC`.
5. 사용자 `CURRENT_PLANNING_COMPLETE_DECLARATION` 전 제품 runtime 구현 금지.

## 21. 증거 경계

- `BS-ENHANCE-20260825-25`: `USER_APPROVED / PLANNING_CANON`.
- `BS-DAMAGE-20260825-26`: `USER_APPROVED / STRUCTURAL_CANON`.
- `BS-DAMAGE-20260826-28`: `USER_APPROVED / PLANNING_CANON`; exact enhancement-failure conditional damage curve만 소유하며 repair/customer-event/failure-composition/UI rounding은 미확정.
- `BS-CHRONICLE-20260825-27`: `USER_APPROVED / PLANNING_CANON`.
- `BS-ART-20260825-03`: `USER_APPROVED_DIRECTION`; final product asset/runtime approval은 아님.
- older CURRENT/MAX / repair / overhaul / damage-family numeric evidence: historical/partially superseded.
- Monte Carlo: `PLANNING_SIMULATION_EVIDENCE`; Decision28 + 새 repair 모델 뒤 경제 재검산 필요.
- Human/Player: `NOT_RUN`.
- Runtime implementation of Decisions25~28/Art03 mechanics: `NOT_RUN / BLOCKED`; current V2 runtime의 CURRENT/MAX·다중 precision은 implementation drift/history다.
