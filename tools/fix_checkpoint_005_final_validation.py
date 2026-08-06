from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "[기획서]" / "00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HEALTH = ROOT / "docs" / "PROJECT_OPERATING_HEALTH.json"


def _update_active() -> None:
    text = ACTIVE.read_text(encoding="utf-8")
    marker = "- 현재 단계: `R2_CORE_SESSION_META_LOOP / R2_CHECKPOINT_005_CLOSED_MAIN_CANON`\n"
    counter = "- 현재 승인 카운터: `0/10`\n"
    if counter not in text:
        text = text.replace(marker, marker + counter, 1)
    ACTIVE.write_text(text.rstrip() + "\n", encoding="utf-8")


def _update_hub_merge_routes() -> None:
    for path in (ROADMAP, GATES):
        text = path.read_text(encoding="utf-8")
        if "MERGED_PR109" not in text:
            text = text.replace(
                "`R2_BATCH_005_CLOSED_10_OF_10 / R2_BATCH_006_NOT_STARTED_0_OF_10`",
                "`R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / R2_BATCH_006_NOT_STARTED_0_OF_10`",
                1,
            )
        path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _update_health_hash() -> None:
    health = json.loads(HEALTH.read_text(encoding="utf-8"))
    digest = hashlib.sha256(CURRENT.read_bytes()).hexdigest()
    records = health["evidence"]["operating"]
    record = next(item for item in records if item["id"] == "BS-CURRENT-DECISIONS")
    record["sha256"] = digest
    HEALTH.write_text(
        json.dumps(health, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    _update_active()
    _update_hub_merge_routes()
    _update_health_hash()


if __name__ == "__main__":
    main()
