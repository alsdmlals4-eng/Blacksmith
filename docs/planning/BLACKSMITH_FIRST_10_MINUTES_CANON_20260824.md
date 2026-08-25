# [현재 정본] Blacksmith 첫 10분 Core Thesis 온보딩

- Original Decision: `BS-ONBOARD-20260824-23`
- Current refinement: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-CHRONICLE-20260825-27`
- Current owner: `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- 상태: `USER_APPROVED / PLANNING_CANON / PARTIALLY_REFINED_2026-08-25`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Human/Player validation: `NOT_RUN`

> 2026-08-24 원본의 pacing·STOP/PUSH·실제 확률·Nadia handoff 원리는 유지한다. CURRENT/MAX teaching, +10/+20/... 다중 정밀강화, +11 MAX structural-scar 설명은 Decisions25~27에서 대체됐다. 이전 전문은 Git history에 보존된다.

## 1. 목적

첫 10분의 목적은 전체 시스템 설명이 아니다.

```text
GOAL
= 플레이어가 Blacksmith의 핵심 재미를 직접 한 번 경험하고
  왜 다음 작품/다음 강화를 하고 싶은지 설명할 수 있게 한다.
```

핵심 thesis:

```text
좋은 작품을 지킬까
vs
한 번 더 강화해 더 큰 가치를 노릴까
```

정밀강화·고객/세계·경제·UID 생애는 이 질문을 강화하는 SUPPORT다.

## 2. Current first-session flow

```text
New Game
-> 짧은 첫 작품 제작
-> +1/+2 LEARN
-> +3~+9 ordinary BUILD_CONFIDENCE
-> +9 -> +10 Precision Enhancement
-> 성공 시 ITEM_KEYWORD 1개 생성
-> +10 checkpoint + 첫 경제 확보/break-even state
-> +11 first damage-eligible risk Preview
-> STOP vs PUSH 실제 선택
-> 실제 결과
-> 짧은 same-UID 고객 acknowledgement
-> delayed customer/world result는 이후 일정에서 해결
```

불변:

```text
SUCCESS_LEVEL_DELTA = +1
NO_MULTI_LEVEL_SUCCESS
NO_SCRIPTED_FAILURE
NO_HIDDEN_SUCCESS_BOOST
NO_TUTORIAL_ONLY_ODDS
NO_FORCED_+11
NO_VENDOR_GATE_BEFORE_FIRST_STOP_DECISION
NO_FULL_SYSTEM_LECTURE
```

첫 10분은 강제 countdown이 아니라 UX pacing 목표다.

## 3. Pacing target

| 목표 시간 | 경험 | 새로 학습하는 것 |
|---:|---|---|
| `0:00~0:45` | New Game -> Workshop | 나는 대장장이이고 첫 작품을 만든다 |
| `0:45~2:00` | 첫 작품 짧은 직접 제작 | 작품명·등급·UID·기본성능 |
| `2:00~3:00` | +1/+2 | 한 번의 강화 입력 -> 기대 -> 한 결과 |
| `3:00~5:30` | +3~+9 | 강화 가치와 same-target recovery |
| `5:30~7:30` | +9 -> +10 Precision | 첫 커스터마이즈·키워드·checkpoint·경제 확보 |
| `7:30~9:00` | +11 risk preview | 처음으로 실패 시 작품 손상 가능 |
| `9:00~10:00` | STOP vs PUSH | 핵심 의사결정 + same UID payoff |

시간을 넘겨도 실패 처리하지 않는다.

## 4. Stage 0 · Main Menu / Workshop

기존 `MainMenu -> BlacksmithApp -> WORKSHOP` shell은 reuse 가능하다. 첫 New Game 전에 장황한 세계관 exposition, 클래스 선택, 전체 고객/상점 강의를 요구하지 않는다.

최소 표시:

```text
첫 의뢰/목표 한 줄
첫 작품 제작 CTA
```

MainMenu/Save의 실제 runtime 구현은 기존 구현 사실이며 이번 PLAN Decision이 수정하지 않는다.

## 5. Stage 1 · 첫 작품 제작

