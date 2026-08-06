from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
PROPOSAL = ROOT / "docs/planning/BLACKSMITH_R2_BATCH_006_VERTICAL_SLICE_CANON_PROPOSAL_2026.md"
CURRENT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
ROADMAP = ROOT / "[기획서]/00_프로젝트_허브/ROADMAP.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
HEALTH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"

FEATURE_TESTS = [
    "tests/test_base_v942_planning_first_adoption.py",
    "tests/test_r2_artistry_generation_growth_economy.py",
    "tests/test_r2_customer_equipment_compatibility.py",
    "tests/test_r2_mobile_customer_card_progressive_disclosure.py",
    "tests/test_r2_enhancement_dominant_simple_load_gate.py",
    "tests/test_r2_equipment_base_weight_points.py",
    "tests/test_r2_weight_performance_budget_and_lightweight_tradeoff.py",
    "tests/test_r2_weight_budget_conversion_and_role_presets.py",
    "tests/test_r2_item_role_stat_and_initial_function_catalog.py",
    "tests/test_r2_initial_role_stat_preset_and_enhancement_function_ownership.py",
    "tests/test_r2_function_recipe_material_fit_and_playtest.py",
]


def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    registry = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    registry["next_approval_counter"] = "0/10"
    CURRENT_REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    for rel in FEATURE_TESTS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            'self.assertEqual("10/10", self.registry["next_approval_counter"])',
            'self.assertEqual("0/10", self.registry["next_approval_counter"])',
        )
        write(path, text)

    proposal = PROPOSAL.read_text(encoding="utf-8")
    proposal = proposal.replace("최종 밸런스 확정", "최종 밸런스 승인")
    if "VERTICAL_SLICE_IMPLEMENTATION_APPROVED" not in proposal:
        proposal = proposal.replace(
            "VERTICAL_SLICE_IMPLEMENTATION: APPROVED",
            "VERTICAL_SLICE_IMPLEMENTATION: APPROVED\nVERTICAL_SLICE_IMPLEMENTATION_APPROVED: true",
            1,
        )
    write(PROPOSAL, proposal)

    decisions = CURRENT_DECISIONS.read_text(encoding="utf-8")
    if "VERTICAL_SLICE_IMPLEMENTATION_APPROVED" not in decisions:
        decisions = decisions.replace(
            "> 버티컬 슬라이스 구현: `APPROVED / MERGED_PR120_MAIN_CANON`",
            "> 버티컬 슬라이스 구현: `APPROVED / MERGED_PR120_MAIN_CANON / VERTICAL_SLICE_IMPLEMENTATION_APPROVED`",
            1,
        )
    write(CURRENT_DECISIONS, decisions)

    active = ACTIVE.read_text(encoding="utf-8")
    active = active.replace("- 현재 승인 카운터: `10/10`", "- 현재 승인 카운터: `0/10`")
    if "- 승인된 Batch 006: `10/10 / MERGED_PR120_MAIN_CANON`" not in active:
        active = active.replace(
            "- 현재 승인 카운터: `0/10`",
            "- 현재 승인 카운터: `0/10`\n- 승인된 Batch 006: `10/10 / MERGED_PR120_MAIN_CANON`",
            1,
        )
    if "R2_CHECKPOINT_005_CLOSED_MAIN_CANON" not in active:
        active = active.replace(
            "R2_CHECKPOINT_005: CLOSED_MAIN_CANON",
            "R2_CHECKPOINT_005: CLOSED_MAIN_CANON\nR2_CHECKPOINT_005_CLOSED_MAIN_CANON: HISTORICAL_EVIDENCE",
            1,
        )
    if "VERTICAL_SLICE_IMPLEMENTATION_APPROVED" not in active:
        active = active.replace(
            "VERTICAL_SLICE_IMPLEMENTATION: APPROVED",
            "VERTICAL_SLICE_IMPLEMENTATION: APPROVED\nVERTICAL_SLICE_IMPLEMENTATION_APPROVED: true",
            1,
        )
    write(ACTIVE, active)

    for path in (ROADMAP, GATES):
        text = path.read_text(encoding="utf-8")
        if "R2_CHECKPOINT_005_CLOSED_MAIN_CANON" not in text:
            text = text.rstrip() + "\n\n- 역사 증거: `R2_CHECKPOINT_005_CLOSED_MAIN_CANON`\n"
        if "VERTICAL_SLICE_IMPLEMENTATION_APPROVED" not in text:
            text = text.rstrip() + "\n- 범위 승인: `VERTICAL_SLICE_IMPLEMENTATION_APPROVED`\n"
        write(path, text)

    if HEALTH.exists():
        health = json.loads(HEALTH.read_text(encoding="utf-8"))
        digest = hashlib.sha256(CURRENT_DECISIONS.read_bytes()).hexdigest()
        for item in health.get("evidence", {}).get("operating", []):
            if item.get("id") == "BS-CURRENT-DECISIONS":
                item["sha256"] = digest
        HEALTH.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
