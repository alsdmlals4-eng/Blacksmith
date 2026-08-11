from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_required(text: str, old: str, new: str, path: str, count: int = -1) -> str:
    if old not in text:
        raise RuntimeError(f"missing anchor in {path}: {old!r}")
    return text.replace(old, new, count)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.strip() + "\n"


def update_registry() -> None:
    path = "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
    data = json.loads(read(path))
    if data.get("next_approval_counter") != "2/10":
        raise RuntimeError(f"unexpected R3 counter: {data.get('next_approval_counter')!r}")
    data["next_approval_counter"] = "3/10"

    ids = [item.get("id") for item in data.get("current_decisions", [])]
    if "BS-CONTENT-20260811-03" not in ids:
        data.setdefault("current_decisions", []).append(
            {
                "id": "BS-CONTENT-20260811-03",
                "title": "군인 01 마레크 올덴 소량 표준 납품 콘텐츠",
                "status": "USER_APPROVED_R3_R7_3_OF_10",
                "canon": "docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md",
                "refines": ["BS-CONTENT-20260804-01", "BS-CONTENT-20260804-02"],
                "depends_on": [
                    "BS-CUSTOMER-20260803-02",
                    "BS-CUSTOMER-20260806-01",
                    "BS-ITEM-20260806-04",
                    "BS-ITEM-20260806-05",
                    "BS-UX-20260805-01",
                    "BS-CORE-20260811-01",
                    "BS-CONTENT-20260811-02",
                ],
                "contract": {
                    "content_id": "SOLDIER_01",
                    "customer_id": "MAREK_OLDEN",
                    "customer_archetype": "SOLDIER",
                    "activity_family": "SMALL_LOT_STANDARD_ORDER",
                    "content_goal": "UNIT_READINESS_AND_STANDARD_FIT",
                    "player_role": "BLACKSMITH_SMALL_LOT_EQUIPMENT_DECISION_MAKER_NOT_LOGISTICS_OR_COMBAT_CONTROLLER",
                    "baseline_order_quantity": 10,
                    "order_quantity_status": "NON_CANONICAL_BASELINE_TEST_FIXTURE",
                    "reference_item_required": True,
                    "per_item_uid_preserved": True,
                    "per_item_cost_and_result_preserved": True,
                    "free_item_cloning": False,
                    "worker_or_production_line_system": False,
                    "direct_tactical_combat": False,
                    "realtime_logistics_control": False,
                    "opaque_standardization_score": False,
                    "single_highest_enhancement_always_best": False,
                    "low_enhancement_target": "NON_CANONICAL_BASELINE_TEST_PRESET",
                    "auto_enhancement_cap_owner": "BS-CORE-20260811-01",
                    "result_axes": [
                        "UNIT_MISSION_STATE",
                        "STANDARD_ADOPTION_STATE",
                        "BATCH_ITEM_LIFECYCLE_STATE",
                    ],
                    "product_implementation": "BLOCKED",
                    "task3_implementation": "NOT_APPROVED",
                    "human_playtest": "NOT_RUN",
                },
            }
        )

    existing_sources = {item.get("source") for item in data.get("benchmark_context", []) if isinstance(item, dict)}
    additions = [
        {
            "source": "Blacksmith Master official Steam page",
            "decision": "ADAPT",
            "use": "small-order and production-throughput context",
            "avoid": "worker production-line or industrial mass-production core",
        },
        {
            "source": "Anvil Saga official Steam page",
            "decision": "ADAPT",
            "use": "customer order to crafted output to world consequence",
            "avoid": "broad shop-simulation scope drift",
        },
        {
            "source": "Battle Brothers official features",
            "decision": "ADAPT",
            "use": "equipment suitability affects group outcome",
            "avoid": "direct tactical combat and soldier-management gameplay",
        },
        {
            "source": "Lean Enterprise Institute standardized work guidance",
            "decision": "ADAPT",
            "use": "explicit common standard and repeatable process",
            "avoid": "industrial statistical-control simulation",
        },
    ]
    for item in additions:
        if item["source"] not in existing_sources:
            data.setdefault("benchmark_context", []).append(item)

    for boundary in (
        "NO_THREE_DIGIT_MASS_PRODUCTION_CORE",
        "NO_WORKER_OR_PRODUCTION_LINE_SYSTEM_FROM_SOLDIER_01",
        "NO_REALTIME_LOGISTICS_CONTROL",
        "NO_DIRECT_TACTICAL_COMBAT",
        "NO_FREE_ITEM_CLONING",
        "SMALL_LOT_PER_ITEM_UID_COST_RESULT_PRESERVED",
        "NO_OPAQUE_STANDARDIZATION_SCORE",
    ):
        if boundary not in data.setdefault("protected_boundaries", []):
            data["protected_boundaries"].append(boundary)

    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def update_current_decisions() -> None:
    path = "CURRENT_CONFIRMED_DECISIONS.md"
    text = read(path)
    text = re.sub(
        r"> \*\*R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-02 / R3_R7_2_OF_10 / PLANNING_ONLY\*\*",
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-03 / R3_R7_3_OF_10 / PLANNING_ONLY**",
        text,
        count=1,
    )
    text = replace_required(text, "R3_R7_APPROVAL_COUNTER: 2/10", "R3_R7_APPROVAL_COUNTER: 3/10", path)
    text = replace_required(
        text,
        "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-02",
        "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-03",
        path,
    )

    if "- `BS-CONTENT-20260811-03`:" not in text:
        lines = text.splitlines()
        index = next(i for i, line in enumerate(lines) if line.startswith("- `BS-CONTENT-20260811-02`:"))
        lines.insert(
            index + 1,
            "- `BS-CONTENT-20260811-03`: `SOLDIER_01` 마레크 올덴 소량 표준 주문. 기준품 한 점을 직접 만든 뒤 반복 설정은 압축할 수 있지만 약 10개 baseline fixture의 각 작품은 독립 UID·비용·작업·단조·강화·연대기를 유지한다. 결과는 `UNIT_MISSION_STATE / STANDARD_ADOPTION_STATE / BATCH_ITEM_LIFECYCLE_STATE`로 분리하며 직접 전술 전투·실시간 병참·작업자 생산라인·무료 복제를 추가하지 않는다. — `USER_APPROVED / R3_R7_3_OF_10 / PLANNING_ONLY`",
        )
        text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

    if "- `BS-CORE-20260811-01`:" not in text:
        lines = text.splitlines()
        index = next(i for i, line in enumerate(lines) if line.startswith("- `BS-OPS-20260811-02`:"))
        lines.insert(
            index + 1,
            "- `BS-CORE-20260811-01`: 기존 저위험 연속강화를 성장형 `AUTO_ENHANCEMENT_CAP_UNLOCK`으로 refine한다. 초기 `수동 15회 → AUTO_CAP +20`을 보존하고, 이후 분야별 기술 돌파보다 한 10강 밴드 뒤까지 목표 지정 자동 강화를 해금한다. 정상 확률·비용·자원·UID 이력을 보존하고 `HIGH / VERY_HIGH`, 정밀강화, 기술 돌파, 무보호 파괴 가능 시도는 자동화하지 않는다. — `USER_APPROVED_DIRECTION / PLANNING_ONLY`",
        )
        text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

    text = append_once(
        text,
        "## 19. R3–R7 세 번째 상세 콘텐츠 — 마레크 올덴 소량 표준 주문",
        """
## 19. R3–R7 세 번째 상세 콘텐츠 — 마레크 올덴 소량 표준 주문

Decision: `BS-CONTENT-20260811-03`.

```text
SOLDIER_01 / MAREK_OLDEN
SMALL_LOT_STANDARD_ORDER
UNIT_READINESS_AND_STANDARD_FIT
```

- 첫 검증 수량은 `ORDER_QUANTITY = 10 / NON_CANONICAL_BASELINE_TEST_PRESET`다.
- 기준품 뒤 반복 설정은 압축할 수 있지만 각 작품의 UID·비용·작업·단조·강화·연대기는 독립한다.
- 결과는 `UNIT_MISSION_STATE / STANDARD_ADOPTION_STATE / BATCH_ITEM_LIFECYCLE_STATE`로 분리한다.
- 직접 전술 전투·실시간 병참·작업자 생산라인·무료 복제·불투명 표준화 점수는 추가하지 않는다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.
""",
    )
    text = append_once(
        text,
        "## 20. 자동 강화 최대치 해금",
        """
## 20. 자동 강화 최대치 해금

Decision: `BS-CORE-20260811-01 / AUTO_ENHANCEMENT_CAP_UNLOCK`.

- 기존 `수동 강화 15회 뒤 해금 / +1~+20` 저위험 연속강화를 보존한다.
- 이후 해당 분야의 수동 기술 돌파보다 한 10강 밴드 뒤까지 자동 상한을 해금한다.
- 플레이어가 목표 강화 수치를 지정하며 목표는 해당 분야 `AUTO_CAP` 이하만 가능하다.
- 자동 시도는 정상 강화 확률·비용·자원·작업 기회비용·동일 UID 이력을 그대로 사용한다.
- `HIGH / VERY_HIGH`, 정밀강화, 기술 돌파, 무보호 파괴 가능 시도는 수동 전용이다.
- 이 시스템 Decision은 R3 콘텐츠 승인 카운터를 증가시키지 않는다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.
""",
    )
    write(path, text)


