# [현재 승인] Blacksmith Checkpoint Cadence

- Parent: `BS-ENHANCE-20260820-05`, `BS-ENHANCE-20260820-13`, `BS-PROGRESSION-20260820-14~15`
- Decision: `BS-PROGRESSION-20260820-16`
- 사용자 승인: `2026-08-20 KST / 권장안 진행 승인`
- 상태: `USER_APPROVED / STRUCTURAL_CANON / NUMERIC_CURVE_NOT_FINAL`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 승인 Checkpoint

```text
CHECKPOINT_FLOORS = [10, 30, 60, 90]
MAX_ENHANCEMENT_LEVEL = 100
```

역할:

```text
+10 = FIRST_ECONOMIC_CHECKPOINT_FLOOR
+30 = TENSION_COMPLETION_FLOOR
+60 = HIGH_STAKES_COMPLETION_FLOOR
+90 = FINAL_MASTERY_PUSH_FLOOR
+100 = MAX_ENHANCEMENT_TERMINAL
```

`+100`은 종착점이며 별도 DOWNGRADE floor로서의 실익보다 최대 강화 완료 상태가 우선한다.

## 2. Checkpoint 의미

Checkpoint는 같은 작품 UID에 귀속되는 영구 단계 floor다.

```text
highest_secured_floor
= highest reached checkpoint level
```

DOWNGRADE가 선택되면:

```text
raw_result = current_level - 1
resolved_level = max(raw_result, highest_secured_floor)
```

예:

```text
current +41 / floor +30 / DOWNGRADE -> +40
current +31 / floor +30 / DOWNGRADE -> +30
current +30 / floor +30 / DOWNGRADE -> +30 (protected)
```

## 3. Checkpoint가 보호하지 않는 것

Checkpoint는 오직 단계 하락의 하한만 보호한다.

다음은 변경하지 않는다.

```text
CURRENT durability
MAX durability
MAX scar history
failure recovery progress
attempt cost
repair cost
item UID/history
existing affix/artistry/chronicle
```

Checkpoint 도달로 CURRENT/MAX를 회복하지 않는다.

Checkpoint 도달로 실패 누적 회복을 초기화하지 않는다.

Checkpoint 도달로 성공률 보너스를 자동 지급하지 않는다.

## 4. 경험 밴드와 Checkpoint는 별개

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

15의 경험 밴드:

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

Checkpoint:

```text
+10 / +30 / +60 / +90
```

- +30과 +60은 위험 구간 완주 의미가 있어 checkpoint이기도 하다.
- +90은 밴드 경계가 아니며 마지막 +91~+100 러시를 분리하기 위한 의도적 floor다.
- 밴드 경계라는 이유만으로 자동 checkpoint를 생성하지 않는다.

## 5. 플레이어-facing DOWNGRADE 표시

Checkpoint가 실제 하락을 막는 상황에서 조건부 family의 내부 선택을 그대로 `단계 하락`이라고 표시하지 않는다.

예:

```text
current +30
floor +30
family = DOWNGRADE
resolved level = +30
```

플레이어 UI는 최종 결과 기준으로 `유지 / 체크포인트 보호` 계열에 합산한다.

사전 정보 공개 계약은 항상 최종 per-attempt outcome 기준을 사용한다.

## 6. 왜 매 10단위가 아닌가

거부안:

```text
10 / 20 / 30 / 40 / 50 / 60 / 70 / 80 / 90
```

문제:
- DOWNGRADE가 거의 장식화된다.
- 플레이어 질문이 `한 번 더 밀까?`보다 `다음 저장점까지 몇 단계 남았나?`로 바뀐다.
- 고강화의 장기 위험 구간이 너무 짧게 잘린다.

## 7. 왜 +10/+30/+60만이 아닌가

거부안:

```text
10 / 30 / 60
```

문제:
- +61~+100 MASTERY 전체 40단계가 하나의 rollback 구간이 된다.
- 후기 반복 복구 노동이 과도하게 길어질 수 있다.
- +100 도전 직전 별도의 마지막 확보 상태가 없다.

따라서 +90을 마지막 staging floor로 추가한다.

## 8. 왜 +80/+90 둘 다 두지 않는가

거부안:

```text
10 / 30 / 60 / 80 / 90
```

문제:
- MASTERY 후반에 floor가 다시 과밀해진다.
- +80~+100의 고위험 최종 구간이 두 번 잘려 긴장이 약해질 가능성이 높다.

첫 기준은 +90 하나만 사용한다.

## 9. 5회 전체 적대 검토 결론

### Loop 1 — Checkpoint 과다
매 10강 floor는 DOWNGRADE 의미를 약화한다. `10/30/60/90`은 통과.

### Loop 2 — Checkpoint 부족
`10/30/60`은 MASTERY 40단계가 과도하게 길다. +90 staging floor를 추가해 통과.

### Loop 3 — Floor 직후 공짜 도전
Checkpoint가 막는 것은 DOWNGRADE뿐이다. DAMAGE/CRITICAL·시도비·수리비는 남으므로 공짜 도전이 아니다. 플레이테스트 필요.

### Loop 4 — Band와 floor 혼동
+90을 비밴드 checkpoint로 둬 자동 연동 규칙을 명시적으로 부정한다. 통과.

### Loop 5 — 경제 차익
Checkpoint 자체에 별도 판매가 프리미엄을 붙이지 않는다. rollback 감소가 기대원가에 미치는 효과만 17 경제 계산에 반영한다. 통과.

## 10. 재검토 조건

다음이면 cadence를 재검토한다.

- DOWNGRADE가 체감상 의미 없는 결과가 된다.
- 플레이어가 checkpoint 직후 시도를 사실상 무위험으로 인식한다.
- +31~+60 또는 +61~+90에서 단계 복구가 강화 플레이시간을 과도하게 차지한다.
- +91~+100이 실패 회복/수리까지 고려해도 지나치게 긴 반복 노동이 된다.
- 플레이어가 band boundary와 checkpoint를 같은 규칙으로 오해한다.
- checkpoint 직전 판매/수리 타이밍이 지배전략이 된다.

## 11. 다음 계산 입력

17의 `+0~+100 성공률 / 강화비 / 판매가 / 누적 기대원가` 계산은 다음 floor를 직접 사용한다.

```text
[10, 30, 60, 90]
```

- DOWNGRADE는 최대 1단계.
- 최근 floor 아래로 내려가지 않는다.
- DAMAGE/CRITICAL은 별도 CURRENT/MAX 계약을 따른다.
- 제품 code/data/runtime은 새 `기획 완료` 전 변경하지 않는다.
