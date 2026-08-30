# SDD ledger — plan: C:\Users\user\Documents\GitHub\Ninza\Blacksmith\docs\superpowers\plans\2026-08-30-blacksmith-recurring-precision-tag-evolution.md

## Workspace and authority

- Worktree: `C:\Users\user\Documents\GitHub\Ninza\Blacksmith-worktrees\codex-recurring-precision-tag-evolution-20260830`
- Branch start: `ab7ca9ba1bf6599bb96a16eb44688475a64a25bf` (`codex/recurring-precision-tag-evolution-20260830`)
- Binding design spec: `C:\Users\user\Documents\GitHub\Ninza\Blacksmith\docs\superpowers\specs\2026-08-30-blacksmith-recurring-precision-tag-evolution-design.md`
- User direction: `+9→+10` through `+99→+100` are Precision; every successful Precision action is exactly one `ADD_TAG` or `UPGRADE_TAG`.
- Isolation: the dirty primary `main` worktree, its user-owned GDD/PDF/receipt/AI-spec/contract-test changes, `.base-contract/`, `tmp/`, and PR #196 are outside this worktree and will not be staged, reset, copied, or merged.

## Pre-flight plan/interface scan

| Producer task | Consumer task | Shared file or interface | Check and ruling |
| --- | --- | --- | --- |
| 1 | 2, 3, 4, 5, 6, 7 | Decision38 + catalog schema 2; exact targets/actions/effect values | Clean dependency: Task 1 canon/canonical JSON must land before all runtime consumers. |
| 2 | 3, 4, 5 | `VSItem` V4 `catalyst_affix: Dictionary`, tag entry shape, sole `used_precision_milestones` list | Clean dependency: Task 2 supplies normalized storage; Task 3 must not add a second completion list. |
| 3 | 4, 5 | `selection_preview` / `apply_selection_success` action dictionary and growth result payload | Clean dependency: Task 3 owns resolver mutation; later callers must not duplicate effects. |
| 4 | 5, 7, 8 | atomic save/action outcome and success ledger/Chronicle summary | Clean dependency: UI invokes Task 4 service; GDD describes behavior but does not assert runtime completion. |
| 5 | 6, 7, 8 | Workshop `view_state` and native 48dp controls | Clean dependency: visual requirement and GDD use the actual consumer only after implementation. |
| 6 | 7, 8 | Candidate visual requirement records, candidate status, updated text-native scene flow | Clean dependency: candidate generation cannot promote/bind without user lock; GDD can state candidate status but cannot call it runtime art. |
| 7 | 8 | Markdown/PDF/receipt and document contract | Clean dependency: delivery validation runs only after generated PDF/receipt match source. |
| 1, 7 | 8 | handoff evidence status | Ruling: handoff updates are restricted to exact observed evidence; no future, Android, human-play, or release PASS claim may be written. |

| Task | Internal consistency check | Result |
| --- | --- | --- |
| 1 | Test-first static contract precedes owner/catalog changes; owner documents have a single Decision38 field authority. | Clean. |
| 2 | V4 migration creates no fourth affix/top-level completion field and preserves existing stats. | Clean. |
| 3 | `ADD_TAG` uses lineage/method while `UPGRADE_TAG` uses tag ID; both have one effect on success only. | Clean. |
| 4 | Cost/roll gate belongs before mutation; ordinary targets remain selection-free. | Clean. |
| 5 | Dynamic native controls avoid prohibited scene serialization/assets and align with resolver candidates. | Clean. |
| 6 | Each image record has an actual dynamic runtime consumer, candidate status, explicit fallback, and no fake-screen/flow-map raster path. | Clean; post-generation user lock gates promotion. |
| 7 | GDD/PDF is human-facing while AI spec retains technical trace; ReportLab publisher is deterministic and receipt-backed. | Clean. |
| 8 | Automated, runtime, Android, accessibility, performance, human-play and release evidence remain distinct. | Clean. |

Ruling: retain the existing `VSSaveEnvelope` schema version unless implementation proves an envelope-level field changes. — The V4 catalyst record is an item-owned migration and the plan forbids speculative envelope schema churn. — Cost if wrong: an old envelope might need a narrowly scoped follow-up migration; focused save-boundary tests will expose it before delivery.

