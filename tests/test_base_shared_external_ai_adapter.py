from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
SKILL = "orchestrating-deepseek-worktrees"


def load() -> dict:
    return json.loads(ADAPTER.read_text(encoding="utf-8"))


def active_routes(data: dict) -> set[str]:
    return {
        route if isinstance(route, str) else route["skill_id"]
        for route in data["routing"]["base_routes"]
        if isinstance(route, str) or route.get("status") == "ACTIVE"
    }


class BaseSharedExternalAIAdapterTests(unittest.TestCase):
    def test_current_base_identity_is_v944(self) -> None:
        data = load()
        release = data["base_release"]
        self.assertEqual("9.4.4", release["version"])
        self.assertEqual("210ec78292fa12ed7563ba743b322dd36103ae4a", release["release_commit"])
        self.assertEqual("bb61e68dc3028421b60c11b87ba2abd297ee6f78", release["release_evidence_commit"])
        self.assertEqual("5adc196c0185951f50e49ab5e51586eff8d60886", release["finalization_commit"])
        self.assertEqual("08f882d0c77339e8f7ff187c35b79501e0a2958ab1ff1c7aaa1c0ef8dbee45d6", data["skill_registry"]["base"]["sha256"])

    def test_external_ai_remains_separate_v941_boundary(self) -> None:
        data = load()
        self.assertIn(SKILL, active_routes(data))
        self.assertFalse((ROOT / f"skills/{SKILL}/SKILL.md").exists())
        policy = data["shared_overrides"][SKILL]
        self.assertEqual(".worktrees/", policy["worktree_parent"])
        self.assertEqual("REVIEW_PENDING", policy["result_state"])
        self.assertEqual("LOCAL_REVIEW_REQUIRED_BEFORE_CANON", policy["integration_policy"])
        self.assertEqual("ADOPTED_FROM_BASE_V9_4_1", policy["base_validator_adoption"])
        self.assertEqual("base-v9.4.1.lock.json", policy["base_release_lock"])
        self.assertEqual("NOT_RUN", policy["actual_external_ai_worktree_execution"])

    def test_worktree_and_validator_contract(self) -> None:
        result = subprocess.run(["git", "check-ignore", "-q", ".worktrees/"], cwd=ROOT, check=False)
        self.assertEqual(0, result.returncode)
        commands = {item if isinstance(item, str) else item.get("command") for item in load().get("validators", [])}
        self.assertIn("python tests/test_base_shared_external_ai_adapter.py", commands)


if __name__ == "__main__":
    unittest.main()
