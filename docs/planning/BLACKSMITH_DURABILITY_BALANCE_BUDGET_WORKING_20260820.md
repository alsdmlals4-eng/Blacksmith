# [승인된 테스트 Budget / 튜닝중] Blacksmith CURRENT/MAX 내구도 Balance Budget

- Parent: `BS-ENHANCE-20260820-05~10`
- 상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- 구현: `BLOCKED`
- Human/Player evidence: `NOT_RUN`

## 1. 목적

내구도는 강화의 긴장을 높이되 자동 유지비·숨은 즉사·반복 수리 노동으로 변하지 않는다.

핵심 분리:

```text
CURRENT = 단기 생존 버퍼
MAX = 누적 구조 흉터
0% = 물리 작품 DESTROYED
```

일반 수리는 `CURRENT = MAX`, MAX는 유지한다.

## 2. CURRENT 손실 Budget

| 경험 밴드 | 일반 CURRENT 손상 | 심각 CURRENT 손상 |
|---|---:|---:|
| `LEARN` | `0%` | `0%` |
| `BUILD_CONFIDENCE` | `3~6%` | 없음 |
| `FIRST_STOP_POINT` | `4~8%` | `10~15%` |
| `TENSION` | `6~12%` | `15~25%` |
| `HIGH_STAKES` | `10~20%` | `25~50%` |
| `MASTERY` | 후속 튜닝 | 후속 튜닝 |

- 100% 작품이 일반 실패 한 번으로 바로 파괴되지 않는다.
- 파괴는 주로 `이미 손상된 작품 + 추가 욕심`에서 현실화한다.

## 3. MAX 구조 손상 Budget — BS-ENHANCE-20260820-09

MAX 손상은 실패 뒤 2차 판정이다.

| 경험 밴드 | `P(MAX scar | failure)` | MAX 손실 |
|---|---:|---:|
| `LEARN` | `0%` | `0` |
| `BUILD_CONFIDENCE` | `0%` | `0` |
| `FIRST_STOP_POINT` | `0~5%` | `-1~-3` |
| `TENSION` | `8~12%` | `-2~-5` |
| `HIGH_STAKES` | `12~20%` | `-4~-10` |
| `MASTERY` | `15~25%` | `-6~-15` |

플레이어에게는 최종 시도 기준 구조 손상 가능성을 공개한다.

```text
P(MAX scar per attempt)
= P(failure) × P(MAX scar | failure)
```

한 시도에서 MAX scar는 최대 1회다.

## 4. MAX 상태 페널티 Budget

| MAX | 상태 | 성공률 보정 | 신규 강화 효과 |
|---|---|---:|---:|
| `81~100` | `STABLE` | `0pp` | `100%` |
| `61~80` | `STRESSED` | `-3pp` | `100%` |
| `41~60` | `DAMAGED` | `-6pp` | `95%` |
| `21~40` | `FRACTURED` | `-10pp` | `90%` |
| `1~20` | `CRITICAL` | `-15pp` | `80%` |
| `0` | `DESTROYED` | 불가 | 불가 |

기존 획득 성능은 소급 감소하지 않는다.

## 5. 실패 resolution

```text
SUCCESS
or FAILURE
  → FAIL_HOLD
  → FAIL_DOWNGRADE
  → FAIL_DAMAGE
  → FAIL_CRITICAL_DAMAGE
```

`FAIL_CRITICAL_DAMAGE`에서만 MAX scar를 판정한다.

적용 순서:

```text
CURRENT direct loss
→ MAX direct loss
→ CURRENT = min(CURRENT, MAX)
→ CURRENT==0 or MAX==0이면 DESTROYED
```

MAX loss를 CURRENT에서 별도로 한 번 더 차감하지 않는다.

## 6. 일반 수리 불변식

```text
REPAIR_CURRENT
precondition: 0 < CURRENT < MAX
result: CURRENT = MAX
MAX = unchanged
failure_recovery_progress = unchanged
```

- 한 작품의 일반 수리는 **한 번의 공방 수리 행동**으로 끝낸다.
- 부분수리·5% 단위 연타수리·자동수리는 첫 Vertical Slice에서 사용하지 않는다.
- 정확한 하루 작업량 포인트는 아직 고정하지 않지만 수리는 다른 공방 작업과 경쟁하는 `REPAIR_JOB`으로 취급한다.
- 일반 수리는 MAX를 복원하지 않는다.
- 첫 Vertical Slice에는 MAX 완전 복구/대수선 기능을 넣지 않는다.

