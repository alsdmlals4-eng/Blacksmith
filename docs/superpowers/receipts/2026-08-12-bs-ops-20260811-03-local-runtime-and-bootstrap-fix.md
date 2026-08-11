# BS-OPS-20260811-03 — Local Runtime and Bootstrap Fix Receipt

Date/time (user local): `2026-08-12T01:08:11+09:00`

Decision: `BS-OPS-20260811-03` (same-ID runtime hardening; no new Decision).

## Scope

This change fixes local executor bootstrap only. It does not start product
gameplay implementation, Task3, image generation, or persistent Godot
authoring.

## Initial failure record

The user supplied these original runtime observations; they are retained as
historical evidence and are distinct from the current recheck below.

1. Two untracked Godot executable files were quarantined outside this repo.
2. A retained Blacksmith `godot-ai` server could occupy HTTP 8006 / WS 9506
   after the user closed the editor session.
3. Codex rejected the managed config with `carriage return must be followed by
   newline, expected newline`.

## RED → GREEN

- RED head: `bc8cadf1e9cca3863d2958d5b9cabd8563f43378`.
- Command: `python -m unittest tests.test_blacksmith_dedicated_local_executor_bootstrap -v`.
- Expected semantic RED: the new TOML test found the here-string plus
  `Set-Content` writer; the retained-server test found neither the verified
  candidate predicate nor exact-PID cleanup helper. The other six focused tests
  passed.
- GREEN: the launcher now writes deterministic LF-only UTF-8 without BOM via
  explicit lines and `File.WriteAllText`; it can stop only a reverified,
  exact-PID retained Blacksmith listener and confirms both ports released.
- GREEN command: `python -m unittest tests.test_blacksmith_dedicated_local_executor_bootstrap -v` — `8/8 PASS`.
- Parser: `[System.Management.Automation.Language.Parser]::ParseFile(...)` — `PASS`.

## Original observed receipt and current recheck

The original Phase C readiness receipt reported PASS for exact Blacksmith path,
main, clean worktree, dedicated CODEX_HOME, dedicated Godot, HTTP 8006, WS
9506, Godot-AI MCP, one exact project session, editor state, hierarchy, and
project settings.

Current read-only recheck in this session:

```text
project: C:\Users\user\Documents\GitHub\Ninza\Blacksmith
Godot: 4.7.1-stable (official), dedicated editor PID 22068
Godot AI plugin/server: 3.1.4
CODEX_HOME: C:\Users\user\.codex-blacksmith
config.toml: UTF-8 no BOM, LF present, no bare CR
HTTP 8006 / WS 9506: listener PID 26780, exact Blacksmith godot-ai command line
exact normalized project sessions: 1 (blacksmith@2ff1)
editor_state: ready, project_name Blacksmith
scene_get_hierarchy: PASS (2 readable nodes)
project_manage(settings_get application/config/name): PASS (Blacksmith)
PERSISTENT_MUTATION_GATE: OPEN
```

The current recheck was read-only and did not run the changed launcher or alter
the live Godot project.

## Remaining non-claims

`HUMAN_PLAYTEST`, Android, and accessibility are `NOT_RUN`. This receipt does
not claim gameplay implementation or widen Task3 approval.
