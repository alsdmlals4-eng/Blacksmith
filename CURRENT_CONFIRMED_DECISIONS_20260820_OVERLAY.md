# [현재 우선 Overlay] Blacksmith 2026-08-20 Confirmed Decisions

- 상태: `CURRENT_PRIORITY_OVERLAY`
- 기준: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~13 / BS-PROGRESSION-20260820-14~15`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player validation: `NOT_RUN`

## 0. 현재 제품 계층

Blacksmith의 1차 코어는 **강화의 긴장감 + DDD**다.

```text
PRIMARY
강화 전 판단
→ 지금 멈춤 / 한 번 더 도전
→ 짧은 anticipation
→ 성공/실패 결과
→ 작품 상태 변화
→ 다음 강화 질문

SUPPORT
작품 UID·생애
정밀제작
고객/세계 생애주기
경제·하루 작업량
```

새 `기획 완료` 사용자 선언 전 제품 code/data/scene/runtime 구현은 시작하지 않는다.

## 1. 강화 실패·회복·정보 공개 — 02~04

### `BS-ENHANCE-20260820-02`
- 기본 강화 실패 골격은 `RISK_PLUS_RECOVERY_PROGRESS`.
- 모든 실패는 같은 작품 UID에 회복 진전을 남긴다.
- 계정 전체 transferable failstack은 기본 게임에서 사용하지 않는다.

### `BS-ENHANCE-20260820-03`
- 고위험 실패는 작품 손상을 만들 수 있다.
- 물리 작품 손실과 UID/역사 기록 삭제를 동일시하지 않는다.

### `BS-ENHANCE-20260820-04`
강화 전 최소 다음을 공개한다.

```text
현재 상태
최종 성공 확률
시도 비용
주요 실패 결과
현재 회복 효과
다음 확보점
```

핵심 확률을 숨겨 긴장감을 만들지 않는다.

## 2. 체크포인트·CURRENT/MAX·파괴 — 05~09

### `BS-ENHANCE-20260820-05`
- 주요 이정표는 확보점으로 보호.
- DOWNGRADE는 확보점 사이에서만 제한적으로 사용.
- 첫 테스트는 한 번 최대 1단계 하락.

### `BS-ENHANCE-20260820-06`
```text
CURRENT_DURABILITY_PERCENT = 0~100
CURRENT == 0 -> physical item DESTROYED
```
UID·이름·강화·소유·사건·파괴 원인·Chronicle provenance는 기록으로 보존한다.

### `BS-ENHANCE-20260820-07`
첫 Vertical Slice에는 별도 0% 파괴 방지 보험을 기본 제공하지 않는다.

### `BS-ENHANCE-20260820-08`
```text
0 <= CURRENT <= MAX <= 100
new item = 100 / 100
normal repair = CURRENT -> MAX
MAX = unchanged
```

- `FAIL_DAMAGE`: CURRENT 중심 손상.
- `FAIL_CRITICAL_DAMAGE`: CURRENT 심각 손상 + MAX 구조 흉터.
- CURRENT 또는 MAX 0이면 물리 작품 `DESTROYED`.
- MAX가 낮아지면 성공 기대와 미래 신규 강화 효과가 단계적으로 악화될 수 있다.
- 이미 얻은 성능은 MAX 손상만으로 소급 삭감하지 않는다.

MAX 상태 첫 테스트:

```text
MAX 81~100: success 0pp   / new effect 100%
MAX 61~80 : success -3pp  / new effect 100%
MAX 41~60 : success -6pp  / new effect 95%
MAX 21~40 : success -10pp / new effect 90%
MAX 1~20  : success -15pp / new effect 80%
```

### `BS-ENHANCE-20260820-09`
MAX 흉터는 성공 시 독립 주사위가 아니라 실패 결과군의 심각 결과에만 연결한다.

승인 범위:

```text
LEARN             0%
BUILD_CONFIDENCE  0%
FIRST_STOP_POINT  0~5%
TENSION           8~12%
HIGH_STAKES       12~20%
MASTERY           15~25%
```

별도 destroy roll은 없다.

## 3. 일반 CURRENT 수리 경제 — 10~12

### `BS-ENHANCE-20260820-10`
```text
missing_current_points = MAX - CURRENT

