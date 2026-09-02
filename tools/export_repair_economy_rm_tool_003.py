#!/usr/bin/env python3
"""Project-owned Decision31 adapter for Base RM-TOOL-003 analysis.

This module does not implement repair rules. It calls the current Blacksmith
planning model, projects its deterministic rows into the provider-neutral Base
manifest, and preserves the planning/runtime/Human claim ceiling.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from decimal import Decimal
from pathlib import Path
from statistics import median
from types import ModuleType
from typing import Any


DECISION_ID = "BS-REPAIR-20260826-31"
BASE_SOURCE_COMMIT = "aaa94caf5772c262f023dd9e80fd4b8bbffd85db"
BASE_ANALYZER_BLOB_SHA = "a99ae419fd755b6e19f3dee232dd3a11cd74d4ae"
BASE_DEPENDENCY_ROLE = "READ_ONLY_EXACT_ANALYZER_NOT_PROJECT_BASE_RELEASE_ADOPTION"
BASE_UPDATE_POLICY = "MANUAL_REVALIDATION_REQUIRED_BEFORE_PIN_CHANGE"
SEED_SEMANTICS = "DETERMINISTIC_PROJECT_CASE_PAIRING_ID_NOT_RNG_SAMPLE"
CANON_RELATIVE_PATH = Path("docs/planning/BLACKSMITH_REPAIR_ECONOMY_REBASE_20260826.json")
INPUT_RELATIVE_PATH = Path("docs/planning/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_INPUT_20260826.json")
RUNNER_RELATIVE_PATH = Path("tools/run_repair_economy_sensitivity.py")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


class IntegrationContractError(ValueError):
    pass


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise IntegrationContractError(f"could not read JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise IntegrationContractError(f"JSON root must be an object: {path}")
    return payload


def _load_runner(path: Path) -> ModuleType:
    if not path.is_file():
        raise IntegrationContractError(f"current repair sensitivity runner is missing: {path}")
    spec = importlib.util.spec_from_file_location("blacksmith_current_repair_economy_runner", path)
    if spec is None or spec.loader is None:
        raise IntegrationContractError(f"could not load current repair sensitivity runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if not callable(getattr(module, "analyze", None)):
        raise IntegrationContractError("current repair sensitivity runner does not export analyze(payload)")
    return module


def _decimal(value: Any, *, label: str) -> Decimal:
    if isinstance(value, bool):
        raise IntegrationContractError(f"{label} must be numeric")
    try:
        result = Decimal(str(value))
    except Exception as exc:
        raise IntegrationContractError(f"{label} must be numeric") from exc
    if not result.is_finite():
        raise IntegrationContractError(f"{label} must be finite")
    return result


def _decimal_key(value: Any, *, label: str) -> str:
    number = _decimal(value, label=label).normalize()
    return format(number, "f")


def _variant_id(value: Any) -> str:
    normalized = _decimal_key(value, label="loss coefficient")
    safe = normalized.replace("-", "neg_").replace(".", "p")
    return f"loss_b_{safe}"


def _stable_seed(event_id: str) -> int:
    digest = hashlib.sha256(f"{DECISION_ID}:{event_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") & ((1 << 63) - 1)


def _sha256_json(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validate_current_contract(
    canon: dict[str, Any], sensitivity_input: dict[str, Any]
) -> tuple[list[Decimal], Decimal, list[dict[str, Any]]]:
    if canon.get("decision_id") != DECISION_ID or sensitivity_input.get("decision_id") != DECISION_ID:
        raise IntegrationContractError(f"current decision must be {DECISION_ID}")
    if canon.get("scope") != "PLANNING_ONLY":
        raise IntegrationContractError("Decision31 scope must remain PLANNING_ONLY")
    if canon.get("numeric_status") != "TEMPORARY_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE":
        raise IntegrationContractError("Decision31 numeric status was promoted unexpectedly")
    if sensitivity_input.get("status") != "TEMP_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE":
        raise IntegrationContractError("sensitivity input must remain a temporary test budget")

    sensitivity = canon.get("sensitivity")
    if not isinstance(sensitivity, dict):
        raise IntegrationContractError("Decision31 sensitivity contract is missing")
    baseline = _decimal(sensitivity.get("baseline_loss_coefficient"), label="baseline loss coefficient")
    canon_sweep_raw = sensitivity.get("loss_coefficient_sweep")
    input_sweep_raw = sensitivity_input.get("loss_coefficients")
    if not isinstance(canon_sweep_raw, list) or not isinstance(input_sweep_raw, list):
        raise IntegrationContractError("loss coefficient sweep must be an array")
    canon_sweep = [_decimal(value, label="canon loss coefficient") for value in canon_sweep_raw]
    input_sweep = [_decimal(value, label="input loss coefficient") for value in input_sweep_raw]
    if canon_sweep != input_sweep:
        raise IntegrationContractError("input loss coefficient sweep must match current Decision31 canon")
    if len(set(canon_sweep)) != len(canon_sweep):
        raise IntegrationContractError("loss coefficient sweep values must be unique")
    if baseline not in canon_sweep:
        raise IntegrationContractError("baseline loss coefficient must be one of the sweep values")

    events = sensitivity_input.get("events")
    if not isinstance(events, list) or not events:
        raise IntegrationContractError("sensitivity events must be a non-empty array")
    event_ids: list[str] = []
    normalized_events: list[dict[str, Any]] = []
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise IntegrationContractError(f"event {index} must be an object")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id.strip():
            raise IntegrationContractError(f"event {index} requires event_id")
        event_id = event_id.strip()
        if event_id in event_ids:
            raise IntegrationContractError(f"duplicate event_id: {event_id}")
        event_ids.append(event_id)
        normalized_events.append(event)

    seeds = [_stable_seed(event_id) for event_id in event_ids]
    if len(set(seeds)) != len(seeds):
        raise IntegrationContractError("stable event seed collision")
    return canon_sweep, baseline, normalized_events


def build_manifest(
    canon: dict[str, Any],
    sensitivity_input: dict[str, Any],
    *,
    source_commit: str,
    canon_path: str = CANON_RELATIVE_PATH.as_posix(),
    input_path: str = INPUT_RELATIVE_PATH.as_posix(),
    runner: ModuleType | None = None,
) -> dict[str, Any]:
    if not isinstance(source_commit, str) or not COMMIT_RE.fullmatch(source_commit):
        raise IntegrationContractError("source_commit must be an exact 40-character Git SHA")
    coefficients, baseline, events = _validate_current_contract(canon, sensitivity_input)
    runner = runner or _load_runner(Path(__file__).resolve().parent / "run_repair_economy_sensitivity.py")
    result = runner.analyze(copy.deepcopy(sensitivity_input))
    if not isinstance(result, dict) or result.get("decision_id") != DECISION_ID:
        raise IntegrationContractError("current repair model returned a mismatched decision")
    if result.get("status") != "TEMP_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE":
        raise IntegrationContractError("current repair model evidence status was promoted unexpectedly")
    rows = result.get("rows")
    if not isinstance(rows, list):
        raise IntegrationContractError("current repair model rows are missing")
    expected_row_count = len(events) * len(coefficients)
    if len(rows) != expected_row_count:
        raise IntegrationContractError(f"current repair model row count mismatch: {len(rows)} != {expected_row_count}")

    row_by_identity: dict[tuple[str, str], dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise IntegrationContractError(f"model row {index} must be an object")
        event_id = row.get("event_id")
        if not isinstance(event_id, str):
            raise IntegrationContractError(f"model row {index} requires event_id")
        coefficient_key = _decimal_key(row.get("b"), label=f"model row {index} coefficient")
        identity = (event_id, coefficient_key)
        if identity in row_by_identity:
            raise IntegrationContractError(f"duplicate model row identity: {identity}")
        row_by_identity[identity] = row

    runs: list[dict[str, Any]] = []
    gold_by_variant: dict[str, list[float]] = {}
    for coefficient in coefficients:
        coefficient_key = _decimal_key(coefficient, label="loss coefficient")
        variant = _variant_id(coefficient)
        gold_by_variant[variant] = []
        for event in events:
            event_id = str(event["event_id"]).strip()
            row = row_by_identity.get((event_id, coefficient_key))
            if row is None:
                raise IntegrationContractError(f"current repair model omitted event/coefficient row: {event_id}/{coefficient_key}")

            failures: list[str] = []
            if int(row["recovery"]) <= 0:
                failures.append("NON_POSITIVE_REPAIR_GAIN")
            if row.get("repeat_repair_outcome") != "BLOCKED_NO_REPAIR_JOB":
                failures.append("REPEAT_REPAIR_NOT_BLOCKED")
            if bool(row.get("material_included_in_gold")):
                failures.append("MATERIAL_INCLUDED_IN_GOLD")

            metrics = {
                "gold": int(row["gold"]),
                "recovery": int(row["recovery"]),
                "loss_ratio": float(row["loss_ratio"]),
                "new_current": int(row["new_current"]),
                "post_scar_max": int(row["post_scar_max"]),
                "material_use": int(row["material_use"]),
                "scar_skip_flag": 1 if bool(row["scar_skipped"]) else 0,
            }
            gold_by_variant[variant].append(float(metrics["gold"]))
            runs.append(
                {
                    "seed": _stable_seed(event_id),
                    "variant": variant,
                    "project_case_id": event_id,
                    "parameters": {"loss_coefficient_b": float(coefficient)},
                    "metrics": metrics,
                    "choices": [str(row["player_decision_outcome"])],
                    "failures": failures,
                }
            )

    baseline_variant = _variant_id(baseline)
    baseline_median = float(median(gold_by_variant[baseline_variant]))
    setup_coefficient = float(_decimal(sensitivity_input.get("setup_coefficient"), label="setup coefficient"))
    r_band = int(sensitivity_input["r_band_normalized"])
    material = sensitivity_input.get("material", {})

    return {
        "schema_version": 1,
        "project_id": "BLACKSMITH",
        "snapshot": {
            "source_commit": source_commit.lower(),
            "canon_path": canon_path,
            "canon_payload_sha256": _sha256_json(canon),
            "input_path": input_path,
            "input_payload_sha256": _sha256_json(sensitivity_input),
        },
        "baseline_variant": baseline_variant,
        "analysis_context": {
            "adapter_evidence_mode": "MATHEMATICAL_MODEL",
            "adapter_equivalence": {"status": "NOT_VERIFIED"},
        },
        "integration_context": {
            "decision_id": DECISION_ID,
            "numeric_status": canon["numeric_status"],
            "model_artifact_role": result.get("artifact_role"),
            "base_source_commit": BASE_SOURCE_COMMIT,
            "base_analyzer_blob_sha": BASE_ANALYZER_BLOB_SHA,
            "base_dependency_role": BASE_DEPENDENCY_ROLE,
            "base_update_policy": BASE_UPDATE_POLICY,
            "seed_semantics": SEED_SEMANTICS,
            "project_rule_owner": RUNNER_RELATIVE_PATH.as_posix(),
            "projection_owner": "tools/export_repair_economy_rm_tool_003.py",
            "baseline_median_target_role": "CURRENT_BASELINE_MEDIAN_SMOKE_ONLY_NOT_DESIGN_TARGET",
        },
        "evidence_ceiling": [
            "PLANNING_MODEL_ONLY",
            "RUNTIME_EQUIVALENCE_NOT_VERIFIED",
            "FINAL_PRODUCT_BALANCE_NOT_APPROVED",
            "HUMAN_PLAYER_EVIDENCE_NOT_RUN",
        ],
        "runs": runs,
        "parameter_sweeps": [
            {
                "parameter": "loss_coefficient_b",
                "metric": "gold",
                "summary_stat": "median",
                "target": baseline_median,
                "target_role": "CURRENT_BASELINE_MEDIAN_SMOKE_ONLY_NOT_DESIGN_TARGET",
                "locked_parameters": [
                    f"setup_coefficient={setup_coefficient}",
                    f"r_band_normalized={r_band}",
                    "same_deterministic_project_case_set",
                    "same_quality_scar_stream",
                    f"material_id={material.get('id')}",
                    f"material_quantity={material.get('quantity')}",
                ],
                "points": [
                    {"value": float(coefficient), "variant": _variant_id(coefficient)}
                    for coefficient in coefficients
                ],
            }
        ],
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    root = args.project_root.resolve()
    canon_path = root / CANON_RELATIVE_PATH
    input_path = root / INPUT_RELATIVE_PATH
    runner_path = root / RUNNER_RELATIVE_PATH
    try:
        manifest = build_manifest(
            _load_json(canon_path),
            _load_json(input_path),
            source_commit=args.source_commit,
            canon_path=CANON_RELATIVE_PATH.as_posix(),
            input_path=INPUT_RELATIVE_PATH.as_posix(),
            runner=_load_runner(runner_path),
        )
        atomic_write_json(args.output.resolve(), manifest)
    except IntegrationContractError as exc:
        print(f"repair economy RM-TOOL-003 export rejected: {exc}", file=sys.stderr)
        return 2

    print(
        json.dumps(
            {
                "decision_id": DECISION_ID,
                "run_count": len(manifest["runs"]),
                "variant_count": len(manifest["parameter_sweeps"][0]["points"]),
                "base_source_commit": BASE_SOURCE_COMMIT,
                "base_analyzer_blob_sha": BASE_ANALYZER_BLOB_SHA,
                "evidence_ceiling": manifest["evidence_ceiling"],
                "output": str(args.output.resolve()),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
