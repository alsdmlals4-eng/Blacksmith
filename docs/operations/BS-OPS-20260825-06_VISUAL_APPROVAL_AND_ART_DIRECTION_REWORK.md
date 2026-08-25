# BS-OPS-20260825-06 · Visual Approval + Art Direction Rework

- Date: `2026-08-25 KST`
- Work Mode: `PLAN`
- Status: `IN_PROGRESS / PR206`
- Baseline Blacksmith main: `827ac4147cc58dba22a39b4a3f7babd8079cddff`
- Base fresh-read at start: `210ec78292fa12ed7563ba743b322dd36103ae4a`
- Open pre-existing PR: `#196 OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. User-approved change

The user approved the newly generated Visual GDDs:

- `BS-VIS-20260820-04` · 강화 긴장 Band 상태 매트릭스
- `BS-VIS-20260820-08` · MAX 구조 손상과 강화 페널티 비교

At the same time, the user explicitly rejected the **current generated art style as a future final style** and asked for a later art-direction change because the look reads as too generic/AI-generated and insufficiently ownable.

This operation therefore separates two approvals:

```text
VISUAL_GDD_INFORMATION_ARCHITECTURE = USER_APPROVED
CURRENT_GENERATED_ART_STYLE_AS_FINAL = REJECTED / REWORK_REQUIRED
```

## 2. Binary receipts

### `BS-VIS-20260820-04`

- Generation ID: `d5a862ee-0bcf-4604-930e-23ffda4a9a48`
- SHA-256: `b675de17a0a48b5719c6bb80a4e1bf39f7a7dea99583ba2a9923d5dbb8d0b028`
- Durable Drive ID: `1UUTIvitHRMjW6NVCuzJthWd3U96ZXkw_`
- Notion Asset record: `3c71b237-eb1c-8171-bf2a-d7c38fc643f9`

### `BS-VIS-20260820-08`

- Generation ID: `20e2d949-5bca-4f9d-b289-7ad26220efe1`
- SHA-256: `8cb10166a354f13ee0117c279870bc76bb2f226a13e56e37005952aea329bdec`
- Durable Drive ID: `1qDJ2Khz1I9L0FwdH-XFZ3Zf63CP0_CDp`
- Notion Asset record: `3c71b237-eb1c-81b3-b9eb-e34275055153`

Both Notion records are `Approved=true / Status=APPROVED / Decision=ADOPT`, with approval explicitly limited to explanatory Visual GDD usage.

## 3. Current art-direction status

Decision: `BS-ART-20260825-02`

```text
ART_STYLE_STATUS = REWORK_REQUIRED
STYLIZED_DARK_FORGE = LEGACY_VISUAL_REFERENCE_NOT_FINAL_STYLE_CANON
APPROVED_VISUAL_SCOPE = INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD
REPLACEMENT_ART_STYLE = USER_DECISION_REQUIRED
```

Preserve:
- item/workpiece as visual hero,
- forge materiality and evidence of heat/wear,
- warm localized light against dark surroundings,
- readable STOP/PUSH and damage/risk hierarchy,
- redundant non-color state channels.

Rework:
- overall rendering language,
- black/gold ornamental frame dominance,
- faux-medieval serif/title treatment,
- icon family,
- repeated amber glow,
- panel density,
- generic AI-generated fantasy presentation.

## 4. Reuse-first disposition

Fresh Base #669 requires reuse-first preflight for meaningful Visual work.

This operation is a governance/approval continuation rather than replacement-style creation. Existing project-owned Visual GDDs remain the first source for information structure. No new Base visual skin is adopted, no cross-project skin is copied, and no external benchmark is needed to record the user's explicit approval/rejection state.

For the **next replacement-style design task**, reuse-first must run before creation:

```text
Blacksmith current Visuals / Asset / Reference / Benchmark
-> Base visual semantic/reuse principles
-> targeted external/commercial references
-> >= 3 materially different style alternatives
-> user approval
-> representative regeneration first
```

Reuse learning handoff for this operation:
- selected_modules: `PROJECT_OWNED_APPROVED_VISUAL_GDDS`
- reuse_mode: `REUSE_EXISTING_PROJECT_IMPLEMENTATION / INFORMATION_CONTRACT`
- project_paths_changed: approval manifest, art-direction decision, AGENTS, focused approval test, this ops receipt
- verification_evidence: `RED observed; GREEN pending at authoring time; postmerge readback required`
- evidence_ceiling: `Notion client render / Human comparative style test / Android / runtime NOT_RUN`
- rollback: revert PR #206 and restore previous Visual/style-status projections
- project_only_lessons: separate information-architecture approval from art-style approval
- base_promotion_candidates: `NONE`

## 5. TDD receipt

### RED

Head: `58fabe9db7f6a74ae9e4dd11468623195a856524`

`Validate Visual GDD Asset Approval` run `32803221350`, job `97668137506` failed exactly because the existing manifest lacked:
- 04 and 08 IDs,
- their generation IDs and hashes,
- `BS-ART-20260825-02`,
- `ART_STYLE_STATUS = REWORK_REQUIRED`,
- legacy-not-final style guard,
- information-architecture-only approval guard.

Checkout and Python setup succeeded. This is the intended RED.

### GREEN

`PENDING_EXACT_HEAD_VALIDATION`

## 6. Adversarial review · minimum five full loops

### Loop 1 · approval overreach

Attack: Visual approval could accidentally become final product/style approval.

Refinement: manifest and Notion records explicitly split information-GDD approval from final style/runtime asset approval.

Result: `PASS_PENDING_GREEN`.

### Loop 2 · stale art authority

Attack: root `AGENTS.md` still called `STYLIZED_DARK_FORGE` current and said no approved representative images existed.

Refinement: route `BS-ART-20260825-02`, 8 approved Visual GDDs, and `REWORK_REQUIRED` at the entrypoint.

Result: `PASS_PENDING_GREEN`.

### Loop 3 · binary identity / destination integrity

Attack: image approval without durable identity could be unrecoverable.

Refinement: generation ID + SHA-256 + durable Drive ID + Notion Asset record are recorded for both 04 and 08.

Result: `PASS`.

### Loop 4 · feedback distortion

Attack: repeating the user's shorthand as a nationality label would not create an actionable design contract.

Refinement: normalize it into concrete failures: template-like black/gold ornament, repeated amber glow, generic generated iconography, dense AI pitch-board composition, insufficient project-specific rendering identity.

Result: `PASS`.

### Loop 5 · future production drift

Attack: subsequent images could continue cloning the same rejected style because the existing eight images are approved.

Refinement: subsequent production may reuse their information architecture only; replacement art direction requires research, >=3 alternatives, user approval, and representative regeneration before bulk asset work.

Result: `PASS_PENDING_POSTMERGE`.

## 7. Evidence boundary

Verified / observable:
- two generated PNG identities and hashes,
- durable Drive uploads,
- Notion Asset record creation,
- user approval of Visual GDDs,
- user direction to redesign art style,
- repository RED evidence.

Not verified:
- replacement style quality,
- Notion client-side visual geometry,
- Android readability,
- accessibility,
- Godot/runtime match,
- Human comparative evaluation of future alternatives.

No claim above these ceilings is allowed.
