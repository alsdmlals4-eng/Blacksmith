# Blacksmith Dedicated Local Executor Bootstrap Design

Decision ID: `BS-OPS-20260811-03`

Status: `USER_APPROVED / PLANNING_COMPLETE_DECLARED / PHASE_B_FINAL_REVIEW / IMPLEMENTATION_ENTRY_BINDING`

Date: 2026-08-11 KST

## User approval and phase transition

The user explicitly declared `기획 완료` after approving R3–R7 Decisions 01–09 and explicitly requested Plan C implementation work.

The R3–R7 planning batch closes at `9/10`. `grill_me_approval_batch_max: 10` is a maximum batch size, not a requirement to manufacture a tenth content decision. No new Decision10 is invented merely to fill the counter.

This decision records the Phase B final-review result and binds the local execution environment required before Phase C persistent Godot authoring.

```yaml
planning_completion_trigger: USER_EXPLICIT_PLANNING_COMPLETE_DECLARATION
planning_batch_closed_at: R3_R7_9_OF_10
phase_b_final_review: PASS_FOR_APPROVED_CANON_IMPLEMENTATION_ENTRY
product_implementation: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON
new_unapproved_product_scope: FORBIDDEN
task3_implementation: NOT_SEPARATELY_APPROVED
image_generation: DEFERRED_BY_USER
```

`TASK3_IMPLEMENTATION` remains separately gated. `기획 완료` opens implementation of already-approved current canon; it does not silently revive or approve an unrelated historical Task3 scope.

## Existing Solution First

The design consumes Base current `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` and `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY` instead of inventing a second broad workflow.

Blacksmith already vendors Godot AI/HiGodot with project settings:

- `godot_ai/http_port`
- `godot_ai/ws_port`
- `godot_ai/keep_server_on_exit`

and Codex client support for `CODEX_HOME` plus `[mcp_servers.godot-ai]`.

Godot persistent Scene/Node/Resource/script/project-setting authoring remains under the project's adopted HiGodot authority. The PowerShell launcher is orchestration only and is not authoring evidence.

## Dedicated local environment binding

Blacksmith local PowerShell work MUST start by establishing or reusing the following dedicated environment:

```yaml
project: Blacksmith
project_path: 'C:\Users\user\Documents\GitHub\Ninza\Blacksmith'
godot_project_path: 'C:/Users/user/Documents/GitHub/Ninza/Blacksmith'
godot_version: '4.7.1-stable'
dedicated_godot_dir: 'C:\Users\user\Tools\Godot-Blacksmith-4.7.1'
dedicated_godot_exe: 'C:\Users\user\Tools\Godot-Blacksmith-4.7.1\Godot_v4.7.1-stable_win64.exe'
self_contained_marker: '_sc_'
self_contained_data_dir: 'C:\Users\user\Tools\Godot-Blacksmith-4.7.1\editor_data'
higodot_http_port: 8006
higodot_ws_port: 9506
codex_home: 'C:\Users\user\.codex-blacksmith'
codex_sandbox_mode: workspace-write
codex_approval_policy: never
powershell_session: EPHEMERAL_CLOSE_AND_FRESH_START_EACH_EXECUTION_BLOCK
```

The Codex install itself is shared. Only its state/config/auth/log/session root is isolated through Blacksmith's dedicated `CODEX_HOME`.

## One-copy/paste startup contract

The user must be able to paste one PowerShell block that performs the complete bounded startup sequence:

```text
exact Blacksmith path check
→ dedicated Godot exists? reuse : create first
→ verify Godot 4.7.1 exact family
→ ensure `_sc_` and self-contained editor_data
→ ensure project-specific Godot-AI settings 8006 / 9506
→ ensure dedicated CODEX_HOME exists before setting env var
→ ensure dedicated Codex config points godot-ai MCP to http://127.0.0.1:8006/mcp
→ detect port ownership/conflicts without killing anything
→ reuse exact matching Blacksmith dedicated editor when safely identifiable
  OR launch exact dedicated editor
→ bounded wait for HTTP 8006 and WS 9506 listeners
→ fail closed if readiness opportunity does not appear
→ launch Codex from the exact Blacksmith project directory with dedicated CODEX_HOME
→ inside Codex obtain fresh HiGodot project/session/version/readiness receipt BEFORE persistent mutation
```

