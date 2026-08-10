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

    def test_task2_higodot_exception_is_one_shot_blob_exact_and_decision_bound(self) -> None:
        workflow = (ROOT / ".github/workflows/validate-base-v9-adoption.yml").read_text(encoding="utf-8")
        for token in (
            "BS-HIGODOT-EXEC-20260808-01",
            "pull_request.number == 131",
            "c3d7f0cf0f5b3662803ae58b7176d8a996638c60",
            "feat/vertical-slice-task2-app-shell",
            "addons/godot_ai/handlers/project_handler.gd",
            "e3c2e4568a0d44cb621742241678814df90f31f5",
            "addons/godot_ai/plugin.gd",
            "e465cb9f308d3968252f08bf9e0a0a83a80b87bd",
            "approved-task2-higodot-protected-paths.txt",
        ):
            self.assertIn(token, workflow)
        self.assertNotIn("addons/godot_ai/.*", workflow)
        stripped = workflow.replace("addons/godot_ai/handlers/project_handler.gd", "").replace("addons/godot_ai/plugin.gd", "")
        self.assertNotIn("addons/godot_ai/", stripped)

    def test_task2_published_product_exception_is_exact_four_paths_and_blob_bound(self) -> None:
        workflow = (ROOT / ".github/workflows/validate-base-v9-adoption.yml").read_text(encoding="utf-8")
        expected = {
            "project.godot": "27372b3862207aab5942b7dcc71cfb4b74aa4b92",
            "scenes/vertical_slice/main_menu.tscn": "6a8d9c4340f7b134d16a1ee4d91c0f9751c4e926",
            "scenes/vertical_slice/vertical_slice_app.tscn": "bb7578a45bab294018ed6654ef9accfcde1b85e6",
            "scenes/vertical_slice/screens/vs_workshop_screen.tscn": "731445f7d35a46c92ab834a8d46c18ba7e5655e2",
        }
        self.assertIn("BS-HIGODOT-EXEC-20260808-01", workflow)
        self.assertIn("approved-task2-published-product-paths.txt", workflow)
        for path, blob in expected.items():
            self.assertIn(path, workflow)
            self.assertIn(blob, workflow)
        self.assertNotIn("scenes/vertical_slice/.*", workflow)
        self.assertNotIn("project.godot.*", workflow)


if __name__ == "__main__":
    unittest.main()
