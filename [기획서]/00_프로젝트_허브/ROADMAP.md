# [현재 정본] Blacksmith Roadmap

<!-- R3_R7_DESIGN_RESUMED -->
> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-02 / ADVENTURER_02_TOREN_LONG_RANGE_RELIABILITY_APPROVED / PLANNING_ONLY**
>
> R2 Batch 006과 Task2 완료 상태를 기반으로 R3–R7 콘텐츠 기획을 재개한다. 제품 구현 Gate는 계속 닫혀 있다.

```yaml
CURRENT_STAGE: R3_R7_DESIGN_ACTIVE
CURRENT_STAGE_STATUS: R3_R7_2_OF_10_USER_APPROVED_PLANNING_CANON
R2_CHECKPOINT_005: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_005_STATE: R2_BATCH_005_CLOSED_10_OF_10
R2_BATCH_005_MERGE: MERGED_PR109_MAIN_CANON
R2_BATCH_006: APPROVED_10_OF_10
R2_BATCH_006_STATE: R2_BATCH_006_APPROVED_10_OF_10
R3_R7_APPROVAL_COUNTER: 2/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-02
R3_R7_RESUME_LOCATOR: ADVENTURER_02_TOREN_LONG_RANGE_RELIABILITY_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
VERTICAL_SLICE_IMPLEMENTATION: APPROVED_TASK2_COMPLETE
VERTICAL_SLICE_IMPLEMENTATION_EVIDENCE: VERTICAL_SLICE_IMPLEMENTATION_APPROVED
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

상태: `R2_BATCH_006_APPROVED_MAIN_CANON / R2_BATCH_006_APPROVED_10_OF_10 / TASK2_MAIN_MERGED / VERTICAL_SLICE_IMPLEMENTATION_APPROVED`.

## 불변 체크포인트 이력

- `R2_CHECKPOINT_004`: 제작 등급 5단계·예술성 원수치 정제와 후속 폐쇄를 완료했다.
- `R2_CHECKPOINT_005 / R2_CHECKPOINT_005_CLOSED_MAIN_CANON`: `BS-CRAFT-20260805-02`를 포함한 승인 10건과 작품 역할·기능 레시피 Gate를 폐쇄했다.
- `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON`: Batch 005 승인과 main 병합을 보존하는 호환 앵커다.
- `R2_BATCH_006 / R2_BATCH_006_APPROVED_10_OF_10`: 대표 버티컬 슬라이스 계획과 승인 범위를 main canon으로 병합했다.
- 체크포인트 004 planning/closure main: `789c73f38003f40dde5e9a99cd7dcb3ca03863f7 / 7a46fa38586a42f268cd0432744203049649ddd5`
- 체크포인트 005 planning/closure main: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9 / 06f03323c1309d8da0e6f5b9f4680a20ce388126`
- Batch 006 merge main: `a8a94343c78a68bf7bb14b411e7741f43b257138`

이 항목은 현재 활성 카운터가 아니라 재현 가능한 병합 증거다. R3–R7 설계 활성화는 이 역사/호환 토큰을 폐기하지 않는다.

## R3–R7 현재 설계 배치

현재 승인 카운터: `1/10`.

### 1/10 — `BS-CONTENT-20260811-01`

```text
ADVENTURER_01 / NADIA_VENN
나디아 벤 유적 탐사 개인 일정
생환 + 회수
```

목표:

- 대장장이가 고객의 목적·위험을 읽고 작품 한 점을 선택한다.
- 강화 단계가 주효과이되 중량 배정 가능 여부와 실제 관련 환경·유틸리티 기능이 설명 가능한 trade-off를 만든다.
- 직접 전투·탐험 미니게임 없이 하루 종료당 최대 한 번 개인 일정이 진행된다.
- 귀환·회수·작품 UID 상태를 분리하고 같은 UID의 복원·후속 강화·새 제작 이유로 환류한다.
- 구조 상태를 전역 고정 3일 계약으로 만들지 않는다.
- 일상 사건 완료만으로 연대기 수식어·예술성을 자동 지급하지 않는다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`

정확한 기간·확률·보상·손실·복구 비용은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## R3 — 버티컬 슬라이스 기반

- 최신 정본 전용 데이터 Schema
- 작품 UID와 저장·로드
- 단일 앱 셸과 화면 전환
- 대표 제작·강화·고객·일정·연대기 경로
- 원인 설명 로그와 로컬 검증 데이터

기존 POC의 구형 품질·보조재료·범용 수식어 구조는 재사용하지 않는다.

현재 `BS-CONTENT-20260811-01`은 이 단계의 **콘텐츠 설계**만 구체화한다. 실제 제품 구현은 열지 않는다.

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

`BS-CONTENT-20260811-01`의 플레이테스트는 작품 선택 행동과 중립적 회상 인터뷰를 함께 사용한다. 실제 playable scope와 사람 검증은 아직 `NOT_RUN`이다.

## R8 — 적대적 최종 검토

- 핵심 재미와 모바일 복잡도
- 현재 정본·구형 문서·PR·데이터 충돌
- 저장·migration·접근성·성능
- 내부 테스트와 외부 사람 플레이테스트

## 구현 Gate

현재 상태:

```yaml
R3_R7_DESIGN_ACTIVE: true
BS-CONTENT-20260811-01: USER_APPROVED_PLANNING_ONLY
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
HUMAN_PLAYTEST: NOT_RUN
VERTICAL_SLICE_TASK2: COMPLETE
NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED
```

R3–R7 기획 재개는 제품 코드·Scene·Resource·Godot authoring 범위를 자동으로 열지 않는다.

## 세 수식어 불변 계약

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

일반 수식어 A·B와 보조재료 슬롯은 재도입하지 않는다.
## R3–R7 Decision 02 — 토렌 마치 장거리 여정

- Decision: `BS-CONTENT-20260811-02 / R3_R7_2_OF_10`
- Content: `ADVENTURER_02 / TOREN_MARCH`
- 목표: `JOURNEY_CONTINUITY_AND_RELIABILITY`
- 기존 `WEIGHT / DURABILITY / ENVIRONMENTAL_SEALING / FIELD_SERVICEABILITY`만 소비하고 새 신뢰성·수리성 원수치를 만들지 않는다.
- 직접 여행·지도 경로·생존 미니게임과 자동 마모세를 추가하지 않는다.
- 결과는 도착·경로 노출·같은 UID 작품 상태를 분리해 수리·복원·후속 강화·다음 여정 신작 이유로 환류한다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

