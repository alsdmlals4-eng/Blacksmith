from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_pre_work_research_gate_is_canonical_and_propagated():
    decision = read("docs/decisions/BS-OPS-20260811-02_PRE_WORK_RESEARCH_GATE.md")
    agents = read("AGENTS.md")
    decisions = read("CURRENT_CONFIRMED_DECISIONS.md")
    active = read("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md")
    gates = read("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md")

    for text in (decision, agents, decisions, active, gates):
        assert "BS-OPS-20260811-02" in text

    for token in (
        "PRE_WORK_RESEARCH_GATE",
        "ADOPT",
        "ADAPT",
        "REJECT",
        "DIFFERENTIATOR",
        "BENCHMARK_NOT_APPLICABLE",
    ):
        assert token in decision

    assert "PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK" in gates
    assert "PRE_WORK_RESEARCH_GATE" in agents
    assert "BS-OPS-20260805-01" in decision
    assert "PRODUCT_IMPLEMENTATION: BLOCKED" in decision
    assert "TASK3_IMPLEMENTATION: NOT_APPROVED" in decision


def test_current_merge_policy_and_product_blocks_do_not_regress():
    agents = read("AGENTS.md")
    gates = read("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md")

    assert "같은 승인 범위" in agents
    assert "재승인" in agents
    assert "R3_R7_APPROVAL_COUNTER: 4/10" in gates
    assert "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04" in gates
    assert "BS-CONTENT-20260811-03" in gates
    assert "PRODUCT_IMPLEMENTATION: BLOCKED" in gates
    assert "TASK3_IMPLEMENTATION: NOT_APPROVED" in gates