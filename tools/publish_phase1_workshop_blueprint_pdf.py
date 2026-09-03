#!/usr/bin/env python3
"""Publish a deterministic, non-canonical Phase 1 Workshop Blueprint Viewer PDF."""
from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
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
    ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md",
    ROOT / "docs/operations/receipts/2026-09-01-phase1-workshop-blueprint.json",
    ROOT / "assets/ASSET_MANIFEST.json",
    ROOT / "docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json",
    ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md",
    ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md",
    ROOT / "docs/decisions/BS-ENHANCE-20260830-38_RECURRING_PRECISION_TAG_EVOLUTION.md",
    ROOT / "docs/decisions/BS-ENHANCE-20260901-40_CONSUMABLE_PRECISION_CATALYST_RESOURCES.md",
)
PAGE_COUNT = 14
PAGE_SECTIONS = (
    "읽기 안내",
    "전체 흐름",
    "공방 공통 셸",
    "정본·상태 경계",
    "검토 경계",
    "일반 강화",
    "최초 +10",
    "+20 이후",
    "손상·수리",
    "고객 실제 사용·연대기",
    "검증과 증거 한계",
    "통합 실행 체크리스트",
    "목표별 점검",
    "대표 케이스 점검",
)
RUNTIME_ASSET_REFERENCE_PAGES = (1, 3, 9, 10, 11)
RUNTIME_ASSET_REFERENCES = (
    {
        "asset_id": "ASSET-ANVIL-OATH-LOGO-AO02-V1",
        "path": "assets/ui/identity/anvil_oath_logo_ao02_v1.png",
        "pdf_reference_max_pixels": 768,
        "actual_consumer": "MAIN_MENU / MenuLayout/MenuTitleLogo",
        "runtime_asset_role": "Localized title-logo TextureRect with native-label fallback",
    },
    {
        "asset_id": "ASSET-WORKSHOP-BACKGROUND-V2",
        "path": "assets/ui/workshop/workshop_enhancement_background_v2.png",
        "pdf_reference_max_pixels": 768,
        "actual_consumer": "WORKSHOP / WorkshopIllustratedBackground",
        "runtime_asset_role": "Portrait illustrated workshop backdrop behind native controls",
    },
    {
        "asset_id": "ASSET-WORKPIECE-DURABILITY-STATE-ATLAS-V1",
        "path": "assets/ui/workshop/workpiece_durability_state_atlas_v1.png",
        "pdf_reference_max_pixels": 512,
        "actual_consumer": "WORKSHOP / WorkpieceDurabilityHero",
        "runtime_asset_role": "Derived durability-state atlas; native CURRENT/MAX/BASE_MAX remains authoritative",
    },
    {
        "asset_id": "ASSET-CUSTOMER-RESULT-RETURN-ILLUSTRATION-V1",
        "path": "assets/ui/workshop/customer_result_return_illustration_v1.png",
        "pdf_reference_max_pixels": 256,
        "actual_consumer": "CUSTOMER_WORLD_RESULT / CustomerResultEventIllustration",
        "runtime_asset_role": "Valid-saved-result illustration behind native factual result text",
    },
    {
        "asset_id": "ASSET-EQUIPMENT-IRON-SWORD-CARD-V2",
        "path": "assets/ui/equipment/iron_sword_card_v2.png",
        "pdf_reference_max_pixels": 256,
        "actual_consumer": "FIRST_FORGE_AND_WORKSHOP / EquipmentIdentityHero",
        "runtime_asset_role": "Transparent equipment identity illustration",
    },
    {
        "asset_id": "ASSET-EQUIPMENT-IRON-SHIELD-CARD-V2",
        "path": "assets/ui/equipment/iron_shield_card_v2.png",
        "pdf_reference_max_pixels": 256,
        "actual_consumer": "FIRST_FORGE_AND_WORKSHOP / EquipmentIdentityHero",
        "runtime_asset_role": "Transparent equipment identity illustration",
    },
    {
        "asset_id": "ASSET-EQUIPMENT-IRON-BOW-CARD-V2",
        "path": "assets/ui/equipment/iron_bow_card_v2.png",
        "pdf_reference_max_pixels": 256,
        "actual_consumer": "FIRST_FORGE_AND_WORKSHOP / EquipmentIdentityHero",
        "runtime_asset_role": "Transparent equipment identity illustration",
    },
    {
        "asset_id": "ASSET-EQUIPMENT-IRON-ARMOR-CARD-V2",
        "path": "assets/ui/equipment/iron_armor_card_v2.png",
        "pdf_reference_max_pixels": 256,
        "actual_consumer": "FIRST_FORGE_AND_WORKSHOP / EquipmentIdentityHero",
        "runtime_asset_role": "Transparent equipment identity illustration",
    },
    {
        "asset_id": "ASSET-EQUIPMENT-IRON-HELMET-CARD-V2",
        "path": "assets/ui/equipment/iron_helmet_card_v2.png",
        "pdf_reference_max_pixels": 256,
        "actual_consumer": "FIRST_FORGE_AND_WORKSHOP / EquipmentIdentityHero",
        "runtime_asset_role": "Transparent equipment identity illustration",
    },
)
ASSET_REFERENCE_BY_ID = {reference["asset_id"]: reference for reference in RUNTIME_ASSET_REFERENCES}

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


def runtime_asset_path(asset_id: str) -> Path:
    """Resolve only a declared existing runtime asset reference."""
    return ROOT / ASSET_REFERENCE_BY_ID[asset_id]["path"]


@lru_cache(maxsize=None)
def runtime_asset_image_reader(asset_id: str) -> ImageReader:
    """Create an in-memory PDF derivative without mutating the source PNG."""
    reference = ASSET_REFERENCE_BY_ID[asset_id]
    asset_path = runtime_asset_path(asset_id)
    if not asset_path.is_file():
        raise FileNotFoundError(asset_path)
    with Image.open(asset_path) as source_image:
        pdf_image = source_image.convert("RGBA")
    max_pixels = reference["pdf_reference_max_pixels"]
    pdf_image.thumbnail((max_pixels, max_pixels), Image.Resampling.LANCZOS)
    return ImageReader(pdf_image)


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
    alpha: float = 1.0,
) -> None:
    pdf.saveState()
    pdf.setFillAlpha(alpha)
    pdf.setStrokeAlpha(alpha)
    pdf.setFillColor(fill)
    pdf.setStrokeColor(stroke)
    pdf.setLineWidth(0.7)
    pdf.roundRect(x, top - height, width, height, radius, fill=1, stroke=1)
    pdf.restoreState()


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


