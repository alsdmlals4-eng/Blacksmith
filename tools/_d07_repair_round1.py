from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW_HASH = "05c982e494fa6f361ad1e877428593179e5457936be4259633cefb452131d3c1"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 match, got {count}: {old!r}")
    return text.replace(old, new, 1)


def repair_health() -> None:
    path = "docs/PROJECT_OPERATING_HEALTH.json"
    data = json.loads(read(path))
    record = next(item for item in data["evidence"]["operating"] if item.get("id") == "BS-CURRENT-DECISIONS")
    record["sha256"] = NEW_HASH
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def repair_core_alignment() -> None:
    path = "tests/check_project_core_alignment_current.py"
    text = read(path)
    text = text.replace('"R3_R7_APPROVAL_COUNTER: 6/10"', '"R3_R7_APPROVAL_COUNTER: 7/10"')
    text = text.replace('"R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-06"', '"R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07"')
    text = text.replace('"NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED"', '"SOLDIER_02_LIANA_MISSION_FIT_APPROVED"')
    text = text.replace(
        '"R3_R7_RESUME_LOCATOR: NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED"',
        '"R3_R7_RESUME_LOCATOR: SOLDIER_02_LIANA_MISSION_FIT_APPROVED"',
    )
    text = text.replace('"현재 R3–R7 승인 카운터: `6/10`"', '"현재 R3–R7 승인 카운터: `7/10`"')

    gate_anchor = '            "BS-CONTENT-20260811-05",\n            "R3_R7_APPROVAL_COUNTER: 7/10",'
    gate_replacement = '            "BS-CONTENT-20260811-05",\n            "BS-CONTENT-20260811-06",\n            "BS-CONTENT-20260811-07",\n            "R3_R7_APPROVAL_COUNTER: 7/10",'
    text = replace_once(text, gate_anchor, gate_replacement, "core alignment gate decisions")

    active_anchor = '            "BS-CONTENT-20260811-05",\n            "PRODUCT_IMPLEMENTATION: BLOCKED",'
    active_replacement = '            "BS-CONTENT-20260811-05",\n            "BS-CONTENT-20260811-06",\n            "BS-CONTENT-20260811-07",\n            "PRODUCT_IMPLEMENTATION: BLOCKED",'
    text = replace_once(text, active_anchor, active_replacement, "core alignment active decisions")
    write(path, text)


def repair_gates_history() -> None:
    path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
    text = read(path)
    anchor = "- `BS-CONTENT-20260811-01`~`06`은 승인 완료 이력으로 보존한다.\n"
    replacement = (
        anchor
        + "- `BS-CONTENT-20260811-06 / NOBLE_01 / CEREMONIAL_NOBLE`은 6/10 승인 이력이며 current locator가 아니다.\n"
        + "- `BS-CONTENT-20260811-07 / SOLDIER_02 / LIANA_BERG`가 현재 7/10 Decision이다.\n"
    )
    text = replace_once(text, anchor, replacement, "gates Decision06 history")
    write(path, text)


def repair_roadmap() -> None:
    path = "[기획서]/00_프로젝트_허브/ROADMAP.md"
    text = read(path)
    anchor = """책임 원본:\n\n- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`\n\n## R3 — 버티컬 슬라이스 기반\n"""
    history = """책임 원본:\n\n- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`\n\n### 6/10 — `BS-CONTENT-20260811-06`\n\n```text\nNOBLE_01 / CEREMONIAL_NOBLE\nHEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY\nCEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE\n```\n\n목표:\n\n- 기존 가보 UID의 실제 상태·손상·과거 수리·소유·계승·Chronicle evidence와 공개된 계승 목적을 읽고 개입 깊이를 판단한다.\n- 최대 복원·최고 Artistry를 자동 정답으로 만들지 않고 새 가문 위신·진품성·계승 총점을 추가하지 않는다.\n- 물리 흔적을 처치하더라도 의미 있는 과거 생애 기록을 삭제하지 않는다.\n- 같은 UID를 처치 전·후·의식·반환까지 보존한다.\n- 복원/의식 반복으로 Artistry 또는 Chronicle Affix를 자동 성장시키지 않는다.\n- 직접 의식·귀족 가문·궁정·외교 경영을 추가하지 않는다.\n\n책임 원본:\n\n- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`\n\n## R3 — 버티컬 슬라이스 기반\n"""
    text = replace_once(text, anchor, history, "roadmap D06 history")
    text = replace_once(
        text,
        "`BS-CONTENT-20260811-01`부터 `BS-CONTENT-20260811-05`까지는 R3–R7 상세 **콘텐츠 설계** 승인이다.",
        "`BS-CONTENT-20260811-01`부터 `BS-CONTENT-20260811-07`까지는 R3–R7 상세 **콘텐츠 설계** 승인이다.",
        "roadmap approval prose",
    )
    text = replace_once(
        text,
        "BS-CONTENT-20260811-05: USER_APPROVED_PLANNING_ONLY\nPRODUCT_IMPLEMENTATION: BLOCKED",
        "BS-CONTENT-20260811-05: USER_APPROVED_PLANNING_ONLY\nBS-CONTENT-20260811-06: USER_APPROVED_PLANNING_ONLY\nBS-CONTENT-20260811-07: USER_APPROVED_PLANNING_ONLY\nPRODUCT_IMPLEMENTATION: BLOCKED",
        "roadmap implementation gate",
    )
    write(path, text)


if __name__ == "__main__":
    repair_health()
    repair_core_alignment()
    repair_gates_history()
    repair_roadmap()
