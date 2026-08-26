# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX / POSTMERGE_PLANNING`
- current decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03`
- current owner: `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. 충돌 시 우선순위

1. 사용자의 최신 지시와 승인.
2. `AGENTS.md`.
3. `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` — Decisions25~29 / Art03 current player/system meaning.
4. `BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md` + `BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json` — current numeric durability/repair owner.
5. `BS-DAMAGE-20260826-28_DAMAGE_PROBABILITY_CURVE.md` + `BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json` — target-level damage base curve owner.
6. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md` current override.
7. 2026-08-20/24 개별 Canon — 새 owner와 충돌하지 않는 필드만 current; 충돌 필드는 역사/부분대체 evidence.
8. 실제 runtime/data/test evidence — 구현 사실을 증명하지만 PLAN Gate의 implementation drift가 최신 승인 기획을 덮어쓰지 않는다.
9. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장.
10. R2/R3 Game Bible·과거 PoC·구형 data/runtime.

```text
CURRENT_OWNER = docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
BS-ENHANCE-20260825-25
BS-DAMAGE-20260825-26
BS-DAMAGE-20260826-28
BS-REPAIR-20260826-29
BS-CHRONICLE-20260825-27
BS-ART-20260825-03
```

새 `기획 완료` 사용자 선언 전 제품 `data/scripts/scenes/assets/addons/project.godot` 변경은 금지한다.

## 2. 현재 핵심 계약

### Enhancement / Precision

```text
SUCCESS_LEVEL_DELTA = +1
TARGET = CURRENT + 1
+9 -> +10 = PRECISION_ENHANCEMENT
+10 PRECISION SUCCESS -> exactly one ITEM_KEYWORD
ITEM_KEYWORD machine owner = CATALYST_AFFIX
NO_FOURTH_AFFIX_SLOT
```

+20/+30/+40/+50은 current Precision Enhancement milestone이 아니다.

### Durability / Damage / Repair

Decision29이 같은 필드에서 Decision26의 pure four-state authority를 부분대체한다.

```text
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
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

Decision28 target base curve remains:

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
DAMAGE_CURVE_ANCHORS_PERCENT = [11:5, 30:6, 60:7, 90:8, 100:10]
DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
DAMAGE_CURVE_ROUNDING = NONE_CANON_EXACT_UI_ROUNDING_NOT_DECIDED
```

Decision29 temporary durability modifiers:

```text
NORMAL success 0pp / new effect ×1.00 / damage risk ×1.00
MINOR  success -3pp / new effect ×0.90 / damage risk ×1.25
MAJOR  success -7pp / new effect ×0.75 / damage risk ×1.75
DURABILITY_MODIFIERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

Hard guarantee remains 100%. Effect multiplier applies only newly added ordinary enhancement effect. Existing stats, +1 level delta and +10 keyword count are not reduced.

```text
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, STATE)
= Decision28_base_probability(TARGET) * Decision29_state_multiplier(STATE)
```

Repair contract:

```text
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY
DESTROYED_REPAIR_ALLOWED = FALSE
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
MAX_DURABILITY_RECOVERY = NOT_APPROVED
```

Temporary quality:

```text
EXCELLENT 20% -> post-scar MAX 100%
STANDARD  60% -> post-scar MAX 75%
POOR      20% -> post-scar MAX 50%
REPAIR_MINIMUM_CURRENT_GAIN_WHEN_POSSIBLE = 1
```

Temporary `MAX -1` scar chance:

| pre-repair state | +0~10 | +11~30 | +31~60 | +61~90 | +91~100 |
|---|---:|---:|---:|---:|---:|
| MINOR | 10% | 15% | 20% | 25% | 30% |
| MAJOR | 25% | 30% | 35% | 40% | 45% |

All detailed Decision29 numbers are `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`. `MAX_DURABILITY_FLOOR=1`; repair cannot directly destroy the item.

`FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED`; `UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED`.

### Customer/world damage

```text
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
```

Customer-event eligibility and exact probabilities remain unresolved. A later event damage implementation must feed the same Decision29 numeric durability authority rather than recreate a second damage state machine.

