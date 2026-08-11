# Blacksmith Dedicated Local Executor Bootstrap Implementation Plan

Decision: `BS-OPS-20260811-03`

Design: `docs/superpowers/specs/2026-08-11-blacksmith-dedicated-local-executor-bootstrap-design.md`

Execution mode: inline, test-first, planning-complete Phase B closure followed by bounded Phase C bootstrap implementation.

## Goal

Create a durable Blacksmith-specific one-shot PowerShell launcher and authority record so every local implementation session starts or safely reuses the exact isolated environment:

`self-contained Godot 4.7.1 → HiGodot 8006/9506 → dedicated CODEX_HOME → Codex in exact Blacksmith project`.

The launcher configures local execution infrastructure only. It does not author gameplay or claim HiGodot readiness by itself.

## Task 1 — Semantic RED contract

Files:
- create `tests/test_blacksmith_dedicated_local_executor_bootstrap.py`
- modify `.github/workflows/python-validation.yml`

The test must require, before implementation exists:

- Decision `BS-OPS-20260811-03` current authority record;
- planning-complete / Phase C entry state;
- exact project path;
- Godot 4.7.1 dedicated path and `_sc_` self-contained contract;
- ports 8006 / 9506;
- dedicated `C:\Users\user\.codex-blacksmith`;
- one-shot PowerShell launcher file;
- fail-closed port policy with no automatic kill;
- no reset/restore/clean/stage behavior;
- exact matching editor reuse path;
- current Codex `CODEX_HOME`/MCP config tokens;
- fresh HiGodot readiness required before mutation;
- product implementation entry opened only for already-approved canon;
- Task3 still separately gated;
- image generation deferred.

Run in GitHub Actions. RED is valid only if checkout/Python are healthy and failures are semantic absence/current-state failures.

## Task 2 — Implement the one-shot PowerShell launcher

Create `tools/start_blacksmith_local_executor.ps1`.

Implementation requirements:

1. Strict mode and stop-on-error.
2. Exact constants for Blacksmith path, Godot version, target executable, HTTP 8006, WS 9506, CODEX_HOME.
3. Fail if `project.godot` is absent.
4. Detect exact matching dedicated Godot process before deciding whether to launch another.
5. Inspect 8006/9506 listener ownership; never kill processes.
6. If ports are occupied without safe exact-session reuse, print PID/process/path/command line when available and stop.
7. If dedicated Godot is absent:
   - look for exact local exe or zip under Downloads;
   - otherwise download official 4.7.1 standard Windows zip;
   - extract/copy only into the dedicated target;
   - create `_sc_`;
   - verify `--version` contains `4.7.1`.
8. If first-time self-contained editor settings are absent, initialize with a bounded headless editor recovery launch that disables normal plugin startup, then locate the created `editor_settings-4*.tres`.
9. Back up an existing settings file before changing Blacksmith-owned keys.
10. Set only `godot_ai/http_port = 8006`, `godot_ai/ws_port = 9506`, and `godot_ai/keep_server_on_exit = true` in the dedicated editor settings.
11. Create CODEX_HOME before exporting it.
12. Create/refresh a Blacksmith-managed `config.toml` with `approval_policy = never`, `sandbox_mode = workspace-write`, network access, and required `godot-ai` HTTP MCP at `http://127.0.0.1:8006/mcp` with 60/360 second timeouts.
13. If an unmarked existing config is present, stop instead of overwriting it.
14. Start the dedicated editor if not reused.
15. Bound readiness opportunity wait; require both 8006 and 9506 listening before Codex launch.
16. Start Codex from exact Blacksmith directory in the same PowerShell environment.
17. Print a clear mandatory instruction that the first Codex action is fresh HiGodot project/session/version/readiness verification before persistent mutation.
18. No product files are modified by the bootstrap.

## Task 3 — Canonize the Phase B / local executor binding

Create:
- `docs/decisions/BS-OPS-20260811-03_DEDICATED_LOCAL_EXECUTOR_BOOTSTRAP.md`

