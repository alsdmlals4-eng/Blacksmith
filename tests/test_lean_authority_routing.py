# 현재 책임 경로 검사가 끊어진 참조와 안전 경계 손실을 검출하는지 확인한다.
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = Path('docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md')
spec = importlib.util.spec_from_file_location('entrypoint', ROOT / 'tests/check_current_authority_entrypoint_contract.py')
entrypoint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entrypoint)


class LeanAuthorityRoutingTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(entrypoint, 'validate', None)),
                        'entrypoint must validate actual owner paths, not historical AGENTS literals')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.contract = (ROOT / CONTRACT).read_text(encoding='utf-8')
        self.record = entrypoint.read_authority_record(self.contract)
        paths = set(self.record['owners'].values()) | {
            'AGENTS.md', str(CONTRACT), 'skills/PROJECT_BASE_ADAPTER.json',
            '.agents/skills/blacksmith-workflow-router/SKILL.md',
        }
        for relative in paths:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def write_record(self):
        start = self.contract.index('<!-- current-authority -->')
        end = self.contract.index('<!-- /current-authority -->')
        (self.root / CONTRACT).write_text(
            self.contract[:start] + '<!-- current-authority -->\n```json\n' +
            json.dumps(self.record, ensure_ascii=False, indent=2) + '\n```\n' +
            self.contract[end:], encoding='utf-8')

    def test_current_owners_are_reachable(self):
        self.assertEqual([], entrypoint.validate(self.root))

    def test_missing_owner_fails_even_when_filename_remains_in_document(self):
        (self.root / self.record['owners']['production']).unlink()
        self.assertTrue(any('production' in x for x in entrypoint.validate(self.root)))

    def test_existing_history_cannot_replace_current_production_owner(self):
        self.record['owners']['production'] = self.record['owners']['history']
        self.write_record()
        self.assertTrue(entrypoint.validate(self.root))

    def test_owner_outside_repository_is_rejected(self):
        self.record['owners']['production'] = '../outside.md'
        self.write_record()
        self.assertTrue(any('outside' in x for x in entrypoint.validate(self.root)))

    def test_adoption_does_not_authorize_release_or_protected_path_change(self):
        path = self.root / 'skills/PROJECT_BASE_ADAPTER.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        data['protected_paths'].remove('assets/')
        path.write_text(json.dumps(data), encoding='utf-8')
        self.assertTrue(any('protected' in x for x in entrypoint.validate(self.root)))

    def test_observed_main_is_evidence_not_floating_execution_pin(self):
        self.record['base_observation']['commit'] = 'main'
        self.write_record()
        self.assertTrue(any('observation' in x for x in entrypoint.validate(self.root)))

    def test_removed_bootstrap_link_is_detected(self):
        path = self.root / 'AGENTS.md'
        path.write_text('# no authority route\n', encoding='utf-8')
        self.assertTrue(any('AGENTS' in x for x in entrypoint.validate(self.root)))


if __name__ == '__main__':
    unittest.main()
