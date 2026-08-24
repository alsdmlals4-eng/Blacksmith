# [현재 정본] Blacksmith 정밀강화·고객/세계 인과 연결

- Parent: `BS-ONBOARD-20260824-23`, `BS-CONTENT-20260811-01`, `BS-CUSTOMER-20260805-01`, `BS-CUSTOMER-20260806-01`
- Cross-reference: `BS-CRAFT-20260804-04~06`, `BS-ITEM-20260806-04~06`, `BS-UX-20260805-01`, `BS-DESTRUCTION-20260824-21`
- Decision: `BS-LINK-20260824-24`
- 사용자 승인: `2026-08-24 KST / 권장안 B + 고객 강화 기여 0.30pp/level 테스트 Budget + NADIA_VENN starter-order binding 승인`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Numeric status: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Runtime mutation: `NOT_ALLOWED_IN_THIS_DECISION`
- Human/Player validation: `NOT_RUN`

## 1. 목적

정밀강화가 단순한 내부 스탯 커스터마이즈로 끝나지 않고, **누구에게 어떤 작품을 맡길지에 대한 실제 이유**가 되게 한다.

동시에 고객 시스템이 강화보다 상위 메인 게임으로 커지지 않도록 한다.

```text
CUSTOMER CONTEXT
-> PRECISION CHOICE
-> ITEM UID
-> EQUIPMENT HANDOFF
-> MULTI-AXIS WORLD RESULT
-> 2~4 CAUSAL REASONS
-> SAME UID NEXT ACTION
```

핵심은 `정답 레시피`도 `종합 적합도 점수`도 아니다.

## 2. 승인 구조

```text
DISCLOSED_CONTEXT_FIT_AND_CAUSAL_MULTI_AXIS_RESULT
```

고객은 다음을 공개한다.

```text
목적
제약
알려진 상황
```

플레이어는 다음을 결정한다.

```text
어떤 작품을 만들지
어디까지 강화할지
정밀강화에서 어떤 방식을 선택할지
어떤 촉매를 사용할지
언제 멈출지
어떤 고객에게 인계할지
```

시스템은 다음을 설명한다.

```text
배정 가능/불가 hard gate
이번 맥락에 직접 도움이 되는 원인
trade-off
공개 가능한 예상 결과 방향
실제 결과의 원인 2~4개
```

금지:

```text
NO_UNIVERSAL_FIT_SCORE
NO_BEST_BADGE
NO_OPAQUE_AUTO_RECOMMENDATION
NO_CUSTOMER_EXACT_RECIPE_AS_DEFAULT
NO_HIDDEN_CONTEXT_BONUS
```

## 3. 첫 세션 starter-order owner

```text
STARTER_ORDER_OWNER = NADIA_VENN
CONTENT_ID = ADVENTURER_01
STARTER_GOAL = SURVIVAL_AND_RECOVERY
STARTER_REQUIRED_SPECIAL_FUNCTION = NONE
```

나디아를 첫 세션 owner로 사용한다.

이유:
- R3 첫 상세 고객 콘텐츠다.
- 작품 한 점만 인계한다.
- `ENHANCEMENT_LEVEL_AND_RISK / WEIGHT_AND_CUSTOMER_FIT / ENVIRONMENTAL_OR_UTILITY_FIT` 세 축이 이미 정의되어 있다.
- `single_always_best_equipment_answer=false`가 이미 승인되어 있다.
- 결과가 같은 UID의 복원·후속 강화·다음 제작 이유로 돌아간다.

Decision24는 새 Nadia 설정·성격·세계관을 만들지 않는다. 기존 `BS-CONTENT-20260811-01`을 소비한다.

## 4. Customer Context Packet

고객 판단 입력은 다음 의미 계층으로 제공한다.

```text
CUSTOMER_CONTEXT_PACKET
  PRIMARY_NEED
  SECONDARY_NEED
  KNOWN_CONTEXT
  HARD_LOAD_GATE
  REQUIRED_FUNCTION_IF_EXPLICIT
```

