# Blacksmith R3–R7 SOLDIER_01 — Marek Olden Small-Lot Standard Order Canon

- Decision: `BS-CONTENT-20260811-03`
- 상태: `USER_APPROVED_R3_R7_3_OF_10 / PLANNING_ONLY`
- Content ID: `SOLDIER_01`
- Customer ID: `MAREK_OLDEN`
- 고객: 마레크 올덴
- Activity Family: `SMALL_LOT_STANDARD_ORDER`
- Content Goal: `UNIT_READINESS_AND_STANDARD_FIT`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`

## 1. 목적

마레크 올덴은 변경 수비대 병참장교다. 이 콘텐츠는 한 점의 최고 강화 명작이 아니라, **동일한 공개 표준을 만족하는 소량 장비 묶음을 장인이 직접 책임지는 경험**을 검증한다.

플레이어는 병참·전술 지휘관이 아니다. 수비대의 요구를 읽고 어떤 기준품을 만들지, 어떤 정도까지 강화할지, 완성된 개별 작품 가운데 무엇을 납품할지 결정하는 대장장이다.

```text
PLAYER_ROLE: BLACKSMITH_SMALL_LOT_EQUIPMENT_DECISION_MAKER_NOT_LOGISTICS_OR_COMBAT_CONTROLLER
DIRECT_TACTICAL_COMBAT: false
REALTIME_LOGISTICS_CONTROL: false
WORKER_PRODUCTION_LINE: false
FREE_ITEM_CLONING: false
```

## 2. 기본 흐름

```text
마레크 방문
→ 공개 표준 요구 확인
→ 기준품 한 점 직접 제작
→ 소량 표준 주문 수락
→ 반복 설정 압축 + 개별 작품 생산
→ 개별 작품 저강화/마무리
→ 조건을 만족하는 UID들 선택·납품
→ 수비대의 비직접 임무·사용 결과
→ 부대 상태 + 표준 채택 + 개별 작품 생애 결과
→ 수리·교체·다음 규격·새 제작 이유
```

직접 전술 전투와 실시간 병참 조작은 추가하지 않는다.

## 3. 소량 주문과 첫 fixture

소량 주문은 3자리 산업 생산이 아니다. 첫 검증 fixture는 다음을 사용한다.

```text
ORDER_QUANTITY = 10
ORDER_QUANTITY_STATUS = NON_CANONICAL_BASELINE_TEST_PRESET
```

정확히 10개가 모든 Soldier 주문의 영구 규칙은 아니다. 후속 플레이테스트·경제 검증에서 수량은 조절할 수 있지만, 한 명의 대장장이가 제한된 하루 작업량을 배분하는 코어를 침식할 정도의 산업 생산 규모로 확장하지 않는다.

## 4. 기준품과 반복 생산

첫 작품은 평소 제작처럼 직접 만들고 `REFERENCE_ITEM_UID`로 기록한다. 기준품은 플레이어가 이번 주문의 공개 요구를 어떻게 해석했는지 보여주는 대표 작품이다.

나머지 작품에서는 다음 반복 입력을 재사용할 수 있다.

- 작품 범주
- 선택한 재료 계열
- 공개 표준 설정
- 이미 확인한 반복 제작 UI 선택

그러나 성공한 기준품의 상태를 그대로 복제하지 않는다.

```text
PER_ITEM_UID_PRESERVED
PER_ITEM_COST_AND_RESULT_PRESERVED
```

각 작품은 반드시:

- 고유 UID를 가진다.
- 자체 재료·골드 등 현재 책임 원본의 비용을 소비한다.
- 현재 제작 계약이 요구하는 작업량·피로도 기회비용을 독립적으로 소비한다.
- 자체 단조 결과를 가진다.
- 자체 강화 시도와 결과를 가진다.
- 자체 provenance·연대기·소유·손상·복원 이력을 가진다.

반복 입력은 줄일 수 있지만 작품 생성 결과를 무료 복사하는 기능은 금지한다.

## 5. 공개 표준 요구

마레크의 표준은 새로운 불투명 총점이 아니다. 기존 작품 증거 중 이번 의뢰에 실제 관련된 항목을 공개 조건으로 사용한다.

예시 축:

- 장비 범주·역할 eligibility
- 현재 `WEIGHT` 또는 이미 승인된 하중 Gate
- 강화 단계
- 현재 `DURABILITY`
- 의뢰가 명시적으로 요구하는 기존 승인 특수기능

```text
STANDARDIZATION_SCORE: false
SUPPLY_EFFICIENCY_SCORE: false
UNIT_READINESS_SCORE: false
```

**10개가 모두 같은 수치를 가져야 하는 것이 아니라, 납품되는 모든 UID가 같은 공개 규격을 만족해야 한다.** 제작 등급·세부 단조 결과·작품 이력의 개별 차이는 유지된다.

## 6. 저강화 기준과 자동 강화 관계

첫 Soldier fixture는 저강화 소량 주문으로 검증한다. 정확한 저강화 목표 수치는 출시 정본이 아니다.

```text
LOW_ENHANCEMENT_TARGET: NON_CANONICAL_BASELINE_TEST_PRESET
```

중·후반 반복 입력을 줄이기 위한 자동 강화 상한은 별도 시스템 Decision이 소유한다.

**Marek 콘텐츠 자체는 자동 강화 상한을 해금하거나 상승시키지 않는다.**

`BS-CORE-20260811-01 / AUTO_ENHANCEMENT_CAP_UNLOCK`이 이미 해금된 구간에서만 편의 기능을 제공할 수 있으며, 자동 강화 역시 각 UID별 정상 확률·비용·자원·작업 기회비용·시도 이력을 그대로 사용한다.

## 7. 결과 구조

하나의 배치 성공률로 모든 결과를 압축하지 않는다.

```text
UNIT_MISSION_STATE
STANDARD_ADOPTION_STATE
BATCH_ITEM_LIFECYCLE_STATE
```

예를 들어 임무는 성공했지만 표준 채택은 보류되고, 특정 UID 두 점이 손상되어 돌아올 수 있다. 이 조합은 정상 결과다.

### UNIT_MISSION_STATE

수비대의 이번 비직접 임무·사용 결과를 요약한다. 플레이어가 전술 전투를 직접 조작하지 않는다.

### STANDARD_ADOPTION_STATE

이번 규격이 수비대의 반복 표준으로 채택될 가치가 있었는지 별도로 보여준다. 단순히 최고 강화인지가 아니라 공개 요구와 소량 전체의 일관된 충족 여부를 설명한다.

### BATCH_ITEM_LIFECYCLE_STATE

납품된 UID 중 어떤 작품이 정상 사용, 손상, 회수, 분실 단서, 특이 사건 등을 겪었는지 묶음 요약한다. 중요한 작품은 개별 UID로 다시 진입할 수 있다.

## 8. 배치 UI와 UID 생애

```text
SMALL_LOT_ORDER_ID
→ item_uid[]
→ batch summary
→ notable UID callouts
→ full per-UID history remains queryable
```

일상적인 반복 로그는 UI에서 접을 수 있지만 원본 이벤트를 삭제하지 않는다. 같은 UID는 이후 수리·복원·회수·재판매·다른 고객·전시·Chronicle 흐름으로 이어질 수 있다.

## 9. 적대적 보호 경계

```text
NO_THREE_DIGIT_MASS_PRODUCTION_CORE
NO_WORKER_OR_PRODUCTION_LINE_SYSTEM_FROM_THIS_DECISION
NO_REALTIME_LOGISTICS_CONTROL
NO_DIRECT_TACTICAL_COMBAT
NO_FREE_ITEM_CLONING
PER_ITEM_UID_PRESERVED
PER_ITEM_COST_AND_RESULT_PRESERVED
NO_OPAQUE_STANDARDIZATION_SCORE
NO_SINGLE_HIGHEST_ENHANCEMENT_ALWAYS_BEST
PRODUCT_IMPLEMENTATION_BLOCKED
TASK3_IMPLEMENTATION_NOT_APPROVED
```

### 공격과 판정

1. 10회 동일 조작 노가다 → `MUST_FIX`: 반복 설정·입력은 압축하되 개별 제작 결과는 유지한다.
2. 기준품 복사 버튼으로 공장화 → `MUST_FIX`: 비용·작업·단조·강화·UID 결과의 독립성을 강제한다.
3. UID 10개로 UI 폭발 → `MUST_FIX`: 묶음 요약 + notable UID + 상세 진입으로 계층화한다.
4. 높은 강화가 항상 정답 → `MUST_FIX`: 공개 표준 조건과 결과 축을 분리한다.
5. 군인 콘텐츠가 전투·병참 게임화 → `MUST_FIX`: 사용 결과는 비직접 world feedback으로 유지한다.

## 10. 벤치마킹 판정

- Blacksmith Master: `ADAPT` — 주문·생산 맥락. 직원·산업 생산라인은 `REJECT`.
- Anvil Saga: `ADAPT` — 고객 주문과 결과 연결. 광역 상점 시뮬레이션 drift는 `REJECT`.
- Battle Brothers: `ADAPT` — 장비 적합이 집단 결과에 의미를 갖는 원리. 직접 전술 전투·용병 생존 관리는 `REJECT`.
- Lean standardized work: `ADAPT` — 공개 기준과 반복 가능한 과정. 산업 통계 시뮬레이션은 `REJECT`.
- `DIFFERENTIATOR`: 소량 표준 주문에서도 각각의 장비는 이름 없는 stack이 아니라 개별 UID와 작품 생애를 가진다.

## 11. 플레이테스트

현재 사람 플레이테스트: `NOT_RUN`.

후속 검증은 다음을 관찰한다.

- 왜 이 기준품을 만들었는가.
- 더 높은 강화 장비가 왜 표준에 반드시 더 좋은 것은 아닌지 설명할 수 있는가.
- 반복 입력 압축이 공장 자동화가 아니라 장인의 반복 작업 편의로 느껴지는가.
- 납품한 작품들이 각각 독립 작품이라는 사실을 이해하는가.

정확한 주문 수량·저강화 목표·보상·비용·사건 확률은 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.
