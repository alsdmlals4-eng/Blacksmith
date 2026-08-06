# BCA Workflow Parse Repair Design

## Problem

`.github/workflows/validate-bca-visual-sheet-adoption.yml` is registered by GitHub under its file path, creates zero jobs, and fails immediately on pushes. The same failure existed on main before and after PR #109, so it is a preexisting workflow-definition problem rather than a planning or product regression.

## Scope

Repair only the BCA validation workflow and its workflow-level regression contract.

In scope:

- canonical block-form GitHub Actions YAML
- explicit quoted top-level `"on"` key for YAML 1.1/1.2 tooling compatibility
- pinned action SHAs
- full checkout history for `origin/main...HEAD`
- deterministic workflow contract test
- actual GitHub job creation and PASS evidence

Out of scope:

- game design or balance changes
- Google Sheet content changes
- runtime, data, scripts, scenes, images, assets, addons, or `project.godot`
- changes to the existing BCA adoption assertions

## Root-cause boundary

Because the invalid workflow creates no job, there is no executable job log. The repair therefore treats GitHub's zero-job failure as the authoritative symptom and removes all compact/ambiguous YAML constructs at once rather than guessing one byte-level parser defect.

The repaired workflow must use:

```yaml
name: Validate Blacksmith BCA Adoption

"on":
  pull_request:
    branches:
      - main
    paths:
      - ...
```

It must also use block-form permissions, quoted concurrency expression, pinned actions, `fetch-depth: 0`, and named steps.

## TDD

1. Add `tests/test_bca_workflow_contract.py` and route it through the already valid Planning-first workflow.
2. Confirm RED against the compact invalid workflow.
3. Replace the BCA workflow with canonical YAML.
4. Confirm the regression contract passes and GitHub creates a real `contract` job under the correct workflow name.
5. Confirm full repository validation remains green.

## Conflict review

No game-design conflict is possible in this scope. Any conflict discovered outside CI structure must be reported and excluded from this PR.