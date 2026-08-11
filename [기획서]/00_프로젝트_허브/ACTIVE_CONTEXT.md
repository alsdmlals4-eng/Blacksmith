# [현재 정본] Active Context

<!-- R3_R7_DESIGN_RESUMED -->
> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**
>
> 이 문서는 현재 상태와 다음 읽기 순서를 연결하는 압축 라우터다. 세부 Decision·과거 단계·실행 로그는 책임 원본에서 읽는다.

- 갱신 기준: `2026-08-11 KST`
- Blacksmith current main observed at Decision 08 start: `7005a939e003f7248e7d2546c4266bb5d144f90a`
- `BASE_CURRENT_MAIN_OBSERVED`: `23d5b292f619022cdd8ab7a33fb1debc2d294861`
- `PROJECT_BASE_ADAPTER_PIN`: `2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b`
- 현재 R3–R7 승인 카운터: `8/10`
- Base current main 관측값과 프로젝트가 채택한 Base adapter pin은 서로 다른 증거다. 새 Base main 관측만으로 프로젝트 pin을 자동 승격하지 않는다.

```yaml
CURRENT_STAGE: R3_R7_DESIGN_ACTIVE
R2_BASELINE: R2_BATCH_006_MAIN_CANON
R2_CHECKPOINT_005: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: R2_BATCH_005_CLOSED_10_OF_10
R2_BATCH_005_MERGE: MERGED_PR109_MAIN_CANON
R2_BATCH_006: R2_BATCH_006_APPROVED_10_OF_10
R2_BATCH_006_MERGE: MERGED_PR120_MAIN_CANON
R3_R7_APPROVAL_COUNTER: 8/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08
PRE_WORK_RESEARCH_DECISION: BS-OPS-20260811-02
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
R3_R7_RESUME_LOCATOR: COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED
VERTICAL_SLICE_IMPLEMENTATION: APPROVED_TASK2_COMPLETE
VERTICAL_SLICE_IMPLEMENTATION_EVIDENCE: VERTICAL_SLICE_IMPLEMENTATION_APPROVED
TASK2: TASK2_MAIN_MERGED
POSTMERGE_CLOSURE: POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE
WORK_MODE: PLAN_REVIEW
PRODUCT_IMPLEMENTATION: BLOCKED
NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED
TASK3_IMPLEMENTATION: NOT_APPROVED
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

## 현재 R3–R7 기획 재개 상태

`BS-CONTENT-20260811-01`~`07`은 승인 완료 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-08`이다.

```text
COLLECTOR_02 / SEDRIC_VAEL
→ 기존 수집가 추가 고객·귀족 기록 보관가를 두 번째 Collector-family 상세 콘텐츠로 승격
→ ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
→ archival category / keeping purpose 공개
→ 실제 작품 UID와 기록된 provenance·custody·생애 근거 비교
→ 한 작품 UID 선택·같은 UID 인계
→ accession은 비직접 고객/세계 사건
→ ARCHIVE_ACCESSION_STATE
 + PROVENANCE_DOCUMENTATION_STATE
 + ITEM_UID_CUSTODY_LEGACY_STATE
→ 보존·기존 treatment·재평가·후속 전시/연구·다른 작품 제작 이유
```

- Ersa/Collector01의 공개 전시 증거·thesis 책임을 보존한다.
- Noble01의 물리적 수리·복원·재작업 개입 깊이 책임을 보존한다.
- 진품성·provenance completeness·archive prestige 같은 aggregate score를 만들지 않는다.
- 최고 Artistry·가장 오래된 작품·가장 많은 Chronicle·최고 강화가 자동 정답이 아니다.
- 기록되지 않은 provenance/custody를 생성하거나 자동 보완하지 않는다.
- archive storage·museum·visitor·staff/shelf·보존환경·loan logistics 관리 게임을 추가하지 않는다.
- accession/review 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 같은 작품 UID를 후보·인계·accession 결과·후속 custody까지 보존한다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`를 이번 Decision에서 재정의하지 않는다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`

