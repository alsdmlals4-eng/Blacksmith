# [제안] Blacksmith 절대 수리 기준가·일반 재료 Shadow Value

- Parent: `BS-ENHANCE-20260820-10~11`
- Proposed Decision: `BS-ENHANCE-20260820-12`
- 상태: `PROPOSED_ONLY / USER_DECISION_REQUIRED`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 결정 목적

`BS-ENHANCE-20260820-10~11`은 일반 수리 구조를 다음처럼 승인했다.

```text
missing_current_points = MAX - CURRENT

repair_cost
= REPAIR_REFERENCE_COST
× (setup_fraction + variable_fraction × missing_current_points / 100)

REPAIR_REFERENCE_COST
= STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER
× SECURED_BAND_MULTIPLIER
```

12는 첫 Vertical Slice 대표 장비군인 `SWORD`의 절대 기준값과 일반 재료의 shadow value를 정한다.

이번 결정은 전체 후기 경제의 영구 기준을 고정하지 않는다. 특히 구형 +40~+60 판매가 곡선까지 단일 `SWORD_BASE_R`로 커버한다고 주장하지 않는다.

## 2. 기존 경제 기준

대표 철검 현재 POC 경제 기준:

```text
기본 제작 골드 = 500
일반 재료 = 20개
일반 재료 shadow value = 50 gold / unit
기본 제작 기대원가 = 1,500 gold
```

현재 재료 shadow value 50은 강화 누적 기대원가와 수익곡선에 이미 사용되는 값이다.

따라서 수리만 다른 shadow value를 만들지 않고 `COMMON_MATERIAL_SHADOW_VALUE = 50`을 재사용하는 안을 우선한다.

## 3. Base R 대안 비교

공통 조건:

```text
setup_fraction = 0.05
variable_fraction = 0.65
iron material multiplier = 1.00
```

### A. 안전 우선형 — `SWORD_BASE_R = 600`

| 상황 | 결손 CURRENT | secured band | 견적 |
|---|---:|---:|---:|
| BUILD 경미 | 10 | 1.00 | 69 |
| FIRST_STOP | 20 | 1.10 | 119 |
| TENSION | 35 | 1.25 | 208 |
| HIGH | 60 | 1.50 | 396 |
| HIGH 심각 | 80 | 1.50 | 513 |

장점:
- 수리 접근성이 높다.

문제:
- 경미·중간 손상 수리가 너무 싼 유지비로 느껴질 가능성이 높다.
- 실패 후 `그대로 한 번 더`보다 수리부터 누르는 경향이 강해질 수 있다.

판정: `REJECT_AS_BASELINE / LOWER_BOUND_TEST`.

### B. 균형형 — `SWORD_BASE_R = 800` — 권장

| 상황 | 결손 CURRENT | secured band | 견적 | 기본 제작원가 대비 |
|---|---:|---:|---:|---:|
| BUILD 경미 | 10 | 1.00 | 92 | 약 6% |
| FIRST_STOP | 20 | 1.10 | 158 | 약 11% |
| TENSION | 35 | 1.25 | 278 | 약 19% |
| HIGH | 60 | 1.50 | 528 | 약 35% |
| HIGH 심각 | 80 | 1.50 | 684 | 약 46% |

장점:
- 작은 수리는 setup cost와 fatigue 2 때문에 자동 정답이 되기 어렵다.
- 중간 손상부터 실제 비용 판단이 생긴다.
- 심각 손상도 기본 철검 재제작 1,500골드보다는 낮게 유지된다.
- MAX 흉터는 복구되지 않으므로 CURRENT 수리를 지나치게 비싸게 만들 필요가 없다.

판정: `RECOMMENDED_BASELINE`.

### C. 위험 우선형 — `SWORD_BASE_R = 1,000`

| 상황 | 결손 CURRENT | secured band | 견적 |
|---|---:|---:|---:|
| BUILD 경미 | 10 | 1.00 | 115 |
| FIRST_STOP | 20 | 1.10 | 198 |
| TENSION | 35 | 1.25 | 347 |
| HIGH | 60 | 1.50 | 660 |
| HIGH 심각 | 80 | 1.50 | 855 |

장점:
- 수리와 강행의 경제적 긴장이 강하다.

문제:
- 심각 손상에서 수리비가 기본 철검 제작원가의 절반을 크게 넘는다.
- 이미 MAX 구조 흉터·성공률 불이익을 가진 작품을 추가로 경제적으로 폐기 압박할 가능성이 있다.

판정: `REJECT_AS_BASELINE / UPPER_BOUND_TEST`.

## 4. 권장 첫 테스트값

