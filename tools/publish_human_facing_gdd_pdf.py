#!/usr/bin/env python3
"""Deterministically publish the Korean human-facing Blacksmith GDD to A4 PDF."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md"
OUTPUT = ROOT / "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf"
RECEIPT = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json"
FONT = Path(r"C:\Windows\Fonts\malgun.ttf")
ASSETS = [
    ("메인 메뉴", ROOT / "assets/ui/workshop/main_menu_dawn_background_v1.png"),
    ("정밀 강화 공방", ROOT / "assets/ui/workshop/precision_tag_workshop_background_v1.png"),
    ("고객 결과", ROOT / "assets/ui/workshop/customer_result_return_illustration_v1.png"),
]


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text: str) -> str:
    """Escape source text first, then render only bold and code delimiters as safe typography."""
    escaped = xml(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    return re.sub(r"`([^`]+)`", r'<font color="#725A45">\1</font>', escaped)


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Malgun", 8)
    canvas.setFillColor(colors.HexColor("#725A45"))
    canvas.drawString(18 * mm, 12 * mm, "Blacksmith · 사람용 게임 기획서")
    canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, f"{doc.page} / 2026-08-30")
    canvas.restoreState()


def parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        if re.match(r"^\|?\s*[-:]+", line.strip()):
            continue
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def story(markdown: str):
    pdfmetrics.registerFont(TTFont("Malgun", str(FONT)))
    s = getSampleStyleSheet()
    title = ParagraphStyle("TitleKO", parent=s["Title"], fontName="Malgun", fontSize=22, leading=30, alignment=TA_CENTER, textColor=colors.HexColor("#4B3024"), spaceAfter=9 * mm)
    h1 = ParagraphStyle("H1KO", parent=s["Heading1"], fontName="Malgun", fontSize=15, leading=22, textColor=colors.HexColor("#7A3F25"), spaceBefore=6 * mm, spaceAfter=3 * mm, keepWithNext=True)
    h2 = ParagraphStyle("H2KO", parent=s["Heading2"], fontName="Malgun", fontSize=11.5, leading=17, textColor=colors.HexColor("#5D4635"), spaceBefore=4 * mm, spaceAfter=2 * mm, keepWithNext=True)
    body = ParagraphStyle("BodyKO", parent=s["BodyText"], fontName="Malgun", fontSize=9.2, leading=14.2, spaceAfter=2.5 * mm)
    bullet = ParagraphStyle("BulletKO", parent=body, leftIndent=5 * mm, firstLineIndent=-3.5 * mm)
    caption = ParagraphStyle("CaptionKO", parent=body, fontSize=8.2, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#725A45"))
    flow = ParagraphStyle("FlowKO", parent=body, backColor=colors.HexColor("#F5EFE7"), borderColor=colors.HexColor("#C8AD90"), borderWidth=0.5, borderPadding=7)
    out = []
    lines, i = markdown.splitlines(), 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1; continue
        if line.startswith("# "):
            out.append(Paragraph(xml(line[2:]), title)); i += 1; continue
        if line.startswith("## "):
            out.append(Paragraph(xml(line[3:]), h1)); i += 1; continue
        if line.startswith("### "):
            out.append(Paragraph(xml(line[4:]), h2)); i += 1; continue
        if line.startswith("|"):
            chunk = []
            while i < len(lines) and lines[i].startswith("|"):
                chunk.append(lines[i]); i += 1
            rows = parse_table(chunk)
            if rows:
                count = len(rows[0]); width = (A4[0] - 36 * mm) / count
                data = [[Paragraph(inline(cell), body) for cell in row] for row in rows]
                table = Table(data, colWidths=[width] * count, repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8D9C7")), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B89E83")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
                out.extend([table, Spacer(1, 3 * mm)])
            continue
        if line.startswith("```"):
            is_mermaid = line.startswith("```mermaid")
            block, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                if lines[i] and not lines[i].startswith("flowchart"):
                    block.append(lines[i])
                i += 1
            i += 1
            if block and not is_mermaid: out.append(Paragraph("<br/>".join(xml(x) for x in block), flow))
            continue
        if line.startswith("- "):
            out.append(Paragraph("• " + inline(line[2:]), bullet)); i += 1; continue
        out.append(Paragraph(inline(line), body)); i += 1
    out.append(Spacer(1, 5 * mm))
    out.append(Paragraph("승인된 런타임 소비처 삽화", h1))
    for name, asset in ASSETS:
        if asset.exists():
            out.append(KeepTogether([Paragraph(xml(name), h2), Image(str(asset), width=68 * mm, height=120.8 * mm), Paragraph("이 삽화는 런타임 스크린샷이 아니다. 실제 클라이언트·Android·접근성·사람 시각 검수는 NOT_RUN.", caption), Spacer(1, 4 * mm)]))
    return out


def build_pdf() -> str:
    """Build once with invariant ReportLab metadata and return the exact artifact SHA-256."""
    def invariant_canvas(*args, **kwargs):
        kwargs["invariant"] = 1
        return canvas.Canvas(*args, **kwargs)

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm, title="Blacksmith 사람용 게임 기획서", author="Blacksmith Project", subject="Human-facing Korean GDD", creator="Blacksmith deterministic ReportLab publisher")
    doc.build(story(SOURCE.read_text(encoding="utf-8")), onFirstPage=footer, onLaterPages=footer, canvasmaker=invariant_canvas)
    return hashlib.sha256(OUTPUT.read_bytes()).hexdigest()


def main() -> None:
    if not FONT.exists():
        raise FileNotFoundError(FONT)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    first_sha256 = build_pdf()
    second_sha256 = build_pdf()
    if first_sha256 != second_sha256:
        raise RuntimeError("invariant publisher produced different PDF bytes")
    reader = PdfReader(str(OUTPUT))
    receipt = {
        "schema_version": 2,
        "receipt_id": "BS-GDD-20260830-RECURRING-PRECISION-HUMAN-PDF",
        "status": "RENDERED_AND_VISUALLY_INSPECTED / NOT_PRODUCT_RUNTIME_EVIDENCE",
        "source_markdown": {"path": "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md", "sha256": normalized_sha256(SOURCE), "hash_basis": "UTF-8_BYTES_WITH_CRLF_TO_LF_NORMALIZATION"},
        "artifact": {"path": "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf", "sha256": second_sha256, "page_count": len(reader.pages), "pdf_title": reader.metadata.title, "pdf_subject": reader.metadata.subject, "target_format": "A4"},
        "publish_recipe": {"publisher": "tools/publish_human_facing_gdd_pdf.py", "engine": "ReportLab", "font": "C:/Windows/Fonts/malgun.ttf", "invariant": True, "images": [str(path.relative_to(ROOT)).replace("\\", "/") for _, path in ASSETS]},
        "deterministic_publish_proof": {"invariant": True, "identical_sha256_runs": [first_sha256, second_sha256], "run_count": 2, "basis": "two consecutive invariant ReportLab publishes with unchanged source"},
        "render_validation": {"required_tool": "Poppler pdftoppm", "rendered_pages": list(range(1, len(reader.pages) + 1)), "inspection": "ALL_PAGES_RENDERED_AND_REVIEWED_BEFORE_RECEIPT_FINALIZATION", "result": "KOREAN_TEXT_TABLES_FLOW_AND_SCENE_CONTEXT_INSPECTED"},
        "provenance": {"document_role": "human-facing project GDD PDF", "runtime_asset": False, "human_usability_or_player_experience_evidence": False},
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
