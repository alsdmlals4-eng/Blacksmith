[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$RepoRoot,
    [Parameter(Mandatory = $true)][string]$ExpectedHead,
    [Parameter(Mandatory = $true)][string]$PrBaseSha,
    [Parameter(Mandatory = $true)][string]$BaseOperatingRoot,
    [Parameter(Mandatory = $true)][string]$BaseContractRoot,
    [Parameter(Mandatory = $true)][string]$Godot,
    [string]$WslDistribution = "",
    [string]$OutputRoot = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path $RepoRoot).Path
$BaseOperatingRoot = (Resolve-Path $BaseOperatingRoot).Path
$BaseContractRoot = (Resolve-Path $BaseContractRoot).Path
$Godot = (Resolve-Path $Godot).Path
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $env:TEMP "blacksmith-windows-wsl2-$($ExpectedHead.Substring(0, 12))"
}
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

function Invoke-NativeChecked {
    param([string]$FilePath, [string[]]$Arguments)
    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$FilePath failed with exit code $LASTEXITCODE"
    }
}

Push-Location $RepoRoot
try {
    $Head = (git rev-parse HEAD).Trim()
    if ($Head -ne $ExpectedHead) {
        throw "HEAD mismatch: $Head != $ExpectedHead"
    }
    if (@(git status --porcelain --untracked-files=no).Count -ne 0) {
        throw "Tracked worktree must be clean"
    }

    $RequiredWindowsPython = @("-3.11", "-3.12", "-3.13")
    $Venvs = @{}
    foreach ($Selector in $RequiredWindowsPython) {
        $Version = $Selector.TrimStart("-")
        $Name = $Version.Replace(".", "")
        $Venv = Join-Path $OutputRoot "venv-py$Name"
        if (Test-Path $Venv) {
            Remove-Item -Recurse -Force $Venv
        }
        Invoke-NativeChecked "py" @($Selector, "-m", "venv", $Venv)
        $Python = Join-Path $Venv "Scripts/python.exe"
        Invoke-NativeChecked $Python @(
            "-m", "pip", "install", "--disable-pip-version-check",
            "pytest==8.3.5"
        )
        $Venvs[$Version] = $Python
    }
    Invoke-NativeChecked $Venvs["3.12"] @(
        "-m", "pip", "install", "--disable-pip-version-check", "-r",
        (Join-Path $BaseContractRoot ".github/validation-requirements.txt")
    )

    $Full = Join-Path $OutputRoot "windows-authoritative-py312.json"
    Invoke-NativeChecked $Venvs["3.12"] @(
        "tools/run_local_validation_v2.py",
        "--repo-root", ".",
        "--pr-base-sha", $PrBaseSha,
        "--base-root", $BaseOperatingRoot,
        "--base-contract-root", $BaseContractRoot,
        "--godot", $Godot,
        "--require-godot",
        "--scope", "code",
        "--expected-head", $ExpectedHead,
        "--output", $Full
    )

    $LaneFiles = @()
    foreach ($Lane in @(
        @{Id = "windows-py311"; Version = "3.11"},
        @{Id = "windows-py312"; Version = "3.12"},
        @{Id = "windows-py313"; Version = "3.13"}
    )) {
        $Output = Join-Path $OutputRoot "$($Lane.Id).json"
        Invoke-NativeChecked $Venvs[$Lane.Version] @(
            "tools/run_local_python_matrix_lane.py",
            "--repo-root", ".",
            "--expected-head", $ExpectedHead,
            "--lane-id", $Lane.Id,
            "--platform-kind", "windows",
            "--expected-python", $Lane.Version,
            "--scope", "code",
            "--output", $Output
        )
        $LaneFiles += $Output
    }

    $WslArgs = @()
    if (-not [string]::IsNullOrWhiteSpace($WslDistribution)) {
        $WslArgs += @("-d", $WslDistribution)
    }
    $WslRepo = (& wsl.exe @WslArgs -- wslpath -a -u $RepoRoot).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "wslpath failed for repo"
    }
    $WslOutputRoot = (& wsl.exe @WslArgs -- wslpath -a -u $OutputRoot).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "wslpath failed for output"
    }
    $WslOutput = Join-Path $OutputRoot "wsl-ubuntu-py312.json"
    Invoke-NativeChecked "wsl.exe" ($WslArgs + @(
        "--", "bash", "$WslRepo/tools/run_wsl_python_lane.sh",
        $WslRepo, $ExpectedHead,
        "$WslOutputRoot/wsl-ubuntu-py312.json"
    ))
    $LaneFiles += $WslOutput

    $Pack = Join-Path $OutputRoot "windows-wsl2-validation-pack.json"
    $AggregateArgs = @(
        "tools/aggregate_local_validation_pack.py",
        "--expected-head", $ExpectedHead,
        "--full-manifest", $Full,
        "--output", $Pack
    )
    foreach ($LaneFile in $LaneFiles) {
        $AggregateArgs += @("--lane-manifest", $LaneFile)
    }
    Invoke-NativeChecked $Venvs["3.12"] $AggregateArgs

    Get-Content $Pack
    Get-FileHash $Pack -Algorithm SHA256
    if (@(git status --porcelain --untracked-files=no).Count -ne 0) {
        throw "Tracked worktree changed during validation"
    }
}
finally {
    Pop-Location
}
