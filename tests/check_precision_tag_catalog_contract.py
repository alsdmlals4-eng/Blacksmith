import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION38 = ROOT / "docs/decisions/BS-ENHANCE-20260830-38_RECURRING_PRECISION_TAG_EVOLUTION.md"
CATALOG = ROOT / "docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json"
OWNERS = (
    ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md",
    ROOT / "docs/decisions/BS-ENHANCE-20260828-34_WEAPON_KEYWORD_OWNERSHIP.md",
    ROOT / "docs/decisions/BS-ENHANCE-20260829-37_PRECISION_TAG_CATALOG_AND_SELECTION_GATE.md",
    ROOT / "docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md",
    ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md",
    ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    assert DECISION38.is_file(), "Decision38 must be the recurring-precision field owner"
    catalog = json.loads(_text(CATALOG))
    assert catalog["schema_version"] == 2
    assert catalog["source_decision_id"] == "BS-ENHANCE-20260830-38"
    assert catalog["machine_owner"] == "CATALYST_AFFIX"
    assert catalog["precision_targets"] == list(range(10, 101, 10))
    assert catalog["tag_growth"]["max_active_tags"] == 3
    assert catalog["tag_growth"]["max_stage"] == 4
    assert catalog["selection_flow"]["actions"] == ["ADD_TAG", "UPGRADE_TAG"]
    assert catalog["selection_flow"]["persistence"] == "ATTEMPT_LOCAL_ONLY"
    assert catalog["selection_flow"]["no_default_random_or_reroll"] is True
    assert catalog["mechanical_boundary"]["durability_delta_in_first_catalog"] == 0
    assert set(catalog["mechanical_boundary"]["allowed_effect_axes"]) == {"RAW_ROLE_STAT", "WEIGHT_POINT"}
    assert catalog["mechanical_boundary"]["no_fourth_affix_slot"] is True
    assert catalog["migration"]["v3_empty_string"] == "EMPTY_TAG_COLLECTION"
    assert catalog["migration"]["v3_known_tag_at_level_10_or_higher"] == "SEED_STAGE_I_AND_MILESTONE_10"
    assert catalog["migration"]["v3_pending_placeholder"] == "INITIAL_TAG_PENDING_BLOCK_FOLLOWUP_PRECISION"
    assert catalog["migration"]["v3_unknown_nonempty_string"] == "FAIL_CLOSED_UNREADABLE_CATALYST_STATE"
    tag_ids = [tag["id"] for tag in catalog["tags"]]
    assert len(tag_ids) == 4
    assert len(tag_ids) == len(set(tag_ids))
    tag_id_set = set(tag_ids)
    lineages = {lineage["id"] for lineage in catalog["lineages"]}
    methods = {method["id"] for method in catalog["methods"]}
    assert tag_id_set == {"TAG_EMBER_EDGE", "TAG_EMBER_LIGHT", "TAG_ANVIL_EDGE", "TAG_ANVIL_LIGHT"}
    assert {(tag["id"], tag["lineage_id"], tag["method_id"]) for tag in catalog["tags"]} == {
        ("TAG_EMBER_EDGE", "EMBER_LINEAGE", "EDGE_REINFORCEMENT"),
        ("TAG_EMBER_LIGHT", "EMBER_LINEAGE", "LIGHTWEIGHTING"),
        ("TAG_ANVIL_EDGE", "ANVIL_LINEAGE", "EDGE_REINFORCEMENT"),
        ("TAG_ANVIL_LIGHT", "ANVIL_LINEAGE", "LIGHTWEIGHTING"),
    }
    expected_effects = {
        "EDGE_REINFORCEMENT": {"axis": "RAW_ROLE_STAT", "delta": 3, "durability_delta": 0},
        "LIGHTWEIGHTING": {"axis": "WEIGHT_POINT", "delta": -3, "durability_delta": 0},
    }
    for tag in catalog["tags"]:
        assert tag["machine_owner"] == "CATALYST_AFFIX"
        assert tag["lineage_id"] in lineages
        assert tag["method_id"] in methods
        compatible = tag["compatible_tag_ids"]
        assert len(compatible) == len(set(compatible))
        assert tag["id"] not in compatible
        assert set(compatible) == tag_id_set - {tag["id"]}
        for other_id in compatible:
            other = next(candidate for candidate in catalog["tags"] if candidate["id"] == other_id)
            assert tag["id"] in other["compatible_tag_ids"]
    for method in catalog["methods"]:
        assert method["effect"] == expected_effects[method["id"]]
    for owner in OWNERS:
        text = _text(owner)
        assert "BS-ENHANCE-20260830-38" in text, f"{owner.name}: missing Decision38 link"
        assert "[대체됨]" in text, f"{owner.name}: missing explicit supersession"
    authority = _text(OWNERS[4])
    phase_contract = _text(OWNERS[3])
    core_canon = _text(OWNERS[0])
    assert "RECURRING_PRECISION_DECISION = BS-ENHANCE-20260830-38" in phase_contract
    assert "Decision34/37 = RESIDUAL_NON_CONFLICTING_HISTORICAL_EVIDENCE" in authority
    assert "+10-only current" not in authority
    assert "+10-only current" not in core_canon
    assert "+10-only current" not in phase_contract
    print("precision tag catalog contract: PASS")


if __name__ == "__main__":
    main()