이 승인은 **기획 재개 승인**이다. Task3 또는 일반 제품 구현 승인이 아니다.

## 현재 권위와 보호 경계

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
6. R3–R7 분야별 승인 책임 원본
7. 이 문서와 `START_HERE.md`, `DEVELOPMENT_GATES.md`, `ROADMAP.md`
8. 실제 code/data/Scene/tests
9. Google Sheet — 같은 Decision과 상태를 연결하는 소비처

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
BS-OPS-20260811-02 / PRE_WORK_RESEARCH_GATE
```

## 불변 체크포인트 호환 이력

- R2 체크포인트 004·005와 Batch 006은 삭제 금지 이력이며 R3–R7 설계의 상속 기반이다.
- `R2_CHECKPOINT_004 / MERGED_PR106 / MAIN_CANON`
- checkpoint 004 closure squash merge: `7a46fa38586a42f268cd0432744203049649ddd5`
- Batch 006 merge main: `a8a94343c78a68bf7bb14b411e7741f43b257138`

## 다음 실행 순서

1. `BS-CONTENT-20260811-08`의 RED→GREEN 회귀, 적대 검토, exact-head CI, GitHub·Sheet 동일 Decision ID 동기화를 끝낸다.
2. Sedric archival accession이 Ersa exhibition과 Noble01 treatment-depth를 침범하지 않고, same-UID provenance/custody 3축과 anti-score·anti-fabrication·anti-management·anti-farming 경계를 유지하는지 검증한다.
3. 새 제품 Task는 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED`와 `TASK3_IMPLEMENTATION: NOT_APPROVED`가 별도 사용자 승인으로 해소되기 전 시작하지 않는다.
4. Decision08 merge·Sheet readback 뒤 다음 신규 R3–R7 Decision은 `9/10` 사용자 기획 승인 Gate에서 이어간다.

## 먼저 읽을 파일

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
9. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
10. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
11. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
12. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
13. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
14. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
15. Google Sheet `00_프로젝트_허브`, `01_작업순서`, `02_현재_확정결정`, `04_누락_충돌_감사`, `13_주요인물`, `50_메인콘텐츠`

## 현재 프로젝트 작업지시문 바인딩

```yaml
WORK_INSTRUCTION: V4_5_R2_CURRENT_CANON
WORK_INSTRUCTION_PATH: PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md
WORK_INSTRUCTION_DECISION: BS-OPS-20260811-01
PRE_WORK_RESEARCH_DECISION: BS-OPS-20260811-02
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
PROJECT_REPOSITORY: alsdmlals4-eng/Blacksmith
PROJECT_LOCAL_PATH: C:\Users\user\Documents\GitHub\Ninza\Blacksmith
GODOT_PROJECT_PATH: C:/Users/user/Documents/GitHub/Ninza/Blacksmith
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

첨부 v4.5 r2 source의 `Switchy-Express-Cargo-Puzzle` 경로는 source provenance를 위해 수정하지 않고 보존한다. 현재 실행은 `BS-OPS-20260811-01`의 Blacksmith override를 따른다.

<!-- BS-CONTENT-20260811-08 CURRENT -->
## R3–R7 current 8/10 — Sedric Collector02

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 8/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08
R3_R7_RESUME_LOCATOR: COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

Nadia 1/10, Toren 2/10, Marek 3/10, Ersa 4/10, Cassia 5/10, Noble01 6/10, Liana 7/10은 승인 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-08`이다.

`COLLECTOR_02 / SEDRIC_VAEL / ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY`는 공개된 archival purpose와 실제 작품 UID의 provenance·custody·생애 근거를 비교해 한 작품을 인계한다. accession은 비직접 사건이며 `ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE`를 분리해 돌려준다.

Ersa의 exhibition evidence/thesis, Noble01의 physical treatment depth, Liana의 commander mission-fit 책임은 각각 승인 이력으로 유지한다. 같은 UID, anti-score, anti-fabrication, anti-management, anti-farming 경계를 보존하며 제품 구현과 Task3는 계속 차단한다.
