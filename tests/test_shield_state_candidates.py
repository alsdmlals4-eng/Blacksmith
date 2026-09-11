"""Candidate provenance, not asset approval or runtime verification."""
import hashlib
import json
from pathlib import Path
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'docs/design/candidates/shield-states-20260912/record.json'


class ShieldStateCandidates(unittest.TestCase):
    def test_candidate_is_source_bound_and_not_promoted(self):
        record = json.loads(RECORD.read_text(encoding='utf-8'))
        image = ROOT / record['path']
        self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), record['sha256'])
        self.assertEqual(len(record['states']), 6)
        self.assertEqual(record['consumer_id'], 'BP12-SHIELD-STATES')
        self.assertFalse(record['user_approved'])
        self.assertFalse(record['runtime_promoted'])
        self.assertTrue(record['prompt'])
        self.assertIn('alpha_verified', record)
        with Image.open(image) as sprite:
            self.assertEqual(sprite.mode, record['mode'])
            self.assertEqual(list(sprite.size), record['size'])
            has_transparency = 'A' in sprite.getbands() and sprite.getchannel('A').getextrema()[0] < 255
            self.assertEqual(has_transparency, record['alpha_verified'])
        self.assertTrue(record['inspection']['failures'])


if __name__ == '__main__':
    unittest.main()
