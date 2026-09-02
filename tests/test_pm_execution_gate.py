from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('pm_gate', ROOT / 'tools/check_pm_work_receipt.py')
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class PMExecutionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / 'base'
        self.base.mkdir()
        (self.base / 'tools').mkdir()
        # Synthetic provider tests forwarding only, not Base validation correctness.
        (self.base / 'tools/project_work_tracking.py').write_text('# fixture\n')
        (self.base / 'tools/validate_work_contract_receipt.py').write_text('import json,sys\nprint(json.dumps(sys.argv[1:]))\n')
        for args in (["init", "-q"], ["config", "user.email", "fixture@example.invalid"], ["config", "user.name", "fixture"], ["add", "tools"], ["commit", "-qm", "fixture"]):
            subprocess.run(['git', '-C', str(self.base), *args], check=True, capture_output=True)
        self.sha = subprocess.check_output(['git', '-C', str(self.base), 'rev-parse', 'HEAD'], text=True).strip()

    def test_wrong_checkout_is_rejected(self):
        self.assertTrue(GATE.check_tooling(self.base, '0' * 40))

    def test_clean_pinned_checkout_is_accepted(self):
        self.assertEqual([], GATE.check_tooling(self.base, self.sha))

    def test_dirty_pinned_python_is_rejected(self):
        (self.base / 'tools/project_work_tracking.py').write_text('# tampered\n')
        self.assertTrue(GATE.check_tooling(self.base, self.sha))

    def test_assume_unchanged_does_not_hide_modified_tool_bytes(self):
        subprocess.run(['git', '-C', str(self.base), 'update-index', '--assume-unchanged', 'tools/project_work_tracking.py'], check=True)
        (self.base / 'tools/project_work_tracking.py').write_text('# hidden tamper\n')
        self.assertTrue(GATE.check_tooling(self.base, self.sha))

    def test_untracked_replacement_is_rejected(self):
        subprocess.run(['git', '-C', str(self.base), 'rm', '--cached', '-q', 'tools/project_work_tracking.py'], check=True)
        self.assertTrue(GATE.check_tooling(self.base, self.sha))

    def test_nested_path_is_not_repository_root(self):
        self.assertTrue(GATE.check_tooling(self.base / 'tools', self.sha))

    def test_command_forwards_required_phase_source_and_visible_output(self):
        receipt = Path(self.tmp.name) / 'receipt with spaces.json'; receipt.write_text('{}')
        result = subprocess.run(GATE.command(self.base, receipt, 'resume', 'a' * 40), text=True, capture_output=True, check=True)
        self.assertEqual(['--receipt', str(receipt), '--phase', 'resume', '--expected-source-sha', 'a' * 40, '--render-markdown'], json.loads(result.stdout))

    def test_closeout_forwards_independently_supplied_trusted_head(self):
        receipt = Path(self.tmp.name) / 'receipt.json'; receipt.write_text('{}')
        result = subprocess.run(
            GATE.command(self.base, receipt, 'closeout', 'a' * 40, 'b' * 40),
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(
            [
                '--receipt', str(receipt), '--phase', 'closeout',
                '--expected-source-sha', 'a' * 40,
                '--expected-head-sha', 'b' * 40,
                '--render-markdown',
            ],
            json.loads(result.stdout),
        )

    def test_closeout_requires_exact_trusted_head_before_execution(self):
        for head in (None, 'main', 'A' * 40):
            with self.subTest(head=head):
                with self.assertRaises(ValueError):
                    GATE.command(self.base, Path('r.json'), 'closeout', 'a' * 40, head)

    def test_non_closeout_rejects_misleading_head_argument(self):
        for phase in ('start', 'resume'):
            with self.subTest(phase=phase):
                with self.assertRaises(ValueError):
                    GATE.command(self.base, Path('r.json'), phase, 'a' * 40, 'b' * 40)

    def test_invalid_phase_and_source_are_rejected_before_execution(self):
        for phase, source in [('new-goal', 'a' * 40), ('start', 'main'), ('start', None)]:
            with self.subTest(phase=phase, source=source):
                with self.assertRaises(ValueError):
                    GATE.command(self.base, Path('r.json'), phase, source)

    def test_cli_missing_tooling_does_not_pass(self):
        result = subprocess.run([sys.executable, str(ROOT / 'tools/check_pm_work_receipt.py'), '--base-root', str(self.base / 'missing'), '--receipt', 'r.json', '--expected-source-sha', 'a' * 40], text=True, capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('BLOCKED_UNVERIFIED', result.stdout)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
