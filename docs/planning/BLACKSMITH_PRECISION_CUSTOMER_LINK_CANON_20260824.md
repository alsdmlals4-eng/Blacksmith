# [현재 정본] Blacksmith 정밀강화·고객/세계 인과 연결

- Original Decision: `BS-LINK-20260824-24`
- Current refinement: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-CHRONICLE-20260825-27`
- Current owner: `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- 사용자 승인: original Decision24 + 2026-08-25 simplified-core refinement
- 상태: `USER_APPROVED / PLANNING_CANON / PARTIALLY_REFINED_2026-08-25`
- Numeric status: customer enhancement contribution `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Human/Player validation: `NOT_RUN`

> Decision24의 고객 목적·제약·same-UID delayed causality는 유지한다. 구형 `+10/+20/+30/+40/+50` Precision cadence와 CURRENT/MAX durability references는 Decisions25~26에서 대체됐다. 이전 전문은 Git history에 보존된다.

## 1. 목적

Precision Enhancement를 단순 내부 스탯 커스터마이즈가 아니라 **어떤 작품을 어떤 사람에게 맡길지**에 연결한다. 동시에 고객 시스템이 강화보다 상위 메인 게임으로 커지지 않게 한다.

```text
CUSTOMER CONTEXT
-> +9 -> +10 PRECISION CHOICE
-> ITEM KEYWORD
-> ITEM UID
-> EQUIPMENT HANDOFF / PURCHASE
-> DELAYED WORLD EVENT
-> MULTI-AXIS RESULT + POSSIBLE ITEM DAMAGE
-> 2~4 CAUSAL REASONS
-> SAME UID NEXT ACTION
```

핵심은 `정답 레시피`나 `종합 적합도 점수`가 아니다.

## 2. 고객이 공개하는 정보 / 플레이어가 결정하는 것

고객은:

```text
목적
제약
알려진 상황
```

을 공개한다.

플레이어는:

```text
어떤 작품을 만들지
어디까지 강화할지
+9 -> +10 Precision에서 어떤 방식을 선택할지
어떤 촉매를 사용할지
언제 멈출지
어떤 고객에게 인계/판매할지
```

를 결정한다.

금지:

```text
NO_UNIVERSAL_FIT_SCORE
NO_BEST_BADGE
NO_OPAQUE_AUTO_RECOMMENDATION
NO_CUSTOMER_EXACT_RECIPE_AS_DEFAULT
NO_HIDDEN_CONTEXT_BONUS
```

## 3. Starter owner · Nadia

```text
STARTER_ORDER_OWNER = NADIA_VENN
CONTENT_ID = ADVENTURER_01
STARTER_GOAL = SURVIVAL_AND_RECOVERY
STARTER_REQUIRED_SPECIAL_FUNCTION = NONE
```

Nadia는 첫 세션 대표 고객으로 유지한다. 새 Nadia 성격·능력치를 이 Decision에서 발명하지 않는다.

## 4. Customer Context Packet

기존 의미 계층을 유지한다.

```text
CUSTOMER_CONTEXT_PACKET
  PRIMARY_NEED
  SECONDARY_NEED
  KNOWN_CONTEXT
  HARD_LOAD_GATE
  REQUIRED_FUNCTION_IF_EXPLICIT
