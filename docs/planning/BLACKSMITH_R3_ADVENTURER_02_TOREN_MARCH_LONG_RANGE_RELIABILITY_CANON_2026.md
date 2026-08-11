# Blacksmith R3–R7 ADVENTURER_02 — 토렌 마치 장거리 여정 지속성·신뢰성 정본

- Decision ID: `BS-CONTENT-20260811-02`
- Content ID: `ADVENTURER_02`
- Customer ID: `TOREN_MARCH`
- 상태: `USER_APPROVED / R3_R7_2_OF_10 / PLANNING_ONLY`
- 단계: `R3_R7_CONTENT_DESIGN / PLAN_REVIEW`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`
- 기준 main: `cb5ceff127bf4f2adb38b34ebaa092d97111fa94`
- 기준 Base: `315c66eea9614c284b9c11c4d522141065dfa4b0`

## 1. 설계 목적

`ADVENTURER_02`는 나디아의 유적 탐사 콘텐츠를 이름만 바꿔 반복하지 않는다. 토렌 마치는 장거리 길잡이로서 **장거리 이동과 환경 변화 속에서 작품이 얼마나 계속 쓸 수 있는 상태로 기능하는가**를 검증한다.

핵심 판타지는 다음과 같다.

```text
여정의 알려진 환경·부담을 읽는다
→ 작품 한 점을 비교·인계한다
→ 토렌이 직접 여정을 수행한다
→ 환경 노출·우회·현장 유지보수 사건이 발생할 수 있다
→ 도착 상태와 같은 UID 작품의 마모·손상·유지보수 흔적을 돌려받는다
→ 수리·복원·후속 강화·다음 여정용 신작 판단으로 연결한다
```

플레이어는 토렌을 직접 조종하거나 지도에서 경로를 찍지 않는다. Blacksmith의 역할은 **여행자가 아니라 장비 판단을 하는 대장장이**다.

## 2. 상속 정본

이 설계는 다음 현재 계약을 소비한다.

- `BS-CONTENT-20260804-01`: 상황→작품 판단→사용 결과→UID 생애→다음 제작 환류
- `BS-CONTENT-20260804-02`: 모험가의 탐사·개척, 장기 활동용 작품, 부식·오염·유실·회수 생애
- `BS-WORLD-20260803-03`: 개인 일정은 고객 방문+판매/납품으로 활성화되고 하루 종료당 최대 한 진행 단위
- `BS-CUSTOMER-20260806-01`: 일반 사건 성공에서는 강화가 주효과, 중량 초과는 배정 불가 Gate
- `BS-ITEM-20260806-04`: 공통 `WEIGHT / DURABILITY / HANDLING / ARTISTRY`, 승인 유틸리티 `ENVIRONMENTAL_SEALING`, `FIELD_SERVICEABILITY`, `TASK_INTEGRATION`
- `BS-UX-20260805-01`: 고객 카드 progressive disclosure, 원인 `2~4개`, 자동 추천 금지
- `BS-CORE-20260803-04`: 관찰 행동 + 중립 회상으로 이해 검증
- `BS-CONTENT-20260811-01`: 같은 모험가 유형에서 직접 탐험 미니게임·고정 일수·자동 Best·일상 사건의 수식어/예술성 자동 지급 금지

충돌 시 위 현재 정본과 `CURRENT_CONFIRMED_DECISIONS.md`, `CURRENT_R2_CANON_REGISTRY.json`, `CURRENT_R3_R7_CANON_REGISTRY.json`을 우선한다.

## 3. 접근안 비교

### A. 여정 지속성·작품 신뢰성 중심 — 채택

- 토렌의 목적을 `JOURNEY_CONTINUITY_AND_RELIABILITY`로 둔다.
- 강화는 일반 성공의 기존 주효과를 유지한다.
- 중량은 배정 가능 여부와 휴대 판단을 만든다.
- `DURABILITY`는 환경 노출 뒤 작품 상태를 설명하는 기존 원수치로 사용한다.
- `ENVIRONMENTAL_SEALING`과 `FIELD_SERVICEABILITY`는 실제 관련 맥락에서만 별도 역할을 한다.
- 여정 자체는 비직접 진행이며 결과가 작품 UID 생애로 돌아온다.

장점: Blacksmith 코어를 유지하면서 Nadia와 다른 작품 생애를 만든다.

### B. 경로 선택 중심 — 비채택

플레이어가 지도에서 경로·우회·쉼터를 직접 선택하는 방향이다. 환경 판단은 선명하지만 대장간 밖 이동 플레이가 길어지고 별도 여행 게임으로 팽창할 위험이 크다.

### C. 수리·유지보수 중심 — 비채택

매 여정마다 내구도 감소와 수리 비용을 핵심 자원 세금으로 만드는 방향이다. 작품이 살아 돌아오는 감각보다 반복 유지보수 의무가 앞설 수 있고, 군인 `현장 수리성` 콘텐츠와도 경계가 흐려진다.

## 4. 고객·상황

```yaml
customer_id: TOREN_MARCH
name: 토렌 마치
archetype: ADVENTURER
role: 장거리 길잡이
values:
  - 실용성
  - 신뢰성
  - 휴대성
  - 수리 용이성
