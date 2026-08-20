# [제안] Blacksmith +10 이후 Checkpoint Cadence

- Parent: `BS-ENHANCE-20260820-05`, `BS-ENHANCE-20260820-13`, `BS-PROGRESSION-20260820-14~15`
- Proposed Decision: `BS-PROGRESSION-20260820-16`
- 상태: `PROPOSED_ONLY / USER_DECISION_REQUIRED`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 결정 목적

15에서 다음이 승인됐다.

```text
+10 = FIRST_ECONOMIC_CHECKPOINT_FLOOR

TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

16은 **+10 이후 어떤 강화 단계가 영구 DOWNGRADE floor가 되는지** 결정한다.

Checkpoint의 목적은 강화 실패를 없애는 것이 아니다.

```text
checkpoint
= 반복 단계복구 노동의 상한
!= DAMAGE/CRITICAL 제거
!= 성공률 보너스
!= 수리
!= 시장가 보너스
```

## 2. Checkpoint 공통 불변식

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
current +41
highest floor +30
DOWNGRADE -> +40

current +31
highest floor +30
DOWNGRADE -> +30

current +30
highest floor +30
DOWNGRADE -> +30 (checkpoint protected)
```

Checkpoint가 막는 것은 **단계 하락만**이다.

Checkpoint가 변경하지 않는 것:

```text
CURRENT durability
MAX durability
MAX scar history
failure recovery progress
attempt cost
repair cost formula
item UID/history
existing affix/artistry/chronicle
```

Checkpoint 성공 자체로 CURRENT/MAX를 회복하지 않는다.

## 3. Checkpoint에 막힌 DOWNGRADE의 표시

내부 family 선택 기록은 보존할 수 있다.

```text
selected_family = FAIL_DOWNGRADE
resolved_result = CHECKPOINT_PROTECTED_HOLD
```

플레이어 UI는 실제 결과를 보여준다.

```text
단계 유지 · 체크포인트 보호
```

실제 단계가 내려가지 않는데 `단계 하락 N%`라고 표시하지 않는다.

Checkpoint에 막힌 DOWNGRADE를 DAMAGE로 몰래 바꾸지 않는다. 결과 severity를 숨게 보정하지 않는다.

## 4. 대안 A · 10단위 균등형

```text
CHECKPOINT_FLOORS
= +10 / +20 / +30 / +40 / +50 / +60 / +70 / +80 / +90
```

장점:
- 가장 직관적이다.
- UI 설명과 기억이 쉽다.
- 최대 floor 간격이 10단계라 단계 복구 노동이 작다.

문제:
- 100단계 중 checkpoint가 9개로 지나치게 많다.
- `다음 10단위 저장점까지`가 `멈춤 vs 한 번 더`보다 강한 메타 목표가 될 수 있다.
- DOWNGRADE가 floor 근처에서 반복적으로 무력화되어 13의 실패 family 중 하나가 장식이 될 위험이 있다.
- 과거 +10/+20/+30... 관성에 다시 종속된다.

판정:

```text
REJECT_AS_BASELINE
OVERPROTECTED / TOO_REGULAR
```

## 5. 대안 B · 최소 보호형

```text
CHECKPOINT_FLOORS
= +10 / +30 / +60

+100 = terminal max, not rollback floor
```

장점:
- checkpoint가 드물어 강화 긴장감이 강하다.
- TENSION/HIGH의 완료 지점만 크게 확보한다.
- 구조가 단순하다.

문제:
- +61~+100 MASTERY가 하나의 40단계 긴 rollback 구간이 된다.
- MASTERY는 실패 중 DOWNGRADE 20%의 late-game test budget이라 반복 단계복구 피로가 크게 누적될 수 있다.
- 플레이어가 +60에서 판매/중단하고 +100 목표 자체를 회피하는 지배전략이 될 위험이 있다.

판정:

```text
REJECT_AS_BASELINE
UNDERPROTECTED_LATE_GAME
```

## 6. 대안 C · 위험막 전환 + 최종 러시형 — 권장

```text
CHECKPOINT_FLOORS
= +10 / +30 / +60 / +90

+100 = terminal max
```

### +10

```text
FIRST_ECONOMIC_CHECKPOINT_FLOOR
```

- 14~15에서 이미 승인.
- 평균 본전 회수 상태를 보존한다.

