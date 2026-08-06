# [현재 정본] Blacksmith Roadmap

<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON`

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
CURRENT_STAGE_STATUS: R2_BATCH_006_APPROVED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_006: APPROVED_10_OF_10
PRODUCT_IMPLEMENTATION: BLOCKED
VERTICAL_SLICE_IMPLEMENTATION: APPROVED
HUMAN_PLAYTEST: NOT_RUN
```

## R0–R2 — 완료된 기획 기반

- 프로젝트 코어와 권위 체계
- 직접 단조·제작 등급 5단계·예술성
- 등급·촉매·연대기 3수식어
- 일반 강화와 다섯 정밀강화 이정표
- 작품 역할·중량·기능 용량·재작업 레시피
- 고객 능력·장비 적합·모바일 정보 계층
- 개인 일정·세계 일정 분리와 작품 생애 환류

상태: `R2_CHECKPOINT_005_CLOSED_MAIN_CANON`.

## 불변 체크포인트 이력

- `R2_CHECKPOINT_004`: 제작 등급 5단계·예술성 원수치 정제와 후속 폐쇄를 완료했다.
- `R2_CHECKPOINT_005`: `BS-CRAFT-20260805-02`를 포함한 승인 10건과 작품 역할·기능 레시피 Gate를 폐쇄했다.
- 체크포인트 004 planning/closure main: `789c73f38003f40dde5e9a99cd7dcb3ca03863f7 / 7a46fa38586a42f268cd0432744203049649ddd5`
- 체크포인트 005 planning/closure main: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9 / 06f03323c1309d8da0e6f5b9f4680a20ce388126`

이 항목은 현재 활성 카운터가 아니라 재현 가능한 병합 증거다.

## R2 Batch 006 — 다음 기획 배치

최대 10개 Decision으로 다음 순서를 권장한다.

1. 버티컬 슬라이스 대표 콘텐츠와 완료 조건
2. 작품 UID Schema·변동 장부·세이브 최소 계약
3. 제작 등급 5단계 데모 확률 프리셋
4. 예술성·역할 수치·중량 초기 프리셋
5. 일반 강화 데모 구간과 정밀강화 `+10` 대표 이정표
6. 촉매 씨앗·진화 대표 한 계보
7. 고객 3종과 설명 가능한 적합도 결과
8. 개인 일정 1개·세계 일정 1개
9. 손상·복원·연대기 대표 사건
10. 내부 테스트·사람 플레이테스트 프로토콜

정확한 값은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`로 유지한다.

## R3 — 버티컬 슬라이스 기반

- 최신 정본 전용 데이터 Schema
- 작품 UID와 저장·로드
- 단일 앱 셸과 화면 전환
- 대표 제작·강화·고객·일정·연대기 경로
- 원인 설명 로그와 로컬 검증 데이터

기존 POC의 구형 품질·보조재료·범용 수식어 구조는 재사용하지 않는다.

## R4 — 콘텐츠와 경제

- 장비군·주재료·기능·고객 확장
- 판매·증여·복원·상속 소유권 상태
- 가격·예술성·수요 점감
- 피로도·장기 성장·세계 일정

## R5–R6 — 모바일 제품화

- Android 세로형 UX
- 접근성·성능·저사양 검증
- 아트·오디오·피드백
- 세이브 migration과 복구

## R7 — 첫 코어 버티컬 슬라이스

```text
대표 작품 한 점 직접 단조
→ 제작 등급·예술성·역할·중량 확인
→ 일반 강화 지속·중단
→ 대표 정밀강화와 촉매 계보
→ 고객에게 배정하고 성공률·핵심 원인 확인
→ 결과·연대기·손상 또는 복원
→ 같은 UID로 재방문
→ 다음 제작 판단
```

필수 행동 증거:

- 플레이어가 강화 지속·중단을 고민한다.
- 등급·예술성·촉매·연대기의 원인을 구분한다.
- 고객 결과와 작품 선택의 인과를 설명한다.
- 같은 작품의 변화와 다음 행동을 기억한다.

## R8 — 적대적 최종 검토

- 핵심 재미와 모바일 복잡도
- 현재 정본·구형 문서·PR·데이터 충돌
- 저장·migration·접근성·성능
- 내부 테스트와 외부 사람 플레이테스트

## 구현 Gate

현재 상태:

```yaml
PRODUCT_IMPLEMENTATION: BLOCKED
HUMAN_PLAYTEST: NOT_RUN
VERTICAL_SLICE_PLAN: CONDITIONALLY_FEASIBLE
VERTICAL_SLICE_CODE: USER_APPROVAL_REQUIRED
```

## 세 수식어 불변 계약

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

일반 수식어 A·B와 보조재료 슬롯은 재도입하지 않는다.
