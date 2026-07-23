from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("check_no_merge_conflicts.py")
SPEC = importlib.util.spec_from_file_location("check_no_merge_conflicts", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MergeConflictScannerTests(unittest.TestCase):
    def test_detects_complete_conflict_block(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "broken.md").write_text(
                "before\n<<<<<<< HEAD\nnew\n=======\nold\n>>>>>>> parent\nafter\n",
                encoding="utf-8",
            )

            self.assertEqual(MODULE.find_conflicts(root), ["broken.md"])

    def test_ignores_documented_isolated_marker_words(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.md").write_text(
                "검사 대상 문자열: <<<<<<<, =======, >>>>>>>\n",
                encoding="utf-8",
            )

            self.assertEqual(MODULE.find_conflicts(root), [])

    def test_ignores_generated_and_vendored_work_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ignored = root / "artifacts"
            ignored.mkdir()
            (ignored / "broken.md").write_text(
                "<<<<<<< HEAD\nnew\n=======\nold\n>>>>>>> parent\n",
                encoding="utf-8",
            )

            self.assertEqual(MODULE.find_conflicts(root), [])


if __name__ == "__main__":
    unittest.main()
