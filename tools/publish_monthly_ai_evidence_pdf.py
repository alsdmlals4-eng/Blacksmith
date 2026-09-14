"""Publish a source-bound monthly report without overwriting issued copies."""
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
from html import escape
import io
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/operations/evidence/2026-09-ai-work-journal.json'


def source_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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
                cells.append(Image(str(ROOT / path), width=151.875, height=270))
                labels.append(p(caption, small))
            table = Table([cells, labels], colWidths=[240, 240])
            table.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'), ('VALIGN',(0,0),(-1,-1),'TOP')]))
            story.extend([Spacer(1, 5), table])
        if page.get('footer'):
            story.append(p(page['footer'], small))
        if page.get('source_index'):
            for path, digest in hashes:
                story.append(p(f'{path} | SHA-256 {digest[:16]}', small))
            story.append(p('Git 원본: https://github.com/alsdmlals4-eng/Blacksmith / commits 3d4c1c37, d7f337a9, 30e1a874. 관련 PR381 및 명세 PR383.', small))
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
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(build(args.output))
