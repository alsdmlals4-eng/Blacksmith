from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/superpowers/specs/2026-08-11-blacksmith-dedicated-local-executor-bootstrap-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-11-blacksmith-dedicated-local-executor-bootstrap.md"
DECISION = ROOT / "docs/decisions/BS-OPS-20260811-03_DEDICATED_LOCAL_EXECUTOR_BOOTSTRAP.md"
SCRIPT = ROOT / "tools/start_blacksmith_local_executor.ps1"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
BASE_DEDICATED_ENV_MAIN = "6d2feba2bc49fda2d8d273248b55087853615d5d"


class BlacksmithDedicatedLocalExecutorBootstrapTests(unittest.TestCase):
    def test_approved_design_and_plan_exist(self) -> None:
        self.assertTrue(SPEC.is_file(), str(SPEC))
        self.assertTrue(PLAN.is_file(), str(PLAN))
        design = SPEC.read_text(encoding="utf-8")
        self.assertIn("BS-OPS-20260811-03", design)
        self.assertIn("USER_EXPLICIT_PLANNING_COMPLETE_DECLARATION", design)
        self.assertIn("R3_R7_9_OF_10", design)
        self.assertIn("PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON", design)
        self.assertIn(BASE_DEDICATED_ENV_MAIN, design)
        for token in (
            "ASSUME_PREVIOUS_POWERSHELL_CLOSED",
            "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST",
            "CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST",
        ):
            self.assertIn(token, design)

    def test_current_authority_records_planning_complete_phase_c_entry(self) -> None:
        self.assertTrue(DECISION.is_file(), str(DECISION))
        decision = DECISION.read_text(encoding="utf-8")
        current = CURRENT.read_text(encoding="utf-8")
        active = ACTIVE.read_text(encoding="utf-8")
        gates = GATES.read_text(encoding="utf-8")
        required = [
            "BS-OPS-20260811-03",
            "PLANNING_COMPLETE: USER_DECLARED",
            "R3_R7_PLANNING_BATCH: CLOSED_AT_9_OF_10",
            "PHASE_B_FINAL_REVIEW: COMPLETE",
            "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON",
            "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED",
            "P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING",
            "IMAGE_GENERATION: DEFERRED_BY_USER",
            "P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED",
            "ASSUME_PREVIOUS_POWERSHELL_CLOSED",
            "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST",
            "CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST",
            BASE_DEDICATED_ENV_MAIN,
        ]
        for token in required:
            self.assertIn(token, decision)
        for text in [current, active, gates]:
            self.assertIn("BS-OPS-20260811-03", text)
            self.assertIn("PLANNING_COMPLETE: USER_DECLARED", text)
            self.assertIn(
                "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON",
                text,
            )
            self.assertIn("TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED", text)
            self.assertIn("PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST", text)
            self.assertIn("ASSUME_PREVIOUS_POWERSHELL_CLOSED", text)

    def test_launcher_uses_exact_isolated_blacksmith_bindings(self) -> None:
        self.assertTrue(SCRIPT.is_file(), str(SCRIPT))
        text = SCRIPT.read_text(encoding="utf-8")
        required = [
            r"C:\Users\user\Documents\GitHub\Ninza\Blacksmith",
            r"C:\Users\user\Tools\Godot-Blacksmith-4.7.1",
            "Godot_v4.7.1-stable_win64.exe",
            '"_sc_"',
            "8006",
            "9506",
            r"C:\Users\user\.codex-blacksmith",
            "CODEX_HOME",
            "http://127.0.0.1:8006/mcp",
            'approval_policy = "never"',
            'sandbox_mode = "workspace-write"',
            "network_access = true",
            "startup_timeout_sec = 60",
            "tool_timeout_sec = 360",
            "godot_ai/http_port",
            "godot_ai/ws_port",
            "godot_ai/keep_server_on_exit",
            "--recovery-mode",
            "--version",
            "4.7.1",
            "project.godot",
            "ASSUME_PREVIOUS_POWERSHELL_CLOSED",
            "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST",
            "CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST",
            "$codexCommand.Source -C $Project",
        ]
        for token in required:
            self.assertIn(token, text)

    def test_launcher_is_fail_closed_and_non_destructive(self) -> None:
        self.assertTrue(SCRIPT.is_file(), str(SCRIPT))
        text = SCRIPT.read_text(encoding="utf-8")
        required = [
            "PORT_CONFLICT_FAIL_CLOSED",
            "EXACT_BLACKSMITH_EDITOR_REUSE",
            "FRESH_HIGODOT_READINESS_REQUIRED_BEFORE_MUTATION",
            "UNMANAGED_CODEX_CONFIG_FAIL_CLOSED",
            "POST_BOOTSTRAP_LIVE_READINESS_NOT_PROVEN",
        ]
        for token in required:
            self.assertIn(token, text)

        forbidden = [
            "taskkill",
            "Stop-Process -Name",
            "git reset",
            "git restore",
            "git clean",
            "git add",
            "%APPDATA%\\Godot",
            "C:\\Users\\user\\.codex\\config.toml",
        ]
        for token in forbidden:
            self.assertNotIn(token, text)

    def test_launcher_writes_managed_codex_toml_as_lf_only_utf8_without_bom(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        start = text.index("function Ensure-DedicatedCodexHome")
        end = text.index("function Wait-ForDedicatedListeners", start)
        writer = text[start:end]

        for token in (
            "$configLines = @(",
            '[string]::Join("`n", $configLines)',
            "System.Text.UTF8Encoding($false)",
            "[System.IO.File]::WriteAllText($configPath, $config, $utf8NoBom)",
            "$ManagedCodexMarker",
            'url = "http://127.0.0.1:8006/mcp"',
            'approval_policy = "never"',
            'sandbox_mode = "workspace-write"',
            "network_access = true",
            "startup_timeout_sec = 60",
            "tool_timeout_sec = 360",
            "UNMANAGED_CODEX_CONFIG_FAIL_CLOSED",
        ):
            self.assertIn(token, writer)
        self.assertNotIn("Set-Content", writer)
        self.assertNotIn('@"', writer)

    def test_launcher_cleans_only_a_verified_retained_blacksmith_server(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        for token in (
            "function Test-VerifiedBlacksmithRetainedServer",
            "function Clear-VerifiedBlacksmithRetainedServer",
            "OLD_BLACKSMITH_RETAINED_SERVER",
            "app_userdata/Blacksmith/godot_ai_server.pid",
            "--port\\s+8006",
            "--ws-port\\s+9506",
            "Stop-Process -Id $verified.PID",
            "Wait-ForPortsReleased",
            "UNVERIFIED_RETAINED_SERVER_REUSE_FORBIDDEN",
            "RETAINED_SERVER_CLEANUP_EDITOR_RACE_FAIL_CLOSED",
            "PORT_CONFLICT_FAIL_CLOSED",
        ):
            self.assertIn(token, text)
        self.assertNotIn("Stop-Process -Name", text)

    def test_retained_server_cleanup_rechecks_editor_absence_before_stop(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        start = text.index("function Clear-VerifiedBlacksmithRetainedServer")
        end = text.index("function Assert-SafePortState", start)
        cleanup = text[start:end]
        self.assertIn("Find-ExactBlacksmithEditors", cleanup)
        self.assertIn("Find-ConflictingBlacksmithEditor", cleanup)
        self.assertLess(cleanup.index("Find-ExactBlacksmithEditors"), cleanup.index("Stop-Process -Id"))
        self.assertLess(cleanup.index("Find-ConflictingBlacksmithEditor"), cleanup.index("Stop-Process -Id"))

    def test_launcher_rejects_duplicate_project_editor_and_unverified_orphan_ports(self) -> None:
        self.assertTrue(SCRIPT.is_file(), str(SCRIPT))
        text = SCRIPT.read_text(encoding="utf-8")
        for token in (
            "NON_DEDICATED_BLACKSMITH_EDITOR_CONFLICT_FAIL_CLOSED",
            "UNVERIFIED_RETAINED_SERVER_REUSE_FORBIDDEN",
            "Find-ConflictingBlacksmithEditor",
        ):
            self.assertIn(token, text)
        self.assertNotIn(
            "Recognizable retained godot-ai listener detected; dedicated editor will be started for fresh adoption/readiness verification.",
            text,
        )

    def test_launcher_does_not_author_product_files(self) -> None:
        self.assertTrue(SCRIPT.is_file(), str(SCRIPT))
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("BOOTSTRAP_ORCHESTRATION_ONLY", text)
        self.assertIn("FRESH_HIGODOT_READINESS_REQUIRED_BEFORE_MUTATION", text)
        for token in [
            "addons/godot_ai/handlers/scene_handler.gd",
            "project.godot =",
            "create_scene",
            "create_node",
            "patch_script",
            "write_file",
        ]:
            self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