```text
STRUCTURAL_FAMILY_BASE_R
SWORD = 800 gold

COMMON_MATERIAL_SHADOW_VALUE = 50 gold / unit
OPTIONAL_COMMON_MATERIAL_OFFSET_CAP = 25%
REPAIR_JOB_FATIGUE_COST = 2
```

상태 목표:

```text
SWORD 800 = FIRST_VERTICAL_SLICE_ABSOLUTE_ANCHOR
50 gold = REUSE_EXISTING_POC_SHADOW_VALUE
```

둘 다 `PROPOSED_BASELINE_TEST_PRESET / NOT_FINAL_PRODUCT_BALANCE`다.

## 5. 일반 재료 대체 계산

일반 재료는 할인 쿠폰이 아니라 골드 부담의 대체 지불수단이다.

```text
max_material_units
= floor(repair_quote × 0.25 / 50)

material_credit
= chosen_material_units × 50

gold_due
= repair_quote - material_credit
```

불변식:

```text
0 <= chosen_material_units <= max_material_units
material_credit <= repair_quote × 25%
```

- 재료가 없어도 `chosen_material_units = 0`으로 100% 골드 지불 가능.
- 작은 견적에서는 1개 재료의 50골드가 25% 상한을 넘으면 재료 대체가 0개일 수 있다.
- 이는 초반 수리 UI에 재료 선택을 강제하지 않는 장점도 있다.
- 재료 사용으로 총 경제 burden을 할인하지 않는다. 1개는 기존 경제의 50골드 shadow value로 정확히 환산한다.

## 6. `R=800` 대표 재료별 견적

### FIRST_STOP_POINT / missing 20

```text
iron         158
silver       190
meteor_iron  238
```

### TENSION / missing 35

```text
iron         278
silver       333
meteor_iron  416
```

### HIGH_STAKES / missing 60

```text
iron         528
silver       634
meteor_iron  792
```

### HIGH_STAKES / missing 80

```text
iron         684
silver       821
meteor_iron  1,026
```

원시 재료 가격을 직접 쓰지 않기 때문에 운석철도 철 대비 `1.50x`로 압축된다.

## 7. 5회 전체 적대적 검토

### Loop 1 — 수리가 너무 싸서 자동 정답인가

공격:
- `R=600`에서는 FIRST_STOP 20pt가 약 119골드, TENSION 35pt가 약 208골드다.
- 수리 피로도 2가 있어도 골드 부담이 거의 무시되면 실패 후 습관적으로 수리할 수 있다.

방어:
- `R=800`은 경미 수리 92골드지만 TENSION 35pt부터 278골드로 올라가 실제 판단 비용을 만든다.
- fatigue 2와 setup 5%는 작은 손상 즉시수리를 추가로 억제한다.

재검사:
- 경미 손상은 감수할 여지가 남고, 낮은 CURRENT에서만 수리 매력이 뚜렷해진다.

판정: `R600 LOWER_BOUND / R800 PASS_WITH_PLAYTEST`.

### Loop 2 — 수리가 너무 비싸서 손상 작품 폐기 정답인가

공격:
- `R=1,000`의 HIGH 80pt 철검 수리는 855골드다.
- MAX 흉터와 성공률 페널티까지 가진 작품에 높은 수리비를 붙이면 새 작품 제작/판매 쪽으로 지나치게 수렴할 수 있다.

방어:
- `R=800`의 같은 수리는 684골드로 기본 철검 제작 기대원가 1,500골드의 약 46%다.
- 일반 수리는 MAX를 지우지 않으므로 낮은 가격이 장기 위험을 리셋하지 않는다.

재검사:
- 구조적으로 손상된 작품도 계속 밀어붙일 경제적 이유가 남는다.

판정: `R1000 UPPER_BOUND / R800 PASS`.

### Loop 3 — 일반 재료 shadow value가 수리 전용 차익거래를 만드는가

공격:
- 수리에서만 일반 재료를 25/75/100골드처럼 다르게 평가하면 플레이어가 재료를 수리 전용 차익거래 수단으로 취급한다.

방어:
- 기존 제작·강화 수익곡선이 이미 사용하는 `50 gold / unit`을 그대로 재사용한다.
- 수리에서 재료 사용은 할인 없이 골드를 정확히 대체한다.

재검사:
- 재료 경제의 기준값이 한 곳에서 유지된다.

판정: `PASS`.

### Loop 4 — 25% 상한의 정수 재료 단위가 수리 타이밍 메타를 만드는가

공격:
- 견적 199골드에서는 재료 대체 0개, 200골드부터 1개가 가능해지는 식의 경계가 생길 수 있다.

