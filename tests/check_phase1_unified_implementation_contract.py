from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md"
CORE_CANON = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
WEAPON_KEYWORD_DECISION = ROOT / "docs/decisions/BS-ENHANCE-20260828-34_WEAPON_KEYWORD_OWNERSHIP.md"
HISTORICAL_PRECISION = ROOT / "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md"
HISTORICAL_CATALYST = ROOT / "docs/planning/BLACKSMITH_R2_CATALYST_AFFIX_SEED_EVOLUTION_AND_MUTATION_CANON_2026.md"
SUPERSEDED_INCIDENT = ROOT / "docs/operations/BS-INC-20260828-39_CATALYST_TAG_AND_PRECISION_METHOD_OWNERSHIP.md"
INCIDENT = ROOT / "docs/operations/BS-INC-20260828-40_CATALYST_METHOD_TAG_RESOLUTION.md"
RECURRING_PRECISION_DECISION = ROOT / "docs/decisions/BS-ENHANCE-20260830-38_RECURRING_PRECISION_TAG_EVOLUTION.md"
CONSUMABLE_CATALYST_DECISION = ROOT / "docs/decisions/BS-ENHANCE-20260901-40_CONSUMABLE_PRECISION_CATALYST_RESOURCES.md"


def require_tokens(tokens: tuple[str, ...]) -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{CONTRACT.name}: missing {missing}"


