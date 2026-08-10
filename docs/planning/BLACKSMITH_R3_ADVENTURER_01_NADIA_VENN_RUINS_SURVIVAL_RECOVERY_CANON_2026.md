# Blacksmith R3–R7 모험가 01 — 나디아 벤 유적 탐사 생환·회수 정본

- Decision ID: `BS-CONTENT-20260811-01`
- 상태: `USER_APPROVED / R3_R7_1_OF_10 / MERGED_PR142_MAIN_CANON`
- 승인 main: `13f878589b4849defb97d2c4509e7bf50bcb507d`
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

## 9. 모바일 정보 공개 — 나디아 상세 계약

이 상세화는 `BS-UX-20260805-01`의 3단계 구조를 Nadia 콘텐츠에 그대로 적용한다. 새 고객 UI 시스템을 만들지 않는다.

```text
DEFAULT_CUSTOMER_CARD
→ POST_EQUIPMENT_DECISION_LAYER
→ DETAIL_VIEW
```

### 9.1 기본 고객 카드 — `DEFAULT_CUSTOMER_CARD`

항상 보이는 정보는 인계 판단에 직접 필요한 것만 둔다.

- `NADIA_VENN / 나디아 벤`과 `유적 탐사대장` 역할
- 현재 목적: `유적 탐사 — 생환 + 회수`
- 알려진 사건 위험도 `1~10`
- 근력·기량·체력·판단력 `1~10`
- 현재 탐사와 실제로 관련된 주·보조 적성만
- 현재 선택 작품이 없을 때도 명확한 주 행동 `작품 선택`

전체 적성 행렬, 내부 보정식, 숨은 위험 경고, 아직 발생하지 않은 결과 스포일러는 기본 카드에 펼치지 않는다. 핵심 상호작용 목표는 최소 `48dp`이며 색상·호버·길게 누르기만으로 상태나 행동을 전달하지 않는다.

### 9.2 작품 선택 후 판단층 — `POST_EQUIPMENT_DECISION_LAYER`

작품을 고르면 같은 판단 맥락에서 다음 정보를 갱신한다.

```text
LOAD_GATE_THEN_ENHANCEMENT_THEN_RELEVANT_UTILITY_THEN_SMALL_CUSTOMER_CONTEXT
```

우선순위는 다음과 같다.

1. **배정 가능 여부** — `WITHIN_LIMIT / OVERWEIGHT`, 현재 중량 / 최대 중량
2. **강화 단계** — 일반 사건 성공률의 주효과
3. **실제 관련 환경·유틸리티 적합** — 현재 유적 상황에 연결되는 승인 기능만
4. **고객 능력·적성 맥락** — 강화보다 작은 보조 원인

`OVERWEIGHT이면 예상 성공률보다 배정 불가를 우선한다`. 중량 초과 작품에는 행동 가능한 성공률을 강조하지 않고 `배정 불가 / 중량 초과`와 원인을 먼저 보여준다. 한도 이내 작품은 기존 공개 계약에 따라 `약 N%`와 선택 전후 방향을 보여주고, 핵심 원인 `2~4개`를 함께 표시한다.

- 선택 작품의 이름·같은 UID 식별자·강화 단계·중량을 확인할 수 있다.
- 실제 관련 기능이 없으면 기능 적합 칸을 억지로 채우지 않는다.
- `자동 추천·Best 배지 금지`. 하나의 녹색 정답·자동 추천·불투명 종합점수로 선택을 대신하지 않는다.
- `이 작품을 맡긴다`가 주 행동이며 `OVERWEIGHT`에서는 비활성 이유를 텍스트로 설명한다.
- `다른 작품 보기`로 교체할 수 있지만 기본 화면에 전체 작품 비교 행렬을 강제하지 않는다.

### 9.3 상세 보기 — `DETAIL_VIEW`

한 개의 명확한 상세 진입점에서만 다음을 확장한다.

