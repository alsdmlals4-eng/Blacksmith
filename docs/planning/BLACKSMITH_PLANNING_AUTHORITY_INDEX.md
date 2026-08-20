# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX`
- 기준: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~13 / BS-PROGRESSION-20260820-14~17`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`

## 1. 충돌 시 우선순위

1. 사용자의 최신 지시와 승인.
2. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`.
3. 2026-08-20 개별 Canon 문서.
4. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장.
5. R2/R3 Game Bible·과거 PoC·구형 data/runtime.

새 `기획 완료` 사용자 선언 전 제품 code/data/scenes/assets/addons/project.godot 변경은 금지한다.

## 2. 책임 원본

### 코어
- `BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md` — 01, 강화 긴장감 + DDD.

### 실패·회복·내구도
- `BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md` — 02~04.
- `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` — 05~06.
- `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` — 07~09.
- `BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md` — CURRENT/MAX 첫 Budget.
- `BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md` — 13 failure family.

### 수리
- `BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md` — 10~11.
- `BLACKSMITH_REPAIR_ABSOLUTE_ANCHOR_CANON_20260820.md` — 12.

### 진행·경제
- `BLACKSMITH_ENHANCEMENT_PROGRESSION_ECONOMY_CANON_20260820.md` — 14, +10 본전/+100 최대.
- `BLACKSMITH_LEVEL_TO_EXPERIENCE_BAND_CANON_20260820.md` — 15, target-level band + +10 first floor.
- `BLACKSMITH_CHECKPOINT_CADENCE_CANON_20260820.md` — 16, floor `[10,30,60,90]`.
- `BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md` — 17, 성공률/회복/강화비/expected cost/static sale value.
- `BLACKSMITH_ENHANCEMENT_PROFIT_CURVE_2026.md` — current 경제 색인 + historical numeric evidence.
- `BLACKSMITH_ENHANCEMENT_TENSION_AND_DDD_REWARD_LADDER_20260820.md` — DDD 경험 역할.

## 3. 강화 진행 권위

```text
MIN_LEVEL = 0
MAX_LEVEL = 100

+0~+9      INVESTMENT_RECOVERY_ZONE
+10        BREAK_EVEN_RECOVERY_POINT
+11~+100   PROFITABLE_ENHANCEMENT_ZONE
```

`+100` 이후 +101/무한 초월은 기본 시스템에 없다.

## 4. 경험 밴드 권위 — 15

경험 밴드는 **target level 기준**이다.

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

```text
CURRENT +10 = FIRST_ECONOMIC_STOP_STATE
TARGET +11  = FIRST_STOP_POINT ATTEMPT
```

## 5. Checkpoint 권위 — 16

```text
CHECKPOINT_FLOORS = [10, 30, 60, 90]
```

- +10: 경제 본전 확보.
- +30: TENSION 완료.
- +60: HIGH_STAKES 완료.
- +90: 최종 MASTERY push staging.

Checkpoint는 오직 DOWNGRADE 하한이다.

```text
resolved_level = max(current_level - 1, highest_secured_floor)
```

Checkpoint로 CURRENT/MAX/recovery/attempt cost/repair cost를 리셋하지 않는다.

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

## 6. 실패 family 권위 — 13

```text
order = HOLD / DOWNGRADE / DAMAGE / CRITICAL

LEARN             100 /  0 /  0 /  0
BUILD_CONFIDENCE   90 /  0 / 10 /  0
FIRST_STOP_POINT   65 / 10 / 23 /  2
TENSION            45 / 10 / 35 / 10
HIGH_STAKES        30 / 15 / 39 / 16
MASTERY            20 / 20 / 40 / 20
```

```text
P(CRITICAL | failure) = P(MAX scar | failure)
```

CRITICAL 뒤 별도 MAX-scar/destroy roll 금지.

## 7. 기본 성공률·회복 권위 — 17

```text
TARGET +1       100%
TARGET +2        97%
TARGET +3~+10    95% -> 86%
TARGET +11       82%
TARGET +12~+30   81% -> 72%
TARGET +31~+60   71% -> 67%
TARGET +61~+100  66% -> 60%
```

기존 working의 `MASTERY 25~40%` 범위는 17에서 대체된다.

회복:

```text
+6%p / failure
soft cap 95%
owner = ITEM_UID + TARGET_LEVEL
```

hard guarantee:

```text
LEARN 2 / BUILD 4 / FIRST 4 / TENSION 5 / HIGH 6 / MASTERY 7 failures
```

MAX 상태 페널티는 최종 성공률에 추가 적용한다.

## 8. 강화비 권위 — 17

골드:

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)
```

