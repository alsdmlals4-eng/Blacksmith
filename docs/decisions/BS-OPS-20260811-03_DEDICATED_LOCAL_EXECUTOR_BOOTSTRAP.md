# BS-OPS-20260811-03 — Dedicated Local Executor Bootstrap and Phase C Entry

Status: `USER_APPROVED / PLANNING_COMPLETE_DECLARED / PHASE_B_FINAL_REVIEW_COMPLETE / PHASE_C_ENTRY_APPROVED`

Date: 2026-08-11 KST

## Decision

사용자가 명시적으로 `기획 완료`를 선언했고, 이미지 생성은 보류한 채 Plan C 구현으로 진행하도록 승인했다.

R3–R7 기획 배치는 승인된 9개 Decision에서 닫는다. `10`은 승인 배치 최대치이며 10번째 콘텐츠 Decision을 채우기 위한 의무값이 아니다. 따라서 승인되지 않은 Decision10을 생성하지 않는다.

```text
PLANNING_COMPLETE: USER_DECLARED
R3_R7_PLANNING_BATCH: CLOSED_AT_9_OF_10
PHASE_B_FINAL_REVIEW: COMPLETE
PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON
TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED
P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING
IMAGE_GENERATION: DEFERRED_BY_USER
P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED
```

`기획 완료`는 현재까지 승인된 정본을 구현할 수 있게 하는 Phase C 진입 승인이다. 승인되지 않은 신규 게임 시스템, 범위 확대, 역사적 Task3를 자동 승인하지 않는다.

## Blacksmith dedicated local environment

모든 로컬 PowerShell 구현 블록은 제품 작업보다 먼저 아래 전용 실행환경을 생성 또는 재사용한다.

```yaml
project_path: C:\Users\user\Documents\GitHub\Ninza\Blacksmith
godot_project_path: C:/Users/user/Documents/GitHub/Ninza/Blacksmith
godot_version: 4.7.1-stable
dedicated_godot_dir: C:\Users\user\Tools\Godot-Blacksmith-4.7.1
dedicated_godot_exe: C:\Users\user\Tools\Godot-Blacksmith-4.7.1\Godot_v4.7.1-stable_win64.exe
self_contained_marker: _sc_
higodot_http_port: 8006
higodot_ws_port: 9506
codex_home: C:\Users\user\.codex-blacksmith
codex_approval_policy: never
codex_sandbox_mode: workspace-write
powershell_session: EPHEMERAL_CLOSE_AND_FRESH_START_EACH_EXECUTION_BLOCK
```

실행 순서:

```text
전용 self-contained Godot 4.7.1 확보/검증
→ `_sc_` 격리 확인
→ Blacksmith 전용 EditorSettings에 HTTP 8006 / WS 9506 / keep-server-on-exit ON
→ 포트 소유권 확인 및 exact Blacksmith editor reuse-or-start
→ 전용 CODEX_HOME 생성/검증
→ godot-ai HTTP MCP를 8006으로 바인딩
→ 8006/9506 startup opportunity 확인
→ 정확 Blacksmith 경로에서 Codex 실행
→ Codex 내부에서 fresh HiGodot project/session/version/readiness receipt
→ 그 뒤에만 persistent Godot mutation
```

실행 스크립트 정본:

`tools/start_blacksmith_local_executor.ps1`

## Isolation and safety

```text
BOOTSTRAP_ORCHESTRATION_ONLY
PORT_CONFLICT_FAIL_CLOSED
EXACT_BLACKSMITH_EDITOR_REUSE
UNMANAGED_CODEX_CONFIG_FAIL_CLOSED
POST_BOOTSTRAP_LIVE_READINESS_NOT_PROVEN
FRESH_HIGODOT_READINESS_REQUIRED_BEFORE_MUTATION
```

