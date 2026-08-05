#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

path = Path(__file__).resolve().parents[1] / "tools/audit_project_operating_system.py"
text = path.read_text(encoding="utf-8")
old = '"R2_BATCH_005_ACTIVE_2_OF_10"'
new = '"R2_BATCH_005_ACTIVE_3_OF_10"'
if old not in text:
    raise RuntimeError(f"required stale operating-audit token is absent: {old}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("Operating audit active-batch assertion repaired.")
