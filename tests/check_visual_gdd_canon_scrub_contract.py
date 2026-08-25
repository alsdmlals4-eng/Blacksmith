from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRUB = ROOT / "docs/planning/BLACKSMITH_APPROVED_VISUAL_GDD_CANON_SCRUB_20260825.md"
SPEC = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_SAFE_SPEC_20260825.md"
BINDINGS = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_BINDINGS_20260825.json"

VISUAL_IDS = (
    "BS-VIS-20260820-01",
    "BS-VIS-20260820-02",
    "BS-VIS-20260820-05",
    "BS-VIS-20260820-06",
    "BS-VIS-20260820-09",
    "BS-VIS-20260824-10",
)

REQUIRED_TOKENS = (
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
    except AssertionError as exc:
        print(f"Visual GDD canon scrub contract FAILED\n- {exc}")
        return 1

    combined = "\n".join((scrub, spec, binding_text))
    for visual_id in VISUAL_IDS:
        if visual_id not in combined:
            errors.append(f"missing visual id: {visual_id}")

    for token in REQUIRED_TOKENS:
        if token not in combined:
            errors.append(f"missing scrub/spec token: {token}")

    try:
        payload = json.loads(binding_text)
    except json.JSONDecodeError as exc:
        errors.append(f"bindings json invalid: {exc}")
        payload = {}

    if payload:
        if payload.get("schema_version") != 1:
            errors.append("bindings schema_version must be 1")
        if payload.get("status") != "IMPLEMENTATION_SAFE_PLANNING_SPEC":
            errors.append("bindings status must be IMPLEMENTATION_SAFE_PLANNING_SPEC")
        if payload.get("image_text_authority") != "NEVER":
            errors.append("image_text_authority must be NEVER")
        if payload.get("product_implementation") != "BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION":
            errors.append("product implementation gate drift")
        visual_map = payload.get("visuals", {})
        for visual_id in VISUAL_IDS:
            if visual_id not in visual_map:
                errors.append(f"bindings missing visual: {visual_id}")
        repair = payload.get("bindings", {}).get("repair", {})
        if repair.get("player_material_name_ko") != "보강재":
            errors.append("repair material must be 보강재")
        if repair.get("normal_repair_effect") != "CURRENT=MAX;MAX=UNCHANGED":
            errors.append("normal repair effect drift")
        durability = payload.get("bindings", {}).get("durability", {})
        if durability.get("structure_state_owner") != "MAX":
            errors.append("structure state must be owned by MAX")
        onboarding = payload.get("bindings", {}).get("onboarding", {})
        if onboarding.get("first_stop_target") != 11:
            errors.append("first stop target must be +11")
        customer = payload.get("bindings", {}).get("customer_context", {})
        if customer.get("starter_customer_id") != "NADIA_VENN":
            errors.append("starter customer drift")
        if customer.get("numeric_capability_profile") != "SEPARATE_CANON_SOURCE_REQUIRED":
            errors.append("Nadia numeric capability must remain unresolved")

    if errors:
        print("Visual GDD canon scrub contract FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Visual GDD canon scrub contract PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
