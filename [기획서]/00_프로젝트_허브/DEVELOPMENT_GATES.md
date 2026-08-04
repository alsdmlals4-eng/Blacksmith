# [현재 정본] Development Gates

## Current Gate Summary

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R2_STATUS: CHECKPOINT_003_CANON / BATCH_004_ACTIVE_2_OF_10
CURRENT_AFFIX_SLOTS: GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
CURRENT_CRAFTING_GRADES: 보통 / 우수 / 명품 / 걸작 / 전설
CURRENT_ARTISTRY: INTEGER_1_TO_10_WEAPON_ITEM_STAT_NO_NAMED_TIERS
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
- `전설`은 출생 극희귀 결과
- 예술성·촉매·연대기·명성으로 등급 변경 금지
- 과거 4단계와 `STANDARD / GOOD / PERFECT`는 현재 제품 모델 아님

판정: `USER_APPROVED / R2_BATCH_004_1_OF_10 / IMPLEMENTATION_BLOCKED`.

## Artistry Gate

```text
예술성 7/10
```

- 무기·작품 능력치
- 정수 `1~10`, 소수점 없음
- 단계명 없음
- 다른 능력치와 함께 상세 표시
- 판매 가치·귀족·후원자·수집가·전시·감정·증여·의식 수요에 기여 가능
- 전투 성능을 기본적으로 올리지 않음
- 범용 속성·수식어 배율 금지

판정: `USER_APPROVED / R2_BATCH_004_2_OF_10 / IMPLEMENTATION_BLOCKED`.

## Three Affix Gate

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

- 정확히 세 슬롯
- 등급 수식어는 제작 완료 시 생성·고정
- 촉매·연대기는 최초 제작 시 `EMPTY`
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

## Equipment Name·Chronicle Detail Gate

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

- 연대기 부분을 누르면 UID 기반 읽기 전용 하단 패널
- 형성 사건·타임라인·진화 계보·소유·손상·복원 기록
- 기록 없는 사건·미해결 미래 결과·열람 보상 금지

판정: `PASS / USER_APPROVED`.

## Benchmark Gate

- 질문·추천·설계 전에 유사 게임·현업 사례 비교
- `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성` 기록
- 출처·확인 날짜 기록
- 유명 사례라도 프로젝트 코어와 충돌하면 비채택

판정: `REQUIRED_BY_BS-OPS-20260805-01`.

## TDD Gate

```text
RED → GREEN → REFACTOR
```

- 테스트 먼저
- 의도한 RED 관측
- 최소 변경으로 GREEN
- GREEN 이후 정리
- RED·GREEN 증거 없이 PASS 주장 금지
- 문서·기획도 기계 판독 계약으로 보호

증거:

- RED commit `a5f20ab4578c83f75d044b68f19ed0bcb7b45d00`, Planning-first run `33`, expected failure
- GREEN reference commit `25d5f53a380328a7ff655498adb8c10bdd1073f1`
- Planning-first `57`, Base `524`, PR validation `1115`
- Python full `PASS`, Godot 4.7.1 `PASS`

판정: `RED_GREEN_OBSERVED / FINAL_EVIDENCE_COMMIT_EXACT_HEAD_PENDING`.

## Batch·Checkpoint Gate

- 승인 10건은 최대 배치 크기
- 현재 `2/10`
- 고위험 충돌·세션 종료·정본 영향이 크면 조기 체크포인트 허용
- 조기 체크포인트도 적대적 감사·PR·CI·Sheet readback 필수
- 병합은 명시적 사용자 승인 필요

## Core Fun Validation Gate

필수 행동 증거:

- 강화 지속·중단 고민
- 제작 등급·예술성·촉매·연대기의 원인 구분
- 고객 결과와 작품 선택 인과 설명
- 재방문 뒤 다음 행동 선택

판정: `CONTRACT_APPROVED / EXECUTION_NOT_RUN`.

## Historical Forging Validation Gate

현재 제품 승인과 분리된 과거 reference implementation 회귀 기준선:

- `POC v0.6.4 · main · 2026.07.23.1`
- 제작 모델 7건
- 제작 결과 통합 6건
- `STANDARD / GOOD / PERFECT`
- `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET`

판정: `HISTORICAL_EVIDENCE / AUTOMATED_REGRESSION_PASS_REQUIRED / NOT_CURRENT_FIVE_GRADE_PRODUCT_PASS`.

## Legacy Document Gate

- `[현재 정본] / [부분 대체됨] / [대체됨] / [보류] / [폐기] / [역사 증거]`
- 구형 4등급 문서 직접 `[대체됨]`
- 구형 예술성 단계 프리셋 `[대체됨]`
- PR #81 `DO_NOT_MERGE_AS_UNIT`

판정: `PASS_PENDING_FINAL_DRIFT_SCAN`.

## Product Implementation Gate

R1~R8와 최종 사용자 검수, 저장·migration 계약, 테스트 프리셋 승인 전까지 `BLOCKED`다.
