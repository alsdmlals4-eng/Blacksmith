"""Protect deliverable coverage, asset references and source binding, not game PASS."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/design/BLACKSMITH_HUMAN_BLUEPRINT_20260911.md'
RECORD = ROOT / 'docs/design/candidates/blueprint-20260911/record.json'


class IntegratedHumanBlueprint(unittest.TestCase):
    def test_receipt_binds_source_and_pdf(self):
        receipt=json.loads((ROOT/'docs/operations/receipts/2026-09-10-pixel-world-blueprint.json').read_text(encoding='utf-8'))['artifact']
        self.assertEqual(receipt['source_sha256'],hashlib.sha256(SOURCE.read_bytes().replace(b'\r\n',b'\n')).hexdigest())
        self.assertEqual(receipt['sha256'],hashlib.sha256((ROOT/receipt['path']).read_bytes()).hexdigest())

    def test_trial_budget_and_probability_fixture(self):
        import math
        cost=lambda target:10*math.floor(1.2*target**1.84+0.5)
        self.assertEqual(sum(cost(t) for t in range(1,11)),3330)
        worst=sum(cost(t)*(3 if t<=2 else 5) for t in range(1,11))
        self.assertEqual(worst,16550)
        self.assertLessEqual(worst,20000)
        self.assertAlmostEqual((1-.82)*.05,.009)
        self.assertAlmostEqual(.82+(1-.82)*.05+(1-.82)*.95,1)

    def test_pdf_has_one_page_per_section(self):
        import re
        from pypdf import PdfReader
        count=len(re.findall(r'^## ',SOURCE.read_text(encoding='utf-8'),re.M))
        reader=PdfReader(ROOT/'exports/blacksmith_HUMAN_BLUEPRINT_20260911.pdf')
        self.assertEqual(len(reader.pages),count)
        for index,page in enumerate(reader.pages,1):
            self.assertIn(f'{index:02}.',page.extract_text())

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
