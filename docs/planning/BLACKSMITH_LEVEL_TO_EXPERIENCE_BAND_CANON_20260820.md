# [현재 승인] Blacksmith +0~+100 레벨 → 경험 밴드 매핑

- Parent: `BS-CORE-20260820-01`, `BS-ENHANCE-20260820-05~13`, `BS-PROGRESSION-20260820-14`
- Decision: `BS-PROGRESSION-20260820-15`
- 사용자 승인: `2026-08-20 KST / 권장 B안 진행 승인`
- 상태: `USER_APPROVED / STRUCTURAL_CANON / NUMERIC_CURVE_NOT_FINAL`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 상위 진행 계약

```text
+0~+9      = INVESTMENT_RECOVERY_ZONE
+10        = BREAK_EVEN_RECOVERY_POINT
+11~+100   = PROFITABLE_ENHANCEMENT_ZONE
+100       = MAX_ENHANCEMENT_LEVEL
```

경험 밴드:

```text
LEARN
BUILD_CONFIDENCE
FIRST_STOP_POINT
TENSION
HIGH_STAKES
MASTERY
```

15는 강화 시도의 **목표 단계(target level)** 를 위 경험 밴드에 연결한다.

## 2. 밴드는 target level 기준

```text
current_level = +10
target_level  = +11
attempt_band  = band_for_target(+11)
```

- `+0`은 제작 완료 기본 상태이며 강화 시도 밴드가 아니다.
- 현재 상태와 다음 위험 행동을 분리한다.
- 강화 전 UI는 target level의 밴드로 최종 성공/실패 outcome을 계산한다.

## 3. 승인 레벨 → 경험 밴드 매핑

```text
TARGET +1~+2     = LEARN
TARGET +3~+10    = BUILD_CONFIDENCE
TARGET +11       = FIRST_STOP_POINT
TARGET +12~+30   = TENSION
TARGET +31~+60   = HIGH_STAKES
TARGET +61~+100  = MASTERY
```

이 매핑은 구조 Canon이다. 다만 밴드 내부의 정확 성공률·비용·판매가·CURRENT 손실량은 후속 Balance Decision이다.

## 4. +1~+2 · LEARN

목적:
- 강화 입력→결과 규칙 학습.
- 첫 강화부터 작품 손상 공포를 만들지 않는다.

13 failure family:

```text
HOLD 100
DOWNGRADE 0
DAMAGE 0
CRITICAL 0
```

정확 성공률은 기존 `90~100%` 권장 범위에서 후속 결정한다.

## 5. +3~+10 · BUILD_CONFIDENCE

목적:
- 강화가 작품 가치와 다음 목표를 올린다는 신뢰를 만든다.
- 첫 경제 회수선 +10까지 영구 MAX 흉터를 열지 않는다.

13 failure family:

```text
HOLD 90
DOWNGRADE 0
DAMAGE 10
CRITICAL 0
```

- DAMAGE는 CURRENT만 손상한다.
- +10 도달 전 MAX 구조 흉터는 없다.

`+10` 성공 후 UI는 다음을 명확히 보여준다.

```text
투자 회수선 도달
기본 공개시장 기준 평균 본전
다음 +11부터 기본 기대수익 가능
다음 시도부터 첫 영구 구조 위험 개방
```

## 6. +11 · FIRST_STOP_POINT

`+11` 시도 한 단계만 FIRST_STOP_POINT로 둔다.

```text
CURRENT +10
= FIRST_ECONOMIC_STOP_STATE

TARGET +11
= FIRST_STOP_POINT ATTEMPT
```

플레이어 질문:

> 이 작품은 이미 평균 본전을 회수할 수 있다. 첫 이익을 위해 한 번 더 밀 것인가?

13 failure family:

```text
HOLD 65
DOWNGRADE 10
DAMAGE 23
CRITICAL 2
```

+11부터 처음으로 MAX 구조 흉터가 가능하다.

## 7. +12~+30 · TENSION

목적:
- 본전 이후 수익 확대와 실제 손실 위험을 충돌시킨다.
- `수리 / 계속 / 멈춤` 질문이 반복적으로 생기는 본격 강화 구간이다.

13 failure family:

```text
HOLD 45
DOWNGRADE 10
DAMAGE 35
CRITICAL 10
```

## 8. +31~+60 · HIGH_STAKES

목적:
- 같은 UID에 누적된 높은 작품 가치와 더 큰 수익 욕심을 충돌시킨다.

13 failure family:

```text
HOLD 30
DOWNGRADE 15
DAMAGE 39
CRITICAL 16
```

HIGH_STAKES 진입 전 위험 상승을 강화 UI에서 명시한다.

## 9. +61~+100 · MASTERY

목적:
- 선택적 후기 장기 목표.
- +100 최고 작품을 노리는 고숙련 영역.

13 late-game family test budget:

```text
HOLD 20
DOWNGRADE 20
DAMAGE 40
CRITICAL 20
```

주의:
- +61~+100이 동일 확률·비용·보상으로 40회 반복된다는 의미가 아니다.
- 15는 큰 경험 역할만 정한다.
- 밴드 내부 성공률·비용·보상·checkpoint cadence는 별도 후속으로 변화시킨다.

## 10. +10 첫 경제 checkpoint floor

15와 함께 다음을 승인한다.

```text
+10 = FIRST_ECONOMIC_CHECKPOINT_FLOOR
```

- +10 도달 후 제한 DOWNGRADE 때문에 +10 아래로 내려가지 않는다.
- 본전 회수라는 경제 확보감이 실제 시스템 floor와 일치한다.
- +11 이후 DAMAGE/CRITICAL/CURRENT/MAX 위험은 그대로 존재하므로 공짜 도전이 아니다.
- 강화 시도 비용과 실패 recovery 변화도 그대로 발생한다.

### +11에서 DOWNGRADE가 뽑힌 경우

```text
current = +10
floor = +10
selected family = DOWNGRADE
result level = +10
```

실제 단계 하락이 없다면 플레이어 UI는 이를 `단계 하락`이라고 거짓 표시하지 않고 checkpoint 보호를 반영한 최종 outcome으로 재분류한다.

## 11. 밴드 경계와 checkpoint는 별개

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

따라서:
- +10 = 승인된 첫 경제 checkpoint floor.
- +30 = TENSION/HIGH 경계일 뿐 자동 checkpoint 아님.
- +60 = HIGH/MASTERY 경계일 뿐 자동 checkpoint 아님.
- +20/+30/+40/+50/+60/+70/+80/+90의 checkpoint 여부는 `BS-PROGRESSION-20260820-16`에서 별도 결정한다.

## 12. +100 종착 계약

```text
TARGET +100 = MASTERY
SUCCESS +100 => MAX_ENHANCEMENT_REACHED
NEXT_NORMAL_ENHANCEMENT = NONE
```

+100 이후 기본 UX는 더 높은 숫자가 아니라 다음으로 전환한다.

```text
보유
판매/인계
전시
Chronicle
최고 작품 표현
다음 작품 시작
```

## 13. 5회 전체 적대 검토 결론

### Loop 1 · 본전 전에 영구 위험이 열리는가
- +9→+10을 FIRST_STOP으로 두면 본전 회수 전 CRITICAL이 열릴 수 있다.
- +3~+10을 BUILD로 유지해 CRITICAL 0%로 차단.
- 판정: `PASS`.

### Loop 2 · +11이 +10 floor 때문에 공짜인가
- DOWNGRADE는 floor로 막힐 수 있으나 DAMAGE 23%, CRITICAL 2%, 시도비가 남는다.
- 판정: `PASS_WITH_PLAYTEST`.

### Loop 3 · TENSION이 너무 길어지는가
- +12~+30은 19개 target이지만 내부 성공률·비용·보상은 후속에서 단조 반복을 금지한다.
- 판정: `PASS_WITH_INTERNAL_CURVE_REQUIRED`.

### Loop 4 · HIGH/MASTERY가 반복 grind가 되는가
- 경험 밴드는 큰 역할 구분일 뿐이며 내부 checkpoint·비용·보상 곡선이 별도 필요하다.
- +100을 필수 완주로 취급하지 않는다.
- 판정: `PASS_WITH_LATE_GAME_DESIGN_REQUIRED`.

### Loop 5 · 경제/밴드/checkpoint 개념이 섞이는가
- +10만 현재 경제 회수선 + checkpoint floor로 결합한다.
- 다른 band boundary를 자동 checkpoint로 취급하지 않는다.
- 판정: `PASS`.

## 14. 재검토 조건

다음이면 15를 재검토한다.

- +10 도달 전 강화 회피가 높아짐.
- +11 첫 수익 도전이 checkpoint 보호 때문에 위험하지 않게 느껴짐.
- +12~+30이 같은 경험의 반복으로 읽힘.
- +31~+60에서 새 작품 제작이 항상 지배전략이 됨.
- +61~+100이 콘텐츠 분량 늘리기용 저확률 grind가 됨.
- +10 checkpoint가 이후 checkpoint 설계를 과도하게 규칙화함.
- +100이 사실상 필수 progression으로 변함.

## 15. 다음 Decision

`BS-PROGRESSION-20260820-16`에서 후속 checkpoint cadence를 결정한다.

최소 비교 대상:

```text
A. 10단위 균등 checkpoint
B. 점점 넓어지는 sparse checkpoint
C. 경제/위험 전환점 기반 비균등 checkpoint
```

16 승인 뒤 +0~+100 단계별 성공률·강화 비용·판매가·누적 기대원가 곡선을 설계한다.

제품 code/data/runtime은 새 `기획 완료` 전 변경하지 않는다.
