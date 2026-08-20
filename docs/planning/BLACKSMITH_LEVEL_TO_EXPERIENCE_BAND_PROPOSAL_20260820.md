# [제안] Blacksmith +0~+100 레벨 → 경험 밴드 매핑

- Parent: `BS-CORE-20260820-01`, `BS-ENHANCE-20260820-05~13`, `BS-PROGRESSION-20260820-14`
- Proposed Decision: `BS-PROGRESSION-20260820-15`
- 상태: `PROPOSED_ONLY / USER_DECISION_REQUIRED`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 결정 목적

현재 확정된 상위 구조는 다음이다.

```text
+0~+9      = INVESTMENT_RECOVERY_ZONE
+10        = BREAK_EVEN_RECOVERY_POINT
+11~+100   = PROFITABLE_ENHANCEMENT_ZONE
+100       = MAX_ENHANCEMENT_LEVEL
```

또한 경험 밴드는 다음 역할을 가진다.

```text
LEARN
BUILD_CONFIDENCE
FIRST_STOP_POINT
TENSION
HIGH_STAKES
MASTERY
```

15는 `+0~+100`의 어느 강화 시도가 어느 경험 밴드의 실패비율·긴장도·피드백 규칙을 사용하는지 정한다.

이번 Decision은 **후속 체크포인트 전체 간격, 단계별 성공률, 단계별 가격/비용**까지 확정하지 않는다.

---

## 2. 중요한 의미 규칙 — 밴드는 `target_level`에 붙인다

플레이어가 현재 `+10`이고 `+11`을 시도한다면:

```text
current_level = +10
target_level  = +11
attempt_band  = band_for_target(+11)
```

이 규칙을 사용하는 이유:

- 강화 결과가 무엇을 노리고 있는지 기준이 명확하다.
- 강화 전 UI에서 다음 시도의 성공/실패 위험을 바로 계산할 수 있다.
- `+10`이라는 **확보된 상태**와 `+11을 노리는 위험 행동`을 분리할 수 있다.

`+0`은 제작 완료 기본 상태이며 강화 시도 밴드가 아니다.

---

## 3. 대안 A · +10 도달 자체를 FIRST_STOP으로 만드는 안

```text
TARGET +1~+2    LEARN
TARGET +3~+9    BUILD_CONFIDENCE
TARGET +10      FIRST_STOP_POINT
TARGET +11~+30  TENSION
TARGET +31~+60  HIGH_STAKES
TARGET +61~+100 MASTERY
```

### 장점

- +10 경제 이정표와 경험 밴드 이름이 숫자상 정확히 일치한다.
- 설명이 단순하다.

### 문제

- `+9 → +10` 시도에서 FIRST_STOP의 DAMAGE/CRITICAL 위험이 열릴 수 있다.
- 플레이어가 **아직 평균 본전도 회수하지 못한 상태에서 영구 MAX 흉터 위험**을 감수하게 된다.
- `+10 = 처음으로 안전하게 멈출 수 있는 회수선`이라는 14의 경제 의미가 약해진다.

판정:

```text
REJECT_AS_BASELINE
RISK_OPENS_ONE_STEP_TOO_EARLY
```

---

## 4. 대안 B · +10 확보 후 첫 수익 시도를 FIRST_STOP으로 만드는 안 — 권장

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

상태 의미:

```text
CURRENT +10
= FIRST_ECONOMIC_STOP_STATE
= 투자금 평균 회수 완료 상태

TARGET +11 ATTEMPT
= FIRST_STOP_POINT attempt band
= 본전을 지키고 멈출지, 수익을 위해 처음 위험을 열지 결정
```

### 장점

1. **경제와 감정 곡선이 일치한다.**
   - +10을 먼저 확보한다.
   - 그 다음 +11부터 실제 이익과 실제 위험이 정면 충돌한다.

2. **영구 구조 손상이 본전 회수 전에 열리지 않는다.**
   - BUILD_CONFIDENCE는 CRITICAL 0%.
   - FIRST_STOP(+11 target)부터 CRITICAL 2% of failures.

3. **첫 10분 DDD에 적합하다.**
   - 초반 성공 경험 → +10 회수선 → +11 첫 욕심이라는 명확한 드라마를 만들 수 있다.