- 일반 Godot `%APPDATA%` 설정을 수정하지 않는다.
- 다른 프로젝트의 Godot/HiGodot/Codex 프로필을 재사용하지 않는다.
- HTTP/WS 포트가 미확인 프로세스에 점유됐으면 프로세스를 죽이거나 포트를 훔치지 않고 중단한다.
- 8006/9506을 다른 번호로 자동 변경하지 않는다.
- 이전 PowerShell 세션 상태를 신뢰하지 않는다. 매 실행 블록에서 `CODEX_HOME`, 경로, 전용 Godot, 포트를 다시 해석한다.
- bootstrap은 local infrastructure configuration만 수행하며 제품 Scene/Node/Resource/script/project-setting 저작 권위를 갖지 않는다.
- 포트 listen이나 프로세스 존재는 HiGodot readiness PASS가 아니다.
- 실제 persistent Godot authoring은 프로젝트가 채택한 HiGodot 권위와 fresh live receipt 뒤에만 수행한다.
- GUT은 deterministic GDScript test authority를 유지하고, Hera는 별도 현재 채택 조건 안에서 live QA/observability만 수행한다.

## Phase B final review result

현재 승인 정본은 구현 패키지로 분해해 순차 진행한다.

1. `P0_LOCAL_EXECUTOR_BOOTSTRAP`
2. `P1_AUTHORITY_AND_CURRENT_STATE_READBACK`
3. `P2_FOUNDATION_DATA_AND_STATE_CONTRACTS`
4. `P3_APPROVED_CONTENT_VERTICAL_IMPLEMENTATION`
5. `P4_RUNTIME_UX_AND_FEEDBACK`
6. `P5_GUT_AFFECTED_FULL_REGRESSION`
7. `P6_HERA_LIVE_QA_IF_CURRENTLY_ADOPTED_AND_REQUIRED`
8. `P7_EXACT_HEAD_PR_AND_POSTMERGE_READBACK`
9. `P8_USER_LOCAL_FETCH_PULL_PROJECT_PLAY`

각 패키지는 Existing Solution First, TDD RED→GREEN→REFACTOR, 적대 검토, exact-head evidence를 다시 적용한다. 한 번에 저장소 전체를 고충격 재작성하지 않는다.

## Preserved decisions and unresolved items

- `BS-CONTENT-20260811-01` ~ `BS-CONTENT-20260811-09`는 승인된 R3–R7 기획 정본으로 보존한다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 별도 승인 없이 해결하지 않는다.
- `TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED`를 유지한다.
- 이미지 생성은 `DEFERRED_BY_USER`다.
- 사람 플레이테스트, Android 실기기, 접근성, 실제 Windows bootstrap 실행은 실제 관측 전까지 `NOT_RUN`이다.

## Evidence boundary

이 Decision/스크립트가 GitHub CI에서 통과해도 다음은 자동 PASS가 아니다.

```text
WINDOWS_LOCAL_BOOTSTRAP: NOT_RUN until user executes
DEDICATED_GODOT_EDITOR_LIVE: NOT_RUN until observed
HIGODOT_8006_9506_LIVE: NOT_RUN until observed
CODEX_DEDICATED_PROFILE_LIVE: NOT_RUN until observed
FRESH_HIGODOT_SESSION_READINESS: NOT_RUN until observed
HUMAN_PLAYTEST: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY: NOT_RUN
```

## Sources and Existing Solution First

- Base current `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` 및 `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY` 정책을 소비한다.
- Blacksmith vendored Godot AI 3.1.4의 `godot_ai/http_port`, `godot_ai/ws_port`, `godot_ai/keep_server_on_exit`, Codex `CODEX_HOME` 지원을 재사용한다.
- Godot self-contained `_sc_`와 Codex custom home/MCP 구성을 프로젝트 전용 값으로 바인딩한다.

본 Decision은 새 제품 기능이 아니라 이미 승인된 제품 구현을 안전하게 시작하기 위한 실행 환경 및 Phase 전환 정본이다.

## Current Base dedicated-environment authority

Fresh same-goal Base main observed before Blacksmith acceptance:

`6d2feba2bc49fda2d8d273248b55087853615d5d` — `docs: require project-dedicated local execution environment (#288)`

