from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"
LEGACY_CUSTOMER = ROOT / "data/customers/gladiator_poc.json"
LEGACY_MATCH = ROOT / "data/world/gladiator_match_poc.json"


class Gladiator01CassiaContentContractTests(unittest.TestCase):
    def test_r3_registry_preserves_cassia_as_approved_fifth_content_decision(self) -> None:
        self.assertTrue(REGISTRY.is_file())
        registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
        self.assertEqual("R3_R7_DESIGN_ACTIVE", registry.get("stage_status"))
        self.assertEqual("BLOCKED", registry.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", registry.get("task3_implementation"))
        self.assertEqual("9/10", registry.get("next_approval_counter"))

        decisions = {item["id"]: item for item in registry.get("current_decisions", [])}
        for decision_id in (
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
            "BS-CONTENT-20260811-05",
            "BS-CONTENT-20260811-06",
            "BS-CONTENT-20260811-07",
        ):
            self.assertIn(decision_id, decisions)

        decision = decisions.get("BS-CONTENT-20260811-05", {})
        self.assertIn("USER_APPROVED_R3_R7_5_OF_10", decision.get("status", ""))
        contract = decision.get("contract", {})
        self.assertEqual("GLADIATOR_01", contract.get("content_id"))
        self.assertEqual("CASSIA_BELLAN", contract.get("customer_id"))
        self.assertEqual("GLADIATOR", contract.get("customer_archetype"))
        self.assertEqual("ARENA_SIGNATURE_WEAPON_AND_LEGACY", contract.get("activity_family"))
        self.assertEqual(
            "ARENA_RENOWN_THROUGH_EXPLAINABLE_EQUIPMENT_CONTRIBUTION",
            contract.get("content_goal"),
        )
        self.assertEqual(
            "BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER",
            contract.get("player_role"),
        )
        self.assertFalse(contract.get("direct_arena_combat"))
        self.assertFalse(contract.get("gladiator_team_or_guild_management"))
        self.assertFalse(contract.get("betting_system"))
        self.assertFalse(contract.get("opaque_arena_score"))
        self.assertFalse(contract.get("single_highest_enhancement_always_best"))
        self.assertFalse(contract.get("win_equals_good_item_collapse"))
        self.assertTrue(contract.get("same_item_uid_preserved"))
        self.assertFalse(contract.get("match_count_artistry_growth"))
        self.assertFalse(contract.get("automatic_chronicle_affix_from_win_or_appearance"))
        self.assertFalse(contract.get("match_farming_multiplier"))
        self.assertEqual("NON_AUTHORITATIVE_HISTORICAL_FIXTURE", contract.get("legacy_gladiator_poc_status"))
        self.assertEqual(
            ["ARENA_MATCH_STATE", "EQUIPMENT_CONTRIBUTION_STATE", "ITEM_UID_ARENA_LEGACY_STATE"],
            contract.get("result_axes"),
        )
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", contract.get("task3_implementation"))

    def test_cassia_canon_separates_match_outcome_from_item_contribution(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-05",
            "GLADIATOR_01",
            "CASSIA_BELLAN",
            "카시아 벨란",
            "ARENA_SIGNATURE_WEAPON_AND_LEGACY",
            "ARENA_MATCH_STATE",
            "EQUIPMENT_CONTRIBUTION_STATE",
            "ITEM_UID_ARENA_LEGACY_STATE",
            "SAME_ITEM_UID_PRESERVED",
            "NO_DIRECT_ARENA_COMBAT",
            "NO_OPAQUE_ARENA_SCORE",
            "NO_WIN_EQUALS_GOOD_ITEM_COLLAPSE",
            "NO_MATCH_COUNT_ARTISTRY_GROWTH",
            "NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_APPEARANCE",
            "LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05",
            "제품 구현: `BLOCKED`",
            "Task3 구현: `NOT_APPROVED`",
        ):
            self.assertIn(token, canon)

        for forbidden in (
            "DIRECT_ARENA_COMBAT: true",
            "ARENA_SCORE: true",
            "FAME_SCORE: true",
            "GLADIATOR_SCORE: true",
            "MATCH_COUNT_ARTISTRY_GROWTH: true",
            "AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN: true",
            "TASK3_IMPLEMENTATION_APPROVED",
        ):
            self.assertNotIn(forbidden, canon)

    def test_current_routers_preserve_cassia_history_while_sedric_is_current(self) -> None:
        current = CURRENT.read_text(encoding="utf-8")
        active = ACTIVE.read_text(encoding="utf-8")
        start_here = START_HERE.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        gates = GATES.read_text(encoding="utf-8")

        for decision_id in (
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
            "BS-CONTENT-20260811-05",
            "BS-CONTENT-20260811-06",
            "BS-CONTENT-20260811-07",
        ):
            self.assertIn(decision_id, current)

        for text in (active, start_here, roadmap, gates):
            self.assertIn("R3_R7_DESIGN_ACTIVE", text)
            self.assertIn("R3_R7_APPROVAL_COUNTER: 9/10", text)
            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", text)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", text)
            self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", text)

        for text in (active, start_here, roadmap):
            self.assertIn("GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED", text)

        self.assertIn("현재 Decision은 `BS-CONTENT-20260811-09`", active)
        self.assertIn("현재 연속 작업은 `BS-CONTENT-20260811-09`", start_here)
        self.assertIn("현재 승인 카운터: `9/10`.", roadmap)
        self.assertIn("Decision: `BS-CONTENT-20260811-09`.", gates)

    def test_legacy_gladiator_poc_remains_historical_fixture_not_decision05_authority(self) -> None:
        self.assertTrue(LEGACY_CUSTOMER.is_file())
        self.assertTrue(LEGACY_MATCH.is_file())
        customer = json.loads(LEGACY_CUSTOMER.read_text(encoding="utf-8"))
        match = json.loads(LEGACY_MATCH.read_text(encoding="utf-8"))

        # These legacy values remain historical evidence; Decision05 must not silently relabel them as canon.
        self.assertEqual("gladiator_kyle_iron_sword", customer.get("contract_id"))
        self.assertEqual("iron_sword", customer.get("equipment_id"))
        self.assertIn("score_weights", match)
        self.assertIn("grade_scores", match)

        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        self.assertIn("LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05", canon)
        self.assertIn("NO_FIXED_IRON_SWORD_CANON", canon)
        self.assertIn("NO_LEGACY_ARENA_SCORE_FORMULA_CANON", canon)
        self.assertIn("NO_UNIVERSAL_FIXED_DAY_COUNT", canon)


if __name__ == "__main__":
    unittest.main()
