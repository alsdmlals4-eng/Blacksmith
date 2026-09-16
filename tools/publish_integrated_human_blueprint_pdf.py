"""Project-owned human reading view; illustrations remain referenced candidate PNGs."""
from pathlib import Path
import argparse
import re
import sys
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
sys.path.insert(0,str(Path(__file__).resolve().parent))
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
        c.setFillColor(colors.HexColor('#f4e5bf'));c.setFont('KRB',11);c.drawString(10,79,f'{self.number+1:02}  {self.title}')
        c.setFont('KR',9)
        for i,s in enumerate(self.detail.split(' / ')): c.drawString(10,56-i*18,s)


class StatePanel(Flowable):
    """Text-native UI state diagram with unchanged existing candidate images."""
    def __init__(self, row):
        Flowable.__init__(self)
        self.width, self.height = 240, 312
        fields = row.split('|')
        if len(fields) != 9:
            raise ValueError('State atlas requires nine fields')
        self.title,self.mode,self.level,self.durability,self.tag,self.owner,self.notice,self.button,self.delta = fields

    def draw(self):
        c=self.canv
        def box(x,y,w,h,color):
            c.setFillColor(colors.HexColor(color));c.rect(x,y,w,h,fill=1,stroke=0)
        def text(x,y,value,size=9,color='#20383c',bold=False):
            c.setFillColor(colors.HexColor(color));c.setFont('KRB' if bold else 'KR',size);c.drawString(x,y,value)
        box(0,0,240,307,'#d7d3c8');box(3,3,234,301,'#fcfaf4')
        box(3,277,234,27,'#20383c');text(12,286,self.title,11,'#f4e5bf',True)
        text(12,261,'철방패 / 동일 작품 UID S-001',9,bold=True)
        expanded=self.mode in ('WORLD_EXPANDED','WORLD_FOCUS')
        if expanded:
            bh=118 if self.mode=='WORLD_FOCUS' else 69
            c.drawImage(str(ASSETS/'adventure.png'),12,242-bh,216,bh,mask='auto')
            box(12,242-bh,216,17,'#20383c');text(17,247-bh,'세계 기록 재현 / 결과 조작 불가',8,'#ffffff')
            text(12,249,'세계창 '+('확대' if bh==118 else '펼침'),8)
            if bh==118:
                text(12,108,'목표 달성 / 방패 손상',11,bold=True)
                text(12,90,'닫아도 결과·보상 동일',9)
            else:
                text(12,155,'+%s  |  %s'%(self.level,self.tag),11,bold=True)
                text(12,137,'작품 편집: '+self.owner,9)
                text(12,119,'관람 화면과 작업 영역 분리',9)
                text(12,101,'결정창을 열면 관람 일시정지',9)
        else:
            box(12,167,72,77,'#e6e0d4')
            # Clip the existing 128x128 shield cell; no new art or file mutation.
            c.saveState();clip=c.beginPath();clip.rect(15,171,64,64);c.clipPath(clip,stroke=0,fill=0)
            c.drawImage(str(ASSETS/'items.png'),15-64,171-128,192,192,mask='auto');c.restoreState()
            text(94,226,'+%s 철방패'%self.level,15,bold=True)
            text(94,207,self.tag,10,'#765316',True)
            text(94,188,self.owner,9)
            current,maximum,base=map(int,self.durability.split('/'))
            text(12,151,'현재 / 한계 / 출생  '+self.durability,9,bold=True)
            for y,label,ratio in [(130,'현재 상태',current/maximum),(110,'구조 상태',maximum/base)]:
                text(12,y,label,8);box(70,y-1,100,8,'#dedbd3');box(70,y-1,100*ratio,8,'#45837e' if ratio==1 else '#b8773b')
                text(180,y,f'{ratio:.0%}',8)
            if self.mode=='CHRONICLE':
                text(12,88,'연대기: 손상 → 수리·흉터',9,bold=True)
            else:
                text(12,88,self.notice,9,bold=True)
        box(12,47,216,27,'#c8ccc7' if self.button.startswith('불가') else '#275f60')
        text(21,57,self.button,10,'#34443f' if self.button.startswith('불가') else '#ffffff',True)
        text(12,29,self.delta,8,'#7d4825',True)
        text(12,12,'설계 상태 비교 / 인게임 촬영 아님',7,'#67716c')

def build(output):
    output=Path(output)
    if output.exists():
        raise FileExistsError(f'Preserve published blueprint; choose an explicit candidate path: {output}')
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
            elif kind=='runtimecaptures':
                cells=[]
                for row in block:
                    rel,caption=row.split('|',1)
                    path=(SOURCE.parent/rel).resolve()
                    if not path.is_relative_to((ROOT/'docs/testing').resolve()):
                        raise ValueError('Runtime capture path escapes testing evidence')
                    img=Image(str(path))
                    max_height=260 if 'commission-' in rel else 290
                    scale=min(330/img.imageWidth,max_height/img.imageHeight)
                    img.drawWidth=img.imageWidth*scale;img.drawHeight=img.imageHeight*scale
                    cells.append([img,Spacer(1,5),p(caption,small)])
                if len(cells)!=2: raise ValueError('Runtime evidence requires two captured states')
                story.append(Table([cells],colWidths=[(W-80)/2]*2))
            elif kind=='stateatlas':
                if len(block)!=3: raise ValueError('State atlas must compare three states')
                story.append(Table([[StatePanel(row) for row in block]],colWidths=[254]*3))
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
        c.setFont('KR',8);c.setFillColor(colors.HexColor('#5f6d6a'));c.drawString(40,19,'2026.09.16 갱신 · 설계도/후보/실행 촬영은 각 페이지 표기 · 최종 미술·Android·사람 검수는 별도')
        c.drawRightString(W-40,19,str(doc.page))
    output.parent.mkdir(parents=True,exist_ok=True)
    SimpleDocTemplate(str(output),pagesize=(W,H),leftMargin=40,rightMargin=40,topMargin=48,bottomMargin=43,title='모루의 서약 사람용 통합 블루프린트',author='Blacksmith project').build(story,onFirstPage=page,onLaterPages=page)
    print(output)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    build(parser.parse_args().output)
