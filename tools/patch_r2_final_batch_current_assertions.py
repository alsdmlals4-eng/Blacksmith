#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for path in sorted((ROOT / "tests").glob("test_*.py")):
    text = path.read_text(encoding="utf-8")
    updated = text.replace(
        'self.assertIn("R2_BATCH_005 / 9/10", read_or_empty(CURRENT))',
        'self.assertIn("R2_BATCH_005 / 10/10", read_or_empty(CURRENT))',
    ).replace(
        'self.assertIn("현재 승인 카운터: `9/10`", active)',
        'self.assertIn("현재 승인 카운터: `10/10`", active)',
    )
    if updated != text:
        path.write_text(updated, encoding="utf-8")

core_path = ROOT / "tests/check_project_core_alignment.py"
core = core_path.read_text(encoding="utf-8")
for document, old, new in (
    (
        "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
        '"R2_BATCH_005_ACTIVE_9_OF_10"',
        '"R2_BATCH_005_ACTIVE_10_OF_10"',
    ),
    (
        "[기획서]/00_프로젝트_허브/START_HERE.md",
        '"R2_BATCH_005_ACTIVE_9_OF_10"',
        '"R2_BATCH_005_ACTIVE_10_OF_10"',
    ),
    (
        "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md",
        '"R2_BATCH_005_9_OF_10"',
        '"R2_BATCH_005_10_OF_10"',
    ),
):
    start = core.index(f'    "{document}": (')
    end = core.index("    ),", start) + len("    ),")
    block = core[start:end]
    if old not in block:
        raise RuntimeError(f"missing core assertion {old} in {document}")
    core = core[:start] + block.replace(old, new, 1) + core[end:]
core_path.write_text(core, encoding="utf-8")

print("final batch current-state assertions patched")
