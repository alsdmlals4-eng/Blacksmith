# BCA Workflow Parse Repair Implementation Plan

**Goal:** Replace the zero-job BCA Actions definition with a canonical, executable workflow and lock the structure with a regression contract.

**Constraints:** No game-design, Sheet-content, or product-path changes. Keep the PR Draft and unmerged until explicit approval.

### Task 1 — Establish RED

- [ ] Add `tests/test_bca_workflow_contract.py`.
- [ ] Route the test through the valid Planning-first workflow.
- [ ] Open a Draft PR and verify expected failure against the current compact workflow.

### Task 2 — Repair workflow

- [ ] Rewrite `.github/workflows/validate-bca-visual-sheet-adoption.yml` in canonical block form.
- [ ] Quote `"on"` and concurrency expression.
- [ ] Pin checkout/setup-python actions.
- [ ] Use `fetch-depth: 0` before comparing `origin/main...HEAD`.
- [ ] Include the workflow contract test in trigger paths and the BCA job.

### Task 3 — Verify

- [ ] Confirm the BCA workflow is displayed by name, creates a `contract` job, and passes.
- [ ] Confirm Planning-first, Thin Adapter, Project Adapter, Base adoption, PR validation, Python, and Godot pass on the exact head.
- [ ] Confirm comments/review threads are clear and product-path changes are zero.
- [ ] Update the PR body with RED/GREEN evidence; do not merge.