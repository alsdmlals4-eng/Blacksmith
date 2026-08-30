#!/usr/bin/env python3
"""Require real consumers, recorded candidates, and a user-lock boundary for equipment art."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "docs/planning/BLACKSMITH_FIVE_EQUIPMENT_VISUAL_REQUIREMENTS_20260830.json"


class FiveEquipmentVisualRequirementsContractTest(unittest.TestCase):
    def test_five_item_candidates_have_real_consumers_and_wait_for_user_lock(self) -> None:
        payload = json.loads(REQUIREMENTS.read_text(encoding="utf-8"))
        self.assertEqual(payload["art_direction"], "ILLUSTRATED_WORKSHOP_BOOK")
        self.assertEqual(payload["post_generation_user_lock"], "REQUIRED_FOR_RUNTIME_PROMOTION")
        entries = payload["visual_requirements"]
        self.assertEqual(
            [entry["consumer_id"] for entry in entries],
            [
                "VIS-EQUIP-20260830-01",
                "VIS-EQUIP-20260830-02",
                "VIS-EQUIP-20260830-03",
                "VIS-EQUIP-20260830-04",
                "VIS-EQUIP-20260830-05",
            ],
        )
        for entry in entries:
            self.assertEqual(entry["candidate_status"], "GENERATED_CANDIDATE")
            self.assertEqual(entry["runtime_promotion_status"], "NOT_PROMOTED_WAITING_FOR_USER_LOCK")
            self.assertEqual(entry["target_aspect_resolution"], "1:1 / 1024x1024 PNG")
            self.assertFalse(entry["generated_ui_screenshot"])
            self.assertEqual(entry["actual_consumers"], ["FIRST_FORGE_EQUIPMENT_CHOICE", "WORKSHOP_EQUIPMENT_IDENTITY_HERO"])
            self.assertTrue(entry["primary_use"])
            self.assertTrue(entry["state_family_requirement"])
            receipt = entry["candidate_receipt"]
            self.assertEqual(receipt["source"], "OpenAI ImageGen")
            self.assertEqual(receipt["pixel_dimensions"], "1254x1254")
            self.assertEqual(receipt["review_status"], "GENERATED_CANDIDATE_PENDING_USER_LOCK")
            self.assertTrue(receipt["local_candidate_path"].endswith(".png"))
            self.assertEqual(len(receipt["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
