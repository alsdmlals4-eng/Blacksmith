# [현재 승인] Blacksmith 실패 결과군 비율 Budget

- Parent: `BS-ENHANCE-20260820-02~09`, `BS-ENHANCE-20260820-12`
- Decision: `BS-ENHANCE-20260820-13`
- 사용자 승인: `2026-08-20 KST / 권장 B안 진행 승인`
- 상태: `USER_APPROVED / USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 결정 목적

강화가 실패했을 때 선택되는 결과군을 경험 밴드별로 정한다.

```text
FAIL_HOLD
FAIL_DOWNGRADE
FAIL_DAMAGE
FAIL_CRITICAL_DAMAGE
```

이 표는 성공 확률이 아니라 **실패가 이미 확정된 뒤의 조건부 비율**이다.

```text
failure_family_ratio = P(family | failure)

P(final family per attempt)
= P(failure on this attempt) × P(family | failure)
```

플레이어 UI는 조건부 비율을 그대로 노출하지 않고 현재 성공률을 반영한 최종 시도 기준 outcome 확률을 보여준다.

## 2. 승인 첫 테스트표 — B · 상태 변화 균형형

순서: `HOLD / DOWNGRADE / DAMAGE / CRITICAL`

| 경험 밴드 | HOLD | DOWNGRADE | DAMAGE | CRITICAL |
|---|---:|---:|---:|---:|
| `LEARN` | `100%` | `0%` | `0%` | `0%` |
| `BUILD_CONFIDENCE` | `90%` | `0%` | `10%` | `0%` |
| `FIRST_STOP_POINT` | `65%` | `10%` | `23%` | `2%` |
| `TENSION` | `45%` | `10%` | `35%` | `10%` |
| `HIGH_STAKES` | `30%` | `15%` | `39%` | `16%` |
| `MASTERY` | `20%` | `20%` | `40%` | `20%` |

상태:

```text
LEARN~HIGH_STAKES = USER_APPROVED_TEST_BUDGET
MASTERY = USER_APPROVED_LATE_GAME_TEST_BUDGET
NOT_FINAL_PRODUCT_BALANCE
```

MASTERY의 정확 CURRENT 일반/심각 손실량은 아직 별도 후속 튜닝 대상이다.

## 3. 결과군 불변식

### 모든 FAILURE
- 시도 비용/작업량은 현재 계약대로 소비한다.
- 같은 작품 UID의 실패 누적 회복 진전이 증가한다.
- family 결과 때문에 회복 진전이 사라지지 않는다.

### FAIL_HOLD
- 강화 단계 유지.
- CURRENT/MAX 유지.
- 실패 누적 회복만 증가.

### FAIL_DOWNGRADE
- 첫 테스트 최대 1단계 하락.
- 최근 확보 체크포인트 아래로 내려가지 않는다.
- CURRENT/MAX 손상과 기본 중첩하지 않는다.

### FAIL_DAMAGE
- 강화 단계 유지.
- 해당 밴드의 일반 CURRENT 손상 Budget을 적용한다.
- MAX는 감소하지 않는다.

### FAIL_CRITICAL_DAMAGE
- 강화 단계 유지가 기본이다.
- 해당 밴드의 심각 CURRENT 손상 Budget을 적용한다.
- MAX 구조 흉터를 1회 적용한다.
- 별도 destroy roll은 없다.
- 실제 CURRENT 또는 MAX가 0이 되었을 때만 `DESTROYED`다.

## 4. CRITICAL = MAX 구조 흉터 단일화

`BS-ENHANCE-20260820-09`의 `P(MAX scar | failure)` 범위를 13의 `P(CRITICAL | failure)`와 같은 축으로 사용한다.

```text
P(CRITICAL | failure)
= P(MAX scar | failure)
```

따라서 CRITICAL 뒤에 별도 MAX-scar 주사위를 다시 굴리지 않는다.

승인된 첫 값은 기존 범위 안에 있다.

```text
LEARN             0%
BUILD_CONFIDENCE  0%
FIRST_STOP_POINT  2%
TENSION           10%
HIGH_STAKES       16%
MASTERY           20%
```

기존 09 허용 범위:

```text
FIRST_STOP_POINT  0~5%
TENSION           8~12%
HIGH_STAKES       12~20%
MASTERY           15~25%
```

## 5. 최종 시도 확률 예시

`HIGH_STAKES`에서 현재 최종 성공률이 50%라면:

```text
SUCCESS   50.00%
HOLD      15.00%
DOWN       7.50%
DAMAGE    19.50%
CRITICAL   8.00%
```

`CRITICAL 16%`는 버튼을 누를 때마다 16%라는 뜻이 아니다. 실패가 50%일 때 최종 시도 기준 CRITICAL은 8%다.

`TENSION` family가 `45/10/35/10`이고 성공률이 60%라면:

```text
SUCCESS   60%
HOLD      18%
DOWN       4%
DAMAGE    14%
CRITICAL   4%
```

회복 누적으로 성공률이 75%가 되면 최종 CRITICAL은 `2.5%`로 자연스럽게 감소한다.

## 6. 실패 누적 회복과 severity 분리

첫 Vertical Slice에서는:

```text
recovery_progress -> P(success)만 변경
failure_family_table -> 같은 경험 밴드 안에서 고정
```

금지:
- 회복이 높아질수록 숨은 실패 severity를 올리는 보정.
- 회복이 쌓였다는 이유로 DOWNGRADE/DAMAGE/CRITICAL 비율을 몰래 높이기.

의도는 `실패했지만 다음 성공 기대는 좋아졌다`이지 `다음 실패가 더 위험해졌다`가 아니다.

## 7. resolution 순서

```text
1. final success expectation 계산
2. SUCCESS / FAILURE 판정
3. SUCCESS면 성공 처리
4. FAILURE면 현재 경험 밴드 table에서 family 정확히 1개 선택
5. 모든 FAILURE에 item-UID recovery progress 증가
6. HOLD: 추가 상태 손실 없음
7. DOWNGRADE: 최대 1단계, checkpoint floor, CURRENT/MAX 유지
8. DAMAGE: ordinary CURRENT loss, MAX 유지
9. CRITICAL: severe CURRENT loss + MAX loss 1회
10. CURRENT = min(CURRENT_after_direct_loss, MAX_after_scar)
11. CURRENT == 0 or MAX == 0이면 DESTROYED
12. outcome + recovery를 UID history에 기록
```

금지:
- DOWNGRADE + DAMAGE 기본 중첩.
- DAMAGE + CRITICAL 이중 선택.
- CRITICAL 뒤 별도 destroy roll.
- CRITICAL 뒤 별도 MAX-scar roll.

## 8. 대안 비교 기록

### A · 회복 우선형
- TENSION/HIGH에서도 HOLD가 과도해 위험이 진행바처럼 느껴질 가능성.
- `REJECT_AS_BASELINE / LOWER_CONSEQUENCE_BOUND`.

### B · 상태 변화 균형형 — 채택
- 초반 HOLD 중심.
- FIRST_STOP부터 실제 상태 변화가 시작.
- TENSION 실패의 55%, HIGH 실패의 70%가 HOLD 이외 상태 변화.
- CRITICAL은 기존 MAX 흉터 범위 중앙권.
- `ADOPT`.

### C · 결과 압박형
- 12의 골드+재료 필수 수리와 결합할 때 maintenance loop가 강화를 덮을 위험.
- `REJECT_AS_BASELINE / UPPER_CONSEQUENCE_BOUND`.

## 9. 5회 전체 적대 검토

### Loop 1 — 첫 10분 강화 회피
- LEARN 실패 HOLD 100%.
- BUILD 실패 중 DAMAGE 10%, DOWN/CRITICAL 0%.
- 판정: `PASS`.

### Loop 2 — TENSION/HIGH가 가짜 위험인지
- TENSION 실패 55%, HIGH 실패 70%가 실제 상태 변화.
- DAMAGE가 주 결과이고 CRITICAL은 제한.
- 판정: `PASS_WITH_PLAYTEST`.

### Loop 3 — 수리 루프가 메인을 덮는지
- BUILD 손상은 낮게 유지.
- TENSION/HIGH에서만 손상 빈도 상승.
- 한 번의 REPAIR_JOB으로 CURRENT를 MAX까지 복구.
- 첫 10분 수리 행동이 강화 의사결정 행동의 25% 이상이면 DAMAGE share 또는 CURRENT loss를 먼저 낮춘다.
- 판정: `PASS_WITH_MONITORING`.

### Loop 4 — DOWNGRADE 재노동
- FIRST/TENSION 10%, HIGH 15% of failures.
- 한 번 최대 1단계, checkpoint floor 유지, durability와 기본 비중첩.
- 판정: `PASS_WITH_PLAYTEST`.

### Loop 5 — MAX scar/UI 중복 확률
- CRITICAL과 MAX scar를 단일화.
- UI는 final per-attempt outcome 합계 100%를 보여준다.
- 판정: `PASS`.

## 10. 외부 원리 적용

- **Black Desert · ADAPT:** 실패 결과에 내구도 감소·단계 하락·파괴가 존재하고 위험을 사전에 보여주는 원리.
- **Lost Ark · ADAPT:** 실패 후 성공 기대를 보완하는 progression 완화 원리.
- **MapleStory Star Force · ADAPT:** 초반 손실 제한, 후반 위험 개방, 확보 구간 보호 원리.

외부 게임의 실제 확률·재화량은 복사하지 않는다.

## 11. 재검토 조건

- 첫 위험 실패 후 강화 회피가 급증.
- BUILD에서 수리가 의미 있게 반복됨.
- TENSION 실패가 대부분 `아무 일 없음`으로 인식됨.
- HIGH에서 한 번 실패 후 새 작품 제작이 지배전략이 됨.
- 수리 행동이 강화 의사결정 행동의 25% 이상을 지속 점유.
- DOWNGRADE 복구가 강화 시간의 큰 비율을 차지.
- 플레이어가 조건부 CRITICAL과 최종 시도 CRITICAL을 혼동.
- 회복 진전에 따라 숨은 severity가 변경되는 구현이 제안됨.

## 12. 증거 경계

- 기획 구조: `USER_APPROVED`.
- 비율표: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- Human/Player validation: `NOT_RUN`.
- Runtime implementation: `BLOCKED`.
