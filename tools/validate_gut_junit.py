from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree


def _attribute_int(node: ElementTree.Element, name: str) -> int | None:
    value = node.attrib.get(name)
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"invalid JUnit {name} value: {value!r}") from exc


def _aggregate(root: ElementTree.Element, name: str) -> int:
    direct = _attribute_int(root, name)
    if direct is not None:
        return direct
    suites = root.findall(".//testsuite")
    values = [_attribute_int(suite, name) for suite in suites]
    present = [value for value in values if value is not None]
    if present:
        return sum(present)
    if name == "tests":
        return len(root.findall(".//testcase"))
    if name == "failures":
        return len(root.findall(".//failure"))
    if name == "errors":
        return len(root.findall(".//error"))
    if name == "skipped":
        return len(root.findall(".//skipped"))
    return 0


def validate_junit(
    path: Path,
    *,
    minimum_tests: int = 1,
    fail_on_skipped: bool = True,
) -> dict[str, int | str]:
    if not path.is_file():
        raise ValueError(f"missing JUnit file: {path}")
    try:
        root = ElementTree.parse(path).getroot()
    except ElementTree.ParseError as exc:
        raise ValueError(f"invalid JUnit XML: {path}") from exc

    summary: dict[str, int | str] = {
        "path": str(path),
        "tests": _aggregate(root, "tests"),
        "failures": _aggregate(root, "failures"),
        "errors": _aggregate(root, "errors"),
        "skipped": _aggregate(root, "skipped"),
    }
    tests = int(summary["tests"])
    failures = int(summary["failures"])
    errors = int(summary["errors"])
    skipped = int(summary["skipped"])

    if tests < minimum_tests:
        raise ValueError(
            f"GUT discovered {tests} tests; minimum required is {minimum_tests}"
        )
    if failures or errors:
        raise ValueError(
            f"GUT JUnit reported failures={failures}, errors={errors}"
        )
    if fail_on_skipped and skipped:
        raise ValueError(f"GUT JUnit reported skipped={skipped}")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail closed on missing, empty, skipped, or failing GUT JUnit results."
    )
    parser.add_argument("junit", type=Path)
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--allow-skipped", action="store_true")
    args = parser.parse_args()

    try:
        summary = validate_junit(
            args.junit,
            minimum_tests=args.minimum_tests,
            fail_on_skipped=not args.allow_skipped,
        )
    except ValueError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
