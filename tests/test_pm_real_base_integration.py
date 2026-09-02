"""Real Base integration; missing external checkout is an error, never a skip."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('pm_gate', ROOT / 'tools/check_pm_work_receipt.py')
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
RECEIPT = ROOT / 'docs/operations/receipts/2026-09-02-pm-execution-gate.json'
# Fixed current integration baseline; callers must still fresh-read before real execution.
SOURCE = '296ad86c2315357998ed86c594b8b006a1bde420'


class PMRealBaseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configured = os.environ.get('BS_BASE_PM_ROOT')
        if not configured:
            raise RuntimeError('BS_BASE_PM_ROOT must name the exact selected Base checkout')
        cls.base = Path(configured)
        errors = GATE.check_tooling(cls.base)
        if errors:
            raise RuntimeError('; '.join(errors))
        cls.receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))

    def invoke(self, value, phase='start', source=SOURCE, expected_head=None):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'receipt.json'
            path.write_text(json.dumps(value, ensure_ascii=True), encoding='utf-8')
            argv = [
                sys.executable,
                str(ROOT / 'tools/check_pm_work_receipt.py'),
                '--base-root',
                str(self.base),
                '--receipt',
                str(path),
                '--phase',
                phase,
                '--expected-source-sha',
                source,
            ]
            if expected_head is not None:
                argv.extend(['--expected-head-sha', expected_head])
            return subprocess.run(argv, text=True, capture_output=True, check=False, timeout=120)

    def complete_copy(self):
        value = copy.deepcopy(self.receipt)
        board = value['project_work_kanban']
        board['active_work_item_ref'] = None
        board['next_action'] = 'STOP_APPROVED_SCOPE_COMPLETE'
        for item in board['work_items']:
            item['status'] = 'DONE'
            for check in item['checklist']:
                check['status'] = 'PASS'
                check['evidence'] = ['synthetic integration fixture evidence']
            for verification in item['verification']:
                verification['status'] = 'PASS'
                verification['evidence'] = ['synthetic integration fixture evidence']
            item['verified_head_sha'] = SOURCE
            item['repository_readback'] = 'PASS'
            item['readback_evidence'] = ['synthetic exact-head readback fixture']
            item['rollback'] = 'Synthetic test fixture only; discard the temporary file.'
            item['must_fix_remaining'] = 0
            item['blocked_unverified_remaining'] = 0
            item['user_decision_required_remaining'] = 0
        board['progress_summary'] = {
            'completed_items': len(board['work_items']),
            'applicable_items': len(board['work_items']),
            'display': f"{len(board['work_items'])} / {len(board['work_items'])}",
        }
        return value

    def test_real_project_receipt_is_rendered(self):
        result = self.invoke(self.receipt)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        for expected in ('1 / 4', 'BS-PM-02', 'IN_PROGRESS'):
            self.assertIn(expected, result.stdout)

    def test_missing_pm_is_rejected_by_actual_base(self):
        value = copy.deepcopy(self.receipt); value.pop('project_work_kanban')
        result = self.invoke(value)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('project_work_kanban', result.stdout)

    def test_wrong_trusted_source_is_rejected(self):
        result = self.invoke(self.receipt, source='a' * 40)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('source_main_sha', result.stdout)

    def test_closeout_requires_trusted_head_at_project_wrapper(self):
        result = self.invoke(self.receipt, phase='closeout')
        self.assertNotEqual(0, result.returncode)
        self.assertIn('fresh-read 40-character verified subject HEAD', result.stdout)

    def test_unfinished_project_is_not_complete(self):
        result = self.invoke(self.receipt, phase='closeout', expected_head=SOURCE)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('closeout', result.stdout)

    def test_mislabeled_done_does_not_pass(self):
        value = copy.deepcopy(self.receipt)
        value['project_work_kanban']['work_items'][1]['status'] = 'DONE'
        result = self.invoke(value, phase='closeout', expected_head=SOURCE)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('DONE', result.stdout)

    def test_complete_copy_passes_only_for_matching_trusted_head(self):
        value = self.complete_copy()
        passed = self.invoke(value, phase='closeout', expected_head=SOURCE)
        self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
        self.assertIn('4 / 4', passed.stdout)

        stale = self.invoke(value, phase='closeout', expected_head='b' * 40)
        self.assertNotEqual(0, stale.returncode)
        self.assertIn('verified_head_sha', stale.stdout)
        self.assertNotIn('## PM 작업 체크리스트 — 4 / 4', stale.stdout)


if __name__ == '__main__':
    unittest.main()
