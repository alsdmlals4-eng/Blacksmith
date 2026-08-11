from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "docs/planning/BLACKSMITH_AUTO_ENHANCEMENT_CAP_UNLOCK_CANON_2026.md"
DECISION = ROOT / "docs/decisions/BS-CORE-20260811-01_AUTO_ENHANCEMENT_CAP_UNLOCK.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
LEGACY_CONTINUOUS = ROOT / "docs/planning/BLACKSMITH_DECISION_LEDGER_ADDENDUM_07.md"
BREAKTHROUGH = ROOT / "docs/planning/BLACKSMITH_GROWTH_SYSTEM_ADDENDUM_02.md"
RISK = ROOT / "docs/planning/BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026.md"


class AutoEnhancementCapUnlockContractTests(unittest.TestCase):
    def test_existing_low_risk_continuous_enhancement_authority_is_preserved(self) -> None:
        text = LEGACY_CONTINUOUS.read_text(encoding="utf-8")
        for token in (
            "수동 강화 15회 뒤 해금",
            "+1~+20",
            "요청 최대치는 10회",
            "고위험 자동 강화와 정밀강화 자동 처리는 `REJECTED`",
        ):
            self.assertIn(token, text)

    def test_auto_cap_canon_trails_category_manual_frontier(self) -> None:
        self.assertTrue(CANON.is_file())
        self.assertTrue(DECISION.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        decision = DECISION.read_text(encoding="utf-8") if DECISION.is_file() else ""

        for token in (
            "BS-CORE-20260811-01",
            "AUTO_ENHANCEMENT_CAP_UNLOCK",
            "15 manual attempts → AUTO_CAP +20",
            "+40 breakthrough complete → AUTO_CAP +30",
            "+50 breakthrough complete → AUTO_CAP +40",
            "+60 breakthrough complete → AUTO_CAP +50",
            "AUTO_CAP = highest completed category breakthrough - 10",
            "CATEGORY_SPECIFIC_AUTO_CAP",
            "PLAYER_SELECTED_TARGET_REQUIRED",
            "TARGET_ENHANCEMENT <= AUTO_CAP",
        ):
            self.assertIn(token, canon)
            self.assertIn(token, decision)

    def test_auto_attempts_reuse_normal_enhancement_semantics_and_stop_at_manual_boundaries(self) -> None:
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "NO_HIDDEN_SUCCESS_RATE_BONUS",
            "NO_RESOURCE_OR_FATIGUE_BYPASS",
            "PER_ATTEMPT_UID_HISTORY_PRESERVED",
            "NO_UNPROTECTED_AUTO_DESTRUCTION",
            "HIGH / VERY_HIGH",
            "AUTO_PRECISION_ENHANCEMENT: false",
            "AUTO_TECHNICAL_BREAKTHROUGH: false",
            "실제 단계 하락이 발생하면 그 시도 해결 후 즉시 정지",
            "보호 파괴 결과가 발생하면 그 시도 해결 후 즉시 정지",
            "정밀강화 대기 지점에서 자동 진행을 멈춘다",
            "기술 돌파 대기 지점에서 자동 진행을 멈춘다",
            "REJECTED_IMPORT",
        ):
            self.assertIn(token, canon)

        # Rejected benchmark mechanisms may be named as evidence; they must not
        # appear as enabled or owned Blacksmith contracts.
        for forbidden in (
            "AUTO_HIGH_RISK: true",
            "AUTO_VERY_HIGH_RISK: true",
            "AUTO_PRECISION_ENHANCEMENT: true",
            "AUTO_TECHNICAL_BREAKTHROUGH: true",
            "AUTO_SUCCESS_RATE_BONUS: true",
            "ANCIENT_ANVIL_GAUGE: true",
            "PITY_GAUGE: true",
        ):
            self.assertNotIn(forbidden, canon)

    def test_refinement_does_not_duplicate_breakthrough_or_probability_authority(self) -> None:
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        breakthrough = BREAKTHROUGH.read_text(encoding="utf-8")
        risk = RISK.read_text(encoding="utf-8")

        self.assertIn("+40 → 분야별 1차 기술 돌파 → +41 개방", breakthrough)
        self.assertIn("정식 최대 강화 단계는 `+100`", risk)
        self.assertIn("BREAKTHROUGH_AUTHORITY: BLACKSMITH_GROWTH_SYSTEM_ADDENDUM_02", canon)
        self.assertIn("RISK_PROBABILITY_AUTHORITY: BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026", canon)
        self.assertIn("이 문서는 새 성공률 표나 새 돌파 비용을 소유하지 않는다", canon)

    def test_current_decisions_discovers_core_refinement_without_incrementing_r3_counter(self) -> None:
        current = CURRENT.read_text(encoding="utf-8")
        self.assertIn("BS-CORE-20260811-01", current)
        self.assertIn("AUTO_ENHANCEMENT_CAP_UNLOCK", current)
        self.assertIn("R3_R7_APPROVAL_COUNTER: 5/10", current)
        self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05", current)
        self.assertIn("BS-CONTENT-20260811-03", current)
        self.assertNotIn("R3_R7_CURRENT_DECISION: BS-CORE-20260811-01", current)
        self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", current)
        self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", current)


if __name__ == "__main__":
    unittest.main()
