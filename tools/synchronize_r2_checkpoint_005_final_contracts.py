from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
ACTIVE_CONTEXT_PATH = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
ROOT_DECISIONS_PATH = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"

OLD_STAGE = "R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING"
NEW_STAGE = "R2_CHECKPOINT_005_CLOSED_MAIN_CANON"
CLOSURE_HEAD = "51d4acf4fc31233b4b218a6f20589fdbf2557ee2"
CLOSURE_MERGE = "06f03323c1309d8da0e6f5b9f4680a20ce388126"
CURRENT_MAIN_AT_AUDIT = "e525b7ca5df0d40a4dd7411789b8a36228063e84"

BATCH_005_DECISIONS = [
    "BS-CRAFT-20260805-02",
    "BS-CUSTOMER-20260805-01",
    "BS-UX-20260805-01",
    "BS-CUSTOMER-20260806-01",
    "BS-ITEM-20260806-01",
    "BS-ITEM-20260806-02",
    "BS-ITEM-20260806-03",
    "BS-ITEM-20260806-04",
    "BS-ITEM-20260806-05",
    "BS-ITEM-20260806-06",
]

OLD_ROOT_HEADER = """<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005 / POSTMERGE_CLOSURE_PENDING**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109 / MAIN_CANON`
>
> planning exact head: `77eba15415bc9ede661639b45bb526d5ce4410a5` / squash merge: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9`
>
> next batch: `R2_BATCH_006_NOT_STARTED_0_OF_10` / 제품 구현: `BLOCKED` / 사람 플레이테스트: `NOT_RUN`
"""

NEW_ROOT_HEADER = """<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / CLOSURE_PR117_MERGED_MAIN_CANON`
>
> planning exact head: `77eba15415bc9ede661639b45bb526d5ce4410a5` / planning squash merge: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9`
>
> closure exact head: `51d4acf4fc31233b4b218a6f20589fdbf2557ee2` / closure squash merge: `06f03323c1309d8da0e6f5b9f4680a20ce388126`
>
> next batch: `R2_BATCH_006_NOT_STARTED_0_OF_10` / 제품 구현: `BLOCKED` / 사람 플레이테스트: `NOT_RUN`
"""

ACTIVE_COMPATIBILITY_SECTION = """

## 승인 Decision 호환 인덱스

다음 카운터는 현재 활성 상태가 아니라 Batch 005의 **역사적 승인 순서**다.

```text
BS-CRAFT-20260805-02 / R2_BATCH_005_1_OF_10
BS-CUSTOMER-20260805-01 / R2_BATCH_005_2_OF_10
BS-UX-20260805-01 / R2_BATCH_005_3_OF_10
BS-CUSTOMER-20260806-01 / R2_BATCH_005_4_OF_10
BS-ITEM-20260806-01 / R2_BATCH_005_5_OF_10
BS-ITEM-20260806-02 / R2_BATCH_005_6_OF_10
BS-ITEM-20260806-03 / R2_BATCH_005_7_OF_10
BS-ITEM-20260806-04 / R2_BATCH_005_8_OF_10
BS-ITEM-20260806-05 / R2_BATCH_005_9_OF_10
BS-ITEM-20260806-06 / R2_BATCH_005_10_OF_10
```

대표 예술성 표기는 `예술성 27`이며, 도메인은 `고정 설계 최대치 없음`이다.
"""


def _replace_live_stage_expectations() -> None:
    candidates = list((ROOT / "tests").rglob("*.py"))
    candidates.append(ROOT / "tools/audit_project_operating_system.py")
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        updated = text.replace(OLD_STAGE, NEW_STAGE)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def _update_root_decisions() -> None:
    text = ROOT_DECISIONS_PATH.read_text(encoding="utf-8")
    if OLD_ROOT_HEADER in text:
        text = text.replace(OLD_ROOT_HEADER, NEW_ROOT_HEADER, 1)
    else:
        text = text.replace(
            "<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->",
            NEW_ROOT_HEADER.rstrip(),
            1,
        )
    ROOT_DECISIONS_PATH.write_text(text, encoding="utf-8")


def _update_active_context() -> None:
    text = ACTIVE_CONTEXT_PATH.read_text(encoding="utf-8")
    if "## 승인 Decision 호환 인덱스" not in text:
        text = text.rstrip() + ACTIVE_COMPATIBILITY_SECTION + "\n"
    ACTIVE_CONTEXT_PATH.write_text(text, encoding="utf-8")


def _update_registry() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["stage_status"] = NEW_STAGE
    registry["next_approval_counter"] = "0/10"
    registry["product_implementation"] = "BLOCKED"
    registry["human_playtest"] = "NOT_RUN"
    registry["closed_batch"] = {
        "id": "R2_BATCH_005",
        "status": "CLOSED_MERGED_PR109_AND_CLOSURE_PR117_MAIN_CANON",
        "approved_decisions": 10,
        "approved_count": 10,
        "counter": "10/10",
        "decisions": BATCH_005_DECISIONS,
        "maximum_size": 10,
        "maximum_count": 10,
        "closure_pr": 117,
        "closure_merge_sha": CLOSURE_MERGE,
    }
    registry["active_batch"] = {
        "id": "R2_BATCH_006",
        "status": "NOT_STARTED",
        "approved_decisions": 0,
        "approved_count": 0,
        "counter": "0/10",
        "decisions": [],
        "maximum_size": 10,
        "maximum_count": 10,
    }
    evidence = registry["immutable_merge_evidence"]["checkpoint_005"]
    evidence["closure_exact_head"] = CLOSURE_HEAD
    evidence["closure_merge_sha"] = CLOSURE_MERGE
    evidence["closure_status"] = "MERGED_MAIN_CANON"
    evidence["closure_github_readback"] = "PASS"
    evidence["closure_sheet_readback"] = "PASS"
    evidence["current_main_at_finalization_audit"] = CURRENT_MAIN_AT_AUDIT
    registry.setdefault("validation_boundaries", {})["human_playtest"] = "NOT_RUN"
    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    _replace_live_stage_expectations()
    _update_root_decisions()
    _update_active_context()
    _update_registry()


if __name__ == "__main__":
    main()
