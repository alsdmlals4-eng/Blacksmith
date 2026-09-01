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
# Fixed historical test input, not a claim about future current project HEAD.
SOURCE = '511e6047607f2f9bb63e75fa9df019665b922e24'


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

    def invoke(self, value, phase='start', source=SOURCE):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'receipt.json'
            path.write_text(json.dumps(value, ensure_ascii=True), encoding='utf-8')
            return subprocess.run([sys.executable, str(ROOT / 'tools/check_pm_work_receipt.py'), '--base-root', str(self.base), '--receipt', str(path), '--phase', phase, '--expected-source-sha', source], text=True, capture_output=True, check=False, timeout=120)

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

    def test_unfinished_project_is_not_complete(self):
        result = self.invoke(self.receipt, phase='closeout')
        self.assertNotEqual(0, result.returncode)
        self.assertIn('closeout', result.stdout)

    def test_mislabeled_done_does_not_pass(self):
        value = copy.deepcopy(self.receipt)
        value['project_work_kanban']['work_items'][1]['status'] = 'DONE'
        result = self.invoke(value, phase='closeout')
        self.assertNotEqual(0, result.returncode)
        self.assertIn('DONE', result.stdout)


if __name__ == '__main__':
    unittest.main()
