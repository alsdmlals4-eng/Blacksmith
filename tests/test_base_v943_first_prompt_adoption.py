from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
PAYLOAD = "210ec78292fa12ed7563ba743b322dd36103ae4a"
EVIDENCE = "bb61e68dc3028421b60c11b87ba2abd297ee6f78"
FINALIZATION = "5adc196c0185951f50e49ab5e51586eff8d60886"
REGISTRY = "08f882d0c77339e8f7ff187c35b79501e0a2958ab1ff1c7aaa1c0ef8dbee45d6"
SKILL = "managing-project-intake-and-work-contract"


def load() -> dict:
    return json.loads(ADAPTER.read_text(encoding="utf-8"))


def routes(data: dict) -> set[str]:
    found: set[str] = set()
    for route in data["routing"]["base_routes"]:
        if isinstance(route, str):
            found.add(route)
        elif route.get("status") == "ACTIVE":
            found.add(route["skill_id"])
    return found


def contract(data: dict) -> dict:
    value = data.get("shared_overrides", {}).get(SKILL, {}).get("first_prompt_governance")
    if value is None:
        value = data.get("base_v94_contract", {}).get("first_prompt_governance")
    if not isinstance(value, dict):
        raise AssertionError("missing first_prompt_governance")
    return value


class AdoptionTests(unittest.TestCase):
    def test_release_identity(self) -> None:
        data = load()
        release = data["base_release"]
        self.assertEqual("9.4.4", release["version"])
        self.assertEqual(PAYLOAD, release["release_commit"])
        self.assertEqual(EVIDENCE, release["release_evidence_commit"])
        self.assertEqual(FINALIZATION, release["finalization_commit"])
        registry = data.get("skill_registry", {}).get("base", {}).get("sha256")
        self.assertEqual(REGISTRY, registry or release.get("registry_sha256"))

    def test_intake_route_and_adapter_only_policy(self) -> None:
        self.assertIn(SKILL, routes(load()))
        self.assertFalse((ROOT / "skills" / SKILL / "SKILL.md").exists())

    def test_first_prompt_gate(self) -> None:
        value = contract(load())
        self.assertEqual(["route", "first-prompt", "contract", "clarify"], value["instruction_flow"])
        self.assertEqual("AWAITING_USER_CONFIRMATION", value["unconfirmed_state"])
        self.assertEqual("REUSE_EXACT_APPROVAL_REFERENCE", value["approval_reuse"])
        self.assertEqual("base-v9.4.3.lock.json", value["base_release_lock"])
        self.assertEqual("0b7c94f38d959efc0fc9442274c60b2e268a3c97", value["base_release_finalization_commit"])
        self.assertEqual("NOT_RUN", value["actual_project_instruction_execution"])
        self.assertEqual(
            "skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md",
            value["direction_anchor_reference"],
        )

    def test_project_boundaries_remain_declared(self) -> None:
        self.assertTrue(load()["protected_paths"])


if __name__ == "__main__":
    unittest.main()
