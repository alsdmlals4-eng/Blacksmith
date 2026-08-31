from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "exports" / "blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf"
FONT = Path(r"C:\Windows\Fonts\malgun.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\malgunbd.ttf")


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text.replace("\n", "<br/>"), style)


def build() -> None:
    pdfmetrics.registerFont(TTFont("Malgun", str(FONT)))
    pdfmetrics.registerFont(TTFont("MalgunBold", str(FONT_BOLD)))
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "KoreanBody",
        parent=styles["BodyText"],
        fontName="Malgun",
        fontSize=9.4,
        leading=15,
        textColor=colors.HexColor("#22262B"),
        wordWrap="CJK",
        spaceAfter=5,
    )
    small = ParagraphStyle(
        "KoreanSmall",
        parent=body,
        fontSize=7.5,
        leading=11,
        textColor=colors.HexColor("#5C6570"),
    )
    h1 = ParagraphStyle(
        "KoreanH1",
        parent=styles["Heading1"],
        fontName="MalgunBold",
        fontSize=25,
        leading=34,
        textColor=colors.HexColor("#542E1D"),
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    h2 = ParagraphStyle(
        "KoreanH2",
        parent=styles["Heading2"],
        fontName="MalgunBold",
        fontSize=15,
        leading=23,
        textColor=colors.HexColor("#713F2A"),
        spaceBefore=7,
        spaceAfter=7,
    )
    h3 = ParagraphStyle(
        "KoreanH3",
        parent=styles["Heading3"],
        fontName="MalgunBold",
        fontSize=11,
        leading=17,
        textColor=colors.HexColor("#875233"),
        spaceBefore=5,
        spaceAfter=3,
    )
    callout = ParagraphStyle(
        "KoreanCallout",
        parent=body,
        fontName="MalgunBold",
        fontSize=11,
        leading=18,
        textColor=colors.HexColor("#542E1D"),
        alignment=TA_CENTER,
    )

    def section(title: str, content: list[str]) -> list[object]:
        return [paragraph(title, h2)] + [paragraph(line, body) for line in content]

    def table(rows: list[list[str]], widths: list[float]) -> Table:
        rendered = [[paragraph(cell, small if r else body) for cell in row] for r, row in enumerate(rows)]
        result = Table(rendered, colWidths=widths, repeatRows=1, hAlign="LEFT")
        result.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6B3B27")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "MalgunBold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9C9B5")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFF9EE")),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return result

    story: list[object] = []
    story += [Spacer(1, 25 * mm), paragraph("Blacksmith", h1), paragraph("사람용 게임 기획서", h1)]
    story += [Spacer(1, 7 * mm), paragraph("강화가 메인이고, 한 무기의 생애가 기억이 되는 Android 세로형 공방 게임", callout)]
    story += [Spacer(1, 20 * mm), paragraph("HUMAN_FACING_GDD / KOREAN_PRIMARY", small)]
    story += [paragraph("기준: main 69aa3240 · 2026-08-28 KST", small)]
    story += [paragraph("사람용 본문은 플레이 경험과 의사결정을 설명합니다. 수치·코드·테스트의 정밀 추적은 별도 기술 명세가 맡습니다.", small)]
    story.append(PageBreak())

    story += section("1. 한눈에 보는 게임", [
        "<b>장르</b> — 강화 중심 제작·경영 내러티브 게임. Android 세로형 1인 싱글플레이 Godot 프로젝트.",
        "<b>플레이어 시점</b> — 전장을 직접 조작하는 전사가 아니라 고객의 무기를 만들고 위험을 판단하는 대장장이 공방 주인.",
        "<b>핵심 재미</b> — 다음 +1의 이득·위험·비용을 읽고 ‘지금 멈출까, 한 번 더 밀까’를 내 결정으로 감수하는 강화의 긴장.",
        "<b>차별점</b> — 동일한 무기 UID가 고객의 실제 사용, 손상, 수리, 사건, 연대기로 이어진다. 강화의 숫자가 한 작품의 생애가 된다.",
    ])
    story.append(table([
        ["핵심 질문", "플레이어가 느껴야 할 것", "판매 포인트"],
        ["STOP OR PUSH", "내 판단 때문에 안도·긴장·아쉬움이 생긴다.", "강화를 충분히 즐긴 뒤, 고객과 무기의 생애로 그 선택을 기억한다."],
    ], [45 * mm, 59 * mm, 65 * mm]))
    story += section("2. 게임의 약속", [
        "플레이어는 한 작품의 강화 정보를 읽고, STOP 또는 PUSH를 고른다. 성공은 분명한 +1 전진이다. 실패는 유지 또는 손상으로 읽히며, 손상은 수리·위험 관리·인계 시점을 배우는 다음 선택으로 이어진다.",
        "고객 생애는 강화 플레이의 대체물이 아니다. 이미 충분히 재미있게 누적한 강화 판단을 ‘이 무기가 누군가에게 실제로 쓰였다’는 기억으로 바꾸는 지연된 인과성이다.",
    ])
    story.append(PageBreak())

    story += section("3. 첫 세션: 기억해야 할 한 편", [
        "새 작품을 만들고 +0에서 +9까지 일반 강화를 한 번씩 경험한다. 성공은 언제나 +1이다.",
        "5강 단위에서는 제작 상승감이 커진다. +5·+10·+15의 표현 비트는 성장을 느끼게 하지만, +10 이외의 새 확률·재료·부가효과 규칙을 만들지 않는다.",
        "+9 → +10은 유일한 정밀강화다. 성공 시 무기에만 태그 키워드 하나가 남는다.",
        "+11부터는 실패 시 손상 가능성이 열리고, 플레이어는 여러 번 STOP OR PUSH를 판단한다. +15에 반드시 가야 하는 것이 아니라 언제 멈출지 스스로 고른다.",
        "인계 뒤 같은 무기가 고객의 실제 사용 결과로 돌아온다. 보여주기 위한 강제 손상은 없다. 손상됐을 때만 수리 선택이 열린다.",
    ])
    story.append(table([
        ["첫 세션의 목적", "성공 조건", "아직 검증하지 않은 것"],
        ["강화가 메인이고 생애가 그 결과를 기억나게 한다는 약속을 한 번에 전달", "플레이어가 ‘왜 여기서 멈추거나 밀었는지’를 자기 말로 설명", "6~8분 목표 길이, 실제 재미, 터치/글자/Android 사용성은 NOT_RUN"],
    ], [52 * mm, 58 * mm, 59 * mm]))
    story.append(PageBreak())

    story += section("4. 핵심 루프", [
        "제작 → 강화 미리보기 → STOP/PUSH 판단 → 성공/유지/손상 즉시 확인 → 상태 재평가 → 인계 → 고객 실제 사용 결과 → 필요 시 수리 또는 다음 강화.",
        "화면에서는 작품 정체성, 이번 결정의 이득/위험/비용, 상태 변화, 고객 생애 맥락 순서로 읽혀야 한다. 장식은 이 순서를 가리면 안 된다.",
    ])
    story.append(table([
        ["단계", "플레이어가 보는 것", "의미 있는 판단", "피드백"],
        ["준비", "무기·강화·등급·내구도", "이 작품에 투자할 가치", "작품의 출생과 정체성"],
        ["강화", "목표·성공/손상·비용", "지금 PUSH할 가치", "+1 / 유지 / 손상"],
        ["수리", "현재/최대/기본 내구도", "수리·손상 도전·인계", "다음 위험의 조건 변화"],
        ["생애", "고객의 실제 사용 결과", "결과를 해석하고 다음 시도로", "연대기에 남는 작품의 기억"],
    ], [25 * mm, 48 * mm, 50 * mm, 46 * mm]))
    story.append(PageBreak())

    story += section("5. 강화 → 태그 → 생애", [
        "강화는 메인이다. 태그와 생애는 강화 뒤에 따로 수집하는 시스템이 아니라, 한 번의 강화 판단을 작품 정체성과 이후 이야기로 남기는 세 층이다.",
        "제작 등급 확인 → +0~+9 STOP/PUSH → +9 → +10에서 유효하게 승인된 촉매 계보와 정밀강화 방식의 조합으로 태그 해석 → 성공 시 무기 태그 → +11 이후 재도전·수리·인계 → 고객 실제 사용 결과 → 연대기와 다음 판단.",
        "+5 단위 제작 상승감은 연출의 비트다. 일반 강화 성공은 언제나 +1이며, +10을 제외해 새 정밀강화·새 부가효과·새 확률·새 재료 규칙을 만들지 않는다.",
        "+10 태그는 ‘강화를 끝냈다’는 도장이 아니다. 승인된 촉매 계보와 방식의 조합으로 완성된 정체성을 무기에 보이게 하는 전환점이다.",
    ])
    story.append(table([
        ["강화의 결과", "무기에 남는 것", "생애에서 돌아오는 것"],
        ["STOP/PUSH의 누적과 +10 정밀강화", "등급·태그·사건을 구분해 읽는 한 작품의 정체성", "실제 사용의 결과가 수리·다음 강화·다음 인계 판단으로 돌아옴"],
    ], [53 * mm, 59 * mm, 68 * mm]))
    story.append(PageBreak())

    story += section("6. 태그 시스템: 무기에 남는 완성 경로의 정체성", [
        "무기 키워드는 임의 수식어가 아니다. 등급은 출발 품질, 태그는 +10에서의 완성 결과, 사건은 의미 있는 생애를 말한다. 네 번째 슬롯이 아니다.",
        "태그는 촉매 계보 → 정밀강화 방식 → 태그 키워드 순서로 해석된다. 촉매 계보가 후보 가족을 정하고, 방식이 그 안에서 태그 정체성의 문맥을 정하며 무기 능력치·내구도에만 영향을 준다.",
        "유효하게 승인된 촉매 계보·방식 조합이 있는 +9 → +10 성공 시 정확히 하나의 태그가 CATALYST_AFFIX에 기록된다. 빈 촉매 계보는 현재 태그 기록을 막는다. 태그는 등급·사건 키워드나 플레이어 칭호를 바꾸지 않는다.",
    ])
    story.append(table([
        ["구분", "언제 생기는가", "사람이 읽는 뜻", "보호 경계"],
        ["등급", "제작 시", "작품의 출발 품질", "정밀강화/사건이 바꾸지 않음"],
        ["태그", "+9 → +10 성공", "촉매 계보 + 방식으로 완성한 무기", "무기 귀속, 플레이어 칭호 아님"],
        ["사건", "의미 있는 생애", "고객·세계에서 겪은 일", "단순 인계/표시만으로 부여하지 않음"],
    ], [24 * mm, 36 * mm, 58 * mm, 62 * mm]))
    story += section("미확정 경계", [
        "실제 태그 이름·표시 문구·계보와 방식의 조합표, 빈 촉매 계보에서의 선택/기본값/차단 흐름은 확정되지 않았다. 선택 UX도 미확정이다. 현재 PRECISION_KEYWORD_PENDING_CONTENT는 플레이어 태그가 아닌 내부 임시 값과 구현 흔적이다.",
    ])
    story.append(PageBreak())

    story += section("7. 실패와 내구도: 다시 판단하게 만드는 손실", [
        "실패의 최종 결과는 실패·유지 또는 실패·손상이다. 단계 하락과 별도 치명타 결과는 없다. +10 이하 목표 강화에는 손상이 없고, +11부터 손상은 실패했을 때만 가능하다.",
        "내구도는 현재/최대/기본 최대 세 숫자가 보이는 유일한 기계적 기준이다. 현재 손상과 최대 내구도 흉터를 두 벌점으로 중첩하지 않고, 하나의 유효 상태로 읽는다.",
        "중대 상태여도 강화는 막히지 않는다. 수리, 손상된 채로 PUSH, 멈춤/인계 중 무엇을 할지 플레이어가 선택한다.",
    ])
    story.append(table([
        ["보이는 값", "사람이 이해하는 의미", "플레이어에게 필요한 피드백"],
        ["현재 내구도", "지금의 손상", "이번 손상이 얼마나 회복을 요구하는지"],
        ["최대 내구도", "남은 구조적 상한", "수리 뒤에도 남는 흉터가 있는지"],
        ["기본 최대 내구도", "태어났을 때의 기준", "작품이 원래 얼마나 온전했는지"],
    ], [40 * mm, 59 * mm, 80 * mm]))
    story.append(PageBreak())

    story += section("8. 생애 주기: 고객의 실제 사용으로 닫히는 흐름", [
        "고객 콘텐츠는 고객 관리량을 늘리는 장치가 아니다. 같은 무기 UID를 끝까지 추적해 강화의 결과를 다음 판단으로 돌려주는 짧은 닫힌 흐름이다.",
        "제작·등급 기록 → 강화와 +10 태그 → 인계 → 실제 사용 → 사건 결과 → 내구도·수리 가능 여부·연대기 확인 → 다음 강화 / 수리 / 다음 인계 판단.",
        "인계 → 실제 사용 → 사건 결과 → 다음 판단. 인계·구매·보유 기간·메뉴 조작만으로는 손상이 나지 않는다. 임무 성패와 무기 손상도 같은 축이 아니다.",
    ])
    story.append(table([
        ["단계", "플레이어가 이해할 것", "다음 행동"],
        ["인계", "같은 UID가 고객에게 갔다", "실제 사용 결과를 기다리는 관리가 아니라 맥락 확인"],
        ["실제 사용", "내가 만든 무기가 사건에서 쓰였다", "결과와 원인을 읽기"],
        ["사건 결과", "손상 여부·내구도 전후·수리 가능 여부", "수리 / 손상 상태 PUSH / 작품 확인"],
    ], [31 * mm, 72 * mm, 77 * mm]))
    story.append(PageBreak())

    story += section("9. 고객 이벤트: 결과의 원인을 보여 주는 규칙", [
        "이 이벤트는 랜덤하게 내구도를 깎는 알림이 아니다. 같은 UID, 실제 사용, 선언된 위험 프로필, 사건 원인을 가진 결과다.",
        "한 사건·한 UID에 손상 판정은 최대 한 번이다. 세계 사건은 최대 내구도를 직접 깎지 않으며, 실제 손상 뒤에만 내구도와 수리 규칙이 이어진다.",
        "현재 테스트 프로필 NONE / LOW / MEDIUM / HIGH / DIRECT는 최종 밸런스가 아니다. 모든 고객 카드에 보편 수치를 강요하지 않으며, DIRECT는 일반 키워드로 무효화할 수 없다.",
        "손상이 발생한 결과 화면은 실제 원인, 같은 UID의 내구도 전후, 수리 가능 여부와 다음 행동을 보여 줘야 한다. 연대기는 제작·+10 태그·의미 있는 손상/수리/인계/세계 결과만 남긴다.",
    ])
    story += section("10. 시각 언어", [
        "승인 방향은 ILLUSTRATED_WORKSHOP_BOOK: 따뜻한 손그림 공방 노트, 종이·가죽·철·목재 물성, 현대적으로 선명한 조작 계층이다.",
        "유지할 것: 작품의 손맛, 기록하는 책의 정서, 한눈에 읽히는 강화 결과. 피할 것: 과거 검정·금색 보드를 최종 그림체로 되돌리는 일, 장식 때문에 다음 행동이 묻히는 UI.",
        "새 이미지는 실제 게임 consumer·해상도·상태 요구·권리 기록이 있을 때만 만든다. 생성 후보는 제품 에셋·구현 완료·사람 플레이 증거가 아니며, 최종 잠금은 별도 사용자 확인을 따른다.",
    ])
    story.append(PageBreak())

    story += section("11. 지금 확정된 것과 아직 확인할 것", [
        "확정: 강화 우선, STOP OR PUSH, +10 유일 정밀강화, 무기 귀속 태그, 보이는 내구도, 실제 사용 기반 고객 결과, 작품 연대기, Illustrated Workshop Book 방향.",
        "부분 구현: vertical_slice 공방·고객 결과 화면과 강화/수리/실제사용 resolver가 있다. 2026-08-28 Godot 4.7.1 headless GUT은 167 tests / 0 failures / 0 errors였다. 그러나 +10의 PRECISION_KEYWORD_PENDING_CONTENT는 내부 임시 값이라 실제 태그 콘텐츠를 증명하지 않는다.",
        "NOT_RUN: Godot 클라이언트 렌더, Android 기기, 접근성, 성능, 사람 사용성, Player Experience, 출시 준비, 최종 제품 에셋.",
    ])
    story.append(table([
        ["위험", "왜 중요한가", "다음 검증"],
        ["태그 콘텐츠 미확정", "+10의 보상이 구체적이지 않으면 첫 세션의 상승감이 약해짐", "빈 촉매 계보 규칙과 태그 content row를 별도 Decision으로 잠금"],
        ["고객 생애 과확장", "강화보다 관리/대화가 길어지면 핵심 재미가 흐려짐", "Slice B에서 강화 판단 시간이 중심인지 Human playtest"],
        ["모바일 가독성", "수치·위험·다음 행동을 못 읽으면 STOP/PUSH가 성립하지 않음", "실제 세로형 클라이언트와 Android에서 관찰"],
    ], [43 * mm, 63 * mm, 73 * mm]))
    story.append(PageBreak())

    story += section("12. 조사와 적대적 검토 결과", [
        "ADAPT — Godot Control의 anchor/offset 및 container 계층을 써서 세로형 화면에서도 정보 우선순위를 유지한다. 실제 화면과 터치 확인은 아직 NOT_RUN이다.",
        "TEST — Android export는 SDK/JDK·서명·AAB 준비가 필요한 별도 경로다. 이 문서는 출시 가능 선언이 아니다.",
        "ADAPT — Shop Titans는 제작품이 고객/모험의 맥락을 얻는 감정적 프레이밍만, Moonlighter는 공방 주인의 역할과 귀환 비트의 선명도만 참고한다.",
        "REJECT — 시장·길드·넓은 타이쿤 관리, Moonlighter식 던전 액션·소매 가격 책정을 두 번째 메인 루프로 넣지 않는다. Blacksmith의 차별점은 같은 무기 UID가 실제 사용·손상·연대기로 이어지는 데 있다.",
        "적대 검토 교정 — 기능 목록을 나열하지 않고, 모든 시스템을 STOP OR PUSH → 즉시 결과 → 같은 UID의 생애로 연결했다. 태그 해석 순서와 실제 사용 기반 고객 이벤트를 독립 설명으로 보강했고, +10을 플레이어 보상으로 오해하지 않게 무기 태그 경계를 고정했다.",
        "조사 원문 — Godot UI layout / Android export, Android game design / vitals, Shop Titans·Moonlighter 공식 Steam 페이지를 2026-08-28 KST에 확인했다. 남은 불확실성은 6~8분 Slice의 Human/Player Experience이며, 외부 사례는 요구사항을 자동으로 만들지 않는다.",
    ])
    story += section("13. 다음 구현 계약의 순서", [
        "1) 태그 콘텐츠/빈 촉매 계보 동작 결정 → 2) 실제 consumer를 가진 +5 피드백·+10·고객 결과 UI 계약 → 3) Godot/Android 가독성 검증 → 4) 사람 플레이테스트.",
        "각 구현은 승인된 Issue/Goal, RED→GREEN→REFACTOR, exact-head 검증을 따라야 한다. 문서가 존재하거나 PDF가 예쁘다는 이유로 제품 구현·사용성·권리를 PASS 처리하지 않는다.",
    ])
    story += [Spacer(1, 14 * mm), paragraph("자세한 기계 정본과 경로: docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md", small)]

    def footer(canvas, doc) -> None:
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D9C9B5"))
        canvas.line(20 * mm, 14 * mm, 190 * mm, 14 * mm)
        canvas.setFont("Malgun", 7.5)
        canvas.setFillColor(colors.HexColor("#6B625C"))
        canvas.drawString(20 * mm, 9 * mm, "Blacksmith · 사람용 게임 기획서 · HUMAN_FACING_GDD / KOREAN_PRIMARY")
        canvas.drawRightString(190 * mm, 9 * mm, f"{doc.page}")
        canvas.restoreState()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="Blacksmith 사람용 게임 기획서",
        author="Blacksmith Project",
        subject="Human-facing Korean GDD",
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
