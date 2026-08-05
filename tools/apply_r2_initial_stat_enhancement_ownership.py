#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-ITEM-20260806-05"
CANON_PATH = "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md"
SPEC_PATH = "docs/superpowers/specs/2026-08-06-initial-role-stat-preset-and-enhancement-function-ownership-design.md"
PLAN_PATH = "docs/superpowers/plans/2026-08-06-initial-role-stat-preset-and-enhancement-function-ownership.md"
SHEET_TAB = "42_능력치_강화_참조표"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def write(relative: str, text: str) -> None:
    (ROOT / relative).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise RuntimeError(f"missing replacement anchor for {label}: {old!r}")


def append_once(relative: str, marker: str, block: str) -> None:
    text = read(relative)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write(relative, text)


def update_registry() -> None:
    relative = "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
    data = json.loads(read(relative))
    data["stage_status"] = "R2_BATCH_005_ACTIVE_9_OF_10"
    data["next_approval_counter"] = "9/10"
    data["product_implementation"] = "BLOCKED"

    active = data["active_batch"]
    active["approved_decisions"] = 9
    active["counter"] = "9/10"
    if DECISION_ID not in active["decisions"]:
        active["decisions"].append(DECISION_ID)

    contract = {
        "crafted_role_stat_formula": "MAX_ZERO_BASE_PLUS_MATERIAL_FIT_PLUS_DIRECT_FORGING",
        "base_item_role_base": {
            "SWORD": 5,
            "RANGED": 5,
            "AXE": 10,
            "BLUNT": 10,
            "POLEARM": 15,
            "SHIELD_SUPPORT": 5,
            "LIGHT_ARMOR": 5,
            "MEDIUM_ARMOR": 10,
            "HEAVY_ARMOR": 15,
            "TOOL": None,
            "CLOTHING_OR_ROBE": None,
            "ACCESSORY": None,
        },
        "primary_material_role_fit_modifier": {
            "LOW_ROLE_FIT": -2,
            "STANDARD_ROLE_FIT": 0,
            "HIGH_ROLE_FIT": 2,
        },
        "direct_forging_role_modifier": {
            "BELOW_EXPECTED_DIRECT_FORGING": -1,
            "EXPECTED_DIRECT_FORGING": 0,
            "ABOVE_EXPECTED_DIRECT_FORGING": 1,
        },
        "balance_status": "BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
        "general_enhancement_owner": "ENHANCEMENT_LEVEL_AND_EVENT_SUCCESS_OWNER",
        "general_event_success_bonus_per_level_pp": 1,
        "general_enhancement_auto_changed_item_fields": [],
        "general_enhancement_forbidden_auto_fields": [
            "ATTACK",
            "DEFENSE",
            "WEIGHT",
            "DURABILITY",
            "HANDLING",
            "ARTISTRY",
            "MAGIC_FUNCTION_CAPACITY",
            "UTILITY_CAPACITY",
            "SPECIAL_FUNCTIONS",
        ],
        "precision_output_lanes": ["STAT_METHOD", "FUNCTION_REWORK"],
        "precision_output_lanes_mutually_exclusive": True,
        "precision_method_outputs": {
            "EDGE_REINFORCEMENT": {
                "lane": "STAT_METHOD",
                "changed_field": "APPROVED_ENHANCEMENT_ATTACK_OUTPUT",
                "delta": 5,
            },
            "SHOCK_ABSORPTION": {
                "lane": "STAT_METHOD",
                "changed_field": "APPROVED_ENHANCEMENT_DEFENSE_OUTPUT",
                "delta": 5,
            },
            "BALANCE_TUNING": {
                "lane": "STAT_METHOD",
                "changed_field": "HANDLING",
                "delta": 5,
            },
            "ARTISTIC_FINISH": {
                "lane": "STAT_METHOD",
                "changed_field": "ARTISTRY",
                "delta": 5,
            },
            "LIGHTWEIGHTING": {
                "lane": "STAT_METHOD",
                "changed_field": "CURRENT_WEIGHT",
                "delta": -5,
                "preserves_allocated_output": True,
            },
            "WEIGHTING": {
                "lane": "STAT_METHOD",
                "changed_field": "CURRENT_WEIGHT",
                "delta": 5,
                "peak_only_role_output": True,
            },
            "ENVIRONMENTAL_TREATMENT": {
                "lane": "FUNCTION_REWORK",
                "changed_field": "SPECIAL_FUNCTIONS",
                "operations": ["ADD", "REPLACE", "REBIND", "REMOVE"],
                "item_stat_delta": 0,
            },
        },
        "post_craft_function_owner": "FUNCTION_REWORK",
        "function_rework_actions": ["ADD", "REPLACE", "REBIND", "REMOVE"],
        "function_rework_requires_precision_milestone": True,
        "function_rework_consumes_milestone": True,
        "function_rework_milestone_refund_allowed": False,
        "failed_function_rework_preserves_previous_state": True,
        "duplicate_function_id_allowed": False,
        "hidden_function_level_allowed": False,
        "approved_function_recipe_required": True,
        "weight_capacity_auto_grants_function": False,
        "item_change_ledger_fields": [
            "item_uid",
            "source_action_id",
            "source_owner",
            "enhancement_level_before",
            "enhancement_level_after",
            "changed_field",
            "value_before",
            "value_after",
            "delta_or_operation",
            "precision_milestone",
            "decision_id",
        ],
        "one_changed_field_per_ledger_row": True,
        "multi_field_action_uses_shared_source_action_id": True,
        "customer_user_stat_reference": {
            "STRENGTH": {"range": [1, 10], "use": "MAXIMUM_LOAD_STRENGTH_X_10"},
            "DEXTERITY": {"range": [1, 10], "use": "RELEVANT_EVENT_CAPABILITY"},
            "CONSTITUTION": {"range": [1, 10], "use": "RELEVANT_EVENT_CAPABILITY"},
            "JUDGMENT": {"range": [1, 10], "use": "EVENT_OR_FUNCTION_CONTROL"},
            "EQUIPMENT_PROFICIENCY": {"range": [0, 3], "use": "MINUS10_0_PLUS5_PLUS10_PP"},
            "MAGIC_APTITUDE": {"range": [0, 10], "use": "MAGIC_FUNCTION_ELIGIBILITY_AND_RISK"},
            "MAGIC_AFFINITY_TAGS": {"range": [0, 2], "use": "BOUND_FUNCTION_COMPATIBILITY"},
        },
        "customer_stats_modify_item_attack_or_defense": False,
        "relevant_capability_met_bonus_pp": 5,
        "sheet_reference_tab": SHEET_TAB,
        "sheet_reference_sections": [
            "ITEM_WEAPON_STATS",
            "CUSTOMER_USER_STATS",
            "ENHANCEMENT_DELTAS",
            "SPECIAL_FUNCTION_REWORK",
        ],
        "sheet_is_authority": False,
        "product_implementation": "BLOCKED",
    }

    decision = {
        "id": DECISION_ID,
        "title": "최초 제작 역할 수치 테스트 프리셋과 강화·특수기능 변동 소유권",
        "status": "USER_APPROVED_R2_BATCH_005_9_OF_10_APPROVED_PENDING_MERGE",
        "refines": [
            "BS-ITEM-20260806-04",
            "BS-CRAFT-20260804-04",
            "BS-CUSTOMER-20260806-01",
            "BS-ITEM-20260806-03",
            "BS-CRAFT-20260805-02",
        ],
        "canon": CANON_PATH,
        "spec": SPEC_PATH,
        "plan": PLAN_PATH,
        "contract": contract,
    }

    decisions = data["current_decisions"]
    for index, item in enumerate(decisions):
        if item.get("id") == DECISION_ID:
            decisions[index] = decision
            break
    else:
        decisions.append(decision)

    by_id = {item.get("id"): item for item in decisions if isinstance(item, dict)}
    refinement_fields = {
        "BS-ITEM-20260806-04": "stat_delta_and_function_rework_refined_by",
        "BS-CRAFT-20260804-04": "exact_precision_output_refined_by",
        "BS-CUSTOMER-20260806-01": "enhancement_delta_refined_by",
        "BS-ITEM-20260806-03": "initial_role_stat_and_delta_refined_by",
        "BS-CRAFT-20260805-02": "artistic_finish_delta_refined_by",
    }
    for decision_id, field in refinement_fields.items():
        if decision_id in by_id:
            by_id[decision_id][field] = DECISION_ID

    write(relative, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def update_design_registry() -> None:
    relative = "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    data = json.loads(read(relative))
    data["current_batch"] = "R2_BATCH_005_9_OF_10"
    data["current_design_decision"] = DECISION_ID
    data["product_implementation"] = "BLOCKED"
    data["current_reference_sheet_tab"] = SHEET_TAB

    documents = data["documents"]
    additions = [
        {
            "document_id": "initial-role-stat-preset-enhancement-function-ownership-canon",
            "source_path": "../../" + CANON_PATH,
            "status": "ACTIVE",
            "source_role": "current_initial_role_stat_and_enhancement_function_ownership_contract",
        },
        {
            "document_id": "initial-role-stat-preset-enhancement-function-ownership-design",
            "source_path": "../../" + SPEC_PATH,
            "status": "ACTIVE",
            "source_role": "approved_design_input_for_bs_item_20260806_05",
        },
        {
            "document_id": "initial-role-stat-preset-enhancement-function-ownership-plan",
            "source_path": "../../" + PLAN_PATH,
            "status": "ACTIVE",
            "source_role": "executed_canon_plan_for_bs_item_20260806_05",
        },
    ]
    existing_ids = {item.get("document_id") for item in documents if isinstance(item, dict)}
    for item in additions:
        if item["document_id"] not in existing_ids:
            documents.append(item)

    write(relative, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def update_current_documents() -> None:
    relative = "CURRENT_CONFIRMED_DECISIONS.md"
    text = read(relative)
    text = replace_once(text, "> 현재 승인 배치: `R2_BATCH_005 / 8/10`", "> 현재 승인 배치: `R2_BATCH_005 / 9/10`", relative)
    bullet_04 = "- `BS-ITEM-20260806-04`: 작품군 단일 역할 원수치와 최초 마법·유틸리티 기능 카탈로그 — `R2_BATCH_005_8_OF_10 / APPROVED_PENDING_MERGE`"
    bullet_05 = "- `BS-ITEM-20260806-05`: 최초 제작 역할 수치 테스트 프리셋과 강화·특수기능 변동 소유권 — `R2_BATCH_005_9_OF_10 / APPROVED_PENDING_MERGE`"
    if bullet_05 not in text:
        text = replace_once(text, bullet_04, bullet_04 + "\n" + bullet_05, relative + " decision bullet")
    write(relative, text)
    append_once(
        relative,
        "<!-- BS-ITEM-20260806-05 CURRENT AUTHORITY -->",
        """
<!-- BS-ITEM-20260806-05 CURRENT AUTHORITY -->
## 현재 작품 역할 수치·강화 변동 소유권

- Decision: `BS-ITEM-20260806-05 / R2_BATCH_005_9_OF_10`
- 통합 변동 장부: `GENERAL_ENHANCEMENT / STAT_METHOD / FUNCTION_REWORK`
- 최초 역할 수치: `장비군 기준값 5·10·15 + 주재료 -2·0·+2 + 직접 단조 -1·0·+1`
- 일반 강화: 강화 단계와 사건 성공률 `+1%p/단계`만 소유하고 작품 원수치를 자동 변경하지 않음
- 정밀강화: 공격·방어·취급·예술성 `+5`, 경량화·중량화 `±5`, 환경 기능 재작업 중 한 패키지만 선택
- 기능 재작업: `ADD / REPLACE / REBIND / REMOVE`, 정밀 이정표 소비, 실패 시 기존 기능 보존
- Google Sheet 미러: `42_능력치_강화_참조표`
- 밸런스: `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`
- 제품 구현: `BLOCKED`
""",
    )

    relative = "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
    text = read(relative)
    text = replace_once(text, "- 상태: `CURRENT_CANON / R2_BATCH_005_8_OF_10`", "- 상태: `CURRENT_CANON / R2_BATCH_005_9_OF_10`", relative)
    if "BS-ITEM-20260806-05" not in text.split("\n", 8)[0:8]:
        text = text.replace(" / BS-ITEM-20260806-04", " / BS-ITEM-20260806-04 / BS-ITEM-20260806-05", 1)
    write(relative, text)
    append_once(
        relative,
        "<!-- BS-ITEM-20260806-05 CURRENT GAME BIBLE -->",
        """
<!-- BS-ITEM-20260806-05 CURRENT GAME BIBLE -->
## 작품 역할 수치와 통합 변동 장부

```text
CRAFTED_ROLE_STAT = max(0, 장비군 기준값 + 주재료 적합 보정 + 직접 단조 보정)
장비군 기준값 = 5 / 10 / 15
주재료 적합 = -2 / 0 / +2
직접 단조 = -1 / 0 / +1
```

일반 강화는 강화 단계와 사건 성공률만 바꾼다. 작품 공격·방어·중량·내구·취급·예술성·기능 용량·기능 목록은 자동 변경하지 않는다. 실제 작품 수치 변화는 정밀강화 `STAT_METHOD`, 기능 목록 변화는 `FUNCTION_REWORK`가 소유한다. 한 이정표에서 두 차선을 동시에 받을 수 없다.

변경은 `ITEM_CHANGE_LEDGER_ENTRY`로 기록한다. 조회용 Google Sheet 탭은 `42_능력치_강화_참조표`이며 GitHub 정본보다 우선하지 않는다. 정확한 값은 `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`, 제품 구현은 `BLOCKED`다.
""",
    )

    hub_updates = {
        "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": [
            ("- 단계: `R2_CORE_SESSION_META_LOOP / R2_BATCH_005_8_OF_10`", "- 단계: `R2_CORE_SESSION_META_LOOP / R2_BATCH_005_9_OF_10`"),
            ("- 현재 승인 카운터: `8/10`", "- 현재 승인 카운터: `9/10`"),
        ],
        "[기획서]/00_프로젝트_허브/START_HERE.md": [
            ("R2_STATUS: R2_BATCH_005_ACTIVE_8_OF_10", "R2_STATUS: R2_BATCH_005_ACTIVE_9_OF_10"),
        ],
        "[기획서]/00_프로젝트_허브/ROADMAP.md": [
            ("R2_BATCH_005_ACTIVE_8_OF_10", "R2_BATCH_005_ACTIVE_9_OF_10"),
        ],
        "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": [
            ("R2_BATCH_005_ACTIVE_8_OF_10", "R2_BATCH_005_ACTIVE_9_OF_10"),
        ],
        "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": [
            ("R2_BATCH_005_8_OF_10", "R2_BATCH_005_9_OF_10"),
        ],
    }
    block = """
<!-- BS-ITEM-20260806-05 CURRENT HUB ROUTING -->
## 현재 9/10 작품 수치·강화 변동 Gate

- Decision: `BS-ITEM-20260806-05 / R2_BATCH_005_9_OF_10`
- 권위 정본: `docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md`
- 조회 시트: `42_능력치_강화_참조표`
- 핵심: 최초 역할 수치 `5·10·15`, 일반 강화 원수치 자동 변동 없음, 정밀강화 수치 패키지와 기능 재작업 상호배타, 통합 변동 장부 필수
- 다음 Gate: 작품별 특수기능 제작·재작업 레시피와 테스트 프리셋 플레이테스트 계획
- 제품 구현: `BLOCKED`
"""
    for relative, replacements in hub_updates.items():
        text = read(relative)
        for old, new in replacements:
            text = replace_once(text, old, new, relative)
        write(relative, text)
        append_once(relative, "<!-- BS-ITEM-20260806-05 CURRENT HUB ROUTING -->", block)


def append_refinements() -> None:
    refinements = {
        "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-05 -->
## [현재 후속 정제] 최초 역할 수치와 기능 재작업 소유권

- `REFINED_BY_BS-ITEM-20260806-05`
- `R2_BATCH_005_9_OF_10`
- 최초 역할 수치는 장비군 기준값 `5 / 10 / 15`, 주재료 적합 `-2 / 0 / +2`, 직접 단조 `-1 / 0 / +1`의 합으로 정한다.
- 제작 후 특수기능 목록 변경은 `FUNCTION_REWORK`만 소유한다.
- 일반 강화와 남는 기능 용량은 기능을 자동 생성하지 않는다.
""",
        "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-05 -->
## [현재 후속 정제] 정밀강화 수치 패키지와 기능 재작업 차선

- `REFINED_BY_BS-ITEM-20260806-05`
- `R2_BATCH_005_9_OF_10`
- `PRECISION_OUTPUT_LANE = STAT_METHOD | FUNCTION_REWORK`이며 같은 이정표에서 두 차선을 동시에 적용하지 않는다.
- 공격·방어·취급·예술성 테스트 변동은 `+5`, 중량은 `±5`다.
- `ENVIRONMENTAL_TREATMENT`는 승인 환경 기능 레시피가 있을 때 `FUNCTION_REWORK` 차선을 사용하며 별도 수치 패키지를 동시에 주지 않는다.
- 촉매는 계속 촉매 수식어 계보·확률을 담당하며 기능 목록을 자동 변경하지 않는다.
""",
        "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-05 -->
## [현재 후속 정제] 일반 강화와 작품 원수치 경계

- `REFINED_BY_BS-ITEM-20260806-05`
- `R2_BATCH_005_9_OF_10`
- 일반 강화는 강화 단계와 일반 사건 성공률 `+1%p/단계`만 소유한다.
- 일반 강화가 공격·방어·중량·내구·취급·예술성·기능 용량·기능 목록을 자동 변경하지 않는다.
- 고객 능력치는 작품 공격·방어에 직접 합산하지 않는다.
""",
        "docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-05 -->
## [현재 후속 정제] 최초 제작 수치와 중량 출력 장부 분리

- `REFINED_BY_BS-ITEM-20260806-05`
- `R2_BATCH_005_9_OF_10`
- 최초 제작 역할 수치와 중량 기반 출력은 별도 장부에 기록한다.
- 중량화는 새 인정 최고 중량일 때만 기존 프로필에 따라 공격·방어 `+5` 또는 기능 용량 `+1`을 준다.
- 같은 중량 원천을 최초 제작 수치에 다시 포함하지 않는다.
""",
        "docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-05 -->
## [현재 후속 정제] 예술 마감의 테스트 변동

- `REFINED_BY_BS-ITEM-20260806-05`
- `R2_BATCH_005_9_OF_10`
- 성공한 `ARTISTIC_FINISH` 정밀강화의 테스트 변동은 `ARTISTRY +5`다.
- 예술 마감은 해당 정밀 이정표 기회를 소비하며 공격·방어 수치 패키지를 동시에 주지 않는다.
- 정확한 값은 `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`다.
""",
    }
    for relative, block in refinements.items():
        append_once(relative, "<!-- REFINED_BY_BS-ITEM-20260806-05 -->", block)


def update_contract_tests() -> None:
    for path in sorted((ROOT / "tests").glob("test_r2_*.py")):
        if path.name == "test_r2_initial_role_stat_preset_and_enhancement_function_ownership.py":
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        text = text.replace("test_batch_005_contains_eight_approved_decisions", "test_batch_005_contains_nine_approved_decisions")
        text = text.replace("test_batch_005_is_active_at_eight_of_ten", "test_batch_005_is_active_at_nine_of_ten")
        text = text.replace('"R2_BATCH_005_ACTIVE_8_OF_10", self.registry["stage_status"]', '"R2_BATCH_005_ACTIVE_9_OF_10", self.registry["stage_status"]')
        text = text.replace('"8/10", self.registry["next_approval_counter"]', '"9/10", self.registry["next_approval_counter"]')
        text = text.replace('self.assertEqual(8, active["approved_decisions"])', 'self.assertEqual(9, active["approved_decisions"])')
        text = text.replace('self.assertEqual("8/10", active["counter"])', 'self.assertEqual("9/10", active["counter"])')
        text = text.replace('self.assertIn("현재 승인 카운터: `8/10`", active)', 'self.assertIn("현재 승인 카운터: `9/10`", active)')
        text = text.replace('self.assertIn("R2_BATCH_005 / 8/10", read_or_empty(CURRENT))', 'self.assertIn("R2_BATCH_005 / 9/10", read_or_empty(CURRENT))')
        pattern = re.compile(r'(\n\s+"BS-ITEM-20260806-04",\n)(\s+\],\n\s+active\["decisions"\],)')
        if "BS-ITEM-20260806-05" not in text:
            text = pattern.sub(r'\1                "BS-ITEM-20260806-05",\n\2', text, count=1)
        else:
            # Existing files can mention the Decision only in authority tokens later; inspect the active-list window.
            match = pattern.search(text)
            if match and "BS-ITEM-20260806-05" not in match.group(0):
                text = pattern.sub(r'\1                "BS-ITEM-20260806-05",\n\2', text, count=1)
        if text != original:
            path.write_text(text, encoding="utf-8")

    path = ROOT / "tests/test_base_v942_planning_first_adoption.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("test_batch_005_is_active_at_eight_of_ten", "test_batch_005_is_active_at_nine_of_ten")
    text = text.replace('"R2_BATCH_005_ACTIVE_8_OF_10", registry["stage_status"]', '"R2_BATCH_005_ACTIVE_9_OF_10", registry["stage_status"]')
    text = text.replace('"8/10", registry["next_approval_counter"]', '"9/10", registry["next_approval_counter"]')
    text = text.replace('self.assertEqual(8, active["approved_decisions"])', 'self.assertEqual(9, active["approved_decisions"])')
    text = text.replace('self.assertEqual("8/10", active["counter"])', 'self.assertEqual("9/10", active["counter"])')
    pattern = re.compile(r'(\n\s+"BS-ITEM-20260806-04",\n)(\s+\],\n\s+active\["decisions"\],)')
    match = pattern.search(text)
    if match and "BS-ITEM-20260806-05" not in match.group(0):
        text = pattern.sub(r'\1                "BS-ITEM-20260806-05",\n\2', text, count=1)
    path.write_text(text, encoding="utf-8")


def update_core_alignment() -> None:
    relative = "tests/check_project_core_alignment.py"
    text = read(relative)
    replacements = [
        ('"R2_BATCH_005 / 7/10",', '"R2_BATCH_005 / 9/10",'),
        ('"stage_status": "R2_BATCH_005_ACTIVE_8_OF_10",', '"stage_status": "R2_BATCH_005_ACTIVE_9_OF_10",'),
        ('"next_approval_counter": "8/10",', '"next_approval_counter": "9/10",'),
        ('active.get("counter") != "8/10"', 'active.get("counter") != "9/10"'),
        ('active batch must be R2_BATCH_005 at 8/10', 'active batch must be R2_BATCH_005 at 9/10'),
        ('active.get("approved_decisions") != 8', 'active.get("approved_decisions") != 9'),
        ('active batch 005 must contain the eight approved decisions', 'active batch 005 must contain the nine approved decisions'),
        ('"현재 승인 카운터: `8/10`",', '"현재 승인 카운터: `9/10`",'),
        ('"R2_BATCH_005_ACTIVE_8_OF_10",', '"R2_BATCH_005_ACTIVE_9_OF_10",'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    active_list_anchor = '        "BS-ITEM-20260806-04",\n    ]:'
    if active_list_anchor in text and '        "BS-ITEM-20260806-05",\n    ]:' not in text:
        text = text.replace(active_list_anchor, '        "BS-ITEM-20260806-04",\n        "BS-ITEM-20260806-05",\n    ]:', 1)
    new_required = '''    "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md": (
        "BS-ITEM-20260806-05",
        "R2_BATCH_005_9_OF_10",
        "MAX_ZERO_BASE_PLUS_MATERIAL_FIT_PLUS_DIRECT_FORGING",
        "GENERAL_ENHANCEMENT",
        "FUNCTION_REWORK",
        "ITEM_CHANGE_LEDGER_ENTRY",
        "42_능력치_강화_참조표",
        "제품 구현: `BLOCKED`",
    ),
'''
    anchor = '}\n\nFORBIDDEN = {'
    if new_required not in text:
        if anchor not in text:
            raise RuntimeError("core alignment dictionary anchor missing")
        text = text.replace(anchor, new_required + anchor, 1)
    write(relative, text)


def update_operating_audit() -> None:
    relative = "tools/audit_project_operating_system.py"
    text = read(relative)
    active_doc = '    "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md",\n'
    new_active_doc = '    "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md",\n'
    if new_active_doc not in text:
        text = text.replace(active_doc, active_doc + new_active_doc, 1)

    targeted = [
        ('"R2_BATCH_005 / 8/10",', '"R2_BATCH_005 / 9/10",'),
        ('\'"stage_status":"R2_BATCH_005_ACTIVE_8_OF_10"\',', '\'"stage_status":"R2_BATCH_005_ACTIVE_9_OF_10"\','),
        ('\'"next_approval_counter":"8/10"\',', '\'"next_approval_counter":"9/10"\','),
        ('"현재 승인 카운터: `8/10`",', '"현재 승인 카운터: `9/10`",'),
        ('"R2_BATCH_005_ACTIVE_8_OF_10",', '"R2_BATCH_005_ACTIVE_9_OF_10",'),
    ]
    for old, new in targeted:
        text = text.replace(old, new)

    registry_id_anchor = '        \'"id":"BS-ITEM-20260806-04"\',\n'
    registry_new = '        \'"id":"BS-ITEM-20260806-05"\',\n        \'"crafted_role_stat_formula":"MAX_ZERO_BASE_PLUS_MATERIAL_FIT_PLUS_DIRECT_FORGING"\',\n        \'"post_craft_function_owner":"FUNCTION_REWORK"\',\n        \'"sheet_reference_tab":"42_능력치_강화_참조표"\',\n'
    if registry_new not in text:
        text = text.replace(registry_id_anchor, registry_id_anchor + registry_new, 1)

    new_required = '''    "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md": (
        "BS-ITEM-20260806-05",
        "R2_BATCH_005_9_OF_10",
        "MAX_ZERO_BASE_PLUS_MATERIAL_FIT_PLUS_DIRECT_FORGING",
        "GENERAL_ENHANCEMENT",
        "PRECISION_OUTPUT_LANE",
        "FUNCTION_REWORK",
        "ITEM_CHANGE_LEDGER_ENTRY",
        "42_능력치_강화_참조표",
        "제품 구현: `BLOCKED`",
    ),
'''
    anchor = '}\n\nHISTORICAL_ASSERTIONS = {'
    if new_required not in text:
        if anchor not in text:
            # Older file uses a different next dictionary name; use first dictionary close before class declarations.
            alt = '}\n\n@dataclass'
            if alt not in text:
                raise RuntimeError("operating audit assertion dictionary anchor missing")
            text = text.replace(alt, new_required + alt, 1)
        else:
            text = text.replace(anchor, new_required + anchor, 1)
    write(relative, text)


def main() -> None:
    update_registry()
    update_design_registry()
    update_current_documents()
    append_refinements()
    update_contract_tests()
    update_core_alignment()
    update_operating_audit()
    print("R2 initial role stat and enhancement ownership synchronization applied")


if __name__ == "__main__":
    main()
