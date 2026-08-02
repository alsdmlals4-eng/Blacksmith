from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BaseV94BlacksmithAdoptionTests(unittest.TestCase):
    def test_identity_routes_and_project_skills(self) -> None:
        adapter = json.loads((ROOT / 'skills/PROJECT_BASE_ADAPTER.json').read_text(encoding='utf-8'))
        snapshot = json.loads((ROOT / 'skills/PROJECT_SKILL_SNAPSHOT.json').read_text(encoding='utf-8'))
        self.assertEqual('9.4.0', adapter['base_release']['version'])
        self.assertEqual('3f2c4a624d302b704c1b5322eb5c9f34ad55abb9', adapter['base_release']['release_commit'])
        self.assertEqual('ff117d24d5bdb121314e109a6aa9b4f552e0fdc1', adapter['base_release']['release_evidence_commit'])
        self.assertEqual('693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59', adapter['skill_registry']['base']['sha256'])
        self.assertIn('optimizing-ai-model-and-prompt-costs', {item['route_id'] for item in adapter['routing']['base_routes']})
        self.assertEqual({'blacksmith-engineering', 'blacksmith-game-design', 'blacksmith-qa'}, {item['route_id'] for item in adapter['routing']['project_routes']})
        self.assertEqual('BASE_SHARED', snapshot['effective_routes']['optimizing-ai-model-and-prompt-costs']['source'])
        self.assertEqual(['data/', 'scripts/', 'scenes/', 'assets/', 'addons/', 'project.godot'], adapter['protected_paths'])

    def test_generated_views_bind_to_adapter(self) -> None:
        sha = hashlib.sha256((ROOT / 'skills/PROJECT_BASE_ADAPTER.json').read_bytes()).hexdigest()
        snapshot = json.loads((ROOT / 'skills/PROJECT_SKILL_SNAPSHOT.json').read_text(encoding='utf-8'))
        self.assertEqual(sha, snapshot['source_registry']['sha256'])
        for file in ('skills/BASE_V9_ADAPTER.json', 'skills/PROJECT_BASE_SKILL_ADAPTER.json'):
            view = json.loads((ROOT / file).read_text(encoding='utf-8'))
            self.assertEqual(sha, view['canonical_source_sha256'])
            self.assertEqual('9.4.0', view['base_release']['version'])

    def test_ai_ui_and_evidence_limits(self) -> None:
        ai = (ROOT / '[기획서]/00_프로젝트_허브/AI_WORKFLOW.md').read_text(encoding='utf-8')
        ux = (ROOT / 'docs/UX_UI_SYSTEM.md').read_text(encoding='utf-8')
        audit = (ROOT / 'docs/reviews/2026-08-01_BASE_V9_4_ADOPTION_AUDIT.md').read_text(encoding='utf-8')
        for token in ('[모델 추천]', 'HARD_CONSTRAINT', 'Interface-first', 'Example-as-Fixture', 'refresh_trigger', 'NOT_RUN'):
            self.assertIn(token, ai)
        for token in ('입력 접수', '처리 중', '중단', '즉시 완료', '재진입', 'Reduced Motion', 'mute', 'haptic-off', '권위 시점'):
            self.assertIn(token, ux)
        self.assertIn('product_paths_changed: false', audit)
        self.assertIn('HUMAN_NOT_RUN', audit)


if __name__ == '__main__':
    unittest.main()