2분 안에 첫 강화 가능한 정상 UID 작품을 얻는 것을 목표로 한다.

완료 시 최소 공개:

```text
작품명
제작 등급
ITEM_UID
기본 성능
강화 가능 상태
```

Artistry·세 affix·고급 경제 전체 설명은 필요 시 상세 보기로 미룬다.

## 6. Stage 2 · +1/+2 LEARN

첫 강화 input 목표는 약 3분 이내다.

P0 정보:

```text
현재 강화 단계
다음 TARGET = CURRENT + 1
최종 성공률
시도 비용
보강재 필요량
[강화]
```

튜토리얼용 성공률 보정이나 scripted failure를 사용하지 않는다.

## 7. Stage 3 · +3~+9 BUILD_CONFIDENCE

목표는 반복 클릭이 아니라 `강화 -> 가치 상승 -> 다음 선택` 패턴 학습이다.

Current damage rule:

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
```

따라서 이전처럼 +3에서 CURRENT 손상 UI를 가르치지 않는다. 실패가 실제 발생하면 same-UID recovery만 just-in-time으로 설명한다.

```text
same UID + same target failure
-> recovery progress
-> next success expectation improves according to current recovery owner
```

BUILD 구간 feedback:

```text
fast expectation
-> short impact
-> immediate result
-> next question
```

매 단계마다 스킵 불가 대형 연출을 반복하지 않는다.

## 8. Stage 4 · +9 -> +10 Precision Keyword

+10의 current 의미:

```text
FIRST_ECONOMIC_STOP_STATE
CHECKPOINT_FLOOR +10
ONLY_PRECISION_ENHANCEMENT_MOMENT
FIRST_ITEM_KEYWORD_CREATION_GATE
```

Precision 입력은 기존 역할 분리를 활용할 수 있다.

```text
주재료 맥락
+ 강화 방식
+ 촉매 1개
-> compatible ITEM_KEYWORD candidate/result
```

기본 화면:

```text
추천 강화 방식
추천 호환 촉매
예상 방향 / trade-off
[이 조합으로 진행]
[다른 방식 보기]
```

```text
FULL_RULES_AVAILABLE
DEFAULT_PATH_RECOMMENDED
NO_HARD_LOCK
```

성공 시:

```text
+10 확보 완료
ITEM_KEYWORD 1개 생성
최근 checkpoint = +10
대표 기본 공개시장 기준 첫 경제 확보/break-even state
```

실패하면 keyword는 생성되지 않는다. 성공은 +10 한 단계만 올린다.

`+20/+30/+40/+50`에서 Precision Enhancement를 다시 열지 않는다.

## 9. Stage 5 · +11 First Damage-Eligible Risk

+11은 첫 `FIRST_STOP_POINT ATTEMPT`이며 처음으로 강화 실패가 작품 손상을 만들 수 있는 시도다.

```text
TARGET +11: ENHANCEMENT_DAMAGE = POSSIBLE
```

필수 비교:

```text
현재 +10을 지키면
- checkpoint와 첫 경제 확보 상태 유지
- +10 keyword를 가진 작품을 보유/인계 가능

