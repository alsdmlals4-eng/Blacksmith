param([switch]$Move)
$ErrorActionPreference = 'Stop'
$repoPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$reviewPath = 'C:\Users\user\Documents\GitHub\Ninza\Blacksmith-delete-review\2026-09-12'
if ($repoPath -ne 'C:\Users\user\Documents\GitHub\Ninza\Blacksmith') { throw 'Wrong repository' }
$ignored = @(git -C $repoPath ls-files --others --ignored --exclude-standard)
if ($LASTEXITCODE -ne 0) { throw 'Git inventory failed' }
$selected = @($ignored | Where-Object {
    $_ -match '^tmp/pdfs/(modak-update|blueprint-visual-comparison|phase1-workshop-blueprint-baseline)/[^/]+\.png$' -or
    $_ -match '^(?:(?:tools|tests|tmp)/)?(?:[^/]+/)*__pycache__/[^/]+\.pyc$'
} | Where-Object { $_ -notmatch '^(addons|assets|scripts|\.godot|\.git|\.asset-vault)/' })
$rows = @()
foreach ($rel in $selected) {
    $source = [IO.Path]::GetFullPath((Join-Path $repoPath $rel))
    $destination = [IO.Path]::GetFullPath((Join-Path $reviewPath $rel))
    if (-not $source.StartsWith($repoPath + '\') -or -not $destination.StartsWith($reviewPath + '\')) { throw 'Path escape' }
    $cursor = Get-Item -LiteralPath $source
    while ($null -ne $cursor -and $cursor.FullName -ne $repoPath) {
        if ($cursor.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse path forbidden' }
        $cursor = $cursor.Parent
        if ($null -eq $cursor) { $cursor = (Get-Item -LiteralPath $source).Directory }
    }
    if (Test-Path -LiteralPath $destination) { throw "Destination already exists: $rel" }
    $item = Get-Item -LiteralPath $source
    $rows += [pscustomobject]@{Original=$source;Destination=$destination;Bytes=$item.Length;SHA256=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash;Reason=$(if($rel.EndsWith('.pyc')){'REGENERABLE_PYTHON_CACHE'}else{'REGENERABLE_PDF_INSPECTION_RENDER'})}
}
if (-not $Move) {
    $rows | Select-Object Original,Bytes,Reason
    "DRY_RUN: $($rows.Count) files / $(($rows | Measure-Object Bytes -Sum).Sum) bytes"
    exit 0
}
New-Item -ItemType Directory -Path $reviewPath -Force | Out-Null
if (Test-Path -LiteralPath (Join-Path $reviewPath 'manifest.csv')) { throw 'Existing manifest; use a new reviewed batch' }
$rows | Export-Csv -LiteralPath (Join-Path $reviewPath 'manifest.csv') -NoTypeInformation -Encoding utf8
foreach ($row in $rows) {
    New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($row.Destination)) -Force | Out-Null
    Move-Item -LiteralPath $row.Original -Destination $row.Destination
    if ((Get-FileHash -LiteralPath $row.Destination -Algorithm SHA256).Hash -ne $row.SHA256) { throw 'Moved hash mismatch' }
}
"MOVED_VERIFIED: $($rows.Count) files / $(($rows | Measure-Object Bytes -Sum).Sum) bytes / $reviewPath"
