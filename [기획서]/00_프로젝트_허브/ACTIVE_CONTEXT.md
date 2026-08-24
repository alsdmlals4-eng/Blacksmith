# [현재 정본] Active Context

<!-- BS_CURRENT_PRIORITY_OVERLAY_20260820 -->
> **CURRENT_PRIORITY_OVERLAY / 2026-08-20 PLANNING AUTHORITY**
>
> 현재 Blacksmith 작업 진입점은 `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`와 `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`다. 2026-08-11 Phase-C 진입 기록은 역사 증거이며 현재 제품 구현 승인으로 재사용하지 않는다.
>
> ```yaml
> CURRENT_STAGE: PLANNING_REOPENED_CURRENT_PRIORITY_OVERLAY
> CURRENT_AUTHORITY: CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md
> AUTHORITY_INDEX: docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md
> WORK_MODE: PLAN
> PRODUCT_IMPLEMENTATION: BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION
> HUMAN_PLAYER_VALIDATION: NOT_RUN
> RUNTIME_MUTATION_FROM_HISTORICAL_PHASE_C: FORBIDDEN
> ```
>
> 최신 제품 계층은 `강화의 긴장감 + DDD`가 PRIMARY CORE이고, 작품 UID·생애 / 정밀제작 / 고객·세계 생애주기 / 경제·하루 작업량은 이를 지지하는 SUPPORT다. CURRENT/MAX 내구도·파괴·수리·checkpoint·+0~+100 test budget은 2026-08-20 개별 Canon을 따르고, 일반 강화/수리 Resource Supply는 2026-08-24 `BS-RESOURCE-20260824-18`, 후기 HIGH/MASTERY 일반 CURRENT 수리 경제는 `BS-REPAIR-20260824-19`, MAX 생애 1회 부분 대수선은 `BS-OVERHAUL-20260824-20`, DESTROYED 기록·추모·후계 UX는 `BS-DESTRUCTION-20260824-21`, +100 최대 강화 완료 payoff는 `BS-MAX-20260824-22` Canon을 따른다.
>
> 다음 제품 구현은 새 `기획 완료` 선언과 해당 구현 Gate가 열리기 전 시작하지 않는다. 과거 Task1/Task2 구현과 runtime receipt는 구현 사실/역사 증거로 보존하지만 이 Gate를 자동으로 열지 않는다.

<!-- BS_OPS_20260811_03_PHASE_C_ENTRY_HISTORICAL -->
> **HISTORICAL / BS-OPS-20260811-03 / PHASE_B_FINAL_REVIEW_COMPLETE / PHASE_C_ENTRY_APPROVED_AT_THE_TIME**
>
> `ASSUME_PREVIOUS_POWERSHELL_CLOSED` / `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` / `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`
>
> `BASE_DEDICATED_ENV_MAIN_OBSERVED: 6d2feba2bc49fda2d8d273248b55087853615d5d`
>
> 2026-08-11 당시 사용자가 `기획 완료`를 명시했고, R3–R7 기획 배치를 승인된 9/10에서 닫아 당시 승인된 정본 구현만 Phase C로 진입시켰다. 이 기록은 2026-08-20 `CURRENT_PRIORITY_OVERLAY`에 의해 현재 구현 Gate로서는 대체되었다.
>
> `HISTORICAL_PLANNING_COMPLETE: USER_DECLARED` / `R3_R7_PLANNING_BATCH: CLOSED_AT_9_OF_10` / `PHASE_B_FINAL_REVIEW: COMPLETE`
>
> `HISTORICAL_PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON`
>
> `TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED`
>
> `P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING`
>
> `IMAGE_GENERATION: DEFERRED_BY_USER`
>
> 전용 로컬 실행환경: self-contained Godot 4.7.1 (`_sc_`) → HiGodot HTTP `8006` / WS `9506` → `C:\Users\user\.codex-blacksmith` → exact Blacksmith 경로에서 Codex. 포트/process 존재는 readiness PASS가 아니며 Codex 내부 fresh HiGodot receipt 전 persistent mutation 금지.


