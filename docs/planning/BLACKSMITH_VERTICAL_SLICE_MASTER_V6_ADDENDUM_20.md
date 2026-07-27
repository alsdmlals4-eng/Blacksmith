# 블랙스미스 버티컬 슬라이스 마스터 기획서 v6 — 추가 결정 20

> 상태: `CANDIDATE_AUTHORITY / PLANNING_IN_PROGRESS`
>
> 상위 문서: `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_DRAFT.md`
>
> 선행 추가 결정:
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_01.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_02.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_03.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_04.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_05.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_06.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_07.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_08.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_09.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_10.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_11.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_12.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_13.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_14.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_15.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_16.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_17.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_18.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_19.md`
>
> 결정 기록: GitHub Issue #60
>
> 기준일: 2026-07-27

## 세션 시작 완제품 자동 지급 제안 폐기

`세션 시작 시 완제품 재고를 정해진 수량만큼 지급한다`는 구조는 게임 규칙으로 채택하지 않는다.

플레이어의 제품 재고는 실제 제작·강화·수리·보관·판매 이력의 결과다. 고객 판매 검증을 위해 세션이 시작될 때 장비가 이유 없이 생성되거나, 매 세션 동일한 완제품 목록으로 초기화되지 않는다.

```text
금지되는 해석
→ 세션을 시작하면 완제품 6개 자동 지급
→ 네 고객 판매를 위해 제품 4개 자동 생성
→ 매 영업일 재고가 정해진 구성으로 초기화

확정된 해석
→ 플레이어가 제작한 제품이 재고에 남음
→ 고객은 현재 존재하는 재고를 평가
→ 판매한 제품은 재고에서 빠지고 소유권이 이전
→ 미판매 제품은 다음 영업일에도 유지
```

이 결정은 추가 결정 19의 `일반 완제품 재고 판매` 원칙을 보강한다.

## 게임 규칙과 테스트 시작 조건 분리

버티컬 슬라이스 테스트는 검증 시간을 단축하기 위해 특정 진행 상태를 불러올 수 있다. 그러나 이것은 **테스트 픽스처 또는 준비 저장 데이터**이며, 게임의 일반적인 시작 보상이나 재고 생성 규칙이 아니다.

### 게임 규칙

- 제품은 제작·강화·수리 등 실제 플레이 행동으로 생성·변경된다.
- 제작 완료 제품은 대장간의 지속 재고에 등록된다.
- 미판매 재고는 영업일이 바뀌어도 자동 삭제·교체되지 않는다.
- 판매된 제품은 기존 장비 식별자와 연대기를 유지한 채 고객에게 소유권이 이전된다.
- 고객 방문은 제품을 생성하지 않는다.
- 고객 수에 맞춰 시스템이 판매용 제품을 자동 보충하지 않는다.
- 재고 부족은 실제 운영 상태이며 숨은 자동 지급으로 해결하지 않는다.

### 테스트 픽스처

- 특정 강화 단계의 장비가 존재하는 준비 저장 데이터를 사용할 수 있다.
- 준비 저장의 제품은 `이전 제작 이력이 이미 존재하는 상태`로 취급한다.
- 테스트 픽스처는 테스트 빌드와 기록에서 명확히 식별한다.
- 테스트 픽스처 사용을 정식 캠페인의 신규 시작 규칙으로 표현하지 않는다.
- 준비 저장을 다시 불러와도 실제 플레이 중 확정된 결과를 되돌리는 수단으로 사용하지 않는다.
- 준비 저장은 핵심 루프 검증 시간을 단축하기 위한 장치이며 밸런스 합격 근거가 아니다.

```text
VERTICAL SLICE TEST FIXTURE
→ 이미 진행된 제작 이력을 가진 검증용 저장

