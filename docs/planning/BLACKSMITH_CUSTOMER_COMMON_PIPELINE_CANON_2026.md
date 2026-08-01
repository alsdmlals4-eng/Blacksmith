# Blacksmith 고객 4유형 공통 파이프라인 승인 정본

> Decision ID: `BS-CUSTOMER-PIPELINE-20260801-01`
>
> 상태: `USER_PREAPPROVED_RECOMMENDED / CANONICAL_DESIGN_COMPLETE`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 선행 결정: `BS-CUST-20260731-01`, `BS-V9-20260731-04~06`, `BS-SAVE-20260801-01`

## 1. 목적

카일·철검·검투사 경기 중심 PoC를 수집가·모험가·검투사·군인 4유형과 유형별 복수 이름 고객이 재사용하는 공통 데이터·화면·결과 파이프라인으로 전환한다.

핵심 원칙:

```text
고객별 고유 데이터
+ 유형별 평가·세계 결과 Profile
+ 하나의 공통 요청·적합도·인계·관계·저장 엔진
```

고객별 전용 Core Engine·전용 저장 구조·전용 결과 화면을 만들지 않는다.

## 2. 고객 유형과 이름 고객

### 수집가 COLLECTOR

| Customer ID | 이름 | 역할 | 핵심 가치 |
|---|---|---|---|
| `ERSA_ROEN` | 에르사 로엔 | 이동 전시 감정인 | 희소성·계보·이야기·보존 상태 |
| `SEDRIC_VAEL` | 세드릭 바엘 | 귀족 기록 보관가 | 역사적 출처·완성도·전시 가치 |

### 모험가 ADVENTURER

| Customer ID | 이름 | 역할 | 핵심 가치 |
|---|---|---|---|
| `NADIA_VENN` | 나디아 벤 | 유적 탐사대장 | 범용성·경량·생존성·회수 가능성 |
| `TOREN_MARCH` | 토렌 마치 | 장거리 길잡이 | 신뢰성·환경 대응·휴대성·수리 용이성 |

### 검투사 GLADIATOR

| Customer ID | 이름 | 역할 | 핵심 가치 |
|---|---|---|---|
| `CASSIA_BELLAN` | 카시아 벨란 | 투기장 대표 검투사 | 공격성·기술 표현·관중성·개인 상징 |
| `KYLE_VAREN` | 카일 바렌 | 실전형 검투사 | 안정적 화력·위험 감수·승부 성과 |

`gladiator_kyle` 구형 ID는 `KYLE_VAREN`으로 이전한다. 기존 관계·납품·경기 이력과 장비 UID를 보존한다.

### 군인 SOLDIER

| Customer ID | 이름 | 역할 | 핵심 가치 |
|---|---|---|---|
| `MAREK_OLDEN` | 마레크 올덴 | 변경 수비대 병참장교 | 신뢰성·표준화·내구적 운용·보급 효율 |
| `LIANA_BERG` | 리아나 베르크 | 전선 지휘관 | 임무 적합성·방어·부대 생존·책임성 |

## 3. 공통 데이터 모델

```text
CustomerTypeDefinition
├─ customer_type_id
├─ display_name
├─ value_tag_weights
├─ preferred_equipment_categories
├─ world_outcome_profile_id
└─ default_request_duration_days

NamedCustomerDefinition
├─ customer_id
├─ customer_type_id
├─ display_name
├─ role
├─ value_overrides
├─ request_template_ids
├─ relationship_profile_id
└─ presentation_asset_ids

RequestTemplate
├─ request_template_id
├─ customer_type_id
├─ eligible_equipment_category_ids
├─ required_tags
├─ preferred_tags
├─ disliked_tags
├─ deadline_rule_id
├─ reward_formula_id
└─ world_outcome_profile_id

CustomerContract
├─ contract_id
├─ customer_id
├─ request_template_id
├─ accepted_day
├─ due_day
├─ state
├─ eligibility_snapshot
└─ delivery_transaction_id

CustomerRelationship
├─ customer_id
├─ relationship_level
├─ relationship_xp
├─ completed_contract_count
├─ failed_contract_count
├─ last_interaction_day
└─ unlocked_request_tiers
```

