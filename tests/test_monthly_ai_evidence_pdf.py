"""The publisher must not overwrite submissions or silently invent evidence."""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/publish_monthly_ai_evidence_pdf.py'


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


def test_published_report_keeps_evidence_limits_and_actual_images(tmp_path):
    pytest.importorskip('reportlab', reason='PDF render evidence requires the document runtime')
    if not Path('C:/Windows/Fonts/malgun.ttf').exists():
        pytest.skip('Korean PDF render is verified on the Windows publication host')
    from pypdf import PdfReader
    target = tmp_path / 'report.pdf'
    publisher().build(target)
    reader = PdfReader(target)
    text = '\n'.join(page.extract_text() for page in reader.pages)
    for required in ['사후 정리', '작업일 미확인', '계정', '결제', '크로마키', 'AI 활용 작업일지']:
        assert required in text
    assert len(reader.pages) == 6
    assert sum(len(page.images) for page in reader.pages) == 4


def test_missing_source_is_rejected_without_publishing(tmp_path):
    with pytest.raises(FileNotFoundError):
        publisher().source_digest(tmp_path / 'missing.png')
