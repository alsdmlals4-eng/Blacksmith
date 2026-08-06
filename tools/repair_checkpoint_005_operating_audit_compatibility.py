from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
ACTIVE = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
ROADMAP = ROOT / "[기획서]/00_프로젝트_허브/ROADMAP.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.rstrip() + "\n"
        path.write_text(text, encoding="utf-8")


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["batch_005_planning_closure_evidence"] = {
        "status": "CLOSED_MERGED_PR109_MAIN_CANON",
        "planning_pr": 109,
        "planning_merge_sha": "31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9",
        "checkpoint_closure_pr": 117,
        "checkpoint_closure_merge_sha": "06f03323c1309d8da0e6f5b9f4680a20ce388126",
    }
    REGISTRY.write_text(
        json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    append_once(
        ACTIVE,
        "MERGED_PR106",
        "## 역사 상태 호환 표기\n\n- 체크포인트 004 제작 기획 상태: `MERGED_PR106 / MAIN_CANON`\n- 이 표기는 현재 활성 배치가 아니라 불변 병합 이력이다.",
    )
    append_once(
        ROADMAP,
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "## 세 수식어 불변 계약\n\n```text\nGRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX\n```\n\n일반 수식어 A·B와 보조재료 슬롯은 재도입하지 않는다.",
    )
    append_once(
        GATES,
        "## Three Affix Gate",
        "## Three Affix Gate\n\n```text\nGRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX\n```\n\n세 슬롯의 생성·진화·덮어쓰기 책임을 분리한다. 판정: `REQUIRED`.",
    )
    append_once(
        GATES,
        "## Benchmark Gate",
        "## Benchmark Gate\n\n- 새 Decision과 수치 프리셋은 유사 게임·현업 사례 비교를 먼저 수행한다.\n- 결과는 `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성`으로 기록한다.\n- 프로젝트 코어와 충돌하는 유명 사례는 비채택한다.\n\n판정: `REQUIRED_BY_BS-OPS-20260805-01`.",
    )


if __name__ == "__main__":
    main()
