# [현재 정본] Active Context

- 갱신: `2026-08-05 21:45 KST`
- Work Mode: `TOTAL_PLANNING`
- 단계: `R2_CORE_SESSION_META_LOOP / R2_BATCH_005_5_OF_10`
- R2 체크포인트 003: `PR #103 / closure #104 / canon audit #105`
- R2 체크포인트 004: `planning #106 / closure #107 / canon audit #108`
- PR #106 exact head: `227b2dabf0d98832811415156e72f65d601332a9`
- PR #106 squash merge: `789c73f38003f40dde5e9a99cd7dcb3ca03863f7`
- PR #107 exact head: `1ad791123eaf6c727e964380814ffb69f1357bbf`
- PR #107 squash merge: `7a46fa38586a42f268cd0432744203049649ddd5`
- 이전 제작 Decision 상태: `BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / MERGED_PR106 / MAIN_CANON`
- 현재 제작 Decision: `BS-CRAFT-20260805-02 / R2_BATCH_005_4_OF_10`
- 현재 운영 Decision: `BS-OPS-20260805-01`
- 현재 승인 카운터: `5/10`
- 제품 구현: `BLOCKED`

## 현재 핵심

```text
직접 단조
→ 제작 등급 5단계
→ 일반 강화와 멈춤·추가 도전
→ 정밀강화 방식·촉매
→ 고객·세계 전달
→ 같은 UID 연대기·손상·복원
→ 다음 제작 판단
```

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

## 체크포인트 004 폐쇄

```text
R2_CHECKPOINT_004 / MAIN_CANON
R2_BATCH_004_CLOSED_2_OF_10 / CLOSED_MERGED_PR107
NEXT: R2_BATCH_005 / 1_OF_10
```

## 제작 등급 5단계

```text
[보통] → [우수] → [명품] → [걸작] → [전설]
```

- 최초 직접 단조 완료 시 한 번 확정
- 동일 UID 영구 고정
- 제작 후 승격·강등 없음
- 제작 등급은 예술성 최소값·상한·배율을 결정하지 않음

과거 `STANDARD / GOOD / PERFECT`는 `HISTORICAL_IMPLEMENTED_VALUE`다.

## 예술성 원수치

대표 원수치 표기: `예술성 27`.

- `0` 이상의 정수
- 고정 설계 최대치 없음
- 분모·별점·백분율·예술성 단계명 없음
- 전투 성능을 기본적으로 올리지 않음
- 제작 등급이 예술성 상한을 만들지 않음

```text
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

## 예술성 생성·성장·가치 평가

```text
artistry = 작품 UID에 저장되는 원수치
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

가치 모델:

```text
ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE
```

고객 관심 유형:

```text
IGNORE / SECONDARY / PRIMARY / REQUIREMENT
```

- 높은 구간일수록 추가 예술성의 한계 가치는 작아짐
- 화면 원수치는 압축하지 않음
- 같은 원인의 이중 계산과 전체 곱셈 중첩 금지
- 수리·손상·판매·전시·감정·증여·저비용 반복으로 순증가 금지
- 모든 변화는 작품 UID와 출처를 기록
- 정확한 수치는 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`

## 운영 계약

- 질문·추천·설계 전 벤치마킹·현업 비교
- 최대 배치 크기: `10`
- 현재: `R2_BATCH_005 / 2/10`
- 조기 체크포인트: `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT`
- 작업마다 TDD: `RED → GREEN → REFACTOR`
- 병합은 명시적 사용자 승인 필요

## 이번 TDD

RED:

- commit `c5459a81447a6f3d5f14d628a12acbdea34d1fcf`
- Planning-first `109`: `EXPECTED_FAILURE`
- 실패 원인: `BS-CRAFT-20260805-02` 부재와 배치 `0/10`

관측된 GREEN:

- commit `3665c5894591b241736de1a48981a71800203116`
- Planning-first `127`: `PASS`
- Base `609`: `PASS`
- PR validation `1200`: `PASS`
- Python 전체 계약: `PASS`
- Godot 4.7.1 headless: `PASS`

최종 exact-head: PR·Sheet 재검증 후 기록.

## 역사 구현·회귀 기준선

다음은 현재 제품 구현 PASS가 아니라 `[역사 증거]`다.

- 최신 역사 구현 배지: `POC v0.6.4 · main · 2026.07.23.1`
- 제작 모델 7건
- 제작 결과 통합 6건
- 과거 제작 품질: `STANDARD / GOOD / PERFECT`
- 강화 실패·위험 data 소유자: `data/crafting/enhancement_balance.json`
- 정밀 이정표 data 소유자: `data/crafting/enhancement_milestones.json`
- 과거 피버·품질 정확 수치: `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET`

## 검증 경계

- focused artistry generation/growth/economy test standalone: `NOT_RUN`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
- 제품 구현: `BLOCKED`

## 다음 작업

1. 증거 커밋 자체 exact-head CI·리뷰·Sheet readback
2. Draft PR #109에 `1/10` 누적 유지
3. 명시적 병합 승인 전 병합 금지

## 고객 능력·장비 적합성 승인

- Decision: `BS-CUSTOMER-20260805-01`
- 고객: 근력·기량·체력·판단력 `1~10`, 희소 무기·갑옷 적성 `0~3`, 마력 적성 `0~10`
- 작품: `WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL`
- 파생: 총 중량·적정 하중·균형 상태·특수기능 적합도
- 상태: `R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE / PRODUCT_IMPLEMENTATION_BLOCKED`

<!-- BS-UX-20260805-01 -->
## 현재 UX 승인

- Decision: `BS-UX-20260805-01`
- 기본 카드 → 장비 선택 후 판단층 → 상세 보기
- 장비 선택 후 균형·성공률·핵심 원인 2~4개 표시
- 전체 적성 행렬 기본 노출 금지
- 모바일 최소 `48dp`, 색상·길게 누르기·호버 단독 핵심 정보 금지
- 제품 구현: `BLOCKED`

<!-- BS-CUSTOMER-20260806-01 -->
### 강화 중심 단순 장비 판정

- Decision: `BS-CUSTOMER-20260806-01` / `R2_BATCH_005_4_OF_10`
- 최대 중량: `STRENGTH × 10 WEIGHT_POINT`
- 상태: `WITHIN_LIMIT / OVERWEIGHT`; 초과 시 배정 불가
- 성공률: 강화 레벨이 주효과, 고객 능력·적성은 작은 보조 보정
- 정본: `docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md`
- 제품 구현: `BLOCKED`

## BS-ITEM-20260806-01 현재 정제

- 활성 배치: `R2_BATCH_005_5_OF_10`
- 장비군 고정 기본 중량: `0 / 5 / 10 / 15 / 20 / 30 WEIGHT_POINT`
- 중량 전용 효과: `LIGHTWEIGHT -5 / NONE 0 / WEIGHTED +5`, 작품당 최대 하나
- 자동 중량 변경 금지: 재료·제작 등급·예술성·원수치·일반 강화 단계
- 정본: `docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md`
- 제품 구현: `BLOCKED`