## 4. 공통 의뢰 규칙

- 동시 활성 이름 고객 요청은 최대 2개다.
- 유형별 최소 2명의 이름 고객이 데이터에 존재한다.
- 기본 의뢰 기한은 2영업일이며 템플릿이 명시적으로 변경할 수 있다.
- 의뢰는 정확한 `iron_sword` 같은 단일 item ID가 아니라 장비 범주와 공개 조건을 사용한다.
- 신규 고객이 추가돼도 요청·적합도·인계·결과 엔진을 수정하지 않는다.

### 상태

```text
OFFERED
→ ACCEPTED
→ READY_FOR_DELIVERY
→ DELIVERED
→ RESULT_PENDING
→ RESULT_READY
→ CLOSED

EXPIRED / CANCELLED / FAILED
```

상태 전이는 event/transaction ID로 멱등 처리한다.

## 5. 거래 자격과 적합도 분리

### Eligibility

판매·인계 가능 여부만 판정한다.

```text
플레이어 보유
+ 제작 완료
+ 판매 가능 상태
+ 요청 장비 범주 일치
+ 필수 공개 조건 충족
```

### Fit

자격이 있는 장비가 고객의 가치관에 얼마나 맞는지 설명한다.

```text
craftsmanship_grade
+ lineage_affix
+ secondary_affixes
+ special_affix/evolution
+ enhancement_level
+ chronology/fate
+ customer value tags
```

- Fit은 0~100 정규화 점수와 이유 목록을 제공한다.
- 점수만 표시하지 않고 긍정·부정 요인을 최소 1개씩 공개한다.
- 낮은 Fit도 eligibility를 충족하면 판매 가능하다.
- 화면은 자동 추천·자동 선택·숨은 정답 표시를 하지 않는다.
- 모닥은 결과나 최적 장비를 예측하지 않는다.

## 6. 인계 트랜잭션

```text
1. 계약·장비·소유권·Fit 재검증
2. DeliveryIntent PREPARED 저장
3. 장비 소유권 이전·보상·관계 변화 계산
4. EquipmentWorldRegistry record 생성
5. 계약 RESULT_PENDING 전환
6. 변경 상태 + ResultEnvelope APPLIED 동일 revision 저장
7. 결과 화면 표시
```

- `delivery_transaction_id`는 한 번만 적용한다.
- 장비는 플레이어 보관함에서 제거되더라도 Registry와 연대기에 남는다.
- 저장 실패 시 소유권·골드·관계가 부분 적용되지 않는다.

## 7. 유형별 세계 결과 Profile

공통 Resolver는 `world_outcome_profile_id`와 장비 Snapshot을 입력받는다. 유형별 Profile은 결과 후보·가중치·설명 템플릿만 제공한다.

### 수집가

- 전시 성공
- 감정가 상승
- 기록 발견
- 보존 중 손상
- 분실·회수

주요 출력: 전시 명성, 수집가 관계, 장비 역사 태그, 소유·운명 변화.

### 모험가

- 탐사 성공
- 희귀 자원 발견
- 위험 탈출
- 장비 전투 흔적
- 분실·회수

주요 출력: 탐험 명성, 재료 획득, 모험가 관계, 장비 운명.

### 검투사

- 경기 승리·패배
- 관중 반응
- 라이벌 사건
- 장비 파손·전투 흔적
- 개인 명작 선언

주요 출력: 투기장 명성, 검투사 관계, 장비 사건·운명.

### 군인

- 임무 성공·실패
- 부대 생존 기여
- 보급 평가
- 표창·징계
- 장비 분실·회수·영구 파괴

주요 출력: 군사 명성, 군인 관계, 보급 거래 해금, 장비 운명.

### 공통 금지

- 결과 유형마다 별도 저장 구조 사용
- 고객 이름을 코드에 switch 하여 결과 분기
- 같은 event ID 재적용
- 결과 화면 진입 때 RNG 재호출
- 장비 운명과 소유권 변경을 Envelope 밖에서 별도 저장

## 8. 세계 결과 상태

```text
NONE
PENDING
RESULT_READY
PRESENTED
ACKNOWLEDGED
RESULT_ERROR
```

