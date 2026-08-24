# [현재 정본] Blacksmith 후기 HIGH/MASTERY 일반 CURRENT 수리 경제

- Parent: `BS-ENHANCE-20260820-10~12`, `BS-PROGRESSION-20260820-17`, `BS-RESOURCE-20260824-18`
- Decision: `BS-REPAIR-20260824-19`
- 사용자 승인: `2026-08-24 KST / 권장안 B 승인`
- 상태: `USER_APPROVED / USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Runtime mutation: `NOT_ALLOWED_IN_THIS_DECISION`
- Human/Player validation: `NOT_RUN`
- Simulation evidence: `fresh 20,000-run planning Monte Carlo / deterministic independent reproduction`

## 1. 목적

`BS-ENHANCE-20260820-10~12`의 일반 CURRENT 수리 공식은 초반 Vertical Slice에서 읽기 쉽고 안전한 기준을 만들었다. 그러나 기존 `HIGH_STAKES 1.50 / MASTERY 1.80` 확보 밴드 배율은 후기 강화 시도비가 수만 골드로 커진 뒤 일반 수리의 골드 비용을 거의 무시 가능한 수준으로 만든다.

19의 목표는 일반 수리를 새 메인 루프나 벌금으로 만들지 않으면서 후기 작품에서 `수리 / 그대로 한 번 더 / 멈춤`의 경제 판단이 실제로 보이게 하는 것이다.

```text
PRIMARY CORE
= 강화 긴장감 + DDD

LATE REPAIR ECONOMY
= 작품을 지키는 안전 행동에도 읽을 수 있는 기회비용을 부여
```

## 2. 변경 범위

19는 10~12의 수리 구조를 유지하고 **secured band multiplier 중 HIGH/MASTERY 두 값만 부분 대체**한다.

```text
[UNCHANGED]
SWORD_BASE_R = 800G
MATERIAL_STRUCTURE_MULTIPLIER = iron 1.00 / silver 1.20 / meteor_iron 1.50
setup_fraction = 0.05
variable_fraction = 0.65
COMMON_REINFORCEMENT_MATERIAL = 보강재
COMMON_MATERIAL_UNIT_VALUE = 50G
material_units = max(1, ceil((MAX-CURRENT)/25))
PAYMENT = GOLD + MATERIAL
REPAIR_JOB_FATIGUE_COST = 2
CURRENT -> MAX
MAX unchanged
recovery unchanged

[UPDATED BY 19]
SECURED_BAND_MULTIPLIER
LEARN / BUILD = 1.00
FIRST         = 1.10
TENSION       = 1.25
HIGH          = 2.25
MASTERY       = 3.00
```

따라서 11의 `HIGH 1.50 / MASTERY 1.80`과 12의 해당 값 기반 HIGH 예시는 `HISTORICAL_PRE_19_NUMERIC_EVIDENCE`다. 다른 10~12 계약은 유지한다.

## 3. 런타임 수리 공식

```text
missing = MAX - CURRENT

R
= 800
× MATERIAL_STRUCTURE_MULTIPLIER[primary_material]
× SECURED_BAND_MULTIPLIER[highest_secured_band]

gold_cost
= round(R × (0.05 + 0.65 × missing / 100))

required_reinforcement_material
= max(1, ceil(missing / 25))

