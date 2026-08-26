#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-REPAIR-20260826-29"
DECISION = ROOT / "docs/decisions/BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md"
MODEL = ROOT / "docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json"
CORE = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
AUTHORITY = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
AGENTS = ROOT / "AGENTS.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"


def require_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{label} missing tokens: {missing}"


def derived_state(current: int, maximum: int, base_maximum: int) -> str:
    if current == 0:
        return "DESTROYED"
    current_condition = current / maximum
    structural_condition = maximum / base_maximum
    effective = min(current_condition, structural_condition)
    if effective == 1.0:
        return "NORMAL"
    if effective > 0.5:
        return "MINOR"
    return "MAJOR"


def main() -> None:
    assert DECISION.exists(), f"missing Decision29 owner: {DECISION.relative_to(ROOT)}"
    assert MODEL.exists(), f"missing machine-readable durability model: {MODEL.relative_to(ROOT)}"

    decision_text = DECISION.read_text(encoding="utf-8")
    require_tokens(
        decision_text,
        [
            DECISION_ID,
            "USER_APPROVED_STRUCTURAL_CANON",
            "TEMP_TEST_BUDGET",
            "BASE_MAX_DURABILITY",
            "MAX_DURABILITY",
            "CURRENT_DURABILITY",
            "CURRENT_CONDITION_RATIO = CURRENT_DURABILITY / MAX_DURABILITY",
            "STRUCTURAL_CONDITION_RATIO = MAX_DURABILITY / BASE_MAX_DURABILITY",
            "EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)",
            "NORMAL = EFFECTIVE_DURABILITY_RATIO == 1.00",
            "MINOR = 0.50 < EFFECTIVE_DURABILITY_RATIO < 1.00",
            "MAJOR = 0 < EFFECTIVE_DURABILITY_RATIO <= 0.50",
            "DESTROYED = CURRENT_DURABILITY == 0",
            "4/4 with BASE_MAX 5 = MINOR",
            "2/2 with BASE_MAX 5 = MAJOR",
            "MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES",
            "MAX_DURABILITY_FLOOR = 1",
            "MAX_DURABILITY_RECOVERY = NOT_APPROVED",
            "DAMAGE_EVENT_CURRENT_LOSS = 1",
        ],
        "Decision29",
    )

    model = json.loads(MODEL.read_text(encoding="utf-8"))
    assert model["decision_id"] == DECISION_ID
    assert model["status"] == "USER_APPROVED_STRUCTURAL_CANON_TEMP_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE"
    assert model["reference_base_max_durability"] == 5
    assert model["max_durability_floor"] == 1
    assert model["damage_event_current_loss"] == 1
    assert model["destroyed_repair_allowed"] is False
    assert model["major_enhancement_allowed"] is True

    derivation = model["durability_state_derivation"]
    assert derivation == {
        "current_condition_ratio": "CURRENT_DURABILITY / MAX_DURABILITY",
        "structural_condition_ratio": "MAX_DURABILITY / BASE_MAX_DURABILITY",
        "effective_durability_ratio": "min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)",
        "destroyed_override": "CURRENT_DURABILITY == 0",
    }

    states = model["durability_states"]
    assert states["NORMAL"] == {"effective_ratio_equals": 1.0}
    assert states["MINOR"] == {"effective_ratio_gt": 0.5, "effective_ratio_lt": 1.0}
    assert states["MAJOR"] == {"effective_ratio_gt": 0.0, "effective_ratio_lte": 0.5}
    assert states["DESTROYED"] == {"current_equals": 0}

    # A repaired item with permanent MAX loss must remain structurally worse than pristine.
    assert derived_state(5, 5, 5) == "NORMAL"
    assert derived_state(4, 4, 5) == "MINOR"
    assert derived_state(2, 2, 5) == "MAJOR"
    assert derived_state(1, 1, 5) == "MAJOR"
    assert derived_state(3, 5, 5) == "MINOR"
    assert derived_state(2, 5, 5) == "MAJOR"
    assert derived_state(0, 5, 5) == "DESTROYED"

    modifiers = model["enhancement_modifiers"]
    assert modifiers["NORMAL"] == {"success_delta_pp": 0, "new_effect_multiplier": 1.0, "damage_risk_multiplier": 1.0}
    assert modifiers["MINOR"] == {"success_delta_pp": -3, "new_effect_multiplier": 0.9, "damage_risk_multiplier": 1.25}
    assert modifiers["MAJOR"] == {"success_delta_pp": -7, "new_effect_multiplier": 0.75, "damage_risk_multiplier": 1.75}

    quality = model["repair_quality_temp_budget"]
    assert sum(entry["probability_percent"] for entry in quality) == 100
    assert [(entry["id"], entry["probability_percent"], entry["target_current_ratio"]) for entry in quality] == [
        ("EXCELLENT", 20, 1.0),
        ("STANDARD", 60, 0.75),
        ("POOR", 20, 0.5),
    ]
    assert model["repair_minimum_current_gain_when_possible"] == 1

    scar = model["repair_max_scar_chance_percent_temp_budget"]
    bands = ["PLUS_0_10", "PLUS_11_30", "PLUS_31_60", "PLUS_61_90", "PLUS_91_100"]
    assert [scar["MINOR"][band] for band in bands] == [10, 15, 20, 25, 30]
    assert [scar["MAJOR"][band] for band in bands] == [25, 30, 35, 40, 45]
    for state in ("MINOR", "MAJOR"):
        values = [scar[state][band] for band in bands]
        assert values == sorted(values), f"{state} scar chance must be non-decreasing by enhancement band"
    for band in bands:
        assert scar["MAJOR"][band] > scar["MINOR"][band], f"MAJOR must be riskier than MINOR at {band}"

    for path in (CORE, AUTHORITY, AGENTS, HANDOFF):
        text = path.read_text(encoding="utf-8")
        require_tokens(text, [DECISION_ID], path.name)

    core_text = CORE.read_text(encoding="utf-8")
    require_tokens(
        core_text,
        [
            "DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC",
            "DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW",
            "EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)",
            "ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29",
            "CURRENT_MAX_AUTHORITY = SUPERSEDED = HISTORICAL_DECISION26_ONLY",
        ],
        "current core owner",
    )

    print("durability repair model current contract: PASS")


if __name__ == "__main__":
    main()
