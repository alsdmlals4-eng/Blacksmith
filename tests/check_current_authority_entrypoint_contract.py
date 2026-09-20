#!/usr/bin/env python3
# 현재 운영 원본의 실제 경로와 보호 경계를 검사한다.
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = Path("docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md")
REQUIRED_OWNERS = {
    "context", "production", "decisions", "fields", "blueprint", "remaining",
    "handoff", "history", "design_skill", "qa_skill", "engineering_skill",
}
PROTECTED = {"data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"}


def read_authority_record(text: str) -> dict:
    matches = re.findall(
        r"<!-- current-authority -->\s*```json\s*(.*?)\s*```\s*<!-- /current-authority -->",
        text, re.S)
    if len(matches) != 1:
        raise ValueError("expected one current-authority record")
    record = json.loads(matches[0])
    if not isinstance(record, dict) or record.get("schema_version") != 1:
        raise ValueError("unsupported current-authority record")
    return record


def validate(root: Path) -> list[str]:
    root = root.resolve()
    failures = []
    try:
        record = read_authority_record((root / CONTRACT).read_text(encoding="utf-8"))
        owners = record["owners"]
        observation = record["base_observation"]
        if not isinstance(owners, dict) or set(owners) != REQUIRED_OWNERS:
            failures.append("current owner roles incomplete or unknown")
        for role, relative in owners.items():
            if not isinstance(relative, str):
                failures.append(f"{role}: invalid owner path")
                continue
            path = (root / relative).resolve()
            if not path.is_relative_to(root) or Path(relative).is_absolute():
                failures.append(f"{role}: owner outside repository")
            elif not path.is_file():
                failures.append(f"{role}: missing owner {relative}")
        if owners.get("production") == owners.get("history"):
            failures.append("history cannot own current production")
        if len(set(owners.values())) != len(owners):
            failures.append("distinct owner roles must not collapse")
        if (observation.get("repository") != "alsdmlals4-eng/Base"
                or observation.get("ref") != "refs/heads/main"
                or observation.get("role") != "OBSERVATION_NOT_RELEASE_LOCK"
                or not re.fullmatch(r"[0-9a-f]{40}", str(observation.get("commit", "")))
                or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(observation.get("observed_at", "")))):
            failures.append("invalid Base observation; not an execution pin")
        for name in ("AGENTS.md",
                     owners.get("context", ""), owners.get("fields", ""),
                     owners.get("handoff", ""), owners.get("design_skill", ""),
                     owners.get("qa_skill", ""), owners.get("engineering_skill", "")):
            path = (root / name).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                failures.append(f"missing bootstrap {name}")
            elif CONTRACT.as_posix() not in path.read_text(encoding="utf-8"):
                failures.append(f"{name}: missing operational owner link")
        adapter = json.loads((root / "skills/PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        # The adopted generator owns the router bytes. Follow its real adapter
        # edge instead of hand-editing a generated Skill to duplicate this owner.
        router = (root / ".agents/skills/blacksmith-workflow-router/SKILL.md").read_text(encoding="utf-8")
        for target in ("skills/PROJECT_BASE_ADAPTER.json", "skills/PROJECT_SKILL_SNAPSHOT.json"):
            if target not in router:
                failures.append(f"generated router: missing {target}")
        overrides = adapter.get("shared_overrides", {})
        if CONTRACT.as_posix() not in json.dumps(overrides, ensure_ascii=False):
            failures.append("adapter: missing operational owner link")
        if set(adapter["protected_paths"]) != PROTECTED:
            failures.append("protected product paths changed")
        release = adapter["base_release"]
        if (release["version"] != "9.4.4"
                or release["release_commit"] != "210ec78292fa12ed7563ba743b322dd36103ae4a"):
            failures.append("adopted release changed without release-adoption scope")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        failures.append(f"invalid authority input: {exc}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=ROOT)
    args = parser.parse_args()
    failures = validate(args.project_root)
    if failures:
        print("Current authority entrypoint contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Current authority entrypoint contract PASSED (paths and boundaries, not agent/runtime proof)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
