# BS-OPS-20260811-03 Postmerge Local Executor Hardening Receipt

Date: 2026-08-11 KST

Decision: `BS-OPS-20260811-03`

PR: `#156`

## Why this follow-up exists

After PR #155 merged, the mandatory `POST_CHANGE_MONITOR_LOOP` attacked the one-shot launcher against the user's strict rule that project-local HiGodot ports must never be shared.

Two material complement gaps were found:

1. Blacksmith could already be open in a non-dedicated Godot executable while the launcher started the dedicated editor, producing two editors against the same project;
2. if the exact dedicated Blacksmith editor was absent but 8006/9506 were occupied by a process that merely resembled godot-ai, the launcher could accept that retained server even though project ownership was not provable.

Classification: `COMPLEMENT_GAP / MUST_FIX`.

No gameplay/product scope is added. This is same-Decision postmerge hardening.

## Semantic RED

Test-only head:

`a9fd56b97e53675278a625c0fbbb7346bd33a622`

PR validation:
- run `31498561843`
- Python job `93802395639`

Before the new isolation failure:
- checkout: PASS
- pinned Base checkout: PASS
- Python 3.12: PASS
- merge-conflict contract: PASS
- PowerShell parser: PASS
- project-core alignment: PASS
- existing R3/current/bootstrap tests: PASS

The new test failed specifically because the merged launcher did not yet contain `NON_DEDICATED_BLACKSMITH_EDITOR_CONFLICT_FAIL_CLOSED` and still contained permissive orphan-server reuse behavior.

## Hardening materialization

One-shot hardening workflow:
- run `31498966481`
- job `93803685539`
- result: SUCCESS
- materialized branch head: `c56f87b2358a75b3653680d933b72a56ca499596`

The temporary hardening helper and workflow self-deleted in the materialized commit.

Implemented fail-closed behavior:

```text
NON_DEDICATED_BLACKSMITH_EDITOR_CONFLICT_FAIL_CLOSED
MULTIPLE_DEDICATED_BLACKSMITH_EDITORS_FAIL_CLOSED
UNVERIFIED_RETAINED_SERVER_REUSE_FORBIDDEN
PORT_CONFLICT_FAIL_CLOSED
```

Rules after hardening:
- enumerate Godot processes targeting the exact Blacksmith project path;
- allow no non-dedicated Godot process targeting Blacksmith;
- allow at most one exact dedicated Blacksmith editor;
- if no exact dedicated editor is alive, any occupied 8006/9506 port fails closed, even when its owner resembles godot-ai;
- no process is killed or restarted automatically;
- exact dedicated editor reuse remains permitted only when its expected listeners are recognizable;
- listener/process presence remains bootstrap evidence only; fresh HiGodot project/session/version/readiness inside Codex is still mandatory before persistent mutation.

## Runtime evidence boundary

This hardening is CI/static contract work until the user executes the final one-shot launcher on Windows. The following remain `NOT_RUN`:

- `WINDOWS_LOCAL_BOOTSTRAP`
- `DEDICATED_GODOT_EDITOR_LIVE`
- `HIGODOT_8006_9506_LIVE`
- `CODEX_DEDICATED_PROFILE_LIVE`
- `FRESH_HIGODOT_SESSION_READINESS`