NOT
→ 신규 캠페인 기본 지급
→ 영업일마다 재생성되는 무료 완제품
→ 플레이어 재고 부족을 자동 보정하는 시스템
```

## 지속 재고 계약

재고는 세션 단위 임시 목록이 아니라 캠페인 진행 상태다.

각 제품은 다음 생애주기를 가진다.

```text
재료 확보
→ 제작
→ 완제품 또는 작업 중 제품
→ 강화·정밀강화·수리·정비
→ 판매 가능 재고
→ 고객 제안 비교
→ 판매 또는 보유
→ 판매 시 소유권 이전
→ 세계 사건과 장비 연대기 지속
```

### 재고 상태

- `작업 중`: 아직 판매 가능한 완제품이 아님
- `완제품`: 판매 가능한 기본 상태
- `정비 필요`: 판매 가능 여부와 가치가 상태에 따라 달라짐
- `판매 보류`: 플레이어가 당장 판매하지 않기로 선택
- `판매 완료`: 대장간 재고에서 제외되고 고객 소유로 이전
- `외부 활동 중`: 판매 후 고객·세계 활동에 사용되는 상태
- `분실·회수·손상`: 판매 후에도 동일 장비 식별자와 연대기를 유지하는 운명 상태

제품 상태는 고객 이름으로 분류하지 않는다.

## 고객 방문과 재고의 관계

고객은 방문 시점의 실제 판매 가능 재고를 평가한다.

```text
현재 판매 가능 재고
+ 고객 요구·선호·야망
+ 장비 유형·강화·수식어·내구·역사 가치
→ 고객별 적합도·가격·즉시 보상·후속 가치 제안
```

- 같은 제품이 여러 고객에게 제안을 받을 수 있다.
- 제안은 소유권 예약이 아니다.
- 판매 확정 전까지 제품은 플레이어 소유 재고다.
- 판매 확정 후 다른 고객 제안은 판매 불가 상태로 갱신된다.
- 고객이 원하는 제품이 없을 수 있다.
- 적합한 제품이 부족한 상태를 자동 생성 제품으로 감추지 않는다.
- 고객 전용 제품 슬롯을 미리 채우지 않는다.

## 네 고객 동일 깊이 결정과의 충돌 정리

추가 결정 17~18은 한 버티컬 슬라이스 세션에서 네 고객의 판매와 후속 결과를 모두 완주하도록 정했다.

이 목표를 달성하려면 테스트 흐름에 충분한 실제 재고가 필요하지만, 다음 방식은 금지한다.

- 네 고객 전용 제품 자동 생성
- 세션 시작 무료 완제품 지급
- 판매 직전 부족한 제품 자동 보충
- 고객별 예약 장비를 시스템이 숨겨서 제공

허용되는 방법은 다음 두 종류다.

1. 플레이어가 슬라이스 흐름 안에서 필요한 제품을 실제 제작·완성한다.
2. 테스트 픽스처가 이전 제작 이력을 가진 지속 재고 상태에서 시작한다.

두 방식 모두 제품은 일반 재고이며 어떤 고객에게 팔릴지는 판매 시점에 플레이어가 결정한다.

### 미해결 충돌

- 네 고객 전체 완주를 15~25분 안에 수행하기 위해 제작 과정을 어디까지 직접 플레이할지
- 테스트 픽스처에 어느 정도의 작업 중 제품과 완제품을 둘지
- 당일 영업 전·영업 중·영업 후에 제작과 강화가 가능한 범위
- 고객 방문 후 새로 완성한 제품을 기존 제안에 다시 반영하는 방식
- 재고가 부족한 영업일에 네 고객 완주를 강제할지, 다음 영업일로 넘길지

이 항목들은 실제 영업 흐름 결정에서 확정한다.

## 자동 초기화 금지

다음 동작은 사용하지 않는다.

- 세션 시작 시 재고를 고정 수량으로 맞춤
- 매 영업일 같은 제품 조합 재생성
- 미판매 제품을 자동 폐기하고 새 제품으로 교체
- 판매 제품을 다음 세션에서 다시 플레이어 재고로 복원
- 테스트 재시작을 캠페인 내 시간 되감기로 제공
- 네 고객 판매 목표 때문에 재고 무결성을 깨뜨림

신규 캠페인의 튜토리얼 시작 장비나 기본 제작 재료는 별도 결정 대상이다. 그것이 존재하더라도 `세션마다 완제품 자동 지급`을 의미하지 않는다.

## 저장·복귀 계약

지속 재고는 기존 원자적 저장 규칙을 따른다.

- 제작 완료 시 재료 소비와 제품 생성 상태를 함께 저장한다.
- 강화·수리·정비 시 비용과 제품 상태를 함께 저장한다.
- 판매 시 보상과 소유권 이전을 함께 저장한다.
- 앱 종료 후 미판매 재고가 사라지거나 새 제품으로 대체되지 않는다.
- 판매 완료 제품이 재고와 고객 소유 상태에 동시에 존재하지 않는다.
- 테스트 픽스처 로딩과 일반 캠페인 이어하기를 UI·빌드 식별상 혼동하지 않는다.

```text
제작 완료
→ 원자적 저장
→ 지속 재고 등록

