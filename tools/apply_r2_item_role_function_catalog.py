#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-ITEM-20260806-04"
BATCH_STATUS = "R2_BATCH_005_8_OF_10"
ACTIVE_STATUS = "R2_BATCH_005_ACTIVE_8_OF_10"
CANON_PATH = "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md"
SPEC_PATH = "docs/superpowers/specs/2026-08-06-item-role-stat-and-function-catalog-design.md"
PLAN_PATH = "docs/superpowers/plans/2026-08-06-item-role-stat-and-function-catalog.md"
TEST_PATH = "tests/test_r2_item_role_stat_and_initial_function_catalog.py"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def write(relative: str, text: str) -> None:
    (ROOT / relative).write_text(text, encoding="utf-8")


def replace_once(relative: str, old: str, new: str) -> None:
    text = read(relative)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"missing replacement anchor: {relative}: {old!r}")
    write(relative, text.replace(old, new, 1))


def replace_all(relative: str, old: str, new: str) -> None:
    text = read(relative)
    if old not in text:
        return
    write(relative, text.replace(old, new))


def append_once(relative: str, marker: str, block: str) -> None:
    text = read(relative)
    if marker in text:
        return
    write(relative, text.rstrip() + "\n\n" + block.strip() + "\n")


def insert_after_once(relative: str, anchor: str, addition: str, marker: str) -> None:
    text = read(relative)
    if marker in text:
        return
    if anchor not in text:
        raise SystemExit(f"missing insertion anchor: {relative}: {anchor!r}")
    write(relative, text.replace(anchor, anchor + addition, 1))


def load_json(relative: str) -> dict[str, Any]:
    value = json.loads(read(relative))
    if not isinstance(value, dict):
        raise SystemExit(f"JSON root must be object: {relative}")
    return value


def save_json(relative: str, value: dict[str, Any], *, compact: bool) -> None:
    if compact:
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"
    else:
        text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    write(relative, text)


