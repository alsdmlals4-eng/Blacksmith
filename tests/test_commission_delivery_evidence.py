"""Bounded native evidence, never a whole-game or human acceptance claim."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_commission_native_receipt_preserves_three_cycles_and_six_real_captures():
    receipt = json.loads((ROOT / 'docs/operations/receipts/2026-09-16-general-commissions.json').read_text(encoding='utf-8'))
    assert len(receipt['native']['cycles']) == 3
    assert len(receipt['native']['captures']) == 6
    for capture in receipt['native']['captures']:
        assert hashlib.sha256((ROOT / capture['path']).read_bytes()).hexdigest() == capture['sha256']
    assert receipt['native']['default_player_save_modified'] is False
    assert 'Human balance' in receipt['not_verified']
    assert 'Release' in receipt['not_verified']
    assert receipt['verification_at_source_revision']['debug_mode_ci_reproduction'] == 'RED_8_OF_9_THEN_GREEN_9_OF_9_FULL_369_OF_369'
    assert receipt['verification_at_source_revision']['native_resume_review'] == 'APPROVED_NO_FINDINGS_PURPOSE_HELPER_CONFIRMED'


def test_closeout_does_not_start_next_feature_and_journal_is_cumulative():
    production = (ROOT / 'docs/design/BLACKSMITH_HUMAN_BLUEPRINT_PRODUCTION_20260911.md').read_text(encoding='utf-8')
    assert 'CURRENT_BUNDLE_CLOSEOUT_NO_R05_START' in production
    assert 'same existing monthly PDF' in production
