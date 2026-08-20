# [현재 승인] Blacksmith 최대 내구도 구조 손상·강화 리스크 계약

- Parent: `BS-CORE-20260820-01`
- Refines: `BS-ENHANCE-20260820-06~08`
- Decisions: `BS-ENHANCE-20260820-07`, `BS-ENHANCE-20260820-08`, `BS-ENHANCE-20260820-09`
- 사용자 승인: `2026-08-20 KST / MAX 구조 손상 Balance 시작안 승인`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. BS-ENHANCE-20260820-07 — 별도 파괴 방지 기본 제외

첫 Vertical Slice 기본 강화에는 별도의 `0% 파괴 방지 보험`을 두지 않는다.

```text
안전 선택 = CURRENT를 MAX까지 수리하고 멈추거나 다시 준비
도전 선택 = CURRENT/MAX 상태를 감수하고 추가 강화
```

일반 수리는 리스크를 완전히 초기화하지 않는다. `CURRENT_DURABILITY_PERCENT`만 현재 MAX까지 회복하며 구조 손상인 MAX는 복구하지 않는다.

## 2. BS-ENHANCE-20260820-08 — CURRENT/MAX 이중 내구도

```yaml
NEW_ITEM:
  CURRENT_DURABILITY_PERCENT: 100
  MAX_DURABILITY_PERCENT: 100
```

불변식:

```text
0 <= CURRENT_DURABILITY_PERCENT <= MAX_DURABILITY_PERCENT <= 100
```

- `CURRENT`: 단기 생존 버퍼. 일반 수리 가능.
- `MAX`: 누적 구조 건전성. 일반 수리 불가.
- 일반 수리: `CURRENT = MAX`, `MAX = unchanged`.
- MAX가 CURRENT 아래로 내려가면 CURRENT를 새 MAX로 clamp한다.
- CURRENT 또는 MAX가 `0%`면 물리 작품은 `DESTROYED`다.
- UID·이름·제작·강화·소유·손상·수리·파괴 원인·Chronicle provenance는 기록으로 보존한다.

예:

```text
강화 전   CURRENT 72 / MAX 84
심각 실패 CURRENT -18 / MAX -6
결과       CURRENT 54 / MAX 78
일반 수리 CURRENT 78 / MAX 78
```

## 3. 실패 outcome 책임

```text
FAIL_HOLD
- CURRENT 유지
- MAX 유지

FAIL_DOWNGRADE
- 체크포인트 내 제한 단계 하락
- CURRENT 기본 유지
- MAX 유지

FAIL_DAMAGE
- CURRENT 손상
- MAX 유지

FAIL_CRITICAL_DAMAGE
- CURRENT 큰 손상
- MAX 구조 손상 가능
- 단계 하락과 기본 중첩하지 않음
```

일반 실패마다 MAX를 깎지 않는다. 성공 강화·단순 시간 경과·일상 사용도 자동 MAX 손상 원인이 아니다.

## 4. MAX 구조 상태가 강화에 미치는 영향

채택 구조는 `성공률 페널티 우선 + 심각 손상에서 미래 강화 효과 감소`다.

| MAX 내구도 | 구조 상태 | 강화 성공률 보정 | 새 강화 효과 배율 |
|---|---|---:|---:|
| `81~100%` | `STABLE` | `0pp` | `100%` |
| `61~80%` | `STRESSED` | `-3pp` | `100%` |
| `41~60%` | `DAMAGED` | `-6pp` | `95%` |
| `21~40%` | `FRACTURED` | `-10pp` | `90%` |
| `1~20%` | `CRITICAL` | `-15pp` | `80%` |
| `0%` | `DESTROYED` | 강화 불가 | 강화 불가 |

