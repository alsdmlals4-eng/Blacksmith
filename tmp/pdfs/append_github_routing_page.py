from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(r"C:\Users\user\Documents\GitHub\Ninza\Blacksmith")
TARGET = ROOT / "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf"
ADDENDUM = ROOT / "tmp/pdfs/github-routing-addendum.pdf"
OUTPUT = ROOT / "tmp/pdfs/blacksmith_MASTER_PRODUCTION_GDD_20260828.updated.pdf"
FONT = Path(r"C:\Windows\Fonts\malgun.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\malgunbd.ttf")


pdfmetrics.registerFont(TTFont("Malgun", str(FONT)))
pdfmetrics.registerFont(TTFont("MalgunBold", str(FONT_BOLD)))


def draw_wrapped(canvas: Canvas, text: str, x: float, y: float, width: float, font: str, size: float, leading: float) -> float:
    canvas.setFont(font, size)
    words = text.split(" ")
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if canvas.stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            canvas.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        canvas.drawString(x, y, line)
        y -= leading
    return y


canvas = Canvas(str(ADDENDUM), pagesize=A4)
width, height = A4
ink = HexColor("#4B2F1E")
accent = HexColor("#8A542F")
paper = HexColor("#F8F1E4")
canvas.setFillColor(paper)
canvas.rect(0, 0, width, height, fill=1, stroke=0)
canvas.setStrokeColor(HexColor("#B17843"))
canvas.setLineWidth(0.75)
canvas.line(55, height - 43, width - 55, height - 43)
canvas.setFillColor(accent)
canvas.setFont("Malgun", 8.5)
canvas.drawString(55, height - 30, "BLACKSMITH · MASTER PRODUCTION GDD · 2026-08-28")
canvas.setFillColor(ink)
canvas.setFont("MalgunBold", 23)
canvas.drawString(55, height - 88, "28. CURRENT ROUTING ADDENDUM")
canvas.setFont("MalgunBold", 14)
canvas.drawString(55, height - 113, "GitHub-only 정본과 이미지 생성·확정 운영 규칙")

y = height - 151
sections = [
    ("Current authority", [
        "BS-OPS-20260828-35 is the latest user-approved operational override.",
        "GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE. The repository is the only current canon, human-facing GDD, operational handoff, asset record, and evidence surface.",
        "NOTION_STATUS = HISTORICAL_REFERENCE_ONLY / NO_FUTURE_READ_WRITE_REQUIRED. Historical Notion records can prove only their past state and cannot create a current requirement.",
    ]),
    ("Image execution", [
        "ACTUAL_GAME_CONSUMER_REQUIRED and PRIMARY_USE_GATE_REQUIRED remain unchanged. Required consumer metadata and provenance/rights fields must exist before generation.",
        "IMAGE_GENERATION_EXECUTION = USER_PREAUTHORIZED_AFTER_CONSUMER_REQUIREMENT. The agent generates a candidate without a pre-generation approval interruption.",
        "POST_GENERATION_USER_LOCK = REQUIRED_FOR_FINAL_DIRECTION_OR_RUNTIME_PROMOTION. Before this lock, a candidate is not a final visual direction, runtime asset, release asset, or Human/Player Experience proof.",
    ]),
    ("Repository receipt and evidence ceiling", [
        "A locked result records its repository destination, exact path, consumer, SHA-256/provenance and rights state, then receives exact-head readback.",
        "This routing change does not claim Godot client rendering, Android readability, accessibility, performance, human usability, player experience, or release readiness. Those remain NOT_RUN until directly evidenced.",
    ]),
]

for heading, bullets in sections:
    canvas.setFillColor(accent)
    canvas.setFont("MalgunBold", 13)
    canvas.drawString(55, y, heading)
    y -= 19
    canvas.setFillColor(ink)
    for bullet in bullets:
        canvas.setFillColor(accent)
        canvas.circle(63, y + 3, 2.2, fill=1, stroke=0)
        canvas.setFillColor(ink)
        y = draw_wrapped(canvas, bullet, 74, y, width - 130, "Malgun", 10.2, 15)
        y -= 4
    y -= 8

canvas.setStrokeColor(HexColor("#B17843"))
canvas.line(55, 48, width - 55, 48)
canvas.setFillColor(accent)
canvas.setFont("Malgun", 8)
canvas.drawRightString(width - 55, 28, "39")
canvas.save()

reader = PdfReader(str(TARGET))
addendum = PdfReader(str(ADDENDUM))
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
writer.add_page(addendum.pages[0])
writer.add_metadata({
    "/Title": "Blacksmith Master Production GDD",
    "/Subject": "Current canon planning and implementation contract; BS-OPS-20260828-35 addendum",
    "/Author": "Blacksmith Project",
})
with OUTPUT.open("wb") as stream:
    writer.write(stream)
OUTPUT.replace(TARGET)
print(f"updated {TARGET} with {len(reader.pages) + 1} pages")