```

Nadia baseline 의미:

```text
PRIMARY_NEED = SAFE_RETURN
SECONDARY_NEED = RECOVERY_POSSIBILITY
HARD_LOAD_GATE = CURRENT_TOTAL_WEIGHT <= NADIA_MAXIMUM_LOAD
REQUIRED_FUNCTION_IF_EXPLICIT = NONE
```

정확한 Nadia capability 수치가 별도 정본에 없으면 생성하지 않는다.

## 5. Current Precision Enhancement 연결

```text
+9 -> +10 = ONLY_PRECISION_ENHANCEMENT
SUCCESS_LEVEL_DELTA = +1
SUCCESS +10 -> exactly one ITEM_KEYWORD
ITEM_KEYWORD machine owner = CATALYST_AFFIX
```

`+20/+30/+40/+50`에서 Precision Enhancement를 다시 열지 않는다.

### 5.1 방식

기존 방식 family는 +10 keyword를 만들 때의 맥락으로 재사용할 수 있다.

대표 의미:

```text
BLADE_REINFORCEMENT
IMPACT_ABSORPTION
LIGHTWEIGHT
BALANCE_ADJUSTMENT
ARTISTIC_FINISH
ENVIRONMENTAL_TREATMENT
```

각 방식은 주요 이점과 trade-off를 갖고, 고객 context와 실제 관련될 때만 causal reason이 된다.

### 5.2 촉매 / keyword

촉매는 기존 `CATALYST_AFFIX` 한 슬롯의 keyword 결과를 위한 입력이다.

```text
CATALYST_SELECTED
!= CUSTOMER_BONUS_GRANTED

ITEM_KEYWORD
= player-facing representation of the single CATALYST_AFFIX owner
```

촉매 선택만으로 고객 성공률을 올리지 않는다. 실제 생성된 keyword/기능이 현재 고객 상황과 관련될 때만 원인으로 소비한다.

### 5.3 Precision preview

`Best` 대신 다음을 설명한다.

```text
이번 의뢰에 직접 도움
Gate 변화
trade-off
이번 의뢰에 직접 관련 없음
```

정확 keyword 결과를 성공 전 확정적으로 보장하지 않는다.

## 6. 고객 사건에서의 강화 레벨 기여

Decision24의 첫 테스트 Budget은 이번 구조 변경으로 자동 폐기하지 않는다.

```text
ENHANCEMENT_EVENT_BONUS_PP
= round(0.30 * enhancement_level)
MIN = 0pp
MAX = 30pp at +100
```

상태:

```text
USER_APPROVED_TEST_BUDGET
NOT_FINAL_PRODUCT_BALANCE
```

이 수치는 `damage probability`와 별개다. 고객 사건 성공/결과 추정과 item damage roll을 한 opaque score로 합치지 않는다.

## 7. 고객 장비 판단 계층

작품 선택 후 우선순위:

```text
1. HARD GATE
2. ENHANCEMENT CONTRIBUTION
3. RELEVANT ITEM KEYWORD / FUNCTION / PRECISION CONTEXT
4. SMALL CUSTOMER ABILITY / PROFICIENCY CONTEXT
```

`OVERWEIGHT` 또는 explicit required function 미충족이면 먼저 `배정 불가`를 표시한다.

한도 이내이면 필요할 때 `약 N%`와 핵심 원인 2~4개를 표시할 수 있다. universal fit score는 만들지 않는다.

## 8. Delayed result는 다중 축

Nadia 기존 결과축을 유지한다.

```text
EXPEDITION_RETURN_STATE
RECOVERY_STATE
ITEM_UID_LIFECYCLE_STATE
```

결과에는:

```text
RESULT_AXES
+ CAUSAL_REASONS 2~4
+ SAME UID
+ PRIMARY_NEXT_ACTION 1
```

을 제공한다.

기존 `VSContentResultRecord`는 `content_id/customer_id/item_refs/result_axes/causal_reasons/primary_next_action` 구조의 reuse evidence다. Decision26의 damage mutation runtime 증거는 아니다.

## 9. Customer/world-event damage · Decision26

고객이 작품을 구매/인계받았다고 자동 손상하지 않는다.

```text
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
```

그러나 delayed event에서 실제 장비 사용이 발생하면, 그 event가 damage-eligible한 경우 same UID damage가 한 단계 악화될 수 있다.

```text
CUSTOMER_HANDOFF_OR_PURCHASE
-> PERSONAL_SCHEDULE / DELAYED_EVENT
-> event resolution
-> if EVENT_DAMAGE_ELIGIBLE:
     optional damage roll / deterministic causal result
-> if triggered:
     NORMAL -> MINOR
     MINOR -> MAJOR
     MAJOR -> DESTROYED
