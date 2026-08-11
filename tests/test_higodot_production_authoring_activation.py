from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-HIGODOT-20260808-01"
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
DECISION = ROOT / "docs/decisions/BS-HIGODOT-20260808-01_PRODUCTION_AUTHORING_ACTIVATION.md"
CURRENT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
AGENTS = ROOT / "AGENTS.md"


def _text(path: Path) -> str:
    assert path.is_file(), f"missing required activation surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def test_user_approved_higodot_production_authoring_is_current_authority() -> None:
    policy = json.loads(_text(POLICY))
    assert DECISION_ID in policy["decision_ids"]
    assert policy["higodot"]["current_state"] == "FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY"
    assert policy["higodot"]["production_activation"] == "USER_APPROVED_ACTIVE"
    assert policy["higodot"]["policy_role"] == "SOLE_GODOT_AUTHORING_AUTHORITY"
    # Historical activation-scope snapshot: HiGodot activation itself did not
    # authorize general product implementation. Later Phase C entry is owned by
    # BS-OPS-20260811-03 and does not rewrite this activation evidence.
    assert policy["remaining_blockers"]["general_product_implementation"] == "BLOCKED"
    assert policy["hera"]["authoring_authority"] == "NONE"


def test_activation_is_scoped_and_recorded_in_current_canon() -> None:
    decision = _text(DECISION)
    current = _text(CURRENT_DECISIONS)
    gates = _text(GATES)
    agents = _text(AGENTS)

    for text in (decision, current, gates, agents):
        assert DECISION_ID in text

    for marker in (
        "TASK2_SCOPED_AUTHORING_ONLY",
        "GENERAL_PRODUCT_IMPLEMENTATION_BLOCKED",
        "HERA_AUTHORITY_NONE",
        "GUT_SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY",
        "FILE_AUTHORITY_MANIFEST_REQUIRED_FOR_MIXED_SURFACE_PR",
    ):
        assert marker in decision

    assert "HIGODOT_AUTHORING_AUTHORITY: FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY" in gates
    assert "BS-OPS-20260811-03" in gates
    assert "PLANNING_COMPLETE: USER_DECLARED" in gates
    assert (
        "GENERAL_PRODUCT_IMPLEMENTATION: APPROVED_WITHIN_EXISTING_CANON_NEW_SCOPE_REQUIRES_DECISION"
        in gates
    )
    assert (
        "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON"
        in gates
    )
    assert "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED" in gates
    assert "HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED" in gates
