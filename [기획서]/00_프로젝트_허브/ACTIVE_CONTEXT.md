# [현재 정본] Active Context

<!-- BS_OPS_20260811_03_PHASE_C_LIVE_CONTINUATION -->
> **PLANNING_COMPLETE / BS-OPS-20260811-03 / PHASE_C_EXISTING_APPROVED_CANON / LOCAL_RUNTIME_GATE_OPEN**
>
> `STATE_OBSERVED_AT_MAIN: 8e9a9cf8b0b053b5bfc5667b9a1070d3b45c3486`
>
> `RESUME_RULE: FETCH_LATEST_MAIN_BEFORE_USE`
>
> `P0_LOCAL_EXECUTOR_BOOTSTRAP: PASS`
>
> `P1_AUTHORITY_AND_CURRENT_STATE_READBACK: PASS`
>
> `PERSISTENT_MUTATION_GATE: OPEN`
>
> `PHASE_C_NEXT_PACKAGE: P2_FOUNDATION_DATA_AND_STATE_CONTRACTS`
>
> `CURRENT_EXECUTION_SURFACE: REUSE_LIVE_DEDICATED_CODEX_WHEN_FRESH`
>
> `BOOTSTRAP_REENTRY_POLICY: ONLY_WHEN_RUNTIME_ENVELOPE_EXPIRED_OR_RECOVERY_REQUIRED`
>
> `SHEET_SYNC_WRITE_POLICY: TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE`
>
> `PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON`
>
> `TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED`
>
> `IMAGE_GENERATION: DEFERRED_BY_USER`
>
> `P1_BS_CT_06_TAXONOMY_AMBIGUITY: DEFERRED`
>
> 현재 Blacksmith 전용 live envelope는 PR #157 receipt에서 Godot 4.7.1, Godot-AI 3.1.4, HTTP 8006, WS 9506, dedicated `CODEX_HOME`, exact Blacksmith session 1개, `editor_state`, hierarchy, project settings까지 PASS했다. 동일 세션이 fresh한 동안 Codex 내부 작업은 PowerShell bootstrap 재실행 없이 이어간다. 세션/포트/process identity가 만료되거나 복구가 필요할 때만 전용 bootstrap으로 재진입한다.

## 현재 기준선

```yaml
CURRENT_STAGE: PHASE_C_IMPLEMENTATION
WORK_MODE: BUILD_REVIEW
STATE_OBSERVED_AT_MAIN: 8e9a9cf8b0b053b5bfc5667b9a1070d3b45c3486
BASE_CURRENT_MAIN_OBSERVED_AT_HANDOFF: 449b83c6f1afdf191327a52a8e71d11b4fba7eb3
BASE_SAME_GOAL_DEDICATED_ENV_AUTHORITY: 6d2feba2bc49fda2d8d273248b55087853615d5d
PROJECT_BASE_ADAPTER_PIN: 2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b
WORK_INSTRUCTION: V4_5_R2_CURRENT_CANON
PROJECT_LOCAL_PATH: C:\Users\user\Documents\GitHub\Ninza\Blacksmith
GODOT_PROJECT_PATH: C:/Users/user/Documents/GitHub/Ninza/Blacksmith
PLANNING_COMPLETE: USER_DECLARED
R3_R7_DESIGN_ACTIVE: true
R3_R7_PLANNING_BATCH: CLOSED_AT_9_OF_10
R3_R7_APPROVAL_COUNTER: 9/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09
R3_R7_RESUME_LOCATOR: GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED
R2_CHECKPOINT_005: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: R2_BATCH_005_CLOSED_10_OF_10
R2_BATCH_006: R2_BATCH_006_APPROVED_10_OF_10
TASK2: TASK2_MAIN_MERGED
POSTMERGE_CLOSURE: POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE
P0_LOCAL_EXECUTOR_BOOTSTRAP: PASS
P1_AUTHORITY_AND_CURRENT_STATE_READBACK: PASS
PERSISTENT_MUTATION_GATE: OPEN
PHASE_C_NEXT_PACKAGE: P2_FOUNDATION_DATA_AND_STATE_CONTRACTS
CURRENT_EXECUTION_SURFACE: REUSE_LIVE_DEDICATED_CODEX_WHEN_FRESH
BOOTSTRAP_REENTRY_POLICY: ONLY_WHEN_RUNTIME_ENVELOPE_EXPIRED_OR_RECOVERY_REQUIRED
SHEET_SYNC_WRITE_POLICY: TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE
PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON
NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED_BEYOND_EXISTING_APPROVED_CANON
TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED
IMAGE_GENERATION: DEFERRED_BY_USER
HUMAN_PLAYTEST: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY: NOT_RUN
PR81: PR81_REFERENCE_ONLY_DO_NOT_MERGE
```

현재 R3–R7 승인 카운터: `9/10`.

`PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md` (`v4.5 r2`)와 project binding `BS-OPS-20260811-01`은 계속 현재 작업지시 권위다. `BS-OPS-20260811-02` pre-work research Gate와 `BS-OPS-20260811-03` Phase C/runtime binding을 그 위에 적용한다.

`BASE_CURRENT_MAIN_OBSERVED_AT_HANDOFF`와 `PROJECT_BASE_ADAPTER_PIN`은 서로 다른 증거다. Base remote가 전진해도 project pin을 자동 승격하지 않는다. 새 세션은 이 파일의 관측 SHA를 latest truth로 가정하지 않고 `RESUME_RULE`대로 GitHub main과 open PR을 먼저 재조회한다.

## 현재 승인 콘텐츠 구현 입력

