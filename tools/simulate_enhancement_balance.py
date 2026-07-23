#!/usr/bin/env python3
"""Run reproducible baseline simulations for Blacksmith enhancement balance.

This tool mirrors the rules owned by ``EnhancementSession``.  It deliberately
does not edit balance data or replace the runtime session.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_FILES = (
    "data/crafting/enhancement_balance.json",
    "data/crafting/enhancement_milestones.json",
    "data/crafting/materials.json",
    "data/crafting/affixes.json",
    "data/crafting/forging_balance.json",
)


def godot_round(value: float) -> int:
    """Match Godot's positive-number round behavior used by the session."""
    return int(math.floor(value + 0.5))


def percentile(values: list[int], fraction: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    return ordered[min(math.ceil(fraction * len(ordered)) - 1, len(ordered) - 1)]


@dataclass(frozen=True)
class Scenario:
    target_level: int
    skill_id: str
    secondary_id: str = "whetstone"
    catalyst_id: str = ""
    precision_bonus: float = 0.2
    weapon_attack: int = 20

    @property
    def name(self) -> str:
        return f"target_{self.target_level}_{self.skill_id}"


@dataclass
class Attempt:
    outcome: str
    target_level: int
    result_level: int
    success_chance: float
    attempt_cost: int
    leap_triggered: bool = False
    downgrade_steps: int = 0


@dataclass
class TrialResult:
    reached_target: bool
    destroyed: bool
    stop_reason: str
    attempts: int
    total_spent: int
    material_attempts: int
    outcomes: Counter[str]
    final_level: int
    final_attack: int
    sale_price: int
    max_failure_streak: int


@dataclass
class EnhancementSimulator:
    balance: dict[str, Any]
    milestones: list[dict[str, Any]]
    materials: dict[str, dict[str, Any]]
    affixes: dict[str, dict[str, Any]]
    scenario: Scenario
    rng: random.Random = field(default_factory=random.Random)
    level: int = 0
    progression_attack: int = 20
    failure_streak: int = 0
    max_failure_streak: int = 0
    total_spent: int = 0
    total_attempts: int = 0
    material_attempts: int = 0
    destroyed: bool = False
    value_bonus_total: float = 0.0
    affix_list: list[dict[str, Any]] = field(default_factory=list)
    attack_history: dict[int, int] = field(default_factory=dict)
    value_history: dict[int, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.progression_attack = self.scenario.weapon_attack
        self.attack_history[0] = self.progression_attack
        self.value_history[0] = 0.0

    def is_special(self, target_level: int) -> bool:
        interval = max(int(self.balance.get("material_interval", 10)), 1)
        return target_level > 0 and target_level % interval == 0

    def selected_skill(self, target_level: int) -> dict[str, Any]:
        skills = self.balance["skills"]
        if self.scenario.skill_id == "overdrive" and not self.can_use_overdrive(target_level):
            return skills["balanced"]
        return skills[self.scenario.skill_id]

    def can_use_overdrive(self, target_level: int) -> bool:
        if self.scenario.skill_id != "overdrive" or target_level <= 0:
            return False
        skill = self.balance["skills"].get("overdrive", {})
        final_level = min(target_level + max(int(skill.get("leap_levels", 2)), 2) - 1, int(self.balance["max_level"]))
        return all(not self.is_special(level) for level in range(target_level, final_level + 1))

    def material(self, material_id: str) -> dict[str, Any]:
        return self.materials.get(material_id, {})

    def base_success_chance(self, target_level: int) -> float:
        explicit = self.balance.get("base_success_by_target_level", {})
        if str(target_level) in explicit:
            return float(explicit[str(target_level)])
        pattern = self.balance["base_success_pattern_by_cycle_position"]
        base = float(pattern[str(((target_level - 1) % 10) + 1)])
        penalty = min(
            ((target_level - 1) // 10) * float(self.balance["decade_penalty"]),
            float(self.balance["max_decade_penalty"]),
        )
        return max(base - penalty, float(self.balance["minimum_base_success"]))

    def success_chance(self, target_level: int) -> float:
        catalyst = self.material(self.scenario.catalyst_id) if self.is_special(target_level) else {}
        skill = self.selected_skill(target_level)
        pity = min(
            self.failure_streak * float(self.balance["pity"]["bonus_per_failure"]),
            float(self.balance["pity"]["max_bonus"]),
        )
        precision = self.scenario.precision_bonus if self.is_special(target_level) else 0.0
        return min(max(
            self.base_success_chance(target_level)
            + float(catalyst.get("success_bonus", 0.0))
            + pity
            + float(skill.get("success_bonus", 0.0))
            + precision * float(skill.get("precision_bonus_multiplier", 1.0)),
            0.0,
        ), 1.0)

    def conditional_risk(self, target_level: int, kind: str) -> float:
        risk = self.balance["risk"]
        if kind == "downgrade" and target_level <= int(risk["safe_until_level"]):
            return 0.0
        if kind == "destroy" and target_level < int(risk["destroy_start_level"]):
            return 0.0
        decade = (target_level - 1) // 10
        ratio = float(risk[f"{kind}_ratio_by_decade"].get(str(decade), 0.0))
        if self.is_special(target_level):
            ratio *= float(risk[f"special_{kind}_multiplier"])
        skill = self.selected_skill(target_level)
        ratio *= float(skill.get(f"{kind}_multiplier", 1.0))
        if self.is_special(target_level):
            ratio *= float(self.material(self.scenario.catalyst_id).get(f"{kind}_multiplier", 1.0))
        return min(max(ratio, 0.0), 1.0)

    def attempt_cost(self, target_level: int) -> int:
        economy = self.balance["economy"]
        decade = (target_level - 1) // 10
        cost = float(economy["base_attempt_cost"]) * target_level ** float(economy["attempt_cost_exponent"])
        cost *= 1.0 + decade * float(economy["attempt_decade_multiplier"])
        if self.is_special(target_level):
            cost *= float(economy["special_cost_multiplier"])
            cost += float(self.material(self.scenario.secondary_id).get("price", 0))
            cost += float(self.material(self.scenario.catalyst_id).get("price", 0))
        cost *= float(self.selected_skill(target_level).get("cost_multiplier", 1.0))
        return max(godot_round(cost), 1)

    def growth_gain(self, target_level: int, attack: int) -> int:
        growth = self.balance["growth"]
        decade = (target_level - 1) // 10
        special = self.is_special(target_level)
        rate = float(growth["normal_rate"]) + decade * float(growth["normal_rate_per_decade"])
        if special:
            rate = float(growth["special_rate"]) + decade * float(growth["special_rate_per_decade"])
        rate *= float(self.selected_skill(target_level).get("growth_multiplier", 1.0))
        if special:
            rate *= float(self.material(self.scenario.catalyst_id).get("growth_multiplier", 1.0))
        return max(math.ceil(attack * rate), 1)

    def milestone(self, level: int) -> dict[str, Any]:
        return next((item for item in self.milestones if int(item["level"]) == level), {})

    def choose_affix(self, excluded: set[str]) -> dict[str, Any]:
        tags = self.material(self.scenario.secondary_id).get("affix_tags", [])
        for tag in tags:
            candidate = next((item for item in self.affixes.values() if tag in item.get("material_tags", []) and item["id"] not in excluded), None)
            if candidate:
                return candidate
        return next((item for item in self.affixes.values() if item["id"] not in excluded), {})

    def apply_milestone(self, level: int) -> None:
        milestone = self.milestone(level)
        effect = milestone.get("effect")
        if effect == "ADD_AFFIX":
            excluded = {item["id"] for item in self.affix_list}
            definition = self.choose_affix(excluded)
            if definition:
                self.affix_list.append({"id": definition["id"], "tier": 1, "effects": definition["tiers"]["1"]})
        elif effect == "UPGRADE_AFFIX":
            index = int(milestone["slot"]) - 1
            if 0 <= index < len(self.affix_list):
                item = self.affix_list[index]
                tiers = self.affixes[item["id"]]["tiers"]
                tier = min(int(item["tier"]) + int(milestone.get("tier_delta", 1)), max(map(int, tiers)))
                item["tier"] = tier
                item["effects"] = tiers[str(tier)]
        elif effect == "ASCEND_ALL":
            for item in self.affix_list:
                tiers = self.affixes[item["id"]]["tiers"]
                tier = min(int(item["tier"]) + int(milestone.get("tier_delta", 1)), max(map(int, tiers)))
                item["tier"] = tier
                item["effects"] = tiers[str(tier)]

    def restore_to_level(self, level: int) -> None:
        self.progression_attack = self.attack_history[level]
        self.value_bonus_total = self.value_history[level]
        allowed = 0
        for milestone in self.milestones:
            if int(milestone["level"]) <= level and milestone["effect"] == "ADD_AFFIX":
                allowed += 1
        self.affix_list = self.affix_list[:allowed]
        for index, item in enumerate(self.affix_list, start=1):
            tier = 1
            for milestone in self.milestones:
                if int(milestone["level"]) <= level and int(milestone.get("slot", 0)) == index:
                    if milestone["effect"] == "UPGRADE_AFFIX":
                        tier += int(milestone.get("tier_delta", 1))
                    elif milestone["effect"] == "ASCEND_ALL":
                        tier += int(milestone.get("tier_delta", 1))
            tiers = self.affixes[item["id"]]["tiers"]
            tier = min(tier, max(map(int, tiers)))
            item["tier"] = tier
            item["effects"] = tiers[str(tier)]

    def final_attack(self) -> int:
        percent = sum(float(item["effects"].get("attack_percent", 0.0)) for item in self.affix_list)
        return godot_round(self.progression_attack * (1.0 + percent))

    def sale_price(self) -> int:
        if self.destroyed:
            return 0
        economy = self.balance["economy"]
        price = float(economy["base_weapon_price"])
        price += max(float(self.final_attack()), 1.0) ** float(economy["attack_price_exponent"]) * float(economy["attack_price_scale"])
        price += max(float(self.level), 0.0) ** float(economy["level_price_exponent"]) * float(economy["level_price_scale"])
        for item in self.affix_list:
            effects = item["effects"]
            price += int(item["tier"]) * 60.0
            price += float(effects.get("fire_damage", 0)) * 22.0
            price += float(effects.get("special_trigger_chance", 0.0)) * 1800.0
        return max(godot_round(price * (1.0 + max(self.value_bonus_total, 0.0))), 0)

    def resolve(self, roll: float | None = None, leap_roll: float | None = None) -> Attempt:
        if self.destroyed or self.level >= int(self.balance["max_level"]):
            raise RuntimeError("Attempted to resolve a completed simulation")
        target = self.level + 1
        cost = self.attempt_cost(target)
        self.total_attempts += 1
        self.total_spent += cost
        if self.is_special(target):
            self.material_attempts += 1
        success = self.success_chance(target)
        roll = self.rng.random() if roll is None else roll
        failure = 1.0 - success
        destroy = failure * self.conditional_risk(target, "destroy")
        downgrade = failure * (1.0 - self.conditional_risk(target, "destroy")) * self.conditional_risk(target, "downgrade")
        outcome = "SUCCESS" if roll < success else "DESTROY" if roll < success + destroy else "DOWNGRADE" if roll < success + destroy + downgrade else "HOLD"
        before = self.level
        downgrade_steps = 0
        leap = False
        if outcome == "SUCCESS":
            result_level = target
            skill = self.selected_skill(target)
            chance = float(skill.get("leap_chance", 0.0)) if self.can_use_overdrive(target) else 0.0
            leap_roll = self.rng.random() if leap_roll is None else leap_roll
            if chance and leap_roll < chance:
                leap = True
                result_level = min(target + max(int(skill.get("leap_levels", 2)), 2) - 1, int(self.balance["max_level"]))
            for reached in range(target, result_level + 1):
                self.progression_attack += self.growth_gain(reached, self.progression_attack)
                self.level = reached
                self.attack_history[reached] = self.progression_attack
                self.apply_milestone(reached)
                if self.is_special(reached):
                    self.value_bonus_total += float(self.material(self.scenario.catalyst_id).get("sale_value_bonus", 0.0)) + float(self.selected_skill(reached).get("sale_value_bonus", 0.0))
                self.value_history[reached] = self.value_bonus_total
            self.failure_streak = 0
        elif outcome == "DOWNGRADE":
            decade = (target - 1) // 10
            downgrade_steps = max(int(self.balance["risk"]["downgrade_steps_by_decade"].get(str(decade), 1)), 1)
            self.level = max(self.level - downgrade_steps, 0)
            self.restore_to_level(self.level)
            self.failure_streak += 1
        elif outcome == "DESTROY":
            self.destroyed = True
            self.level = 0
            self.progression_attack = 0
            self.affix_list.clear()
            self.failure_streak += 1
        else:
            self.failure_streak += 1
        self.max_failure_streak = max(self.max_failure_streak, self.failure_streak)
        return Attempt(outcome, target, self.level, success, cost, leap, downgrade_steps)


def load_simulator(root: Path, scenario: Scenario, seed: int = 0) -> EnhancementSimulator:
    def read(relative: str) -> dict[str, Any]:
        return json.loads((root / relative).read_text(encoding="utf-8"))
    balance = read(DATA_FILES[0])
    balance["milestones"] = read(DATA_FILES[1])["milestones"]
    materials = {item["id"]: item for item in read(DATA_FILES[2])["materials"]}
    affixes = {item["id"]: item for item in read(DATA_FILES[3])["affixes"]}
    return EnhancementSimulator(balance, balance["milestones"], materials, affixes, scenario, random.Random(seed))


def run_trial(root: Path, scenario: Scenario, seed: int) -> TrialResult:
    simulator = load_simulator(root, scenario, seed)
    outcomes: Counter[str] = Counter()
    while not simulator.destroyed and simulator.level < scenario.target_level:
        attempt = simulator.resolve()
        outcomes[attempt.outcome] += 1
    return TrialResult(
        simulator.level >= scenario.target_level,
        simulator.destroyed,
        "DESTROYED" if simulator.destroyed else "TARGET_REACHED",
        simulator.total_attempts,
        simulator.total_spent,
        simulator.material_attempts,
        outcomes,
        simulator.level,
        simulator.final_attack(),
        simulator.sale_price(),
        simulator.max_failure_streak,
    )


def input_fingerprint(root: Path) -> dict[str, str]:
    return {relative: hashlib.sha256((root / relative).read_bytes()).hexdigest() for relative in DATA_FILES}


def git_commit(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNVERIFIED"


def summarize(root: Path, scenario: Scenario, trials: int, seed: int) -> dict[str, Any]:
    results = [run_trial(root, scenario, seed + index) for index in range(trials)]
    attempts = [result.attempts for result in results]
    spent = [result.total_spent for result in results]
    return {
        "scenario": {"name": scenario.name, "target_level": scenario.target_level, "skill_id": scenario.skill_id, "secondary_id": scenario.secondary_id, "catalyst_id": scenario.catalyst_id, "precision_bonus": scenario.precision_bonus},
        "trials": trials,
        "seed_start": seed,
        "target_reach_rate": sum(item.reached_target for item in results) / trials,
        "destruction_rate": sum(item.destroyed for item in results) / trials,
        "attempts": {"mean": round(mean(attempts), 3), "median": median(attempts), "p90": percentile(attempts, 0.90), "p95": percentile(attempts, 0.95)},
        "gold_spent": {"mean": round(mean(spent), 3), "median": median(spent), "p90": percentile(spent, 0.90), "p95": percentile(spent, 0.95)},
        "outcomes": dict(sum((item.outcomes for item in results), Counter())),
        "material_attempts_mean": round(mean(item.material_attempts for item in results), 3),
        "max_failure_streak_p95": percentile([item.max_failure_streak for item in results], 0.95),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=29029)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.trials <= 0:
        parser.error("--trials must be positive")
    scenarios = [Scenario(target, skill) for target in (10, 30, 50, 70, 100) for skill in ("balanced", "safeguard", "overdrive")]
    payload = {
        "schema_version": 1,
        "tool": "tools/simulate_enhancement_balance.py",
        "input_commit": git_commit(ROOT),
        "input_sha256": input_fingerprint(ROOT),
        "randomness": {"engine": "python.random.MersenneTwister", "seed_strategy": "seed + trial_index", "semantic_parity": "fixed roll tests"},
        "scenarios": [summarize(ROOT, item, args.trials, args.seed) for item in scenarios],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Balance simulation complete: {len(scenarios)} scenarios x {args.trials} trials")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
