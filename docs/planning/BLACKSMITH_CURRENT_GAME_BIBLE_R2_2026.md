# [현재 정본] Blacksmith R2 통합 Game Bible

- 상태: `CURRENT_CANON / R2_BATCH_005_9_OF_10`
- 체크포인트 004: `PR106_HEAD_227b2dabf0d98832811415156e72f65d601332a9 / MERGE_789c73f38003f40dde5e9a99cd7dcb3ca03863f7 / MAIN_CANON`
- 현재 Decision: `BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / BS-CRAFT-20260805-02 / BS-CUSTOMER-20260805-01 / BS-UX-20260805-01 / BS-CUSTOMER-20260806-01 / BS-ITEM-20260806-01 / BS-OPS-20260805-01` / BS-ITEM-20260806-03 / BS-ITEM-20260806-04 / BS-ITEM-20260806-05
- 제품 구현: `BLOCKED`

## 1. 프로젝트 약속

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품을 만들고, 강화 위험 앞에서 멈출지 더 도전할지 선택하며, 작품이 고객과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
강화의 즉각 판단
→ 작품에 제작자의 선택을 새김
→ 고객과 세계에 보냄
→ 같은 UID 작품의 생애 결과를 돌려받음
→ 다음 강화·복원·제작 이유가 생김
```

## 2. 작품 구조

```text
작품 UID
├─ 작품 종류·주재료·기본 작품명
├─ 제작 등급·GRADE_AFFIX
├─ 공격·방어·내구·조작성·예술성 등 능력치
├─ 강화 단계·방식 이력·촉매 이력
├─ CATALYST_AFFIX
├─ CHRONICLE_AFFIX
└─ 소유·사건·손상·복원·계승 기록
```

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

일반 수식어 A·B 구조 재도입 금지. 보조재료 슬롯 재도입 금지.

## 3. 제작 등급

```text
[보통] → [우수] → [명품] → [걸작] → [전설]
```

- 최초 직접 단조 완료 시 한 번 확정
- 동일 UID에서 영구 고정
- 제작 후 승격·강등 없음
- 제작 등급은 예술성 최소값·상한·배율을 결정하지 않음
- 과거 `STANDARD / GOOD / PERFECT`는 역사 구현이며 현재 5단계 제품 구현이 아님
- 과거 3단계 구현 PASS를 현재 5단계 제품 구현 PASS로 해석 금지

## 4. 예술성 원수치

대표 원수치 표기: `예술성 27`.

- `0` 이상의 정수, 소수점 없음
- 고정 설계 최대치 없음
- 분모·별점·백분율·예술성 단계명 없음
- 다른 능력치와 함께 원수치 표시
- 전투 성능을 기본적으로 올리지 않음
- 범용 전투력·수식어 배율이 아님
- 기술적 자료형 한계는 콘텐츠 최대치가 아님

```text
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

`예술성 0`은 정상 기능품이다. `[전설] / 예술성 3`과 `[보통] / 예술성 87`이 모두 가능하다.

## 5. 예술성 생성·성장·가치 평가

```text
artistry = UID에 저장되는 원수치
artistry_value = 시장·감정 맥락의 파생 점감 가치
customer_artistry_fit = 고객·일정 맥락의 파생 적합도
```

최초 제작 허용 원천:

```text
BASE_ITEM_DESIGN_AESTHETIC_TENDENCY
MATERIAL_VISUAL_PROCESSING_FIT
DIRECT_FORGING_AESTHETIC_RESULT
```

제작 후 허용 성장 원천:

```text
ARTISTIC_FINISH
ARTISTRY_OWNED_CATALYST_EFFECT
APPROVED_FINISHING_OR_DECORATION_CONTENT
MEANINGFUL_ARTISTIC_REWORK
```

자동 증가 금지:

```text
GENERAL_ENHANCEMENT_LEVEL / SALE / GIFT / EXHIBITION_COUNT
APPRAISAL_COUNT / OWNERSHIP_TRANSFER / FAME / CHRONICLE_EVENT
LOW_COST_REPEAT_ACTION
```

가치 구조:

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

- 예술성 가치 기여는 단조 증가하고, 높은 구간일수록 한계 가치가 작아짐
- 원수치는 압축하지 않음
- 구간별 한계 가치 테이블을 우선
- 같은 원인의 이중 계산과 전체 곱셈 중첩 금지
- 고객 관심 유형은 `IGNORE / SECONDARY / PRIMARY / REQUIREMENT`
- 관심 없는 고객은 초과 예술성에 추가 지불하지 않을 수 있으나 패널티는 주지 않음
- 수리·손상·판매·전시·감정·증여·저비용 반복으로 예술성 순증가 금지
- 모든 변화는 작품 UID와 출처를 기록

