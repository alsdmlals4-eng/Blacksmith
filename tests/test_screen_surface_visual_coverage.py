from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json"
RUNTIME_BACKGROUND = ROOT / "assets/ui/workshop/workshop_enhancement_background_v1.png"


class ScreenSurfaceVisualCoverageTests(unittest.TestCase):
    def test_current_runtime_screens_and_their_asset_modes_are_accounted_for(self) -> None:
        self.assertTrue(MODEL.is_file(), MODEL)
        model = json.loads(MODEL.read_text(encoding="utf-8"))

        self.assertEqual(model["issue"], "#291")
        self.assertEqual(model["image_generation"], "NOT_RUN")
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
                "PRECISION_PLUS_9_TO_10",
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

        self.assertEqual(rows["MAIN_MENU"]["coverage_status"], "GAP_BLOCKING")
        self.assertEqual(rows["FIRST_FORGE"]["coverage_status"], "COVERED_EXISTING")
        self.assertEqual(rows["WORKSHOP"]["coverage_status"], "GAP_BLOCKING")
        self.assertEqual(rows["ENHANCEMENT_IN_WORKSHOP"]["coverage_status"], "COVERED_EXISTING")
        self.assertEqual(rows["CUSTOMER_WORLD_RESULT"]["coverage_status"], "COVERED_EXISTING")
        self.assertEqual(rows["SETTINGS_OVERLAY"]["coverage_status"], "GAP_NONBLOCKING")
        self.assertEqual(rows["PRECISION_PLUS_9_TO_10"]["coverage_status"], "DEFERRED_BY_DECISION")
        self.assertEqual(rows["ITEM_CHRONICLE"]["coverage_status"], "DEFERRED_BY_DECISION")

    def test_existing_runtime_raster_is_described_without_approval_promotion(self) -> None:
        self.assertTrue(MODEL.is_file(), MODEL)
        self.assertTrue(RUNTIME_BACKGROUND.is_file(), RUNTIME_BACKGROUND)
        model = json.loads(MODEL.read_text(encoding="utf-8"))
        assets = {row["asset_id"]: row for row in model["asset_coverage"]}
        asset = assets["ASSET-WORKSHOP-BACKGROUND-V1"]

        self.assertEqual(asset["production_mode"], "EXISTING_PROJECT_RASTER")
        self.assertEqual(asset["asset_lifecycle_state"], "LEGACY_RUNTIME_BOUND_UNVERIFIED")
        self.assertEqual(asset["approval_state"], "UNVERIFIED_NOT_PROMOTED")
        self.assertEqual(asset["runtime_consumption"], "IMPLEMENTED_STATIC_BINDING")
        self.assertEqual(
            asset["rights_and_provenance"],
            "NO_MATCHING_CURRENT_APPROVAL_OR_PROVENANCE_RECORD_FOUND",
        )
        self.assertEqual(asset["sha256"], hashlib.sha256(RUNTIME_BACKGROUND.read_bytes()).hexdigest().upper())
        self.assertEqual(asset["dimensions"], "941x1672")
        self.assertEqual(asset["consumer_ids"], ["MAIN_MENU", "WORKSHOP"])

        queue = {row["queue_id"]: row for row in model["runtime_asset_family_queue"]}
        self.assertEqual(queue["RUNTIME-EXISTING-01"]["image_generation"], "NOT_AUTHORIZED")
        self.assertEqual(
            model["adversarial_review"]["asset_completeness"],
            "EXPLICIT_P0_APPROVAL_PROVENANCE_BLOCKER",
        )
        p0_findings = {
            row["finding_id"]: row
            for row in model["correction_log"]
            if row["severity"] == "P0"
        }
        self.assertIn("BS-VIS-AUDIT-20260827-02", p0_findings)
        self.assertIn("do not generate, replace, or mark approved", p0_findings["BS-VIS-AUDIT-20260827-02"]["disposition"])


if __name__ == "__main__":
    unittest.main()
