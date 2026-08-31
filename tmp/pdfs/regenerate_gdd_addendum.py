from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(r"C:\Users\user\Documents\GitHub\Ninza\Blacksmith")
TARGET = ROOT / "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf"
ADDENDUM = ROOT / "tmp/pdfs/rebuilt-gdd-addendum.pdf"
OUTPUT = ROOT / "tmp/pdfs/blacksmith_MASTER_PRODUCTION_GDD_20260828.rebuilt.pdf"
pdfmetrics.registerFont(TTFont("Malgun", r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", r"C:\Windows\Fonts\malgunbd.ttf"))


def wrap(canvas: Canvas, text: str, x: float, y: float, width: float) -> float:
    canvas.setFont("Malgun", 10.2)
    line = ""
    for word in text.split(" "):
        candidate = word if not line else f"{line} {word}"
        if canvas.stringWidth(candidate, "Malgun", 10.2) <= width:
            line = candidate
            continue
        canvas.drawString(x, y, line)
        y -= 15
        line = word
    if line:
        canvas.drawString(x, y, line)
        y -= 15
    return y


def start_page(canvas: Canvas, number: str, title: str, subtitle: str, page_number: str) -> float:
    width, height = A4
    canvas.setFillColor(HexColor("#F8F1E4"))
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setStrokeColor(HexColor("#B17843"))
    canvas.setLineWidth(0.75)
    canvas.line(55, height - 43, width - 55, height - 43)
    canvas.setFillColor(HexColor("#8A542F"))
    canvas.setFont("Malgun", 8.5)
    canvas.drawString(55, height - 30, "BLACKSMITH · MASTER PRODUCTION GDD · 2026-08-28")
    canvas.setFillColor(HexColor("#4B2F1E"))
    canvas.setFont("MalgunBold", 23)
    canvas.drawString(55, height - 88, f"{number}. {title}")
    canvas.setFont("MalgunBold", 14)
    canvas.drawString(55, height - 113, subtitle)
    canvas.setStrokeColor(HexColor("#B17843"))
    canvas.line(55, 48, width - 55, 48)
    canvas.setFillColor(HexColor("#8A542F"))
    canvas.setFont("Malgun", 8)
    canvas.drawRightString(width - 55, 28, page_number)
    return height - 151


def sections(canvas: Canvas, y: float, groups: list[tuple[str, list[str]]]) -> None:
    ink = HexColor("#4B2F1E")
    accent = HexColor("#8A542F")
    width, _ = A4
    for heading, bullets in groups:
        canvas.setFillColor(accent)
        canvas.setFont("MalgunBold", 13)
        canvas.drawString(55, y, heading)
        y -= 19
        for bullet in bullets:
            canvas.setFillColor(accent)
            canvas.circle(63, y + 3, 2.2, fill=1, stroke=0)
            canvas.setFillColor(ink)
            y = wrap(canvas, bullet, 74, y, width - 130)
            y -= 4
        y -= 8


canvas = Canvas(str(ADDENDUM), pagesize=A4)
y = start_page(
    canvas,
    "28",
    "CURRENT ROUTING ADDENDUM",
    "GitHub-only 정본과 이미지 생성·확정 운영 규칙",
    "39",
)
sections(canvas, y, [
    ("Current authority", [
        "BS-OPS-20260828-35 is the latest user-approved operational override.",
        "GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE. The repository is the only current canon, human-facing GDD, operational handoff, asset record, and evidence surface.",
        "NOTION_STATUS = HISTORICAL_REFERENCE_ONLY / NO_FUTURE_READ_WRITE_REQUIRED. Historical records prove only their past state and cannot create a current requirement.",
    ]),
    ("Image execution", [
        "ACTUAL_GAME_CONSUMER_REQUIRED and PRIMARY_USE_GATE_REQUIRED remain unchanged. Required consumer metadata and provenance/rights fields must exist before generation.",
        "IMAGE_GENERATION_EXECUTION = USER_PREAUTHORIZED_AFTER_CONSUMER_REQUIREMENT. The agent may generate a candidate without a pre-generation approval interruption.",
        "POST_GENERATION_USER_LOCK = REQUIRED_FOR_FINAL_DIRECTION_OR_RUNTIME_PROMOTION. Before lock, a candidate is not a final visual direction, runtime asset, release asset, or Human/Player Experience proof.",
    ]),
    ("Repository receipt and evidence ceiling", [
        "A locked result records its repository destination, exact path, consumer, SHA-256/provenance and rights state, then receives exact-head readback.",
        "This routing change does not claim Godot client rendering, Android readability, accessibility, performance, human usability, player experience, or release readiness. Those remain NOT_RUN until directly evidenced.",
    ]),
])

canvas.showPage()
y = start_page(
    canvas,
    "29",
    "NOTION MIGRATION RECEIPT",
    "Notion 구조·작업물의 GitHub 정본 이관 완료",
    "40",
)
sections(canvas, y, [
    ("One-time source migration", [
        "NOTION_READ_ONLY_ONE_TIME_SOURCE_MIGRATION = COMPLETE. All future Blacksmith canon, human-facing GDD, handoff, asset, and evidence work stays in GitHub.",
        "NO_FUTURE_NOTION_READ_WRITE = TRUE. Old Notion pages remain provenance only and cannot become current requirements or receive destination readback.",
    ]),
    ("Structure coverage", [
        "Project Home / Hub, System Record, Direction, Flow, Core Systems, Enhancement Economy, Visual Bible, Visual UX Assets, Asset Library, Handoff, Validation, and Benchmark all map to existing current GitHub owners.",
        "The old Project Plan's superseded numeric tables, state models, milestone arrangements, and prior receipts are intentionally omitted as stale data; current decision owners remain authoritative.",
    ]),
    ("Historical visual preservation", [
        "All eight approved Visual GDD original PNGs are archived at docs/migration/historical_notion_gdd, outside runtime asset paths, and SHA-256 checked against the historical approval manifest.",
        "The archive is HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME / NOT_FINAL_STYLE_CANON / STALE_DO_NOT_IMPORT. It preserves information architecture and provenance, never a current UI, balance, style, or player-evidence claim.",
    ]),
    ("Verification", [
        "The GitHub migration receipt and machine-readable manifest own the mapping. The GitHub-only migration contract checks each required destination and all eight exact binary hashes.",
    ]),
])
canvas.save()

existing = PdfReader(str(TARGET))
assert len(existing.pages) >= 40
addendum = PdfReader(str(ADDENDUM))
writer = PdfWriter()
for page in existing.pages[:38]:
    writer.add_page(page)
for page in addendum.pages:
    writer.add_page(page)
writer.add_metadata({
    "/Title": "Blacksmith Master Production GDD",
    "/Subject": "Current canon planning and implementation contract; GitHub-only routing and Notion migration addenda",
    "/Author": "Blacksmith Project",
})
with OUTPUT.open("wb") as stream:
    writer.write(stream)
OUTPUT.replace(TARGET)
print("rebuilt Blacksmith Master Production GDD with 40 pages")
