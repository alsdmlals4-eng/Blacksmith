# Artistry Unbounded Stat Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the obsolete `1~10` artistry contract with a non-negative integer stat that has no fixed design maximum, while preserving grade/affix boundaries, historical traceability, TDD evidence, and the product implementation block.

**Architecture:** The change is planning-contract-only. A failing planning contract is added first, then current canon, machine registries, routers, legacy status, and audit validators are minimally updated to the same semantic contract. Historical `1~10` and `/10` statements remain only in explicitly superseded/history sections. No protected product path is modified.

**Tech Stack:** Markdown canon, JSON registries, Python contract tests/audit tools, GitHub Actions, Google Sheets authority mirror.

## Global Constraints

- Decision ID remains `BS-CRAFT-20260805-01`; this is a refinement, not a third batch approval.
- Active batch remains `R2_BATCH_004 / 2/10`.
- Artistry domain is `NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM`.
- Minimum is `0`; values are integers; decimals are forbidden.
- User-facing display is a decimal raw value such as `예술성 27`; denominators, percentages, stars, and named tiers are forbidden.
- A technical storage limit may exist but must not become a player-facing or content maximum.
- Artistry does not increase combat power by default and is not a universal affix/stat multiplier.
- Crafting grade does not set an artistry maximum; `[전설] / 예술성 3` and `[보통] / 예술성 87` are valid.
- Product implementation remains `BLOCKED`; protected product paths remain unchanged.
- Every change follows `RED → GREEN → REFACTOR` and records observed evidence.

---

### Task 1: Add the failing unbounded-artistry contract

**Files:**
- Create: `tests/test_r2_artistry_unbounded_stat_contract.py`
- Modify: `tests/test_base_v942_planning_first_adoption.py`

**Interfaces:**
- Consumes: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`, current artistry canon, Current Decisions, Current R2 Game Bible, Active Context.
- Produces: machine-readable assertions for the new artistry domain and forbidden current-contract strings.

- [ ] **Step 1: Write the focused failing test**

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CURRENT_FILES = (
    ROOT / "CURRENT_CONFIRMED_DECISIONS.md",
    ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md",
    ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md",
    ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
)


class ArtistryUnboundedStatContractTests(unittest.TestCase):
    def test_registry_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        contract = decisions["BS-CRAFT-20260805-01"]["contract"]
        self.assertEqual("NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM", contract["domain"])
        self.assertEqual(0, contract["minimum"])
        self.assertIsNone(contract["fixed_design_maximum"])
        self.assertFalse(contract["denominator_display_allowed"])
        self.assertFalse(contract["named_tiers_exist"])

    def test_current_authority_uses_raw_values(self) -> None:
        for path in CURRENT_FILES:
            text = path.read_text(encoding="utf-8")
            self.assertIn("예술성 27", text, path.as_posix())
            self.assertIn("고정 설계 최대치 없음", text, path.as_posix())
            self.assertNotIn("예술성 7/10", text, path.as_posix())
            self.assertNotIn("예술성 1~10", text, path.as_posix())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Extend the planning-first test with the new required tokens**

Require `NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM`, `minimum: 0`, `고정 설계 최대치 없음`, and `예술성 27`, while rejecting active `/10` and `INTEGER_1_TO_10` contracts.

- [ ] **Step 3: Commit the RED tests before changing canon**

```bash
git add tests/test_r2_artistry_unbounded_stat_contract.py tests/test_base_v942_planning_first_adoption.py
git commit -m "test: require unbounded artistry stat contract"
```

- [ ] **Step 4: Verify RED through the PR-triggered planning workflow**

Expected: Planning-first validation fails because current Registry and canon still use `INTEGER_1_TO_10`, `예술성 1~10`, and `예술성 7/10`. Base adoption should remain green, proving the failure is the intended missing contract rather than an environment failure.

---

### Task 2: Update current canon and machine registry

**Files:**
- Modify: `docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_THREE_AFFIX_SLOT_ARCHITECTURE_CANON_2026.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`

**Interfaces:**
- Consumes: approved spec `docs/superpowers/specs/2026-08-05-artistry-unbounded-stat-design.md`.
- Produces: one consistent current contract used by all routers and tests.

- [ ] **Step 1: Replace the current artistry canon**

Use this exact contract:

```text
field: artistry
conceptual type: non-negative integer
minimum: 0
fixed design maximum: none
user display: decimal integer without denominator
```

Include `예술성 0` as a valid functional item with negligible aesthetic investment, examples `예술성 27`, `[전설] ... / 예술성 3`, and `[보통] ... / 예술성 87`, plus economic diminishing-return safeguards.

- [ ] **Step 2: Update Current Decisions and Game Bible**

Replace active `1~10`, `/10`, and “예술성 10” wording with:

```text
예술성 0 이상의 정수
고정 설계 최대치 없음
표시: 예술성 27
```

Retain the combat boundary and product block.

- [ ] **Step 3: Update Registry contract**

Set:

```json
{
  "domain": "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
  "minimum": 0,
  "fixed_design_maximum": null,
  "decimals_allowed": false,
  "denominator_display_allowed": false,
  "named_tiers_exist": false,
  "displayed_with_weapon_stats": true,
  "technical_storage_limit_is_content_maximum": false,
  "combat_power_by_default": false,
  "universal_affix_multiplier": false
}
```

Change implementation alignment to `NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM_NO_NAMED_TIERS` and preserve batch `2/10`.

- [ ] **Step 4: Update Active Context and three-affix boundary**

State explicitly that artistry is not an affix slot, grade does not cap it, and raw-value display has no denominator.

- [ ] **Step 5: Run focused tests to reach first GREEN candidate**

```bash
python -m unittest tests.test_r2_artistry_unbounded_stat_contract -v
python tests/test_base_v942_planning_first_adoption.py
```

Expected: both pass locally when available; if the focused file is not invoked by default CI, record standalone status honestly.

---

### Task 3: Update routers, legacy status, and benchmark language

**Files:**
- Modify: `docs/planning/BLACKSMITH_R2_ARTISTRY_MINIMUM_SCALE_PRICE_AFFIX_VISUAL_PRESET_CANON_2026.md`
- Modify: `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`
- Modify: `docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: current contract from Task 2.
- Produces: safe cold-start routing and explicit history classification.

