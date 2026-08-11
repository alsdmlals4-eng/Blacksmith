from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_288 = "6d2feba2bc49fda2d8d273248b55087853615d5d"
OLD_BASE = "23d5b292f619022cdd8ab7a33fb1debc2d294861"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise RuntimeError(f"missing anchor in {path}: {old[:160]!r}")
    write(path, text.replace(old, new, 1))


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


# Launcher: make fresh-shell/dedicated-env invariants executable documentation and
# pin Codex to the exact project/worktree with -C.
script = "tools/start_blacksmith_local_executor.ps1"
replace_once(
    script,
    "# BLACKSMITH_DEDICATED_LOCAL_EXECUTOR\n# BOOTSTRAP_ORCHESTRATION_ONLY",
    "# BLACKSMITH_DEDICATED_LOCAL_EXECUTOR\n# ASSUME_PREVIOUS_POWERSHELL_CLOSED\n# PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST\n# CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST\n# BOOTSTRAP_ORCHESTRATION_ONLY",
)
replace_once(
    script,
    "Write-Step 'Starting bounded Blacksmith local executor bootstrap.'",
    "Write-Host 'ASSUME_PREVIOUS_POWERSHELL_CLOSED'\nWrite-Host 'PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST'\nWrite-Host 'CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST'\nWrite-Step 'Starting bounded Blacksmith local executor bootstrap.'",
)
replace_once(
    script,
    "Set-Location -LiteralPath $Project\n& $codexCommand.Source\n",
    "Set-Location -LiteralPath $Project\n& $codexCommand.Source -C $Project\n",
)

# Reconcile spec/plan/decision to the newest Base main that directly owns this goal.
append_once(
    "docs/superpowers/specs/2026-08-11-blacksmith-dedicated-local-executor-bootstrap-design.md",
    "## Base #288 reconciliation",
    f"""## Base #288 reconciliation

Post-design fresh Base read advanced to `{BASE_288}` (`docs: require project-dedicated local execution environment (#288)`). This is a same-goal upstream authority change and is therefore consumed before Blacksmith merge.

Blacksmith explicitly inherits:

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
```

The one-shot launcher is always presented/executed from a fresh-shell assumption, creates or repairs missing Blacksmith-local components before product work, and launches the executor with exact project targeting:

```powershell
codex -C 'C:\\Users\\user\\Documents\\GitHub\\Ninza\\Blacksmith'
```

The dedicated PowerShell boundary means a fresh PowerShell process with Blacksmith-specific environment injection, not a separately installed PowerShell binary. HiGodot remains the sole persistent Godot authoring authority. Hera, when a later acceptance step actually requires the adopted profile, remains `LIVE_QA_AND_OBSERVABILITY_ONLY` and non-authoring.
""",
)
append_once(
    "docs/superpowers/plans/2026-08-11-blacksmith-dedicated-local-executor-bootstrap.md",
    "## Base #288 reconciliation task",
    f"""## Base #288 reconciliation task

Fresh Base main `{BASE_288}` directly strengthens this goal. Before exact-head acceptance:

- [x] require `ASSUME_PREVIOUS_POWERSHELL_CLOSED`;
- [x] require `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`;
- [x] require `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`;
- [x] invoke Codex with `-C` and the exact Blacksmith project path;
- [x] preserve HiGodot persistent-authoring exclusivity and Hera live-QA/non-authoring boundary;
- [x] keep port/process existence as bootstrap evidence only;
- [x] preserve no destructive Git/process side effects.

The Base #288 follow-up used a new semantic RED before these production tokens were added.
""",
)
append_once(
    "docs/decisions/BS-OPS-20260811-03_DEDICATED_LOCAL_EXECUTOR_BOOTSTRAP.md",
    "## Current Base dedicated-environment authority",
    f"""## Current Base dedicated-environment authority

Fresh same-goal Base main observed before Blacksmith acceptance:

`{BASE_288}` — `docs: require project-dedicated local execution environment (#288)`

Blacksmith consumes the shared invariants with project-owned concrete values:

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP
BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY
```

The executor launch is additionally pinned with `codex -C C:\\Users\\user\\Documents\\GitHub\\Ninza\\Blacksmith`. A dedicated PowerShell is a fresh PowerShell process with the Blacksmith environment injected; it is not a second PowerShell installation.
""",
)

# Add the three shared invariants to every current top router block.
routers = [
    "CURRENT_CONFIRMED_DECISIONS.md",
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "[기획서]/00_프로젝트_허브/START_HERE.md",
    "[기획서]/00_프로젝트_허브/ROADMAP.md",
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
]
anchor = "> **PLANNING_COMPLETE / BS-OPS-20260811-03 / PHASE_B_FINAL_REVIEW_COMPLETE / PHASE_C_ENTRY_APPROVED**"
addition = anchor + f"\n>\n> `ASSUME_PREVIOUS_POWERSHELL_CLOSED` / `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` / `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`\n>\n> `BASE_DEDICATED_ENV_MAIN_OBSERVED: {BASE_288}`"
for path in routers:
    text = read(path)
    if "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST" not in text.split("<!-- R3_R7_PLANNING_BATCH_HISTORICAL_CLOSED_AT_9_OF_10 -->", 1)[0]:
        if anchor not in text:
            raise RuntimeError(f"Phase C top block missing in {path}")
        text = text.replace(anchor, addition, 1)
        write(path, text)

