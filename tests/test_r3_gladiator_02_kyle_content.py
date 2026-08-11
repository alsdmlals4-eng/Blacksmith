from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"


class Gladiator02KyleVeteranContinuityContractTests(unittest.TestCase):
    def test_r3_registry_promotes_kyle_as_approved_ninth_content_decision(self) -> None:
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
            "BS-CONTENT-20260811-08",
            "BS-CONTENT-20260811-09",
        ):
            self.assertIn(decision_id, decisions)

        decision = decisions.get("BS-CONTENT-20260811-09", {})
        self.assertIn("USER_APPROVED_R3_R7_9_OF_10", decision.get("status", ""))
        contract = decision.get("contract", {})
        self.assertEqual("GLADIATOR_02", contract.get("content_id"))
        self.assertEqual("KYLE_VAREN", contract.get("customer_id"))
        self.assertEqual("GLADIATOR", contract.get("customer_archetype"))
        self.assertEqual(
            "VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION",
            contract.get("activity_family"),
        )
        self.assertEqual(
            "EQUIPMENT_CONTINUITY_RESPONSIBILITY_THROUGH_KEEP_OR_REPLACE",
            contract.get("content_goal"),
        )
        self.assertEqual(
            "BLACKSMITH_EQUIPMENT_CONTINUITY_DECISION_MAKER_NOT_GLADIATOR_CONTROLLER",
            contract.get("player_role"),
        )
        self.assertTrue(contract.get("existing_kyle_varen_customer_reused"))
        self.assertTrue(contract.get("actual_prior_record_required_for_continuity_branch"))
        self.assertTrue(contract.get("keep_path_same_uid_preserved"))
        self.assertTrue(contract.get("old_item_history_preserved"))
        self.assertTrue(contract.get("new_item_gets_new_uid"))
        self.assertTrue(contract.get("cassia_arena_fit_responsibility_preserved"))
        self.assertTrue(contract.get("noble01_treatment_depth_responsibility_preserved"))
        self.assertFalse(contract.get("fabricated_kyle_history"))
        self.assertFalse(contract.get("fake_legacy_item_for_content_unlock"))
        self.assertFalse(contract.get("history_transfer_to_replacement"))
        self.assertFalse(contract.get("uid_rewrite"))
        self.assertFalse(contract.get("old_item_always_best"))
        self.assertFalse(contract.get("new_item_always_best"))
        self.assertFalse(contract.get("highest_enhancement_always_best"))
        self.assertFalse(contract.get("highest_artistry_always_best"))
        self.assertFalse(contract.get("most_chronicle_always_best"))
        self.assertFalse(contract.get("sentiment_score"))
        self.assertFalse(contract.get("veteran_total_score"))
        self.assertFalse(contract.get("lineage_power_bonus"))
        self.assertFalse(contract.get("legacy_arena_score_formula_canon"))
        self.assertFalse(contract.get("fixed_iron_sword_canon"))
        self.assertFalse(contract.get("direct_arena_combat"))
        self.assertFalse(contract.get("gladiator_roster_or_guild_management"))
        self.assertFalse(contract.get("training_or_injury_management"))
        self.assertFalse(contract.get("betting_system"))
        self.assertFalse(contract.get("baseline_permadeath"))
        self.assertFalse(contract.get("comeback_count_artistry_growth"))
        self.assertFalse(contract.get("replacement_count_artistry_growth"))
        self.assertFalse(contract.get("automatic_chronicle_affix_from_comeback_or_retirement"))
        self.assertFalse(contract.get("comeback_farming_multiplier"))
        self.assertEqual(
            ["VETERAN_RETURN_STATE", "EQUIPMENT_CONTINUITY_STATE", "ITEM_UID_LINEAGE_STATE"],
            contract.get("result_axes"),
        )
        self.assertEqual("P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED", contract.get("taxonomy_ambiguity"))
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", contract.get("task3_implementation"))
        self.assertEqual("NOT_RUN", contract.get("human_playtest"))

    def test_kyle_canon_separates_continuity_from_cassia_fit_and_noble_treatment(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-09",
            "GLADIATOR_02",
            "KYLE_VAREN",
            "VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION",
            "VETERAN_RETURN_STATE",
            "EQUIPMENT_CONTINUITY_STATE",
            "ITEM_UID_LINEAGE_STATE",
            "KEEP_IN_SERVICE",
            "RETIRE_AND_REPLACE",
            "NO_UID_REWRITE",
            "NO_HISTORY_TRANSFER_TO_REPLACEMENT",
            "OLD_ITEM_HISTORY_PRESERVED",
            "NEW_ITEM_GETS_NEW_UID",
            "CASSIA_ARENA_FIT_RESPONSIBILITY_PRESERVED",
            "NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED",
            "NO_FABRICATED_KYLE_HISTORY",
            "NO_FAKE_LEGACY_ITEM_FOR_CONTENT_UNLOCK",
            "NO_OLD_ITEM_ALWAYS_BEST",
            "NO_NEW_ITEM_ALWAYS_BEST",
            "NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST",
            "NO_HIGHEST_ARTISTRY_ALWAYS_BEST",
            "NO_MOST_CHRONICLE_ALWAYS_BEST",
            "NO_SENTIMENT_SCORE",
            "NO_VETERAN_TOTAL_SCORE",
            "NO_LINEAGE_POWER_BONUS",
            "LEGACY_GLADIATOR_KYLE_FIXTURE_NON_AUTHORITATIVE",
            "NO_FIXED_IRON_SWORD_CANON",
            "NO_LEGACY_ARENA_SCORE_FORMULA_CANON",
            "NO_DIRECT_ARENA_COMBAT",
            "NO_GLADIATOR_ROSTER_OR_GUILD_MANAGEMENT",
            "NO_TRAINING_OR_INJURY_MANAGEMENT",
            "NO_BASELINE_PERMADEATH",
            "NO_COMEBACK_COUNT_ARTISTRY_GROWTH",
            "NO_REPLACEMENT_COUNT_ARTISTRY_GROWTH",
            "NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_COMEBACK_OR_RETIREMENT",
            "NO_COMEBACK_FARMING_MULTIPLIER",
            "CASSIA_BELLAN",
            "ARENA_SIGNATURE_WEAPON_AND_LEGACY",
            "CEREMONIAL_NOBLE",
            "HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY",
            "P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED",
            "제품 구현: `BLOCKED`",
            "Task3 구현: `NOT_APPROVED`",
        ):
            self.assertIn(token, canon)

        for forbidden in (
            "LINEAGE_POWER: true",
            "SUCCESSION_SCORE: true",
            "VETERAN_LEGACY_SCORE: true",
            "HISTORY_TRANSFER_TO_REPLACEMENT: true",
            "UID_REWRITE: true",
            "LEGACY_ARENA_SCORE_FORMULA_CANON: true",
            "TASK3_IMPLEMENTATION_APPROVED",
        ):
            self.assertNotIn(forbidden, canon)

    def test_current_routers_move_to_nine_of_ten_without_rewriting_eighth_history(self) -> None:
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
            "BS-CONTENT-20260811-08",
            "BS-CONTENT-20260811-09",
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

        d07_heading = "### 7/10 — `BS-CONTENT-20260811-07`"
        d08_heading = "### 8/10 — `BS-CONTENT-20260811-08`"
        d09_heading = "### 9/10 — `BS-CONTENT-20260811-09`"
        self.assertIn(d07_heading, roadmap)
        self.assertIn(d08_heading, roadmap)
        self.assertIn(d09_heading, roadmap)
        self.assertLess(roadmap.index(d07_heading), roadmap.index(d08_heading))
        self.assertLess(roadmap.index(d08_heading), roadmap.index(d09_heading))
        self.assertIn("COLLECTOR_02 / SEDRIC_VAEL", roadmap[roadmap.index(d08_heading):roadmap.index(d09_heading)])


if __name__ == "__main__":
    unittest.main()
