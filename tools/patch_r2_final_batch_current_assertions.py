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

print("final batch current-state assertions patched")
