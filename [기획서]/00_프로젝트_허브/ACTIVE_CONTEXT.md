# [현재 정본] Active Context

<!-- R3_R7_DESIGN_RESUMED -->
> **R3_R7_DESIGN_ACTIVE / COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED / PLANNING_ONLY**
>
> 이 문서는 현재 상태와 다음 읽기 순서를 연결하는 압축 라우터다. 세부 Decision·과거 단계·실행 로그는 책임 원본에서 읽는다.

- 갱신 기준: `2026-08-11 KST`
- Blacksmith current main observed at Decision 04 start: `1e60cf163191d547b96ffc392e3da24d072b7956`
- `BASE_CURRENT_MAIN_OBSERVED`: `315c66eea9614c284b9c11c4d522141065dfa4b0`
- `PROJECT_BASE_ADAPTER_PIN`: `2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b`
- 현재 R3–R7 승인 카운터: `4/10`
- Base current main 관측값과 프로젝트가 채택한 Base adapter pin은 서로 다른 증거다. 새 Base main 관측만으로 프로젝트 pin을 자동 승격하지 않는다.

```yaml
CURRENT_STAGE: R3_R7_DESIGN_ACTIVE
R2_BASELINE: R2_BATCH_006_MAIN_CANON
R2_CHECKPOINT_005: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: R2_BATCH_005_CLOSED_10_OF_10
R2_BATCH_005_MERGE: MERGED_PR109_MAIN_CANON
R2_BATCH_006: R2_BATCH_006_APPROVED_10_OF_10
R2_BATCH_006_MERGE: MERGED_PR120_MAIN_CANON
R3_R7_APPROVAL_COUNTER: 4/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04
PRE_WORK_RESEARCH_DECISION: BS-OPS-20260811-02
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
R3_R7_RESUME_LOCATOR: COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED
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

`BS-CONTENT-20260811-01` Nadia, `BS-CONTENT-20260811-02` Toren, `BS-CONTENT-20260811-03` Marek는 승인 완료 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-04`다.

```text
COLLECTOR_01 / ERSA_ROEN
→ 수집가 대표 고객
→ EXHIBITION_EVIDENCE_AND_PROVENANCE
→ CRAFTSMANSHIP_EVIDENCE 또는 LIVED_HISTORY_EVIDENCE 전시 의도 공개
→ 후보 작품의 실제 UID 증거 비교
→ 같은 작품 UID 한 점 + 기존 증거 2~4개 강조
→ 전시는 비직접 세계 사건
→ EXHIBITION_RECEPTION_STATE
 + EXHIBIT_THESIS_FIT_STATE
 + ITEM_UID_PUBLIC_LEGACY_STATE
→ 후속 제작·복원·판매·재전시 이유
```

- 새 `RARITY_SCORE / PRESTIGE_SCORE / COLLECTOR_SCORE / EXHIBITION_SCORE`를 만들지 않는다.
- Chronicle 개수·최고 예술성·최고 강화·가장 오래된 작품을 자동 정답으로 만들지 않는다.
- 전시 횟수나 전시 자체로 `ARTISTRY`를 자동 성장시키거나 `CHRONICLE_AFFIX`를 자동 부여하지 않는다.
- 플레이어는 작품·증거를 고르는 대장장이이며 전시관·관람객을 직접 운영하지 않는다.
- 같은 작품 UID의 제작·소유·손상·복원·Chronicle/provenance 증거를 보존한다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`

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
- 같은 UID의 작품 생애를 유지한다.
- 모든 개인 일정에 고정 3일 결과·4일 재방문을 재도입하지 않는다.
- 사람 플레이테스트·Android 실기기·접근성은 실제 실행 전 `NOT_RUN`.
- HiGodot은 승인된 Godot persistent authoring 권위, GUT 9.7.1은 GDScript test 권위, Hera는 enabled non-authoritative / `AUTHORITY_NONE`이다.

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
BS-OPS-20260811-02 / PRE_WORK_RESEARCH_GATE
```

## 불변 체크포인트 호환 이력

- R2 체크포인트 004·005와 Batch 006은 삭제 금지 이력이며 R3–R7 설계의 상속 기반이다.
- `R2_CHECKPOINT_004 / MERGED_PR106 / MAIN_CANON`
- checkpoint 004 closure squash merge: `7a46fa38586a42f268cd0432744203049649ddd5`
- Batch 006 merge main: `a8a94343c78a68bf7bb14b411e7741f43b257138`

## 다음 실행 순서

1. `BS-CONTENT-20260811-04`의 exact-head CI·적대 검토·GitHub·Sheet 동일 Decision ID 동기화를 끝낸다.
2. TDD RED→GREEN으로 Ersa 전시 증거 계약과 current/history 라우팅을 검증한다.
3. 희귀도/위신 총점·Chronicle 개수 최적화·전시 farming·큐레이터 게임화·UID 손실을 적대적으로 차단한다.
4. 새 제품 Task는 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED`와 `TASK3_IMPLEMENTATION: NOT_APPROVED`가 별도 사용자 승인으로 해소되기 전 시작하지 않는다.
5. 다음 R3–R7 신규 Decision은 현재 승인 카운터 `4/10`에서 이어간다.

## 먼저 읽을 파일

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
9. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
10. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
11. Google Sheet `00_프로젝트_허브`, `01_작업순서`, `02_현재_확정결정`, `04_누락_충돌_감사`, `13_주요인물`, `50_메인콘텐츠`

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

<!-- BS-CONTENT-20260811-04 CURRENT -->
## R3–R7 current 4/10 — Ersa Collector01

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 4/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04
R3_R7_RESUME_LOCATOR: COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

Nadia 1/10, Toren 2/10, Marek 3/10은 승인 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-04`이다.

`COLLECTOR_01 / ERSA_ROEN / EXHIBITION_EVIDENCE_AND_PROVENANCE`는 `CRAFTSMANSHIP_EVIDENCE` 또는 `LIVED_HISTORY_EVIDENCE` 전시 의도와 작품에 실제 존재하는 증거를 비교한다. 숨은 총점이나 단일 최대 수치가 정답이 아니다.

같은 UID의 결과는 `EXHIBITION_RECEPTION_STATE / EXHIBIT_THESIS_FIT_STATE / ITEM_UID_PUBLIC_LEGACY_STATE`로 분리한다. 전시는 비직접 세계 사건이며 플레이어는 대장장이·작품 증거 선택자로 남는다.