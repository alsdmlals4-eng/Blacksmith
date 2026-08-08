from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "higodot-task2-authoring-bridge.yml"


def test_higodot_runtime_pins_verified_fastmcp_version() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert 'godot-ai==3.0.5' in text
    assert 'fastmcp==3.4.2' in text
    assert 'version("fastmcp")' in text
    assert 'actual_fastmcp != "3.4.2"' in text


def test_higodot_runtime_does_not_install_floating_fastmcp_selector() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    for forbidden in (
        'fastmcp>=',
        'fastmcp~=',
        'fastmcp>',
        'fastmcp<',
        'fastmcp @ git+',
        'fastmcp==latest',
    ):
        assert forbidden not in text