gold_cost
= REPAIR_REFERENCE_COST
× (0.05 + 0.65 × missing_current_points / 100)
```

- 일반 수리 1회로 `CURRENT = MAX`.
- MAX와 실패 누적 회복은 유지.
- 최종 시장가/수식어/연대기/고객 수요/실제 다음 강화비를 수리 공식에 직접 넣지 않는다.
- 부분수리·자동수리·수리 RNG·일반 MAX 복구는 첫 Vertical Slice 제외.

### `BS-ENHANCE-20260820-11`
```text
REPAIR_REFERENCE_COST
= STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER[primary_material]
× SECURED_BAND_MULTIPLIER[highest_secured_band]
```

주재료 구조 배율 첫 테스트:

```text
iron         1.00
silver       1.20
meteor_iron  1.50
```

확보 밴드 배율 첫 테스트:

```text
LEARN / BUILD_CONFIDENCE  1.00
FIRST_STOP_POINT          1.10
TENSION                   1.25
HIGH_STAKES               1.50
MASTERY                   1.80
```

```text
REPAIR_JOB_FATIGUE_COST = 2
```

11의 과거 `optional material offset / 100% gold-only repair`는 12에서 대체됐다.

### `BS-ENHANCE-20260820-12`
첫 Vertical Slice 대표 검:

```text
SWORD_BASE_R = 800 gold
COMMON_MATERIAL_SHADOW_VALUE = 50 gold / unit

common_material_units
= max(1, ceil((MAX - CURRENT) / 25))

PAYMENT = GOLD_COST + REQUIRED_COMMON_MATERIAL
```

첫 재료 수량:

```text
1~25pt   1개
26~50pt  2개
51~75pt  3개
76~99pt  4개
```

- 골드와 일반 구조재료를 둘 다 필수 소모.
- 재료는 골드를 할인하지 않고 골드는 재료를 대체하지 않는다.
- 재료 수량에 주재료 배율/secured band/MAX 상태를 다시 곱하지 않는다.
- `SWORD_BASE_R=800`은 `FIRST_VERTICAL_SLICE_ABSOLUTE_ANCHOR`; 후기 전체 경제 영구값이 아니다.

## 4. 실패 결과군 정확 비율 — 13

### `BS-ENHANCE-20260820-13`
실패가 이미 확정된 뒤의 조건부 family 비율:

```text
order = HOLD / DOWNGRADE / DAMAGE / CRITICAL

LEARN             100 /  0 /  0 /  0
BUILD_CONFIDENCE   90 /  0 / 10 /  0
FIRST_STOP_POINT   65 / 10 / 23 /  2
TENSION            45 / 10 / 35 / 10
HIGH_STAKES        30 / 15 / 39 / 16
MASTERY            20 / 20 / 40 / 20
```

- LEARN~HIGH_STAKES: `USER_APPROVED_TEST_BUDGET`.
- MASTERY: `USER_APPROVED_LATE_GAME_TEST_BUDGET`; 정확 CURRENT 손실량은 후속.

핵심 단일화:

```text
P(CRITICAL | failure)
= P(MAX scar | failure)
```

CRITICAL 뒤 별도 MAX-scar roll을 하지 않는다.

모든 실패에는 item-UID recovery가 증가한다. 첫 Vertical Slice에서 recovery는 성공률만 바꾸고 같은 밴드의 failure family ratio는 숨게 변경하지 않는다.

## 5. 강화 범위·경제 전환점 — 14

### `BS-PROGRESSION-20260820-14`
사용자 승인 구조:

```text
MIN_LEVEL = +0
MAX_LEVEL = +100

