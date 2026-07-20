#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def main() -> int:
    errors: list[str] = []
    json_files = sorted(DATA_ROOT.rglob("*.json"))

    if not json_files:
        errors.append("No JSON game data files found.")

    for path in json_files:
        try:
            data = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{path.relative_to(ROOT)}: root must be an object")
            continue

        if data.get("schema_version") != 1:
            errors.append(f"{path.relative_to(ROOT)}: schema_version must be 1")

    material_path = DATA_ROOT / "crafting" / "materials.json"
    recipe_path = DATA_ROOT / "crafting" / "hidden_recipes.json"

    if material_path.exists() and recipe_path.exists():
        materials = load_json(material_path)
        recipes = load_json(recipe_path)
        material_ids = {item["id"] for item in materials.get("materials", [])}

        for recipe in recipes.get("recipes", []):
            recipe_input = recipe.get("input", {})
            for field in ("secondary_material", "catalyst"):
                material_id = recipe_input.get(field)
                if material_id and material_id not in material_ids:
                    errors.append(
                        f"data/crafting/hidden_recipes.json: {recipe.get('id')} references "
                        f"unknown {field} '{material_id}'"
                    )

    if errors:
        print("Blacksmith data validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Blacksmith data validation PASSED ({len(json_files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
