from pathlib import Path

root = Path(__file__).resolve().parents[1]
runner_path = root / "tools/run_project_operating_system_audit.py"
test_path = root / "tests/test_project_operating_system_audit_runner.py"

runner = runner_path.read_text(encoding="utf-8")

repls = [
    (
        'R3_ERSA_CANON = "docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md"\n',
        'R3_ERSA_CANON = "docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md"\nR3_CASSIA_CANON = "docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md"\n',
    ),
    (
        'R3_THIRD_DECISION = "BS-CONTENT-20260811-03"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-04"\n',
        'R3_THIRD_DECISION = "BS-CONTENT-20260811-03"\nR3_FOURTH_DECISION = "BS-CONTENT-20260811-04"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-05"\n',
    ),
    ('\'"next_approval_counter": "4/10"\',', '\'"next_approval_counter": "5/10"\','),
    (
        '        f\'"id": "{R3_THIRD_DECISION}"\',\n        f\'"id": "{R3_CURRENT_DECISION}"\',\n        \'"content_id": "COLLECTOR_01"\',\n',
        '        f\'"id": "{R3_THIRD_DECISION}"\',\n        f\'"id": "{R3_FOURTH_DECISION}"\',\n        f\'"id": "{R3_CURRENT_DECISION}"\',\n        \'"content_id": "COLLECTOR_01"\',\n',
    ),
    (
        '        \'"opaque_collector_or_exhibition_score": false\',\n    )\n',
        '        \'"opaque_collector_or_exhibition_score": false\',\n        \'"content_id": "GLADIATOR_01"\',\n        \'"customer_id": "CASSIA_BELLAN"\',\n        \'"activity_family": "ARENA_SIGNATURE_WEAPON_AND_LEGACY"\',\n        \'"same_item_uid_preserved": true\',\n        \'"opaque_arena_score": false\',\n    )\n',
    ),
    (
        '    assertions[R3_ERSA_CANON] = (\n        R3_CURRENT_DECISION,\n',
        '    assertions[R3_ERSA_CANON] = (\n        R3_FOURTH_DECISION,\n',
    ),
    (
        '    )\n\n    gates_path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"\n',
        '    )\n    assertions[R3_CASSIA_CANON] = (\n        R3_CURRENT_DECISION,\n        "GLADIATOR_01",\n        "CASSIA_BELLAN",\n        "ARENA_SIGNATURE_WEAPON_AND_LEGACY",\n        "ARENA_MATCH_STATE",\n        "EQUIPMENT_CONTRIBUTION_STATE",\n        "ITEM_UID_ARENA_LEGACY_STATE",\n        "SAME_ITEM_UID_PRESERVED",\n        "NO_DIRECT_ARENA_COMBAT",\n        "NO_OPAQUE_ARENA_SCORE",\n        "LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05",\n        "제품 구현: `BLOCKED`",\n        "Task3 구현: `NOT_APPROVED`",\n    )\n\n    gates_path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"\n',
    ),
    (
        '            R3_THIRD_DECISION,\n            R3_CURRENT_DECISION,\n            f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION}",\n',
        '            R3_THIRD_DECISION,\n            R3_FOURTH_DECISION,\n            R3_CURRENT_DECISION,\n            f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION}",\n',
    ),
    (
        '        if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `4/10`" not in tokens:\n            tokens.append("현재 R3–R7 승인 카운터: `4/10`")\n',
        '        if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `5/10`" not in tokens:\n            tokens.append("현재 R3–R7 승인 카운터: `5/10`")\n',
    ),
    (
        '    for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON):\n',
        '    for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON):\n',
    ),
]

for old, new in repls:
    count = runner.count(old)
    if count != 1:
        raise RuntimeError(f"runner replacement count mismatch {count}: {old!r}")
    runner = runner.replace(old, new)
runner_path.write_text(runner, encoding="utf-8")

test = test_path.read_text(encoding="utf-8")
test_repls = [
    ('        ersa = audit.REQUIRED_ASSERTIONS[runner.R3_ERSA_CANON]\n', '        ersa = audit.REQUIRED_ASSERTIONS[runner.R3_ERSA_CANON]\n        cassia = audit.REQUIRED_ASSERTIONS[runner.R3_CASSIA_CANON]\n'),
    ('        self.assertIn(\'"next_approval_counter": "4/10"\', registry)\n', '        self.assertIn(\'"next_approval_counter": "5/10"\', registry)\n'),
    (
        '            \'"id": "BS-CONTENT-20260811-04"\',\n        ):\n',
        '            \'"id": "BS-CONTENT-20260811-04"\',\n            \'"id": "BS-CONTENT-20260811-05"\',\n        ):\n',
    ),
    (
        '        self.assertIn("SAME_ITEM_UID_PRESERVED", ersa)\n        for path in (\n',
        '        self.assertIn("SAME_ITEM_UID_PRESERVED", ersa)\n        self.assertIn("BS-CONTENT-20260811-05", cassia)\n        self.assertIn("ARENA_SIGNATURE_WEAPON_AND_LEGACY", cassia)\n        self.assertIn("EQUIPMENT_CONTRIBUTION_STATE", cassia)\n        self.assertIn("SAME_ITEM_UID_PRESERVED", cassia)\n        for path in (\n',
    ),
    (
        '            runner.R3_ERSA_CANON,\n        ):\n',
        '            runner.R3_ERSA_CANON,\n            runner.R3_CASSIA_CANON,\n        ):\n',
    ),
    ('        self.assertIn("현재 R3–R7 승인 카운터: `4/10`", active)\n', '        self.assertIn("현재 R3–R7 승인 카운터: `5/10`", active)\n'),
]
for old, new in test_repls:
    count = test.count(old)
    if count != 1:
        raise RuntimeError(f"test replacement count mismatch {count}: {old!r}")
    test = test.replace(old, new)
test_path.write_text(test, encoding="utf-8")

for rel in ["tools/_repair_cassia_operating_audit.py", ".github/workflows/_repair-cassia-operating-audit.yml"]:
    p = root / rel
    if p.exists():
        p.unlink()

print("Cassia operating audit current-state repair complete")
