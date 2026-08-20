# Blacksmith 최대 내구도 구조 손상 — 적대적 검토 기록

- 대상: `BS-ENHANCE-20260820-07~09`
- 상태: `PLAN_REVIEW_EVIDENCE`
- Human/Player evidence: `NOT_RUN`

## A. 07~08 구조 설계 5회 검토

### Loop 1 — 수리로 리스크가 사라지는가
공격: CURRENT만 수리해도 MAX가 강화에 영향이 없으면 결국 완전 리셋과 다르지 않다.

개선: MAX가 성공 기대에 직접 페널티를 주고 심각 손상에서는 미래 강화 성장량도 감소한다.

재검사: CURRENT 수리는 즉사 위험을 낮추지만 누적 구조 리스크는 지우지 못한다.

### Loop 2 — 죽음의 나선인가
공격: 성공률↓, 기존 성능↓, 파괴위험↑를 동시에 적용하면 손상 작품은 즉시 폐기 대상이 된다.

개선: 기존 획득 성능은 소급 삭감하지 않고, MAX 저하 자체로 별도 파괴 확률을 추가하지 않는다.

### Loop 3 — MAX 손상이 유지비 세금인가
공격: 일반 실패마다 MAX가 줄면 모든 작품은 결국 강제 소모품이 된다.

개선: `FAIL_HOLD / FAIL_DOWNGRADE / FAIL_DAMAGE`는 MAX 유지. `FAIL_CRITICAL_DAMAGE`와 직접 구조 손상 사건만 MAX 감소.

### Loop 4 — CURRENT 수리가 무의미한가
공격: MAX만 중요하면 CURRENT는 장식이 된다.

개선: CURRENT 0%도 즉시 DESTROYED. 일반 수리는 CURRENT를 MAX까지 복구해 실제 생존 버퍼를 제공한다.

### Loop 5 — 모바일 계산표가 되는가
공격: CURRENT/MAX/성공률/회복/효과배율을 전부 펼치면 DDD 리듬이 깨진다.

개선: 기본 화면은 CURRENT/MAX, 구조 상태, 최종 성공 기대, 주요 손실, 신규 효과 배율 중심. 상세 계산은 별도 보기.

최종 구조 권장: **성공률 페널티 우선 + 심각 MAX 손상에서 미래 강화 효과 감소**.

## B. BS-ENHANCE-20260820-09 Balance Budget 5회 검토

### Loop 1 — 조건부 확률이 숨은 확률처럼 보이는가

공격:
- `P(MAX scar | failure)`를 내부 값으로 쓰면 플레이어는 실제 한 번 누를 때 위험을 계산하기 어렵다.

개선:
- 내부 밸런스는 실패 후 conditional 구조를 유지한다.
- UI는 `P(failure) × P(scar|failure)`로 계산한 **이번 시도의 최종 구조 손상 가능성**을 표시한다.
- 발생 시 MAX 손실 범위도 함께 공개한다.

재검사:
- 설계자는 failure family를 독립 튜닝할 수 있고 플레이어는 한 번의 선택 기준 위험을 이해할 수 있다.

### Loop 2 — 첫 세션에 영구 흉터가 너무 빨리 발생하는가

공격:
- 첫 강화 학습 중 MAX가 손상되면 플레이어는 강화의 쾌감보다 영구 손실부터 학습한다.

개선:
- `LEARN = 0%`, `BUILD_CONFIDENCE = 0%`.
- 첫 MAX scar는 `FIRST_STOP_POINT` 이후에만 열린다.

재검사:
- 첫 세션의 핵심은 안전 성공→확보점→첫 위험 판단 순서를 유지한다.

### Loop 3 — 고위험 구간에서 연속 흉터가 작품을 너무 빨리 죽이는가

공격:
- HIGH_STAKES/MASTERY에서 여러 critical이 연속되면 MAX가 빠르게 붕괴할 수 있다.

개선:
- 한 시도에서 MAX scar는 최대 1회.
- 밴드별 MAX loss 상한을 둔다.
- `FAIL_CRITICAL_DAMAGE` 외 실패는 MAX를 깎지 않는다.
- 문제가 생기면 성공률이나 기존 보상을 먼저 흔들지 않고 **scar occurrence → scar loss** 순으로 조정한다.

재검사:
- 영구 흉터는 기억에 남지만 모든 실패가 작품 수명을 깎는 구조는 아니다.

### Loop 4 — CURRENT와 MAX가 이중 벌점인가

공격:
- critical 실패에서 CURRENT -X, MAX -Y를 적용한 뒤 MAX 감소분을 CURRENT에서도 또 빼면 손실이 이중 계산된다.

개선:

```text
CURRENT direct loss
→ MAX direct loss
→ CURRENT = min(CURRENT_after_direct, MAX_after_loss)
```

- MAX loss 자체를 CURRENT에서 다시 차감하지 않는다.
- `FAIL_DOWNGRADE`와 `FAIL_CRITICAL_DAMAGE`는 기본 중첩하지 않는다.
- 별도 destroy roll을 두지 않는다.

재검사:
- 한 실패의 주 손실 축이 읽히며 예상하지 못한 삼중 벌점이 없다.

### Loop 5 — 플레이어가 MAX 손상 이후 항상 강화를 포기하는가

공격:
- 영구 흉터와 성공률/신규효과 페널티가 결합되면 손상된 애착 작품의 최적 행동이 항상 은퇴가 될 수 있다.

개선:
- 기존 획득 성능은 유지한다.
- 실패 누적 회복은 성공 기대를 일부 회복할 수 있다.
- MAX 상태가 지나치게 억제적이면 조정 우선순위를 `scar 발생률 → scar 손실량 → MAX 성공률 페널티 → 신규 효과 배율`로 둔다.

재검사:
- 손상 작품은 불리하지만 여전히 강화/인계/보존 중 선택 가능해야 한다.

## C. Better Alternative Search — 09 판정 방식

### A. 시도마다 독립 MAX scar roll
- 성공에도 구조 손상이 섞일 위험이 있고 인과가 약하다.
- `REJECT`.

### B. 실패 후 conditional scar roll
- 실패 안에서만 영구 흉터가 발생한다.
- failure family를 독립적으로 튜닝할 수 있다.
- `ADOPT`.

### C. N회 실패마다 확정 scar
- 예측 가능하지만 실패 횟수 파밍/최적화가 생길 수 있다.
- baseline `REJECT`.

## D. 승인된 09 테스트 Budget

```text
LEARN             scar|failure 0%      / MAX loss 0
BUILD_CONFIDENCE  scar|failure 0%      / MAX loss 0
FIRST_STOP_POINT  scar|failure 0~5%    / MAX loss 1~3
TENSION           scar|failure 8~12%   / MAX loss 2~5
HIGH_STAKES       scar|failure 12~20%  / MAX loss 4~10
MASTERY           scar|failure 15~25%  / MAX loss 6~15
```

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## E. CLEAN EXIT 경계

- 07~08 구조 검토 5회 완료.
- 09 Balance Budget 검토 5회 완료.
- 현재 P0/P1 구조 모순 없음.
- 정확 출시 수치는 `NOT_FINAL`.
- Human/Player validation이 없으므로 재미 PASS 선언 금지.
- 제품 구현은 새 `기획 완료` 선언 전 `BLOCKED`.
