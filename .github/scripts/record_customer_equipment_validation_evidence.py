from __future__ import annotations

import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
registry_path = root / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
tdd = registry.setdefault("tdd_evidence", {})
tdd["customer_equipment_validator_red"] = {
    "commit": "4cb8f6dc09e3d21613a77066e11ca56bba9ae211",
    "pr_validation_run": 1225,
    "status": "EXPECTED_FAILURE",
    "cause": "GLOBAL_BATCH_TOKEN_REPLACEMENT_CREATED_CONTRADICTORY_VALIDATOR_EXPECTATIONS",
}
tdd["customer_equipment_operating_audit_red"] = {
    "commit": "1d2dbe1cd88be0de6c016741547595a95ca47716",
    "pr_validation_run": 1229,
    "status": "EXPECTED_FAILURE",
    "cause": "OPERATING_AUDIT_RETAINED_STALE_ONE_OF_TEN_AND_FORBIDDEN_TWO_OF_TEN_ASSERTIONS",
}
tdd["customer_equipment_green"] = {
    "commit": "cdfd74d49525227cee3d15d8a38da07219e6ac32",
    "planning_first_run": 155,
    "base_run": 642,
    "pr_validation_run": 1233,
    "python_full_contracts": "PASS",
    "godot_4_7_1_headless": "PASS",
    "status": "OBSERVED_GREEN",
}
registry_path.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

plan_path = root / "docs/superpowers/plans/2026-08-05-customer-equipment-compatibility.md"
plan = plan_path.read_text(encoding="utf-8")
block = '''
## Observed GREEN evidence

- exact head: `cdfd74d49525227cee3d15d8a38da07219e6ac32`
- Planning-first `155`: PASS
- Base `642`: PASS
- PR validation `1233`: PASS
- Python full contracts: PASS
- Godot `4.7.1` headless: PASS
- evidence-recording commit requires one final exact-head verification before Sheet/PR readback is declared complete.
'''
if "## Observed GREEN evidence" not in plan:
    plan = plan.rstrip() + "\n\n" + block.strip() + "\n"
plan_path.write_text(plan, encoding="utf-8")

for one_shot in (
    root / ".github/scripts/record_customer_equipment_validation_evidence.py",
    root / ".github/workflows/record-customer-equipment-validation-evidence.yml",
):
    if one_shot.exists():
        one_shot.unlink()
