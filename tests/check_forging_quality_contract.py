from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def text(rel: str) -> str:
    path = ROOT / rel
    require(path.is_file(), f"필수 파일 누락: {rel}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


balance = json.loads(text("data/crafting/forging_balance.json"))
session = balance.get("session", {})
expected = {
    "weapon_base_attack": 10,
    "quality_standard_attack_multiplier": 1.0,
    "quality_standard_value_multiplier": 1.0,
    "quality_good_attack_multiplier": 1.05,
    "quality_good_value_multiplier": 1.05,
    "quality_perfect_attack_multiplier": 1.10,
    "quality_perfect_value_multiplier": 1.12,
}
for key, value in expected.items():
    require(session.get(key) == value, f"forging_balance.json {key}는 {value}여야 합니다.")

contract_files = (
    list((ROOT / "scripts").rglob("*.gd"))
    + list((ROOT / "tests").rglob("*.gd"))
    + list((ROOT / "scenes").rglob("*.tscn"))
    + list((ROOT / "data").rglob("*.json"))
)
for path in contract_files:
    source = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    require('"quality_multiplier"' not in source, f"구형 단일 품질 배율 필드가 남아 있습니다: {rel}")
    require('weapon_result["base_attack"] = 10' not in source, f"제작 결과 기본 공격력 덮어쓰기가 남아 있습니다: {rel}")

for rel in ["scripts/ui/game_flow_screen.gd", "scripts/ui/enhancement_test_runner.gd"]:
    source = text(rel)
    require('POC v0.6.2 · main · 2026.07.22.2' in source, f"최신 버전 배지가 없습니다: {rel}")
    require('POC v0.6.1 · main · 2026.07.22.1' not in source, f"구형 버전 배지가 남아 있습니다: {rel}")

for rel in [
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md",
    "docs/MVP-001_SCOPE.md",
    "docs/MVP-002_SCOPE.md",
    "docs/GODOT_PLAYTEST.md",
]:
    source = text(rel)
    require("×1.05" in source and "×1.12" in source, f"품질 공격력·가치 계약이 문서에 없습니다: {rel}")

for rel in [
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "docs/GODOT_PLAYTEST.md",
]:
    source = text(rel)
    require("POC v0.6.2 · main · 2026.07.22.2" in source, f"최신 버전 설명이 없습니다: {rel}")
    require("POC v0.6.1 · main · 2026.07.22.1" not in source, f"활성 문서가 구형 버전을 참조합니다: {rel}")

for rel in [
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "[기획서]/00_프로젝트_허브/CHANGELOG.md",
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
]:
    require("통합 3건" in text(rel), f"제작 품질 통합 테스트 3건 기록이 최신이 아닙니다: {rel}")

playtest = text("docs/GODOT_PLAYTEST.md")
require("scenes/main/main.tscn" in playtest and "F6" in playtest, "제작 품질 수동 검증은 전체 흐름 Scene F6 진입을 안내해야 합니다.")

decisions = text("[기획서]/00_프로젝트_허브/DECISION_LOG.md")
dec_016 = decisions.find("## DEC-016 ")
dec_017 = decisions.find("## DEC-017 ")
require(dec_016 >= 0 and dec_017 > dec_016, "Decision Log는 DEC-016 뒤에 DEC-017을 배치해야 합니다.")

workflow = text(".github/workflows/godot-validation.yml")
require("test_forging_quality_enhancement.gd" in workflow, "Godot Workflow에 제작 품질 통합 테스트가 없습니다.")
require("check_forging_quality_contract.py" in workflow, "Godot Workflow에 품질 정적 계약 검사가 없습니다.")
require("godot_status=${PIPESTATUS[0]}" in workflow, "Godot Workflow가 Scene·파싱 프로세스 종료 코드를 수집해야 합니다.")
require("status=1" in workflow, "Godot Workflow가 비정상 테스트 종료를 실패 상태로 승격해야 합니다.")
require("SCRIPT ERROR:|Parse Error:|Compile Error:|ERROR:" in workflow, "Godot Workflow가 오류 로그 패턴을 실패로 판정해야 합니다.")
require("godot-validation-logs" in workflow, "Godot Workflow가 파싱·Scene·테스트 로그를 증거로 업로드해야 합니다.")

if FAILURES:
    for failure in FAILURES:
        print(f"ERROR: {failure}")
    raise SystemExit(1)

print("Forging quality contract PASSED")