+11에 도전하면
- 한 단계 높은 성장 가능
- 실패 결과가 존재
- 실패 시 낮은 damage 가능성이 처음 열림
- damage event가 발생하면 NORMAL -> MINOR처럼 정확히 한 단계 악화
```

정확 damage percent는 아직 승인되지 않았다.

```text
DAMAGE_PROBABILITY_CURVE = USER_APPROVAL_REQUIRED
MONOTONIC_NON_DECREASING_DAMAGE_RISK
```

UI는 확률이 확정되기 전 숫자를 만들어내지 않는다. +11을 튜토리얼 진행 조건으로 강제하지 않는다.

버튼 의미:

```text
[이 작품을 지킨다]
[+11에 도전한다]
```

## 10. Stage 6 · STOP / PUSH 모두 정상 완료

### STOP

```text
+10 작품 보유/인계
-> 정상 first-session completion
```

### PUSH

+11은 실제 current success/recovery 계약으로 해결한다. 성공/실패 모두 same UID에 실제 상태만 반영한다.

손상 event가 발생할 때만:

```text
NORMAL -> MINOR
MINOR -> MAJOR
MAJOR -> DESTROYED
```

한 event가 두 단계를 건너뛰지 않는다.

## 11. Stage 7 · Nadia / same-UID acknowledgement

첫 세션 starter owner는 기존 `NADIA_VENN / ADVENTURER_01`을 재사용한다. Nadia는 exact recipe 정답을 주지 않고 목적·제약·알려진 상황을 제공한다.

```text
STARTER_ORDER
-> 실제 UID 작품
-> STOP +10 또는 PUSH 결과 모두 정상 handoff 후보
-> 실제 선택 장점/대가 1~2개 acknowledgement
-> delayed personal schedule 활성화
```

첫 10분에 전체 탐사 결과를 즉시 해결하지 않는다.

## 12. Customer/world event damage와 첫 세션 경계

```text
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
```

고객이 작품을 구매/인계받는 순간 자동 손상시키지 않는다. 이후 실제 사용이 포함된 eligible event가 해결될 때 same UID가 한 damage state 악화될 수 있다.

첫 세션에서는 이 가능성의 존재를 장황하게 강의하지 않는다. 실제 delayed event에서 손상이 발생하면 그 사건의 원인으로 설명한다.

정확 event eligibility와 damage probability는 후속 `CUSTOMER_EVENT_DAMAGE_POLICY` owner가 결정한다.

## 13. Information disclosure ladder

| 시점 | 새 P0 정보 | 아직 강제하지 않는 것 |
|---|---|---|
| 첫 제작 | 작품명/등급/UID/기본성능 | 전체 Artistry/affix 경제 |
| +1 | 단계/성공률/비용/보강재 | 손상/수리/후기 시스템 |
| 실제 첫 실패 | same-target recovery | damage probability — +10 이하에는 없음 |
| +9→+10 | Precision 입력/키워드/checkpoint/경제 확보 | 후기 고객·시장 전체 |
| +11 preview | damage 가능성 + STOP/PUSH | 정확 미승인 damage curve |
| 첫 결과 | same UID + 짧은 고객 acknowledgement | 전체 세계 일정 관리 |
| 실제 후속 damage event | 사건 원인 + damage state delta | 보편 customer damage 공식 |

원칙:

```text
TEACH_WHEN_NEEDED
NOT_ALL_AT_START
```

## 14. Chronicle disclosure

첫 세션에서 `+1 성공 / +2 성공 / N일 전` 같은 routine attempt timeline을 만들지 않는다.

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
```

보여줄 가치가 있는 첫 사건 후보:

```text
ITEM_CREATED
PRECISION_KEYWORD_CREATED
DAMAGE_STATE_CHANGED
CUSTOMER_HANDOFF
CUSTOMER_WORLD_CONSEQUENCE
DESTROYED
```

내부 game-day/sequence provenance는 delayed causality를 위해 남을 수 있다.

## 15. 첫 핵심 선택 전에 강제하지 않는 것

- MINOR/MAJOR repair의 미승인 상세 모델
- 고객 event damage 확률표
- Archive/Memorial/Successor 관리 전체
- +100 completion 상세
- 전체 고객 관계 관리
- 전체 세계 일정 관리
- 고급 Artistry 가치 공식
- 자동 단조
- 모든 catalyst/keyword catalogue

## 16. Validation / evidence boundary

Automated planning acceptance:

```text
+1 success only
+9 -> +10 only Precision
+10 keyword exactly one
no enhancement damage through +10
+11 first damage-eligible attempt
STOP/PUSH both valid
same UID handoff
no routine dated Chronicle log
```

Human validation still required:

- 첫 +10 keyword가 작품 정체성 순간으로 이해되는가.
- +11에서 처음 열린 손상 위험을 과도한 공포 없이 이해하는가.
- STOP와 PUSH가 모두 정상 선택으로 느껴지는가.
- 10분 pacing이 실제 기기/독해속도에서 성립하는가.

```text
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
```