Ruling: make `tools/publish_human_facing_gdd_pdf.py` the planned deterministic publisher using the verified bundled ReportLab runtime and available Malgun Gothic font. — The repository has no existing publisher and the user requested a maintained human Blueprint PDF. — Cost if wrong: a reportlab layout limitation requires changing the publisher, not hand-editing the binary.

Ruling: use the current Base `check_project_operating_contract.py --check` as this worktree's entry gate, not `tools/audit_project_operating_system.py`. — The latter asserts superseded R2 snapshot values that the current `AGENTS.md` explicitly classifies below active current owners; it produced nine stale-assertion errors while the current operating-contract validator passed. — Cost if wrong: a legacy audit finding not mapped by the current contract could be missed; the final exact-head validation will retain both its result and the explicit evidence ceiling rather than relabel it PASS.

Ruling: user-approved 2026-08-30 visual scope is three portrait candidate illustrations only: Main Menu, recurring Precision inside Workshop, and Customer World Result. — Each has a current source-verified dynamic consumer/fallback, while the requested flow map remains editable Mermaid/table content. — Cost if wrong: a candidate may need `REBRIEF` after user review; no candidate becomes `assets/`, runtime, or GDD-final art before the required post-generation user lock.

## Task checklist

- [ ] Task 1 — Current-canon amendment and machine-readable catalog
- [ ] Task 2 — V4 `VSItem` catalyst collection and migration boundary
- [ ] Task 3 — Action-aware precision resolver and exact success semantics
- [ ] Task 4 — Atomic enhancement, action service, ledger, and Chronicle integration
- [ ] Task 5 — Workshop tag-growth UI and input flow
- [ ] Task 5.1 — V4 first-forge compatibility repair and app-flow regression
- [ ] Task 5.2 — Customer-world V4 fixture compatibility repair
- [ ] Task 6 — Consumer-first scene art requirements, candidate generation, and lock gate
- [ ] Task 7 — Human-facing GDD, technical trace, and reproducible Blueprint PDF
- [ ] Task 8 — Full regression, adversarial review, runtime evidence, and safe delivery

## Baseline evidence

- `python tests/check_precision_tag_catalog_contract.py` — PASS at `ab7ca9ba`.
- Focused GUT baseline did not start because `godot` is absent from this host's command path (`The term 'godot' is not recognized`). This is an execution-environment discovery result, not a test failure.
- Fresh read of `tools/start_blacksmith_local_executor.ps1` located the historical dedicated executable path. The launcher is not reused because its `8006/9506` port routing is historical-only; the existing exact Godot 4.7.1 binary is used only for the same headless GUT test role pinned by the repository CI. `C:\Users\user\Tools\Godot-Blacksmith-4.7.1\Godot_v4.7.1-stable_win64.exe --version` returned `4.7.1.stable.official.a13da4feb`.
- Focused baseline GUT command with that explicit binary exited `0` for `test_vs_precision_tag_catalog.gd`, `test_vs_item.gd`, and `test_vs_enhancement_resolver.gd`; the runner emitted only its engine banner. Full exact-head GUT/JUnit verification remains Task 7 evidence.
- `python tools/audit_project_operating_system.py --base-root C:\Users\user\Documents\GitHub\Base` wrote its normal generated report and failed only on historical R2 assertions. Its generated tracked report is restored to exact HEAD after inspection; no audit artifact is part of this task.
- `python C:\Users\user\Documents\GitHub\Base\tools\check_project_operating_contract.py --project-root . --base-repository C:\Users\user\Documents\GitHub\Base --check` — PASS at this worktree HEAD.

Task 1: fix round 1/5 started — Authority Index/Core Canon routing conflict, Phase-1 pointer omission, catalog/migration contract gaps, and Decision38 source identity require correction; findings are in `task-1-review-round-1.md`.

Task 1: fix round 1/5 (7 addressed, 0 open; commits 868bb661..51331c87).
Task 1: minor (deferred): `BLACKSMITH_PLANNING_AUTHORITY_INDEX.md` precedence numbering repeats `5`; this is non-semantic documentation numbering.
Task 1: minor (deferred): `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` top Decisions metadata omits Decision38 despite correct body ownership; later owner-metadata review should align it.
Task 1: minor (deferred): `tests/check_core_simplification_current_contract.py` retains a Decision34 ownership assertion; Task 2/whole-branch review must confirm its residual scope remains compatible with Decision38.
Task 1: complete (commits ab7ca9ba..51331c87, review clean after fix round 1).

