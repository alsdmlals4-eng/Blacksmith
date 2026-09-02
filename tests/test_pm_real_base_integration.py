"""Real Base integration; missing external checkout or trusted revisions is an error."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('pm_gate', ROOT / 'tools/check_pm_work_receipt.py')
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
RECEIPT_RELATIVE = 'docs/operations/receipts/2026-09-02-pm-execution-gate.json'
RECEIPT = ROOT / RECEIPT_RELATIVE
SHA = re.compile(r'[0-9a-f]{40}\Z')
RECEIPT_ONLY_CLOSURE_CHANGED_PATHS = frozenset({RECEIPT_RELATIVE})
REQUIRED_MERGED_PM_PATHS = frozenset({
    '.github/workflows/validate-current-base-adaptation-work-contract.yml',
    'docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md',
    RECEIPT_RELATIVE,
    'tests/test_pm_execution_gate.py',
    'tests/test_pm_real_base_integration.py',
    'tools/check_pm_work_receipt.py',
})


def _git(root: Path, *args: str, text: bool = False) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment['GIT_NO_REPLACE_OBJECTS'] = '1'
    return subprocess.run(
        ['git', '-C', str(root), *args],
        text=text,
        capture_output=True,
        check=False,
        timeout=30,
        env=environment,
    )


def _exact_repository_head(root: Path, expected_sha: str, label: str) -> list[str]:
    if not root.is_dir() or root.is_symlink():
        return [f'{label} checkout is missing or a symlink']
    top = _git(root, 'rev-parse', '--show-toplevel', text=True)
    head = _git(root, 'rev-parse', 'HEAD', text=True)
    errors: list[str] = []
    if top.returncode or Path(top.stdout.strip()).resolve() != root.resolve():
        errors.append(f'{label} path is not its repository root')
    if head.returncode or head.stdout.strip() != expected_sha:
        errors.append(f'{label} HEAD does not match its independently supplied SHA')
    return errors


def _tree_blobs(root: Path) -> tuple[dict[str, str], list[str]]:
    listed = _git(root, 'ls-tree', '-r', '-z', '--full-tree', 'HEAD')
    if listed.returncode:
        return {}, ['repository tree cannot be read']
    entries: dict[str, str] = {}
    try:
        for record in listed.stdout.split(b'\0'):
            if not record:
                continue
            metadata, raw_path = record.split(b'\t', 1)
            parts = metadata.split()
            if len(parts) != 3:
                return {}, ['repository tree entry is malformed']
            entries[raw_path.decode('utf-8')] = parts[2].decode('ascii')
    except (UnicodeDecodeError, ValueError):
        return {}, ['repository tree contains an undecodable entry']
    return entries, []


def verify_receipt_only_closure(
    project_root: Path,
    project_base_root: Path,
    source_sha: str,
    subject_sha: str,
) -> list[str]:
    """Prove that a complete receipt is only metadata over the merged PM base."""
    errors: list[str] = []
    if SHA.fullmatch(source_sha) is None or SHA.fullmatch(subject_sha) is None:
        return ['receipt-only closure requires exact source and subject SHAs']
    errors.extend(_exact_repository_head(project_root, subject_sha, 'project subject'))
    errors.extend(_exact_repository_head(project_base_root, source_sha, 'project base'))
    if errors:
        return errors

    subject_tree, subject_errors = _tree_blobs(project_root)
    base_tree, base_errors = _tree_blobs(project_base_root)
    errors.extend(subject_errors)
    errors.extend(base_errors)
    if errors:
        return errors

    changed_paths = {
        path
        for path in set(subject_tree) | set(base_tree)
        if subject_tree.get(path) != base_tree.get(path)
    }
    if changed_paths != RECEIPT_ONLY_CLOSURE_CHANGED_PATHS:
        errors.append(
            'receipt-only closure changed paths must be exactly '
            f'{sorted(RECEIPT_ONLY_CLOSURE_CHANGED_PATHS)}; observed {sorted(changed_paths)}'
        )

    missing = sorted(REQUIRED_MERGED_PM_PATHS - set(base_tree))
    if missing:
        errors.append(f'project base does not contain the merged PM integration: {missing}')
    else:
        try:
            base_receipt = json.loads((project_base_root / RECEIPT_RELATIVE).read_text(encoding='utf-8'))
            base_board = base_receipt['project_work_kanban']
            base_item = next(
                item for item in base_board['work_items']
                if item['work_item_id'] == 'BS-PM-04'
            )
            if base_board.get('progress_summary', {}).get('display') != '3 / 4':
                errors.append('project base must preserve the reviewed 3 / 4 premerge receipt')
            if base_item.get('status') != 'VERIFY_REVIEW':
                errors.append('project base must keep BS-PM-04 in VERIFY_REVIEW before closure')
            wrapper = (project_base_root / 'tools/check_pm_work_receipt.py').read_text(encoding='utf-8')
            if GATE.PM_TOOLING_COMMIT not in wrapper or 'GIT_NO_REPLACE_OBJECTS' not in wrapper:
                errors.append('project base PM wrapper does not contain the reviewed merged-tooling boundary')
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, StopIteration, TypeError):
            errors.append('project base PM integration evidence cannot be read')
    return errors


class PMRealBaseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configured = os.environ.get('BS_BASE_PM_ROOT')
        project_base = os.environ.get('BS_PM_PROJECT_BASE_ROOT')
        if not configured:
            raise RuntimeError('BS_BASE_PM_ROOT must name the exact selected Base checkout')
        if not project_base:
            raise RuntimeError('BS_PM_PROJECT_BASE_ROOT must name the independently checked-out project base')
        cls.base = Path(configured)
        cls.project_base = Path(project_base)
        errors = GATE.check_tooling(cls.base)
        if errors:
            raise RuntimeError('; '.join(errors))
        cls.receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
        cls.source = os.environ.get('BS_PM_EXPECTED_SOURCE_SHA')
        cls.subject = os.environ.get('BS_PM_EXPECTED_SUBJECT_HEAD_SHA')
        for name, value in (
            ('BS_PM_EXPECTED_SOURCE_SHA', cls.source),
            ('BS_PM_EXPECTED_SUBJECT_HEAD_SHA', cls.subject),
        ):
            if not isinstance(value, str) or SHA.fullmatch(value) is None:
                raise RuntimeError(f'{name} must be an independently supplied exact 40-character SHA')
        cls.receipt_complete = all(
            item.get('status') == 'DONE'
            for item in cls.receipt['project_work_kanban']['work_items']
        )
        cls.closure_errors = verify_receipt_only_closure(
            ROOT,
            cls.project_base,
            cls.source,
            cls.subject,
        )
        if cls.receipt_complete and cls.closure_errors:
            raise RuntimeError('; '.join(cls.closure_errors))

    def invoke(self, value, phase='start', source=None, expected_head=None):
        selected_source = self.source if source is None else source
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
                selected_source,
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
            item['verified_head_sha'] = self.subject
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

    def test_repository_receipt_matches_its_declared_phase(self):
        board = self.receipt['project_work_kanban']
        if self.receipt_complete:
            # Base-bound closeout is allowed only after the exact-tree proof in setUpClass.
            result = self.invoke(self.receipt, phase='closeout', expected_head=self.source)
            expected = [f"{len(board['work_items'])} / {len(board['work_items'])}", 'STOP_APPROVED_SCOPE_COMPLETE']
        else:
            active = board['active_work_item_ref']
            active_item = next(item for item in board['work_items'] if item['work_item_id'] == active)
            result = self.invoke(self.receipt)
            expected = [board['progress_summary']['display'], active, active_item['status'], 'ACTIVE']
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        for text in expected:
            self.assertIn(text, result.stdout)

    def test_base_bound_closeout_requires_mechanically_proven_receipt_only_diff(self):
        if self.receipt_complete:
            self.assertEqual([], self.closure_errors)
        else:
            self.assertTrue(self.closure_errors)
            self.assertIn('receipt-only closure changed paths', '; '.join(self.closure_errors))

    def test_receipt_cannot_select_its_own_trusted_source(self):
        value = copy.deepcopy(self.receipt)
        replacement = 'f' * 40 if self.source != 'f' * 40 else 'e' * 40
        value['project_work_kanban']['source_main_sha'] = replacement
        result = self.invoke(value)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('source_main_sha', result.stdout)

    def test_missing_pm_is_rejected_by_actual_base(self):
        value = copy.deepcopy(self.receipt); value.pop('project_work_kanban')
        result = self.invoke(value)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('project_work_kanban', result.stdout)

    def test_wrong_trusted_source_is_rejected(self):
        wrong = 'a' * 40 if self.source != 'a' * 40 else 'b' * 40
        result = self.invoke(self.receipt, source=wrong)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('source_main_sha', result.stdout)

    def test_closeout_requires_trusted_head_at_project_wrapper(self):
        result = self.invoke(self.receipt, phase='closeout')
        self.assertNotEqual(0, result.returncode)
        self.assertIn('fresh-read 40-character verified subject HEAD', result.stdout)

    def test_unfinished_project_is_not_complete(self):
        value = copy.deepcopy(self.receipt)
        board = value['project_work_kanban']
        board['active_work_item_ref'] = board['work_items'][0]['work_item_id']
        board['next_action'] = 'Continue the approved integration fixture'
        board['work_items'][0]['status'] = 'IN_PROGRESS'
        result = self.invoke(value, phase='closeout', expected_head=self.subject)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('closeout', result.stdout)

    def test_mislabeled_done_does_not_pass(self):
        value = copy.deepcopy(self.receipt)
        item = value['project_work_kanban']['work_items'][1]
        item['status'] = 'DONE'
        item.pop('verified_head_sha', None)
        result = self.invoke(value, phase='closeout', expected_head=self.subject)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('DONE', result.stdout)

    def test_complete_copy_passes_only_for_matching_trusted_head(self):
        value = self.complete_copy()
        passed = self.invoke(value, phase='closeout', expected_head=self.subject)
        self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
        self.assertIn('4 / 4', passed.stdout)

        stale_head = 'b' * 40 if self.subject != 'b' * 40 else 'c' * 40
        stale = self.invoke(value, phase='closeout', expected_head=stale_head)
        self.assertNotEqual(0, stale.returncode)
        self.assertIn('verified_head_sha', stale.stdout)
        self.assertNotIn('## PM 작업 체크리스트 — 4 / 4', stale.stdout)


if __name__ == '__main__':
    unittest.main()
