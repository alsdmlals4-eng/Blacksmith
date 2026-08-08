from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path
from typing import Any

try:
    from tools import higodot_task2_bridge as bridge
except ModuleNotFoundError:  # Direct execution: python tools/higodot_task2_real_prove.py
    import higodot_task2_bridge as bridge


_SHA40 = re.compile(r"^[0-9a-f]{40}$")


async def run_prove(
    client,
    recipe: dict[str, Any],
    expected_project_path: str,
    expected_head: str,
) -> dict[str, Any]:
    """Run one fail-closed HiGodot PROVE transaction and return hash-only evidence."""
    if not isinstance(expected_head, str) or _SHA40.fullmatch(expected_head) is None:
        raise ValueError("expected_head must be a lowercase 40-hex commit SHA")
    bridge.validate_recipe(recipe)
    bridge.validate_executable_recipe(recipe)

    preflight = await bridge.preflight_mcp(client, recipe, expected_project_path)
    session_id = str(preflight["session_id"])
    operations = await bridge.execute_recipe_operations(client, recipe, session_id)
    if len(operations) != len(recipe["operations"]):
        raise ValueError("operation evidence count does not match the approved recipe")

    context = {
        "decision_ids": [
            bridge.DECISION_ID,
            "BS-HIGODOT-20260808-01",
            "BS-VS-TASK2-20260807-01",
        ],
        "repository": bridge.TARGET_REPOSITORY,
        "pr_number": bridge.TARGET_PR,
        "input_head_sha": expected_head,
        "godot": {"version": bridge.TARGET_GODOT_VERSION},
        "higodot": {"version": bridge.TARGET_HIGODOT_VERSION},
        "server": {"version": bridge.TARGET_HIGODOT_VERSION},
        "session": {
            "id": session_id,
            "project_path": expected_project_path,
        },
        "changed_paths": sorted(bridge.ALLOWED_SERIALIZED_PATHS),
    }
    return {"context": context, "operations": operations}


def write_prove_evidence(
    result: dict[str, Any],
    context_out: Path,
    operations_out: Path,
) -> None:
    if set(result) != {"context", "operations"}:
        raise ValueError("PROVE result must contain context and operations only")
    if not isinstance(result["context"], dict) or not isinstance(result["operations"], list):
        raise ValueError("PROVE result has invalid evidence shape")
    context_out.parent.mkdir(parents=True, exist_ok=True)
    operations_out.parent.mkdir(parents=True, exist_ok=True)
    context_out.write_text(
        json.dumps(result["context"], sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    operations_out.write_text(
        json.dumps(result["operations"], sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Blacksmith Task 2 real HiGodot PROVE orchestrator")
    parser.add_argument("command", choices=["prove"])
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--project-path", required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument(
        "--context-out",
        type=Path,
        default=Path("artifacts/higodot-task2/session-context.json"),
    )
    parser.add_argument(
        "--operations-out",
        type=Path,
        default=Path("artifacts/higodot-task2/operation-evidence.json"),
    )
    return parser


async def _run_cli(args: argparse.Namespace) -> None:
    recipe = bridge.load_recipe(args.recipe)
    async with bridge.FastMCPBridgeClient() as client:
        result = await run_prove(client, recipe, args.project_path, args.expected_head)
    write_prove_evidence(result, args.context_out, args.operations_out)


def main() -> None:
    args = _build_parser().parse_args()
    if args.command != "prove":
        raise SystemExit("unsupported command")
    asyncio.run(_run_cli(args))


if __name__ == "__main__":
    main()
