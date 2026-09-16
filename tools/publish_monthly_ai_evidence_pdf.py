"""Publish a source-bound cumulative report with guarded current-copy refresh."""
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import hmac
from html import escape
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/operations/evidence/2026-09-ai-work-journal.json'


def source_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fit_dimensions(width, height, max_width, max_height):
    if min(width, height, max_width, max_height) <= 0:
        raise ValueError('Image dimensions must be positive')
    scale = min(1.0, max_width / width, max_height / height)
    return width * scale, height * scale


def source_reference(record):
    repository = record['repository']
    commits = ', '.join(commit[:8] for commit in record['commits'])
    pull_requests = ', '.join(f'PR{number}' for number in repository['pull_requests'])
    return f"Git 원본: {repository['url']} / commits {commits}. 관련 {pull_requests}."


def replace_current(output, candidate, expected_old_sha256):
    """Atomically replace one known review copy after exact hash verification."""
    output = Path(output)
    candidate = Path(candidate)
    expected = expected_old_sha256.strip().lower()
    if len(expected) != 64 or any(character not in '0123456789abcdef' for character in expected):
        raise ValueError('Expected old SHA-256 must be 64 hexadecimal characters')
    if not output.is_file():
        raise FileNotFoundError(f'Current review copy not found: {output}')
    old_digest = source_digest(output)
    if not hmac.compare_digest(old_digest, expected):
        raise ValueError(
            f'Current review copy does not match expected old SHA-256: {old_digest}'
        )
    candidate_bytes = candidate.read_bytes()
    if not candidate_bytes.startswith(b'%PDF-'):
        raise ValueError(f'Candidate is not a PDF: {candidate}')

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode='xb',
            dir=output.parent,
            prefix=f'.{output.name}.',
            suffix='.refresh.tmp',
            delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
            stream.write(candidate_bytes)
            stream.flush()
            os.fsync(stream.fileno())
        if not hmac.compare_digest(source_digest(output), expected):
            raise RuntimeError('Current review copy changed during guarded refresh')
        os.replace(temporary_path, output)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return source_digest(output)


def build(output):
    output = Path(output)
    if output.exists():
        raise FileExistsError(f'Preserve issued report; choose a new version: {output}')
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
    record = json.loads(SOURCE.read_text(encoding='utf-8'))
    hashes = [(path, source_digest(ROOT / path)) for path in record['sources']]
    for commit in record['commits']:
        subprocess.run(['git', 'cat-file', '-e', commit + '^{commit}'], cwd=ROOT, check=True, capture_output=True)
    pdfmetrics.registerFont(TTFont('JournalKR', 'C:/Windows/Fonts/malgun.ttf'))
    pdfmetrics.registerFont(TTFont('JournalBold', 'C:/Windows/Fonts/malgunbd.ttf'))
    body = ParagraphStyle('journal', fontName='JournalKR', fontSize=9.4, leading=15, spaceAfter=10, wordWrap='CJK')
    small = ParagraphStyle('small', parent=body, fontSize=7.2, leading=10, spaceAfter=5)
    title = ParagraphStyle('title', parent=body, fontName='JournalBold', fontSize=21, leading=28, spaceAfter=15, textColor=colors.HexColor('#213b44'))
    heading = ParagraphStyle('heading', parent=title, fontSize=16, leading=23)
    def p(value, style=body):
        return Paragraph(escape(value), style)
    issued = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec='seconds')
    story = []
    for number, page in enumerate(record['pages']):
        if number:
            story.append(PageBreak())
        else:
            story.extend([p(record['title'], title), p(record['edition']), p(record['scope'])])
        story.append(p(page['heading'], heading))
        for paragraph in page['paragraphs']:
            story.append(p(paragraph))
        if page.get('images'):
            cells, labels = [], []
            for path, caption in page['images']:
                source_digest(ROOT / path)
                report_image = Image(str(ROOT / path))
                column_width = 480 / len(page['images'])
                width, height = fit_dimensions(
                    report_image.imageWidth,
                    report_image.imageHeight,
                    min(151.875, column_width - 8),
                    270,
                )
                report_image.drawWidth = width
                report_image.drawHeight = height
                cells.append(report_image)
                labels.append(p(caption, small))
            table = Table(
                [cells, labels],
                colWidths=[480 / len(cells)] * len(cells),
            )
            table.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'), ('VALIGN',(0,0),(-1,-1),'TOP')]))
            story.extend([Spacer(1, 5), table])
        if page.get('footer'):
            story.append(p(page['footer'], small))
        if page.get('source_index'):
            for path, digest in hashes:
                story.append(p(f'{path} | SHA-256 {digest[:16]}', small))
            story.append(p(source_reference(record), small))
            story.append(p(f'이 보고서 입력 JSON SHA-256: {source_digest(SOURCE)}', small))
    def decoration(canvas, doc):
        canvas.setStrokeColor(colors.HexColor('#bac6c9'))
        canvas.line(42, 39, A4[0]-42, 39)
        canvas.setFont('JournalKR', 7)
        canvas.drawString(42, 27, f'기록 작성 {record["recorded_on"]} | PDF 발행 {issued} | 제출 전 검토본')
        canvas.drawRightString(A4[0]-42, 27, str(doc.page))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=38, bottomMargin=52, title=record['title'], author='Blacksmith / AI-assisted working record')
    doc.build(story, onFirstPage=decoration, onLaterPages=decoration)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('xb') as stream:
        stream.write(buffer.getvalue())
    return source_digest(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument('--output', type=Path)
    operation.add_argument('--replace-current', type=Path)
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--expected-old-sha256')
    args = parser.parse_args()
    if args.output is not None:
        if args.candidate is not None or args.expected_old_sha256 is not None:
            parser.error('--candidate and --expected-old-sha256 require --replace-current')
        print(build(args.output))
    else:
        if args.candidate is None or args.expected_old_sha256 is None:
            parser.error('--replace-current requires --candidate and --expected-old-sha256')
        print(replace_current(args.replace_current, args.candidate, args.expected_old_sha256))