content_goal: JOURNEY_CONTINUITY_AND_RELIABILITY
```

`신뢰성`과 `수리 용이성`은 새 작품 원수치를 만들지 않는다.

- 신뢰성 판단은 현재 `DURABILITY`, 강화, 실제 환경 기능과 결과 이력으로 설명한다.
- 수리 용이성은 `FIELD_SERVICEABILITY`가 있는 작품에서만 기능적 근거가 된다.
- `FIELD_SERVICEABILITY`가 없는 작품에 숨은 `REPAIRABILITY` 수치를 생성하지 않는다.

여정의 정확한 지명·거리·날씨·목적지는 `CONTENT_INSTANCE_DATA`가 소유한다. `ADVENTURER_02` 전역 정본에 특정 도시·노선·기후 하나를 영구 고정하지 않는다.

## 5. 플레이어 선택

플레이어는 작품 한 점을 맡기기 전에 다음을 함께 본다.

```text
1. LOAD_GATE_AND_PORTABILITY
2. ENHANCEMENT_LEVEL_AND_GENERAL_SUCCESS
3. DURABILITY_AND_KNOWN_EXPOSURE
4. APPROVED_CONTEXT_FUNCTION_FIT
```

### 5.1 중량·휴대성

- `MAXIMUM_LOAD = STRENGTH × 10` 계약을 유지한다.
- `OVERWEIGHT`는 배정 불가다.
- 한도 이내의 더 가벼운 작품에 범용 성공 보너스를 자동 지급하지 않는다.
- 토렌의 휴대성 선호는 선택 설명과 기회비용에 쓰되 새 `PORTABILITY` 원수치를 만들지 않는다.

### 5.2 강화

- 일반 사건 성공률의 주효과는 기존대로 강화다.
- 토렌 콘텐츠가 강화의 현재 소유권을 약화하거나 `DURABILITY`를 새 범용 성공 주효과로 승격하지 않는다.

### 5.3 내구도와 환경 노출

- `DURABILITY`는 장거리 노출 뒤 마모·손상 가능성을 설명하는 기존 작품 상태다.
- 내구도가 높다고 모든 일정의 성공률을 자동 증가시키지 않는다.
- 알려진 환경 노출과 실제로 연결될 때만 작품 상태 결과의 주요 원인으로 사용한다.

### 5.4 승인된 기능

#### `ENVIRONMENTAL_SEALING`

- `BOUND_ENVIRONMENT`가 현재 여정의 알려진 환경과 맞을 때만 위험 완화 근거가 된다.
- 완전 면역이나 범용 성공 보너스를 제공하지 않는다.

#### `FIELD_SERVICEABILITY`

- 여정 중 제한된 유지보수 사건이 발생했을 때만 기능한다.
- 완전 복원, 손상 이력 삭제, 무료 수리, 일반 성공률 상시 보너스를 허용하지 않는다.

#### 기타 기능

- 실제 `BOUND_TASK`가 있는 경우 `TASK_INTEGRATION`을 사용할 수 있으나, 장거리 이동 전체를 하나의 범용 task로 묶어 상시 보너스를 주지 않는다.
- 존재하지 않는 기능이나 미승인 기능명을 fixture 편의를 위해 생성하지 않는다.

## 6. 단일 정답 방지

`single_always_best_equipment_answer = false`.

한 테스트 세션에서 서로 다른 작품은 서로 다른 이유를 가져야 한다.

- 높은 강화지만 무겁고 환경 기능이 없는 작품
- 중간 강화·중간 중량·높은 현재 내구도를 가진 작품
- 강화는 낮을 수 있지만 현재 `BOUND_ENVIRONMENT`와 일치하는 `ENVIRONMENTAL_SEALING` 작품
- 또는 `FIELD_SERVICEABILITY`로 현장 유지보수 선택지를 여는 작품

정확한 우열은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`이며 제품 밸런스 정본이 아니다.

