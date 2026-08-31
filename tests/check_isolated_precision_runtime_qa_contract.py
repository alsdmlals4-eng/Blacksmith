#!/usr/bin/env python3
"""Protect the disposable, player-save-isolated Precision runtime QA fixture."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/gut/unit/vertical_slice/test_vs_precision_isolated_runtime_qa.gd"


def main() -> None:
    assert FIXTURE.is_file(), "missing isolated Precision runtime QA fixture"
    source = FIXTURE.read_text(encoding="utf-8")

    assert 'const FIXTURE_SAVE_PATH := "user://gut/blacksmith_precision_runtime_qa_v4.json"' in source
    assert 'SaveServiceScript.new(FIXTURE_SAVE_PATH)' in source
    assert "SaveServiceScript.DEFAULT_SAVE_PATH" in source
    assert "request_enhancement_with_rolls" in source
    assert "load_envelope()" in source
    assert "_remove_fixture_files()" in source
    assert "func after_each() -> void:\n\t_remove_fixture_files()" in source
    assert "the QA fixture must clean its disposable save file" in source
    assert source.count("DEFAULT_SAVE_PATH") == 1, "fixture may only name the player path for its identity guard"
    assert "MOBILE_TOUCH_TARGET_HEIGHT" not in source, "fixture must measure runtime controls, not duplicate source tokens"
    assert "96.0" in source and "112.0" in source

    print("isolated Precision runtime QA contract: PASS")


if __name__ == "__main__":
    main()
