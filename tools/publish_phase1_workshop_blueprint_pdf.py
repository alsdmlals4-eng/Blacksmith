#!/usr/bin/env python3
"""Publish a deterministic, non-canonical Phase 1 Workshop Blueprint Viewer PDF."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "exports/blacksmith_PHASE1_WORKSHOP_BLUEPRINT_20260902.pdf"
RECEIPT = ROOT / "docs/operations/receipts/2026-09-02-phase1-workshop-blueprint-pdf.json"
FONT_REGULAR = Path(r"C:\Windows\Fonts\malgun.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\malgunbd.ttf")
TITLE = "모루의 서약 · Phase 1 워크숍 블루프린트"
SOURCES = (
    ROOT / "docs/superpowers/specs/2026-09-01-phase1-workshop-blueprint-design.md",
    ROOT / "docs/planning/PROJECT_CORE_SCENE_VISUAL_BOARD_20260828.md",
    ROOT / "docs/planning/BLACKSMITH_HUMAN_GAME_FLOW_MAP_2026.md",
    ROOT / "docs/operations/receipts/2026-09-01-phase1-workshop-blueprint.json",
)

PARCHMENT = colors.HexColor("#F7F0E5")
PAPER = colors.HexColor("#FFFDF8")
INK = colors.HexColor("#36261F")
MUTED = colors.HexColor("#765D4D")
COPPER = colors.HexColor("#A95732")
GOLD = colors.HexColor("#B88A3B")
LINE = colors.HexColor("#D7BFA3")
PALE_COPPER = colors.HexColor("#F1E1D4")
PALE_GOLD = colors.HexColor("#F4E9CF")
PALE_GREEN = colors.HexColor("#E7F0E4")
PALE_BLUE = colors.HexColor("#E4EEF2")
FOOTER_LINE_MM = 14.0
PAGE_TWO_NODE_HEIGHT_MM = 18.0
PAGE_TWO_NODE_GAP_MM = 5.0
PAGE_TWO_GUARD_TOP_MM = 88.0
PAGE_TWO_GUARD_HEIGHT_MM = 26.0
PAGE_THREE_PHONE_TOP_OFFSET_MM = 49.0
PAGE_THREE_PHONE_HEIGHT_MM = 200.0
PAGE_THREE_SUPPORT_TOP_MM = 90.0
PAGE_THREE_SUPPORT_HEIGHT_MM = 26.0
PAGE_THREE_SUPPORT_WIDTH_MM = 31.0
FLOW_NODE_BODY_LEFT_MM = 16.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def layout_bounds() -> dict[str, float]:
    """Expose the footer-clearance geometry used by the fixed-layout pages."""
    page_height_mm = A4[1] / mm
    return {
        "footer_line_mm": FOOTER_LINE_MM,
        "page_two_guard_bottom_mm": PAGE_TWO_GUARD_TOP_MM - PAGE_TWO_GUARD_HEIGHT_MM,
        "page_three_phone_bottom_mm": page_height_mm - PAGE_THREE_PHONE_TOP_OFFSET_MM - PAGE_THREE_PHONE_HEIGHT_MM,
        "page_three_support_card_bottom_mm": PAGE_THREE_SUPPORT_TOP_MM - PAGE_THREE_SUPPORT_HEIGHT_MM,
        "flow_node_body_left_mm": FLOW_NODE_BODY_LEFT_MM,
    }


def register_fonts() -> None:
    if not FONT_REGULAR.exists() or not FONT_BOLD.exists():
        raise FileNotFoundError("Malgun Gothic regular and bold fonts are required")
    pdfmetrics.registerFont(TTFont("BlueprintMalgun", str(FONT_REGULAR)))
    pdfmetrics.registerFont(TTFont("BlueprintMalgunBold", str(FONT_BOLD)))


def draw_wrapped(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    top: float,
    width: float,
    *,
    font: str = "BlueprintMalgun",
    size: float = 9.0,
    leading: float = 14.0,
    color: colors.Color = INK,
) -> float:
    """Draw Korean-safe text by wrapping at individual glyph boundaries."""
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    current = ""
    y = top
    for character in text:
        if character == "\n":
            pdf.drawString(x, y, current)
            y -= leading
            current = ""
            continue
        candidate = current + character
        if current and pdfmetrics.stringWidth(candidate, font, size) > width:
            pdf.drawString(x, y, current)
            y -= leading
            current = character
        else:
            current = candidate
    if current:
        pdf.drawString(x, y, current)
        y -= leading
    return y


def panel(
    pdf: canvas.Canvas,
    x: float,
    top: float,
    width: float,
    height: float,
    *,
    fill: colors.Color = PAPER,
    stroke: colors.Color = LINE,
    radius: float = 3 * mm,
) -> None:
    pdf.setFillColor(fill)
    pdf.setStrokeColor(stroke)
    pdf.setLineWidth(0.7)
    pdf.roundRect(x, top - height, width, height, radius, fill=1, stroke=1)


def label(pdf: canvas.Canvas, text: str, x: float, top: float, *, color: colors.Color = COPPER) -> None:
    pdf.setFont("BlueprintMalgunBold", 7.4)
    pdf.setFillColor(color)
    pdf.drawString(x, top, text)


def heading(pdf: canvas.Canvas, text: str, x: float, top: float, *, size: float = 16.0) -> float:
    pdf.setFont("BlueprintMalgunBold", size)
    pdf.setFillColor(INK)
    pdf.drawString(x, top, text)
    return top - size - 4


def arrow(pdf: canvas.Canvas, x1: float, y1: float, x2: float, y2: float, *, color: colors.Color = COPPER) -> None:
    pdf.setStrokeColor(color)
    pdf.setFillColor(color)
    pdf.setLineWidth(1.4)
    pdf.line(x1, y1, x2, y2)
    angle = 0.44
    from math import atan2, cos, sin

    direction = atan2(y2 - y1, x2 - x1)
    head = 3.2 * mm
    pdf.line(x2, y2, x2 - head * cos(direction - angle), y2 - head * sin(direction - angle))
    pdf.line(x2, y2, x2 - head * cos(direction + angle), y2 - head * sin(direction + angle))


def header(pdf: canvas.Canvas, page: int, section: str) -> None:
    page_width, page_height = A4
    pdf.setFillColor(PARCHMENT)
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.5)
    pdf.line(14 * mm, page_height - 12 * mm, page_width - 14 * mm, page_height - 12 * mm)
    label(pdf, "모루의 서약 · BLUEPRINT VIEWER · DERIVED NON-CANONICAL", 14 * mm, page_height - 9 * mm)
    pdf.setFont("BlueprintMalgun", 8)
    pdf.setFillColor(MUTED)
    pdf.drawRightString(page_width - 14 * mm, page_height - 9 * mm, section)
    pdf.setStrokeColor(LINE)
    pdf.line(14 * mm, FOOTER_LINE_MM * mm, page_width - 14 * mm, FOOTER_LINE_MM * mm)
    pdf.setFont("BlueprintMalgun", 7.4)
    pdf.setFillColor(MUTED)
    pdf.drawString(14 * mm, 9 * mm, "정본 대체 금지 · 실제 게임 화면 또는 런타임 에셋이 아님")
    pdf.drawRightString(page_width - 14 * mm, 9 * mm, f"{page} / 5 · 2026-09-02")


def card(
    pdf: canvas.Canvas,
    x: float,
    top: float,
    width: float,
    height: float,
    kicker: str,
    title_text: str,
    body: str,
    *,
    fill: colors.Color = PAPER,
) -> None:
    panel(pdf, x, top, width, height, fill=fill)
    label(pdf, kicker, x + 5 * mm, top - 6 * mm)
    y = heading(pdf, title_text, x + 5 * mm, top - 12 * mm, size=11.3)
    draw_wrapped(pdf, body, x + 5 * mm, y - 2 * mm, width - 10 * mm, size=8.5, leading=12.5, color=MUTED)


def page_one(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 1, "읽기 안내")
    y = page_height - 28 * mm
    label(pdf, "PHASE 1 · PORTRAIT WORKSHOP INFORMATION ARCHITECTURE", 18 * mm, y)
    y -= 12 * mm
    y = heading(pdf, "모루의 서약", 18 * mm, y, size=27)
    y = heading(pdf, "Phase 1 워크숍 블루프린트", 18 * mm, y - 2 * mm, size=18)
    y = draw_wrapped(
        pdf,
        "한 작품의 강화 판단이 고객의 실제 사용 결과와 연대기로 이어지는 세로형 공방 흐름을 읽기 위한 파생 PDF입니다.",
        18 * mm,
        y - 5 * mm,
        page_width - 36 * mm,
        size=10,
        leading=16,
        color=MUTED,
    )
    card(
        pdf,
        18 * mm,
        y - 5 * mm,
        page_width - 36 * mm,
        31 * mm,
        "PLAYER PROMISE",
        "STOP OR PUSH",
        "이미 충분히 좋은 작품을 지금 지킬지, 한 번 더 강화해 특별한 결과를 노릴지 판단한다. 이 PDF는 그 선택이 흐름 속에서 어디에 놓이는지를 보여 준다.",
        fill=PALE_GOLD,
    )
    flow_top = y - 44 * mm
    column_width = (page_width - 42 * mm) / 3
    flow_cards = (
        ("01", "같은 UID 작품", "제작 뒤에도 장비 정체성·레벨·태그·내구도가 하나의 작품에 남는다."),
        ("02", "정밀강화 판단", "+10 단위마다 태그를 추가하거나 기존 태그를 강화한다. 성공은 항상 +1이다."),
        ("03", "실제 사용의 귀환", "인계 자체는 손상이 아니며, 고객의 실제 사용 결과와 조건부 수리·연대기가 돌아온다."),
    )
    for index, (number, title_text, body) in enumerate(flow_cards):
        x = 18 * mm + index * column_width
        card(pdf, x, flow_top, column_width - 6 * mm, 50 * mm, f"{number} · CORE LINK", title_text, body)
        if index < 2:
            arrow(pdf, x + column_width - 7 * mm, flow_top - 25 * mm, x + column_width + 1 * mm, flow_top - 25 * mm)
    card(
        pdf,
        18 * mm,
        flow_top - 59 * mm,
        page_width - 36 * mm,
        42 * mm,
        "VIEWER BOUNDARY",
        "정본을 대체하지 않는 검토용 PDF",
        "원본 owner는 기존 Markdown·JSON·코드·테스트입니다. 이 문서는 화면 구조를 빠르게 확인하기 위한 파생 보기이며, 새 경제·새 자산·새 게임 규칙을 만들지 않습니다. 사용자 블루프린트 검토 대기 상태를 유지합니다.",
        fill=PALE_COPPER,
    )


def flow_node(pdf: canvas.Canvas, x: float, top: float, width: float, height: float, number: str, title_text: str, body: str, *, fill: colors.Color) -> None:
    panel(pdf, x, top, width, height, fill=fill)
    pdf.setFillColor(COPPER)
    pdf.circle(x + 8 * mm, top - 8 * mm, 4.2 * mm, fill=1, stroke=0)
    pdf.setFont("BlueprintMalgunBold", 7.2)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(x + 8 * mm, top - 9 * mm, number)
    y = heading(pdf, title_text, x + 16 * mm, top - 7 * mm, size=10.8)
    draw_wrapped(pdf, body, x + FLOW_NODE_BODY_LEFT_MM * mm, y - 1 * mm, width - (FLOW_NODE_BODY_LEFT_MM + 6) * mm, size=8.2, leading=11.8, color=MUTED)


def page_two(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 2, "전체 흐름")
    y = heading(pdf, "한 작품의 Phase 1 흐름", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "일반 강화의 짧은 리듬과 +10 단위의 정밀 판단, 그리고 같은 UID의 실제 사용 결과를 한 줄로 연결한다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.5, leading=14, color=MUTED)
    x = 22 * mm
    width = page_width - 44 * mm
    height = PAGE_TWO_NODE_HEIGHT_MM * mm
    nodes = (
        ("1", "메인 메뉴", "한 작품의 여정을 시작한다. 이 단계는 선택을 강요하지 않는 기대 설정이다.", PALE_GOLD),
        ("2", "첫 제작", "검·방패·활·갑옷·투구 중 장비 종류를 선택하고, 이후 같은 UID 작품을 만든다.", PAPER),
        ("3", "공방: 일반 강화", "다음 target과 성공·유지·손상 가능성을 읽고 일반 강화의 +1 결과를 확인한다.", PALE_BLUE),
        ("4", "정밀강화: +10 단위", "첫 +10은 태그 추가만, 이후 +20…+100은 태그 추가 또는 태그 강화다.", PALE_COPPER),
        ("5", "고객의 실제 사용 결과", "인계만으로 손상을 만들지 않는다. 실제 사용 뒤 임무 결과와 손상을 별도 축으로 되돌린다.", PAPER),
        ("6", "수리와 작품 연대기", "실제 손상 뒤에만 조건부 수리 job을 열고, 의미 사건만 같은 작품의 역사로 기록한다.", PALE_GREEN),
    )
    top = y - 6 * mm
    for index, (number, title_text, body, fill) in enumerate(nodes):
        flow_node(pdf, x, top, width, height, number, title_text, body, fill=fill)
        if index < len(nodes) - 1:
            arrow(pdf, x + width / 2, top - height - 2 * mm, x + width / 2, top - height - 7 * mm)
        top -= height + PAGE_TWO_NODE_GAP_MM * mm
    guard_top = PAGE_TWO_GUARD_TOP_MM * mm
    panel(pdf, 18 * mm, guard_top, page_width - 36 * mm, PAGE_TWO_GUARD_HEIGHT_MM * mm, fill=PALE_COPPER)
    label(pdf, "GUARDRAIL", 23 * mm, guard_top - 6 * mm)
    draw_wrapped(pdf, "손상을 보여 주기 위해 결과를 조작하지 않는다. 수리·연대기·고객 결과는 강화의 긴장감을 보조하며, 핵심 선택을 대체하지 않는다.", 23 * mm, guard_top - 12 * mm, page_width - 46 * mm, size=8.8, leading=13.3, color=INK)


def thin_line(pdf: canvas.Canvas, x: float, y: float, width: float) -> None:
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.4)
    pdf.line(x, y, x + width, y)


def page_three(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 3, "세로형 공방 와이어프레임")
    heading(pdf, "공방 · 핵심 판단 화면", 18 * mm, page_height - 27 * mm, size=18)
    draw_wrapped(pdf, "설명용 와이어프레임입니다. 실제 게임 스크린샷이 아니며 네이티브 Control의 정보 우선순위를 표현합니다.", 18 * mm, page_height - 37 * mm, page_width - 36 * mm, size=9.2, leading=14, color=MUTED)
    phone_x = 54 * mm
    phone_top = page_height - PAGE_THREE_PHONE_TOP_OFFSET_MM * mm
    phone_width = 102 * mm
    phone_height = PAGE_THREE_PHONE_HEIGHT_MM * mm
    panel(pdf, phone_x, phone_top, phone_width, phone_height, fill=colors.white, stroke=INK, radius=7 * mm)
    pdf.setFillColor(INK)
    pdf.roundRect(phone_x + 42 * mm, phone_top - 5 * mm, 18 * mm, 2 * mm, 1 * mm, fill=1, stroke=0)
    screen_x = phone_x + 7 * mm
    screen_width = phone_width - 14 * mm
    panel(pdf, screen_x, phone_top - 10 * mm, screen_width, 21 * mm, fill=PALE_GOLD)
    label(pdf, "WORKSHOP", screen_x + 4 * mm, phone_top - 16 * mm)
    pdf.setFont("BlueprintMalgunBold", 11)
    pdf.setFillColor(INK)
    pdf.drawString(screen_x + 4 * mm, phone_top - 22 * mm, "모루의 서약 · 공방")
    panel(pdf, screen_x, phone_top - 36 * mm, screen_width, 43 * mm, fill=PARCHMENT)
    label(pdf, "현재 작품 · SAME UID", screen_x + 4 * mm, phone_top - 42 * mm)
    pdf.setFont("BlueprintMalgunBold", 12.5)
    pdf.setFillColor(INK)
    pdf.drawString(screen_x + 4 * mm, phone_top - 50 * mm, "철검 · +19 · 예리함 II")
    draw_wrapped(pdf, "현재 4 / 최대 5 / 출생 5\n상태: 경미 손상", screen_x + 4 * mm, phone_top - 59 * mm, screen_width - 8 * mm, size=8.4, leading=12, color=MUTED)
    panel(pdf, screen_x, phone_top - 85 * mm, screen_width, 51 * mm, fill=PALE_COPPER)
    label(pdf, "NEXT DECISION", screen_x + 4 * mm, phone_top - 91 * mm)
    pdf.setFont("BlueprintMalgunBold", 12)
    pdf.setFillColor(INK)
    pdf.drawString(screen_x + 4 * mm, phone_top - 99 * mm, "정밀강화 +20")
    draw_wrapped(pdf, "태그 행동: [태그 추가] [태그 강화]\n성공 · 실패 유지 · 조건부 손상\n성공 시: 레벨 +1과 선택한 태그 성장", screen_x + 4 * mm, phone_top - 109 * mm, screen_width - 8 * mm, size=8.2, leading=11.7, color=INK)
    panel(pdf, screen_x, phone_top - 142 * mm, screen_width, 37 * mm, fill=PALE_BLUE)
    label(pdf, "정밀 촉매 = 실제 소모 자원", screen_x + 4 * mm, phone_top - 148 * mm)
    draw_wrapped(pdf, "불의 심장 · 보유 63\n대지의 결정 · 보유 64\n계보 선택이 아님 · 필요 촉매 ×1을 원자적으로 소비", screen_x + 4 * mm, phone_top - 156 * mm, screen_width - 8 * mm, size=8.1, leading=10.8, color=INK)
    panel(pdf, screen_x, phone_top - 184 * mm, screen_width, 15 * mm, fill=COPPER, stroke=COPPER)
    pdf.setFont("BlueprintMalgunBold", 9.5)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(screen_x + screen_width / 2, phone_top - 193.5 * mm, "정밀강화 시도")
    support_top = PAGE_THREE_SUPPORT_TOP_MM * mm
    support_width = PAGE_THREE_SUPPORT_WIDTH_MM * mm
    support_height = PAGE_THREE_SUPPORT_HEIGHT_MM * mm
    left_support_x = 18 * mm
    right_support_x = page_width - 18 * mm - support_width
    panel(pdf, left_support_x, support_top, support_width, support_height, fill=PALE_GOLD)
    label(pdf, "읽기 순서", left_support_x + 3 * mm, support_top - 5 * mm)
    draw_wrapped(pdf, "1. 작품\n2. 판단\n3. 조건\n4. 귀환", left_support_x + 3 * mm, support_top - 11 * mm, support_width - 6 * mm, size=7.1, leading=9.5, color=INK)
    panel(pdf, right_support_x, support_top, support_width, support_height, fill=PALE_GREEN)
    label(pdf, "추가하지 않음", right_support_x + 3 * mm, support_top - 5 * mm)
    draw_wrapped(pdf, "일반 인벤토리\n고객 관리 loop\n정밀 전용 배경\n촉매 전용 그림", right_support_x + 3 * mm, support_top - 11 * mm, support_width - 6 * mm, size=6.7, leading=8.8, color=INK)


def table_row(pdf: canvas.Canvas, x: float, top: float, columns: tuple[float, float, float], values: tuple[str, str, str], *, fill: colors.Color) -> float:
    height = 25 * mm
    panel(pdf, x, top, sum(columns), height, fill=fill, radius=1.5 * mm)
    cursor = x
    for index, (column, value) in enumerate(zip(columns, values)):
        draw_wrapped(pdf, value, cursor + 3 * mm, top - 5 * mm, column - 6 * mm, size=7.6, leading=10.5, color=INK)
        cursor += column
        if index < len(columns) - 1:
            pdf.setStrokeColor(LINE)
            pdf.line(cursor, top - 2 * mm, cursor, top - height + 2 * mm)
    return top - height - 3 * mm


def page_four(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 4, "상태·정본 경계")
    y = heading(pdf, "화면은 보여 주고, 정본은 계산한다", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "블루프린트는 화면에 필요한 입력과 결과를 정리할 뿐, 확률·비용·손상 규칙과 이미지 승격을 새로 소유하지 않는다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.3, leading=14, color=MUTED)
    x = 18 * mm
    columns = (41 * mm, 59 * mm, page_width - 36 * mm - 100 * mm)
    y -= 5 * mm
    y = table_row(pdf, x, y, columns, ("화면 상태", "화면의 책임", "하지 않는 일"), fill=PALE_GOLD)
    rows = (
        ("일반 강화 준비", "현재 작품, 다음 target, resolver가 준 성공·실패·손상 확률과 비용을 읽기 좋게 표시한다.", "확률을 재계산하거나 실패 결과를 바꾸지 않는다."),
        ("정밀 태그 추가", "+10 단위에서 태그 추가 또는 강화의 사전 조건·미리보기·비용을 명시한다.", "무작위 태그·reroll·네 번째 affix를 만들지 않는다."),
        ("정밀 태그 강화", "선택한 기존 태그의 필요한 촉매를 자동 표시하고 실제 소모 결과를 보여 준다.", "촉매를 계보 선택으로 바꾸거나 다른 재료로 우회하지 않는다."),
        ("수리·결과·연대기", "같은 UID의 실제 사용 결과와 CURRENT/MAX/BASE_MAX, 수리 가능 여부를 표시한다.", "인계만으로 손상을 만들거나 고객 관리 loop를 추가하지 않는다."),
    )
    fills = (PAPER, PALE_COPPER, PAPER, PALE_GREEN)
    for row, fill in zip(rows, fills):
        y = table_row(pdf, x, y, columns, row, fill=fill)
    panel(pdf, 18 * mm, y - 3 * mm, page_width - 36 * mm, 46 * mm, fill=PALE_BLUE)
    label(pdf, "ASSET AND PROVENANCE BOUNDARY", 23 * mm, y - 10 * mm)
    draw_wrapped(pdf, "장비 등급이 달라도 같은 종류의 투명 장비 외형은 바꾸지 않는다. 강화 단계와 태그는 프레임·배지·텍스트·상태로 표현한다. 이 PDF는 새 raster asset, 새 UI screenshot, 새 촉매 아이콘을 만들거나 제품 asset으로 등록하지 않는다.", 23 * mm, y - 17 * mm, page_width - 46 * mm, size=8.8, leading=13.2, color=INK)


def status_row(pdf: canvas.Canvas, x: float, top: float, status: str, detail: str, *, fill: colors.Color) -> float:
    panel(pdf, x, top, 174 * mm, 15 * mm, fill=fill, radius=1.5 * mm)
    pdf.setFont("BlueprintMalgunBold", 8.2)
    pdf.setFillColor(INK)
    pdf.drawString(x + 4 * mm, top - 8 * mm, status)
    draw_wrapped(pdf, detail, x + 48 * mm, top - 5.5 * mm, 120 * mm, size=7.8, leading=10.5, color=MUTED)
    return top - 18 * mm


def page_five(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 5, "검토·증거 경계")
    y = heading(pdf, "이 PDF가 증명하는 것과 증명하지 않는 것", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "PDF 파일 자체의 구조와 글자·페이지 레이아웃은 기계적으로 검증한다. 게임의 Android 가독성, 접근성, 플레이 재미는 이 PDF만으로 통과가 아니다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.2, leading=14, color=MUTED)
    y -= 6 * mm
    x = 18 * mm
    y = status_row(pdf, x, y, "PDF 계약", "5쪽 A4, 제목·정본 비대체 표기·핵심 텍스트·영수증 SHA-256을 검사한다.", fill=PALE_GREEN)
    y = status_row(pdf, x, y, "PDF 렌더", "모든 페이지를 PNG로 렌더해 글자 잘림·겹침·여백을 시각 점검한다.", fill=PALE_GREEN)
    y = status_row(pdf, x, y, "기존 Phase 1", "원래 블루프린트 계약과 시각 보드 계약은 별도의 기계 검증 상태를 유지한다.", fill=PALE_BLUE)
    y = status_row(pdf, x, y, "Godot·Android", "NOT RUN - 이 문서는 게임 런타임, 기기 안전 여백, 터치, 성능을 검증하지 않는다.", fill=PALE_GOLD)
    y = status_row(pdf, x, y, "사람 플레이", "NOT RUN - STOP OR PUSH의 재미, 촉매 텍스트 판독성, 최종 UX 수용은 사용자/플레이테스트가 필요하다.", fill=PALE_GOLD)
    panel(pdf, 18 * mm, y - 4 * mm, page_width - 36 * mm, 42 * mm, fill=PALE_COPPER)
    label(pdf, "NEXT HUMAN CHECKPOINT", 23 * mm, y - 11 * mm)
    heading(pdf, "사용자 블루프린트 검토 대기", 23 * mm, y - 19 * mm, size=12.2)
    draw_wrapped(pdf, "확인할 항목: (1) 공방 화면의 읽기 순서, (2) 정밀강화가 +10 단위 태그 행동으로 보이는지, (3) 불의 심장·대지의 결정이 계보가 아닌 소모 자원으로 이해되는지, (4) 같은 UID의 결과 귀환 흐름이 자연스러운지.", 23 * mm, y - 27 * mm, page_width - 46 * mm, size=8.1, leading=11.2, color=INK)


def draw_pdf() -> str:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4, invariant=1)
    pdf.setTitle(TITLE)
    pdf.setAuthor("Blacksmith Project")
    pdf.setSubject("Derived non-canonical Blueprint Viewer")
    pdf.setCreator("Blacksmith deterministic ReportLab publisher")
    for page in (page_one, page_two, page_three, page_four, page_five):
        page(pdf)
        pdf.showPage()
    pdf.save()
    return sha256(OUTPUT)


def write_receipt(*, render_status: str, rendered_pages: list[int], visual_review: str) -> None:
    reader = PdfReader(str(OUTPUT))
    source_documents = [
        {
            "path": source.relative_to(ROOT).as_posix(),
            "sha256": normalized_sha256(source),
            "hash_basis": "UTF-8_BYTES_WITH_CRLF_TO_LF_NORMALIZATION",
        }
        for source in SOURCES
    ]
    receipt = {
        "schema_version": 1,
        "receipt_id": "BLACKSMITH_PHASE1_WORKSHOP_BLUEPRINT_PDF_20260902",
        "artifact_class": "DERIVED_NONCANONICAL_REVIEW_PDF",
        "status": render_status,
        "user_review_status": "USER_BLUEPRINT_REVIEW_PENDING",
        "runtime_asset": False,
        "artifact": {
            "path": OUTPUT.relative_to(ROOT).as_posix(),
            "sha256": sha256(OUTPUT),
            "page_count": len(reader.pages),
            "pdf_title": reader.metadata.title,
            "pdf_subject": reader.metadata.subject,
            "target_format": "A4",
        },
        "source_documents": source_documents,
        "publisher": {
            "path": "tools/publish_phase1_workshop_blueprint_pdf.py",
            "engine": "ReportLab",
            "fonts": ["C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"],
            "invariant_pdf": True,
            "contains_generated_raster_asset": False,
            "contains_product_runtime_screenshot": False,
        },
        "render_validation": {
            "required_tool": "pdftoppm",
            "status": render_status,
            "rendered_pages": rendered_pages,
            "visual_review": visual_review,
        },
        "evidence_ceiling": {
            "pdf_structure_and_text": "MACHINE_VERIFIED_AFTER_CONTRACT_RUN",
            "pdf_visual_layout": "AGENT_VISUAL_REVIEW_AFTER_RENDER" if rendered_pages else "NOT_RUN",
            "godot_runtime": "NOT_RUN_BY_THIS_DERIVED_DOCUMENT",
            "android_device": "NOT_RUN",
            "accessibility": "NOT_RUN",
            "human_player_experience": "NOT_RUN",
            "user_blueprint_review": "PENDING",
        },
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> None:
    first_sha = draw_pdf()
    second_sha = draw_pdf()
    if first_sha != second_sha:
        raise RuntimeError("invariant PDF generation produced different bytes")
    reader = PdfReader(str(OUTPUT))
    if len(reader.pages) != 5:
        raise RuntimeError(f"expected five pages, found {len(reader.pages)}")
    if reader.metadata.title != TITLE:
        raise RuntimeError("PDF metadata title mismatch")
    write_receipt(
        render_status="GENERATED_PENDING_RENDER_INSPECTION",
        rendered_pages=[],
        visual_review="NOT_RUN",
    )
    print(f"published {OUTPUT.relative_to(ROOT)} sha256={second_sha} pages={len(reader.pages)}")


def finalize_render_review() -> None:
    if not OUTPUT.exists():
        raise FileNotFoundError(OUTPUT)
    reader = PdfReader(str(OUTPUT))
    if len(reader.pages) != 5:
        raise RuntimeError(f"expected five pages, found {len(reader.pages)}")
    write_receipt(
        render_status="RENDERED_AND_AGENT_VISUAL_LAYOUT_REVIEWED",
        rendered_pages=list(range(1, len(reader.pages) + 1)),
        visual_review="ALL_FIVE_PAGES_RENDERED_AND_VISUALLY_REVIEWED_FOR_CLIPPING_OVERLAP_AND_LEGIBILITY",
    )
    print(f"recorded render review for {OUTPUT.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finalize-render-review", action="store_true")
    args = parser.parse_args()
    if args.finalize_render_review:
        finalize_render_review()
    else:
        build()


if __name__ == "__main__":
    main()