def update_registry() -> None:
    relative = "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
    registry = load_json(relative)
    registry["stage_status"] = ACTIVE_STATUS
    registry["next_approval_counter"] = "8/10"

    active = registry.setdefault("active_batch", {})
    active["id"] = "R2_BATCH_005"
    active["counter"] = "8/10"
    active["approved_decisions"] = 8
    active["maximum_size"] = 10
    decisions = active.setdefault("decisions", [])
    if DECISION_ID not in decisions:
        decisions.append(DECISION_ID)

    contract = {
        "item_role_stat_model": "SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS",
        "primary_role_stat_by_equipment_group": {
            "SWORD": "ATTACK",
            "AXE": "ATTACK",
            "BLUNT": "ATTACK",
            "POLEARM": "ATTACK",
            "RANGED": "ATTACK",
            "SHIELD_SUPPORT": "DEFENSE",
            "LIGHT_ARMOR": "DEFENSE",
            "MEDIUM_ARMOR": "DEFENSE",
            "HEAVY_ARMOR": "DEFENSE",
            "TOOL": None,
            "CLOTHING_OR_ROBE": None,
            "ACCESSORY": None,
        },
        "common_item_stats_preserved": ["WEIGHT", "DURABILITY", "HANDLING", "ARTISTRY"],
        "non_applicable_stats_are_omitted": True,
        "display_attack_sources": [
            "CRAFTED_ATTACK",
            "WEIGHT_ATTACK_OUTPUT",
            "APPROVED_ENHANCEMENT_ATTACK_OUTPUT",
        ],
        "display_defense_sources": [
            "CRAFTED_DEFENSE",
            "WEIGHT_DEFENSE_OUTPUT",
            "APPROVED_ENHANCEMENT_DEFENSE_OUTPUT",
        ],
        "crafted_role_stat_determination": "FIRST_CRAFT_COMPLETION_SINGLE_STORED_RESULT_WITH_SOURCE_LEDGER",
        "crafted_role_stat_sources": ["BASE_ITEM_DESIGN", "PRIMARY_MATERIAL", "DIRECT_FORGING_RESULT"],
        "crafting_grade_auto_modifies_attack_or_defense": False,
        "artistry_auto_modifies_attack_or_defense": False,
        "same_source_double_count_allowed": False,
        "default_secondary_combat_stats": [],
        "secondary_stats_require_separate_approved_owner": [
            "CRITICAL_CHANCE",
            "CRITICAL_DAMAGE",
            "PENETRATION",
            "ACCURACY",
            "ATTACK_SPEED",
            "EVASION",
            "BLOCK_RATE",
            "ELEMENTAL_DAMAGE",
        ],
        "special_function_instance_model": "FUNCTION_ID_PLUS_CAPACITY_COST_PLUS_OPTIONAL_BOUND_CONTEXT",
        "capacity_is_total_cost_limit": True,
        "duplicate_function_id_stack_allowed": False,
        "remaining_capacity_auto_generates_function": False,
        "weight_gain_auto_grants_function": False,
        "function_tags_added_to_generic_event_success": False,
        "function_effect_modes": ["ELIGIBILITY", "RISK_MITIGATION", "SPECIFIC_INTERACTION"],
        "initial_magic_function_catalog": {
            "ARCANE_CONDUCTION": {
                "capacity_cost": 1,
                "output_tag": "CAN_CHANNEL_MAGIC_THROUGH_ITEM",
                "bound_context_required": False,
            },
            "ELEMENTAL_WARD": {
                "capacity_cost": 1,
                "output_tag": "MITIGATES_ONE_BOUND_ELEMENTAL_HAZARD",
                "bound_context_required": True,
            },
            "ARCANE_SENSING": {
                "capacity_cost": 2,
                "output_tag": "CAN_DETECT_MATCHING_ARCANE_TRACE",
                "bound_context_required": True,
            },
        },
        "initial_utility_function_catalog": {
            "ENVIRONMENTAL_SEALING": {
                "capacity_cost": 1,
                "output_tag": "RESISTS_ONE_BOUND_ENVIRONMENT",
                "bound_context_required": True,
            },
            "FIELD_SERVICEABILITY": {
                "capacity_cost": 1,
                "output_tag": "CAN_PERFORM_FIELD_MAINTENANCE",
                "bound_context_required": False,
            },
            "TASK_INTEGRATION": {
                "capacity_cost": 1,
                "output_tag": "SUPPORTS_ONE_BOUND_TASK",
                "bound_context_required": True,
            },
        },
        "transformative_function_capacity_cost": 3,
        "transformative_function_requires_separate_design_approval": True,
        "exact_values": "BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
        "product_implementation": "BLOCKED",
    }
    decision = {
        "id": DECISION_ID,
        "title": "작품군 단일 역할 원수치와 최초 마법·유틸리티 기능 카탈로그",
        "status": "USER_APPROVED_R2_BATCH_005_8_OF_10_APPROVED_PENDING_MERGE",
        "refines": [
            "BS-ITEM-20260806-03",
            "BS-CUSTOMER-20260805-01",
            "BS-CRAFT-20260804-04",
            "BS-UX-20260805-01",
        ],
        "canon": CANON_PATH,
        "spec": SPEC_PATH,
        "plan": PLAN_PATH,
        "contract": contract,
    }
    current = registry.setdefault("current_decisions", [])
    for index, item in enumerate(current):
        if isinstance(item, dict) and item.get("id") == DECISION_ID:
            current[index] = decision
            break
    else:
        current.append(decision)

    for item in current:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        if item_id == "BS-ITEM-20260806-03":
            item["item_role_stat_refined_by"] = DECISION_ID
            item["function_catalog_refined_by"] = DECISION_ID
        elif item_id == "BS-CUSTOMER-20260805-01":
            item["item_role_stat_refined_by"] = DECISION_ID
        elif item_id == "BS-CRAFT-20260804-04":
            item["function_catalog_refined_by"] = DECISION_ID
        elif item_id == "BS-UX-20260805-01":
            item["item_function_display_refined_by"] = DECISION_ID

    alignment = registry.setdefault("implementation_alignment", {})
    alignment["item_role_stat_and_function_catalog_product_implementation"] = "NOT_STARTED_BLOCKED"
    save_json(relative, registry, compact=True)