def update_router(path: str, current_phrase: str | None = None) -> None:
    text = read(path)
    text = text.replace("R3_R7_APPROVAL_COUNTER: 2/10", "R3_R7_APPROVAL_COUNTER: 3/10")
    text = text.replace(
        "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-02",
        "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-03",
    )
    text = text.replace("현재 R3–R7 승인 카운터: `2/10`", "현재 R3–R7 승인 카운터: `3/10`")
    text = text.replace("현재 승인 카운터: `2/10`.", "현재 승인 카운터: `3/10`.")
    text = text.replace(
        "ADVENTURER_02_TOREN_LONG_RANGE_RELIABILITY_APPROVED",
        "SOLDIER_01_MAREK_SMALL_LOT_STANDARD_ORDER_APPROVED",
    )
    text = text.replace("현재 Decision은 `BS-CONTENT-20260811-02`", "현재 Decision은 `BS-CONTENT-20260811-03`")
    text = text.replace("현재 연속 작업은 `BS-CONTENT-20260811-02`", "현재 연속 작업은 `BS-CONTENT-20260811-03`")
    text = re.sub(
        r"(현재 R3.?R7 승인 카운터[^\n]*?)`2/10`",
        lambda m: m.group(1) + "`3/10`",
        text,
    )
    text = append_once(
        text,
        "<!-- BS-CONTENT-20260811-03 CURRENT -->",
        """
<!-- BS-CONTENT-20260811-03 CURRENT -->
## R3–R7 current 3/10 — Marek Soldier01

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 3/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-03
R3_R7_RESUME_LOCATOR: SOLDIER_01_MAREK_SMALL_LOT_STANDARD_ORDER_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

`BS-CONTENT-20260811-01` Nadia와 `BS-CONTENT-20260811-02` Toren은 승인 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-03`이다.

`SOLDIER_01 / MAREK_OLDEN / SMALL_LOT_STANDARD_ORDER`는 기준품 + 소량 반복 제작을 사용하며, 첫 `ORDER_QUANTITY = 10`은 `NON_CANONICAL_BASELINE_TEST_PRESET`이다. 개별 UID·비용·단조·강화·연대기를 유지하고 직접 전술 전투·실시간 병참·작업자 생산라인·무료 복제를 추가하지 않는다.

`BS-CORE-20260811-01 / AUTO_ENHANCEMENT_CAP_UNLOCK`은 별도 시스템 Decision이며 R3 콘텐츠 카운터를 올리지 않는다. 기존 +20 저위험 자동강화를 보존하고 수동 분야 돌파보다 한 10강 밴드 뒤에서 목표 지정 자동 상한을 해금한다.
""",
    )
    if current_phrase and current_phrase not in text:
        text += "\n" + current_phrase + "\n"
    write(path, text)


