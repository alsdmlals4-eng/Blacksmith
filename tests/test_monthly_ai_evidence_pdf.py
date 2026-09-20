"""The publisher must preserve cumulative evidence and guard in-place refreshes."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/publish_monthly_ai_evidence_pdf.py'
SOURCE = ROOT / 'docs/operations/evidence/2026-09-ai-work-journal.json'
RECEIPT = ROOT / 'docs/operations/receipts/2026-09-14-monthly-ai-evidence.json'


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


def test_receipt_separates_historical_and_cumulative_gate_evidence():
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    historical = receipt['validation']['protected_contract']
    cumulative = receipt['validation']['cumulative_refresh_preparation'].get('protected_contract')

    assert historical.startswith('INITIAL_SEP14_HISTORICAL:')
    assert cumulative == {
        'prework': 'EXACT14_PASS',
        'end': 'FAIL_UNVERIFIED_DUE_TO_ROOT_SCOPE15_STAGING_MISMATCH',
        'scope_registration_commit': 'ebf0ceee',
        'retention': 'RETAIN_INTERMEDIATE_FAILURE_EVEN_AFTER_LATER_EXACT15_PASS',
    }


def test_historical_world5_image_paths_remain_in_cumulative_source():
    record = json.loads(SOURCE.read_text(encoding='utf-8'))
    historical_images = {
        'docs/testing/world5-bow-result-20260914.png',
        'docs/testing/world5-bow-restored-20260914.png',
        'docs/testing/world5-armor-result-fixture-20260914.png',
        'docs/testing/world5-helmet-result-fixture-20260914.png',
    }
    page_images = {
        path
        for page in record['pages']
        for path, _caption in page.get('images', [])
    }

    assert historical_images <= set(record['sources'])
    assert historical_images <= page_images


def test_three_verified_commission_cycles_and_six_captures_are_appended():
    record = json.loads(SOURCE.read_text(encoding='utf-8'))
    commission_images = {
        'docs/testing/commission-offers-native-20260916.png',
        'docs/testing/commission-transit-native-20260916.png',
        'docs/testing/commission-sale-restored-native-20260916.png',
        'docs/testing/commission-loan-chronicle-native-20260916.png',
        'docs/testing/commission-purpose-preview-native-20260916.png',
        'docs/testing/commission-purpose-result-native-20260916.png',
    }
    page_images = {
        path
        for page in record['pages']
        for path, _caption in page.get('images', [])
    }
    text = json.dumps(record, ensure_ascii=False)

    assert 'docs/operations/receipts/2026-09-16-general-commissions.json' in record['sources']
    assert commission_images <= set(record['sources'])
    assert commission_images <= page_images
    assert '세 번의 제한된 desktop 의뢰 순환' in text
    assert 'BSI-743d42640b103aebcb6747b615915999' in text
    assert 'BSI-7174f11179a8006541685c300c20b541' in text
    assert '5→4' in text
    assert '11 SUCCESS/1 conditional SKIP' in text


def test_monthly_receipt_records_published_final_candidate_binding():
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    preparation = receipt['append_update_history'][-1]
    candidate = preparation['candidate']
    source_text = SOURCE.read_bytes().decode('utf-8')
    normalized_source = source_text.replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')

    assert preparation['state'] == 'CUMULATIVE_PRE_SUBMISSION_REVIEW_COPY_MODAK_PARTIAL'
    assert candidate['pages'] == 13
    assert candidate['native_images'] == 13
    assert candidate['source_hash_definition'] == 'UTF8_TEXT_LF_NORMALIZED_SHA256'
    assert candidate['source_sha256'] == hashlib.sha256(normalized_source).hexdigest()
    historical = receipt['append_update_history'][-2]
    assert historical['candidate']['source_generation_raw_hash_definition'] == 'ORIGINAL_WINDOWS_INPUT_BYTES_SHA256'
    assert historical['candidate']['source_generation_raw_sha256'] == (
        'a2c9f00c6383a50c5bb5819d686e3ca968e881c3e6701d7e7abe2a26ddbe84ec'
    )
    assert historical['replaced_output']['sha256'] == (
        'a4e7aad5e6c3c3cd8085de8bc9d8de2b48ca39fc38782edc8618c60824f314c8'
    )
    assert preparation['current_output_readback']['sha256'] == candidate['sha256']
    assert preparation['replaced_output']['sha256'] == historical['candidate']['sha256']


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


def test_source_text_digest_is_stable_across_lf_and_crlf(tmp_path):
    lf_source = tmp_path / 'lf.json'
    crlf_source = tmp_path / 'crlf.json'
    lf_source.write_bytes(b'{"line": 1}\n{"line": 2}\n')
    crlf_source.write_bytes(b'{"line": 1}\r\n{"line": 2}\r\n')
    expected = 'ecd93c40eb0593978eee0166474432b677a2a925b36f981f43dadd2806e117e7'

    assert publisher().source_text_digest(lf_source) == expected
    assert publisher().source_text_digest(crlf_source) == expected


def test_missing_source_is_rejected_without_publishing(tmp_path):
    with pytest.raises(FileNotFoundError):
        publisher().source_digest(tmp_path / 'missing.png')
