from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION = "BS-CUSTOMER-20260805-01"
CONTENT_DECISION = "BS-CONTENT-20260804-02"

registry_path = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
decisions = {item["id"]: item for item in registry["current_decisions"]}

refines = decisions[DECISION].setdefault("refines", [])
if CONTENT_DECISION not in refines:
    refines.insert(0, CONTENT_DECISION)

decisions[CONTENT_DECISION]["contract"]["noble_optional_secondary_stat"] = "DEXTERITY"
registry.setdefault("tdd_evidence", {})["customer_equipment_archetype_identifier_red"] = {
    "commit": "ef19658ab0bfae74a673eb0e4740384842686ee9",
    "planning_first_run": 143,
    "status": "EXPECTED_FAILURE",
}
registry_path.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

canon_path = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md"
canon = canon_path.read_text(encoding="utf-8")
canon = canon.replace(
    "- 정제 대상: `BS-CUSTOMER-20260803-01`, `BS-CUSTOMER-20260803-02`의 고객 능력 구조",
    "- 정제 대상: `BS-CONTENT-20260804-02`, `BS-CUSTOMER-20260803-01`, `BS-CUSTOMER-20260803-02`의 고객 능력 구조",
)
needle = "근력은 작품 공격력을 직접 더하지 않고, 기량도 작품 공격·방어 능력치를 중복 생성하지 않는다."
replacement = needle + "\n\n기존 방문고객 정본의 보조 능력치 식별자 `SKILL`은 현재 기초 능력치 식별자 `DEXTERITY`로 정제한다. 한국어 표시는 계속 `기량`을 사용한다."
if "보조 능력치 식별자 `SKILL`" not in canon:
    canon = canon.replace(needle, replacement)
canon_path.write_text(canon.rstrip() + "\n", encoding="utf-8")

for one_shot in (
    ROOT / ".github/scripts/apply_customer_archetype_stat_fix.py",
    ROOT / ".github/workflows/apply-customer-archetype-stat-fix.yml",
):
    if one_shot.exists():
        one_shot.unlink()