Nadia starter의 baseline 의미:

```text
PRIMARY_NEED = SAFE_RETURN
SECONDARY_NEED = RECOVERY_POSSIBILITY
HARD_LOAD_GATE = CURRENT_TOTAL_WEIGHT <= NADIA_MAXIMUM_LOAD
REQUIRED_FUNCTION_IF_EXPLICIT = NONE
```

고객은 `경량화를 선택하라`, `특정 촉매를 넣어라` 같은 exact recipe를 정답으로 알려주지 않는다.

## 5. 정밀강화 연결

현재 정밀강화는 `+10/+20/+30/+40/+50` 이정표에서 강화 방식과 촉매를 선택한다.

Decision24는 이 선택을 고객 맥락과 연결하되 기존 역할 소유권을 유지한다.

### 5.1 강화 방식

대표 의미:

```text
BLADE_REINFORCEMENT
-> 공격/정밀 방향
-> 해당 의뢰가 공격 역할을 실제 요구할 때만 고객 맥락 원인

IMPACT_ABSORPTION
-> 방어/내구 방향
-> 생존·충격 부담과 실제 관련 있을 때 원인

LIGHTWEIGHT
-> current weight 감소 및 handling 방향
-> load gate 또는 휴대 맥락과 실제 관련 있을 때 원인

BALANCE_ADJUSTMENT
-> handling/stability 방향
-> 취급·운용 맥락과 실제 관련 있을 때 원인

ARTISTIC_FINISH
-> Artistry/value 방향
-> Nadia starter의 일반 생환·회수 성공 원인으로 자동 합산하지 않음

ENVIRONMENTAL_TREATMENT
-> 승인된 bound environment가 현재 고객/사건 context와 실제 일치할 때만 원인
```

정밀강화 미리보기는 `Best` 대신 다음을 보여준다.

```text
이번 의뢰에 직접 도움
Gate 변화
trade-off
이번 의뢰에 직접 관련 없음
```

### 5.2 촉매

촉매는 계속 `CATALYST_AFFIX`의 계보·씨앗·분기·변형 확률을 소유한다.

```text
CATALYST_SELECTED
!= CUSTOMER_BONUS_GRANTED
```

촉매를 넣었다는 이유만으로 고객 성공률을 올리지 않는다.

실제로 생성된 승인 수식어/기능이 현재 고객 맥락과 관련될 때만 고객 판단 원인으로 소비한다.

### 5.3 특수기능

특수기능은 기존 권위대로 다음 중 하나로만 작동한다.

```text
ELIGIBILITY
RISK_MITIGATION
SPECIFIC_INTERACTION
```

일반 사건 전체에 범용 성공률 보너스로 자동 합산하지 않는다.

## 6. 강화 레벨의 고객 사건 기여 교정

### 6.1 역사 수치

기존 R2:

```text
ENHANCEMENT_EVENT_BONUS_PP = enhancement_level
```

즉 `+1 level = +1%p`였다.

현재 +0~+100 구조에서는 후기 강화만으로 95% cap에 너무 쉽게 도달하여 `최고 강화 자동 정답`을 만들 가능성이 크다.

Decision24 승인 후 이 수치는:

```text
HISTORICAL_PRE_24_NUMERIC_EVIDENCE
```

로 강등한다.

### 6.2 승인된 새 테스트 Budget

```text
ENHANCEMENT_EVENT_BONUS_PP
= round(0.30 * enhancement_level)

MIN = 0pp
MAX = 30pp at +100
```

고객 일반 사건의 첫 테스트 shell은 다음 구조를 사용한다.

```text
risk_base
= clamp(100 - risk * 10, 5, 90)

related_ability_met
= +5pp

proficiency
0 = -10pp
1 =   0pp
2 =  +5pp
3 = +10pp

enhancement_contribution
= round(0.30 * enhancement_level)

final_primary_estimate
= clamp(
    risk_base
    + enhancement_contribution
    + related_ability_modifier
    + proficiency_modifier,
    5,
    95
  )
```

