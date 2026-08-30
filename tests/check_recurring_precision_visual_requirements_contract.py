#!/usr/bin/env python3
"""Protect the consumer-first art requirements for recurring Precision delivery."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "docs/planning/BLACKSMITH_RECURRING_PRECISION_VISUAL_REQUIREMENTS_20260830.json"
COVERAGE = ROOT / "docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json"
MANIFEST = ROOT / "assets/ASSET_MANIFEST.json"

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

APPROVED_ASSETS = {
    "VIS-REC-20260830-01": ("ASSET-MAIN-MENU-DAWN-BACKGROUND-V1", "assets/ui/workshop/main_menu_dawn_background_v1.png", "5870f6958135516b9d5f42f81e0d11e0724a5cbf27af9e3382f1de155a7f713a", "MenuIllustratedBackground"),
    "VIS-REC-20260830-02": ("ASSET-PRECISION-TAG-WORKSHOP-BACKGROUND-V1", "assets/ui/workshop/precision_tag_workshop_background_v1.png", "45679f660ad9fc24796e0080aded8474be6b0c462ae7bb2d58a91b6c0530ef32", "PrecisionIllustratedBackground"),
    "VIS-REC-20260830-03": ("ASSET-CUSTOMER-RESULT-RETURN-ILLUSTRATION-V1", "assets/ui/workshop/customer_result_return_illustration_v1.png", "716ce4dd4c6c4bdf48255c4b10aef906573d1113b331d20304e4f75f6e74eca1", "CustomerResultEventIllustration"),
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
        assert entry["candidate_status"] == "USER_APPROVED"
        assert entry["runtime_promotion_status"] == "IMPLEMENTED_MACHINE_VERIFIED"
        assert entry["generated_ui_screenshot"] is False
        receipt = entry["candidate_receipt"]
        assert receipt["source"] == "OpenAI ImageGen"
        assert receipt["pixel_dimensions"] == "941x1672"
        asset_id, asset_path, expected_hash, runtime_slot = APPROVED_ASSETS[consumer_id]
        assert receipt["repository_asset_path"] == asset_path
        assert receipt["review_status"] == "USER_APPROVED"
        binary = ROOT / asset_path
        assert binary.is_file(), f"missing approved runtime asset: {asset_path}"
        assert hashlib.sha256(binary.read_bytes()).hexdigest() == expected_hash

    main_menu = requirements["VIS-REC-20260830-01"]
    assert main_menu["rejected_candidate_receipts"][0]["reason"] == "TEXT_LIKE_HANGING_TAG_MARK"
    assert main_menu["candidate_receipt"]["sha256"] == "5870f6958135516b9d5f42f81e0d11e0724a5cbf27af9e3382f1de155a7f713a"

    customer_result = requirements["VIS-REC-20260830-03"]
    readability = customer_result["post_lock_readability_contract"]
    assert readability["required"] is True
    assert readability["native_layer_id"] == "CustomerResultReadabilityVeil"
    assert readability["candidate_background_layer"] == "BEHIND_NATIVE_RESULT_CONTROLS"
    assert readability["promotion_gate"] == "GUT_LAYER_ORDER_AND_GODOT_ANDROID_READABILITY_REVIEW"

    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    delivery = coverage["candidate_visual_delivery"]
    assert delivery["requirements_owner"] == "docs/planning/BLACKSMITH_RECURRING_PRECISION_VISUAL_REQUIREMENTS_20260830.json"
    assert delivery["status"] == "THREE_USER_APPROVED_RUNTIME_ASSETS_CANON_REGISTERED"
    assert delivery["runtime_promotion"] == "IMPLEMENTED_MACHINE_VERIFIED"
    assert delivery["flow_map"] == "TEXT_NATIVE_MERMAID_AND_TABLE_ONLY"
    recurring = next(entry for entry in coverage["screen_inventory"] if entry["screen_id"] == "RECURRING_PRECISION_TAG_CHOICE")
    assert recurring["coverage_status"] == "COVERED_APPROVED_RUNTIME_ASSET_MACHINE_VERIFIED"
    assert recurring["consumer_surface"] == EXPECTED["VIS-REC-20260830-02"]["implementation_owner_or_path"]

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = {entry["asset_id"]: entry for entry in manifest["asset_records"]}
    for consumer_id, (asset_id, asset_path, expected_hash, runtime_slot) in APPROVED_ASSETS.items():
        record = records[asset_id]
        assert record["status"] == "IMPLEMENTED_MACHINE_VERIFIED"
        assert record["tracked_asset_path"] == asset_path
        assert record["sha256"].lower() == expected_hash
        assert runtime_slot in record["runtime_slot"]
        assert record["approval_reference"] == "User 2026-08-30: 승인"

    print("recurring precision visual requirements contract: PASS")


if __name__ == "__main__":
    main()
