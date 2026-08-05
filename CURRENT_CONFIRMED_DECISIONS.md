# [현재 정본] Blacksmith Current Confirmed Decisions

> R2 체크포인트 003: PR `#103` / closure `#104` / canon audit `#105`
>
> R2_CHECKPOINT_004 planning: PR `#106` / exact head `227b2dabf0d98832811415156e72f65d601332a9` / squash merge `789c73f38003f40dde5e9a99cd7dcb3ca03863f7`
>
> R2_CHECKPOINT_004 closure: PR `#107` / exact head `1ad791123eaf6c727e964380814ffb69f1357bbf` / squash merge `7a46fa38586a42f268cd0432744203049649ddd5`
>
> 폐쇄 배치: `R2_BATCH_004_CLOSED_2_OF_10 / CLOSED_MERGED_PR107`
>
> 현재 승인 배치: `R2_BATCH_005 / 5/10`
>
> 제품 구현: `BLOCKED`

## 1. 프로젝트 코어

> 제한된 하루 작업량 안에서 작품을 만들고, 강화 위험 앞에서 멈출지 더 도전할지 선택하며, 작품이 고객과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
직접 단조와 출생 등급
→ 강화 성공·실패와 멈춤 판단
→ 정밀강화 방식·촉매 선택
→ 고객·세계에 작품 전달
→ 같은 UID의 연대기·손상·복원 결과
→ 다음 제작·강화 판단
```

## 2. 현재 승인 Decision

- `BS-WORLD-20260803-03`: 고객 개인 일정과 날짜 예고형 세계 일정 분리
- `BS-CUSTOMER-20260803-02`: 위험도·능력치 `1~10`, 예상 성공률 `5~95%`
- `BS-CUSTOMER-20260805-01`: 근력·기량·체력·판단력, 희소 무기·갑옷 적성, 마력 적성, 장비 적합성 — `R2_BATCH_005_2_OF_10 / APPROVED_PENDING_MERGE`
- `BS-UX-20260805-01`: 모바일 고객 카드 3단계 정보 공개와 설명 가능한 장비 판단 — `R2_BATCH_005_3_OF_10 / APPROVED_PENDING_MERGE`
- `BS-CUSTOMER-20260806-01`: 강화 중심 단순 장비 판정과 근력 기반 최대 중량 게이트 — `R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE`
- `BS-ITEM-20260806-01`: 장비군 고정 기본 중량 포인트와 중량 전용 ±5 강화 효과 — `R2_BATCH_005_5_OF_10 / APPROVED_PENDING_MERGE`
- `BS-SCHEDULE-20260804-01`: 주요 일정·소식·묶음 요약·일정 장부
- `BS-CONTENT-20260804-01`: 고객 결과·작품 UID 상태·다음 제작 환류
- `BS-CONTENT-20260804-02`: 검투사·모험가·군인·귀족과 초기 콘텐츠 가족
- `BS-CRAFT-20260804-04`: 보조재료 제거와 정밀강화 방식·촉매 책임 분리
- `BS-CRAFT-20260804-05`: 촉매 수식어 씨앗·계보·진화
- `BS-CRAFT-20260804-06`: `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`
- `BS-CRAFT-20260804-07`: 제작 등급 5단계와 출생 전설 고정 — `MERGED_PR106 / MAIN_CANON`
- `BS-CRAFT-20260805-01`: 예술성을 고정 설계 최대치 없는 숫자형 무기·작품 능력치로 확정 — `MERGED_PR106 / MAIN_CANON`
- `BS-CRAFT-20260805-02`: 예술성 초기 생성·후천 성장·가치 점감·고객 선호 경계 — `R2_BATCH_005_1_OF_10 / APPROVED_PENDING_MERGE`
- `BS-UX-20260804-01`: 조합 장비명과 UID 연대기 상세
- `BS-OPS-20260804-02`: 정본 드리프트·구형 문서 상태 관리
- `BS-OPS-20260805-01`: 벤치마킹·조기 체크포인트·상시 TDD

## 3. 제작 등급

```text
[보통] → [우수] → [명품] → [걸작] → [전설]
```

- 최초 직접 단조 완료 시 한 번 확정
- 동일 UID에서 영구 고정
- 제작 후 승격·강등 없음
- `전설`은 최초 제작에서만 극희귀하게 발생
- 제작 등급은 예술성 최소값·상한·배율을 결정하지 않음
- 정확한 확률·배율은 `BASELINE_TEST_PRESET`

## 4. 예술성 원수치

```text
예술성 27
```

- 무기·작품 능력치의 하나
- `0` 이상의 정수, 소수점 없음
- 고정 설계 최대치 없음
- 분모·별점·백분율·예술성 단계명 없음
- 제작 등급과 별도 축
- 다른 능력치와 함께 원수치 표시
- 전투 성능을 기본적으로 올리지 않음
- 범용 전투력·수식어 배율이 아님
- 기술적 자료형 한계는 콘텐츠 최대치가 아님

```text
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

