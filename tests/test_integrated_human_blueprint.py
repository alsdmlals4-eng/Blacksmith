"""Protect deliverable coverage, asset references and source binding, not game PASS."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/design/BLACKSMITH_HUMAN_BLUEPRINT_20260911.md'
RECORD = ROOT / 'docs/design/candidates/blueprint-20260911/record.json'
RECEIPT = ROOT / 'docs/operations/receipts/2026-09-10-pixel-world-blueprint.json'
PUBLISHER = ROOT / 'tools/publish_integrated_human_blueprint_pdf.py'


class IntegratedHumanBlueprint(unittest.TestCase):
    def test_exchange_checkpoint_shows_reinvestment_and_evidence_limits(self):
        content = SOURCE.read_text(encoding='utf-8')
        for text in ['## 63.', '## 64.', '15470', 'CATALYST_EXCHANGE_TRIAL_V1',
                     'catalyst-exchange-confirm-20260913.png',
                     'catalyst-exchange-restored-20260913.png']:
            self.assertIn(text, content)

    def test_manual_day_checkpoint_shows_repeat_play_and_remaining_limits(self):
        content = SOURCE.read_text(encoding='utf-8')
        for text in ['## 61.', '## 62.', '17470', 'recovery-day-confirm-20260913.png',
                     'recovery-day-repeat-delivered-20260913.png', 'MANUAL_CLOSE_V1']:
            self.assertIn(text, content)

    def test_recovery_checkpoint_preserves_prior_atlas_and_shows_real_delivery(self):
        content = SOURCE.read_text(encoding='utf-8')
        self.assertIn('## 59.', content)
        self.assertIn('17070', content)
        for capture in ['recovery-order-forged-20260913.png', 'recovery-order-delivered-20260913.png']:
            self.assertIn(capture, content)
            self.assertTrue((ROOT/'docs/testing'/capture).is_file())
        receipt=json.loads((ROOT/'docs/operations/receipts/2026-09-10-pixel-world-blueprint.json').read_text(encoding='utf-8'))
        self.assertEqual(receipt['recovery_delivery']['decision'], 'BS-REPLAN-20260913-04')

    def test_current_runtime_checkpoint_is_distinct_from_design_candidates(self):
        content = SOURCE.read_text(encoding='utf-8')
        for section in ['## 52.', '## 53.', '## 54.', '## 55.', '## 56.']:
            self.assertIn(section, content)
        for capture in ['replan-aqueduct-detailed-report-20260913.png', 'replan-aqueduct-readable-chronicle-20260913.png']:
            self.assertIn(capture, content)
            self.assertTrue((ROOT/'docs/testing'/capture).is_file())
        self.assertIn('Android / 사람 플레이', content)
        self.assertIn('replan-from-zero-correct-risk-20260913.png', content)
        self.assertIn('replan-world-report-split-20260913.png', content)

    def test_atlas_contains_state_comparisons_not_repeated_backdrops(self):
        content = SOURCE.read_text(encoding='utf-8')
        self.assertEqual(content.count('```stateatlas'), 5)
        for section in ['## 46.', '## 47.', '## 48.', '## 49.', '## 50.', '## 51.']:
            self.assertIn(section, content, section)
        self.assertIn('4/4/5', content)
        self.assertIn('WORLD_EXPANDED', content)
        import re
        states = [row.split('|') for block in re.findall(r'```stateatlas\n(.*?)\n```', content, re.S) for row in block.splitlines()]
        self.assertEqual(len(states), 15)
        for state in states:
            self.assertEqual(len(state), 9)
            current, maximum, base = map(int, state[3].split('/'))
            self.assertTrue(0 <= current <= maximum <= base)
        repair = next(state for state in states if state[0] == '수리 전')
        result = next(state for state in states if state[0] == '수리 후 / 흉터 예')
        self.assertGreater(int(result[3].split('/')[0]), int(repair[3].split('/')[0]))

    def test_approved_character_growth_is_in_human_reader(self):
        content = SOURCE.read_text(encoding='utf-8')
        for expected in ['## 42.', '## 43.', '## 44.', '## 45.',
                         'modak-human-02-younger.png', 'modak-human-01.png',
                         'smith-01.png', '3년 차', '게임 1년의 길이']:
            self.assertIn(expected, content, expected)

    def test_receipt_binds_source_and_pdf(self):
        receipt=json.loads(RECEIPT.read_text(encoding='utf-8'))
        artifact=receipt['artifact']
        preparation=receipt['modak_cumulative_preparation']
        self.assertEqual(artifact['sha256'],hashlib.sha256((ROOT/artifact['path']).read_bytes()).hexdigest())
        self.assertEqual(artifact['page_count'],79)
        self.assertEqual(
            artifact['source_sha256'],
            hashlib.sha256(SOURCE.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        )
        self.assertEqual(
            preparation['source_sha256_normalized_lf'],
            hashlib.sha256(SOURCE.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        )
        self.assertEqual(preparation['candidate_sha256'],artifact['sha256'])
        self.assertEqual(preparation['replaced_artifact']['page_count'],77)
        self.assertEqual(
            preparation['replaced_artifact']['sha256'],
            'e89f1721e9ec0057b4db69b66d52cc369d904891ea6bbfbca5ad1e223f616877',
        )
        self.assertEqual(preparation['publication_status'],'PUBLISHED_REVIEW_COPY_M1_M3_PARTIAL_M4_PENDING')
        self.assertEqual(receipt['commission_cumulative_preparation']['candidate_pages'],77)
        self.assertEqual(receipt['commission_cumulative_preparation']['replaced_artifact']['page_count'],74)

    def test_trial_budget_and_probability_fixture(self):
        import math
        cost=lambda target:10*math.floor(1.2*target**1.84+0.5)
        self.assertEqual(sum(cost(t) for t in range(1,11)),3330)
        worst=sum(cost(t)*(3 if t<=2 else 5) for t in range(1,11))
        self.assertEqual(worst,16550)
        self.assertLessEqual(worst,20000)
        self.assertAlmostEqual((1-.82)*.05,.009)
        self.assertAlmostEqual(.82+(1-.82)*.05+(1-.82)*.95,1)

    def test_pdf_candidate_has_one_page_per_section(self):
        import importlib.util
        import re
        import tempfile
        try:
            import reportlab  # noqa: F401
        except ImportError:
            self.skipTest('candidate build requires ReportLab')
        if not Path('C:/Windows/Fonts/malgun.ttf').exists():
            self.skipTest('candidate build is verified on the Windows publication host')
        from pypdf import PdfReader
        count=len(re.findall(r'^## ',SOURCE.read_text(encoding='utf-8'),re.M))
        spec=importlib.util.spec_from_file_location('integrated_blueprint_publisher',PUBLISHER)
        publisher=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(publisher)
        with tempfile.TemporaryDirectory() as directory:
            candidate=Path(directory)/'blueprint-candidate.pdf'
            publisher.build(candidate)
            reader=PdfReader(candidate)
            self.assertEqual(len(reader.pages),count)
            for index,page in enumerate(reader.pages,1):
                self.assertIn(f'{index:02}.',page.extract_text())

    def test_published_pdf_has_one_page_per_section(self):
        import re
        from pypdf import PdfReader
        count=len(re.findall(r'^## ',SOURCE.read_text(encoding='utf-8'),re.M))
        reader=PdfReader(ROOT/'exports/blacksmith_HUMAN_BLUEPRINT_20260911.pdf')
        self.assertEqual(len(reader.pages),count)
        for index,page in enumerate(reader.pages,1):
            self.assertIn(f'{index:02}.',page.extract_text())

    def test_commission_runtime_append_preserves_74_sections_and_adds_three_pairs(self):
        import re
        content=SOURCE.read_text(encoding='utf-8')
        headings=re.findall(r'^## (\d+)\.',content,re.M)
        self.assertEqual(headings[:74],[f'{number:02}' for number in range(1,75)])
        self.assertEqual(headings[74:77],['75','76','77'])
        captures=[
            'commission-offers-native-20260916.png',
            'commission-transit-native-20260916.png',
            'commission-sale-restored-native-20260916.png',
            'commission-loan-chronicle-native-20260916.png',
            'commission-purpose-preview-native-20260916.png',
            'commission-purpose-result-native-20260916.png',
        ]
        appended=content[content.index('## 75.'):content.index('## 78.')]
        self.assertEqual(appended.count('```runtimecaptures'),3)
        for capture in captures:
            self.assertEqual(appended.count(capture),1)
            self.assertTrue((ROOT/'docs/testing'/capture).is_file())
        for required in [
            '세 번의 제한된 desktop 의뢰 순환',
            'BSI-743d42640b103aebcb6747b615915999',
            'BSI-7174f11179a8006541685c300c20b541',
            '5→4',
            'Android',
            '사람 밸런스',
            'remote CI11 SUCCESS/1 conditional SKIP',
        ]:
            self.assertIn(required,appended)

    def test_deliverable_covers_requested_sections(self):
        self.assertTrue(SOURCE.is_file(), 'Integrated blueprint not yet authored')
        content = SOURCE.read_text(encoding='utf-8')
        for section in ['화면 아틀라스', 'SWOT', '시스템', '데이터', '모션', '구현', '검수', '출처']:
            self.assertIn(section, content)

    def test_candidate_assets_are_bound_to_actual_files(self):
        self.assertTrue(RECORD.is_file(), 'Candidate manifest missing')
        record = json.loads(RECORD.read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(record['assets']), 5)
        for asset in record['assets']:
            path = ROOT / asset['path']
            self.assertTrue(path.is_file(), asset['path'])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), asset['sha256'])
            self.assertTrue(asset['consumer'])
            self.assertNotEqual(asset['status'], 'RUNTIME_VERIFIED')


if __name__ == '__main__':
    unittest.main()
