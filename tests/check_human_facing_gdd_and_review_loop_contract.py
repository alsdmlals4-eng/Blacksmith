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
AI_SPEC = ROOT / "docs/design/PROJECT_AI_PRODUCTION_SPEC.md"
ROUTING = ROOT / "docs/decisions/BS-OPS-20260828-35_GITHUB_ONLY_CANON_AND_IMAGE_EXECUTION_ROUTING.md"
REVIEW_LOOP = ROOT / "docs/decisions/BS-OPS-20260828-36_EVIDENCE_RESEARCH_AND_ADVERSARIAL_REVIEW_LOOP.md"
AGENTS = ROOT / "AGENTS.md"
PDF = ROOT / "exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf"
PDF_RECEIPT = ROOT / "docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json"
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
    ai_spec = read(AI_SPEC, failures)
    routing = read(ROUTING, failures)
    review_loop = read(REVIEW_LOOP, failures)
    agents = read(AGENTS, failures)

    for token in (
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
        "NOT_RUN",
        "+9 → +10",
        "태그 키워드",
        "촉매 계보",
        "정밀강화 방식",
        "강화 → 태그 → 생애",
        "태그 시스템: 무기에 남는 완성 경로의 정체성",
        "촉매 계보 → 정밀강화 방식 → 태그 키워드",
        "생애 주기: 고객의 실제 사용으로 닫히는 흐름",
        "고객 이벤트: 결과의 원인을 보여 주는 규칙",
        "인계 → 실제 사용 → 사건 결과 → 다음 판단",
        "선택 UX는 아직 미확정",
        "빈 촉매 계보는 현재 태그 기록을 막는다",
        "손상이 발생했을 때",
        "내부 임시 값",
        "5강 단위",
        "REJECT",
        "차별점",
        "남은 불확실성",
    ):
        require(human_gdd, token, failures, "human-facing GDD")

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
    ):
        require(ai_spec, token, failures, "AI production spec")

    if not PDF.exists() or PDF.stat().st_size < 10_000:
        failures.append("human-facing Korean GDD PDF is missing or implausibly small")
    if not PDF_RECEIPT.exists():
        failures.append("human-facing PDF provenance receipt is missing")
    else:
        try:
            receipt = json.loads(PDF_RECEIPT.read_text(encoding="utf-8"))
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
            if reader.metadata.subject != "Human-facing Korean GDD":
                failures.append("PDF subject does not identify the human-facing Korean GDD")
            if len(reader.pages) < 9:
                failures.append("PDF has fewer than the inspected 9 human-facing GDD pages")
        except Exception as exc:  # noqa: BLE001 - report contract evidence, not a traceback.
            failures.append(f"cannot validate human-facing PDF provenance: {exc}")
    if not ARCHIVE_GDIGNORE.exists():
        failures.append("historical Notion visual archive must be Godot-ignored")

    if failures:
        print("Human-facing GDD and review-loop contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Human-facing GDD and review-loop contract PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