```

불변:

```text
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE
NO_AUTOMATIC_PURCHASE_DAMAGE
NO_UNIVERSAL_CUSTOMER_DAMAGE_PERCENT
```

정확 event eligibility, 확률, deterministic cause 목록은 아직 미승인이다.

```text
CUSTOMER_EVENT_DAMAGE_POLICY = CONTENT_OWNER_DECISION_REQUIRED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
```

같은 event에서 하나의 damage event가 두 단계를 건너뛰지 않는다.

## 10. Damage가 발생한 결과 설명

실제 고객/world event에서 damage가 발생하면 결과의 causal reason에 사건 원인을 포함한다.

예시 의미:

```text
유적 붕괴 충격으로 작품 상태가 NORMAL -> MINOR로 악화됨
```

이 문구는 사건 data가 실제로 그러한 원인을 제공할 때만 사용할 수 있다. 존재하지 않는 사건/위험을 AI가 만들어내지 않는다.

파괴가 발생하면:

```text
CUSTOMER != DESTROYED
ITEM_UID = DESTROYED
```

고객 identity/관계는 유지하고, 같은 physical UID는 부활하지 않는다. Archive/Memorial/optional new-UID successor 원칙을 따른다.

## 11. Chronicle 연결

고객 handoff, 실제 world consequence, event damage는 의미 있는 작품 생애 사건이므로 Chronicle 후보다.

```text
OWNER_OR_CUSTOMER_HANDOFF
CUSTOMER_WORLD_CONSEQUENCE
DAMAGE_STATE_CHANGED_BY_CUSTOMER_WORLD_EVENT
DESTROYED_BY_CUSTOMER_WORLD_EVENT
```

반대로 `+6 성공 / N일 전` 같은 routine enhancement attempt는 player-facing Chronicle에 넣지 않는다.

내부 game-day / event sequence는 delayed result causality를 위해 유지할 수 있다.

## 12. 첫 10분과 delayed result 분리

첫 10분:

```text
Nadia starter order
-> first item
-> +9 -> +10 Precision Keyword
-> STOP or +11 PUSH
-> 살아 있고 배정 가능하면 handoff
-> Nadia가 실제 장점/대가 1~2개 acknowledgement
-> personal schedule 활성화
```

전체 world result와 event damage는 이후 실제 일정에서 해결한다. 첫 세션용 가짜 즉시 탐사결과나 자동 damage를 만들지 않는다.

## 13. 사전/사후 UI 경계

### Handoff 전

필요 정보:

```text
hard gate
강화 레벨 기여
관련 keyword / function
trade-off
```

모든 고객 카드에 universal damage risk percent를 추가하지 않는다.

### Event 결과 후

실제 damage가 발생했을 때:

```text
same item UID
before damage state
actual event cause
after damage state
next action
```

을 읽을 수 있게 한다.

## 14. 금지

```text
+20/+30/+40/+50 Precision Enhancement 재도입
fourth keyword/affix slot 생성
촉매 선택 자체를 고객 bonus로 사용
구매 즉시 자동 손상
모든 customer event를 damage event로 처리
damage를 숨은 universal fit score에 합산
한 damage event에서 두 단계 이상 악화
CURRENT/MAX를 customer lifecycle damage의 숨은 authority로 재도입
```

## 15. Remaining gates

```text
DAMAGE_PROBABILITY_CURVE
CUSTOMER_EVENT_DAMAGE_POLICY
MINOR_MAJOR_REPAIR_MODEL
MAJOR_ENHANCEMENT_ELIGIBILITY
```

특히 customer event damage 확률을 enhancement damage curve에서 자동 복사하지 않는다. 서로 다른 원인 owner다.

## 16. Evidence boundary

```text
DECISION24_CAUSAL_STRUCTURE = USER_APPROVED
DECISION25_PRECISION_REFINEMENT = USER_APPROVED
DECISION26_CUSTOMER_EVENT_DAMAGE_HOOK = USER_APPROVED_STRUCTURE
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
RUNTIME_CUSTOMER_EVENT_DAMAGE = NOT_RUN / BLOCKED
HUMAN_PLAYER = NOT_RUN
```