- [ ] **Step 1: Mark the `1~10` artistry scale as superseded history**

The legacy registry must retain:

```json
{
  "source": "BS-CRAFT-20260805-01 initial bounded-stat draft",
  "model": "INTEGER_1_TO_10_NO_NAMED_TIERS",
  "status": "SUPERSEDED",
  "replacement": "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM"
}
```

- [ ] **Step 2: Update cold-start documents**

Every active entry point must show `예술성 0 이상의 정수 / 고정 설계 최대치 없음 / 예술성 27`, not `/10`.

- [ ] **Step 3: Refine the benchmark record**

State that raw numeric stat display is adopted, a universal quality multiplier is rejected, and no benchmark is being used to justify a fixed maximum.

- [ ] **Step 4: Keep historical strings only under explicit `[대체됨]` or `SUPERSEDED` headings**

Do not delete the old model from history. Do not allow routers to present it as active.

---

### Task 4: Align validators and complete REFACTOR

**Files:**
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tests/test_r2_customer_disclosure_batch_003.py`
- Modify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: current canon and legacy registry.
- Produces: CI contracts that reject future reintroduction of a fixed artistry maximum.

- [ ] **Step 1: Replace bounded artistry assertions**

Require the new Registry domain, `minimum == 0`, `fixed_design_maximum is None`, and raw display.

- [ ] **Step 2: Add adversarial guards**

Reject current claims matching:

```text
예술성 1~10
예술성 <number>/10
INTEGER_1_TO_10 as current artistry model
예술성 10 = 최고치
```

Allow them only in status-marked historical/spec sections.

- [ ] **Step 3: Preserve unrelated audit coverage**

Do not remove Base mapping, broken-reference detection, three-affix checks, protected runtime paths, historical forging regression, PR #81 boundary, batch/TDD governance, or product-block checks.

- [ ] **Step 4: REFACTOR duplicate active wording**

Ensure current documents use one canonical phrase: `NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM` and Korean explanation `0 이상의 정수 / 고정 설계 최대치 없음`.

---

### Task 5: Exact-head verification, Sheet synchronization, and PR evidence

**Files:**
- Metadata only: Draft PR `#106`
- Google Sheet: `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`

**Interfaces:**
- Consumes: final repository HEAD after Tasks 1–4.
- Produces: exact-head CI evidence and same-ID authority readback.

- [ ] **Step 1: Run exact-head workflows**

Verify:

```text
Planning-first adoption: PASS
Base v9 adoption: PASS
Python full contracts: PASS
Godot 4.7.1 headless: PASS
```

Record any focused test not directly invoked by default CI as `NOT_RUN`, not PASS.

- [ ] **Step 2: Verify change boundaries**

Confirm protected product paths remain unchanged and review comments/threads are zero or resolved.

- [ ] **Step 3: Update Google Sheet using the same Decision ID**

Update existing `BS-CRAFT-20260805-01` rows instead of creating a third batch decision. Record the final exact HEAD, RED and GREEN evidence, superseded `1~10` contract, and product block.

- [ ] **Step 4: Read back five authority areas**

```text
00_프로젝트_허브!H2:J2
02_현재_확정결정
04_누락_충돌_감사
05_GDD_요약
99_변경이력
```

All must show Decision `BS-CRAFT-20260805-01`, batch `2/10`, final HEAD, and exact-head validation.

- [ ] **Step 5: Update PR #106 body**

Replace obsolete `/10` wording, document the current unbounded contract, TDD RED/GREEN evidence, changed-file count, product-path count, review state, and Sheet readback.

- [ ] **Step 6: Keep PR Draft and unmerged**

Do not merge without explicit user approval or a separately approved early-checkpoint decision.