## 5. 예술성 생성·성장·가치 평가

```text
artistry = 작품 UID에 저장되는 원수치
artistry_value = 시장·감정 맥락의 파생 점감 가치
customer_artistry_fit = 고객·일정 맥락의 파생 적합도
```

### 최초 제작 허용 원천

```text
BASE_ITEM_DESIGN_AESTHETIC_TENDENCY
MATERIAL_VISUAL_PROCESSING_FIT
DIRECT_FORGING_AESTHETIC_RESULT
```

- 재료 가격·희귀도 자체는 예술성으로 직접 변환하지 않음
- 제작 등급을 예술성 보너스표로 변환하지 않음
- 별도 보조재료·장식재료 슬롯을 추가하지 않음

### 제작 후 허용 성장 원천

```text
ARTISTIC_FINISH
ARTISTRY_OWNED_CATALYST_EFFECT
APPROVED_FINISHING_OR_DECORATION_CONTENT
MEANINGFUL_ARTISTIC_REWORK
```

다음은 예술성을 자동 증가시키지 않는다.

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

### 가치 평가

```text
최종 가치
= 기능 가치
+ 제작 등급 가치
+ 예술성 점감 가치
+ 촉매 수식어 가치
+ 연대기 가치
+ 고객·시장 수요 보정
```

```text
ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE
```

- 예술성이 증가하면 가치 기여는 감소하지 않음
- 높은 구간일수록 추가 1점의 한계 가치는 작아짐
- 원수치는 압축하지 않음
- 구간별 한계 가치 테이블을 우선
- 제작 등급·재료·예술성·촉매·연대기의 연속 곱셈 금지
- 같은 원인의 이중 계산 금지

### 고객 관심 유형

```text
IGNORE / SECONDARY / PRIMARY / REQUIREMENT
```

예술성에 관심 없는 고객은 초과 예술성에 추가 비용을 지불하지 않을 수 있지만, 높은 예술성 자체에 패널티를 주지 않는다.

### 악용 방지

- 수리·손상·판매·전시·감정·증여 반복으로 예술성 순증가 금지
- 동일 저비용 세공 반복 파밍 금지
- 촉매 직접 증가와 가격·수식어 배율의 이중 계산 금지
- 연대기·명성은 예술성 원수치를 자동 변경하지 않음
- 모든 예술성 변화는 작품 UID와 출처를 기록

정확한 초기 분포·증감값·가격 구간·고객 요구치는 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 6. 고객 능력·장비 적합성

```text
근력 / 기량 / 체력 / 판단력 = 각 1~10
무기 적성 / 갑옷 적성 = 희소 저장, 0~3
마력 적성 = 0~10, 선택 친화 태그 최대 2개
```

작품 종류는 `WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL`로 분리한다. 공통 작품 능력치는 `WEIGHT / DURABILITY / HANDLING / ARTISTRY`, 조건부 능력치는 `ATTACK / DEFENSE / STABILITY / ENVIRONMENTAL_RESPONSE / SPECIAL_FUNCTIONS`다. 적용되지 않는 수치는 생략한다.

