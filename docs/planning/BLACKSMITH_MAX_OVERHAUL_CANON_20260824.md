# [현재 정본] Blacksmith MAX 내구도 생애 1회 부분 대수선

- Parent: `BS-ENHANCE-20260820-07~09`, `BS-PROGRESSION-20260820-17`, `BS-RESOURCE-20260824-18`, `BS-REPAIR-20260824-19`
- Decision: `BS-OVERHAUL-20260824-20`
- 사용자 승인: `2026-08-24 KST / 권장안 B 승인`
- 상태: `USER_APPROVED / USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Runtime mutation: `NOT_ALLOWED_IN_THIS_DECISION`
- Human/Player validation: `NOT_RUN`

## 1. 목적

MAX 내구도는 강화 실패로 누적되는 구조 흉터다. 일반 CURRENT 수리는 `CURRENT -> MAX`만 수행하고 MAX를 복구하지 않는다.

두 극단을 피한다.

```text
A. MAX 복구 완전 없음
→ 작품 생애의 무게는 강하지만, 후기 애착 작품에 마지막 구제 선택이 없음

C. 반복/완전 MAX 복구
→ CRITICAL/MAX 흉터가 유지비로 환원되고 강화 긴장감이 약해짐
```

20은 **작품 생애에 단 한 번, 심각하게 손상된 후기 작품을 부분적으로만 구제**한다.

```text
MAX_OVERHAUL
= 원상복구가 아니라 생애 1회 구조 구제
```

## 2. 승인 구조 — ONE_LIFETIME_PARTIAL_OVERHAUL

```yaml
eligibility:
  highest_checkpoint_at_least: 60
  max_durability_min_exclusive: 0
  max_durability_max_inclusive: 40
  overhaul_used: false
  destroyed: false

effect:
  max_durability_gain: 15
  max_durability_after_overhaul_ceiling: 60
  current_durability_after_overhaul: NEW_MAX
  overhaul_used_after: true

cost:
  base_gold: 750000
  gold_material_structure_multiplier: true
  reinforcement_material: 20
  workshop_fatigue: 5

preserve:
  physical_item_uid: true
  enhancement_level: true
  secured_checkpoint: true
  affixes: true
  existing_power: true
  failure_recovery_progress: true
  chronicle_and_history: true

forbidden:
  destroyed_item_revival: true
  repeated_overhaul_same_physical_uid: true
  restore_to_100: true
  rng_success_or_failure: true
  automatic_market_value_refund: true
  dedicated_rare_overhaul_currency: true
