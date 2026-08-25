# BS-OPS-20260825-04 · Approved Visual GDD Canon Scrub

- Decision ID: `BS-OPS-20260825-04`
- Date: `2026-08-25 KST`
- Status: `CURRENT_PLANNING_OPERATION`
- Work Mode: `PLAN`
- Baseline Blacksmith main: `2c84793773e74a5b4cdcf9888f972d664d2b8060`
- Base main fresh-read: `3c3376845b9a1b7921a4260aa6259cd61533ffc4`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## Decision

The six `USER_APPROVED_VISUAL_GDD` boards remain approved as human-facing explanatory design references. Their rasterized text and numbers do **not** become gameplay/runtime authority.

The approved operating rule is:

```text
VISUAL GDD = layout / hierarchy / visual language / explanatory intent
CURRENT CANON = semantics / numeric values / availability / outcomes
IMAGE_TEXT_NEVER_OVERRIDES_CANON
```

Each visual has been scrubbed into `KEEP / CANON_VALUE / VARIABLE_PLACEHOLDER / CONFLICT_REMOVE`, and a machine-readable implementation binding contract is added so future UI consumes resolver/data output rather than raster examples.

## Primary corrections discovered

1. First structural-risk decision is `CURRENT +10 -> TARGET +11`; generated `+9 -> +10` risk examples are non-authoritative.
2. Checkpoint `[10,30,60,90]` is a downgrade floor only, not a save/restore or success-bonus checkpoint.
3. MAX, not CURRENT, owns the structural state bands and success/new-effect penalties.
4. Normal repair is `CURRENT=MAX; MAX unchanged`; generated partial repair examples are rejected.
5. Player-facing ordinary repair material is `보강재`; generated ingot/wood/leather bundles are rejected.
6. Normal CURRENT repair does not raise enhancement success probability while MAX is unchanged.
7. First-session +11 PUSH uses the real resolver outcome; no scripted success/failure/tutorial odds.
8. Nadia exact numeric capability remains `SEPARATE_CANON_SOURCE_REQUIRED`; generated weights/scores/quest values are placeholders.
9. Full Nadia world result remains delayed after first-session acknowledgement.

## Repository owners

- `docs/planning/BLACKSMITH_APPROVED_VISUAL_GDD_CANON_SCRUB_20260825.md`
- `docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_SAFE_SPEC_20260825.md`
- `docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_BINDINGS_20260825.json`
- `tests/check_visual_gdd_canon_scrub_contract.py`
- `.github/workflows/visual-gdd-canon-scrub.yml`

## Destination contract

- GitHub: structured authority for scrub/bindings/test contract.
- Notion Human Home / Visual Bible: show the six approved visuals as approved design references and clearly state that canonical runtime values come from current canon.
- Notion System Record: AI/operation evidence, PR/SHA/sync state, and evidence ceiling.
- Google Sheet: migration compatibility + same Decision ID mirror only.

## Explicitly unchanged

- the six generated PNG identities/hashes and their user approval
- `STYLIZED_DARK_FORGE`
- product mechanics and current numeric planning canon
- PR #196, which remains read-only
- runtime/Godot scenes/resources/data

## Evidence ceiling

```text
CANON_SCRUB = DOCUMENTED
IMPLEMENTATION_SAFE_SPEC = DOCUMENTED
RUNTIME = NOT_RUN
HUMAN = NOT_RUN
ANDROID = NOT_RUN
ACCESSIBILITY = NOT_RUN
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION
```
