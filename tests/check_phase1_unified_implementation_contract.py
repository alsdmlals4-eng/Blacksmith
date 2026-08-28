from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md"
CORE_CANON = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"


def require_tokens(tokens: tuple[str, ...]) -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{CONTRACT.name}: missing {missing}"


def main() -> None:
    require_tokens(
        (
            "CONTRACT_STATUS = PHASE_1_APPROVED_PLAN / IMPLEMENTATION_NOT_YET_AUTHORIZED",
            "PRIMARY_PLAYABLE_CONTENT = REPEATED_ENHANCEMENT_JUDGMENT_AND_FEEDBACK",
            "PHASE_1_SLICE = +0_TO_+10 / +11_TO_+15 / ONE_SAME_UID_RESULT",
            "CRAFT_FEEDBACK_MILESTONE = EVERY_5_LEVELS",
            "+5 = PRESENTATION_ONLY",
            "+10 = PRESENTATION_PLUS_ONLY_PRECISION_AND_ONE_KEYWORD",
            "NO_PRECISION_OR_AFFIX_OR_PROBABILITY_OR_RESOURCE_RULE_AT_+20_OR_LATER",
            "RETURN_BEAT = ONE_NON_ECONOMIC_WORKSHOP_MOMENT",
            "NO_TIMER / NO_CUSTOMER_MANAGEMENT / NO_SECOND_ITEM / NO_FAKE_DAMAGE",
            "IMPLEMENTATION_DRIFT = LEGACY_MULTI_PRECISION_DATA_AND_NON_VERTICAL_SLICE_MODULES",
            "INCIDENT_ID = BS-OPS-20260828-37",
            "NO_BASE_PROMOTION = PROJECT_SPECIFIC_LEGACY_AND_SLICE_BOUNDARY",
            "P0_IMPLEMENTATION_GUARD = VERTICAL_SLICE_ONLY_CURRENT_CANON",
            "OUT_OF_SCOPE = NEW_ART_ASSET_BATCH / ECONOMY_REBALANCE / MULTI_CUSTOMER_SYSTEM / RELEASE_WORK",
            "TEST_ORDER = RED_CONTRACTS -> GREEN_MINIMUM_FLOW -> REFACTOR_LEGACY_BOUNDARIES",
            "HUMAN_PLAYTEST = REQUIRED_AFTER_AUTOMATED_GREEN",
            "PHASE_2_ENTRY_REQUIRES = USER_PLANNING_COMPLETE_DECLARATION",
        )
    )
    locator = "BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md"
    assert locator in CORE_CANON.read_text(encoding="utf-8"), "core canon must locate the unified contract"
    assert locator in HANDOFF.read_text(encoding="utf-8"), "handoff must locate the unified contract"
    print("phase1 unified implementation contract: PASS")


if __name__ == "__main__":
    main()
