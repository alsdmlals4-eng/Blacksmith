#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_all(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"missing token in {relative}: {old}")
    path.write_text(text.replace(old, new), encoding="utf-8")


replace_all(
    "tests/check_project_core_alignment.py",
    '"R2_BATCH_005_ACTIVE_2_OF_10"',
    '"R2_BATCH_005_ACTIVE_3_OF_10"',
)

print("Focused active-batch validator tokens repaired.")
