from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

core = ROOT / "tests/check_project_core_alignment_current.py"
text = core.read_text(encoding="utf-8")
old = '            "현재 R3–R7 승인 카운터: `7/10`",\n'
new = '            "현재 R3–R7 승인 카운터: `8/10`",\n'
if old not in text:
    raise RuntimeError("core-alignment old current counter token missing")
core.write_text(text.replace(old, new, 1), encoding="utf-8")

gates = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
text = gates.read_text(encoding="utf-8")
anchor = "- `BS-CONTENT-20260811-07 / SOLDIER_02 / LIANA_BERG`는 7/10 승인 이력이며 current locator가 아니다.\n"
line = "- `BS-CONTENT-20260811-06 / NOBLE_01 / CEREMONIAL_NOBLE`은 6/10 승인 이력이며 current locator가 아니다.\n"
if anchor not in text:
    raise RuntimeError("Decision07 historical gate anchor missing")
if line not in text:
    text = text.replace(anchor, line + anchor, 1)
gates.write_text(text, encoding="utf-8")

print("Decision08 preverify moving-current patch complete")
