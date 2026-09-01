from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
APP_SCENE = ROOT / "scenes" / "vertical_slice" / "vertical_slice_app.tscn"
APP_SCRIPT_UID = ROOT / "scripts" / "vertical_slice" / "ui" / "vs_app.gd.uid"
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PROTECTED_BASELINE = "48c73c37f5d8b7f3a436a51aeb96d78febd0fe02"
APPROVED_PATHS = (
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scripts/vertical_slice/resolvers/vs_repair_resolver.gd",
    "scripts/vertical_slice/ui/vs_app.gd",
    "scripts/vertical_slice/ui/vs_customer_result_screen.gd",
    "scripts/vertical_slice/ui/vs_main_menu.gd",
    "scripts/vertical_slice/ui/vs_workshop_screen.gd",
)

WARNING_SOURCE_FRAGMENTS: dict[Path, tuple[str, ...]] = {
    ROOT / "scripts" / "vertical_slice" / "ui" / "vs_customer_result_screen.gd": (
        "func _set_result_illustration_visible(visible: bool)",
    ),
    ROOT / "scripts" / "vertical_slice" / "resolvers" / "vs_repair_resolver.gd": (
        "var reference := int(R_BAND[band][material])",
    ),
    ROOT / "scripts" / "vertical_slice" / "ui" / "vs_workshop_screen.gd": (
        "func _set_decision_detail_labels_visible(is_visible: bool)",
        "WorkpieceDurabilityStateAtlasTexture.get_width() / 2)",
        "WorkpieceDurabilityStateAtlasTexture.get_height() / 2)",
    ),
    ROOT / "scripts" / "vertical_slice" / "ui" / "vs_app.gd": (
        "func _set_phase1_handoff_visibility(is_visible: bool)",
    ),
    ROOT / "scripts" / "vertical_slice" / "ui" / "vs_main_menu.gd": (
        "func _set_menu_visible(visible: bool)",
    ),
    ROOT / "tests" / "gut" / "unit" / "vertical_slice" / "test_vs_precision_tag_catalog.gd": (
        "var duplicate: Dictionary = resolver.selection_preview",
        "var duplicate: Dictionary = resolver.apply_selection_success",
    ),
}


def _script_uid_from_scene(scene_path: Path, script_path: str) -> str:
    scene_text = scene_path.read_text(encoding="utf-8")
    match = re.search(
        rf'\[ext_resource type="Script" uid="(?P<uid>uid://[^"]+)" path="{re.escape(script_path)}"',
        scene_text,
    )
    if match is None:
        raise AssertionError(f"No Script ExtResource found for {script_path}")
    return match.group("uid")


class GodotWarningHygieneTests(unittest.TestCase):
    def test_one_shot_protected_change_approval_covers_exact_warning_hygiene_paths(self) -> None:
        approval = json.loads(APPROVAL.read_text(encoding="utf-8"))

        self.assertEqual("PROJECT_PROTECTED_CHANGE_APPROVAL", approval["artifact_role"])
        self.assertEqual("APPROVED", approval["status"])
        self.assertEqual(PROTECTED_BASELINE, approval["protected_base_commit"])
        self.assertEqual(list(APPROVED_PATHS), approval["approved_paths"])

    def test_vertical_slice_app_script_uid_matches_the_script_sidecar(self) -> None:
        self.assertEqual(
            _script_uid_from_scene(APP_SCENE, "res://scripts/vertical_slice/ui/vs_app.gd"),
            APP_SCRIPT_UID.read_text(encoding="utf-8").strip(),
        )

    def test_known_gdscript_warning_sources_are_absent(self) -> None:
        for path, fragments in WARNING_SOURCE_FRAGMENTS.items():
            source = path.read_text(encoding="utf-8")
            for fragment in fragments:
                with self.subTest(path=path.relative_to(ROOT), fragment=fragment):
                    self.assertNotIn(fragment, source)
