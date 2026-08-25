from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRUB = ROOT / "docs/planning/BLACKSMITH_APPROVED_VISUAL_GDD_CANON_SCRUB_20260825.md"
SPEC = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_SAFE_SPEC_20260825.md"
BINDINGS = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_BINDINGS_20260825.json"
CURRENT_OWNER = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"

HISTORICAL_VISUAL_IDS = (
    "BS-VIS-20260820-01",
    "BS-VIS-20260820-02",
    "BS-VIS-20260820-05",
    "BS-VIS-20260820-06",
    "BS-VIS-20260820-09",
    "BS-VIS-20260824-10",
)

CURRENT_VISUAL_IDS = HISTORICAL_VISUAL_IDS + (
    "BS-VIS-20260820-04",
    "BS-VIS-20260820-08",
)

# PR #204 history must remain legible. These tokens are intentionally checked
# in the historical scrub document only and are NOT current gameplay authority.
HISTORICAL_SCRUB_TOKENS = (
    "KEEP",
    "CANON_VALUE",
    "VARIABLE_PLACEHOLDER",
    "CONFLICT_REMOVE",
    "IMAGE_TEXT_NEVER_OVERRIDES_CANON",
    "TARGET +11 = FIRST_STOP_POINT",
    "CHECKPOINT_IS_DOWNGRADE_FLOOR_NOT_SAVE_POINT",
    "NORMAL_REPAIR: CURRENT = MAX",
    "MAX determines structure state",
    "REPAIR_DOES_NOT_CHANGE_SUCCESS_RATE_WHEN_MAX_UNCHANGED",
    "PLAYER_REPAIR_MATERIAL = 보강재",
    "NADIA_NUMERIC_CAPABILITY = SEPARATE_CANON_SOURCE_REQUIRED",
    "DELAYED_RESULT = POST_FIRST_10_MINUTES_SCHEDULE",
)

CURRENT_TOKENS = (
    "BS-ENHANCE-20260825-25",
    "BS-DAMAGE-20260825-26",
    "BS-CHRONICLE-20260825-27",
    "BS-ART-20260825-03",
    "SUCCESS_LEVEL_DELTA = +1",
    "+9 -> +10 = PRECISION_ENHANCEMENT",
    "NORMAL -> MINOR -> MAJOR -> DESTROYED",
    "TARGET <= +10: ENHANCEMENT_DAMAGE = 0",
    "TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE",
    "CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE",
    "PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE",
    "ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE",
    "ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK",
    "PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION",
)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AssertionError(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc


def main() -> int:
    errors: list[str] = []

    try:
        scrub = read(SCRUB)
        spec = read(SPEC)
        binding_text = read(BINDINGS)
        current_owner = read(CURRENT_OWNER)
    except AssertionError as exc:
        print(f"Visual GDD canon scrub contract FAILED\n- {exc}")
        return 1

    for visual_id in HISTORICAL_VISUAL_IDS:
        if visual_id not in scrub:
            errors.append(f"historical scrub missing visual id: {visual_id}")

    for token in HISTORICAL_SCRUB_TOKENS:
        if token not in scrub:
            errors.append(f"historical scrub token lost: {token}")

    current_combined = "\n".join((spec, binding_text, current_owner))
    for visual_id in CURRENT_VISUAL_IDS:
        if visual_id not in current_combined:
            errors.append(f"current Visual reference missing: {visual_id}")

    for token in CURRENT_TOKENS:
        if token not in current_combined:
            errors.append(f"current simplified token missing: {token}")

    try:
        payload = json.loads(binding_text)
    except json.JSONDecodeError as exc:
        errors.append(f"bindings json invalid: {exc}")
        payload = {}

    if payload:
        if payload.get("schema_version") != 2:
            errors.append("bindings schema_version must be 2 after simplified-core rebind")
        if payload.get("status") != "IMPLEMENTATION_SAFE_PLANNING_SPEC_REBOUND_TO_CORE_SIMPLIFICATION":
            errors.append("bindings status must reflect simplified-core rebind")
        guards = payload.get("global_guards", {})
        if guards.get("image_text_authority") != "NEVER":
            errors.append("image_text_authority must be NEVER")
        if payload.get("product_implementation") != "BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION":
            errors.append("product implementation gate drift")

        enhancement = payload.get("enhancement", {})
        if enhancement.get("success_level_delta") != 1:
            errors.append("enhancement success delta must be exactly +1")
        precision = enhancement.get("precision_transition", {})
        if precision.get("current_level") != 9 or precision.get("target_level") != 10:
            errors.append("Precision transition must be +9 -> +10")
        if precision.get("keyword_machine_owner") != "CATALYST_AFFIX":
            errors.append("item keyword must reuse CATALYST_AFFIX owner")
        if enhancement.get("other_precision_milestones") != []:
            errors.append("later Precision milestones must be empty")
        damage_gate = enhancement.get("damage_gate", {})
        if damage_gate.get("target_le_10") != "IMPOSSIBLE_FROM_ENHANCEMENT_FAILURE":
            errors.append("enhancement damage must be impossible through target +10")
        if damage_gate.get("target_ge_11") != "POSSIBLE_ON_FAILURE":
            errors.append("enhancement damage must open from target +11")
        if damage_gate.get("curve_rule") != "MONOTONIC_NON_DECREASING_WITH_TARGET_LEVEL":
            errors.append("enhancement damage curve monotonic rule drift")

        damage = payload.get("damage", {})
        if damage.get("states") != ["NORMAL", "MINOR", "MAJOR", "DESTROYED"]:
            errors.append("damage state authority drift")
        if damage.get("hidden_numeric_current_max") is not False:
            errors.append("CURRENT/MAX must not survive as hidden authority")
        if damage.get("repair_model") != "NOT_DECIDED":
            errors.append("repair model must remain unresolved")

        customer_damage = payload.get("customer_world_event_damage", {})
        if customer_damage.get("possible_if_event_eligible") is not True:
            errors.append("eligible customer/world events must be able to damage item")
        if customer_damage.get("purchase_or_handoff_itself_causes_damage") is not False:
            errors.append("purchase/handoff itself must not cause damage")
        if customer_damage.get("max_state_advance_per_damage_event") != 1:
            errors.append("one customer/world damage event must advance one state")

        chronicle = payload.get("chronicle", {})
        if chronicle.get("routine_enhancement_attempt_rows") is not False:
            errors.append("routine enhancement attempts must not be player Chronicle rows")

        art = payload.get("art_direction", {})
        if art.get("id") != "ILLUSTRATED_WORKSHOP_BOOK":
            errors.append("current art direction drift")
        if art.get("status") != "USER_APPROVED_DIRECTION":
            errors.append("art direction approval state drift")

        previous_visuals = payload.get("previous_visual_gdd_status", {})
        for visual_id in CURRENT_VISUAL_IDS:
            if visual_id not in previous_visuals:
                errors.append(f"bindings missing Visual reference: {visual_id}")

    if errors:
        print("Visual GDD canon scrub contract FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Visual GDD canon scrub contract PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
