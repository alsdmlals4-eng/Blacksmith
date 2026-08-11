from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"


class Soldier02LianaMissionFitContentContractTests(unittest.TestCase):
    def test_r3_registry_promotes_liana_as_approved_seventh_content_decision(self) -> None:
        self.assertTrue(REGISTRY.is_file())
        registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
        self.assertEqual("R3_R7_DESIGN_ACTIVE", registry.get("stage_status"))
        self.assertEqual("BLOCKED", registry.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", registry.get("task3_implementation"))
        self.assertEqual("8/10", registry.get("next_approval_counter"))

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

        decision = decisions.get("BS-CONTENT-20260811-07", {})
        self.assertIn("USER_APPROVED_R3_R7_7_OF_10", decision.get("status", ""))
        contract = decision.get("contract", {})
        self.assertEqual("SOLDIER_02", contract.get("content_id"))
        self.assertEqual("LIANA_BERG", contract.get("customer_id"))
        self.assertEqual("SOLDIER", contract.get("customer_archetype"))
        self.assertEqual(
            "FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY",
            contract.get("activity_family"),
        )
        self.assertEqual("MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY", contract.get("content_goal"))
        self.assertEqual(
            "BLACKSMITH_COMMANDER_EQUIPMENT_DECISION_MAKER_NOT_TACTICAL_OR_UNIT_CONTROLLER",
            contract.get("player_role"),
        )
        self.assertTrue(contract.get("existing_liana_berg_customer_reused"))
        self.assertTrue(contract.get("same_item_uid_preserved"))
        self.assertFalse(contract.get("direct_tactical_combat"))
        self.assertFalse(contract.get("unit_movement_or_formation_control"))
        self.assertFalse(contract.get("realtime_logistics_control"))
        self.assertFalse(contract.get("soldier_casualty_micromanagement"))
        self.assertFalse(contract.get("opaque_command_hero_leadership_or_mission_fit_score"))
        self.assertFalse(contract.get("highest_defense_always_best"))
        self.assertFalse(contract.get("highest_enhancement_always_best"))
        self.assertFalse(contract.get("item_as_sole_cause_of_mission_result"))
        self.assertFalse(contract.get("baseline_permadeath_for_liana"))
        self.assertFalse(contract.get("death_farming_or_recruit_replacement_loop"))
        self.assertFalse(contract.get("mission_count_artistry_growth"))
        self.assertFalse(contract.get("automatic_chronicle_affix_from_win_or_survival"))
        self.assertFalse(contract.get("mission_farming_multiplier"))
        self.assertEqual(
            ["MISSION_DUTY_STATE", "COMMANDER_RETURN_STATE", "ITEM_UID_FIELD_LEGACY_STATE"],
            contract.get("result_axes"),
        )
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", contract.get("task3_implementation"))
        self.assertEqual("NOT_RUN", contract.get("human_playtest"))

    def test_liana_canon_preserves_single_commander_responsibility_without_combat_drift(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-07",
            "SOLDIER_02",
            "LIANA_BERG",
            "FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY",
            "MISSION_DUTY_STATE",
            "COMMANDER_RETURN_STATE",
            "ITEM_UID_FIELD_LEGACY_STATE",
            "EXISTING_LIANA_BERG_CUSTOMER_REUSED",
            "SAME_ITEM_UID_PRESERVED",
            "NO_DIRECT_TACTICAL_COMBAT",
            "NO_UNIT_MOVEMENT_OR_FORMATION_CONTROL",
            "NO_REALTIME_LOGISTICS_CONTROL",
            "NO_SOLDIER_CASUALTY_MICROMANAGEMENT",
            "NO_COMMAND_POWER_SCORE",
            "NO_HERO_SCORE",
            "NO_LEADERSHIP_SCORE",
            "NO_MISSION_FIT_TOTAL_SCORE",
            "NO_HIGHEST_DEFENSE_ALWAYS_BEST",
            "NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST",
            "NO_ITEM_AS_SOLE_CAUSE_OF_MISSION_RESULT",
            "NO_BASELINE_PERMADEATH_FOR_LIANA",
            "NO_DEATH_FARMING_OR_RECRUIT_REPLACEMENT_LOOP",
            "NO_MISSION_COUNT_ARTISTRY_GROWTH",
            "NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_SURVIVAL",
            "NO_MISSION_FARMING_MULTIPLIER",
            "MAREK_OLDEN",
            "SMALL_LOT_STANDARD_ORDER",
            "CASSIA_BELLAN",
            "ARENA_SIGNATURE_WEAPON_AND_LEGACY",
            "BLACKSMITH_COMMANDER_EQUIPMENT_DECISION_MAKER_NOT_TACTICAL_OR_UNIT_CONTROLLER",
            "제품 구현: `BLOCKED`",
            "Task3 구현: `NOT_APPROVED`",
        ):
            self.assertIn(token, canon)

        for forbidden in (
            "DIRECT_TACTICAL_COMBAT: true",
            "COMMAND_POWER_SCORE: true",
            "HERO_SCORE: true",
            "LEADERSHIP_SCORE: true",
            "MISSION_FIT_TOTAL_SCORE: true",
            "BASELINE_PERMADEATH_FOR_LIANA: true",
            "TASK3_IMPLEMENTATION_APPROVED",
        ):
            self.assertNotIn(forbidden, canon)

    def test_current_routers_preserve_liana_history_while_sedric_is_current(self) -> None:
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
            self.assertIn("R3_R7_APPROVAL_COUNTER: 8/10", text)
            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", text)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", text)
            self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", text)

        for text in (active, start_here, roadmap):
            self.assertIn("COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED", text)

        self.assertIn("현재 Decision은 `BS-CONTENT-20260811-08`", active)
        self.assertIn("현재 연속 작업은 `BS-CONTENT-20260811-08`", start_here)
        self.assertIn("현재 승인 카운터: `8/10`.", roadmap)
        self.assertIn("Decision: `BS-CONTENT-20260811-08`.", gates)
        self.assertIn("BS-CONTENT-20260811-07 / R3_R7_7_OF_10", active)
        self.assertIn("Liana 7/10", start_here)


if __name__ == "__main__":
    unittest.main()
