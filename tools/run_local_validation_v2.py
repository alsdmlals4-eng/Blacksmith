#!/usr/bin/env python3
"""Fail-closed local replacement for GitHub-hosted PR validation."""
from __future__ import annotations

import argparse
import json
import platform
import re
import sys
from dataclasses import asdict
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from local_validation_commands import godot_commands, python_commands
from local_validation_contract import (
    BASE_CONTRACT_PIN, BASE_OPERATING_PIN, PYTHON_MAJOR_MINOR, CommandResult,
    base_v9_changed_paths_allowed, git_output, git_succeeds, run_command,
    summarize_status, tracked_authoring_hashes, utc_now, validate_logged_result,
    workflow_has_exact_ref, is_authoring_surface, sha256_file,
)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--pr-base-sha", required=True)
    parser.add_argument("--base-root", required=True)
    parser.add_argument("--base-contract-root", required=True)
    parser.add_argument("--godot")
    parser.add_argument("--scope", choices=("docs", "code"), default="code")
    parser.add_argument("--require-godot", action="store_true")
    parser.add_argument("--output", required=True)
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    repo = Path(args.repo_root).resolve()
    output = Path(args.output).resolve()
    log_dir = output.parent / f"{output.stem}-logs"
    operating_base = Path(args.base_root).resolve()
    contract_base = Path(args.base_contract_root).resolve()
    head = git_output(repo, "rev-parse", "HEAD")
    exact_head = head == args.expected_head
    clean_before = git_output(repo, "status", "--porcelain", "--untracked-files=no") == ""
    before_hashes = tracked_authoring_hashes(repo)

    pr_base_valid = bool(re.fullmatch(r"[0-9a-f]{40}", args.pr_base_sha)) and git_succeeds(repo, "cat-file", "-e", f"{args.pr_base_sha}^{{commit}}")
    changed_paths = git_output(repo, "diff", "--name-only", f"{args.pr_base_sha}...HEAD").splitlines() if pr_base_valid else []
    base_v9_scope_ok = pr_base_valid and base_v9_changed_paths_allowed(changed_paths)
    base_v9_adapter_present = (repo / "skills" / "BASE_V9_ADAPTER.json").is_file()

    adapter_changed = "skills/PROJECT_BASE_ADAPTER.json" in changed_paths
    protected_base_sha = None
    try:
        adapter = json.loads((repo / "skills" / "PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        protected_base_sha = args.pr_base_sha if adapter_changed else adapter["protected_baseline"]["commit"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError):
        pass
    protected_base_valid = bool(
        protected_base_sha and re.fullmatch(r"[0-9a-f]{40}", protected_base_sha)
        and git_succeeds(repo, "cat-file", "-e", f"{protected_base_sha}^{{commit}}")
        and git_succeeds(repo, "merge-base", "--is-ancestor", protected_base_sha, args.pr_base_sha)
    )

    operating_head = git_output(operating_base, "rev-parse", "HEAD") if (operating_base / ".git").exists() else None
    contract_head = git_output(contract_base, "rev-parse", "HEAD") if (contract_base / ".git").exists() else None
    operating_pin_match = operating_head == BASE_OPERATING_PIN
    contract_pin_match = contract_head == BASE_CONTRACT_PIN
    python_version_match = sys.version_info[:2] == PYTHON_MAJOR_MINOR
    workflow_operating_pin_match = workflow_has_exact_ref(repo / ".github/workflows/python-validation.yml", BASE_OPERATING_PIN)
    workflow_contract_pin_match = workflow_has_exact_ref(repo / ".github/workflows/validate-project-base-adapter.yml", BASE_CONTRACT_PIN)
    contract_consistent = all((python_version_match, pr_base_valid, base_v9_scope_ok, base_v9_adapter_present, protected_base_valid, workflow_operating_pin_match, workflow_contract_pin_match))

    results: list[CommandResult] = []
    if contract_consistent:
        for name, command in python_commands(sys.executable, args.scope, operating_base, contract_base, protected_base_sha, args.pr_base_sha):
            result = run_command(name, command, repo, log_dir)
            results.append(result)
            if not result.passed:
                break

    godot_required = args.require_godot or args.scope == "code"
    godot_present = bool(args.godot and Path(args.godot).is_file())
    if contract_consistent and all(result.passed for result in results) and godot_present:
        (repo / "artifacts/gut").mkdir(parents=True, exist_ok=True)
        for name, command in godot_commands(str(Path(args.godot).resolve()), repo):
            result = validate_logged_result(run_command(name, command, repo, log_dir))
            results.append(result)
            if not result.passed:
                break

    after_hashes = tracked_authoring_hashes(repo)
    authoring_unchanged = before_hashes == after_hashes
    clean_after = git_output(repo, "status", "--porcelain", "--untracked-files=no") == ""
    bases_ready = operating_pin_match and contract_pin_match
    status = summarize_status(results, exact_head, clean_before, clean_after, authoring_unchanged, bases_ready, godot_present, godot_required, contract_consistent)
    manifest = {
        "schema_version": "1.1.0", "validation_mode": "LOCAL_EXACT_HEAD_NO_GITHUB_ACTIONS",
        "head_sha": head, "expected_head_sha": args.expected_head, "pr_base_sha": args.pr_base_sha,
        "exact_head": exact_head, "scope": args.scope, "status": status,
        "environment": {"platform": platform.platform(), "python": sys.version, "python_required": "3.12.x", "python_version_match": python_version_match, "working_directory": str(repo)},
        "changed_paths": changed_paths, "base_v9_scope_ok": base_v9_scope_ok,
        "base_v9_adapter_present": base_v9_adapter_present, "protected_base_sha": protected_base_sha,
        "protected_base_valid": protected_base_valid,
        "operating_base": {"path": str(operating_base), "expected_head": BASE_OPERATING_PIN, "actual_head": operating_head, "pin_match": operating_pin_match, "workflow_pin_match": workflow_operating_pin_match},
        "contract_base": {"path": str(contract_base), "expected_head": BASE_CONTRACT_PIN, "actual_head": contract_head, "pin_match": contract_pin_match, "workflow_pin_match": workflow_contract_pin_match},
        "godot_executable": str(Path(args.godot).resolve()) if args.godot else None,
        "godot_required": godot_required, "godot_present": godot_present,
        "clean_before": clean_before, "clean_after": clean_after,
        "authoring_surface_hash_unchanged": authoring_unchanged,
        "authoring_surface_count": len(before_hashes),
        "commands": [asdict(result) | {"passed": result.passed} for result in results],
        "completed_at": utc_now(),
        "limitations": ["Execution venue only; no v4.3 gate is waived.", "Windows/Android device validation requires separate evidence."],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "manifest": str(output), "head": head}, ensure_ascii=False))
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