R3–R7 기획은 승인된 9건에서 닫혔다. 다음 ID는 current implementation input이며 세부 책임은 각 canon 파일과 `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`이 소유한다.

```text
R3_R7_DESIGN_ACTIVE
BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN
BS-CONTENT-20260811-02 / ADVENTURER_02 / TOREN_MARCH
BS-CONTENT-20260811-03 / SOLDIER_01 / MAREK_OLDEN
BS-CONTENT-20260811-04 / COLLECTOR_01 / ERSA_ROEN
BS-CONTENT-20260811-05 / GLADIATOR_01 / CASSIA_BELLAN
BS-CONTENT-20260811-06 / NOBLE_01 / CEREMONIAL_NOBLE
BS-CONTENT-20260811-07 / SOLDIER_02 / LIANA_BERG
BS-CONTENT-20260811-08 / COLLECTOR_02 / SEDRIC_VAEL
BS-CONTENT-20260811-09 / GLADIATOR_02 / KYLE_VAREN
```

대표 locator:
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
- 이후 D02–D09도 `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`의 current path를 따른다.

보호 경계:
- 같은 UID 작품 생애·손상·복원·소유·provenance를 보존한다.
- replacement는 old UID/history를 보존하고 distinct new UID로 시작한다.
- 직접 탐험/전투/전술/투기장/전시관/박물관/가문 경영으로 범위를 확장하지 않는다.
- 새 hidden total score, rarity/prestige/fame/lineage total score를 편의상 만들지 않는다.
- 최고 강화·최고 Artistry·가장 오래된 작품·가장 많은 Chronicle을 보편적 자동 정답으로 만들지 않는다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`를 임의 해결하지 않는다.
- `BS-UX-20260805-01` 모바일 고객 카드의 progressive disclosure와 설명 가능한 판단 계약을 유지한다.

## Phase C 다음 실행

```text
P2_FOUNDATION_DATA_AND_STATE_CONTRACTS
→ Existing Solution First inventory
→ 가장 작은 공통 foundation slice 1개 선택
→ semantic RED
→ 최소 GREEN
→ affected regression / GUT / Godot 4.7.1 / HiGodot
→ exact-head PR
→ postmerge readback
```

새 substantive gameplay Decision이 필요하면 그 지점만 `USER_DECISION_REQUIRED`로 격리한다. 이미 승인된 P2 범위는 재승인을 요구하지 않는다. Task3는 별도 승인 없이 시작하지 않는다.

## 현재 Handoff / Learning Closure

```yaml
LRN-BS-HANDOFF-001:
  classification: SPLIT
  problem: PR157 이후 live runtime은 PASS인데 current router가 P0-required 상태에 머무를 수 있음
  project_application: CURRENT_CONFIRMED_DECISIONS + ACTIVE_CONTEXT + DEVELOPMENT_GATES + START_HERE + ROADMAP + AGENTS + machine regression
  base_existing_solution: REUSE BCP-2026-013 / BCP-2026-016
LRN-BS-SHEET-001:
  classification: SPLIT
  problem: broad Sheet replacement가 historical PR156 SHA까지 바꾼 사례
  project_application: TARGETED_RANGES_ONLY + live/history landmark readback
  base_existing_solution: REUSE BCP-2026-016
LRN-BS-RUNTIME-001:
  classification: BASE_CANDIDATE_REUSE
  problem: retained godot-ai / stale PID-session-port authority
  project_application: PR157 merged runtime hardening + live receipt
  base_existing_solution: REUSE BCP-2026-015
LRN-BS-EXEC-SURFACE-001:
  classification: SPLIT_REUSE
  problem: valid live dedicated session에서 불필요한 bootstrap 반복
  project_application: live Codex reuse + bounded re-entry policy
  base_existing_solution: REUSE existing dedicated-runtime/handoff owners
```

새 broad project Skill은 만들지 않는다. 기존 current-state owner와 `tests/check_project_core_alignment_current.py`에 흡수한다.

## 먼저 읽을 파일

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. 이 `ACTIVE_CONTEXT.md`
4. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
5. `[기획서]/00_프로젝트_허브/START_HERE.md`
6. `[기획서]/00_프로젝트_허브/ROADMAP.md`
7. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
8. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
9. D01–D09 분야별 canon
10. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
11. 실제 code/data/Scene/tests
12. Google Sheet `00_프로젝트_허브`, `01_작업순서`, `02_현재_확정결정`, `04_누락_충돌_감사`, `10_제품방향`, `13_주요인물`, `50_메인콘텐츠`, `99_변경이력`

## 역사 호환 앵커

아래 문자열은 current action을 지시하지 않고 과거 R2/R3 폐쇄와 machine consumer를 찾기 위한 compatibility locator다.

```text
R2 체크포인트 004
R2_CHECKPOINT_004
R2_CHECKPOINT_005
R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005_CLOSED_10_OF_10
R2_BATCH_006_APPROVED_10_OF_10
MERGED_PR109
MERGED_PR120_MAIN_CANON
VERTICAL_SLICE_IMPLEMENTATION_APPROVED
BS-CRAFT-20260805-02
BS-UX-20260805-01
TASK2_MAIN_MERGED
POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE
HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED
HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED
7a46fa38586a42f268cd0432744203049649ddd5
HISTORICAL_PRODUCT_IMPLEMENTATION: 제품 구현: `BLOCKED`
```

Task2 PROVE/PUBLISH, PR #139/#140/#141, R3 D01–D09의 상세 과거 실행 로그는 해당 Decision/canon/receipt/GitHub history에서 읽는다. 이 Active Context는 live continuation router만 소유한다.