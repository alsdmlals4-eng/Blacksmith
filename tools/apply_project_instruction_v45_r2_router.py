#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = "PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md"
DECISION = "BS-OPS-20260811-01"

BLOCKS = {
    ROOT / "AGENTS.md": f'''\n\n## 10. 현재 프로젝트 총 작업지시문\n\n- 작업지시문 정본: `{CANON}` (`v4.5 r2`)\n- 프로젝트 바인딩 override Decision: `{DECISION}`\n- 첨부 source의 Switchy-Express 경로는 원문 보존 역사값이며, 현재 Blacksmith 실행 경로는 `{DECISION}`의 사용자 최신 바인딩을 따른다.\n- 같은 승인 범위는 기술 재검증 후 병합 재승인을 요구하지 않는다. 새 기획 충돌·범위 확대만 별도 사용자 Decision이 필요하다.\n- `PRODUCT_IMPLEMENTATION: BLOCKED`, `TASK3_IMPLEMENTATION: NOT_APPROVED`를 유지한다.\n''',
    ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": f'''\n\n## 현재 프로젝트 작업지시문 바인딩\n\n```yaml\nWORK_INSTRUCTION: V4_5_R2_CURRENT_CANON\nWORK_INSTRUCTION_PATH: {CANON}\nWORK_INSTRUCTION_DECISION: {DECISION}\nPROJECT_REPOSITORY: alsdmlals4-eng/Blacksmith\nPROJECT_LOCAL_PATH: C:\\Users\\user\\Documents\\GitHub\\Ninza\\Blacksmith\nGODOT_PROJECT_PATH: C:/Users/user/Documents/GitHub/Ninza/Blacksmith\nPRODUCT_IMPLEMENTATION: BLOCKED\nTASK3_IMPLEMENTATION: NOT_APPROVED\n```\n\n첨부 v4.5 r2 source의 `Switchy-Express-Cargo-Puzzle` 경로는 source provenance를 위해 수정하지 않고 보존한다. 현재 실행은 `{DECISION}`의 Blacksmith override를 따른다.\n''',
    ROOT / "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": f'''\n\n## 프로젝트 총 작업지시문 정본\n\n| 질문 | 책임 원본 | 상태 |\n|---|---|---|\n| 프로젝트 총 작업지시문 | `{CANON}` | `CURRENT / V4_5_R2` |\n| Blacksmith 경로·repo override | `docs/decisions/{DECISION}_PROJECT_INSTRUCTION_V45_R2_CANON.md` | `CURRENT / USER_APPROVED` |\n\nDecision: `{DECISION}`. Source 원문과 현재 Blacksmith 바인딩 충돌은 숨기지 않고 explicit override로 관리한다.\n''',
}

for path, block in BLOCKS.items():
    text = path.read_text(encoding="utf-8")
    if CANON not in text or DECISION not in text:
        path.write_text(text.rstrip() + block + "\n", encoding="utf-8")
        print(f"UPDATED {path.relative_to(ROOT)}")
    else:
        print(f"UNCHANGED {path.relative_to(ROOT)}")
