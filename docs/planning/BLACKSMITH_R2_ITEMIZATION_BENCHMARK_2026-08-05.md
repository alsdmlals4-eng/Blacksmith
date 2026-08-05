# Blacksmith R2 아이템화 벤치마킹·현업 비교

- 기준일: `2026-08-05`
- 관련 Decision: `BS-CRAFT-20260804-07`, `BS-CRAFT-20260805-01`, `BS-CRAFT-20260805-02`, `BS-OPS-20260805-01`
- 용도: 설계 입력·적대적 비교
- 제품 구현: `BLOCKED`

## 비교 대상

### Diablo IV

공식 아이템화 자료는 아이템의 기본 성능·속성·담금질·명품화와 같은 후천 성장 책임을 여러 정보 축으로 분리한다. 2.5 패치에서는 아이템 품질이 높아질수록 명품화 비용이 지수적으로 증가한다고 명시한다.

- 채택: 이름이 붙는 등급과 숫자형 능력치를 분리하는 정보 구조
- 채택: 기본 상태와 후천 제작·성장 출처의 분리
- 수정 채택: 높은 성장 구간일수록 추가 비용과 한계 효율을 다르게 설계하는 방향
- 비채택: 예술성 숫자가 모든 속성을 일괄 증폭하는 범용 품질 배율
- 비채택: Diablo의 품질 상한이나 전체 속성 증폭 방식을 예술성에 직접 이식

참고:

- https://news.blizzard.com/en-us/article/24077223/galvanize-your-legend-in-season-4-loot-reborn
- https://news.blizzard.com/en-gb/article/24244466/diablo-iv-patch-notes-2-5

### Path of Exile

공식 아이템 필터 문서는 아이템 레벨·지역 레벨·소켓 수 등 여러 숫자값을 비교 연산자로 다룬다.

- 채택: 이름이 붙는 상태와 별개로 비교 가능한 원수치 정보 구조
- 수정 채택: 예술성도 `예술성 27`처럼 분모 없이 표시
- 비채택: 필터 문법이나 특정 수치 범위를 게임 디자인 최대치로 직접 이식

참고:

- https://www.pathofexile.com/forum/view-thread/2771031

### Dwarf Fortress

Dwarf Fortress는 물건 형태·재료·제작 품질과 장식 가치를 구분해 가치에 반영한다. 현재 Wiki의 가치 설명도 물건·재료·제작 품질의 곱에 장식 가치를 더하는 구조를 설명한다.

- 채택: 제작 기술 완성도와 장식·세공 가치가 서로 다른 원인으로 기여하는 방향
- 채택: 장식과 작품 본체의 가치 출처를 추적할 수 있는 구조
- 수정 채택: Blacksmith에서는 재료·등급·예술성·촉매·연대기를 각각 한 번만 반영
- 비채택: 여러 가치 축의 연속 곱셈으로 후반 가격이 급팽창하는 구조
- 이유: Blacksmith는 작품 가치의 원인을 설명하고 개별 축을 독립적으로 조정할 수 있어야 함

참고:

- https://dwarffortresswiki.org/index.php/Item_quality
- https://dwarffortresswiki.org/index.php/Item_value

### Guild Wars 2

Guild Wars 2 Wiki는 반복 가능한 같은 활동이 경제와 정상 플레이를 해치는 것을 막기 위해 특정 활동·지역·반복 경로에 감소 보상을 적용하며, 일반적인 정상 플레이에서는 드물게 체감하도록 설계됐다고 설명한다.

- 채택: 반복 악용 가능성이 있는 **특정 출처**에만 점감·제한 적용
- 수정 채택: 수리·전시·감정·판매·저비용 세공 같은 동일 원천 반복에는 순증가 금지 또는 별도 제한 적용
- 비채택: 정상적인 제작·고객·세계 활동 전체를 묶어 보이지 않는 광역 점감 적용
- 이유: 플레이어가 예술성 변화 원인을 설명할 수 있어야 하며 정상적인 다양한 플레이를 처벌하면 안 됨

참고:

- https://wiki.guildwars2.com/wiki/Diminishing_returns

## Blacksmith 채택 구조

```text
제작 등급 5단계 = 출생 기술 완성도
예술성 = UID에 저장되는 고정 상한 없는 원수치
artistry_value = 시장·감정 맥락에서 계산되는 파생 점감 가치
customer_artistry_fit = 고객·일정 맥락에서 계산되는 파생 적합도
촉매 수식어 = 플레이어 정밀강화 선택의 흔적
연대기 수식어 = 실제 작품 생애
```

대표 표시:

```text
예술성 27
```

### 생성·성장 원천

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

일반 강화·판매·증여·전시·감정·소유권·명성·연대기는 예술성 원수치를 자동 증가시키지 않는다.

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

- 예술성 원수치는 압축하지 않음
- 경제 평가에서 높은 구간의 한계 가치가 감소
- 구간별 data table을 우선
- 동일 원인 이중 계산 금지
- 가치 구성요소 전체 곱셈 중첩 금지

### 고객 관심

```text
IGNORE / SECONDARY / PRIMARY / REQUIREMENT
```

관심 없는 고객은 초과 예술성에 추가 지불하지 않을 수 있지만 높은 예술성 자체에 패널티를 주지 않는다.

## 현업식 채택·수정·거절 판정

- Adopt: named grade와 raw numeric stat의 분리
- Adopt: 제작 품질·장식·후천 성장의 원인 분리
- Adapt: 예술성 원수치는 유지하고 시장·감정 가치에서 구간별 한계 가치 점감
- Adapt: 반복 악용 제한은 특정 원천에만 적용
- Reject: 예술성을 전투 전체 증폭 배율로 사용
- Reject: 희귀도·품질·예술성·연대기·명성을 하나의 영구 총점으로 합산
- Reject: 재료·등급·예술성·촉매·연대기의 연속 곱셈
- Reject: 정상 플레이 전체를 처벌하는 불투명한 광역 점감
- Differentiation: 같은 UID의 출생 등급·미적 투자·촉매 선택·실제 생애와 시장 맥락을 독립적으로 설명
- Remaining uncertainty: 초기 분포·증감량·가격 점감 구간·고객 요구치·손상/복원·저장 자료형은 별도 승인

## 이후 벤치마킹 운영

질문·추천·새 시스템 확정 전 다음을 수행한다.

1. 비교할 현업 사례와 유사 게임을 찾는다.
2. 표면 기능이 아니라 플레이어 판단·정보 구조·제작 비용을 비교한다.
3. `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성`으로 기록한다.
4. 프로젝트 코어와 충돌하면 유명 사례라도 채택하지 않는다.
5. 출처와 확인 날짜를 정본 또는 PR 증거에 남긴다.
