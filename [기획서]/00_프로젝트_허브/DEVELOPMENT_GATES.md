# [현재 정본] Development Gates

<!-- R2_BATCH_006_CURRENT_AUTHORITY -->
> **R2_BATCH_006_APPROVED_MAIN_CANON / SCOPED_VERTICAL_SLICE_ONLY**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON`

## Current Gate Summary

```yaml
CURRENT_STAGE: R2_BATCH_006_MAIN_CANON_SCOPED_VERTICAL_SLICE
R2_STATUS: R2_BATCH_006_APPROVED_MAIN_CANON
R2_CHECKPOINT_005: CLOSED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_006: APPROVED_10_OF_10
TDD_GATE: RED_GREEN_REFACTOR_REQUIRED
CODEX_IMPLEMENTATION_GATE: VERTICAL_SLICE_APPROVED
VERTICAL_SLICE_PLAN_GATE: CONDITIONALLY_FEASIBLE
VERTICAL_SLICE_CODE_GATE: USER_APPROVED_SCOPED_ONLY
LATEST_RUNTIME_VALIDATION_GATE: HISTORICAL_POC_ONLY
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST: NOT_RUN
PRODUCT_IMPLEMENTATION: BLOCKED
GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED
VERTICAL_SLICE_IMPLEMENTATION: APPROVED_SCOPED_NAMESPACES_ONLY
VERTICAL_SLICE_IMPLEMENTATION_APPROVED: SCOPED_ONLY
HIGODOT_AUTHORING_AUTHORITY: PILOT_ONLY_NOT_PRODUCTION_READY
GUT_TEST_AUTHORITY: VENDORED_PRESENT_FORMAL_ADOPTION_PENDING
ENTRY_STATE_GATE: FAIL_CLOSED
IMAGE_PRODUCT_GATE: BLOCKED_NOT_PRODUCT_READY
IMAGE_LIST_SCHEMA_GATE: SCHEMA_ALIGNMENT_REPAIRED_READBACK_PASS
```

## Canon Gate

버티컬 슬라이스를 포함한 모든 새 구현은 다음을 동시에 지켜야 한다.

- 제작 등급 5단계와 동일 UID 고정
- 예술성 비음수 정수·고정 설계 최대치 없음
- `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`
- 보조재료 슬롯 없음
- 일반 강화 한 입력 한 결과
- 정밀강화 `+10/+20/+30/+40/+50`
- 장비군별 주재료·역할·기본 중량
- 역할 수치 프리셋 `5/10/15`
- 기능 용량과 명시적 재작업 레시피
- 고객 최대 중량 `STRENGTH × 10`
- 모바일 3단계 정보 공개와 설명 가능한 핵심 원인
- 개인 일정·세계 일정 분리
- 작품 UID 변동 장부와 연대기

판정: `REQUIRED`.

## R2_CHECKPOINT_004 Historical Evidence

- planning main: `789c73f38003f40dde5e9a99cd7dcb3ca03863f7`
- closure main: `7a46fa38586a42f268cd0432744203049649ddd5`
- 현재 활성 상태가 아니라 제작 등급·예술성 계약의 불변 출처다.

## Artistry Generation·Growth·Valuation Gate

Decision: `BS-CRAFT-20260805-02`.

```text
artistry = UID persisted non-negative integer
artistry_value = CONTEXT_DERIVED_NOT_PERSISTED
customer_artistry_fit = CONTEXT_DERIVED_NOT_PERSISTED
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

- 예술성은 제작 등급·일반 강화·판매·전시·소유권·명성으로 자동 증가하지 않는다.
- 최초 생성과 후속 성장 원천을 분리한다.
- 시장 가치 기여는 가산 후 구간별 한계 가치가 점감한다.
- 동일 원인 이중 계산과 저비용 반복 파밍을 금지한다.
- 정확한 값은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

판정: `USER_APPROVED / MERGED_PR109_MAIN_CANON / IMPLEMENTATION_BLOCKED`.

## Historical POC Gate

현재 Godot 프로젝트는 실행·파싱·씬 스모크·모델·통합 테스트가 통과하는 역사 POC다. 다음은 새 정본 구현으로 승격하지 않는다.

- 구형 `STANDARD / GOOD / PERFECT` 품질
- 보조재료 입력과 관련 재고
- 범용 수식어 배열
- 고정 계약 일수 중심 고객 평가
- 과거 정확한 확률·공격 배율·경제 수치

판정: `REFERENCE_ONLY / REUSE_BY_PORT_NOT_BY_AUTHORITY`.

## Vertical Slice Readiness Gate

판정: `CONDITIONALLY_FEASIBLE / SCOPED_IMPLEMENTATION_APPROVED`.

필수 선행 조건:

1. 대표 콘텐츠 경로를 전체 콘텐츠와 구분한다.
2. 최신 정본 전용 Item UID·Save Schema를 확정한다.
3. 정확한 수치를 테스트 프리셋으로 격리한다.
4. 기존 POC 구형 모델을 새 Schema에 직접 혼합하지 않는다.
5. 앱 시작 씬을 테스트 씬과 분리한다.
6. 자동 검증과 사람 플레이테스트 결과를 별도로 기록한다.

PR #122는 Task 1 UID·Save 기반의 Draft·미병합 구현이며, Green 테스트만으로 다음 Task나 일반 제품 범위를 자동 개방하지 않는다.

## TDD Gate

모든 변경은 다음 순서를 따른다.

```text
RED → GREEN → REFACTOR → exact-head CI → review readback
```

