from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "project.godot"
MAIN_MENU = ROOT / "scenes/vertical_slice/main_menu.tscn"
APP_SCENE = ROOT / "scenes/vertical_slice/vertical_slice_app.tscn"
WORKSHOP = ROOT / "scenes/vertical_slice/screens/vs_workshop_screen.tscn"
MENU_SCRIPT = ROOT / "scripts/vertical_slice/ui/vs_main_menu.gd"
APP_SCRIPT = ROOT / "scripts/vertical_slice/ui/vs_app.gd"


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

    def test_task2_does_not_enable_hera(self) -> None:
        text = PROJECT.read_text(encoding="utf-8")
        self.assertNotIn("addons/hera_agent_godot/plugin.cfg", text)

    def test_task2_uses_no_external_product_assets(self) -> None:
        for path in [MAIN_MENU, APP_SCENE, WORKSHOP]:
            self.assertTrue(path.is_file(), str(path))
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("res://assets/", text)

    def test_project_mobile_baseline_is_preserved(self) -> None:
        text = PROJECT.read_text(encoding="utf-8")
        self.assertIn("window/size/viewport_width=720", text)
        self.assertIn("window/size/viewport_height=1280", text)
        self.assertIn("window/handheld/orientation=1", text)


if __name__ == "__main__":
    unittest.main()
