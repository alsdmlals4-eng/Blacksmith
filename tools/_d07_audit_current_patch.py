from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools/run_project_operating_system_audit.py"
TEST = ROOT / "tests/test_project_operating_system_audit_runner.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 match, got {count}")
    return text.replace(old, new, 1)


def patch_runner() -> None:
    text = RUNNER.read_text(encoding="utf-8")
    text = replace_once(
        text,
        'R3_NOBLE_CANON = "docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md"\n',
        'R3_NOBLE_CANON = "docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md"\nR3_LIANA_CANON = "docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md"\n',
        "runner Liana canon constant",
    )
    text = replace_once(
        text,
        'R3_FIFTH_DECISION = "BS-CONTENT-20260811-05"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-06"\n',
        'R3_FIFTH_DECISION = "BS-CONTENT-20260811-05"\nR3_SIXTH_DECISION = "BS-CONTENT-20260811-06"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-07"\n',
        "runner decision constants",
    )
    text = replace_once(text, "'\"next_approval_counter\": \"6/10\"',", "'\"next_approval_counter\": \"7/10\"',", "runner registry counter")
    text = replace_once(
        text,
        "        f'\"id\": \"{R3_FIFTH_DECISION}\"',\n        f'\"id\": \"{R3_CURRENT_DECISION}\"',\n",
        "        f'\"id\": \"{R3_FIFTH_DECISION}\"',\n        f'\"id\": \"{R3_SIXTH_DECISION}\"',\n        f'\"id\": \"{R3_CURRENT_DECISION}\"',\n",
        "runner registry decision IDs",
    )
    text = replace_once(
        text,
        "        '\"history_erasure_on_repair\": false',\n    )\n",
        "        '\"history_erasure_on_repair\": false',\n        '\"content_id\": \"SOLDIER_02\"',\n        '\"customer_id\": \"LIANA_BERG\"',\n        '\"activity_family\": \"FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY\"',\n        '\"same_item_uid_preserved\": true',\n        '\"direct_tactical_combat\": false',\n        '\"item_as_sole_cause_of_mission_result\": false',\n        '\"baseline_permadeath_for_liana\": false',\n    )\n",
        "runner registry Liana assertions",
    )
    text = replace_once(
        text,
        "    assertions[R3_NOBLE_CANON] = (\n        R3_CURRENT_DECISION,\n",
        "    assertions[R3_NOBLE_CANON] = (\n        R3_SIXTH_DECISION,\n",
        "runner Noble historical decision",
    )
    noble_block = '''    assertions[R3_NOBLE_CANON] = (
        R3_SIXTH_DECISION,
        "NOBLE_01",
        "CEREMONIAL_NOBLE",
        "HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY",
        "CEREMONY_READINESS_STATE",
        "HEIRLOOM_TREATMENT_FIT_STATE",
        "ITEM_UID_DYNASTIC_LEGACY_STATE",
        "SAME_ITEM_UID_PRESERVED",
        "NO_FULL_RESTORATION_ALWAYS_BEST",
        "NO_HISTORY_ERASURE_ON_REPAIR",
        "NO_NOBLE_HOUSE_MANAGEMENT",
        "제품 구현: `BLOCKED`",
        "Task3 구현: `NOT_APPROVED`",
    )
'''
    liana_block = noble_block + '''
    assertions[R3_LIANA_CANON] = (
        R3_CURRENT_DECISION,
        "SOLDIER_02",
        "LIANA_BERG",
        "FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY",
        "MISSION_DUTY_STATE",
        "COMMANDER_RETURN_STATE",
        "ITEM_UID_FIELD_LEGACY_STATE",
        "SAME_ITEM_UID_PRESERVED",
        "NO_DIRECT_TACTICAL_COMBAT",
        "NO_ITEM_AS_SOLE_CAUSE_OF_MISSION_RESULT",
        "NO_BASELINE_PERMADEATH_FOR_LIANA",
        "제품 구현: `BLOCKED`",
        "Task3 구현: `NOT_APPROVED`",
    )
'''
    text = replace_once(text, noble_block, liana_block, "runner Liana canon assertions")
    text = replace_once(text, '            "R3_R7_APPROVAL_COUNTER: 6/10",', '            "R3_R7_APPROVAL_COUNTER: 7/10",', "runner gate counter")
    text = replace_once(
        text,
        "            R3_FIFTH_DECISION,\n            R3_CURRENT_DECISION,\n",
        "            R3_FIFTH_DECISION,\n            R3_SIXTH_DECISION,\n            R3_CURRENT_DECISION,\n",
        "runner router decision history",
    )
    text = replace_once(
        text,
        '            "NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED",',
        '            "SOLDIER_02_LIANA_MISSION_FIT_APPROVED",',
        "runner current resume locator",
    )
    text = replace_once(
        text,
        '        if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `6/10`" not in tokens:\n            tokens.append("현재 R3–R7 승인 카운터: `6/10`")',
        '        if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `7/10`" not in tokens:\n            tokens.append("현재 R3–R7 승인 카운터: `7/10`")',
        "runner active current counter",
    )
    text = replace_once(
        text,
        "    for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON, R3_NOBLE_CANON):",
        "    for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON, R3_NOBLE_CANON, R3_LIANA_CANON):",
        "runner active docs",
    )
    RUNNER.write_text(text, encoding="utf-8", newline="\n")


