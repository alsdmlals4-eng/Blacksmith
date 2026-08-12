# Blacksmith Loop Engineering Pilot Profile

Decision: `BS-OPS-20260813-LOOP-01`

이 문서는 Base `LOOP_ENGINEERING_CONTROL_PLANE`을 Blacksmith에 처음 채택하는 프로젝트별 Pilot Profile이다. Base 공용 계약을 복제하거나 Blacksmith 정본보다 높은 권한을 만들지 않는다.

```yaml
loop_engineering_profile:
  decision_id: BS-OPS-20260813-LOOP-01
  profile_role: BLACKSMITH_PROJECT_LOOP_ENGINEERING_PILOT
  adoption_status: PILOT_ACTIVE
  BASE_LOOP_CONTRACT_COMMIT: 453f790821a108a1d4f6e1f4e45f6931c2396ee0
  blacksmith_source_main_sha: 8e9a9cf8b0b053b5bfc5667b9a1070d3b45c3486

  planning_gate_required: PLANNING_LOCKED
  current_stage: SHADOW
  current_effective_autonomy: A0_OBSERVE
  default_autonomy_after_shadow: A2_EXECUTE_ISOLATED
  a3_auto_merge_allowlist: []
  scheduler_runtime_provider: NOT_CONFIGURED

  max_agents: 2
  max_parallel_agents: 1
  max_model_calls: 12
  max_repair_cycles: 2
  max_ci_runs: 3

  product_write_policy: PRODUCT_WRITES_PROHIBITED_IN_SHADOW
  persistent_godot_authoring_gate: P0_LOCAL_EXECUTOR_BOOTSTRAP
  task3_gate: "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED"
```

## 1. 잠긴 Pilot 목표

이 Pilot의 WHAT/WHY는 다음으로 한정한다.

> Blacksmith의 승인된 기획을 바꾸지 않은 채, AI가 현재 정본·보호면·검증 상태를 읽고 작업 후보를 분해·분류하는 SHADOW 실행을 증명한다. SHADOW 검증을 통과한 뒤에만 승인된 기존 canon 범위의 기술 HOW를 격리 Branch/Worktree에서 수행하는 A2 경로를 열 수 있다.

사용자의 `블랙스미스에서 해보자` 요청은 이 운영 Pilot의 승인 근거다. 이는 Task3·신규 제품 범위·게임 코어 변경 승인이 아니다.

## 2. 현재 허용 변경

이번 Pilot 도입 PR의 writer 범위는 다음 네 경로뿐이다.

```text
docs/operations/BLACKSMITH_LOOP_ENGINEERING_PROFILE.md
docs/operations/BLACKSMITH_LOOP_RUN_CONTRACT.json
[기획서]/00_프로젝트_허브/AI_WORKFLOW.md
tests/test_ci_workflow_structure.py
```

SHADOW 실행 중에는 persistent 제품 변경을 하지 않는다. 조사·분류·정본 readback·작업 정당화·검증 계획만 기록한다.

## 3. 보호면

다음 repository root는 SHADOW에서 읽기 전용이며 A2에서도 별도 승인된 작업 계약·resource lock·검증 없이는 변경할 수 없다.

```yaml
protected_repository_roots:
  - data/
  - scripts/
  - scenes/
  - assets/
  - addons/
  - project.godot
```

다음 의미적 자원은 파일이 달라도 동일 writer lock으로 취급한다.

```yaml
semantic_resource_locks:
  - project_core
  - crafting_and_enhancement_meaning
  - economy_and_probability_authority
  - item_uid_and_lifecycle
  - save_compatibility
  - major_ux_meaning
  - input_meaning
  - approved_content_causality
  - Godot_persistent_authoring
```

특히 다음을 자동으로 추론하지 않는다.

- 승인되지 않은 Decision10 또는 Task3 생성
- 직접 전투·투기장 운영·베팅·여행 조작·공장/병참 범위 추가
- 작품 UID 역사 덮어쓰기
- 제작·강화·경제 수치 변경
- Base v9.4.3 project adapter pin 자동 승격
- repository workflow·ruleset·권한 변경
- 이미지 생성 또는 승인 자산 변경

## 4. SHADOW 계약

SHADOW는 `A0_OBSERVE`다.

