import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_OWNER = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
AUTHORITY_INDEX = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
DAMAGE_CURVE = ROOT / "docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json"
DAMAGE_DECISION = ROOT / "docs/decisions/BS-DAMAGE-20260826-28_DAMAGE_PROBABILITY_CURVE.md"
DURABILITY_MODEL = ROOT / "docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json"
DURABILITY_DECISION = ROOT / "docs/decisions/BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md"
CUSTOMER_DAMAGE_MODEL = ROOT / "docs/planning/BLACKSMITH_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY_20260826.json"
VISUAL_CONSUMER_MODEL = ROOT / "docs/planning/BLACKSMITH_ACTUAL_GAME_IMAGE_CONSUMER_GATE_20260826.json"
WEAPON_KEYWORD_DECISION = ROOT / "docs/decisions/BS-ENHANCE-20260828-34_WEAPON_KEYWORD_OWNERSHIP.md"
PRECISION_TAG_DECISION = ROOT / "docs/decisions/BS-ENHANCE-20260829-37_PRECISION_TAG_CATALOG_AND_SELECTION_GATE.md"
CURRENT_STATUS_DECISIONS = [
    ROOT / "docs/decisions/BS-DAMAGE-20260826-28_DAMAGE_PROBABILITY_CURVE.md",
    ROOT / "docs/decisions/BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md",
    ROOT / "docs/decisions/BS-DAMAGE-20260826-30_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY.md",
    ROOT / "docs/decisions/BS-REPAIR-20260826-31_REPAIR_ECONOMY_REBASE_AND_SENSITIVITY.md",
    ROOT / "docs/decisions/BS-ART-20260826-04_ACTUAL_GAME_IMAGE_CONSUMER_GATE.md",
]
ENTRYPOINTS = [
    ROOT / "AGENTS.md",
    ROOT / "CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md",
    AUTHORITY_INDEX,
]

REQUIRED_OWNER = [
    "BS-ENHANCE-20260825-25",
    "BS-DAMAGE-20260825-26",
    "BS-DAMAGE-20260826-28",
    "BS-REPAIR-20260826-29",
    "BS-REPAIR-20260826-31",
    "BS-ENHANCE-20260826-32",
    "BS-DAMAGE-20260826-30",
    "BS-CHRONICLE-20260825-27",
    "BS-ART-20260825-03",
    "BS-ART-20260826-04",
    "BS-ENHANCE-20260828-34",
    "BS-ENHANCE-20260829-37",
    "BS-ENHANCE-20260830-38",
    "SUCCESS_LEVEL_DELTA = +1",
    "+9 -> +10 = PRECISION_ENHANCEMENT",
    "ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY",
    "PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10",
    "DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC",
    "DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW",
    "EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)",
    "TARGET <= +10: ENHANCEMENT_DAMAGE = 0",
    "TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE",
    "DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS",
    "FAILURE_OUTCOMES = SUCCESS / FAILED_HOLD / FAILED_DAMAGE",
    "FAILED_DAMAGE_REPLACES_FAILED_HOLD = TRUE",
    "FAILURE_LEVEL_DOWNGRADE = FORBIDDEN",
    "FAILURE_SEPARATE_CRITICAL_OUTCOME = FORBIDDEN",
    "UI_OUTCOME_DISPLAY = FINAL_PER_ATTEMPT_ONE_DECIMAL_HALF_UP",
    "MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES",
    "PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE",
    "ACTUAL_ITEM_USE_REQUIRED = TRUE",
    "MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1",
    "WORLD_EVENT_MAX_DURABILITY_DAMAGE = FALSE",
    "ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE",
    "ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK",
    "ACTUAL_GAME_CONSUMER_REQUIRED = TRUE",
    "NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE",
]

REQUIRED_ENTRYPOINT = [
    "BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md",
    "BS-ENHANCE-20260825-25",
    "BS-DAMAGE-20260825-26",
    "BS-DAMAGE-20260826-28",
    "BS-REPAIR-20260826-29",
    "BS-REPAIR-20260826-31",
    "BS-ENHANCE-20260826-32",
    "BS-DAMAGE-20260826-30",
    "BS-CHRONICLE-20260825-27",
    "BS-ART-20260825-03",
    "BS-ART-20260826-04",
]

