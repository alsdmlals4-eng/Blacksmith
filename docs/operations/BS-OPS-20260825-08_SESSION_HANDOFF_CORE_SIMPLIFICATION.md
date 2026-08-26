# Blacksmith Session Handoff · Core Simplification

- Decision ID: `BS-OPS-20260825-08`
- Date: `2026-08-25 KST`
- Status: `CURRENT_SESSION_HANDOFF / POSTMERGE_PLANNING_ONLY`
- `PR #207 = MERGED_TO_MAIN / 5c29af1e0bb633f8d4513aee16987a3ff9889a4b`
- `CURRENT_PLANNING_WORK = DAMAGE_PROBABILITY_CURVE / USER_DECISION_REQUIRED`
- Pre-existing protected PR: `#196 / OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. Cold-start rule for the next chat

Do not resume from chat memory alone. Before mutation:

```text
1. fresh-read Base current main and relevant owner docs
2. fresh-read Blacksmith default branch / latest commit / open PRs
3. fresh-read Google Sheet only as migration compatibility evidence for unique/unmigrated or same-ID drift; do not promote it to active canon
4. fresh-read Notion Human Home / Core Detail / Visual Bible / AI System Record
5. report authority conflicts before mutation
6. preserve #196 read-only unless the user explicitly changes that boundary
```

The next chat should treat this handoff as a locator, not as a substitute for fresh authority discovery. Any SHA written in this handoff is historical/post-merge evidence; the live repository head must always be re-read.

## 2. Current planning authority

Current product-design owner:

`docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`

Current approved Decisions:

| Decision | Current meaning |
| --- | --- |
| `BS-ENHANCE-20260825-25` | Enhancement success always advances exactly `+1`. Only `+9 -> +10` is Precision Enhancement. Successful +10 Precision creates exactly one player-facing item keyword, machine-owned by the existing `CATALYST_AFFIX` slot. |
| `BS-DAMAGE-20260825-26` | Replace hidden/numeric CURRENT/MAX durability authority with `NORMAL -> MINOR -> MAJOR -> DESTROYED`. One damage event advances exactly one state. Enhancement-failure damage is impossible through target +10, opens from +11, and its conditional probability must increase or remain equal as target level rises. Exact curve is not final. |
| `BS-CHRONICLE-20260825-27` | Player Chronicle does not list routine enhancement success/failure or `N days ago` rows. Keep meaningful identity/lifecycle events only. Internal provenance/telemetry may retain sequence/day data. |
| `BS-ART-20260825-03` | Current art-direction choice is `ILLUSTRATED_WORKSHOP_BOOK`: hand-drawn workshop notebook, paper/leather/iron/wood material cues, warm workshop feel, modern readable interaction hierarchy. Final product asset/runtime approval is separate. |

Unchanged high-level thesis:

```text
PRIMARY CORE = enhancement tension + DDD
PLAYER QUESTION = STOP or PUSH
ITEM IDENTITY = stable UID through crafting / ownership / world consequence / damage / destruction archive
```

## 3. Damage sources

Enhancement failure:

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
P(DAMAGE | FAILURE, TARGET) = LOW_AT_+11_AND_MONOTONIC_NON_DECREASING
EXACT_CURVE = TUNABLE / NOT_FINAL_PRODUCT_BALANCE
```

Customer/world use:

```text
PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE
ELIGIBLE_DELAYED_CUSTOMER_WORLD_EVENT_CAN_CAUSE_DAMAGE = TRUE
EVENT_DAMAGE_ADVANCE = EXACTLY_ONE_STATE
EXACT_EVENT_PROBABILITY_AND_ELIGIBILITY_TABLE = NOT_FINAL
```

Do not create hidden CURRENT/MAX points behind the four labels.

## 4. Explicitly superseded / stale current-looking material

The following old semantics remain historical evidence only where they conflict with Decisions25~27:

- numeric `CURRENT/MAX` gameplay authority;
- `STABLE/STRESSED/DAMAGED/FRACTURED/CRITICAL` MAX bands;
- MAX-based success penalty and new-effect multiplier;
- `CURRENT -> MAX` repair formula as current fallback;
- MAX overhaul `+15 / cap 60` as current fallback;
- precision milestones at `+10/+20/+30/+40/+50`;
- routine enhancement attempt rows with relative-day labels;
- approved old Visual GDD system values that contain these semantics.

Historical source documents are retained for provenance. The current owner and current-entrypoint routers must win on conflicting fields.

## 5. Current runtime reality

Current V2 runtime/data still implements the pre-simplification model. Examples include:

- `scripts/vertical_slice/domain/vs_item.gd` — CURRENT/MAX fields and old precision milestones;
- `scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd` — old DAMAGE/CRITICAL/MAX-penalty logic;
- repair/overhaul resolvers — old CURRENT/MAX formulas;
- `data/vertical_slice/vertical_slice_schema.json` — old schema contract;
- destroyed-history record — old CURRENT/MAX snapshot fields.

