from pathlib import Path

root = Path(__file__).resolve().parents[2]
path = root / "tools/audit_project_operating_system.py"
text = path.read_text(encoding="utf-8")
replacements = (
    ('\'"next_approval_counter":"1/10"\'', '\'"next_approval_counter":"2/10"\''),
    ('"docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md": (\n        "BS-CRAFT-20260805-02",\n        "R2_BATCH_005_2_OF_10",', '"docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md": (\n        "BS-CRAFT-20260805-02",\n        "R2_BATCH_005_1_OF_10",'),
    ('"[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (\n        "R2 체크포인트 004",\n        "R2_BATCH_005_2_OF_10",\n        "현재 승인 카운터: `1/10`",', '"[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (\n        "R2 체크포인트 004",\n        "R2_BATCH_005_2_OF_10",\n        "현재 승인 카운터: `2/10`",'),
    ('"[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (\n        "R2_BATCH_004_2_OF_10",\n        "현재 승인 카운터: `0/10`",\n        "현재 승인 카운터: `2/10`",\n    ),', '"[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (\n        "R2_BATCH_004_2_OF_10",\n        "현재 승인 카운터: `0/10`",\n    ),'),
)
for old, new in replacements:
    if old not in text:
        raise SystemExit(f"required audit token block missing: {old[:90]}")
    text = text.replace(old, new, 1)

active_marker = '    "docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md",\n'
customer_active = '    "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md",\n'
if customer_active not in text:
    text = text.replace(active_marker, active_marker + customer_active, 1)

required_marker = '''    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": (\n'''
customer_required = '''    "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md": (\n        "BS-CUSTOMER-20260805-01",\n        "R2_BATCH_005_2_OF_10",\n        "근력 / 기량 / 체력 / 판단력",\n        "WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL",\n        "부적합 / 불안정 / 안정 / 능숙",\n        "제품 구현: `BLOCKED`",\n    ),\n'''
if "BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md\": (" not in text:
    if required_marker not in text:
        raise SystemExit("required insertion marker missing")
    text = text.replace(required_marker, customer_required + required_marker, 1)

path.write_text(text, encoding="utf-8")

for one_shot in (
    root / ".github/scripts/fix_operating_audit_batch_tokens.py",
    root / ".github/workflows/fix-operating-audit-batch-tokens.yml",
):
    if one_shot.exists():
        one_shot.unlink()
