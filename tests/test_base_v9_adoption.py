from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BaseV9AdoptionTests(unittest.TestCase):
    def test_base_v9_adapter_and_android_boundary(self) -> None:
        data = json.loads((ROOT / "skills/BASE_V9_ADAPTER.json").read_text(encoding="utf-8"))
        self.assertEqual(data["base"]["release_commit"], "585a53a25be1b04c543196f5901551deb49c7691")
        self.assertFalse(data["base"]["copy_common_skill_bodies"])
        self.assertEqual(data["sheet"]["sync_status"], "SHEET_GITHUB_CONFLICT")
        self.assertEqual(data["maturity"]["level"], 2)
        self.assertEqual(data["validation"]["android_device"], "NOT_RUN")

    def test_adoption_contract_and_gates_exist(self) -> None:
        audit = (ROOT / "docs/BASE_V9_ADOPTION_AUDIT.md").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/validate-base-v9-adoption.yml").read_text(encoding="utf-8")
        for token in ("OPERATING_SYSTEM_ONLY", "ANDROID_VERTICAL_UI", "SAFE_AREA", "NOT_RUN"):
            self.assertIn(token, audit)
        self.assertIn("ci-gate", workflow)
        self.assertIn("adversarial-gate", workflow)

    def test_only_approved_vertical_slice_product_paths_are_exempt(self) -> None:
        workflow = (ROOT / ".github/workflows/validate-base-v9-adoption.yml").read_text(encoding="utf-8")
        self.assertIn("^(src/|scripts/|scenes/|data/|assets/|addons/|project", workflow)
        self.assertIn("^(scripts|scenes|data)/vertical_slice/", workflow)
        self.assertIn("protected-product-paths.txt", workflow)
        self.assertIn("Unapproved product paths changed", workflow)
        self.assertNotIn("grep -Ev '^vertical_slice/'", workflow)


if __name__ == "__main__":
    unittest.main()