# Active/Start current Base observation is a moving current field; keep historical
# old SHA occurrences elsewhere untouched.
for path in [
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "[기획서]/00_프로젝트_허브/START_HERE.md",
]:
    text = read(path)
    text = text.replace(f"BASE_CURRENT_MAIN_OBSERVED: {OLD_BASE}", f"BASE_CURRENT_MAIN_OBSERVED: {BASE_288}", 1)
    text = text.replace(f"`BASE_CURRENT_MAIN_OBSERVED`: `{OLD_BASE}`", f"`BASE_CURRENT_MAIN_OBSERVED`: `{BASE_288}`", 1)
    write(path, text)

# Relabel pre-planning-complete lower sections so old product-blocked statements are
# explicitly historical evidence rather than active routing.
replace_once(
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "## 현재 R3–R7 기획 재개 상태",
    "## 역사 snapshot — `기획 완료` 직전 R3–R7 9/10 기획 상태",
)
replace_once(
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "이 승인은 **기획 재개 승인**이다. Task3 또는 일반 제품 구현 승인이 아니다.",
    "이 문장은 `기획 완료` 직전 Decision09의 **역사적 기획 재개 경계**다. 현재 Phase C 구현 Gate는 상단 `BS-OPS-20260811-03`이 소유하며, Task3는 여전히 별도 승인 대상이다.",
)
replace_once(
    "[기획서]/00_프로젝트_허브/START_HERE.md",
    "## 현재 R3–R7 설계 재개",
    "## 역사 snapshot — `기획 완료` 직전 R3–R7 9/10 설계 상태",
)

# Hera closure: preserve historical Task2/Hera authority, but make current routing
# assert Phase C entry rather than the old planning-only product gate.
hera = "tests/test_hera_postmerge_closure_contract.py"
replace_once(hera, f'BASE_CURRENT_MAIN_OBSERVED = "{OLD_BASE}"', f'BASE_CURRENT_MAIN_OBSERVED = "{BASE_288}"')
replace_once(
    hera,
    "def test_handoff_router_records_current_main_and_r3_planning_only_boundary() -> None:",
    "def test_handoff_router_records_current_main_and_bounded_phase_c_boundary() -> None:",
)
replace_once(
    hera,
    '        assert "R3_R7_DESIGN_ACTIVE" in text\n        assert R3_FIRST_DECISION_ID in text\n        assert R3_THIRD_DECISION_ID in text\n        assert R3_CURRENT_DECISION_ID in text\n        assert R3_CURRENT_RESUME_LOCATOR in text\n        assert "PRODUCT_IMPLEMENTATION: BLOCKED" in text\n        assert "TASK3_IMPLEMENTATION: NOT_APPROVED" in text\n',
    '        assert "R3_R7_DESIGN_ACTIVE" in text  # historical planning snapshot remains discoverable\n        assert R3_FIRST_DECISION_ID in text\n        assert R3_THIRD_DECISION_ID in text\n        assert R3_CURRENT_DECISION_ID in text\n        assert R3_CURRENT_RESUME_LOCATOR in text\n        assert "BS-OPS-20260811-03" in text\n        assert "PLANNING_COMPLETE: USER_DECLARED" in text\n        assert "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST" in text\n        assert "P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING" in text\n        assert "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON" in text\n        assert "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED" in text\n        assert "HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED" in text\n        assert "HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED" in text\n',
)
replace_once(
    hera,
    '    assert "R3_R7_DESIGN_STATE: R3_R7_DESIGN_ACTIVE" in current\n    assert f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION_ID}" in current\n    assert f"R3_R7_APPROVAL_COUNTER: {R3_CURRENT_APPROVAL_COUNTER}" in current\n    assert R3_THIRD_DECISION_ID in text\n    assert "TASK3_IMPLEMENTATION: NOT_APPROVED" in current\n    assert "PRODUCT_IMPLEMENTATION: BLOCKED" in current\n',
    '    assert "R3_R7_DESIGN_STATE: R3_R7_PLANNING_BATCH_CLOSED_AT_9_OF_10" in current\n    assert f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION_ID}" in current\n    assert f"R3_R7_APPROVAL_COUNTER: {R3_CURRENT_APPROVAL_COUNTER}" in current\n    assert R3_THIRD_DECISION_ID in text\n    assert "BS-OPS-20260811-03" in current\n    assert "PLANNING_COMPLETE: USER_DECLARED" in current\n    assert "P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING" in current\n    assert "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED" in current\n    assert "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON" in current\n    assert "HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED" in current\n    assert "HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED" in current\n',
)

# Current Decisions changed; refresh operating health digest.
health_path = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"
health = json.loads(health_path.read_text(encoding="utf-8"))
digest = hashlib.sha256((ROOT / "CURRENT_CONFIRMED_DECISIONS.md").read_bytes()).hexdigest()
for item in health.get("evidence", {}).get("operating", []):
    if item.get("id") == "BS-CURRENT-DECISIONS":
        item["sha256"] = digest
        break
else:
    raise RuntimeError("BS-CURRENT-DECISIONS evidence missing")
health_path.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("Base #288 / Phase C reconciliation materialized")
print("Base current", BASE_288)
print("CURRENT sha256", digest)