<!-- R3_R7_PLANNING_BATCH_HISTORICAL_CLOSED_AT_9_OF_10 -->
> **HISTORICAL_R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-09 / GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED / PLANNING_ONLY**
>
> 이 문서는 현재 상태와 다음 읽기 순서를 연결하는 압축 라우터다. 세부 Decision·과거 단계·실행 로그는 책임 원본에서 읽는다.

- 갱신 기준: `2026-08-11 KST`
- Blacksmith current main observed at Decision 09 start: `80b35b9fc914853428e991c4130edc87dd260083`
- `BASE_CURRENT_MAIN_OBSERVED`: `6d2feba2bc49fda2d8d273248b55087853615d5d`
- `PROJECT_BASE_ADAPTER_PIN`: `2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b`
- 현재 R3–R7 승인 카운터: `9/10`
- Base current main 관측값과 프로젝트가 채택한 Base adapter pin은 서로 다른 증거다. 새 Base main 관측만으로 프로젝트 pin을 자동 승격하지 않는다.

```yaml
HISTORICAL_STAGE: PHASE_C_IMPLEMENTATION_ENTRY
R2_BASELINE: R2_BATCH_006_MAIN_CANON
R2_CHECKPOINT_005: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: R2_BATCH_005_CLOSED_10_OF_10
R2_BATCH_005_MERGE: MERGED_PR109_MAIN_CANON
R2_BATCH_006: R2_BATCH_006_APPROVED_10_OF_10
R2_BATCH_006_MERGE: MERGED_PR120_MAIN_CANON
R3_R7_APPROVAL_COUNTER: 9/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09
PRE_WORK_RESEARCH_DECISION: BS-OPS-20260811-02
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
R3_R7_RESUME_LOCATOR: GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED
VERTICAL_SLICE_IMPLEMENTATION: APPROVED_TASK2_COMPLETE
VERTICAL_SLICE_IMPLEMENTATION_EVIDENCE: VERTICAL_SLICE_IMPLEMENTATION_APPROVED
TASK2: TASK2_MAIN_MERGED
POSTMERGE_CLOSURE: POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE
HISTORICAL_WORK_MODE: BUILD_REVIEW
HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED
HISTORICAL_PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON
NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED_BEYOND_EXISTING_APPROVED_CANON
HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED
TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED
HUMAN_PLAYTEST: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY: NOT_RUN
PR81: PR81_REFERENCE_ONLY_DO_NOT_MERGE
```

## 현재 완료 상태

- R0–R2 기획 기반과 R2 Batch 006은 main canon이다.
- Task 1 UID·SaveEnvelope는 main 정본으로 병합됐다.
- Task 2 MainMenu → BlacksmithApp → Workshop 시작 경로와 `project.godot application/run/main_scene` 전환은 HiGodot provenance를 거쳐 병합됐다.
- `BS-HIGODOT-EXEC-20260808-01` Task2 제품 provenance:
  - PROVE input: `02420ebd3bcdd86776c4ab70824738aa4071a168`
  - PROVE run: `31341840236`
  - provenance artifact: `9046072682`
  - serialized publish commit: `8afb9a439df46eec3568a75d7f2536b89e1edaba`
  - approved PR branch head: `345cf339e2af754d447099dd8e1b278b80b849d5`
  - Task2 merge main: `a61a0bceec4254c4b78350980275cc9a903f9042`
- 후속 CI 복구는 제품 직렬화 bytes를 바꾸지 않았다.
  - PR #139 merge main: `7ccee408cf5c936ae9302a986fa0c786e0247078`
  - PR #140 merge/current technical baseline before handoff refresh: `fa9595b2df95897c915331a1cb5d9b1a583611f0`
  - PR #141 handoff refresh main: `68540e6cd288aff138b1ea4c5b1feeb9e0653947`
  - Full validation: run `31357963490` SUCCESS
  - Live-Editor Pilot: run `31357963734` attempt 2 SUCCESS