## 7. 개인 일정 구조

```text
activation = CUSTOMER_VISIT_PLUS_EQUIPMENT_HANDOFF
progression = ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE
```

구조 상태:

```text
PREP_AND_DEPARTURE
→ EXPOSURE_AND_ROUTE_ADAPTATION
→ ARRIVAL_AND_ITEM_ASSESSMENT
```

이 상태는 정확히 3일을 뜻하지 않는다.

```yaml
UNIVERSAL_FIXED_DAY_COUNT: false
EXACT_DURATION: BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED
```

토렌은 자신의 판단으로 경로 변경·쉼터·현장 유지보수를 수행한다. 플레이어에게 직접 이동·지도 경로 선택·실시간 생존 조작을 요구하지 않는다.

## 8. 결과 축

결과를 단일 성공/실패 점수로 압축하지 않는다.

```text
JOURNEY_ARRIVAL_STATE
ROUTE_EXPOSURE_STATE
ITEM_UID_LIFECYCLE_STATE
```

### 8.1 여정 도착

대표 상태:

```text
ARRIVED_AS_PLANNED
ARRIVED_DELAYED
FORCED_RETURN
```

고객 사망·영구 이탈은 baseline 자동 결과로 두지 않는다.

### 8.2 경로·환경 대응

대표 상태:

```text
ROUTE_STABLE
DETOUR_REQUIRED
SHELTER_OR_FIELD_STOP_REQUIRED
```

이 축은 플레이어가 경로를 직접 조작했다는 뜻이 아니라, 맡긴 작품과 알려진 환경이 토렌의 여정 대응에 어떤 영향을 줬는지 설명하기 위한 결과 축이다.

### 8.3 같은 UID 작품 상태

대표 상태:

```text
RETURNED_SERVICEABLE
RETURNED_WORN
FIELD_MAINTAINED_UID_PRESERVED
DAMAGED_UID_PRESERVED
LOST_PENDING_RECOVERY
RECOVERED_SAME_UID
```

- 모든 여정이 자동 마모를 발생시키지 않는다.
- 마모·손상은 환경 노출·사건과 인과가 있을 때만 결과로 기록한다.
- `FIELD_MAINTAINED_UID_PRESERVED`는 완전 수리가 아니라 현장 유지보수 흔적을 가진 같은 UID다.
- 완전 소실은 별도 명시적 고위험 선택 없이는 baseline에 넣지 않는다.

## 9. 즉시 결과와 후속 환류

즉시 결과는 원인 `2~4개`로 제한한다.

예시 원인 순서:

```text
LOAD_GATE_OR_PORTABILITY
→ ENHANCEMENT
→ MATCHED_ENVIRONMENT_OR_SERVICEABILITY
→ DURABILITY_EXPOSURE
→ SMALL_CUSTOMER_CONTEXT
```

결과 뒤 주 다음 행동은 현재 상태에 맞는 하나를 우선 제안한다.

```text
REPAIR
RESTORE
FOLLOWUP_ENHANCEMENT
CHECK_RECOVERY_LEAD
CRAFT_FOR_NEXT_ROUTE
```

자동으로 행동을 실행하거나 작품을 교체하지 않는다.

## 10. 정보 공개

Nadia에서 확정한 3단계 정보 구조를 재사용한다.

```text
DEFAULT_CUSTOMER_CARD
→ POST_EQUIPMENT_DECISION_LAYER
→ DETAIL_VIEW
```

기본 카드:

- 토렌의 역할·목적
- 알려진 여정 환경·위험
- 관련 능력·적성
- 작품 미선택 기본 예상 성공률 `약 N%`
- 주 행동 `작품 선택`

작품 선택 후:

