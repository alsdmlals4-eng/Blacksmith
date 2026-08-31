from __future__ import annotations

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
GITIGNORE = ROOT / ".gitignore"


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> int:
    failures: list[str] = []
    tracked_tmp = [path for path in git("ls-files", "--", "tmp").stdout.splitlines() if path]
    if tracked_tmp:
        failures.append(f"temporary generated derivatives remain tracked: {tracked_tmp}")

    ignore_text = GITIGNORE.read_text(encoding="utf-8")
    if "tmp/" not in ignore_text.splitlines():
        failures.append("root .gitignore must keep future temporary generated derivatives out of Git")
    elif git("check-ignore", "-q", "tmp/future-derived-output.pdf").returncode != 0:
        failures.append("root tmp/ ignore rule does not ignore a future generated derivative")

    if failures:
        print("Temporary generated derivative hygiene FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Temporary generated derivative hygiene PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
