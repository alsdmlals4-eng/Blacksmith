#!/usr/bin/env python3
"""Unit-level regression check for the five-page Blueprint Viewer publisher."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from tools import publish_phase1_workshop_blueprint_pdf as publisher


class Phase1WorkshopBlueprintPublisherTest(unittest.TestCase):
    def test_draw_pdf_emits_five_pages_without_node_argument_errors(self) -> None:
        original_output = publisher.OUTPUT
        try:
            with tempfile.TemporaryDirectory() as temporary_directory:
                publisher.OUTPUT = Path(temporary_directory) / "blueprint.pdf"
                publisher.draw_pdf()
                self.assertTrue(publisher.OUTPUT.exists())
                self.assertEqual(5, len(PdfReader(str(publisher.OUTPUT)).pages))
        finally:
            publisher.OUTPUT = original_output

    def test_layout_reserves_clear_space_above_the_footer(self) -> None:
        bounds = publisher.layout_bounds()
        self.assertGreaterEqual(bounds["footer_line_mm"], 14.0)
        self.assertGreaterEqual(bounds["page_two_guard_bottom_mm"], 20.0)
        self.assertGreaterEqual(bounds["page_three_phone_bottom_mm"], 48.0)
        self.assertGreaterEqual(bounds["page_three_support_card_bottom_mm"], 60.0)
        self.assertGreaterEqual(bounds["flow_node_body_left_mm"], 14.0)


if __name__ == "__main__":
    unittest.main()
