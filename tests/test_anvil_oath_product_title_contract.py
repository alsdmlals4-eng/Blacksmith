"""Protect the player-visible Anvil Oath title boundary across its real consumers."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
TITLE_DECISION = ROOT / "docs/decisions/BS-IDENTITY-20260831-39_ANVIL_OATH_PRODUCT_TITLE.md"
MAIN_MENU = ROOT / "scenes/vertical_slice/main_menu.tscn"
HUMAN_GDD = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md"
PDF = ROOT / "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf"
PDF_RECEIPT = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json"


class AnvilOathProductTitleContractTests(unittest.TestCase):
    def test_player_facing_title_is_consistent_without_renaming_workshop_actions(self) -> None:
        """Changing a product title must not erase the generic workshop actions players use."""
        decision_text = TITLE_DECISION.read_text(encoding="utf-8")
        scene_text = MAIN_MENU.read_text(encoding="utf-8")
        human_gdd = HUMAN_GDD.read_text(encoding="utf-8")
        receipt = json.loads(PDF_RECEIPT.read_text(encoding="utf-8"))
        reader = PdfReader(str(PDF))

        self.assertIn("PRODUCT_TITLE_KO = 모루의 서약", decision_text)
        self.assertIn("PRODUCT_TITLE_LATIN = ANVIL OATH", decision_text)
        self.assertIn('text = "모루의 서약"', scene_text)
        self.assertIn('text = "새 대장간 시작"', scene_text)
        self.assertTrue(human_gdd.startswith("# 모루의 서약 — 사람용 게임 기획서"))
        self.assertIn("모루의 서약 / ANVIL OATH", human_gdd)
        self.assertEqual(reader.metadata.title, "모루의 서약 · 사람용 게임 기획서")
        self.assertEqual(receipt["product_identity"]["decision_id"], "BS-IDENTITY-20260831-39")
        self.assertEqual(receipt["product_identity"]["latin_lockup"], "ANVIL OATH")
        self.assertEqual(receipt["product_identity"]["legal_clearance"], "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