This is `IMPLEMENTATION_DRIFT`, not current design authority. Do not mutate protected product paths until the user later declares current planning complete and an implementation Gate is opened.

## 6. Notion responsibility split

Human-facing current surfaces:

- Home: `3c41b237-eb1c-813f-a481-e415e3250d1c`
- Core Detail: `3c11b237-eb1c-8143-baef-ecf4e697a258`
- Visual Bible: `3c01b237-eb1c-8147-abdf-fab51a8f9ad3`

AI/System Record:

- `3c01b237-eb1c-81a1-8cd0-f8bc7eb2f420`

Human Home must show current gameplay/art meaning directly. PR/SHA/test/evidence/runtime drift belongs in the AI/System Record or repository.

## 7. Visual state and image-storage caveat

The earlier generated Visual GDD boards remain approved only for `INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD` where their system semantics do not conflict with current decisions. The selected replacement direction is `ILLUSTRATED_WORKSHOP_BOOK`.

Do not reuse old CURRENT/MAX, old multi-precision cadence, or dated enhancement-log text from those images as game canon.

Notion image storage must be verified independently from Asset metadata. An Asset Library record, `Approved=true`, hash, or Google Drive Source link does **not** by itself prove that the PNG is directly embedded in Notion `Preview`. If Preview is empty, report `NOTION_DIRECT_IMAGE_EMBED_GAP` rather than claiming the image is uploaded inside Notion.

## 8. Next planning Gates

Do not invent exact values for the unresolved areas. Next order:

```text
1. DAMAGE_PROBABILITY_CURVE
   - exact P(damage | failure, target) from +11..+100
2. FOUR_STATE_REPAIR_MODEL
   - MINOR repair result/cost
   - MAJOR repair result/cost
   - whether MAJOR can enhance before repair
3. CUSTOMER_WORLD_EVENT_DAMAGE_POLICY
   - eligible event classes
   - exact probability/rules
   - how event damage is explained in causal result
4. REPRESENTATIVE_VISUAL_REGENERATION
   - Main Menu
   - Enhancement Main (+1)
   - +9 -> +10 Precision Keyword
   - Four-state Damage/Repair
   - Event-only Chronicle
5. adversarial full-planning review
6. only after explicit user `planning complete` declaration: implementation-plan/runtime Gate
```

## 9. Validation/evidence ceiling at handoff

Planning/documentation technical validation may be GREEN without proving product quality.

Keep these evidence ceilings explicit until actually run:

```text
NEW_CORE_RUNTIME = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_DEVICE = NOT_RUN
ACCESSIBILITY = NOT_RUN
PERFORMANCE = NOT_RUN
NOTION_CLIENT_GEOMETRY_RENDER = NOT_RUN
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
FINAL_DAMAGE_BALANCE = NOT_FINAL
FOUR_STATE_REPAIR_BALANCE = NOT_DECIDED
CUSTOMER_EVENT_DAMAGE_BALANCE = NOT_FINAL
```

## 10. Post-merge state and next-PR rule

PR #207 was validated and merged into Blacksmith main as `5c29af1e0bb633f8d4513aee16987a3ff9889a4b` on 2026-08-25 KST. It is historical completion evidence, not the current task PR.

```text
CORE_SIMPLIFICATION_CANON_MIGRATION = COMPLETE
GITHUB_NOTION_SYNC_FOR_DECISIONS25_27_ART03 = POSTMERGE_PASS
CURRENT_PLANNING_WORK = DAMAGE_PROBABILITY_CURVE
PRODUCT_RUNTIME_IMPLEMENTATION = BLOCKED
PR_196 = OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER
```

For any new planning PR:

- fresh-read current Blacksmith `main` and current Base before branching;
- start from current completed `main`, never from #207's old head;
- inspect #196 only for overlap and keep it read-only;
- keep Google Sheet migration-only unless a unique/unmigrated or same-ID compatibility reconciliation is actually required;
- after merge, read new Blacksmith main and update the Notion System Record `Repo Main SHA` / `Sync State` when repository operational metadata changed.

## 11. Base learning/promotion handoff

This session produced reusable evidence for Base review:

1. a historical regression test must not freeze a superseded current state; history assertions and current-state assertions need separate owners/checks;
2. a visible simplification is not real if a hidden second authority (such as CURRENT/MAX under four labels) still controls gameplay;
3. Visual GDD approval must separate information-architecture approval, gameplay-value authority, art-style approval, and final product-asset approval;
4. Notion Asset metadata/Drive Source is not proof of direct Notion Preview embedding;
5. when a new canon invalidates a dependent formula, mark that formula unresolved/stale rather than silently adapting it.

Promote only the cross-project portions through existing Base owners and Learning Logs. Project-specific enhancement/damage values stay in Blacksmith.
