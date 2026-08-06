# Blacksmith R2 예술성 고정 상한 없는 수치형 무기 능력치 정본

- Decision ID: `BS-CRAFT-20260805-01`
- 상태: `USER_APPROVED_REFINED_MERGED_PR106 / R2_CHECKPOINT_004_MAIN_CANON`
- 후속 책임 정제: `BS-CRAFT-20260805-02 / R2_BATCH_005_1_OF_10 / APPROVED_PENDING_MERGE`
- 후속 정본: `docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md`
- 제품 구현: `BLOCKED`

## 결정

```text
field: artistry
conceptual type: non-negative integer
minimum: 0
fixed design maximum: none
named tiers: none
```

대표 원수치 표기: `예술성 27`.

- `0` 이상의 정수
- 소수점 없음
- 고정 설계 최대치 없음
- 분모·별점·백분율 표기 없음
- 예술성 단계명 없음
- 다른 무기 능력치와 같은 영역에 원수치 표시
- 기술적 자료형 한계는 콘텐츠 최대치가 아님

`예술성 0`은 미완성품이나 사용 불가가 아니라 미적 투자가 거의 없는 정상 기능품이다.

## 책임

예술성은 조형 완성도, 표면 마감과 세공, 장식 구성과 조화, 작품으로서의 인상에 관한 작품 UID 원수치다.

```text
제작 등급 = 최초 단조의 기술적 완성도
예술성 = 누적 가능한 미적·작품 능력치
촉매 수식어 = 정밀강화 선택과 촉매 계보
연대기 수식어 = 실제 작품 생애
```

```text
[전설] 운철 전투도끼 / 예술성 3
[보통] 은제 의장검 / 예술성 87
```

- 제작 등급은 예술성 최소값·고정 상한·배율을 만들지 않음
- 예술성은 네 번째 수식어 슬롯이 아님
- 예술성은 전투 성능을 기본적으로 올리지 않는다.
- 범용 전투력·수식어 배율이 아님

## 생성·성장 책임

`BS-CRAFT-20260805-02`가 생성·성장 원천을 다음처럼 제한한다.

최초 제작:

```text
BASE_ITEM_DESIGN_AESTHETIC_TENDENCY
MATERIAL_VISUAL_PROCESSING_FIT
DIRECT_FORGING_AESTHETIC_RESULT
```

제작 후:

```text
ARTISTIC_FINISH
ARTISTRY_OWNED_CATALYST_EFFECT
APPROVED_FINISHING_OR_DECORATION_CONTENT
MEANINGFUL_ARTISTIC_REWORK
```

일반 강화 레벨, 판매, 증여, 전시, 감정, 소유권 이전, 명성, 연대기 사건은 예술성 원수치를 자동 증가시키지 않는다.

## 가치·고객 책임

```text
artistry_value = 시장·감정 맥락의 파생 점감 가치
customer_artistry_fit = 고객·일정 맥락의 파생 적합도
```

두 값은 새 영구 능력치가 아니다.

```text
ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE
```

- 원수치는 그대로 표시
- 예술성 가치 기여는 증가하되 높은 구간일수록 한계 가치가 작아짐
- 구간별 한계 가치 테이블 우선
- 고객 관심 유형: `IGNORE / SECONDARY / PRIMARY / REQUIREMENT`
- 관심 없는 고객은 초과 예술성에 추가 지불하지 않을 수 있으나 패널티를 받지 않음
- 같은 원인의 이중 계산과 전체 가치 곱셈 중첩 금지

## 변화 이력과 악용 방지

모든 예술성 변화는 작품 UID에 출처·변화 전 값·증감·결과값을 남긴다.

금지:

- 수리·손상·판매·전시·감정·증여 반복 순증가
- 동일 저비용 행동 반복 상승
- 제작 등급·재료 가격의 자동 예술성 배율
- 촉매 직접 증가와 가격·수식어 배율의 이중 계산
- 예술성·연대기·명성을 하나의 영구 총점으로 통합

## 대체·미확정

동일 Decision의 초기 bounded-stat 초안과 named-tier 프리셋은 `[대체됨]`이다.

```text
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

다음은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

- 최초 제작 분포와 작품 종류별 범위
- 재료 적합성 태그·기여량
- `ARTISTIC_FINISH`와 촉매 증감·비용·성공률
- 구간별 한계 가치 경계·계수
- 고객별 요구치·선호 구간
- 손상·복원 계산
- 저장 자료형·overflow 보호

## 적대적 보호 조건

- 고정 설계 최대치·분모·named tier 재도입 금지
- 예술성 0을 미완성·사용 불가와 동일시 금지
- 제작 등급이 예술성 상한을 결정하게 하지 않음
- 예술성을 범용 전투력·수식어 배율로 변환 금지
- 구체적 점감·분포를 사용자 승인 없이 제품값으로 고정하지 않음
- 제품 구현은 계속 `BLOCKED`
