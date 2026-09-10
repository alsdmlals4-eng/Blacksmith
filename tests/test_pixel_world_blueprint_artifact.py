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

    def test_refined_candidate_files_and_png_dimensions(self):
        import struct
        folder = ROOT / 'docs/design/candidates/pixel-stylish-20260910'
        self.assertTrue((folder / 'record.json').is_file(), 'Refined candidate provenance missing')
        record = json.loads((folder / 'record.json').read_text(encoding='utf-8'))
        self.assertEqual(record['user_approval'], 'PENDING')
        self.assertEqual(record['runtime_status'], 'NOT_RUN')
        sheet = json.loads((folder / 'actor-sheet.json').read_text(encoding='utf-8'))
        atlas = folder / sheet['meta']['image']
        self.assertTrue(atlas.is_file(), 'Atlas JSON references a missing PNG')
        self.assertEqual(list(struct.unpack('>II', atlas.read_bytes()[16:24])),
                         [sheet['meta']['size']['w'], sheet['meta']['size']['h']])
        for item in record['files']:
            content = (folder / item['name']).read_bytes()
            if item.get('hash_basis') == 'UTF8_CRLF_TO_LF':
                content = content.replace(b'\r\n', b'\n')
            self.assertEqual(hashlib.sha256(content).hexdigest(), item['sha256'])
            if 'dimensions' in item:
                self.assertEqual(list(struct.unpack('>II', content[16:24])), item['dimensions'])

if __name__ == '__main__': unittest.main()