1. `WITHIN_LIMIT / OVERWEIGHT`
2. 강화 단계와 갱신된 `약 N%`
3. 현재 내구도와 알려진 노출의 관계
4. 실제 일치하는 `ENVIRONMENTAL_SEALING` 또는 `FIELD_SERVICEABILITY`
5. 핵심 원인 `2~4개`

- 자동 추천·Best 배지·불투명 종합점수 금지
- 기능이 실제 관련 없으면 해당 줄을 억지로 채우지 않는다.
- 최소 터치 목표 `48dp`
- 색·호버·길게 누르기만으로 상태를 전달하지 않는다.

## 11. 비정본 테스트 fixture

```yaml
fixture_status: NON_CANONICAL_BASELINE_TEST_FIXTURE
canonical_balance: false
product_data_authority: NONE
```

최소 세 후보:

- `FIXTURE_A_HIGH_ENHANCEMENT_HEAVY`: 높은 강화, 높은 중량, 관련 환경 기능 없음
- `FIXTURE_B_BALANCED_DURABLE`: 중간 강화·한도 이내 중량·현재 내구도 우수
- `FIXTURE_C_CONTEXT_FUNCTION`: 더 낮은 강화 가능, 현재 여정과 일치하는 `ENVIRONMENTAL_SEALING` 또는 `FIELD_SERVICEABILITY`

한 fixture에서 `ENVIRONMENTAL_SEALING`과 `FIELD_SERVICEABILITY`를 모두 억지로 넣지 않는다. 세션 목표에 따라 하나의 실제 승인 기능을 선택한다.

정확한 위험도·능력치·성공률·마모량·수리 비용·보상·일수는 `BASELINE_TEST_PRESET`이다.

## 12. 플레이테스트 계약

```text
OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL
→ KEEP / CHANGE / RETEST
```

행동 관찰:

1. 인계 전 최소 두 작품을 실제로 비교하는가.
2. 최고 강화만 보지 않고 중량·내구도·실제 관련 기능 중 하나 이상을 확인하는가.
3. `OVERWEIGHT`를 성공률보다 우선하는 배정 불가 Gate로 이해하는가.
4. `ENVIRONMENTAL_SEALING`을 결속 환경에만 적용되는 완화로 이해하는가.
5. `FIELD_SERVICEABILITY`를 완전 복원이나 상시 성공 보너스로 오해하지 않는가.
6. 결과 뒤 같은 UID의 마모·현장 유지보수·손상을 알아보고 다음 수리/강화/신작 판단을 고민하는가.

중립 회상 질문:

- “어떤 작품을 맡겼나요?”
- “결정할 때 무엇을 봤나요?”
- “이번 여정에서 어떤 환경이나 부담이 중요했다고 생각하나요?”
- “현장 유지보수가 있었다면 무엇이 달라졌다고 생각하나요?”
- “돌아온 작품은 이전 작품과 어떤 관계인가요?”
- “다음에 무엇을 하고 싶나요? 왜인가요?”

질문에서 정답 원인이나 기대 행동을 먼저 말하지 않는다. 행동과 회상이 충돌하면 이해 PASS를 보류한다.

## 13. SOURCE_CONTEXT_PACKET

### Death Stranding Director's Cut beginner guidance

```yaml
source_role: PRODUCT_REFERENCE
observed_fact: 출발 전 cargo weight를 확인하고 terrain·order를 보고 route와 equipment를 준비하는 구조가 명시되어 있다.
judgment: ADAPT
apply_to_blacksmith: 토렌 출발 전에 알려진 환경·부담과 작품 선택 trade-off를 읽게 한다.
do_not_copy: 직접 이동·균형 잡기·지도 경로 최적화를 Blacksmith 플레이로 가져오지 않는다.
```

### Pacific Drive

```yaml
source_role: PRODUCT_REFERENCE
observed_fact: 반복 excursion에서 차량이 환경 위험으로 손상되고, 귀환 후 repair·upgrade가 다음 출발 준비로 이어진다.
judgment: ADAPT
apply_to_blacksmith: 같은 작품 UID의 마모·손상·현장 유지보수 흔적이 다음 수리·복원·강화 이유가 되게 한다.
do_not_copy: 모든 여정에 강제되는 유지보수 세금이나 차량 생존 시뮬레이션을 가져오지 않는다.
```

