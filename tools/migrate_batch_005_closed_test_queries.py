from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
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
)

METHOD = re.compile(
    r"(?ms)(^    def test_batch_005_[^\n]+\n.*?)(?=^    def |\Z)"
)


def migrate_block(match: re.Match[str]) -> str:
    block = match.group(1)
    block = block.replace(
        'active = self.registry["active_batch"]',
        'closed = self.registry["closed_batch"]',
    )
    block = block.replace('active["', 'closed["')
    block = block.replace(
        "test_batch_005_is_active_at_ten_of_ten",
        "test_batch_005_is_closed_at_ten_of_ten",
    )
    return block


def main() -> int:
    changed: list[str] = []
    for relative in TESTS:
        path = ROOT / relative
        before = path.read_text(encoding="utf-8")
        after, count = METHOD.subn(migrate_block, before)
        after = after.replace(
            'self.assertIn("현재 승인 카운터: `10/10`", active)',
            'self.assertIn("현재 승인 카운터: `0/10`", active)',
        )
        if count == 0:
            raise RuntimeError(f"Batch 005 test block not found: {relative}")
        if after != before:
            path.write_text(after, encoding="utf-8", newline="\n")
            changed.append(relative)
    print("changed=" + (",".join(changed) if changed else "NONE"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
