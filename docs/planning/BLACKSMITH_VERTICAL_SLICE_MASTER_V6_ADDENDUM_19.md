# 블랙스미스 버티컬 슬라이스 마스터 기획서 v6 — 추가 결정 19

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
>
> 결정 기록: GitHub Issue #60
>
> 기준일: 2026-07-27

## 장비와 고객의 관계 정정

블랙스미스에는 **고객용 전용 장비** 개념이 없다.

대장간에서 제작·강화·보유하는 장비는 모두 일반적인 상품 재고다. 고객이 방문하면 이미 만들어진 완제품 재고를 대상으로 요구·선호·야망·가격·후속 가치를 비교하고, 플레이어가 그중 판매할 제품을 선택한다.

```text
장비 제작·강화
→ 대장간 재고에 완제품 등록
→ 고객 방문
→ 고객 조건과 재고 제품 비교
→ 플레이어가 판매 제품 선택
→ 판매·소유권 이전
```

고객이 방문했다는 이유로 해당 고객만을 위한 장비가 생성되거나, 특정 고객에게만 판매 가능한 장비 종류가 생기지 않는다.

## 기존 표현의 해석 교정

선행 문서에 등장한 다음과 같은 표현은 시스템 개념이 아니라 세션 구성 설명을 위한 임시 표기였다.

- `검투사 후보 무기`
- `모험가 후보 탐험용 방어구`
- `수집가 후보 전시·의식용 장비`
- `병사 후보 군용 장비`

이 표현을 다음처럼 해석한다.

```text
잘못된 해석
→ 검투사만 사용할 수 있는 전용 무기
→ 모험가만 사용할 수 있는 전용 방어구

올바른 해석
→ 일반 재고 중 검투사의 조건에 잘 맞을 수 있는 무기
→ 일반 재고 중 모험가의 조건에 잘 맞을 수 있는 방어구
```

장비의 유형·강화 단계·수식어·내구·역사 가치가 고객 조건과 결합해 적합도를 만들 뿐, 장비 데이터에 고객 전용 플래그를 두지 않는다.

## 완제품 재고 계약

대장간 재고의 각 제품은 최소한 다음 정보를 가진다.

- 장비 식별자
- 장비 유형
- 제작 완료 여부
- 현재 강화 단계
- 정밀강화·고위 정밀강화 결과
- 대표 수식어와 보조 수식어
- 내구·손상 상태
- 제작자
- 현재 소유자
- 가치와 역사 가치
- 장비 연대기
- 판매 가능 여부

고객별 적합도는 장비에 영구 저장된 고객 전용 속성이 아니라, 고객 조건과 장비 상태를 비교해 계산하거나 표현하는 결과다.

```text
고객 적합도
= 고객 요구 충족
+ 고객 선호 방향
+ 고객 야망과의 장기 적합성
+ 현재 장비 상태
+ 가격·후속 가치
```

정확한 적합도 계산식과 가중치는 후속 수치 설계 및 플레이테스트 조정 대상으로 남긴다.

## 고객 전용 장비 금지

다음 구조를 사용하지 않는다.

- 특정 고객 식별자가 장비 정의에 포함됨
- 특정 고객이 아니면 구매할 수 없는 일반 장비
- 고객 방문 시 자동으로 해당 고객용 장비 생성
- 고객마다 별도 장비 클래스 또는 저장 구조 사용
- 고객 이름을 검사해 장비 효과가 활성화됨
- 고객 전용 장비를 다른 고객 비교 화면에서 숨김
- 판매 전부터 장비의 미래 소유자를 고정

특별 의뢰 장비가 장기 제품 범위에서 검토될 수는 있으나, 그것도 `고객 전용 장비 타입`이 아니라 특정 요구 조건을 가진 주문·계약으로 다뤄야 한다. 현재 버티컬 슬라이스에서는 일반 완제품 재고 판매가 기준이다.

## 네 고객 비교 구조에 미치는 영향

수집가·모험가·검투사·병사는 동일한 완제품 재고 풀을 본다.

각 고객은 장비를 다음 관점으로 다르게 평가한다.

| 고객 | 주요 평가 방향 예시 |
|---|---|
| 수집가 | 희소성, 역사 가치, 외형, 제작자·소유자 계보 |
| 모험가 | 생존, 내구, 기동, 환경 대응, 회수 가능성 |
| 검투사 | 전투 성능, 명성, 경기 적합성, 대표 수식어 |
| 병사 | 내구, 보급성, 부대 운용, 수리성, 공적 기록 |

같은 장비가 여러 고객에게 판매 가능할 수 있다. 다만 가격, 즉시 보상, 후속 세계 결과와 장기 가치가 다르게 제시될 수 있다.

```text
같은 완제품 장비
├─ 수집가: 역사 가치가 높아 높은 가격 제시
├─ 검투사: 성능은 좋지만 경기 스타일과 일부 불일치
├─ 모험가: 내구는 적합하지만 무게가 부담
└─ 병사: 표준화·수리성 부족으로 낮은 평가
```

