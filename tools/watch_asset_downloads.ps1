$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Source      = Join-Path $env:USERPROFILE "Downloads"
$Destination = Join-Path $ProjectRoot ".asset-vault\incoming"

$Extensions = @(
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".svg"
)

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

Write-Host ""
Write-Host "GPT asset download watcher"
Write-Host "FROM : $Source"
Write-Host "TO   : $Destination"
Write-Host ""
Write-Host "종료하려면 Ctrl+C"
Write-Host ""

function Move-Asset {
    param([string]$Path)

    if (-not (Test-Path $Path -PathType Leaf)) {
        return
    }

    $Extension = [System.IO.Path]::GetExtension($Path).ToLower()

    if ($Extensions -notcontains $Extension) {
        return
    }

    # 브라우저가 파일 쓰기를 끝낼 때까지 기다림
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $Stream = [System.IO.File]::Open(
                $Path,
                'Open',
                'Read',
                'None'
            )
            $Stream.Close()
            break
        }
        catch {
            Start-Sleep -Milliseconds 500
        }
    }

    if (-not (Test-Path $Path)) {
        return
    }

    $FileName = [System.IO.Path]::GetFileName($Path)
    $Target   = Join-Path $Destination $FileName

    # 같은 이름의 파일이 이미 있으면 덮어쓰지 않음
    if (Test-Path $Target) {
        $Base = [System.IO.Path]::GetFileNameWithoutExtension($FileName)
        $Ext  = [System.IO.Path]::GetExtension($FileName)
        $Time = Get-Date -Format "yyyyMMdd_HHmmss"

        $Target = Join-Path $Destination "${Base}_${Time}${Ext}"
    }

    try {
        Move-Item -LiteralPath $Path -Destination $Target -ErrorAction Stop
        Write-Host "저장됨 -> $Target"
    }
    catch {
        Write-Warning "이동 실패: $Path"
    }
}

$Watcher = New-Object System.IO.FileSystemWatcher
$Watcher.Path = $Source
$Watcher.Filter = "*.*"
$Watcher.IncludeSubdirectories = $false
$Watcher.EnableRaisingEvents = $true

$Action = {
    Start-Sleep -Milliseconds 800
    Move-Asset $Event.SourceEventArgs.FullPath
}

Register-ObjectEvent $Watcher Created -Action $Action | Out-Null
Register-ObjectEvent $Watcher Renamed -Action $Action | Out-Null

while ($true) {
    Start-Sleep -Seconds 1
}