def update_document_registry() -> None:
    relative = "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    registry = load_json(relative)
    registry["current_batch"] = BATCH_STATUS
    registry["current_design_decision"] = DECISION_ID
    documents = registry.setdefault("documents", [])
    additions = [
        {
            "document_id": "item-role-stat-initial-function-catalog-canon",
            "source_path": "../../" + CANON_PATH,
            "status": "ACTIVE",
            "source_role": "current_item_role_stat_and_initial_special_function_contract",
        },
        {
            "document_id": "item-role-stat-initial-function-catalog-design",
            "source_path": "../../" + SPEC_PATH,
            "status": "ACTIVE",
            "source_role": "approved_design_input_for_bs_item_20260806_04",
        },
        {
            "document_id": "item-role-stat-initial-function-catalog-plan",
            "source_path": "../../" + PLAN_PATH,
            "status": "ACTIVE",
            "source_role": "executed_canon_plan_for_bs_item_20260806_04",
        },
        {
            "document_id": "item-role-stat-initial-function-catalog-contract-test",
            "source_path": "../../" + TEST_PATH,
            "status": "ACTIVE",
            "source_role": "tdd_contract_for_bs_item_20260806_04",
        },
    ]
    existing = {item.get("document_id") for item in documents if isinstance(item, dict)}
    for item in additions:
        if item["document_id"] not in existing:
            documents.append(item)

    guards = registry.setdefault("routing_guards", [])
    for guard in [
        "R2_BATCH_005_IS_ACTIVE_AT_8_OF_10_WITH_BS_ITEM_20260806_04",
        "ITEM_ROLE_STAT_MODEL_IS_SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS",
        "DEFAULT_SECONDARY_COMBAT_STAT_SCHEMA_IS_FORBIDDEN",
        "FUNCTION_CAPACITY_DOES_NOT_AUTO_GENERATE_FUNCTIONS",
        "FUNCTION_TAGS_DO_NOT_AUTO_ADD_TO_GENERIC_EVENT_SUCCESS",
        "TRANSFORMATIVE_FUNCTIONS_REQUIRE_SEPARATE_DESIGN_APPROVAL",
    ]:
        if guard not in guards:
            guards.append(guard)
    save_json(relative, registry, compact=False)


