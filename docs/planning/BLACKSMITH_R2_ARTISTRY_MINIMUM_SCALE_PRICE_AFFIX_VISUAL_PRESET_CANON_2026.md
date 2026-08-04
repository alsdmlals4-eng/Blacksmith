# [부분 대체됨] Blacksmith R2 예술성 표시·가격·시각 프리셋

- 원 Decision: `BS-CRAFT-20260804-02`
- 정제 Decision: `BS-CRAFT-20260805-01`
- 현재 대체 문서: `docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md`
- 제품 구현: `BLOCKED`

## 현재 유지되는 계약

- 예술성은 `0` 이상의 정수이며 소수점 없음
- 고정 설계 최대치 없음
- 대표 원수치 표기: `예술성 27`
- 예술성 단계명·분모·별점·백분율 없음
- 강화 단계만으로 자동 상승하지 않음
- 판매·감정 가치와 귀족·후원자·수집가·전시·증여·의식 수요에 기여 가능
- 실용 성능과 별도 축
- 높은 예술성이 모든 고객·상황의 최적해가 되어서는 안 됨
- 정확한 기대 범위·점감·계수는 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`

## [대체됨] 초기 bounded 모델과 named tier

다음은 역사적 초기 초안이며 현재 표시 계약이 아니다.

```text
INTEGER_1_TO_10_WEAPON_ITEM_STAT_NO_NAMED_TIERS
BASIC 1~2
REFINED 3~5
MASTERWORK 6~8
MASTERPIECE 9~10
```

정확한 역사 상태는 `BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`이 책임진다.

현재 기계 계약:

```text
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

## 가격·수식어·시각 경계

- 화면에는 예술성 원수치를 그대로 표시한다.
- 판매·감정·고객 선호에는 콘텐츠별 기대 범위·선호 구간·점감 함수를 적용할 수 있다.
- 예술성은 모든 속성을 일괄 증폭하는 범용 품질 배율이 아니다.
- 예술성 관련 촉매·정밀강화 방식은 예술성 값이나 경향에 영향을 줄 수 있지만 `GRADE_AFFIX`를 변경하지 않는다.
- 제작 등급은 예술성의 고정 상한을 만들지 않는다.
- 실루엣과 기능 판독성을 보존한다.
- 금색·보석·광원만으로 높은 예술성을 표현하지 않는다.
- 색상만으로 수치 차이를 전달하지 않는다.

## 상태

이 문서는 가격·수요·시각 경계와 초기 모델의 역사 설명으로만 사용한다. 예술성의 현재 표시·도메인·능력치 책임은 `BS-CRAFT-20260805-01` 정본이 우선한다.
