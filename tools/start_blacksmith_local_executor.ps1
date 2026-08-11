Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# BLACKSMITH_DEDICATED_LOCAL_EXECUTOR
# ASSUME_PREVIOUS_POWERSHELL_CLOSED
# PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
# CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
# BOOTSTRAP_ORCHESTRATION_ONLY
# The launcher prepares/reuses the isolated local tool envelope. It is NOT
# HiGodot authoring evidence and does not mutate product Scene/Resource/script
# surfaces. Persistent Godot mutation starts only after a fresh live receipt.

$Project = 'C:\Users\user\Documents\GitHub\Ninza\Blacksmith'
$GodotDir = 'C:\Users\user\Tools\Godot-Blacksmith-4.7.1'
$GodotExe = Join-Path $GodotDir 'Godot_v4.7.1-stable_win64.exe'
$SelfContainedMarker = Join-Path $GodotDir "_sc_"
$EditorDataDir = Join-Path $GodotDir 'editor_data'
$CodexHome = 'C:\Users\user\.codex-blacksmith'
$HttpPort = 8006
$WsPort = 9506
$ExpectedGodotVersion = '4.7.1'
$GodotZipName = 'Godot_v4.7.1-stable_win64.exe.zip'
$OfficialGodotZip = 'https://github.com/godotengine/godot-builds/releases/download/4.7.1-stable/Godot_v4.7.1-stable_win64.exe.zip'
$ManagedCodexMarker = '# BLACKSMITH_DEDICATED_PROFILE_MANAGED'
$BootstrapWaitSeconds = 90

function Write-Step([string]$Message) {
    Write-Host "[Blacksmith bootstrap] $Message"
}

function Fail-Bootstrap([string]$Message) {
    throw "[Blacksmith bootstrap] $Message"
}

