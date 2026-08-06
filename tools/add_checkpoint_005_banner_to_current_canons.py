from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md",
    ROOT / "docs/planning/BLACKSMITH_R2_FUNCTION_RECIPE_MATERIAL_FIT_AND_PLAYTEST_CANON_2026.md",
)
MARKER = "<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->"
BANNER = """<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005 / POSTMERGE_CLOSURE_PENDING**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109 / MAIN_CANON`
>
> planning exact head: `77eba15415bc9ede661639b45bb526d5ce4410a5` / squash merge: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9`
>
> next batch: `R2_BATCH_006_NOT_STARTED_0_OF_10` / 제품 구현: `BLOCKED` / 사람 플레이테스트: `NOT_RUN`

"""


def main() -> int:
    changed: list[str] = []
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        line_end = text.find("\n")
        if line_end < 0:
            updated = text + "\n\n" + BANNER
        else:
            updated = text[: line_end + 1] + "\n" + BANNER + text[line_end + 1 :]
        path.write_text(updated, encoding="utf-8", newline="\n")
        changed.append(str(path.relative_to(ROOT)))
    print("changed=" + (",".join(changed) if changed else "NONE"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