### Chronicle

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY
```

Durability damage, meaningful repair and MAX structural scar may be Chronicle events; routine enhancement clicks are not.

### Art direction

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

## 3. Current owner map

### 3.1 Current simplified owner

- `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` — current integrated meaning.
- `BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md` — Decision29 rationale, benchmark, structural rules, temp Budget boundaries.
- `BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json` — Decision29 machine-readable model.
- `BS-DAMAGE-20260826-28_DAMAGE_PROBABILITY_CURVE.md` — Decision28 target curve rationale/scope.
- `BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json` — Decision28 target anchors/interpolation.

### 3.2 Preserved progression where non-conflicting

- `BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md` — PRIMARY CORE enhancement tension + DDD.
- `BLACKSMITH_ENHANCEMENT_PROGRESSION_ECONOMY_CANON_20260820.md` — +10 break-even / +100 range; economy needs Decision29 rebase.
- `BLACKSMITH_LEVEL_TO_EXPERIENCE_BAND_CANON_20260820.md` — target bands only.
- `BLACKSMITH_CHECKPOINT_CADENCE_CANON_20260820.md` — `CHECKPOINT_FLOORS=[10,30,60,90]`.
- `BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md` — success/recovery/attempt-cost planning inputs where non-conflicting.
- `BLACKSMITH_COMMON_RESOURCE_SUPPLY_CANON_20260824.md` — enhancement supply where non-conflicting.
- `BLACKSMITH_MAX_LEVEL_PAYOFF_CANON_20260824.md` — +100 terminal identity/payoff.

### 3.3 Durability / repair historical evidence

- `BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md` — disclosure/recovery principles only where non-conflicting.
- `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` — checkpoint parts retained; old durability numbers historical.
- `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` — historical; not Decision29.
- `BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md` — old budget only.
- `BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md` — old DAMAGE/CRITICAL composition historical.
- `BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md` / `BLACKSMITH_REPAIR_ABSOLUTE_ANCHOR_CANON_20260820.md` / `BLACKSMITH_LATE_REPAIR_ECONOMY_CANON_20260824.md` — old repair economy evidence; formulas not fallback.
- `BLACKSMITH_MAX_OVERHAUL_CANON_20260824.md` — `SUPERSEDED`; no current MAX recovery approved.

### 3.4 Destruction / item life

Physical UID death, immutable archive, curated memorial, optional new-UID successor and zero power inheritance remain current principles. Current terminal trigger is numeric:

```text
CURRENT_DURABILITY == 0 -> DESTROYED
```

### 3.5 First session / customer causality

Pacing, STOP/PUSH and delayed same-UID causality remain. CURRENT/MAX teaching must now use Decision29's **visible current numeric model**, not the historical hidden MAX-scar model.

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

## 5. Success / recovery / resource status

Existing planning input remains unless Decision29 sensitivity later changes it:

```text
+1       100%
+2        97%
+3~+10    95% -> 86%
+11       82%
+12~+30   81% -> 72%
+31~+60   73% -> 69%
+61~+100  69% -> 64%
recovery = +6pp / same-target failure
soft cap 95%
hard guarantee = LEARN2 / BUILD4 / FIRST4 / TENSION5 / HIGH6 / MASTERY7
```

Common reinforcement material planning input:

```text
+1~20 1
+21~40 2
+41~60 3
+61~80 4
+81~100 5
```

Decision29 requires economy/sensitivity revalidation before final balance claims.

## 6. Current unresolved gates

```text
CUSTOMER_EVENT_DAMAGE_POLICY
- eligible event classes
- event-specific probability/deterministic causes
- same numeric durability resolver integration

REPAIR_ECONOMY_REBASE
- gold/material/fatigue cost after Decision29
- sensitivity of repair vs damaged push vs stop

FAILURE_CONSEQUENCE_COMPOSITION
- whether failed enhancement can combine damage with DOWNGRADE/HOLD/other consequence

UI_DAMAGE_PERCENT_ROUNDING
- display precision only; no second resolver probability authority
```

Decision29 closes `MINOR_MAJOR_REPAIR_MODEL` structural behavior and `MAJOR_ENHANCEMENT_ELIGIBILITY`. Exact tuning remains temporary.

## 7. Current work order

```text
1. CUSTOMER_WORLD_EVENT_DAMAGE_POLICY
2. REPAIR_ECONOMY_REBASE + durability/economy sensitivity simulation
3. FAILURE_CONSEQUENCE_COMPOSITION + UI_DAMAGE_PERCENT_ROUNDING if needed
4. REPRESENTATIVE_VISUAL_REGENERATION_AFTER_SYSTEM_SYNC
5. full planning adversarial review
6. CURRENT_PLANNING_COMPLETE user declaration
7. runtime implementation plan refresh and TDD migration
```

## 8. Runtime reality / drift

Current V2 runtime includes `current_durability`, `max_durability` and old failure/repair semantics. Field-name overlap does not prove Decision29 implementation.

```text
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = NOT_RUN / BLOCKED
OLD_V2_RUNTIME = IMPLEMENTATION_DRIFT / HISTORICAL_RUNTIME_TRUTH
```

Do not mutate protected product paths while Work Mode remains PLAN.

## 9. Operational synchronization

Meaningful planning changes update current GitHub owner/index/handoff, Notion Human Home + Enhancement/Durability/Economy views, AI/System operational metadata, and migration-only Sheet same-ID row when needed.

Pre-existing PR #196 remains `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`.

## 10. Evidence ceiling

```text
PLANNING_DESIGN = USER_APPROVED
DAMAGE_CURVE_NUMBERS = USER_APPROVED / BS-DAMAGE-20260826-28
DURABILITY_REPAIR_STRUCTURE = USER_APPROVED / BS-REPAIR-20260826-29
DURABILITY_REPAIR_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
REPAIR_ECONOMY = NOT_FINAL
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
RUNTIME_IMPLEMENTATION = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_GEOMETRY = NOT_RUN
```
