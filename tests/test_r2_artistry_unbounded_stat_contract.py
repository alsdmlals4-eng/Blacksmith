from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CURRENT_FILES = (
    ROOT / "CURRENT_CONFIRMED_DECISIONS.md",
    ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md",
    ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md",
    ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
)


class ArtistryUnboundedStatContractTests(unittest.TestCase):
    def test_registry_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-CRAFT-20260805-01"]
        self.assertEqual(
            "USER_APPROVED_REFINED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON",
            decision["status"],
        )
        contract = decision["contract"]
        self.assertEqual("NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM", contract["domain"])
        self.assertEqual(0, contract["minimum"])
        self.assertIsNone(contract["fixed_design_maximum"])
        self.assertFalse(contract["decimals_allowed"])
        self.assertFalse(contract["denominator_display_allowed"])
        self.assertFalse(contract["named_tiers_exist"])
        self.assertFalse(contract["technical_storage_limit_is_content_maximum"])
        self.assertFalse(contract["grade_sets_fixed_artistry_maximum"])
        self.assertFalse(contract["zero_means_incomplete_or_unusable"])
        self.assertFalse(contract["combat_power_by_default"])
        self.assertFalse(contract["universal_affix_multiplier"])

    def test_current_authority_uses_raw_values(self) -> None:
        for path in CURRENT_FILES[:-1]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("예술성 27", text, path.as_posix())
            self.assertIn("고정 설계 최대치 없음", text, path.as_posix())
            self.assertNotIn("예술성 7/10", text, path.as_posix())
            self.assertNotIn("예술성 1~10", text, path.as_posix())
        # The original artistry decision preserves a dated handoff to its
        # successor; that historical label must not erase the active contract.
        self.assertIn("USER_APPROVED_REFINED_MERGED_PR106 / R2_CHECKPOINT_004_MAIN_CANON", CURRENT_FILES[2].read_text(encoding="utf-8"))

    def test_checkpoint_and_product_boundary(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual("R2_BATCH_006_APPROVED_MAIN_CANON", registry["stage_status"])
        self.assertEqual("0/10", registry["next_approval_counter"])
        self.assertEqual("R2_BATCH_005", registry["closed_batch"]["id"])
        self.assertEqual("10/10", registry["closed_batch"]["counter"])
        self.assertEqual("R2_BATCH_006", registry["active_batch"]["id"])
        self.assertEqual("10/10", registry["active_batch"]["counter"])
        self.assertEqual("BLOCKED", registry["product_implementation"])


if __name__ == "__main__":
    unittest.main()