- 역사 POC 회귀 증거는 현재 제품 PASS가 아니다: `POC v0.6.4 · main · 2026.07.23.1 / 제작 모델 7건 / 통합 6건 / HISTORICAL_EVIDENCE_ONLY`.
- 역사 POC 강화 데이터 소유권 locator: `enhancement_balance.json`은 failure/risk를, `enhancement_milestones.json`은 milestone 정의를 소유한다. 이 문자열은 구형 데이터의 책임 위치를 보존하는 호환 앵커일 뿐 현재 R3 제품 밸런스 확정이나 제품 구현 승인을 뜻하지 않는다.

## 역사 snapshot — `기획 완료` 직전 R3–R7 9/10 기획 상태

`BS-CONTENT-20260811-01`~`08`은 승인 완료 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-09`이다.

```text
GLADIATOR_02 / KYLE_VAREN
→ 기존 구형 PoC 계승 고객을 두 번째 Gladiator-family 상세 콘텐츠로 승격
→ VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION
→ 실제 prior Kyle item record 확인
→ comeback 목적 + 현재 필요한 장비 역할 공개
→ 과거 작품 UID의 현재 상태·실제 생애 증거 확인
→ hard serviceability / eligibility gate
→ 가능한 경우 KEEP_IN_SERVICE vs RETIRE_AND_REPLACE 비교
→ 플레이어 결정
→ 비직접 comeback/arena world event 해결
→ VETERAN_RETURN_STATE
 + EQUIPMENT_CONTINUITY_STATE
 + ITEM_UID_LINEAGE_STATE
→ 실제 원인 2~4개
→ 주 후속 행동 1개
```

- Cassia/Gladiator01의 current-match arena fit·equipment contribution 책임을 보존한다.
- Noble01/기존 repair owner의 treatment-depth 책임을 보존한다.
- keep path는 같은 UID를 유지한다.
- replacement는 old UID/history를 보존하고 new UID로 시작하며 history/progression을 복사하지 않는다.
- 오래된 작품·새 작품·최고 강화·최고 Artistry·가장 많은 Chronicle이 자동 정답이 아니다.
- sentiment/veteran/lineage 총점을 추가하지 않는다.
- legacy `gladiator_kyle / iron_sword` fixed data와 score formula는 historical non-authoritative fixture다.
- 직접 arena combat·roster/guild·training/injury management·betting·baseline permadeath를 추가하지 않는다.
- comeback/replacement 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`를 이번 Decision에서 재정의하지 않는다.

책임 원본:

