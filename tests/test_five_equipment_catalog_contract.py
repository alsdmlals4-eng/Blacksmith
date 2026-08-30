#!/usr/bin/env python3
"""Protect the current five-equipment MVP catalog before Godot consumes it."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/vertical_slice/vertical_slice_equipment_catalog_20260830.json"


class FiveEquipmentCatalogContractTest(unittest.TestCase):
    def test_catalog_has_exactly_the_approved_five_types(self) -> None:
        payload = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "CURRENT_USER_APPROVED_FIVE_EQUIPMENT_MVP")
        entries = payload["equipment"]
        self.assertEqual(
            [entry["equipment_id"] for entry in entries],
            ["iron_sword", "iron_shield", "iron_bow", "iron_armor", "iron_helmet"],
        )

    def test_precision_is_weapon_only_without_a_new_defensive_tag_system(self) -> None:
        payload = json.loads(CATALOG.read_text(encoding="utf-8"))
        eligibility = {entry["equipment_id"]: entry["precision_tag_eligible"] for entry in payload["equipment"]}
        self.assertEqual(
            eligibility,
            {
                "iron_sword": True,
                "iron_shield": True,
                "iron_bow": True,
                "iron_armor": False,
                "iron_helmet": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
