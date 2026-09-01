# Blacksmith Current Base Adaptation Work Contract · 2026-09-01

- Status: `CURRENT_PROJECT_OPERATIONAL_OWNER / USER_APPROVED`
- Scope: Blacksmith work order, Base-current adaptation, repository structure, L1+ receipts, context hygiene, and validation workflow.
- Does not own: gameplay meaning, balance, product scope, Scene/Resource/GDScript/data/assets, Base repository state, release approval, or Human/Player Experience approval.

## 1. Base observation and adopted lock

```text
BASE_CURRENT_MAIN_OBSERVED_AT = 2026-09-01 KST
BASE_CURRENT_MAIN_OBSERVED = 19355b7ef065a21d0f2b685c7d9be64a4a3970f8
BASE_CURRENT_OBSERVATION_STATUS = REFERENCE_FOR_PROJECT_ADAPTATION_ONLY

BLACKSMITH_ADOPTED_BASE_RELEASE = v9.4.4
BLACKSMITH_ADOPTED_BASE_RELEASE_COMMIT = 210ec78292fa12ed7563ba743b322dd36103ae4a
BLACKSMITH_ADOPTED_BASE_RELEASE_OWNER = skills/PROJECT_BASE_ADAPTER.json
NO_AUTOMATIC_BASE_PIN_UPDATE = TRUE
NO_MANUAL_GENERATED_ADAPTER_EDIT = TRUE
```

Base current `main` is a fresh-read source for reusable practices and drift detection. It is not a newer Blacksmith adoption simply because its SHA is newer. The generated adapter and snapshot remain the only project-adopted Base release lock until a separately validated release-adoption decision changes them.

## 2. Current Blacksmith owner map

| Question | Current owner | Use in this contract |
|---|---|---|
| User direction, authority precedence, protected paths | `AGENTS.md` | Read first after the latest user instruction. |
| Base-current adaptation and work-mode routing | this document | Resolve Base reuse without duplicating Base or replacing project canon. |
| Cold-start state and accepted frontier | `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md` | Read after this contract; it is a locator, not a frozen substitute for fresh discovery. |
| Product field ownership | `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md` and linked current Decisions | Unchanged; product owner always outranks this operational contract for product facts. |
| Human GDD / technical trace | `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md` / `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` | Unchanged. |
| Adopted Base lock / generated route snapshot | `skills/PROJECT_BASE_ADAPTER.json` / `skills/PROJECT_SKILL_SNAPSHOT.json` | Read-only machine adoption evidence. |

## 3. Project-adapted execution modes

| Mode | Allowed work | Required gate | Explicit exclusion |
|---|---|---|---|
| `PLAN` | fresh canonical read, research, reuse-first comparison, ADOPT/ADAPT/REJECT, design, scope and evidence planning | current owner/consumer/open-PR read plus approval boundary | no implementation or product-scope inference |
| `NONCODING_BUILD` | documentation, structured contract, validator, receipt, metadata, generated derivative readback | RED → GREEN → REFACTOR where a machine contract changes | no change to product behavior or protected product path |
| `GODOT_PRODUCT_BUILD` | only user-approved current-canon MVP implementation and correction | current product owner, protected-path authority, HiGodot/GUT authority, TDD and runtime-feasibility review | no new product scope, no evidence inflation, no manual bypass |
| `REVIEW` | adversarial review, exact-head checks, runtime evidence classification, PR/CI/readback, learning handoff | current PR head, required checks, destination readback | no unverified Human/Android/accessibility/performance/release PASS |

`PLAN → NONCODING_BUILD → GODOT_PRODUCT_BUILD → REVIEW` is a routing sequence, not a license to perform every mode in one task. Select the smallest mode that is sufficient for the approved scope. A `NONCODING_BUILD` task never upgrades itself into `GODOT_PRODUCT_BUILD`.

## 4. Required work sequence

```text
latest user instruction
→ AGENTS.md
→ this contract
→ current handoff + product owner + actual consumer + open PR boundary
→ Base current relevant owner and adopted adapter route
→ benchmark/reuse/legacy-hygiene receipt
→ adversarial + feasibility pre-check
→ RED
→ selected mode implementation
→ GREEN / REFACTOR
→ exact-head validation
→ branch push / PR / CI
→ merge only through repository protection
→ main and destination readback
→ evidence ceiling + reuse-learning handoff
```

