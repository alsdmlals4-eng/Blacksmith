from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "docs" / "PLATFORM_RELEASE_AND_ASSET_RIGHTS_PROFILE.md"
ASSET_RECORD = ROOT / "docs" / "ASSET_RIGHTS_AND_PROVENANCE_RECORD.md"
RELEASE_PACK = ROOT / "docs" / "GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md"
AGENTS = ROOT / "AGENTS.md"

class ContractTests(unittest.TestCase):
    def test_required_documents_exist(self):
        for path in (PROFILE, ASSET_RECORD, RELEASE_PACK):
            self.assertTrue(path.is_file(), f"missing: {path}")

    def test_project_profile(self):
        text = PROFILE.read_text(encoding="utf-8")
        for token in ("LOWEST_VIABLE_RATING", "AVOID_ADULTS_ONLY", "Android", "Google_Play", "ALL_OR_12_CANDIDATE", "RELEASE_BLOCKED_UNVERIFIED", "target_audience", "ads/IAP", "PLATFORM_SUBMISSION_NOT_RUN", "LEGAL_REVIEW_NOT_PERFORMED"):
            self.assertIn(token, text)

    def test_asset_record(self):
        text = ASSET_RECORD.read_text(encoding="utf-8")
        for token in ("commercial_use", "distribution_in_game_build", "raw_source_redistribution", "license_version_or_terms_date", "reference_brief", "forbidden_expression", "final_asset_record", "reference_similarity_status", "secure_original_location", "MUSIC_SFX", "FONT", "CHARACTER_ILLUSTRATION", "MODEL_3D_ANIMATION", "PLUGIN_ASSET", "OPEN_SOURCE_LIBRARY", "AI_OUTPUT_MODEL_TERMS", "OUTSOURCING_CONTRACT", "VOICE_COMPOSER_TRANSLATOR_CONTRACT"):
            self.assertIn(token, text)

    def test_release_pack_and_routing(self):
        release = RELEASE_PACK.read_text(encoding="utf-8")
        agents = AGENTS.read_text(encoding="utf-8")
        for token in ("build_store_questionnaire_consistency", "asset_rights_coverage", "RELEASE_BLOCKED_UNVERIFIED", "Google_Play"):
            self.assertIn(token, release)
        for path in ("docs/PLATFORM_RELEASE_AND_ASSET_RIGHTS_PROFILE.md", "docs/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md", "docs/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md"):
            self.assertIn(path, agents)

if __name__ == "__main__":
    unittest.main()