```

## 3. 사용 조건

대수선은 미리 사는 보험이 아니다.

```text
highest secured checkpoint >= +60
0 < MAX <= 40
OVERHAUL_USED == false
physical state != DESTROYED
```

따라서 MAX 41 이상에서 선제적으로 사용할 수 없다. +60 이전 작품에도 사용할 수 없다.

의도:
- 초반/중반의 일반 유지 행동이 되지 않음.
- 후기 작품이 `FRACTURED / CRITICAL` 구조 상태에 들어간 뒤에만 마지막 구제 선택이 열림.
- 사용 가능 상태 자체가 이미 상당한 구조 손상을 의미함.

## 4. 효과

```text
new_MAX = min(60, old_MAX + 15)
CURRENT = new_MAX
OVERHAUL_USED = true
```

예:

```text
CURRENT 28 / MAX 34
→ 대수선
→ CURRENT 49 / MAX 49
```

```text
CURRENT 35 / MAX 40
→ 대수선
→ CURRENT 55 / MAX 55
```

대수선 한 번으로 MAX 61 이상에 도달하지 못한다.

즉 대수선 뒤에도 `STRESSED 61~80` 또는 `STABLE 81~100`으로 돌아갈 수 없고, 작품은 구조 흉터를 계속 가진다.

## 5. 비용

첫 테스트 Budget:

```text
OVERHAUL_BASE_GOLD = 750,000G
OVERHAUL_REINFORCEMENT_MATERIAL = 보강재 20
OVERHAUL_JOB_FATIGUE_COST = 5
```

골드에는 기존 주재료 구조 배율만 재사용한다.

```text
iron        750,000G
silver      900,000G
meteor_iron 1,125,000G
```

보강재는 Decision 18의 50G·상시 확정 공급 계약을 재사용한다.

금지:
- 작품 판매가에 직접 비례.
- 실제 다음 강화비에 직접 비례.
- 현재 MAX에 역비례하는 벌금 배율.
- 전용 희귀 `overhaul token` 추가.
- 대수선 지출을 작품 시장가에 자동 환급.

## 6. 상태와 작품 생애 기록

대수선은 같은 물리 UID를 유지한다.

```text
ITEM_UID unchanged
ENHANCEMENT_LEVEL unchanged
SECURED_CHECKPOINT unchanged
AFFIX / ARTISTRY / EXISTING POWER unchanged
FAILURE_RECOVERY unchanged
CUSTOMER / WORLD / CHRONICLE history preserved
```

추가 기록:

```text
MAX_OVERHAUL_USED = true
overhaul_before_current
overhaul_before_max
overhaul_after_current
overhaul_after_max
overhaul_at_enhancement_level
overhaul_highest_checkpoint
overhaul_cost_gold
overhaul_material_units
overhaul_reason = PLAYER_CHOSEN_STRUCTURAL_RESCUE
```

대수선 사용 사실은 제거하지 않는다. 이것 자체가 작품의 생애 사건이다.

## 7. 대안 비교

### A. MAX 영구 흉터 / 복구 없음 — REJECT AS BASELINE

장점:
- MAX 손실의 무게가 가장 강함.
- 시스템이 단순함.

문제:
- 후기 애착 작품이 깊게 손상된 뒤 `계속 위험 감수 / 폐기`만 남기 쉬움.
- UID·생애 중심 게임에서 큰 대가를 치르고 한 작품을 살리는 선택이 없음.

`LOWER_RECOVERY_BOUND / REFERENCE_ONLY`.

### B. 생애 1회 +15 부분 대수선 — APPROVED

장점:
- 한 작품을 살릴 마지막 경제·감정 선택 생성.
- MAX 100 복구 불가.
- MAX 40 이하에서만 가능.
- 한 UID 1회라 반복 유지비가 되지 않음.
- 기존 보강재와 주재료 구조 배율을 재사용.

`ADOPT / USER_APPROVED_TEST_BUDGET`.

### C. 반복/완전 MAX 복구 — REJECT

장점:
- 접근성이 높고 작품 보존이 쉬움.

문제:
- CRITICAL/MAX 흉터가 사실상 골드 유지비가 됨.
- 반복 복구가 최적해가 되면 강화의 `멈춤 / 한 번 더` 긴장이 약해짐.
- 전용 MAX 복구재 파밍을 붙이면 별도 유지보수 루프가 메인을 침범할 수 있음.

`REJECT_AS_BASELINE`.

## 8. 시뮬레이션 증거 경계

### 8.1 사용자 승인 직전 비교

승인에 사용된 session planning comparison은 대표 +100에서 다음 방향을 보였다.

```text
A no-overhaul
mean expected cost ≈ 5.616M
mean physical destruction ≈ 1.034

B lifetime partial +15 / 750k
mean expected cost ≈ 5.614M
mean physical destruction ≈ 0.893

C repeat/full recovery
mean expected cost ≈ 4.003M
physical destruction ≈ near-zero in that policy model
```

B는 거시경제를 거의 흔들지 않으면서 작품 생존을 유의미하게 개선했고, C는 위험 곡선을 크게 약화했다.

### 8.2 승인 후 독립 재구성

Decision 13/17/18/19의 현재 계약을 별도로 재구성하여 20,000-run을 다시 돌렸다.

대표 +100 / 동일 계열 RNG 비교:

```text
A no-overhaul
mean ≈ 5.675M
mean destruction ≈ 1.058
mean attempts ≈ 277.6

