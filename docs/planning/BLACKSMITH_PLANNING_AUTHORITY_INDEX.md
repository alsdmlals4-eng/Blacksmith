# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX`
- 기준: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~13 / BS-PROGRESSION-20260820-14~17 / BS-RESOURCE-20260824-18 / BS-REPAIR-20260824-19 / BS-OVERHAUL-20260824-20 / BS-DESTRUCTION-20260824-21`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`

## 1. 충돌 시 우선순위

1. 사용자의 최신 지시와 승인.
2. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`.
3. 2026-08-20/24 개별 Canon 문서. 같은 필드를 다루면 더 늦은 승인 Decision이 해당 필드만 부분 대체한다.
4. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장.
5. R2/R3 Game Bible·과거 PoC·구형 data/runtime.

새 `기획 완료` 사용자 선언 전 제품 code/data/scenes/assets/addons/project.godot 변경은 금지한다.

## 2. 운영 상태 동기화 규칙

의미 있는 기획 변경마다 GitHub와 Notion 모두에 아래를 갱신한다.

```text
CURRENT WORK ORDER
APPROVED DECISIONS
PROPOSED / UNRESOLVED ITEMS
Repo Main SHA / Sync State
```

GitHub 책임면:
- `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
- 이 Authority Index
- 관련 Canon

Notion 책임면:
- Project Home
- `01 · 프로젝트 전체 작업계획`
- 관련 핵심 시스템/Benchmark
- Project Registry properties

## 3. 현재 책임 원본

### Core
- `BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md` — 01.

### 실패·회복·내구도
- `BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md` — 02~04.
- `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` — 05~06.
- `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` — 07~09.
- `BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md` — CURRENT/MAX Budget.
- `BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md` — 13.

### 수리 경제
- `BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md` — 10~11.
- `BLACKSMITH_REPAIR_ABSOLUTE_ANCHOR_CANON_20260820.md` — 12.
- `BLACKSMITH_LATE_REPAIR_ECONOMY_CANON_20260824.md` — 19. **HIGH/MASTERY secured-band multiplier의 최신 owner**. 11의 `1.50/1.80`과 12의 해당 값 기반 후기 예시를 부분 대체한다.

### MAX 구조 구제
- `BLACKSMITH_MAX_OVERHAUL_CANON_20260824.md` — 20. **MAX 복구 예외의 최신 owner**. 일반 수리는 MAX를 복구하지 않으며, `highest_checkpoint>=60 / 0<MAX<=40 / same physical UID lifetime 1회` 조건에서만 `MAX +15 / after ceiling 60` 부분 대수선을 허용한다.

### DESTROYED 기록·추모·후계
- `BLACKSMITH_DESTRUCTION_UX_CANON_20260824.md` — 21. **물리 파괴 이후 UX/기록/후계 관계의 최신 owner**. `DESTROYED`는 같은 physical UID의 영구 종료이며 immutable history archive를 남긴다. Memorial은 archive의 선택적 강조 view이고, successor는 새 UID와 predecessor relation만 가지며 gameplay power/history를 상속하지 않는다.

### 진행·경제
- `BLACKSMITH_ENHANCEMENT_PROGRESSION_ECONOMY_CANON_20260820.md` — 14.
- `BLACKSMITH_LEVEL_TO_EXPERIENCE_BAND_CANON_20260820.md` — 15.
- `BLACKSMITH_CHECKPOINT_CADENCE_CANON_20260820.md` — 16.
- `BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md` — 17.
- `BLACKSMITH_ENHANCEMENT_PROFIT_CURVE_2026.md` — 경제 색인 + historical evidence.

### 일반 Resource Supply
- `BLACKSMITH_COMMON_RESOURCE_SUPPLY_CANON_20260824.md` — 18. `common_reinforcement_material / 보강재 / 50G / 상시 무제한 공급 / 강화 1~5 / 일반 수리 1~4`.

## 4. 진행 구조 권위 — 14~16

```text
MIN_LEVEL = +0
MAX_LEVEL = +100

+0~+9      INVESTMENT_RECOVERY_ZONE
+10        BREAK_EVEN_RECOVERY_POINT
+11~+100   PROFITABLE_ENHANCEMENT_ZONE
```

경험 밴드:

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

Checkpoint:

```text
CHECKPOINT_FLOORS = [10, 30, 60, 90]
```

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

Checkpoint는 DOWNGRADE 하한만 보호한다. CURRENT/MAX/recovery/attempt cost/repair cost는 리셋하지 않는다.

## 5. 실패 family 권위 — 13

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

## 6. 기본 성공률·회복 권위 — 17

```text
TARGET +1       100%
TARGET +2        97%
TARGET +3~+10    95% -> 86%
TARGET +11       82%
TARGET +12~+30   81% -> 72%
TARGET +31~+60   73% -> 69%
TARGET +61~+100  69% -> 64%
```

과거 `MASTERY 25~40%` working range는 17에서 대체된다.