def main() -> None:
    require_tokens(
        (
            "CONTRACT_STATUS = CURRENT_CANON_MVP_IMPLEMENTATION_AUTHORIZED",
            "BS-ENHANCE-20260828-34",
            "ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY",
            "PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10",
            "WEAPON_KEYWORD_TAXONOMY = GRADE_KEYWORD / TAG_KEYWORD / EVENT_KEYWORD",
            "PRECISION_METHOD_EFFECT_SCOPE = WEAPON_STATS_DURABILITY_AND_TAG_RESOLUTION_CONTEXT",
            "PRECISION_METHOD_TAG_ROLE = TAG_IDENTITY_RESOLUTION",
            "PRECISION_METHOD_CANNOT_AFFECT_GRADE_OR_EVENT_KEYWORD = TRUE",
            "BS-ENHANCE-20260829-37",
            "PRECISION_SELECTION_PERSISTENCE = ATTEMPT_LOCAL_ONLY",
            "+10_PRECISION_OUTPUT_KEYWORD = TAG_KEYWORD",
            "WEAPON_KEYWORD_CONTENT_ID = DATA_BACKED_FIRST_TAG_CATALOG / BS-ENHANCE-20260829-37",
            "KEYWORD_PRESENTATION = REQUIRED_IN_WORKSHOP_PRECISION_UI / NO_NEW_RASTER",
            "PRIMARY_PLAYABLE_CONTENT = REPEATED_ENHANCEMENT_JUDGMENT_AND_FEEDBACK",
            "PHASE_1_SLICE = +0_TO_+10 / +11_TO_+15 / ONE_SAME_UID_RESULT",
            "CRAFT_FEEDBACK_MILESTONE = EVERY_5_LEVELS",
            "+5 = PRESENTATION_ONLY",
            "+10 = PRESENTATION_PLUS_ONLY_PRECISION_AND_ONE_KEYWORD",
            "Runtime support must cover targets 10~100 without changing Decision28/29/30.",
            "RETURN_BEAT = ONE_NON_ECONOMIC_WORKSHOP_MOMENT",
            "NO_TIMER / NO_CUSTOMER_MANAGEMENT / NO_SECOND_ITEM / NO_FAKE_DAMAGE",
            "IMPLEMENTATION_DRIFT = LEGACY_MULTI_PRECISION_DATA_AND_NON_VERTICAL_SLICE_MODULES",
            "INCIDENT_ID = BS-OPS-20260828-37",
            "NO_BASE_PROMOTION = PROJECT_SPECIFIC_LEGACY_AND_SLICE_BOUNDARY",
            "P0_IMPLEMENTATION_GUARD = VERTICAL_SLICE_ONLY_CURRENT_CANON",
            "OUT_OF_SCOPE = NEW_ART_ASSET_BATCH / ECONOMY_REBALANCE / MULTI_CUSTOMER_SYSTEM / RELEASE_WORK",
            "TEST_ORDER = RED_CONTRACTS -> GREEN_MINIMUM_FLOW -> REFACTOR_LEGACY_BOUNDARIES",
            "HUMAN_PLAYTEST = DEFERRED_BY_USER / NOT_RUN",
            "PHASE_2_ENTRY = SATISFIED_BY_CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826",
        )
    )
    locator = "BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md"
    assert locator in CORE_CANON.read_text(encoding="utf-8"), "core canon must locate the unified contract"
    assert locator in HANDOFF.read_text(encoding="utf-8"), "handoff must locate the unified contract"
    decision_text = WEAPON_KEYWORD_DECISION.read_text(encoding="utf-8")
    require_decision_tokens = (
        "STATUS = USER_APPROVED_CURRENT",
        "FIELD_OWNER = WEAPON_KEYWORD_OWNERSHIP",
        "ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY",
        "ITEM_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX",
        "PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10",
        "WEAPON_KEYWORD_TAXONOMY = GRADE_KEYWORD / TAG_KEYWORD / EVENT_KEYWORD",
        "GRADE_KEYWORD_MACHINE_OWNER = GRADE_AFFIX",
        "TAG_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX",
        "EVENT_KEYWORD_MACHINE_OWNER = CHRONICLE_AFFIX",
        "+10_PRECISION_OUTPUT_KEYWORD = TAG_KEYWORD",
        "WEAPON_KEYWORD_CONTENT_ID = DATA_BACKED_FIRST_TAG_CATALOG / BS-ENHANCE-20260829-37",
        "HISTORICAL_FIXTURE_OR_CUSTOMER_EPITHET_REUSE = FORBIDDEN",
        "BS-ENHANCE-20260901-40",
        "not a competing current Tag cadence owner",
    )
    missing_decision = [token for token in require_decision_tokens if token not in decision_text]
    assert not missing_decision, f"{WEAPON_KEYWORD_DECISION.name}: missing {missing_decision}"
    taxonomy_token = "WEAPON_KEYWORD_TAXONOMY = GRADE_KEYWORD / TAG_KEYWORD / EVENT_KEYWORD"
    assert taxonomy_token in CORE_CANON.read_text(encoding="utf-8"), "core canon must mirror weapon keyword taxonomy"
    assert taxonomy_token in HANDOFF.read_text(encoding="utf-8"), "handoff must preserve weapon keyword taxonomy"
    ownership_tokens = (
        "TAG_KEYWORD_SOURCE = CONSUMABLE_PRECISION_CATALYST_AND_PRECISION_METHOD",
        "TAG_KEYWORD_RESOLUTION = CATALYST_AND_PRECISION_METHOD_GOVERN_TAG_IDENTITY",
        "PRECISION_METHOD_EFFECT_SCOPE = WEAPON_STATS_DURABILITY_AND_TAG_RESOLUTION_CONTEXT",
        "PRECISION_METHOD_TAG_ROLE = TAG_IDENTITY_RESOLUTION",
        "PRECISION_METHOD_CANNOT_AFFECT_GRADE_OR_EVENT_KEYWORD = TRUE",
        "MISSING_PRECISION_CATALYST_BEHAVIOR = BLOCK_BEFORE_COST_OR_ROLL",
        "NO_DEFAULT_PRECISION_CATALYST = TRUE",
        "PRECISION_CATALYST_CONSUMPTION = ONE_UNIT_ON_NORMAL_RESOLVED_ATTEMPT",
    )
    for document in (CORE_CANON, HANDOFF):
        document_text = document.read_text(encoding="utf-8")
        missing = [token for token in ownership_tokens if token not in document_text]
        assert not missing, f"{document.name}: missing {missing}"
    recurring_text = RECURRING_PRECISION_DECISION.read_text(encoding="utf-8")
    assert "PRECISION_TARGETS=[10,20,30,40,50,60,70,80,90,100]" in recurring_text
    assert "ADD_TAG" in recurring_text and "UPGRADE_TAG" in recurring_text
    consumable_text = CONSUMABLE_CATALYST_DECISION.read_text(encoding="utf-8")
    assert "불의 심장" in consumable_text and "대지의 결정" in consumable_text
    assert "CONSUME_REQUIRED_CATALYST_ONE_UNIT" in consumable_text
    for document in (HISTORICAL_PRECISION, HISTORICAL_CATALYST):
        document_text = document.read_text(encoding="utf-8")
        assert "CURRENT_OVERRIDE_BS-ENHANCE-20260828-34" in document_text, f"{document.name}: missing current override"
    assert "SUPERSEDED_BY_BS-INC-20260828-40" in SUPERSEDED_INCIDENT.read_text(encoding="utf-8")
    incident_text = INCIDENT.read_text(encoding="utf-8")
    assert "NO_BASE_PROMOTION = PROJECT_SPECIFIC_WEAPON_KEYWORD_OWNERSHIP" in incident_text
    assert "data-backed, localized first-slice keyword" not in CONTRACT.read_text(encoding="utf-8")
    assert "non-placeholder weapon keyword" not in CONTRACT.read_text(encoding="utf-8")
    print("phase1 unified implementation contract: PASS")


if __name__ == "__main__":
    main()
