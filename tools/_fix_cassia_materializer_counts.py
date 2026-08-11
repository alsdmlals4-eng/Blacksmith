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
p.write_text(text, encoding="utf-8")
Path(__file__).unlink()
print("materializer count guards corrected")
