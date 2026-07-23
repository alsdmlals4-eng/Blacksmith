#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"


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
        raise ValueError(f"{path}: root must be an object")
    return value


def _finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _score_fixture(fixture: dict[str, Any], contract: dict[str, Any], activity: dict[str, Any]) -> int:
    weights = activity["score_weights"]
    score = 0
    level = int(fixture.get("level", 0))
    if level >= int(contract["required_level"]):
        score += int(weights["required_level"])
    if level >= int(contract["stretch_level"]):
        score += int(weights["stretch_level"])
    preferred = set(contract.get("preferred_affix_ids", []))
    affixes = set(fixture.get("affix_ids", []))
    if preferred.intersection(affixes):
        score += int(weights["preferred_affix"])
    score += int(activity["grade_scores"].get(str(fixture.get("grade_id", "")), 0))
    if int(fixture.get("attack", 0)) >= int(weights["attack_threshold"]):
        score += int(weights["attack"])
    return score


def _band_for_score(score: int, bands: list[dict[str, Any]]) -> str:
    selected = ""
    for band in bands:
        if score >= int(band["minimum_score"]):
            selected = str(band["id"])
    return selected


def validate_lifecycle_poc(errors: ValidationErrors, data_root: Path = DATA_ROOT) -> None:
    required_paths = {
        "calendar": data_root / "progression/workshop_day_balance.json",
        "grades": data_root / "crafting/craftsmanship_grades.json",
        "contract": data_root / "customers/gladiator_poc.json",
        "activity": data_root / "world/gladiator_match_poc.json",
        "affixes": data_root / "crafting/affixes.json",
    }
    payloads: dict[str, dict[str, Any]] = {}
    for name, path in required_paths.items():
        if not path.is_file():
            errors.add(f"lifecycle data missing: {path}")
            continue
        try:
            payloads[name] = load_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.add(f"{path}: {exc}")
    if len(payloads) != len(required_paths):
        return

    calendar = payloads["calendar"]
    errors.require(calendar.get("schema_version") == 1, "workshop calendar schema_version must be 1")
    errors.require(isinstance(calendar.get("base_fatigue"), int) and int(calendar["base_fatigue"]) > 0, "base_fatigue must be a positive integer")
    ratio = calendar.get("carryover_ratio")
    errors.require(_finite_number(ratio) and 0.0 <= float(ratio) <= 1.0, "carryover_ratio must be from 0 to 1")
    action_costs = calendar.get("action_costs", {})
    errors.require(isinstance(action_costs, dict), "action_costs must be an object")
    if isinstance(action_costs, dict):
        for action_id in ("forge", "normal_enhance", "special_enhance", "restore"):
            value = action_costs.get(action_id)
            errors.require(isinstance(value, int) and value > 0, f"action cost {action_id} must be a positive integer")

    grades = payloads["grades"]
    grade_items = grades.get("grades", [])
    errors.require(isinstance(grade_items, list) and len(grade_items) == 5, "craftsmanship grades must contain exactly five entries")
    grade_ids: list[str] = []
    if isinstance(grade_items, list):
        for item in grade_items:
            if not isinstance(item, dict):
                errors.add("craftsmanship grade entry must be an object")
                continue
            grade_id = item.get("id")
            if not isinstance(grade_id, str) or not grade_id:
                errors.add(f"invalid grade id {grade_id!r}")
                continue
            if grade_id in grade_ids:
                errors.add(f"duplicate grade id {grade_id!r}")
            grade_ids.append(grade_id)
            errors.require(isinstance(item.get("score_bonus"), int), f"grade {grade_id} score_bonus must be an integer")
    distributions = grades.get("precision_distributions", {})
    errors.require(isinstance(distributions, dict), "precision_distributions must be an object")
    if isinstance(distributions, dict):
        for precision_id in ("AUTO", "STANDARD", "GOOD", "PERFECT"):
            distribution = distributions.get(precision_id)
            if not isinstance(distribution, dict):
                errors.add(f"distribution {precision_id} must be an object")
                continue
            errors.require(set(distribution) == set(grade_ids), f"distribution {precision_id} must cover all grade ids")
            total = 0.0
            for grade_id, value in distribution.items():
                if not _finite_number(value) or float(value) < 0.0:
                    errors.add(f"distribution {precision_id}.{grade_id} must be a non-negative number")
                    continue
                total += float(value)
            errors.require(abs(total - 1.0) <= 1e-6, f"distribution {precision_id} must sum to 1.0")

    affix_payload = payloads["affixes"]
    affix_ids = {
        item.get("id")
        for item in affix_payload.get("affixes", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    contract = payloads["contract"]
    required_level = contract.get("required_level")
    stretch_level = contract.get("stretch_level")
    errors.require(isinstance(required_level, int) and required_level == 5, "gladiator required_level must be 5")
    errors.require(isinstance(stretch_level, int) and stretch_level == 10, "gladiator stretch_level must be 10")
    errors.require(isinstance(required_level, int) and isinstance(stretch_level, int) and required_level < stretch_level, "required_level must be below stretch_level")
    for affix_id in contract.get("preferred_affix_ids", []):
        errors.require(affix_id in affix_ids, f"unknown preferred affix {affix_id!r}")
    for field, expected in (("deadline_days", 3), ("report_delay_days", 1), ("payment_gold", 500)):
        errors.require(contract.get(field) == expected, f"gladiator {field} must be {expected}")

    activity = payloads["activity"]
    bands = activity.get("result_bands", [])
    errors.require(isinstance(bands, list) and len(bands) >= 3, "result_bands must contain at least three entries")
    band_ids: list[str] = []
    previous = -1
    if isinstance(bands, list):
        for band in bands:
            if not isinstance(band, dict):
                errors.add("result band entry must be an object")
                continue
            band_id = band.get("id")
            minimum = band.get("minimum_score")
            errors.require(isinstance(band_id, str) and bool(band_id), "result band id must be non-empty")
            errors.require(isinstance(minimum, int), f"result band {band_id} minimum_score must be an integer")
            if isinstance(minimum, int):
                errors.require(minimum > previous, "result band minimum_score values must be strictly increasing")
                previous = minimum
            if isinstance(band_id, str):
                band_ids.append(band_id)
    errors.require(band_ids == ["DEFEAT", "WIN", "DECISIVE_WIN"], "result bands must be DEFEAT, WIN, DECISIVE_WIN")

    grade_scores = activity.get("grade_scores", {})
    errors.require(isinstance(grade_scores, dict) and set(grade_scores) == set(grade_ids), "grade_scores must cover all grade ids")
    fixtures = activity.get("reachability_fixtures", [])
    reached: set[str] = set()
    if not isinstance(fixtures, list):
        errors.add("reachability_fixtures must be an array")
        fixtures = []
    for fixture in fixtures:
        if not isinstance(fixture, dict):
            errors.add("reachability fixture must be an object")
            continue
        score = _score_fixture(fixture, contract, activity)
        band = _band_for_score(score, bands)
        errors.require(score == fixture.get("expected_score"), f"fixture {fixture.get('id')} expected_score mismatch: {score}")
        errors.require(band == fixture.get("expected_band"), f"fixture {fixture.get('id')} expected_band mismatch: {band}")
        reached.add(band)
    for band_id in band_ids:
        errors.require(band_id in reached, f"result band {band_id} has no reachable fixture")


def main() -> int:
    errors = ValidationErrors()
    validate_lifecycle_poc(errors)
    if errors.items:
        print("Lifecycle data validation FAILED")
        for item in errors.items:
            print(f"- {item}")
        return 1
    print("Lifecycle data validation PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
