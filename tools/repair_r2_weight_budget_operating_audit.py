#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
AUDIT = ROOT / "tools/audit_project_operating_system.py"
NEW_CANON = "docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md"


def compact_registry() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    REGISTRY.write_text(
        json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def repair_audit_contract() -> None:
    text = AUDIT.read_text(encoding="utf-8")

    replacements = {
        '\'"next_approval_counter":"5/10"\'': '\'"next_approval_counter":"6/10"\'',
        '        "R2_BATCH_005_5_OF_10",\n        "현재 승인 카운터: `5/10`",\n        "MERGED_PR106",':
            '        "R2_BATCH_005_6_OF_10",\n        "현재 승인 카운터: `6/10`",\n        "MERGED_PR106",',
        '    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (\n        "R2_CHECKPOINT_004",\n        "R2_BATCH_005_5_OF_10",':
            '    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (\n        "R2_CHECKPOINT_004",\n        "R2_BATCH_005_6_OF_10",',
    }
    for old, new in replacements.items():
        if old not in text and new not in text:
            raise RuntimeError(f"audit replacement target missing: {old}")
        text = text.replace(old, new)

    if f'    "{NEW_CANON}",' not in text:
        anchor = '    "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md",\n'
        if anchor not in text:
            raise RuntimeError("ACTIVE_DOCS insertion anchor missing")
        text = text.replace(anchor, anchor + f'    "{NEW_CANON}",\n', 1)

    if f'    "{NEW_CANON}": (' not in text:
        anchor = '    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": (\n'
        block = f'''    "{NEW_CANON}": (\n        "BS-ITEM-20260806-02",\n        "R2_BATCH_005_6_OF_10",\n        "최초 제작 중량 5당 초기 성능 예산 +1",\n        "경량화 -5 중량 / 기존 예산 유지",\n        "중량화 +5 중량 / 과거 최고 인정 중량 초과분만 예산 추가",\n        "PRECISION_ENHANCEMENT_METHOD",\n        "제품 구현: `BLOCKED`",\n    ),\n'''
        if anchor not in text:
            raise RuntimeError("REQUIRED_ASSERTIONS insertion anchor missing")
        text = text.replace(anchor, block + anchor, 1)

    AUDIT.write_text(text, encoding="utf-8")


def verify_repair_shape() -> None:
    registry_text = REGISTRY.read_text(encoding="utf-8")
    required_registry = (
        '"schema_version":8',
        '"stage_status":"R2_BATCH_005_ACTIVE_6_OF_10"',
        '"next_approval_counter":"6/10"',
        '"id":"BS-ITEM-20260806-02"',
        '"weight_performance_budget_model":"PEAK_RECOGNIZED_WEIGHT_MONOTONIC_SINGLE_SOURCE"',
    )
    for token in required_registry:
        if token not in registry_text:
            raise RuntimeError(f"compact registry token missing: {token}")

    audit_text = AUDIT.read_text(encoding="utf-8")
    required_audit = (
        '"next_approval_counter":"6/10"',
        "현재 승인 카운터: `6/10`",
        NEW_CANON,
        "BS-ITEM-20260806-02",
    )
    for token in required_audit:
        if token not in audit_text:
            raise RuntimeError(f"audit token missing after repair: {token}")

    stale = (
        '\'"next_approval_counter":"5/10"\'',
        '"현재 승인 카운터: `5/10`"',
    )
    for token in stale:
        if token in audit_text:
            raise RuntimeError(f"stale audit token remains: {token}")


def main() -> None:
    compact_registry()
    repair_audit_contract()
    verify_repair_shape()


if __name__ == "__main__":
    main()