Task 2: fix round 1/5 started — V4 nested catalyst scalar fields must retain raw type checks and fail closed; finding is in `task-2-review-round-1.md`.
Task 2: fix round 1/5 (1 addressed, 0 open; commits f2af631e..f09c8457).
Task 2: complete (commits 51331c87..f09c8457, review clean after fix round 1).

Task 3: fix round 1/5 started — resolver must fail closed for impossible milestone/tag history and malformed display catalog shapes; findings are in `task-3-review-round-1.md`.
Task 3: fix round 1/5 implemented (2 findings addressed; commit `1b21c0f6`); independent re-review pending.
Task 3: fix round 2/5 started — P2 is addressed, but P1 still permits unassigned used milestones; matching-based complete action-history validation and immutable RED/GREEN coverage are required. Findings are in `task-3-review-round-1-rereview.md`.
Task 3: fix round 2/5 implemented (P1 complete action-history matching; commit `766d00b3`); independent re-review PASS.
Task 3: complete (commits `f09c8457..766d00b3`, two fix/review rounds clean; focused resolver evidence only, whole vertical-slice integration remains Task 4+).

Task 4: started — atomic all-ten-target action service/resolver integration, V4 deep-copy, bounded ledger evidence, and item-owned pending backfill. Binding brief: `task-4-brief.md`.
Task 4: implemented (commit `488cff1a`); 30/30 focused tests and 200 assertions reported, independent review pending. Report: `task-4-report.md`.
Task 4: complete (commit `488cff1a`, independent review PASS; no P0–P3 finding; full regression and runtime remain later evidence).

Task 5: started — dynamic native Workshop action flow/view state for all recurring precision targets. Binding brief: `task-5-brief.md`.
Task 5: review P2 found — independent ADD source selectors exposed an invalid duplicate pair and raw reason risk; implementation fix/re-review required.
Task 5: complete (commit `5b10863d`, review P2 resolved; 19/19 Workshop focused tests, 150 assertions, UI dynamic controls only). App integration remains NOT PASS due to out-of-scope V4 birth-service string assignment at `vs_item_birth_service.gd:43`; schedule repair before claiming end-to-end flow.
Task 5.1: complete (commit `164a8413`) — V4 first-forge now initializes the item-owned empty catalyst record; focused birth-service `4/4` (22 assertions) and app flow `10/10` (47 assertions) pass. Report: `task-5-1-v4-birth-repair-report.md`. Existing `vertical_slice_app.tscn` external-resource invalid-UID warning remains non-blocking and out of scope; current Base validator reports the inherited branch's protected runtime paths, not a validator PASS.
Task 5.1: independent review clean; unrelated P2 legacy V4 scalar fixture remains in `test_vs_customer_world_event_resolver.gd`, so full regression is NOT PASS until a narrow fixture repair completes.
Task 5.2: complete (commit `f41f659a`) — customer-world level-10 fixture now carries canonical V4 `TAG_EMBER_EDGE` stage-I record and matching milestone 10; focused customer suite `8/8` (65 assertions) and app boundary `10/10` (47 assertions) pass. No production scalar fallback added. Report: `task-5-2-customer-fixture-repair-report.md`.
Task 6: complete (commit `ae0a87cd`; three 941×1672 consumer-first generated candidates recorded outside repository, text-native recurring flow map/coverage updated, two document contracts PASS). Candidate/runtime promotion remains blocked pending user lock. Report: `task-6-report.md`.
Task 5.2: complete (commit `f41f659a`, independent review PASS; customer-world focused GUT 8/8 and app boundary 10/10 PASS). Full cross-suite regression remains Task 8 evidence.
Task 6: review P1/P2 repaired (commit `d87b1f93`; original text-like Main candidate rejected, clean replacement verified; Customer Result promotion requires the named native readability veil and Godot/Android checks). Independent re-review PASS; all selected candidates await user lock.
Task 6.1: started — user 2026-08-30 explicit `승인` locks all three reviewed candidates for the narrow dynamic runtime-consumer integration. Binding brief: `task-6-1-approved-art-integration-brief.md`.
# Task 6.1

- Approved art integration implemented with machine contract PASS; focused GUT entrypoint currently INCONCLUSIVE because it emits no test summary or assertion totals.