```text
현재 main·정본·보호면 readback
→ 동일 Goal의 열린 PR·Branch 확인
→ 승인된 canon과 실제 구현 차이 분류
→ WORK_JUSTIFICATION_GATE 작성
→ Task DAG·의존성·RESOURCE_LOCK 후보 작성
→ 필요한 Evidence 수준 지정
→ 실행하지 않고 검증 결과 보고
```

각 작업 후보는 다음을 모두 가져야 한다.

```yaml
WORK_JUSTIFICATION_GATE:
  problem:
  evidence:
  player_or_user_value:
  risk_if_ignored:
  expected_outcome:
  verification:
```

승인된 acceptance criterion, 실제 bug/regression, 검증된 canon drift, 승인 구현의 기술 의존성 중 어느 것에도 연결되지 않으면 `IMPROVEMENT_CANDIDATE / DEFER`다.

## 5. A2 승격 Gate

SHADOW에서 A2로 승격하려면 다음을 모두 충족해야 한다.

1. Pilot Profile과 Run Contract의 exact-head CI가 PASS다.
2. 도입 PR diff에 보호된 제품 root 변경이 0개다.
3. 현재 main SHA와 Run의 `source_main_sha`가 일치하거나 최신 main으로 재조정됐다.
4. P0/P1 적대적 finding과 unresolved review thread가 0개다.
5. Builder와 최종 Verifier/Critic 역할을 분리한다.
6. 첫 A2 Task가 이미 승인된 Blacksmith canon 범위에 있고 별도 `LOOP_RUN_CONTRACT`로 잠긴다.
7. Godot persistent authoring이 필요하면 `P0_LOCAL_EXECUTOR_BOOTSTRAP`과 Codex 내부 fresh HiGodot receipt를 먼저 통과한다.

A2는 다음까지만 허용한다.

```text
exact main에서 격리 Branch/Worktree 생성
→ TASK_LEASE + RESOURCE_LOCK
→ 승인된 HOW 구현
→ 정적/GUT/필요한 실제 runtime 검증
→ 독립 적대적 검토
→ PR
```

A2가 project core, player experience, major UX, save/data 의미, Task3 또는 새 제품 범위를 바꿔야만 진행할 수 있으면 `PLANNING_CONFLICT / USER_DECISION_REQUIRED`다.

## 6. A3·지속 실행·자기개선

- `a3_auto_merge_allowlist: []`는 fail-closed 기본값이다. 이번 Pilot에서 자동 병합 범주를 만들지 않는다.
- `scheduler_runtime_provider: NOT_CONFIGURED`다. 이 파일은 24/7 scheduler, webhook, daemon 또는 상시 Agent를 설치하지 않는다.
- 실행 경험은 `Learning != Canon`이다. 반복 관찰은 `IMPROVEMENT_CANDIDATE`로 남기고 공용 변경은 기존 BCP 경계를 거친다.

## 7. Evidence ceiling

```text
E0_CONTRACT       Pilot 계약 존재
E1_STATIC         JSON·경로·정본·보호면 검사
E2_TEST           자동화 계약 테스트
E3_RUNTIME        실제 앱/엔진 runtime
E4_VISUAL         실제 render/screenshot
E5_PLAY           실제 플레이
E6_HUMAN_PLAYTEST 사람 플레이테스트
```

이번 도입 PR의 목표 ceiling은 E2다. Godot runtime, Android 실기기, 시각 결과, 사람 플레이테스트는 제품 변경이 없으므로 실행하지 않으며 각각 `NOT_RUN` 또는 `HUMAN_NOT_RUN`으로 유지한다.

## 8. 실패·중지·롤백

다음은 즉시 해당 Task를 중지한다.

- `STALE_BASE_SHA`
- `RESOURCE_COLLISION`
- `PROTECTED_SURFACE`
- `PLANNING_CONFLICT`
- `BUDGET_EXCEEDED`
- `RETRY_LIMIT`
- `NO_PROGRESS`

Rollback은 이 도입 PR의 네 경로를 이전 main 상태로 되돌리는 것이다. 제품 root를 건드리지 않았으므로 제품 save/data/runtime rollback은 발생하지 않는다.

## 9. 검증

```text
python -m unittest tests/test_ci_workflow_structure.py -v
python -m unittest discover -s tests -p "test_*.py" -v
GitHub PR exact-head required checks
post-merge main readback
```

완료 보고는 실제 diff, exact SHA, 실행한 검증, 미실행 Evidence, 남은 위험, rollback을 분리한다.
