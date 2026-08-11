# Pre-Work Research Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Canonize `BS-OPS-20260811-02` so every meaningful Blacksmith work item requires benchmark + current professional/official research before design, canon mutation, implementation, tests, assets, or configuration changes.

**Architecture:** Keep the v4.5 r2 source document verbatim. Add a project-level refinement Decision that narrows research depth by work type, then propagate a small set of machine-readable tokens into existing authority surfaces. Protect the contract with a focused Python document test and use the existing PR/exact-head CI path; keep R3–R7 at 2/10 and product/Task3 blocked.

**Tech Stack:** Markdown canon, Python `pytest`/document contract tests, GitHub PR validation, Google Sheets same-ID synchronization.

## Global Constraints

- Decision ID: `BS-OPS-20260811-02`.
- Refines only the benchmark/research scope of `BS-OPS-20260805-01`; its TDD and early-checkpoint authority remain active.
- `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md` stays byte/content untouched in this change.
- Base current main baseline at start: `315c66eea9614c284b9c11c4d522141065dfa4b0`.
- Blacksmith main baseline at start: `ec0ab3b971955cb25409535eb7d9c2108b82fbeb`.
- Open PR inventory at start: PR `#81` only, `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT`.
- R3–R7 counter stays `2/10`.
- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- No changes to `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.

---

### Task 1: Add a failing contract test

**Files:**
- Create: `tests/test_pre_work_research_gate.py`

**Interfaces:**
- Consumes: current repository text files through `pathlib.Path`.
- Produces: a focused document contract proving Decision file existence, propagation tokens, merge-policy freshness, and product-scope preservation.

- [ ] **Step 1: Write the failing test**

```python
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
    assert "R3_R7_APPROVAL_COUNTER: 2/10" in gates
    assert "PRODUCT_IMPLEMENTATION: BLOCKED" in gates
    assert "TASK3_IMPLEMENTATION: NOT_APPROVED" in gates
```

- [ ] **Step 2: Push only the test and observe RED**

Expected failure: missing `docs/decisions/BS-OPS-20260811-02_PRE_WORK_RESEARCH_GATE.md` or missing propagation tokens. Record the failed workflow run/job as RED evidence.

- [ ] **Step 3: Do not weaken assertions to match stale canon**

The RED is valid only when it fails because the approved gate is absent. Syntax/import/harness failure is not acceptable RED evidence.

---

### Task 2: Materialize the approved operating Decision

**Files:**
- Create: `docs/decisions/BS-OPS-20260811-02_PRE_WORK_RESEARCH_GATE.md`
- Modify: `AGENTS.md`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`

**Interfaces:**
- Consumes: `BS-OPS-20260805-01`, `BS-OPS-20260811-01`, v4.5 r2, current R3–R7 state.
- Produces: one active project-level pre-work research gate and stable routing tokens for future sessions.

- [ ] **Step 1: Create the Decision responsibility file**

The file must state:

```yaml
DECISION_ID: BS-OPS-20260811-02
STATUS: USER_APPROVED_PRE_WORK_RESEARCH_GATE
REFINES: BS-OPS-20260805-01_BENCHMARK_SCOPE_ONLY
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
R3_R7_APPROVAL_COUNTER: 2/10
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

It must include work-type tiers, source quality, `ADOPT / ADAPT / REJECT / DIFFERENTIATOR`, `BENCHMARK_NOT_APPLICABLE`, evidence-packet schema, and the 2026-08-11 research basis.

- [ ] **Step 2: Update `AGENTS.md` entry order**

Replace the current benchmark subsection with a stricter form:

```text
fresh authority preflight
→ PRE_WORK_RESEARCH_GATE
→ brainstorming/adversarial review
→ RED → GREEN → REFACTOR
→ exact-head validation
→ GitHub/Sheet readback
→ approved-scope merge policy
```

Also remove stale wording that says every merge requires a new explicit user approval; use the already-approved v4.5 r2 rule: same approved scope inherits merge authority after exact technical validation, while new planning conflict/scope expansion requires a new user Decision.

- [ ] **Step 3: Add the Decision to `CURRENT_CONFIRMED_DECISIONS.md`**

Add one bullet under current approved Decisions and an operating note that it refines only benchmarking/research behavior; do not change `R3_R7_CURRENT_DECISION` or the 2/10 content counter.

- [ ] **Step 4: Add resume context to `ACTIVE_CONTEXT.md`**

Add machine-readable tokens:

```yaml
PRE_WORK_RESEARCH_DECISION: BS-OPS-20260811-02
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
```

Preserve current Toren resume locator and product/Task3 blocks.

- [ ] **Step 5: Add the gate to `DEVELOPMENT_GATES.md`**

Add to Current Gate Summary:

```yaml
PRE_WORK_RESEARCH_DECISION: BS-OPS-20260811-02
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
```

Add a short section defining the required sequence and evidence packet; retain `R3_R7_APPROVAL_COUNTER: 2/10`.

- [ ] **Step 6: Run the focused test and observe GREEN**

Run through the repository's existing PR validation environment. Expected: both tests in `tests/test_pre_work_research_gate.py` pass.

---

### Task 3: Adversarial and exact-head validation

**Files:**
- Review only all PR-changed files.

**Interfaces:**
- Consumes: exact PR head after Task 2.
- Produces: merge-ready evidence or a bounded fix list.

- [ ] **Step 1: Review the actual PR diff**

Attack:

- duplicate authority vs `BS-OPS-20260805-01`
- accidental edit of the verbatim v4.5 r2 source
- false requirement to compare unrelated games for technical maintenance
- ability to use `BENCHMARK_NOT_APPLICABLE` as a blanket bypass
- R3–R7 counter drift to 3/10
- product/Task3 gate opening
- stale merge-policy wording
- missing GitHub/Sheet same-ID propagation

- [ ] **Step 2: Classify findings**

Use `MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED`. Only `MUST_FIX` and in-scope `SHOULD_FIX` may change the branch automatically.

- [ ] **Step 3: Re-run exact-head workflows**

Require all workflows associated with the final PR head to be `SUCCESS`. Record workflow names/run IDs. Do not claim Human/Android/accessibility/performance evidence that was not run.

- [ ] **Step 4: Check review state**

Require unresolved inline review threads = 0 and requested-changes reviews = 0 before merge.

---

### Task 4: Merge and postmerge readback

**Files:**
- No new source changes unless postmerge conflict is found.

**Interfaces:**
- Consumes: exact validated PR head.
- Produces: new main SHA and postmerge canonical truth.

- [ ] **Step 1: Re-read main immediately before merge**

Confirm base main has not moved in a way that invalidates the exact-head evidence.

- [ ] **Step 2: Merge with expected-head protection**

Use squash merge and pass the exact validated head SHA.

- [ ] **Step 3: Re-read new main**

Verify Decision file, AGENTS, Current Decisions, Active Context, Development Gates, 2/10 counter, product/Task3 blocks.

---

### Task 5: Same-ID Google Sheet synchronization

**Files:**
- Google Sheet only.

**Interfaces:**
- Consumes: postmerge main SHA and Decision `BS-OPS-20260811-02`.
- Produces: same-ID operational state and change-history evidence.

- [ ] **Step 1: Append a row to `02_현재_확정결정`**

Record Decision ID, approval date, operating category, rule summary, status, protected gates, canon path, merged main SHA, PR/head evidence, and sync status.

- [ ] **Step 2: Update `00_프로젝트_허브!F2`**

Add `BS-OPS-20260811-02 PRE_WORK_RESEARCH_GATE MAIN_CANON` without changing the R3–R7 2/10 state.

- [ ] **Step 3: Append `99_변경이력`**

Record preflight SHAs, research sources, TDD RED→GREEN evidence, adversarial findings, exact-head CI, merged main SHA, and affected ranges.

- [ ] **Step 4: Read all written ranges back**

Require exact same-ID and main SHA match between GitHub and Sheet. If they conflict, report and repair before completion.

---

## Self-review

- Spec coverage: all approved requirements are mapped to Tasks 1–5.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation steps remain.
- Type/token consistency: Decision ID and gate tokens are identical across tasks.
- Scope check: this is one operating-system governance change; no product implementation is included.
