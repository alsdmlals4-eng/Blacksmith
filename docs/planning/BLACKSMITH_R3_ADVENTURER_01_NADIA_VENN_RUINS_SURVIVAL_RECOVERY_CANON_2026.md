# Blacksmith R3–R7 모험가 01 — 나디아 벤 유적 탐사 생환·회수 정본

- Decision ID: `BS-CONTENT-20260811-01`
- 상태: `USER_APPROVED / R3_R7_1_OF_10 / PENDING_MERGE`
- Content ID: `ADVENTURER_01`
- Customer ID: `NADIA_VENN`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`

## 1. 승인된 방향

첫 상세 모험가 콘텐츠는 **나디아 벤의 유적 탐사에서 생환 + 회수를 함께 노리는 개인 일정**으로 고정한다.

나디아는 기존 Sheet에 등록된 모험가 유형 대표 고객·유적 탐사대장이다. 대담하지만 무모함 자체를 목표로 삼지 않고, 범용성·경량·생존성을 중시한다. 플레이어는 나디아를 직접 조종하거나 유적을 직접 탐험하지 않는다. 대장장이로서 고객의 목적과 위험을 읽고 자신이 만든 작품 가운데 어떤 한 점을 맡길지 결정한다.

```text
고객 대화로 목적·위험 파악
→ 작품 한 점 선택·인계
→ 개인 일정 활성화
→ 하루 종료마다 최대 한 번 진행
→ 탐사 중간 상태와 회수 시도
→ 생환·회수·작품 상태 결과
→ 같은 UID의 흔적·연대기·복원·후속 강화 이유
```

핵심 판타지는 `퀘스트를 대신 플레이한다`가 아니라 **내가 만든 작품이 세계에서 실제로 쓰이고 돌아와 다음 제작 판단을 만든다**이다.

## 2. 상속하는 정본

이 Decision은 새 고객 시스템을 만들지 않고 다음 승인 계약을 구체 콘텐츠로 소비한다.

- `BS-CONTENT-20260804-01`: 고객 결과·작품 UID 상태·다음 제작/복원 환류
- `BS-CONTENT-20260804-02`: 모험가의 탐사·개척 가족과 유실·회수 작품 생애
- `BS-WORLD-20260803-03`: 개인 일정은 고객 방문+판매/납품으로 활성화되고 활성 중 하루 종료마다 최대 한 번 진행
- `BS-CUSTOMER-20260803-02`: 사건 위험도·고객 능력치 `1~10`, 예상 성공률 `5~95%`의 대략적 공개
- `BS-CUSTOMER-20260806-01`: 강화가 일반 사건 성공률의 주효과이며 중량 초과는 배정 불가
- `BS-UX-20260805-01`: 장비 선택 후 핵심 원인 `2~4개`를 설명
- `BS-CORE-20260803-04`: 행동 증거와 중립적 회상 인터뷰를 함께 사용

충돌 시 위 상속 정본과 `CURRENT_CONFIRMED_DECISIONS.md`, `CURRENT_R2_CANON_REGISTRY.json`을 우선한다.

## 3. 고객과 상황

### 나디아 벤

```yaml
customer_id: NADIA_VENN
name: 나디아 벤
archetype: ADVENTURER
role: 유적 탐사대장
values:
  - 범용성
  - 경량
  - 생존성
  - 회수 가능성
