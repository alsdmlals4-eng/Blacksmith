"""Blacksmith에 통합된 Godot AI 자기 업데이트 안전성 구조를 검증합니다."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPO_ROOT / "addons" / "godot_ai"
PLUGIN_GD = PLUGIN_ROOT / "plugin.gd"


class PluginSelfUpdateSafetyTests(unittest.TestCase):
    def test_update_backup_suffix_stays_in_sync(self) -> None:
        """백업 파일 suffix의 생산자와 검사자가 같은 값을 사용해야 합니다."""
        runner = (PLUGIN_ROOT / "update_reload_runner.gd").read_text(encoding="utf-8")
        scanner = (PLUGIN_ROOT / "utils" / "update_mixed_state.gd").read_text(encoding="utf-8")

        runner_match = re.search(
            r'^const\s+INSTALL_BACKUP_SUFFIX\s*:=\s*"([^"]+)"',
            runner,
            re.MULTILINE,
        )
        self.assertIsNotNone(
            runner_match,
            'update_reload_runner.gd must declare `const INSTALL_BACKUP_SUFFIX := "..."`.',
        )

        scanner_match = re.search(
            r'^const\s+BACKUP_SUFFIX\s*:=\s*"([^"]+)"',
            scanner,
            re.MULTILINE,
        )
        self.assertIsNotNone(
            scanner_match,
            'update_mixed_state.gd must declare `const BACKUP_SUFFIX := "..."`.',
        )
        assert runner_match is not None and scanner_match is not None
        self.assertEqual(runner_match.group(1), scanner_match.group(1))

    def test_plugin_documents_the_untyped_policy(self) -> None:
        """장기 생존 필드를 untyped로 유지하는 자기 업데이트 정책을 보존합니다."""
        source = PLUGIN_GD.read_text(encoding="utf-8")
        normalized = " ".join(line.strip("# \t") for line in source.splitlines())

        self.assertIn("Self-update field and load-surface policy", source)
        for issue in ("#242", "#244", "#398"):
            self.assertIn(issue, source)
        self.assertIn("single-phase runner", source)
        self.assertIn("preload aliases are not the self-update safety metric", normalized)
        self.assertTrue("static-var" in source.lower() or "static var" in source.lower())


if __name__ == "__main__":
    unittest.main()