결과는 `BS-SAVE-20260801-01`의 ResultEnvelope와 연결한다. Resolver 실패는 결과를 재추첨하지 않고 `RESULT_ERROR`와 원인 코드를 저장하며, 동일 event commitment로 재처리한다.

## 9. 고객 화면 계약

### Customer Board

- 활성 요청 최대 2개
- 4유형 필터
- 이름·역할·기한·장비 범주·보상 종류·상태
- 조건이 부족하면 이유 표시

### Request Detail

- 필수 조건과 선호 조건 분리
- 고객 가치관·관계·기한
- 적합도 계산 전 후보 장비를 자동 정렬하지 않음

### Delivery Selection

- eligibility 충족 장비만 선택 가능
- 각 장비의 Fit·긍정·부정 이유 표시
- 현재 소유권과 인계 후 변화를 명시
- 최종 버튼: `이 장비를 인계한다`

### World Result

- 장비가 무엇을 했는지
- 소유권·운명·관계·명성·자원 변화
- 연대기 항목
- 다음 행동

공통 ResultEnvelope Overlay 또는 Shell 내 전체 화면 View를 사용한다.

## 10. 저장 계약

CampaignSnapshot에 다음을 포함한다.

```text
customer_def_version
active_contracts
contract_history
customer_relationships_by_id
customer_offer_rotation_state
world_result_commitments
```

- 정의 데이터는 저장하지 않고 version과 ID만 저장한다.
- 계약 생성 당시 조건 Snapshot은 이후 데이터 조정에도 보존한다.
- 고객 ID migration ledger를 둔다.
- `gladiator_kyle → KYLE_VAREN` 이전은 한 번만 수행한다.

## 11. 콘텐츠 최소 범위

### Vertical Slice

- 카시아: 검투사 대표 완주
- 에르사: 수집가 공통 파이프라인 재사용 증명
- 나디아: 모험가 Profile 데이터 분리 증명
- 마레크: 군인 Profile 데이터 분리 증명

토렌·카일·세드릭·리아나는 이름 고객 데이터와 계약 fixture까지 포함하며 전체 전용 연출은 본제작 범위다.

### Production 목표

- 유형별 3명 이상 확장 가능
- 고객 추가가 엔진 코드 수정 없이 데이터 추가로 끝남
- 유형별 결과 Profile 후보 다양화

## 12. 테스트 매트릭스

1. 8명 customer ID uniqueness
2. 유형별 최소 2명
3. 활성 요청 최대 2개
4. exact item ID 없이 범주 eligibility
5. 낮은 Fit 장비도 판매 가능
6. 자동 추천·자동 선택 없음
7. 동일 delivery transaction 이중 보상 0
8. 동일 world event 이중 적용 0
9. 카시아·에르사·나디아·마레크가 같은 pipeline 사용
10. customer ID를 바꿔도 Core Engine 파일 수정 없음
11. 결과 중 종료 후 동일 ResultEnvelope 복구
12. legacy Kyle 관계·계약·장비 history 보존
13. 소유권·관계·보상·Registry가 같은 save revision에 반영
14. Resolver 오류 후 RNG 재추첨 0

## 13. 감사 판정

```text
BS-AUD-F07_PLANNING_TARGET: RESOLVED
BS-AUD-F08_PLANNING_TARGET: RESOLVED
BS-AUD-F09_CUSTOMER_INTEGRATION_TARGET: RESOLVED
SHEET-F05: RESOLVED_BY_NAMED_CUSTOMERS
RUNTIME_CUSTOMER_PIPELINE: NOT_RUN
CONTENT_FIXTURES: NOT_RUN
AUTOMATED_TESTS: NOT_RUN
P0_FINDING_COUNT: 유지
```

## 14. 현재 Gate

```text
CUSTOMER_TYPES: 4 APPROVED
NAMED_CUSTOMERS_MINIMUM: 8 APPROVED
COMMON_PIPELINE: APPROVED
ELIGIBILITY_VS_FIT: APPROVED
RELATIONSHIP_BY_CUSTOMER_ID: APPROVED
WORLD_OUTCOME_PROFILES: APPROVED
LEGACY_KYLE_MAPPING: APPROVED
PRODUCT_CODE_CHANGE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