def patch_test() -> None:
    text = TEST.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "        noble = audit.REQUIRED_ASSERTIONS[runner.R3_NOBLE_CANON]\n",
        "        noble = audit.REQUIRED_ASSERTIONS[runner.R3_NOBLE_CANON]\n        liana = audit.REQUIRED_ASSERTIONS[runner.R3_LIANA_CANON]\n",
        "meta Liana assertion variable",
    )
    text = replace_once(text, "        self.assertIn('\"next_approval_counter\": \"6/10\"', registry)", "        self.assertIn('\"next_approval_counter\": \"7/10\"', registry)", "meta registry counter")
    text = replace_once(
        text,
        "            '\"id\": \"BS-CONTENT-20260811-06\"',\n",
        "            '\"id\": \"BS-CONTENT-20260811-06\"',\n            '\"id\": \"BS-CONTENT-20260811-07\"',\n",
        "meta D07 registry ID",
    )
    text = replace_once(
        text,
        "        self.assertIn(\"NO_HISTORY_ERASURE_ON_REPAIR\", noble)\n",
        "        self.assertIn(\"NO_HISTORY_ERASURE_ON_REPAIR\", noble)\n        self.assertIn(\"BS-CONTENT-20260811-07\", liana)\n        self.assertIn(\"SOLDIER_02\", liana)\n        self.assertIn(\"LIANA_BERG\", liana)\n        self.assertIn(\"FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY\", liana)\n        self.assertIn(\"MISSION_DUTY_STATE\", liana)\n        self.assertIn(\"COMMANDER_RETURN_STATE\", liana)\n        self.assertIn(\"ITEM_UID_FIELD_LEGACY_STATE\", liana)\n        self.assertIn(\"SAME_ITEM_UID_PRESERVED\", liana)\n        self.assertIn(\"NO_DIRECT_TACTICAL_COMBAT\", liana)\n        self.assertIn(\"NO_ITEM_AS_SOLE_CAUSE_OF_MISSION_RESULT\", liana)\n        self.assertIn(\"NO_BASELINE_PERMADEATH_FOR_LIANA\", liana)\n",
        "meta Liana details",
    )
    text = replace_once(
        text,
        "            runner.R3_NOBLE_CANON,\n",
        "            runner.R3_NOBLE_CANON,\n            runner.R3_LIANA_CANON,\n",
        "meta active docs Liana",
    )
    text = replace_once(text, '        self.assertIn("R3_R7_APPROVAL_COUNTER: 6/10", tokens)', '        self.assertIn("R3_R7_APPROVAL_COUNTER: 7/10", tokens)', "meta gate counter")
    text = replace_once(text, '        self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-06", tokens)', '        self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07", tokens)', "meta gate current decision")
    text = replace_once(
        text,
        "                \"BS-CONTENT-20260811-06\",\n",
        "                \"BS-CONTENT-20260811-06\",\n                \"BS-CONTENT-20260811-07\",\n",
        "meta router D07 history",
    )
    text = replace_once(text, '            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-06", tokens)', '            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07", tokens)', "meta router current decision")
    text = replace_once(text, '            self.assertIn("NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED", tokens)', '            self.assertIn("SOLDIER_02_LIANA_MISSION_FIT_APPROVED", tokens)', "meta router locator")
    text = replace_once(text, '        self.assertIn("현재 R3–R7 승인 카운터: `6/10`", active)', '        self.assertIn("현재 R3–R7 승인 카운터: `7/10`", active)', "meta active counter")
    TEST.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    patch_runner()
    patch_test()