## 7. BS-ENHANCE-20260820-10 — 수리 경제 승인

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`

### A. 최종 시장가 × 결손 CURRENT

```text
repair_cost ∝ final_sale_value × missing_current
```

장점:
- 플레이어가 비싼 작품은 비싸게 고친다고 직관적으로 이해하기 쉽다.

문제:
- 강화·수식어·예술성·연대기·고객 수요가 이미 최종 가치에 반영되므로 수리비가 같은 프리미엄을 다시 과금할 수 있다.
- 강화/감정/수식어 적용 순서에 따라 수리비가 달라지는 정답 순서를 만들기 쉽다.

판정: `REJECT`.

### B. 다음 강화 시도 비용 × 결손 CURRENT

```text
repair_cost ∝ next_attempt_cost × missing_current
```

장점:
- `수리 vs 한 번 더 강화` 비용 비교가 쉽다.

문제:
- 체크포인트/특수 강화에서 다음 시도 비용이 급변하면 수리비까지 튄다.
- 강화가 끝난 작품이나 납품 대기 작품에는 기준이 부자연스럽다.
- 실제 다음 시도 비용에 종속되면 수리 시점 최적화가 메타가 된다.

판정: `REJECT_AS_RUNTIME_FORMULA / USE_ONLY_AS_BALANCE_REFERENCE`.

### C. 안정된 수리 참조비용 + 고정 준비비 + 절대 결손 포인트 비례 — 채택

런타임 수리비는 시장가/다음 강화비가 아니라 **수리 전용 참조비용표**를 사용한다.

```text
missing_current_points = MAX - CURRENT

repair_cost
= REPAIR_REFERENCE_COST[structural_family, secured_band]
× (setup_fraction + variable_fraction × missing_current_points / 100)
```

승인된 첫 테스트 shell:

```text
setup_fraction    = 0.05
variable_fraction = 0.65
```

따라서 표준 참조비용 `R` 대비 대략:

| 결손 CURRENT | 수리비 목표 |
|---|---:|
| `1~20pt` | 약 `6~18% × R` |
| `21~50pt` | 약 `19~38% × R` |
| `51~75pt` | 약 `38~54% × R` |
| `76~99pt` | 약 `54~69% × R` |

숫자는 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`이며 출시 최종 수치가 아니다.

### REPAIR_REFERENCE_COST의 의미

`R`은 플레이어가 얻는 최종 시장가가 아니다.

포함 후보:
- 기본 작품 구조/무기군
- 주재료 구조 가치
- 현재 확보된 강화 위험 밴드의 수리 복잡도

제외:
- 현재 공개시장 판매가
- 예술성 프리미엄
- 촉매/수식어 프리미엄
- 연대기/명성 가치
- 고객 수요 배율
- 현재 성공률
- 실패 누적 회복
- 실제 다음 강화가 특수 강화인지 여부

`R`은 같은 확보 밴드 안에서 안정된 data table 값으로 유지한다. 다음 강화 시도의 실제 비용을 런타임 공식에 직접 넣지 않는다.

## 8. MAX 손상 이중 과금 금지

수리 가능한 양은 비율이 아니라 **절대 결손 포인트**다.

```text
MAX 50 / CURRENT 20
missing_current_points = 30
```

`CURRENT/MAX = 40%`를 수리비 배율로 사용하지 않는다.

이유:
- 낮은 MAX는 이미 성공률과 신규 강화 효과에 장기 페널티를 준다.
- MAX가 낮다는 사실만으로 일반 수리까지 더 비싸게 만들면 구조 흉터를 중복 과금한다.
- 일반 수리는 오직 `MAX - CURRENT`를 복구한다.

## 9. 자원·작업량 정책

첫 Vertical Slice 승인 구조:

- 새 수리 전용 화폐/토큰은 만들지 않는다.
- 기존 골드 + 기존 구조/일반 재료 계열을 재사용한다.
- 희귀한 MAX 복구 전용 재료는 일반 수리에 쓰지 않는다.
- 일반 수리는 `REPAIR_JOB` 1회로 끝난다.
- 정확한 `DAY_WORK_COST`는 하루 작업량 시스템 최종 정본과 함께 튜닝한다.

### 왜 고정 준비비가 필요한가

준비비가 없으면 `CURRENT -1` 같은 잔기스도 거의 공짜라 매 손상마다 수리가 정답이 되기 쉽다.

고정 준비비는 작은 손상을 모아 수리할지, 지금 바로 안전 버퍼를 회복할지의 선택을 만든다.

## 10. 강화와의 상대 비용 검증

런타임 수리 공식은 실제 다음 강화비에 종속하지 않지만, Balance Lab에서는 같은 경험 밴드의 **일반 강화 1회 참조비용**과 비교한다.

첫 목표:

- 경미한 수리: 일반 강화 1회 참조보다 충분히 저렴하되 `매번 즉시 수리`가 자동 정답은 아님.
- 중간 손상: 강화 1회와 실제로 경쟁하는 비용.
- 심각 손상: 대부분 강화 1회보다 저렴하지만, 작업 기회비용 때문에 `그대로 한 번 더` 선택도 남음.
- 특수 체크포인트 강화의 일시적 비용 폭증은 수리 기준값에 직접 전파하지 않음.

정확 비율은 Human/Simulation 전 `NOT_FINAL`이다.

## 11. 수리가 변경하지 않는 것

일반 수리는 다음을 변경하지 않는다.

