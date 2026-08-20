# [승인된 테스트 Budget / 튜닝중] Blacksmith CURRENT/MAX 내구도 Balance Budget

- Parent: `BS-ENHANCE-20260820-05~09`
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

## 6. 수리 Budget 원칙

공방 일반 수리:

```text
CURRENT 1~MAX → MAX
MAX unchanged
```

- 여러 번 클릭하지 않는다.
- 비용·작업량은 `missing CURRENT × item value context`에 비례하는 후보로 유지한다.
- MAX를 복원하지 않는다.
- 첫 Vertical Slice에는 MAX 완전 복구/대수선 기능을 넣지 않는다.

## 7. 세계 활동

단순 시간 경과로 CURRENT/MAX가 자동 감소하지 않는다.

CURRENT 손상 후보:
- 경미 마모 `1~5%`
- 의미 있는 노출/충격 `5~12%`
- 큰 사건 `10~25%`

MAX 손상은 `파손·변형·구조 균열·심각 환경 손상`처럼 직접 구조 손상 인과가 있는 별도 사건만 허용한다. 정확 세계 MAX Budget은 후속 Decision이다.

## 8. 시뮬레이션 지표

- 밴드별 SUCCESS/FAIL family 분포
- `P(MAX scar per attempt)`와 `P(MAX scar | failure)`
- 첫 MAX 흉터까지 실패 횟수
- N회 강화 후 CURRENT/MAX 분포
- 체크포인트 도달 전 MAX 손상률
- `MAX <= 60 / 40 / 20` 도달 비율
- 파괴까지 평균·중앙 시도 수
- 수리 횟수와 MAX 상태 상관
- 손상 후 계속/수리/멈춤 비율
- 지배 전략 여부

## 9. Human 검증 질문

- CURRENT와 MAX 차이를 이해하는가
- 수리가 안전하지만 완전 초기화는 아니라는 점을 이해하는가
- MAX scar 전에 위험을 읽었는가
- 파괴 후 `불공정`보다 `내가 무리했다`고 설명하는가
- MAX가 손상돼도 작품을 계속 사용할 이유가 남는가

## 10. 09 Budget 5회 적대 검토 결론

1. **조건부 확률 혼동:** 내부는 실패 후 conditional, UI는 per-attempt 최종 위험으로 표시.
2. **초반 영구 손상:** LEARN/BUILD_CONFIDENCE MAX scar 0%.
3. **연속 흉터 폭주:** 한 시도 scar 1회, 밴드별 MAX loss 상한.
4. **이중 벌점:** DOWNGRADE와 CRITICAL을 분리하고 MAX loss를 CURRENT에 이중 차감하지 않음.
5. **손상 작품 폐기 수렴:** 기존 성능 소급 감소 금지, 먼저 발생률→손실량 순으로 튜닝.

## 11. 튜닝 순서

1. MAX scar 발생률
2. MAX 손실량
3. CURRENT 손실량
4. MAX 성공률 페널티
5. 신규 강화 효과 배율
6. 수리 경제

여러 축을 동시에 흔들지 않는다.

## 12. 완료 경계

이 문서는 승인된 **시뮬레이션/첫 플레이테스트 시작 Budget**이다. 출시 최종 수치는 아니다. 기존 `tools/simulate_enhancement_balance.py` 계열은 재사용 후보지만 CURRENT/MAX 계약 반영은 제품 구현 Gate 이후 별도 작업이다.
