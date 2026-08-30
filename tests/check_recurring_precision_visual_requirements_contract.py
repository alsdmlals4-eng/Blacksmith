#!/usr/bin/env python3
"""Protect the consumer-first art requirements for recurring Precision delivery."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "docs/planning/BLACKSMITH_RECURRING_PRECISION_VISUAL_REQUIREMENTS_20260830.json"
COVERAGE = ROOT / "docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json"

EXPECTED = {
    "VIS-REC-20260830-01": {
        "consumer_surface": "MAIN_MENU",
        "runtime_asset_role": "SCREEN_BACKGROUND",
        "implementation_owner_or_path": "res://scenes/vertical_slice/main_menu.tscn#MenuIllustratedBackground",
        "target_aspect_resolution": "9:16 / 941x1672 PNG",
        "fallback_if_unconsumed": "KEEP_ASSET-WORKSHOP-BACKGROUND-V2 / DEFER",
    },
    "VIS-REC-20260830-02": {
        "consumer_surface": "WORKSHOP_RECURRING_PRECISION",
        "runtime_asset_role": "STATE_BACKGROUND_ILLUSTRATION",
        "implementation_owner_or_path": "res://scripts/vertical_slice/ui/vs_workshop_screen.gd#recurring_precision_state",
        "target_aspect_resolution": "9:16 / 941x1672 PNG",
        "fallback_if_unconsumed": "KEEP_ASSET-WORKSHOP-BACKGROUND-V2 / DEFER",
    },
    "VIS-REC-20260830-03": {
        "consumer_surface": "CUSTOMER_WORLD_RESULT",
        "runtime_asset_role": "EVENT_ILLUSTRATION",
        "implementation_owner_or_path": "res://scenes/vertical_slice/screens/vs_customer_result_screen.tscn",
        "target_aspect_resolution": "9:16 / 941x1672 PNG",
        "fallback_if_unconsumed": "KEEP_NATIVE_COLORRECT_LABEL_COMPOSITION / DEFER",
    },
}


def main() -> None:
    assert REQUIREMENTS.is_file(), "missing consumer-first recurring Precision visual requirements"
    payload = json.loads(REQUIREMENTS.read_text(encoding="utf-8"))
    assert payload["status"] == "CURRENT_CONSUMER_FIRST_VISUAL_REQUIREMENTS"
    assert payload["art_direction"] == "ILLUSTRATED_WORKSHOP_BOOK"
    assert payload["post_generation_user_lock"] == "REQUIRED_FOR_FINAL_DIRECTION_OR_RUNTIME_PROMOTION"
    assert payload["flow_map"] == {
        "format": "TEXT_NATIVE_MERMAID_AND_TABLE",
        "raster_generation": "PROHIBITED",
    }

    requirements = {entry["consumer_id"]: entry for entry in payload["visual_requirements"]}
    assert set(requirements) == set(EXPECTED)
    for consumer_id, expected in EXPECTED.items():
        entry = requirements[consumer_id]
        for key, value in expected.items():
            assert entry[key] == value, f"{consumer_id}.{key} drifted"
        assert entry["primary_use"], f"{consumer_id} must name its player value"
        assert entry["state_family_requirement"], f"{consumer_id} must declare its state family"
        assert entry["candidate_status"] in {"BRIEF_READY", "GENERATED_CANDIDATE", "REVIEWED"}
        assert entry["runtime_promotion_status"] == "BLOCKED_PENDING_USER_LOCK"
        assert entry["generated_ui_screenshot"] is False

    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    delivery = coverage["candidate_visual_delivery"]
    assert delivery["requirements_owner"] == "docs/planning/BLACKSMITH_RECURRING_PRECISION_VISUAL_REQUIREMENTS_20260830.json"
    assert delivery["status"] == "THREE_GENERATED_CANDIDATES_AWAITING_USER_LOCK"
    assert delivery["runtime_promotion"] == "BLOCKED_PENDING_USER_LOCK"
    assert delivery["flow_map"] == "TEXT_NATIVE_MERMAID_AND_TABLE_ONLY"
    recurring = next(entry for entry in coverage["screen_inventory"] if entry["screen_id"] == "RECURRING_PRECISION_TAG_CHOICE")
    assert recurring["coverage_status"] == "NATIVE_STATE_IMPLEMENTED_CANDIDATE_ART_PENDING_USER_LOCK"
    assert recurring["consumer_surface"] == EXPECTED["VIS-REC-20260830-02"]["implementation_owner_or_path"]

    print("recurring precision visual requirements contract: PASS")


if __name__ == "__main__":
    main()
