"""The publisher must preserve cumulative evidence and guard in-place refreshes."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/publish_monthly_ai_evidence_pdf.py'
SOURCE = ROOT / 'docs/operations/evidence/2026-09-ai-work-journal.json'


def publisher():
    assert SCRIPT.exists(), 'Monthly evidence publisher is not implemented'
    spec = importlib.util.spec_from_file_location('monthly_evidence', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_existing_submission_is_never_overwritten(tmp_path):
    target = tmp_path / 'issued.pdf'
    target.write_bytes(b'original submission')
    with pytest.raises(FileExistsError):
        publisher().build(target)
    assert target.read_bytes() == b'original submission'


def test_published_report_is_cumulative_and_uses_record_references(tmp_path):
    pytest.importorskip('reportlab', reason='PDF render evidence requires the document runtime')
    if not Path('C:/Windows/Fonts/malgun.ttf').exists():
        pytest.skip('Korean PDF render is verified on the Windows publication host')
    from pypdf import PdfReader
    target = tmp_path / 'report.pdf'
    publisher().build(target)
    reader = PdfReader(target)
    text = '\n'.join(page.extract_text() for page in reader.pages)
    record = json.loads(SOURCE.read_text(encoding='utf-8'))
    for required in [
        '활: 실제 제작부터 저장된 세계 결과',
        '사후 정리',
        '작업일 미확인',
        '계정',
        '결제',
        '크로마키',
        'AI 활용 작업일지',
        '2026-09-14',
        '2026-09-16',
        'PR384',
        'cfacad55',
    ]:
        assert required in text
    assert len(record['pages']) > 6
    assert len(reader.pages) >= len(record['pages'])
    assert sum(len(page.images) for page in reader.pages) >= 4


def test_explicit_expected_hash_replaces_current_review_copy(tmp_path):
    target = tmp_path / 'current.pdf'
    candidate = tmp_path / 'candidate.pdf'
    original = b'%PDF-1.4\nold review copy\n'
    replacement = b'%PDF-1.4\ninspected cumulative candidate\n'
    target.write_bytes(original)
    candidate.write_bytes(replacement)

    result = publisher().replace_current(
        target,
        candidate,
        hashlib.sha256(original).hexdigest(),
    )

    assert target.read_bytes() == replacement
    assert candidate.read_bytes() == replacement
    assert result == hashlib.sha256(replacement).hexdigest()


def test_refresh_failure_preserves_current_review_copy(tmp_path):
    target = tmp_path / 'current.pdf'
    candidate = tmp_path / 'candidate.pdf'
    original = b'%PDF-1.4\nold review copy\n'
    target.write_bytes(original)
    candidate.write_bytes(b'%PDF-1.4\nnew candidate\n')

    with pytest.raises(ValueError, match='expected old SHA-256'):
        publisher().replace_current(target, candidate, '0' * 64)

    assert target.read_bytes() == original


def test_image_dimensions_preserve_aspect_ratio():
    width, height = publisher().fit_dimensions(360, 640, 151.875, 270)
    assert width / height == pytest.approx(360 / 640)
    assert width <= 151.875
    assert height <= 270


def test_missing_source_is_rejected_without_publishing(tmp_path):
    with pytest.raises(FileNotFoundError):
        publisher().source_digest(tmp_path / 'missing.png')
