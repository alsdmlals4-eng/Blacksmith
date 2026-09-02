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
INTEGRATION_SPEC = importlib.util.spec_from_file_location(
    'pm_real_base_integration',
    ROOT / 'tests/test_pm_real_base_integration.py',
)
INTEGRATION = importlib.util.module_from_spec(INTEGRATION_SPEC)
INTEGRATION_SPEC.loader.exec_module(INTEGRATION)
MERGED_BASE_PM = '96bee2700c8931b9262ad5a24a0664a400858f20'
RETIRED_CANDIDATE = 'ff1dedc5dd1a5c770ea0f1f12efa7928484841c2'


class PMExecutionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / 'base'
        self.base.mkdir()
        (self.base / 'tools').mkdir()
        # Synthetic provider tests forwarding and checkout integrity, not Base validation correctness.
        (self.base / 'tools/project_work_tracking.py').write_text('# fixture\n')
        (self.base / 'tools/validate_work_contract_receipt.py').write_text('import json,sys\nprint(json.dumps(sys.argv[1:]))\n')
        (self.base / 'tools/helper.py').write_text('# tracked sibling\n')
        for args in (["init", "-q"], ["config", "user.email", "fixture@example.invalid"], ["config", "user.name", "fixture"], ["add", "tools"], ["commit", "-qm", "fixture"]):
            subprocess.run(['git', '-C', str(self.base), *args], check=True, capture_output=True)
        self.sha = subprocess.check_output(['git', '-C', str(self.base), 'rev-parse', 'HEAD'], text=True).strip()

    def _write_placeholder_pm_base(self, root: Path) -> str:
        root.mkdir()
        for relative in INTEGRATION.REQUIRED_MERGED_PM_PATHS:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if relative == INTEGRATION.RECEIPT_RELATIVE:
                path.write_text(
                    json.dumps({
                        'project_work_kanban': {
                            'progress_summary': {'display': '3 / 4'},
                            'work_items': [
                                {'work_item_id': 'BS-PM-04', 'status': 'VERIFY_REVIEW'}
                            ],
                        }
                    }),
                    encoding='utf-8',
                )
            elif relative == 'tools/check_pm_work_receipt.py':
                path.write_text(
                    f'{GATE.PM_TOOLING_COMMIT}\nGIT_NO_REPLACE_OBJECTS\n',
                    encoding='utf-8',
                )
            else:
                path.write_text('fixture\n', encoding='utf-8')
        for args in (
            ['init', '-q'],
            ['config', 'user.email', 'fixture@example.invalid'],
            ['config', 'user.name', 'fixture'],
            ['add', '.'],
            ['commit', '-qm', 'base'],
        ):
            subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)
        return subprocess.check_output(
            ['git', '-C', str(root), 'rev-parse', 'HEAD'],
            text=True,
        ).strip()

    def _clone_receipt_subject(self, project_base: Path, *, mode_change: bool = False) -> tuple[Path, str]:
        subject = Path(self.tmp.name) / ('subject-mode' if mode_change else 'subject-placeholders')
        subprocess.run(
            ['git', 'clone', '-q', str(project_base), str(subject)],
            check=True,
            capture_output=True,
        )
        subprocess.run(['git', '-C', str(subject), 'config', 'user.email', 'fixture@example.invalid'], check=True)
        subprocess.run(['git', '-C', str(subject), 'config', 'user.name', 'fixture'], check=True)
        subject_receipt = subject / INTEGRATION.RECEIPT_RELATIVE
        receipt_value = json.loads(subject_receipt.read_text(encoding='utf-8'))
        receipt_value['receipt_tail'] = True
        subject_receipt.write_text(json.dumps(receipt_value), encoding='utf-8')
        subprocess.run(
            ['git', '-C', str(subject), 'add', INTEGRATION.RECEIPT_RELATIVE],
            check=True,
        )
        if mode_change:
            (subject / 'scripts/tool.sh').chmod(0o755)
            subprocess.run(
                ['git', '-C', str(subject), 'add', '--chmod=+x', 'scripts/tool.sh'],
                check=True,
            )
        subprocess.run(
            ['git', '-C', str(subject), 'commit', '-qm', 'receipt tail fixture'],
            check=True,
        )
        subject_sha = subprocess.check_output(
            ['git', '-C', str(subject), 'rev-parse', 'HEAD'],
            text=True,
        ).strip()
        return subject, subject_sha

    def test_operational_surfaces_pin_merged_base_pm_tooling(self):
        self.assertEqual(MERGED_BASE_PM, GATE.PM_TOOLING_COMMIT)
        workflow = (ROOT / '.github/workflows/validate-current-base-adaptation-work-contract.yml').read_text(encoding='utf-8')
        receipt = (ROOT / 'docs/operations/receipts/2026-09-02-pm-execution-gate.json').read_text(encoding='utf-8')
        owner = (ROOT / 'docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md').read_text(encoding='utf-8')
        pm_section = owner.split('## 9. PM execution-gate integration', 1)[1]
        for name, value in (('workflow', workflow), ('receipt', receipt), ('owner PM section', pm_section)):
            with self.subTest(surface=name):
                self.assertIn(MERGED_BASE_PM, value)
                self.assertNotIn(RETIRED_CANDIDATE, value)
        self.assertIn('ref: ${{ github.event.pull_request.head.sha || inputs.expected_subject_head_sha }}', workflow)
        self.assertIn('python -m pip install -r base-pm/.github/validation-requirements.txt', workflow)
        self.assertIn('runs-on: ubuntu-24.04', workflow)
        self.assertIn('timeout-minutes: 5', workflow)
        self.assertIn('workflow supplies independently fresh-read source and subject revisions', pm_section)
        self.assertNotIn('derives its source baseline', pm_section)

    def test_workflow_covers_every_checker_input_and_trusted_revision_env(self):
        workflow = (ROOT / '.github/workflows/validate-current-base-adaptation-work-contract.yml').read_text(encoding='utf-8')
        integration = (ROOT / 'tests/test_pm_real_base_integration.py').read_text(encoding='utf-8')
        for path in (
            'AGENTS.md',
            'docs/BASE_RULES_VERSION.md',
            'docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md',
            'docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md',
            'skills/PROJECT_BASE_ADAPTER.json',
        ):
            with self.subTest(path=path):
                self.assertIn(f'- "{path}"', workflow)
        for token in (
            'expected_source_sha:',
            'expected_subject_head_sha:',
            'ref: ${{ github.event.pull_request.base.sha || inputs.expected_source_sha }}',
            'path: project-base',
            'BS_PM_EXPECTED_SOURCE_SHA: ${{ github.event.pull_request.base.sha || inputs.expected_source_sha }}',
            'BS_PM_EXPECTED_SUBJECT_HEAD_SHA: ${{ github.event.pull_request.head.sha || inputs.expected_subject_head_sha }}',
            'BS_PM_PROJECT_BASE_ROOT: ../project-base',
        ):
            with self.subTest(token=token):
                self.assertIn(token, workflow)
        for token in (
            'RECEIPT_ONLY_CLOSURE_CHANGED_PATHS',
            'REVIEWED_INTEGRATION_MANIFEST_RELATIVE',
            'def verify_receipt_only_closure(',
            'BS_PM_PROJECT_BASE_ROOT',
        ):
            with self.subTest(integration_token=token):
                self.assertIn(token, integration)

    def test_receipt_only_proof_rejects_unreviewed_placeholder_artifacts(self):
        project_base = Path(self.tmp.name) / 'project-base-placeholders'
        source_sha = self._write_placeholder_pm_base(project_base)
        subject, subject_sha = self._clone_receipt_subject(project_base)
        errors = INTEGRATION.verify_receipt_only_closure(
            subject,
            project_base,
            source_sha,
            subject_sha,
        )
        self.assertIn(
            INTEGRATION.REVIEWED_INTEGRATION_MANIFEST_RELATIVE,
            '; '.join(errors),
        )

    def test_receipt_only_proof_rejects_mode_only_extra_change(self):
        project_base = Path(self.tmp.name) / 'project-base-mode'
        source_sha = self._write_placeholder_pm_base(project_base)
        extra = project_base / 'scripts/tool.sh'
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_text('#!/bin/sh\nexit 0\n', encoding='utf-8')
        extra.chmod(0o644)
        subprocess.run(['git', '-C', str(project_base), 'add', 'scripts/tool.sh'], check=True)
        subprocess.run(['git', '-C', str(project_base), 'commit', '-qm', 'add mode fixture'], check=True)
        source_sha = subprocess.check_output(
            ['git', '-C', str(project_base), 'rev-parse', 'HEAD'],
            text=True,
        ).strip()
        subject, subject_sha = self._clone_receipt_subject(project_base, mode_change=True)
        errors = INTEGRATION.verify_receipt_only_closure(
            subject,
            project_base,
            source_sha,
            subject_sha,
        )
        self.assertIn('scripts/tool.sh', '; '.join(errors))

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

    def test_crlf_conversion_is_rejected_as_executable_byte_drift(self):
        path = self.base / 'tools/project_work_tracking.py'
        subprocess.run(['git', '-C', str(self.base), 'update-index', '--assume-unchanged', 'tools/project_work_tracking.py'], check=True)
        path.write_bytes(path.read_bytes().replace(b'\n', b'\r\n'))
        self.assertTrue(GATE.check_tooling(self.base, self.sha))

    def test_untracked_import_shadow_in_tools_is_rejected(self):
        (self.base / 'tools/json.py').write_text('raise RuntimeError("shadowed")\n')
        self.assertTrue(GATE.check_tooling(self.base, self.sha))

    def test_modified_tracked_sibling_in_tools_is_rejected(self):
        (self.base / 'tools/helper.py').write_text('# modified sibling\n')
        self.assertTrue(GATE.check_tooling(self.base, self.sha))

    def test_untracked_replacement_is_rejected(self):
        subprocess.run(['git', '-C', str(self.base), 'rm', '--cached', '-q', 'tools/project_work_tracking.py'], check=True)
        self.assertTrue(GATE.check_tooling(self.base, self.sha))

    def test_git_replace_cannot_substitute_the_selected_commit(self):
        original = self.sha
        (self.base / 'tools/validate_work_contract_receipt.py').write_text('raise RuntimeError("replacement executed")\n')
        subprocess.run(['git', '-C', str(self.base), 'add', 'tools'], check=True)
        subprocess.run(['git', '-C', str(self.base), 'commit', '-qm', 'replacement'], check=True)
        replacement = subprocess.check_output(['git', '-C', str(self.base), 'rev-parse', 'HEAD'], text=True).strip()
        subprocess.run(['git', '-C', str(self.base), 'replace', original, replacement], check=True)
        subprocess.run(['git', '-C', str(self.base), 'reset', '--hard', original], check=True, capture_output=True)
        self.assertEqual(original, subprocess.check_output(['git', '-C', str(self.base), 'rev-parse', 'HEAD'], text=True).strip())
        self.assertIn('replacement executed', (self.base / 'tools/validate_work_contract_receipt.py').read_text())
        self.assertTrue(GATE.check_tooling(self.base, original))

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
