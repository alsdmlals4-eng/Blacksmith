# BS-OPS-20260828-35 · GitHub-only Canon and Image Execution Routing

- Status: `USER_APPROVED_CURRENT_OPERATIONAL_OVERRIDE`
- Date: `2026-08-28 KST`
- Scope: project documentation, handoff, visual planning and asset-provenance routing only. It does not approve new gameplay scope, Godot implementation, release submission, or rights clearance.

## 1. Current routing

The user has retired Notion from all future Blacksmith work. Historical Notion records remain provenance-only and must not be read, written, or used as current truth.

```text
GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE
GITHUB_HUMAN_FACING_GDD_OWNER = docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md + exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf
HUMAN_FACING_GDD = docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md
HUMAN_FACING_PDF = exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf
HUMAN_FACING_PDF_RECEIPT = docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json
GITHUB_TECHNICAL_TRACE_OWNER = docs/design/PROJECT_AI_PRODUCTION_SPEC.md
GITHUB_OPERATIONAL_OWNER = docs/planning + docs/decisions + docs/operations + code/data/scenes/tests/runtime evidence
NOTION_STATUS = HISTORICAL_REFERENCE_ONLY / NO_FUTURE_READ_WRITE_REQUIRED
NOTION_DESTINATION_READBACK = NOT_APPLICABLE
GOOGLE_SHEET_STATUS = HISTORICAL_MIGRATION_ONLY / NO_FUTURE_WRITE_REQUIRED
```

GitHub current owners, the current handoff, repository Asset Manifest, exact commit SHA, tests, and runtime evidence are the only durable current-routing surfaces. A historical Notion URL, record, preview, or status can prove its own past existence only; it cannot create a current requirement or overrule a repository owner.

The Korean Human-Facing GDD and its PDF are the project owner's primary
reading surface: genre, player point of view, core fun, loops, choice, visual
language, scope, and evidence ceiling must be understandable without reading
machine-oriented terminology. `PROJECT_AI_PRODUCTION_SPEC.md` remains a
technical trace for structured canon, code/data/test routing, and evidence;
it is not the primary human GDD.

## 2. Image execution policy

The user has pre-authorized generation work after the existing actual-consumer and provenance requirements are complete. This changes the timing of the approval gate, not the consumer-first or rights rules.

```text
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
PRIMARY_USE_GATE_REQUIRED = TRUE
REQUIRED_CONSUMER_METADATA = REQUIRED
IMAGE_GENERATION_EXECUTION = USER_PREAUTHORIZED_AFTER_CONSUMER_REQUIREMENT
PRE_GENERATION_USER_APPROVAL = NOT_REQUIRED
POST_GENERATION_USER_LOCK = REQUIRED_FOR_FINAL_DIRECTION_OR_RUNTIME_PROMOTION
GENERATED_CANDIDATE = NOT_PROJECT_ASSET_APPROVED_UNTIL_USER_LOCK
NO_CONSUMER = CUT_OR_DEFER
NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE = TRUE
```

Before generation, record the exact consumer, target aspect/resolution, state-family requirement, repository destination, source/provenance, and fallback if unused. The agent may then generate the candidate without interrupting the user for a pre-generation approval. It must ask only whether the user wishes to lock the selected candidate. Until that lock, a candidate is not a final runtime asset, a release asset, a visual-direction change, or Human/Player Experience evidence.

## 3. Repository receipts

Every locked asset or visual-direction update must record its repository destination, exact path, consumer, provenance/rights state, and exact-head readback. Existing `assets/ASSET_MANIFEST.json`, current visual coverage, structured visual packet, and the current GDD are the intended repository surfaces; create a narrowly scoped record only when no existing owner can hold a required field.

## 4. Supersession

This decision supersedes only the following operational fields in older documents:

- current Notion Project Home, Visual Bible, Flow, Asset Library, System Record, and destination-readback requirements;
- the pre-generation separate-conversation-approval requirement;
- Notion-only comparison-sheet routing.

It does not supersede `BS-ART-20260825-03` style direction, `BS-ART-20260826-04` actual-consumer gate, rights/provenance gates, implementation gates, or historical records.
