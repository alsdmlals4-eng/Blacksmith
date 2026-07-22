from __future__ import annotations

import json
import re
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
    "weapon_base_attack": 20,
    "quality_standard_attack_multiplier": 1.0,
    "quality_standard_value_multiplier": 1.0,
    "quality_good_attack_multiplier": 1.05,
    "quality_good_value_multiplier": 1.05,
    "quality_perfect_attack_multiplier": 1.10,
    "quality_perfect_value_multiplier": 1.12,
}
for key, value in expected.items():
    require(session.get(key) == value, f"forging_balance.json {key}는 {value}여야 합니다.")

quality_attacks = {
    quality: round(float(session["weapon_base_attack"]) * float(session[f"quality_{quality}_attack_multiplier"]))
    for quality in ("standard", "good", "perfect")
}
require(
    quality_attacks == {"standard": 20, "good": 21, "perfect": 22},
    f"품질별 실제 정수 공격력이 20/21/22로 구분되어야 합니다: {quality_attacks}",
)
require(
    quality_attacks["standard"] < quality_attacks["good"] < quality_attacks["perfect"],
    "STANDARD/GOOD/PERFECT 공격력이 실제 정수 결과에서도 엄격히 증가해야 합니다.",
)

enhancement_balance = json.loads(text("data/crafting/enhancement_balance.json"))
require(enhancement_balance.get("growth", {}).get("base_attack") == 20, "강화 기본 공격력 fallback은 20이어야 합니다.")
require(enhancement_balance.get("economy", {}).get("attack_price_scale") == 5.3, "공격력 단위 변경 뒤 가격 곡선 보정값은 5.3이어야 합니다.")
old_baseline_price = 100.0 + pow(10.0, 1.18) * 12.0
new_baseline_price = 100.0 + pow(20.0, 1.18) * 5.3
require(abs(old_baseline_price - new_baseline_price) < 1.0, "공격력 단위 변경 뒤 보통 철검 기준 판매가가 1G 이상 변하면 안 됩니다.")

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
    stale_attack = re.search(
        r'(?:(?:raw_)?base_attack|weapon_base_attack|final_attack)[^\n]{0,48}(?::|==|,|\))\s*10(?:\D|$)',
        source,
    )
    require(stale_attack is None, f"구형 철검 기본 공격력 10 참조가 남아 있습니다: {rel}")

for rel in ["scripts/ui/game_flow_screen.gd", "scripts/ui/enhancement_test_runner.gd"]:
    source = text(rel)
    require('POC v0.6.3 · main · 2026.07.22.3' in source, f"최신 버전 배지가 없습니다: {rel}")
    require('POC v0.6.2 · main · 2026.07.22.2' not in source, f"구형 버전 배지가 남아 있습니다: {rel}")

for rel in [
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md",
    "docs/MVP-001_SCOPE.md",
    "docs/MVP-002_SCOPE.md",
    "docs/GODOT_PLAYTEST.md",
]:
    source = text(rel)
    require("×1.05" in source and "×1.12" in source, f"품질 공격력·가치 계약이 문서에 없습니다: {rel}")
    require("20" in source and "21" in source and "22" in source, f"품질별 실제 공격력 20/21/22가 문서에 없습니다: {rel}")

for rel in [
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "docs/GODOT_PLAYTEST.md",
]:
    source = text(rel)
    require("POC v0.6.3 · main · 2026.07.22.3" in source, f"최신 버전 설명이 없습니다: {rel}")
    require("POC v0.6.2 · main · 2026.07.22.2" not in source, f"활성 문서가 구형 버전을 참조합니다: {rel}")

for rel in [
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "[기획서]/00_프로젝트_허브/CHANGELOG.md",
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
]:
    require("통합 4건" in text(rel), f"제작 품질 통합 테스트 4건 기록이 최신이 아닙니다: {rel}")

