# [현재 정본] Development Gates

## Current Gate Summary

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R2_STATUS: R2_CHECKPOINT_004_MAIN_CANON / R2_BATCH_005_ACTIVE_5_OF_10
R2_CHECKPOINT_004_PLANNING: PR106_HEAD_227b2dabf0d98832811415156e72f65d601332a9 / MERGE_789c73f38003f40dde5e9a99cd7dcb3ca03863f7
R2_CHECKPOINT_004_CLOSURE: PR107_HEAD_1ad791123eaf6c727e964380814ffb69f1357bbf / MERGE_7a46fa38586a42f268cd0432744203049649ddd5
CURRENT_AFFIX_SLOTS: GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
CURRENT_CRAFTING_GRADES: 보통 / 우수 / 명품 / 걸작 / 전설
CURRENT_ARTISTRY: NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
CURRENT_ARTISTRY_FLOW: BS-CRAFT-20260805-02
NEXT_APPROVAL_COUNTER: 1/10
MAXIMUM_BATCH_SIZE: 10
EARLY_CHECKPOINTS: HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT
TDD_GATE: RED_GREEN_OBSERVED / FINAL_EXACT_HEAD_REVALIDATION
CODEX_IMPLEMENTATION_GATE: BLOCKED
LATEST_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## Crafting Grade Gate

```text
[보통] → [우수] → [명품] → [걸작] → [전설]
```

- 최초 직접 단조 완료 시 확정
- 동일 UID 고정
- 후천 승격·강등 없음
- 제작 등급은 예술성 최소값·상한·배율을 결정하지 않음

판정: `USER_APPROVED / MERGED_PR106 / R2_CHECKPOINT_004_MAIN_CANON / IMPLEMENTATION_BLOCKED`.

## Artistry Gate