+0 ~ +9      INVESTMENT_RECOVERY_ZONE
+10          BREAK_EVEN_RECOVERY_POINT
+11 ~ +100   PROFITABLE_ENHANCEMENT_ZONE
```

`+10`은 대표 평범한 작품의 기본 공개시장 가치가 **누적 기대원가를 처음 회수하는 경제 이정표**다.

```text
EXPECTED_NET_PROFIT(+10) ~= 0
EXPECTED_NET_PROFIT(+11..+100) > 0
```

본전 계산에는 다음을 포함한다.

```text
기본 제작비
강화 골드/재료
실패 반복
DOWNGRADE 복구
강화 때문에 발생한 일반 수리 골드+재료 기대부담
해당 구간에서 실제 발생 가능한 파괴/재제작 기대비용
```

다음은 기본 강화 회수선과 분리한다.

```text
정밀제작/완성도
수식어/촉매
연대기
특정 고객 적합도
거래 채널 프리미엄
```

따라서 특수한 작품은 +10 이전에 실제 이익이 날 수 있지만, 그것은 강화 단계 자체의 회수선을 앞당긴 것으로 보지 않는다.

`+100`은 현재 최대 강화이며 기본 +101, 무한 초월/프레스티지는 없다. 별도 사용자 승인 없이는 추가하지 않는다.

과거 `+5 최초 흑자 / +60 마지막 가격 앵커`는 최신 구조와 충돌하므로 `HISTORICAL_NUMERIC_EVIDENCE / RECALIBRATION_INPUT`으로 강등한다.

## 6. 레벨 → 경험 밴드 및 첫 경제 checkpoint — 15

### `BS-PROGRESSION-20260820-15`
경험 밴드는 **현재 레벨이 아니라 target level**에 붙인다.

```text
TARGET +1~+2     = LEARN
TARGET +3~+10    = BUILD_CONFIDENCE
TARGET +11       = FIRST_STOP_POINT
TARGET +12~+30   = TENSION
TARGET +31~+60   = HIGH_STAKES
TARGET +61~+100  = MASTERY
```

따라서:

```text
CURRENT +10
= FIRST_ECONOMIC_STOP_STATE

TARGET +11
= FIRST_STOP_POINT attempt
```

+10을 먼저 확보해 평균 투자금을 회수한 뒤, +11부터 첫 수익을 위해 실제 영구 구조 위험을 여는 순서다.

### 첫 경제 checkpoint floor

```text
+10 = FIRST_ECONOMIC_CHECKPOINT_FLOOR
```

- +10 도달 후 제한 DOWNGRADE 때문에 +10 아래로 내려가지 않는다.
- +11 첫 수익 시도에는 DAMAGE/CRITICAL·시도비가 남으므로 공짜 도전은 아니다.
- +11에서 DOWNGRADE가 선택돼도 floor 때문에 실제 단계가 유지되면 UI는 checkpoint 보호를 반영한 최종 outcome으로 표시한다.

중요:

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

- +30은 TENSION/HIGH 경계일 뿐 자동 checkpoint가 아니다.
- +60은 HIGH/MASTERY 경계일 뿐 자동 checkpoint가 아니다.
- +20/+30/+40/+50/+60/+70/+80/+90의 checkpoint 여부는 16에서 별도 결정한다.

+100 성공 후 기본 강화 버튼은 종료되고 보유/판매/인계/전시/Chronicle/다음 작품으로 전환한다.

## 7. 현재 미확정

- +10 이후 checkpoint 최종 간격/cadence.
- +11~+100 단계별 판매가/누적 기대원가/기대수익 곡선.
- 단계별 성공률과 강화 비용.
- CURRENT 손실 범위 최종값 및 MASTERY 손실량.
- 검 이외 장비군별 base R.
- 후기 HIGH_STAKES/MASTERY 수리 경제 스케일.
- 일반 구조재료 공급량·획득 경로.
- 하루 총 피로도/작업량 출시값.
- MAX 대수선 여부와 대가.
- 파괴 작품 memorial/successor.
- +100 비수치 payoff.
- 첫 10분 실제 강화 수치와 UX.

## 8. 책임 원본

1. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md` — 최신 요약
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
12. `docs/planning/BLACKSMITH_ENHANCEMENT_PROFIT_CURVE_2026.md` — 최신 구조 + 과거 수치 증거
13. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장

## 9. 증거 경계

- 01~15 사용자 결정: current planning authority.
- 테스트 비율/계수: `NOT_FINAL_PRODUCT_BALANCE`.
- 새 +0~+100 가격/성공률 곡선: `NOT_FINAL / FOLLOW_UP_REQUIRED`.
- 제품 구현: `BLOCKED`.
- Human/Player evidence: `NOT_RUN`.