The launcher may configure the local dedicated environment, but process/port/editor existence is only bootstrap evidence. It is not proof that HiGodot's active session is correct and is not product validation.

## Godot acquisition and self-contained isolation

If the dedicated Godot installation does not exist, the launcher creates it before any product authoring.

Acquisition order:

1. reuse an exact local `Godot_v4.7.1-stable_win64.exe` when found in the user's Downloads area;
2. otherwise reuse an exact local `Godot_v4.7.1-stable_win64*.zip` and extract the exact executable;
3. otherwise download the official Godot 4.7.1 Windows standard archive from the official Godot build release location;
4. verify the launched executable reports the expected `4.7.1` version family;
5. create `_sc_` beside the executable before normal editor launch.

The bootstrap never copies `%APPDATA%\Godot` settings into the dedicated install. `_sc_` isolation is required so Blacksmith editor settings are stored beside the dedicated binary in `editor_data/` instead of the user's shared Godot settings.

## Godot-AI port seeding

Blacksmith owns exactly:

```text
HTTP 8006
WS   9506
```

The dedicated editor settings must resolve:

```text
godot_ai/http_port = 8006
godot_ai/ws_port = 9506
godot_ai/keep_server_on_exit = true
```

A first-time bootstrap may start the dedicated editor once in a bounded safe initialization mode that prevents normal editor-plugin startup, create the self-contained settings file, patch only these Blacksmith-owned keys, then start the normal editor.

The launcher must create a timestamped backup before modifying an existing dedicated editor settings file.

## Port conflict policy

Port conflict handling is fail-closed.

- Never kill, stop, restart, reconfigure, or steal an unrelated editor/server/process.
- If 8006 or 9506 is occupied and the environment cannot safely establish that it is the exact reusable Blacksmith dedicated session, stop before Codex launch.
- Print the occupied port, listener PID, process name/path/command line when available, and the exact remediation: close the owning process manually or choose a separately approved Blacksmith port binding.
- Do not silently fall back to 8000/9500 or auto-suggest-and-switch to another port. The user's binding is exactly 8006/9506.
- If an exact matching Blacksmith dedicated editor and expected local listeners are already active, reuse is preferred over duplicate editor startup.

## Dedicated Codex profile

`C:\Users\user\.codex-blacksmith` must be created before `CODEX_HOME` is exported because current Codex requires a custom `CODEX_HOME` directory to already exist.

The dedicated `config.toml` must bind:

```toml
approval_policy = "never"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true

[mcp_servers.godot-ai]
url = "http://127.0.0.1:8006/mcp"
enabled = true
required = true
startup_timeout_sec = 60
tool_timeout_sec = 360
```

The bootstrap never copies global Codex credentials/config wholesale into the dedicated home and never records credentials in project files or logs. First use may require normal Codex authentication in the isolated profile.

If `config.toml` already exists and is not marked as a Blacksmith-managed dedicated profile, fail closed instead of overwriting unknown user configuration. A managed file may be idempotently refreshed to the approved binding.

## Fresh-shell assumption

The launcher assumes the user may close PowerShell after every work block.

Therefore no correctness condition may depend on shell state from a previous session. Every paste must recreate shell-scoped environment variables, resolve paths again, verify the dedicated install/profile, and establish or reuse the exact editor/server before Codex starts.

## Phase B final review: implementation package decomposition

The approved planning canon is decomposed for Phase C into implementation packages rather than one repository-wide mutation:

1. `P0_LOCAL_EXECUTOR_BOOTSTRAP` — dedicated self-contained Godot + 8006/9506 + CODEX_HOME + one-shot handoff. Must pass before persistent authoring.
2. `P1_AUTHORITY_AND_CURRENT_STATE_READBACK` — Codex/HiGodot reads exact project/session/plugin/version/current canon and verifies authoring authority.
3. `P2_FOUNDATION_DATA_AND_STATE_CONTRACTS` — implement approved shared data/state structures needed by multiple content decisions, reusing existing code first.
4. `P3_APPROVED_CONTENT_VERTICAL_IMPLEMENTATION` — implement approved R3–R7 content in bounded slices with TDD and same-UID/history boundaries.
5. `P4_RUNTIME_UX_AND_FEEDBACK` — implement approved explanation/feedback surfaces without introducing new scoring authority.
6. `P5_GUT_AFFECTED_FULL_REGRESSION` — deterministic GDScript validation under adopted GUT authority.
7. `P6_HERA_LIVE_QA_IF_CURRENTLY_ADOPTED_AND_REQUIRED` — observability/live QA only; zero persistent source mutation.
8. `P7_EXACT_HEAD_PR_AND_POSTMERGE_READBACK` — current Base/Sheet/PR inventory, exact-head CI, adversarial review, merge within approved scope, merged-main readback.
9. `P8_USER_LOCAL_FETCH_PULL_PROJECT_PLAY` — final user-facing local pull and Project Play evidence.

