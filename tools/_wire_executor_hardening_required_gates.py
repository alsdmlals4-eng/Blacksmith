from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    "tools/start_blacksmith_local_executor.ps1",
    "tests/test_blacksmith_dedicated_local_executor_bootstrap.py",
    "docs/decisions/BS-OPS-20260811-03_DEDICATED_LOCAL_EXECUTOR_BOOTSTRAP.md",
]


def insert_paths(path: str, anchor: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if all(f'      - "{item}"' in text for item in PATHS):
        return
    if anchor not in text:
        raise RuntimeError(f"anchor missing in {path}: {anchor!r}")
    block = anchor + "\n" + "\n".join(f'      - "{item}"' for item in PATHS)
    target.write_text(text.replace(anchor, block, 1), encoding="utf-8", newline="\n")


insert_paths(
    ".github/workflows/validate-base-v942-planning-first-adoption.yml",
    '      - "CURRENT_CONFIRMED_DECISIONS.md"',
)
insert_paths(
    ".github/workflows/gut-validation.yml",
    '      - ".github/workflows/python-validation.yml"',
)
insert_paths(
    ".github/workflows/validate-higodot-gut-authority-gate.yml",
    "      - docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json",
)

print("Local executor hardening paths wired to Planning First, GUT, and HiGodot authority gates")