For L1 and above, the repository-owned receipt must include a nonempty `benchmark_preflight_receipt` and `context_configuration_hygiene` inventory. `NOT_APPLICABLE` is reserved for L0 mechanical work. Current project canon and actual consumers precede Base reference material; external research never changes a product field without its user-approved owner.

## 5. Legacy and configuration hygiene

| Classification | Paths / kind | Policy |
|---|---|---|
| `ACTIVE_OWNER` | `AGENTS.md`, current handoff, Planning Authority Index, current Decisions, actual code/data/scenes/tests/runtime evidence, project adapter | Read and update only when the approved change affects their owned fact. |
| `COMPATIBILITY` | `[기획서]/00_프로젝트_허브/*`, `docs/BASE_ADOPTION_PROFILE.json`, earlier Base adoption audits | Preserve provenance and direct consumers. Do not treat stale operational vocabulary as current authority. |
| `ARCHIVE` | historical R1/R2/R3 docs, merged PR evidence, previous plans/specs/reports | Preserve as historical evidence; never promote an old value over a current owner. |
| `OBSOLETE_CANDIDATE` | only a file with a confirmed duplicate owner and zero checked references/consumers | No deletion without a recoverable Git path, before/after reference check, and exact readback. |
| `UNKNOWN_UNVERIFIED` | a file with unclear owner, provenance, or consumer | Preserve and investigate; no automatic move, rewrite, or deletion. |

`docs/BASE_ADOPTION_PROFILE.json` remains a compatibility profile because archive governance and operating-system audit tools consume it. The file is not a current Base-release owner. `docs/BASE_RULES_VERSION.md` is historical adoption evidence; this contract and the generated adapter resolve current adoption questions.

## 6. Non-negotiable project boundaries

```text
GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE
NOTION_STATUS = HISTORICAL_REFERENCE_ONLY / NO_FUTURE_READ_WRITE_REQUIRED
GOOGLE_SHEET_STATUS = HISTORICAL_MIGRATION_ONLY / NO_FUTURE_WRITE_REQUIRED
NO_PRODUCT_PATH_CHANGE = TRUE
PROTECTED_PRODUCT_PATHS = data/ / scripts/ / scenes/ / assets/ / addons/ / project.godot
OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER = PR #196
NO_DIRECT_MAIN_PUSH = TRUE
NO_FORCE_PUSH = TRUE
```

Decision `BS-OPS-20260828-35` continues to own GitHub-only canon and image execution routing. Decision `BS-OPS-20260828-36` continues to require fresh read, current research, adversarial review, feasibility confirmation, correction/readback, and an explicit evidence ceiling for substantive work. This contract does not reactivate Notion or Google Sheet, and it does not alter image candidate, user-lock, rights, or runtime-promotion policy.

## 7. Validation and evidence ceiling

Run the following for a contract change before PR creation:

```powershell
& $python C:\Users\user\Documents\GitHub\Base\tools\validate_work_contract_receipt.py --receipt docs/operations/receipts/2026-09-01-base-current-adaptation-work-contract.json
& $python tests/check_base_current_adaptation_work_contract.py
& $python tests/check_current_authority_entrypoint_contract.py
& $python tools/check_archive_governance.py
& $python C:\Users\user\Documents\GitHub\Base\tools\check_project_operating_contract.py --project-root . --base-repository C:\Users\user\Documents\GitHub\Base --check
```

Then review the exact branch diff, verify no protected product path changed, and read back the remote PR head and merged `main`. This contract validates repository/contract structure only. Godot runtime, Android device, accessibility, performance, visual-client, Human/Player Experience, rights, and release evidence remain `NOT_RUN` unless separately observed.

## 8. Supersession and rollback

This document supersedes only conflicting **operational-routing** claims in compatibility material that imply an older Base release is the current lock, that `BUILD` is an undifferentiated mode, or that Notion/Google Sheet requires future sync. It does not alter historical content, game rules, current product owners, or generated adapter data.

Rollback is a normal revert of the associated documentation-and-test PR. No deletion, migration, Base mutation, protected-path edit, direct-main push, force-push, ruleset bypass, or external permission change is authorized by this contract.
