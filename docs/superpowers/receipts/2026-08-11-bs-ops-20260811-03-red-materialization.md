# BS-OPS-20260811-03 RED / Materialization Receipt

Date: 2026-08-11 KST

Decision: `BS-OPS-20260811-03`

## Semantic RED

PR: `#155`

RED branch head: `a1f38a8d7de1ff5192a9c6c93652653aaf44853b`

PR validation:
- run `31493577064`
- Python job `93785706135`

Infrastructure before failure:
- checkout: PASS
- pinned Base checkout: PASS
- Python 3.12 setup: PASS
- merge conflict contract: PASS
- existing project core / R3 tests before the new test: PASS

New contract result:
- `test_approved_design_and_plan_exist`: PASS
- four implementation/current-state tests: FAIL

Semantic failure causes:
- `docs/decisions/BS-OPS-20260811-03_DEDICATED_LOCAL_EXECUTOR_BOOTSTRAP.md` did not yet exist;
- `tools/start_blacksmith_local_executor.ps1` did not yet exist.

This is a valid semantic RED rather than YAML/import/infrastructure failure.

## Materialization

Implementation artifacts added after RED:
- `tools/start_blacksmith_local_executor.ps1`
- `docs/decisions/BS-OPS-20260811-03_DEDICATED_LOCAL_EXECUTOR_BOOTSTRAP.md`
- Phase C current-authority blocks in Current Decisions / Active Context / Start Here / Roadmap / Development Gates
- refreshed `BS-CURRENT-DECISIONS` operating-health digest

One-shot materializer run:
- workflow run `31494338033`
- job `93788185971`
- result: SUCCESS
- materialized commit: `13d0a639536d6aaeaf088cf469bb228fbc80d367`
- temporary materializer script and temporary workflow removed in the same materialized commit.

The PR workflows emitted for the bot-authored materialized commit were `action_required`, not test failures. A subsequent user-authored evidence commit was used to trigger normal GREEN/regression validation.

## Phase C moving-current regression repairs

### Finding 1 — project-core alignment still owned the planning-only product gate

Classification: `CONFLICT / MUST_FIX`.

Evidence:
- PR validation run `31494596091`
- PowerShell parser step: PASS
- failure: project-core alignment expected `GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED` in the current Development Gates.

Repair:
- moved only current gate expectations to `BS-OPS-20260811-03` / bounded Phase C entry;
- preserved historical R3 blocked and Task3-not-approved tokens explicitly.

### Finding 2 — HiGodot activation test mixed historical activation scope with the new current product gate

Classification: `CONFLICT / MUST_FIX`.

Evidence:
- PR validation run `31494756224`
- Godot 4.7.1 headless job: SUCCESS
- project-core alignment: PASS
- R3 history/current regression tests through Kyle and the new bootstrap contract: PASS
- bootstrap contract: `5/5 PASS`
- failure: `test_higodot_production_authoring_activation.py` still required current `GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED`.

Repair:
- kept the original HiGodot activation decision/policy snapshot that says activation itself did not open general product implementation;
- moved only the current Development Gates assertion to `BS-OPS-20260811-03` bounded Phase C entry;
- preserved current Task3 as `NOT_SEPARATELY_APPROVED`.

### Finding 3 — operating audit current-router assertions still assumed planning-only state

Classification: `CONFLICT + COMPLEMENT_GAP / MUST_FIX`.

Repair materializer:
- workflow run `31495208745`
- job `93791065634`
- result: SUCCESS

Repair rule:
- R3 registry and Decisions01–09 canon retain their historical planning-time `BLOCKED` / `NOT_APPROVED` contract;
- only Development Gates / Start Here / Active Context current assertions move to bounded Phase C entry;
- `BS-OPS-20260811-03`, planning-complete, P0 bootstrap-required, historical R3 blockers, and Task3 separate gate are all asserted together.

### Finding 4 — Hera postmerge closure mixed Task2 history with the new current Phase C router

Classification: `CONFLICT / MUST_FIX`.

Evidence:
- PR validation run `31495310383`
- all contracts through Hera vendor reconciliation passed;
- failure was the Hera postmerge current-router test still requiring the old planning-only R3 current gate.