```text
예술성 27
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

- `0` 이상의 정수, 고정 설계 최대치 없음
- 소수점·분모·별점·백분율·단계명 없음
- 다른 능력치와 함께 원수치 표시
- 예술성 0은 정상 기능품
- 전투 성능을 기본적으로 올리지 않음
- 범용 속성·수식어 배율 금지

판정: `USER_APPROVED_REFINED / MERGED_PR106 / R2_CHECKPOINT_004_MAIN_CANON / IMPLEMENTATION_BLOCKED`.

## Artistry Generation·Growth·Valuation Gate

Decision: `BS-CRAFT-20260805-02`.

필수 계약:

```text
artistry = UID persisted stat
artistry_value = CONTEXT_DERIVED_NOT_PERSISTED
customer_artistry_fit = CONTEXT_DERIVED_NOT_PERSISTED
```

최초 생성 허용 원천:

```text
BASE_ITEM_DESIGN_AESTHETIC_TENDENCY
MATERIAL_VISUAL_PROCESSING_FIT
DIRECT_FORGING_AESTHETIC_RESULT
```

제작 후 성장 허용 원천:

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

- 예술성 가치 기여는 단조 증가
- 높은 구간일수록 한계 가치 감소
- 원수치 압축 금지
- 구간별 한계 가치 data table 우선
- 동일 원인 이중 계산 금지
- 전체 가치 구성요소 곱셈 중첩 금지
- 고객 관심 유형: `IGNORE / SECONDARY / PRIMARY / REQUIREMENT`
- 관심 없는 고객은 초과 예술성에 추가 지불하지 않을 수 있으나 패널티 없음
- 수리·손상·판매·전시·감정·증여·저비용 반복 순증가 금지
- 모든 변화는 UID와 출처 기록
- 정확한 수치: `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`

판정: `USER_APPROVED / R2_BATCH_005_4_OF_10 / DRAFT_PR109 / IMPLEMENTATION_BLOCKED`.

## Three Affix Gate

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

- 정확히 세 슬롯
- 슬롯 간 생성·진화·덮어쓰기 금지
- 일반 수식어 A·B 재도입 금지

판정: `PASS / USER_APPROVED`.

## Precision Enhancement Gate

- 일반 강화: 한 입력 한 결과
- 정밀 이정표: `+10/+20/+30/+40/+50`
- 주재료 맥락 + 강화 방식 + 촉매 한 개
- 보조재료 슬롯 없음
- 같은 이정표 무한 리롤 금지

판정: `STRUCTURE_APPROVED / EXACT_VALUES_BASELINE_TEST_PRESET`.

## Benchmark Gate

- 질문·추천·설계 전에 유사 게임·현업 사례 비교
- `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성` 기록
- 유명 사례라도 프로젝트 코어와 충돌하면 비채택

판정: `REQUIRED_BY_BS-OPS-20260805-01`.

## TDD Gate

```text
RED → GREEN → REFACTOR
```

이번 Decision RED:

- commit `c5459a81447a6f3d5f14d628a12acbdea34d1fcf`
- Planning-first `109`: `EXPECTED_FAILURE`
- 실패 원인: 새 Decision 부재와 배치 `0/10`

관측된 GREEN:

- commit `3665c5894591b241736de1a48981a71800203116`
- Planning-first `127`: `PASS`
- Base `609`: `PASS`
- PR validation `1200`: `PASS`
- Python full contracts: `PASS`
- Godot 4.7.1 headless: `PASS`

판정: `RED_GREEN_OBSERVED / FINAL_EVIDENCE_COMMIT_EXACT_HEAD_PENDING`.

## Batch·Checkpoint Gate

- R2_BATCH_004: `CLOSED_MERGED_PR107 / 2_OF_10 / USER_APPROVED_EARLY_CHECKPOINT`
- R2_BATCH_005: `ACTIVE / 1_OF_10`
- 승인 10건은 최대 배치 크기
- 고위험 충돌·세션 종료·정본 영향이 크면 조기 체크포인트 허용
- 병합은 명시적 사용자 승인 필요

## Core Fun Validation Gate

필수 행동 증거:

- 강화 지속·중단 고민
- 제작 등급·예술성·촉매·연대기의 원인 구분
- 예술성 변화 원인과 고객 가치 차이 설명
- 고객 결과와 작품 선택 인과 설명

판정: `CONTRACT_APPROVED / EXECUTION_NOT_RUN`.

## Historical Forging Validation Gate

다음은 현재 제품 구현 승인이 아니라 과거 reference implementation의 `[역사 증거]`다.

- `POC v0.6.4 · main · 2026.07.23.1`
- 제작 모델 7건
- 제작 결과 통합 6건
- 과거 품질: `STANDARD / GOOD / PERFECT`
- 정확 수치: `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET`

## Legacy Document Gate

- `[현재 정본] / [부분 대체됨] / [대체됨] / [보류] / [폐기] / [역사 증거]`
- PR #81 `DO_NOT_MERGE_AS_UNIT`

## Product Implementation Gate

R1~R8와 최종 사용자 검수, 저장·migration 계약, 테스트 프리셋 승인 전까지 `BLOCKED`다.

## 고객 능력·장비 적합성 승인

- Decision: `BS-CUSTOMER-20260805-01`
- 고객: 근력·기량·체력·판단력 `1~10`, 희소 무기·갑옷 적성 `0~3`, 마력 적성 `0~10`
- 작품: `WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL`
- 파생: 총 중량·적정 하중·균형 상태·특수기능 적합도
- 상태: `R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE / PRODUCT_IMPLEMENTATION_BLOCKED`

<!-- BS-UX-20260805-01 -->
### Mobile Customer Card Progressive Disclosure Gate

- Decision: `BS-UX-20260805-01`
- 3단계 정보 계층: APPROVED
- 설명 가능한 이유 2~4개: REQUIRED
- 접근성 48dp·비색상 단독 신호: REQUIRED
- 이미지·애니메이션 HX: BLOCKED_UNTIL_REVIEW_COMPLETE
- CODEX_IMPLEMENTATION_GATE: BLOCKED

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