REPAIR_PAYMENT
= gold_cost
+ required_reinforcement_material
```

보강재는 `BS-RESOURCE-20260824-18`의 공방 재료상 50G 상시·무제한 공급을 그대로 사용한다.

## 4. 왜 Base R이나 next-attempt cost를 바꾸지 않는가

대안으로 다음을 다시 비교했다.

### A. 현행 후기 배율 유지 — REJECT AS FINAL LATE BASELINE

```text
HIGH 1.50
MASTERY 1.80
```

- 장점: 일반 수리가 매우 접근 가능하다.
- 문제: 후기 강화비가 수만 골드로 커진 뒤 수리의 골드 비용 신호가 지나치게 작아진다.
- 일반 수리의 경제 판단을 사실상 `fatigue 2` 하나가 담당하게 된다.

### B. HIGH 2.25 / MASTERY 3.00 — APPROVED

- 후기 수리의 체감비용을 올리되 구조는 유지한다.
- +1마다 가격이 변하지 않고 큰 위험 밴드에서만 달라진다.
- 시장가·실제 다음 강화비·MAX 상태를 직접 공식에 넣지 않는다.
- 전체 +100 경제에는 거의 영향을 주지 않는다.

### C. 강한 후기 스케일 — REJECT

대표 검토값:

```text
HIGH 3.75
MASTERY 7.50
```

- 일반 CURRENT 수리가 안전 선택이 아니라 또 하나의 징벌 세금으로 변할 위험.
- MAX 흉터·성공률 불이익·작품 손실 위험과 중첩해 작품 폐기를 과도하게 유도할 수 있다.

## 5. 대표 철검 수리 부담

보강재 shadow burden을 포함한 대표값이다.

| 상황 | 결손 | Pre-19 | 19 승인 B |
|---|---:|---:|---:|
| HIGH 일반 | 20pt | 약 266G-eq | 약 374G-eq |
| HIGH 심각 | 50pt | 약 550G-eq | 약 775G-eq |
| MASTERY 일반 | 25pt | 약 356G-eq | 약 560G-eq |
| MASTERY 심각 | 60pt | 약 784G-eq | 약 1,206G-eq |

대표 MASTERY 심각 수리도 기본 철검 제작 기대원가 1,500G-eq보다 낮게 남는다. 일반 CURRENT 수리는 MAX를 복구하지 않으므로 새 작품과 동등하거나 더 비싼 가격을 기본 목표로 삼지 않는다.

## 6. HIGH 대표 주재료별 재검산

### HIGH / missing 60 / 보강재 3

```text
iron         792G + 3 material = 942G-eq
silver       950G + 3 material = 1,100G-eq
meteor_iron 1,188G + 3 material = 1,338G-eq
```

### HIGH / missing 80 / 보강재 4

```text
iron        1,026G + 4 material = 1,226G-eq
silver      1,231G + 4 material = 1,431G-eq
meteor_iron 1,539G + 4 material = 1,739G-eq
```

고급 주재료 배율은 여전히 압축된 `1.20 / 1.50`만 사용한다. 원시 재료 시장가나 작품 판매가를 다시 과금하지 않는다.

## 7. Fresh 20,000-run 재현 검증

### 모델 경계

현재 승인된 planning contract만 사용했다.

```text
success curve = BS-PROGRESSION-17
UID+target recovery = +6%p + hard guarantee
failure family = BS-ENHANCE-13
CURRENT/MAX loss = current approved budgets
checkpoint = [10,30,60,90]
reference safe repair policy = BS-PROGRESSION-17
resource supply/value = BS-RESOURCE-18
physical destroy = CURRENT==0 or MAX==0
recraft = 1,500G-eq representative iron sword
```

비교에서 수리 배율 외 규칙과 난수 계열은 동일하게 유지했다.

### 현행 A 재현

| Goal | Fresh Mean | Existing Canon Anchor | 차이 |
|---:|---:|---:|---:|
| +10 | 5,770 | 5,779 | 약 -0.16% |
| +60 | 712,869 | 712,986 | 약 -0.02% |
| +90 | 3,243,733 | 3,235,853 | 약 +0.24% |
| +100 | 5,656,479 | 5,632,657 | 약 +0.42% |

모두 17의 independent reproduction tolerance `±1.5%` 안이다.

### 승인 B 비교

| Goal | Pre-19 Mean | Decision 19 Mean | Mean 변화 | Decision 19 P90 |
|---:|---:|---:|---:|---:|
| +10 | 5,770 | 5,770 | 0.000% | 6,500 |
| +60 | 712,869 | 713,376 | +0.071% | 814,780 |
| +90 | 3,243,733 | 3,246,947 | +0.099% | 5,167,466 |
| +100 | 5,656,479 | 5,661,842 | +0.095% | 10,086,044 |

+100 기준:

```text
mean attempts ≈ 276.87
mean physical destruction/recraft ≈ 1.053
mean surviving MAX ≈ 59.28
```

수리 가격만 바뀌므로 attempt/destruction/MAX 통계는 비교안 사이에서 동일하다.

## 8. 경제 판정

19로 인한 전체 경제 변화는 작다.

```text
+100 mean expected cost delta ≈ +0.095%
```

따라서 현재 승인된 static market anchor를 19 때문에 즉시 재생성하지 않는다.

```text
+10 break-even structure = preserved
+11~+100 positive expected-profit structure = preserved
existing static market table = retained as current planning anchor
```

출시 전 최종 Balance Lab에서는 19와 후속 MAX_OVERHAUL을 함께 넣은 뒤 전체 static table을 다시 생성해야 한다.

## 9. 외부 벤치마크 흡수

외부 게임의 숫자는 복사하지 않고 구조 원리만 사용한다.

- `FINAL FANTASY XIV · ADAPT`: 일반 장비 수리는 Dark Matter 같은 재료를 vendor 등에서 안정적으로 구해 수행할 수 있다. 일반 유지 행동을 희귀 파밍 병목으로 만들지 않는 원리를 18과 함께 유지한다.
  - https://na.finalfantasyxiv.com/uiguide/equipment/equipment-repair/equipment_repair_myself.html
- `Diablo IV · ADAPT`: Enchant 비용을 sell value에 묶었을 때 작업 순서 최적화가 생기자 Base Item Power와 item type 기반으로 변경했다. Blacksmith도 판매가/실제 next-attempt cost를 일반 수리 runtime 공식에 직접 연결하지 않는다.
  - https://news.blizzard.com/en-us/article/24092662/diablo-iv-patch-notes-1-0-1-2

## 10. 5회 전체 적대 검토

### Loop 1 — 일반 수리가 코어를 덮는가
- 공식·행동 횟수·피로도는 그대로다.
- 골드 신호만 후기에서 강화한다.
- `PASS_WITH_HUMAN_TEST`.

### Loop 2 — MAX 흉터 이중 처벌인가
- MAX 자체를 수리비 배율로 사용하지 않는다.
- 기존 성공률/신규 강화효과 페널티 외 새 MAX 벌금을 추가하지 않는다.
- `PASS`.

### Loop 3 — 거시경제가 깨지는가
- fresh 20,000-run에서 +100 mean delta 약 +0.095%.
- 기존 anchor reproduction tolerance 안.
- `PASS`.

### Loop 4 — 수리 타이밍 메타가 생기는가
- 실제 next-attempt cost와 무관하다.
- 같은 확보 밴드의 +1 이동/제한 하락으로 R이 변하지 않는다.
- 위험 밴드 전환 전 수리는 reference safe policy와도 일치한다.
- `PASS_WITH_PLAYTEST`.

### Loop 5 — 더 나은 단순안이 있는가
- A는 후기 경제 신호가 너무 약하다.
- C는 일반 수리를 벌금화할 위험이 크다.
- B는 단 두 배율만 조정해 체감과 거시경제를 분리한다.
- `PASS / APPROVED_B`.

## 11. Implementation Reality Gate

```text
DESIGN_DECISION = USER_APPROVED
PLANNING_SIMULATION = RUN_FRESH
GITHUB_CANON_SYNC = REQUIRED
NOTION_SYNC = REQUIRED
PRODUCT_RUNTIME = BLOCKED
PRODUCT_DATA = NOT_MUTATED
HUMAN_PLAYTEST = NOT_RUN
FINAL_PRODUCT_BALANCE = NOT_CLAIMED
```

## 12. 후속 작업

19 완료 뒤 현재 planning 순서는:

```text
MAX_OVERHAUL
→ DESTRUCTION_UX
→ MAX_LEVEL_PAYOFF
→ FIRST_10_MINUTES
→ PRECISION_CUSTOMER_LINK
→ RELEASE_NEAR_VERTICAL_SLICE
```

`MAX_OVERHAUL`은 일반 CURRENT 수리와 분리해 **MAX 구조 흉터를 복구할 기능이 존재해야 하는지, 존재한다면 어떤 대가와 제한을 가져야 하는지**를 소유한다.
