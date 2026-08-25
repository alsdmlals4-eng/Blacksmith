from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs/planning/BLACKSMITH_P0_VISUAL_04_08_REVIEW_20260825.md"

REQUIRED = (
    "BS-VIS-20260820-04",
    "BS-VIS-20260820-08",
    "REVIEW_COMPLETE / READY_FOR_USER_APPROVAL_FOR_GENERATION",
    "LEARN / BUILD_CONFIDENCE / FIRST_STOP_POINT / TENSION / HIGH_STAKES / MASTERY",
    "STATIC_SCREEN_STATE_MATRIX",
    "DYNAMIC_FEEDBACK_OWNER = BS-VIS-20260820-02",
    "MAX determines structure state",
    "EXISTING_STATS_UNCHANGED",
    "NEW_ENHANCEMENT_EFFECT_ONLY",
    "USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE",
    "IMAGE_GENERATION = NOT_RUN",
    "PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION",
)


def main() -> int:
    try:
        text = REVIEW.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"P0 Visual 04/08 review contract FAILED\n- cannot read {REVIEW.relative_to(ROOT)}: {exc}")
        return 1

    errors = [f"missing token: {token}" for token in REQUIRED if token not in text]
    if errors:
        print("P0 Visual 04/08 review contract FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("P0 Visual 04/08 review contract PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
