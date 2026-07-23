"""Deterministic semantic parity checks for the balance simulator."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from simulate_enhancement_balance import Scenario, load_simulator, run_trial  # noqa: E402


def guaranteed_to(simulator, target: int) -> None:
    while simulator.level < target:
        simulator.resolve(roll=0.0, leap_roll=1.0)


class EnhancementBalanceSimulatorTests(unittest.TestCase):
    def test_fixed_seed_trial_is_reproducible(self) -> None:
        scenario = Scenario(50, "balanced")

        first = run_trial(ROOT, scenario, seed=29029)
        second = run_trial(ROOT, scenario, seed=29029)

        self.assertEqual(first, second)

    def test_hold_accumulates_pity_in_safe_range(self) -> None:
        simulator = load_simulator(ROOT, Scenario(10, "balanced"), seed=1)
        simulator.balance["base_success_by_target_level"] = {"1": 0.5}

        result = simulator.resolve(roll=0.9)

        self.assertEqual("HOLD", result.outcome)
        self.assertEqual(0, simulator.level)
        self.assertEqual(1, simulator.failure_streak)
        self.assertAlmostEqual(0.54, simulator.success_chance(1))

    def test_downgrade_restores_prior_level(self) -> None:
        simulator = load_simulator(ROOT, Scenario(30, "balanced"), seed=2)
        simulator.balance["base_success_by_target_level"] = {str(level): 1.0 for level in range(1, 11)} | {"11": 0.0}
        simulator.balance["risk"] = copy.deepcopy(simulator.balance["risk"])
        simulator.balance["risk"]["downgrade_ratio_by_decade"] = {"1": 1.0}
        simulator.balance["risk"]["destroy_ratio_by_decade"] = {"1": 0.0}
        simulator.balance["risk"]["downgrade_steps_by_decade"] = {"1": 1}
        guaranteed_to(simulator, 10)

        result = simulator.resolve(roll=0.5)

        self.assertEqual("DOWNGRADE", result.outcome)
        self.assertEqual(9, simulator.level)
        self.assertEqual(1, result.downgrade_steps)

    def test_destruction_ends_the_weapon(self) -> None:
        simulator = load_simulator(ROOT, Scenario(30, "balanced", precision_bonus=0.0), seed=3)
        simulator.balance["base_success_by_target_level"] = {str(level): 1.0 for level in range(1, 30)} | {"30": 0.0}
        guaranteed_to(simulator, 29)

        result = simulator.resolve(roll=0.0)

        self.assertEqual("DESTROY", result.outcome)
        self.assertTrue(simulator.destroyed)
        self.assertEqual(0, simulator.sale_price())

    def test_overdrive_cannot_cross_a_special_level(self) -> None:
        simulator = load_simulator(ROOT, Scenario(30, "overdrive"), seed=4)
        simulator.balance["base_success_by_target_level"] = {str(level): 1.0 for level in range(1, 101)}
        guaranteed_to(simulator, 8)

        self.assertFalse(simulator.can_use_overdrive(9))
        result = simulator.resolve(roll=0.0, leap_roll=0.0)

        self.assertEqual("SUCCESS", result.outcome)
        self.assertFalse(result.leap_triggered)
        self.assertEqual(9, simulator.level)

    def test_special_cost_and_catalyst_value_affect_sale_path(self) -> None:
        plain = load_simulator(ROOT, Scenario(10, "balanced", catalyst_id=""), seed=5)
        catalyst = load_simulator(ROOT, Scenario(10, "balanced", catalyst_id="salamander_core"), seed=5)
        plain.balance["base_success_by_target_level"] = {str(level): 1.0 for level in range(1, 101)}
        catalyst.balance["base_success_by_target_level"] = {str(level): 1.0 for level in range(1, 101)}
        guaranteed_to(plain, 9)
        guaranteed_to(catalyst, 9)

        self.assertGreater(catalyst.attempt_cost(10), plain.attempt_cost(10))
        plain.resolve(roll=0.0)
        catalyst.resolve(roll=0.0)
        self.assertGreater(catalyst.sale_price(), plain.sale_price())


if __name__ == "__main__":
    unittest.main()