### +30

- TENSION의 마지막 성공 단계.
- +31부터 HIGH_STAKES가 열린다.
- `수익을 키우며 TENSION을 통과했다`는 첫 장기 위험막 완료 지점.

### +60

- HIGH_STAKES의 마지막 성공 단계.
- +61부터 MASTERY가 열린다.
- 높은 손상/CRITICAL 위험을 통과한 작품의 진행을 확보한다.

### +90

- band boundary가 아니다.
- MASTERY 40단계를 하나의 긴 구간으로 두지 않고 마지막 +91~+100을 **FINAL PUSH**로 분리한다.
- +90을 포함함으로써 `band boundary = checkpoint` 자동 규칙이 아님을 명확히 한다.

### +100

- 최대 강화 성공 상태.
- 다음 정상 강화 시도가 없으므로 별도 rollback floor로서의 의미가 없다.

장점:
- checkpoint는 총 4개로 제한된다.
- +10 경제 milestone과 +30/+60 위험막 완료를 일치시킨다.
- +90은 MASTERY 후반 재노동을 제한하면서 최종 10단계 긴장을 남긴다.
- DAMAGE/CRITICAL/MAX scar는 모든 위험 구간에서 그대로 남아 checkpoint가 강화 리스크를 지우지 않는다.

판정:

```text
RECOMMENDED_BASELINE
```

## 7. 탐색 대안 D · 후기 보호 강화형

```text
CHECKPOINT_FLOORS
= +10 / +30 / +60 / +80 / +90
```

장점:
- MASTERY 복구 피로를 더 강하게 억제한다.

문제:
- +61~+100에 floor가 +60/+80/+90으로 촘촘해져 MASTERY가 가장 위험한 구간이라는 의미를 약화한다.
- +90 FINAL PUSH의 특별성이 감소한다.
- 이후 성공률 recovery까지 결합하면 단계 손실 압력이 지나치게 작아질 수 있다.

판정:

```text
REJECT_AS_BASELINE
USE_AS_SAFETY_FALLBACK_IF_MASTERY_REWORK_TOO_HIGH
```

## 8. 권장 C의 구간 구조

```text
+0~+10
first secured floor = +10

+11~+30
floor = +10
reach +30 -> floor becomes +30

+31~+60
floor = +30
reach +60 -> floor becomes +60

+61~+90
floor = +60
reach +90 -> floor becomes +90

+91~+100
floor = +90
reach +100 -> max enhancement terminal
```

중요:
- 한 번의 DOWNGRADE는 계속 최대 1단계다.
- checkpoint는 여러 단계를 즉시 +floor까지 떨어뜨리는 시스템이 아니다.
- floor는 연속 실패에서 **더 아래로 누적 후퇴하는 경계**만 제한한다.

## 9. 13 failure family와 결합

```text
TENSION      DOWNGRADE 10% of failures
HIGH_STAKES  DOWNGRADE 15% of failures
MASTERY      DOWNGRADE 20% of failures
```

Checkpoint가 있는 이유는 이 DOWNGRADE를 삭제하기 위함이 아니라 장기 bad-luck/recovery 과정에서 무한 재노동으로 변하는 것을 막기 위함이다.

DAMAGE/CRITICAL share는 checkpoint와 무관하게 유지한다.

```text
TENSION      DAMAGE 35 / CRITICAL 10
HIGH         DAMAGE 39 / CRITICAL 16
MASTERY      DAMAGE 40 / CRITICAL 20
```

따라서 floor 직후 한 번 더 누르는 선택도 CURRENT/MAX 손상·수리비·시도비 위험을 갖는다.

## 10. Checkpoint와 수리 경제 분리

Checkpoint 개수/도달 자체를 수리비의 새 배율로 사용하지 않는다.

금지:

```text
repair_R × checkpoint_count
repair_R × checkpoint_level_bonus
```

11의 `MATERIAL_STRUCTURE_MULTIPLIER / SECURED_BAND_MULTIPLIER` 계약은 별도 축으로 유지한다.

Checkpoint에 도달했다고 CURRENT/MAX가 회복되거나 수리비가 자동 할인되지 않는다.

## 11. Checkpoint와 판매가 분리

Checkpoint 도달 자체에 별도 판매가 프리미엄을 중복 부여하지 않는다.