- 현재 판단에 관련된 전체 능력·적성
- 현재 중량 / 최대 중량
- 선택 작품의 실제 적용 기능과 활성 조건
- 공개 가능한 예상 성공률 원인
- 작품 UID·제작 provenance·관련 생애 기록

내부 RNG 식, 숨은 사건 전개, 미래 결과는 공개하지 않는다. 상세에서 돌아오면 선택 작품과 현재 판단 맥락을 유지한다.

### 9.4 결과 화면 정보 계층

결과는 내부적으로 세 축을 유지하지만 첫 화면을 세 개의 상세 보고서로 만들지 않는다.

```text
THREE_STATE_SUMMARY_TWO_TO_FOUR_REASONS_ONE_PRIMARY_NEXT_ACTION
```

기본 결과 화면 순서:

1. `나디아 귀환` — `SAFE_RETURN / FORCED_RETREAT`
2. `회수` — `RECOVERED / PARTIAL_RECOVERY / ABANDONED`
3. `작품 상태` — 같은 UID와 `RETURNED_WITH_TRACES / DAMAGED_UID_PRESERVED / MAJOR_DAMAGED_UID_PRESERVED / LOST_PENDING_RECOVERY / RECOVERED_SAME_UID` 중 현재 상태
4. 핵심 인과 원인 `2~4개`
5. 현재 상태에 맞는 **주 다음 행동 하나** — 복원, 후속 강화, 회수 단서 확인, 또는 새 제작 이유 중 해당하는 것

같은 UID임을 결과 상단에서 분명히 보이게 하고, 연대기 세부·전체 원인·소유/손상 이력은 하나의 상세 진입점으로 보낸다. 결과 화면에서 성공/실패 하나의 총점이나 자동 다음 행동을 강요하지 않는다.

## 10. 비정본 테스트 프리셋·플레이테스트 계약

이 Decision은 제품 구현 승인이 아니다. 아래 숫자·fixture는 밸런스 정본이 아니라 선택 구조를 검증하기 위한 폐기 가능한 시험 입력이다.

```yaml
fixture_status: NON_CANONICAL_BASELINE_TEST_FIXTURE
canonical_balance: false
product_data_authority: NONE
playtest_evidence: OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL
```

### 10.1 비정본 fixture 후보

한 번의 테스트 세션에서 최소 세 작품 후보가 서로 다른 이유를 갖도록 구성한다.

- `FIXTURE_A_HIGH_ENHANCEMENT_HEAVY`: 강화가 높지만 현재 테스트 프로필에서는 중량 Gate를 넘길 수 있는 작품
- `FIXTURE_B_BALANCED_WITHIN_LOAD`: 중간 강화·중량 한도 이내의 일반 후보
- `FIXTURE_C_CONTEXT_UTILITY`: 강화는 더 낮을 수 있지만 현재 유적 상황과 실제로 연결되는 승인 유틸리티를 가진 후보

실제 승인 기능을 확정하지 못한 fixture에서는 새 기능명을 만들지 않고 `APPROVED_RELEVANT_UTILITY_PLACEHOLDER`를 사용한다. 이 토큰은 제품 기능이 아니라 **현재 정본에서 승인된 실제 관련 유틸리티를 테스트 준비 시 대입하라는 자리표시자**다.

사건 위험도·나디아 능력치·정확한 예상 성공률·보상·손상·복구 비용은 테스트 세션별 `BASELINE_TEST_PRESET`으로 기록하며 제품 정본으로 승격하지 않는다. 예상 성공률 표시는 기존 `약 N% / 10% 단위 / 5~95%` 공개 계약을 따른다.

### 10.2 행동 관찰

다음 행동을 실제 화면 조작에서 관찰한다.