B one-lifetime +15 / 750k
mean ≈ 5.665M
mean destruction ≈ 0.914
mean attempts ≈ 260.2

C repeat full recovery under the reconstructed trigger policy
mean ≈ 4.796M
mean destruction ≈ 0.568
mean attempts ≈ 216.1
```

해석:
- B의 정확한 mean delta는 reference safe-repair/overhaul 자동 사용 정책에 따라 약간 변하지만 **전체 경제 대비 작은 범위**에 남았다.
- B는 파괴와 재시도 수를 줄이되 위험을 제거하지 않았다.
- C의 정확한 절감폭도 반복 복구 trigger에 민감하지만, 어느 비교에서도 B보다 훨씬 큰 경제·생존 완화를 만들었다.

따라서 숫자 하나의 동일 재현보다 다음 구조 결론을 신뢰한다.

```text
ONE_LIFETIME_PARTIAL_OVERHAUL = ROBUST_CANDIDATE
REPEAT_FULL_OVERHAUL = RISK_CURVE_EROSION
EXACT_RELEASE_BALANCE = USER_PLAYTEST + FINAL_BALANCE_LAB_REQUIRED
```

이 시뮬레이션은 runtime/human evidence가 아니다.

## 9. 외부 벤치마크

외부 수치를 복사하지 않고 가역성의 정도만 비교한다.

### Black Desert — ADAPT / AVOID

공식 가이드에서 강화 실패는 최대 내구도를 낮추며, 동일 장비나 Memory Fragment로 최대 내구도를 복구할 수 있다.

흡수:
- CURRENT 성격의 일반 수리와 MAX 성격의 구조 복구를 분리할 수 있다는 원리.

비채택:
- 반복 MAX 복구를 일반 유지 루프로 만들기.
- 동일 장비/전용 복구재 반복 소비를 필수 파밍으로 만들기.

Source:
`https://www.naeu.playblackdesert.com/News/Notice/Detail?countryType=fr-fr&groupContentNo=5583`

### FINAL FANTASY XIV — REFERENCE / REJECT FOR MAX RESET

공식 UI Guide에서 자가 수리는 Dark Matter로 장비를 수리하며 100%를 넘어 최대 199%까지 내구를 회복할 수 있다. 0% 장비도 물리적으로 남아 수리 가능하다.

흡수:
- 유지 행동은 이해 가능하고 접근 가능해야 한다.

비채택:
- 구조 흉터까지 반복적으로 완전 초기화하는 가역성.
- 0% 물리 작품 부활.

Source:
`https://na.finalfantasyxiv.com/uiguide/equipment/equipment-repair/equipment_repair_myself.html`

### Breath of the Wild — ADAPT

Nintendo Explorer's Guide는 일반 무기는 파괴되고, 특정 특별 무기는 필요한 재료를 통해 다시 만들 수 있다고 설명한다.

흡수:
- 대부분의 손실은 실제 손실로 남기되, 특별한 가치가 있는 장비에 제한적 예외적 구제 경로가 있을 수 있다는 원리.

변형:
- Blacksmith는 새 복제품으로 바꾸기보다 파괴 전 동일 UID를 생애 1회 부분 구제한다.

Source:
`https://media.nintendo.com/zelda/breath-of-the-wild/assets/ExplorersGuide.pdf`

## 10. UX 계약

대수선 화면은 일반 수리와 명확히 분리한다.

표시:

```text
현재 CURRENT / MAX
대수선 후 CURRENT / MAX
회복량 +15
회복 후 MAX 상한 60
이 작품의 대수선 사용 여부
골드 / 보강재 / 공방 부담
대수선 후에도 남는 구조 상태와 강화 페널티
'같은 작품의 생애 1회' 경고
```

확정 버튼 문구는 결과를 숨기지 않는다.

금지:
- `완전 복구`, `새것처럼`, `100% 복원` 표현.
- 성공 확률이 있는 것처럼 연출.
- 대수선 후 MAX 흉터 기록 삭제.
- DESTROYED를 되살릴 수 있다고 암시.
- 반복 사용 가능한 일반 서비스처럼 배치.