Do not implement all approved content in one high-impact mutation. Each package starts with current-state readback and Existing Solution First analysis.

## Definition of Ready

Phase C implementation is ready only when all of the following are true:

- user `기획 완료` declaration exists;
- current GitHub/Sheet canon is reconciled;
- current Base one-shot bootstrap policy has been reviewed;
- R3–R7 closes at approved 9/10 without invented Decision10;
- dedicated Blacksmith local environment values are exact and unambiguous;
- local bootstrap is test-first and fail-closed for wrong path/version/port/profile;
- persistent Godot authoring is forbidden until fresh HiGodot readiness is obtained inside Codex;
- no existing user work is reset/restored/cleaned/staged by bootstrap;
- no unrelated server/editor is killed;
- image generation remains deferred;
- new gameplay scope outside approved canon still requires a new user decision;
- Human/Android/accessibility evidence remains `NOT_RUN` until actually observed.

## Adversarial review

### Failure: shared Godot settings leak

Attack: use a normal Godot binary and change 8006/9506 globally.

Defense: dedicated binary + `_sc_` is mandatory; no `%APPDATA%\Godot` mutation.

### Failure: port stealing

Attack: kill whatever owns 8006/9506 so Blacksmith can start.

Defense: forbidden. Unknown ownership stops the bootstrap.

### Failure: stale orphan server mistaken for readiness

Attack: treat an open TCP listener as sufficient HiGodot readiness.

Defense: listener is only bootstrap evidence; Codex must obtain a fresh project/session/version/readiness receipt before mutation.

### Failure: duplicate dedicated editor

Attack: every fresh PowerShell opens another Blacksmith editor.

Defense: exact matching editor reuse is preferred when safely identifiable.

### Failure: Codex profile contaminates another project

Attack: modify `~/.codex/config.toml` or reuse a generic CODEX_HOME.

Defense: Blacksmith-only `C:\Users\user\.codex-blacksmith`; global config is not modified.

### Failure: overwrite an existing custom Blacksmith Codex config

Attack: replace an unknown existing dedicated config.

Defense: unmanaged existing config fails closed; managed profile is idempotent.

### Failure: bootstrap becomes authoring authority

Attack: write product Scene/Resource/project settings from PowerShell because the editor is reachable.

Defense: bootstrap may only configure its dedicated local environment. Persistent Godot product mutation remains HiGodot-only after fresh receipt.

### Failure: `기획 완료` becomes unlimited scope approval

Attack: treat Phase C entry as permission for unapproved gameplay systems or historical Task3.

Defense: implementation is constrained to existing approved canon. New substantive scope still requires a new decision; Task3 remains separately gated.

## Expected result

Before this binding, Blacksmith could accidentally share a global Godot settings profile, generic ports, or generic Codex state with another project. After it, every local implementation block starts from a reproducible Blacksmith-only execution envelope, so concurrent Godot projects do not fight over the same HiGodot ports and Codex cannot accidentally load another project's MCP profile.

## Base #288 reconciliation

Post-design fresh Base read advanced to `6d2feba2bc49fda2d8d273248b55087853615d5d` (`docs: require project-dedicated local execution environment (#288)`). This is a same-goal upstream authority change and is therefore consumed before Blacksmith merge.

Blacksmith explicitly inherits:

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
```

The one-shot launcher is always presented/executed from a fresh-shell assumption, creates or repairs missing Blacksmith-local components before product work, and launches the executor with exact project targeting:

```powershell
codex -C 'C:\Users\user\Documents\GitHub\Ninza\Blacksmith'
```

The dedicated PowerShell boundary means a fresh PowerShell process with Blacksmith-specific environment injection, not a separately installed PowerShell binary. HiGodot remains the sole persistent Godot authoring authority. Hera, when a later acceptance step actually requires the adopted profile, remains `LIVE_QA_AND_OBSERVABILITY_ONLY` and non-authoring.
