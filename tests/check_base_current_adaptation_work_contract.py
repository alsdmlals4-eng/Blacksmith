#!/usr/bin/env python3
from __future__ import annotations

"""Fail closed unless the current Base adaptation contract is consumable."""

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md"
RECEIPT = (
    ROOT
    / "docs/operations/receipts/2026-09-01-base-current-adaptation-work-contract.json"
)
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
AGENTS = ROOT / "AGENTS.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
AUTHORITY_INDEX = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
BASE_RULES = ROOT / "docs/BASE_RULES_VERSION.md"
WORKFLOW = ROOT / ".github/workflows/validate-current-base-adaptation-work-contract.yml"
EXPECTED_RELEASE = "9.4.4"
EXPECTED_RELEASE_COMMIT = "210ec78292fa12ed7563ba743b322dd36103ae4a"
EXPECTED_BASE_CURRENT = "19355b7ef065a21d0f2b685c7d9be64a4a3970f8"
REQUIRED_MODES = ("PLAN", "NONCODING_BUILD", "GODOT_PRODUCT_BUILD", "REVIEW")


def require_file(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing required current Base adaptation path: {path.relative_to(ROOT)}")


def main() -> int:
    failures: list[str] = []
    for path in (CONTRACT, RECEIPT, WORKFLOW):
        require_file(path, failures)

    if failures:
        print("Base current adaptation work contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
    if adapter["base_release"]["version"] != EXPECTED_RELEASE:
        failures.append("adapter no longer holds the adopted Base v9.4.4 release lock")
    if adapter["base_release"]["release_commit"] != EXPECTED_RELEASE_COMMIT:
        failures.append("adapter no longer holds the adopted Base v9.4.4 release commit")

    contract = CONTRACT.read_text(encoding="utf-8")
    for token in (EXPECTED_BASE_CURRENT, EXPECTED_RELEASE, *REQUIRED_MODES):
        if token not in contract:
            failures.append(f"current Base adaptation contract missing operational marker: {token}")
    for token in (
        "GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE",
        "NOTION_STATUS = HISTORICAL_REFERENCE_ONLY / NO_FUTURE_READ_WRITE_REQUIRED",
        "GOOGLE_SHEET_STATUS = HISTORICAL_MIGRATION_ONLY / NO_FUTURE_WRITE_REQUIRED",
        "NO_AUTOMATIC_BASE_PIN_UPDATE = TRUE",
        "NO_PRODUCT_PATH_CHANGE = TRUE",
        "OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER",
        "NO_DIRECT_MAIN_PUSH = TRUE",
        "NO_FORCE_PUSH = TRUE",
    ):
        if token not in contract:
            failures.append(f"current Base adaptation contract missing boundary: {token}")

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if receipt.get("work_level") != "L3":
        failures.append("current Base adaptation receipt must be L3")
    if receipt.get("base_current_main_observed") != EXPECTED_BASE_CURRENT:
        failures.append("receipt must retain the exact Base current observation")
    if receipt.get("base_adopted_release", {}).get("version") != EXPECTED_RELEASE:
        failures.append("receipt must retain the adopted Base v9.4.4 release")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    for token in (
        EXPECTED_BASE_CURRENT,
        "BLACKSMITH_BASE_ROOT",
        "tests/check_base_current_adaptation_work_contract.py",
    ):
        if token not in workflow:
            failures.append(f"current Base adaptation CI workflow missing required marker: {token}")

    for path in (AGENTS, HANDOFF, AUTHORITY_INDEX, BASE_RULES):
        if CONTRACT.relative_to(ROOT).as_posix() not in path.read_text(encoding="utf-8"):
            failures.append(f"current entrypoint does not route to the Base adaptation contract: {path.relative_to(ROOT)}")

    base_root = Path(
        os.environ.get("BLACKSMITH_BASE_ROOT", r"C:\Users\user\Documents\GitHub\Base")
    )
    validator = base_root / "tools/validate_work_contract_receipt.py"
    if not validator.exists():
        failures.append(f"Base receipt validator unavailable: {validator}")
    else:
        completed = subprocess.run(
            [sys.executable, str(validator), "--receipt", str(RECEIPT)],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = (completed.stdout + completed.stderr).strip().replace("\n", " | ")
            failures.append(f"Base receipt validator rejected current receipt: {detail}")

    if failures:
        print("Base current adaptation work contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Base current adaptation work contract PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
