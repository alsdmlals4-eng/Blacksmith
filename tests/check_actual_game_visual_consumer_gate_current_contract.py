#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-ART-20260826-04"
DECISION = ROOT / "docs/decisions/BS-ART-20260826-04_ACTUAL_GAME_IMAGE_CONSUMER_GATE.md"
MODEL = ROOT / "docs/planning/BLACKSMITH_ACTUAL_GAME_IMAGE_CONSUMER_GATE_20260826.json"
ROUTING = ROOT / "docs/decisions/BS-OPS-20260828-35_GITHUB_ONLY_CANON_AND_IMAGE_EXECUTION_ROUTING.md"
COVERAGE = ROOT / "docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json"
ART_OWNER = ROOT / "docs/planning/BLACKSMITH_ART_DIRECTION_REWORK_DECISION_20260825.md"
VISUAL_APPROVAL = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_ASSET_APPROVAL_2026-08-25.md"
CORE = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
AUTHORITY = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
AGENTS = ROOT / "AGENTS.md"


def require_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{label} missing tokens: {missing}"


def main() -> None:
    assert DECISION.exists(), f"missing visual consumer Decision: {DECISION.relative_to(ROOT)}"
    assert MODEL.exists(), f"missing visual consumer model: {MODEL.relative_to(ROOT)}"

    decision_text = DECISION.read_text(encoding="utf-8")
    require_tokens(
        decision_text,
        [
            DECISION_ID,
            "USER_APPROVED_PROJECT_VISUAL_DELIVERY_CANON",
            "ACTUAL_GAME_CONSUMER_REQUIRED = TRUE",
            "NEW_EXPLANATORY_GDD_SHEET_IMAGE_TARGET = FALSE",
            "GENERATED_UI_SCREENSHOT_MOCKUP_AS_PRODUCT_ASSET = FALSE",
            "FULL_FRAME_IMAGE_ALLOWED_ONLY_IF_RUNTIME_CONSUMES_FULL_FRAME = TRUE",
            "PRIMARY_USE_GATE_REQUIRED = TRUE",
            "NO_CONSUMER = CUT_OR_DEFER",
            "EXISTING_VISUAL_GDD_8 = HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY",
        ],
        "visual consumer Decision",
    )

    model = json.loads(MODEL.read_text(encoding="utf-8"))
    assert model["decision_id"] == DECISION_ID
    assert model["status"] == "USER_APPROVED_PROJECT_VISUAL_DELIVERY_CANON"
    assert model["actual_game_consumer_required"] is True
    assert model["new_explanatory_gdd_sheet_image_target"] is False
    assert model["generated_ui_screenshot_mockup_as_product_asset"] is False
    assert model["full_frame_image_allowed_only_if_runtime_consumes_full_frame"] is True
    assert model["primary_use_gate_required"] is True
    assert model["no_consumer_disposition"] == "CUT_OR_DEFER"
    assert model["existing_visual_gdd_8_status"] == "HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY"
    assert model["actual_runtime_consumption"] == "IMPLEMENTED_STATIC_BINDING_UNVERIFIED"
    assert model["current_coverage_record"] == "docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json"

    required = model["required_consumer_metadata"]
    assert required == [
        "consumer_id",
        "consumer_surface",
        "runtime_asset_role",
        "primary_use",
        "implementation_owner_or_path",
        "target_aspect_resolution",
        "state_family_requirement",
        "fallback_if_unconsumed",
    ]

    assert model["ui_layout_prototype_is_not_generated_raster_asset"] is True
    assert model["repository_structured_flow_may_use_text_tables_or_mermaid_not_generated_sheet"] is True
    assert model["image_generation_requires_separate_conversation_approval_gate"] is False
    assert model["image_generation_execution"] == "USER_PREAUTHORIZED_AFTER_CONSUMER_REQUIREMENT"
    assert model["post_generation_user_lock"] == "REQUIRED_FOR_FINAL_DIRECTION_OR_RUNTIME_PROMOTION"
    assert model["automatic_generation_from_candidate_consumer_list"] is False

    routing = ROUTING.read_text(encoding="utf-8")
    require_tokens(
        routing,
        [
            "BS-OPS-20260828-35",
            "GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE",
            "NOTION_STATUS = HISTORICAL_REFERENCE_ONLY / NO_FUTURE_READ_WRITE_REQUIRED",
            "IMAGE_GENERATION_EXECUTION = USER_PREAUTHORIZED_AFTER_CONSUMER_REQUIREMENT",
        ],
        "GitHub-only image routing",
    )

    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    for screen in coverage["screen_inventory"]:
        assert screen["notion_destination"] is None, screen["screen_id"]
        assert screen["repository_destination"], screen["screen_id"]

    for path in (ART_OWNER, VISUAL_APPROVAL, CORE, AUTHORITY, HANDOFF, AGENTS):
        text = path.read_text(encoding="utf-8")
        require_tokens(text, [DECISION_ID], path.name)

    handoff = HANDOFF.read_text(encoding="utf-8")
    require_tokens(
        handoff,
        [
            "GPT_WORK_PRIMARY_EXECUTION_SURFACE = GPT_WORK",
            "GPT_WORK_MEMORY_MODE = DEFAULT_MEMORY",
            "GPT_WORK_POLICY_OWNER = BASE_CURRENT",
            "PROJECT_CANON_AUTHORITY = UNCHANGED",
            "IMAGE_GOAL_QUEUE = READY_FOR_GPT_WORK",
            "IMG-01",
            "NORMAL_WORKPIECE_HERO_MASTER",
            "IMG-02",
            "IMG-03",
            "IMG-04",
            "IMG-05",
            "PRODUCT_IMAGE_ASSET_APPROVAL = 0",
            "IMPLEMENTATION_READY_IMAGE_ASSET = 0",
            "ACTUAL_RUNTIME_IMAGE_CONSUMPTION = 1 / LEGACY_RUNTIME_BOUND_UNVERIFIED",
            "RUNTIME_VERIFIED_IMAGE_ASSET = 0",
            "FRESH_READ_REQUIRED",
        ],
        "GPT Work handoff",
    )

    agents = AGENTS.read_text(encoding="utf-8")
    require_tokens(
        agents,
        [
            "ACTUAL_GAME_CONSUMER_REQUIRED",
            "NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE",
            "PRIMARY_USE_GATE_REQUIRED",
        ],
        "AGENTS visual gate",
    )

    print("actual game visual consumer gate current contract: PASS")


if __name__ == "__main__":
    main()
