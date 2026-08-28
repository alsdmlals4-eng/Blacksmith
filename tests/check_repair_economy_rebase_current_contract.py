#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-REPAIR-20260826-31"
DECISION = ROOT / "docs/decisions/BS-REPAIR-20260826-31_REPAIR_ECONOMY_REBASE_AND_SENSITIVITY.md"
MODEL = ROOT / "docs/planning/BLACKSMITH_REPAIR_ECONOMY_REBASE_20260826.json"
REPORT = ROOT / "docs/research/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_REPORT_20260826.md"
OVERLAY = ROOT / "CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md"
CORE = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"
AUTHORITY = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
AGENTS = ROOT / "AGENTS.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"


def require_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{label} missing tokens: {missing}"


def resolve_repair(
    old_current: int,
    maximum: int,
    quality_ratio: float,
    candidate_post_scar_max: int,
) -> tuple[int, int, bool]:
    scar_skipped = candidate_post_scar_max <= old_current
    post_scar_max = maximum if scar_skipped else candidate_post_scar_max
    quality_target = -(-int(post_scar_max * quality_ratio * 100) // 100)
    new_current = min(post_scar_max, max(old_current + 1, quality_target))
    return post_scar_max, new_current, scar_skipped


def main() -> None:
    assert DECISION.exists(), f"missing Decision31 owner: {DECISION.relative_to(ROOT)}"
    assert MODEL.exists(), f"missing repair economy model: {MODEL.relative_to(ROOT)}"
    assert REPORT.exists(), f"missing sensitivity report: {REPORT.relative_to(ROOT)}"

    decision_text = DECISION.read_text(encoding="utf-8")
    report_text = REPORT.read_text(encoding="utf-8")
    require_tokens(
        report_text,
        [
            "R_BAND = 100",
            "b = 0.50 / 0.65 / 0.80",
            "TEST_IN_PLAY",
            "NOT_FINAL_PRODUCT_BALANCE",
            "15 / 18 / 21",
            "25 / 31 / 37",
            "35 / 44 / 53",
            "45 / 57 / 69",
        ],
        "sensitivity report",
    )
    assert "final price table" not in report_text.lower()
    require_tokens(
        decision_text,
        [
            DECISION_ID,
            "USER_APPROVED_PLANNING_CANON",
            "TEMPORARY_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE",
            "REPAIR_JOB_AVAILABLE",
            "0 < CURRENT < MAX",
            "GOLD = ceil(R_BAND * (0.05 + 0.65 * LOSS_RATIO))",
            "REPAIR_PAYMENT = GOLD + 1 common_reinforcement_material",
            "candidate_post_scar_max <= OLD_CURRENT",
            "skip the scar; do not reroll quality or scar",
            "NEW_CURRENT = min(",
            "b = 0.50, 0.65, 0.80",
            "CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826",
            "CURRENT_CANON_MVP_AUTHORIZED / EXACT_HEAD_CONTRACT_AND_TDD_REQUIRED",
        ],
        "Decision31",
    )
    assert "BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION" not in decision_text

    model = json.loads(MODEL.read_text(encoding="utf-8"))
    assert model["contract_schema_version"] == 1
    assert model["decision_id"] == DECISION_ID
    assert model["status"] == "USER_APPROVED_PLANNING_CANON"
    assert model["scope"] == "PLANNING_ONLY"
    assert model["runtime_status"] == "MVP_CORE_IMPLEMENTED_GODOT_GUT_VERIFIED_20260826"

    repair_job = model["repair_job"]
    assert repair_job["unit"] == "boolean_per_item_uid"
    assert repair_job["opens_on"] == "resolved_actual_damage_event_that_reduces_current"
    assert repair_job["multiple_damage_before_repair"] == "remains_true_no_stacking"
    assert repair_job["consumed_on"] == "repair_start_regardless_of_quality_or_scar"
    assert repair_job["reopens_on"] == "later_resolved_actual_damage_event_that_reduces_current"

    assert model["implementation_contract"]["runtime_mvp_status"] == "IMPLEMENTED_GODOT_GUT_VERIFIED_20260826"
    assert model["implementation_contract"]["ui_integration"] == "NOT_RUN"

    payment = model["payment"]
    assert payment["formula"] == "GOLD = ceil(R_BAND * (0.05 + 0.65 * ((MAX - CURRENT) / BASE_MAX)))"
    assert payment["payment"] == "GOLD + 1 common_reinforcement_material"
    assert payment["base_max_denominator"] == "decision_29_base_max"
    assert payment["common_material"] == {
        "id": "common_reinforcement_material",
        "quantity": 1,
        "availability": "always_available",
        "grants_discount": False,
    }
    assert payment["r_band"]["explicit_simulation_input"] is True
    assert payment["r_band"]["status"] == "USER_APPROVED_MUTABLE_TEST_BASELINE"
    assert payment["r_band"]["change_policy"] == "MAY_CHANGE_AFTER_HUMAN_PLAYTEST_OR_NEW_BALANCE_EVIDENCE"
    assert payment["r_band"]["reference_definition"] == "fixed_gold_only_standard_enhancement_reference_by_primary_material_and_secured_band"
    assert payment["r_band"]["table"] == {
        "PLUS_0_10": {"iron": 125, "silver": 145, "meteor_iron": 170},
        "PLUS_11_30": {"iron": 160, "silver": 185, "meteor_iron": 215},
        "PLUS_31_60": {"iron": 220, "silver": 255, "meteor_iron": 295},
        "PLUS_61_90": {"iron": 300, "silver": 345, "meteor_iron": 405},
        "PLUS_91_100": {"iron": 400, "silver": 460, "meteor_iron": 540},
    }
    assert payment["r_band"]["prohibited_sources"] == [
        "current_sell_price",
        "forecast_next_attempt_price",
        "max_multiplier",
        "scar_multiplier",
    ]

    safety = model["scar_rounding_safety"]
    assert safety["blocking_condition"] == "candidate_post_scar_max <= OLD_CURRENT"
    assert safety["blocking_outcome"] == "skip_scar_without_quality_or_scar_reroll"
    assert safety["new_current"] == "min(POST_SCAR_MAX, max(OLD_CURRENT + 1, QUALITY_TARGET))"
    assert safety["invariant"] == "eligible_paid_repair_gives_at_least_one_current_point"

    sensitivity = model["sensitivity"]
    assert sensitivity["baseline_setup_coefficient"] == 0.05
    assert sensitivity["baseline_loss_coefficient"] == 0.65
    assert sensitivity["loss_coefficient_sweep"] == [0.5, 0.65, 0.8]
    assert "same_deterministic_event_sequence" in sensitivity["comparison_controls"]
    assert "no_eligible_repair_zero_current_gain" in sensitivity["required_invariants"]
    assert "no_repeat_repair_without_later_actual_damage" in sensitivity["required_invariants"]

    for path in (OVERLAY, CORE, AUTHORITY, AGENTS, HANDOFF):
        require_tokens(path.read_text(encoding="utf-8"), [DECISION_ID], path.name)
    require_tokens(
        HANDOFF.read_text(encoding="utf-8"),
        [
            "REPAIR_ECONOMY_HUMAN_PLAYTEST + MUTABLE_R_BAND_BASELINE_REVIEW",
            "b=.65 / USER_APPROVED_FIRST_TEST_DEFAULT",
            "R_BAND_TEST_TABLE = USER_APPROVED_MUTABLE_BASELINE",
            "R_BAND=100 / HISTORICAL_NORMALIZED_SENSITIVITY_INPUT_ONLY",
            "HUMAN_PLAYTEST = NOT_RUN",
        ],
        "Decision31 handoff",
    )
    require_tokens(
        CORE.read_text(encoding="utf-8"),
        ["BLACKSMITH_REPAIR_ECONOMY_REBASE_20260826.json"],
        "current core owner",
    )

    # Scar safety is behavioral: a blocking scar is skipped, never rerolled,
    # and every eligible repair outcome must improve Current.
    quality_cases = {"EXCELLENT": 1.0, "STANDARD": 0.75, "POOR": 0.5}
    for label, ratio in quality_cases.items():
        post, new_current, skipped = resolve_repair(1, 5, ratio, 4)
        assert (post, skipped) == (4, False), label
        assert new_current > 1, (label, post, new_current)

        post, new_current, skipped = resolve_repair(4, 5, ratio, 4)
        assert (post, skipped) == (5, True), label
        assert new_current > 4, (label, post, new_current)

    print("repair economy rebase current contract: PASS")


if __name__ == "__main__":
    main()