function Normalize-Path([string]$Path) {
    try {
        return [System.IO.Path]::GetFullPath($Path).TrimEnd('\').ToLowerInvariant()
    }
    catch {
        return $Path.TrimEnd('\').ToLowerInvariant()
    }
}

function Get-ProcessRecord([int]$ProcessId) {
    try {
        return Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" -ErrorAction Stop
    }
    catch {
        return $null
    }
}

function Get-PortListeners([int]$Port) {
    try {
        return @(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction Stop)
    }
    catch {
        return @()
    }
}

function Get-ListenerDiagnostics([int]$Port) {
    $rows = @()
    foreach ($listener in (Get-PortListeners $Port)) {
        $proc = Get-ProcessRecord ([int]$listener.OwningProcess)
        $rows += [pscustomobject]@{
            Port = $Port
            PID = [int]$listener.OwningProcess
            Name = if ($proc) { [string]$proc.Name } else { '<unknown>' }
            ExecutablePath = if ($proc) { [string]$proc.ExecutablePath } else { '' }
            CommandLine = if ($proc) { [string]$proc.CommandLine } else { '' }
        }
    }
    return $rows
}

function Find-ExactBlacksmithEditor {
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

function Test-RecognizableGodotAiListener($Row) {
    $cmd = ([string]$Row.CommandLine).ToLowerInvariant()
    if ([string]::IsNullOrWhiteSpace($cmd)) {
        return $false
    }
    return ($cmd.Contains('godot-ai') -or $cmd.Contains('godot_ai'))
}

function Assert-SafePortState($ExactEditor) {
    $occupied = @()
    foreach ($port in @($HttpPort, $WsPort)) {
        $occupied += @(Get-ListenerDiagnostics $port)
    }
    if ($occupied.Count -eq 0) {
        return
    }

    # EXACT_BLACKSMITH_EDITOR_REUSE: if the exact dedicated Blacksmith editor is
    # already alive, recognized godot-ai listeners are eligible for reuse.
    if ($ExactEditor) {
        $unknown = @($occupied | Where-Object { -not (Test-RecognizableGodotAiListener $_) })
        if ($unknown.Count -eq 0) {
            Write-Step 'EXACT_BLACKSMITH_EDITOR_REUSE: dedicated editor and recognizable godot-ai listeners found.'
            return
        }
    }

    # If the editor was closed while keep_server_on_exit was enabled, the server
    # can remain. Only accept that orphan when every occupied listener identifies
    # itself as godot-ai; the freshly started dedicated editor must then adopt it.
    $unrecognized = @($occupied | Where-Object { -not (Test-RecognizableGodotAiListener $_) })
    if (-not $ExactEditor -and $unrecognized.Count -eq 0) {
        Write-Step 'Recognizable retained godot-ai listener detected; dedicated editor will be started for fresh adoption/readiness verification.'
        return
    }

    Write-Host 'PORT_CONFLICT_FAIL_CLOSED'
    foreach ($row in $occupied) {
        Write-Host ("Port {0} PID {1} Name={2}`n  Executable={3}`n  CommandLine={4}" -f $row.Port, $row.PID, $row.Name, $row.ExecutablePath, $row.CommandLine)
    }
    Fail-Bootstrap 'HTTP 8006 or WS 9506 is owned by an unverified process. No process was stopped. Close the owner manually or approve a different Blacksmith port binding.'
}

function Find-LocalGodotExe {
    $downloads = Join-Path $HOME 'Downloads'
    if (-not (Test-Path -LiteralPath $downloads -PathType Container)) {
        return $null
    }
    $candidate = Get-ChildItem -LiteralPath $downloads -Filter 'Godot_v4.7.1-stable_win64.exe' -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($candidate) { return $candidate.FullName }
    return $null
}

function Find-LocalGodotZip {
    $downloads = Join-Path $HOME 'Downloads'
    if (-not (Test-Path -LiteralPath $downloads -PathType Container)) {
        return $null
    }
    $candidate = Get-ChildItem -LiteralPath $downloads -Filter $GodotZipName -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($candidate) { return $candidate.FullName }
    return $null
}

function Ensure-DedicatedGodot {
    New-Item -ItemType Directory -Force -Path $GodotDir | Out-Null

    if (-not (Test-Path -LiteralPath $GodotExe -PathType Leaf)) {
        $sourceExe = Find-LocalGodotExe
        if ($sourceExe) {
            Write-Step "Creating dedicated Godot from local exact executable: $sourceExe"
            Copy-Item -LiteralPath $sourceExe -Destination $GodotExe -Force
        }
        else {
            $sourceZip = Find-LocalGodotZip
            $tempDir = $null
            $tempZip = $null
            try {
                if (-not $sourceZip) {
                    $tempZip = Join-Path ([System.IO.Path]::GetTempPath()) ("blacksmith-godot-" + [guid]::NewGuid().ToString('N') + '.zip')
                    Write-Step 'No exact local Godot 4.7.1 executable/archive found; downloading official 4.7.1 Windows archive.'
                    Invoke-WebRequest -Uri $OfficialGodotZip -OutFile $tempZip -UseBasicParsing
                    $sourceZip = $tempZip
                }
                $tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("blacksmith-godot-" + [guid]::NewGuid().ToString('N'))
                New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
                Expand-Archive -LiteralPath $sourceZip -DestinationPath $tempDir -Force
                $expandedExe = Get-ChildItem -LiteralPath $tempDir -Filter 'Godot_v4.7.1-stable_win64.exe' -File -Recurse | Select-Object -First 1
                if (-not $expandedExe) {
                    Fail-Bootstrap "Archive did not contain Godot_v4.7.1-stable_win64.exe: $sourceZip"
                }
                Copy-Item -LiteralPath $expandedExe.FullName -Destination $GodotExe -Force
            }
            finally {
                if ($tempDir -and (Test-Path -LiteralPath $tempDir)) { Remove-Item -LiteralPath $tempDir -Recurse -Force }
                if ($tempZip -and (Test-Path -LiteralPath $tempZip)) { Remove-Item -LiteralPath $tempZip -Force }
            }
        }
    }

    if (-not (Test-Path -LiteralPath $SelfContainedMarker -PathType Leaf)) {
        New-Item -ItemType File -Path $SelfContainedMarker -Force | Out-Null
    }

    $versionOutput = (& $GodotExe --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $versionOutput.Contains($ExpectedGodotVersion)) {
        Fail-Bootstrap "Dedicated Godot version mismatch. Expected $ExpectedGodotVersion, got '$versionOutput'."
    }
    Write-Step "Dedicated self-contained Godot verified: $versionOutput"
}

function Find-DedicatedEditorSettings {
    if (-not (Test-Path -LiteralPath $EditorDataDir -PathType Container)) {
        return $null
    }
    return Get-ChildItem -LiteralPath $EditorDataDir -Filter 'editor_settings-4*.tres' -File -Recurse -ErrorAction SilentlyContinue | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1
}

function Ensure-DedicatedEditorSettings {
    $settings = Find-DedicatedEditorSettings
    if (-not $settings) {
        Write-Step 'Initializing self-contained editor_data in recovery mode (editor plugins disabled for this initialization pass).'
        & $GodotExe --headless --editor --recovery-mode --path $Project --quit-after 2 | Out-Host
        $settings = Find-DedicatedEditorSettings
    }
    if (-not $settings) {
        Fail-Bootstrap "Could not locate editor_settings-4*.tres under dedicated editor_data: $EditorDataDir"
    }

    $settingsPath = $settings.FullName
    $raw = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8
    if (-not $raw.Contains('[resource]')) {
        Fail-Bootstrap "Dedicated EditorSettings file has an unexpected format: $settingsPath"
    }

    $backup = "$settingsPath.blacksmith-bootstrap-$(Get-Date -Format 'yyyyMMdd-HHmmss').bak"
    Copy-Item -LiteralPath $settingsPath -Destination $backup -Force

    $pairs = [ordered]@{
        'godot_ai/http_port' = '8006'
        'godot_ai/ws_port' = '9506'
        'godot_ai/keep_server_on_exit' = 'true'
    }
    foreach ($key in $pairs.Keys) {
        $escaped = [regex]::Escape($key)
        $line = "$key = $($pairs[$key])"
        if ($raw -match "(?m)^$escaped\s*=") {
            $raw = [regex]::Replace($raw, "(?m)^$escaped\s*=.*$", $line)
        }
        else {
            $raw = $raw.TrimEnd() + "`r`n$line`r`n"
        }
    }
    Set-Content -LiteralPath $settingsPath -Value $raw -Encoding UTF8 -NoNewline
    Write-Step "Dedicated Godot-AI settings locked to HTTP 8006 / WS 9506 / keep-server-on-exit ON. Backup: $backup"
}

function Ensure-DedicatedCodexHome {
    New-Item -ItemType Directory -Force -Path $CodexHome | Out-Null
    $env:CODEX_HOME = $CodexHome
    $configPath = Join-Path $CodexHome 'config.toml'

    if (Test-Path -LiteralPath $configPath -PathType Leaf) {
        $existing = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8
        if (-not $existing.Contains($ManagedCodexMarker)) {
            Write-Host 'UNMANAGED_CODEX_CONFIG_FAIL_CLOSED'
            Fail-Bootstrap "Dedicated CODEX_HOME already contains an unmanaged config.toml. Move/review it manually before this bootstrap may manage $configPath"
        }
    }

    $config = @"
$ManagedCodexMarker
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
"@
    Set-Content -LiteralPath $configPath -Value $config -Encoding UTF8
    Write-Step "Dedicated CODEX_HOME ready: $CodexHome"
}

function Wait-ForDedicatedListeners {
    $deadline = (Get-Date).AddSeconds($BootstrapWaitSeconds)
    do {
        $http = @(Get-PortListeners $HttpPort)
        $ws = @(Get-PortListeners $WsPort)
        if ($http.Count -gt 0 -and $ws.Count -gt 0) {
            $bad = @()
            foreach ($row in @(Get-ListenerDiagnostics $HttpPort) + @(Get-ListenerDiagnostics $WsPort)) {
                if (-not (Test-RecognizableGodotAiListener $row)) { $bad += $row }
            }
            if ($bad.Count -gt 0) {
                Write-Host 'PORT_CONFLICT_FAIL_CLOSED'
                foreach ($row in $bad) {
                    Write-Host ("Port {0} PID {1} Name={2} CommandLine={3}" -f $row.Port, $row.PID, $row.Name, $row.CommandLine)
                }
                Fail-Bootstrap 'Expected Blacksmith ports are listening but ownership is not recognizable as godot-ai.'
            }
            return
        }
        Start-Sleep -Milliseconds 500
    } while ((Get-Date) -lt $deadline)
    Fail-Bootstrap "Dedicated listeners did not appear within $BootstrapWaitSeconds seconds. HTTP=$HttpPort WS=$WsPort. POST_BOOTSTRAP_LIVE_READINESS_NOT_PROVEN"
}

Write-Host 'ASSUME_PREVIOUS_POWERSHELL_CLOSED'
Write-Host 'PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST'
Write-Host 'CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST'
Write-Step 'Starting bounded Blacksmith local executor bootstrap.'

if (-not (Test-Path -LiteralPath $Project -PathType Container)) {
    Fail-Bootstrap "Project directory not found: $Project"
}
if (-not (Test-Path -LiteralPath (Join-Path $Project 'project.godot') -PathType Leaf)) {
    Fail-Bootstrap "project.godot not found under exact Blacksmith project: $Project"
}
$codexCommand = Get-Command 'codex.cmd' -ErrorAction SilentlyContinue
if (-not $codexCommand) {
    Fail-Bootstrap 'codex.cmd is not available on PATH.'
}

Ensure-DedicatedGodot
$exactEditor = Find-ExactBlacksmithEditor
Assert-SafePortState $exactEditor

if (-not $exactEditor) {
    Ensure-DedicatedEditorSettings
}
else {
    Write-Step 'EXACT_BLACKSMITH_EDITOR_REUSE: skipping on-disk EditorSettings mutation while the exact editor is active.'
}
Ensure-DedicatedCodexHome

if (-not $exactEditor) {
    Write-Step "Launching dedicated Blacksmith Godot: $GodotExe"
    Start-Process -FilePath $GodotExe -ArgumentList @('--path', $Project, '--editor') -WorkingDirectory $Project | Out-Null
}
else {
    Write-Step "Reusing dedicated Blacksmith Godot PID $($exactEditor.ProcessId)."
}

Wait-ForDedicatedListeners
Write-Host 'POST_BOOTSTRAP_LIVE_READINESS_NOT_PROVEN'
Write-Host 'FRESH_HIGODOT_READINESS_REQUIRED_BEFORE_MUTATION'
Write-Step "Bootstrap listeners are present on HTTP $HttpPort / WS $WsPort. This is startup evidence only."
Write-Step 'Inside Codex, FIRST verify exact Blacksmith project/session, Godot-AI version, HTTP/WS binding, and HiGodot readiness. Do not perform persistent mutation before that fresh receipt.'
Write-Step "Launching Codex with CODEX_HOME=$CodexHome from $Project"

Set-Location -LiteralPath $Project
& $codexCommand.Source -C $Project