```text
MAX durability
MAX scar history
enhancement level
secured checkpoint
failure recovery progress
existing affixes / artistry / chronicle
customer/world history
```

특히 실패 누적 회복을 수리 때문에 초기화하지 않는다. 안전 행동을 택했다고 이미 얻은 실패 회복 진전을 벌주지 않는다.

## 12. 수리 경제 5회 적대 검토 결론

### Loop 1 — 작은 손상마다 무조건 수리하는가
- 공격: 순수 비례식이면 1~5pt 손상 수리가 거의 공짜다.
- 방어: `setup_fraction` + 한 번의 공방 작업 기회비용을 둔다.
- 재검사: 작은 손상은 모아서 수리할 이유가 생긴다.

### Loop 2 — 반대로 수리를 아무도 안 하는가
- 공격: 수리 작업이 너무 무거우면 CURRENT 시스템 자체가 장식이 된다.
- 방어: 한 번의 `REPAIR_JOB`으로 CURRENT를 MAX까지 모두 회복하고 부분수리를 없앤다. 수리비는 같은 밴드 일반 강화 1회보다 대체로 낮은 범위에서 먼저 테스트한다.
- 재검사: 중·저 CURRENT에서 실제 안전 선택이 남는다.

### Loop 3 — 작업 순서 악용이 생기는가
- 공격: 판매가나 실제 다음 강화비를 쓰면 `수리 먼저/수식어 먼저/강화 먼저`의 비용 최적 순서가 생긴다.
- 방어: 최종 판매가·수식어·연대기·실제 next-attempt cost를 공식에서 제외하고 안정된 `REPAIR_REFERENCE_COST` table을 사용한다.
- 재검사: 수리비가 가치 연출이나 특수 강화 순간에 따라 출렁이지 않는다.

### Loop 4 — MAX 흉터를 이중 처벌하는가
- 공격: `(MAX-CURRENT)/MAX` 비율을 쓰면 MAX가 낮은 작품일수록 같은 30pt 복구가 더 비싸진다.
- 방어: `MAX-CURRENT` 절대 포인트만 수리량으로 사용하고 MAX 자체에는 할증을 붙이지 않는다.
- 재검사: MAX는 장기 강화 리스크, CURRENT 수리는 단기 생존 비용으로 역할이 분리된다.

### Loop 5 — 수리가 유지보수 노가다로 변하는가
- 공격: 자동 마모 + 부분수리 + 여러 전용 재료가 결합되면 강화보다 정비가 메인이 된다.
- 방어: 자동 일일 마모 없음, 수리 한 행동, 새 화폐 없음, MAX 복구 없음, 일반 수리 UI는 단일 견적/확정으로 제한한다.
- 재검사: 수리는 강화 선택을 보조하고 메인 루프를 대체하지 않는다.

## 13. 첫 검증 신호

다음은 PASS가 아니라 튜닝 신호다.

### 수리가 너무 싸거나 편함
- 작은 손상 후 대부분의 플레이어가 생각 없이 즉시 수리한다.
- `수리하지 않고 도전`이 사실상 사라진다.
- 수리 여부를 보기 전에 자동 클릭한다.

### 수리가 너무 비싸거나 무거움
- CURRENT가 매우 낮아도 거의 아무도 수리하지 않는다.
- 수리 대신 새 작품 제작이 항상 싸다.
- 수리 작업 때문에 강화 세션이 자주 끊긴다.

### 수리 경제가 적절함
- 높은 CURRENT에서는 손상을 감수하는 선택이 흔하다.
- 낮은 CURRENT에서는 수리가 강하게 매력적이지만 여전히 비용/작업량을 아끼고 밀어붙이는 사례가 존재한다.
- MAX가 손상된 작품을 수리해도 `완전히 안전해졌다`고 오해하지 않는다.

## 14. 튜닝 순서

기존 09 순서 뒤에 수리 경제를 붙인다.

1. MAX scar 발생률
2. MAX 손실량
3. CURRENT 손실량
4. MAX 성공률 페널티
5. 신규 강화 효과 배율
6. 수리 `setup_fraction`
7. 수리 `variable_fraction`
8. `REPAIR_REFERENCE_COST` band table
9. 수리 작업량 부담

한 번에 여러 축을 바꾸지 않는다.

## 15. 완료 경계

- `BS-ENHANCE-20260820-09`는 승인된 테스트 Budget이다.
- `BS-ENHANCE-20260820-10`은 **USER_APPROVED**이며 C 구조를 현재 수리 경제 정본으로 사용한다.
- `setup_fraction=0.05`, `variable_fraction=0.65`와 구간별 `R` 비율은 승인된 첫 테스트값이며 출시 최종 수치가 아니다.
- 정확 `REPAIR_REFERENCE_COST` table과 `DAY_WORK_COST`는 후속 Balance Decision에서 정교화한다.
- 기존 시뮬레이터·런타임에는 아직 CURRENT/MAX/수리 경제를 구현하지 않는다.
- 제품 구현: `BLOCKED`.