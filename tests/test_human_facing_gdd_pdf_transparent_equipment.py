"""Require transparent equipment art to stay free of black boxes in the human-facing PDF."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image as PILImage


ROOT = Path(__file__).resolve().parents[1]
PUBLISHER_PATH = ROOT / "tools/publish_human_facing_gdd_pdf.py"
SPEC = importlib.util.spec_from_file_location("blacksmith_human_gdd_publisher", PUBLISHER_PATH)
assert SPEC is not None and SPEC.loader is not None
PUBLISHER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PUBLISHER)


class HumanFacingGddPdfTransparentEquipmentTest(unittest.TestCase):
    def test_transparent_equipment_derivative_uses_the_document_paper_not_black(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source_path = Path(temporary_directory) / "transparent_equipment.png"
            source = PILImage.new("RGBA", (8, 8), (0, 0, 0, 0))
            source.putpixel((4, 4), (160, 96, 42, 255))
            source.save(source_path)

            derivative = PUBLISHER.pdf_derivative_image(
                source_path,
                width=10,
                height=10,
                max_pixels=(8, 8),
            )
            derivative._blacksmith_derivative_buffer.seek(0)
            with PILImage.open(derivative._blacksmith_derivative_buffer) as rendered:
                self.assertEqual(rendered.mode, "RGB")
                self.assertGreaterEqual(min(rendered.getpixel((0, 0))), 250)


if __name__ == "__main__":
    unittest.main()
