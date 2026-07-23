from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import validate_lifecycle_data


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DATA = ROOT / "data"


class LifecycleDataContractTests(unittest.TestCase):
    def _copy_lifecycle_data(self, target: Path) -> None:
        for relative in (
            "progression/workshop_day_balance.json",
            "crafting/craftsmanship_grades.json",
            "customers/gladiator_poc.json",
            "world/gladiator_match_poc.json",
            "crafting/affixes.json",
        ):
            source = SOURCE_DATA / relative
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def _validate(self, mutate=None) -> list[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            data_root = Path(temp_dir)
            self._copy_lifecycle_data(data_root)
            if mutate is not None:
                mutate(data_root)
            errors = validate_lifecycle_data.ValidationErrors()
            validate_lifecycle_data.validate_lifecycle_poc(errors, data_root)
            return errors.items

    @staticmethod
    def _mutate_json(data_root: Path, relative: str, callback) -> None:
        path = data_root / relative
        payload = json.loads(path.read_text(encoding="utf-8"))
        callback(payload)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_current_lifecycle_data_passes(self) -> None:
        self.assertEqual([], self._validate())

    def test_grade_distribution_must_sum_to_one(self) -> None:
        def mutate(root: Path) -> None:
            self._mutate_json(
                root,
                "crafting/craftsmanship_grades.json",
                lambda payload: payload["precision_distributions"]["STANDARD"].__setitem__("STANDARD", 0.9),
            )

        self.assertTrue(any("distribution" in item for item in self._validate(mutate)))

    def test_grade_ids_must_be_unique(self) -> None:
        def mutate(root: Path) -> None:
            self._mutate_json(
                root,
                "crafting/craftsmanship_grades.json",
                lambda payload: payload["grades"].append(dict(payload["grades"][0])),
            )

        self.assertTrue(any("duplicate grade id" in item for item in self._validate(mutate)))

    def test_contract_affixes_must_exist(self) -> None:
        def mutate(root: Path) -> None:
            self._mutate_json(
                root,
                "customers/gladiator_poc.json",
                lambda payload: payload.__setitem__("preferred_affix_ids", ["unknown_affix"]),
            )

        self.assertTrue(any("unknown preferred affix" in item for item in self._validate(mutate)))

    def test_result_bands_must_be_ordered(self) -> None:
        def mutate(root: Path) -> None:
            self._mutate_json(
                root,
                "world/gladiator_match_poc.json",
                lambda payload: payload["result_bands"][1].__setitem__("minimum_score", 10),
            )

        self.assertTrue(any("strictly increasing" in item for item in self._validate(mutate)))

    def test_every_result_band_requires_reachable_fixture(self) -> None:
        def mutate(root: Path) -> None:
            self._mutate_json(
                root,
                "world/gladiator_match_poc.json",
                lambda payload: payload.__setitem__("reachability_fixtures", payload["reachability_fixtures"][:-1]),
            )

        self.assertTrue(any("reachable fixture" in item for item in self._validate(mutate)))


if __name__ == "__main__":
    unittest.main()
