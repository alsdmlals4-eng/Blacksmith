from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: str, replacements: list[tuple[str, str]]) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"missing anchor in {path}: {old[:120]!r}")
        text = text.replace(old, new, 1)
    target.write_text(text, encoding="utf-8", newline="\n")


patch(
    "tools/run_project_operating_system_audit.py",
    [
        (
            "    R2/Task2 merge evidence remains historical/current-compatible authority. R3–R7 is\n    a planning-only layer: it is current for design routing but does not open product\n    or Task3 implementation. Earlier R3 decisions stay auditable as history while the\n    current router advances with later user-approved planning decisions.\n",
            "    R2/Task2 merge evidence remains historical/current-compatible authority. The R3–R7\n    registry/canons remain the approved planning record, while BS-OPS-20260811-03 now owns\n    the current bounded Phase C entry. Earlier planning blockers remain auditable as history;\n    current routers must require P0 bootstrap and keep new scope / Task3 separately gated.\n",
        ),
        (
            '        "GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED"\n        if token == "CODEX_IMPLEMENTATION_GATE: BLOCKED"\n',
            '        "GENERAL_PRODUCT_IMPLEMENTATION: APPROVED_WITHIN_EXISTING_CANON_NEW_SCOPE_REQUIRES_DECISION"\n        if token == "CODEX_IMPLEMENTATION_GATE: BLOCKED"\n',
        ),
        (
            '        "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED",\n        "R3_R7_DESIGN_ACTIVE",\n        "R3_R7_APPROVAL_COUNTER: 9/10",\n        f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION}",\n        R3_THIRD_DECISION,\n        "TASK3_IMPLEMENTATION: NOT_APPROVED",\n',
            '        "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED",\n        "R3_R7_DESIGN_ACTIVE",\n        "R3_R7_APPROVAL_COUNTER: 9/10",\n        f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION}",\n        R3_THIRD_DECISION,\n        "BS-OPS-20260811-03",\n        "PLANNING_COMPLETE: USER_DECLARED",\n        "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON",\n        "P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING",\n        "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED",\n        "HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED",\n        "HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED",\n',
        ),
        (
            '            "PRODUCT_IMPLEMENTATION: BLOCKED",\n            "R3_R7_DESIGN_ACTIVE",\n',
            '            "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON",\n            "P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING",\n            "BS-OPS-20260811-03",\n            "PLANNING_COMPLETE: USER_DECLARED",\n            "HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED",\n            "R3_R7_DESIGN_ACTIVE",\n',
        ),
        (
            '            "GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED",\n            "TASK3_IMPLEMENTATION: NOT_APPROVED",\n',
            '            "GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED",\n            "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED",\n            "HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED",\n',
        ),
    ],
)

patch(
    "tests/test_project_operating_system_audit_runner.py",
    [
        (
            "    def test_r3_planning_authority_is_audited_without_opening_product_scope(self) -> None:\n",
            "    def test_r3_planning_authority_remains_historical_while_phase_c_router_is_separate(self) -> None:\n",
        ),
        (
            '    def test_gate_assertions_keep_general_block_and_task2_closed_scope(self) -> None:\n        runner.configure_current_assertions()\n        tokens = audit.REQUIRED_ASSERTIONS["[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"]\n        self.assertIn("GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED", tokens)\n        self.assertIn("VERTICAL_SLICE_CODE_GATE: TASK2_MAIN_MERGED_NO_NEW_PRODUCT_SCOPE", tokens)\n        self.assertIn("NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED", tokens)\n        self.assertIn("R3_R7_DESIGN_ACTIVE", tokens)\n        self.assertIn("R3_R7_APPROVAL_COUNTER: 9/10", tokens)\n        self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09", tokens)\n        self.assertIn("BS-CONTENT-20260811-03", tokens)\n        self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", tokens)\n        self.assertNotIn("VERTICAL_SLICE_CODE_GATE: USER_APPROVED", tokens)\n        self.assertNotIn("CODEX_IMPLEMENTATION_GATE: BLOCKED", tokens)\n',
            '    def test_gate_assertions_keep_task2_history_and_open_only_bounded_phase_c_scope(self) -> None:\n        runner.configure_current_assertions()\n        tokens = audit.REQUIRED_ASSERTIONS["[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"]\n        self.assertIn("GENERAL_PRODUCT_IMPLEMENTATION: APPROVED_WITHIN_EXISTING_CANON_NEW_SCOPE_REQUIRES_DECISION", tokens)\n        self.assertIn("PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON", tokens)\n        self.assertIn("VERTICAL_SLICE_CODE_GATE: TASK2_MAIN_MERGED_NO_NEW_PRODUCT_SCOPE", tokens)\n        self.assertIn("NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED", tokens)\n        self.assertIn("R3_R7_DESIGN_ACTIVE", tokens)\n        self.assertIn("R3_R7_APPROVAL_COUNTER: 9/10", tokens)\n        self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09", tokens)\n        self.assertIn("BS-CONTENT-20260811-03", tokens)\n        self.assertIn("BS-OPS-20260811-03", tokens)\n        self.assertIn("PLANNING_COMPLETE: USER_DECLARED", tokens)\n        self.assertIn("P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING", tokens)\n        self.assertIn("TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED", tokens)\n        self.assertIn("HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED", tokens)\n        self.assertIn("HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED", tokens)\n        self.assertNotIn("VERTICAL_SLICE_CODE_GATE: USER_APPROVED", tokens)\n        self.assertNotIn("CODEX_IMPLEMENTATION_GATE: BLOCKED", tokens)\n',
        ),
        (
            '            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", tokens)\n            self.assertIn("R3_R7_DESIGN_ACTIVE", tokens)\n',
            '            self.assertIn("PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON", tokens)\n            self.assertIn("P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING", tokens)\n            self.assertIn("BS-OPS-20260811-03", tokens)\n            self.assertIn("PLANNING_COMPLETE: USER_DECLARED", tokens)\n            self.assertIn("HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED", tokens)\n            self.assertIn("R3_R7_DESIGN_ACTIVE", tokens)\n',
        ),
        (
            '            self.assertIn("GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED", tokens)\n            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", tokens)\n',
            '            self.assertIn("GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED", tokens)\n            self.assertIn("TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED", tokens)\n            self.assertIn("HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED", tokens)\n',
        ),
    ],
)

print("Phase C audit moving-current assertions repaired")
