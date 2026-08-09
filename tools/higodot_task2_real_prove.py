from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
from pathlib import Path
from typing import Any

try:
    from tools import higodot_task2_bridge as bridge
except ModuleNotFoundError:  # Direct execution: python tools/higodot_task2_real_prove.py
    import higodot_task2_bridge as bridge


_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_EXPECTED_CONTEXT_PATH = "artifacts/higodot-task2/session-context.json"
_EXPECTED_OPERATIONS_PATH = "artifacts/higodot-task2/operation-evidence.json"


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


def _git(
    repo: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        capture_output=True,
        text=True,
    )


def _is_tracked(repo: Path, relative_path: str) -> bool:
    result = _git(
        repo,
        "ls-files",
        "--error-unmatch",
        "--",
        relative_path,
        check=False,
    )
    return result.returncode == 0


def _require_exact_evidence_path(repo: Path, path: Path, expected: str) -> str:
    candidate = path if path.is_absolute() else repo / path
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(repo).as_posix()
    except ValueError as exc:
        raise ValueError("PROVE evidence path must stay inside the project repository") from exc
    if relative != expected:
        raise ValueError(f"PROVE evidence path must equal {expected}")
    if not resolved.is_file():
        raise ValueError(f"PROVE evidence path is missing: {expected}")
    if _is_tracked(repo, relative):
        raise ValueError(f"PROVE evidence path must remain untracked: {expected}")
    return relative


def register_runtime_byproduct_excludes(
    repo: Path,
    context_out: Path,
    operations_out: Path,
) -> None:
    """Hide only validated ephemeral PROVE byproducts from the strict product diff."""
    repo = repo.resolve()
    top_level = Path(_git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if top_level != repo:
        raise ValueError("PROVE project path must be the Git repository root")

    excluded = [
        _require_exact_evidence_path(repo, context_out, _EXPECTED_CONTEXT_PATH),
        _require_exact_evidence_path(repo, operations_out, _EXPECTED_OPERATIONS_PATH),
    ]

    untracked = _git(repo, "ls-files", "--others", "--exclude-standard").stdout.splitlines()
    for relative in sorted(path for path in untracked if path.endswith(".gd.uid")):
        source_relative = relative[: -len(".uid")]
        source_path = repo / source_relative
        if not source_path.is_file() or not _is_tracked(repo, source_relative):
            raise ValueError(
                f"generated .gd.uid requires paired tracked .gd: {relative}"
            )
        excluded.append(relative)

    git_exclude_value = _git(repo, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    exclude_path = Path(git_exclude_value)
    if not exclude_path.is_absolute():
        exclude_path = repo / exclude_path
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
    existing_lines = set(existing.splitlines())
    additions = [f"/{relative}" for relative in excluded if f"/{relative}" not in existing_lines]
    if not additions:
        return
    prefix = "" if not existing or existing.endswith("\n") else "\n"
    exclude_path.write_text(
        existing + prefix + "\n".join(additions) + "\n",
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
        default=Path(_EXPECTED_CONTEXT_PATH),
    )
    parser.add_argument(
        "--operations-out",
        type=Path,
        default=Path(_EXPECTED_OPERATIONS_PATH),
    )
    return parser


async def _run_cli(args: argparse.Namespace) -> None:
    recipe = bridge.load_recipe(args.recipe)
    async with bridge.FastMCPBridgeClient() as client:
        result = await run_prove(client, recipe, args.project_path, args.expected_head)
    write_prove_evidence(result, args.context_out, args.operations_out)
    register_runtime_byproduct_excludes(
        Path(args.project_path),
        args.context_out,
        args.operations_out,
    )


def main() -> None:
    args = _build_parser().parse_args()
    if args.command != "prove":
        raise SystemExit("unsupported command")
    asyncio.run(_run_cli(args))


if __name__ == "__main__":
    main()