4. **13 실패 family를 그대로 소비한다.**

```text
+1~+2    LEARN             100/0/0/0
+3~+10   BUILD              90/0/10/0
+11      FIRST_STOP         65/10/23/2
+12~+30  TENSION            45/10/35/10
+31~+60  HIGH               30/15/39/16
+61~100  MASTERY            20/20/40/20
```

order = `HOLD / DOWNGRADE / DAMAGE / CRITICAL`.

판정:

```text
RECOMMENDED_BASELINE
```

---

## 5. 대안 C · +10 이후 완충구간을 길게 두는 안

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11~+15   FIRST_STOP_POINT
TARGET +16~+40   TENSION
TARGET +41~+70   HIGH_STAKES
TARGET +71~+100  MASTERY
```

### 장점

- 본전 회수 직후 바로 위험이 크게 뛰지 않는다.
- 접근성이 가장 높다.

### 문제

- FIRST_STOP이라는 특별한 선택 순간이 5개 레벨에 걸쳐 반복되어 의미가 흐려진다.
- +11부터 수익 영역인데 +15까지 낮은 위험을 유지하면 `본전 이후 욕심`의 핵심 긴장이 늦게 열린다.
- +100 장기 사다리 중 TENSION/HIGH 진입이 지나치게 늦어질 수 있다.

판정:

```text
REJECT_AS_BASELINE
TOO_LONG_POST_BREAK_EVEN_GRACE
```

---

## 6. 권장 B의 상세 계약

### 6.1 +1~+2 · LEARN

목적:
- 강화 행동과 결과를 학습.
- 실패가 나더라도 작품 상태를 훼손하지 않음.

현재 family:

```text
HOLD 100
DOWN 0
DAMAGE 0
CRITICAL 0
```

성공 기대는 기존 권장 범위 `90~100%`에서 후속 수치화한다.

### 6.2 +3~+10 · BUILD_CONFIDENCE

목적:
- `강화하면 가치가 오른다`는 신뢰 형성.
- +10 본전 회수 지점까지 작품의 영구 구조 흉터를 만들지 않음.

현재 family:

```text
HOLD 90
DOWN 0
DAMAGE 10
CRITICAL 0
```

DAMAGE는 CURRENT만 손상하며 MAX 흉터는 없음.

`+10` 성공 후 즉시 다음을 보여준다.

```text
투자 회수선 도달
지금 판매/인계 시 평균 본전
다음 +11부터 기본 수익 가능
다음 시도부터 첫 영구 구조 위험 개방
```

### 6.3 +11 · FIRST_STOP_POINT

`+11` 한 단계만 특별 band로 둔다.

플레이어 질문:

> “이 작품은 이미 본전을 회수할 수 있다. 첫 이익을 위해 한 번 더 밀 것인가?”

family:

```text
HOLD 65
DOWN 10
DAMAGE 23
CRITICAL 2
```

`+10`을 첫 경제 체크포인트 floor로 채택할 경우, +11 시도의 DOWNGRADE가 +10 아래로 내려가려 하면 floor에서 막힌다.

따라서 플레이어-facing 최종 outcome은 checkpoint 제약을 반영해 다시 합산한다.

예:

```text
selected = DOWNGRADE
current = +10
floor = +10
result level = +10
```

이때 UI는 실제로 단계가 내려가지 않는다면 `단계 하락 10%`라고 거짓 표시하지 않는다. 최종 효과를 `유지/보호됨` 계열로 합쳐 표시한다.

### 6.4 +12~+30 · TENSION

목적:
- 강화가 Blacksmith의 메인이라는 감정적 증거.
- 수익을 더 키우는 선택과 실제 CURRENT 손상/하락을 충돌시킴.

family:

```text
HOLD 45
DOWN 10
DAMAGE 35
CRITICAL 10
```

### 6.5 +31~+60 · HIGH_STAKES

목적:
- 같은 작품 UID에 쌓인 가치와 더 큰 수익을 정면 충돌.

family:

```text
HOLD 30
DOWN 15
DAMAGE 39
CRITICAL 16
```

이 구간 진입 전에는 강화 UI에서 위험 상승을 명시적으로 보여준다.

### 6.6 +61~+100 · MASTERY

목적:
- 선택적 후기 장기 목표.
- +100은 기본 완주 필수가 아니라 최고 작품 목표.

family 첫 테스트:

```text
HOLD 20
DOWN 20
DAMAGE 40
CRITICAL 20
```

주의:
- `+61~+100`이 같은 성공률/비용/보상으로 40회 반복된다는 뜻이 아니다.
- 15는 **failure family/경험 역할의 큰 band**만 정한다.
- 밴드 내부 성공률·비용·보상 곡선과 중간 이정표는 후속 Decision에서 변화해야 한다.

---

## 7. +10 checkpoint floor — 권장 결합안

15의 B안과 함께 다음을 권장한다.

```text
+10 = FIRST_ECONOMIC_CHECKPOINT_FLOOR
```

의미:

- +10 도달 후 추가 강화를 시도해도 제한 DOWNGRADE 때문에 +10 아래로 내려가지 않는다.
- `본전 회수 완료`라는 경제적 확보감이 실제 시스템 floor와 일치한다.
- 추가 수익을 노리다 실패해도 이미 확보한 첫 경제 milestone 전체를 잃지 않는다.
- 손상/CURRENT/MAX 위험은 여전히 존재하므로 +11이 공짜 도전이 되지는 않는다.

중요:

**+10 이후 모든 10단위를 자동 checkpoint로 확정하지 않는다.**

```text
+20 ?
+30 ?
+40 ?
...
```

은 후속 `CHECKPOINT_CADENCE` Decision에서 별도 비교한다.

또한:

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

따라서 +30/+60은 B안의 경험 band 경계일 뿐, 자동 영구 floor가 아니다.

---

## 8. +100 종착 계약

```text
TARGET +100 = MASTERY
SUCCESS +100 => MAX_ENHANCEMENT_REACHED
NEXT NORMAL ENHANCEMENT = NONE
```

+100에서 기본 강화 버튼은 더 높은 숫자를 제안하지 않는다.

후속 UX는 다음 쪽으로 전환한다.

```text
보유
판매/인계
전시
Chronicle
최고 작품 표현
다음 작품 시작
```

정확한 +100 비수치 payoff는 후속 Decision이다.

---

## 9. 5회 전체 적대적 검토

### Loop 1 — 본전 전에 영구 위험을 여는가

공격:
- target +10을 FIRST_STOP으로 두면 +10 도달 전 CRITICAL/MAX 흉터가 발생할 수 있다.
- 평균 투자 회수선에 도달하기도 전에 영구 손실을 강제하면 `본전 회수` 의미가 약해진다.

방어:
- B는 target +3~+10을 BUILD로 유지해 CRITICAL 0%.
- +10 확보 후 target +11부터 FIRST_STOP을 연다.

판정:

```text
B PASS
A REJECT
```

### Loop 2 — +11이 checkpoint 때문에 너무 안전한가

공격:
- +10 floor가 있으면 +11 실패의 DOWNGRADE 10%는 실질 단계 하락이 되지 않는다.
- 첫 수익 도전이 거의 공짜처럼 느껴질 수 있다.

방어:
- FIRST_STOP 실패에는 DAMAGE 23%와 CRITICAL 2%가 여전히 존재한다.
- 시도 비용과 UID recovery 변화도 남는다.
- +12부터는 TENSION으로 진입해 실제 단계 하락/손상 비율이 강해진다.

재검사:
- +11의 DOWNGRADE가 floor에 막히면 UI는 실제 결과에 맞게 HOLD-like 결과로 합산한다.

판정:

```text
PASS_WITH_PLAYTEST
```

### Loop 3 — +11~+100이 90회 반복 노동이 되는가

공격:
- band만 나누고 레벨당 보상/비용이 비슷하면 최대 100이라는 숫자가 장기 클릭 노동이 된다.

방어:
- B는 11/12/31/61에 경험 역할 변화를 만든다.
- 15는 band만 책임지고, 다음 Decision에서 checkpoint cadence와 band 내부 보상/성공률/비용 곡선을 별도로 만든다.
- MASTERY는 선택적 후기이며 기본 완주 필수로 만들지 않는다.

판정:

```text
PASS_ONLY_WITH_FOLLOW_UP_CURVE
```

### Loop 4 — +31/+61 직전 최적화 메타가 생기는가

공격:
- band 경계에서 family ratio가 바뀌므로 +30/+60에서 무조건 팔거나 수리하는 정답이 생길 수 있다.

방어:
- 위험 변화는 숨기지 않고 다음 시도 카드에서 선공개한다.
- band 경계는 보상/수익 변화와 함께 조정해야 한다.
- `멈춤`이 합리적 선택이 되는 것 자체는 코어에 부합하지만 100% 지배전략이 되면 실패다.

재검토 신호:
- +30 또는 +60 판매/정지가 80%+로 수렴하면 다음 band 보상 또는 위험 jump를 조정한다.

판정:

```text
PASS_WITH_BALANCE_GATE
```

### Loop 5 — band boundary를 checkpoint로 오해하는가

공격:
- +30 TENSION→HIGH, +60 HIGH→MASTERY 경계가 자동 checkpoint처럼 구현될 수 있다.

방어:
- `BAND_BOUNDARY != CHECKPOINT_FLOOR`를 명시한다.
- 15가 승인해도 +10 외 후속 floor cadence는 미확정으로 남긴다.

판정:

```text
PASS
```

---

## 10. 외부 벤치마크 적용

### MapleStory Star Force — ADAPT

현재 공식 가이드는 낮은 스타포스 구간을 하락/파괴 없는 구간으로 두고, 높은 구간에서 파괴 위험을 연다. 최근 흔적 복구 개편도 고강화 파괴 후 획득 상태 보존/복구를 강화했다.

Blacksmith 적용:
- 초반 신뢰 형성 구간과 후반 위험 구간을 명확히 분리.
- +10 회수 이후 위험 상승을 명시.

비채택:
- 스타포스 단계 수/성공률/파괴율/메소 수치 복사.

공식 참고:
- https://maplestory.nexon.com/Guide/N23GameInformation/Articles/412
- https://maplestory.nexon.com/news/update/799

### Black Desert Enhancement — ADAPT

공식 가이드는 무기 +7 등 안전 강화 범위를 둔 뒤, 이후 실패 시 최대 내구도 감소·단계 하락·일부 파괴 위험이 열릴 수 있음을 명시한다.

Blacksmith 적용:
- 안전 학습/회수 구간과 실제 위험 구간 분리.
- 다음 시도의 실패 결과를 사전 공개.

비채택:
- +7 등 외부 숫자와 MMO식 장기 복구 노가다.

공식 참고:
- https://www.sa.playblackdesert.com/Pt-BR/Wiki?wikiNo=48

### Lost Ark — REFERENCE / AVOID

공식 업데이트들은 특정 성장 구간의 성공률·재료·골드 요구량을 반복 조정해 progression 부담을 줄여 왔다.

Blacksmith 적용:
- +100 장기 목표라도 모든 레벨을 동일 실패/재료 부담으로 반복시키지 않는다.

비채택:
- 긴 재료 파밍 자체를 핵심 플레이 시간으로 사용.

공식 참고:
- https://www.playlostark.com/en-us/news/articles/may-2023-release-notes

---

## 11. 권장안 요약

```text
B · +10 확보 후 위험 전환형

TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY

+10 = FIRST_ECONOMIC_STOP_STATE
+10 = recommended FIRST_ECONOMIC_CHECKPOINT_FLOOR
+100 = MAX_ENHANCEMENT_LEVEL

BAND_BOUNDARY != CHECKPOINT_FLOOR
```

상태:

```text
PROPOSED_ONLY / USER_DECISION_REQUIRED
```

---

## 12. 승인 후 다음 Decision

15 승인 후 바로 확정해야 하는 것은:

```text
BS-PROGRESSION-20260820-16
CHECKPOINT_CADENCE
```

비교 대상 예:
- 소수 대형 checkpoint.
- 10단위 checkpoint.
- 비대칭 checkpoint.

그 뒤에야 `+0~+100` 단계별 성공률·강화 비용·판매가·누적 기대원가를 계산한다.

제품 code/data/runtime은 새 `기획 완료` 전 변경하지 않는다.
