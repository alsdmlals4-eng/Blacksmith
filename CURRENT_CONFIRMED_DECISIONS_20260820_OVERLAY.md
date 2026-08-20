# [현재 우선 Overlay] Blacksmith 2026-08-20 Confirmed Decisions

- 상태: `CURRENT_PRIORITY_OVERLAY`
- 기준: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~13 / BS-PROGRESSION-20260820-14~17`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player validation: `NOT_RUN`

## 0. 현재 제품 계층

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

새 `기획 완료` 사용자 선언 전 `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 제품 구현은 시작하지 않는다.

## 1. 실패·회복·정보 공개 — 02~04

### `BS-ENHANCE-20260820-02`
- 기본 골격: `RISK_PLUS_RECOVERY_PROGRESS`.
- 모든 실패는 실제 비용/손실과 같은 작품 UID의 회복 진전을 남긴다.
- account-wide transferable failstack은 기본 게임에서 금지.

### `BS-ENHANCE-20260820-03`
- 고위험 실패는 작품 손상을 만들 수 있다.
- 물리 작품 파괴와 UID/역사 삭제를 동일시하지 않는다.

### `BS-ENHANCE-20260820-04`
강화 전 최소 공개:

```text
현재 상태
최종 성공률
시도 비용
최종 실패 outcome 확률
CURRENT/MAX 위험
현재 recovery 효과
다음 checkpoint/이정표
```

핵심 확률을 숨겨 긴장감을 만들지 않는다.

## 2. Checkpoint·CURRENT/MAX·파괴 — 05~09

### `BS-ENHANCE-20260820-05`
- 주요 확보점은 영구 DOWNGRADE floor.
- floor 사이에서만 제한 DOWNGRADE.
- 첫 테스트 한 번 최대 1단계 하락.
- 큰 DOWNGRADE와 큰 durability 손상을 기본 중첩하지 않는다.

### `BS-ENHANCE-20260820-06~08`

```text
0 <= CURRENT <= MAX <= 100
new item = 100 / 100
normal repair = CURRENT -> MAX
MAX unchanged
CURRENT == 0 or MAX == 0 -> physical DESTROYED
```

- `FAIL_DAMAGE`: CURRENT 중심.
- `FAIL_CRITICAL_DAMAGE`: CURRENT 큰 손상 + MAX 구조 흉터.
- 물리 파괴 후에도 UID·이름·강화/소유/사건/파괴 원인·Chronicle provenance는 기록 보존.
- 성공 강화·날짜 경과·판매/전시 자체는 durability를 자동 감소시키지 않는다.

MAX 상태 첫 테스트:

```text
MAX 81~100: success  0pp / new effect 100%
MAX 61~80 : success -3pp / new effect 100%
MAX 41~60 : success -6pp / new effect 95%
MAX 21~40 : success -10pp / new effect 90%
MAX 1~20  : success -15pp / new effect 80%
```

이미 얻은 성능은 MAX 흉터만으로 소급 삭감하지 않는다.

### `BS-ENHANCE-20260820-09`
MAX 흉터는 실패의 `CRITICAL` family에 결합한다.

```text
LEARN             0%      / MAX loss 0
BUILD_CONFIDENCE  0%      / MAX loss 0
FIRST_STOP_POINT  0~5%    / MAX loss 1~3
TENSION           8~12%   / MAX loss 2~5
HIGH_STAKES       12~20%  / MAX loss 4~10
MASTERY           15~25%  / MAX loss 6~15
```

별도 destroy roll은 금지. 실제 CURRENT/MAX가 0에 도달했을 때만 파괴한다.

## 3. 일반 CURRENT 수리 — 10~12

### `BS-ENHANCE-20260820-10`

```text
missing = MAX - CURRENT

gold_cost
= REPAIR_REFERENCE_COST
× (0.05 + 0.65 × missing / 100)
```

- 한 번의 `REPAIR_JOB`으로 CURRENT=MAX.
- MAX/recovery unchanged.
- 부분수리·자동수리·수리 RNG·일반 MAX 복구는 첫 Vertical Slice 제외.

### `BS-ENHANCE-20260820-11`

