# Blacksmith Current Confirmed Decisions

> Current operating Decisions: `BS-OPS-20260802-01`, `BS-OPS-20260802-02`
>
> Status: `R0_RECOVERED / R1_IN_PROGRESS / GRILL_BATCH_01_MERGED / NEW_COUNTER_0_OF_10`
>
> Current branch: `main`
>
> Last merged PR: `#84`
>
> Batch 01 merge SHA: `bd68c2dbf20592e84c1bebfdc83c4c925d010dbf`
>
> Product implementation: `BLOCKED`

## 1. Authority Rule

이 파일은 현재 Decision 상태의 루트 진입점이다. 상세 계약은 등록된 분야별 GitHub 정본이 가지며, 실제 구현 사실은 코드·Scene·Resource·data·tests가 가진다. Google Sheet는 연결된 `USER_FACING_GDD_WORKSPACE`이며 GitHub 정본을 독립적으로 덮어쓰지 않는다.

사용자 승인 기획, Draft, 실제 구현, 자동 테스트, Godot 런타임, Android·접근성·성능·사람 플레이 상태를 서로 혼합하지 않는다.

## 2. Status Vocabulary

- `CONFIRMED_WITH_APPROVAL_EVIDENCE`: 원 사용자 승인 증거가 확인됨.
- `CONFIRMED_BY_LATEST_USER_DIRECTION`: 최신 사용자 지시로 명시 승인됨.
- `RECOMMENDED_DEFAULT`: 증거에 따라 변경 가능한 GPT 권장 상세값.
- `TEST_VALUE`: 시뮬레이션·런타임·기기·플레이테스트가 필요한 시험값.
- `PROPOSED_REVIEW_REQUIRED`: 유용하지만 승인되지 않은 Draft.
- `USER_DECISION_REQUIRED`: 검증된 중요 충돌로 Grill Me가 필요한 상태.
- `RESEARCH_OR_TEST_REQUIRED`: 문서만으로 확정할 수 없는 상태.
- `REFERENCE_IMPLEMENTATION`: 실제 또는 과거 구현 사실이며 자동 기획 승인이 아님.
- `HISTORY_ONLY`: 대체되었거나 현행 권위가 아닌 기록.

## 3. Current Operating Decisions

### `BS-OPS-20260802-01` — Planning-first canonical recovery and Grill Me boundary

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- Canonical evidence:
  - `docs/operations/BS-OPS-20260802-01_BASELINE.md`
  - `docs/operations/BS-OPS-20260802-01_FINAL_REPORT.md`
  - `docs/superpowers/specs/2026-08-02-planning-canon-recovery-design.md`
  - `docs/superpowers/plans/2026-08-02-blacksmith-planning-canon-recovery.md`

확정 계약:

1. 제품 구현보다 총기획과 정본 복구를 먼저 진행한다.
2. 기획·검수 중 제품 코드·Scene·런타임 data·assets를 변경하지 않는다.
3. 초기 수치와 기술 상세는 `RECOMMENDED_DEFAULT / TEST_VALUE`로 분리한다.
4. 검증된 중요 기획 충돌만 한 질문씩 Grill Me로 묻는다.
5. 주요 승인 Decision은 GitHub와 Sheet에 같은 ID로 동기화한다.
6. Android portrait mobile이 현재 플랫폼이며 PC는 미래 고려다.
7. 전체 기획·적대적 최종 검수·사용자 검수 전 제품 구현을 차단한다.

### `BS-OPS-20260802-02` — Grill Me 10건 단위 병합 운영

- Status: `APPROVED / BATCH_01_MERGED / ACTIVE_POLICY`.
- Canon: `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`.
- Completed batch: `BS-GRILL-BATCH-20260802-01`.
- Current new approval counter: `0/10`.

운영 계약:

1. Grill Me 배치 01의 승인 질문 5건은 PR #84로 squash 병합 완료했다.
2. 이후 새 Grill Me 승인 10건을 한 병합 배치로 묶는다.
3. 10번째 승인 직후 GitHub 정본·Sheet·PR changed files·리뷰·CI·충돌·금지 경로를 적대적으로 재검증한다.
4. P0/P1 누락·충돌·권위 불일치가 있으면 병합하지 않는다.
5. 통과 후 원칙적으로 squash 병합한다.
6. 병합 후 main SHA와 다음 카운터를 Sheet와 진입점에 기록한다.

## 4. R1 Approved Core Decisions — Batch 01