- `docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md`
- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`

이 문장은 `기획 완료` 직전 Decision09의 **역사적 기획 재개 경계**다. 현재 구현 Gate는 상단 `CURRENT_PRIORITY_OVERLAY`가 소유하며, 새 `기획 완료` 선언 전 제품 구현은 차단되고 Task3도 별도 승인 대상이다.

## 현재 권위와 보호 경계

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
3. `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`
4. 2026-08-20/24 분야별 Canon
5. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장
6. R2/R3 Game Bible·과거 PoC·구형 data/runtime — 역사/비교 증거
7. 이 문서와 `START_HERE.md`, `DEVELOPMENT_GATES.md`, `ROADMAP.md`
8. 실제 code/data/Scene/tests — 구현 현실
9. Google Sheet — `MIGRATION_ONLY_UNTIL_REMOVAL` compatibility 자료

불변 보호:

- PR #81 전체 병합 금지.
- 일반 제품 구현은 `BLOCKED`.
- Task2 완료나 R3–R7 기획 재개를 Task3 구현 승인으로 해석하지 않는다.
- `BS-CONTENT-20260811-01`은 직접 전투·탐험 미니게임을 추가하지 않는다.
- `BS-CONTENT-20260811-02`는 직접 이동·지도 경로 선택·실시간 생존 조작을 추가하지 않는다.
- `BS-CONTENT-20260811-02`는 새 신뢰성·휴대성·수리 용이성 원수치를 만들지 않는다.
- `BS-CONTENT-20260811-02`는 자동 매일 내구도 감소·루틴 수리세를 만들지 않는다.
- `BS-CONTENT-20260811-03`은 소량 주문에서도 개별 UID·비용·결과를 보존하고 공장·전술·실시간 병참으로 확장하지 않는다.
- `BS-CONTENT-20260811-04`는 희귀도/위신/수집가/전시 총점과 Chronicle 개수 최적화를 만들지 않는다.
- `BS-CONTENT-20260811-04`는 전시 횟수만으로 예술성 또는 Chronicle을 자동 성장시키지 않는다.
- `BS-CONTENT-20260811-05`는 직접 투기장 전투·팀/길드 경영·배팅·불투명 투기장 총점을 추가하지 않는다.
- `BS-CONTENT-20260811-05`는 경기 승패와 작품 기여를 분리하고 경기 반복으로 예술성 또는 Chronicle을 자동 성장시키지 않는다.
- `BS-CONTENT-20260811-06`은 최대 복원·최고 Artistry·가문 위신/진품성 총점 자동 정답을 만들지 않는다.
- `BS-CONTENT-20260811-06`은 의미 있는 과거 생애 기록을 지우거나 복원/의식 반복으로 예술성·Chronicle을 자동 성장시키지 않는다.
- `BS-CONTENT-20260811-07`은 Marek의 소량 표준화와 Cassia의 arena contribution 책임을 침범하지 않는다.
- `BS-CONTENT-20260811-07`은 직접 전술전투·부대 이동/대형·실시간 병참·사상자 micromanagement·baseline Liana permadeath를 추가하지 않는다.
- `BS-CONTENT-20260811-07`은 command/hero/leadership/mission-fit 총점, 최고 방어/강화 자동 정답, 작품 단독 인과, 임무 반복 Artistry/Chronicle 파밍을 만들지 않는다.
- 같은 UID의 작품 생애를 유지한다.
- 모든 개인 일정에 고정 3일 결과·4일 재방문을 재도입하지 않는다.
- 사람 플레이테스트·Android 실기기·접근성은 실제 실행 전 `NOT_RUN`.
- HiGodot은 승인된 Godot persistent authoring 권위, GUT 9.7.1은 GDScript test 권위, Hera는 enabled non-authoritative / `AUTHORITY_NONE`이다.
- `BS-CONTENT-20260811-08`은 Ersa 전시·Noble01 처치 책임을 침범하지 않고, 숨은 archive/provenance 총점·기록 조작·museum 관리·same-UID 훼손·accession farming을 금지한다.

## 승인 Decision 호환 인덱스

아래 표기는 Active Context가 도메인 본책을 복제하기 위한 것이 아니라 재개 locator다. 상세 내용은 Current Decisions와 각 Registry가 책임진다.

```text
BS-CRAFT-20260805-02 / R2_BATCH_005_1_OF_10
BS-CUSTOMER-20260805-01 / R2_BATCH_005_2_OF_10
BS-UX-20260805-01 / R2_BATCH_005_3_OF_10
BS-CUSTOMER-20260806-01 / R2_BATCH_005_4_OF_10
BS-ITEM-20260806-01 / R2_BATCH_005_5_OF_10
BS-ITEM-20260806-02 / R2_BATCH_005_6_OF_10
BS-ITEM-20260806-03 / R2_BATCH_005_7_OF_10
BS-ITEM-20260806-04 / R2_BATCH_005_8_OF_10
BS-ITEM-20260806-05 / R2_BATCH_005_9_OF_10
BS-ITEM-20260806-06 / R2_BATCH_005_10_OF_10
BS-CONTENT-20260811-01 / R3_R7_1_OF_10
BS-CONTENT-20260811-02 / R3_R7_2_OF_10
BS-CONTENT-20260811-03 / R3_R7_3_OF_10
BS-CONTENT-20260811-04 / R3_R7_4_OF_10
BS-CONTENT-20260811-05 / R3_R7_5_OF_10
BS-CONTENT-20260811-06 / R3_R7_6_OF_10
BS-CONTENT-20260811-07 / R3_R7_7_OF_10
BS-CONTENT-20260811-08 / R3_R7_8_OF_10
BS-CONTENT-20260811-09 / R3_R7_9_OF_10
BS-OPS-20260811-02 / PRE_WORK_RESEARCH_GATE
BS-RESOURCE-20260824-18 / RESOURCE_SUPPLY_CANON
BS-REPAIR-20260824-19 / LATE_REPAIR_ECONOMY_CANON
BS-OVERHAUL-20260824-20 / MAX_OVERHAUL_CANON
BS-DESTRUCTION-20260824-21 / DESTRUCTION_UX_CANON
BS-MAX-20260824-22 / MAX_LEVEL_PAYOFF_CANON
```

## 불변 체크포인트 호환 이력

- R2 체크포인트 004·005와 Batch 006은 삭제 금지 이력이며 R3–R7 설계의 상속 기반이다.
- `R2_CHECKPOINT_004 / MERGED_PR106 / MAIN_CANON`
- checkpoint 004 closure squash merge: `7a46fa38586a42f268cd0432744203049649ddd5`
- Batch 006 merge main: `a8a94343c78a68bf7bb14b411e7741f43b257138`

## 다음 실행 순서

1. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`와 `BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`를 fresh readback한다.
2. 현재 `PLAN` 범위의 남은 기획(`FIRST_10_MINUTES → PRECISION_CUSTOMER_LINK → RELEASE_NEAR_VERTICAL_SLICE`)을 승인된 순서로 처리한다.
3. 의미 있는 기획 변경은 GitHub·Notion 양쪽에 동기화하고 정본 충돌/적대 검토를 닫는다.
4. 새 `기획 완료` 선언 전에는 제품 code/data/scenes/assets/addons/project.godot 변경을 시작하지 않는다.
5. 구현 Gate가 열리면 그때 fresh main/open-PR/Runtime Reality를 다시 확인하고 승인된 구현 패키지만 TDD로 실행한다.

