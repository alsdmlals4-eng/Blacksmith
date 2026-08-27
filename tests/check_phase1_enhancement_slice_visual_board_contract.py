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
            "PANEL_04 = PRECISION_AND_RISK_RUN",
            "PANEL_05 = CUSTOMER_WORLD_RESULT",
            "DO_NOT_FAKE_DAMAGE_FOR_DEMONSTRATION = TRUE",
            "TARGET_PLAYER_TIME = 6_TO_8_MINUTES / PHASE_1_HYPOTHESIS",
        ),
    )
    require_tokens(
        ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md",
        (
            "CURRENT_PHASE_1_SLICE = B_ENHANCEMENT_FIRST_SAME_UID_LIFECYCLE",
            "PHASE_1_ENHANCEMENT_WINDOW = +0_TO_+10 + +11_TO_+15",
            "PHASE_1_TARGET_SESSION_DURATION = 6_TO_8_MINUTES",
        ),
    )
    print("phase1 enhancement slice visual board contract: PASS")


if __name__ == "__main__":
    main()