R1 전체는 아직 완료되지 않았다. 아래 결정은 PR #84를 통해 main에 병합된 현재 승인 정본이다.

### `BS-CORE-20260802-01` — 피로도·날짜 진행은 핵심 불변

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 피로도는 한 명의 대장장이가 제한된 하루의 작업 우선순위를 정하는 핵심 리듬이다.
- 날짜는 세계 일정·의뢰 마감·시장·고객 재방문·토너먼트·전쟁·계절 사건을 연결하는 공통 시간축이다.
- 제거, 장식적 캘린더 축소, 사실상 무제한 반복 허용은 재승인이 필요하다.
- 정확한 피로도·행동 수·회복·일정 주기는 `RECOMMENDED_DEFAULT / TEST_VALUE`다.

### `BS-CORE-20260802-02` — 강화 주도 코어와 작품 역사 환류

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 가장 자주 반복되는 즉각 재미는 강화의 성공·실패와 멈춤·추가 도전 판단이다.
- 방문 고객 납품과 짧은 결과 이벤트는 강화 사이의 휴식·보상·세계 환류 구간이다.
- 장기 약속은 작품이 판매 후에도 소유자·사건·운명·연대기를 남기고 다음 제작 동기로 돌아오는 것이다.

### `BS-SET-20260802-01` — 다양한 작품 제작 동기와 세트 시스템

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 고객 역할·세계 일정·사건·관계가 무기·방어구·장신구 등 다양한 작품을 만들 이유를 제공한다.
- 세트는 개별 작품의 UID·제작 등급·강화 경로·소유자·운명·연대기를 보존하는 연결된 작품군이다.
- 세트 보너스가 개별 작품의 제작·강화 가치를 압도해서는 안 된다.

### `BS-SET-20260802-02` — 사건 연대기 기반 동적 세트

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 동일 세계 사건에 실제 납품·사용·기여한 작품들이 같은 사건 연대기 ID를 공유하면 하나의 연대기 세트가 된다.
- 사건 전 후보는 예정 세트이며 실제 기여가 확인된 뒤에만 역사적 세트가 된다.
- 동일 세계 일정의 반복을 전제로 하지 않는다.
- Canon: `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`.

### `BS-SET-20260802-03` — 연대기 세트 3층 보상

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 1층: 모든 상황에서 적용되는 작고 영구적인 범용 능력치 보정.
- 2층: 환경·위협·임무·제약·전술·사회 태그가 유사한 새 사건의 추가 정보·선택지·전용 장면.
- 3층: 사건명·날짜·기여 작품·결과의 짧은 역사 요약과 선택형 상세 기록.
- 수치·누적 상한·태그 유사도는 `RECOMMENDED_DEFAULT / TEST_VALUE`다.

### `BS-SET-20260802-04` — 실패 사건도 연대기 세트 성립

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 성공·부분 성공·실패·참패와 무관하게 실제 사용·기여한 작품은 사건 연대기와 세트 자격을 얻는다.
- 결과에 따라 별칭·보정 성격·상황 태그·전용 장면·후속 의뢰가 달라진다.
- 실패했다고 실제 기여와 역사를 삭제하지 않지만 실패 파밍이 최적 성장 경로가 되어서는 안 된다.
- Canon: `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`.

## 5. Confirmed Product Decisions with Approval Evidence

다음은 승인 기획이며 구현·검증 완료와는 별개다.

- `BS-ART-20260731-01`: Stylized Dark Forge — `SELECTIVE_DOMAIN_PROMOTION_PENDING`.
- `BS-MODAK-20260731-01`: Bright fire-spirit Modak — `SELECTIVE_DOMAIN_PROMOTION_PENDING`.
- `BS-MAIN-20260801-01`: Separate main menu — `IMPLEMENTATION_NOT_STARTED`.
- `BS-SHELL-20260801-01`: Single BlacksmithApp shell — `IMPLEMENTATION_NOT_STARTED`.
- `BS-GRADE-20260801-02`: Five craftsmanship grades — `DATA_MIGRATION_NOT_STARTED`.
- `BS-SAVE-20260801-01`: Save·Continue·ResultEnvelope — `IMPLEMENTATION_NOT_STARTED`.

## 6. Protected Project Direction

- 한 명의 대장장이, 직원 경영이 아님.
- 직접 제작과 보이는 강화 위험 판단.
- 장비가 UID·정체성·소유자·운명·연대기를 가진 기억할 작품.
- 판매·납품 이후에도 세계 결과와 연대기 세트로 의미 유지.
- 플레이어 직접 전투는 현재 코어 활동이 아님.
- Android 세로형·한 손 가독성.
- 일반 강화 입력 1회는 결과 1회로 해결.
- 자동화는 반복을 줄일 수 있지만 정체성·정밀·파괴·재료·판매·소유·피로도·날짜 판단을 우회할 수 없음.

