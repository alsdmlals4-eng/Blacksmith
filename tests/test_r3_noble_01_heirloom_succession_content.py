from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"
VERTICAL_SLICE = ROOT / "data/vertical_slice/vertical_slice_preset.json"


class Noble01HeirloomSuccessionContentContractTests(unittest.TestCase):
    def test_r3_registry_preserves_ceremonial_noble_as_approved_sixth_content_decision(self) -> None:
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

        decision = decisions.get("BS-CONTENT-20260811-06", {})
        self.assertIn("USER_APPROVED_R3_R7_6_OF_10", decision.get("status", ""))
        contract = decision.get("contract", {})
        self.assertEqual("NOBLE_01", contract.get("content_id"))
        self.assertEqual("CEREMONIAL_NOBLE", contract.get("customer_id"))
        self.assertEqual("NOBLE", contract.get("customer_archetype"))
        self.assertEqual("HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY", contract.get("activity_family"))
        self.assertEqual(
            "PRESERVE_MEANINGFUL_HISTORY_WHILE_PREPARING_FOR_SUCCESSION",
            contract.get("content_goal"),
        )
        self.assertEqual(
            "BLACKSMITH_HEIRLOOM_TREATMENT_DECISION_MAKER_NOT_HOUSE_OR_CEREMONY_CONTROLLER",
            contract.get("player_role"),
        )
        self.assertTrue(contract.get("existing_ceremonial_noble_representative_reused"))
        self.assertFalse(contract.get("new_named_noble_lore"))
        self.assertTrue(contract.get("same_item_uid_preserved"))
        self.assertFalse(contract.get("full_restoration_always_best"))
        self.assertFalse(contract.get("highest_artistry_always_best"))
        self.assertFalse(contract.get("opaque_house_prestige_or_authenticity_score"))
        self.assertFalse(contract.get("history_erasure_on_repair"))
        self.assertFalse(contract.get("restoration_count_artistry_growth"))
        self.assertFalse(contract.get("automatic_chronicle_affix_from_ceremony_or_restoration"))
        self.assertFalse(contract.get("restoration_farming_multiplier"))
        self.assertFalse(contract.get("direct_ceremony_minigame"))
        self.assertFalse(contract.get("noble_house_management"))
        self.assertFalse(contract.get("court_or_diplomacy_management"))
        self.assertEqual(
            ["CEREMONY_READINESS_STATE", "HEIRLOOM_TREATMENT_FIT_STATE", "ITEM_UID_DYNASTIC_LEGACY_STATE"],
            contract.get("result_axes"),
        )
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", contract.get("task3_implementation"))

    def test_noble_canon_preserves_history_without_full_restoration_dominance(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-06",
            "NOBLE_01",
            "CEREMONIAL_NOBLE",
            "HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY",
            "CEREMONY_READINESS_STATE",
            "HEIRLOOM_TREATMENT_FIT_STATE",
            "ITEM_UID_DYNASTIC_LEGACY_STATE",
            "SAME_ITEM_UID_PRESERVED",
            "NO_FULL_RESTORATION_ALWAYS_BEST",
            "NO_HIGHEST_ARTISTRY_ALWAYS_BEST",
            "NO_HOUSE_PRESTIGE_SCORE",
            "NO_AUTHENTICITY_TOTAL_SCORE",
            "NO_SUCCESSION_TOTAL_SCORE",
            "NO_HISTORY_ERASURE_ON_REPAIR",
            "NO_RESTORATION_COUNT_ARTISTRY_GROWTH",
            "NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_CEREMONY_OR_RESTORATION",
            "NO_RESTORATION_FARMING_MULTIPLIER",
            "NO_DIRECT_CEREMONY_MINIGAME",
            "NO_NOBLE_HOUSE_MANAGEMENT",
            "NO_COURT_OR_DIPLOMACY_MANAGEMENT",
            "EXISTING_CEREMONIAL_NOBLE_REPRESENTATIVE_REUSED",
            "BLACKSMITH_HEIRLOOM_TREATMENT_DECISION_MAKER_NOT_HOUSE_OR_CEREMONY_CONTROLLER",
            "제품 구현: `BLOCKED`",
            "Task3 구현: `NOT_APPROVED`",
        ):
            self.assertIn(token, canon)

        for forbidden in (
            "FULL_RESTORATION_ALWAYS_BEST: true",
            "HOUSE_PRESTIGE_SCORE: true",
            "AUTHENTICITY_SCORE: true",
            "SUCCESSION_SCORE: true",
            "RESTORATION_COUNT_ARTISTRY_GROWTH: true",
            "TASK3_IMPLEMENTATION_APPROVED",
        ):
            self.assertNotIn(forbidden, canon)

    def test_current_routers_preserve_noble01_history_while_liana_is_current(self) -> None:
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
            self.assertIn("BS-CONTENT-20260811-06", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", text)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", text)
            self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", text)

        for text in (active, start_here, roadmap):
            self.assertIn("COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED", text)

        self.assertIn("현재 Decision은 `BS-CONTENT-20260811-07`", active)
        self.assertIn("현재 연속 작업은 `BS-CONTENT-20260811-07`", start_here)
        self.assertIn("현재 승인 카운터: `7/10`.", roadmap)
        self.assertIn("Decision: `BS-CONTENT-20260811-07`.", gates)
        self.assertIn("### 6/10 — `BS-CONTENT-20260811-06`", roadmap)

    def test_decision06_reuses_existing_ceremonial_noble_fixture(self) -> None:
        self.assertTrue(VERTICAL_SLICE.is_file())
        preset = json.loads(VERTICAL_SLICE.read_text(encoding="utf-8"))
        customer_ids = preset.get("representative_scope", {}).get("customer_ids", [])
        self.assertIn("ceremonial_noble", customer_ids)

        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        self.assertIn("EXISTING_CEREMONIAL_NOBLE_REPRESENTATIVE_REUSED", canon)
        self.assertIn("NO_NEW_NAMED_NOBLE_LORE_IN_DECISION06", canon)


if __name__ == "__main__":
    unittest.main()
