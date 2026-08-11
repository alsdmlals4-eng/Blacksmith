from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/run_project_operating_system_audit.py"
TEST = ROOT / "tests/test_project_operating_system_audit_runner.py"


def rep(text: str, old: str, new: str, label: str, count: int = 1) -> str:
    if old not in text:
        raise RuntimeError(f"missing {label}: {old!r}")
    return text.replace(old, new, count)


def repair_tool() -> None:
    text = TOOL.read_text(encoding="utf-8")
    text = rep(
        text,
        'R3_LIANA_CANON = "docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md"\n',
        'R3_LIANA_CANON = "docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md"\n'
        'R3_SEDRIC_CANON = "docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md"\n',
        "Sedric canon constant",
    )
    text = rep(
        text,
        'R3_SIXTH_DECISION = "BS-CONTENT-20260811-06"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-07"\n',
        'R3_SIXTH_DECISION = "BS-CONTENT-20260811-06"\n'
        'R3_SEVENTH_DECISION = "BS-CONTENT-20260811-07"\n'
        'R3_CURRENT_DECISION = "BS-CONTENT-20260811-08"\n',
        "historical/current decision constants",
    )
    text = rep(text, '"next_approval_counter": "7/10"', '"next_approval_counter": "8/10"', "registry counter")
    text = rep(
        text,
        '        f\'"id": "{R3_SIXTH_DECISION}"\',\n        f\'"id": "{R3_CURRENT_DECISION}"\',\n',
        '        f\'"id": "{R3_SIXTH_DECISION}"\',\n'
        '        f\'"id": "{R3_SEVENTH_DECISION}"\',\n'
        '        f\'"id": "{R3_CURRENT_DECISION}"\',\n',
        "registry decision sequence",
    )
    text = rep(
        text,
        '    assertions[R3_LIANA_CANON] = (\n        R3_CURRENT_DECISION,\n',
        '    assertions[R3_LIANA_CANON] = (\n        R3_SEVENTH_DECISION,\n',
        "Liana historical owner",
    )
    sedric_assertions = '''    assertions[R3_SEDRIC_CANON] = (\n        R3_CURRENT_DECISION,\n        "COLLECTOR_02",\n        "SEDRIC_VAEL",\n        "ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY",\n        "ARCHIVE_ACCESSION_STATE",\n        "PROVENANCE_DOCUMENTATION_STATE",\n        "ITEM_UID_CUSTODY_LEGACY_STATE",\n        "SAME_ITEM_UID_PRESERVED",\n        "ERSA_EXHIBITION_RESPONSIBILITY_PRESERVED",\n        "NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED",\n        "NO_AUTHENTICITY_TOTAL_SCORE",\n        "NO_DOCUMENT_FABRICATION",\n        "NO_UNRECORDED_HISTORY_AUTOFILL",\n        "NO_MUSEUM_MANAGEMENT_SIM",\n        "P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED",\n        "제품 구현: `BLOCKED`",\n        "Task3 구현: `NOT_APPROVED`",\n    )\n\n'''
    text = rep(text, '    gates_path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"\n', sedric_assertions + '    gates_path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"\n', "Sedric audit assertions")
    text = rep(
        text,
        '            R3_SIXTH_DECISION,\n            R3_CURRENT_DECISION,\n',
        '            R3_SIXTH_DECISION,\n            R3_SEVENTH_DECISION,\n            R3_CURRENT_DECISION,\n',
        "router decision sequence",
    )
    text = rep(
        text,
        '        if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `7/10`" not in tokens:\n            tokens.append("현재 R3–R7 승인 카운터: `7/10`")\n',
        '        if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `8/10`" not in tokens:\n            tokens.append("현재 R3–R7 승인 카운터: `8/10`")\n',
        "Active current counter",
    )
    text = rep(
        text,
        '    for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON, R3_NOBLE_CANON, R3_LIANA_CANON):\n',
        '    for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON, R3_NOBLE_CANON, R3_LIANA_CANON, R3_SEDRIC_CANON):\n',
        "active docs",
    )
    TOOL.write_text(text, encoding="utf-8")


def repair_test() -> None:
    text = TEST.read_text(encoding="utf-8")
    text = rep(
        text,
        '        liana = audit.REQUIRED_ASSERTIONS[runner.R3_LIANA_CANON]\n',
        '        liana = audit.REQUIRED_ASSERTIONS[runner.R3_LIANA_CANON]\n'
        '        sedric = audit.REQUIRED_ASSERTIONS[runner.R3_SEDRIC_CANON]\n',
        "Sedric test fixture",
    )
    text = rep(text, '        self.assertIn(\'"next_approval_counter": "7/10"\', registry)\n', '        self.assertIn(\'"next_approval_counter": "8/10"\', registry)\n', "test registry counter")
    text = rep(
        text,
        '            \'"id": "BS-CONTENT-20260811-07"\',\n        ):\n',
        '            \'"id": "BS-CONTENT-20260811-07"\',\n'
        '            \'"id": "BS-CONTENT-20260811-08"\',\n'
        '        ):\n',
        "test registry decision sequence",
    )
    sedric_checks = '''        self.assertIn("BS-CONTENT-20260811-08", sedric)\n        self.assertIn("COLLECTOR_02", sedric)\n        self.assertIn("SEDRIC_VAEL", sedric)\n        self.assertIn("ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY", sedric)\n        self.assertIn("ARCHIVE_ACCESSION_STATE", sedric)\n        self.assertIn("PROVENANCE_DOCUMENTATION_STATE", sedric)\n        self.assertIn("ITEM_UID_CUSTODY_LEGACY_STATE", sedric)\n        self.assertIn("SAME_ITEM_UID_PRESERVED", sedric)\n        self.assertIn("NO_AUTHENTICITY_TOTAL_SCORE", sedric)\n        self.assertIn("NO_DOCUMENT_FABRICATION", sedric)\n'''
    text = rep(
        text,
        '        self.assertIn("NO_BASELINE_PERMADEATH_FOR_LIANA", liana)\n        for path in (\n',
        '        self.assertIn("NO_BASELINE_PERMADEATH_FOR_LIANA", liana)\n' + sedric_checks + '        for path in (\n',
        "Sedric test assertions",
    )
    text = rep(
        text,
        '            runner.R3_LIANA_CANON,\n        ):\n',
        '            runner.R3_LIANA_CANON,\n            runner.R3_SEDRIC_CANON,\n        ):\n',
        "Sedric active doc expectation",
    )
    text = rep(
        text,
        '        self.assertIn("현재 R3–R7 승인 카운터: `7/10`", active)\n',
        '        self.assertIn("현재 R3–R7 승인 카운터: `8/10`", active)\n',
        "test Active current counter",
    )
    TEST.write_text(text, encoding="utf-8")


repair_tool()
repair_test()
print("Decision08 operating audit historical/current separation repaired")
