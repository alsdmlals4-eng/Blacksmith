from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "project.godot"
AUTHORITY_POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
MAIN_MENU = ROOT / "scenes/vertical_slice/main_menu.tscn"
APP_SCENE = ROOT / "scenes/vertical_slice/vertical_slice_app.tscn"
WORKSHOP = ROOT / "scenes/vertical_slice/screens/vs_workshop_screen.tscn"
MENU_SCRIPT = ROOT / "scripts/vertical_slice/ui/vs_main_menu.gd"
APP_SCRIPT = ROOT / "scripts/vertical_slice/ui/vs_app.gd"
APPROVED_WORKSHOP_BACKGROUND = "res://assets/ui/workshop/workshop_enhancement_background_v1.png"


class VerticalSliceTask2AppShellContractTests(unittest.TestCase):
    def test_application_entry_is_vertical_slice_main_menu(self) -> None:
        text = PROJECT.read_text(encoding="utf-8")
        self.assertIn(
            'run/main_scene="res://scenes/vertical_slice/main_menu.tscn"',
            text,
        )

    def test_required_task2_runtime_files_exist(self) -> None:
        for path in [MAIN_MENU, APP_SCENE, WORKSHOP, MENU_SCRIPT, APP_SCRIPT]:
            self.assertTrue(path.is_file(), str(path))

    def test_task2_preserves_enabled_non_authoritative_hera(self) -> None:
        project_text = PROJECT.read_text(encoding="utf-8")
        policy = json.loads(AUTHORITY_POLICY.read_text(encoding="utf-8"))
        self.assertIn("addons/hera_agent_godot/plugin.cfg", project_text)
        self.assertTrue(policy["hera"]["project_plugin_enabled"])
        self.assertEqual(policy["hera"]["authoring_authority"], "NONE")
        self.assertEqual(
            policy["hera"]["serialized_mutation_permission"],
            "NONE_UNLESS_SEPARATELY_SCOPED",
        )
        self.assertEqual(
            policy["higodot"]["policy_role"],
            "SOLE_GODOT_AUTHORING_AUTHORITY",
        )

    def test_task2_uses_only_the_approved_workshop_background_as_a_scene_asset(self) -> None:
        self.assertTrue(MAIN_MENU.is_file(), str(MAIN_MENU))
        main_menu_text = MAIN_MENU.read_text(encoding="utf-8")
        self.assertIn(APPROVED_WORKSHOP_BACKGROUND, main_menu_text)
        self.assertIn('name="MenuIllustratedBackground"', main_menu_text)
        for path in [APP_SCENE, WORKSHOP]:
            self.assertTrue(path.is_file(), str(path))
            if path.is_file():
                self.assertNotIn("res://assets/", path.read_text(encoding="utf-8"))

    def test_project_mobile_baseline_is_preserved(self) -> None:
        text = PROJECT.read_text(encoding="utf-8")
        self.assertIn("window/size/viewport_width=720", text)
        self.assertIn("window/size/viewport_height=1280", text)
        self.assertIn("window/handheld/orientation=1", text)


if __name__ == "__main__":
    unittest.main()