정확한 분포·증감값·가격 구간·고객 요구치는 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 6. 강화와 촉매

일반 강화는 한 입력에 한 결과다.

```text
+10 / +20 / +30 / +40 / +50
주재료 맥락 + 강화 방식 + 촉매 한 개
```

촉매 수식어는 `EMPTY → SEED → DEVELOPED → EVOLVED → MASTERED`로 성장한다. 무관한 계보로 무작위 교체하거나 같은 이정표를 무한 리롤하지 않는다.

## 7. 연대기와 장비명

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

연대기 수식어를 누르면 UID 기반 읽기 전용 상세를 연다. 연대기 사건은 예술성 원수치를 자동 변경하지 않는다.

## 8. 고객·장비 적합성·일정·콘텐츠

고객 능력과 사건 위험도는 `1~10`, 예상 성공률은 `5~95%`다. 고객 기초 능력은 `근력 / 기량 / 체력 / 판단력`, 무기·갑옷 적성은 희소 `0~3`, 마력 적성은 `0~10`이다.

```text
WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL
```

작품 원수치는 작품 UID에 남고, 고객 능력·적성·중량 상태·특수기능 조건으로 고객·장비 적합성을 파생한다. `TOTAL_WEIGHT / COMFORTABLE_LOAD / BALANCE_STATE / SPECIAL_FUNCTION_FIT`은 착용 조합마다 다시 계산한다. 고객 능력치를 작품 공격·방어에 직접 중복 합산하지 않는다.

모든 콘텐츠는 고객 결과, 작품 UID 상태·유산, 다음 제작·강화·복원 판단을 남겨야 한다. Decision: `BS-CUSTOMER-20260805-01`.

## 9. 운영 방법

- 질문·추천·설계 전 벤치마킹·현업 비교
- 승인 10건은 최대 배치 크기
- 현재 `R2_BATCH_005_7_OF_10`
- 조기 체크포인트도 적대적 감사·CI·Sheet readback 필수
- 모든 작업은 `RED → GREEN → REFACTOR`
- 명시적 사용자 승인 전 병합 금지

## 10. 검증 경계

- 제품 구현: `BLOCKED`
- 현재 5등급·예술성 생성·성장·가치 평가 제품 구현: `NOT_STARTED`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
- 과거 PoC PASS는 현재 제품 PASS가 아님

<!-- BS-UX-20260805-01 -->
## 모바일 고객 카드와 장비 판단

```text
기본 카드 → 장비 선택 후 판단층 → 상세 보기
```

고객 카드의 목적은 고객 RPG 육성이 아니라 작품을 누구에게 맡길지 설명 가능한 판단을 제공하는 것이다. 기본 카드에는 4능력치와 관련 적성만 표시한다. 작품 선택 후 균형·예상 성공률·핵심 원인 2~4개를 즉시 보여주며, 전체 관련 적성·총 중량·적정 하중·특수기능 근거는 상세 보기로 보낸다. 핵심 상태는 색상만으로 전달하지 않으며 모바일 상호작용 목표는 최소 `48dp`다. 제품 구현: `BLOCKED`.

<!-- BS-CUSTOMER-20260806-01 -->
## 강화 중심 보조 판정

강화가 주효과다. 고객 능력치·적성·작품 원수치는 작품 배정을 설명하는 보조 요소만 담당한다.

```text
MAXIMUM_LOAD = STRENGTH × 10 WEIGHT_POINT
WITHIN_LIMIT → 보너스·페널티 없음
OVERWEIGHT → 중량 초과 시 배정 불가
```

```text
최종 성공률
= 위험도 기본 성공률
+ 강화 레벨(+1당 +1%p)
+ 관련 능력 충족(+5%p)
+ 적성 보정(-10/0/+5/+10%p)
```

공격·방어·조작성·예술성은 모든 고객 사건에 자동 합산하지 않는다. 제품 구현: `BLOCKED`.

<!-- BS-ITEM-20260806-01 -->
## 장비군 고정 기본 중량