Blacksmith consumes the shared invariants with project-owned concrete values:

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP
BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY
```

The executor launch is additionally pinned with `codex -C C:\Users\user\Documents\GitHub\Ninza\Blacksmith`. A dedicated PowerShell is a fresh PowerShell process with the Blacksmith environment injected; it is not a second PowerShell installation.

## Postmerge hardening — strict project/editor/port isolation

`POST_CHANGE_MONITOR_LOOP` after PR #155 found two material complement gaps in the local launcher:

1. a non-dedicated Godot executable could already target the exact Blacksmith project while the bootstrap started the dedicated editor, creating duplicate same-project editors;
2. when no exact dedicated Blacksmith editor was alive, a retained listener that merely looked like godot-ai could be accepted without proving it belonged to Blacksmith.

These violate the user's strict project-port isolation rule. The same Decision `BS-OPS-20260811-03` is hardened without adding product scope.

```text
NON_DEDICATED_BLACKSMITH_EDITOR_CONFLICT_FAIL_CLOSED
MULTIPLE_DEDICATED_BLACKSMITH_EDITORS_FAIL_CLOSED
UNVERIFIED_RETAINED_SERVER_REUSE_FORBIDDEN
PORT_CONFLICT_FAIL_CLOSED
```

New behavior:

- enumerate Godot processes that target the exact Blacksmith path;
- allow at most one exact dedicated Blacksmith editor;
- any other Godot executable targeting Blacksmith stops the bootstrap without killing it;
- if the exact dedicated editor is absent, any occupied 8006/9506 listener stops the bootstrap, even when its process resembles godot-ai;
- retained listener reuse is allowed only as part of an already-running exact dedicated Blacksmith editor session, and still does not replace the required fresh HiGodot receipt inside Codex.

Semantic RED evidence for this hardening:

- PR #156 test-only head `a9fd56b97e53675278a625c0fbbb7346bd33a622`
- PR validation run `31498561843`
- Python job `93802395639`
- checkout/Base/Python/PowerShell parser/project-core/existing bootstrap tests all passed before the new isolation test;
- the new isolation test failed specifically because `NON_DEDICATED_BLACKSMITH_EDITOR_CONFLICT_FAIL_CLOSED` and the stricter orphan-port policy were not yet implemented.

## 2026-08-12 same-ID local executor runtime hardening

This is a bounded correction under `BS-OPS-20260811-03`, not a new Decision
and not gameplay implementation.

- The managed `CODEX_HOME/config.toml` writer constructs an explicit line list,
  joins it with LF only, and calls `System.IO.File.WriteAllText` with
  `System.Text.UTF8Encoding($false)`. The managed marker, fail-closed unmanaged
  config check, 8006 MCP URL, approval, sandbox, network, and timeout settings
  remain required.
- When no exact dedicated Blacksmith editor exists, the launcher may clean up
  only `VERIFIED_BLACKSMITH_RETAINED_SERVER` / `OLD_BLACKSMITH_RETAINED_SERVER`:
  exactly one HTTP 8006 listener and one WS 9506 listener, one shared PID,
  a `godot-ai`/`godot_ai` command line with `--port 8006`, `--ws-port 9506`,
  and `app_userdata/Blacksmith/godot_ai_server.pid`.
- The candidate identity is rechecked immediately before `Stop-Process -Id`.
  The launcher also rechecks that neither an exact nor a conflicting Blacksmith
  editor appeared after the original snapshot; that race fails closed without
  stopping a process.
  No name-based, broad, foreign, unknown, partial, or multi-listener process
  termination is permitted. Both ports must release within the bounded wait or
  the launcher fails closed.
- An exact dedicated editor suppresses retained-server cleanup. Any state that
  does not meet every predicate retains
  `UNVERIFIED_RETAINED_SERVER_REUSE_FORBIDDEN` and `PORT_CONFLICT_FAIL_CLOSED`.
- Bootstrap remains orchestration only. A fresh exact HiGodot session,
  `editor_state`, `scene_get_hierarchy`, and `settings_get` receipt remains
  required before persistent Godot authoring.
