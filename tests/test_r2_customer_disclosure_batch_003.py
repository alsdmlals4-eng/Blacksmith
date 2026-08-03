from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_DISCLOSURE_MINIMUM_CANON_2026.md"
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


class CustomerDisclosureBatch003Tests(unittest.TestCase):
    def test_registry_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-CUSTOMER-20260803-02"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CUSTOMER-20260803-01", decision["refines"])
        self.assertEqual(
            ["EVENT_RISK_SCORE", "CUSTOMER_CORE_STATS", "APPROXIMATE_SUCCESS_CHANCE"],
            contract["public_fields"],
        )
        self.assertEqual("INTEGER_1_TO_10", contract["event_risk_display_scale"])
        self.assertEqual("INTEGER_1_TO_10", contract["customer_stat_display_scale"])
        self.assertFalse(contract["display_decimals"])
        self.assertEqual("APPROXIMATE_PERCENT_ROUNDED_TO_NEAREST_10", contract["success_display"])
        self.assertEqual(5, contract["success_display_min_percent"])
        self.assertEqual(95, contract["success_display_max_percent"])
        self.assertTrue(contract["post_equipment_recalculation"])
        self.assertFalse(contract["unknown_variable_notice"])
        self.assertFalse(contract["pre_sale_modifier_breakdown"])
        self.assertTrue(contract["result_causes_explained"])
        self.assertEqual("BASELINE_TEST_PRESET", contract["numeric_authority"])

        previous = decisions["BS-CUSTOMER-20260803-01"]["contract"]
        self.assertEqual("1_TO_5_HISTORICAL_PRESET", previous["display_scale"])
        self.assertEqual(
            "SUPERSEDED_FOR_PLAYER_DISPLAY_BY_BS-CUSTOMER-20260803-02",
            previous["display_scale_status"],
        )

    def test_batch_counter_and_product_gate(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        active_batch = registry["active_batch"]
        self.assertEqual("R2_BATCH_003", active_batch["id"])
        self.assertEqual(1, active_batch["approved_decisions"])
        self.assertEqual("1/10", active_batch["counter"])
        self.assertEqual("APPROVED_PENDING_MERGE", active_batch["state"])
        self.assertEqual(["BS-CUSTOMER-20260803-02"], active_batch["decisions"])
        self.assertFalse(active_batch["product_paths_changed"])
        self.assertEqual("BLOCKED", registry["product_implementation"])

    def test_canon_and_entry_documents(self) -> None:
        canon = CANON.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")

        for token in (
            "BS-CUSTOMER-20260803-02",
            "사건 위험도: 7/10",
            "기량 8/10 / 체력 6/10 / 판단력 7/10",
            "예상 성공률: 약 60%",
            "최소 5%, 최대 95%",
            "별도 경고는 표시하지 않는다",
            "1~5 표시는 병합 당시의 역사적 표시 프리셋",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)

        for token in (
            "BS-CUSTOMER-20260803-02",
            "R2_BATCH_003_1_OF_10",
            "APPROVED_PENDING_MERGE",
            "사건 위험도: `1~10`",
            "고객 핵심 능력치: `기량 / 체력 / 판단력` 각 `1~10`",
        ):
            self.assertIn(token, root)

        for token in (
            "BS-CUSTOMER-20260803-02",
            "사건 위험도: 정수 `1~10`",
            "고객 능력: `기량 / 체력 / 판단력` 각 정수 `1~10`",
            "약 10% 단위",
            "승인 카운터: `1/10`",
        ):
            self.assertIn(token, active)


if __name__ == "__main__":
    unittest.main()