def runtime_asset_thumbnail(
    pdf: canvas.Canvas,
    asset_id: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    """Place a source PNG as a reference, never as a new product asset."""
    pdf.drawImage(
        runtime_asset_image_reader(asset_id),
        x,
        y,
        width,
        height,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )


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
    pdf.drawRightString(page_width - 14 * mm, 9 * mm, f"{page} / {PAGE_COUNT} · 2026-09-03")


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
    logo_x = 109 * mm
    label(pdf, "IMPLEMENTED TITLE ASSET · MAIN MENU", logo_x, page_height - 28 * mm)
    runtime_asset_thumbnail(
        pdf,
        "ASSET-ANVIL-OATH-LOGO-AO02-V1",
        logo_x,
        page_height - 72 * mm,
        80 * mm,
        39 * mm,
    )
    y = draw_wrapped(
        pdf,
        "한 작품의 강화 판단이 고객의 실제 사용 결과와 연대기로 이어지는 세로형 공방 흐름을 읽기 위한 파생 PDF입니다.",
        18 * mm,
        y - 5 * mm,
        80 * mm,
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
    runtime_asset_thumbnail(
        pdf,
        "ASSET-WORKSHOP-BACKGROUND-V2",
        phone_x + 4 * mm,
        phone_top - phone_height + 4 * mm,
        phone_width - 8 * mm,
        phone_height - 12 * mm,
    )
    pdf.setFillColor(INK)
    pdf.roundRect(phone_x + 42 * mm, phone_top - 5 * mm, 18 * mm, 2 * mm, 1 * mm, fill=1, stroke=0)
    screen_x = phone_x + 7 * mm
    screen_width = phone_width - 14 * mm
    panel(pdf, screen_x, phone_top - 10 * mm, screen_width, 21 * mm, fill=PALE_GOLD, alpha=0.93)
    label(pdf, "WORKSHOP", screen_x + 4 * mm, phone_top - 16 * mm)
    pdf.setFont("BlueprintMalgunBold", 11)
    pdf.setFillColor(INK)
    pdf.drawString(screen_x + 4 * mm, phone_top - 22 * mm, "모루의 서약 · 공방")
    panel(pdf, screen_x, phone_top - 36 * mm, screen_width, 43 * mm, fill=PARCHMENT, alpha=0.93)
    label(pdf, "현재 작품 · SAME UID", screen_x + 4 * mm, phone_top - 42 * mm)
    label(pdf, "ASSET REF · IRON SWORD V2", screen_x + 57 * mm, phone_top - 42 * mm, color=MUTED)
    pdf.setFont("BlueprintMalgunBold", 12.5)
    pdf.setFillColor(INK)
    pdf.drawString(screen_x + 4 * mm, phone_top - 50 * mm, "철검 · +19 · 예리함 II")
    draw_wrapped(pdf, "현재 4 / 최대 5 / 출생 5\n상태: 경미 손상", screen_x + 4 * mm, phone_top - 59 * mm, screen_width - 35 * mm, size=8.4, leading=12, color=MUTED)
    runtime_asset_thumbnail(
        pdf,
        "ASSET-EQUIPMENT-IRON-SWORD-CARD-V2",
        screen_x + 57 * mm,
        phone_top - 77 * mm,
        24 * mm,
        29 * mm,
    )
    panel(pdf, screen_x, phone_top - 85 * mm, screen_width, 51 * mm, fill=PALE_COPPER, alpha=0.93)
    label(pdf, "NEXT DECISION", screen_x + 4 * mm, phone_top - 91 * mm)
    pdf.setFont("BlueprintMalgunBold", 12)
    pdf.setFillColor(INK)
    pdf.drawString(screen_x + 4 * mm, phone_top - 99 * mm, "정밀강화 +20")
    draw_wrapped(pdf, "태그 행동: [태그 추가] [태그 강화]\n성공 · 실패 유지 · 조건부 손상\n성공 시: 레벨 +1과 선택한 태그 성장", screen_x + 4 * mm, phone_top - 109 * mm, screen_width - 8 * mm, size=8.2, leading=11.7, color=INK)
    panel(pdf, screen_x, phone_top - 142 * mm, screen_width, 37 * mm, fill=PALE_BLUE, alpha=0.93)
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
    y = status_row(pdf, x, y, "PDF 계약", f"{PAGE_COUNT}쪽 A4, 제목·정본 비대체 표기·핵심 텍스트·영수증 SHA-256을 검사한다.", fill=PALE_GREEN)
    y = status_row(pdf, x, y, "PDF 렌더", "모든 페이지를 PNG로 렌더해 글자 잘림·겹침·여백을 시각 점검한다.", fill=PALE_GREEN)
    y = status_row(pdf, x, y, "기존 Phase 1", "원래 블루프린트 계약과 시각 보드 계약은 별도의 기계 검증 상태를 유지한다.", fill=PALE_BLUE)
    y = status_row(pdf, x, y, "Godot·Android", "NOT RUN - 이 문서는 게임 런타임, 기기 안전 여백, 터치, 성능을 검증하지 않는다.", fill=PALE_GOLD)
    y = status_row(pdf, x, y, "사람 플레이", "NOT RUN - STOP OR PUSH의 재미, 촉매 텍스트 판독성, 최종 UX 수용은 사용자/플레이테스트가 필요하다.", fill=PALE_GOLD)
    panel(pdf, 18 * mm, y - 4 * mm, page_width - 36 * mm, 42 * mm, fill=PALE_COPPER)
    label(pdf, "NEXT HUMAN CHECKPOINT", 23 * mm, y - 11 * mm)
    heading(pdf, "사용자 블루프린트 검토 대기", 23 * mm, y - 19 * mm, size=12.2)
    draw_wrapped(pdf, "확인할 항목: (1) 공방 화면의 읽기 순서, (2) 정밀강화가 +10 단위 태그 행동으로 보이는지, (3) 불의 심장·대지의 결정이 계보가 아닌 소모 자원으로 이해되는지, (4) 같은 UID의 결과 귀환 흐름이 자연스러운지.", 23 * mm, y - 27 * mm, page_width - 46 * mm, size=8.1, leading=11.2, color=INK)


def compact_card(
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
    """A denser explanatory card for the detailed implementation pages."""
    panel(pdf, x, top, width, height, fill=fill)
    label(pdf, kicker, x + 4 * mm, top - 5.5 * mm)
    title_bottom = heading(pdf, title_text, x + 4 * mm, top - 10.5 * mm, size=10.0)
    draw_wrapped(pdf, body, x + 4 * mm, title_bottom - 1 * mm, width - 8 * mm, size=7.75, leading=10.9, color=MUTED)


def page_six(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 6, "일반 강화")
    y = heading(pdf, "일반 강화와 +5 제작 리듬", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "일반 강화는 매번 현재 레벨 + 1을 목표로 삼는다. 화면은 확률을 새로 만들지 않고 resolver가 준 다음 시도의 비용·결과를 순서대로 읽게 한다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.2, leading=14, color=MUTED)
    column_width = (page_width - 42 * mm) / 2
    left = 18 * mm
    right = left + column_width + 6 * mm
    top = y - 6 * mm
    compact_card(pdf, left, top, column_width, 48 * mm, "READ ORDER 01", "같은 UID 작품을 먼저 고정", "장비 그림, 작품명, 현재 +레벨, 활성 태그, CURRENT / MAX / BASE_MAX를 항상 상단에 둔다. 등급이 바뀌어도 같은 장비 종류의 외형은 유지하고, 강화 단계와 태그는 배지·텍스트·테두리 상태로 읽는다.", fill=PALE_GOLD)
    compact_card(pdf, right, top, column_width, 48 * mm, "READ ORDER 02", "다음 target과 실제 비용", "일반 target은 Gold·보강재를, +10 단위 정밀 target은 선택한 촉매까지 비용 상단에 표시한다. 현재 +19의 다음 target은 +20이므로 정밀 패널로 이어진다. 이 화면은 수식·경제 수치를 재계산하지 않고 resolver의 현재 결과를 표시하는 consumer다.", fill=PALE_BLUE)
    top -= 54 * mm
    compact_card(pdf, left, top, column_width, 58 * mm, "RESULT MAP", "성공과 두 종류의 실패", "일반 성공은 항상 SUCCESS_LEVEL_DELTA = +1이다. 실패는 FAILED_HOLD 또는 FAILED_DAMAGE 하나로만 해결된다. 단계 하락, 별도의 CRITICAL, 강제 파괴 연출은 만들지 않는다. 손상 가능성은 target 10 이하에서 0이며, 11 이상에서만 조건부로 열릴 수 있다.", fill=PAPER)
    compact_card(pdf, right, top, column_width, 58 * mm, "STOP OR PUSH", "한 번의 주 CTA, 두 개의 합법적 선택", "CTA는 ‘강화 시도’ 하나만 둔다. 플레이어는 지금의 작품을 보존하기 위해 돌아가거나, 표시된 성공·유지·손상 최종 시도 확률을 보고 시도한다. 일반 강화 로그를 연대기로 자동 기록하지 않아, 핵심 판단의 밀도를 흐리지 않는다.", fill=PALE_COPPER)
    top -= 64 * mm
    compact_card(pdf, left, top, column_width, 47 * mm, "+5 PRESENTATION", "+5 제작 리듬은 별도 시스템이 아니다", "+5는 ‘지금까지의 성취’를 잠깐 강조하는 presentation beat다. +5에서 새 정밀 규칙, 새 태그, 새 촉매 소비, 새 실패 규칙을 열지 않는다. 실제 정밀강화는 +10 단위가 유일한 cadence다.", fill=PALE_GREEN)
    compact_card(pdf, right, top, column_width, 47 * mm, "BLOCKED STATES", "보유량 부족은 굴림 전에 차단", "재료가 부족하거나 아이템 상태가 유효하지 않다면 비용 소비와 확률 굴림 전에 버튼을 비활성화하고 이유·필요 수량·되돌아갈 선택을 표시한다. 실패 메시지로 부족을 숨기거나 반쯤 소비하는 경로는 없다.", fill=PALE_GOLD)
    top -= 53 * mm
    panel(pdf, 18 * mm, top, page_width - 36 * mm, 31 * mm, fill=PALE_COPPER)
    label(pdf, "WORKSHOP RETURN", 23 * mm, top - 6 * mm)
    draw_wrapped(pdf, "해결 뒤에는 같은 공방으로 돌아온다. SUCCESS는 갱신된 +레벨과 태그 상태를, FAILED_HOLD는 보존된 작품을, 손상 실패는 갱신된 내구도와 조건부 수리 job을 보인다. 이 귀환이 ‘다음 행동’을 재설명하지 않고 곧바로 읽히게 한다.", 23 * mm, top - 12 * mm, page_width - 46 * mm, size=8.15, leading=11.4, color=INK)


def page_seven(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 7, "최초 +10")
    y = heading(pdf, "정밀강화: 최초 +10은 태그 추가만", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "+9 → +10은 반복되는 정밀 단위의 첫 관문이지만, 첫 관문에서는 기존 태그를 강화할 수 없다. 무기 타입만 태그 패널을 열며, 선택이 없으면 비용·굴림 이전에 멈춘다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.2, leading=14, color=MUTED)
    left = 18 * mm
    full_width = page_width - 36 * mm
    top = y - 6 * mm
    compact_card(pdf, left, top, full_width, 37 * mm, "ENTRY GATE", "누가 최초 +10 태그 선택을 보는가", "검·방패·활만 정밀 태그 UI의 recipient다. 갑옷·투구는 같은 강화 흐름을 사용하되 weapon item keyword를 받지 않는다. 첫 +10에서 선택 가능한 action은 [태그 추가] 하나다. [태그 강화]는 기존 태그가 있어도 이 최초 관문에서는 숨긴다.", fill=PALE_GOLD)
    top -= 43 * mm
    column_width = (page_width - 42 * mm) / 2
    right = left + column_width + 6 * mm
    compact_card(pdf, left, top, column_width, 63 * mm, "STEP 01", "태그와 방식의 의미를 먼저 읽는다", "태그 추가는 두 방법을 text-native 카드로 제시한다. 날 세우기와 경량 담금은 선택 결과를 미리 설명하며, 각각 불의 심장 또는 대지의 결정이라는 촉매 비용을 보인다. 촉매는 계보·진영·영구 클래스가 아니라 한 번의 시도에 소모되는 자원이다.", fill=PALE_COPPER)
    compact_card(pdf, right, top, column_width, 63 * mm, "STEP 02", "2×2 선택은 무작위가 아니다", "선택 표: 불의 심장 × 날 세우기, 불의 심장 × 경량 담금, 대지의 결정 × 날 세우기, 대지의 결정 × 경량 담금. 선택 카드는 예상 태그 효과, Gold·보강재·촉매 1개, 보유량을 함께 보인다. default 촉매·random 태그·reroll은 없다.", fill=PALE_BLUE)
    top -= 69 * mm
    compact_card(pdf, left, top, column_width, 58 * mm, "PRECHECK", "사전 조건 차단은 친절한 실패가 아니다", "태그 행동을 선택하지 않았거나 요구 Gold·보강재·촉매가 부족하면 [정밀강화 시도]를 누를 수 없다. 패널은 ‘선택 필요’ 또는 ‘불의 심장 1개 부족’처럼 부족 이유를 명시한다. 이 상태에서는 비용도, 로그도, 확률 판정도 발생하지 않는다.", fill=PALE_GREEN)
    compact_card(pdf, right, top, column_width, 58 * mm, "ATOMIC RESOLUTION", "선택한 비용과 결과는 한 단위", "유효한 선택과 보유량이 확인된 뒤에만 필요한 자원을 한 번에 소비하고 시도를 해결한다. 성공은 +10과 선택 태그 I을 함께 반영한다. 실패는 FAILED_HOLD 또는 FAILED_DAMAGE로 끝나며, 누적 단계 하락이나 별도 네 번째 affix 슬롯은 없다.", fill=PAPER)
    top -= 64 * mm
    panel(pdf, 18 * mm, top, full_width, 36 * mm, fill=PALE_GOLD)
    label(pdf, "RESULT RETURN", 23 * mm, top - 6 * mm)
    draw_wrapped(pdf, "성공·실패 모두 공방의 같은 UID 카드로 귀환한다. 성공 카드에는 ‘+10 / 태그 I / 소비된 촉매’를, 유지 실패에는 ‘작품 보존’을, 손상 실패에는 ‘현재 내구도 변화 / 수리 job 가능 여부’를 명시한다. 고객 인계는 이 정밀 결과의 다음 목적지이지 손상을 꾸미는 연출이 아니다.", 23 * mm, top - 12 * mm, full_width - 10 * mm, size=8.15, leading=11.4, color=INK)


def page_eight(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 8, "+20 이후")
    y = heading(pdf, "정밀강화: +20 이후는 추가 또는 강화", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "+20, +30 … +100은 같은 cadence를 반복한다. 이때 화면의 목적은 ‘어떤 태그를 얼마나 키울지’를 명확하게 고르게 하는 것이며, 촉매를 새로운 계보 선택처럼 분리하지 않는 것이다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.2, leading=14, color=MUTED)
    left = 18 * mm
    full_width = page_width - 36 * mm
    top = y - 6 * mm
    compact_card(pdf, left, top, full_width, 38 * mm, "ACTION DECISION", "+20 이후의 두 행동", "활성 태그가 3개 미만이면 [태그 추가]를 선택할 수 있다. 활성 태그가 하나 이상이면 [태그 강화]를 선택할 수 있다. 화면은 action을 먼저 고르게 하고, 그 뒤에 선택 가능한 태그·예상 단계·필요 촉매를 보여 준다. 아무 행동도 선택하지 않으면 정밀 시도는 차단된다.", fill=PALE_GOLD)
    top -= 44 * mm
    column_width = (page_width - 42 * mm) / 2
    right = left + column_width + 6 * mm
    compact_card(pdf, left, top, column_width, 68 * mm, "ADD PATH", "태그 추가: 빈 슬롯을 작품의 성격으로", "태그 추가는 아직 비어 있는 태그 슬롯을 한 개만 채운다. 추가 직전 카드에는 현재 태그 수 0~2 / 최대 3, 선택 결과, 촉매 종류·보유량, 시도 후 예상 표기를 같이 둔다. 세 번째 태그가 이미 있다면 추가 action은 설명 가능한 비활성 상태가 된다.", fill=PALE_COPPER)
    compact_card(pdf, right, top, column_width, 68 * mm, "UPGRADE PATH", "태그 강화: 기존 태그 하나만 성장", "태그 강화는 활성 태그 중 하나를 명시적으로 고른다. resolver가 선택 태그에 대응하는 필요 촉매를 자동 결정해 표시한다. 성공하면 고른 태그만 I → II → III → IV로 한 단계 성장하며, 다른 태그·기존 강화 레벨·태그 총수는 줄지 않는다.", fill=PALE_BLUE)
    top -= 74 * mm
    compact_card(pdf, left, top, column_width, 53 * mm, "CARD CONTENT", "작은 카드가 반드시 담을 것", "태그 이름·현재 단계, 예상 다음 단계, 선택 action, 소비 Gold·보강재·촉매, 보유량, 성공·유지·손상 결과를 한 카드 안에서 이어서 읽게 한다. 촉매의 현재 보유량은 선택을 바꾸는 자원 정보이지 장비의 영구 속성이 아니다.", fill=PAPER)
    compact_card(pdf, right, top, column_width, 53 * mm, "HARD BOUNDARY", "금지되는 지름길", "무작위로 태그를 주지 않는다. 없는 촉매를 자동 대체하지 않는다. 선택을 초기화하는 reroll을 만들지 않는다. 네 번째 affix 슬롯을 만들지 않는다. 같은 태그를 한 시도에 두 단계 강화하지 않는다. 이 경계는 결과의 예측 가능성을 지킨다.", fill=PALE_GREEN)
    top -= 59 * mm
    panel(pdf, 18 * mm, top, full_width, 39 * mm, fill=PALE_COPPER)
    label(pdf, "RECURRING CADENCE", 23 * mm, top - 6 * mm)
    draw_wrapped(pdf, "정밀 target은 [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]이다. +10 단위가 아닌 일반 목표에서는 이 패널을 띄우지 않는다. +5는 연출 전용이다. 따라서 플레이어는 ‘매 10단위에 한 번, 태그의 방향 또는 깊이를 고른다’는 규칙을 반복해서 학습한다.", 23 * mm, top - 12 * mm, full_width - 10 * mm, size=8.15, leading=11.4, color=INK)


def page_nine(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 9, "손상·수리")
    y = heading(pdf, "손상·내구도·수리 판단은 숫자 하나의 축", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "내구도 화면은 CURRENT / MAX / BASE_MAX를 유일한 gameplay authority로 읽는다. Current 손상과 Max 흉터를 별도 패널티로 중첩하지 않고, 더 나쁜 비율 하나가 player-facing effective state를 정한다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.2, leading=14, color=MUTED)
    left = 18 * mm
    full_width = page_width - 36 * mm
    top = y - 6 * mm
    panel(pdf, left, top, full_width, 53 * mm, fill=PALE_GOLD)
    label(pdf, "VISIBLE AUTHORITY · RUNTIME ASSET REFERENCE", left + 4 * mm, top - 5.5 * mm)
    title_bottom = heading(pdf, "CURRENT / MAX / BASE_MAX와 상태 예시", left + 4 * mm, top - 10.5 * mm, size=10.0)
    draw_wrapped(pdf, "5 / 5 / 5 = 정상, 4 / 5 / 5 = 경미, 2 / 5 / 5 = 심각, 4 / 4 / 5 = 경미, 2 / 2 / 5 = 심각, 0 / 5 / 5 = 파괴다. CURRENT는 현재 회복 가능한 양, MAX는 구조 흉터 이후의 상한, BASE_MAX는 출생 상한이다.", left + 4 * mm, title_bottom - 1 * mm, 102 * mm, size=7.75, leading=10.9, color=MUTED)
    runtime_asset_thumbnail(
        pdf,
        "ASSET-WORKPIECE-DURABILITY-STATE-ATLAS-V1",
        left + full_width - 58 * mm,
        top - 48 * mm,
        52 * mm,
        42 * mm,
    )
    label(pdf, "ATLAS · NATIVE NUMBERS REMAIN AUTHORITY", left + full_width - 62 * mm, top - 51 * mm, color=MUTED)
    top -= 59 * mm
    column_width = (page_width - 42 * mm) / 2
    right = left + column_width + 6 * mm
    compact_card(pdf, left, top, column_width, 61 * mm, "DAMAGE DISPLAY", "손상 확률은 실패에 조건부", "target 10 이하의 강화 손상은 0이다. target 11 이상에서 base damage curve와 effective state multiplier를 결합한다. 화면은 정확한 내부 계산을 바꾸지 않고 ‘성공 / FAILED_HOLD /\nFAILED_DAMAGE’의 최종 시도 확률을 소수 첫째 자리로 표시한다.", fill=PALE_BLUE)
    compact_card(pdf, right, top, column_width, 61 * mm, "FAILURE RESOLUTION", "한 번의 실패는 한 결과", "성공이 아니면 FAILED_HOLD 또는\nFAILED_DAMAGE 중 하나다. FAILED_HOLD는 레벨과 내구도를 보존한다. FAILED_DAMAGE는 실제 CURRENT를 낮추고, 조건이 맞으면 수리 job을 연다. 단계 하락, 추가 critical 판정, 한 이벤트에 두 번 손상시키기는 금지한다.", fill=PALE_COPPER)
    top -= 67 * mm
    compact_card(pdf, left, top, column_width, 52 * mm, "REPAIR ELIGIBILITY", "수리 job은 실제 손상 뒤에만", "수리는 0 < CURRENT < MAX 이고 repair job이 있을 때만 시작할 수 있다. 수리 시작 시 job은 소비된다. 파괴된 작품의 수리, 이미 CURRENT = MAX인 작품의 수리, MAX 내구도의 완전 복원은 이 Phase 1 범위에 없다.", fill=PALE_GREEN)
    compact_card(pdf, right, top, column_width, 52 * mm, "TEMP TEST BUDGET", "수리 품질과 MAX 흉터는 확정 경제가 아니다", "Excellent 20% / Standard 60% / Poor 20%와 구간별 MAX -1 scar 확률은 테스트 예산이다. 화면은 quality 결과와 post-scar MAX를 보이게 준비하되, 이 숫자를 최종 밸런스나 출시 약속으로 표시하지 않는다.", fill=PAPER)
    top -= 58 * mm
    panel(pdf, 18 * mm, top, full_width, 36 * mm, fill=PALE_COPPER)
    label(pdf, "DECISION AFTER DAMAGE", 23 * mm, top - 6 * mm)
    draw_wrapped(pdf, "심각 상태에서도 강화는 가능하지만 success -7pp, 새 효과 ×0.75, damage risk ×1.75라는 임시 테스트 modifier를 동반한다. 플레이어에게는 ‘지금 수리할지 / 손상된 작품으로 한 번 더 밀지’라는 선택만 남기고, 손상 경고가 강화 화면의 주제를 빼앗지 않도록 보조 정보로 배치한다.", 23 * mm, top - 12 * mm, full_width - 10 * mm, size=8.15, leading=11.4, color=INK)


def page_ten(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 10, "고객 실제 사용·연대기")
    y = heading(pdf, "고객 실제 사용의 귀환과 작품 연대기", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "공방 밖으로 나간 장비는 같은 UID로 돌아온다. 고객에게 건네는 행위와 실제 사용 결과를 분리해, ‘손상을 위한 연출’이 아니라 작품의 다음 목적을 보여 준다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.2, leading=14, color=MUTED)
    left = 18 * mm
    full_width = page_width - 36 * mm
    top = y - 6 * mm
    compact_card(pdf, left, top, full_width, 39 * mm, "CAUSALITY", "인계 자체는 손상을 만들지 않는다", "고객 인계 또는 구매만으로는 손상 이벤트가 발생하지 않는다. 실제 장비 사용이 있어야 하며, UID 당 이벤트 한 번에 최대 한 번만 손상 판정을 한다. 임무 결과와 장비 손상은 독립 축이다. 세계·고객 이벤트가 MAX를 직접 낮추지 않는다.", fill=PALE_GOLD)
    top -= 45 * mm
    column_width = (page_width - 42 * mm) / 2
    right = left + column_width + 6 * mm
    compact_card(pdf, left, top, column_width, 63 * mm, "HANDOFF CARD", "보내기 전: 목적과 작품을 함께 읽기", "공방의 인계 CTA는 현재 작품, 장비 종류, 강화·태그, 내구도, 고객이 실제로 사용할 맥락을 확인한다. 고객 관리형 반복 흐름을 추가하지 않는다. 이 단계에서 ‘인계가 손상시키지 않음’을 짧게 명시해 잘못된 공포를 만들지 않는다.", fill=PALE_BLUE)
    panel(pdf, right, top, column_width, 63 * mm, fill=PALE_COPPER)
    label(pdf, "RESULT RETURN · RUNTIME ASSET REFERENCE", right + 4 * mm, top - 5.5 * mm)
    runtime_asset_thumbnail(
        pdf,
        "ASSET-CUSTOMER-RESULT-RETURN-ILLUSTRATION-V1",
        right + 4 * mm,
        top - 58 * mm,
        27 * mm,
        47 * mm,
    )
    title_bottom = heading(pdf, "돌아온 뒤: 두 결과 축", right + 35 * mm, top - 12 * mm, size=8.8)
    draw_wrapped(pdf, "고객 실제 사용 후 결과 카드는 임무·세계 결과와 장비 상태를 분리해 보인다. 손상이 없으면 작품의 내구도를 보존한다. 손상이 있었다면 CURRENT 변화와 수리 job 가능 여부를 정확히 보인다. 그림이 없더라도 text-native 결과 패널은 동작해야 한다.", right + 35 * mm, title_bottom - 1 * mm, column_width - 39 * mm, size=6.9, leading=9.5, color=MUTED)
    top -= 69 * mm
    compact_card(pdf, left, top, column_width, 53 * mm, "CHRONICLE IN", "연대기에 남길 의미 사건", "제작, 태그 획득 또는 성장, 실제 손상, MAX 흉터 수리, 고객 인계, 세계 결과, 파괴는 작품 연대기의 후보다. 각 기록은 UID와 사건 종류·짧은 결과를 연결한다. 플레이어가 ‘이 장비가 왜 지금 이런 상태인지’를 거꾸로 읽을 수 있어야 한다.", fill=PALE_GREEN)
    compact_card(pdf, right, top, column_width, 53 * mm, "CHRONICLE OUT", "남기지 않을 반복", "일반 강화 성공·유지 실패를 매번 연대기에 적지 않는다. 반복 강화 기록은 player chronicle이 아니다. 고객 결과가 아직 없는데 미래 사건을 미리 쓰지 않는다. 설명을 위해 가짜 손상·가짜 고객 결과·가짜 스크린샷을 제품 asset처럼 쓰지 않는다.", fill=PAPER)
    top -= 59 * mm
    panel(pdf, 18 * mm, top, full_width, 36 * mm, fill=PALE_COPPER)
    label(pdf, "RETURN DESTINATION", 23 * mm, top - 6 * mm)
    draw_wrapped(pdf, "결과를 읽은 뒤에는 같은 공방으로 돌아가며, 조건부 수리와 다음 강화·다음 인계 중 가능한 행동만 제시한다. 이 재진입은 새 인벤토리나 새 고객 관리 화면을 요구하지 않는다. ‘한 작품이 공방–세계–연대기 사이에서 지속된다’는 약속을 작은 화면 수로 완성한다.", 23 * mm, top - 12 * mm, full_width - 10 * mm, size=8.15, leading=11.4, color=INK)


def page_eleven(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 11, "구현 인계·검증과 증거 한계")
    y = heading(pdf, "구현 인계와 검증과 증거 한계", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "이 상세 PDF는 변경해야 할 화면의 순서와 owner 연결을 보이게 하지만, Markdown·JSON·코드·테스트 정본을 대체하지 않는다. 아래 연결은 Phase 1 구현 시작 전의 검토용 인계 지도다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.2, leading=14, color=MUTED)
    left = 18 * mm
    full_width = page_width - 36 * mm
    top = y - 6 * mm
    compact_card(pdf, left, top, full_width, 43 * mm, "구현 소유 경로", "UI는 표시하고 resolver·저장은 정본 규칙을 소유", "세로 공방 shell은 MarginContainer → ScrollContainer → VBoxContainer다. 정밀 패널은 scripts/vertical_slice/ui/\nvs_workshop_screen.gd, 재료·차단 CTA는 resolver, 수리와 내구도는 resolver·저장 owner, 고객 결과·연대기는 read-only consumer가 맡는다.\nContainer는 child 위치를 소유하므로 수동 배치로 교체하지 않는다.", fill=PALE_GOLD)
    top -= 49 * mm
    column_width = (page_width - 42 * mm) / 2
    right = left + column_width + 6 * mm
    panel(pdf, left, top, column_width, 64 * mm, fill=PALE_GREEN)
    label(pdf, "ASSET REUSE · RUNTIME ASSET REFERENCES", left + 4 * mm, top - 5.5 * mm)
    body_top = heading(pdf, "새 이미지 없이도 화면은 비지 않는다", left + 4 * mm, top - 10.5 * mm, size=10.0)
    draw_wrapped(pdf, "메뉴·첫 제작·공방에는 기존 승인 로고, 공방 배경·내구도 atlas·고객 결과 illustration, 투명 장비 5종을 실제 consumer에서만 재사용한다. 장비 등급별 새 외형, 정밀 전용 공방 배경, 촉매 전용 raster, 가짜 제품 스크린샷은 만들지 않는다.", left + 4 * mm, body_top - 1 * mm, column_width - 8 * mm, size=7.25, leading=9.9, color=MUTED)
    equipment_ids = (
        "ASSET-EQUIPMENT-IRON-SWORD-CARD-V2",
        "ASSET-EQUIPMENT-IRON-SHIELD-CARD-V2",
        "ASSET-EQUIPMENT-IRON-BOW-CARD-V2",
        "ASSET-EQUIPMENT-IRON-ARMOR-CARD-V2",
        "ASSET-EQUIPMENT-IRON-HELMET-CARD-V2",
    )
    for index, equipment_id in enumerate(equipment_ids):
        runtime_asset_thumbnail(
            pdf,
            equipment_id,
            left + (4 + index * 15.3) * mm,
            top - 61 * mm,
            13.4 * mm,
            17 * mm,
        )
    compact_card(pdf, right, top, column_width, 64 * mm, "IMPLEMENTATION UNITS", "작게 나누어 실제 화면으로 검증", "1) portrait shell, 2) same-UID item card, 3) normal enhancement, 4) precision add/upgrade precheck·atomic resolution, 5) damage/repair return, 6) customer result/chronicle readback 순서다. 각각은 RED 계약 테스트 → 최소 GREEN → refactor → exact-head 검증으로 연결한다.", fill=PALE_BLUE)
    top -= 70 * mm
    compact_card(pdf, left, top, column_width, 55 * mm, "WHAT THIS PDF PROVES", "문서 산출물의 기계·시각 검증", f"PDF는 {PAGE_COUNT}쪽 A4, 핵심 텍스트, metadata, SHA-256 영수증, 입력 문서 해시, benchmark preflight와 hygiene record를 기계 검사한다. 모든 쪽은 PNG 렌더 후 글자 잘림·겹침·여백을 agent가 검토한다. 이 검증은 문서 레이아웃의 evidence ceiling을 넘지 않는다.", fill=PAPER)
    compact_card(pdf, right, top, column_width, 55 * mm, "NOT RUN", "런타임·기기·사람 판단은 별도 gate", "Godot runtime, Android safe area·touch, 접근성, 성능, 실제 플레이 재미, 사용자 UX 수용, 출시 승인은 이 문서만으로 PASS가 아니다. 이전 runtime capture는 역사 evidence이며, 이번 PDF 개정이 새 runtime proof나 자산 승격을 만들지 않는다.", fill=PALE_COPPER)
    top -= 61 * mm
    panel(pdf, 18 * mm, top, full_width, 37 * mm, fill=PALE_GOLD)
    label(pdf, "NEXT HUMAN CHECKPOINT", 23 * mm, top - 6 * mm)
    heading(pdf, "사용자 블루프린트 검토 대기", 23 * mm, top - 14 * mm, size=11.6)
    draw_wrapped(pdf, "확인 질문: 일반 강화의 읽기 순서가 명확한가? 최초 +10과 +20 이후의 행동 차이가 분명한가? 불의 심장·대지의 결정이 소모 자원으로 보이는가? 손상·수리·고객 실제 사용·연대기가 같은 UID로 자연스럽게 이어지는가? 이 네 가지는 실제 Godot 화면에서 최종 UX 검토가 필요하다.", 23 * mm, top - 22 * mm, full_width - 10 * mm, size=8.0, leading=11.2, color=INK)


def checklist_badge(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    top: float,
    *,
    fill: colors.Color,
) -> float:
    """Draw a text-labelled checklist status; color is never the sole signal."""
    pdf.setFont("BlueprintMalgunBold", 6.7)
    width = max(25 * mm, pdfmetrics.stringWidth(text, "BlueprintMalgunBold", 6.7) + 8 * mm)
    panel(pdf, x, top, width, 7.5 * mm, fill=fill, stroke=LINE, radius=1.5 * mm)
    pdf.setFillColor(INK)
    pdf.drawCentredString(x + width / 2, top - 5.1 * mm, text)
    return width


def checklist_row(
    pdf: canvas.Canvas,
    x: float,
    top: float,
    number: str,
    title_text: str,
    status: str,
    detail: str,
    *,
    fill: colors.Color,
    height_mm: float = 22.0,
) -> float:
    """Render one readable PM checklist row without relying on a raster mockup."""
    width = A4[0] - 36 * mm
    height = height_mm * mm
    panel(pdf, x, top, width, height, fill=fill, radius=2 * mm)
    checkbox_x = x + 5 * mm
    checkbox_y = top - 10.5 * mm
    pdf.setStrokeColor(COPPER)
    pdf.setLineWidth(1.0)
    pdf.rect(checkbox_x, checkbox_y, 4.3 * mm, 4.3 * mm, fill=0, stroke=1)
    pdf.setFont("BlueprintMalgunBold", 6.7)
    pdf.setFillColor(COPPER)
    pdf.drawCentredString(checkbox_x + 2.15 * mm, checkbox_y + 1.15 * mm, number)
    title_x = x + 12 * mm
    label(pdf, title_text, title_x, top - 6 * mm)
    badge_width = checklist_badge(pdf, status, title_x, top - 10 * mm, fill=PALE_GOLD)
    draw_wrapped(
        pdf,
        detail,
        title_x + badge_width + 3 * mm,
        top - 12.2 * mm,
        width - (title_x - x) - badge_width - 9 * mm,
        size=7.45,
        leading=9.9,
        color=MUTED,
    )
    return top - height - 4 * mm


def page_twelve(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 12, "통합 실행 체크리스트")
    y = heading(pdf, "통합 실행 체크리스트", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "블루프린트를 읽는 동안 목표·시스템·대표 케이스의 현재 증거를 같은 형식으로 확인한다. 이 페이지는 새 PM 도구나 제품 기능이 아니라, 이미 있는 정본과 검증 상태를 빠르게 읽는 보기다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.1, leading=13.6, color=MUTED)
    top = y - 6 * mm
    panel(pdf, 18 * mm, top, page_width - 36 * mm, 20 * mm, fill=PALE_COPPER)
    label(pdf, "DELIVERY BOUNDARY", 23 * mm, top - 6 * mm)
    heading(pdf, "PDF 내부 전용", 23 * mm, top - 13 * mm, size=10.8)
    draw_wrapped(pdf, "별도 HTML 대시보드를 만들지 않는다. 체크리스트는 이 Blueprint Viewer의 12~14쪽에만 통합하며, 제품 정본·게임 런타임·사용자 승인 상태를 대신하지 않는다.", 75 * mm, top - 7 * mm, page_width - 98 * mm, size=7.65, leading=10.5, color=INK)
    top -= 27 * mm
    card_width = (page_width - 42 * mm) / 2
    right = 18 * mm + card_width + 6 * mm
    compact_card(pdf, 18 * mm, top, card_width, 26 * mm, "STATUS 01", "정본 확정", "사용자 승인된 현재 규칙과 owner가 있다. 구현이나 사람 경험의 PASS를 뜻하지 않는다.", fill=PALE_GOLD)
    compact_card(pdf, right, top, card_width, 26 * mm, "STATUS 02", "구현·기계 검증", "코드·데이터·자동 계약의 현재 근거가 있다. 실제 사람이 잘 읽는지는 별도다.", fill=PALE_GREEN)
    top -= 32 * mm
    compact_card(pdf, 18 * mm, top, card_width, 26 * mm, "STATUS 03", "제한 런타임 UI 관찰", "+9→+10 촉매 선택·보유량·시도 준비만 실제 Godot 화면에서 관찰했다. 결제·저장은 누르지 않았다.", fill=PALE_BLUE)
    compact_card(pdf, right, top, card_width, 26 * mm, "STATUS 04", "NOT RUN", "Android, 접근성, 성능, 전체 플레이, 사람 UX 수용, 출시 판단은 아직 실행하지 않음이다.", fill=PALE_COPPER)
    top -= 38 * mm
    column_width = (page_width - 42 * mm) / 3
    flow_cards = (
        ("01 · GOAL", "목표를 확인", "STOP OR PUSH와 같은 UID 작품 생애가 현재 제품 약속인지 먼저 본다.", PALE_GOLD),
        ("02 · SYSTEM", "시스템을 확인", "강화·태그·촉매·손상·수리·고객 귀환의 owner와 검증 상태를 나눠 본다.", PALE_BLUE),
        ("03 · CASE", "케이스를 확인", "막힘·성공·유지·손상·귀환을 한 행씩 살피고 미실행 gate를 남긴다.", PALE_GREEN),
    )
    for index, (kicker, title_text, body, fill) in enumerate(flow_cards):
        x = 18 * mm + index * column_width
        compact_card(pdf, x, top, column_width - 6 * mm, 47 * mm, kicker, title_text, body, fill=fill)
        if index < len(flow_cards) - 1:
            arrow(pdf, x + column_width - 7 * mm, top - 23.5 * mm, x + column_width + 1 * mm, top - 23.5 * mm)
    top -= 54 * mm
    panel(pdf, 18 * mm, top, page_width - 36 * mm, 35 * mm, fill=PAPER)
    label(pdf, "HOW TO READ", 23 * mm, top - 6 * mm)
    draw_wrapped(pdf, "체크된 사각형은 ‘자동 계약 또는 current-canon 구현 근거가 존재함’을 뜻한다. 런타임·Android·사람 플레이 칸은 의도적으로 비워 둔다. 색은 찾기 속도를 돕지만, 모든 상태는 텍스트로도 반복한다.", 23 * mm, top - 13 * mm, page_width - 46 * mm, size=8.2, leading=11.4, color=INK)


def page_thirteen(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 13, "목표별 점검")
    y = heading(pdf, "목표별 점검", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "아래 상태는 2026-09-03의 current main과 현재 사람용 GDD·Phase 1 계약·Decision38/40·세션 handoff를 함께 읽어 만든 파생 보기다. 새 의미를 만들지 않고, 구현 근거와 남은 검토를 분리한다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=8.9, leading=13.2, color=MUTED)
    top = y - 6 * mm
    label(pdf, "GOAL CHECKLIST", 18 * mm, top)
    top -= 5 * mm
    top = checklist_row(pdf, 18 * mm, top, "1", "강화의 긴장감", "CANON + MACHINE", "다음 +1의 성공·유지·손상 가능성을 읽고 STOP 또는 PUSH를 고른다. 일반 성공 +1과 exclusive failure 결과는 정본·자동 계약 근거가 있다. 사람의 재미 판정은 NOT RUN.", fill=PALE_GOLD)
    top = checklist_row(pdf, 18 * mm, top, "2", "태그가 남는 정밀 단위", "CANON + MACHINE", "+9→+10부터 +99→+100까지 매 10단위에 태그 추가 또는 강화 하나를 고른다. 촉매 1개 소비와 V5 저장 원자성은 기계 검증, live 결제는 NOT RUN.", fill=PALE_GREEN)
    top = checklist_row(pdf, 18 * mm, top, "3", "같은 UID 작품 생애", "CANON + MACHINE", "제작·강화·손상·수리·인계·실제 사용·연대기가 한 작품으로 이어진다. 인계 자체는 손상이 아니며, 전체 사람이 플레이하는 흐름은 NOT RUN.", fill=PALE_BLUE)
    top -= 1 * mm
    label(pdf, "시스템별 점검", 18 * mm, top)
    top -= 5 * mm
    top = checklist_row(pdf, 18 * mm, top, "A", "일반 강화와 +5 제작 리듬", "MACHINE", "현재 target과 결과를 분리해 표시하고, +5는 presentation-only다. +5가 촉매·태그·새 실패 규칙을 열지 않는 계약을 유지한다.", fill=PAPER, height_mm=19.0)
    top = checklist_row(pdf, 18 * mm, top, "B", "정밀 태그·소모형 촉매", "LIMITED UI", "불의 심장·대지의 결정은 실제 자원이며 1개씩 소비한다. +9→+10의 선택·보유량·활성 CTA는 관찰, 시도 결과의 live 영속은 NOT RUN.", fill=PALE_COPPER, height_mm=19.0)
    top = checklist_row(pdf, 18 * mm, top, "C", "손상·수리", "MACHINE", "CURRENT / MAX / BASE_MAX가 유일한 visible authority다. 실제 손상 뒤 한 수리 job만 열며, Android과 사람의 이해도는 NOT RUN.", fill=PALE_GREEN, height_mm=19.0)
    top = checklist_row(pdf, 18 * mm, top, "D", "고객 실제 사용·연대기", "MACHINE", "인계와 실제 사용 결과를 분리하고 의미 사건만 연대기에 남긴다. 전체 귀환 흐름은 실제 화면·사람 검수 전이다.", fill=PALE_BLUE, height_mm=19.0)


def page_fourteen(pdf: canvas.Canvas) -> None:
    page_width, page_height = A4
    header(pdf, 14, "대표 케이스 점검")
    y = heading(pdf, "대표 케이스 점검", 18 * mm, page_height - 27 * mm, size=18)
    y = draw_wrapped(pdf, "한 행은 ‘조건 → 기대 행동 → 근거 → 남은 인간 검토’를 묶는다. MACHINE은 자동 계약 근거이고, LIMITED UI는 실제 Godot 화면을 일부 관찰한 경우만 표기한다.", 18 * mm, y - 2 * mm, page_width - 36 * mm, size=9.0, leading=13.5, color=MUTED)
    top = y - 6 * mm
    top = checklist_row(pdf, 18 * mm, top, "01", "일반 +1과 +5", "MACHINE", "+0~+9 일반 시도는 정확히 +1만 성공하고, +5는 presentation-only다. 정밀 태그·촉매가 누출되지 않는다. 실제 인간 판독성은 NOT RUN.", fill=PALE_GOLD)
    top = checklist_row(pdf, 18 * mm, top, "02", "+9→+10 사전 조건", "LIMITED UI", "선택 누락·촉매 부족·무효 조합은 비용·보강재·굴림 전에 막힌다. 실제 화면에서 촉매 선택과 CTA 준비만 관찰했으며 결제·저장은 NOT RUN.", fill=PALE_COPPER)
    top = checklist_row(pdf, 18 * mm, top, "03", "+9→+10 정상 해소", "MACHINE", "유효한 시도는 골드·보강재·필요 촉매 1개를 같은 save 후보에 반영한다. 성공은 태그 I 하나, hold/damage는 태그 변화 없음. live 결과는 NOT RUN.", fill=PALE_GREEN)
    top = checklist_row(pdf, 18 * mm, top, "04", "+19→+20 이후", "MACHINE", "태그가 세 개 미만이면 추가, I~III이면 강화가 가능하다. 중복 태그·IV 태그·네 번째 affix·재굴림은 시도 전에 막힌다. 실제 화면·사람 검토는 NOT RUN.", fill=PALE_BLUE)
    top = checklist_row(pdf, 18 * mm, top, "05", "+11 실패·손상·수리", "MACHINE", "손상은 실패 뒤에만 조건부이며 한 결과는 FAILED_HOLD 또는 FAILED_DAMAGE 하나다. 실제 CURRENT 손상일 때만 수리 job을 열고, live UX는 NOT RUN.", fill=PAPER)
    top = checklist_row(pdf, 18 * mm, top, "06", "인계 → 실제 사용 → 연대기", "MACHINE", "인계는 손상을 만들지 않는다. 실제 사용 결과와 장비 손상은 별도 축이며, 의미 사건만 기록한다. 전체 흐름의 runtime·human 검수는 NOT RUN.", fill=PALE_COPPER)
    panel(pdf, 18 * mm, top, page_width - 36 * mm, 31 * mm, fill=PALE_GOLD)
    label(pdf, "NEXT REVIEW", 23 * mm, top - 6 * mm)
    draw_wrapped(pdf, "다음 실제 화면 검토는 페이지 3의 공방 읽기 순서, 페이지 7·8의 촉매/태그 행동, 페이지 9·10의 손상·귀환을 순서대로 확인한다. 이 체크리스트는 별도 HTML을 만들지 않으며, 빈 NOT RUN을 완료로 바꾸지 않는다.", 23 * mm, top - 12 * mm, page_width - 46 * mm, size=8.0, leading=11.0, color=INK)


def draw_pdf() -> str:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4, invariant=1)
    pdf.setTitle(TITLE)
    pdf.setAuthor("Blacksmith Project")
    pdf.setSubject("Derived non-canonical Blueprint Viewer")
    pdf.setCreator("Blacksmith deterministic ReportLab publisher")
    for page in (
        page_one,
        page_two,
        page_three,
        page_four,
        page_five,
        page_six,
        page_seven,
        page_eight,
        page_nine,
        page_ten,
        page_eleven,
        page_twelve,
        page_thirteen,
        page_fourteen,
    ):
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
    runtime_asset_references = [
        {
            **reference,
            "sha256": sha256(ROOT / reference["path"]),
            "reuse_scope": "DERIVED_PDF_REFERENCE_ONLY / EXISTING_RUNTIME_ASSET_UNCHANGED",
        }
        for reference in RUNTIME_ASSET_REFERENCES
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
        "runtime_asset_references": runtime_asset_references,
        "publisher": {
            "path": "tools/publish_phase1_workshop_blueprint_pdf.py",
            "engine": "ReportLab",
            "fonts": ["C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"],
            "invariant_pdf": True,
            "contains_new_generated_raster_asset": False,
            "embeds_existing_runtime_asset_references": True,
            "embedded_runtime_asset_reference_count": len(runtime_asset_references),
            "contains_product_runtime_screenshot": False,
        },
        "integrated_checklist": {
            "delivery_surface": "BLUEPRINT_PDF_ONLY",
            "standalone_html_created": False,
            "sections": ["goal", "system", "case"],
            "status_terms": [
                "CANON + MACHINE",
                "LIMITED UI",
                "NOT RUN",
            ],
            "as_of": "2026-09-03 / main ee60c74df2b3a9aef8544c5bc349a71339065249",
            "scope": "DERIVED_STATUS_VIEW / NO_NEW_PRODUCT_RULE_OR_RUNTIME_CLAIM",
        },
        "render_validation": {
            "required_tool": "pdftoppm",
            "status": render_status,
            "rendered_pages": rendered_pages,
            "visual_review": visual_review,
        },
        "benchmark_preflight_receipt": {
            "date": "2026-09-03",
            "scope": "INTEGRATED_BLUEPRINT_CHECKLIST / NO_STANDALONE_HTML_OR_NEW_PRODUCT_RULE_OR_ASSET",
            "inputs": [
                {
                    "source": "Godot 4.7 TextureRect official documentation",
                    "type": "PRIMARY_TECHNICAL_SOURCE",
                    "disposition": "ADOPT",
                    "finding": "Keep-aspect centered texture placement preserves transparent equipment identity and portrait-background reference proportions.",
                },
                {
                    "source": "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf",
                    "type": "PROJECT_HUMAN_GDD_REFERENCE",
                    "disposition": "ADAPT",
                    "finding": "Retain its visual-anchor pattern by placing actual-consumer assets next to the current detailed flow, not by importing superseded rule text.",
                },
                {
                    "source": "W3C WAI Headings and Tables tutorials",
                    "type": "PRIMARY_DOCUMENT_STRUCTURE_SOURCE",
                    "disposition": "ADAPT",
                    "finding": "Use short section labels and text-described status rows so the PM summary has a clear hierarchy and does not rely on color alone. This guidance changes no game rule or runtime accessibility claim.",
                },
                {
                    "source": "Reference-only user-supplied PM screenshot",
                    "type": "USER_REFERENCE_LAYOUT_DENSITY",
                    "disposition": "ADAPT",
                    "finding": "Retain at-a-glance goal, system, and case grouping while preserving the approved illustrated-workshop-book PDF direction rather than copying the dark dashboard surface.",
                },
            ],
        },
        "context_configuration_hygiene": {
            "scope_class": "NONCODING_BUILD",
            "modified_paths": [
                "tools/publish_phase1_workshop_blueprint_pdf.py",
                "tests/check_phase1_workshop_blueprint_pdf_contract.py",
                "tests/test_phase1_workshop_blueprint_pdf_publisher.py",
                "exports/blacksmith_PHASE1_WORKSHOP_BLUEPRINT_20260902.pdf",
                "docs/operations/receipts/2026-09-02-phase1-workshop-blueprint-pdf.json",
            ],
            "protected_product_paths_modified": False,
            "new_runtime_asset": False,
            "temporary_render_directory": "tmp/pdfs/phase1-workshop-blueprint-checklists-render (task-created; cleanup pending host deletion policy)",
            "unused_temporary_files_retained": True,
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
    if len(reader.pages) != PAGE_COUNT:
        raise RuntimeError(f"expected {PAGE_COUNT} pages, found {len(reader.pages)}")
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
    if len(reader.pages) != PAGE_COUNT:
        raise RuntimeError(f"expected {PAGE_COUNT} pages, found {len(reader.pages)}")
    write_receipt(
        render_status="RENDERED_AND_AGENT_VISUAL_LAYOUT_REVIEWED",
        rendered_pages=list(range(1, len(reader.pages) + 1)),
        visual_review=f"ALL_{PAGE_COUNT}_PAGES_RENDERED_AND_VISUALLY_REVIEWED_FOR_CLIPPING_OVERLAP_AND_LEGIBILITY",
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