```text
ACCESSORY 0 / TOOL 5
CLOTHING_OR_ROBE 5 / LIGHT_ARMOR 10 / MEDIUM_ARMOR 20 / HEAVY_ARMOR 30
SWORD 10 / AXE 15 / BLUNT 15 / POLEARM 20 / RANGED 10 / SHIELD_SUPPORT 10
```

작품 중량은 `BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER`이며 최솟값은 0이다. 작품당 중량 전용 효과는 하나만 허용한다. 재료·제작 등급·예술성·공격·방어·조작성·내구도·일반 강화 단계는 중량을 자동 변경하지 않는다. 장비군 고정 기본 중량은 고객 배정 가능 여부만 보조하며 강화보다 중요한 성장 축이 아니다. 제품 구현: `BLOCKED`.

<!-- BS-ITEM-20260806-02 -->
## 중량 성능 예산

- 최초 제작 중량 5당 초기 성능 예산 +1.
- 경량화는 현재 중량만 5 낮추고 기존 예산과 능력치를 유지한다.
- 중량화는 현재 중량이 UID의 과거 최고 인정 중량을 넘을 때만 초과분 5당 예산 +1.
- 고객 중량 판정은 현재 중량, 성능 예산은 인정 중량을 사용한다.
- 중량 조정은 정밀강화 `+10/+20/+30/+40/+50`에서만 이정표당 한 번 가능하다.
- 공격·방어·마법 기능·유틸리티 중 한 예산점은 한 호환 축에만 배분한다.
- 일반 사건 성공률 직접 보정과 다른 성장축 배율은 금지한다.
- 제품 구현: `BLOCKED`.

<!-- BS-ITEM-20260806-03 -->
## 중량 예산 환산

```text
공격 예산 1점 = 공격 +5
방어 예산 1점 = 방어 +5
마법 기능 예산 1점 = 마법 기능 용량 +1
유틸리티 예산 1점 = 유틸리티 용량 +1
```

기본 작품 설계가 최초 제작 시 하나의 역할 프로필을 확정한다. 플레이어 자유 배분·제작 후 무료 재배분·기본 혼합 프로필은 없다. 새 최고 중량으로 얻는 예산은 기존 프로필을 따르고, 경량화는 이미 배분된 결과를 유지한다. 제품 구현: `BLOCKED`.

<!-- BS-ITEM-20260806-04 -->
## 작품 역할 원수치와 최초 기능 카탈로그

```text
SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS
무기 -> ATTACK
방패·갑옷 -> DEFENSE
도구·의복·장신구 -> 공격·방어 강제 없음
```

```text
DISPLAY_ATTACK = CRAFTED_ATTACK + WEIGHT_ATTACK_OUTPUT + APPROVED_ENHANCEMENT_ATTACK_OUTPUT
DISPLAY_DEFENSE = CRAFTED_DEFENSE + WEIGHT_DEFENSE_OUTPUT + APPROVED_ENHANCEMENT_DEFENSE_OUTPUT
```

최초 승인 마법 기능은 `ARCANE_CONDUCTION / ELEMENTAL_WARD / ARCANE_SENSING`, 유틸리티 기능은 `ENVIRONMENTAL_SEALING / FIELD_SERVICEABILITY / TASK_INTEGRATION`이다. 기능은 용량을 소비하지만 자동 생성되지 않고 일반 사건 성공률에 범용 합산되지 않는다. 제품 구현은 `BLOCKED`다.

<!-- BS-ITEM-20260806-05 CURRENT GAME BIBLE -->
## 작품 역할 수치와 통합 변동 장부

```text
CRAFTED_ROLE_STAT = max(0, 장비군 기준값 + 주재료 적합 보정 + 직접 단조 보정)
장비군 기준값 = 5 / 10 / 15
주재료 적합 = -2 / 0 / +2
직접 단조 = -1 / 0 / +1
```

일반 강화는 강화 단계와 사건 성공률만 바꾼다. 작품 공격·방어·중량·내구·취급·예술성·기능 용량·기능 목록은 자동 변경하지 않는다. 실제 작품 수치 변화는 정밀강화 `STAT_METHOD`, 기능 목록 변화는 `FUNCTION_REWORK`가 소유한다. 한 이정표에서 두 차선을 동시에 받을 수 없다.

변경은 `ITEM_CHANGE_LEDGER_ENTRY`로 기록한다. 조회용 Google Sheet 탭은 `42_능력치_강화_참조표`이며 GitHub 정본보다 우선하지 않는다. 정확한 값은 `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`, 제품 구현은 `BLOCKED`다.