HiGodot·GUT 설계 변경도 정책·상태 snapshot·변경 경계를 기계 판독 테스트로 보호한다. GUT runtime PASS는 별도 정식 채택 PR에서만 주장한다.

## Save·UID Gate

버티컬 슬라이스 최소 저장 항목:

- 고유 작품 UID
- 주재료·장비군·역할 프로필
- 제작 등급·예술성·역할 원수치·중량
- 세 수식어 슬롯
- 강화 단계·정밀강화 사용 이정표
- 기능과 기능 용량
- 손상·복원·소유권·고객 결과
- 모든 변동 원인 장부

저장·로드 재추첨은 금지한다.

판정: `TASK1_DRAFT_IMPLEMENTED / PR122_UNMERGED / HUMAN_AND_ANDROID_NOT_RUN`.

## Human Playtest Gate

필수 검증:

- 강화 지속·중단 고민
- 등급·예술성·촉매·연대기 구분
- 고객 결과의 원인 설명
- 모바일 정보 과부하 여부
- 같은 UID에 대한 애착과 다음 행동

판정: `NOT_RUN`.

## Product Implementation Gate

일반 제품 구현은 `BLOCKED`다. 버티컬 슬라이스는 R2 Batch 006이 승인한 namespace와 사용자 승인 Task에서만 허용한다.

## Three Affix Gate

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

세 슬롯의 생성·진화·덮어쓰기 책임을 분리한다. 판정: `REQUIRED`.

## Benchmark Gate

- 새 Decision과 수치 프리셋은 유사 게임·현업 사례 비교를 먼저 수행한다.
- 결과는 `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성`으로 기록한다.
- 프로젝트 코어와 충돌하는 유명 사례는 비채택한다.

판정: `REQUIRED_BY_BS-OPS-20260805-01`.

## Historical Forging Validation Gate

다음은 현재 제품 구현 승인이 아니라 보존해야 하는 `[역사 증거]`다.

- 최신 역사 구현 배지: `POC v0.6.4 · main · 2026.07.23.1`
- 제작 모델 7건
- 제작 결과 통합 6건
- 정확한 구형 품질·피버 수치는 `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET`

판정: `HISTORICAL_EVIDENCE / PRODUCT_IMPLEMENTATION_BLOCKED`.

## HiGodot·GUT Authority Gate

Decision: `BS-OPS-20260806-10 / BS-TEST-20260806-01`.

- `HIGODOT_SOLE_AUTHORING_AUTHORITY`: 정식 채택 뒤 Scene·Node·Resource·Godot 프로젝트 설정은 HiGodot만 저작한다.
- `GUT_SOLE_TEST_AUTHORITY`: 정식 채택 뒤 GUT 9.7.1은 GDScript 단위·통합 테스트의 정식 프레임워크다.
- `ENTRY_GATE_FAIL_CLOSED`: 결정 원장·미확정/감사·이미지 목록/검수·열린 PR exact-head 상태가 모두 현재가 아니면 진입을 차단한다.

현재 상태:

```yaml
HIGODOT: PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY
GUT_VENDOR: PRESENT_9_7_1
GUT_PLUGIN_ENABLED: false
GUT_CONFIG_PRESENT: false
GUT_PROJECT_TEST_ROOT_PRESENT: false
GUT_RUNTIME_CI: false
GUT_FORMAL_AUTHORITY: PENDING
GUT_SOURCE: bitwes/Gut@v9.7.1
GUT_COMMIT: aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605
GUT_LICENSE: MIT
GUT_GODOT_COMPATIBILITY: 4.7.x
GUT_RUNTIME_TRACKED_MUTATION: FORBIDDEN
SAME_FILE_DUAL_AUTHORITY: FORBIDDEN
```

GUT Plugin 활성화·config·테스트 이관·runtime CI는 이 설계 PR과 분리된 후속 Draft PR에서 수행한다. `project.godot` 변경은 HiGodot 저작 증거가 있어야 하며, GUT 실행 전후 Scene·Resource·프로젝트 설정 hash가 달라지면 CI를 실패시킨다.

## Missing-State Entry Gate

진입 전 실제로 읽어야 하는 Sheet:

- `00_프로젝트_허브`
- `01_작업순서`
- `02_현재_확정결정`
- `04_누락_충돌_감사`
- `71_이미지기획_생성목록`
- `72_이미지검수_승인로그`

현재 판정:

```yaml
GENERAL_PRODUCT: BLOCKED
SCOPED_VERTICAL_SLICE: OPEN_ONLY_FOR_APPROVED_NAMESPACES
PR122: OPEN_DRAFT_UNMERGED
PRODUCT_IMAGE: BLOCKED_NOT_PRODUCT_READY
IMAGE_GENERATED: NOT_RUN
IMAGE_RIGHTS: NOT_RUN
IMAGE_RUNTIME: NOT_RUN
IMAGE_LIST_SCHEMA: SCHEMA_ALIGNMENT_REPAIRED_READBACK_PASS
IMAGE_ASSET_COMPLETION: BLOCKED_NOT_GENERATED_AND_RIGHTS_NOT_RUN
GUT_ADOPTION: VENDORED_PRESENT_FORMAL_ADOPTION_PENDING
```

이미지 목록의 열 정렬 복구는 제품 이미지 생성·권리·가독성·런타임 Gate를 개방하지 않는다.

`READY`·`AWAITING`·`IN_REVIEW`·`APPROVED` 같은 일반 문자열은 범위·근거 SHA·검증 상태가 없으면 진입 허용으로 사용할 수 없다.
