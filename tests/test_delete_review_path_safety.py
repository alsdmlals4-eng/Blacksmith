"""Exercise the quarantine guard without moving or deleting user files."""
import pathlib
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("powershell"), "Windows PowerShell path semantics")
class DeleteReviewPathSafety(unittest.TestCase):
    def test_existing_destination_ancestors_and_move_rechecks(self):
        script = ROOT / "tools/collect_delete_review.ps1"
        source = script.read_text(encoding="utf-8")
        self.assertIn("function Assert-NoReparseAncestor", source)
        # Extract only the guard: never execute the inventory or move entrypoint.
        command = r'''
$ErrorActionPreference = 'Stop'
$ast = [Management.Automation.Language.Parser]::ParseFile('__SCRIPT__', [ref]$null, [ref]$null)
$guard = $ast.Find({param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq 'Assert-NoReparseAncestor'}, $true)
Invoke-Expression $guard.Extent.Text
function Test-Path { param($LiteralPath) return $LiteralPath -notlike '*missing*' }
function Get-Item {
    param($LiteralPath, [switch]$Force)
    $attributes = [IO.FileAttributes]::Directory
    if ($LiteralPath -eq $script:blocked) { $attributes = $attributes -bor [IO.FileAttributes]::ReparsePoint }
    return [pscustomobject]@{Attributes=$attributes}
}
foreach ($blockedPath in @('C:\review', 'C:\review\tmp', 'C:\')) {
    $script:blocked = $blockedPath
    $rejected = $false
    try { Assert-NoReparseAncestor 'C:\review\tmp\missing\image.png' } catch {
        if ($_.Exception.Message -notlike '*Reparse path forbidden*') { throw }
        $rejected = $true
    }
    if (-not $rejected) { throw "Missed ancestor: $blockedPath" }
}
$script:blocked = 'C:\unrelated'
Assert-NoReparseAncestor 'C:\review\tmp\missing\image.png'
'PATH_GUARD_PASS'
'''.replace("__SCRIPT__", str(script).replace("'", "''"))
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
            text=True, capture_output=True, timeout=30,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PATH_GUARD_PASS", result.stdout)
        self.assertIn("Assert-NoReparseAncestor $reviewPath", source)
        self.assertIn("Assert-NoReparseAncestor $destination", source)
        move = source.index("Move-Item -LiteralPath")
        loop = source.rindex("foreach ($row in $rows)", 0, move)
        before_move = source[loop:move]
        self.assertIn("Assert-NoReparseAncestor $row.Original", before_move)
        self.assertIn("Assert-NoReparseAncestor $row.Destination", before_move)


if __name__ == "__main__":
    unittest.main()
