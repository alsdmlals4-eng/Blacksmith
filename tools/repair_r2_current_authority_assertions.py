#!/usr/bin/env python3
from pathlib import Path


def replace_after(text: str, anchor: str, old: str, new: str, label: str) -> str:
    start = text.find(anchor)
    if start < 0:
        raise SystemExit(f"missing block anchor: {label}")
    pos = text.find(old, start)
    if pos < 0:
        if text.find(new, start) >= 0:
            return text
        raise SystemExit(f"missing token after anchor: {label}: {old}")
    return text[:pos] + new + text[pos + len(old):]


core_path = Path("tests/check_project_core_alignment.py")
core = core_path.read_text(encoding="utf-8")
core = replace_after(core, '"CURRENT_CONFIRMED_DECISIONS.md": (', '"R2_BATCH_005 / 7/10"', '"R2_BATCH_005 / 9/10"', "core current decisions")
core = replace_after(core, '"docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (', '"R2_BATCH_005_8_OF_10"', '"R2_BATCH_005_9_OF_10"', "core game bible")
core = replace_after(core, '"[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (', '"R2_BATCH_005_8_OF_10"', '"R2_BATCH_005_9_OF_10"', "core active context status")
core = replace_after(core, '"[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (', '"현재 승인 카운터: `8/10`"', '"현재 승인 카운터: `9/10`"', "core active context counter")
core = replace_after(core, '"[기획서]/00_프로젝트_허브/ROADMAP.md": (', '"R2_BATCH_005_ACTIVE_8_OF_10"', '"R2_BATCH_005_ACTIVE_9_OF_10"', "core roadmap")
core = replace_after(core, '"[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (', '"R2_BATCH_005_ACTIVE_8_OF_10"', '"R2_BATCH_005_ACTIVE_9_OF_10"', "core gates")
core = replace_after(core, '"[기획서]/00_프로젝트_허브/START_HERE.md": (', '"R2_BATCH_005_ACTIVE_8_OF_10"', '"R2_BATCH_005_ACTIVE_9_OF_10"', "core start")
core = replace_after(core, '"[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (', '"R2_BATCH_005_8_OF_10"', '"R2_BATCH_005_9_OF_10"', "core map")
core_path.write_text(core, encoding="utf-8")

audit_path = Path("tools/audit_project_operating_system.py")
audit = audit_path.read_text(encoding="utf-8")
audit = replace_after(audit, '"CURRENT_CONFIRMED_DECISIONS.md": (', '"R2_BATCH_005 / 8/10"', '"R2_BATCH_005 / 9/10"', "audit current decisions")
audit = replace_after(audit, '"docs/planning/CURRENT_R2_CANON_REGISTRY.json": (', '\'"stage_status":"R2_BATCH_005_ACTIVE_8_OF_10"\'', '\'"stage_status":"R2_BATCH_005_ACTIVE_9_OF_10"\'', "audit registry stage")
audit = replace_after(audit, '"docs/planning/CURRENT_R2_CANON_REGISTRY.json": (', '\'"next_approval_counter":"8/10"\'', '\'"next_approval_counter":"9/10"\'', "audit registry counter")
audit = replace_after(audit, '"docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (', '"R2_BATCH_005_8_OF_10"', '"R2_BATCH_005_9_OF_10"', "audit game bible")
for anchor, old, new, label in (
    ('"[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (', '"R2_BATCH_005_8_OF_10"', '"R2_BATCH_005_9_OF_10"', "audit active context status"),
    ('"[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (', '"현재 승인 카운터: `8/10`"', '"현재 승인 카운터: `9/10`"', "audit active context counter"),
    ('"[기획서]/00_프로젝트_허브/ROADMAP.md": (', '"R2_BATCH_005_ACTIVE_8_OF_10"', '"R2_BATCH_005_ACTIVE_9_OF_10"', "audit roadmap"),
    ('"[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (', '"R2_BATCH_005_ACTIVE_8_OF_10"', '"R2_BATCH_005_ACTIVE_9_OF_10"', "audit gates"),
    ('"[기획서]/00_프로젝트_허브/START_HERE.md": (', '"R2_BATCH_005_ACTIVE_8_OF_10"', '"R2_BATCH_005_ACTIVE_9_OF_10"', "audit start"),
    ('"[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (', '"R2_BATCH_005_8_OF_10"', '"R2_BATCH_005_9_OF_10"', "audit map"),
):
    audit = replace_after(audit, anchor, old, new, label)
audit_path.write_text(audit, encoding="utf-8")
print("current authority assertions repaired")