Recovery:

```text
+6%p / same-target failure
soft cap 95%
owner = ITEM_UID + TARGET_LEVEL
hard guarantee = LEARN2 / BUILD4 / FIRST4 / TENSION5 / HIGH6 / MASTERY7
```

MAX 상태 페널티는 최종 성공률에 추가 적용한다.

## 7. 강화비·일반 재료 권위 — 17~18

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)
```

17의 내부 회계 단위:

```text
COMMON_ENHANCEMENT_MATERIAL_SHADOW_VALUE = 50G / balance unit
units = ceil(target / 20)
```

18에서 실제 player-facing 재료로 확정:

```text
CANONICAL_ID = common_reinforcement_material
PLAYER_NAME_KO = 보강재
SHOP_UNIT_PRICE = 50G
SUPPLY = WORKSHOP_MATERIAL_VENDOR / ALWAYS_AVAILABLE / NO_CAP
```

강화 수량:

```text
+1~20 1
+21~40 2
+41~60 3
+61~80 4
+81~100 5
```

`balance unit`은 플레이어에게 노출하지 않는다. 보강재는 새 currency가 아니라 실제 공통 공방 재료다.

## 8. MASTERY 손상 Budget — 17

```text
FAIL_DAMAGE           CURRENT -15~-25
FAIL_CRITICAL_DAMAGE  CURRENT -35~-60
MAX scar              MAX -6~-15
```

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 9. 일반 CURRENT 수리 권위 — 10~12 + 18~19

```text
missing = MAX - CURRENT

R = 800G
  × material_structure_mult
  × secured_band_mult

gold = R × (0.05 + 0.65 × missing/100)
required_common_material = max(1, ceil(missing/25))
PAYMENT = GOLD + COMMON_MATERIAL
CURRENT -> MAX
MAX unchanged
recovery unchanged
REPAIR_JOB_FATIGUE_COST = 2
```

현재 배율:

```text
material: iron 1.00 / silver 1.20 / meteor_iron 1.50
secured: LEARN·BUILD 1.00 / FIRST 1.10 / TENSION 1.25 / HIGH 2.25 / MASTERY 3.00
```

권위 주의:

```text
11 pre-19: HIGH 1.50 / MASTERY 1.80 = HISTORICAL_PRE_19_NUMERIC_EVIDENCE
19 current : HIGH 2.25 / MASTERY 3.00 = USER_APPROVED_TEST_BUDGET
```

18의 실제 일반 재료 mapping:

```text
missing 1~25  -> 보강재 1
missing 26~50 -> 보강재 2
missing 51~75 -> 보강재 3
missing 76~99 -> 보강재 4
```

- 골드와 보강재를 모두 지불하고 상호 대체하지 않는다.
- 보강재 수량에 material/secured 배율을 다시 곱하지 않는다.
- `iron / silver / meteor_iron`은 일반 보강재 직접 소비 대상이 아니다.
- 기본 공급은 RNG/희귀 드롭/일일 cap이 아닌 상시 구매다.
- 시장가·실제 다음 강화비·MAX 상태는 일반 CURRENT 수리 런타임 공식에 직접 넣지 않는다.
- 19 fresh 20,000-run: +100 mean `5,661,842G-eq`, pre-19 대비 약 `+0.095%`.

## 10. MAX 생애 1회 부분 대수선 권위 — 20

```text
eligibility:
  highest_checkpoint >= +60
  0 < MAX <= 40
  OVERHAUL_USED == false
  DESTROYED == false

effect:
  MAX = min(60, MAX + 15)
  CURRENT = MAX
  OVERHAUL_USED = true

cost:
  750,000G × material_structure_multiplier
  + 보강재 20
  + fatigue 5
