from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_OWNER = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
AUTHORITY_INDEX = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
ENTRYPOINTS = [
    ROOT / "AGENTS.md",
    ROOT / "CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md",
    AUTHORITY_INDEX,
]

REQUIRED_OWNER = [
    "BS-ENHANCE-20260825-25",
    "BS-DAMAGE-20260825-26",
    "BS-CHRONICLE-20260825-27",
    "BS-ART-20260825-03",
    "SUCCESS_LEVEL_DELTA = +1",
    "+9 -> +10 = PRECISION_ENHANCEMENT",
    "NORMAL -> MINOR -> MAJOR -> DESTROYED",
    "TARGET <= +10: ENHANCEMENT_DAMAGE = 0",
    "TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE",
    "MONOTONIC_NON_DECREASING_DAMAGE_RISK",
    "CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE",
    "PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE",
    "ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE",
    "ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK",
]

REQUIRED_ENTRYPOINT = [
    "BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md",
    "BS-ENHANCE-20260825-25",
    "BS-DAMAGE-20260825-26",
    "BS-CHRONICLE-20260825-27",
    "BS-ART-20260825-03",
]

FORBIDDEN_CURRENT = [
    "CURRENT/MAX = CURRENT_DURABILITY_AUTHORITY",
    "PRECISION_MILESTONES = [10, 20, 30, 40, 50]",
]


def require_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{label} missing tokens: {missing}"


def main() -> None:
    assert CURRENT_OWNER.exists(), f"missing current owner: {CURRENT_OWNER.relative_to(ROOT)}"
    owner_text = CURRENT_OWNER.read_text(encoding="utf-8")
    require_tokens(owner_text, REQUIRED_OWNER, "current owner")

    for path in ENTRYPOINTS:
        text = path.read_text(encoding="utf-8")
        require_tokens(text, REQUIRED_ENTRYPOINT, path.name)
        stale = [token for token in FORBIDDEN_CURRENT if token in text]
        assert not stale, f"{path.name} keeps forbidden current tokens: {stale}"

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION" in agents
    assert "ART_STYLE_STATUS = REWORK_REQUIRED" not in agents

    # Post-merge fresh-read routing must not send a new session back into the
    # already-merged #207 synchronization workstream.
    handoff_text = HANDOFF.read_text(encoding="utf-8")
    assert "PR #207 = MERGED_TO_MAIN" in handoff_text
    assert "CURRENT_PLANNING_WORK = DAMAGE_PROBABILITY_CURVE" in handoff_text
    assert "Current task PR: `#207" not in handoff_text

    assert "POSTMERGE_PLANNING / DAMAGE_PROBABILITY_CURVE_NEXT" in agents

    authority_text = AUTHORITY_INDEX.read_text(encoding="utf-8")
    assert "1. DAMAGE_PROBABILITY_CURVE" in authority_text
    assert "CURRENT_CANON_MIGRATION = COMPLETE" in authority_text
    assert "CORE_SIMPLIFICATION_CANON_MIGRATION\n2. DAMAGE_PROBABILITY_CURVE" not in authority_text

    assert "GITHUB_CURRENT_CANON_SYNC = SYNCED" in owner_text
    assert "NOTION_CURRENT_CANON_SYNC = SYNCED" in owner_text
    assert "SHEET_SAME_ID_COMPATIBILITY = MIGRATION_ONLY / POSTMERGE_READBACK_PASS" in owner_text
    assert "GITHUB_CURRENT_CANON_SYNC = IN_PROGRESS_UNTIL_MERGE" not in owner_text

    print("core simplification current contract: PASS")


if __name__ == "__main__":
    main()