이 표는 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`다.

- 이미 획득한 공격력·방어력·수식어·과거 강화 보상은 소급 삭감하지 않는다.
- `새 강화 효과 배율`은 그 시도에서 새로 얻는 성장량에만 적용한다.
- 실패 누적 회복과 CURRENT 수리는 MAX를 복구하지 않는다.
- MAX 저하 자체에 별도 파괴 확률 보너스를 자동 추가하지 않는다.

## 5. BS-ENHANCE-20260820-09 — MAX 구조 손상 Balance 시작 Budget

### 5.1 판정 방식

MAX 구조 손상은 **전체 시도와 독립된 별도 즉사 주사위가 아니다. 실패가 발생한 뒤의 2차 failure-family 판정**이다.

```text
강화 시도
→ 최종 성공률로 SUCCESS / FAILURE 판정
→ FAILURE인 경우 failure family 판정
→ 일부 FAILURE만 FAIL_CRITICAL_DAMAGE
→ FAIL_CRITICAL_DAMAGE일 때만 MAX 구조 손상
```

내부 Balance 변수:

```text
critical_scar_chance_given_failure
max_durability_loss_when_scar
```

플레이어 UI에서는 조건부 수학을 강요하지 않고 최종 계산된 **이번 시도의 구조 손상 가능성**을 공개한다.

```text
P(structural scar per attempt)
= P(failure) × P(critical scar | failure)
```

### 5.2 승인된 첫 테스트 범위

| 경험 밴드 | 실패 후 MAX 구조 손상 판정 | 발생 시 MAX 손실 | 상태 |
|---|---:|---:|---|
| `LEARN` | `0%` | `0` | 승인 시작값 |
| `BUILD_CONFIDENCE` | `0%` | `0` | 승인 시작값 |
| `FIRST_STOP_POINT` | `0~5%` | `-1~-3` | 승인 테스트 범위 |
| `TENSION` | `8~12%` | `-2~-5` | 승인 테스트 범위 |
| `HIGH_STAKES` | `12~20%` | `-4~-10` | 승인 테스트 범위 |
| `MASTERY` | `15~25%` | `-6~-15` | 승인 테스트 범위 |

이 범위는 사용자가 승인한 **공식 시뮬레이션/첫 플레이테스트 시작 Budget**이다. 범위 자체가 출시 최종 수치를 뜻하지는 않는다.

### 5.3 초반 보호

- `LEARN`과 `BUILD_CONFIDENCE`에서는 MAX 구조 손상이 발생하지 않는다.
- 첫 영구 흉터는 `FIRST_STOP_POINT` 이후에만 열린다.
- 첫 10분 경험이 `영구 손상 튜토리얼`로 변하지 않도록 한다.

### 5.4 한 시도의 구조 손상 상한

- 한 강화 시도에서 MAX 구조 손상 event는 최대 1회다.
- `FAIL_CRITICAL_DAMAGE`는 `FAIL_DOWNGRADE`와 동시에 발생하지 않는다.
- 별도 `destroy roll`을 추가하지 않는다. 파괴는 CURRENT/MAX 실제 수치가 0에 도달했을 때만 발생한다.

### 5.5 CURRENT/MAX 손실 적용 순서

중복 손실을 막기 위해 다음 순서를 고정한다.

```text
1. failure family 결정
2. CURRENT direct loss 적용
3. CRITICAL이면 MAX direct loss 적용
4. CURRENT = min(CURRENT_after_direct_loss, MAX_after_loss)
5. CURRENT == 0 or MAX == 0 → DESTROYED
```

MAX 손실량을 CURRENT에서 다시 한 번 별도로 빼지 않는다. MAX가 CURRENT 아래로 내려온 경우에만 clamp로 추가 영향을 받는다.

## 6. Better Alternative Search

### A. 시도마다 독립적으로 MAX 손상 판정
- 성공한 시도에도 구조 손상 주사위를 붙이기 쉬워 인과가 흐려진다.
- 비채택.

### B. 실패 후 conditional critical-scar 판정 — 채택
- 실패 안에서만 영구 흉터가 생겨 결과 인과가 읽힌다.
- 성공률이 낮은 위험 구간에서는 per-attempt 구조 손상 위험도 자연스럽게 증가한다.
- 채택.

### C. N회 실패마다 확정 MAX 손상
- 예측 가능하지만 실패 횟수 최적화와 조작이 메타가 되기 쉽다.
- baseline 비채택. 필요 시 별도 사건형 시스템으로만 재검토.

## 7. 강화 전 P0 정보

기본 화면:

```text
현재 강화 단계 / 체크포인트
CURRENT NN% / MAX MM%
구조 상태
최종 성공 기대
이번 실패의 주요 결과
이번 시도의 구조 손상 가능성
구조 손상 시 MAX 예상 손실 범위
신규 강화 효과 배율
실패 누적 회복
다음 체크포인트
```

상세 보기에서만 기본 성공률→회복→MAX 페널티→failure-family 계산을 펼친다.

## 8. Balance 튜닝 순서

문제가 발생하면 원인을 섞지 않기 위해 다음 순서로 조정한다.

1. `critical_scar_chance_given_failure`
2. `max_durability_loss_when_scar`
3. CURRENT direct loss
4. MAX 상태별 성공률 페널티
5. 신규 강화 효과 배율

즉 구조 손상이 너무 자주 느껴질 때 곧바로 기존 보상이나 전체 성공률을 흔들지 않는다.

## 9. 시뮬레이션 지표

기존 강화 시뮬레이터 재사용 시 최소 다음을 측정한다.

- 경험 밴드별 `P(structural scar per attempt)`
- 경험 밴드별 `P(structural scar | failure)`
- 첫 MAX 흉터까지 평균/중앙 실패 횟수
- 체크포인트 도달 전 MAX 손상률
- N회 강화 후 MAX 분포
- `MAX <= 60 / <= 40 / <= 20` 도달 비율
- 구조 손상 후 계속 강화 / 수리 후 강화 / 멈춤 비율
- CURRENT 수리 횟수와 MAX 상태의 상관
- 파괴 원인 중 CURRENT 소진 vs MAX 소진 비율

Human/Player:

- 영구 흉터가 발생하기 전에 위험을 이해했는가
- 손상 결과를 `숨은 즉사`가 아니라 자기 도전의 결과로 설명하는가
- MAX 손상 후에도 작품을 계속 쓸 이유가 남는가
- CURRENT 수리가 의미 있지만 완전 리셋은 아니라는 것을 이해하는가

## 10. 재검토 조건

다음이면 09 Budget을 조정한다.

- FIRST_STOP_POINT 이전에 MAX 손상 경험이 발생한다.
- 한두 번의 critical scar만으로 작품을 사실상 폐기한다.
- HIGH_STAKES에서 모든 합리적 플레이가 강화 포기로 수렴한다.
- 반대로 MAX 구조 손상이 너무 희박해 플레이어가 존재를 무시한다.
- 구조 손상과 CURRENT 손상의 중복 계산을 플레이어가 이중 벌점으로 느낀다.
- 구조 손상 가능성을 이해하려면 상세 수학 화면을 반드시 열어야 한다.

## 11. 증거 경계

- `BS-ENHANCE-20260820-09`의 범위는 **승인된 테스트 Budget**이다.
- 출시 최종 확률·손실량은 `NOT_FINAL`.
- 기존 simulator는 재사용 후보이며 새 CURRENT/MAX 계약을 아직 구현 검증하지 않았다.
- Human/Player validation: `NOT_RUN`.
- 제품 구현: `BLOCKED`.
