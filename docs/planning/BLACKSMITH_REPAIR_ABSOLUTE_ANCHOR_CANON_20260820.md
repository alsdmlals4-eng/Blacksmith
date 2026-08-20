# [현재 승인] Blacksmith 절대 수리 기준가 + 골드·재료 동시 소모

- Parent: `BS-ENHANCE-20260820-10~11`
- Decision: `BS-ENHANCE-20260820-12`
- 사용자 승인: `2026-08-20 KST / SWORD_BASE_R 800 승인 + 재료와 골드 양쪽 모두 소모 조건`
- 상태: `USER_APPROVED / USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 결정 목적

10~11은 일반 CURRENT 수리의 골드 견적 구조와 상대 구조 배율을 승인했다.

```text
missing_current_points = MAX - CURRENT

REPAIR_REFERENCE_COST
= STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER[primary_material]
× SECURED_BAND_MULTIPLIER[highest_secured_band]

gold_cost
= REPAIR_REFERENCE_COST
× (setup_fraction + variable_fraction × missing_current_points / 100)
```

12는 첫 Vertical Slice 대표 검의 절대 기준값과 **골드 + 일반 구조재료 동시 소모**를 정한다.

12는 11의 다음 부분만 최신 규칙으로 대체한다.

```text
[11 historical]
optional material offset
100% gold-only repair possible

[12 current]
gold is always consumed
common structural material is always consumed
material never discounts gold
```

11의 구조 배율·확보 밴드·`REPAIR_JOB_FATIGUE_COST=2`는 계속 유지한다.

## 2. 기존 경제 기준

대표 철검 POC 기준:

```text
기본 제작 골드 = 500
일반 재료 = 20개
COMMON_MATERIAL_SHADOW_VALUE = 50 gold / unit
기본 제작 기대원가 = 1,500 gold
```

수리만 별도 재료 환율을 만들지 않는다.

```text
COMMON_MATERIAL_SHADOW_VALUE = 50 gold / unit
```

상태: `REUSE_EXISTING_POC_SHADOW_VALUE / USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 3. SWORD 절대 Base R 대안

공통:

```text
setup_fraction = 0.05
variable_fraction = 0.65
iron material multiplier = 1.00
```

### A. `SWORD_BASE_R = 600`
- 골드 부담이 너무 약해 작은 손상마다 수리가 자동 정답이 될 위험.
- `LOWER_BOUND_TEST / REJECT_AS_BASELINE`.

### B. `SWORD_BASE_R = 800` — 채택
- 작은 수리는 부담이 있으나 접근 가능.
- 중·심각 손상에서 `수리 vs 추가 강화 vs 새 작품` 판단을 남김.
- MAX 흉터는 일반 수리로 지워지지 않으므로 CURRENT 수리를 과도하게 비싸게 만들 필요가 없음.
- `ADOPT / FIRST_VERTICAL_SLICE_ABSOLUTE_ANCHOR`.

### C. `SWORD_BASE_R = 1,000`
- 고위험 손상 작품에 MAX 흉터 + 성공률 불이익 + 높은 수리비가 동시에 걸려 폐기 압력이 과해질 위험.
- `UPPER_BOUND_TEST / REJECT_AS_BASELINE`.

승인 첫 테스트:

```text
STRUCTURAL_FAMILY_BASE_R
SWORD = 800 gold
```

이 값은 **첫 Vertical Slice/초기 강화 경제용 절대 anchor**이며 후기 전체 경제의 영구 기준이 아니다.

## 4. 골드 + 일반 구조재료 동시 소모 — 최신 계약

골드는 구조 난이도·재료 구조·확보 밴드 복잡도를 책임진다.

일반 구조재료는 실제 복구해야 하는 CURRENT 손상량을 책임진다.

```text
gold_cost = existing repair quote

common_material_units
= max(1, ceil(missing_current_points / 25))

material_shadow_burden
= common_material_units × 50

total_shadow_burden
= gold_cost + material_shadow_burden
```

불변식:

