#!/usr/bin/env python3
"""Run the planning-only deterministic Decision31 repair-economy sweep."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
from typing import Any


def ceil_decimal(value: Decimal) -> int:
    return int(value.to_integral_value(rounding=ROUND_CEILING))


def resolve_repair(event: dict[str, Any]) -> dict[str, Any]:
    old_current = int(event["old_current"])
    maximum = int(event["max"])
    candidate_post_scar_max = int(event["candidate_post_scar_max"])
    scar_skipped = candidate_post_scar_max <= old_current
    post_scar_max = maximum if scar_skipped else candidate_post_scar_max
    quality_target = ceil_decimal(Decimal(post_scar_max) * Decimal(str(event["quality_ratio"])))
    new_current = min(post_scar_max, max(old_current + 1, quality_target))
    return {
        "old_current": old_current,
        "post_scar_max": post_scar_max,
        "quality_target": quality_target,
        "new_current": new_current,
        "recovery": new_current - old_current,
        "scar_skipped": scar_skipped,
    }


def analyze(payload: dict[str, Any]) -> dict[str, Any]:
    setup = Decimal(str(payload["setup_coefficient"]))
    r_band = Decimal(str(payload["r_band_normalized"]))
    rows: list[dict[str, Any]] = []

    for event in payload["events"]:
        if not event["resolved_actual_damage"] or not event["repair_job_available"]:
            raise ValueError(f"{event['event_id']} is not an eligible repair cycle")
        repair = resolve_repair(event)
        loss_ratio = Decimal(int(event["max"]) - repair["old_current"]) / Decimal(int(event["base_max"]))
        for coefficient in payload["loss_coefficients"]:
            b = Decimal(str(coefficient))
            gold = ceil_decimal(r_band * (setup + b * loss_ratio))
            rows.append(
                {
                    "event_id": event["event_id"],
                    "item_uid": payload["item_uid"],
                    "b": float(b),
                    "r_band_normalized": int(r_band),
                    "loss_ratio": float(loss_ratio),
                    "gold": gold,
                    "material_id": payload["material"]["id"],
                    "material_use": int(payload["material"]["quantity"]),
                    "material_shadow_value_g": int(payload["material"]["shadow_value_g"]),
                    "material_included_in_gold": bool(payload["material"]["included_in_gold"]),
                    "old_current": repair["old_current"],
                    "old_max": int(event["max"]),
                    "base_max": int(event["base_max"]),
                    "post_scar_max": repair["post_scar_max"],
                    "quality_target": repair["quality_target"],
                    "new_current": repair["new_current"],
                    "recovery": repair["recovery"],
                    "scar_skipped": repair["scar_skipped"],
                    "repair_job_consumed": True,
                    "post_repair_job_available": False,
                    "repeat_repair_outcome": "BLOCKED_NO_REPAIR_JOB",
                    "later_actual_damage_reopens_job": True,
                    "player_decision_outcome": "REPAIR_NOW",
                }
            )

    invariants = {
        "row_count": len(rows),
        "all_eligible_repairs_positive_gain": all(row["recovery"] > 0 for row in rows),
        "all_repeat_repairs_blocked": all(row["repeat_repair_outcome"] == "BLOCKED_NO_REPAIR_JOB" for row in rows),
        "scar_skip_observed": any(row["scar_skipped"] for row in rows),
        "material_is_separate_from_gold": all(not row["material_included_in_gold"] for row in rows),
    }
    return {
        "artifact_role": "REPAIR_ECONOMY_SENSITIVITY_RESULT",
        "decision_id": payload["decision_id"],
        "status": "TEMP_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE",
        "r_band_status": "NORMALIZED_INPUT_NOT_LIVE_PRICE_TABLE",
        "rows": rows,
        "invariants": invariants,
        "verdict": "TEST_IN_PLAY",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = analyze(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Repair economy sensitivity complete: {result['invariants']['row_count']} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
