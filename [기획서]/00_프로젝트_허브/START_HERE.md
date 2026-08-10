# [현재 정본] Blacksmith 시작 지점

<!-- CURRENT_OPERATIONAL_HANDOFF -->
> **TASK2_MAIN_MERGED / POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE**
>
> 현재 실행 가능한 동일 범위 기술 작업은 닫혔다. 새 제품 Task는 사용자 승인 없이는 추론하지 않는다.

## 현재 상태

```yaml
BLACKSMITH_BASELINE_MAIN_BEFORE_HANDOFF_REFRESH: fa9595b2df95897c915331a1cb5d9b1a583611f0
BASE_CURRENT_MAIN_OBSERVED: 49f6190b9b5a535ceb7986755c1b68b221754cf5
PROJECT_BASE_ADAPTER_PIN: 2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b
CURRENT_STAGE: R2_BATCH_006_MAIN_CANON
TASK2: TASK2_MAIN_MERGED
POSTMERGE_CLOSURE: POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE
WORK_MODE: CONTINUOUS_WORK_SCOPE_CLOSED
PRODUCT_IMPLEMENTATION: BLOCKED
NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED
HUMAN_PLAYTEST: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY: NOT_RUN
PR81: PR81_REFERENCE_ONLY_DO_NOT_MERGE
R3_R7_DESIGN_STATE: R3_R7_DESIGN_PAUSED
R3_R7_RESUME_LOCATOR: ADVENTURER_01_DETAIL_PENDING
R3_R7_RESUME_LOCATOR_AUTHORITY: NON_CANONICAL_RESUME_LOCATOR
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

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
5. `ACTIVE_CONTEXT.md`
6. `DEVELOPMENT_GATES.md`
7. `docs/decisions/BS-HIGODOT-EXEC-20260808-01_TASK2_CI_AUTHORING_BRIDGE.md`
8. `ROADMAP.md`
9. 실제 code/data/Scene/tests
10. Google Sheet `00`, `01`, `02`, `04` current rows

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
  - Full validation `31344872151` SUCCESS
  - Live-Editor Pilot `31344872263` SUCCESS
  - authority workflow `31344719243` SUCCESS

후속 복구 PR은 Task2 serialized product bytes를 다시 저작하지 않았다.

## 현재 보호 규칙

- PR #81은 `PR81_REFERENCE_ONLY_DO_NOT_MERGE`다.
- 일반 제품 구현은 `BLOCKED`다.
- Task2 완료는 Task3 또는 R3–R7 구현 승인으로 자동 확장되지 않는다.
- GUT 9.7.1은 GDScript test authority다.
- HiGodot은 승인된 Godot persistent authoring authority다.
- Hera는 enabled non-authoritative이며 authoring/mutation authority는 `NONE`이다.
- 사람 플레이테스트·Android 실기기·접근성 결과는 실제 실행 전 `NOT_RUN`이다.

## 비정본 설계 locator

`R3_R7_DESIGN_PAUSED / ADVENTURER_01_DETAIL_PENDING / NON_CANONICAL_RESUME_LOCATOR`

이 값은 대화상 브레인스토밍 재개 위치만 가리킨다. 고객 상세·R3–R7 단계·Task3 제품 범위를 정본으로 승격하지 않으며, 재개 시 반드시 최신 GitHub·Sheet·사용자 지시를 다시 읽는다.

## 다음 작업

현재 동일 범위의 기술적 blocker는 없다. 진행 중인 handoff/current-state refresh가 있으면 그것만 exact-head 검증·병합·postmerge readback까지 닫는다. 이후 제품 작업은 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED`가 해소된 뒤에만 시작한다.
