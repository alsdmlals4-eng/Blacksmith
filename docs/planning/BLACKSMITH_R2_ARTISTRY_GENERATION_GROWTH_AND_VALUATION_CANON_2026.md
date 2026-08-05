# Blacksmith R2 예술성 생성·성장·가치 평가 정본

- Decision ID: `BS-CRAFT-20260805-02`
- 상태: `USER_APPROVED / R2_BATCH_005_1_OF_10 / APPROVED_PENDING_MERGE`
- 선행 Decision: `BS-CRAFT-20260805-01`
- 설계 명세: `docs/superpowers/specs/2026-08-05-artistry-generation-growth-economy-design.md`
- 구현 계획: `docs/superpowers/plans/2026-08-05-artistry-generation-growth-economy.md`
- 제품 구현: `BLOCKED`

## 1. 책임 분리

```text
artistry = 작품 UID에 저장되는 예술성 원수치
artistry_value = 시장·감정 맥락에서 계산되는 점감 가치
customer_artistry_fit = 고객·일정 맥락에서 계산되는 적합도
```

- `artistry`만 작품의 영구 능력치다.
- `artistry_value`와 `customer_artistry_fit`은 맥락별 파생 결과이며 새 영구 능력치로 저장하지 않는다.
- 예술성은 계속 `0` 이상의 정수이며 고정 설계 최대치가 없다.
- 표시 형식은 `예술성 27`처럼 분모 없는 원수치다.

## 2. 최초 제작 예술성의 허용 원천

```text
BASE_ITEM_DESIGN_AESTHETIC_TENDENCY
MATERIAL_VISUAL_PROCESSING_FIT
DIRECT_FORGING_AESTHETIC_RESULT
```

### 기본 작품 설계의 미적 성향

의장검·의식용 무기처럼 조형을 중시하는 설계는 미적 기여를 가질 수 있다. 전투용 설계도 예술성 `0` 이상을 가질 수 있다.

### 재료의 시각·가공 특성과 설계 적합성

재료 가격이나 희귀도 자체가 아니라 색·결·광택·가공성·설계와의 조화가 기여한다. 비싼 재료만으로 높은 예술성을 보장하지 않는다.

### 직접 단조의 미적 완성 결과

동일 제작 판정이 제작 등급과 예술성 양쪽에 영향을 줄 수는 있지만, 제작 등급을 고정 예술성 보너스표로 변환하지 않는다.

현재 추가하지 않는 것:

- 보조재료 슬롯
- 별도 장식재료 슬롯
- 승인되지 않은 대장장이 숙련 능력치
- 재료 희귀도 × 제작 등급의 자동 예술성 배율

## 3. 제작 후 성장의 허용 원천

```text
ARTISTIC_FINISH
ARTISTRY_OWNED_CATALYST_EFFECT
APPROVED_FINISHING_OR_DECORATION_CONTENT
MEANINGFUL_ARTISTIC_REWORK
```

- `ARTISTIC_FINISH`: 정밀강화의 예술적 마감 방식
- `ARTISTRY_OWNED_CATALYST_EFFECT`: 예술성 수치 책임이 명시된 촉매 효과
- `APPROVED_FINISHING_OR_DECORATION_CONTENT`: 승인된 세공·마감·장식 콘텐츠
- `MEANINGFUL_ARTISTIC_REWORK`: 비용·위험·결과가 있는 의미 있는 예술적 재작업

## 4. 자동 증가 금지

다음 행동만으로 `artistry`가 증가하지 않는다.

```text
GENERAL_ENHANCEMENT_LEVEL
SALE
GIFT
EXHIBITION_COUNT
APPRAISAL_COUNT
OWNERSHIP_TRANSFER
FAME
CHRONICLE_EVENT
LOW_COST_REPEAT_ACTION
```

- 일반 강화 레벨 상승은 예술성을 자동 증가시키지 않는다.
- 판매·증여·전시·감정·소유권 이전·명성·연대기는 작품의 맥락이나 사회적 가치에 영향을 줄 수 있지만 예술성 원수치를 직접 바꾸지 않는다.
- 같은 저비용 행동을 반복해 예술성을 무한 생성할 수 없다.

## 5. 변화 출처와 UID 기록

모든 예술성 변화는 작품 UID에 다음 원인을 남긴다.

```text
source_category
source_action_or_event
before_artistry
artistry_delta
result_artistry
related_catalyst_or_process
```

정확한 저장 Schema는 제품 구현 Gate가 열린 뒤 확정한다. 현재는 원인 추적 가능성이 계약이다.

## 6. 가치 평가

권장 가치 구조:

```text
최종 가치
= 기능 가치
+ 제작 등급 가치
+ 예술성 점감 가치
+ 촉매 수식어 가치
+ 연대기 가치
+ 고객·시장 수요 보정
```

기계 계약:

```text
ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE
```

가치 구성요소:

```text
FUNCTIONAL_VALUE
CRAFTING_GRADE_VALUE
DIMINISHING_ARTISTRY_VALUE
CATALYST_AFFIX_VALUE
CHRONICLE_VALUE
CUSTOMER_OR_MARKET_DEMAND_ADJUSTMENT
```

### 점감 원칙

- 예술성이 증가하면 예술성 가치 기여는 감소하지 않는다.
- 높은 구간일수록 추가 `1`점의 한계 가치는 작아진다.
- 화면의 예술성 원수치를 압축하거나 낮추지 않는다.
- 구간 경계와 계수는 data 기반 테스트 프리셋에서 관리한다.
- 로그·제곱근 공식의 코드 직접 고정보다 **구간별 한계 가치 테이블**을 우선한다.

정확한 구간·계수는 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 7. 중복 계산 금지

- 하나의 원인은 한 가치 구성요소에 한 번만 반영한다.
- 재료 가격을 예술성으로 변환한 뒤 재료 가치에서도 다시 곱하지 않는다.
- 촉매가 직접 예술성을 올렸다면 동일 증가분을 촉매 수식어 배율과 가격에서 다시 증폭하지 않는다.
- 연대기 사건은 연대기 가치에 기여할 수 있지만 같은 사건을 예술성에도 자동 합산하지 않는다.
- 제작 등급·재료·예술성·촉매·연대기의 연속 곱셈은 금지한다.

## 8. 고객 관심 유형

```text
IGNORE / SECONDARY / PRIMARY / REQUIREMENT
```

- `IGNORE`: 예술성을 판단에 사용하지 않음
- `SECONDARY`: 주요 요구 충족 후 보조 가치로 사용
- `PRIMARY`: 주요 요구 능력 중 하나
- `REQUIREMENT`: 최소 요구치 또는 선호 구간 충족 필요

높은 예술성은 예술성에 관심 없는 고객에게 패널티가 아니다. 다만 해당 고객은 초과 예술성에 추가 비용을 지불하지 않을 수 있다.

초기 방향:

- 검투사: `IGNORE` 또는 `SECONDARY`
- 모험가: `IGNORE` 또는 `SECONDARY`
- 군인: `IGNORE`
- 귀족: `PRIMARY`
- 후원자: `PRIMARY` 또는 `REQUIREMENT`
- 수집가: `PRIMARY`, 연대기와 별도 평가
- 의식·행사: `REQUIREMENT` 가능

정확한 고객별 배치는 후속 콘텐츠·경제 테스트 프리셋에서 확정한다.

## 9. 플레이어 정보 공개

결정적 결과:

```text
예술성 +4
```

확률적 결과:

```text
예술성 +2~5 예상
```

고객·일정:

```text
예술성 중요도: 높음
현재 작품: 요구 충족
초과 예술성 추가 보상: 낮음
```

공개 항목:

```text
DIRECTION
EXPECTED_RANGE_FOR_PROBABILISTIC_ACTION
CUSTOMER_IMPORTANCE
REQUIREMENT_STATUS
```

내부 가격 공식을 전부 공개하지 않더라도 선택의 방향과 결과 원인은 설명 가능해야 한다.

## 10. 손상·복원 경계

- 수리 반복으로 예술성 순증가 금지
- 손상 반복으로 예술성 순증가 금지
- 복원만 수행한 경우 손상 전 기록값을 초과하는 순증가 금지
- 손상 전 값을 넘는 증가는 별도 예술적 재작업의 비용·위험·결과를 요구
- 손상·복원 원인은 작품 UID에 기록

영구 원수치 감소와 일시적 유효 예술성 감소 중 어느 방식을 사용할지는 손상 시스템 Decision에서 확정한다.

## 11. 악용 방지

다음 반복은 예술성 순증가를 만들 수 없다.

```text
repair loop
 damage loop
sale loop
exhibition loop
appraisal loop
gift loop
low-cost repeat loop
```

추가 금지:

- 같은 정밀강화 이정표 무한 리롤
- 비싼 재료만으로 높은 예술성 보장
- 제작 등급이 예술성 최소값·상한·배율을 결정
- 촉매 직접 증가와 수식어 배율의 이중 계산
- 예술성·연대기·명성을 하나의 영구 총점으로 통합
- 높은 예술성이 모든 고객의 최적해가 되는 구조
- 모든 가치 구성요소의 곱셈 중첩

## 12. 미확정

- 최초 제작 예술성 분포
- 작품 종류별 초기 범위
- 재료 적합성 태그와 증가량
- `ARTISTIC_FINISH` 증가량·비용·성공률
- 촉매별 증감과 계보
- 구간별 한계 가치 경계·계수
- 고객별 최소 요구치·선호 구간
- 손상·복원 계산
- 저장 자료형·overflow 보호

모두 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`이며 제품값으로 고정하지 않는다.

## 13. 검증 경계

- 현재 변경은 기획 정본·Registry·검증 계약에 한정
- 제품 코드·Scene·runtime data·asset 변경 없음
- 제품 구현: `BLOCKED`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
