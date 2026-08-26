#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-DAMAGE-20260826-30"
DECISION = ROOT / "docs/decisions/BS-DAMAGE-20260826-30_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY.md"
MODEL = ROOT / "docs/planning/BLACKSMITH_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY_20260826.json"
DURABILITY_MODEL = ROOT / "docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json"
CORE = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
AUTHORITY = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
AGENTS = ROOT / "AGENTS.md"


def require_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{label} missing tokens: {missing}"


def main() -> None:
    assert DECISION.exists(), f"missing Decision30 owner: {DECISION.relative_to(ROOT)}"
    assert MODEL.exists(), f"missing Decision30 model: {MODEL.relative_to(ROOT)}"

    decision_text = DECISION.read_text(encoding="utf-8")
    require_tokens(
        decision_text,
        [
            DECISION_ID,
            "USER_APPROVED_STRUCTURAL_CANON",
            "TEMP_TEST_BUDGET",
            "PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE",
            "ACTUAL_ITEM_USE_REQUIRED = TRUE",
            "MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1",
            "NONE = 0%",
            "LOW = 10%",
            "MEDIUM = 20%",
            "HIGH = 40%",
            "DIRECT = 100%",
            "PROBABILISTIC_DAMAGE_CAP = 95%",
            "WORLD_EVENT_MAX_DURABILITY_DAMAGE = FALSE",
            "MISSION_OUTCOME_AND_ITEM_DAMAGE = INDEPENDENT_AXES",
            "NO_UNIVERSAL_CUSTOMER_DAMAGE_PERCENT",
        ],
        "Decision30",
    )

    model = json.loads(MODEL.read_text(encoding="utf-8"))
    assert model["decision_id"] == DECISION_ID
    assert model["status"] == "USER_APPROVED_STRUCTURAL_CANON_TEMP_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE"
    assert model["purchase_or_handoff_itself_causes_damage"] is False
    assert model["actual_item_use_required"] is True
    assert model["max_damage_rolls_per_event_per_uid"] == 1
    assert model["world_event_max_durability_damage"] is False
    assert model["mission_outcome_and_item_damage_independent"] is True
    assert model["no_universal_customer_damage_percent"] is True
    assert model["probabilistic_damage_cap_percent"] == 95
    assert model["durability_multiplier_owner"] == "BS-REPAIR-20260826-29"
    assert model["damage_resolution_owner"] == "BS-REPAIR-20260826-29"

    profiles = model["damage_profiles_temp_budget_percent"]
    assert profiles == {"NONE": 0, "LOW": 10, "MEDIUM": 20, "HIGH": 40, "DIRECT": 100}

    durability = json.loads(DURABILITY_MODEL.read_text(encoding="utf-8"))
    modifiers = durability["enhancement_modifiers"]
    multipliers = {state: values["damage_risk_multiplier"] for state, values in modifiers.items()}
    assert multipliers == {"NORMAL": 1.0, "MINOR": 1.25, "MAJOR": 1.75}

    expected = {
        "LOW": {"NORMAL": 10.0, "MINOR": 12.5, "MAJOR": 17.5},
        "MEDIUM": {"NORMAL": 20.0, "MINOR": 25.0, "MAJOR": 35.0},
        "HIGH": {"NORMAL": 40.0, "MINOR": 50.0, "MAJOR": 70.0},
    }
    for profile, states in expected.items():
        for state, expected_percent in states.items():
            actual = min(95.0, profiles[profile] * multipliers[state])
            assert actual == expected_percent, (profile, state, actual, expected_percent)
    assert profiles["DIRECT"] == 100

    mitigation = model["explicit_relevant_protection_profile_shift"]
    assert mitigation["enabled"] is True
    assert mitigation["max_steps"] == 1
    assert mitigation["requires_event_specific_relevance"] is True
    assert mitigation["universal_keyword_damage_bonus_allowed"] is False
    assert mitigation["direct_profile_mitigated_by_generic_keyword"] is False

    for path in (CORE, AUTHORITY, HANDOFF, AGENTS):
        text = path.read_text(encoding="utf-8")
        require_tokens(text, [DECISION_ID], path.name)

    handoff_text = HANDOFF.read_text(encoding="utf-8")
    assert "CURRENT_PLANNING_WORK = DURABILITY_ECONOMY_SENSITIVITY + R_BAND_INPUT_EVIDENCE" in handoff_text

    print("customer world event damage policy current contract: PASS")


if __name__ == "__main__":
    main()
