#!/usr/bin/env python3
"""Require real consumers, recorded candidates, and a user-lock boundary for equipment art."""

from __future__ import annotations

import json
import hashlib
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "docs/planning/BLACKSMITH_FIVE_EQUIPMENT_VISUAL_REQUIREMENTS_20260830.json"
CATALOG = ROOT / "data/vertical_slice/vertical_slice_equipment_catalog_20260830.json"
ASSET_MANIFEST = ROOT / "assets/ASSET_MANIFEST.json"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SOURCE_DIMENSIONS = "1254x1254"
RUNTIME_IMPORT_MAX_DIMENSION = 512


def png_dimensions(path: Path) -> tuple[int, int]:
    payload = path.read_bytes()
    if not payload.startswith(PNG_SIGNATURE) or payload[12:16] != b"IHDR":
        raise AssertionError(f"not a PNG with an IHDR header: {path}")
    return struct.unpack(">II", payload[16:24])


class FiveEquipmentVisualRequirementsContractTest(unittest.TestCase):
    def test_five_user_locked_item_illustrations_are_registered_at_their_real_runtime_consumers(self) -> None:
        payload = json.loads(REQUIREMENTS.read_text(encoding="utf-8"))
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        manifest_by_id = {asset["asset_id"]: asset for asset in manifest["asset_records"]}
        self.assertEqual(payload["art_direction"], "ILLUSTRATED_WORKSHOP_BOOK")
        self.assertEqual(payload["post_generation_user_lock"], "REQUIRED_FOR_RUNTIME_PROMOTION")
        self.assertEqual(catalog["runtime_image_promotion"], "IMPLEMENTED_MACHINE_VERIFIED")
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
        catalog_by_id = {entry["equipment_id"]: entry for entry in catalog["equipment"]}
        for entry in entries:
            self.assertEqual(entry["candidate_status"], "USER_APPROVED")
            self.assertEqual(entry["runtime_promotion_status"], "IMPLEMENTED_MACHINE_VERIFIED")
            self.assertEqual(entry["target_aspect_resolution"], f"1:1 / {SOURCE_DIMENSIONS} PNG")
            self.assertEqual(entry["accepted_source_dimensions"], SOURCE_DIMENSIONS)
            self.assertEqual(
                entry["runtime_import_policy"],
                {
                    "max_dimension_px": RUNTIME_IMPORT_MAX_DIMENSION,
                    "compression": "LOSSLESS_2D_NO_MIPMAPS",
                    "source_provenance_bytes_preserved": True,
                },
            )
            self.assertFalse(entry["generated_ui_screenshot"])
            self.assertEqual(entry["actual_consumers"], ["FIRST_FORGE_EQUIPMENT_CHOICE", "WORKSHOP_EQUIPMENT_IDENTITY_HERO"])
            self.assertTrue(entry["primary_use"])
            self.assertTrue(entry["state_family_requirement"])
            receipt = entry["candidate_receipt"]
            self.assertEqual(receipt["source"], "OpenAI ImageGen")
            self.assertEqual(receipt["pixel_dimensions"], SOURCE_DIMENSIONS)
            self.assertEqual(receipt["review_status"], "USER_LOCKED_FOR_RUNTIME_PROMOTION")
            self.assertTrue(receipt["local_candidate_path"].endswith(".png"))
            self.assertEqual(len(receipt["sha256"]), 64)
            catalog_entry = catalog_by_id[entry["equipment_id"]]
            image_path = ROOT / catalog_entry["image_path"].replace("res://", "")
            self.assertTrue(image_path.is_file())
            self.assertEqual(png_dimensions(image_path), (1254, 1254))
            actual_sha256 = hashlib.sha256(image_path.read_bytes()).hexdigest()
            self.assertEqual(actual_sha256, receipt["sha256"])
            import_text = image_path.with_name(image_path.name + ".import").read_text(encoding="utf-8")
            self.assertIn(f'source_file="{catalog_entry["image_path"]}"', import_text)
            self.assertIn(f"process/size_limit={RUNTIME_IMPORT_MAX_DIMENSION}", import_text)
            self.assertIn('"vram_texture": false', import_text)
            self.assertIn("compress/mode=0", import_text)
            self.assertIn("mipmaps/generate=false", import_text)
            asset = manifest_by_id[catalog_entry["image_asset_id"]]
            self.assertEqual(asset["status"], "IMPLEMENTED_MACHINE_VERIFIED")
            self.assertEqual(asset["sha256"].lower(), actual_sha256)
            self.assertEqual(asset["dimensions"], SOURCE_DIMENSIONS)
            self.assertEqual(asset["tracked_asset_path"], catalog_entry["image_path"].replace("res://", ""))
            self.assertEqual(asset["actual_consumer"], entry["actual_consumers"])


if __name__ == "__main__":
    unittest.main()
