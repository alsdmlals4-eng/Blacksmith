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

source_files = list((ROOT / "scripts").rglob("*.gd")) + list((ROOT / "tests").rglob("*.gd"))
for path in source_files:
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

workflow = text(".github/workflows/godot-validation.yml")
require("test_forging_quality_enhancement.gd" in workflow, "Godot Workflow에 제작 품질 통합 테스트가 없습니다.")
require("check_forging_quality_contract.py" in workflow, "Godot Workflow에 품질 정적 계약 검사가 없습니다.")

if FAILURES:
    for failure in FAILURES:
        print(f"ERROR: {failure}")
    raise SystemExit(1)

print("Forging quality contract PASSED")