integration_test = text("tests/integration/test_forging_quality_enhancement.gd")
require('base_attack) == 20' in integration_test, "통합 테스트가 보통 마감 공격력 20을 검증해야 합니다.")
require('base_attack) == 21' in integration_test, "통합 테스트가 좋은 마감 공격력 21을 검증해야 합니다.")
require('base_attack) == 22' in integration_test, "통합 테스트가 완벽한 마감 공격력 22를 검증해야 합니다.")
require(
    'good_screen.session.base_attack < perfect_screen.session.base_attack' in integration_test,
    "통합 테스트가 GOOD/PERFECT 실제 공격력 차이를 검증해야 합니다.",
)
require(
    'good_screen.session.progression_attack < perfect_screen.session.progression_attack' in integration_test,
    "통합 테스트가 강화 뒤 GOOD/PERFECT 공격력 차이를 검증해야 합니다.",
)

runner_contracts = {
    "tests/unit/test_enhancement_session.gd": "EnhancementSession tests PASSED (12 cases)",
    "tests/unit/test_workshop_resources.gd": "WorkshopResources tests PASSED (7 cases)",
    "tests/integration/test_manual_enhancement_economy.gd": "Manual enhancement economy integration tests PASSED (2 cases)",
    "tests/integration/test_forging_quality_enhancement.gd": "Forging quality enhancement integration tests PASSED (4 cases)",
}
for rel, marker in runner_contracts.items():
    source = text(rel)
    success_flow = re.search(
        rf'if failures\.is_empty\(\):\s+print\("{re.escape(marker)}"\)\s+quit\(0\)\s+return',
        source,
        re.DOTALL,
    )
    require(success_flow is not None, f"성공한 Godot 테스트 러너가 quit(0) 뒤 즉시 return해야 합니다: {rel}")
    require("quit(1)" in source, f"실패한 Godot 테스트 러너가 종료코드 1을 반환해야 합니다: {rel}")

playtest = text("docs/GODOT_PLAYTEST.md")
require("scenes/main/main.tscn" in playtest and "F6" in playtest, "제작 품질 수동 검증은 전체 흐름 Scene F6 진입을 안내해야 합니다.")

decisions = text("[기획서]/00_프로젝트_허브/DECISION_LOG.md")
dec_017 = decisions.find("## DEC-017 ")
dec_018 = decisions.find("## DEC-018 ")
require(dec_017 >= 0 and dec_018 > dec_017, "Decision Log는 DEC-017 뒤에 DEC-018을 배치해야 합니다.")

workflow = text(".github/workflows/godot-validation.yml")
require("test_forging_quality_enhancement.gd" in workflow, "Godot Workflow에 제작 품질 통합 테스트가 없습니다.")
require("check_forging_quality_contract.py" in workflow, "Godot Workflow에 품질 정적 계약 검사가 없습니다.")
require("godot_status=${PIPESTATUS[0]}" in workflow, "Godot Workflow가 Scene·파싱 프로세스 종료 코드를 수집해야 합니다.")
nonzero_exit_guard = re.search(
    r'if \[ "\$forging_status".*?"\$forging_quality_status" -ne 0 \]; then\s+'
    r'echo .*?\s+status=1\s+fi',
    workflow,
    re.DOTALL,
)
require(nonzero_exit_guard is not None, "Godot Workflow가 모델 테스트 비정상 종료를 실패 상태로 승격해야 합니다.")
require('economy.get("attack_price_scale", 5.3)' in text("scripts/enhancement/enhancement_session.gd"), "강화 가격 계산 fallback이 5.3이어야 합니다.")
require('snapshot.get("base_attack", 20)' in text("scripts/ui/enhancement_screen.gd"), "보관 기록 최종 공격력 fallback이 최신 기본 공격력을 사용해야 합니다.")
require("SCRIPT ERROR:|Parse Error:|Compile Error:|ERROR:" in workflow, "Godot Workflow가 오류 로그 패턴을 실패로 판정해야 합니다.")
require("godot-validation-logs" in workflow, "Godot Workflow가 파싱·Scene·테스트 로그를 증거로 업로드해야 합니다.")

if FAILURES:
    for failure in FAILURES:
        print(f"ERROR: {failure}")
    raise SystemExit(1)

print("Forging quality contract PASSED")
