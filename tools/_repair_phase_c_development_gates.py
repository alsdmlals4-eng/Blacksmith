from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
TEST = ROOT / "tests/test_vertical_slice_new_campaign_initializer_authority.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing anchor {label}: {old[:180]!r}")
    return text.replace(old, new, 1)


g = GATES.read_text(encoding="utf-8")
g = replace_once(
    g,
    "- R3–R7 `9/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.",
    "- R3–R7 planning은 사용자 `기획 완료`로 9/10에서 닫혔다. 현재 제품 구현은 기존 승인 canon 범위의 Phase C만 허용되고, Task3·신규 범위는 별도 승인 대상이다.",
    "pre-work current phase",
)
g = replace_once(
    g,
    "판정: `USER_APPROVED / REQUIRED / PLANNING_ONLY`.",
    "판정: `USER_APPROVED / REQUIRED / PHASE_C_EXISTING_CANON_ONLY`.",
    "pre-work verdict",
)
g = replace_once(
    g,
    "## R3–R7 Planning-Only Gate",
    "## Historical R3–R7 Planning-Only Gate — closed at 9/10",
    "historical R3 heading",
)
g = replace_once(
    g,
    "## Product Implementation Gate\n\n일반 제품 구현은 `BLOCKED`다. 버티컬 슬라이스는 R2 Batch 006이 승인한 namespace와 사용자 승인 Task에서만 허용한다. Task2의 승인 범위는 병합·postmerge CI closure까지 완료됐으며, 이를 다음 Task나 일반 제품 Gate 개방으로 해석하지 않는다. `BS-VS-INIT-20260808-01`, `BS-HIGODOT-20260808-01`, `BS-HIGODOT-EXEC-20260808-01`, `BS-TOOLCHAIN-20260809-01`은 각자의 승인 범위를 넘어 확장되지 않는다.\n\n`BS-CONTENT-20260811-01`~`BS-CONTENT-20260811-09`는 planning-only Decision이며 현재 Decision은 `BS-CONTENT-20260811-09`다. 이 승인들만으로 제품 구현, Task3, HiGodot authoring scope를 개방하지 않는다.",
    "## Product Implementation Gate\n\n사용자 `기획 완료`와 `BS-OPS-20260811-03`에 따라 **이미 승인된 current canon 범위의 제품 구현만** `PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON`이다. 첫 영속 Godot 저작 전에 `P0_LOCAL_EXECUTOR_BOOTSTRAP`과 Codex 내부 fresh HiGodot project/session/version/readiness receipt가 필수다. Task2의 역사 범위는 그대로 보존하며, `BS-VS-INIT-20260808-01`, `BS-HIGODOT-20260808-01`, `BS-HIGODOT-EXEC-20260808-01`, `BS-TOOLCHAIN-20260809-01`의 과거 승인 범위를 임의 확장하지 않는다.\n\n`BS-CONTENT-20260811-01`~`BS-CONTENT-20260811-09`는 완료된 기획 정본이며 Phase C 구현 입력이다. 승인되지 않은 신규 게임 시스템·범위 확대는 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED_BEYOND_EXISTING_APPROVED_CANON`, Task3는 `TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED`다.",
    "product implementation gate",
)
g = replace_once(g, "GENERAL_PRODUCT: BLOCKED", "GENERAL_PRODUCT: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON", "missing state general product")
g = replace_once(g, "R3_R7_DESIGN: ACTIVE_PLANNING_ONLY", "R3_R7_DESIGN: PLANNING_COMPLETE_CLOSED_AT_9_OF_10", "missing state R3")
g = replace_once(g, "TASK3_IMPLEMENTATION: NOT_APPROVED", "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED", "missing state task3")
g = replace_once(g, "PRODUCT_IMAGE: BLOCKED_NOT_PRODUCT_READY", "PRODUCT_IMAGE: DEFERRED_BY_USER", "missing state image")
g = replace_once(g, "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED\n```\n\nTask2의 script", "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED_BEYOND_EXISTING_APPROVED_CANON\n```\n\nTask2의 script", "missing state new scope")
g = replace_once(
    g,
    "Task2의 script와 serialized surface는 모두 main에 병합되고 postmerge CI가 폐쇄됐다. R3–R7 설계 재개는 이 제품 구현 폐쇄 상태를 변경하지 않는다. 이미지 목록의 열 정렬 복구나 engine-native UI 사용은 제품 이미지 생성·권리·가독성·런타임 Gate를 개방하지 않는다. 새 제품 Task는 별도 사용자 범위 승인 전 진입하지 않는다.",
    "Task2의 script와 serialized surface는 모두 main에 병합되고 postmerge CI가 폐쇄됐다. 이후 R3–R7 9/10 기획이 완료되어 현재는 기존 승인 canon 범위의 Phase C entry만 열렸다. 이미지 생성은 사용자가 보류했으므로 이미지 생성·권리·가독성·런타임 증거는 여전히 `NOT_RUN`/deferred다. 승인 canon 밖 신규 제품 Task와 Task3는 별도 사용자 범위 승인 전 진입하지 않는다.",
    "missing state narrative",
)
# Current HiGodot/GUT/Hera status block also owns current scope labels.
g = replace_once(g, "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED\nTASK3_IMPLEMENTATION: NOT_APPROVED\n```\n\nHiGodot Task2", "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED_BEYOND_EXISTING_APPROVED_CANON\nTASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED\n```\n\nHiGodot Task2", "authority current scope")
GATES.write_text(g, encoding="utf-8", newline="\n")


t = TEST.read_text(encoding="utf-8")nt_old = '''        self.assertIn(\n            "ENTRY_STATE_GATE: PASS_R3_R7_PLANNING_ONLY_PRODUCT_SCOPE_STILL_REQUIRED",\n            text,\n        )'''
t_new = '''        self.assertIn(\n            "ENTRY_STATE_GATE: PASS_PLANNING_COMPLETE_PHASE_C_EXISTING_CANON_P0_BOOTSTRAP_REQUIRED",\n            text,\n        )'''
t = replace_once(t, t_old, t_new, "initializer entry gate")
t = replace_once(t, '        self.assertIn("GENERAL_PRODUCT: BLOCKED", text)', '        self.assertIn("GENERAL_PRODUCT: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON", text)', "initializer general product")
t = replace_once(t, '        self.assertIn("R3_R7_DESIGN: ACTIVE_PLANNING_ONLY", text)', '        self.assertIn("R3_R7_DESIGN: PLANNING_COMPLETE_CLOSED_AT_9_OF_10", text)', "initializer R3")
t = replace_once(t, '        self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", text)', '        self.assertIn("TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED", text)', "initializer Task3")
t = replace_once(t, '        self.assertIn("NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED", text)', '        self.assertIn("NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED_BEYOND_EXISTING_APPROVED_CANON", text)', "initializer new scope")
t = replace_once(t, '        self.assertIn("BS-CONTENT-20260811-08", text)', '        self.assertIn("BS-CONTENT-20260811-08", text)\n        self.assertIn("BS-OPS-20260811-03", text)\n        self.assertIn("PLANNING_COMPLETE: USER_DECLARED", text)\n        self.assertIn("P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING", text)', "initializer phase c owner")
TEST.write_text(t, encoding="utf-8", newline="\n")

print("Phase C Development Gates and initializer current assertions repaired")
