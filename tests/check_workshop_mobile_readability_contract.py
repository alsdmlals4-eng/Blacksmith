#!/usr/bin/env python3
"""Protect the approved workshop flow from sub-mobile-size interactive controls."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "project.godot"
WORKSHOP = ROOT / "scripts/vertical_slice/ui/vs_workshop_screen.gd"


def constant_value(source: str, name: str) -> int:
    match = re.search(rf"const {name} := (\d+)", source)
    assert match, f"missing workshop mobile token: {name}"
    return int(match.group(1))


def main() -> None:
    project_text = PROJECT.read_text(encoding="utf-8")
    workshop_text = WORKSHOP.read_text(encoding="utf-8")

    viewport_width = int(re.search(r"window/size/viewport_width=(\d+)", project_text).group(1))
    output_width = int(re.search(r"window/size/window_width_override=(\d+)", project_text).group(1))
    assert viewport_width == 720 and output_width == 360
    assert viewport_width // output_width == 2, "the mobile preview must retain its documented 2x scale"

    assert constant_value(workshop_text, "MOBILE_BODY_FONT_SIZE") == 28
    assert constant_value(workshop_text, "MOBILE_SECTION_FONT_SIZE") == 35
    assert constant_value(workshop_text, "MOBILE_TITLE_FONT_SIZE") == 44
    assert constant_value(workshop_text, "MOBILE_TOUCH_TARGET_HEIGHT") == 96
    assert constant_value(workshop_text, "MOBILE_PRIMARY_TOUCH_TARGET_HEIGHT") == 112
    assert "func _apply_mobile_readability_tokens() -> void:" in workshop_text
    assert "_apply_mobile_readability_tokens()" in workshop_text.split("func _ready() -> void:", 1)[1].split("func _ensure_scrollable_layout", 1)[0]
    assert "_apply_font_size_to_controls(MOBILE_TITLE_CONTROL_PATHS, MOBILE_TITLE_FONT_SIZE)" in workshop_text
    assert "_apply_font_size_to_controls(MOBILE_SECTION_CONTROL_PATHS, MOBILE_SECTION_FONT_SIZE)" in workshop_text
    assert "_apply_font_size_to_controls(MOBILE_BODY_CONTROL_PATHS, MOBILE_BODY_FONT_SIZE)" in workshop_text
    assert "_apply_minimum_height_to_controls(MOBILE_ACTION_CONTROL_PATHS, MOBILE_TOUCH_TARGET_HEIGHT)" in workshop_text
    assert "_apply_minimum_height_to_controls(MOBILE_PRIMARY_ACTION_CONTROL_PATHS, MOBILE_PRIMARY_TOUCH_TARGET_HEIGHT)" in workshop_text

    required_controls = {
        "RepairButton",
        "PrecisionActionAddButton",
        "PrecisionActionUpgradeButton",
        "PrecisionTagOption",
        "PrecisionLineageOption",
        "PrecisionMethodOption",
        "PrecisionBackfillButton",
        "HandoffButton",
        "ChronicleButton",
    }
    for control_name in required_controls:
        assert control_name in workshop_text, f"mobile touch target missing: {control_name}"
    assert "const MOBILE_ACTION_CONTROL_PATHS := PackedStringArray" in workshop_text
    assert "EnhancementButton" in workshop_text
    assert "const MOBILE_PRIMARY_ACTION_CONTROL_PATHS := PackedStringArray" in workshop_text

    print("workshop mobile readability contract: PASS")


if __name__ == "__main__":
    main()