1. 인계 전에 서로 다른 작품을 최소 두 개 이상 비교하는가.
2. 강화 숫자 외에 중량 또는 실제 관련 환경·유틸리티 근거를 한 번 이상 확인하는가.
3. `약 N%`를 확정 성공으로 취급하지 않는가.
4. `OVERWEIGHT`를 높은 강화보다 우선하는 배정 불가 Gate로 이해하는가.
5. 결과 뒤 같은 UID의 작품을 알아보고 복원·후속 강화·보존·새 제작 중 다음 행동을 고민하는가.
6. 여러 작품을 오갈 때 반복 탭·뒤로가기가 과도해지는지 기록하되, 이 관찰만으로 즉시 전체 비교 행렬을 추가하지 않는다.

### 10.3 중립적 회상 질문

- “어떤 작품을 맡겼나요?”
- “결정할 때 무엇을 봤나요?”
- “결과에 가장 영향을 준 것은 무엇이라고 생각하나요?”
- “돌아온 작품은 이전 작품과 어떤 관계인가요?”
- “다음에 무엇을 하고 싶나요? 왜인가요?”

질문에서 정답 원인이나 기대 행동을 먼저 말하지 않는다. 만족도·`재미있었나요?` 하나만으로 PASS하지 않는다. 관찰 행동과 회상이 충돌하면 이해·인과 PASS를 보류한다.

### 10.4 판정 Gate

```text
OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL
→ KEEP / CHANGE / RETEST
```

- 여러 플레이어가 자동으로 최고 강화만 고르면 `CHANGE / RETEST`.
- 중량 Gate를 성공률보다 하위 정보로 해석하면 `CHANGE`.
- 결과 3축을 구분하지 못하거나 같은 UID를 새 작품으로 오해하면 `CHANGE / RETEST`.
- 정확한 수치 조정은 구조 이해가 확보된 뒤 별도 테스트 프리셋에서 수행한다.

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

### 11.4 Android 접근성·터치 목표

```yaml
source_domain: ANDROID_DEVELOPERS_ACCESSIBILITY
source_role: PROFESSIONAL_PRACTICE_OFFICIAL
observed_fact: 모바일 상호작용은 충분한 터치 목표를 제공하고 핵심 행동을 숨은 제스처에만 의존시키지 않는 것이 권장된다.
judgment: ADOPT_AS_SUPPORT
apply_to_blacksmith: 기존 `48dp` 계약과 명시적 작품 선택·상세 진입점을 유지한다.
do_not_copy: 플랫폼 일반 규칙을 이유로 Blacksmith 정보 계층을 확장하거나 별도 UI 시스템을 만들지 않는다.
```

### 11.5 Xbox 접근성 — UI context·readability

```yaml
source_domain: XBOX_ACCESSIBILITY_GUIDELINES
source_role: PROFESSIONAL_PRACTICE_OFFICIAL
observed_fact: 사용자가 화면 목적, 요소 기능, 상호작용 결과를 이해할 수 있는 맥락과 읽기 쉬운 UI가 중요하다.
judgment: ADAPT
apply_to_blacksmith: `배정 가능 여부 → 강화 → 관련 기능 → 고객 맥락`의 이유 순서와 결과의 다음 행동을 텍스트로 설명한다.
do_not_copy: 자동 추천·Best 표식으로 판단 자체를 대신하지 않는다.
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

위 네 상세화 항목은 이 same-ID refinement에서 완료했다. 다음 반복에서는 실제 playable scope가 승인된 뒤 **비정본 fixture를 실행해 관찰·회상 증거를 수집**하거나, 별도 프로젝트 방향 Decision이 필요한 항목으로 이동한다.

다음 신규 Decision으로 올려야 하는 것은 프로젝트 방향을 바꾸는 항목뿐이다.

- 고객 사망·영구 이탈을 기본 결과로 도입
- 별도 직접 탐험/전투 플레이 추가
- 일반 콘텐츠 전체에 고정 일정 일수 도입
- 기존 성공률·중량·수식어 계약 변경
- Task3 또는 일반 제품 구현 Gate 개방
