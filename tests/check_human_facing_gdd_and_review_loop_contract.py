#!/usr/bin/env python3
"""사람용 한국어 GDD와 증거·적대 검토 운영 계약을 보호한다."""
from __future__ import annotations

import sys
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
HUMAN_GDD = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md"
TITLE_DECISION = ROOT / "docs/decisions/BS-IDENTITY-20260831-39_ANVIL_OATH_PRODUCT_TITLE.md"
AI_SPEC = ROOT / "docs/design/PROJECT_AI_PRODUCTION_SPEC.md"
ROUTING = ROOT / "docs/decisions/BS-OPS-20260828-35_GITHUB_ONLY_CANON_AND_IMAGE_EXECUTION_ROUTING.md"
REVIEW_LOOP = ROOT / "docs/decisions/BS-OPS-20260828-36_EVIDENCE_RESEARCH_AND_ADVERSARIAL_REVIEW_LOOP.md"
AGENTS = ROOT / "AGENTS.md"
PDF = ROOT / "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf"
PDF_RECEIPT = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json"
PUBLISHER = ROOT / "tools/publish_human_facing_gdd_pdf.py"
ARCHIVE_GDIGNORE = ROOT / "docs/migration/historical_notion_gdd/.gdignore"


def require(text: str, token: str, failures: list[str], label: str) -> None:
    if token not in text:
        failures.append(f"{label} missing required token: {token}")


