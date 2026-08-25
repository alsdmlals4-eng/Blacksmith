#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_BRIEF_APPROVAL_2026-08-25.md"

REQUIRED = (
    "BS-VIS-20260820-01",
    "BS-VIS-20260820-02",
    "BS-VIS-20260820-05",
    "BS-VIS-20260820-06",
    "BS-VIS-20260820-09",
    "BS-VIS-20260824-10",
    "USER_APPROVED_FOR_GENERATION",
    "STYLIZED_DARK_FORGE = CURRENT",
    "REFERENCE_ONLY_LAYOUT_DENSITY",
    "IMAGE_GENERATION = NOT_RUN",
    "PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION",
)


def main() -> int:
    failures: list[str] = []
    try:
        text = DECISION.read_text(encoding="utf-8")
    except OSError as exc:
        print("Visual GDD brief approval contract FAILED")
        print(f"- cannot read {DECISION.relative_to(ROOT)}: {exc}")
        return 1

    for token in REQUIRED:
        if token not in text:
            failures.append(f"missing required token: {token}")

    if failures:
        print("Visual GDD brief approval contract FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Visual GDD brief approval contract PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
