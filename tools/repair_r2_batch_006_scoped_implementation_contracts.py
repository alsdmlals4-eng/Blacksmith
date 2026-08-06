from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGE_SHA = "a8a94343c78a68bf7bb14b411e7741f43b257138"
SOURCE_HEAD = "388eff03c61126d8021601c3ab84efaa2133253e"

PROPOSAL = ROOT / "docs/planning/BLACKSMITH_R2_BATCH_006_VERTICAL_SLICE_CANON_PROPOSAL_2026.md"
BATCH_REGISTRY = ROOT / "docs/planning/R2_BATCH_006_VERTICAL_SLICE_PROPOSAL_REGISTRY.json"
CURRENT_REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CURRENT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
ROADMAP = ROOT / "[기획서]/00_프로젝트_허브/ROADMAP.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
HEALTH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"

FEATURE_TESTS = [
    "tests/test_base_v942_planning_first_adoption.py",
    "tests/test_r2_artistry_generation_growth_economy.py",
    "tests/test_r2_customer_equipment_compatibility.py",
    "tests/test_r2_mobile_customer_card_progressive_disclosure.py",
    "tests/test_r2_enhancement_dominant_simple_load_gate.py",
    "tests/test_r2_equipment_base_weight_points.py",
    "tests/test_r2_weight_performance_budget_and_lightweight_tradeoff.py",
    "tests/test_r2_weight_budget_conversion_and_role_presets.py",
    "tests/test_r2_item_role_stat_and_initial_function_catalog.py",
    "tests/test_r2_initial_role_stat_preset_and_enhancement_function_ownership.py",
    "tests/test_r2_function_recipe_material_fit_and_playtest.py",
]


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def normalize_registries() -> None:
    batch = json.loads(BATCH_REGISTRY.read_text(encoding="utf-8"))
    batch["status"] = "USER_APPROVED_MERGED_PR120_MAIN_CANON"
    batch["authority"] = "MAIN_CANON"
    batch["source_exact_head"] = SOURCE_HEAD
    batch["merge_sha"] = MERGE_SHA
    batch["product_implementation"] = "BLOCKED"
    batch["vertical_slice_implementation"] = "APPROVED"
    batch["implementation_scope"] = "VERTICAL_SLICE_NAMESPACES_ONLY"
    batch["vertical_slice_verdict"] = "APPROVED_FOR_IMPLEMENTATION"
    for decision in batch["decisions"]:
        decision["status"] = "USER_APPROVED_MERGED_PR120_MAIN_CANON"
        decision["authority"] = "MAIN_CANON"
    BATCH_REGISTRY.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    current = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    current["stage_status"] = "R2_BATCH_006_APPROVED_MAIN_CANON"
    current["product_implementation"] = "BLOCKED"
    current["vertical_slice_implementation"] = "APPROVED"
    current["implementation_scope"] = "VERTICAL_SLICE_NAMESPACES_ONLY"
    current["next_approval_counter"] = "10/10"
    current["human_playtest"] = "NOT_RUN"
    active = current["active_batch"]
    active["id"] = "R2_BATCH_006"
    active["status"] = "APPROVED_MERGED_PR120_MAIN_CANON"
    active["approved_decisions"] = 10
    active["approved_count"] = 10
    active["counter"] = "10/10"
    active["maximum_size"] = 10
    active["maximum_count"] = 10
    active["planning_pr"] = 120
    active["planning_exact_head"] = SOURCE_HEAD
    active["planning_merge_sha"] = MERGE_SHA
    evidence = current.setdefault("immutable_merge_evidence", {}).setdefault("batch_006", {})
    evidence.update(
        {
            "planning_pr": 120,
            "planning_exact_head": SOURCE_HEAD,
            "planning_merge_sha": MERGE_SHA,
            "status": "USER_APPROVED_MERGED_MAIN_CANON",
            "merge_method": "SQUASH",
            "github_readback": "PASS",
            "sheet_readback": "PENDING_CLOSURE_SYNC",
        }
    )
    CURRENT_REGISTRY.write_text(json.dumps(current, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def normalize_proposal_doc() -> None:
    text = PROPOSAL.read_text(encoding="utf-8")
    text = text.replace(
        "PRODUCT_IMPLEMENTATION: VERTICAL_SLICE_IMPLEMENTATION_APPROVED",
        "PRODUCT_IMPLEMENTATION: BLOCKED\nVERTICAL_SLICE_IMPLEMENTATION: APPROVED",
    )
    text = text.replace(
        "판정: `RECOMMENDED_PENDING_USER_APPROVAL / HUMAN_PLAYTEST_NOT_RUN`.",
        "판정: `USER_APPROVED_MERGED_PR120_MAIN_CANON / HUMAN_PLAYTEST_NOT_RUN`.",
    )
    text = text.replace(
        "판정: `RECOMMENDED_PENDING_USER_APPROVAL`.",
        "판정: `USER_APPROVED_MERGED_PR120_MAIN_CANON`.",
    )
    text = text.replace(
        "| 이 문서의 10개 Decision | RECOMMENDED_PENDING_USER_APPROVAL |",
        "| 이 문서의 10개 Decision | MAIN_CANON / MERGED_PR120 |",
    )
    text = text.replace(
        "| 제품 구현 | BLOCKED |",
        "| 일반 제품 구현 | BLOCKED |\n| 버티컬 슬라이스 구현 | APPROVED / NAMESPACE_SCOPED |",
    )
    text = text.replace("R2_BATCH_006_DRAFT_10_OF_10", "R2_BATCH_006_APPROVED_10_OF_10")
    text = text.replace("READY_FOR_USER_REVIEW", "MERGED_PR120_MAIN_CANON")
    text = text.replace(
        "## 1. 제안 목적",
        "## 1. 승인 목적",
    )
    if "GENERAL_PRODUCT_IMPLEMENTATION_REMAINS_BLOCKED" not in text:
        scope = """

## 구현 승인 범위

```yaml
GENERAL_PRODUCT_IMPLEMENTATION_REMAINS_BLOCKED: true
VERTICAL_SLICE_IMPLEMENTATION: APPROVED
APPROVED_NAMESPACES:
  - scripts/vertical_slice/
  - data/vertical_slice/
  - scenes/vertical_slice/
  - tests/vertical_slice/
FINAL_BALANCE_APPROVAL: false
HUMAN_PLAYTEST: NOT_RUN
```

이번 승인은 승인된 대표 버티컬 슬라이스 구현에만 적용한다. 다른 제품 경로, 전체 콘텐츠 생산, 최종 밸런스, 출시 승인은 열지 않는다.
"""
        text = text.replace("## 승인·병합 증거", scope.rstrip() + "\n\n## 승인·병합 증거", 1)
    write_text(PROPOSAL, text)


def normalize_current_docs() -> None:
    for path in (CURRENT_DECISIONS, ACTIVE_CONTEXT, ROADMAP, GATES):
        text = path.read_text(encoding="utf-8")
        text = text.replace("제품 구현: `VERTICAL_SLICE_IMPLEMENTATION_APPROVED`", "제품 구현: `BLOCKED`")
        text = text.replace("PRODUCT_IMPLEMENTATION: VERTICAL_SLICE_IMPLEMENTATION_APPROVED", "PRODUCT_IMPLEMENTATION: BLOCKED")
        write_text(path, text)

    decisions = CURRENT_DECISIONS.read_text(encoding="utf-8")
    if "> 버티컬 슬라이스 구현: `APPROVED / MERGED_PR120_MAIN_CANON`" not in decisions:
        decisions = decisions.replace(
            "> 제품 구현: `BLOCKED`",
            "> 제품 구현: `BLOCKED`\n>\n> 버티컬 슬라이스 구현: `APPROVED / MERGED_PR120_MAIN_CANON`",
            1,
        )
    if "R2_CHECKPOINT_005_CLOSED_MAIN_CANON" not in decisions:
        decisions = decisions.replace(
            "> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / CLOSURE_PR117_MERGED_MAIN_CANON`",
            "> `R2_CHECKPOINT_005_CLOSED_MAIN_CANON / R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / CLOSURE_PR117_MERGED_MAIN_CANON`",
            1,
        )
    write_text(CURRENT_DECISIONS, decisions)

    active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
    active = active.replace(
        "- 현재 단계: `R2_CORE_SESSION_META_LOOP / R2_CHECKPOINT_005_CLOSED_MAIN_CANON`",
        "- 현재 단계: `R2_CORE_SESSION_META_LOOP / R2_BATCH_006_APPROVED_MAIN_CANON`",
    )
    active = active.replace("- 현재 승인 카운터: `0/10`", "- 현재 승인 카운터: `10/10`")
    active = active.replace("R2_BATCH_006: NOT_STARTED_0_OF_10", "R2_BATCH_006: APPROVED_10_OF_10")
    if "- 버티컬 슬라이스 구현: `APPROVED / MERGED_PR120_MAIN_CANON`" not in active:
        active = active.replace(
            "- 제품 구현: `BLOCKED`",
            "- 제품 구현: `BLOCKED`\n- 버티컬 슬라이스 구현: `APPROVED / MERGED_PR120_MAIN_CANON`",
            1,
        )
    if "VERTICAL_SLICE_IMPLEMENTATION: APPROVED" not in active:
        active = active.replace(
            "PRODUCT_IMPLEMENTATION: BLOCKED",
            "PRODUCT_IMPLEMENTATION: BLOCKED\nVERTICAL_SLICE_IMPLEMENTATION: APPROVED",
            1,
        )
    active = re.sub(
        r"## 다음 작업\n.*?\n과거 배치 진행 카운터와 PR 대기 문구는 역사 문서에서만 조회한다\.",
        """## 다음 작업

1. 승인된 구현 계획 Task 1 Schema·UID·SaveEnvelope TDD
2. `scripts/data/scenes/tests/vertical_slice/` 격리 경계 유지
3. Task별 RED → GREEN → REFACTOR 및 Draft PR 검증
4. Android 빌드·실기기 저장 복구 검증
5. 외부 3~5명 사람 플레이테스트

과거 배치 진행 카운터와 PR 대기 문구는 역사 문서에서만 조회한다.""",
        active,
        flags=re.S,
    )
    write_text(ACTIVE_CONTEXT, active)

    roadmap = ROADMAP.read_text(encoding="utf-8")
    roadmap = roadmap.replace("CURRENT_STAGE_STATUS: R2_CHECKPOINT_005_CLOSED_MAIN_CANON", "CURRENT_STAGE_STATUS: R2_BATCH_006_APPROVED_MAIN_CANON")
    roadmap = roadmap.replace("R2_BATCH_006: NOT_STARTED_0_OF_10", "R2_BATCH_006: APPROVED_10_OF_10")
    if "VERTICAL_SLICE_IMPLEMENTATION: APPROVED" not in roadmap:
        roadmap = roadmap.replace("PRODUCT_IMPLEMENTATION: BLOCKED", "PRODUCT_IMPLEMENTATION: BLOCKED\nVERTICAL_SLICE_IMPLEMENTATION: APPROVED", 1)
    write_text(ROADMAP, roadmap)

    gates = GATES.read_text(encoding="utf-8")
    gates = gates.replace("R2_STATUS: R2_CHECKPOINT_005_CLOSED_MAIN_CANON", "R2_STATUS: R2_BATCH_006_APPROVED_MAIN_CANON")
    gates = gates.replace("R2_BATCH_006: NOT_STARTED_0_OF_10", "R2_BATCH_006: APPROVED_10_OF_10")
    gates = gates.replace("CODEX_IMPLEMENTATION_GATE: VERTICAL_SLICE_APPROVED", "CODEX_IMPLEMENTATION_GATE: VERTICAL_SLICE_APPROVED")
    gates = gates.replace("VERTICAL_SLICE_CODE_GATE: USER_APPROVED", "VERTICAL_SLICE_CODE_GATE: USER_APPROVED")
    if "GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED" not in gates:
        gates = gates.replace("PRODUCT_IMPLEMENTATION: BLOCKED", "PRODUCT_IMPLEMENTATION: BLOCKED\nGENERAL_PRODUCT_IMPLEMENTATION: BLOCKED\nVERTICAL_SLICE_IMPLEMENTATION: APPROVED", 1)
    write_text(GATES, gates)


def update_feature_tests() -> None:
    pattern_forward = re.compile(
        r'self\.assertEqual\(\s*"R2_CHECKPOINT_005_CLOSED_MAIN_CANON",\s*self\.registry\["stage_status"\],?\s*\)',
        re.S,
    )
    replacement_forward = 'self.assertEqual("R2_BATCH_006_APPROVED_MAIN_CANON", self.registry["stage_status"])'
    for rel in FEATURE_TESTS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        text = pattern_forward.sub(replacement_forward, text)
        if rel == "tests/test_base_v942_planning_first_adoption.py":
            text = text.replace('self.assertEqual("0/10", self.registry["next_approval_counter"])', 'self.assertEqual("10/10", self.registry["next_approval_counter"])')
        write_text(path, text)


def rewrite_checkpoint_tests() -> None:
    path = ROOT / "tests/test_r2_checkpoint_005_postmerge_closure.py"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'self\.assertEqual\(\s*"R2_CHECKPOINT_005_CLOSED_MAIN_CANON",\s*self\.registry\["stage_status"\],\s*\)',
        'self.assertEqual("R2_BATCH_006_APPROVED_MAIN_CANON", self.registry["stage_status"])',
        text,
        flags=re.S,
    )
    text = text.replace('self.assertEqual("0/10", self.registry["next_approval_counter"])', 'self.assertEqual("10/10", self.registry["next_approval_counter"])')
    text = text.replace(
        '"R2_BATCH_006_NOT_STARTED_0_OF_10",\n            "BLOCKED",',
        '"R2_BATCH_006_APPROVED_10_OF_10",\n            "VERTICAL_SLICE_IMPLEMENTATION_APPROVED",\n            "BLOCKED",',
    )
    write_text(path, text)

    path = ROOT / "tests/test_r2_checkpoint_005_main_canon_finalization.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '"R2_BATCH_006_NOT_STARTED_0_OF_10",\n            "PRODUCT_IMPLEMENTATION: BLOCKED",',
        '"R2_BATCH_006_APPROVED_10_OF_10",\n            "PRODUCT_IMPLEMENTATION: BLOCKED",\n            "VERTICAL_SLICE_IMPLEMENTATION: APPROVED",',
    )
    text = text.replace(
        'registry["stage_status"],\n            "R2_CHECKPOINT_005_CLOSED_MAIN_CANON",',
        'registry["stage_status"],\n            "R2_BATCH_006_APPROVED_MAIN_CANON",',
    )
    text = text.replace('self.assertEqual(registry["active_batch"]["status"], "NOT_STARTED")', 'self.assertEqual(registry["active_batch"]["status"], "APPROVED_MERGED_PR120_MAIN_CANON")')
    text = text.replace('self.assertEqual(registry["active_batch"]["approved_count"], 0)', 'self.assertEqual(registry["active_batch"]["approved_count"], 10)')
    if 'self.assertEqual(registry["vertical_slice_implementation"], "APPROVED")' not in text:
        text = text.replace(
            'self.assertEqual(registry["product_implementation"], "BLOCKED")',
            'self.assertEqual(registry["product_implementation"], "BLOCKED")\n        self.assertEqual(registry["vertical_slice_implementation"], "APPROVED")',
        )
    write_text(path, text)


