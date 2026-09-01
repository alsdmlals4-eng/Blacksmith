#!/usr/bin/env python3
"""Guard the Phase 1 mobile workshop blueprint as a non-runtime, canon-linked design artifact."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "docs/superpowers/specs/2026-09-01-phase1-workshop-blueprint-design.md"
RECEIPT = ROOT / "docs/operations/receipts/2026-09-01-phase1-workshop-blueprint.json"


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{path.name}: missing {missing}"


def main() -> None:
    require_tokens(
        BLUEPRINT,
        (
            "STATUS = USER_APPROVED_DIRECTION / WRITTEN_SPEC_REVIEW_PENDING",
            "ARTIFACT_CLASS = IMPLEMENTATION_BLUEPRINT_CANDIDATE / NON_RUNTIME",
            "NO_CANON_OWNER_REPLACEMENT = TRUE",
            "NO_RUNTIME_OR_ASSET_PROMOTION = TRUE",
            "BS-ENHANCE-20260901-40",
            "PRECISION_TARGETS = [10,20,30,40,50,60,70,80,90,100]",
            "불의 심장",
            "대지의 결정",
            "NO_NEW_PRECISION_WORKSHOP_BACKGROUND = TRUE",
            "NO_NEW_CATALYST_RASTER_ASSET = TRUE",
            "GENERATED_UI_SCREENSHOT_AS_PRODUCT_ASSET = FALSE",
            "TEXT_NATIVE_FLOW_MAP = MERMAID",
            "ADOPT",
            "ADAPT",
            "REJECT",
            "godot_runtime = NOT_RUN",
            "android_device = NOT_RUN",
            "human_player_experience = NOT_RUN",
            "WRITTEN_SPEC_USER_REVIEW_REQUIRED_BEFORE_IMPLEMENTATION = TRUE",
        ),
    )
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert payload["receipt_id"] == "BLACKSMITH_PHASE1_WORKSHOP_BLUEPRINT_20260901"
    assert payload["status"] == "MACHINE_AND_RUNTIME_VERIFIED_LOCAL"
    assert payload["change_boundary"]["protected_product_paths_changed"] is True
    assert payload["change_boundary"]["changed_product_paths"] == [
        "scripts/vertical_slice/ui/vs_workshop_screen.gd"
    ]
    assert payload["change_boundary"]["new_raster_asset_created"] is False
    assert payload["evidence_ceiling"]["godot_runtime"] == "RUNTIME_VERIFIED_ISOLATED_WINDOWS_CAPTURE"
    assert payload["evidence_ceiling"]["human_player_experience"] == "NOT_RUN"
    runtime_capture = payload["runtime_capture"]
    assert runtime_capture["status"] == "RUNTIME_VERIFIED_ISOLATED_WINDOWS_CAPTURE"
    assert runtime_capture["capture_filename"] == "phase1-workshop-wireframe-decision-final.png"
    assert runtime_capture["capture_sha256"] == "A848B2C9A190348EB1E3F37FEB3A6A2B1553F6A7CE93007C25FAF8644D20F764"
    precision_capture = payload["precision_capture"]
    assert precision_capture["status"] == "RUNTIME_VERIFIED_ISOLATED_WINDOWS_CAPTURE"
    assert precision_capture["capture_filename"] == "phase1-workshop-wireframe-precision-final.png"
    assert precision_capture["capture_sha256"] == "3102B355CAA52231F05CE129AB4182F7EEE0ACCE93FAF9EEF0F16A3E138223B3"
    assert precision_capture["target_level"] == 10
    assert precision_capture["source_level"] == 9
    assert precision_capture["observed_catalysts"] == ["불의 심장", "대지의 결정"]
    print("phase1 workshop blueprint contract: PASS")


if __name__ == "__main__":
    main()
