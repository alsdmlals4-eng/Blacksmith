"""Bounded review-artifact checks; never runtime or visual approval."""
import json
import hashlib
import unittest
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]

class PixelBlueprintArtifact(unittest.TestCase):
    def test_candidate_appendix_present(self):
        reader = PdfReader(ROOT / 'exports/blacksmith_PIXEL_WORLD_BLUEPRINT_20260910.pdf')
        text = '\n'.join(page.extract_text() for page in reader.pages)
        self.assertIn('10. 첫 픽셀 후보', text)
        self.assertIn('원본 픽셀 보존', text)
        self.assertGreaterEqual(sum(len(page.images) for page in reader.pages), 3)

    def test_candidate_boundaries_and_hashes(self):
        record = json.loads((ROOT / 'docs/design/candidates/pixel-first-20260910/record.json').read_text(encoding='utf-8'))
        self.assertEqual(record['runtime_status'], 'NOT_RUN')
        self.assertEqual(record['user_approval'], 'PENDING')
        for item in record['files']:
            file = ROOT / 'docs/design/candidates/pixel-first-20260910' / item['name']
            content = file.read_bytes()
            if item.get('hash_basis') == 'UTF8_CRLF_TO_LF':
                content = content.replace(b'\r\n', b'\n')
            self.assertEqual(hashlib.sha256(content).hexdigest(),item['sha256'])

if __name__ == '__main__': unittest.main()
