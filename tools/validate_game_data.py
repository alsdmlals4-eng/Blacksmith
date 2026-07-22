#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"
SUPPORTED_SCHEMA_VERSIONS = {1, 2, 3}


class ValidationErrors:
    def __init__(self) -> None:
        self.items: list[str] = []

    def add(self, message: str) -> None:
        self.items.append(message)

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.add(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("root must be an object")
    return value


def is_finite_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def probability(
    errors: ValidationErrors,
    value: object,
    label: str,
) -> float | None:
    if not is_finite_number(value) or not 0.0 <= float(value) <= 1.0:
        errors.add(f"{label}: must be a finite number from 0 to 1")
        return None
    return float(value)


def validate_json_roots(errors: ValidationErrors) -> list[Path]:
    json_files = sorted(DATA_ROOT.rglob("*.json"))
    errors.require(bool(json_files), "No JSON game data files found.")

    for path in json_files:
        try:
            data = load_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.add(f"{path.relative_to(ROOT)}: {exc}")
            continue

        schema_version = data.get("schema_version")
        errors.require(
            schema_version in SUPPORTED_SCHEMA_VERSIONS,
            f"{path.relative_to(ROOT)}: unsupported schema_version {schema_version!r}",
        )

    return json_files


def validate_hidden_recipe_references(errors: ValidationErrors) -> None:
    materials = load_json(DATA_ROOT / "crafting" / "materials.json")
    recipes = load_json(DATA_ROOT / "crafting" / "hidden_recipes.json")
    material_ids = {
        item.get("id")
        for item in materials.get("materials", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    for recipe in recipes.get("recipes", []):
        if not isinstance(recipe, dict):
            errors.add("hidden_recipes.json: each recipe must be an object")
            continue
        recipe_input = recipe.get("input", {})
        if not isinstance(recipe_input, dict):
            errors.add(f"hidden_recipes.json: {recipe.get('id')} input must be an object")
            continue
        for field in ("secondary_material", "catalyst"):
            material_id = recipe_input.get(field)
            if material_id and material_id not in material_ids:
                errors.add(
                    "data/crafting/hidden_recipes.json: "
                    f"{recipe.get('id')} references unknown {field} {material_id!r}"
                )


def validate_materials(
    errors: ValidationErrors,
    materials: dict[str, Any],
) -> None:
    material_ids: set[str] = set()
    for item in materials.get("materials", []):
        if not isinstance(item, dict):
            errors.add("materials.json: each material must be an object")
            continue

        material_id = item.get("id")
        if not isinstance(material_id, str) or not material_id:
            errors.add(f"materials.json: invalid material id {material_id!r}")
            continue
        if material_id in material_ids:
            errors.add(f"materials.json: duplicate material id {material_id!r}")
            continue
        material_ids.add(material_id)

        effects = item.get("effects", {})
        if not isinstance(effects, dict):
            errors.add(f"materials.json: {material_id} effects must be an object")
            continue
        for effect_name, effect_value in effects.items():
            if not is_finite_number(effect_value) or float(effect_value) < 0.0:
                errors.add(
                    f"materials.json: {material_id}.{effect_name} "
                    "must be a non-negative finite number"
                )


def validate_success_pattern(
    errors: ValidationErrors,
    balance: dict[str, Any],
    interval: int,
) -> None:
    pattern = balance.get("base_success_pattern_by_cycle_position", {})
    if not isinstance(pattern, dict):
        errors.add("enhancement_balance.json: success pattern must be an object")
        return

    expected_keys = {str(position) for position in range(1, interval + 1)}
    errors.require(
        set(pattern) == expected_keys,
        f"enhancement_balance.json: success pattern keys must be 1..{interval}",
    )

    previous = 1.0
    for position in range(1, interval + 1):
        current = probability(
            errors,
            pattern.get(str(position)),
            f"enhancement_balance.json: success pattern {position}",
        )
        if current is None:
            continue
        errors.require(
            current <= previous,
            "enhancement_balance.json: success pattern must be non-increasing",
        )
        previous = current


def validate_pity_and_policy(
    errors: ValidationErrors,
    balance: dict[str, Any],
) -> None:
    pity = balance.get("pity", {})
    if not isinstance(pity, dict):
        errors.add("enhancement_balance.json: pity must be an object")
        return

    bonus_per_failure = probability(
        errors,
        pity.get("bonus_per_failure"),
        "enhancement_balance.json: pity bonus_per_failure",
    )
    max_bonus = probability(
        errors,
        pity.get("max_bonus"),
        "enhancement_balance.json: pity max_bonus",
    )
    if bonus_per_failure is not None and max_bonus is not None:
        errors.require(
            bonus_per_failure <= max_bonus,
            "enhancement_balance.json: pity step cannot exceed its cap",
        )

    expected_policy = {
        "consume_materials_on_attempt_start": True,
        "pity_resets_on_success": True,
        "pity_survives_downgrade": True,
    }
    errors.require(
        balance.get("failure_policy") == expected_policy,
        "enhancement_balance.json: canonical failure_policy mismatch",
    )


def reachable_decade_keys(max_level: int) -> set[str]:
    return {str(decade) for decade in range((max_level - 1) // 10 + 1)}


def validate_risk_table(
    errors: ValidationErrors,
    risk: dict[str, Any],
    field_name: str,
    expected_keys: set[str],
) -> None:
    table = risk.get(field_name, {})
    if not isinstance(table, dict):
        errors.add(f"enhancement_balance.json: risk.{field_name} must be an object")
        return
    if set(table) != expected_keys:
        errors.add(
            "enhancement_balance.json: "
            f"risk.{field_name} must cover only reachable decades "
            f"{sorted(expected_keys, key=int)}"
        )
        return

    previous = -1.0
    for decade in sorted(expected_keys, key=int):
        current = probability(
            errors,
            table.get(decade),
            f"enhancement_balance.json: risk.{field_name}.{decade}",
        )
        if current is None:
            continue
        errors.require(
            current >= previous,
            f"enhancement_balance.json: risk.{field_name} must be non-decreasing",
        )
        previous = current


def validate_risk(
    errors: ValidationErrors,
    balance: dict[str, Any],
    max_level: int,
) -> None:
    risk = balance.get("risk", {})
    if not isinstance(risk, dict):
        errors.add("enhancement_balance.json: risk must be an object")
        return

    safe_until_level = risk.get("safe_until_level")
    destroy_start_level = risk.get("destroy_start_level")
    errors.require(
        isinstance(safe_until_level, int)
        and isinstance(destroy_start_level, int)
        and 0 <= safe_until_level < destroy_start_level <= max_level,
        "enhancement_balance.json: invalid safe/destroy level boundaries",
    )

    expected_keys = reachable_decade_keys(max_level)
    validate_risk_table(errors, risk, "downgrade_ratio_by_decade", expected_keys)
    validate_risk_table(errors, risk, "destroy_ratio_by_decade", expected_keys)

    downgrade_steps = risk.get("downgrade_steps_by_decade", {})
    errors.require(
        isinstance(downgrade_steps, dict)
        and set(downgrade_steps) == expected_keys
        and all(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0
            for value in downgrade_steps.values()
        ),
        "enhancement_balance.json: downgrade steps must cover only reachable decades",
    )


def validate_milestones(
    errors: ValidationErrors,
    milestones: dict[str, Any],
    balance: dict[str, Any],
    max_level: int,
    interval: int,
) -> None:
    errors.require(
        "failure_policy" not in milestones,
        "enhancement_milestones.json must not own failure_policy",
    )

    entries = milestones.get("milestones", [])
    if not isinstance(entries, list):
        errors.add("enhancement_milestones.json: milestones must be an array")
        return

    actual_levels = [
        entry.get("level")
        for entry in entries
        if isinstance(entry, dict)
    ]
    expected_levels = list(range(interval, max_level + 1, interval))
    errors.require(
        actual_levels == expected_levels,
        "enhancement_milestones.json: milestones must be ordered levels 10..100",
    )
    errors.require(
        all(
            isinstance(entry, dict)
            and entry.get("special_enhancement") is True
            for entry in entries
        ),
        "enhancement_milestones.json: every milestone must be special enhancement",
    )

    special = milestones.get("special_enhancement", {})
    precision = balance.get("precision", {})
    if not isinstance(special, dict) or not isinstance(precision, dict):
        errors.add("enhancement special/precision configuration must be objects")
        return
    errors.require(
        special.get("interval") == interval,
        "enhancement_milestones.json: special interval mismatch",
    )
    for key in ("good_success_bonus", "perfect_success_bonus"):
        errors.require(
            special.get(key) == precision.get(key),
            f"enhancement milestone/balance {key} mismatch",
        )


def validate_enhancement_semantics(errors: ValidationErrors) -> None:
    balance = load_json(DATA_ROOT / "crafting" / "enhancement_balance.json")
    milestones = load_json(DATA_ROOT / "crafting" / "enhancement_milestones.json")
    materials = load_json(DATA_ROOT / "crafting" / "materials.json")

    errors.require(
        balance.get("schema_version") == 3,
        "enhancement_balance.json schema_version must be 3",
    )
    errors.require(
        milestones.get("schema_version") == 2,
        "enhancement_milestones.json schema_version must be 2",
    )

    max_level = balance.get("max_level")
    material_interval = balance.get("material_interval")
    valid_structure = (
        isinstance(max_level, int)
        and not isinstance(max_level, bool)
        and max_level > 0
        and isinstance(material_interval, int)
        and not isinstance(material_interval, bool)
        and material_interval > 0
        and max_level % material_interval == 0
    )
    errors.require(
        valid_structure,
        "enhancement_balance.json: invalid max_level/material_interval",
    )
    if not valid_structure:
        return

    errors.require(
        balance.get("precision_interval") == material_interval,
        "enhancement_balance.json: precision and material intervals must match",
    )

    validate_success_pattern(errors, balance, material_interval)
    validate_pity_and_policy(errors, balance)
    validate_risk(errors, balance, max_level)
    validate_milestones(
        errors,
        milestones,
        balance,
        max_level,
        material_interval,
    )
    validate_materials(errors, materials)


def main() -> int:
    errors = ValidationErrors()
    json_files = validate_json_roots(errors)

    try:
        validate_hidden_recipe_references(errors)
        validate_enhancement_semantics(errors)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.add(f"enhancement semantic validation could not run: {exc}")

    if errors.items:
        print("Blacksmith data validation FAILED")
        for error in errors.items:
            print(f"- {error}")
        return 1

    print(
        "Blacksmith data validation PASSED "
        f"({len(json_files)} files; enhancement semantics verified)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
