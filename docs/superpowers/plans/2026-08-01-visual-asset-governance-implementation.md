# Blacksmith Visual Asset Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Apply review gates task-by-task.
>
> **Execution Gate:** 사용자 `기획 완료`와 `검수 완료` 전 제품 에셋 제작·통합 금지.

**Goal:** 승인된 다크 포지·모닥·화면 문법을 제품 에셋으로 안전하게 전환하고, Placeholder·출처·권리·버전·검수·실기기 증거를 추적한다.

**Authority:** `BS-VISUAL-ASSET-GOV-20260801-01`.

**Architecture:** GitHub Asset Manifest와 License Ledger가 상세 정본이고 Sheet 70~72는 작업 Queue·검수 요약이다. 모든 파일은 Asset ID와 License ID로 연결한다. 에셋은 상태 단계를 건너뛰지 않으며 실제 화면·기기 증거 전 RELEASE_APPROVED가 될 수 없다.

## File Map

### Create or maintain

- `docs/assets/BLACKSMITH_ASSET_MANIFEST.md`
- `docs/assets/BLACKSMITH_LICENSE_LEDGER.md`
- `docs/assets/data/blacksmith_asset_manifest.json`
- `docs/assets/data/blacksmith_license_ledger.json`
- `docs/assets/reviews/`
- `docs/assets/screenshots/baselines/`
- `tools/validate_asset_manifest.py`
- `tools/validate_license_ledger.py`
- `tests/test_asset_manifest.py`
- `tests/test_license_ledger.py`
- `tests/test_visual_placeholder_contract.py`

### Modify later

- final `assets/` runtime paths
- Theme/UI scenes
- Sheet tabs 70·71·72
- `.github/workflows/godot-validation.yml`
- `tests/README.md`

---

### Task 1: Machine-readable Manifest and License schemas

- [ ] Write failing tests for required fields, unique IDs, checksum format, valid status transitions and license linkage.
- [ ] Create JSON manifests matching the approved Markdown schemas.
- [ ] Register the three current direction entries as non-shipping references.
- [ ] Reject runtime asset entries without a valid License ID.
- [ ] Commit: `docs: establish machine-readable asset and license ledgers`

### Task 2: Placeholder contract validator

- [ ] Encode the approved NOT_CANON list.
- [ ] Scan planning JSON, implementation goals and product data for unapproved promotion markers.
- [ ] Allow placeholder terms only when tagged `PLACEHOLDER`, `NOT_CANON`, `REFERENCE_ONLY` or historical.
- [ ] Fail when a product implementation manifest lists level, blue gem, achievements, shop, special crafting, 128/150, direct market/arena or image-only numeric values without a Decision ID.
- [ ] Commit: `test: block visual placeholders from becoming product canon`

### Task 3: Asset production queue

- [ ] Create production candidates in priority order:
  1. app logo and main background
  2. forge hub background
  3. equipment presentation frames
  4. Modak expression set
  5. core UI icons
  6. customer portraits
  7. result backgrounds/effects
- [ ] Every queue item includes intended screen, logical size, source plan, license status and review owner.
- [ ] Do not create multiple decorative variants before the first vertical-slice set passes screen review.
- [ ] Commit: `docs: define vertical-slice asset production queue`

### Task 4: Modak production candidate

- [ ] Produce one consistent base model and seven expressions.
- [ ] Create hub 160×160, work/customer 112×112 and result/warning 96×96 logical variants or scalable source.
- [ ] Verify bright yellow/gold/orange body, dark detail ≤15%, no charcoal shell.
- [ ] Test transparent edges, bloom, downscale readability and silhouette.
- [ ] Register source, generation/edit history, checksum and rights review.
- [ ] Keep status at PRODUCTION_CANDIDATE until UI review.
- [ ] Commit: `art: register Modak production candidate set`

### Task 5: Core screen asset candidates

- [ ] Create only assets required for the 12 screenshot baseline states.
- [ ] Keep equipment central and avoid environmental contrast competing with item silhouette.
- [ ] Separate background, equipment, character, UI chrome, icon and effects layers.
- [ ] Register each runtime candidate and source file lineage.
- [ ] Commit: `art: register vertical-slice visual asset candidates`

### Task 6: License and source verification

- [ ] Review fonts, icons, audio, open-source templates and purchased assets individually.
- [ ] Store proof references outside runtime asset folders.
- [ ] Generate attribution obligations list.
- [ ] Mark ambiguous or unavailable terms BLOCKED; replace rather than assume.
- [ ] Verify AI-generated candidate terms and provenance before product use.
- [ ] Commit: `docs: verify vertical-slice asset licenses and attribution`

### Task 7: Screenshot baseline capture

- [ ] Integrate candidates only after SOURCE_AND_LICENSE_VERIFIED.
- [ ] Capture all 12 baseline screens at 720×1280 and 1080×2400.
- [ ] Capture safe inset, text scale and reduced-motion variants.
- [ ] Store screenshot metadata with commit, Scene, state fixture and Asset IDs.
- [ ] Commit: `test: capture Blacksmith visual screenshot baselines`

### Task 8: Adversarial visual review

- [ ] Review information hierarchy, equipment focus, contrast, color-independent states, 48dp targets, safe area, Korean strings, Modak overlap and placeholder leakage.
- [ ] Record P0/P1/P2 findings per screenshot.
- [ ] Iterate until P0 and P1 are zero.
- [ ] Mark candidate VISUAL_REVIEW_PASS only with linked evidence.
- [ ] Commit: `review: close vertical-slice visual findings`

### Task 9: Runtime and device verification

- [ ] Integrate approved assets in Theme and reusable Scenes.
- [ ] Verify Android safe area, memory, import settings, texture compression and frame pacing.
- [ ] Verify Modak animations do not delay input or obscure results.
- [ ] Record device evidence; keep unsupported devices explicit.
- [ ] Promote to DEVICE_VERIFIED only after actual execution.
- [ ] Commit: `test: verify visual assets on Android devices`

### Task 10: Release approval and CI

- [ ] Add CI:

```bash
python tools/validate_asset_manifest.py
python tools/validate_license_ledger.py
python -m unittest tests/test_asset_manifest.py tests/test_license_ledger.py tests/test_visual_placeholder_contract.py
```

- [ ] Fail release packaging for unregistered runtime assets, invalid license states or placeholder leakage.
- [ ] Generate attribution file from verified ledger entries.
- [ ] Promote only linked, reviewed, device-verified assets to RELEASE_APPROVED.
- [ ] Commit: `ci: enforce asset provenance license and visual gates`

## Self-review

- Direction vs final asset separation: explicit.
- Placeholder leakage: blocked.
- Manifest and License schemas: exact.
- Modak size/overlap rules: actionable.
- Screenshot/device/human evidence: separate.
- Runtime execution authorization: blocked.

```text
PLAN_STATUS: COMPLETE
IMPLEMENTATION_EXECUTION: BLOCKED
```
