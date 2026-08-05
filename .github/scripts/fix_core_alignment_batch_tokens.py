from pathlib import Path

root = Path(__file__).resolve().parents[2]
path = root / "tests/check_project_core_alignment.py"
text = path.read_text(encoding="utf-8")
old_required = '''    "docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md": (\n        "BS-CRAFT-20260805-02",\n        "R2_BATCH_005_2_OF_10",'''
new_required = '''    "docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md": (\n        "BS-CRAFT-20260805-02",\n        "R2_BATCH_005_1_OF_10",'''
if old_required not in text:
    raise SystemExit("artistry batch-token expectation not found")
text = text.replace(old_required, new_required, 1)
old_forbidden = '''    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (\n        "현재 승인 카운터: `0/10`",\n        "현재 승인 카운터: `2/10`",\n    ),'''
new_forbidden = '''    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (\n        "현재 승인 카운터: `0/10`",\n    ),'''
if old_forbidden not in text:
    raise SystemExit("contradictory active-counter forbidden block not found")
text = text.replace(old_forbidden, new_forbidden, 1)
path.write_text(text, encoding="utf-8")

for one_shot in (
    root / ".github/scripts/fix_core_alignment_batch_tokens.py",
    root / ".github/workflows/fix-core-alignment-batch-tokens.yml",
):
    if one_shot.exists():
        one_shot.unlink()
