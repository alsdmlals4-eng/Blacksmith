from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools/audit_project_operating_system.py"

REPLACEMENTS = {
    '        "R2_CHECKPOINT_004",\n        "R2_BATCH_005 / 10/10",':
        '        "R2_CHECKPOINT_005",\n        "R2_BATCH_005_CLOSED_10_OF_10",',
    '        \'"schema_version":8\',': '        \'"schema_version":9\',',
    '        \'"stage_status":"R2_BATCH_005_ACTIVE_10_OF_10"\',':
        '        \'"stage_status":"R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING"\',',
    '        \'"next_approval_counter":"10/10"\',':
        '        \'"next_approval_counter":"0/10"\',',
    '        \'"id":"R2_BATCH_004"\',\n        \'"id":"R2_BATCH_005"\',':
        '        \'"status":"CLOSED_MERGED_PR109_MAIN_CANON"\',\n        \'"id":"R2_BATCH_005"\',\n        \'"id":"R2_BATCH_006"\',\n        \'"status":"NOT_STARTED"\',',
    '        "R2_BATCH_005_10_OF_10",\n        "BS-CRAFT-20260805-02",':
        '        "R2_BATCH_005_CLOSED_10_OF_10",\n        "BS-CRAFT-20260805-02",',
    '        "R2_BATCH_005_10_OF_10",\n        "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP",':
        '        "R2_BATCH_005_CLOSED_10_OF_10",\n        "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP",',
    '        "R2_CHECKPOINT_004",\n        "R2_BATCH_005_ACTIVE_10_OF_10",':
        '        "R2_CHECKPOINT_005",\n        "R2_BATCH_005_CLOSED_10_OF_10",',
    '        "R2 체크포인트 004",\n        "R2_BATCH_005_10_OF_10",\n        "현재 승인 카운터: `10/10`",':
        '        "R2 체크포인트 005",\n        "R2_BATCH_005_CLOSED_10_OF_10",\n        "현재 승인 카운터: `0/10`",',
    '        "R2_CHECKPOINT_004",\n        "R2_BATCH_005_10_OF_10",':
        '        "R2_CHECKPOINT_005",\n        "R2_BATCH_005_CLOSED_10_OF_10",',
    '    "CURRENT_CONFIRMED_DECISIONS.md": (\n        "R2_BATCH_005 / 0/10",':
        '    "CURRENT_CONFIRMED_DECISIONS.md": (\n        "R2_BATCH_005 / 10/10",\n        "APPROVED_PENDING_MERGE",\n        "DRAFT_PR109",\n        "R2_BATCH_005 / 0/10",',
    '    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (\n        "R2_BATCH_004_ACTIVE_2_OF_10",':
        '    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (\n        "R2_BATCH_005_ACTIVE_10_OF_10",\n        \'"schema_version":8\',\n        \'"next_approval_counter":"10/10"\',\n        "R2_BATCH_004_ACTIVE_2_OF_10",',
    '    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (\n        "R2_BATCH_004_2_OF_10",\n        "현재 승인 카운터: `0/10`",\n    ),':
        '    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (\n        "R2_BATCH_004_2_OF_10",\n        "현재 승인 카운터: `10/10`",\n        "PR #109 체크포인트 검토·명시적 병합 승인 대기",\n    ),',
}


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    replacements_applied = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            replacements_applied += count
    if replacements_applied == 0:
        print("updated=NONE")
        return 0
    TARGET.write_text(text, encoding="utf-8", newline="\n")
    print(f"updated={TARGET.relative_to(ROOT)} replacements={replacements_applied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
