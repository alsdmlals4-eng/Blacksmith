from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING_PR = 109
CLOSURE_PR = 117
PLANNING_HEAD = "77eba15415bc9ede661639b45bb526d5ce4410a5"
PLANNING_MERGE = "31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9"
CLOSURE_BRANCH = "agent/r2-checkpoint-005-postmerge-closure"
RED_HEAD = "6c7ab4418971bf3d505b42349bfb0bd67e2215b0"
RED_RUN = 306

CURRENT_DOCS = (
    ROOT / "CURRENT_CONFIRMED_DECISIONS.md",
    ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    ROOT / "[기획서]/00_프로젝트_허브/ROADMAP.md",
    ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
)
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CLOSURE = ROOT / "docs/planning/BLACKSMITH_R2_CHECKPOINT_005_POSTMERGE_CLOSURE_2026.md"

BANNER = f"""<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005 / POSTMERGE_CLOSURE_PENDING**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109 / MAIN_CANON`
>
> planning exact head: `{PLANNING_HEAD}` / squash merge: `{PLANNING_MERGE}`
>
> next batch: `R2_BATCH_006_NOT_STARTED_0_OF_10` / 제품 구현: `BLOCKED` / 사람 플레이테스트: `NOT_RUN`

"""


def write_if_changed(path: Path, content: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == content:
        return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def add_banner(text: str) -> str:
    if "<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->" in text:
        return text
    first_break = text.find("\n")
    if first_break < 0:
        return text + "\n\n" + BANNER
    return text[: first_break + 1] + "\n" + BANNER + text[first_break + 1 :]


def close_markdown(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    text = add_banner(text)
    replacements = {
        "APPROVED_PENDING_MERGE": "MERGED_PR109 / MAIN_CANON",
        "DRAFT_PR109": "MERGED_PR109",
        "R2_BATCH_005_ACTIVE_10_OF_10": "R2_BATCH_005_CLOSED_10_OF_10",
        "R2_BATCH_005 / 10/10": "R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109",
        "NEXT_APPROVAL_COUNTER: 8/10": "NEXT_APPROVAL_COUNTER: 0/10",
        "NEXT_APPROVAL_COUNTER: 10/10": "NEXT_APPROVAL_COUNTER: 0/10",
        "현재 `R2_BATCH_005 / 7/10`이다.": "`R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109 / MAIN_CANON`이다.",
        "다음 행동: PR #109 체크포인트 검토·명시적 병합 승인 대기": "다음 행동: PR #117 폐쇄 정본 검증·명시적 병합 승인 대기",
        "PR #109 체크포인트 검토·명시적 병합 승인 대기": "PR #117 폐쇄 정본 검증·명시적 병합 승인 대기",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return write_if_changed(path, text)


def close_registry() -> bool:
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    payload["schema_version"] = max(int(payload.get("schema_version", 0)), 9)
    payload["stage_status"] = "R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING"
    payload["next_approval_counter"] = "0/10"
    payload.setdefault("immutable_merge_evidence", {})["checkpoint_005"] = {
        "planning_pr": PLANNING_PR,
        "planning_exact_head": PLANNING_HEAD,
        "planning_merge_sha": PLANNING_MERGE,
        "planning_status": "MERGED_MAIN_CANON",
        "closure_pr": CLOSURE_PR,
        "closure_branch": CLOSURE_BRANCH,
        "closure_status": "DRAFT_PR117_PENDING",
        "merge_method": "SQUASH",
        "github_readback": "PASS",
        "sheet_readback": "PASS",
    }
    batch_ids = {
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
    }
    found: set[str] = set()
    for item in payload.get("current_decisions", []):
        decision_id = item.get("id")
        if decision_id not in batch_ids:
            continue
        found.add(decision_id)
        status = str(item.get("status", ""))
        status = status.replace("APPROVED_PENDING_MERGE", "MERGED_PR109_MAIN_CANON")
        if "MERGED_PR109" not in status:
            status = f"{status}_MERGED_PR109_MAIN_CANON".strip("_")
        item["status"] = status
    missing = sorted(batch_ids - found)
    if missing:
        raise RuntimeError(f"missing Batch 005 decisions: {missing}")
    payload.setdefault("tdd_evidence", {})["checkpoint_005_closure_red"] = {
        "commit": RED_HEAD,
        "planning_first_run": RED_RUN,
        "status": "EXPECTED_FAILURE",
        "reason": "CURRENT_AUTHORITY_PREMERGE_STATE",
    }
    content = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    return write_if_changed(REGISTRY, content)


def close_closure_document() -> bool:
    content = f"""# Blacksmith R2 Checkpoint 005 Postmerge Closure

상태: `RED_OBSERVED / GREEN_SYNC_PENDING / DRAFT_PR117`

## Planning merge evidence

- planning PR: `#109`
- source exact head: `{PLANNING_HEAD}`
- squash merge: `{PLANNING_MERGE}`
- planning status: `MERGED_MAIN_CANON`
- closure PR: `#117`
- closure branch: `{CLOSURE_BRANCH}`

## Closure state

```text
R2_BATCH_005_CLOSED_10_OF_10
R2_BATCH_006_NOT_STARTED_0_OF_10
R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING
```

## Preserved gates

- 제품 구현: `BLOCKED`
- 사람 플레이테스트: `NOT_RUN`
- 보호된 제품 경로 변경: `0`
- 정확 수치: `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`
- 새 게임 기획 Decision: `NONE`

## TDD

### RED

- contract commit: `{RED_HEAD}`
- Planning-first: `{RED_RUN}` / `EXPECTED_FAILURE`
- 원인: 현재 권위 문서와 registry의 premerge 상태

### GREEN

- exact head: `PENDING`
- Planning-first: `PENDING`
- Base adoption: `PENDING`
- PR validation: `PENDING`

## Next gate

PR #117은 Draft·unmerged 상태를 유지한다. 명시적 사용자 승인 전에는 ready 전환이나 병합을 수행하지 않는다.
"""
    return write_if_changed(CLOSURE, content)


def main() -> int:
    changed: list[str] = []
    for path in CURRENT_DOCS:
        if close_markdown(path):
            changed.append(str(path.relative_to(ROOT)))
    if close_registry():
        changed.append(str(REGISTRY.relative_to(ROOT)))
    if close_closure_document():
        changed.append(str(CLOSURE.relative_to(ROOT)))
    print("changed=" + (",".join(changed) if changed else "NONE"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
