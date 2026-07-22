from __future__ import annotations
import base64, gzip, hashlib, subprocess, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CHUNK_DIR = ROOT / 'tools' / 'fever_patch_chunks'
encoded = ''.join((CHUNK_DIR / f'chunk_{index}.txt').read_text(encoding='utf-8').strip() for index in range(4))
expected = '857a9712e555eda288fc088899008104451d60fa895c80ecdfecc1ca50cfcef1'
if hashlib.sha256(encoded.encode()).hexdigest() != expected:
    raise RuntimeError('fever patch chunk integrity check failed')
legacy_uid = ROOT / 'tests/integration/test_forging_quality_enhancement.gd.uid'
if not legacy_uid.exists():
    legacy_uid.write_text('uid://baopfdqvupgau\n', encoding='utf-8')
with tempfile.NamedTemporaryFile(suffix='.patch', delete=False) as handle:
    handle.write(gzip.decompress(base64.b64decode(encoded)))
    patch_path = handle.name
subprocess.run(['patch', '-p1', '--forward', '--input', patch_path], cwd=ROOT, check=True)
print('Fever game patch applied')
