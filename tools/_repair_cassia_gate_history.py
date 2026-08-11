from pathlib import Path

root = Path(__file__).resolve().parents[1]
gates = root / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
text = gates.read_text(encoding="utf-8")

anchor = "현재 Decision: `BS-CONTENT-20260811-05`.\n"
addition = anchor + "\n첫 승인 완료 Decision: `BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`.\n"
if text.count(anchor) != 1:
    raise RuntimeError(f"expected one Decision05 planning-gate anchor, got {text.count(anchor)}")
if "첫 승인 완료 Decision: `BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`." in text:
    raise RuntimeError("Decision01 historical marker already present")
text = text.replace(anchor, addition)

old = "`BS-CONTENT-20260811-01`, `BS-CONTENT-20260811-02`, `BS-CONTENT-20260811-03`, 현재 `BS-CONTENT-20260811-04`는 planning-only Decision이다."
new = "`BS-CONTENT-20260811-01`, `BS-CONTENT-20260811-02`, `BS-CONTENT-20260811-03`, `BS-CONTENT-20260811-04`, 현재 `BS-CONTENT-20260811-05`는 planning-only Decision이다."
if text.count(old) != 1:
    raise RuntimeError(f"expected one stale planning-only current sentence, got {text.count(old)}")
text = text.replace(old, new)

gates.write_text(text, encoding="utf-8")

for rel in ["tools/_repair_cassia_gate_history.py", ".github/workflows/_repair-cassia-gate-history.yml"]:
    path = root / rel
    if path.exists():
        path.unlink()

print("Cassia gate history/current pointer repair complete")
