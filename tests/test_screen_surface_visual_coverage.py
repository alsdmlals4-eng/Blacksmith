from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json"
RUNTIME_BACKGROUND = ROOT / "assets/ui/workshop/workshop_enhancement_background_v2.png"
WORKPIECE_DURABILITY_ATLAS = ROOT / "assets/ui/workshop/workpiece_durability_state_atlas_v1.png"
FIRST_FORGE_BACKGROUND = ROOT / "assets/ui/workshop/first_forge_background_v1.png"
PRODUCTION_REFERENCE = ROOT / "assets/visual_reference/illustrated_workshop_book_reference_v1.png"
KEY_ART_MASTER = ROOT / "assets/marketing/blacksmith_key_art_master_v1.png"
APP_ICON_MASTER = ROOT / "assets/marketing/blacksmith_app_icon_master_v1.png"
ASSET_MANIFEST = ROOT / "assets/ASSET_MANIFEST.json"


class ScreenSurfaceVisualCoverageTests(unittest.TestCase):
    def test_current_runtime_screens_and_their_asset_modes_are_accounted_for(self) -> None:
        self.assertTrue(MODEL.is_file(), MODEL)
        model = json.loads(MODEL.read_text(encoding="utf-8"))

        self.assertEqual(model["issue"], "#291")
        self.assertEqual(model["delivery_issue"], "#293")
        self.assertEqual(model["image_generation"], "USER_APPROVED_RUNTIME_ASSET_EXECUTED_20260828")
        self.assertTrue(model["no_automatic_generation_from_gaps"])
        self.assertEqual(model["runtime_visual_validation"], "NOT_RUN")

        rows = {row["screen_id"]: row for row in model["screen_inventory"]}
        self.assertEqual(
            set(rows),
            {
                "MAIN_MENU",
                "FIRST_FORGE",
                "WORKSHOP",
                "ENHANCEMENT_IN_WORKSHOP",
                "CUSTOMER_WORLD_RESULT",
                "SETTINGS_OVERLAY",
                "RECURRING_PRECISION_TAG_CHOICE",
                "ITEM_CHRONICLE",
            },
        )
        for row in rows.values():
            self.assertEqual(
                set(row),
                {
                    "screen_id",
                    "screen_family",
                    "screen_name",
                    "project_stage",
                    "priority",
                    "flow_entry",
                    "flow_exit",
                    "player_goal",
                    "player_question",
                    "consumer_kind",
                    "consumer_surface",
                    "screen_design_reference",
                    "runtime_consumer",
                    "existing_evidence",
                    "coverage_status",
                    "notion_destination",
                    "repository_destination",
                    "blockers",
                },
            )
            if row["coverage_status"] == "NOT_APPLICABLE":
                self.assertTrue(row["blockers"])

        self.assertEqual(
            rows["MAIN_MENU"]["coverage_status"],
            "COVERED_APPROVED_RUNTIME_ASSET_MACHINE_VERIFIED",
        )
        self.assertEqual(rows["FIRST_FORGE"]["coverage_status"], "COVERED_PROJECT_ASSET_APPROVED")
        self.assertEqual(rows["WORKSHOP"]["coverage_status"], "COVERED_PROJECT_ASSET_APPROVED")
        self.assertEqual(rows["ENHANCEMENT_IN_WORKSHOP"]["coverage_status"], "COVERED_EXISTING")
        self.assertEqual(
            rows["CUSTOMER_WORLD_RESULT"]["coverage_status"],
            "COVERED_APPROVED_RUNTIME_ASSET_MACHINE_VERIFIED",
        )
        self.assertEqual(rows["SETTINGS_OVERLAY"]["coverage_status"], "GAP_NONBLOCKING")
        self.assertEqual(
            rows["RECURRING_PRECISION_TAG_CHOICE"]["coverage_status"],
            "COVERED_NATIVE_UI_ONLY_MACHINE_VERIFIED",
        )
        self.assertEqual(rows["ITEM_CHRONICLE"]["coverage_status"], "DEFERRED_BY_DECISION")

    def test_user_approved_runtime_raster_has_a_durable_provenance_record(self) -> None:
        self.assertTrue(MODEL.is_file(), MODEL)
        self.assertTrue(RUNTIME_BACKGROUND.is_file(), RUNTIME_BACKGROUND)
        model = json.loads(MODEL.read_text(encoding="utf-8"))
        assets = {row["asset_id"]: row for row in model["asset_coverage"]}
        asset = assets["ASSET-WORKSHOP-BACKGROUND-V2"]

        self.assertEqual(asset["production_mode"], "AI_GENERATED_PROJECT_RASTER")
        self.assertEqual(asset["asset_lifecycle_state"], "PROJECT_ASSET_APPROVED")
        self.assertEqual(asset["approval_state"], "USER_APPROVED_IMAGE_GENERATION_20260828")
        self.assertEqual(asset["runtime_consumption"], "WORKSHOP_STATIC_AND_MAIN_MENU_DYNAMIC_BINDING")
        self.assertEqual(
            asset["rights_and_provenance"],
            "PROJECT_RECORD_PRESENT_RELEASE_RIGHTS_REVIEW_PENDING",
        )
        self.assertEqual(asset["sha256"], hashlib.sha256(RUNTIME_BACKGROUND.read_bytes()).hexdigest().upper())
        self.assertEqual(asset["dimensions"], "941x1672")
        self.assertEqual(asset["consumer_ids"], ["WORKSHOP", "MAIN_MENU"])

        queue = {row["queue_id"]: row for row in model["runtime_asset_family_queue"]}
        self.assertEqual(queue["RUNTIME-CURRENT-01"]["image_generation"], "EXECUTED")
        self.assertEqual(
            model["adversarial_review"]["asset_completeness"],
            "PROJECT_ASSET_APPROVED_RUNTIME_CLIENT_VALIDATION_PENDING",
        )
        p0_findings = {
            row["finding_id"]: row
            for row in model["correction_log"]
            if row["severity"] == "P0"
        }
        self.assertIn("BS-VIS-AUDIT-20260827-02", p0_findings)
        self.assertIn("legacy", p0_findings["BS-VIS-AUDIT-20260827-02"]["disposition"].lower())

    def test_runtime_asset_manifest_matches_the_promoted_background_bytes(self) -> None:
        self.assertTrue(ASSET_MANIFEST.is_file(), ASSET_MANIFEST)
        self.assertTrue(RUNTIME_BACKGROUND.is_file(), RUNTIME_BACKGROUND)
        manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        records = {row["asset_id"]: row for row in manifest["asset_records"]}
        record = records["ASSET-WORKSHOP-BACKGROUND-V2"]
        requirements = {row["requirement_id"]: row for row in manifest["visual_requirements"]}
        requirement = requirements[record["requirement_id"]]

        self.assertEqual(record["status"], "PROJECT_ASSET_APPROVED")
        self.assertEqual(record["tracked_asset_path"], "assets/ui/workshop/workshop_enhancement_background_v2.png")
        self.assertEqual(record["actual_consumer"], ["WORKSHOP", "MAIN_MENU"])
        self.assertIn("MAIN_MENU_USES_RUNTIME_SCRIPT_OVERRIDE", record["delivery_incident"])
        self.assertEqual(record["sha256"], hashlib.sha256(RUNTIME_BACKGROUND.read_bytes()).hexdigest().upper())
        self.assertEqual(requirement["consumer_id"], "WORKSHOP_AND_MAIN_MENU")
        self.assertEqual(
            requirement["consumer_surface"],
            "res://scenes/vertical_slice/screens/vs_workshop_screen.tscn; res://scenes/vertical_slice/main_menu.tscn",
        )
        self.assertEqual(requirement["runtime_asset_role"], "WorkshopIllustratedBackground TextureRect")
        self.assertEqual(requirement["primary_use"], "Portrait illustrated workshop background behind native Godot text and controls")
        self.assertEqual(
            requirement["implementation_owner_or_path"],
            "res://scripts/vertical_slice/ui/vs_workshop_screen.gd; res://scripts/vertical_slice/ui/vs_main_menu.gd",
        )
        self.assertEqual(requirement["target_aspect_resolution"], "PORTRAIT_941x1672")
        self.assertEqual(requirement["state_family_requirement"], "STATIC_BACKGROUND_ONLY")
        self.assertEqual(requirement["fallback_if_unconsumed"], "REVERT_TO_EXISTING_GODOT_COLORRECT_FALLBACK")

    def test_durability_state_atlas_has_a_real_workshop_consumer_and_all_required_states(self) -> None:
        self.assertTrue(MODEL.is_file(), MODEL)
        self.assertTrue(ASSET_MANIFEST.is_file(), ASSET_MANIFEST)
        self.assertTrue(WORKPIECE_DURABILITY_ATLAS.is_file(), WORKPIECE_DURABILITY_ATLAS)
        model = json.loads(MODEL.read_text(encoding="utf-8"))
        manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))

        assets = {row["asset_id"]: row for row in model["asset_coverage"]}
        asset = assets["ASSET-WORKPIECE-DURABILITY-STATE-ATLAS-V1"]
        self.assertEqual(asset["runtime_consumption"], "IMPLEMENTED_DYNAMIC_ATLAS_BINDING")
        self.assertEqual(asset["consumer_ids"], ["WORKSHOP"])
        self.assertEqual(
            asset["state_family_requirement"],
            "NORMAL_TOP_LEFT; MINOR_TOP_RIGHT; MAJOR_BOTTOM_LEFT; DESTROYED_BOTTOM_RIGHT",
        )
        self.assertEqual(asset["sha256"], hashlib.sha256(WORKPIECE_DURABILITY_ATLAS.read_bytes()).hexdigest().upper())

        records = {row["asset_id"]: row for row in manifest["asset_records"]}
        record = records["ASSET-WORKPIECE-DURABILITY-STATE-ATLAS-V1"]
        requirements = {row["requirement_id"]: row for row in manifest["visual_requirements"]}
        requirement = requirements[record["requirement_id"]]
        self.assertEqual(record["runtime_slot"], ["WorkshopScroll/WorkshopLayout/WorkpieceDurabilityHero"])
        self.assertEqual(requirement["consumer_id"], "WORKSHOP")
        self.assertEqual(requirement["runtime_asset_role"], "WorkpieceDurabilityHero TextureRect AtlasTexture")

    def test_first_forge_background_has_an_actual_runtime_consumer(self) -> None:
        self.assertTrue(MODEL.is_file(), MODEL)
        self.assertTrue(ASSET_MANIFEST.is_file(), ASSET_MANIFEST)
        self.assertTrue(FIRST_FORGE_BACKGROUND.is_file(), FIRST_FORGE_BACKGROUND)
        model = json.loads(MODEL.read_text(encoding="utf-8"))
        manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))

        assets = {row["asset_id"]: row for row in model["asset_coverage"]}
        asset = assets["ASSET-FIRST-FORGE-BACKGROUND-V1"]
        self.assertEqual(asset["runtime_consumption"], "IMPLEMENTED_DYNAMIC_BACKGROUND_BINDING")
        self.assertEqual(asset["consumer_ids"], ["FIRST_FORGE"])
        self.assertEqual(asset["sha256"], hashlib.sha256(FIRST_FORGE_BACKGROUND.read_bytes()).hexdigest().upper())

        records = {row["asset_id"]: row for row in manifest["asset_records"]}
        record = records["ASSET-FIRST-FORGE-BACKGROUND-V1"]
        requirements = {row["requirement_id"]: row for row in manifest["visual_requirements"]}
        requirement = requirements[record["requirement_id"]]
        self.assertEqual(record["actual_consumer"], ["FIRST_FORGE"])
        self.assertEqual(requirement["consumer_id"], "FIRST_FORGE")
        self.assertEqual(requirement["runtime_asset_role"], "FirstForgeIllustratedBackground TextureRect")

    def test_production_and_release_visuals_remain_separate_from_runtime_assets(self) -> None:
        self.assertTrue(ASSET_MANIFEST.is_file(), ASSET_MANIFEST)
        for path in (PRODUCTION_REFERENCE, KEY_ART_MASTER, APP_ICON_MASTER):
            self.assertTrue(path.is_file(), path)
        manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        assets = {row["asset_id"]: row for row in manifest["non_runtime_asset_records"]}

        production = assets["ASSET-ILLUSTRATED-WORKSHOP-BOOK-REFERENCE-V1"]
        self.assertEqual(production["asset_category"], "PRODUCTION_VISUAL_REFERENCE")
        self.assertEqual(production["runtime_consumer"], "NONE_BY_DESIGN")
        self.assertEqual(production["sha256"], hashlib.sha256(PRODUCTION_REFERENCE.read_bytes()).hexdigest().upper())

        for asset_id, path in (
            ("ASSET-BLACKSMITH-KEY-ART-MASTER-V1", KEY_ART_MASTER),
            ("ASSET-BLACKSMITH-APP-ICON-MASTER-V1", APP_ICON_MASTER),
        ):
            asset = assets[asset_id]
            self.assertEqual(asset["asset_category"], "RELEASE_MARKETING_MASTER")
            self.assertEqual(asset["status"], "RELEASE_DRAFT_NOT_PLATFORM_READY")
            self.assertEqual(asset["runtime_consumer"], "NONE_BY_DESIGN")
            self.assertEqual(asset["sha256"], hashlib.sha256(path.read_bytes()).hexdigest().upper())


if __name__ == "__main__":
    unittest.main()