def read(path: Path, failures: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        failures.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return ""


def normalized_lf_sha256(path: Path) -> str:
    """Windows CRLF checkout만 정규화한 UTF-8 Markdown 수령증 해시를 계산한다."""
    payload = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    failures: list[str] = []
    human_gdd = read(HUMAN_GDD, failures)
    title_decision = read(TITLE_DECISION, failures)
    ai_spec = read(AI_SPEC, failures)
    publisher = read(PUBLISHER, failures)
    routing = read(ROUTING, failures)
    review_loop = read(REVIEW_LOOP, failures)
    agents = read(AGENTS, failures)

    for token in (
        "# 모루의 서약 — 사람용 게임 기획서",
        "모루의 서약 / ANVIL OATH",
        "사람용 게임 기획서",
        "한눈에 보는 게임",
        "장르",
        "플레이어 시점",
        "핵심 재미",
        "강화 중심 제작·경영 내러티브",
        "대장장이 공방 주인",
        "STOP OR PUSH",
        "사람용 본문 = 플레이 경험의 이해와 의사결정",
        "개발 참고 = 구현·데이터·테스트 추적",
        "현재 증거 한계",
        "아직 실행하지 않음",
        "정밀 강화",
        "+9 → +10",
        "+19 → +20",
        "+99 → +100",
        "태그 추가",
        "태그 강화",
        "최대 세 개",
        "씨앗 / 성장 / 진화 / 완성",
        "정상 강화에서는 태그를 고르지 않는다",
        "성공 한 번에는 태그 행동도 정확히 하나",
        "비용과 굴림 전에 막힌다",
        "태그 키워드",
        "정밀 촉매",
        "정밀강화 방식",
        "강화 → 태그 → 생애",
        "태그 시스템: 무기에 남는 완성 경로의 정체성",
        "정밀 촉매 → 정밀강화 방식 → 태그 키워드",
        "생애 주기: 고객의 실제 사용으로 닫히는 흐름",
        "고객 이벤트: 결과의 원인을 보여 주는 규칙",
        "인계 → 실제 사용 → 사건 결과 → 다음 판단",
        "불의 심장",
        "대지의 결정",
        "날 세우기",
        "경량 담금",
        "태그를 정하지 않으면 강화 시도 자체가 시작되지 않는다",
        "사람 플레이 검수는 이번 계약의 완료 조건이 아니다",
        "손상이 발생했을 때",
        "5강 단위",
        "REJECT",
        "차별점",
        "남은 불확실성",
        "열 번의 정밀 강화",
        "+99 → +100",
        "태그 추가 또는 태그 강화",
        "BS-ENHANCE-20260830-38",
        "BS-ENHANCE-20260901-40",
        "V5 resource migration",
        "all ten Precision gates",
        "LIMITED_RUNTIME_UI_OBSERVED",
    ):
        require(human_gdd, token, failures, "human-facing GDD")

    for token in (
        "PRODUCT_TITLE_KO = 모루의 서약",
        "PRODUCT_TITLE_LATIN = ANVIL OATH",
        "KEEP_GENERIC_WORKSHOP_COPY = TRUE",
        "PUBLIC_BRAND_LEGAL_CLEARANCE = NOT_RUN",
    ):
        require(title_decision, token, failures, "Anvil Oath title decision")

    for token in (
        "HUMAN_FACING_GDD = docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md",
        "HUMAN_FACING_PDF = exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf",
        "HUMAN_FACING_PDF_RECEIPT = docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json",
        "PROJECT_AI_PRODUCTION_SPEC.md",
    ):
        require(routing, token, failures, "GitHub-only routing decision")

    for token in (
        "USER_APPROVED_CURRENT_OPERATIONAL_OVERRIDE",
        "FRESH_CANONICAL_READ = REQUIRED",
        "CURRENT_EXTERNAL_RESEARCH = REQUIRED_FOR_EVERY_SUBSTANTIVE_TASK",
        "ADVERSARIAL_REVIEW_LOOP = REQUIRED",
        "IMPLEMENTATION_FEASIBILITY_GATE = REQUIRED",
        "EVIDENCE_CEILING = NO_AUTO_PASS",
        "ADOPT / ADAPT / AVOID / REJECT / DIFFERENTIATION / REMAINING_UNCERTAINTY / TEST",
    ):
        require(review_loop, token, failures, "evidence and adversarial review decision")

    for token in (
        "BS-OPS-20260828-36",
        "ADVERSARIAL_REVIEW_LOOP = REQUIRED",
        "GITHUB_HUMAN_FACING_GDD_OWNER",
    ):
        require(agents, token, failures, "AGENTS.md")

    for token in (
        "기술·정본 추적용",
        "BLACKSMITH_HUMAN_FACING_GDD_20260828.md",
        "PR #328",
        "DEC-ENH-37",
        "UI-PREC-001",
        "Workshop 안의 선택·미리보기·확인 흐름",
        "IMPLEMENTED / AUTOMATED_TEST_PASS",
    ):
        require(ai_spec, token, failures, "AI production spec")

    for forbidden in (
        "Exactly one `CATALYST_AFFIX` / Tag",
        "Only a successful `+9→+10` enhancement.",
        "V3 save and item schemas",
        "writes V3 on next save",
        "must use no new stored field",
        "SUCCESS_AT_PLUS10: one Tag resolve/write",
    ):
        if forbidden in ai_spec:
            failures.append(f"AI production spec contains unqualified superseded recurring-Precision claim: {forbidden}")
    for forbidden in (
        "and precision-tag Decision37 /",
        "| DAT-SAVE-001 | `VSSaveEnvelope` | V3;",
        "| EVT-SAVE-001 | service → save service | candidate V3 envelope |",
        "Decision37's TDD",
        "Decision37's current JSON/contract owner",
    ):
        if forbidden in ai_spec:
            failures.append(f"AI production spec retains unqualified Decision37/V3 trace: {forbidden}")
    for line_number, line in enumerate(ai_spec.splitlines(), start=1):
        if "Decision37" in line and not all(
            qualification in line
            for qualification in (
                "historical/superseded",
                "first 2×2",
                "Decision38/40",
                "catalog V3/V5",
                "active current owners",
            )
        ):
            failures.append(
                "AI production spec Decision37 entry must locally identify only the "
                f"historical first-2×2 catalog and the active recurring owner (line {line_number})"
            )
        if line.startswith("| SRC-CAN-08A |") or line.startswith("| DEC-PREC-35/36 |"):
            if not all(
                qualification in line
                for qualification in (
                    "historical/superseded",
                    "first 2×2",
                    "Decision38/40",
                    "catalog V3/V5",
                    "active current owners",
                )
            ):
                failures.append(
                    "AI production spec historical precision source entry must locally identify the "
                    f"Decision38/schema2/V4 active recurring owner (line {line_number})"
                )
    for entry_name, line_prefix in (
        ("canonical current owners", "| Canonical current owners |"),
        ("work-stage current owners", "| 1. Intent and canon |"),
        ("Decision37 confirmed-decision row", "| DEC-ENH-37 |"),
        ("recurring Precision Tag traceability row", "| Precision Tag action reflects player choice |"),
        ("Decision37 change-log row", "| 2026-08-29 | Adds `BS-ENHANCE-20260829-37`"),
    ):
        matching_line = next((line for line in ai_spec.splitlines() if line.startswith(line_prefix)), "")
        if not matching_line:
            failures.append(f"AI production spec is missing {entry_name} entry")
            continue
        if not all(
            qualification in matching_line
            for qualification in (
                "historical/superseded",
                "first 2×2",
                "Decision38/40",
                "catalog V3/V5",
                "active current owners",
            )
        ):
            failures.append(
                f"AI production spec {entry_name} entry must locally separate Decision37 "
                "from the Decision38/40 catalog V3/V5 active current owners"
            )
    for forbidden in (
        "Decisions 28-32, 34 and 37 JSON/decision owners",
        "Current owner files and Decisions 25-37.",
    ):
        if forbidden in ai_spec:
            failures.append(f"AI production spec retains unqualified legacy precision owner range: {forbidden}")
    for token in (
        "BS-ENHANCE-20260830-38",
        "V5 resource migration",
        "BS-ENHANCE-20260901-40",
        "First gate is `ADD_TAG` only; later gates use `ADD_TAG` or `UPGRADE_TAG`",
    ):
        require(ai_spec, token, failures, "AI production spec recurring current trace")
    for token in ("class NumberedCanvas", "FOOTER_RESERVE", "_draw_final_footer", "canvasmaker=NumberedCanvas"):
        require(publisher, token, failures, "PDF publisher footer contract")

    if not PDF.exists() or PDF.stat().st_size < 10_000:
        failures.append("human-facing Korean GDD PDF is missing or implausibly small")
    elif PDF.stat().st_size > 5 * 1024 * 1024:
        failures.append("human-facing Korean GDD PDF exceeds the 5 MiB derivative-size budget")
    if not PDF_RECEIPT.exists():
        failures.append("human-facing PDF provenance receipt is missing")
    else:
        try:
            receipt = json.loads(PDF_RECEIPT.read_text(encoding="utf-8"))
            if receipt.get("schema_version") != 2:
                failures.append("PDF receipt must use the current deterministic publisher schema version 2")
            expected_gdd_hash = normalized_lf_sha256(HUMAN_GDD)
            expected_pdf_hash = hashlib.sha256(PDF.read_bytes()).hexdigest()
            if receipt.get("source_markdown", {}).get("sha256") != expected_gdd_hash:
                failures.append("PDF receipt source Markdown SHA-256 does not match the human-facing GDD")
            if receipt.get("source_markdown", {}).get("hash_basis") != "UTF-8_BYTES_WITH_CRLF_TO_LF_NORMALIZATION":
                failures.append("PDF receipt source Markdown hash basis must be portable CRLF-to-LF normalization")
            if receipt.get("artifact", {}).get("sha256") != expected_pdf_hash:
                failures.append("PDF receipt artifact SHA-256 does not match the PDF")
            reader = PdfReader(str(PDF))
            if receipt.get("artifact", {}).get("page_count") != len(reader.pages):
                failures.append("PDF receipt page count does not match the readable PDF")
            for page_number, page in enumerate(reader.pages, start=1):
                expected_footer = f"{page_number} / {len(reader.pages)} · 2026-09-01"
                if expected_footer not in (page.extract_text() or ""):
                    failures.append(f"human-facing GDD PDF page {page_number} footer must show the current document date")
            expected_images = [
                "assets/ui/workshop/main_menu_dawn_background_v1.png",
                "assets/ui/workshop/customer_result_return_illustration_v1.png",
                "assets/ui/equipment/iron_sword_card_v2.png",
                "assets/ui/equipment/iron_shield_card_v2.png",
                "assets/ui/equipment/iron_bow_card_v2.png",
                "assets/ui/equipment/iron_armor_card_v2.png",
                "assets/ui/equipment/iron_helmet_card_v2.png",
            ]
            if receipt.get("publish_recipe", {}).get("images") != expected_images:
                failures.append("PDF receipt must contain the two scene and five equipment runtime illustrations")
            if reader.metadata.title != "모루의 서약 · 사람용 게임 기획서":
                failures.append("PDF title does not identify the Anvil Oath human-facing GDD")
            if reader.metadata.subject != "Human-facing Korean GDD":
                failures.append("PDF subject does not identify the human-facing Korean GDD")
            product_identity = receipt.get("product_identity", {})
            if product_identity.get("decision_id") != "BS-IDENTITY-20260831-39":
                failures.append("PDF receipt product identity must cite the Anvil Oath decision")
            if product_identity.get("korean_title") != "모루의 서약":
                failures.append("PDF receipt Korean product title must be 모루의 서약")
            if product_identity.get("latin_lockup") != "ANVIL OATH":
                failures.append("PDF receipt Latin title lockup must be ANVIL OATH")
            if product_identity.get("legal_clearance") != "NOT_RUN":
                failures.append("PDF receipt must preserve unverified legal-clearance state")
            if len(reader.pages) < 9:
                failures.append("PDF has fewer than the inspected 9 human-facing GDD pages")
            pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
            normalized_pdf_text = " ".join(pdf_text.split())
            for token in (
                "모루의 서약",
                "ANVIL OATH",
                "열 번의 정밀 강화",
                "+99 → +100",
                "태그 추가 또는 태그 강화",
                "BS-ENHANCE-20260830-38",
                "BS-ENHANCE-20260901-40",
                "V5 resource migration",
                "all ten Precision gates",
            ):
                require(normalized_pdf_text, " ".join(token.split()), failures, "human-facing GDD PDF")
        except Exception as exc:  # noqa: BLE001 - report contract evidence, not a traceback.
            failures.append(f"cannot validate human-facing PDF provenance: {exc}")
    if not ARCHIVE_GDIGNORE.exists():
        failures.append("historical Notion visual archive must be Godot-ignored")
    if not PUBLISHER.exists():
        failures.append("deterministic human-facing PDF publisher is missing")

    if failures:
        print("Human-facing GDD and review-loop contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Human-facing GDD and review-loop contract PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
