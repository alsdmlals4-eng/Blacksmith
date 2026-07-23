#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".json", ".py", ".gd", ".tscn", ".yml", ".yaml", ".txt", ".toml"}
IGNORED_PARTS = {".git", ".godot", "external", "artifacts", "__pycache__"}
CONFLICT_BLOCK = re.compile(
    r"(?ms)^<<<<<<<[^\n]*\n.*?^=======\s*$\n.*?^>>>>>>>[^\n]*$"
)


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"AGENTS.md", "README.md", "project.godot"}:
            yield path


def find_conflicts(root: Path) -> list[str]:
    conflicts: list[str] = []
    for path in iter_text_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        if CONFLICT_BLOCK.search(text):
            conflicts.append(path.relative_to(root).as_posix())
    return conflicts


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail when unresolved Git merge conflict blocks remain.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    conflicts = find_conflicts(root)
    if conflicts:
        print("Unresolved Git merge conflict blocks found:")
        for path in conflicts:
            print(f"- {path}")
        return 1

    print("No unresolved Git merge conflict blocks found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