플레이어는 고객 전용 정답을 찾는 것이 아니라, 현재 재고를 어느 고객에게 판매할지 선택한다.

## 네 고객 동일 깊이 세션과의 정합성

추가 결정 17~18의 네 고객 동일 깊이 구조는 유지한다. 다만 세션 시작 시 네 고객에게 하나씩 예약된 장비를 제공하는 방식으로 해석하지 않는다.

세션 흐름은 다음과 같다.

```text
[대장간]
이미 제작된 완제품 재고 확인
→ 일부 제품을 추가 강화·정비

[방문 고객]
네 고객이 같은 재고 풀을 평가
→ 고객별 제안 비교
→ 제품을 고객에게 순차 판매

[후속 준비]
판매된 제품과 고객에 맞는 지원 선택

[영업 종료]
판매 완료된 네 제품의 세계 결과 판정·저장
```

네 고객 모두에게 판매하려면 최소 네 개 이상의 판매 가능한 완제품이 필요하다. 그러나 어떤 제품이 어느 고객에게 판매될지는 사전에 고정하지 않는다.

## 재고와 판매 충돌 처리

하나의 완제품은 한 시점에 한 고객에게만 판매할 수 있다.

```text
제품 A를 검투사에게 판매 확정
→ 제품 A 소유권 검투사로 이전
→ 수집가·모험가·병사 제안에서 판매 불가
→ 다른 재고 제품을 선택해야 함
```

판매 전에는 여러 고객이 동일 제품에 제안을 할 수 있다.

판매 후에는 해당 제품이 다른 고객에게 자동 복제되거나 같은 세션에서 다시 판매되지 않는다.

## 작업대 표시 원칙

작업대와 재고 화면에서 고객 이름을 제품의 본래 분류명으로 사용하지 않는다.

잘못된 표시:

- `검투사용 무기`
- `모험가 전용 방어구`
- `수집가 전용 장식품`
- `병사용 군수품`

허용되는 표시:

- 장검
- 탐험용 흉갑
- 의식용 투구
- 군용 방패
- 현재 고객 적합도 요약
- 고객별 제안 비교

`현재 고객 적합도`는 판매 맥락에서만 나타나는 비교 정보이며 장비의 고유 이름이나 타입을 대체하지 않는다.

## 시작 재고 관련 미정 사항

다음 항목은 후속 세션 시작 재고 결정에서 확정한다.

- 세션 시작 완제품 개수
- 제품 유형 조합
- 시작 강화 단계 분포
- 완성품과 추가 정비 필요 제품의 비율
- 고객 네 명 모두에게 판매 가능한 최소 재고 여유
- 일부 제품에 복수 고객 제안이 발생하는 정도
- 미판매 재고의 세션 종료 후 처리

이 결정만으로 특정 제품과 특정 고객의 일대일 매칭을 확정하지 않는다.

## 저장·데이터 계약

- 장비 데이터에는 `전용 고객` 필드를 두지 않는다.
- 고객 제안은 고객 식별자와 장비 식별자의 관계 데이터로 저장한다.
- 판매 전 복수 제안이 존재할 수 있다.
- 판매 확정 시 선택한 고객과 장비의 소유권 이전을 원자적으로 저장한다.
- 판매되지 않은 제안은 장비 복제나 소유권 변경을 발생시키지 않는다.
- 같은 장비를 여러 고객에게 중복 판매할 수 없다.
- 세계 사건은 판매 완료된 실제 장비 식별자를 참조한다.
- 장비 연대기는 판매 전 제작 이력과 판매 후 고객 이력을 같은 식별자에 이어서 기록한다.

## 기획 상태 반영

```text
EQUIPMENT_CUSTOMER_RELATIONSHIP: GENERAL_INVENTORY_WITH_CONTEXTUAL_FIT
CUSTOMER_EXCLUSIVE_EQUIPMENT_CONCEPT: FORBIDDEN
CUSTOMER_VISIT_AUTO_GENERATES_EQUIPMENT: FORBIDDEN
EQUIPMENT_PREASSIGNED_TO_CUSTOMER: FORBIDDEN
CUSTOMER_FIT: RELATIONSHIP_BETWEEN_CUSTOMER_AND_EXISTING_PRODUCT
MULTIPLE_CUSTOMER_OFFERS_BEFORE_SALE: ALLOWED
ONE_PRODUCT_MULTIPLE_SIMULTANEOUS_OWNERS: FORBIDDEN
SALE_TRANSFERS_EXISTING_PRODUCT_ID: REQUIRED
EQUIPMENT_CHRONICLE_CONTINUES_ACROSS_SALE: REQUIRED
FOUR_CUSTOMER_SESSION_MODEL: MAINTAINED_WITH_SHARED_FINISHED_GOODS_INVENTORY
STARTING_INVENTORY_COMPOSITION: UNRESOLVED
```

이 정정은 고객별 전용 장비 제작 게임이 아니라, 플레이어가 제작한 완제품 재고를 어떤 고객에게 판매할지 판단하는 대장간 운영 게임이라는 방향을 명확히 한다.
