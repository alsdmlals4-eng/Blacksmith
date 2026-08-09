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

    def test_default_product_exemption_remains_task1_only(self) -> None:
        workflow = (ROOT / ".github/workflows/validate-base-v9-adoption.yml").read_text(encoding="utf-8")
        self.assertIn("^(src/|scripts/|scenes/|data/|assets/|addons/|project", workflow)
        self.assertIn("^(scripts|data)/vertical_slice/", workflow)
        self.assertIn("protected-product-paths.txt", workflow)
        self.assertIn("Unapproved product paths changed", workflow)
        self.assertNotIn("^(scripts|scenes|data)/vertical_slice/", workflow)
        self.assertNotIn("^addons/.*", workflow)

    def test_toolchain_repair_exception_is_one_shot_and_exact(self) -> None:
        workflow = (ROOT / ".github/workflows/validate-base-v9-adoption.yml").read_text(encoding="utf-8")
        for token in (
            "BS-TOOLCHAIN-20260809-01",
            "pull_request.number == 138",
            "2dddf864519a557152c6bbf0f0ee7fb94eadf11c",
            "addons/hera_agent_godot/hera_agent_plugin.gd",
            "approved-toolchain-protected-paths.txt",
        ):
            self.assertIn(token, workflow)
        self.assertNotIn("addons/hera_agent_godot/.*", workflow)
        self.assertNotIn("addons/hera_agent_godot/", workflow.replace("addons/hera_agent_godot/hera_agent_plugin.gd", ""))


if __name__ == "__main__":
    unittest.main()
