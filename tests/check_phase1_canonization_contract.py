from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{path.name}: missing {missing}"


def main() -> None:
    require_tokens(
        ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md",
        (
            "CURRENT_2026-08-28_PHASE = IMPLEMENTATION_AND_REVIEW",
            "CURRENT_PRODUCT_MUTATION = AUTHORIZED_WITHIN_CURRENT_CANON_MVP",
            "HISTORICAL_RUNTIME_IMPLEMENTATION = AUTOMATED_EVIDENCE_ONLY_NOT_CURRENT_AUTHORITY",
            "PRIMARY_PLAYABLE_CONTENT = REPEATED_ENHANCEMENT_JUDGMENT_AND_FEEDBACK",
            "CUSTOMER_ITEM_LIFECYCLE = DIFFERENTIATING_CONTEXT_FOR_ENHANCEMENT_CHOICES",
        ),
    )
    require_tokens(
        ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md",
        (
            "CURRENT_PHASE = PHASE_2_UNIFIED_ENHANCEMENT_FIRST_SLICE_CONTRACT_REPAIR",
            "RUNTIME_IMPLEMENTATION_OF_NEW_CORE = PARTIALLY_IMPLEMENTED_HISTORICAL_EVIDENCE / CURRENT_CONTRACT_IMPLEMENTATION_AUTHORIZED",
        ),
    )
    require_tokens(
        ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md",
        (
            "CURRENT_SESSION_HANDOFF / IMPLEMENTATION_AND_REVIEW",
            "CURRENT_ACCEPTED_FRONTIER = PHASE_2_UNIFIED_ENHANCEMENT_FIRST_SLICE_CONTRACT_REPAIR",
            "CURRENT_CORE_HIERARCHY = ENHANCEMENT_PRIMARY / CUSTOMER_ITEM_LIFECYCLE_DIFFERENTIATOR",
        ),
    )
    require_tokens(
        ROOT / "docs/operations/BS-INC-20260828-01_PHASE1_CANONIZATION_DRIFT.md",
        (
            "## Incident",
            "HISTORICAL_PHASE1_CANONIZATION_DRIFT",
            "NO_BASE_PROMOTION",
            "Notion",
            "a1799f910a27954c902297978fb79f81ca586e87",
        ),
    )
    print("phase1 canonization contract: PASS")


if __name__ == "__main__":
    main()
