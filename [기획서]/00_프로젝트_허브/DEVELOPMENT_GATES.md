# [현재 정본] Development Gates

<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / R2_BATCH_006_NOT_STARTED_0_OF_10`

## Current Gate Summary

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R2_STATUS: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_006: NOT_STARTED_0_OF_10
TDD_GATE: RED_GREEN_REFACTOR_REQUIRED
CODEX_IMPLEMENTATION_GATE: BLOCKED
VERTICAL_SLICE_PLAN_GATE: CONDITIONALLY_FEASIBLE
VERTICAL_SLICE_CODE_GATE: USER_APPROVAL_REQUIRED
LATEST_RUNTIME_VALIDATION_GATE: HISTORICAL_POC_ONLY
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST: NOT_RUN
PRODUCT_IMPLEMENTATION: BLOCKED
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

## Historical POC Gate

현재 Godot 프로젝트는 실행·파싱·씬 스모크·모델·통합 테스트가 통과하는 역사 POC다. 다음은 새 정본 구현으로 승격하지 않는다.

- 구형 `STANDARD / GOOD / PERFECT` 품질
- 보조재료 입력과 관련 재고
- 범용 수식어 배열
- 고정 계약 일수 중심 고객 평가
- 과거 정확한 확률·공격 배율·경제 수치

판정: `REFERENCE_ONLY / REUSE_BY_PORT_NOT_BY_AUTHORITY`.

## Vertical Slice Readiness Gate

판정: `CONDITIONALLY_FEASIBLE`.

필수 선행 조건:

1. 대표 콘텐츠 경로를 전체 콘텐츠와 구분한다.
2. 최신 정본 전용 Item UID·Save Schema를 확정한다.
3. 정확한 수치를 테스트 프리셋으로 격리한다.
4. 기존 POC 구형 모델을 새 Schema에 직접 혼합하지 않는다.
5. 앱 시작 씬을 테스트 씬과 분리한다.
6. 자동 검증과 사람 플레이테스트 결과를 별도로 기록한다.

제품 코드를 시작하려면 사용자의 별도 구현 승인이 필요하다.

## TDD Gate

모든 변경은 다음 순서를 따른다.

```text
RED → GREEN → REFACTOR → exact-head CI → review readback
```

현재 정본 폐쇄 보강 작업의 RED는 PR #119에서 관측한다.

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

판정: `DESIGN_REQUIRED_BEFORE_CODE`.

## Human Playtest Gate

필수 검증:

- 강화 지속·중단 고민
- 등급·예술성·촉매·연대기 구분
- 고객 결과의 원인 설명
- 모바일 정보 과부하 여부
- 같은 UID에 대한 애착과 다음 행동

판정: `NOT_RUN`.

## Product Implementation Gate

R2 Batch 006의 버티컬 슬라이스 범위·Schema·테스트 프리셋과 사용자 구현 승인이 있기 전까지 `BLOCKED`다.
