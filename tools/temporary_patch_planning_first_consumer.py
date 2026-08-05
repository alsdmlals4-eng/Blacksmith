from pathlib import Path

path = Path("tests/test_base_v942_planning_first_adoption.py")
text = path.read_text(encoding="utf-8")
text = text.replace(
    'ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"\n',
    'ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"\nMIGRATION_STATE = ROOT / "docs/operations/BLACKSMITH_ADAPTER_MIGRATION_STATE_2026-08-06.json"\n',
)
old = '        self.assertEqual("BLOCKED", adapter["project_operating_state"]["product_implementation"])\n'
new = '        migration = load_json(MIGRATION_STATE)\n        preserved = migration["migrated_adapter_root_fields"]["project_operating_state"]\n        self.assertEqual("BLOCKED", preserved["product_implementation"])\n'
if text.count(old) != 1:
    raise SystemExit(f"expected one legacy assertion, got {text.count(old)}")
path.write_text(text.replace(old, new), encoding="utf-8")
