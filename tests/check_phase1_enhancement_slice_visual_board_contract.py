from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    assert not missing, f"{path.name}: missing {missing}"


def main() -> None:
    require_tokens(
        ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md",
        (
            "PHASE_1_SLICE_VARIANT = B_ENHANCEMENT_FIRST_SAME_UID_LIFECYCLE",
            "PHASE_1_ENHANCEMENT_PATH = +0_TO_+10_INDIVIDUAL_ATTEMPTS",
            "PHASE_1_RISK_WINDOW = +11_TO_+15_MULTIPLE_STOP_PUSH_OPPORTUNITIES",
            "PHASE_1_LIFECYCLE_CLOSURE = ONE_SAME_UID_CUSTOMER_ACTUAL_USE_RESULT",
            "PHASE_1_TARGET_SESSION_DURATION = 6_TO_8_MINUTES",
            "PHASE_1_DURATION_STATUS = EXPERIENCE_HYPOTHESIS_NOT_RUNTIME_TIMER",
            "PHASE_1_RESULT_TIMING = HANDOFF_TO_ONE_WORKSHOP_RETURN_BEAT_TO_RESULT",
            "PHASE_1_RETURN_BEAT = NON_ECONOMIC / NO_SECOND_ITEM / NO_CUSTOMER_MANAGEMENT",
            "CRAFT_FEEDBACK_MILESTONES = EVERY_5_LEVELS",
            "+5 = CRAFT_FEEDBACK_MILESTONE_ONLY",
            "+10 = CRAFT_FEEDBACK_MILESTONE_PLUS_SOLE_PRECISION_ENHANCEMENT",
            "NO_ADDITIONAL_PRECISION_AT_OTHER_5_LEVEL_MILESTONES = TRUE",
        ),
    )
    require_tokens(
        ROOT / "docs/planning/BLACKSMITH_VISUAL_DIRECTION_LOCK_PACKET_20260828.md",
        (
            "LOCKED_VISUAL_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK",
            "NO_NEW_GENERATED_RASTER_FOR_THIS_PACKET = TRUE",
            "RELEASE_RIGHTS_STATUS = RELEASE_BLOCKED_UNVERIFIED",
        ),
    )
    require_tokens(
        ROOT / "docs/planning/PROJECT_CORE_SCENE_VISUAL_BOARD_20260828.md",
        (
            "ARTIFACT_CLASS = PLANNING_VISUALIZATION_ONLY",
            "RUNTIME_ASSET_STATUS = NOT_A_RUNTIME_ASSET",
            "PANEL_03 = ENHANCEMENT_MAIN",
            "PANEL_04 = RECURRING_PRECISION_TAG_CHOICE",
            "PANEL_05 = CUSTOMER_WORLD_RESULT",
            "DO_NOT_FAKE_DAMAGE_FOR_DEMONSTRATION = TRUE",
            "TARGET_PLAYER_TIME = 6_TO_8_MINUTES / PHASE_1_HYPOTHESIS",
            "POST_HANDOFF_TRANSITION = ONE_WORKSHOP_RETURN_BEAT",
            "NO_FAKE_WAITING_OR_CUSTOMER_MANAGEMENT_SYSTEM = TRUE",
            "FIVE_LEVEL_CRAFT_RHYTHM = EVERY_5_LEVEL_PRESENTATION_RISE / EVERY_10_LEVEL_PRECISION_TAG_GROWTH",
            "Decision38 owns targets `10..100`, max three active Tags, stages I–IV",
            "GENERATED_CANDIDATES = MAIN_MENU + WORKSHOP_RECURRING_PRECISION + CUSTOMER_WORLD_RESULT",
            "RUNTIME_PROMOTION = BLOCKED_PENDING_USER_LOCK",
        ),
    )
    require_tokens(
        ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md",
        (
            "CURRENT_PHASE_1_SLICE = B_ENHANCEMENT_FIRST_SAME_UID_LIFECYCLE",
            "PHASE_1_ENHANCEMENT_WINDOW = +0_TO_+10 + +11_TO_+15",
            "PHASE_1_TARGET_SESSION_DURATION = 6_TO_8_MINUTES",
            "PHASE_1_RESULT_TIMING = HANDOFF_TO_WORKSHOP_RETURN_BEAT_TO_RESULT",
            "CRAFT_FEEDBACK_MILESTONES = EVERY_5_LEVELS / +10_SOLE_PRECISION",
        ),
    )
    print("phase1 enhancement slice visual board contract: PASS")


if __name__ == "__main__":
    main()
