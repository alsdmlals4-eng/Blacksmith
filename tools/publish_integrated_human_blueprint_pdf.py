"""Project-owned human reading view; illustrations remain referenced candidate PNGs."""
from pathlib import Path
import re
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from publish_pixel_world_blueprint_pdf import Phone

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/design/BLACKSMITH_HUMAN_BLUEPRINT_20260911.md'
OUTPUT=ROOT/'exports/blacksmith_HUMAN_BLUEPRINT_20260911.pdf'
ASSETS=SOURCE.parent/'candidates/blueprint-20260911'
W,H=landscape(A4)

class AtlasCard(Flowable):
    """Editable layout diagram using actual proposed backdrop, not a runtime claim."""
    def __init__(self, title, detail, number):
        Flowable.__init__(self); self.width=240; self.height=106
        self.title,self.detail,self.number=title,detail,number
    def draw(self):
        c=self.canv;c.setFillColor(colors.HexColor('#172d32'));c.rect(0,0,240,101,fill=1,stroke=0)
        bg=ASSETS/('adventure.png' if self.number in (5,6) else 'forge.png')
        c.drawImage(str(bg),3,28,111,70,mask='auto',preserveAspectRatio=True,anchor='c')
        c.setFillColor(colors.HexColor('#eee7d8'));c.rect(120,30,114,65,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#20333a'));c.setFont('KRB',8)
        for i,s in enumerate(self.detail.split(' / ')): c.drawString(125,80-i*15,s)
        c.setFillColor(colors.HexColor('#f4e5bf'));c.setFont('KRB',10);c.drawString(7,10,f'{self.number+1:02}  {self.title}')

def build():
    pdfmetrics.registerFont(TTFont('KR','C:/Windows/Fonts/malgun.ttf'))
    pdfmetrics.registerFont(TTFont('KRB','C:/Windows/Fonts/malgunbd.ttf'))
    body=ParagraphStyle('body',fontName='KR',fontSize=10,leading=15,spaceAfter=9,wordWrap='CJK')
    small=ParagraphStyle('small',parent=body,fontSize=9,leading=13,spaceAfter=0)
    heading=ParagraphStyle('heading',parent=body,fontName='KRB',fontSize=22,leading=28,spaceAfter=17,keepWithNext=True)
    def p(s,style=body): return Paragraph(escape(s),style)
    def table(rows):
        th=ParagraphStyle('th',parent=small,textColor=colors.white,fontName='KRB')
        t=Table([[p(c,th if index==0 else small) for c in row] for index,row in enumerate(rows)],colWidths=[(W-80)/len(rows[0])]*len(rows[0]),repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#20383c')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#e8e4d9'),colors.HexColor('#f7f4eb')]),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#b9b5a6')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
        return t
    lines=SOURCE.read_text(encoding='utf-8').splitlines();story=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if line=='---': story.append(PageBreak())
        elif line.startswith('# '): pass
        elif line.startswith('## '): story.append(p(line[3:],heading))
        elif i<3: pass
        elif line.startswith('!['):
            caption,rel=re.fullmatch(r'!\[(.*?)\]\((.*?)\)',line).groups()
            path=(SOURCE.parent/rel).resolve()
            if not path.is_relative_to(SOURCE.parent.resolve()): raise ValueError('Image path escapes owner')
            img=Image(str(path)); lim=250 if 'items.png' in rel else 175
            scale=min((W-80)/img.imageWidth,lim/img.imageHeight)
            img.drawWidth=img.imageWidth*scale;img.drawHeight=img.imageHeight*scale
            story.extend([img,Spacer(1,5),p(caption,small),Spacer(1,10)])
        elif line.startswith('```'):
            kind=line[3:];block=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'): block.append(lines[i]);i+=1
            if kind=='atlas':
                cards=[AtlasCard(*s.split('|'),n) for n,s in enumerate(block)]
                story.append(Table([cards[k:k+3] for k in range(0,len(cards),3)],colWidths=[254]*3))
            elif kind=='wireframe':
                first=Phone(block);j=i+1
                while j<len(lines) and not lines[j].strip(): j+=1
                if j<len(lines) and lines[j]=='```wireframe':
                    block2=[];j+=1
                    while lines[j]!='```':block2.append(lines[j]);j+=1
                    story.append(Table([[first,Phone(block2)]],colWidths=[300,300]));i=j
                else:story.append(first)
            else:story.append(table([['진행·상태 흐름']]+[[s] for s in block]))
            story.append(Spacer(1,10))
        elif line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                if not re.fullmatch(r'[| :\-]+',lines[i]): rows.append([c.strip() for c in lines[i].strip('|').split('|')])
                i+=1
            story.extend([table(rows),Spacer(1,12)]);continue
        elif line:story.append(p(line))
        i+=1
    def page(c,doc):
        c.setFillColor(colors.HexColor('#f4f0e6'));c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#20383c'));c.rect(0,H-33,W,33,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#e0bd70'));c.setFont('KRB',9);c.drawString(40,H-22,'모루의 서약 / ANVIL OATH / 사람용 통합 블루프린트')
        c.setStrokeColor(colors.HexColor('#b59b68'));c.line(40,32,W-40,32)
        c.setFont('KR',8);c.setFillColor(colors.HexColor('#5f6d6a'));c.drawString(40,19,'2026.09.11 · 최종 검토용 · 후보/기획/구현/검증 상태 분리 · 인게임 촬영 아님')
        c.drawRightString(W-40,19,str(doc.page))
    SimpleDocTemplate(str(OUTPUT),pagesize=(W,H),leftMargin=40,rightMargin=40,topMargin=48,bottomMargin=43,title='모루의 서약 사람용 통합 블루프린트',author='Blacksmith project').build(story,onFirstPage=page,onLaterPages=page)
    print(OUTPUT)

if __name__=='__main__':build()
