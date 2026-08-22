# RM-TOOL-003 Interoperability Pilot — 2026-08-22

## 목적과 경계

이 문서는 Blacksmith가 이미 보유한 프로젝트 전용 강화 시뮬레이터를 Base `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR`의 **공통 후처리 계약**과 대조한 read-only interoperability evidence다.

- Source commit: `04c52aa37ba10c43b1691ffe6269301f7e065eb0`
- Project simulator: `tools/simulate_enhancement_balance.py`
- Current planning canon: `docs/planning/BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md`
- Product/runtime mutation: **NONE**
- `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 변경: **NONE**
- 현재 강화 수치의 final product balance 승인이나 runtime 연결을 주장하지 않는다.

## Existing Solution First 판정

Blacksmith는 이미 `EnhancementSession` 규칙을 반영하는 프로젝트 전용 simulator를 갖고 있다. 이 simulator는 다음을 스스로 소유한다.

- project data file loading과 fingerprint
- enhancement success / hold / downgrade / destroy rule
- pity, special level, catalyst, skill modifier
- attempt cost와 성장/판매가 계산
- deterministic seed policy
- trial execution과 project-specific scenario 정의

따라서 Base가 동일 규칙을 다시 구현하면 source-of-truth가 둘로 갈라진다.

```text
Blacksmith project simulator
  = project rule owner / run generator

Base RM-TOOL-003 shared analyzer
  = generic distribution / paired-seed / failure-tag / choice-event / goal-seek post-processor
```

**판정: `PROJECT_SIMULATOR_REUSE + BASE_POST_PROCESSOR_ADAPT`.**

## 현재 출력과 공통 계약 매핑

| Blacksmith simulator output | Base RM-TOOL-003 의미 | 처리 방식 |
|---|---|---|
| `input_commit`, `input_sha256` | snapshot provenance | 그대로 snapshot metadata로 전달 |
| `seed_start`, `trials` | seed/run identity | 개별 run export가 필요할 때 동일 seed 정책 유지 |
| `target_reach_rate` | success/failure aggregate | project report에는 유지; 공통 kernel은 개별 run tag에서 재계산 가능 |
| `destruction_rate` | failure tag rate | `DESTROYED` run tag로 투영 가능 |
| attempts / gold spent distribution | numeric metrics | 개별 run의 `attempts`, `gold_spent` metric으로 투영 가능 |
| scenario target/skill | variant/scenario dimension | project adapter가 explicit variant ID로 정규화 |
| project outcome counts | explainability | project-owned detailed report에 유지 |

현재 simulator는 이미 aggregate report를 직접 만든다. Base 공통 kernel의 paired-seed delta와 tail-run trace를 완전히 활용하려면 향후 **동일한 project simulator가 개별 trial record를 optional sidecar로 export**하면 된다. 이 Pilot에서는 그 export를 추가하지 않는다. 제품 구현 gate와 기존 validated simulator를 건드릴 이유가 없기 때문이다.

## 장기 구조

```text
project-authoritative data
→ tools/simulate_enhancement_balance.py
→ optional deterministic trial-record sidecar
→ Base RM-TOOL-003 analyzer
→ generic comparison/report
→ human/GPT review
→ approved project decision
```

Base analyzer 결과가 Blacksmith 수치 정본을 자동 수정해서는 안 된다.

## 현재 balance evidence와의 관계

`BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md`의 planning anchors와 Monte Carlo 근거는 그대로 유지한다. 이 interoperability Pilot은 그 수치를 다시 승인하거나 대체하지 않는다.

- planning/test budget과 final product balance는 분리한다.
- human/player validation이 없으면 재미/긴장감 PASS가 아니다.
- runtime linkage가 막혀 있다면 analyzer 존재가 gate를 해제하지 않는다.

## 판정

1. 새 Blacksmith balance simulator: **REJECT — duplicate owner**.
2. Base가 Blacksmith enhancement rules를 재구현: **REJECT — canon drift risk**.
3. 기존 project simulator + optional record adapter + Base shared post-processor: **ADOPT**.
4. 별도 Balance GUI/Tool Hub surface: **DEFER** — CLI/report 반복 부담이 실제로 증명된 뒤 재검토.

## Evidence ceiling

- `PROJECT_SIMULATOR_EXISTS`
- `INTEROP_CONTRACT_REVIEWED`
- `NEW_TRIAL_EXPORT_NOT_IMPLEMENTED`
- `PRODUCT_RUNTIME_UNCHANGED`
- `FINAL_PRODUCT_BALANCE_NOT_APPROVED`
- `HUMAN_PLAYER_EVIDENCE_NOT_RUN`

Machine-readable mapping: `docs/rm_tool_003_interop_pilot_20260822.json`.
