#!/usr/bin/env python3
"""Aggregate authoritative Windows and Windows/WSL Python lane manifests."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from local_validation_pack_contract import evaluate_pack


def load_json(path: str) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--full-manifest", required=True)
    parser.add_argument("--lane-manifest", action="append", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    full = load_json(args.full_manifest)
    lanes = [load_json(path) for path in args.lane_manifest]
    evaluation = evaluate_pack(full, lanes, args.expected_head)
    manifest = {
        "schema_version": "1.0.0",
        "validation_mode": "WINDOWS_WSL2_LOCAL_VALIDATION_PACK",
        "expected_head_sha": args.expected_head,
        "status": evaluation.status,
        "full_lane_valid": evaluation.full_lane_valid,
        "missing_lanes": evaluation.missing_lanes,
        "failed_lanes": evaluation.failed_lanes,
        "full_manifest": str(Path(args.full_manifest).resolve()),
        "lane_manifests": [
            str(Path(path).resolve()) for path in args.lane_manifest
        ],
    }
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"status": evaluation.status, "manifest": str(output)},
            ensure_ascii=False,
        )
    )
    return 0 if evaluation.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