방어:
- 재료 대체는 할인 효과가 아니라 동일 shadow value의 지불수단 전환이다.
- 총 경제 burden은 바뀌지 않는다.
- 재료의 실제 기회비용이 50과 크게 달라져 경계 악용이 생기면 수리 공식을 바꾸기보다 글로벌 shadow value부터 재검토한다.

재검사:
- 초반 작은 수리에서 재료 UI가 아예 나타나지 않는 것은 인지부하 감소에도 유리하다.

판정: `PASS_WITH_MONITORING`.

### Loop 5 — 단일 `SWORD_BASE_R=800`이 후기 경제까지 감당하는가

공격:
- 기존 July POC 판매가 곡선은 +40~+60에서 수십만~백만 골드까지 상승한다.
- 800골드 기준을 아무 수정 없이 후기까지 사용하면 CURRENT 수리가 경제적으로 무의미해질 수 있다.

방어:
- 12의 800골드는 **첫 Vertical Slice/초기 강화 경제용 절대 anchor**로만 승인 후보로 둔다.
- 후기 `HIGH_STAKES / MASTERY`의 실제 골드 경제가 정본화될 때 `STRUCTURAL_FAMILY_BASE_R` 또는 후기 경제 구조를 별도 재검토한다.
- 구형 +40~+60 수익곡선을 새 2026-08-20 강화 경제의 최종 권위로 취급하지 않는다.

재검사:
- 현재 필요한 첫 테스트값은 얻되, 장기 경제를 잘못 고정하지 않는다.

판정: `PASS_WITH_SCOPE_LIMIT`.

## 8. 외부 벤치마크 적용

### Diablo IV — ADAPT
- 판매가 기반 비용이 작업 순서 최적화를 만들자 아이템 기본 위력·유형 기반으로 비용 공식을 바꾼 사례를 참고한다.
- 최근 제작 경제에서도 재료 종류를 과도하게 늘리지 않고, 골드 부족 때문에 작업이 막히는 상황을 완화하려는 방향을 참고한다.
- Blacksmith는 이를 `안정된 구조 기준 R + 제한된 재료 대체 + 골드 완전 지불 가능`로 변형한다.

### FFXIV — ADAPT / REJECT
- 단순한 수리 UX와 소수 재료 등급은 참고한다.
- 필수 재료가 없으면 자가수리가 막히는 구조는 일반 CURRENT 수리에 비채택한다.

### Black Desert — ADAPT / AVOID
- 현재 내구도와 최대 내구도 복구를 분리하는 원리는 계속 채택한다.
- 동일 장비/특수 재료 반복 투입으로 수리/복구 노가다를 만드는 방향은 일반 CURRENT 수리에 비채택한다.

## 9. 첫 검증 지표

시뮬레이션:
- repair_quote / base_craft_cost
- repair_quote / same-band normal enhancement reference cost
- repair choice rate by CURRENT bucket
- repair choice rate by MAX bucket
- common material offset usage rate
- gold-only repair rate
- repair spend / total session spend
- repair fatigue / total session fatigue
- replacement-vs-repair dominant strategy ratio

Human:
- 경미 손상에서 수리를 반드시 해야 한다고 느끼는가
- 심각 손상에서도 수리가 터무니없이 비싸다고 느끼지 않는가
- 재료 선택을 할인으로 오해하지 않는가
- `MAX는 안 고쳐진다`는 점을 이해하는가

## 10. 재검토 조건

- 경미 손상 직후 수리 선택률이 거의 100%.
- CURRENT가 낮아도 수리 선택률이 거의 0%.
- `R=800` 수리가 새 작품 제작보다 자주 비싸짐.
- 일반 재료를 수리에 쓰기 위해 손상을 일부러 누적하는 메타가 발생.
- 후기 경제에서 수리비가 사실상 0에 가까운 부담으로 붕괴.
- shadow value 50이 다른 제작/강화 경제에서도 더 이상 유효하지 않음.

## 11. 권장 판정

```text
BS-ENHANCE-20260820-12
RECOMMENDATION = B_BALANCED_800
SWORD_BASE_R = 800 gold
COMMON_MATERIAL_SHADOW_VALUE = 50 gold / unit
OPTIONAL_COMMON_MATERIAL_OFFSET_CAP = 25%
REPAIR_JOB_FATIGUE_COST = 2
SCOPE = FIRST_VERTICAL_SLICE_ABSOLUTE_ANCHOR
STATUS = PROPOSED_ONLY / USER_DECISION_REQUIRED
```

제품 코드·runtime data에는 반영하지 않는다.