- `0 < CURRENT < MAX`인 일반 수리는 골드와 일반 구조재료를 **둘 다** 요구한다.
- 재료는 골드 비용을 낮추지 않는다.
- 골드는 재료 비용을 대체하지 않는다.
- 일반 구조재료가 없으면 해당 일반 수리를 실행할 수 없다.
- 단, 희귀 원재료·촉매·수식어 재료·MAX 복구재는 일반 CURRENT 수리에 요구하지 않는다.
- 일반 구조재료는 `COMMON / deterministic supply candidate`여야 하며 희귀 드롭 전용으로 만들지 않는다.
- MAX가 낮다는 이유만으로 재료 수량을 추가 배율하지 않는다.

## 5. 일반 구조재료 첫 테스트 수량

```text
missing 1~25pt  -> 1 unit
missing 26~50pt -> 2 units
missing 51~75pt -> 3 units
missing 76~99pt -> 4 units
```

이 수량은 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`다.

### 왜 secured band를 재료 수량에 다시 곱하지 않는가

골드 견적은 이미:

```text
STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER
× SECURED_BAND_MULTIPLIER
```

를 사용한다.

재료 수량까지 같은 축을 다시 적용하면 고급 재료·고강화 작품에 구조 복잡도를 이중 과금한다. 따라서 일반 구조재료는 **절대 결손 CURRENT 포인트만** 본다.

## 6. R=800 철검 대표 부담

| 상황 | 결손 CURRENT | 골드 | 재료 | 재료 shadow | 총 shadow burden | 제작원가 1,500 대비 |
|---|---:|---:|---:|---:|---:|---:|
| BUILD 경미 | 10 | 92 | 1 | 50 | 142 | 약 9% |
| FIRST_STOP | 20 | 158 | 1 | 50 | 208 | 약 14% |
| TENSION | 35 | 278 | 2 | 100 | 378 | 약 25% |
| HIGH | 60 | 528 | 3 | 150 | 678 | 약 45% |
| HIGH 심각 | 80 | 684 | 4 | 200 | 884 | 약 59% |

일반 수리는 MAX를 복구하지 않는다. 따라서 884 상당의 심각 CURRENT 수리 후에도 구조 흉터·성공률 불이익·미래 신규 강화 효과 불이익은 남는다.

## 7. 대표 주재료별 총 부담

### FIRST_STOP_POINT / missing 20 / material 1

```text
iron         158 gold + 1 material = 208 shadow burden
silver       190 gold + 1 material = 240 shadow burden
meteor_iron  238 gold + 1 material = 288 shadow burden
```

### TENSION / missing 35 / material 2

```text
iron         278 + 2 = 378
silver       333 + 2 = 433
meteor_iron  416 + 2 = 516
```

### HIGH_STAKES / missing 60 / material 3

```text
iron         528 + 3 = 678
silver       634 + 3 = 784
meteor_iron  792 + 3 = 942
```

### HIGH_STAKES / missing 80 / material 4

```text
iron         684 + 4 = 884
silver       821 + 4 = 1,021
meteor_iron  1,026 + 4 = 1,226
```

표의 `+N`은 `N × 50 gold shadow value` 일반 구조재료를 뜻한다.

## 8. 재료 소모 방식 대안 검토

### A. 수리마다 고정 1개
- 단순하지만 10pt와 80pt 손상의 물리적 차이를 거의 반영하지 못함.
- `REJECT`.

### B. 절대 결손 25pt당 1개 — 채택

```text
max(1, ceil(missing_current_points / 25))
```

- 실제 손상량과 직관적으로 연결.
- 골드의 구조/밴드 배율과 역할 중복이 적음.
- 첫 Vertical Slice에서 최대 4개라 유지보수 노가다화를 제한.
- `ADOPT`.

### C. secured band별 1/2/3/4개
- 골드가 이미 secured band를 반영해 이중 과금 가능.
- 동일 손상량이어도 밴드만 높아 재료가 급증.
- `REJECT`.

## 9. 5회 전체 적대적 검토

### Loop 1 — 골드+재료가 너무 비싼가
공격:
- 기존 800 골드 견적 위에 재료를 추가하면 12 초기안보다 부담이 커진다.

방어:
- 철검 HIGH 80pt도 총 shadow burden 884로 기본 제작 기대원가 1,500의 약 59%다.
- 일반 수리는 MAX를 지우지 않으므로 새 작품 제작과 완전히 동등한 가격까지 올릴 필요가 없다.

판정: `PASS_WITH_PLAYTEST`.

### Loop 2 — 재료 부족이 안전 행동을 봉쇄하는가
공격:
- 12 최신 규칙에서는 재료가 없으면 수리할 수 없다.

방어:
- 이는 사용자의 명시적 `재료+골드 동시 소모` 조건이다.
- 대신 요구 재료는 희귀 드롭이 아닌 **공통 구조재료**로 제한한다.
- 첫 수리 가능 시점 이전에 공통 재료의 결정적 획득/구매 경로가 있어야 한다.

재검토 조건:
- 첫 세션에서 재료 RNG 때문에 수리 선택 자체가 사라짐.
- 공통 구조재료가 강화 재료와 경쟁해 모든 선택을 봉쇄함.

판정: `PASS_WITH_SUPPLY_GUARDRAIL`.

### Loop 3 — 구조 난이도를 이중 과금하는가
공격:
- 고급 재료·고강화 작품은 이미 골드 R이 높다.

방어:
- 재료 수량은 `missing_current_points`만 사용한다.
- `MATERIAL_STRUCTURE_MULTIPLIER`, `SECURED_BAND_MULTIPLIER`, MAX 상태를 재료 수량에 다시 적용하지 않는다.

판정: `PASS`.

### Loop 4 — 25pt 경계 직전 수리가 정답이 되는가
공격:
- 25→26, 50→51, 75→76에서 재료가 1개 증가해 경계 직전 수리가 유리할 수 있다.

방어:
- 수리마다 고정 준비비와 피로도 2가 있으므로 여러 번 나눠 수리하면 작업 기회비용을 반복 지불한다.
- 부분수리는 여전히 금지이고 한 번 수리하면 CURRENT 전체가 MAX까지 회복된다.

재검토 조건:
- 플레이어가 재료 1개를 아끼려고 의도적으로 25/50/75 직전에 반복 수리함.

판정: `PASS_WITH_MONITORING`.

### Loop 5 — 800이 후기 경제에서 무의미해지는가
공격:
- 구형 +40~+60 경제는 수십만~백만 골드 단위다.

방어:
- `SWORD_BASE_R=800`은 `FIRST_VERTICAL_SLICE_ABSOLUTE_ANCHOR`로만 사용한다.
- 후기 HIGH_STAKES/MASTERY의 실제 경제 정본화 시 base R 또는 후기 경제 스케일을 별도 재검토한다.

판정: `PASS_WITH_SCOPE_LIMIT`.

## 10. UI 정보 계약 갱신

수리 판단 카드 기본 표시:

```text
CURRENT before -> CURRENT after(MAX)
MAX unchanged
gold cost
required common material units
workshop fatigue 2
remaining MAX scar / structural penalty
continue enhancement risk
```

금지:

- 재료를 골드 할인처럼 표시
- `골드 또는 재료` 선택형으로 표시
- 희귀 촉매를 일반 수리 필수 재료처럼 표시
- MAX가 복구되는 것처럼 표시

## 11. 재검토 조건

- 경미 손상마다 수리가 자동 정답으로 수렴.
- LOW CURRENT에서도 재료 때문에 수리가 거의 불가능.
- 일반 구조재료가 사실상 희귀 화폐가 됨.
- 25/50/75pt 직전 수리 타이밍 메타가 지배적.
- HIGH 80pt 총 부담이 새 대표 검 제작보다 지속적으로 높아짐.
- 후기 경제에서 `SWORD_BASE_R=800`이 무의미하게 작아짐.
- common material shadow value 50이 제작/강화 경제에서 변경됨.

## 12. 완료 경계

```text
BS-ENHANCE-20260820-12
= USER_APPROVED

SWORD_BASE_R = 800
COMMON_MATERIAL_SHADOW_VALUE = 50
COMMON_MATERIAL_UNITS = max(1, ceil(missing_current_points / 25))
REPAIR_JOB_FATIGUE_COST = 2

PAYMENT = GOLD_AND_COMMON_MATERIAL_BOTH_REQUIRED
OPTIONAL_MATERIAL_OFFSET = SUPERSEDED_BY_12
GOLD_ONLY_REPAIR = SUPERSEDED_BY_12
```

- 수치는 첫 Vertical Slice 테스트값이며 출시 최종 Balance가 아니다.
- Human/Player validation: `NOT_RUN`.
- 제품 구현: `BLOCKED`.
- 제품 코드·runtime data에는 아직 반영하지 않는다.
