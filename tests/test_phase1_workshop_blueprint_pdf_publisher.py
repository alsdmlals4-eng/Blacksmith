#!/usr/bin/env python3
"""Unit-level regression checks for the detailed Blueprint Viewer publisher."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from tools import publish_phase1_workshop_blueprint_pdf as publisher


class Phase1WorkshopBlueprintPublisherTest(unittest.TestCase):
    def test_draw_pdf_emits_eleven_pages_without_node_argument_errors(self) -> None:
        original_output = publisher.OUTPUT
        try:
            with tempfile.TemporaryDirectory() as temporary_directory:
                publisher.OUTPUT = Path(temporary_directory) / "blueprint.pdf"
                publisher.draw_pdf()
                self.assertTrue(publisher.OUTPUT.exists())
                self.assertEqual(11, len(PdfReader(str(publisher.OUTPUT)).pages))
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
