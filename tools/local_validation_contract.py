from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

PYTHON_MAJOR_MINOR = (3, 12)
BASE_OPERATING_PIN = "41a20584dd2ee51d917e5c9d7cab6838e1ceba7e"
BASE_CONTRACT_PIN = "bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1"
BLOCKING_GODOT_MARKERS = ("SCRIPT ERROR:", "Parse Error:", "Compile Error:", "ERROR:")
FORBIDDEN_BASE_V9_PATHS = ("src/", "scenes/", "data/", "assets/", "addons/")
EXPECTED_GODOT_MARKERS = {
    "godot-test_forging_session": "ForgingSession tests PASSED",
    "godot-test_enhancement_session": "EnhancementSession tests PASSED",
    "godot-test_workshop_resources": "WorkshopResources tests PASSED",
    "godot-test_workshop_calendar": "WorkshopCalendar tests PASSED",
    "godot-test_craftsmanship_grade_resolver": "CraftsmanshipGradeResolver tests PASSED",
    "godot-test_customer_contract": "CustomerContract tests PASSED",
    "godot-test_world_activity_resolver": "WorldActivityResolver tests PASSED",
    "godot-test_equipment_world_registry": "EquipmentWorldRegistry tests PASSED",
    "godot-test_poc_telemetry": "PocTelemetry tests PASSED",
    "godot-test_manual_enhancement_economy": "Manual enhancement economy integration tests PASSED",
    "godot-test_forging_quality_enhancement": "Forging quality enhancement integration tests PASSED",
    "godot-test_workshop_action_atomicity": "Workshop action atomicity integration tests PASSED",
    "godot-test_equipment_lifecycle_controller": "Equipment lifecycle controller integration tests PASSED",
    "godot-test_equipment_lifecycle_poc": "Equipment lifecycle PoC integration tests PASSED",
}

@dataclass
class CommandResult:
    name: str
    command: list[str]
    exit_code: int
    started_at: str
    completed_at: str
    log_path: str

    @property
    def passed(self) -> bool:
        return self.exit_code == 0

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def is_authoring_surface(path: str) -> bool:
    return path == "project.godot" or path.endswith((".tscn", ".tres", ".res")) or path.startswith("addons/godot_ai/")

def base_v9_changed_paths_allowed(paths: Iterable[str]) -> bool:
    return all(path != "project.godot" and not path.startswith(FORBIDDEN_BASE_V9_PATHS) for path in paths)

def workflow_has_exact_ref(workflow: Path, commit: str) -> bool:
    if not workflow.is_file():
        return False
    return re.search(rf"(?m)^\s*ref:\s*{re.escape(commit)}\s*$", workflow.read_text(encoding="utf-8")) is not None

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def git_output(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True, encoding="utf-8").strip()

def git_succeeds(repo: Path, *args: str) -> bool:
    return subprocess.run(["git", *args], cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def tracked_authoring_hashes(repo: Path) -> dict[str, str]:
    tracked = git_output(repo, "ls-files", "-z").split("\0")
    return {path: sha256_file(repo / path) for path in sorted(tracked) if path and is_authoring_surface(path) and (repo / path).is_file()}

def run_command(name: str, command: Sequence[str], cwd: Path, log_dir: Path) -> CommandResult:
    log_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in name)
    log_path = log_dir / f"{safe_name}.log"
    started = utc_now()
    with log_path.open("w", encoding="utf-8", errors="replace") as log:
        process = subprocess.run(list(command), cwd=cwd, stdout=log, stderr=subprocess.STDOUT, text=True, check=False)
    return CommandResult(name, list(command), process.returncode, started, utc_now(), str(log_path.resolve()))

def validate_logged_result(result: CommandResult) -> CommandResult:
    log_text = Path(result.log_path).read_text(encoding="utf-8", errors="replace")
    if result.name == "godot-version" and not re.search(r"(?m)^4\.7\.1(?:\.|$)", log_text):
        result.exit_code = 20
        return result
    if result.name.startswith(("godot-", "scene-", "gut-cli")) and result.name != "gut-junit":
        if any(marker in log_text for marker in BLOCKING_GODOT_MARKERS):
            result.exit_code = 21
            return result
    expected = EXPECTED_GODOT_MARKERS.get(result.name)
    if expected and expected not in log_text:
        result.exit_code = 22
    return result

def summarize_status(results: Iterable[CommandResult], exact_head: bool, clean_before: bool, clean_after: bool, authoring_unchanged: bool, bases_ready: bool, godot_present: bool, require_godot: bool, contract_consistent: bool = True) -> str:
    if not contract_consistent or not exact_head or not clean_before or not clean_after:
        return "FAIL"
    if not authoring_unchanged or any(not result.passed for result in results):
        return "FAIL"
    if not bases_ready or (require_godot and not godot_present):
        return "PARTIAL"
    return "PASS"
