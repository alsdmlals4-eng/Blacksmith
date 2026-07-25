from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BASE_COMMIT = "6a224e450f9420223c00921f3c56e051612f92ad"


def load_checker():
    path = ROOT / "tools/check_archive_governance.py"
    spec = importlib.util.spec_from_file_location("blacksmith_archive_checker", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ArchiveRetentionGovernanceTests(unittest.TestCase):
    def test_current_repository_contract_passes(self) -> None:
        checker = load_checker()
        self.assertEqual([], checker.validate(ROOT))

    def test_shared_extension_pin_and_routes_match(self) -> None:
        routes = json.loads(
            (ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json").read_text(encoding="utf-8")
        )
        project_adapter = json.loads(
            (ROOT / "skills/PROJECT_BASE_SKILL_ADAPTER.json").read_text(encoding="utf-8")
        )
        archive_adapter = json.loads(
            (ROOT / "docs/archive/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8")
        )
        profile = json.loads(
            (ROOT / "docs/BASE_ADOPTION_PROFILE.json").read_text(encoding="utf-8")
        )
        self.assertEqual(EXPECTED_BASE_COMMIT, routes["base"]["commit"])
        self.assertEqual(EXPECTED_BASE_COMMIT, project_adapter["base"]["commit"])
        self.assertEqual(EXPECTED_BASE_COMMIT, archive_adapter["base"]["commit"])
        self.assertEqual(EXPECTED_BASE_COMMIT, profile["shared_extension_commit"])
        self.assertEqual(
            "governing-legacy-retention-and-archives",
            routes["routes"]["legacy_retention_and_archives"]["skill_id"],
        )
        self.assertEqual(
            "docs/archive/ARCHIVE_RETENTION_ADAPTER.json",
            routes["routes"]["legacy_retention_and_archives"]["adapter"],
        )

    def test_archive_policy_forbids_blank_files_and_secrets(self) -> None:
        adapter = json.loads(
            (ROOT / "docs/archive/ARCHIVE_RETENTION_ADAPTER.json").read_text(encoding="utf-8")
        )
        self.assertTrue(adapter["policies"]["preserve_original_content"])
        self.assertFalse(adapter["policies"]["blank_placeholders_allowed"])
        self.assertFalse(adapter["policies"]["secrets_may_be_archived"])
        self.assertFalse(adapter["policies"]["default_active_authority"])
        self.assertEqual("NONE", adapter["policies"]["default_implementation_authority"])

    def test_base_shared_skill_body_is_not_copied(self) -> None:
        self.assertFalse(
            (ROOT / "skills/governing-legacy-retention-and-archives/SKILL.md").exists()
        )

    def test_archive_readme_declares_non_authority_and_preservation(self) -> None:
        text = (ROOT / "docs/archive/README.md").read_text(encoding="utf-8")
        for token in (
            "현재 정본이 아니며 구현 권한이 없다",
            "원문을 비우지 않는다",
            "비밀키",
            "기존 구형 자료를 이동·삭제·재작성하지 않는다",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
