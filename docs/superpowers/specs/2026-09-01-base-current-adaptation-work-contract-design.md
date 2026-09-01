# Blacksmith Base Current Adaptation Work Contract Design

- Status: `USER_APPROVED_DESIGN_INPUT / MACHINE_VERIFIED_LOCAL_PR_PENDING`
- Date: `2026-09-01 KST`
- User decision: apply the recommended thin project adaptation after a detailed fresh-read of Base.
- Scope: Blacksmith work order, repository structure, operating-contract routing, receipt validation, and legacy-context classification.
- Out of scope: gameplay meaning, game balance, Godot product behavior, Scene/Resource/GDScript/data/asset changes, Base release adoption, Base repository mutation, Notion/Google Sheet reactivation, and deletion.

## 1. Problem

Blacksmith's generated Base adapter is correctly locked to released Base `v9.4.4`, while current Base `main` contains later unreleased operational improvements. The current Blacksmith authority path is also split between current GitHub-only owners and older compatibility hubs that still expose retired work-mode and Sheet-era vocabulary. A new work session must not mistake either condition for an authorization to change the Base pin, revive legacy surfaces, or modify product paths.

## 2. Selected Architecture

Create one thin Blacksmith-owned operating contract plus one repository-owned L3 receipt and one executable contract check. The contract records the exact Base current observation separately from the adopted `v9.4.4` release lock, maps Base practices to Blacksmith's actual owners, and defines the project-specific execution modes.

```text
Base current main observation
  + Blacksmith adopted Base v9.4.4 adapter lock
  + Blacksmith current authority and product boundaries
  -> BASE_CURRENT_ADAPTATION_WORK_CONTRACT
  -> L3 receipt validated by Base tool
  -> executable entrypoint/anti-regression check
```

No Base body, generated adapter, gameplay owner, or protected product path becomes a second owner.

## 3. ADOPT / ADAPT / REJECT

| Disposition | Base practice | Blacksmith result |
|---|---|---|
| `ADOPT` | repository-first authority, exact SHA provenance, PR validation and remote readback | Make these explicit in the project operating contract. |
| `ADOPT` | reuse-first preflight and legacy classification before deletion | Record actual consumers and preserve materials by default. |
| `ADAPT` | `PLAN -> NONCODING_BUILD -> GODOT_PRODUCT_BUILD -> REVIEW` | Bind each mode to Blacksmith's existing current-canon, protected-path, GUT/HiGodot, asset, and evidence rules. |
| `ADAPT` | L1+ benchmark and context hygiene receipt | Add one project-owned JSON receipt that the Base receipt validator can read. |
| `REJECT` | automatic adoption of unreleased Base main | Keep the verified `v9.4.4` release lock unchanged. |
| `REJECT` | full Base template or Skill-body copy | Keep the current thin adapter and project-local owner paths. |
| `REJECT` | Notion/Google Sheet current-surface restoration | Preserve Decision `BS-OPS-20260828-35` GitHub-only routing. |
| `REJECT` | product changes during an operating-contract change | Leave protected paths untouched. |

## 4. Current Owner Map

| Question | Current Blacksmith owner | Contract treatment |
|---|---|---|
| User instructions and project boundaries | `AGENTS.md` | Highest project-level source after the latest user instruction. |
| Cold-start status and accepted frontier | `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md` | Current locator; add a compact pointer to the new contract. |
| Product meaning and field ownership | `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md` and its linked current Decision owners | Unchanged. |
| Human GDD and technical trace | `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md` and `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` | Unchanged. |
| Project-adopted Base release and generated routes | `skills/PROJECT_BASE_ADAPTER.json` and `skills/PROJECT_SKILL_SNAPSHOT.json` | Remain the only adopted release lock; do not edit manually. |
| Historical project-hub and Base adoption materials | `[기획서]/00_프로젝트_허브/*`, `docs/BASE_ADOPTION_PROFILE.json`, older Base adoption audits | Classify as compatibility/history after consumer checks; do not delete. |

## 5. Contract Requirements

The new contract must:

1. record Base current `main` observed at `19355b7ef065a21d0f2b685c7d9be64a4a3970f8` as a time-bound observation;
2. retain Base release `v9.4.4` / `210ec78292fa12ed7563ba743b322dd36103ae4a` as Blacksmith's adopted lock;
3. define `PLAN`, `NONCODING_BUILD`, `GODOT_PRODUCT_BUILD`, and `REVIEW` without granting new gameplay scope;
4. require L1+ benchmark/reuse/legacy-hygiene receipt entries, exact evidence, a rollback path, and an evidence ceiling;
5. preserve GitHub-only current canon and historical-only Notion/Google Sheet routing;
6. preserve generated-adapter, protected-path, no-direct-main-push, PR #196, and human/device/runtime evidence boundaries;
7. state that a historical compatibility document is not silently erased or promoted to current authority;
8. provide exact validation commands and remote-readback order.
9. run the receipt check in a dedicated PR workflow that checks out the exact observed Base SHA, without changing the adopted Base release lock.

## 6. Verification and Rollback

- A new contract check must fail when the contract and receipt are absent or omit the release lock, mode set, GitHub-only boundary, or legacy classification.
- The check must invoke Base `tools/validate_work_contract_receipt.py` against the repository-owned receipt.
- Existing current-authority, archive-governance, and project-operating-contract validations must remain green.
- No Godot, Android, accessibility, performance, visual-client, human-play, or release claim is introduced; all remain at their existing evidence ceiling.
- Rollback is a normal Git revert of the documentation/test-only PR. No deletion or migration is part of this design.