이 수치는 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`다.

Human playtest와 final Balance Lab 전 출시 최종 공식으로 주장하지 않는다.

## 7. 0.30pp/level 선택 근거

위험도 6의 base 40%에서 고객 보정 전:

| Enhancement | pre-24 +1.00pp | 0.20pp alt | approved 0.30pp | 0.40pp alt |
|---:|---:|---:|---:|---:|
| +10 | 50% | 42% | 43% | 44% |
| +30 | 70% | 46% | 49% | 52% |
| +60 | 95% cap | 52% | 58% | 64% |
| +100 | 95% cap | 60% | 70% | 80% |

판정:
- 0.20pp: 후기 강화의 고객 맥락 기여가 너무 약해질 위험.
- 0.30pp: 강화가 가장 큰 단일 가산축으로 남지만 고객·상황 판단을 지우지 않음.
- 0.40pp: 후기에서 다시 최고 강화가 다수 맥락을 압도할 위험.
- pre-24 1.00pp: 현재 +100 체계와 부적합.

정확 체감은 `HUMAN_NOT_RUN`이다.

## 8. 고객 장비 판단 정보 계층

기존 `BS-UX-20260805-01`의 progressive disclosure를 유지한다.

```text
DEFAULT_CUSTOMER_CARD
-> POST_EQUIPMENT_DECISION_LAYER
-> DETAIL_VIEW
```

작품 선택 후 우선순위:

```text
1. HARD GATE
2. ENHANCEMENT CONTRIBUTION
3. RELEVANT PRECISION/FUNCTION FIT
4. SMALL CUSTOMER ABILITY/PROFICIENCY CONTEXT
```

`OVERWEIGHT` 또는 explicit required function 미충족이면 먼저 `배정 불가`를 표시한다.

행동 가능한 성공률을 그 위에 덮어쓰지 않는다.

한도 이내이면 `약 N%`와 핵심 원인 2~4개를 표시한다.

금지:

```text
적합도 92점
추천 1위
Best
자동 장착
숨은 종합점수
```

## 9. 결과는 다중 축으로 유지

Nadia `ADVENTURER_01`의 기존 결과축을 재사용한다.

```text
EXPEDITION_RETURN_STATE
RECOVERY_STATE
ITEM_UID_LIFECYCLE_STATE
```

Decision24는 이를 하나의 `SUCCESS_SCORE`로 압축하지 않는다.

### 9.1 원인 책임

```text
ENHANCEMENT_LEVEL
-> primary mission estimate의 bounded contribution

WEIGHT
-> HARD GATE

DURABILITY / HANDLING
-> 현재 고객/사건 필요와 실제 연결될 때 causal evidence

APPROVED_FUNCTION / AFFIX
-> 특정 eligibility / mitigation / interaction

CUSTOMER ABILITY / PROFICIENCY
-> smaller contextual modifier

