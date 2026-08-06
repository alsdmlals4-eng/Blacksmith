#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-ITEM-20260806-06"
CANON_PATH = "docs/planning/BLACKSMITH_R2_FUNCTION_RECIPE_MATERIAL_FIT_AND_PLAYTEST_CANON_2026.md"
SPEC_PATH = "docs/superpowers/specs/2026-08-06-function-recipes-material-fit-forging-playtest-design.md"
PLAN_PATH = "docs/superpowers/plans/2026-08-06-function-recipes-material-fit-forging-playtest.md"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing replacement anchor {label}: {old!r}")
    return text.replace(old, new, 1)


def append_section(path: str, marker: str, section: str) -> None:
    text = read(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + section.strip() + "\n"
        write(path, text)


def decision_contract() -> dict:
    groups = [
        "SWORD", "AXE", "BLUNT", "POLEARM", "RANGED",
        "SHIELD_SUPPORT", "LIGHT_ARMOR", "MEDIUM_ARMOR", "HEAVY_ARMOR",
    ]
    iron = {group: 0 for group in groups}
    silver = {
        "SWORD": 2, "AXE": -2, "BLUNT": -2, "POLEARM": -2, "RANGED": 2,
        "SHIELD_SUPPORT": 0, "LIGHT_ARMOR": 2, "MEDIUM_ARMOR": 0, "HEAVY_ARMOR": -2,
    }
    meteor = {
        "SWORD": 0, "AXE": 2, "BLUNT": 2, "POLEARM": 2, "RANGED": -2,
        "SHIELD_SUPPORT": 0, "LIGHT_ARMOR": -2, "MEDIUM_ARMOR": 0, "HEAVY_ARMOR": 2,
    }
    recipes = {
        "ARCANE_CONDUCTION": {
            "profiles": ["MAGIC_IMPLEMENT"],
            "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
            "primary_materials": ["silver", "meteor_iron"],
            "minimum_recognized_weight": 5,
            "bound_context": None,
            "capacity_cost": 1,
        },
        "ELEMENTAL_WARD": {
            "profiles": ["MAGIC_IMPLEMENT"],
            "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
            "primary_materials": ["silver"],
            "minimum_recognized_weight": 5,
            "bound_context": "ONE_ELEMENT",
            "capacity_cost": 1,
        },
        "ARCANE_SENSING": {
            "profiles": ["MAGIC_IMPLEMENT"],
            "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
            "primary_materials": ["meteor_iron"],
            "minimum_recognized_weight": 10,
            "bound_context": "ONE_MAGIC_SIGNATURE",
            "capacity_cost": 2,
        },
        "ENVIRONMENTAL_SEALING": {
            "profiles": ["UTILITY_IMPLEMENT", "UTILITY_GARMENT"],
            "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
            "primary_materials": ["iron", "silver"],
            "minimum_recognized_weight": 5,
            "bound_context": "ONE_ENVIRONMENT",
            "capacity_cost": 1,
        },
        "FIELD_SERVICEABILITY": {
            "profiles": ["UTILITY_IMPLEMENT"],
            "equipment_groups": ["TOOL"],
            "primary_materials": ["iron"],
            "minimum_recognized_weight": 5,
            "bound_context": None,
            "capacity_cost": 1,
        },
        "TASK_INTEGRATION": {
            "profiles": ["UTILITY_IMPLEMENT", "UTILITY_GARMENT"],
            "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
            "primary_materials": ["iron", "silver", "meteor_iron"],
            "minimum_recognized_weight": 5,
            "bound_context": "ONE_TASK",
            "capacity_cost": 1,
        },
    }
    rework = {
        "ARCANE_CONDUCTION": {"add_replace": "arcane_matrix", "rebind": None},
        "ELEMENTAL_WARD": {"add_replace": "element:<BOUND_ELEMENT>", "rebind": "element:<NEW_ELEMENT>"},
        "ARCANE_SENSING": {"add_replace": "signature:<BOUND_SIGNATURE>", "rebind": "signature:<NEW_SIGNATURE>"},
        "ENVIRONMENTAL_SEALING": {"add_replace": "environment:<BOUND_ENVIRONMENT>", "rebind": "environment:<NEW_ENVIRONMENT>"},
        "FIELD_SERVICEABILITY": {"add_replace": "service", "rebind": None},
        "TASK_INTEGRATION": {"add_replace": "task:<BOUND_TASK>", "rebind": "task:<NEW_TASK>"},
    }
    return {
        "material_role_fit_model": "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP",
        "primary_material_role_fit": {"iron": iron, "silver": silver, "meteor_iron": meteor},
        "role_fit_not_applied_equipment_groups": ["TOOL", "CLOTHING_OR_ROBE", "ACCESSORY"],
        "role_fit_creates_missing_attack_or_defense": False,
        "direct_forging_role_result_model": "DETERMINISTIC_ROLE_STRIKE_THREE_ZONE",
        "direct_forging_role_result_modifiers": {
            "OUTSIDE_GOOD_ZONE": -1, "GOOD_ZONE": 0, "PERFECT_ZONE": 1,
        },
        "automatic_forging_role_modifier": 0,
        "direct_forging_role_result_uses_rng": False,
        "role_strike_in_grade_calculation": False,
        "role_strike_applies_without_role_stat": False,
        "novice_role_result_target_percent": {
            "BELOW_EXPECTED": 20, "EXPECTED": 60, "ABOVE_EXPECTED": 20,
        },
        "novice_role_result_allowed_percent": {
            "BELOW_EXPECTED": [10, 30], "EXPECTED": [50, 70], "ABOVE_EXPECTED": [10, 30],
        },
        "distribution_semantics": "HUMAN_DIFFICULTY_TUNING_TARGET",
        "function_recipe_model": "ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY",
        "initial_function_recipes": recipes,
        "initial_recipe_success_is_deterministic": True,
        "random_function_generation_allowed": False,
        "rework_catalyst_requirements": rework,
        "catalyst_tag_projection": {"fire": ["element:fire", "environment:fire"]},
        "current_available_bound_reworks": ["ELEMENTAL_WARD_FIRE", "ENVIRONMENTAL_SEALING_FIRE"],
        "content_not_available_reworks": [
            "ARCANE_CONDUCTION", "ARCANE_SENSING", "FIELD_SERVICEABILITY", "TASK_INTEGRATION",
        ],
        "guardian_powder_is_neutral_function_catalyst": False,
        "remove_consumes_any_catalyst": True,
        "remove_consumes_precision_milestone": True,
        "replace_is_atomic": True,
        "solo_playtest_case_count": 48,
        "solo_playtest_case_breakdown": {
            "material_fit": 27, "role_strike": 9, "initial_recipes": 6, "rework_cases": 6,
        },
        "external_playtester_minimum": 3,
        "external_playtester_maximum": 5,
        "external_session_minutes": [45, 60],
        "playtest_integrity_zero_requirements": [
            "NO_DOUBLE_COUNT", "NO_RECIPELESS_FUNCTION_GENERATION", "NO_REPLACE_INTERMEDIATE_STATE_LOSS",
        ],
        "pass_required_quantitative_metrics_of_seven": 6,
        "playtest_outcomes": ["PASS", "REVISE", "REJECT"],
        "human_playtest_status": "NOT_RUN",
        "sheet_reference_tab": "42_능력치_강화_참조표",
        "sheet_reference_sections": [
            "PRIMARY_MATERIAL_ROLE_FIT", "DIRECT_FORGING_ROLE_RESULT",
            "FUNCTION_RECIPE_CATALOG", "HUMAN_PLAYTEST_PLAN",
        ],
        "sheet_is_authority": False,
        "tdd_evidence": {
            "red_verified": "PASS",
            "red_head": "f90dcdf70eabd30ecdde4def11a2ef30112a3caa",
            "red_planning_first_run": 283,
            "red_existing_pass": 76,
            "red_expected_fail": 10,
            "green_verified": "PASS",
            "protected_product_path_changes": 0,
        },
        "balance_status": "BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
        "product_implementation": "BLOCKED",
    }


def update_registry() -> None:
    path = "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
    data = json.loads(read(path))
    data["stage_status"] = "R2_BATCH_005_ACTIVE_10_OF_10"
    data["next_approval_counter"] = "10/10"
    decision = {
        "id": DECISION_ID,
        "title": "주재료 역할 적합·직접 단조 결과·기능 레시피·사람 플레이테스트 Gate",
        "status": "USER_APPROVED_R2_BATCH_005_10_OF_10_APPROVED_PENDING_MERGE",
        "refines": ["BS-ITEM-20260806-03", "BS-ITEM-20260806-04", "BS-ITEM-20260806-05", "BS-CRAFT-20260804-04"],
        "canon": CANON_PATH,
        "spec": SPEC_PATH,
        "plan": PLAN_PATH,
        "contract": decision_contract(),
    }
    current = data["current_decisions"]
    for index, item in enumerate(current):
        if item.get("id") == DECISION_ID:
            current[index] = decision
            break
    else:
        current.append(decision)
    by_id = {item.get("id"): item for item in current}
    by_id["BS-ITEM-20260806-05"]["material_recipe_and_playtest_refined_by"] = DECISION_ID
    by_id["BS-ITEM-20260806-04"]["function_recipe_refined_by"] = DECISION_ID
    by_id["BS-CRAFT-20260804-04"]["function_rework_recipe_refined_by"] = DECISION_ID
    active = data["active_batch"]
    active["approved_decisions"] = 10
    active["counter"] = "10/10"
    if DECISION_ID not in active["decisions"]:
        active["decisions"].append(DECISION_ID)
    active["status"] = "BATCH_FULL_DRAFT_PR109_APPROVED_PENDING_MERGE"
    alignment = data.setdefault("implementation_alignment", {})
    alignment["current_material_role_fit_model"] = "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP_NOT_STARTED_BLOCKED"
    alignment["current_function_recipe_model"] = "ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY_NOT_STARTED_BLOCKED"
    alignment["human_playtest_status"] = "NOT_RUN"
    write(path, json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")


def update_design_registry() -> None:
    path = "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    data = json.loads(read(path))
    data["current_batch"] = "R2_BATCH_005_10_OF_10"
    data["current_design_decision"] = DECISION_ID
    docs = data.setdefault("documents", [])
    entry = {
        "document_id": "function-recipe-material-fit-playtest-canon",
        "source_path": "../../" + CANON_PATH,
        "status": "ACTIVE",
        "source_role": "current_material_recipe_forging_and_playtest_contract",
    }
    if not any(item.get("document_id") == entry["document_id"] for item in docs if isinstance(item, dict)):
        docs.append(entry)
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def update_current_docs() -> None:
    path = "CURRENT_CONFIRMED_DECISIONS.md"
    text = read(path)
    text = replace_required(text, "현재 승인 배치: `R2_BATCH_005 / 9/10`", "현재 승인 배치: `R2_BATCH_005 / 10/10`", path)
    anchor = "- `BS-ITEM-20260806-05`: 최초 제작 역할 수치 테스트 프리셋과 강화·특수기능 변동 소유권 — `R2_BATCH_005_9_OF_10 / APPROVED_PENDING_MERGE`"
    bullet = "- `BS-ITEM-20260806-06`: 주재료 역할 적합·직접 단조 결과·기능 레시피·사람 플레이테스트 Gate — `R2_BATCH_005_10_OF_10 / APPROVED_PENDING_MERGE`"
    if bullet not in text:
        text = replace_required(text, anchor, anchor + "\n" + bullet, path)
    write(path, text)
    append_section(path, "## 16. 주재료 역할 적합·기능 레시피·사람 플레이테스트", """
## 16. 주재료 역할 적합·기능 레시피·사람 플레이테스트

- 철은 모든 역할 장비에서 `STANDARD_ROLE_FIT(0)`이다.
- 은은 검·원거리·경갑에 `+2`, 도끼·둔기·장병기·중장갑에 `-2`다.
- 운석철은 도끼·둔기·장병기·중장갑에 `+2`, 원거리·경갑에 `-2`다.
- 직접 단조 역할 타격은 `OUTSIDE / GOOD / PERFECT = -1 / 0 / +1`이며 제작 등급과 분리된다.
- 최초 기능은 `ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY` 레시피를 충족할 때만 결정적으로 생성된다.
- 현재 즉시 가용한 결속 재작업은 `ELEMENTAL_WARD(FIRE)`와 `ENVIRONMENTAL_SEALING(FIRE)`다.
- 솔로 48케이스와 외부 3~5명 검증 전까지 수치는 `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`다.
- 사람 플레이테스트: `NOT_RUN`.
- 제품 구현: `BLOCKED`.
""")

    path = "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
    text = read(path)
    text = replace_required(text, "CURRENT_CANON / R2_BATCH_005_9_OF_10", "CURRENT_CANON / R2_BATCH_005_10_OF_10", path)
    first_line = next(line for line in text.splitlines() if line.startswith("- 현재 Decision:"))
    if DECISION_ID not in first_line:
        text = text.replace(first_line, first_line + " / " + DECISION_ID, 1)
    write(path, text)
    append_section(path, "## 18. 주재료 역할 적합·기능 레시피·사람 플레이테스트", """
## 18. 주재료 역할 적합·기능 레시피·사람 플레이테스트

```text
철 = 범용 기준
은 = 경량·정밀 역할 우세
운석철 = 중량·충격 역할 우세
```

직접 단조의 역할 정밀 타격은 제작 등급과 분리된 `-1 / 0 / +1` 출력이다. 기능은 역할 프로필·장비군·주재료·최소 인정 중량·결속 맥락·용량을 모두 충족하는 레시피로만 생성한다. 현재 촉매로 가능한 결속 재작업은 불 계열 방호·환경 봉인뿐이다.

사람 플레이테스트는 솔로 `48`케이스와 외부 `3~5명`의 2단계로 진행한다. `NO_DOUBLE_COUNT / NO_RECIPELESS_FUNCTION_GENERATION / NO_REPLACE_INTERMEDIATE_STATE_LOSS`는 각각 `0건`이어야 하며 현재 상태는 `NOT_RUN`이다. 제품 구현은 `BLOCKED`다.
""")

    hub_paths = [
        "[기획서]/00_프로젝트_허브/START_HERE.md",
        "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
        "[기획서]/00_프로젝트_허브/ROADMAP.md",
        "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
        "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md",
    ]
    for hub in hub_paths:
        text = read(hub)
        text = text.replace("R2_BATCH_005_ACTIVE_9_OF_10", "R2_BATCH_005_ACTIVE_10_OF_10")
        text = text.replace("R2_BATCH_005_9_OF_10", "R2_BATCH_005_10_OF_10")
        text = text.replace("현재 승인 카운터: `9/10`", "현재 승인 카운터: `10/10`")
        write(hub, text)
        append_section(hub, DECISION_ID, f"""
## {DECISION_ID} — 배치 005 완료 Gate

- 현재 배치: `R2_BATCH_005_10_OF_10`
- 주재료 역할 적합: `EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP`
- 직접 단조 역할 결과: `DETERMINISTIC_ROLE_STRIKE_THREE_ZONE`
- 기능 레시피: `ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY`
- 사람 플레이테스트: `NOT_RUN`
- 다음 행동: PR #109 체크포인트 검토·명시적 병합 승인 대기
- 제품 구현: `BLOCKED`
""")


def refine_prior_canons() -> None:
    for path in (
        "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md",
        "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md",
        "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md",
    ):
        append_section(path, "REFINED_BY_BS-ITEM-20260806-06", f"""
## REFINED_BY_BS-ITEM-20260806-06

- 상태: `R2_BATCH_005_10_OF_10`
- 주재료별 역할 적합, 직접 단조 역할 결과, 최초·재작업 기능 레시피와 사람 플레이테스트 Gate의 정확한 계약은 `{CANON_PATH}`가 소유한다.
- 기존 수치 소유권·기능 카탈로그·정밀 이정표 배타성은 유지한다.
""")


def update_active_tests() -> None:
    for path in sorted((ROOT / "tests").glob("test_r2_*.py")) + [ROOT / "tests/test_base_v942_planning_first_adoption.py"]:
        text = path.read_text(encoding="utf-8")
        if "BS-ITEM-20260806-05" not in text or path.name == "test_r2_function_recipe_material_fit_and_playtest.py":
            continue
        text = text.replace("test_batch_005_contains_nine_approved_decisions", "test_batch_005_contains_ten_approved_decisions")
        text = text.replace("test_batch_005_is_active_at_nine_of_ten", "test_batch_005_is_active_at_ten_of_ten")
        text = text.replace("R2_BATCH_005_ACTIVE_9_OF_10", "R2_BATCH_005_ACTIVE_10_OF_10")
        text = text.replace('self.assertEqual("9/10", self.registry["next_approval_counter"])', 'self.assertEqual("10/10", self.registry["next_approval_counter"])')
        text = text.replace('self.assertEqual(9, active["approved_decisions"])', 'self.assertEqual(10, active["approved_decisions"])')
        text = text.replace('self.assertEqual("9/10", active["counter"])', 'self.assertEqual("10/10", active["counter"])')
        if DECISION_ID not in text:
            text = re.sub(
                r'(\s+"BS-ITEM-20260806-05",\n)(\s+\],\n\s+active\["decisions"\],)',
                r'\1                "BS-ITEM-20260806-06",\n\2',
                text,
            )
        path.write_text(text, encoding="utf-8")


def update_core_validator() -> None:
    path = "tests/check_project_core_alignment.py"
    text = read(path)
    replacements = {
        '"R2_BATCH_005 / 9/10",': '"R2_BATCH_005 / 10/10",',
        '"R2_BATCH_005_9_OF_10",\n        "BS-CRAFT-20260805-02",': '"R2_BATCH_005_10_OF_10",\n        "BS-CRAFT-20260805-02",',
        '"R2_BATCH_005_9_OF_10",\n        "현재 승인 카운터: `9/10`",': '"R2_BATCH_005_10_OF_10",\n        "현재 승인 카운터: `10/10`",',
        '"R2_BATCH_005_ACTIVE_9_OF_10",\n        "BS-CRAFT-20260805-02",': '"R2_BATCH_005_ACTIVE_10_OF_10",\n        "BS-CRAFT-20260805-02",',
        '"stage_status": "R2_BATCH_005_ACTIVE_9_OF_10",': '"stage_status": "R2_BATCH_005_ACTIVE_10_OF_10",',
        '"next_approval_counter": "9/10",': '"next_approval_counter": "10/10",',
        'active.get("counter") != "9/10"': 'active.get("counter") != "10/10"',
        'active batch must be R2_BATCH_005 at 9/10': 'active batch must be R2_BATCH_005 at 10/10',
        'active.get("approved_decisions") != 9': 'active.get("approved_decisions") != 10',
        '"BS-ITEM-20260806-05",\n    ]:': '"BS-ITEM-20260806-05",\n        "BS-ITEM-20260806-06",\n    ]:',
        'active batch 005 must contain the nine approved decisions': 'active batch 005 must contain the ten approved decisions',
    }
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new, 1)
    current_tuple = '        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",\n        "제품 구현: `BLOCKED`",'
    if '"BS-ITEM-20260806-06",' not in text.split('"docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"', 1)[0]:
        text = text.replace(current_tuple, '        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",\n        "BS-ITEM-20260806-06",\n        "제품 구현: `BLOCKED`",', 1)
    new_entry_anchor = '    "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md": ('
    new_entry = f'''    "{CANON_PATH}": (\n        "BS-ITEM-20260806-06",\n        "R2_BATCH_005_10_OF_10",\n        "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP",\n        "DETERMINISTIC_ROLE_STRIKE_THREE_ZONE",\n        "ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY",\n        "ELEMENTAL_WARD(FIRE)",\n        "ENVIRONMENTAL_SEALING(FIRE)",\n        "제품 구현: `BLOCKED`",\n    ),\n'''
    if CANON_PATH not in text:
        text = text.replace(new_entry_anchor, new_entry + new_entry_anchor, 1)
    marker = '    alignment = registry.get("implementation_alignment", {})'
    contract_checks = '''    final_contract = decisions.get("BS-ITEM-20260806-06", {}).get("contract", {})\n    if final_contract.get("material_role_fit_model") != "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP":\n        failures.append("primary material role-fit model is incorrect")\n    if final_contract.get("direct_forging_role_result_model") != "DETERMINISTIC_ROLE_STRIKE_THREE_ZONE":\n        failures.append("direct forging role-result model is incorrect")\n    if final_contract.get("current_available_bound_reworks") != ["ELEMENTAL_WARD_FIRE", "ENVIRONMENTAL_SEALING_FIRE"]:\n        failures.append("current available bound reworks are incorrect")\n    if final_contract.get("solo_playtest_case_count") != 48:\n        failures.append("solo playtest must contain 48 cases")\n    if final_contract.get("human_playtest_status") != "NOT_RUN":\n        failures.append("human playtest status must remain NOT_RUN")\n    if final_contract.get("product_implementation") != "BLOCKED":\n        failures.append("final batch product implementation must remain blocked")\n\n'''
    if 'final_contract = decisions.get("BS-ITEM-20260806-06"' not in text:
        text = text.replace(marker, contract_checks + marker, 1)
    write(path, text)


def update_operating_audit() -> None:
    path = "tools/audit_project_operating_system.py"
    text = read(path)
    active_anchor = '    "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md",\n'
    if CANON_PATH not in text.split("REQUIRED_ASSERTIONS", 1)[0]:
        text = text.replace(active_anchor, active_anchor + f'    "{CANON_PATH}",\n', 1)
    text = text.replace('"R2_BATCH_005 / 9/10",', '"R2_BATCH_005 / 10/10",', 1)
    text = text.replace('"stage_status":"R2_BATCH_005_ACTIVE_9_OF_10"', '"stage_status":"R2_BATCH_005_ACTIVE_10_OF_10"', 1)
    text = text.replace('"next_approval_counter":"9/10"', '"next_approval_counter":"10/10"', 1)
    text = text.replace('"R2_BATCH_005_9_OF_10",\n        "BS-CRAFT-20260805-02",', '"R2_BATCH_005_10_OF_10",\n        "BS-CRAFT-20260805-02",', 1)
    text = text.replace('"R2_BATCH_005_ACTIVE_9_OF_10",\n        "BS-CRAFT-20260805-02",', '"R2_BATCH_005_ACTIVE_10_OF_10",\n        "BS-CRAFT-20260805-02",')
    text = text.replace('"R2_BATCH_005_9_OF_10",\n        "현재 승인 카운터: `9/10`",', '"R2_BATCH_005_10_OF_10",\n        "현재 승인 카운터: `10/10`",', 1)
    registry_token = '        \'"id":"BS-ITEM-20260806-05"\','
    if '\'"id":"BS-ITEM-20260806-06"\'' not in text:
        text = text.replace(registry_token, registry_token + '\n        \'"id":"BS-ITEM-20260806-06"\',', 1)
    required_anchor = '    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": ('
    required_entry = f'''    "{CANON_PATH}": (\n        "BS-ITEM-20260806-06",\n        "R2_BATCH_005_10_OF_10",\n        "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP",\n        "DETERMINISTIC_ROLE_STRIKE_THREE_ZONE",\n        "ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY",\n        "ELEMENTAL_WARD(FIRE)",\n        "ENVIRONMENTAL_SEALING(FIRE)",\n        "제품 구현: `BLOCKED`",\n    ),\n'''
    if f'"{CANON_PATH}": (' not in text:
        text = text.replace(required_anchor, required_entry + required_anchor, 1)
    write(path, text)


def main() -> None:
    update_registry()
    update_design_registry()
    update_current_docs()
    refine_prior_canons()
    update_active_tests()
    update_core_validator()
    update_operating_audit()
    print("R2 final batch material recipes synchronization applied")


if __name__ == "__main__":
    main()
