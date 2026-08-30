from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PROTECTED_BASE = "464a9be4fe5fbd9aa5bc3692d73999d49fa86f71"
EXPECTED_PATHS = {
    "assets/ASSET_MANIFEST.json",
    "assets/ui/equipment/iron_sword_card_v1.png",
    "assets/ui/equipment/iron_sword_card_v1.png.import",
    "assets/ui/equipment/iron_shield_card_v1.png",
    "assets/ui/equipment/iron_shield_card_v1.png.import",
    "assets/ui/equipment/iron_bow_card_v1.png",
    "assets/ui/equipment/iron_bow_card_v1.png.import",
    "assets/ui/equipment/iron_armor_card_v1.png",
    "assets/ui/equipment/iron_armor_card_v1.png.import",
    "assets/ui/equipment/iron_helmet_card_v1.png",
    "assets/ui/equipment/iron_helmet_card_v1.png.import",
    "assets/ui/workshop/main_menu_dawn_background_v1.png.import",
    "assets/ui/workshop/customer_result_return_illustration_v1.png.import",
    "data/vertical_slice/vertical_slice_equipment_catalog_20260830.json",
    "scripts/ui/forging_screen.gd",
    "scripts/vertical_slice/ui/vs_workshop_screen.gd",
}


class EquipmentImagePromotionProtectedChangeApprovalTests(unittest.TestCase):
    def test_one_shot_approval_is_exactly_scoped_to_the_locked_runtime_promotion(self) -> None:
        payload = json.loads(APPROVAL.read_text(encoding="utf-8"))

        self.assertEqual("APPROVED", payload["status"])
        self.assertEqual(PROTECTED_BASE, payload["protected_base_commit"])
        self.assertEqual(EXPECTED_PATHS, set(payload["approved_paths"]))
        self.assertIn("BS-EQUIPMENT-20260830-39", payload["decision_ids"])
        self.assertIn("First-forge and Workshop identity slots only", payload["scope_summary"])

        for relative_path in payload["approved_paths"]:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)


if __name__ == "__main__":
    unittest.main()
