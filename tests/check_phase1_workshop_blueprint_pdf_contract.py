#!/usr/bin/env python3
"""Verify the derived Phase 1 Workshop Blueprint PDF without promoting it to canon."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "exports/blacksmith_PHASE1_WORKSHOP_BLUEPRINT_20260902.pdf"
RECEIPT = ROOT / "docs/operations/receipts/2026-09-02-phase1-workshop-blueprint-pdf.json"
PUBLISHER = ROOT / "tools/publish_phase1_workshop_blueprint_pdf.py"
EXPECTED_SOURCES = {
    "docs/superpowers/specs/2026-09-01-phase1-workshop-blueprint-design.md",
    "docs/planning/PROJECT_CORE_SCENE_VISUAL_BOARD_20260828.md",
    "docs/planning/BLACKSMITH_HUMAN_GAME_FLOW_MAP_2026.md",
    "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md",
    "docs/operations/receipts/2026-09-01-phase1-workshop-blueprint.json",
}
REQUIRED_TEXT = (
    "모루의 서약",
    "Phase 1 워크숍 블루프린트",
    "BLUEPRINT VIEWER",
    "정본 대체 금지",
    "정밀강화",
    "불의 심장",
    "대지의 결정",
    "STOP OR PUSH",
    "+5 제작 리듬",
    "최초 +10",
    "+20 이후",
    "태그 추가",
    "태그 강화",
    "사전 조건 차단",
    "FAILED_HOLD",
    "FAILED_DAMAGE",
    "CURRENT / MAX / BASE_MAX",
    "수리 job",
    "고객 실제 사용",
    "작품 연대기",
    "구현 소유 경로",
    "검증과 증거 한계",
    "사용자 블루프린트 검토 대기",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    failures: list[str] = []
    if not PUBLISHER.exists():
        failures.append(f"missing deterministic publisher: {PUBLISHER.relative_to(ROOT)}")
    if not PDF.exists():
        failures.append(f"missing derived PDF: {PDF.relative_to(ROOT)}")
    if not RECEIPT.exists():
        failures.append(f"missing PDF receipt: {RECEIPT.relative_to(ROOT)}")
    if PDF.exists():
        reader = PdfReader(str(PDF))
        if len(reader.pages) != 11:
            failures.append(f"expected eleven A4 pages, found {len(reader.pages)}")
        if reader.metadata.title != "모루의 서약 · Phase 1 워크숍 블루프린트":
            failures.append(f"unexpected PDF title: {reader.metadata.title!r}")
        if reader.metadata.subject != "Derived non-canonical Blueprint Viewer":
            failures.append(f"unexpected PDF subject: {reader.metadata.subject!r}")
        extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
        if len(extracted) < 10000:
            failures.append(f"detailed PDF text is too short: {len(extracted)} characters")
        for token in REQUIRED_TEXT:
            if token not in extracted:
                failures.append(f"PDF text missing required token: {token}")
    if RECEIPT.exists() and PDF.exists():
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        if receipt.get("artifact_class") != "DERIVED_NONCANONICAL_REVIEW_PDF":
            failures.append("receipt must retain DERIVED_NONCANONICAL_REVIEW_PDF classification")
        if receipt.get("artifact", {}).get("path") != PDF.relative_to(ROOT).as_posix():
            failures.append("receipt artifact path does not match the generated PDF")
        if receipt.get("artifact", {}).get("sha256") != sha256(PDF):
            failures.append("receipt artifact SHA-256 does not match the generated PDF")
        if receipt.get("artifact", {}).get("page_count") != 11:
            failures.append("receipt must report exactly eleven PDF pages")
        if receipt.get("user_review_status") != "USER_BLUEPRINT_REVIEW_PENDING":
            failures.append("receipt must retain the pending user blueprint review boundary")
        if receipt.get("runtime_asset") is not False:
            failures.append("derived PDF must not be represented as a runtime asset")
        source_paths = {entry.get("path") for entry in receipt.get("source_documents", [])}
        if source_paths != EXPECTED_SOURCES:
            failures.append("receipt source set must exactly identify the five current blueprint owners")
        if not receipt.get("benchmark_preflight_receipt"):
            failures.append("receipt must retain a non-empty benchmark preflight receipt")
        if not receipt.get("context_configuration_hygiene"):
            failures.append("receipt must retain non-empty context/configuration hygiene evidence")
    if failures:
        print("phase1 workshop blueprint PDF contract: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        raise SystemExit(1)
    print("phase1 workshop blueprint PDF contract: PASS")


if __name__ == "__main__":
    main()