판매 완료
→ 원자적 저장
→ 플레이어 재고 제외
→ 고객 소유권 등록
→ 동일 장비 ID·연대기 유지
```

## UI 용어 정정

권장 용어:

- `재고`
- `보유 제품`
- `작업 중`
- `완제품`
- `정비 필요`
- `판매 가능`
- `고객별 제안`
- `현재 소유자`

피해야 할 용어:

- `세션 시작 지급 장비`
- `검투사 슬롯 장비`
- `모험가 전용 지급품`
- `고객용 자동 완제품`
- `이번 세션 판매 세트`

테스트 문서에서는 `준비 저장`, `테스트 픽스처`, `검증용 진행 상태`라고 명시한다.

## 검증 항목

- 미판매 제품이 영업일과 앱 재실행을 넘어 유지되는가
- 판매된 제품이 플레이어 재고에서 제거되고 고객 소유로만 존재하는가
- 고객 방문이 제품을 자동 생성하지 않는가
- 재고 부족 시 숨은 자동 보충이 발생하지 않는가
- 같은 재고를 여러 고객이 평가할 수 있는가
- 판매 후 다른 고객 제안이 즉시 갱신되는가
- 테스트 픽스처와 신규 캠페인 시작이 구분되는가
- 픽스처의 제품도 일반 장비 데이터·저장·연대기 구조를 사용하는가
- 준비 저장을 사용한 테스트 결과를 일반 게임 경제 검증 결과로 과장하지 않는가

## 현재 기획 상태 반영

이 결정으로 다음 오해를 해소한다.

- `SESSION_START_FIXED_FINISHED_INVENTORY: REJECTED`
- `SESSION_START_AUTOMATIC_FINISHED_GOODS_GRANT: FORBIDDEN`
- `INVENTORY_MODEL: PERSISTENT_RESULT_OF_PRODUCTION_AND_SALES`
- `CUSTOMER_VISIT_AUTO_REPLENISHES_INVENTORY: FORBIDDEN`
- `UNSOLD_INVENTORY_PERSISTS_ACROSS_OPERATING_DAYS: REQUIRED`
- `SALE_TRANSFERS_EXISTING_PRODUCT_ID: REQUIRED`
- `VERTICAL_SLICE_TEST_FIXTURE: ALLOWED_WITH_EXPLICIT_LABEL`
- `TEST_FIXTURE_AS_NORMAL_CAMPAIGN_RULE: FORBIDDEN`
- `TEST_FIXTURE_PROVES_ECONOMY_BALANCE: NO`
- `FOUR_CUSTOMER_REQUIRED_INVENTORY_SOURCE: ACTUAL_PRODUCTION_OR_PRIOR_PRODUCTION_FIXTURE`
- `ACTUAL_PRODUCTION_TO_CUSTOMER_FLOW: NEXT_DECISION_REQUIRED`

```text
VERTICAL_SLICE_PLANNING: IN_PROGRESS
READY_FOR_기획_완료: NO
IMPLEMENTATION: BLOCKED
PLAYTEST_RESULT: NOT_AVAILABLE
```
