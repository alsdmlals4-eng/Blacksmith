#!/usr/bin/env python3
"""Prevent the balance simulator from silently dropping runtime rule families."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_all(path: Path, tokens: tuple[str, ...]) -> list[str]:
    source = path.read_text(encoding="utf-8")
    return [f"{path.relative_to(ROOT)}: missing {token}" for token in tokens if token not in source]


def main() -> int:
    session = ROOT / "scripts/enhancement/enhancement_session.gd"
    simulator = ROOT / "tools/simulate_enhancement_balance.py"
    errors = []
    errors += require_all(session, (
        "func calculate_success_chance",
        "func calculate_outcome_probabilities",
        "func can_use_skill_for_level",
        "func calculate_attempt_cost",
        "func _calculate_sale_price",
        "failure_streak",
        "leap_levels",
        "sale_value_bonus",
    ))
    errors += require_all(simulator, (
        "def success_chance",
        "def conditional_risk",
        "def can_use_overdrive",
        "def attempt_cost",
        "def sale_price",
        "def resolve",
        "failure_streak",
        "leap_levels",
        "sale_value_bonus",
        "semantic_parity",
    ))
    if errors:
        print("Enhancement balance simulator contract FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Enhancement balance simulator contract PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
