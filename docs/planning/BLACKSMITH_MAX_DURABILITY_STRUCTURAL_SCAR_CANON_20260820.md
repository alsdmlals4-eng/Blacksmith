# [현재 승인] Blacksmith 최대 내구도 구조 손상·강화 리스크 계약

- Parent: `BS-CORE-20260820-01`
- Refines: `BS-ENHANCE-20260820-06`, `BS-ENHANCE-20260820-07`
- Decisions: `BS-ENHANCE-20260820-07`, `BS-ENHANCE-20260820-08`
- 사용자 승인: `2026-08-20 KST / 보호재 기본 제외 + 최대 내구도 손상으로 수리 후에도 강화 리스크 유지`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- 기준 main: `c9781e73141988ea46d80f3f8200941411d5a258`

## 1. BS-ENHANCE-20260820-07 — 별도 파괴 방지 기본 제외

첫 Vertical Slice의 기본 강화에는 별도의 `0% 파괴 방지 보험`을 두지 않는다.

이 Decision은 기존 제안 A를 승인하되 다음과 같이 정제한다.

```text
안전 선택 = 현재 작품을 수리하고 멈추거나 다시 강화 준비
도전 선택 = 현재/최대 내구도 상태를 감수하고 추가 강화
```

그러나 일반 수리가 리스크를 완전히 리셋하지 않는다. 일반 수리는 `CURRENT_DURABILITY`만 회복하고 `MAX_DURABILITY`의 구조 손상은 복구하지 않는다.

따라서 `수리 = 안전 선택`이지만 `수리 = 새 작품으로 완전 초기화`가 아니다.

## 2. BS-ENHANCE-20260820-08 — 현재 내구도 + 최대 내구도 이중 구조

새 작품은 다음 상태에서 시작한다.

```yaml
CURRENT_DURABILITY_PERCENT: 100
MAX_DURABILITY_PERCENT: 100
```

항상 다음 불변식을 지킨다.

```text
0 <= CURRENT_DURABILITY_PERCENT <= MAX_DURABILITY_PERCENT <= 100
```

### CURRENT_DURABILITY_PERCENT

- 단기 손상 상태다.
- 강화 실패·실제 고객/세계 사건으로 감소할 수 있다.
- 공방 일반 수리로 현재 `MAX_DURABILITY_PERCENT`까지 회복할 수 있다.
- `0%`가 되면 물리 작품은 `DESTROYED`다.

### MAX_DURABILITY_PERCENT

- 작품의 누적 구조 건전성 한계다.
- 일반 수리로 증가하지 않는다.
- 심각한 강화 실패 또는 별도 승인된 구조 손상 사건이 감소시킨다.
- MAX가 CURRENT 아래로 내려가면 CURRENT도 새 MAX로 clamp한다.
- MAX가 `0%`가 되면 CURRENT도 `0%`가 되고 작품은 `DESTROYED`다.

예:

```text
강화 전   CURRENT 72 / MAX 84
심각 실패 CURRENT -18 / MAX -6
결과       CURRENT 54 / MAX 78
일반 수리 CURRENT 78 / MAX 78
```

수리 후에도 작품은 새 작품 `100 / 100`으로 돌아가지 않는다.

## 3. 최대 내구도 손상 소유권

기본 실패 결과의 책임을 분리한다.

```text
FAIL_HOLD
- CURRENT 손실 없음
- MAX 손실 없음

FAIL_DOWNGRADE
- 체크포인트 내 제한 단계 하락
- CURRENT 기본 유지
- MAX 손실 없음

FAIL_DAMAGE
- CURRENT 손실
- MAX 기본 유지

FAIL_CRITICAL_DAMAGE
- CURRENT 큰 손실
- MAX 구조 손실 가능
- 0% 도달 시 DESTROYED
```

일반 실패마다 MAX를 깎지 않는다. 그렇지 않으면 리스크가 긴장보다 누적 유지비 세금으로 변한다.

고객/세계 사건도 단순 사용만으로 MAX를 깎지 않는다. `파손·변형·구조 균열·심각한 환경 손상`처럼 직접 인과가 있는 사건만 MAX 손상 후보가 된다.

## 4. 일반 수리 계약

```text
REPAIR_CURRENT
CURRENT_DURABILITY_PERCENT = MAX_DURABILITY_PERCENT
MAX_DURABILITY_PERCENT = unchanged
```

- 여러 번 클릭하는 수리 작업을 기본 UX로 만들지 않는다.
- 수리 비용·작업량은 결손 CURRENT와 작품 가치에 비례하는 튜닝 후보다.
- 일반 수리로 MAX를 올리지 않는다.
- 첫 Vertical Slice에는 MAX 완전 복원 기능을 넣지 않는다.

후속의 `STRUCTURAL_REBUILD / 대수선`은 별도 Decision 없이는 추가하지 않는다. 추가하더라도 공짜 완전 초기화가 되어서는 안 된다.

## 5. 최대 내구도가 강화에 미치는 영향

목표는 `수리하면 강화 리스크가 사라지는 문제`를 막는 것이다.

세 가지 접근을 비교했다.

