"""Preparation evidence only: never infer product completion from document coverage."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'docs/design/BLACKSMITH_REMAINING_IMPLEMENTATION_SPEC_20260914.md'


class RemainingImplementationSpec(unittest.TestCase):
    def test_reviewed_transaction_and_layout_invariants_are_explicit(self):
        source = SPEC.read_text(encoding='utf-8')
        for token in ['COMMIT_UNCERTAIN', 'funding_origin=COMMISSION_ESCROW',
                      'IN_TRANSIT', '독립 mission/damage 두 draw',
                      '추가소비0', '세계 위/공방 아래', 'produced_item_uid는 제작 전 null']:
            self.assertIn(token, source, token)

    def test_each_work_package_has_an_executable_contract(self):
        self.assertTrue(SPEC.is_file())
        source = SPEC.read_text(encoding='utf-8')
        for number in range(1, 13):
            section = source.split(f'## R{number:02} — ', 1)[1].split('\n## ', 1)[0]
            for field in ['현재 상태', '선행 조건', '설계·흐름', '데이터·구현', '실패·복구', '완료 증거', '제외']:
                self.assertIn(field, section, f'R{number:02}: {field}')

    def test_preparation_preserves_evidence_and_policy_boundaries(self):
        source = SPEC.read_text(encoding='utf-8')
        for token in ['f30baaa60e1fb95905c47d5a8303cd069895ce96',
                      'd73e391e7f81c3f0e349d92505cdeb80fe7063a9',
                      'RECOMMENDED_NOT_LOCKED', 'NOT_RUN', 'PR381',
                      '30 / 64 / 64', '60 / 5 / 5', '48dp',
                      'ADOPT', 'ADAPT', 'REJECT', '120', '240',
                      'MAIN_VERIFIED', 'BRANCH_MACHINE_VERIFIED']:
            self.assertIn(token, source)

    def test_human_blueprint_carries_the_remaining_work_checklist(self):
        source = (ROOT/'docs/design/BLACKSMITH_HUMAN_BLUEPRINT_20260911.md').read_text(encoding='utf-8')
        for number in range(65, 73):
            self.assertIn(f'## {number}.', source)
        for number in range(1, 13):
            self.assertIn(f'R{number:02}', source)


if __name__ == '__main__':
    unittest.main()
