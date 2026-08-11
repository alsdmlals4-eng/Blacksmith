from pathlib import Path

root = Path(__file__).resolve().parents[1]
p = root / "tools/_materialize_cassia_5of10.py"
text = p.read_text(encoding="utf-8")
replacements = {
    'active = replace_exact(active, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10")': 'active = replace_exact(active, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10", expected=2)',
    'active = replace_exact(active, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05")': 'active = replace_exact(active, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05", expected=2)',
    'active = replace_exact(active, "R3_R7_RESUME_LOCATOR: COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED", "R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED")': 'active = replace_exact(active, "R3_R7_RESUME_LOCATOR: COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED", "R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED", expected=2)',
    'gates = replace_exact(gates, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10")': 'gates = replace_exact(gates, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10", expected=2)',
    'gates = replace_exact(gates, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05")': 'gates = replace_exact(gates, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05", expected=3)',
}
for old, new in replacements.items():
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one materializer line for {old!r}, got {count}")
    text = text.replace(old, new)

needle = '''    if rel == "tests/test_r3_collector_01_ersa_content.py":
        text = text.replace('self.assertEqual("4/10", registry.get("next_approval_counter"))', 'self.assertEqual("5/10", registry.get("next_approval_counter"))')
        text = text.replace("test_current_routers_move_to_four_of_ten_without_opening_product_code", "test_current_routers_preserve_ersa_history_while_cassia_is_current")
'''
replacement = needle + '''    if rel == "tests/test_r3_soldier_01_marek_content.py":
        text = text.replace('self.assertEqual("4/10", registry.get("next_approval_counter"))', 'self.assertEqual("5/10", registry.get("next_approval_counter"))')
        text = text.replace("test_current_routers_preserve_marek_history_while_ersa_is_current", "test_current_routers_preserve_marek_history_while_cassia_is_current")
    if rel == "tests/check_project_core_alignment_current.py":
        text = text.replace("현재 R3–R7 승인 카운터: `4/10`", "현재 R3–R7 승인 카운터: `5/10`")
        text = text.replace('            "BS-CONTENT-20260811-04",\n', '            "BS-CONTENT-20260811-04",\n            "BS-CONTENT-20260811-05",\n')
'''
count = text.count(needle)
if count != 1:
    raise RuntimeError(f"expected one collector current-consumer block, got {count}")
text = text.replace(needle, replacement)

p.write_text(text, encoding="utf-8")
Path(__file__).unlink()
print("materializer current consumer updates corrected")
