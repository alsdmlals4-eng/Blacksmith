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
            "CURRENT_2026-08-28_PHASE = PHASE_1_PLANNING_CO_DESIGN",
            "NEW_PRODUCT_MUTATION = BLOCKED_UNTIL_PHASE_1_AND_2_APPROVAL",
            "HISTORICAL_RUNTIME_IMPLEMENTATION = AUTOMATED_EVIDENCE_ONLY_NOT_CURRENT_AUTHORITY",
        ),
    )
    require_tokens(
        ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md",
        (
            "CURRENT_PHASE = PHASE_1_PLANNING_CO_DESIGN",
            "RUNTIME_IMPLEMENTATION_OF_NEW_CORE = HISTORICAL_AUTOMATED_EVIDENCE_NOT_NEW_MUTATION_AUTHORITY",
        ),
    )
    require_tokens(
        ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md",
        (
            "CURRENT_SESSION_HANDOFF / PHASE_1_CANONIZATION_AND_CO_DESIGN",
            "CURRENT_ACCEPTED_FRONTIER = CANONIZATION_AND_CORE_EXPERIENCE_REVIEW",
        ),
    )
    require_tokens(
        ROOT / "docs/operations/BS-INC-20260828-01_PHASE1_CANONIZATION_DRIFT.md",
        (
            "## Incident",
            "NO_BASE_PROMOTION",
            "Notion",
            "a1799f910a27954c902297978fb79f81ca586e87",
        ),
    )
    print("phase1 canonization contract: PASS")


if __name__ == "__main__":
    main()
