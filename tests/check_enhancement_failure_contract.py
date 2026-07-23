#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def read_json(relative_path: str) -> dict[str, object]:
    value = json.loads(read_text(relative_path))
    if not isinstance(value, dict):
        raise ValueError(f"{relative_path}: root must be an object")
    return value


failures: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


balance = read_json("data/crafting/enhancement_balance.json")
milestones = read_json("data/crafting/enhancement_milestones.json")

require(
    balance.get("schema_version") == 3,
    "enhancement_balance.json schema_version must be 3",
)
require(
    milestones.get("schema_version") == 2,
    "enhancement_milestones.json schema_version must be 2",
)
require(
    "failure_policy" not in milestones,
    "enhancement_milestones.json must not own failure_policy",
)
require(
    balance.get("failure_policy")
    == {
        "consume_materials_on_attempt_start": True,
        "pity_resets_on_success": True,
        "pity_survives_downgrade": True,
    },
    "enhancement_balance.json canonical failure_policy mismatch",
)

risk = balance.get("risk", {})
require(isinstance(risk, dict), "enhancement_balance.json risk must be an object")
if isinstance(risk, dict):
    for field_name in (
        "downgrade_ratio_by_decade",
        "destroy_ratio_by_decade",
        "downgrade_steps_by_decade",
    ):
        table = risk.get(field_name, {})
        require(
            isinstance(table, dict) and "10" not in table,
            f"unreachable decade 10 remains in risk.{field_name}",
        )

session_source = read_text("scripts/enhancement/enhancement_session.gd")
resources_source = read_text("scripts/economy/workshop_resources.gd")

require(
    "failure_streak = 0" in session_source,
    "successful enhancement must reset failure_streak",
)
require(
    session_source.count("failure_streak += 1") >= 2,
    "hold and downgrade outcomes must both preserve/increase pity",
)
require(
    "destroyed = true" in session_source
    and "state = State.COMPLETE" in session_source,
    "destroy outcome must destroy the weapon and finish the session",
)

secondary_consume = "_consume_material(secondary_id)"
catalyst_consume = "_consume_material(catalyst_id)"
begin_attempt = "session.begin_attempt"
require(
    secondary_consume in resources_source and catalyst_consume in resources_source,
    "special enhancement material consumption is missing",
)
if secondary_consume in resources_source and begin_attempt in resources_source:
    require(
        resources_source.index(secondary_consume)
        < resources_source.index(begin_attempt),
        "selected materials must be consumed before session.begin_attempt",
    )
require(
    "_restore_material(secondary_id)" in resources_source
    and "_restore_material(catalyst_id)" in resources_source,
    "failed attempt start must restore selected materials",
)

ownership_documents = (
    "README.md",
    "docs/MVP-002_SCOPE.md",
    "docs/GODOT_PLAYTEST.md",
    "tests/README.md",
    "tests/SPECIAL_ENHANCEMENT_VALIDATION.md",
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "[기획서]/00_프로젝트_허브/DECISION_LOG.md",
)
for relative_path in ownership_documents:
    source = read_text(relative_path)
    require(
        "enhancement_balance.json" in source,
        f"failure/risk owner is missing from {relative_path}",
    )
    require(
        "enhancement_milestones.json" in source,
        f"milestone owner is missing from {relative_path}",
    )

workflow_source = read_text(".github/workflows/data-validation.yml")
require(
    "python tests/check_enhancement_failure_contract.py" in workflow_source,
    "Data validation workflow does not run the enhancement failure contract",
)
require(
    "tests/test_documentation_governance.py" in workflow_source
    and "libreoffice-writer" in workflow_source,
    "Data validation workflow must preserve the full Base regression contract",
)

if failures:
    print("Enhancement failure contract FAILED")
    for failure in failures:
        print(f"ERROR: {failure}")
    raise SystemExit(1)

print("Enhancement failure contract PASSED")
