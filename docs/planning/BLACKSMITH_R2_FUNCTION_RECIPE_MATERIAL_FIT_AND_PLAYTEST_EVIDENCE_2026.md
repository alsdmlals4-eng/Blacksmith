# Blacksmith R2 Batch 005 Material Recipe Verification Evidence

- Decision: `BS-ITEM-20260806-06`
- Batch: `R2_BATCH_005_10_OF_10`
- Status: `APPROVED_PENDING_MERGE / BATCH_FULL`
- Product implementation: `BLOCKED`

## RED

```text
RED_HEAD=f90dcdf70eabd30ecdde4def11a2ef30112a3caa
RED_PLANNING_FIRST_RUN=283
RED_EXISTING_PASS=76
RED_EXPECTED_FAIL=10
RED_FAILURE_SCOPE=DECISION_10_OF_10_CANON_MATERIAL_FORGING_RECIPE_PLAYTEST_SHEET_ABSENT
```

## GREEN

```text
GREEN_SYNC_HEAD=b9ba179232d7d3a35da7da3e85ce55fee1583503
GREEN_ONE_SHOT_RUN=31064922435
GREEN_FOCUSED_PASS=86
GREEN_CORE_ALIGNMENT=PASS
GREEN_BASE_OPERATING_AUDIT=PASS
GREEN_PROTECTED_PRODUCT_PATH_CHANGES=0
GREEN_PROTECTED_CRAFTING_FILES=UNCHANGED
```

## Initial exact-head validation

```text
INITIAL_EXACT_HEAD=065f3bfd424c79c66a241ccd9d042bef6a939a51
PLANNING_FIRST_RUN=292
PLANNING_FIRST_PASS=87
BASE_ADOPTION_RUN=795
PR_VALIDATION_RUN=1386
PYTHON_OPERATING_GODOT=PASS
```

`Validate Project Base Adapter #39` failed because the pull request merge ref used the pre-#115 adapter workflow and an obsolete protected-baseline selection. Blacksmith main subsequently merged PR #115 (`42bd0b8981567d0c6ccfadfb29654416bb0098da`), which selects the adapter-recorded historical baseline for ordinary planning PRs. A later branch synchronization run must verify the corrected workflow before merge approval.

## Protection

```text
HUMAN_PLAYTEST=NOT_RUN
PRODUCT_IMPLEMENTATION=BLOCKED
PR_STATE=DRAFT_UNMERGED
```