def update_audit_runner() -> None:
    path = "tools/run_project_operating_system_audit.py"
    text = read(path)
    text = replace_required(
        text,
        'R3_TOREN_CANON = "docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md"\nR3_FIRST_DECISION = "BS-CONTENT-20260811-01"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-02"',
        'R3_TOREN_CANON = "docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md"\nR3_MAREK_CANON = "docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md"\nR3_FIRST_DECISION = "BS-CONTENT-20260811-01"\nR3_SECOND_DECISION = "BS-CONTENT-20260811-02"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-03"',
        path,
    )
    text = text.replace('"next_approval_counter": "2/10"', '"next_approval_counter": "3/10"')
    text = replace_required(
        text,
        'f\'"id": "{R3_FIRST_DECISION}"\',\n        f\'"id": "{R3_CURRENT_DECISION}"\',\n        \'"content_id": "ADVENTURER_02"\',\n        \'"customer_id": "TOREN_MARCH"\',\n        \'"direct_travel_or_route_minigame": false\',\n        \'"new_reliability_or_repairability_raw_stat": false\',\n        \'"routine_automatic_wear_tax": false\',',
        'f\'"id": "{R3_FIRST_DECISION}"\',\n        f\'"id": "{R3_SECOND_DECISION}"\',\n        f\'"id": "{R3_CURRENT_DECISION}"\',\n        \'"content_id": "SOLDIER_01"\',\n        \'"customer_id": "MAREK_OLDEN"\',\n        \'"activity_family": "SMALL_LOT_STANDARD_ORDER"\',\n        \'"per_item_uid_preserved": true\',\n        \'"free_item_cloning": false\',',
        path,
    )
    marek_assertion = '''\n    assertions[R3_MAREK_CANON] = (\n        R3_CURRENT_DECISION,\n        "SOLDIER_01",\n        "MAREK_OLDEN",\n        "SMALL_LOT_STANDARD_ORDER",\n        "ORDER_QUANTITY = 10",\n        "PER_ITEM_UID_PRESERVED",\n        "UNIT_MISSION_STATE",\n        "STANDARD_ADOPTION_STATE",\n        "BATCH_ITEM_LIFECYCLE_STATE",\n        "제품 구현: `BLOCKED`",\n        "Task3 구현: `NOT_APPROVED`",\n    )\n'''
    anchor = "\n    gates_path = \"[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md\""
    if "assertions[R3_MAREK_CANON]" not in text:
        text = replace_required(text, anchor, marek_assertion + anchor, path)
    text = text.replace('"R3_R7_APPROVAL_COUNTER: 2/10"', '"R3_R7_APPROVAL_COUNTER: 3/10"')
    text = text.replace('"현재 R3–R7 승인 카운터: `2/10`"', '"현재 R3–R7 승인 카운터: `3/10`"')
    text = replace_required(
        text,
        "R3_FIRST_DECISION,\n            R3_CURRENT_DECISION,",
        "R3_FIRST_DECISION,\n            R3_SECOND_DECISION,\n            R3_CURRENT_DECISION,",
        path,
    )
    text = replace_required(
        text,
        "for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON):",
        "for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON):",
        path,
    )
    write(path, text)


