# [현재 정본] Blacksmith 시작 지점

<!-- R3_R7_DESIGN_RESUMED -->
> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-02 / ADVENTURER_02_TOREN_LONG_RANGE_RELIABILITY_APPROVED / PLANNING_ONLY**
>
> Task2 기술 작업은 폐쇄 상태를 유지한다. R3–R7 기획은 재개됐지만 새 제품 Task나 Task3 구현은 별도 사용자 승인 없이는 추론하지 않는다.

## 현재 상태

```yaml
BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_02_START: cb5ceff127bf4f2adb38b34ebaa092d97111fa94
BASE_CURRENT_MAIN_OBSERVED: 315c66eea9614c284b9c11c4d522141065dfa4b0
PROJECT_BASE_ADAPTER_PIN: 2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b
CURRENT_STAGE: R3_R7_DESIGN_ACTIVE
R2_BASELINE: R2_BATCH_006_MAIN_CANON
R2_CHECKPOINT_004: HISTORICAL_MERGED_MAIN_CANON
R2_BATCH_005: R2_BATCH_005_CLOSED_10_OF_10
TASK2: TASK2_MAIN_MERGED
POSTMERGE_CLOSURE: POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE
WORK_MODE: PLAN_REVIEW
PRODUCT_IMPLEMENTATION: BLOCKED
NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED
TASK3_IMPLEMENTATION: NOT_APPROVED
HUMAN_PLAYTEST: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY: NOT_RUN
PR81: PR81_REFERENCE_ONLY_DO_NOT_MERGE
R3_R7_DESIGN_STATE: R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 2/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-02
R3_R7_RESUME_LOCATOR: ADVENTURER_02_TOREN_LONG_RANGE_RELIABILITY_APPROVED
```

`BASE_CURRENT_MAIN_OBSERVED`는 작업 시작 때 읽은 공유 Base 원격 main이다. `PROJECT_BASE_ADAPTER_PIN`은 Blacksmith가 현재 채택해 검증하는 Base 계약 pin이다. 둘은 자동 동기화 대상이 아니며, 원격 main이 전진했다고 프로젝트 pin을 임의 변경하지 않는다.

## 프로젝트 약속

> 제한된 하루 작업량 안에서 작품을 만들고 강화 위험 앞에서 멈출지 더 도전할지 선택하며, 같은 UID 작품이 고객과 세계에서 겪은 생애 결과를 돌려받는 Android 세로형 제작 게임.

현재 코어:

```text
직접 단조
→ 제작 등급·예술성·역할 수치 확정
→ 일반 강화 지속·중단 판단
→ 정밀강화 방식·촉매 선택
→ 고객·일정에 작품 전달
→ 같은 UID의 결과·연대기·손상·복원
→ 다음 제작 판단
```

대표 예술성 표기는 `예술성 27`이며 고정 설계 최대치는 없다. 상세 생성·성장·가치 계약은 `BS-CRAFT-20260805-02`와 R2 Game Bible이 책임진다.

## 현재 R3–R7 설계 재개

사용자 승인 Decision: `BS-CONTENT-20260811-01`.

```text
ADVENTURER_01 / NADIA_VENN
나디아 벤 유적 탐사 개인 일정
생환 + 회수
→ 작품 한 점 인계
→ 하루 종료당 최대 한 번 진행
→ 즉시 인과 결과
→ 같은 UID의 지연 생애
→ 복원·후속 강화·새 제작 이유
```

- 직접 전투·탐험 미니게임은 추가하지 않는다.
- 단일 항상최적 장비 정답은 만들지 않는다.
- 구조 상태를 고정 3일 일정으로 해석하지 않는다.
- 사건 완료만으로 연대기 수식어·예술성을 자동 지급하지 않는다.
- 정확한 기간·확률·보상·손실은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

첫 Decision `BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`은 승인 완료 이력으로 유지한다.

현재 사용자 승인 Decision: `BS-CONTENT-20260811-02`.

```text
ADVENTURER_02 / TOREN_MARCH
장거리 여정 지속성·신뢰성
→ 기존 중량·강화·내구도·실제 관련 환경/현장정비 기능 비교
→ 작품 한 점 인계
→ 비직접 여정 진행
→ 도착·경로 노출·같은 UID 작품 상태 결과
→ 수리·복원·후속 강화·다음 여정 신작 이유
```

- 직접 이동·지도 경로 선택·실시간 생존 조작을 추가하지 않는다.
- 새 신뢰성·휴대성·수리 용이성 원수치를 만들지 않는다.
- 자동 매일 내구도 감소·루틴 수리세를 만들지 않는다.
- 정확한 값은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

책임 원본:

1. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
2. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
3. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
7. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
7. `ACTIVE_CONTEXT.md`
8. `DEVELOPMENT_GATES.md`
9. `ROADMAP.md`
10. 실제 code/data/Scene/tests
11. Google Sheet `00`, `01`, `02`, `04`, `13`, `50` current rows

## Task2 폐쇄 증거

- Task2 product provenance:
  - PROVE input `02420ebd3bcdd86776c4ab70824738aa4071a168`
  - PROVE run `31341840236`
  - provenance artifact `9046072682`
  - serialized publish `8afb9a439df46eec3568a75d7f2536b89e1edaba`
  - approved head `345cf339e2af754d447099dd8e1b278b80b849d5`
  - Task2 merge main `a61a0bceec4254c4b78350980275cc9a903f9042`
- same-scope postmerge recovery:
  - PR #139 merged `7ccee408cf5c936ae9302a986fa0c786e0247078`
  - PR #140 merged `fa9595b2df95897c915331a1cb5d9b1a583611f0`
  - PR #141 handoff refresh merged `68540e6cd288aff138b1ea4c5b1feeb9e0653947`
  - Full validation `31357963490` SUCCESS
  - Live-Editor Pilot `31357963734` attempt 2 SUCCESS

후속 복구 PR은 Task2 serialized product bytes를 다시 저작하지 않았다.

## 현재 보호 규칙

- PR #81은 `PR81_REFERENCE_ONLY_DO_NOT_MERGE`다.
- 일반 제품 구현은 `BLOCKED`다.
- Task2 완료 또는 R3–R7 기획 재개는 Task3 구현 승인으로 자동 확장되지 않는다.
- `BS-CONTENT-20260811-01`은 대장장이의 작품 선택·인과 판독·같은 UID 생애 환류를 보호한다.
- GUT 9.7.1은 GDScript test authority다.
- HiGodot은 승인된 Godot persistent authoring authority다.
- Hera는 enabled non-authoritative이며 authoring/mutation authority는 `NONE`이다.
- 사람 플레이테스트·Android 실기기·접근성 결과는 실제 실행 전 `NOT_RUN`이다.

## 다음 작업

현재 연속 작업은 `BS-CONTENT-20260811-02`의 GitHub·Sheet 동기화, exact-head 검증, 적대적 검토까지다. 다음 신규 R3–R7 Decision은 승인 카운터 `2/10`에서 이어간다. 제품 코드·Scene·Resource·Task3는 별도 사용자 승인 전 시작하지 않는다.
