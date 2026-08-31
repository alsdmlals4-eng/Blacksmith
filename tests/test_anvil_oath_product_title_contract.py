"""Protect the player-visible Anvil Oath title boundary across its real consumers."""

from __future__ import annotations

import json
import hashlib
import unittest
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
TITLE_DECISION = ROOT / "docs/decisions/BS-IDENTITY-20260831-39_ANVIL_OATH_PRODUCT_TITLE.md"
MAIN_MENU = ROOT / "scenes/vertical_slice/main_menu.tscn"
HUMAN_GDD = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md"
PDF = ROOT / "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf"
PDF_RECEIPT = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json"
MAIN_MENU_SCRIPT = ROOT / "scripts/vertical_slice/ui/vs_main_menu.gd"
ASSET_MANIFEST = ROOT / "assets/ASSET_MANIFEST.json"
ASSET_RIGHTS = ROOT / "docs/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md"
LOGO_ASSET = ROOT / "assets/ui/identity/anvil_oath_logo_ao02_v1.png"
LOGO_ASSET_SHA256 = "320be3fc5530392e313e20b0a34375971a7a600754bf259b18db2da084e1f475"


class AnvilOathProductTitleContractTests(unittest.TestCase):
    def test_user_locked_ao_logo_02_is_a_registered_main_menu_runtime_asset(self) -> None:
        """The chosen logo must be a real, traceable menu asset rather than a detached candidate."""
        decision_text = TITLE_DECISION.read_text(encoding="utf-8")
        menu_script = MAIN_MENU_SCRIPT.read_text(encoding="utf-8")
        manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        rights_text = ASSET_RIGHTS.read_text(encoding="utf-8")

        self.assertTrue(LOGO_ASSET.is_file(), LOGO_ASSET)
        if not LOGO_ASSET.is_file():
            return
        self.assertEqual(hashlib.sha256(LOGO_ASSET.read_bytes()).hexdigest(), LOGO_ASSET_SHA256)
        self.assertIn("LOGO_CANDIDATE_STATUS = USER_LOCKED_AO_LOGO_02", decision_text)
        self.assertIn("CANDIDATE_RUNTIME_PROMOTION = IMPLEMENTED_MACHINE_VERIFIED", decision_text)
        self.assertIn("LOGO_RUNTIME_VISUAL_STATUS = LIMITED_RUNTIME_VERIFIED", decision_text)
        self.assertIn("assets/ui/identity/anvil_oath_logo_ao02_v1.png", menu_script)
        self.assertIn("func _ensure_product_logo()", menu_script)

        records = {entry["asset_id"]: entry for entry in manifest["asset_records"]}
        requirement_records = {entry["requirement_id"]: entry for entry in manifest["visual_requirements"]}
        record = records["ASSET-ANVIL-OATH-LOGO-AO02-V1"]
        requirement = requirement_records[record["requirement_id"]]
        self.assertEqual(record["sha256"], LOGO_ASSET_SHA256.upper())
        self.assertEqual(record["actual_consumer"], ["MAIN_MENU"])
        self.assertEqual(record["runtime_slot"], ["MenuLayout/MenuTitleLogo"])
        self.assertEqual(record["status"], "IMPLEMENTED_MACHINE_VERIFIED")
        self.assertEqual(requirement["consumer_id"], "MAIN_MENU_PRODUCT_TITLE_LOCKUP")
        self.assertIn("asset_id: ASSET-ANVIL-OATH-LOGO-AO02-V1", rights_text)
        self.assertIn("status: RELEASE_BLOCKED_UNVERIFIED", rights_text)

    def test_player_facing_title_is_consistent_without_renaming_workshop_actions(self) -> None:
        """Changing a product title must not erase the generic workshop actions players use."""
        decision_text = TITLE_DECISION.read_text(encoding="utf-8")
        scene_text = MAIN_MENU.read_text(encoding="utf-8")
        human_gdd = HUMAN_GDD.read_text(encoding="utf-8")
        receipt = json.loads(PDF_RECEIPT.read_text(encoding="utf-8"))
        reader = PdfReader(str(PDF))

        self.assertIn("PRODUCT_TITLE_KO = 모루의 서약", decision_text)
        self.assertIn("PRODUCT_TITLE_LATIN = ANVIL OATH", decision_text)
        self.assertIn("TITLE_TEXT_RUNTIME_STATUS = IMPLEMENTED_MACHINE_AND_RUNTIME_VERIFIED", decision_text)
        self.assertIn("LOGO_CANDIDATE_STATUS = USER_LOCKED_AO_LOGO_02", decision_text)
        self.assertIn("CANDIDATE_RUNTIME_PROMOTION = IMPLEMENTED_MACHINE_VERIFIED", decision_text)
        self.assertIn("POSTMERGE_MAIN_SHA = 16e33b87b5c4880207466443b03beb3705ab8c57", decision_text)
        self.assertIn("PROTECTED_APPROVAL_STATUS = RETIRED_ON_POSTMERGE_BASELINE_CLOSURE", decision_text)
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
