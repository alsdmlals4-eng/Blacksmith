from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []
LATEST_VERSION = "POC v0.6.3 · main · 2026.07.22.3"
OLD_ACTIVE_VERSIONS = (
    "POC v0.6.2 · main · 2026.07.22.2",
    "POC v0.6.1 · main · 2026.07.22.1",
)


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
    "fever_value_bonus_per_activation": 0.02,
    "fever_completion_value_bonus": 0.03,
    "fever_value_bonus_cap": 0.05,
}
for key, value in expected.items():
    require(session.get(key) == value, f"forging_balance.json {key}는 {value}여야 합니다.")

require(not (ROOT / "tests/check_forging_quality_contract.py").exists(), "구형 품질 전용 계약 검사가 남아 있습니다.")
require(not (ROOT / "tests/integration/test_forging_quality_enhancement.gd").exists(), "구형 품질 전용 통합 테스트가 남아 있습니다.")
require((ROOT / "tests/check_forging_result_contract.py").is_file(), "제작 결과 계약 검사가 없습니다.")
require((ROOT / "tests/integration/test_forging_result_enhancement.gd").is_file(), "제작 결과 통합 테스트가 없습니다.")
require((ROOT / "docs/port-conflicts.md").is_file(), "Godot AI 포트 충돌 안내가 없습니다.")
require((ROOT / "tests/unit/test_plugin_self_update_safety.py").is_file(), "Godot AI 자기 업데이트 안전성 테스트가 없습니다.")

source_files = list((ROOT / "scripts").rglob("*.gd")) + list((ROOT / "tests").rglob("*.gd"))
for path in source_files:
    source = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    require('"quality_multiplier"' not in source, f"구형 단일 품질 배율 필드가 남아 있습니다: {rel}")
    require('weapon_result["base_attack"] = 10' not in source, f"제작 결과 기본 공격력 덮어쓰기가 남아 있습니다: {rel}")

for rel in ["scripts/ui/game_flow_screen.gd", "scripts/ui/enhancement_test_runner.gd"]:
    source = text(rel)
    require(LATEST_VERSION in source, f"최신 버전 배지가 없습니다: {rel}")
    for old_version in OLD_ACTIVE_VERSIONS:
        require(old_version not in source, f"구형 버전 배지가 남아 있습니다: {rel}")
    require('"fever_value_bonus": 0.0' in source, f"자동/테스트 무기의 피버 보너스 0 계약이 없습니다: {rel}")
    require('"crafting_value_multiplier": 1.0' in source, f"자동/테스트 무기의 제작 가치 기준값이 없습니다: {rel}")

for rel, tokens in {
    "scripts/forging/forging_session.gd": [
        "fever_value_bonus_per_activation",
        "fever_completion_value_bonus",
        "fever_value_bonus_cap",
        "forging_completed_during_fever",
        "crafting_value_multiplier",
        "_calculate_fever_value_bonus",
    ],
    "scripts/enhancement/enhancement_session.gd": [
        "quality_value_multiplier + fever_value_bonus",
        'value_bonus_history["0"] = value_bonus_total',
        '"crafting_value_multiplier": crafting_value_multiplier',
    ],
    "scripts/ui/enhancement_screen.gd": [
        '"fever_value_bonus"',
        '"crafting_value_multiplier"',
        '"forging_completed_during_fever"',
    ],
}.items():
    source = text(rel)
    for token in tokens:
        require(token in source, f"제작 결과 계약 토큰 누락: {rel} -> {token}")

active_docs = [
    "README.md",
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
    "[기획서]/00_프로젝트_허브/ROADMAP.md",
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md",
    "docs/MVP-001_SCOPE.md",
    "docs/MVP-002_SCOPE.md",
    "docs/GODOT_PLAYTEST.md",
    "scripts/README.md",
    "tests/README.md",
]
for rel in active_docs:
    source = text(rel)
    require("+2%" in source and "+3%" in source and "+5%" in source, f"피버 가치 계약이 활성 문서에 없습니다: {rel}")
    require("공격력" in source and "정밀" in source, f"피버 비영향 경계가 활성 문서에 없습니다: {rel}")
    if rel in {"README.md", "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", "docs/GODOT_PLAYTEST.md"}:
        require(LATEST_VERSION in source, f"최신 버전 설명이 없습니다: {rel}")
        for old_version in OLD_ACTIVE_VERSIONS:
            require(old_version not in source, f"활성 문서가 구형 버전을 참조합니다: {rel}")
    require("test_forging_quality_enhancement.gd" not in source, f"구형 통합 테스트 경로가 남아 있습니다: {rel}")
    require("check_forging_quality_contract.py" not in source, f"구형 계약 검사 경로가 남아 있습니다: {rel}")

workflow = text(".github/workflows/godot-validation.yml")
require("check_forging_result_contract.py" in workflow, "Godot Workflow에 제작 결과 정적 계약 검사가 없습니다.")
require("test_forging_result_enhancement.gd" in workflow, "Godot Workflow에 제작 결과 통합 테스트가 없습니다.")
require("Forging result enhancement integration tests PASSED" in workflow, "Godot Workflow의 제작 결과 PASS 표식이 최신이 아닙니다.")
require("check_forging_quality_contract.py" not in workflow, "Godot Workflow가 구형 품질 계약 검사를 참조합니다.")
require("test_forging_quality_enhancement.gd" not in workflow, "Godot Workflow가 구형 품질 통합 테스트를 참조합니다.")

data_workflow = text(".github/workflows/data-validation.yml")
require("test_plugin_self_update_safety.py" in data_workflow, "Data Workflow에 Godot AI 자기 업데이트 안전성 테스트가 없습니다.")
require("docs/port-conflicts.md" in text("addons/godot_ai/mcp_dock.gd"), "Godot AI dock의 포트 충돌 안내 참조가 사라졌습니다.")
require("test_plugin_self_update_safety.py" in text("addons/godot_ai/plugin.gd"), "Godot AI plugin의 자기 업데이트 안전성 테스트 참조가 사라졌습니다.")

if FAILURES:
    for failure in FAILURES:
        print(f"ERROR: {failure}")
    raise SystemExit(1)

print("Forging result contract PASSED")