def update_current_documents() -> None:
    relative = "CURRENT_CONFIRMED_DECISIONS.md"
    replace_once(relative, "> 현재 승인 배치: `R2_BATCH_005 / 7/10`", "> 현재 승인 배치: `R2_BATCH_005 / 8/10`")
    insert_after_once(
        relative,
        "- `BS-ITEM-20260806-03`: 중량 성능 예산 1점 환산과 장비 역할 프리셋 자동 배분 — `R2_BATCH_005_7_OF_10 / APPROVED_PENDING_MERGE`\n",
        "- `BS-ITEM-20260806-04`: 작품군 단일 역할 원수치와 최초 마법·유틸리티 기능 카탈로그 — `R2_BATCH_005_8_OF_10 / APPROVED_PENDING_MERGE`\n",
        "BS-ITEM-20260806-04`: 작품군 단일 역할 원수치",
    )
    append_once(
        relative,
        "<!-- BS-ITEM-20260806-04 -->",
        """
<!-- BS-ITEM-20260806-04 -->
## 작품 역할 원수치와 최초 특수기능 카탈로그

- Decision: `BS-ITEM-20260806-04`
- 상태: `R2_BATCH_005_8_OF_10 / APPROVED_PENDING_MERGE`
- 모델: `SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS`
- 무기는 공격, 방패·갑옷은 방어를 주 역할 원수치로 사용한다.
- 표시 공격·방어는 최초 제작 + 중량 기반 + 승인된 강화 출력만 가산한다.
- 기본 다중 전투 보조 수치는 추가하지 않는다.
- 최초 마법 기능: `ARCANE_CONDUCTION / ELEMENTAL_WARD / ARCANE_SENSING`.
- 최초 유틸리티 기능: `ENVIRONMENTAL_SEALING / FIELD_SERVICEABILITY / TASK_INTEGRATION`.
- 기능 용량은 기능을 자동 생성하지 않으며 일반 사건 성공률에 자동 합산하지 않는다.
- 제품 구현: `BLOCKED`.
""",
    )

    relative = "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
    replace_once(relative, "- 상태: `CURRENT_CANON / R2_BATCH_005_7_OF_10`", "- 상태: `CURRENT_CANON / R2_BATCH_005_8_OF_10`")
    text = read(relative)
    if "BS-ITEM-20260806-04" not in text.split("\n", 8)[0:8]:
        old = " / BS-ITEM-20260806-03\n"
        if old not in text:
            raise SystemExit("missing game bible current decision anchor")
        write(relative, text.replace(old, " / BS-ITEM-20260806-03 / BS-ITEM-20260806-04\n", 1))
    append_once(
        relative,
        "<!-- BS-ITEM-20260806-04 -->",
        """
<!-- BS-ITEM-20260806-04 -->
## 작품 역할 원수치와 최초 기능 카탈로그

```text
SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS
무기 -> ATTACK
방패·갑옷 -> DEFENSE
도구·의복·장신구 -> 공격·방어 강제 없음
```

```text
DISPLAY_ATTACK = CRAFTED_ATTACK + WEIGHT_ATTACK_OUTPUT + APPROVED_ENHANCEMENT_ATTACK_OUTPUT
DISPLAY_DEFENSE = CRAFTED_DEFENSE + WEIGHT_DEFENSE_OUTPUT + APPROVED_ENHANCEMENT_DEFENSE_OUTPUT
```

최초 승인 마법 기능은 `ARCANE_CONDUCTION / ELEMENTAL_WARD / ARCANE_SENSING`, 유틸리티 기능은 `ENVIRONMENTAL_SEALING / FIELD_SERVICEABILITY / TASK_INTEGRATION`이다. 기능은 용량을 소비하지만 자동 생성되지 않고 일반 사건 성공률에 범용 합산되지 않는다. 제품 구현은 `BLOCKED`다.
""",
    )

    relative = "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
    replace_once(relative, "- 갱신: `2026-08-05 21:45 KST`", "- 갱신: `2026-08-06 07:01 KST`")
    replace_once(relative, "- 단계: `R2_CORE_SESSION_META_LOOP / R2_BATCH_005_7_OF_10`", "- 단계: `R2_CORE_SESSION_META_LOOP / R2_BATCH_005_8_OF_10`")
    replace_once(relative, "- 현재 승인 카운터: `7/10`", "- 현재 승인 카운터: `8/10`")
    append_once(
        relative,
        "<!-- BS-ITEM-20260806-04 -->",
        """
<!-- BS-ITEM-20260806-04 -->
## 현재 작품 역할 원수치·기능 카탈로그 승인

- Decision: `BS-ITEM-20260806-04`
- 활성 배치: `R2_BATCH_005_8_OF_10`
- 역할 모델: `SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS`
- 무기 공격 / 방패·갑옷 방어 / 기타 장비 공격·방어 생략.
- 마법 3종과 유틸리티 3종만 최초 승인.
- 기능 자동 생성·중복 누적·일반 성공률 범용 합산 금지.
- 정본: `docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md`
- 제품 구현: `BLOCKED`.
""",
    )

    hub_blocks = {
        "[기획서]/00_프로젝트_허브/ROADMAP.md": """
<!-- BS-ITEM-20260806-04 -->
## 배치 005 — 작품 역할 원수치·기능 카탈로그

- `BS-ITEM-20260806-04 / R2_BATCH_005_8_OF_10`
- 장비군 단일 역할 원수치와 최초 특수기능 6종을 정본화.
- 다음 Gate: 특수기능 획득·강화 소유권과 최초 제작 원수치 분포 테스트 프리셋.
- `PRODUCT_IMPLEMENTATION: BLOCKED`
""",
        "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": """
<!-- BS-ITEM-20260806-04 -->
## Item Role Stat and Function Catalog Gate

- Decision: `BS-ITEM-20260806-04 / R2_BATCH_005_ACTIVE_8_OF_10`
- `SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS`
- 최초 승인 기능 6종 외 기능과 용량 3 규칙 우회 기능은 별도 승인 필요.
- `CODEX_IMPLEMENTATION_GATE: BLOCKED`
""",
        "[기획서]/00_프로젝트_허브/START_HERE.md": """
<!-- BS-ITEM-20260806-04 -->
## 현재 작품 능력치 진입점

`BS-ITEM-20260806-04 / R2_BATCH_005_ACTIVE_8_OF_10`이 작품 역할 원수치와 최초 기능 카탈로그의 최신 권위다. 제품 구현은 `BLOCKED`다.
""",
        "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": """
<!-- BS-ITEM-20260806-04 -->
## 작품 역할 원수치·기능 카탈로그

- Decision: `BS-ITEM-20260806-04 / R2_BATCH_005_8_OF_10`
- Canon: `docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md`
- Spec: `docs/superpowers/specs/2026-08-06-item-role-stat-and-function-catalog-design.md`
- Plan: `docs/superpowers/plans/2026-08-06-item-role-stat-and-function-catalog.md`
""",
    }
    for path, block in hub_blocks.items():
        text = read(path)
        text = text.replace("R2_BATCH_005_ACTIVE_7_OF_10", "R2_BATCH_005_ACTIVE_8_OF_10", 1)
        text = text.replace("R2_BATCH_005_7_OF_10", "R2_BATCH_005_8_OF_10", 1)
        text = text.replace("NEXT_APPROVAL_COUNTER: 7/10", "NEXT_APPROVAL_COUNTER: 8/10", 1)
        write(path, text)
        append_once(path, "<!-- BS-ITEM-20260806-04 -->", block)