Update current consumers minimally:
- `CURRENT_CONFIRMED_DECISIONS.md`
- `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- `[기획서]/00_프로젝트_허브/START_HERE.md`
- `[기획서]/00_프로젝트_허브/ROADMAP.md`
- `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- `docs/PROJECT_OPERATING_HEALTH.json` if its current-authority hash changes

Required state transition:

```text
PLANNING_COMPLETE: USER_DECLARED
R3_R7_PLANNING_BATCH: CLOSED_AT_9_OF_10
PHASE_B_FINAL_REVIEW: COMPLETE
PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON
TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED
P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING
IMAGE_GENERATION: DEFERRED_BY_USER
```

Do not rewrite Decisions01–09 or resolve `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED` silently.

## Task 4 — GREEN and focused regression

Run:
- bootstrap contract test;
- project core alignment;
- current/historical R3–R7 tests that own moving-current gates;
- project operating audit wrapper;
- compile/static checks for Python tests;
- PowerShell syntax parse if a Windows/PowerShell runner exists; otherwise add a deterministic static syntax/safety contract and mark actual Windows execution `NOT_RUN` until user runs the launcher.

The bootstrap contract must distinguish static correctness from real local runtime evidence.

## Task 5 — Adversarial review / POST_CHANGE_MONITOR_LOOP

Attack:
- stale `PRODUCT_IMPLEMENTATION_BLOCKED` active mirrors after planning-complete;
- accidental Task3 activation;
- invented Decision10;
- global `%APPDATA%\Godot` mutation;
- global `~/.codex` mutation;
- wrong 8000/9500 defaults;
- auto port reassignment;
- `Stop-Process`, `taskkill`, reset/restore/clean/stage commands;
- duplicate editor start;
- port-listener-only readiness claim;
- embedded credentials;
- product Scene/Resource/script mutation inside bootstrap;
- Base/Sheet drift;
- same-goal duplicate PR.

Classify each finding as `OMISSION / CONFLICT / COMPLEMENT_GAP / DUPLICATE_WORK / NO_MATERIAL_FOLLOWUP`, fix minimally, rerun regression.

## Task 6 — Exact-head CI and merge

- Ensure draft PR owns this single goal.
- Validate required workflows on one exact head.
- Review comments/threads and same-goal PR inventory.
- Mark ready only after exact-head success.
- Re-run ready-triggered adapter checks on the same head if applicable.
- Merge within inherited user approval with expected-head lock.
- Re-read merged `main`.

## Task 7 — Same-ID Sheet sync

After merge only, write `BS-OPS-20260811-03` to current hub/work-order/decision/change-log surfaces and update the gate from planning-only to planning-complete Phase C entry while preserving Task3 separate gate and P1 taxonomy deferment.

Re-read exact ranges and only then mark `POSTMERGE_READBACK_PASS`.

## Task 8 — User local execution handoff

Provide one self-contained PowerShell block, not multiple manual startup instructions.

The block must be usable after the user closes every previous PowerShell session. It must rebuild shell-scoped state every time.

The user then pastes the block. First actual local receipt expected from Codex/HiGodot:

```text
project identity: Blacksmith exact path
Godot: dedicated 4.7.1 self-contained editor
HiGodot HTTP: 8006
HiGodot WS: 9506
Codex HOME: C:\Users\user\.codex-blacksmith
fresh HiGodot session/version/readiness: PASS required before mutation
```

Actual Windows bootstrap execution, editor UI state, live ports, Codex authentication, and HiGodot live receipt remain `NOT_RUN` until observed locally.

## Base #288 reconciliation task

Fresh Base main `6d2feba2bc49fda2d8d273248b55087853615d5d` directly strengthens this goal. Before exact-head acceptance:

- [x] require `ASSUME_PREVIOUS_POWERSHELL_CLOSED`;
- [x] require `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`;
- [x] require `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`;
- [x] invoke Codex with `-C` and the exact Blacksmith project path;
- [x] preserve HiGodot persistent-authoring exclusivity and Hera live-QA/non-authoring boundary;
- [x] keep port/process existence as bootstrap evidence only;
- [x] preserve no destructive Git/process side effects.

The Base #288 follow-up used a new semantic RED before these production tokens were added.