FORBIDDEN_CURRENT = [
    "CURRENT/MAX = CURRENT_DURABILITY_AUTHORITY",
    "PRECISION_MILESTONES = [10, 20, 30, 40, 50]",
    "POSTMERGE_PLANNING / FOUR_STATE_REPAIR_MODEL_NEXT",
    "POSTMERGE_PLANNING / CUSTOMER_EVENT_DAMAGE_POLICY_NEXT",
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


def round_half_up_tenth(percent: Fraction) -> Fraction:
    return Fraction(int(percent * 10 + Fraction(1, 2)), 10)


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
    assert "POSTMERGE_PLANNING / REPAIR_ECONOMY_HUMAN_PLAYTEST_AND_VISUAL_REQUIREMENT_NEXT" in agents
    assert "BS-REPAIR-20260826-31" in agents
    assert "ACTUAL_GAME_CONSUMER_REQUIRED" in agents
    assert "USER_SUPPLIED_V4_8_R5_4_SUPERSET_FINAL_CURRENT" in agents
    assert "성공 시 플레이어용 `ITEM_KEYWORD` 하나" not in agents
    assert "WEAPON_ITEM_KEYWORD" in agents

    handoff_text = HANDOFF.read_text(encoding="utf-8")
    assert "PR #207 = MERGED_TO_MAIN" in handoff_text
    assert "CURRENT_RUNTIME_FOLLOWUP = SELECT_NEXT_APPROVED_CURRENT_CANON_ISSUE / NO_SCOPE_AUTOMATICALLY_OPENED" in handoff_text
    assert "CURRENT_ACCEPTED_FRONTIER = ISSUE_326_PRECISION_TAG_CATALOG_MERGED_MAIN_7d12070f37b664cd07fd0e369ea0e0974e41b0eb" in handoff_text
    assert "BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md" in handoff_text
    assert "Product implementation: `CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826 / IMPLEMENTATION_AND_REVIEW_ALLOWED_WITHIN_APPROVED_SCOPE`" in handoff_text
    assert "ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY" in handoff_text
    assert "PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10" in handoff_text
    assert "BS-ENHANCE-20260828-34" in handoff_text
    assert "BS-REPAIR-20260826-31" in handoff_text
    assert "DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC" in handoff_text
    assert "EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)" in handoff_text
    assert "BS-DAMAGE-20260826-30" in handoff_text
    assert "BS-ART-20260826-04" in handoff_text
    assert "BS-ENHANCE-20260826-32" in handoff_text

    authority_text = AUTHORITY_INDEX.read_text(encoding="utf-8")
    assert "CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826" in authority_text
    assert "1. Execute the approved unified contract with RED -> GREEN -> REFACTOR" in authority_text
    assert "BS-ENHANCE-20260828-34" in authority_text
    assert "ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY" in authority_text
    assert "PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10" in authority_text
    assert "RECURRING_PRECISION_FIELD_OWNER = BS-ENHANCE-20260830-38" in authority_text
    assert "Decision34/37 = RESIDUAL_NON_CONFLICTING_HISTORICAL_EVIDENCE" in authority_text
    assert "KEYWORD_OWNERSHIP_FIELD_OWNER = BS-ENHANCE-20260828-34" not in authority_text
    assert "Decision34 overrides the Core Canon for keyword-ownership fields" not in authority_text
    assert "BS-REPAIR-20260826-31" in authority_text
    assert "REPAIR_ECONOMY = USER_APPROVED_TEST_CONTRACT / B65_DEFAULT_PLAYTEST_REQUIRED" in authority_text
    assert "DAMAGE_CURVE_NUMBERS = USER_APPROVED / BS-DAMAGE-20260826-28" in authority_text
    assert "DURABILITY_REPAIR_STRUCTURE = USER_APPROVED / BS-REPAIR-20260826-29" in authority_text
    assert "DURABILITY_REPAIR_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE" in authority_text
    assert "CUSTOMER_WORLD_EVENT_DAMAGE_POLICY = USER_APPROVED / BS-DAMAGE-20260826-30" in authority_text
    assert "VISUAL_DELIVERY_POLICY = USER_APPROVED / BS-ART-20260826-04" in authority_text

    for decision_path in CURRENT_STATUS_DECISIONS:
        decision_text = decision_path.read_text(encoding="utf-8")
        assert "CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826" in decision_text, (
            f"{decision_path.name} still lacks the current execution status"
        )
        assert "RUNTIME_IMPLEMENTATION = NOT_RUN / BLOCKED" not in decision_text, (
            f"{decision_path.name} still keeps a stale runtime block"
        )

    weapon_keyword_decision = WEAPON_KEYWORD_DECISION.read_text(encoding="utf-8")
    require_tokens(
        weapon_keyword_decision,
        [
            "STATUS = USER_APPROVED_CURRENT",
            "FIELD_OWNER = WEAPON_KEYWORD_OWNERSHIP",
            "ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY",
            "ITEM_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX",
            "PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10",
            "WEAPON_KEYWORD_CONTENT_ID = DATA_BACKED_FIRST_TAG_CATALOG / BS-ENHANCE-20260829-37",
            "CONTENT_AND_EMPTY_SELECTION_OWNER = BS-ENHANCE-20260829-37",
            "HISTORICAL_FIXTURE_OR_CUSTOMER_EPITHET_REUSE = FORBIDDEN",
        ],
        "Decision34",
    )
    precision_tag_text = PRECISION_TAG_DECISION.read_text(encoding="utf-8")
    require_tokens(
        precision_tag_text,
        [
            "STATUS = USER_APPROVED_CURRENT",
            "EMPTY_CATALYST_LINEAGE_BEHAVIOR = BLOCK_BEFORE_COST_OR_ROLL",
            "NO_DEFAULT_LINEAGE = TRUE",
            "PRECISION_SELECTION_PERSISTENCE = ATTEMPT_LOCAL_ONLY",
            "NO_NEW_STORED_FIELD_OR_FOURTH_AFFIX_SLOT = TRUE",
        ],
        "Decision37",
    )

    # Decision28 remains the exact target-level probability owner.
    assert DAMAGE_DECISION.exists(), "missing Decision28 damage curve decision record"
    decision_text = DAMAGE_DECISION.read_text(encoding="utf-8")
    require_tokens(
        decision_text,
        [
            "BS-DAMAGE-20260826-28",
            "P(DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)",
            "5% / 6% / 7% / 8% / 10%",
            "PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS",
            "FAILURE_CONSEQUENCE_COMPOSITION = USER_APPROVED_EXCLUSIVE_HOLD_OR_DAMAGE",
            "UI_DAMAGE_PERCENT_ROUNDING = USER_APPROVED_FINAL_OUTCOME_ONE_DECIMAL_HALF_UP",
            "DAMAGE_EVENT_CURRENT_LOSS = 1",
            "RUNTIME_IMPLEMENTATION = CURRENT_CANON_MVP_AUTHORIZED / EXACT_HEAD_CONTRACT_AND_TDD_REQUIRED",
        ],
        "Decision28",
    )

    curve = json.loads(DAMAGE_CURVE.read_text(encoding="utf-8"))
    assert curve["decision_id"] == "BS-DAMAGE-20260826-28"
    assert curve["status"] == "USER_APPROVED_PLANNING_CANON"
    assert curve["probability_basis"] == "P(DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)"
    assert curve["safe_through_target"] == 10
    assert curve["target_min"] == 11
    assert curve["target_max"] == 100
    assert curve["interpolation"] == "PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS"
    assert curve["rounding_authority"] == "CANON_EXACT_UI_FINAL_OUTCOME_ONE_DECIMAL_HALF_UP"
    assert curve["damage_event_current_loss"] == 1
    assert curve["failure_consequence_composition"] == {
        "status": "USER_APPROVED_EXCLUSIVE_HOLD_OR_DAMAGE",
        "failed_outcomes": ["FAILED_HOLD", "FAILED_DAMAGE"],
        "damage_replaces_hold": True,
        "level_downgrade": "FORBIDDEN",
        "separate_critical_outcome": "FORBIDDEN",
        "attempt_cost": "CONSUMED_ON_ATTEMPT",
        "same_uid_recovery": "APPLIES_ON_FAILURE_PER_EXISTING_CONTRACT",
        "damage_current_loss": "DECISION29_CURRENT_MINUS_ONE_FLOOR_ZERO",
        "destroyed_state": "CURRENT_EQUALS_ZERO_DECISION29",
    }
    assert curve["ui_damage_percent_rounding"] == {
        "runtime_probability": "EXACT_NO_ROUNDING",
        "primary_outcome_display": "FINAL_PER_ATTEMPT_SUCCESS_FAILED_HOLD_FAILED_DAMAGE",
        "precision": "ONE_DECIMAL_PERCENT",
        "rounding": "HALF_UP",
        "hold_display": "100.0_MINUS_ROUNDED_SUCCESS_MINUS_ROUNDED_FAILED_DAMAGE",
        "conditional_damage_detail": "FAILURE_CONDITIONAL_PERCENT_ONE_DECIMAL_HALF_UP_WITH_EXACT_RESOLVER_SOURCE",
        "hard_guarantee": "SUCCESS_100.0_NO_FAILURE_OUTCOMES",
    }
    assert curve["runtime_implementation"] == "MVP_CORE_IMPLEMENTED_GODOT_GUT_VERIFIED_20260826"

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

    # Approved resolution: failure yields exactly one player-facing outcome.
    # At +11 NORMAL with a diagnostic 82% success rate, 18% failure and 5%
    # conditional damage become 82.0 / 17.1 / 0.9 final outcomes.
    final_success = Fraction(82)
    conditional_damage = Fraction(5, 100)
    failed_damage = (100 - final_success) * conditional_damage
    failed_hold = 100 - final_success - failed_damage
    shown_success = round_half_up_tenth(final_success)
    shown_damage = round_half_up_tenth(failed_damage)
    shown_hold = Fraction(100) - shown_success - shown_damage
    assert (shown_success, shown_hold, shown_damage) == (Fraction(82), Fraction(171, 10), Fraction(9, 10))
    assert shown_success + shown_hold + shown_damage == 100

    # Safe targets cannot yield failed damage; hard guarantee cannot yield any
    # failure result. Display rounding never feeds resolver probability.
    assert damage_percent_at(10, anchors) == 0
    assert round_half_up_tenth(Fraction(20)) == 20
    assert round_half_up_tenth(Fraction(0)) == 0
    assert (round_half_up_tenth(Fraction(100)), Fraction(0), Fraction(0)) == (100, 0, 0)

    # Decision29 owns the current visible numeric durability/repair architecture.
    assert DURABILITY_DECISION.exists(), "missing Decision29 durability decision"
    durability_text = DURABILITY_DECISION.read_text(encoding="utf-8")
    require_tokens(
        durability_text,
        [
            "BS-REPAIR-20260826-29",
            "USER_APPROVED_STRUCTURAL_CANON",
            "DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC",
            "DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW",
            "EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)",
            "4/4 with BASE_MAX 5 = MINOR",
            "2/2 with BASE_MAX 5 = MAJOR",
            "MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES",
            "TEMP_TEST_BUDGET",
        ],
        "Decision29",
    )
    durability = json.loads(DURABILITY_MODEL.read_text(encoding="utf-8"))
    assert durability["decision_id"] == "BS-REPAIR-20260826-29"
    assert durability["authority"]["durability"] == "CURRENT_MAX_BASE_MAX_NUMERIC"
    assert durability["durability_state_derivation"]["effective_durability_ratio"] == "min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)"
    assert durability["major_enhancement_allowed"] is True
    assert durability["max_durability_recovery"] == "NOT_APPROVED"
    assert durability["runtime_implementation"] == "MVP_CORE_IMPLEMENTED_GODOT_GUT_VERIFIED_20260826"

    customer_damage = json.loads(CUSTOMER_DAMAGE_MODEL.read_text(encoding="utf-8"))
    assert customer_damage["decision_id"] == "BS-DAMAGE-20260826-30"
    assert customer_damage["actual_item_use_required"] is True
    assert customer_damage["max_damage_rolls_per_event_per_uid"] == 1
    assert customer_damage["world_event_max_durability_damage"] is False

    visual_consumer = json.loads(VISUAL_CONSUMER_MODEL.read_text(encoding="utf-8"))
    assert visual_consumer["decision_id"] == "BS-ART-20260826-04"
    assert visual_consumer["actual_game_consumer_required"] is True
    assert visual_consumer["new_explanatory_gdd_sheet_image_target"] is False

    print("core simplification current contract: PASS")


if __name__ == "__main__":
    main()