```

불변:
- 같은 physical UID 생애 1회.
- 강화 단계/checkpoint/affix/기존 성능/recovery/history 유지.
- DESTROYED 부활 금지.
- 반복/완전 MAX 복구 금지.
- 대수선 후 MAX는 60 이하.
- 일반 CURRENT 수리는 계속 MAX를 복구하지 않음.

20의 planning comparison은 정책 민감도를 포함한다. 정확한 숫자보다 `lifetime partial = small macro impact / repeat full = material risk-curve erosion` 구조 결론을 사용하고, release 값은 Human test + 최종 Balance Lab에서 재생성한다.

## 11. DESTROYED 기록·추모·후계 권위 — 21

```text
CURRENT==0 or MAX==0
-> physical item DESTROYED permanently
-> immutable history record retained
```

핵심 계약:
- 파괴 순간에 before CURRENT/MAX, causal loss, 실제 0 도달 축, 직접 cause를 표시.
- 모든 DESTROYED UID는 immutable archive에 자동 보존.
- Archive는 age-based FIFO 삭제 금지.
- Memorial은 Archive 중 플레이어가 선택적으로 강조하는 view이며 power source가 아님.
- successor는 나중에 실제 새 작품을 만든 뒤 optional predecessor relation만 연결.
- `OLD_UID != NEW_UID`.
- enhancement/checkpoint/stat/affix/Artistry/Chronicle/recovery/CURRENT/MAX/material/price premium 상속 금지.
- 고객 작품 파괴 시 고객 identity/관계 기록은 유지하고 새 장비는 새 UID.
- 파괴 자체를 progression/resource farming으로 사용하지 않음.

Runtime Reality:
- historical `enhancement_session.gd`의 별도 destroy 확률과 DESTROY 시 progression/affix clear는 현재 제품 권위가 아니다.
- 현재 causal CURRENT/MAX destruction, immutable history archive, successor provenance runtime은 `IMPLEMENTATION_UNVERIFIED`.

## 12. 누적 기대원가·판매가 권위 — 17 + 19 + 20 검증

17의 고정 planning anchor를 유지한다. 19와 20의 simulation은 후기 수리/대수선 변경이 거시경제를 깨지 않는지 검증하는 비교 evidence이며 static price table을 runtime actual spend와 연결하지 않는다.

```text
independent simulation tolerance ≈ ±1.5%
SALE_PRICE_RUNTIME != ACTUAL_PLAYER_SPEND
```

| Level | Mean Expected Cost Anchor | Base Market Value |
|---:|---:|
| +0 | 1,500 | 1,000 |
| +5 | 2,322 | 1,900 |
| +9 | 4,759 | 4,600 |
| +10 | 5,779 | 5,800 |
| +11 | 7,023 | 7,400 |
| +20 | 30,713 | 34,400 |
| +30 | 96,006 | 117,100 |
| +40 | 219,565 | 285,400 |
| +50 | 419,230 | 578,500 |
| +60 | 712,986 | 1,055,200 |
| +70 | 1,168,898 | 1,846,900 |
| +80 | 1,907,274 | 3,204,200 |
| +90 | 3,235,853 | 5,824,500 |
| +100 | 5,632,657 | 11,265,300 |

구조 검증:

```text
+0~+9 expected profit < 0
+10 expected profit ~= 0
+11~+100 expected profit > 0
```

출시 전에는 19+20 통합 Balance Lab로 static table을 다시 검산한다.

## 13. 과거 숫자 처리

Current numeric authority가 아님:

```text
old +5 first-profit
old +60 last price anchor
old decade success pattern
old MASTERY 25~40%
old multi-step downgrade
old destroy RNG
pre-19 HIGH repair multiplier 1.50
pre-19 MASTERY repair multiplier 1.80
```

상태: `HISTORICAL_NUMERIC_EVIDENCE / RECALIBRATION_INPUT`.

## 14. 현재 승인사항

```text
01     강화 긴장감 + DDD가 PRIMARY CORE
02~04  risk + UID recovery + disclosure
05~09  checkpoint / CURRENT-MAX / destroy-at-zero
10~12  repair economy / GOLD+MATERIAL
13     failure family ratio
14     +10 break-even / +100 max
15     target-level band / +10 first floor
16     checkpoint [10,30,60,90]
17     success/recovery/attempt-cost/expected-cost/static-market anchors
18     common reinforcement material / 50G / deterministic vendor supply / enhancement+repair mapping
19     late repair economy / HIGH 2.25 / MASTERY 3.00 / fresh 20k planning Monte Carlo
20     one-lifetime partial MAX overhaul / +15 / ceiling60 / 750k×material + reinforcement20 + fatigue5
21     causal destruction / immutable archive / curated memorial / optional new-UID successor provenance / zero power inheritance
```

17·19·20의 숫자는 출시 최종이 아니라 `USER_APPROVED_TEST_BUDGET`. 18·21은 `USER_APPROVED / PLANNING_CANON`.

## 15. 현재 작업 순서

1. `MAX_LEVEL_PAYOFF` — +100 비수치 payoff.
2. `FIRST_10_MINUTES` — 첫 10분 pacing/UX/Visual 연결.
3. `PRECISION_CUSTOMER_LINK` — 정밀제작·고객/세계 payoff 연결.
4. `RELEASE_NEAR_VERTICAL_SLICE` — 통합 계약.

## 16. 구현자 확인 순서

1. 최신 사용자 지시.
2. Overlay에서 승인사항/현재 작업 순서 확인.
3. 실패=13, 진행=14~16, 숫자=17, 일반 수리=10~12+19, 일반 재료 공급=18, MAX 대수선=20, DESTROYED UX/기록=21 Canon 소비.
4. HIGH/MASTERY 수리 배율은 반드시 19를 우선한다.
5. MAX 복구 예외는 반드시 20만 사용하고 일반 수리/MAX 자동복구로 확대하지 않는다.
6. DESTROYED physical UID는 21에 따라 부활하지 않으며 successor에는 power/history를 복사하지 않는다.
7. 구형 data/runtime는 historical/reuse evidence로만 사용.
8. 새 `기획 완료` 전 제품 구현 금지.