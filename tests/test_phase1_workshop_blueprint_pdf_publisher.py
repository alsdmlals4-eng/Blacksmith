#!/usr/bin/env python3
"""Unit-level regression checks for the detailed Blueprint Viewer publisher."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from tools import publish_phase1_workshop_blueprint_pdf as publisher


class Phase1WorkshopBlueprintPublisherTest(unittest.TestCase):
    def test_runtime_asset_references_are_limited_to_the_existing_approved_family(self) -> None:
        expected_paths = {
            "assets/ui/identity/anvil_oath_logo_ao02_v1.png",
            "assets/ui/workshop/workshop_enhancement_background_v2.png",
            "assets/ui/workshop/workpiece_durability_state_atlas_v1.png",
            "assets/ui/workshop/customer_result_return_illustration_v1.png",
            "assets/ui/equipment/iron_sword_card_v2.png",
            "assets/ui/equipment/iron_shield_card_v2.png",
            "assets/ui/equipment/iron_bow_card_v2.png",
            "assets/ui/equipment/iron_armor_card_v2.png",
            "assets/ui/equipment/iron_helmet_card_v2.png",
        }

        references = publisher.RUNTIME_ASSET_REFERENCES

        self.assertEqual(expected_paths, {reference["path"] for reference in references})
        self.assertEqual(
            {1, 3, 9, 10, 11},
            set(publisher.RUNTIME_ASSET_REFERENCE_PAGES),
        )
        self.assertTrue(all((publisher.ROOT / reference["path"]).is_file() for reference in references))
        self.assertTrue(all(reference["asset_id"].startswith("ASSET-") for reference in references))

    def test_pdf_reference_rasters_are_bounded_without_changing_the_source_assets(self) -> None:
        source_path = publisher.ROOT / "assets/ui/workshop/workshop_enhancement_background_v2.png"
        source_sha_before = publisher.sha256(source_path)

        image_reader = publisher.runtime_asset_image_reader("ASSET-WORKSHOP-BACKGROUND-V2")

        self.assertEqual((432, 768), image_reader.getSize())
        self.assertEqual(source_sha_before, publisher.sha256(source_path))

    def test_draw_pdf_emits_eleven_pages_without_node_argument_errors(self) -> None:
        original_output = publisher.OUTPUT
        try:
            with tempfile.TemporaryDirectory() as temporary_directory:
                publisher.OUTPUT = Path(temporary_directory) / "blueprint.pdf"
                publisher.draw_pdf()
                self.assertTrue(publisher.OUTPUT.exists())
                reader = PdfReader(str(publisher.OUTPUT))
                self.assertEqual(11, len(reader.pages))
                image_pages = {
                    page_number
                    for page_number, page in enumerate(reader.pages, start=1)
                    if page.images
                }
                self.assertTrue(
                    set(publisher.RUNTIME_ASSET_REFERENCE_PAGES).issubset(image_pages),
                    f"missing runtime asset references on pages: "
                    f"{set(publisher.RUNTIME_ASSET_REFERENCE_PAGES) - image_pages}",
                )
        finally:
            publisher.OUTPUT = original_output

    def test_layout_reserves_clear_space_above_the_footer(self) -> None:
        bounds = publisher.layout_bounds()
        self.assertGreaterEqual(bounds["footer_line_mm"], 14.0)
        self.assertGreaterEqual(bounds["page_two_guard_bottom_mm"], 20.0)
        self.assertGreaterEqual(bounds["page_three_phone_bottom_mm"], 48.0)
        self.assertGreaterEqual(bounds["page_three_support_card_bottom_mm"], 60.0)
        self.assertGreaterEqual(bounds["flow_node_body_left_mm"], 14.0)

    def test_detailed_page_plan_keeps_each_core_decision_visible(self) -> None:
        self.assertEqual(11, publisher.PAGE_COUNT)
        self.assertEqual(11, len(publisher.PAGE_SECTIONS))
        self.assertIn("최초 +10", publisher.PAGE_SECTIONS)
        self.assertIn("+20 이후", publisher.PAGE_SECTIONS)
        self.assertIn("검증과 증거 한계", publisher.PAGE_SECTIONS)


if __name__ == "__main__":
    unittest.main()