Repair:
- preserve the historical Task2/Hera closure evidence unchanged;
- update only current handoff/current-decision assertions to bounded Phase C entry;
- require historical R3 blocked tokens to remain discoverable as history.

### Finding 5 — initializer current test and lower Development Gates still exposed planning-only state as current

Classification: `CONFLICT + COMPLEMENT_GAP / MUST_FIX`.

Evidence:
- PR validation run `31496211022`
- Godot 4.7.1 headless job: SUCCESS
- PowerShell parser: PASS
- bootstrap contract including Base #288: `5/5 PASS`
- Hera postmerge closure: PASS
- failure: initializer current-router test still required `ENTRY_STATE_GATE: PASS_R3_R7_PLANNING_ONLY_PRODUCT_SCOPE_STILL_REQUIRED`.

Adversarial log review additionally found lower current-facing Development Gates sections still saying general product was blocked even though the top current summary had moved to Phase C.

Repair workflow:
- run `31496516490`
- job `93795490874`
- result: SUCCESS

Repair:
- current `ENTRY_STATE_GATE` / general product / R3 state / Task3 / new-scope assertions moved to bounded Phase C;
- R3 `Planning-Only Gate` relabeled explicitly as historical, closed at 9/10;
- Product Implementation Gate now states Phase C is open only within existing approved canon and requires P0 + fresh HiGodot receipt;
- Missing-State current block now reflects Phase C entry, user-deferred images, separately gated Task3, and new-scope approval requirement;
- original initializer decision/entry snapshot remains historical and unchanged.

## Base #288 same-goal upstream reconciliation

During this PR, Base main advanced to:

`6d2feba2bc49fda2d8d273248b55087853615d5d` — `docs: require project-dedicated local execution environment (#288)`.

Classification: `COMPLEMENT_GAP / MUST_FIX` because this upstream commit directly owns the same local-executor goal.

New shared invariants:
- `ASSUME_PREVIOUS_POWERSHELL_CLOSED`
- `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`
- `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`
- explicit executor targeting with `codex -C <exact project/worktree>`

### Base #288 semantic RED

Test-only head:
`e6c4456c6e0f5987cc5d9e6a3501f321e805938c`

PR validation:
- run `31495709662`
- Python job `93792813268`

Verified before failure:
- checkout/Python: PASS
- PowerShell parser: PASS
- project core: PASS
- existing R3 history/current tests: PASS

New bootstrap contract:
- two pre-existing safety tests: PASS
- three new Base #288 reconciliation tests: FAIL

Exact semantic failures:
- design lacked Base #288 SHA/invariants;
- current Decision/authority lacked Base #288 invariants;
- launcher lacked the shared fresh-shell tokens and explicit `-C` project binding.

This was a valid second semantic RED introduced specifically for the newly arrived same-goal Base authority.

### Base #288 GREEN materialization

One-shot reconciliation workflow:
- run `31496092257`
- job `93794051910`
- result: SUCCESS
- materialized branch head: `05450f1e17216b0b52d384b9380dcc96f5ce342e`

Reconciliation applied:
- launcher now declares the three Base #288 invariants and uses `codex -C` with the exact Blacksmith path;
- spec, plan, and Decision record Base #288 and downstream concrete binding;
- current routers carry dedicated-environment invariants;
- Active/Start current Base observation advanced from the old Decision09-time Base SHA to Base #288;
- pre-planning-complete lower sections were relabeled as historical snapshots;
- Hera current-router assertions were separated from historical Task2/Hera evidence;
- `BS-CURRENT-DECISIONS` operating-health digest was refreshed;
- temporary reconciliation helper/workflow were removed in the same materialized commit.

## Evidence boundary

PowerShell Core parser has already reported `PowerShell parser: PASS` in GitHub CI. This proves parse validity only.

The following remain `NOT_RUN` until the user executes the launcher on the target Windows machine:
- `WINDOWS_LOCAL_BOOTSTRAP`
- `DEDICATED_GODOT_EDITOR_LIVE`
- `HIGODOT_8006_9506_LIVE`
- `CODEX_DEDICATED_PROFILE_LIVE`
- `FRESH_HIGODOT_SESSION_READINESS`
