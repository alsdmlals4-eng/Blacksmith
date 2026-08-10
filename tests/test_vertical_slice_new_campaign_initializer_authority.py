from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs/decisions/BS-VS-INIT-20260808-01_NEW_CAMPAIGN_INITIALIZER.md"
DESIGN = ROOT / "docs/superpowers/specs/2026-08-08-blacksmith-new-campaign-initializer-design.md"
ENTRY_GATE = ROOT / "docs/operations/BLACKSMITH_TASK2_ENTRY_GATE_2026-08-08.json"
DEVELOPMENT_GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"


class VerticalSliceNewCampaignInitializerAuthorityTests(unittest.TestCase):
    def test_approved_initializer_authority_files_exist(self) -> None:
        for path in [DECISION, DESIGN, ENTRY_GATE, DEVELOPMENT_GATES]:
            self.assertTrue(path.is_file(), str(path))

    def test_initializer_decision_contract_is_exact(self) -> None:
        text = DECISION.read_text(encoding="utf-8")
        required = [
            "BS-VS-INIT-20260808-01",
            "RUN-<32_LOWER_HEX>",
            "CRYPTO_128_BIT_TOKEN",
            "RUN_RNG_SEED_FIRST_U32_OF_TOKEN",
            "RUN_RNG_SEED_RANGE_0_TO_4294967295",
            "UTC_ISO_8601_SECONDS_Z",
            "VS_RUN_INITIALIZER_SERVICE",
            "FIRST_SAVE_REQUIRED_BEFORE_CAMPAIGN_READY",
            "PRESERVE_VALID_BACKUP_WHEN_PRIMARY_CORRUPT",
            "GENERAL_PRODUCT_BLOCKED",
            "HERA_DISABLED_NON_AUTHORITATIVE",
        ]
        for token in required:
            self.assertIn(token, text)

    def test_entry_gate_snapshot_resolves_only_initializer_blocker(self) -> None:
        gate = json.loads(ENTRY_GATE.read_text(encoding="utf-8"))
        self.assertEqual(gate["decision_id"], "BS-VS-INIT-20260808-01")
        self.assertEqual(gate["initializer_authority"], "RESOLVED_USER_APPROVED")
        self.assertEqual(gate["task2_entry_gate"], "PASS_SCOPED_RED_ALLOWED")
        self.assertEqual(gate["general_product"], "BLOCKED")
        self.assertEqual(gate["product_image"], "BLOCKED_NOT_PRODUCT_READY")
        self.assertEqual(gate["image_rights"], "NOT_RUN")
        self.assertEqual(gate["android_device"], "NOT_RUN")
        self.assertEqual(gate["human_playtest"], "NOT_RUN")
        # Historical snapshot: captured before BS-HIGODOT-20260808-01 activation.
        self.assertEqual(gate["higodot_authority"], "PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY")
        self.assertEqual(gate["hera_authority"], "NONE")

    def test_current_development_gate_preserves_initializer_after_task2_closure(self) -> None:
        text = DEVELOPMENT_GATES.read_text(encoding="utf-8")
        self.assertIn("INITIALIZER_DECISION: BS-VS-INIT-20260808-01", text)
        self.assertIn("INITIALIZER_AUTHORITY: RESOLVED_USER_APPROVED", text)
        self.assertIn(
            "ENTRY_STATE_GATE: PASS_TASK2_CLOSED_NEW_PRODUCT_SCOPE_USER_DECISION_REQUIRED",
            text,
        )
        self.assertIn(
            "VERTICAL_SLICE_CODE_GATE: TASK2_MAIN_MERGED_NO_NEW_PRODUCT_SCOPE",
            text,
        )
        self.assertIn("TASK2: MAIN_MERGED_POSTMERGE_CI_CLOSURE_COMPLETE", text)
        self.assertIn("HIGODOT_ACTIVATION_DECISION: BS-HIGODOT-20260808-01", text)
        self.assertIn("HIGODOT_PRODUCTION_EXECUTION_PATH: PROVEN_TASK2_COMPLETED", text)
        self.assertIn("GENERAL_PRODUCT: BLOCKED", text)
        self.assertIn("NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED", text)


if __name__ == "__main__":
    unittest.main()