현재 착용 조합에서 `TOTAL_WEIGHT / COMFORTABLE_LOAD / BALANCE_STATE / SPECIAL_FUNCTION_FIT`을 파생한다. 균형 상태는 `부적합 / 불안정 / 안정 / 능숙`이며, 적정 하중 이내에는 중량 페널티가 없고 초과 시 단계적으로 부담이 증가한다.

고객 능력은 작품 공격·방어 값을 직접 다시 더하지 않는다. 작품 원수치는 UID에 남고 고객 능력·적성은 활용도·위험·예상 성공률을 조정한다. 정확한 공식은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 7. 작품 이름과 수식어

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

연대기 수식어를 누르면 같은 UID의 형성 사건·주요 타임라인·진화 계보·소유·손상·복원 기록을 읽기 전용 하단 패널에서 확인한다.

## 8. 운영 계약

- 질문·추천·새 시스템 설계 전 벤치마킹·현업 비교
- 결과를 `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성`으로 기록
- 승인 10건은 최대 배치 크기
- `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT` 조기 체크포인트 허용
- 작업마다 TDD: `RED → GREEN → REFACTOR`
- 병합은 명시적 사용자 승인 필요

현재 `R2_BATCH_005 / 2/10`이다.

## 9. 보호 조건

- 일반 수식어 A·B 재도입 금지
- 보조재료 슬롯 재도입 금지
- 세 수식어 교차 생성·진화·덮어쓰기 금지
- 제작 등급 후천 변경 금지
- 예술성 고정 설계 최대치·분모 표기·named tier 재도입 금지
- 예술성을 범용 전투력·수식어 배율로 변환 금지
- 예술성·연대기·명성을 하나의 영구 총점으로 통합 금지
- 제품 구현: `BLOCKED`

<!-- BS-UX-20260805-01 -->
## 모바일 고객 카드 정보 계층

```text
기본 카드 → 장비 선택 후 판단층 → 상세 보기
```

- 기본: 고객 역할·일정, 4능력치, 관련 주·보조 적성, 관련 시 마력 적성
- 장비 선택 후: 균형·예상 성공률·핵심 원인 2~4개·관련 특수기능 위험
- 상세: 전체 관련 적성, 총 중량·적정 하중, 특수기능 근거, 적용 능력치
- 전체 적성 행렬 기본 노출 금지
- 불투명한 결과 전용 적합도 점수 금지
- 색상·길게 누르기·호버 단독 핵심 정보 금지
- 최소 `48dp` 터치 목표
- 제품 구현: `BLOCKED`

<!-- BS-CUSTOMER-20260806-01 -->
## 강화 중심 단순 장비 판정

```text
최대 중량 = 근력 × 10
총 중량 ≤ 최대 중량 → 사용 가능, 보너스·페널티 없음
총 중량 > 최대 중량 → 중량 초과, 배정 불가
```

```text
위험도 기본 성공률
+ 강화 레벨(+1당 +1%p)
+ 관련 능력 충족(+5%p)
+ 적성 보정(-10/0/+5/+10%p)
```

- 강화가 주효과이며 고객 능력·적성은 작은 보조 보정이다.
- `COMFORTABLE_LOAD / BALANCE_STATE / 단계적 초과 페널티`는 현재 중량 계약이 아니다.
- 공격·방어·조작성·예술성 원수치를 일반 성공률에 범용 합산하지 않는다.
- 제품 구현: `BLOCKED`

<!-- BS-ITEM-20260806-01 -->
## 장비군 기본 중량 포인트

```text
장신구 0 / 도구 5
의복·로브 5 / 경갑 10 / 중갑 20 / 중장갑 30
검·원거리·방패보조 10 / 도끼·둔기 15 / 장병기 20
```

`ITEM_WEIGHT = max(0, BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER)`다. 중량 전용 효과는 작품당 하나만 허용하며 `LIGHTWEIGHT -5 / NONE 0 / WEIGHTED +5`다. 재료·제작 등급·예술성·공격·방어·조작성·내구도·일반 강화 단계는 중량을 자동 변경하지 않는다. 제품 구현: `BLOCKED`.