def update_refined_canons() -> None:
    blocks = {
        "docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-04 -->
## [현재 후속 정제] 역할 원수치와 기능 인스턴스

- `REFINED_BY_BS-ITEM-20260806-04`
- `R2_BATCH_005_8_OF_10`
- 중량 예산 출력은 무기 공격 또는 방패·갑옷 방어의 역할 원수치에 합산한다.
- 마법·유틸리티 용량은 승인된 기능 비용 상한이며 기능을 자동 생성하지 않는다.
- 기능 태그는 일반 사건 성공률에 자동 합산하지 않는다.
""",
        "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-04 -->
## [현재 후속 정제] 고객과 작품 역할 원수치·기능

- `REFINED_BY_BS-ITEM-20260806-04`
- `R2_BATCH_005_8_OF_10`
- 고객 능력은 작품의 공격·방어 원수치를 다시 생성하지 않는다.
- 특수기능은 고객의 마력 적성·친화·판단력·관련 적성·활성 조건을 대체하지 않는다.
- 기능 태그는 일반 성공률에 범용 자동 합산되지 않는다.
""",
        "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-04 -->
## [현재 후속 정제] 정밀강화와 특수기능 소유권

- `REFINED_BY_BS-ITEM-20260806-04`
- `R2_BATCH_005_8_OF_10`
- 중량화로 기능 용량을 얻어도 기능이 자동 생성되지 않는다.
- 촉매 수식어·정밀강화 방식·승인된 재작업 중 어느 경로가 기능을 생성·강화하는지는 후속 Gate다.
- 용량 3 규칙 우회 기능은 별도 기획 승인이 필요하다.
""",
        "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md": """
<!-- REFINED_BY_BS-ITEM-20260806-04 -->
## [현재 후속 정제] 작품 원수치·기능 표시

- `REFINED_BY_BS-ITEM-20260806-04`
- `R2_BATCH_005_8_OF_10`
- 기본 작품 카드에는 존재하는 공격 또는 방어와 기능 이름만 표시한다.
- 기능 용량 비용·결속 맥락·출처는 상세 보기에서 제공한다.
- 존재하지 않는 원수치와 전체 기능 카탈로그를 기본 화면에 노출하지 않는다.
""",
    }
    for path, block in blocks.items():
        append_once(path, "REFINED_BY_BS-ITEM-20260806-04", block)


def update_tests() -> None:
    for path in (ROOT / "tests").glob("test_*.py"):
        text = path.read_text(encoding="utf-8")
        original = text
        text = text.replace("R2_BATCH_005_ACTIVE_7_OF_10", "R2_BATCH_005_ACTIVE_8_OF_10")
        text = text.replace('self.assertEqual("7/10", self.registry["next_approval_counter"])', 'self.assertEqual("8/10", self.registry["next_approval_counter"])')
        text = text.replace('self.assertEqual(7, active["approved_decisions"])', 'self.assertEqual(8, active["approved_decisions"])')
        text = text.replace('self.assertEqual("7/10", active["counter"])', 'self.assertEqual("8/10", active["counter"])')
        text = text.replace("contains_seven_approved_decisions", "contains_eight_approved_decisions")
        text = text.replace("active_at_seven_of_ten", "active_at_eight_of_ten")
        sequence = '                "BS-ITEM-20260806-03",\n            ],\n            active["decisions"],'
        replacement = '                "BS-ITEM-20260806-03",\n                "BS-ITEM-20260806-04",\n            ],\n            active["decisions"],'
        if sequence in text:
            text = text.replace(sequence, replacement, 1)
        if text != original:
            path.write_text(text, encoding="utf-8")


def update_core_alignment() -> None:
    relative = "tests/check_project_core_alignment.py"
    text = read(relative)
    text = text.replace("R2_BATCH_005_ACTIVE_7_OF_10", "R2_BATCH_005_ACTIVE_8_OF_10")
    text = text.replace("R2_BATCH_005_7_OF_10", "R2_BATCH_005_8_OF_10")
    text = text.replace("현재 승인 카운터: `7/10`", "현재 승인 카운터: `8/10`")
    text = text.replace('"next_approval_counter": "7/10"', '"next_approval_counter": "8/10"')
    text = text.replace('active.get("counter") != "7/10"', 'active.get("counter") != "8/10"')
    text = text.replace("active batch must be R2_BATCH_005 at 7/10", "active batch must be R2_BATCH_005 at 8/10")
    text = text.replace('active.get("approved_decisions") != 7', 'active.get("approved_decisions") != 8')
    sequence = '        "BS-ITEM-20260806-03",\n    ]:\n        failures.append("active batch 005 must contain the seven approved decisions")'
    replacement = '        "BS-ITEM-20260806-03",\n        "BS-ITEM-20260806-04",\n    ]:\n        failures.append("active batch 005 must contain the eight approved decisions")'
    if sequence not in text and replacement not in text:
        raise SystemExit("missing core alignment active decision sequence")
    text = text.replace(sequence, replacement, 1)

    active_entry = '''    "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md": (
        "BS-ITEM-20260806-04",
        "R2_BATCH_005_8_OF_10",
        "SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS",
        "ARCANE_CONDUCTION",
        "TASK_INTEGRATION",
        "제품 구현: `BLOCKED`",
    ),
'''
    anchor = '    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": ('
    if "BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md" not in text:
        if anchor not in text:
            raise SystemExit("missing core alignment required-text anchor")
        text = text.replace(anchor, active_entry + anchor, 1)

    validation = '''
    role_catalog = decisions.get("BS-ITEM-20260806-04", {}).get("contract", {})
    if role_catalog.get("item_role_stat_model") != "SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS":
        failures.append("item role-stat model is incorrect")
    if role_catalog.get("primary_role_stat_by_equipment_group", {}).get("SWORD") != "ATTACK":
        failures.append("sword primary role stat must be attack")
    if role_catalog.get("primary_role_stat_by_equipment_group", {}).get("HEAVY_ARMOR") != "DEFENSE":
        failures.append("heavy armor primary role stat must be defense")
    if role_catalog.get("display_attack_sources") != ["CRAFTED_ATTACK", "WEIGHT_ATTACK_OUTPUT", "APPROVED_ENHANCEMENT_ATTACK_OUTPUT"]:
        failures.append("display attack sources are incomplete")
    if role_catalog.get("display_defense_sources") != ["CRAFTED_DEFENSE", "WEIGHT_DEFENSE_OUTPUT", "APPROVED_ENHANCEMENT_DEFENSE_OUTPUT"]:
        failures.append("display defense sources are incomplete")
    if set(role_catalog.get("initial_magic_function_catalog", {})) != {"ARCANE_CONDUCTION", "ELEMENTAL_WARD", "ARCANE_SENSING"}:
        failures.append("initial magic function catalog is incomplete")
    if set(role_catalog.get("initial_utility_function_catalog", {})) != {"ENVIRONMENTAL_SEALING", "FIELD_SERVICEABILITY", "TASK_INTEGRATION"}:
        failures.append("initial utility function catalog is incomplete")
    if role_catalog.get("function_tags_added_to_generic_event_success") is not False:
        failures.append("function tags must not auto-add to generic success")
    if role_catalog.get("transformative_function_requires_separate_design_approval") is not True:
        failures.append("transformative functions must require separate approval")
    if role_catalog.get("product_implementation") != "BLOCKED":
        failures.append("item role stat and function catalog implementation must remain blocked")

'''
    anchor2 = '    alignment = registry.get("implementation_alignment", {})'
    if 'role_catalog = decisions.get("BS-ITEM-20260806-04"' not in text:
        if anchor2 not in text:
            raise SystemExit("missing core alignment validation anchor")
        text = text.replace(anchor2, validation + anchor2, 1)
    write(relative, text)


def update_audit() -> None:
    relative = "tools/audit_project_operating_system.py"
    text = read(relative)
    active_anchor = '    "docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md",\n'
    active_add = active_anchor + '    "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md",\n'
    if "BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md" not in text.split("REQUIRED_ASSERTIONS", 1)[0]:
        if active_anchor not in text:
            raise SystemExit("missing audit active-doc anchor")
        text = text.replace(active_anchor, active_add, 1)

    text = text.replace("R2_BATCH_005 / 7/10", "R2_BATCH_005 / 8/10")
    text = text.replace("R2_BATCH_005_ACTIVE_7_OF_10", "R2_BATCH_005_ACTIVE_8_OF_10")
    text = text.replace("R2_BATCH_005_7_OF_10", "R2_BATCH_005_8_OF_10")
    text = text.replace('"next_approval_counter":"7/10"', '"next_approval_counter":"8/10"')

    registry_anchor = '        \'"id":"BS-ITEM-20260806-03"\',\n'
    registry_add = registry_anchor + '''        '"id":"BS-ITEM-20260806-04"',
        '"item_role_stat_model":"SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS"',
        '"ARCANE_CONDUCTION":{"capacity_cost":1',
        '"TASK_INTEGRATION":{"capacity_cost":1',
        '"function_tags_added_to_generic_event_success":false',
'''
    if '\'"id":"BS-ITEM-20260806-04"\'' not in text:
        if registry_anchor not in text:
            raise SystemExit("missing audit registry anchor")
        text = text.replace(registry_anchor, registry_add, 1)

    canon_entry = '''    "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md": (
        "BS-ITEM-20260806-04",
        "R2_BATCH_005_8_OF_10",
        "SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS",
        "DISPLAY_ATTACK",
        "DISPLAY_DEFENSE",
        "ARCANE_CONDUCTION",
        "ELEMENTAL_WARD",
        "ARCANE_SENSING",
        "ENVIRONMENTAL_SEALING",
        "FIELD_SERVICEABILITY",
        "TASK_INTEGRATION",
        "제품 구현: `BLOCKED`",
    ),
'''
    canon_anchor = '    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": ('
    if canon_entry.strip() not in text:
        if canon_anchor not in text:
            raise SystemExit("missing audit canon assertion anchor")
        text = text.replace(canon_anchor, canon_entry + canon_anchor, 1)
    write(relative, text)


def main() -> None:
    if not (ROOT / CANON_PATH).is_file():
        raise SystemExit(f"missing canon: {CANON_PATH}")
    update_registry()
    update_document_registry()
    update_current_documents()
    update_refined_canons()
    update_tests()
    update_core_alignment()
    update_audit()
    print("R2 item role stat and initial function catalog synchronization applied")


if __name__ == "__main__":
    main()