```

나디아의 기본 요구는 특정 이름의 전설 무기나 고정 장비 정답이 아니다. 유적 내부의 불확실한 위험 속에서 탐사대를 무사히 돌아오게 하고, 탐사의 목표물을 가능한 범위에서 회수하는 것이다.

회수 대상의 정확한 이름·희귀도·가격·세계관 고유명사는 `CONTENT_INSTANCE_DATA`가 소유한다. `ADVENTURER_01` 전역 정본에 특정 유물 하나를 영구 고정하지 않는다.

## 4. 플레이어의 핵심 선택

플레이어는 작품 한 점을 인계하기 전에 세 축을 함께 본다.

```text
1. ENHANCEMENT_LEVEL_AND_RISK
2. WEIGHT_AND_CUSTOMER_FIT
3. ENVIRONMENTAL_OR_UTILITY_FIT
```

### 4.1 강화 단계

- 일반 사건 성공률에서는 강화 단계가 주효과다.
- 더 높은 강화 작품을 맡기면 유리할 수 있지만, 그 작품을 위험에 노출하는 기회비용도 커진다.
- 강화 단계만 높으면 모든 유적 상황에서 자동 최적이 되는 구조는 금지한다.

### 4.2 중량·고객 적합

- `MAXIMUM_LOAD = STRENGTH × 10` 계약을 유지한다.
- 중량 초과 작품은 배정할 수 없다.
- 한도 이내라는 이유만으로 추가 성공 보너스를 주지 않는다.
- 적성·관련 능력은 강화보다 작은 보조 판단으로 남는다.

### 4.3 환경·유틸리티 적합

- 유적 상황과 실제로 연결되는 승인된 특수기능만 설명 가능한 보조 근거로 사용할 수 있다.
- 존재하지 않는 기능이나 미승인 촉매를 가용한 것처럼 표시하지 않는다.
- 작품 공격·방어·예술성 원수치를 모든 탐사 결과에 범용 합산하지 않는다.

### 4.4 단일 정답 금지

`single_always_best_equipment_answer = false`.

좋은 선택은 상황과 보유 작품에 따라 달라져야 한다. 예를 들어 강화가 높은 무거운 작품, 강화는 낮지만 가벼운 작품, 상황에 맞는 승인 유틸리티를 가진 작품이 서로 다른 장단점을 가질 수 있다. 이 예시는 구조 설명이며 정확한 수치 우열은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 5. 개인 일정 구조

이 콘텐츠는 `PERSONAL_SCHEDULE`이다.

```text
activation = CUSTOMER_VISIT_PLUS_EQUIPMENT_HANDOFF
progression = ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE
```

직접 전투·탐험 미니게임을 추가하지 않는다.

### 구조 상태

```text
PREP_AND_ENTRY
→ HAZARD_AND_RECOVERY_ATTEMPT
→ RETURN_AND_RESULT
```

이 세 상태는 **정확히 3일**이라는 뜻이 아니다. 한 상태가 여러 날짜에 걸릴 수 있고, 콘텐츠 조정에 따라 진행 길이가 바뀔 수 있다.

```yaml
UNIVERSAL_FIXED_DAY_COUNT: false
EXACT_DURATION: BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED
```

모든 개인 일정에 고정 3일 결과·4일 재방문을 재도입하지 않는다.

## 6. 결과 축

결과를 하나의 성공/실패 점수로 압축하지 않고 세 축으로 나눈다.

```text
EXPEDITION_RETURN_STATE
RECOVERY_STATE
ITEM_UID_LIFECYCLE_STATE
```

### 6.1 탐사대 귀환

기본 표현은 다음처럼 비치명적 결과를 우선한다.

```text
SAFE_RETURN
FORCED_RETREAT
```

고객 사망·영구 이탈·대규모 인명 손실은 이 첫 콘텐츠의 기본 정답으로 자동 확정하지 않는다. 그런 결과가 필요해지면 세계관·관계·콘텐츠 비용을 포함한 별도 Decision으로 다룬다.

### 6.2 회수

```text
RECOVERED
PARTIAL_RECOVERY
ABANDONED
```

회수 성공은 단순 골드 보너스가 아니라 다음 제작·재료·세계 정보·후속 의뢰의 이유가 될 수 있다. 정확한 보상량과 희귀도는 현재 확정하지 않는다.

### 6.3 같은 UID의 작품 상태

허용되는 대표 결과 예시는 다음이다.

```text
RETURNED_WITH_TRACES
DAMAGED_UID_PRESERVED
MAJOR_DAMAGED_UID_PRESERVED
LOST_PENDING_RECOVERY
RECOVERED_SAME_UID
```

- 손상·대파가 발생해도 같은 UID와 기존 생애를 유지한다.
- 분실은 삭제가 아니라 후속 회수 가능 상태가 될 수 있다.
- 완전 소실은 별도 명시적 고위험 선택이 있을 때만 허용하는 기존 경계를 유지한다.
- 이 콘텐츠의 baseline은 자동 영구 파괴를 요구하지 않는다.

## 7. 즉시 피드백과 지연 생애 피드백

### 즉시 결과

결정적 결과가 확정되면 짧은 인과 결과를 보여준다.

- 무엇이 일어났는가
- 나디아의 능력·적성이 어떤 보조 역할을 했는가
- 맡긴 작품의 강화·중량·관련 기능이 어떤 영향을 줬는가
- 왜 생환·회수·철수 결과가 나왔는가

장비 선택 후 판단층과 결과 화면에서 핵심 원인은 `2~4개`로 제한한다.

```text
SHORT_CAUSAL_RESULT_WITH_2_TO_4_REASONS
```

### 지연 생애 결과

후일 재방문이나 관련 일정에서 같은 UID의 상태를 다시 확인한다.

```text
SAME_UID_REVISIT
→ REPAIR / RESTORE / FOLLOWUP_ENHANCEMENT / NEW_CRAFT_REASON
```

플레이어에게 필요한 것은 단순한 성공 보상보다 **왜 이 작품을 다시 만지고 싶은가**이다.

## 8. 연대기·수식어·예술성 경계

일정 하나가 끝났다는 이유만으로 연대기 수식어를 자동 지급하지 않는다.

```yaml
CHRONICLE_AFFIX_AUTO_GRANT: false
ARTISTRY_AUTO_GROWTH: false
```

- 의미 있는 실제 사용·기여·손상·복원·소유 변화는 UID 연대기에 기록할 수 있다.
- 연대기 수식어 생성·진화는 기존 `CHRONICLE_AFFIX` 책임 규칙을 따른다.
- 사건 참여 횟수 채우기만으로 수식어를 지급하지 않는다.
- 일반 강화·판매·회수·귀환 자체가 예술성 원수치를 자동 증가시키지 않는다.
- 같은 원인을 예술성·촉매·연대기·가격에 중복 계산하지 않는다.

## 9. 모바일 정보 공개

### 고객 기본 카드

- 나디아의 역할과 탐사 목적
- 근력·기량·체력·판단력
- 해당 작품 선택과 관련된 적성만
- 사건 위험도와 대략적 예상 성공률

### 작품 선택 후 판단층

- 배정 가능/중량 초과
- 대략적 예상 성공률
- 핵심 원인 `2~4개`
- 실제 관련이 있을 때만 특수기능 적합 근거

### 상세 보기

전체 계산 근거·관련 적성·중량·기능 조건을 필요할 때 확인한다.

색상·호버·길게 누르기만으로 핵심 정보를 전달하지 않는다.

## 10. 플레이테스트 가설

이 Decision은 제품 구현 승인이 아니다. 이후 승인된 playable scope가 생기면 다음을 관찰한다.

### 행동 증거

1. 플레이어가 나디아의 목적을 읽고 작품 선택 이유를 말하기 전에 실제로 서로 다른 작품을 비교하는가.
2. 단순히 가장 높은 강화 숫자만 고르지 않고 중량·적합·상황 기능을 확인하는가.
3. 결과 뒤 어떤 요인이 생환·회수에 영향을 줬는지 설명할 수 있는가.
4. 돌아온 작품을 같은 UID로 기억하고 복원·추가 강화·보존 중 하나를 고민하는가.
5. 실패·부분 성공 뒤 바로 새 작품으로 버리지 않고 기존 작품 생애를 후속 판단에 사용하려는가.

### 중립적 회상 질문

- “어떤 정보를 보고 그 작품을 골랐나요?”
- “결과가 그렇게 나온 가장 큰 이유는 무엇이라고 생각하나요?”
- “이 작품을 다음에 어떻게 하고 싶나요?”

플레이어가 좋다고 말하는지만 묻지 않는다. 행동과 회상이 충돌하면 PASS를 보류한다.

## 11. 인터넷 벤치마킹 — SOURCE_CONTEXT_PACKET

### 11.1 Potion Craft: Alchemist Simulator

```yaml
source_domain: GAME_DEVELOPMENT
source_role: PRODUCT_REFERENCE
source_surface: Steam product page
observed_fact: 고객이 문제 해결을 위해 상점을 방문하며 무엇을 판매하는지에 따라 후속 결과가 달라진다.
judgment: ADAPT
apply_to_blacksmith: 고객 문제 → 제작품 선택 → 결과 인과를 읽을 수 있게 한다.
do_not_copy: 특정 요구에 대한 단일 정답 레시피 매칭 구조를 Blacksmith 장비 선택에 강제하지 않는다.
```

Blacksmith 차별점은 고객 거래 순간에 끝나지 않고 같은 UID의 지연 생애 결과가 복원·강화 판단으로 되돌아오는 것이다.

### 11.2 Crusader Kings III — Dev Diary #85: An Artifact’s Life

```yaml
source_domain: GAME_DEVELOPMENT
source_role: PROFESSIONAL_PRACTICE_OFFICIAL_DEV_DIARY
observed_fact: Artifact를 세계에서 사용·교환·손상되는 살아 있는 물건으로 다루고 시간이 지나며 평판과 이야기를 얻도록 설계했다.
judgment: ADAPT
apply_to_blacksmith: 같은 UID가 사용 흔적·이력·평판성 연대기를 쌓아 기억되는 구조를 강화한다.
do_not_copy: 반복 내구도 유지·주기적 수리 관리 자체를 Blacksmith 코어로 만들지 않는다.
```

Blacksmith의 손상·복원은 관리 세금이 아니라 다음 강화·복원의 선택 이유여야 한다.

### 11.3 Games User Research

```yaml
source_domain: GAME_USER_RESEARCH
source_role: PROFESSIONAL_PRACTICE
observed_fact: 관찰은 실제 행동을 보여주지만 동기는 불명확할 수 있고, 인터뷰는 이유를 이해하는 데 도움이 되므로 방법을 결합하는 것이 유용하다.
judgment: ADOPT
apply_to_blacksmith: 작품 선택 행동 + 결과 원인 회상을 함께 본다.
do_not_copy: 설문 만족도 하나로 재미·이해·인과를 통과시키지 않는다.
```

## 12. 적대적 검토

### 공격 1 — “결국 가장 강화 높은 장비가 정답 아닌가?”

판정: `MUST_FIX_BY_CONTRACT`.

강화는 주효과지만 중량 배정 가능 여부와 실제 상황 기능은 별도 Gate다. 모든 상황에서 하나의 작품이 자동 최적이면 콘텐츠 선택이 사라진다. 다만 보조 요소가 강화 중심성을 뒤집는 복잡한 RPG 계산으로 팽창해서도 안 된다.

### 공격 2 — “모험가 콘텐츠가 별도 던전 게임으로 커질 수 있다.”

판정: `REJECTED_BY_BOUNDARY`.

직접 전투·탐험 미니게임을 추가하지 않는다. 플레이어의 역할은 대장장이의 정보 판독·작품 배정·후속 복원 판단이다.

### 공격 3 — “모든 일정이 다시 3일 구조로 고정된다.”

판정: `MUST_NOT_REINTRODUCE`.

세 구조 상태와 실제 날짜 수를 분리한다. 활성 개인 일정은 하루 종료당 최대 한 번 진행하지만 정확한 기간은 테스트 프리셋이다.

### 공격 4 — “일정 하나만 돌면 연대기 수식어와 예술성이 자동 성장한다.”

판정: `MUST_NOT_REINTRODUCE`.

UID 연대기 기록과 수식어/예술성 성장을 분리한다. 의미 있는 사건과 승인된 성장 원천만 사용한다.

### 공격 5 — “생환+회수라는 두 목표 때문에 결과 화면이 과밀해진다.”

판정: `SHOULD_FIX_IN_UX`.

귀환·회수·작품 상태는 내부적으로 분리하되 기본 결과 화면은 핵심 원인 2~4개와 다음 행동 하나를 우선한다. 전체 세부는 상세 보기로 보낸다.

### 공격 6 — “부분 성공이 사실상 벌점만 남기면 플레이어가 작품을 아끼지 않게 된다.”

판정: `TEST_REQUIRED`.

부분 성공·손상은 복원·후속 강화·회수의 새 목표를 만들 수 있어야 한다. 정확한 손실량·복구 비용은 사람 플레이테스트 전 확정하지 않는다.

## 13. 보호 경계

```text
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
DIRECT_COMBAT_OR_EXPLORATION_MINIGAME: FORBIDDEN_BY_THIS_DECISION
SAME_ITEM_UID_LIFECYCLE: REQUIRED
UNIVERSAL_FIXED_DAY_COUNT: false
SINGLE_ALWAYS_BEST_EQUIPMENT_ANSWER: false
CHRONICLE_AFFIX_AUTO_GRANT: false
ARTISTRY_AUTO_GROWTH: false
EXACT_VALUES: BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED
```

이 Decision은 R3–R7 기획 재개를 승인하지만 Godot Scene·Resource·project.godot·제품 Script/Data 작성 권위를 새로 열지 않는다.

## 14. 다음 상세화 지점

이 콘텐츠 안에서 추가 사용자 Decision 없이 세부 작업안으로 진행 가능한 것은 다음이다.

- 나디아 고객 카드의 정보 계층 초안
- 결과 화면의 귀환·회수·작품 상태 정보 계층
- 테스트 프리셋 후보값의 **비정본** fixture 설계
- 행동 관찰 체크리스트와 중립적 회상 질문

다음 신규 Decision으로 올려야 하는 것은 프로젝트 방향을 바꾸는 항목뿐이다.

- 고객 사망·영구 이탈을 기본 결과로 도입
- 별도 직접 탐험/전투 플레이 추가
- 일반 콘텐츠 전체에 고정 일정 일수 도입
- 기존 성공률·중량·수식어 계약 변경
- Task3 또는 일반 제품 구현 Gate 개방
