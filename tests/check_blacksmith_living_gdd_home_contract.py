#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
DECISION = ROOT / "docs/operations/BS-OPS-20260825-03_BLACKSMITH_LIVING_GDD_HOME.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-25-blacksmith-living-gdd-home-design.md"
VISUAL_APPROVAL = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_ASSET_APPROVAL_2026-08-25.md"

AGENTS_TOKENS = (
    "BS-OPS-20260825-03",
    "HUMAN_PROJECT_HOME_IS_LIVING_GDD_VISUAL_DASHBOARD",
    "HUMAN_RELEVANT_PROJECT_OUTPUTS_VIEWABLE_FROM_HOME",
    "EXPLANATORY_VISUAL_GDD_BEFORE_DECORATIVE_ART = HISTORICAL_PRE_DECISION04",
    "BS-ART-20260825-03",
    "BS-ART-20260826-04",
    "ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK",
    "ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION",
    "ACTUAL_GAME_CONSUMER_REQUIRED",
    "NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE",
    "PRIMARY_USE_GATE_REQUIRED",
    "HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY",
    "SYSTEM_SEMANTICS_STALE",
)

VISUAL_HISTORY_TOKENS = (
    "INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD",
    "EXISTING_VISUAL_GDD_8 = HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY",
    "FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED",
)

DECISION_TOKENS = (
    "BS-OPS-20260825-03",
    "HUMAN_PROJECT_HOME_IS_LIVING_GDD_VISUAL_DASHBOARD",
    "HUMAN_RELEVANT_PROJECT_OUTPUTS_VIEWABLE_FROM_HOME",
    "EXPLANATORY_VISUAL_GDD_BEFORE_DECORATIVE_ART",
    "STYLIZED_DARK_FORGE = CURRENT",
    "APPROVED_REPRESENTATIVE_VISUAL = NOT_AVAILABLE",
    "VISUAL_GDD_GAP = OPEN",
    "EXAMPLE_IMAGES = REFERENCE_ONLY_LAYOUT_DENSITY",
    "PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION",
)

SPEC_TOKENS = (
    "Project Living GDD + Visual Dashboard",
    "REFERENCE_ONLY for information density, layout, and Visual-GDD explanatory level",
    "no new image generation in this task",
    "TEST_BUDGET_NOT_FINAL",
)


def read(path: Path, failures: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        failures.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return ""


def require_tokens(label: str, text: str, tokens: tuple[str, ...], failures: list[str]) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{label} missing required token: {token}")


def main() -> int:
    failures: list[str] = []
    agents = read(AGENTS, failures)
    decision = read(DECISION, failures)
    spec = read(SPEC, failures)
    visual_history = read(VISUAL_APPROVAL, failures)

    require_tokens("AGENTS.md current visual contract", agents, AGENTS_TOKENS, failures)
    require_tokens("Visual GDD historical approval", visual_history, VISUAL_HISTORY_TOKENS, failures)
    require_tokens("Decision 03 historical snapshot", decision, DECISION_TOKENS, failures)
    require_tokens("Living GDD spec", spec, SPEC_TOKENS, failures)

    if failures:
        print("Blacksmith Living GDD Home contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Blacksmith Living GDD Home contract PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())