## 11. 5회 전체 적대 검토

### Loop 1 — CRITICAL/MAX 흉터를 무효화하는가
- MAX<=40에서만 가능.
- +15, after ceiling 60.
- UID lifetime 1회.
- `PASS`.

### Loop 2 — 항상 대수선이 정답인가
- base 750,000G + 보강재 20 + fatigue 5.
- 고급 주재료는 기존 구조 배율 적용.
- 작품을 멈춤/인계/계속 위험 감수하는 선택도 남음.
- `PASS_WITH_HUMAN_TEST`.

### Loop 3 — 거시경제가 깨지는가
- 승인 전·승인 후 두 비교에서 B는 A 대비 전체 경제 변화가 작음.
- 반복 완전복구 C는 훨씬 큰 경제 완화를 만듦.
- `PASS_WITH_FINAL_BALANCE_REGEN`.

### Loop 4 — MAX 흉터가 사실상 사라지는가
- 대수선 후 최대 MAX 60.
- STRESSED/STABLE로 되돌아갈 수 없음.
- OVERHAUL_USED 영구 기록.
- `PASS`.

### Loop 5 — 유지보수 파밍이 메인을 침범하는가
- 전용 희귀 화폐 없음.
- 기존 보강재 20과 골드만 사용.
- 같은 UID 1회라 반복 파밍 동기 최소화.
- `PASS`.

## 12. Implementation Reality Gate

```text
DESIGN_DECISION = USER_APPROVED
PLANNING_COMPARISON = RUN
INDEPENDENT_RECONSTRUCTION = RUN_WITH_POLICY_SENSITIVITY
PRODUCT_RUNTIME = BLOCKED
GODOT_RUNTIME = NOT_RUN_FOR_DECISION_20
HUMAN_PLAYER = NOT_RUN
FINAL_RELEASE_BALANCE = NOT_CLAIMED
```

새 `기획 완료` 선언 전에는 data/code/scene/asset/project.godot를 수정하지 않는다.

## 13. 구현 Gate가 열릴 때 필요한 consumer

1. Item UID state에 `overhaul_used`와 overhaul history event 추가.
2. MAX/CURRENT invariant validator에 대수선 transition 추가.
3. Eligibility: `highest_checkpoint>=60 && 0<MAX<=40 && !overhaul_used && !destroyed`.
4. 골드·보강재·fatigue atomic payment.
5. `MAX=min(60, MAX+15); CURRENT=MAX` atomic state transition.
6. same-UID history append.
7. save/load/migration 및 duplicate-UID 방지 테스트.
8. enhancement/repair UI에서 일반 수리와 대수선 분리.
9. Balance Lab에서 Decision 19+20 통합 static market table 재검증.
10. Human test에서 `구제 선택`인지 `필수 세금`인지 측정.

## 14. 재검토 조건

- 대수선 가능 시 90% 이상 플레이어가 자동으로 선택.
- 대수선 후 위험이 사실상 초기화됐다고 인식.
- MAX<=40 작품의 대부분이 대수선 직후 다시 무조건 강화.
- 750k가 후기 경제에서 무의미하거나 반대로 작품 가치보다 과도함.
- 보강재 20 구매가 반복 클릭/인벤토리 마찰을 만듦.
- +15가 너무 작아 선택되지 않거나 너무 커서 필수화.
- `OVERHAUL_USED`가 save/load/복제 과정에서 유실 가능.
- Decision 19+20 결합 후 static market anchor가 출시 밸런스에서 유의미하게 이동.

## 15. 다음 작업

`MAX_OVERHAUL` 완료 뒤 다음 기획은:

```text
DESTRUCTION_UX
→ DESTROYED 순간의 결과 전달
→ memorial / history / successor 흐름
→ 파괴를 벌점 화면이 아니라 작품 생애의 명확한 종결 사건으로 표현
```