```text
REPAIR_REFERENCE_COST
= STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER
× SECURED_BAND_MULTIPLIER
```

첫 배율:

```text
material: iron 1.00 / silver 1.20 / meteor_iron 1.50
secured: LEARN·BUILD 1.00 / FIRST 1.10 / TENSION 1.25 / HIGH 1.50 / MASTERY 1.80
REPAIR_JOB_FATIGUE_COST = 2
```

구형 `restore=5`와 11의 optional material offset/gold-only 규칙은 current authority가 아니다.

### `BS-ENHANCE-20260820-12`

```text
SWORD_BASE_R = 800G
COMMON_MATERIAL_SHADOW_VALUE = 50G/unit
common_material_units = max(1, ceil((MAX-CURRENT)/25))
PAYMENT = GOLD + REQUIRED_COMMON_MATERIAL
```

재료 수량:

```text
1~25pt 1개 / 26~50pt 2개 / 51~75pt 3개 / 76~99pt 4개
```

## 4. 실패 결과군 정확 비율 — 13

실패가 이미 확정된 뒤의 조건부 비율:

```text
order = HOLD / DOWNGRADE / DAMAGE / CRITICAL

LEARN             100 /  0 /  0 /  0
BUILD_CONFIDENCE   90 /  0 / 10 /  0
FIRST_STOP_POINT   65 / 10 / 23 /  2
TENSION            45 / 10 / 35 / 10
HIGH_STAKES        30 / 15 / 39 / 16
MASTERY            20 / 20 / 40 / 20
```

핵심:

```text
P(CRITICAL | failure) = P(MAX scar | failure)
```

CRITICAL 뒤 별도 MAX-scar/destroy roll을 하지 않는다.

## 5. 강화 범위·경제 전환점 — 14

```text
MIN_LEVEL = +0
MAX_LEVEL = +100

+0~+9      INVESTMENT_RECOVERY_ZONE
+10        BREAK_EVEN_RECOVERY_POINT
+11~+100   PROFITABLE_ENHANCEMENT_ZONE
```

+10 누적 기대원가 포함:

```text
기본 제작
강화 골드/재료
실패 반복
DOWNGRADE 복구
강화 유발 CURRENT 수리
해당 구간 실제 파괴/재제작 기대비용
```

정밀제작·수식어·Chronicle·특수 고객/거래 채널 프리미엄은 별도 가치축.

+100 이후 기본 +101/무한 초월은 별도 사용자 승인 없이는 추가하지 않는다.

## 6. Target level → 경험 밴드 — 15

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

밴드는 current level이 아니라 **target level**에 붙인다.

```text
CURRENT +10 = FIRST_ECONOMIC_STOP_STATE
TARGET +11  = FIRST_STOP_POINT ATTEMPT
```

+10을 먼저 확보한 뒤 +11부터 첫 수익과 영구 구조 위험을 충돌시킨다.

## 7. Checkpoint cadence — 16

```text
CHECKPOINT_FLOORS = [10, 30, 60, 90]
```

역할:

```text
+10 경제 본전 확보
+30 TENSION 완료
+60 HIGH_STAKES 완료
+90 FINAL MASTERY PUSH staging
```

Checkpoint는 오직 DOWNGRADE floor다.

```text
resolved_level = max(current_level - 1, highest_secured_floor)
```

다음은 checkpoint가 변경하지 않는다.

```text
CURRENT / MAX / MAX scar
recovery
attempt cost
repair cost
UID/history
```

중요:

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

+90은 band boundary가 아니며 최종 +91~+100 러시용 의도적 floor다.

## 8. +0~+100 성공률·강화비·경제 — 17

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

### 기본 성공률

```text
+1       100%
+2        97%
+3~+10    95% -> 86%
+11       82%
+12~+30   81% -> 72%
+31~+60   71% -> 67%
+61~+100  66% -> 60%
```

과거 working의 `MASTERY 25~40%` 범위는 current risk와 결합 시 MAX 파괴를 과도하게 만들어 17에서 대체한다.

### 실패 회복

```text
+6%p per failure
soft cap 95%
owner = ITEM_UID + TARGET_LEVEL
```

