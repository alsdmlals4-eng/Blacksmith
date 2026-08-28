import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs/decisions/BS-ENHANCE-20260829-37_PRECISION_TAG_CATALOG_AND_SELECTION_GATE.md"
CATALOG = ROOT / "docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json"
PHASE_CONTRACT = ROOT / "docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md"
CORE_CANON = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
AUTHORITY_INDEX = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
HUMAN_GDD = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md"
AI_SPEC = ROOT / "docs/design/PROJECT_AI_PRODUCTION_SPEC.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = _read(path)
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{path.name}: missing {missing}"


def main() -> None:
    for path in (
        DECISION,
        CATALOG,
        PHASE_CONTRACT,
        CORE_CANON,
        AUTHORITY_INDEX,
        HANDOFF,
        HUMAN_GDD,
        AI_SPEC,
    ):
        assert path.is_file(), f"missing current precision catalog owner: {path}"

    _require_tokens(
        DECISION,
        (
            "STATUS = USER_APPROVED_CURRENT",
            "BS-ENHANCE-20260829-37",
            "TAG_CATALOG_OWNER = BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json",
            "EMPTY_CATALYST_LINEAGE_BEHAVIOR = BLOCK_BEFORE_COST_OR_ROLL",
            "NO_DEFAULT_LINEAGE = TRUE",
            "NO_NEW_STORED_FIELD_OR_FOURTH_AFFIX_SLOT = TRUE",
            "PRECISION_SELECTION_PERSISTENCE = ATTEMPT_LOCAL_ONLY",
            "HUMAN_PLAYTEST = DEFERRED_BY_USER / NOT_RUN",
            "FUNCTION_REWORK = FORBIDDEN",
            "ARTISTRY_EFFECT = FORBIDDEN",
            "UNIVERSAL_CUSTOMER_DAMAGE_MITIGATION = FORBIDDEN",
        ),
    )

    catalog = json.loads(_read(CATALOG))
    assert catalog["schema_version"] == 1
    assert catalog["status"] == "USER_APPROVED_CURRENT"
    assert catalog["source_decision_id"] == "BS-ENHANCE-20260829-37"
    assert catalog["machine_owner"] == "CATALYST_AFFIX"
    assert catalog["new_stored_field"] is False
    assert catalog["selection_flow"]["entry_level"] == 9
    assert catalog["selection_flow"]["target_level"] == 10
    assert catalog["selection_flow"]["persistence"] == "ATTEMPT_LOCAL_ONLY"
    assert catalog["selection_flow"]["empty_lineage_behavior"] == "BLOCK_BEFORE_COST_OR_ROLL"
    assert catalog["selection_flow"]["no_default_lineage"] is True
    assert catalog["selection_flow"]["failure_preserves_selection"] is False
    assert catalog["mechanical_boundary"]["durability_delta_in_first_catalog"] == 0
    assert catalog["mechanical_boundary"]["forbid_function_rework"] is True
    assert catalog["mechanical_boundary"]["forbid_artistry_effect"] is True
    assert catalog["mechanical_boundary"]["forbid_universal_customer_damage_mitigation"] is True

    lineages = {entry["id"]: entry for entry in catalog["lineages"]}
    methods = {entry["id"]: entry for entry in catalog["methods"]}
    tags = {entry["id"]: entry for entry in catalog["tags"]}
    assert set(lineages) == {"EMBER_LINEAGE", "ANVIL_LINEAGE"}
    assert set(methods) == {"EDGE_REINFORCEMENT", "LIGHTWEIGHTING"}
    assert methods["EDGE_REINFORCEMENT"]["effect"] == {
        "axis": "RAW_ROLE_STAT",
        "delta": 3,
    }
    assert methods["LIGHTWEIGHTING"]["effect"] == {
        "axis": "WEIGHT_POINT",
        "delta": -3,
    }
    assert len(tags) == 4
    pairs = {(entry["lineage_id"], entry["method_id"]) for entry in tags.values()}
    assert pairs == {
        ("EMBER_LINEAGE", "EDGE_REINFORCEMENT"),
        ("EMBER_LINEAGE", "LIGHTWEIGHTING"),
        ("ANVIL_LINEAGE", "EDGE_REINFORCEMENT"),
        ("ANVIL_LINEAGE", "LIGHTWEIGHTING"),
    }
    assert all(entry["machine_owner"] == "CATALYST_AFFIX" for entry in tags.values())
    assert all(entry["display_name_ko"] for entry in tags.values())
    assert catalog["legacy_placeholder_backfill"]["placeholder"] == "PRECISION_KEYWORD_PENDING_CONTENT"
    assert catalog["legacy_placeholder_backfill"]["cost_or_roll"] == "NONE"
    assert catalog["legacy_placeholder_backfill"]["effect_application"] == "APPLY_ONCE"

    mirrored_tokens = (
        "BS-ENHANCE-20260829-37",
        "EMPTY_CATALYST_LINEAGE_BEHAVIOR = BLOCK_BEFORE_COST_OR_ROLL",
        "NO_DEFAULT_LINEAGE = TRUE",
        "PRECISION_SELECTION_PERSISTENCE = ATTEMPT_LOCAL_ONLY",
        "HUMAN_PLAYTEST = DEFERRED_BY_USER / NOT_RUN",
    )
    for path in (PHASE_CONTRACT, CORE_CANON, AUTHORITY_INDEX, HANDOFF):
        _require_tokens(path, mirrored_tokens)
    _require_tokens(
        HUMAN_GDD,
        (
            "불씨 계보",
            "모루 계보",
            "날 세우기",
            "경량 담금",
            "태그를 정하지 않으면 강화 시도 자체가 시작되지 않는다",
            "사람 플레이 검수는 이번 계약의 완료 조건이 아니다",
        ),
    )
    _require_tokens(
        AI_SPEC,
        (
            "DEC-ENH-37",
            "결정 완료",
            "사람 플레이 검수는 사용자 지시로 이번 구현 계약의 완료 조건에서 제외",
        ),
    )
    print("precision tag catalog contract: PASS")


if __name__ == "__main__":
    main()
