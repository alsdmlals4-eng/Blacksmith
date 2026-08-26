#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
OPS = ROOT / "docs/operations/BS-OPS-20260825-02_PLANNING_REACTIVATION_AND_HUMAN_AI_WORKSPACE_SPLIT.md"
FLOW = ROOT / "docs/planning/BLACKSMITH_HUMAN_GAME_FLOW_MAP_2026.md"


def require(text: str, token: str, failures: list[str], label: str) -> None:
    if token not in text:
        failures.append(f"{label} missing required token: {token}")


def main() -> int:
    failures: list[str] = []
    agents = AGENTS.read_text(encoding="utf-8")

    required_agents = [
        "CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md",
        "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md",
        "CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장",
        "BS-OPS-20260825-02",
        "BS-DAMAGE-20260826-28",
        "docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json",
        "BS-REPAIR-20260826-29",
        "docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json",
        "DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC",
        "POSTMERGE_PLANNING / CUSTOMER_EVENT_DAMAGE_POLICY_NEXT",
        "USER_SUPPLIED_V4_8_R5_4_SUPERSET_FINAL_CURRENT",
        "TRACKED_V4_5_R2_STALE_SUPERSEDED_DO_NOT_USE",
        "PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.8-r5.4_SUPERSET_FINAL_20260826.md",
        "Notion Project Home = HUMAN_PROJECT_HOME_IS_LIVING_GDD_VISUAL_DASHBOARD",
        "Project Registry / System Record = AI_OPERATIONAL_SURFACE",
        "Google Sheet = unique 미이관 자료와 same-ID compatibility mirror가 필요한 경우의 migration surface",
    ]
    for token in required_agents:
        require(agents, token, failures, "AGENTS.md")

    for stale in (
        "USER_SUPPLIED_V4_8_R4_CURRENT",
        "POSTMERGE_PLANNING / DAMAGE_PROBABILITY_CURVE_NEXT",
        "POSTMERGE_PLANNING / FOUR_STATE_REPAIR_MODEL_NEXT",
    ):
        if stale in agents:
            failures.append(f"AGENTS.md keeps stale current route: {stale}")

    overlay_pos = agents.find("CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md")
    legacy_pos = agents.find("CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장")
    if overlay_pos < 0 or legacy_pos < 0 or overlay_pos >= legacy_pos:
        failures.append("current overlay must precede the historical decision ledger in AGENTS authority order")

    if not OPS.exists():
        failures.append("missing BS-OPS-20260825-02 operational decision")
    else:
        ops = OPS.read_text(encoding="utf-8")
        for token in (
            "PLANNING_REACTIVATED",
            "#196 OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER",
            "Notion Project Home = human-facing game learning map",
            "Google Sheet = migration/compatibility surface",
        ):
            require(ops, token, failures, str(OPS.relative_to(ROOT)))

    if not FLOW.exists():
        failures.append("missing structured human game flow map")
    else:
        flow = FLOW.read_text(encoding="utf-8")
        for token in (
            "reinforcement tension + decision-driven design (DDD)",
            "STOP or PUSH?",
            "Human Project Home contract",
            "human usability / player experience: `NOT_RUN`",
        ):
            require(flow, token, failures, str(FLOW.relative_to(ROOT)))

    if failures:
        print("Current authority entrypoint contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Current authority entrypoint contract PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