hard guarantee:

```text
LEARN 2 failures
BUILD 4
FIRST 4
TENSION 5
HIGH 6
MASTERY 7
```

### 강화 시도 골드

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)
```

대표:

```text
+10 830G / +30 6,270G / +60 22,440G / +90 47,310G / +100 57,440G
```

### 일반 강화 재료

```text
COMMON_ENHANCEMENT_MATERIAL_SHADOW_VALUE = 50G/unit
units = ceil(target / 20)

+1~20 1 / +21~40 2 / +41~60 3 / +61~80 4 / +81~100 5
```

이는 balance accounting bundle이며 새 player-facing currency가 아니다.

### MASTERY CURRENT 손상 첫 값

```text
DAMAGE    -15~-25 CURRENT
CRITICAL  -35~-60 CURRENT
MAX scar  -6~-15 MAX  # 09 유지
```

### 20,000-run 대표 철검 planning simulation

```text
Level   Mean Expected Cost   P90 Cost     Base Market Value
+10          5,770             6,530           5,800
+20         30,736            36,080          34,400
+30         96,163           112,041         117,300
+40        223,091           259,170         290,000
+50        427,991           492,494         590,600
+60        728,187           832,155       1,077,700
+70      1,189,743         1,341,383       1,879,800
+80      1,942,055         2,978,285       3,262,700
+90      3,276,228         5,191,919       5,897,200
+100     5,759,280        10,348,306      11,518,600
```

+100 planning evidence:

```text
mean attempts ≈ 282.7
mean physical destruction/recraft ≈ 1.07
```

기본 판매가는 actual player spend에 동적으로 연동하지 않는다.

```text
SALE_PRICE_RUNTIME != ACTUAL_PLAYER_SPEND
```

offline Balance Lab가 reference expected-cost 분포로 static level price table을 생성한다.

위험 프리미엄 목표:

```text
+10 0% / +11 5% / +20 12% / +30 22% / +40 30%
+50 38% / +60 48% / +70 58% / +80 68% / +90 80% / +100 100%
```

## 9. 과거 숫자 지위

다음 2026-07 값은 current numeric canon이 아니다.

```text
+5 최초 흑자
+60 마지막 가격 앵커
old success decade pattern
old multi-step downgrade
old destroy RNG
```

상태:

```text
HISTORICAL_NUMERIC_EVIDENCE / RECALIBRATION_INPUT
```

## 10. 현재 미확정 / 다음 순서

1. 일반 강화/수리 재료의 실제 공급량·획득 경로.
2. 후기 HIGH/MASTERY 수리 절대경제 재검증.
3. MAX 대수선 필요 여부와 대가.
4. 파괴 작품 memorial/successor UX.
5. +100 비수치 payoff.
6. 첫 10분 실제 pacing/UX/Visual 연결.
7. 정밀제작·고객/세계 payoff 연결.
8. release-near Vertical Slice 계약.

## 11. 책임 원본

1. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
2. `docs/planning/BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md`
3. `docs/planning/BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md`
4. `docs/planning/BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md`
5. `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md`
6. `docs/planning/BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md`
7. `docs/planning/BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md`
8. `docs/planning/BLACKSMITH_REPAIR_ABSOLUTE_ANCHOR_CANON_20260820.md`
9. `docs/planning/BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md`
10. `docs/planning/BLACKSMITH_ENHANCEMENT_PROGRESSION_ECONOMY_CANON_20260820.md`
11. `docs/planning/BLACKSMITH_LEVEL_TO_EXPERIENCE_BAND_CANON_20260820.md`
12. `docs/planning/BLACKSMITH_CHECKPOINT_CADENCE_CANON_20260820.md`
13. `docs/planning/BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md`
14. `docs/planning/BLACKSMITH_ENHANCEMENT_PROFIT_CURVE_2026.md` — current curve index + historical evidence
15. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장

## 12. 증거 경계

- 01~17 current planning authority.
- 17 numeric values: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- 20,000-run model: `PLANNING_SIMULATION_EVIDENCE`.
- Human/Player: `NOT_RUN`.
- Runtime implementation: `BLOCKED`.
