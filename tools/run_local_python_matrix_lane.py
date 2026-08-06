#!/usr/bin/env python3
"""Run one local Python matrix lane against an exact Blacksmith HEAD."""
from __future__ import annotations

import argparse
import json
import platform
import sys
from dataclasses import asdict
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from local_validation_commands import python_matrix_commands
from local_validation_contract import (
    git_output,
    run_command,
    tracked_authoring_hashes,
    utc_now,
)
from local_validation_pack_contract import REQUIRED_MATRIX_LANES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--expected-head", required=True)
    parser.add_argument(
        "--lane-id", choices=tuple(REQUIRED_MATRIX_LANES), required=True
    )
    parser.add_argument(
        "--platform-kind", choices=("windows", "wsl-ubuntu"), required=True
    )
    parser.add_argument("--expected-python", required=True)
    parser.add_argument("--scope", choices=("docs", "code"), default="code")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo_root).resolve()
    output = Path(args.output).resolve()
    log_dir = output.parent / f"{output.stem}-logs"
    head = git_output(repo, "rev-parse", "HEAD")
    clean_before = (
        git_output(repo, "status", "--porcelain", "--untracked-files=no") == ""
    )
    before_hashes = tracked_authoring_hashes(repo)
    actual_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    expected_contract = REQUIRED_MATRIX_LANES[args.lane_id]
    lane_contract_match = expected_contract == (
        args.platform_kind,
        args.expected_python,
    )
    python_version_match = actual_python == args.expected_python

    results = []
    if (
        head == args.expected_head
        and clean_before
        and lane_contract_match
        and python_version_match
    ):
        for name, command in python_matrix_commands(sys.executable, args.scope):
            result = run_command(name, command, repo, log_dir)
            results.append(result)
            if not result.passed:
                break

    after_hashes = tracked_authoring_hashes(repo)
    clean_after = (
        git_output(repo, "status", "--porcelain", "--untracked-files=no") == ""
    )
    authoring_unchanged = before_hashes == after_hashes
    status = (
        "PASS"
        if all(
            (
                head == args.expected_head,
                clean_before,
                clean_after,
                lane_contract_match,
                python_version_match,
                authoring_unchanged,
                bool(results),
                all(result.passed for result in results),
            )
        )
        else "FAIL"
    )
    manifest = {
        "schema_version": "1.0.0",
        "validation_mode": "LOCAL_PYTHON_MATRIX_LANE",
        "lane_id": args.lane_id,
        "platform_kind": args.platform_kind,
        "host_platform": platform.platform(),
        "head_sha": head,
        "expected_head_sha": args.expected_head,
        "exact_head": head == args.expected_head,
        "scope": args.scope,
        "python_required": args.expected_python,
        "python_actual": actual_python,
        "python_version_match": python_version_match,
        "lane_contract_match": lane_contract_match,
        "clean_before": clean_before,
        "clean_after": clean_after,
        "authoring_surface_hash_unchanged": authoring_unchanged,
        "authoring_surface_count": len(before_hashes),
        "commands": [
            asdict(result) | {"passed": result.passed} for result in results
        ],
        "status": status,
        "completed_at": utc_now(),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"lane": args.lane_id, "status": status, "manifest": str(output)},
            ensure_ascii=False,
        )
    )
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