## 7. Proposed, Research-required, and Historical Content

| Decision or area | Current status | Next review |
|---|---|---|
| `PR57-PROB` | `APPROVAL_EVIDENCE_RECOVERY_REQUIRED` | R3/R5 |
| `PR58-ENDGAME` | `RESEARCH_OR_TEST_REQUIRED` | R5 |
| `PR59-CUSTOMER` | `USER_DECISION_CANDIDATE / EVIDENCE_REVIEW_REQUIRED` | R4 |
| lineage and affix cap | `PROPOSED_REVIEW_REQUIRED` | R3/R6 |
| +50 routes and representative placement | `PROPOSED_REVIEW_REQUIRED` | R2/R3/R5/R7 |
| customer eligibility and fit | `PROPOSED_REVIEW_REQUIRED` | R4 |
| fate states and destruction/recovery | `PROPOSED_REVIEW_REQUIRED` | R3/R4 |
| customer count and representative content | `PROPOSED_REVIEW_REQUIRED` | R4/R7 |
| online Hall of Masterpieces | `DEFERRED_FUTURE_REVIEW` | R5/R7 |
| v9 data migration | `PROPOSED_REVIEW_REQUIRED` | R3/R7 |
| Auto Forge boundary | `PROPOSED_REVIEW_REQUIRED` | R3/R5 |
| Android/accessibility detail | `RESEARCH_OR_TEST_REQUIRED` | R6/R7 |
| validation evidence model | `EXECUTION_NOT_RUN` | R7 |
| Base v9.3 migration plans | `HISTORY_ONLY / SUPERSEDED_BY_BASE_V9_4` | do not execute |

## 8. Current Open Decisions

현재 검증된 열린 Grill Me 질문: `0`.

신규 Grill Me 승인 카운터: `0/10`.

R1은 계속 진행 중이다. 새로운 질문은 관련 분야 감사에서 실제 중요 충돌이 확인된 경우에만 한 건씩 연다.

## 9. History and Authority Boundaries

- Issue #79: 현재 총기획 Umbrella.
- PR #84: `MERGED / R0_RECOVERY_AND_R1_BATCH_01_CANON`.
- PR #81: `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`.
- Issue #60: `HISTORY_ONLY / SUPERSEDED` 후보.
- 과거 PoC PASS: `REFERENCE_IMPLEMENTATION`, 최신 제품 검증이 아님.

## 10. Synchronization Ledger

| Decision group | GitHub | Sheet | Status |
|---|---|---|---|
| `BS-OPS-20260802-01` | Root·baseline·final report·PR #84 | `00·01·02·04·05·90·99` | `MERGED / SYNCED` |
| R1 core and set `01~03` | R1 승인 원장·사건 연대기 정본 | `02·05·99` | `MERGED / SYNCED` |
| `BS-SET-20260802-04` | Grill Me batch 01 정본 | `02!A40:M40`, `05!A26:J26`, `99!A41:H41` | `MERGED / POSTMERGE_READBACK_PENDING` |
| `BS-OPS-20260802-02` | Grill Me batch 01 정본 | `02!A41:M41`, `05!A27:J27`, `99!A42:H42` | `ACTIVE / POSTMERGE_READBACK_PENDING` |

## 11. Current Gates

```yaml
CANONICAL_RECOVERY_GATE: PASS
DECISION_AUTHORITY_GATE: PASS
PREMERGE_ADVERSARIAL_AUDIT_GATE: PASS
PR_84_MERGE_GATE: PASS
DECISION_SYNC_GATE: POSTMERGE_READBACK_PENDING
PLANNING_COVERAGE_GATE: R1_IN_PROGRESS
GRILL_ME_DECISION_GATE: NEW_COUNTER_0_OF_10
PLANNING_AND_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
RUNTIME_VALIDATION_GATE: NOT_RUN_FOR_NEW_R1_FEATURES
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## 12. Next Planning Activity

1. postmerge sync PR에서 main 진입 상태와 Sheet를 최종 동기화한다.
2. 신규 Grill Me 카운터 `0/10`으로 R1의 남은 프로젝트 코어·플레이어 약속 기획을 계속한다.
3. 별도 승인 전 제품 구현은 시작하지 않는다.