def rewrite_batch006_tests() -> None:
    path = ROOT / "tests/test_r2_batch_006_vertical_slice_proposal.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("test_registry_is_a_ten_decision_unapproved_proposal", "test_registry_is_a_ten_decision_approved_main_canon")
    text = text.replace('registry["status"], "DRAFT_PENDING_USER_APPROVAL"', 'registry["status"], "USER_APPROVED_MERGED_PR120_MAIN_CANON"')
    text = text.replace('registry["product_implementation"], "BLOCKED")', 'registry["product_implementation"], "BLOCKED")\n        self.assertEqual(registry["vertical_slice_implementation"], "APPROVED")')
    text = text.replace('decision["status"], "RECOMMENDED_PENDING_USER_APPROVAL"', 'decision["status"], "USER_APPROVED_MERGED_PR120_MAIN_CANON"')
    text = text.replace('decision["authority"], "PROPOSAL_ONLY_NOT_MAIN_CANON"', 'decision["authority"], "MAIN_CANON"')
    text = text.replace(
        '"PRODUCT_IMPLEMENTATION: BLOCKED",\n            "HUMAN_PLAYTEST: NOT_RUN",',
        '"PRODUCT_IMPLEMENTATION: BLOCKED",\n            "VERTICAL_SLICE_IMPLEMENTATION: APPROVED",\n            "HUMAN_PLAYTEST: NOT_RUN",',
    )
    write_text(path, text)

    path = ROOT / "tests/test_r2_batch_006_main_canon_closure.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('self.assertEqual(registry["product_implementation"], "VERTICAL_SLICE_IMPLEMENTATION_APPROVED")', 'self.assertEqual(registry["product_implementation"], "BLOCKED")\n        self.assertEqual(registry["vertical_slice_implementation"], "APPROVED")')
    text = text.replace('self.assertEqual(current["product_implementation"], "VERTICAL_SLICE_IMPLEMENTATION_APPROVED")', 'self.assertEqual(current["product_implementation"], "BLOCKED")\n        self.assertEqual(current["vertical_slice_implementation"], "APPROVED")')
    write_text(path, text)


def update_health_hash() -> None:
    if not HEALTH.exists():
        return
    health = json.loads(HEALTH.read_text(encoding="utf-8"))
    digest = hashlib.sha256(CURRENT_DECISIONS.read_bytes()).hexdigest()
    for item in health.get("evidence", {}).get("operating", []):
        if item.get("id") == "BS-CURRENT-DECISIONS":
            item["sha256"] = digest
    HEALTH.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    normalize_registries()
    normalize_proposal_doc()
    normalize_current_docs()
    update_feature_tests()
    rewrite_checkpoint_tests()
    rewrite_batch006_tests()
    update_health_hash()


if __name__ == "__main__":
    main()
