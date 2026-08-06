# BCA Workflow Parse Repair Implementation Plan

**Goal:** Replace the zero-job BCA Actions definition with a canonical, executable workflow and lock the structure with a regression contract.

**Constraints:** No game-design, Sheet-content, or product-path changes. Keep the PR Draft and unmerged until explicit approval.

### Task 1 — Establish RED

- [x] Add `tests/test_bca_workflow_contract.py`.
- [x] Route the test through a known-valid workflow for the RED observation.
- [x] Open a Draft PR and verify expected failure against the invalid workflow.

### Task 2 — Repair workflow

- [x] Rewrite `.github/workflows/validate-bca-visual-sheet-adoption.yml` in canonical block form.
- [x] Escape the literal `[기획서]` directory in the GitHub `paths` glob as `\[기획서\]`.
- [x] Pin checkout/setup-python actions.
- [x] Use `fetch-depth: 0` before comparing `origin/main...HEAD`.
- [x] Include the workflow contract test in trigger paths and the BCA job.
- [x] Align the previously hidden BCA metadata contract with current Base `9.4.0` release and evidence fields.

### Task 3 — Verify

- [x] Confirm the BCA workflow is displayed by name, creates a `BCA visual Sheet adoption contract` job, and passes.
- [x] Confirm Thin Adapter, Project Adapter, Base adoption, PR validation, Python, and Godot pass on the exact head.
- [x] Confirm comments/review threads are clear and product-path changes are zero.
- [x] Keep the final PR diff independent from PR #117 by removing the temporary Planning-first router edit.
- [x] Update the PR body with RED/GREEN evidence.

### Post-PR #117 integration verification

PR #117 was squash-merged to main as `06f03323c1309d8da0e6f5b9f4680a20ce388126`. This checklist update intentionally creates a new PR #118 exact head so GitHub rebuilds the pull-request merge ref against that main commit and reruns the full validation set before PR #118 integration.
