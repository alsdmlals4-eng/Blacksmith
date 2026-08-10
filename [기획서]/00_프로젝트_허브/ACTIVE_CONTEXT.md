# [현재 정본] Active Context

<!-- CURRENT_OPERATIONAL_HANDOFF -->
> **TASK2_MAIN_MERGED / POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE**
>
> 이 문서는 현재 상태와 다음 읽기 순서를 연결하는 압축 라우터다. 세부 Decision·과거 단계·실행 로그는 책임 원본에서 읽는다.

- 갱신 기준: `2026-08-10 KST`
- Blacksmith baseline main before this handoff refresh: `fa9595b2df95897c915331a1cb5d9b1a583611f0`
- `BASE_CURRENT_MAIN_OBSERVED`: `49f6190b9b5a535ceb7986755c1b68b221754cf5`
- `PROJECT_BASE_ADAPTER_PIN`: `2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b`
- Base current main 관측값과 프로젝트가 채택한 Base adapter pin은 서로 다른 증거다. 새 Base main 관측만으로 프로젝트 pin을 자동 승격하지 않는다.

```yaml
CURRENT_STAGE: R2_BATCH_006_MAIN_CANON
R2_BATCH_006: R2_BATCH_006_APPROVED_10_OF_10
R2_BATCH_006_MERGE: MERGED_PR120_MAIN_CANON
VERTICAL_SLICE_IMPLEMENTATION: VERTICAL_SLICE_IMPLEMENTATION_APPROVED_TASK2_COMPLETE
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

## 현재 완료 상태

- Task 1 UID·SaveEnvelope는 main 정본으로 병합됐다.
- Task 2 MainMenu → BlacksmithApp → Workshop 시작 경로와 `project.godot application/run/main_scene` 전환은 HiGodot provenance를 거쳐 병합됐다.
- `BS-HIGODOT-EXEC-20260808-01` Task2 제품 provenance:
  - PROVE input: `02420ebd3bcdd86776c4ab70824738aa4071a168`
  - PROVE run: `31341840236`
  - provenance artifact: `9046072682`
  - serialized publish commit: `8afb9a439df46eec3568a75d7f2536b89e1edaba`
  - approved PR branch head: `345cf339e2af754d447099dd8e1b278b80b849d5`
  - Task2 merge main: `a61a0bceec4254c4b78350980275cc9a903f9042`
- 후속 CI 복구는 제품 직렬화 bytes를 바꾸지 않았다.
  - PR #139 merge main: `7ccee408cf5c936ae9302a986fa0c786e0247078`
  - PR #140 merge/current technical baseline: `fa9595b2df95897c915331a1cb5d9b1a583611f0`
  - Full validation: run `31344872151` SUCCESS
  - Live-Editor Pilot: run `31344872263` SUCCESS
  - PR #140 authority workflow: run `31344719243` SUCCESS

## 현재 권위와 보호 경계

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
5. 이 문서와 `START_HERE.md`, `DEVELOPMENT_GATES.md`, `ROADMAP.md`
6. 실제 code/data/Scene/tests
7. Google Sheet — 같은 Decision과 상태를 연결하는 소비처

불변 보호:

- PR #81 전체 병합 금지.
- 일반 제품 구현은 `BLOCKED`.
- Task2 완료를 새로운 Task3/R3 구현 승인으로 해석하지 않는다.
- 사람 플레이테스트·Android 실기기·접근성은 실제 실행 전 `NOT_RUN`.
- HiGodot은 승인된 Godot persistent authoring 권위, GUT 9.7.1은 GDScript test 권위, Hera는 enabled non-authoritative / `AUTHORITY_NONE`이다.

## 비정본 설계 재개 지점

`R3_R7_DESIGN_PAUSED / ADVENTURER_01_DETAIL_PENDING / NON_CANONICAL_RESUME_LOCATOR`

이 표시는 과거 대화에서 멈춘 브레인스토밍 위치를 찾기 위한 locator일 뿐, 새 제품 범위·고객 상세·Task3 구현 승인 또는 current canon이 아니다. 실제 재개 시 GitHub main·Sheet·현재 사용자 지시를 다시 읽고 새 제품 범위 승인을 확인한다.

## 다음 실행 순서

1. 현재 main과 열린 PR을 다시 읽는다.
2. 이 handoff refresh가 아직 PR이면 exact-head CI·적대적 검토 후 같은 운영 범위로 병합한다.
3. 병합 후 새 main과 Sheet를 readback한다.
4. 새 제품 작업은 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED`가 해소될 때까지 시작하지 않는다.
5. R3–R7 기획 재개가 승인되면 위 비정본 locator에서 참고 대화를 회수하되 저장소 정본과 충돌하는 내용은 폐기한다.

## 먼저 읽을 파일

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/decisions/BS-HIGODOT-EXEC-20260808-01_TASK2_CI_AUTHORING_BRIDGE.md`
5. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
6. Google Sheet `00_프로젝트_허브`, `01_작업순서`, `02_현재_확정결정`, `04_누락_충돌_감사`
