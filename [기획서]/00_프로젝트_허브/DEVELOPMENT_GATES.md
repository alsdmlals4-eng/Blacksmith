# [현재 정본] Development Gates

## 판정 원칙

- 사용자 승인, 기획 완전성, 구현, 자동 테스트, Android, 접근성, 성능, 사람 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN`이다.
- 과거 PoC PASS는 최신 제품 PASS를 대신하지 않는다.
- 미검증 숫자는 버전형 테스트 프리셋이다.
- 제품 구현은 R1~R8와 최종 사용자 검수 뒤 별도 승인으로만 시작한다.
- `[대체됨]`, `[보류]`, `[폐기]`, `[역사 증거]` 문서는 현재 구현 근거로 사용하지 않는다.

## Current Gate Summary

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R1_STATUS: USER_APPROVED / HISTORICAL_BASELINE / R2_REFINED
R2_STATUS: CHECKPOINT_003_CANON / PLANNING_ACTIVE
R2_CHECKPOINT_MERGE_PR: 103
R2_CHECKPOINT_MERGE_SHA: 674ee21013cb5d41f89a1a3f3b10ecfc31238295
R2_CHECKPOINT_CLOSURE_PR: 104
R2_CHECKPOINT_CLOSURE_SHA: d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9
CANON_ADVERSARIAL_AUDIT: BS-OPS-20260804-02 / BS-ADV-20260804-01 / COMPLETE_WITH_OPEN_USER_DECISIONS
CURRENT_AFFIX_SLOTS: GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
NEXT_APPROVAL_COUNTER: 0/10
CORE_DIRECTION_GATE: PASS
R2_CHECKPOINT_003_AUTHORITY_GATE: PASS
LEGACY_DOCUMENT_CLASSIFICATION_GATE: PASS
OPEN_USER_DESIGN_DECISION_GATE: 1_P1_PLUS_7_P2
CODEX_IMPLEMENTATION_GATE: BLOCKED
LATEST_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## R1 Core Gate

유지되는 기반:

- 검증 상한 `+50`
- 정밀 이정표 `+10/+20/+30/+40/+50`
- UID 기반 작품 생애·손상·복원·계승
- 고객 인계와 즉시·지연 결과
- 피로도·날짜 우선순위
- 테스트 프리셋과 제품값 분리
- 행동 증거와 중립적 회상 인터뷰

R2 대체:

- 일반 수식어 A·B → 등급·촉매·연대기 세 수식어
- 보조재료 슬롯 → 제거
- 범용 고정 일정 프리셋 → 개인 일정·날짜 예고형 세계 일정 분리

판정: `PASS / USER_APPROVED_BASELINE / R2_REFINED`.

## Three Affix Gate

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

- 정확히 세 슬롯
- 제작 완료 시 등급 수식어 생성
- 촉매·연대기 수식어는 최초 제작 시 `EMPTY`
- 등급 수식어는 동일 UID에서 고정
- 촉매 수식어는 촉매 이력으로 확률적 성장
- 연대기 수식어는 실제 작품 생애로 사건 기반 성장
- 슬롯 간 생성·진화·덮어쓰기 금지
- 제작 등급 효과 중복 가산 금지
- 일반 수식어 A·B 재도입 금지

판정: `PASS / USER_APPROVED / MERGED_PR103`.

## Precision Enhancement Gate

- 일반 강화: 한 입력 한 결과
- 정밀 이정표: `+10/+20/+30/+40/+50`
- 입력: 주재료 맥락 + 강화 방식 + 촉매 한 개
- 강화 방식: 세부 수치 방향
- 촉매: 촉매 수식어 후보 계보·확률
- 보조재료 슬롯 없음
- 같은 이정표 무한 리롤 금지
- 정확한 성공·수식어·최고 단계 보장 금지

판정: `PASS / STRUCTURE_APPROVED / EXACT_PROBABILITIES_UNVALIDATED`.

## Equipment Name·Chronicle Detail Gate

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

- 빈 촉매 수식어 생략
- 빈 연대기 수식어는 하이픈과 함께 생략
- 현재 연대기 하나만 이름에 표시
- 연대기 부분을 누르면 UID 기반 읽기 전용 하단 상세 패널
- 형성 사건·주요 타임라인·진화 계보·가치·소유·손상·복원 기록 표시
- 기록 없는 사건·미래 결과·열람 보상 금지
- 색상만으로 상호작용 표시 금지

판정: `PASS / USER_APPROVED / MERGED_PR103`.

열린 Gate:

- 긴 이름 줄바꿈·축약·스크린리더 순서
- 제작 등급 수식어와 예술성 시각 단계 한국어 명칭 분리

## Customer Information Gate

- 사건 위험도 `1~10`
- 고객 기량·체력·판단력 `1~10`
- 예상 성공률 약 10% 단위, `5~95%`
- 작품·도구·조언 선택 후 방향 갱신
- 정확한 모든 보정치·RNG 사전 공개 금지
- 수치 최적화가 작품 생애를 압도하지 않는지 사람 플레이 필요

판정: `STRUCTURE_APPROVED / EXACT_MODIFIERS_BASELINE_TEST_PRESET`.

## Schedule Gates

개인 일정:

- 방문·판매·납품으로 활성화
- 재방문 없이 하루 종료마다 최대 한 번 진행
- 판매 당일 최종 해결 금지

세계 일정:

- 특정 날짜·규모 사전 예고
- 작품·도구·조언 준비 기여 누적
- 준비 체크포인트와 예정 날짜 판정
- 범용 고정 날짜 프리셋 금지

표시:

```text
주요 세계 일정 하나 고정
+ 오늘 중요 소식 최대 3건
+ 일반 개인 일정 하루 종료 묶음 요약
+ 중대 결과만 즉시 알림
+ 관심 개인 일정 하나 추적
+ 전체 일정 장부
```

판정: `PASS / USER_APPROVED / NOT_RUNTIME_VALIDATED`.

## Artistry Gate

- 예술성은 새 가치 수치 하나
- 정수 `1~10`
- 실용 성능과 분리
- 강화 단계만으로 자동 상승 금지
- 고예술성이 모든 고객의 최적해가 되는 구조 금지
- 제작 등급 수식어와 예술성 시각 단계는 별개

열린 P1:

- 예시 `[명품]`과 예술성 한국어 단계 `명품`의 어휘 충돌

판정: `STRUCTURE_APPROVED / DISPLAY_LABEL_USER_DECISION_REQUIRED`.

## Content Composition Gate

모든 일정은 다음을 남겨야 한다.

- 고객 결과
- 작품 UID 상태·유산
- 다음 제작·강화·복원 판단

이름·보상만 바꾼 재스킨은 별도 콘텐츠로 세지 않는다.

초기 방문 고객: 검투사·모험가·군인·귀족.

판정: `DIRECTION_APPROVED / EXACT_CONTENT_COUNTS_DEFERRED`.

## Ownership·Lifecycle Gate

승인 기반:

- 판매·납품 뒤에도 작품 UID·생애 기록 유지
- 손상·복원·재방문·계승 가능
- 일반 실패는 역사를 자동 삭제하지 않음

열린 P2:

- 영구 소유권 이전
- 복원 의뢰의 임시 회수
- 재판매 가능 여부
- 증여·상속·상실·회수 상태 전이

판정: `BASELINE_APPROVED / STATE_MACHINE_REVIEW_REQUIRED`.

## Core Fun Validation Gate

필수 행동 증거:

- 강화 지속·중단 고민
- 등급·촉매·연대기 생성 원인 설명
- 작품 선택과 고객 결과 인과 설명
- 일정 현재 상태와 다음 행동 이해
- 재방문 뒤 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 생애 의미 이해

중립적 회상 인터뷰가 행동과 충돌하면 통과를 보류한다.

판정: `CONTRACT_APPROVED / EXECUTION_NOT_RUN`.

## Legacy Document Gate

상태 어휘:

```text
[현재 정본]
[부분 대체됨]
[대체됨]
[보류]
[폐기]
[역사 증거]
```

완료:

- 구형 A/B 수식어·보조재료·2슬롯 문서 직접 상태 표시
- PR #81 전체 병합 단위 `DO_NOT_MERGE / REJECTED`
- 역사 PoC 수치와 최신 제품값 분리
- R1 Registry 역사 기반 재분류
- Design Document Registry 현행 R2 라우팅
- 기계 판독 상태 원장과 파일 배너 자동 검사

판정: `PASS / BS-OPS-20260804-02 / BS-ADV-20260804-01`.

## PR Gate

- PR #103: `MERGED_R2_CHECKPOINT_003_CANON`
- PR #104: `MERGED_POSTMERGE_CLOSURE`
- PR #81: `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT / SELECTIVE_PROMOTION_HOLD`
- PR #105: exact-head 검증·Sheet readback·P0/P1 재감사 뒤 expected-head squash 병합

## Historical Baseline Gate

- `POC v0.6.4 · main · 2026.07.23.1`
- 제작 모델 7건·통합 6건
- 과거 일반 강화 실패 `+11 / LEGACY_IMPLEMENTED_VALUE`
- `data/crafting/enhancement_balance.json`
- `data/crafting/enhancement_milestones.json`
- `HISTORICAL_EVIDENCE`, 최신 제품 PASS 아님

## Product Implementation Gate

R1~R8 기획·검수, 저장·rollback·migration 계약, 테스트 프리셋과 최종 사용자 승인이 완료되기 전까지 `BLOCKED`다.

## Current Next Gate

```yaml
NEXT_ACTIVITY: USER_REVIEW_OPEN_DESIGN_DECISIONS_AND_CONTINUE_R2_PLANNING
NEXT_APPROVAL_COUNTER: 0/10
PRODUCT_IMPLEMENTATION: BLOCKED
```
