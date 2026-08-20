# [현재 승인] Blacksmith 수리 참조비용·작업량 계약

- Parent: `BS-ENHANCE-20260820-10`
- Decision: `BS-ENHANCE-20260820-11`
- 사용자 승인: `2026-08-20 KST / 권장안 진행 승인`
- 상태: `USER_APPROVED / USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 결정 목적

`BS-ENHANCE-20260820-10`은 일반 수리의 비용 구조를 다음처럼 승인했다.

```text
missing_current_points = MAX - CURRENT

repair_cost
= REPAIR_REFERENCE_COST
× (setup_fraction + variable_fraction × missing_current_points / 100)
```

11은 여기서 미정이던 `REPAIR_REFERENCE_COST`의 **상대 구조**, 일반 재료 사용 방식, 공방 작업 부담을 정한다.

핵심 목표:

- 시장 판매가가 오를수록 수리비가 자동 폭증하지 않는다.
- 고급 재료·고강화 구조의 정비 난이도 차이는 읽을 수 있게 남긴다.
- 수리 타이밍 최적화가 +1 단계마다 발생하지 않는다.
- 재료 부족 때문에 CURRENT 수리가 봉쇄되지 않는다.
- 수리가 강화 DDD 세션을 통째로 끊는 별도 메인 루프가 되지 않는다.

## 2. Better Alternative Search

### A. 원가 충실형

```text
R ∝ 원시 주재료 가격 × 현재 강화 투자량
```

장점:
- 경제적 사실성이 높다.

문제:
- 철/은/운석철의 원시 가격 차이를 그대로 적용하면 고급 작품 수리비가 과도하게 벌어진다.
- 강화 한 단계마다 투자량이 변하면 수리 시점 최적화가 생긴다.
- 작품의 시장 프리미엄과 수리 구조를 다시 엮기 쉽다.

판정: `REJECT`.

### B. 압축 구조 참조형 — 채택

```text
REPAIR_REFERENCE_COST
= STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER
× SECURED_BAND_MULTIPLIER
```

- 원시 재료 가격이 아니라 압축된 구조 배율을 사용한다.
- 현재 +1 단계가 아니라 **확보된 위험/체크포인트 밴드**로만 복잡도가 변한다.
- 실제 다음 강화비·판매가·예술성·수식어·연대기는 직접 참조하지 않는다.

판정: `ADOPT`.

### C. 편의 우선 단일가형

모든 일반 수리를 거의 같은 R로 처리한다.

장점:
- 가장 단순하다.

문제:
- 철검과 고급 구조 작품의 정비 차이가 사라진다.
- 후반 고위험 작품의 경제적 무게가 약해진다.

판정: `REJECT_AS_BASELINE`.

## 3. 채택 공식

```text
missing_current_points = MAX - CURRENT

R
= STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER[primary_material]
× SECURED_BAND_MULTIPLIER[highest_secured_band]