## 먼저 읽을 파일

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
3. `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`
4. 관련 2026-08-20/24 개별 Canon
5. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
6. 실제 code/data/Scene/tests — 구현 현실 확인 시

## 현재 프로젝트 작업지시문 바인딩

```yaml
WORK_INSTRUCTION: CURRENT_USER_TASK_OVERLAY_OVER_HISTORICAL_V4_5_R2
WORK_INSTRUCTION_PATH: PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md
PRE_WORK_RESEARCH_DECISION: BS-OPS-20260811-02
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
PROJECT_REPOSITORY: alsdmlals4-eng/Blacksmith
PROJECT_LOCAL_PATH: C:\Users\user\Documents\GitHub\Ninza\Blacksmith
GODOT_PROJECT_PATH: C:/Users/user/Documents/GitHub/Ninza/Blacksmith
PRODUCT_IMPLEMENTATION: BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION
TASK3_IMPLEMENTATION: NOT_APPROVED
```

첨부/저장된 v4.5 r2 source의 역사적 타 프로젝트 경로는 provenance를 위해 수정하지 않는다. 현재 실행은 최신 사용자 지시와 2026-08-20 Overlay를 우선한다.

<!-- BS-CONTENT-20260811-09 HISTORICAL -->
## R3–R7 historical 9/10 — Kyle Gladiator02

```text
HISTORICAL_R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 9/10
R3_R7_DECISION: BS-CONTENT-20260811-09
R3_R7_RESUME_LOCATOR: GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED
PRODUCT_IMPLEMENTATION_AT_CURRENT_GATE: BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION
TASK3_IMPLEMENTATION: NOT_APPROVED
```

`BS-CONTENT-20260811-09`와 `GLADIATOR_02 / KYLE_VAREN`의 prior item / 현역 지속 / 은퇴·교체 판단은 역사 및 재사용 근거로 보존한다. 현재 제품 작업 순서와 구현 Gate는 상단 `CURRENT_PRIORITY_OVERLAY`가 소유한다.