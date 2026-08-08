from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "higodot-task2-authoring-bridge.yml"
DRIVER = ROOT / "tools" / "higodot_task2_bridge.py"
RECIPE = ROOT / ".github" / "validation" / "higodot-task2-authoring-recipe.json"
TARGET_VERSION = "3.1.3"


def test_task2_bridge_targets_exact_godot_ai_313() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    driver = DRIVER.read_text(encoding="utf-8")
    recipe = json.loads(RECIPE.read_text(encoding="utf-8"))

    assert recipe["higodot_version"] == TARGET_VERSION
    assert f'TARGET_HIGODOT_VERSION = "{TARGET_VERSION}"' in driver
    assert f'HIGODOT_VERSION: "{TARGET_VERSION}"' in workflow
    assert f'godot-ai=={TARGET_VERSION}' in workflow
    assert f'actual != "{TARGET_VERSION}"' in workflow


def test_task2_bridge_no_longer_selects_305_runtime() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    driver = DRIVER.read_text(encoding="utf-8")
    recipe_text = RECIPE.read_text(encoding="utf-8")

    assert 'godot-ai==3.0.5' not in workflow
    assert 'HIGODOT_VERSION: "3.0.5"' not in workflow
    assert 'TARGET_HIGODOT_VERSION = "3.0.5"' not in driver
    assert '"higodot_version": "3.0.5"' not in recipe_text


def test_313_migration_keeps_verified_fastmcp_and_uv_exact() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert 'fastmcp==3.4.2' in workflow
    assert 'uv==0.12.3' in workflow
    assert 'actual_fastmcp != "3.4.2"' in workflow
    assert 'actual_uv != "0.12.3"' in workflow


def test_runtime_selectors_remain_exact_not_floating() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    for package in ("godot-ai", "fastmcp", "uv"):
        assert re.search(rf'{re.escape(package)}==[0-9]+\.[0-9]+\.[0-9]+', workflow), package
    for forbidden in (
        'godot-ai>=', 'godot-ai~=', 'godot-ai==latest',
        'fastmcp>=', 'fastmcp~=', 'fastmcp==latest',
        'uv>=', 'uv~=', 'uv==latest',
    ):
        assert forbidden not in workflow
