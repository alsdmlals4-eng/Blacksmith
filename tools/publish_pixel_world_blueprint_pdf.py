"""Derive the pixel/world-window review PDF from its sole Markdown owner."""
from pathlib import Path
import re
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/design/BLACKSMITH_PIXEL_WORLD_BLUEPRINT_20260910.md'
OUTPUT = ROOT / 'exports/blacksmith_PIXEL_WORLD_BLUEPRINT_20260910.pdf'

class Phone(Flowable):
    """Text-native layout diagram; deliberately not an illustrated game image."""
    def __init__(self, block):
        super().__init__()
        self.block = block
        self.width, self.height = 235, 310

    def draw(self):
        c = self.canv
        c.setFont('KRB',10)
        c.drawString(4,296,self.block[0].split('|')[0].strip())
        y = 278
        palette = ['#e7dfcf','#c9c0a5','#ede8dc','#d8b66f','#b9cece','#a5bdba','#d6e3df','#e7dfcf']
        for n, item in enumerate(self.block[1:]):
            label, number = re.match(r'(.+?)\s+(\d+)$',item).groups()
            height = int(number)*.4
            y -= height
            c.setFillColor(colors.HexColor(palette[n])); c.setStrokeColor(colors.white)
            c.rect(4,y,221,height,fill=1,stroke=1)
            c.setFillColor(colors.HexColor('#242c2b')); c.setFont('KR',8)
            c.drawCentredString(114,y+height/2-3,label.strip())
        c.setFont('KR',7); c.drawString(4,6,'360×640 설계 예산 / 실제 터치 검증 전')

def build():
    pdfmetrics.registerFont(TTFont('KR', 'C:/Windows/Fonts/malgun.ttf'))
    pdfmetrics.registerFont(TTFont('KRB', 'C:/Windows/Fonts/malgunbd.ttf'))
    body = ParagraphStyle('body', fontName='KR', fontSize=9, leading=14, spaceAfter=8, wordWrap='CJK')
    small = ParagraphStyle('small', parent=body, fontSize=8, leading=12, spaceAfter=2)
    heading = ParagraphStyle('heading', parent=body, fontName='KRB', fontSize=16, leading=23, spaceBefore=10, spaceAfter=14, keepWithNext=True)
    title = ParagraphStyle('title', parent=heading, fontSize=24, leading=32)
    story = []
    def p(s, style=body):
        return Paragraph(escape(s).replace('[x]', '[완료]').replace('[ ]', '[대기]'), style)
    def table(rows, widths=None):
        result = Table([[p(c, small) for c in row] for row in rows], colWidths=widths, repeatRows=1, hAlign='LEFT')
        result.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9dfcb')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f8f5ee'),colors.white]),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c5bca9')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
        return result
    lines = SOURCE.read_text(encoding='utf-8').splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == '---': story.append(PageBreak())
        elif line.startswith('# '): story.append(p(line[2:], title))
        elif line.startswith('## '): story.append(p(line[3:], heading))
        elif line.startswith('!['):
            match = re.fullmatch(r'!\[(.*?)\]\((.*?)\)',line)
            if not match: raise ValueError('Malformed image reference')
            caption, relative = match.groups()
            asset = (SOURCE.parent / relative).resolve()
            if not asset.is_relative_to(SOURCE.parent.resolve()): raise ValueError('Image outside design owner directory')
            picture = Image(str(asset))
            ratio = min(499/picture.imageWidth, 350/picture.imageHeight)
            picture.drawWidth = picture.imageWidth*ratio
            picture.drawHeight = picture.imageHeight*ratio
            story.extend([picture,Spacer(1,8),p(caption,small),Spacer(1,10)])
        elif line.startswith('```'):
            kind = line[3:]; block=[]; i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i += 1
            if kind == 'wireframe':
                first = Phone(block)
                j = i+1
                while j < len(lines) and not lines[j].strip(): j += 1
                if j < len(lines) and lines[j] == '```wireframe':
                    other=[]; j += 1
                    while j < len(lines) and lines[j] != '```':
                        other.append(lines[j]); j += 1
                    story.append(Table([[first,Phone(other)]],colWidths=[249.5,249.5]))
                    i = j
                else: story.append(first)
            else:
                story.append(table([['저장 → 관람 흐름']] + [[s] for s in block], [499]))
            story.append(Spacer(1,10))
        elif line.startswith('|'):
            rows=[]
            while i < len(lines) and lines[i].startswith('|'):
                if not re.fullmatch(r'[| :\-]+',lines[i]): rows.append([c.strip() for c in lines[i].strip('|').split('|')])
                i += 1
            story.append(table(rows,[499/len(rows[0])]*len(rows[0])))
            story.append(Spacer(1,10)); continue
        elif line: story.append(p(line))
        i += 1
    def page(canvas, doc):
        canvas.setFont('KR',8); canvas.setFillColor(colors.HexColor('#72654e'))
        canvas.drawString(48,25,'ANVIL OATH / PIXEL WORLD BLUEPRINT / 설계 보충편 · 인게임 캡처 아님')
        canvas.drawRightString(A4[0]-48,25,str(doc.page))
    SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=48,leftMargin=48,topMargin=38,bottomMargin=44,title='모루의 서약 · 픽셀 공방과 세계창',author='Blacksmith',pageCompression=1).build(story,onFirstPage=page,onLaterPages=page)
    print(OUTPUT)

if __name__ == '__main__': build()
