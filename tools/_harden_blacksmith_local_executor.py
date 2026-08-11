from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/start_blacksmith_local_executor.ps1"
DECISION = ROOT / "docs/decisions/BS-OPS-20260811-03_DEDICATED_LOCAL_EXECUTOR_BOOTSTRAP.md"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing anchor {label}: {old[:160]!r}")
    return text.replace(old, new, 1)


text = SCRIPT.read_text(encoding="utf-8")
old_editor_fn = r'''function Find-ExactBlacksmithEditor {
    if (-not (Test-Path -LiteralPath $GodotExe -PathType Leaf)) {
        return $null
    }
    $expectedExe = Normalize-Path $GodotExe
    $expectedProject = Normalize-Path $Project
    foreach ($proc in @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.Name -ieq 'Godot_v4.7.1-stable_win64.exe' })) {
        $exe = if ($proc.ExecutablePath) { Normalize-Path ([string]$proc.ExecutablePath) } else { '' }
        $cmd = if ($proc.CommandLine) { ([string]$proc.CommandLine).ToLowerInvariant() } else { '' }
        if ($exe -eq $expectedExe -and $cmd.Contains($expectedProject)) {
            return $proc
        }
    }
    return $null
}
'''
new_editor_fn = r'''function Test-CommandLineTargetsBlacksmith([string]$CommandLine) {
    if ([string]::IsNullOrWhiteSpace($CommandLine)) {
        return $false
    }
    $cmd = $CommandLine.ToLowerInvariant()
    $needles = @(
        (Normalize-Path $Project),
        $Project.ToLowerInvariant(),
        ($Project -replace '\\', '/').ToLowerInvariant()
    ) | Select-Object -Unique
    foreach ($needle in $needles) {
        if (-not [string]::IsNullOrWhiteSpace($needle) -and $cmd.Contains($needle)) {
            return $true
        }
    }
    return $false
}

function Get-BlacksmithGodotEditors {
    $matches = @()
    foreach ($proc in @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue)) {
        $name = ([string]$proc.Name).ToLowerInvariant()
        $exe = if ($proc.ExecutablePath) { Normalize-Path ([string]$proc.ExecutablePath) } else { '' }
        $exeName = if ($exe) { [System.IO.Path]::GetFileName($exe).ToLowerInvariant() } else { '' }
        $isGodot = (($name.StartsWith('godot') -and $name.EndsWith('.exe')) -or ($exeName.StartsWith('godot') -and $exeName.EndsWith('.exe')))
        if (-not $isGodot) {
            continue
        }
        if (-not (Test-CommandLineTargetsBlacksmith ([string]$proc.CommandLine))) {
            continue
        }
        $matches += $proc
    }
    return $matches
}

function Find-ExactBlacksmithEditors {
    if (-not (Test-Path -LiteralPath $GodotExe -PathType Leaf)) {
        return @()
    }
    $expectedExe = Normalize-Path $GodotExe
    return @(Get-BlacksmithGodotEditors | Where-Object {
        $_.ExecutablePath -and (Normalize-Path ([string]$_.ExecutablePath)) -eq $expectedExe
    })
}

function Find-ConflictingBlacksmithEditor {
    $expectedExe = Normalize-Path $GodotExe
    foreach ($proc in @(Get-BlacksmithGodotEditors)) {
        $exe = if ($proc.ExecutablePath) { Normalize-Path ([string]$proc.ExecutablePath) } else { '' }
        if ($exe -ne $expectedExe) {
            return $proc
        }
    }
    return $null
}
'''
text = replace_once(text, old_editor_fn, new_editor_fn, "editor discovery")

old_port_branch = r'''    # If the editor was closed while keep_server_on_exit was enabled, the server
    # can remain. Only accept that orphan when every occupied listener identifies
    # itself as godot-ai; the freshly started dedicated editor must then adopt it.
    $unrecognized = @($occupied | Where-Object { -not (Test-RecognizableGodotAiListener $_) })
    if (-not $ExactEditor -and $unrecognized.Count -eq 0) {
        Write-Step 'Recognizable retained godot-ai listener detected; dedicated editor will be started for fresh adoption/readiness verification.'
        return
    }

    Write-Host 'PORT_CONFLICT_FAIL_CLOSED'
'''
new_port_branch = r'''    # UNVERIFIED_RETAINED_SERVER_REUSE_FORBIDDEN: without the exact dedicated
    # Blacksmith editor alive, an existing 8006/9506 listener cannot be proven to
    # belong to this project. Even a process that looks like godot-ai is rejected.
    if (-not $ExactEditor) {
        Write-Host 'UNVERIFIED_RETAINED_SERVER_REUSE_FORBIDDEN'
    }

    Write-Host 'PORT_CONFLICT_FAIL_CLOSED'
'''
text = replace_once(text, old_port_branch, new_port_branch, "retained server reuse")

old_call = r'''Ensure-DedicatedGodot
$exactEditor = Find-ExactBlacksmithEditor
Assert-SafePortState $exactEditor
'''
new_call = r'''Ensure-DedicatedGodot
$exactEditors = @(Find-ExactBlacksmithEditors)
if ($exactEditors.Count -gt 1) {
    Write-Host 'MULTIPLE_DEDICATED_BLACKSMITH_EDITORS_FAIL_CLOSED'
    foreach ($editor in $exactEditors) {
        Write-Host ("PID {0} Name={1}`n  Executable={2}`n  CommandLine={3}" -f $editor.ProcessId, $editor.Name, $editor.ExecutablePath, $editor.CommandLine)
    }
    Fail-Bootstrap 'More than one dedicated Blacksmith Godot editor targets the same project. Close duplicates manually; no process was stopped.'
}
$exactEditor = if ($exactEditors.Count -eq 1) { $exactEditors[0] } else { $null }
$conflictingEditor = Find-ConflictingBlacksmithEditor
if ($conflictingEditor) {
    Write-Host 'NON_DEDICATED_BLACKSMITH_EDITOR_CONFLICT_FAIL_CLOSED'
    Write-Host ("PID {0} Name={1}`n  Executable={2}`n  CommandLine={3}" -f $conflictingEditor.ProcessId, $conflictingEditor.Name, $conflictingEditor.ExecutablePath, $conflictingEditor.CommandLine)
    Fail-Bootstrap 'Blacksmith is already open in a non-dedicated Godot executable. Close that editor manually before starting the dedicated environment; no process was stopped.'
}
Assert-SafePortState $exactEditor
'''
text = replace_once(text, old_call, new_call, "startup editor conflict gate")
SCRIPT.write_text(text, encoding="utf-8", newline="\n")

receipt = r'''## Postmerge hardening — strict project/editor/port isolation

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
'''
decision = DECISION.read_text(encoding="utf-8")
if "## Postmerge hardening — strict project/editor/port isolation" not in decision:
    DECISION.write_text(decision.rstrip() + "\n\n" + receipt.strip() + "\n", encoding="utf-8", newline="\n")

print("Blacksmith local executor postmerge hardening materialized")
