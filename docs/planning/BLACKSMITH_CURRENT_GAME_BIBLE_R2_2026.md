# [현재 정본] Blacksmith R2 통합 Game Bible

- 상태: `CURRENT_CANON / R2_BATCH_005_1_OF_10`
- 체크포인트 004: `PR106_HEAD_227b2dabf0d98832811415156e72f65d601332a9 / MERGE_789c73f38003f40dde5e9a99cd7dcb3ca03863f7 / MAIN_CANON`
- 현재 Decision: `BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / BS-CRAFT-20260805-02 / BS-OPS-20260805-01`
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

## 8. 고객·일정·콘텐츠

고객 능력과 사건 위험도는 `1~10`, 예상 성공률은 `5~95%`다. 이 bounded 척도는 예술성과 다른 계약이다. 모든 콘텐츠는 고객 결과, 작품 UID 상태·유산, 다음 제작·강화·복원 판단을 남겨야 한다.

## 9. 운영 방법

- 질문·추천·설계 전 벤치마킹·현업 비교
- 승인 10건은 최대 배치 크기
- 현재 `R2_BATCH_005_1_OF_10`
- 조기 체크포인트도 적대적 감사·CI·Sheet readback 필수
- 모든 작업은 `RED → GREEN → REFACTOR`
- 명시적 사용자 승인 전 병합 금지

## 10. 검증 경계

- 제품 구현: `BLOCKED`
- 현재 5등급·예술성 생성·성장·가치 평가 제품 구현: `NOT_STARTED`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
- 과거 PoC PASS는 현재 제품 PASS가 아님