```text
sale_value
!= base_level_value × checkpoint_bonus
```

다음 +0~+100 경제곡선은 checkpoint가 평균 누적 기대원가에 미치는 영향을 **시뮬레이션 입력**으로 반영한다.

즉:
- floor가 rollback 기대비용을 낮추면 누적 기대원가가 바뀐다.
- 그 결과를 판매가/기대수익 곡선에서 검증한다.
- 별도의 `checkpoint premium`으로 다시 과금하지 않는다.

## 12. 외부 Benchmark 적용

### Diablo IV Masterworking — ADAPT

Blizzard의 최근 아이템 여정 개편은 Masterworking을 최대 Quality까지 직접 진행하고 마지막 Capstone 보너스를 분리하며, 최종 보너스 재굴림이 진행 Quality 자체를 리셋하지 않도록 설계했다.

Blacksmith 적용:
- 후기 progression에서 이미 달성한 큰 진행을 반복 전체 리셋하지 않는 원리.
- +90 이후 마지막 +100을 별도 final push처럼 읽히게 하는 원리.

비채택:
- Diablo의 Quality 수치·재료비·Capstone 확률 복사.

공식 참고:
- https://news.blizzard.com/en-us/article/24243142/sanctuary-ignites-with-itemization-systems-changes
- https://news.blizzard.com/en-us/article/24244466/diablo-iv-patch-notes-2-5

### Black Desert Enhancement — ADAPT / AVOID

공식 가이드는 안전 강화 범위 이후 실패가 MAX 내구도 감소·단계 하락·일부 파괴로 무거워질 수 있고 높은 강화 시도일수록 MAX 내구도 감소가 커질 수 있음을 안내한다.

Blacksmith 적용:
- 위험이 커지는 구간을 한 종류의 보호 규칙으로 모두 평탄화하지 않는다.
- checkpoint가 있어도 CURRENT/MAX 손상은 계속 남긴다.

비채택:
- 동일 장비/Memory Fragment 반복 복구 grind.
- 외부 safe-level 숫자 복사.

공식 참고:
- https://www.sa.playblackdesert.com/Pt-BR/Wiki?wikiNo=48
- https://blackdesert.pearlabyss.com/asia/en-US/Game/Wiki?_masterWikiNo=14

### MapleStory Star Force — REFERENCE / AVOID OVERPROTECTION

최근 라이브 구조는 단계 하락/파괴로 인한 반복 재진행 부담을 크게 완화하고, 파괴 복원에서도 과거 진행 보존을 강화하는 방향을 보여준다.

Blacksmith 적용:
- 장기 강화에서 완전 재노동을 제한해야 한다는 원리.

비채택:
- DOWNGRADE 자체를 사실상 제거하는 수준의 보호.
- 외부 Star Force milestone 숫자 복사.

## 13. 5회 전체 적대적 검토

### Loop 1 · checkpoint가 너무 많아 DOWNGRADE가 장식이 되는가

공격:
- 매 10단위 floor는 9개의 영구 저장점을 만든다.
- 강화 목표가 `다음 checkpoint까지`로 수렴할 수 있다.

방어:
- 권장 C는 4개만 사용한다.
- +20/+40/+50/+70/+80은 floor가 아니다.

재검사:
- DOWNGRADE는 긴 구간에서 실제 단계 손실로 계속 작동한다.

판정: `PASS`.

### Loop 2 · checkpoint가 너무 드물어 rollback grind가 되는가

공격:
- +60만 마지막 floor면 MASTERY +61~+100이 40단계다.
- MASTERY는 failure 중 DOWNGRADE 20%라 반복 복구가 강화 재미를 덮을 수 있다.

방어:
- +90 staging floor를 추가해 마지막 +91~+100을 10단계 final push로 분리한다.

재검사:
- +60→+90은 여전히 긴 MASTERY 구간이라 고위험 정체성을 보존한다.

판정: `PASS_WITH_PLAYTEST`.

### Loop 3 · checkpoint 직후가 사실상 free-roll인가

공격:
- floor에서 다음 단계 시도 중 DOWNGRADE가 뽑히면 실제 단계 하락이 막힌다.
- +30→+31, +60→+61, +90→+91이 무조건 누르는 정답이 될 수 있다.