### A. 성공률만 감소

단순하지만 플레이가 확률표 최적화로 수렴하기 쉽다.

### B. 작품 기존 성능까지 감소

손상 체감은 강하지만 애착 작품이 빠르게 폐기되는 죽음의 나선 위험이 크다.

### C. 성공률 페널티 우선 + 심각 손상에서 미래 강화 효과 감소 — 채택

- MAX가 조금 손상됐을 때는 강화 성공 기대만 소폭 악화한다.
- 구조 손상이 누적된 뒤에는 **앞으로 새로 얻는 강화 효과**도 약해진다.
- 이미 획득한 공격력·방어력·수식어·과거 강화 보상을 소급 삭감하지 않는다.
- 단순히 MAX가 낮다는 이유로 기존 고객 결과를 재작성하지 않는다.

## 6. 첫 Balance Band — TUNABLE, NOT FINAL

| MAX 내구도 | 구조 상태 | 강화 성공률 보정 | 새 강화 효과 배율 |
|---|---|---:|---:|
| `81~100%` | `STABLE` | `0pp` | `100%` |
| `61~80%` | `STRESSED` | `-3pp` | `100%` |
| `41~60%` | `DAMAGED` | `-6pp` | `95%` |
| `21~40%` | `FRACTURED` | `-10pp` | `90%` |
| `1~20%` | `CRITICAL` | `-15pp` | `80%` |
| `0%` | `DESTROYED` | 강화 불가 | 강화 불가 |

이 숫자는 `TUNABLE_BASELINE_TEST_PRESET`이며 Human/Player validation 전 확정하지 않는다.

### 적용 원칙

- 성공률 페널티는 강화 전 화면에서 숨기지 않는다.
- 실패 누적 회복은 MAX를 복구하지 않는다.
- 실패 누적 회복이 성공률을 일부 되돌려도 `새 강화 효과 배율` 저하는 그대로 남는다.
- MAX 손상 하나에 `성공률↓ + 기존 성능↓ + 파괴확률↑`를 동시에 기본 적용하지 않는다.
- 최대 내구도 저하 자체로 과거 성공 보상을 소급 박탈하지 않는다.

## 7. 강화 효과 감소의 정확한 의미

`새 강화 효과 배율`은 **그 시도에서 성공했을 때 새로 추가되는 강화 성장량**에만 적용한다.

예:

```text
정상 구조에서 성공 시 공격 +10
MAX 50% / effect multiplier 95%
→ 동일 강화 성공 시 신규 증가량은 +9~10 범위의 규칙화된 값
```

정확한 반올림·최소 증가량은 구현 전 Balance Contract에서 정한다.

이미 보유한 기존 강화 공격력은 MAX 손상으로 자동 감소하지 않는다.

## 8. 강화 전 P0 정보

강화 화면은 최소 다음을 한 화면에서 읽을 수 있어야 한다.

```text
현재 강화 단계 / 체크포인트
CURRENT 내구도 NN%
MAX 내구도 MM%
구조 상태 이름
기본 성공률
MAX 내구도에 의한 성공률 보정
최종 성공 기대
실패 시 CURRENT 손상 가능성
심각 실패 시 MAX 손상 가능성
이번 성공의 신규 강화 효과 배율
실패 누적 회복
다음 체크포인트
```

수학 전체를 펼치지 않고 `왜 불리해졌는지`를 2~4개 원인으로 설명한다.

## 9. DDD와의 연결

이중 내구도는 강화 버튼을 누르기 전 세 종류의 손실을 구분하게 한다.

```text
단기 손실: CURRENT
누적 흉터: MAX
최종 손실: 0% DESTROYED
```

따라서 플레이어 질문은 다음처럼 바뀐다.

> `현재 내구도는 수리하면 되지만, 최대 내구도까지 또 깎일 위험을 감수하고 이 작품을 더 밀어붙일 것인가?`

이 질문이 Blacksmith의 `멈춤 vs 추가 도전`을 강화해야 한다.

## 10. 재검토 조건

다음이 관찰되면 구조를 조정한다.

- MAX가 한두 번의 실패만으로 너무 빨리 내려가 애착 작품을 즉시 폐기하게 된다.
- MAX 페널티 때문에 손상된 작품은 다시 강화할 이유가 전혀 없어진다.
- 플레이어가 모든 시도 전에 무조건 수리해도 여전히 리스크 판단이 없다.
- 반대로 수리가 의미 없어져 CURRENT가 장식 수치가 된다.
- 실패 누적 회복과 MAX 성공률 페널티가 서로 상쇄되어 이해하기 어렵다.
- 성공률·CURRENT·MAX·효과 배율을 동시에 보여줘 모바일 화면이 계산표가 된다.

## 11. 증거 경계

- 기존 `DURABILITY` 정수 표현은 역사 기획이며 새 `%` 이중 구조와 자동 변환하지 않는다.
- 정확한 MAX 손실량·발생 확률·성공률 보정·효과 배율은 `NOT_FINAL`.
- Human/Player validation: `NOT_RUN`.
- 제품 구현: `BLOCKED`.