ARTISTRY
-> Nadia starter의 일반 생환·회수 결과에 자동 합산하지 않음
```

같은 원인을 여러 축에 중복 합산하지 않는다.

## 10. 결과 피드백

결정적 결과에서는:

```text
RESULT_AXES
+ CAUSAL_REASONS 2~4
+ SAME UID
+ PRIMARY_NEXT_ACTION 1
```

을 제공한다.

현재 `VSContentResultRecord`가 `content_id/customer_id/item_refs/result_axes/causal_reasons/primary_next_action` 구조를 이미 보유하지만, 이는 결과 기록 기반의 구현 증거일 뿐 Decision24의 실제 resolver 구현 증거는 아니다.

## 11. 첫 10분과 지연 결과 분리

첫 10분에 Nadia의 전체 유적 탐사를 즉시 해결하지 않는다.

```text
Nadia starter order
-> first item
-> +10
-> STOP or +11 PUSH
-> 살아 있고 배정 가능하면 handoff
-> Nadia가 실제 장점/대가 1~2개를 acknowledgement
-> PERSONAL_SCHEDULE 활성화
-> first-session core thesis complete 가능
```

완전한 world result는 기존 개인 일정 구조에 따라 지연된다.

```text
later day progression
-> expedition result
-> three result axes
-> causal reasons 2~4
-> same UID lifecycle result
-> repair / followup enhancement / recovery / new craft reason
```

첫 10분용 가짜 즉시 탐사결과는 만들지 않는다.

## 12. Nadia starter acknowledgement

인계 직후 짧은 확인은 **실제 선택 데이터만** 사용한다.

예시 의미:

```text
"중량은 감당할 수 있어요. 이 정도 강화면 유적 안에서 버틸 가능성은 있겠네요."
"가볍게 만든 덕분에 다루기 쉽겠어요. 대신 상태를 오래 유지할지는 두고 봐야겠네요."
```

정확한 대사는 후속 카피/콘텐츠 작업 대상이다.

다음은 하지 않는다.
- 아직 발생하지 않은 유적 결과 예언.
- 플레이어가 보지 못한 hidden stat 공개.
- 미래 실패/성공을 확정적으로 말하기.
- Nadia의 기존 성격/설정 변경.

## 13. 단일 정답 방지

첫 테스트에서는 최소 세 후보가 서로 다른 이유를 가져야 한다.

```text
A: 강화 높음 / 상대적으로 무거움 / contextual utility 없음
B: 중간 강화 / load 내 / 범용적
C: 강화 낮을 수 있음 / 실제 context와 맞는 approved utility 또는 정밀 결과
```

이 fixture는 제품 정본이 아니라 테스트 구조다.

PASS 목표:
- 여러 플레이어가 자동으로 최고 강화만 고르지 않음.
- 중량 Gate를 성공률보다 우선 이해.
- context function/precision 결과를 `무조건 bonus`가 아니라 특정 맥락 근거로 이해.
- 결과 뒤 같은 UID와 다음 행동을 연결.

## 14. 벤치마크 비교

### A. Monster Hunter — ADAPT

채택:
- 상대/상황 특성에 따라 장비 속성·역할이 달라지는 contextual loadout 판단.
- 단일 raw power보다 공개된 맥락과 대응 장비의 관계.

비채택:
- 직접 전투 장비 빌드 게임으로 확장.
- 다수 전투 보조 수치 기본화.

### B. FFXIV Custom Deliveries — ADAPT / AVOID

채택:
- 고객의 요구와 보상 방향을 명확히 공개.

비채택:
- 고객이 정답 제작 레시피를 직접 지정하여 선택을 제거하는 구조.

### C. Potion Craft — ADAPT / AVOID

채택:
- 고객 문제를 읽고 여러 해결 경로를 고르는 구조.

비채택:
- matching/compatible 규칙이 숨겨져 실패 원인을 이해하기 어려운 구조.

Blacksmith는 고객 요구를 **목적·제약·알려진 상황**으로 공개하고, 정밀강화 방식 자체를 정답으로 지정하지 않는다.

## 15. 적대적 검토 5회

### Loop 1 — 주문서 게임화
공격: 고객이 exact 방식/촉매를 요구하면 강화 선택이 사라진다.

대응: 목적·제약·상황만 공개, 방법은 복수 경로.

판정: `PASS`.

### Loop 2 — 종합 적합도 메타
공격: 단일 점수/Best가 모든 판단을 대체한다.

대응: hard gate + 공개 추정치 + 원인 2~4개 + 다중 결과축.

판정: `PASS`.

### Loop 3 — 최고 강화 자동 정답
공격: pre-24 +1pp/level은 현재 +100 구조에서 95% cap을 빠르게 만든다.

대응: `0.30pp/level`, max +30pp 테스트 Budget.

판정: `PASS_WITH_BALANCE_TEST`.

### Loop 4 — 중복 계산
공격: 정밀강화 하나가 raw stat + catalyst + customer score + market value에 반복 합산될 수 있다.

대응: 각 source owner를 한 번만 소비. catalyst selected 자체는 고객 bonus가 아님.

판정: `PASS`.

### Loop 5 — 첫 10분 과밀
공격: 제작·정밀·고객·탐사 전체를 10분에 해결하면 고객 시스템이 코어를 압도한다.

대응: 첫 세션은 handoff acknowledgement까지. full world result는 delayed schedule.

판정: `PASS_WITH_HUMAN_TEST`.

새 설계 blocker 없음.

## 16. Implementation Reality Gate

```text
DESIGN_CANON = VERIFIED
R3_NADIA_CANON = EXISTS
CONTENT_RESULT_RECORD_PRIMITIVE = EXISTS
PRECISION_TO_CUSTOMER_PREVIEW = IMPLEMENTATION_UNVERIFIED
CUSTOMER_RESULT_RESOLVER = IMPLEMENTATION_UNVERIFIED
0_30_PP_RUNTIME = NOT_IMPLEMENTED
STARTER_NADIA_ORDER_RUNTIME = NOT_IMPLEMENTED
FIRST_SESSION_HANDOFF_RUNTIME = NOT_IMPLEMENTED
HUMAN_CHOICE_DIVERSITY = NOT_RUN
ANDROID_CUSTOMER_UI = NOT_RUN
PRODUCT_IMPLEMENTATION = BLOCKED
```

주의:
- `VSContentResultRecord` 존재를 전체 고객 gameplay 구현 PASS로 주장하지 않는다.
- historical customer success formula runtime가 있더라도 Decision24 현재 권위 구현으로 간주하지 않는다.
- 새 `기획 완료` 선언 전 runtime/data/scene 변경 금지.

## 17. Release-near 소비 계약

`RELEASE_NEAR_VERTICAL_SLICE`는 Decision24에서 다음을 소비해야 한다.

```text
NADIA starter-order entry
+ customer context packet
+ +10 precision preview
+ +10 STOP / +11 PUSH handoff convergence
+ 0.30pp/level customer enhancement test budget
+ hard load gate
+ no universal fit score
+ delayed Nadia schedule
+ multi-axis causal result record
+ same UID next action
```

Decision24가 final product balance, exact dialogue, final UI layout, Android pass, Human fun pass를 승인하지 않는다.

## 18. 기대효과

작업 전:
- 정밀강화와 고객 콘텐츠는 각각 정본이 있었지만 직접 연결 책임이 분산되어 있었다.
- 구형 `+1%p/level` 고객 공식은 현재 +100 체계에서 최고 강화 자동 정답 위험이 있었다.
- 첫 10분 starter-order owner가 미확정이었다.

작업 후:
- Nadia가 첫 세션의 실제 고객 anchor가 된다.
- 고객은 정답 레시피가 아니라 목적/제약/context를 제공한다.
- 정밀강화 결과가 고객 판단의 설명 가능한 원인이 된다.
- 강화 기여를 +30pp 상한 테스트 Budget으로 제한해 context 선택 공간을 보존한다.
- 결과는 하나의 점수가 아니라 같은 UID의 다중 축 생애 결과로 돌아온다.

기대효과:
- 강화가 계속 메인 게임으로 남는다.
- 정밀강화가 고객/세계에 실제 사용 이유를 얻는다.
- 최고 강화만 반복하는 단일 메타를 줄인다.
- 첫 10분 선택이 이후 세계 결과와 같은 UID에 연결된다.

## 19. 후속 Gate

다음 현재 작업:

```text
RELEASE_NEAR_VERTICAL_SLICE
```

여기서 18~24의 승인 정본을 하나의 구현 가능 vertical-slice 계약으로 묶는다.

제품 구현은 계속 `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`이다.