방어:
- DAMAGE/CRITICAL과 시도비는 그대로다.
- blocked DOWNGRADE를 DAMAGE로 몰래 전환하지 않는다.
- 위험이 약하면 숨은 severity를 추가하지 않고 floor cadence/성공률/비용을 재검토한다.

재검사 지표:
- checkpoint 직후 시도율이 인접 단계보다 과도하게 높고 이유가 오직 DOWNGRADE 차단이면 재검토.

판정: `PASS_WITH_MONITORING`.

### Loop 4 · band boundary가 자동 checkpoint로 굳는가

공격:
- +30/+60을 floor로 선택하면 향후 `band가 바뀌면 floor`라는 잘못된 규칙이 생길 수 있다.

방어:
- +90은 band boundary가 아니지만 floor다.
- +11 FIRST_STOP은 band지만 floor가 아니다.
- floor list는 명시 데이터이며 band mapping과 별도 책임이다.

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

판정: `PASS`.

### Loop 5 · checkpoint가 경제 arbitrage를 만드는가

공격:
- floor 직후 rollback 기대비용이 낮아져 강화 기대원가가 불연속적으로 변할 수 있다.
- 시장가를 checkpoint bonus로 또 올리면 중복 보상/판매 타이밍 메타가 생긴다.

방어:
- checkpoint 자체 판매가 multiplier 금지.
- 다음 경제곡선에서 floor가 기대원가에 미치는 효과를 먼저 계산하고 판매가를 맞춘다.
- `+11 이후 expected profit > 0`과 단조 장기 수익 증가를 함께 검증한다.

판정: `PASS_REQUIRES_ECONOMY_SIMULATION_NEXT`.

## 14. 권장 Checkpoint 계약

현재 권장:

```text
C · 위험막 전환 + 최종 러시형

CHECKPOINT_FLOORS = [10, 30, 60, 90]
MAX_LEVEL = 100
```

```text
on_success(level):
  if level in CHECKPOINT_FLOORS:
    highest_secured_floor = max(highest_secured_floor, level)

on_downgrade(current_level):
  resolved_level = max(current_level - 1, highest_secured_floor)
```

Checkpoint는 UID에 귀속하고 다른 작품/후계 작품으로 자동 이전하지 않는다.

## 15. UI 계약

강화 전 기본 판단 영역:

```text
현재 단계
다음 목표 단계
현재 확보 floor
다음 checkpoint
최종 성공률
최종 실패 outcome
CURRENT/MAX
비용
```

floor에서 DOWNGRADE가 막히는 경우 최종 outcome에 반영한다.

Checkpoint 도달 시:
- `단계 확보 +30`처럼 명료하게 표시.
- CURRENT/MAX가 회복되지 않음을 혼동시키지 않는다.
- +10은 경제 회수선이므로 가장 강한 경제 피드백.
- +30/+60/+90은 진행 확보 피드백이되 매번 대형 장시간 연출로 리듬을 끊지 않는다.

## 16. 시뮬레이션 / Human 검증 지표

다음 경제곡선/Balance Lab에서 최소 측정:

```text
attempts per +10 range
DOWNGRADE count per range
blocked DOWNGRADE count at floors
levels re-earned after downgrade
repair jobs per range
CURRENT/MAX loss by range
stop/sell rate at +10/+30/+60/+90
attempt rate immediately after floor
P50/P75/P90 cumulative cost per floor
P50/P75/P90 attempts to +100
```

재검토 조건:
- checkpoint 직후가 무조건 도전 정답이 됨.
- 플레이어가 checkpoint에서만 판매하고 중간 단계 가치가 사라짐.
- +60→+90 구간에서 MASTERY 포기율/재노동이 과도함.
- +90 floor 때문에 +91~+100 긴장이 의미 있게 사라짐.
- DOWNGRADE의 대부분이 checkpoint에 막혀 family 존재 이유가 약해짐.
- checkpoint가 CURRENT/MAX보다 훨씬 중요한 유일한 위험축이 됨.

## 17. 다음 Decision

16 승인 뒤 다음은:

```text
BS-PROGRESSION-20260820-17
+0~+100 success / attempt cost / sale value / cumulative expected cost curve
```

17은 반드시 13 failure family, 15 band mapping, 16 checkpoint floor를 함께 시뮬레이션 입력으로 사용한다.

제품 code/data/runtime은 새 `기획 완료` 전 변경하지 않는다.
