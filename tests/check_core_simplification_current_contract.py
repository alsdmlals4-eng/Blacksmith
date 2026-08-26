import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_OWNER = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
AUTHORITY_INDEX = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
DAMAGE_CURVE = ROOT / "docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json"
DAMAGE_DECISION = ROOT / "docs/decisions/BS-DAMAGE-20260826-28_DAMAGE_PROBABILITY_CURVE.md"
ENTRYPOINTS = [
    ROOT / "AGENTS.md",
    ROOT / "CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md",
    AUTHORITY_INDEX,
]

REQUIRED_OWNER = [
    "BS-ENHANCE-20260825-25",
    "BS-DAMAGE-20260825-26",
    "BS-DAMAGE-20260826-28",
    "BS-CHRONICLE-20260825-27",
    "BS-ART-20260825-03",
    "SUCCESS_LEVEL_DELTA = +1",
    "+9 -> +10 = PRECISION_ENHANCEMENT",
    "NORMAL -> MINOR -> MAJOR -> DESTROYED",
    "TARGET <= +10: ENHANCEMENT_DAMAGE = 0",
    "TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE",
    "MONOTONIC_NON_DECREASING_DAMAGE_RISK",
    "DAMAGE_CURVE_ANCHORS_PERCENT = [11:5, 30:6, 60:7, 90:8, 100:10]",
    "DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS",
    "CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE",
    "PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE",
    "ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE",
    "ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK",
]

REQUIRED_ENTRYPOINT = [
    "BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md",
    "BS-ENHANCE-20260825-25",
    "BS-DAMAGE-20260825-26",
    "BS-DAMAGE-20260826-28",
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


def damage_percent_at(target: int, anchors: list[dict[str, int]]) -> Fraction:
    if target <= 10:
        return Fraction(0)
    for left, right in zip(anchors, anchors[1:]):
        a = int(left["target"])
        b = int(right["target"])
        if a <= target <= b:
            pa = Fraction(int(left["percent"]))
            pb = Fraction(int(right["percent"]))
            return pa + (pb - pa) * Fraction(target - a, b - a)
    raise AssertionError(f"target outside approved curve: {target}")


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
    assert "CURRENT_PLANNING_WORK = FOUR_STATE_REPAIR_MODEL + MAJOR_ENHANCEMENT_ELIGIBILITY" in handoff_text
    assert "Current task PR: `#207" not in handoff_text

    assert "POSTMERGE_PLANNING / FOUR_STATE_REPAIR_MODEL_NEXT" in agents
    assert "USER_SUPPLIED_V4_8_R5_4_SUPERSET_FINAL_CURRENT" in agents
    assert "PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.8-r5.4_SUPERSET_FINAL_20260826.md" in agents
    assert "USER_SUPPLIED_V4_8_R4_CURRENT" not in agents

    authority_text = AUTHORITY_INDEX.read_text(encoding="utf-8")
    assert "1. MINOR_MAJOR_REPAIR_MODEL + MAJOR_ENHANCEMENT_ELIGIBILITY" in authority_text
    assert "DAMAGE_PROBABILITY_CURVE = USER_APPROVED / BS-DAMAGE-20260826-28" in authority_text
    assert "DAMAGE_CURVE_NUMBERS = USER_APPROVED" in authority_text
    assert "DAMAGE_CURVE_NUMBERS = NOT_FINAL / USER_APPROVAL_REQUIRED" not in authority_text

    assert DAMAGE_DECISION.exists(), "missing Decision28 damage curve decision record"
    decision_text = DAMAGE_DECISION.read_text(encoding="utf-8")
    require_tokens(
        decision_text,
        [
            "BS-DAMAGE-20260826-28",
            "P(DAMAGE_ADVANCE | ENHANCEMENT_FAILURE, TARGET_LEVEL)",
            "5% / 6% / 7% / 8% / 10%",
            "PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS",
            "FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED_BY_THIS_DECISION",
            "RUNTIME_IMPLEMENTATION = BLOCKED / NOT_RUN",
        ],
        "Decision28",
    )

    assert DAMAGE_CURVE.exists(), "missing machine-readable damage curve"
    curve = json.loads(DAMAGE_CURVE.read_text(encoding="utf-8"))
    assert curve["decision_id"] == "BS-DAMAGE-20260826-28"
    assert curve["status"] == "USER_APPROVED_PLANNING_CANON"
    assert curve["probability_basis"] == "P(DAMAGE_ADVANCE | ENHANCEMENT_FAILURE, TARGET_LEVEL)"
    assert curve["safe_through_target"] == 10
    assert curve["target_min"] == 11
    assert curve["target_max"] == 100
    assert curve["interpolation"] == "PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS"
    assert curve["rounding_authority"] == "NONE_CANON_EXACT_UI_ROUNDING_NOT_DECIDED"
    assert curve["damage_advance_steps"] == 1
    assert curve["failure_consequence_composition"] == "NOT_DECIDED_BY_THIS_DECISION"
    assert curve["runtime_implementation"] == "BLOCKED_NOT_RUN"

    anchors = curve["anchors_percent"]
    assert anchors == [
        {"target": 11, "percent": 5},
        {"target": 30, "percent": 6},
        {"target": 60, "percent": 7},
        {"target": 90, "percent": 8},
        {"target": 100, "percent": 10},
    ]
    values = [damage_percent_at(target, anchors) for target in range(11, 101)]
    assert all(value > 0 for value in values)
    assert all(left <= right for left, right in zip(values, values[1:]))
    assert damage_percent_at(11, anchors) == 5
    assert damage_percent_at(30, anchors) == 6
    assert damage_percent_at(60, anchors) == 7
    assert damage_percent_at(90, anchors) == 8
    assert damage_percent_at(100, anchors) == 10

    assert "GITHUB_CURRENT_CANON_SYNC = SYNCED" in owner_text
    assert "NOTION_CURRENT_CANON_SYNC = SYNCED" in owner_text
    assert "SHEET_SAME_ID_COMPATIBILITY = MIGRATION_ONLY / POSTMERGE_READBACK_PASS" in owner_text
    assert "GITHUB_CURRENT_CANON_SYNC = IN_PROGRESS_UNTIL_MERGE" not in owner_text

    print("core simplification current contract: PASS")


if __name__ == "__main__":
    main()
