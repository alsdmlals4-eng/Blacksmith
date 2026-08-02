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
    def test_current_base_identity_is_v943(self) -> None:
        data = load()
        release = data["base_release"]
        self.assertEqual("9.4.3", release["version"])
        self.assertEqual("7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8", release["release_commit"])
        self.assertEqual("da33a350d61b8adc52df97fccc7001708a933370", release["release_evidence_commit"])
        self.assertEqual("0b7c94f38d959efc0fc9442274c60b2e268a3c97", release["finalization_commit"])
        self.assertEqual("693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59", data["skill_registry"]["base"]["sha256"])

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