def update_current_tests() -> None:
    paths = [
        "tests/test_pre_work_research_gate.py",
        "tests/test_r3_adventurer_02_toren_content.py",
        "tests/test_vertical_slice_new_campaign_initializer_authority.py",
        "tests/test_hera_postmerge_closure_contract.py",
        "tests/check_project_core_alignment_current.py",
        "tests/test_project_operating_system_audit_runner.py",
    ]
    for path in paths:
        text = read(path)
        text = text.replace("R3_R7_APPROVAL_COUNTER: 2/10", "R3_R7_APPROVAL_COUNTER: 3/10")
        text = text.replace("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-02", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-03")
        text = text.replace("현재 R3–R7 승인 카운터: `2/10`", "현재 R3–R7 승인 카운터: `3/10`")
        text = text.replace("현재 승인 카운터: `2/10`.", "현재 승인 카운터: `3/10`.")
        text = text.replace("ADVENTURER_02_TOREN_LONG_RANGE_RELIABILITY_APPROVED", "SOLDIER_01_MAREK_SMALL_LOT_STANDARD_ORDER_APPROVED")
        text = text.replace("R3_CURRENT_DECISION_ID = \"BS-CONTENT-20260811-02\"", "R3_CURRENT_DECISION_ID = \"BS-CONTENT-20260811-03\"")
        text = text.replace("R3_CURRENT_RESUME_LOCATOR = \"ADVENTURER_02_TOREN_LONG_RANGE_RELIABILITY_APPROVED\"", "R3_CURRENT_RESUME_LOCATOR = \"SOLDIER_01_MAREK_SMALL_LOT_STANDARD_ORDER_APPROVED\"")
        text = text.replace('self.assertEqual("2/10", registry.get("next_approval_counter"))', 'self.assertEqual("3/10", registry.get("next_approval_counter"))')
        text = text.replace("현재 Decision은 `BS-CONTENT-20260811-02`", "현재 Decision은 `BS-CONTENT-20260811-03`")
        text = text.replace("현재 연속 작업은 `BS-CONTENT-20260811-02`", "현재 연속 작업은 `BS-CONTENT-20260811-03`")
        text = text.replace('"next_approval_counter": "2/10"', '"next_approval_counter": "3/10"')
        text = text.replace("R3_CURRENT_DECISION = \"BS-CONTENT-20260811-02\"", "R3_CURRENT_DECISION = \"BS-CONTENT-20260811-03\"")
        write(path, text)

    path = "tests/check_project_core_alignment_current.py"
    text = read(path)
    if '"BS-CONTENT-20260811-03"' not in text:
        text = replace_required(
            text,
            '"BS-CONTENT-20260811-02",\n            "PRODUCT_IMPLEMENTATION: BLOCKED",',
            '"BS-CONTENT-20260811-02",\n            "BS-CONTENT-20260811-03",\n            "PRODUCT_IMPLEMENTATION: BLOCKED",',
            path,
        )
    write(path, text)

    path = "tests/test_project_operating_system_audit_runner.py"
    text = read(path)
    text = text.replace('self.assertIn(\'"id": "BS-CONTENT-20260811-02"\', registry)', 'self.assertIn(\'"id": "BS-CONTENT-20260811-02"\', registry)\n        self.assertIn(\'"id": "BS-CONTENT-20260811-03"\', registry)')
    text = text.replace('self.assertIn(\'"content_id": "ADVENTURER_02"\', registry)', 'self.assertIn(\'"content_id": "SOLDIER_01"\', registry)')
    text = text.replace('self.assertIn(\'"customer_id": "TOREN_MARCH"\', registry)', 'self.assertIn(\'"customer_id": "MAREK_OLDEN"\', registry)')
    text = text.replace("self.assertIn(runner.R3_TOREN_CANON, audit.ACTIVE_DOCS)", "self.assertIn(runner.R3_TOREN_CANON, audit.ACTIVE_DOCS)\n        self.assertIn(runner.R3_MAREK_CANON, audit.ACTIVE_DOCS)")
    text = text.replace('self.assertIn("BS-CONTENT-20260811-02", tokens)\n            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-03", tokens)', 'self.assertIn("BS-CONTENT-20260811-02", tokens)\n            self.assertIn("BS-CONTENT-20260811-03", tokens)\n            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-03", tokens)')
    write(path, text)


def update_python_validation() -> None:
    path = ".github/workflows/python-validation.yml"
    text = read(path)
    anchor = "          python -m pytest tests/test_pre_work_research_gate.py -q\n"
    addition = (
        anchor
        + "          python -m unittest tests.test_r3_soldier_01_marek_content -v\n"
        + "          python -m unittest tests.test_auto_enhancement_cap_unlock -v\n"
    )
    if "tests.test_r3_soldier_01_marek_content" not in text:
        text = replace_required(text, anchor, addition, path, 1)
    write(path, text)


def update_health_hash() -> None:
    path = "docs/PROJECT_OPERATING_HEALTH.json"
    health = json.loads(read(path))
    current_bytes = (ROOT / "CURRENT_CONFIRMED_DECISIONS.md").read_bytes()
    digest = hashlib.sha256(current_bytes).hexdigest()
    found = False
    for item in health.get("evidence", {}).get("operating", []):
        if item.get("id") == "BS-CURRENT-DECISIONS":
            item["sha256"] = digest
            found = True
    if not found:
        raise RuntimeError("BS-CURRENT-DECISIONS health record missing")
    write(path, json.dumps(health, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    update_registry()
    update_current_decisions()
    update_router("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md")
    update_router("[기획서]/00_프로젝트_허브/START_HERE.md", "현재 연속 작업은 `BS-CONTENT-20260811-03`이다.")
    update_router("[기획서]/00_프로젝트_허브/ROADMAP.md", "현재 승인 카운터: `3/10`.")
    update_router("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md", "Decision: `BS-CONTENT-20260811-03`.")
    update_audit_runner()
    update_current_tests()
    update_python_validation()
    update_health_hash()
    print("materialized Marek 3/10 and auto enhancement cap planning canon")


if __name__ == "__main__":
    main()