일반 재료 balance unit:

```text
shadow = 50G/unit
units = ceil(target / 20)
```

```text
+1~20 1
+21~40 2
+41~60 3
+61~80 4
+81~100 5
```

`unit`은 새 player currency가 아니라 existing ordinary material을 후속 공급/recipe Decision에서 매핑하기 위한 accounting bundle이다.

정밀제작/수식어/촉매 비용은 기본 강화 곡선에서 분리한다.

## 9. MASTERY 손상 첫 Budget — 17

```text
FAIL_DAMAGE           CURRENT -15~-25
FAIL_CRITICAL_DAMAGE  CURRENT -35~-60
MAX scar              MAX -6~-15  # 09 유지
```

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 10. 기본 판매가/기대원가 권위 — 17

대표 철검 20,000-run planning simulation:

```text
Level   Mean Cost     P90 Cost      Base Sale
+10        5,770         6,530          5,800
+20       30,736        36,080         34,400
+30       96,163       112,041        117,300
+40      223,091       259,170        290,000
+50      427,991       492,494        590,600
+60      728,187       832,155      1,077,700
+70    1,189,743     1,341,383      1,879,800
+80    1,942,055     2,978,285      3,262,700
+90    3,276,228     5,191,919      5,897,200
+100   5,759,280    10,348,306     11,518,600
```

+100 reference:

```text
mean attempts ≈ 282.7
mean physical destruction/recraft ≈ 1.07
```

기본 판매가는 actual spend에 동적으로 연동하지 않는다.

```text
SALE_PRICE_RUNTIME != ACTUAL_PLAYER_SPEND
```

Balance Lab가 expected-cost 분포를 이용해 static level price table을 생성한다.

위험 프리미엄 목표:

```text
+10 0% / +11 5% / +20 12% / +30 22% / +40 30%
+50 38% / +60 48% / +70 58% / +80 68% / +90 80% / +100 100%
```

## 11. 수리 권위 요약 — 10~12

```text
missing = MAX - CURRENT

R = SWORD_BASE_R 800
  × material_structure_mult
  × secured_band_mult

gold = R × (0.05 + 0.65 × missing/100)
common_material = max(1, ceil(missing/25))
PAYMENT = GOLD + COMMON_MATERIAL
CURRENT -> MAX
MAX unchanged
recovery unchanged
REPAIR_JOB_FATIGUE_COST = 2
```

배율:

```text
material: iron 1.00 / silver 1.20 / meteor_iron 1.50
secured: LEARN·BUILD 1.00 / FIRST 1.10 / TENSION 1.25 / HIGH 1.50 / MASTERY 1.80
```

## 12. 과거 숫자 처리

다음은 current numeric canon이 아니다.

```text
old +5 first-profit rule
old +60 last price anchor
old decade success pattern
old multi-step downgrade
old destroy RNG
```

상태:

```text
HISTORICAL_NUMERIC_EVIDENCE / RECALIBRATION_INPUT
```

## 13. 현재 열린 Critical Decision

우선순위:

1. 일반 강화/수리 재료의 실제 공급량·획득 경로.
2. 후기 HIGH/MASTERY 수리 절대경제 재검증.
3. MAX 대수선 여부와 대가.
4. 파괴 작품 memorial/successor UX.
5. +100 비수치 payoff.
6. 첫 10분 pacing/UX/Visual 연결.
7. 정밀제작·고객/세계 payoff 연결.
8. release-near Vertical Slice 계약.

## 14. 상태 해석

| 상태 | 의미 |
|---|---|
| `USER_APPROVED` | 구조/방향 사용자 승인 |
| `USER_APPROVED_TEST_BUDGET` | 첫 Balance 입력, 출시 최종값 아님 |
| `PLANNING_SIMULATION_EVIDENCE` | runtime/human evidence가 아닌 planning model |
| `HISTORICAL_NUMERIC_EVIDENCE` | 과거 수치 증거 |
| `BLOCKED` | 제품 구현 금지 |

## 15. 구현자 확인 순서

1. 최신 사용자 지시.
2. Overlay.
3. 실패=13, 진행=14~16, 숫자=17, 수리=10~12 Canon 확인.
4. 구형 data/runtime는 historical/reuse evidence로만 사용.
5. 새 `기획 완료` 전 제품 구현 금지.