repair_cost
= R × (0.05 + 0.65 × missing_current_points / 100)
```

`0.05 / 0.65`는 10에서 승인된 첫 테스트 shell을 그대로 사용한다.

`STRUCTURAL_FAMILY_BASE_R`의 **절대 골드 기준값은 11에서 고정하지 않는다.** 이는 다음 절대 경제 Budget에서 독립 조정한다.

## 4. 주재료 구조 배율 — 승인 첫 테스트값

첫 Vertical Slice 대표 검 3종:

| 주재료 | 구조 배율 |
|---|---:|
| `iron` | `1.00` |
| `silver` | `1.20` |
| `meteor_iron` | `1.50` |

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

원칙:

- 기존 재료 데이터의 원시 판매가 비율을 그대로 복사하지 않는다.
- 배율은 **수리 구조 난이도**만 담당한다.
- 재료의 예술성·희귀성·수식어 프리미엄은 이 배율에서 다시 과금하지 않는다.
- 추후 새 재료는 `구조 수리 난이도` 근거가 있을 때만 새 배율을 받는다.

## 5. 확보 밴드 복잡도 — 승인 첫 테스트값

| 최고 확보 밴드 | 배율 |
|---|---:|
| `LEARN / BUILD_CONFIDENCE` | `1.00` |
| `FIRST_STOP_POINT` | `1.10` |
| `TENSION` | `1.25` |
| `HIGH_STAKES` | `1.50` |
| `MASTERY` | `1.80` |

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

### 왜 현재 강화 단계가 아니라 확보 밴드인가

- 동일 확보 밴드 안에서 +1 오르거나 제한 하락해도 R은 그대로다.
- 체크포인트 직전 수리/직후 수리 같은 세밀한 비용 메타를 줄인다.
- 플레이어가 `이 작품이 어느 위험 등급의 구조인가`라는 큰 단위만 이해하면 된다.

`highest_secured_band`는 작품이 확보한 최고 체크포인트/위험 계층을 뜻하며, 실패로 같은 밴드 안에서 1단계 하락했다고 낮아지지 않는다.

## 6. MAX 상태는 일반 수리비 할증 축이 아니다

`MAX`가 낮다는 이유로 R에 별도 배율을 추가하지 않는다.

```text
MAX 50 / CURRENT 20
missing_current_points = 30
```

이 작품은 30pt만 복구한다.

금지:

```text
R × (100 / MAX)
R × structural_damage_multiplier
repair_missing_ratio = (MAX-CURRENT)/MAX
```

이유:

- MAX 손상은 이미 강화 성공률과 미래 신규 강화 효과에 장기 불이익을 준다.
- 일반 수리비까지 MAX 상태로 할증하면 구조 흉터를 중복 처벌한다.

## 7. 골드·일반 재료 정책

첫 Vertical Slice 일반 수리는 **골드 우세 + 일반 구조 재료 선택 보조**를 사용한다.

불변식:

- 일반 재료가 없어도 수리 가능하다.
- 새 `repair token`이나 수리 전용 화폐를 만들지 않는다.
- 촉매·희귀 수식어 재료·MAX 복구 재료를 CURRENT 수리에 요구하지 않는다.
- 재료 사용은 선택 사항이다.

승인 첫 테스트 상한:

```text
OPTIONAL_COMMON_MATERIAL_OFFSET_CAP = 25% of repair quote
```

- 허용 일반 구조 재료의 고정 shadow value로 수리 견적의 최대 25%까지 대체할 수 있다.
- 남은 75% 이상은 골드로 지불한다.
- 일반 재료가 없으면 100% 골드 지불이 가능하다.
- 재료의 시장 변동가를 실시간으로 수리 공식에 연결하지 않는다.

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 8. 공방 작업량 / 피로도

기존 저장소에는 역사/재사용 기준으로 다음 값이 존재한다.

```text
base_fatigue 20
normal_enhance 1
forge 3
special_enhance 3
restore 5
```

과거 `restore 5` 또는 `게임 내 하루 전체 소비`는 최신 강화 중심 수리 계약의 권위가 아니다.

11의 첫 테스트값:

```text
REPAIR_JOB_FATIGUE_COST = 2
```

의도:

```text
normal enhancement 1
< CURRENT repair 2
< forging / special enhancement 3
```

- 일반 수리는 무료 행동이 아니다.
- 일반 수리 한 번이 하루를 자동 종료시키지 않는다.
- 동일 작품 수리는 한 번의 `REPAIR_JOB`으로 `CURRENT = MAX`까지 처리한다.
- 부분수리 반복으로 피로도 2를 여러 번 내게 하지 않는다.

`base_fatigue=20` 자체를 11이 출시 정본으로 재승인하는 것은 아니다. 이후 하루 작업량 재조정 시에도 **수리는 일반 강화보다 무겁고 단조/특수강화보다 가벼운 보조 행동**이라는 상대 의도를 우선 검증한다.

## 9. UI 정보 계약

수리 판단 카드 기본 정보:

```text
CURRENT before → CURRENT after(MAX)
MAX unchanged
총 수리 견적
골드 지불
선택 일반 재료 절감(사용 시)
공방 부담 2
수리 후에도 남는 MAX 구조 상태
수리하지 않고 강화할 경우 현재 위험
```

원인 설명은 기본 화면에서 최대 2개 핵심 축만 보여준다.

```text
재료 구조: 보통/높음
확보 단계 복잡도: TENSION
```

상세 보기에서만 실제 배율을 펼친다.

금지:

- 시장가 계산기를 요구하는 UI
- +1 단계마다 수리비가 왜 바뀌는지 설명해야 하는 구조
- 재료가 없어서 수리 버튼 자체가 잠기는 기본 UX
- MAX가 수리되는 것처럼 보이는 결과 연출

## 10. 5회 전체 적대적 검토 결론

### Loop 1 — 고급 재료가 수리비 폭탄이 되는가

공격:
- 원시 철/은/운석철 가격을 그대로 쓰면 고급 작품의 수리가 지나치게 비싸진다.

방어:
- `1.00 / 1.20 / 1.50` 압축 구조 배율.
- 예술성·희귀도·시장 프리미엄은 제외.

판정: `PASS_WITH_TUNING`.

### Loop 2 — 수리 타이밍 메타가 강화 DDD를 덮는가

공격:
- 현재 단계/다음 강화비에 연동하면 체크포인트 직전 수리가 항상 유리해질 수 있다.

방어:
- `highest_secured_band`가 바뀔 때만 R이 변한다.
- 같은 밴드 제한 하락은 R을 낮추지 않는다.

판정: `PASS`.

### Loop 3 — 재료 부족이 수리를 봉쇄하는가

공격:
- 구조 재료를 필수 요구하면 안전 행동이 인벤토리 RNG에 종속된다.

방어:
- 100% 골드 지불 가능.
- 일반 재료는 최대 25% 선택 대체만 허용.

판정: `PASS`.

### Loop 4 — 수리가 하루/세션을 지나치게 끊는가

공격:
- 구형 restore 5나 하루 전체 소비를 유지하면 실패 후 강화 리듬이 끊어진다.

방어:
- 첫 테스트 `REPAIR_JOB_FATIGUE_COST=2`.
- 한 번 수리로 CURRENT 전체를 MAX까지 회복.

판정: `PASS_WITH_HUMAN_TEST`.

### Loop 5 — 공식이 지나치게 복잡한가

공격:
- 구조 가족 × 재료 × 확보 밴드 × 결손 × 골드/재료 대체를 전부 노출하면 계산 UI가 된다.

방어:
- 기본 화면은 최종 견적과 2개 원인만 표시.
- 상세 보기에서만 배율을 공개.

판정: `PASS`.

## 11. 시뮬레이션/사람 검증 신호

### 너무 비쌈

- LOW CURRENT에서도 수리 대신 새 작품 제작이 항상 우세.
- silver/meteor_iron 작품이 구조 배율 때문에 거의 수리되지 않음.
- HIGH_STAKES 진입 후 작품 대부분이 첫 손상 뒤 폐기됨.

### 너무 쌈

- 작은 손상마다 즉시 수리가 사실상 자동 정답.
- 재료 25% 대체를 쓰지 않아도 비용이 의사결정에 영향을 거의 주지 않음.
- 수리 후 즉시 다시 강화하는 행동만 반복되어 멈춤 선택이 사라짐.

### 작업량이 너무 무거움

- 수리 1회 때문에 강화 세션이 반복적으로 종료됨.
- 수리 후 그날 추가 강화가 거의 불가능.

### 적절함

- 고급 재료 작품도 수리 가능한 가치가 남음.
- 손상이 작으면 감수하고, 손상이 커지면 수리가 강하게 매력적임.
- 수리/도전/멈춤이 모두 관찰됨.
- 일반 수리 후에도 MAX 흉터와 장기 위험을 이해함.

## 12. 튜닝 순서

11 관련 문제는 한 번에 여러 축을 바꾸지 않는다.

1. `MATERIAL_STRUCTURE_MULTIPLIER`
2. `SECURED_BAND_MULTIPLIER`
3. `OPTIONAL_COMMON_MATERIAL_OFFSET_CAP`
4. `REPAIR_JOB_FATIGUE_COST`
5. `STRUCTURAL_FAMILY_BASE_R` 절대 골드 기준

10의 `setup_fraction / variable_fraction`은 11 축을 확인한 뒤 조정한다.

## 13. 현재 미확정

- `STRUCTURAL_FAMILY_BASE_R`의 절대 골드 기준값
- 검 이외 장비군별 base R
- 일반 재료 shadow value의 최종값
- 하루 총 피로도/작업량의 출시 최종값
- 수리 선택률 목표 범위
- MAX 대수선/구조 복구의 존재 여부와 대가

모두 `NOT_FINAL / USER_PLAYTEST_REQUIRED`다.

## 14. 증거 경계

- 이 Decision은 기획/첫 시뮬레이션 Budget이다.
- `data/progression/workshop_day_balance.json`의 구형 `restore=5`를 지금 수정하지 않는다.
- 제품 코드·runtime data·Scene·asset 변경 없음.
- 기존 simulator는 재사용 후보지만 11 계약은 아직 runtime 구현 검증되지 않았다.
- Human/Player validation: `NOT_RUN`.
- 제품 구현: `BLOCKED`.
