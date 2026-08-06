from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGE_SHA = "a8a94343c78a68bf7bb14b411e7741f43b257138"
SOURCE_HEAD = "388eff03c61126d8021601c3ab84efaa2133253e"
DECISION_IDS = [
    "BS-VS-20260806-01",
    "BS-SAVE-20260806-01",
    "BS-MATERIAL-20260806-01",
    "BS-CRAFT-20260806-01",
    "BS-ITEM-20260806-07",
    "BS-ENHANCE-20260806-01",
    "BS-ENHANCE-20260806-02",
    "BS-CATALYST-20260806-01",
    "BS-CUSTOMER-20260806-02",
    "BS-CHRONICLE-20260806-01",
]

PROPOSAL = ROOT / "docs/planning/BLACKSMITH_R2_BATCH_006_VERTICAL_SLICE_CANON_PROPOSAL_2026.md"
PROPOSAL_REGISTRY = ROOT / "docs/planning/R2_BATCH_006_VERTICAL_SLICE_PROPOSAL_REGISTRY.json"
CURRENT_REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CURRENT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
ROADMAP = ROOT / "[기획서]/00_프로젝트_허브/ROADMAP.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
HEALTH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"


def _replace_all(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        text = text.replace(old, new)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _promote_proposal() -> dict:
    _replace_all(
        PROPOSAL,
        [
            ("# Blacksmith R2 Batch 006 — Godot Vertical Slice Canon Proposal", "# Blacksmith R2 Batch 006 — Godot Vertical Slice Canon"),
            ("`DRAFT_PENDING_USER_APPROVAL`", "`USER_APPROVED_MERGED_PR120_MAIN_CANON`"),
            ("`PROPOSAL_ONLY_NOT_MAIN_CANON`", "`MAIN_CANON`"),
            ("기준 main: `303be5eccd792988cf398e7d54e987373f3b6f71`", f"승인 병합 main: `{MERGE_SHA}`"),
            ("PRODUCT_IMPLEMENTATION: BLOCKED", "PRODUCT_IMPLEMENTATION: VERTICAL_SLICE_IMPLEMENTATION_APPROVED"),
        ],
    )
    text = PROPOSAL.read_text(encoding="utf-8")
    marker = "## 승인·병합 증거"
    if marker not in text:
        text = text.rstrip() + f"""

## 승인·병합 증거

```yaml
USER_APPROVAL: PASS
SOURCE_PR: 120
SOURCE_EXACT_HEAD: {SOURCE_HEAD}
SQUASH_MERGE_SHA: {MERGE_SHA}
AUTHORITY: MAIN_CANON
IMPLEMENTATION_SCOPE: VERTICAL_SLICE_ONLY
FINAL_BALANCE_APPROVAL: false
HUMAN_PLAYTEST: NOT_RUN
```

사용자 승인은 Batch 006의 10개 Decision과 승인된 namespace의 Godot 버티컬 슬라이스 구현 착수를 허용한다. 전체 제품 구현, 최종 밸런스 확정, 사람 플레이테스트 완료를 의미하지 않는다.
"""
        PROPOSAL.write_text(text.rstrip() + "\n", encoding="utf-8")

    registry = json.loads(PROPOSAL_REGISTRY.read_text(encoding="utf-8"))
    registry["status"] = "USER_APPROVED_MERGED_PR120_MAIN_CANON"
    registry["authority"] = "MAIN_CANON"
    registry["source_exact_head"] = SOURCE_HEAD
    registry["merge_sha"] = MERGE_SHA
    registry["product_implementation"] = "VERTICAL_SLICE_IMPLEMENTATION_APPROVED"
    registry["vertical_slice_verdict"] = "APPROVED_FOR_IMPLEMENTATION"
    for item in registry["decisions"]:
        item["status"] = "USER_APPROVED_MERGED_PR120_MAIN_CANON"
        item["authority"] = "MAIN_CANON"
    PROPOSAL_REGISTRY.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return registry


def _promote_current_registry(batch_registry: dict) -> None:
    current = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
    current["stage_status"] = "R2_BATCH_006_APPROVED_MAIN_CANON"
    current["product_implementation"] = "VERTICAL_SLICE_IMPLEMENTATION_APPROVED"
    current["next_approval_counter"] = "10/10"
    current["human_playtest"] = "NOT_RUN"
    current["active_batch"] = {
        "id": "R2_BATCH_006",
        "status": "APPROVED_MERGED_PR120_MAIN_CANON",
        "approved_decisions": 10,
        "approved_count": 10,
        "counter": "10/10",
        "decisions": DECISION_IDS,
        "maximum_size": 10,
        "maximum_count": 10,
        "planning_pr": 120,
        "planning_exact_head": SOURCE_HEAD,
        "planning_merge_sha": MERGE_SHA,
    }
    current.setdefault("immutable_merge_evidence", {})["batch_006"] = {
        "planning_pr": 120,
        "planning_exact_head": SOURCE_HEAD,
        "planning_merge_sha": MERGE_SHA,
        "status": "USER_APPROVED_MERGED_MAIN_CANON",
        "merge_method": "SQUASH",
        "github_readback": "PASS",
        "sheet_readback": "PENDING_CLOSURE_SYNC",
    }

    existing = {item.get("id") for item in current.get("current_decisions", [])}
    for item in batch_registry["decisions"]:
        if item["id"] in existing:
            continue
        current.setdefault("current_decisions", []).append(
            {
                "id": item["id"],
                "title": item["title"],
                "status": "USER_APPROVED_MERGED_PR120_MAIN_CANON",
                "canon": "docs/planning/BLACKSMITH_R2_BATCH_006_VERTICAL_SLICE_CANON_PROPOSAL_2026.md",
                "contract": {key: value for key, value in item.items() if key not in {"id", "title", "status", "authority"}},
            }
        )
    CURRENT_REGISTRY.write_text(
        json.dumps(current, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _promote_markdown_authority() -> None:
    replacements = [
        ("R2_BATCH_006_NOT_STARTED_0_OF_10", "R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON"),
        ("제품 구현: `BLOCKED`", "제품 구현: `VERTICAL_SLICE_IMPLEMENTATION_APPROVED`"),
        ("PRODUCT_IMPLEMENTATION: BLOCKED", "PRODUCT_IMPLEMENTATION: VERTICAL_SLICE_IMPLEMENTATION_APPROVED"),
        ("CODEX_IMPLEMENTATION_GATE: BLOCKED", "CODEX_IMPLEMENTATION_GATE: VERTICAL_SLICE_APPROVED"),
        ("VERTICAL_SLICE_CODE_GATE: USER_APPROVAL_REQUIRED", "VERTICAL_SLICE_CODE_GATE: USER_APPROVED"),
    ]
    for path in (CURRENT_DECISIONS, ACTIVE_CONTEXT, ROADMAP, GATES):
        _replace_all(path, replacements)

    decisions = CURRENT_DECISIONS.read_text(encoding="utf-8")
    decisions = decisions.replace(
        "<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->",
        "<!-- R2_BATCH_006_CURRENT_AUTHORITY -->",
        1,
    )
    decisions = decisions.replace(
        "> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**",
        "> **R2_BATCH_006_APPROVED_MAIN_CANON**",
        1,
    )
    authority_line = f"> `R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON / IMPLEMENTATION_APPROVED`\n>\n> source exact head: `{SOURCE_HEAD}` / squash merge: `{MERGE_SHA}`"
    if authority_line not in decisions:
        insertion = "> **R2_BATCH_006_APPROVED_MAIN_CANON**"
        decisions = decisions.replace(insertion, insertion + "\n>\n" + authority_line, 1)
    decisions = decisions.replace(
        "> 현재 승인 배치: `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109`",
        "> 현재 승인 배치: `R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON`",
    )
    decisions = decisions.replace(
        "> 제품 구현: `BLOCKED`",
        "> 제품 구현: `VERTICAL_SLICE_IMPLEMENTATION_APPROVED`",
    )
    CURRENT_DECISIONS.write_text(decisions.rstrip() + "\n", encoding="utf-8")

    active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
    active = active.replace(
        "<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->",
        "<!-- R2_BATCH_006_CURRENT_AUTHORITY -->",
        1,
    )
    active = active.replace(
        "> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**",
        "> **R2_BATCH_006_APPROVED_MAIN_CANON**",
        1,
    )
    if "MERGED_PR120_MAIN_CANON" not in active:
        active = active.replace(
            "> **R2_BATCH_006_APPROVED_MAIN_CANON**",
            f"> **R2_BATCH_006_APPROVED_MAIN_CANON**\n>\n> `R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON / VERTICAL_SLICE_IMPLEMENTATION_APPROVED`\n>\n> source exact head: `{SOURCE_HEAD}` / squash merge: `{MERGE_SHA}`",
            1,
        )
    ACTIVE_CONTEXT.write_text(active.rstrip() + "\n", encoding="utf-8")


def _update_health_hash() -> None:
    if not HEALTH.exists():
        return
    health = json.loads(HEALTH.read_text(encoding="utf-8"))
    digest = hashlib.sha256(CURRENT_DECISIONS.read_bytes()).hexdigest()
    for item in health.get("evidence", {}).get("operating", []):
        if item.get("id") == "BS-CURRENT-DECISIONS":
            item["sha256"] = digest
    HEALTH.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    batch_registry = _promote_proposal()
    _promote_current_registry(batch_registry)
    _promote_markdown_authority()
    _update_health_hash()


if __name__ == "__main__":
    main()