### Crusader Kings III Dev Diary #85 — An Artifact's Life

```yaml
source_role: PRODUCT_REFERENCE
observed_fact: artifact는 사용·교환·손상·수리·reputation을 거치며 지속되는 물건으로 취급된다.
judgment: ADAPT
apply_to_blacksmith: 같은 UID 작품이 여정 흔적과 수리 이유를 축적한다.
do_not_copy: 시간 경과 자동 내구도 세금과 0 durability 자동 소멸을 Blacksmith baseline으로 가져오지 않는다.
```

### Games User Research — usability playtests / unbiased questions

```yaml
source_role: USER_RESEARCH_METHOD
observed_fact: 관찰 행동만으로 원인을 단정하지 않고, 비유도 질문으로 플레이어 이해를 함께 확인한다.
judgment: ADOPT
apply_to_blacksmith: 작품 비교 행동과 중립 회상을 함께 사용한다.
do_not_copy: 만족도 한 문항이나 유도 질문을 이해 증거로 사용하지 않는다.
```

## 14. 적대적 검토

### P1 — Nadia 재스킨 위험

토렌도 `생환+회수`를 목표로 하면 두 콘텐츠가 환경 이름만 다른 같은 구조가 된다.

조치:

- Toren의 중심 결과를 `JOURNEY_ARRIVAL_STATE + ROUTE_EXPOSURE_STATE + ITEM_UID_LIFECYCLE_STATE`로 분리한다.
- 회수 대상 자체를 기본 목표로 두지 않는다.

### P1 — 직접 여행 게임화

경로·환경을 강조하다 보면 지도 선택·이동 미니게임이 생길 수 있다.

조치:

- 경로 대응은 Toren의 비직접 일정 사건이다.
- 플레이어의 직접 입력은 작품 비교·인계와 후속 제작 판단에 머문다.

### P1 — 새 원수치 팽창

`신뢰성`, `휴대성`, `수리 용이성`을 각각 새 숫자로 만들 위험이 있다.

조치:

- 새 raw stat 없음.
- 기존 `WEIGHT`, `DURABILITY`, 강화, 승인 기능만 사용한다.
- 수리 기능은 기존 `FIELD_SERVICEABILITY`만 소비한다.

### P1 — 유지보수 세금

매 여행마다 무조건 내구도 감소·수리 비용을 강제하면 작품 애착보다 귀찮음이 앞선다.

조치:

- 자동 매일 내구도 감소 금지.
- 마모·손상은 사건과 인과가 있을 때만 발생한다.
- ROUTINE completion만으로 수리 의무를 만들지 않는다.

### P1 — 기능의 범용 성공 보너스화

`ENVIRONMENTAL_SEALING`이나 `FIELD_SERVICEABILITY`를 항상 성공률에 더하면 기능 카탈로그 계약을 깨뜨린다.

조치:

- `ELIGIBILITY / RISK_MITIGATION / SPECIFIC_INTERACTION` 역할만 유지한다.
- 실제 일치 맥락에서만 결과 원인으로 사용한다.

### P0

없음.

최종 설계 판정: `P0_0 / P1_0_AFTER_MITIGATION`.

## 15. 완료 기준과 경계

이 설계의 완료 기준:

- Toren이 Nadia와 다른 작품 선택 이유와 결과 축을 가진다.
- 새 raw stat·새 여행 조작·새 자동 추천 시스템을 만들지 않는다.
- 기존 승인 `FIELD_SERVICEABILITY`·`ENVIRONMENTAL_SEALING`을 정확히 소비한다.
- 같은 UID가 마모·현장 유지보수·손상·분실/회수 이력을 유지한다.
- 결과가 수리·복원·후속 강화·다음 여정용 신작으로 돌아온다.
- 테스트 숫자는 비정본이며 사람 플레이테스트 전 제품 밸런스로 승격하지 않는다.

이번 범위에서 변경하지 않는 것:

- Godot runtime·Scene·Resource·script·asset
- 정확한 일수·확률·보상·수리량·마모량
- 새 아이템 raw stat
- 새 특수기능
- Task3 제품 구현 Gate

```yaml
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
HUMAN_PLAYTEST: NOT_RUN
ANDROID_DEVICE: NOT_RUN
```
