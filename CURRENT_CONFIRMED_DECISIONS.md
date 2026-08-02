# Blacksmith Current Confirmed Decisions

> Current operating Decisions: `BS-OPS-20260802-01`, `BS-OPS-20260802-02`
>
> Status: `R0_RECOVERED / R1_IN_PROGRESS / GRILL_BATCH_01_PREMERGE_AUDIT`
>
> Recovery branch: `agent/blacksmith-planning-canon-recovery`
>
> Draft PR: `#84`
>
> Product implementation: `BLOCKED`

## 1. Authority Rule

이 파일은 현재 Decision 상태의 루트 진입점이다. 상세 계약은 등록된 분야별 GitHub 정본이 가지며, 실제 구현 사실은 코드·Scene·Resource·data·tests가 가진다. Google Sheet는 연결된 `USER_FACING_GDD_WORKSPACE`이며 GitHub 정본을 독립적으로 덮어쓰지 않는다.

다음 상태는 서로 동일하지 않다.

- 사용자 승인 기획
- Draft 또는 제안
- 실제 구현
- 자동 테스트 결과
- Godot 런타임 검증
- Android·접근성·성능·사람 플레이 검증

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

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / SYNCED`.
- Canonical locations:
  - 이 파일
  - `docs/operations/BS-OPS-20260802-01_BASELINE.md`
  - `docs/operations/BS-OPS-20260802-01_FINAL_REPORT.md`
- Approved design: `docs/superpowers/specs/2026-08-02-planning-canon-recovery-design.md`.
- Execution plan: `docs/superpowers/plans/2026-08-02-blacksmith-planning-canon-recovery.md`.

확정 계약:

1. 제품 구현보다 총기획 작성과 정본 복구를 먼저 진행한다.
2. 기획·검수 중 제품 코드·Scene·런타임 data·assets는 변경하지 않는다.
3. 초기 수치와 기술 상세는 `RECOMMENDED_DEFAULT / TEST_VALUE`로 분리한다.
4. 검증된 중요 기획 충돌만 한 질문씩 Grill Me로 묻는다.
5. 주요 승인 Decision은 GitHub와 Sheet에 같은 Decision ID로 즉시 동기화한다.
6. Android portrait mobile이 현재 플랫폼이며 PC는 미래 고려다.
7. 전체 기획·적대적 최종 검수·사용자 검수 전 Codex 제품 구현은 차단한다.

### `BS-OPS-20260802-02` — Grill Me 10건 단위 병합 운영

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / PREMERGE_AUDIT_IN_PROGRESS`.
- Canon: `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`.
- Current batch: `BS-GRILL-BATCH-20260802-01`.

확정 계약:

1. 지금까지 승인된 Grill Me 5건은 이번 PR #84에서 즉시 병합한다.
2. 이번 병합 후 신규 승인 카운터는 `0/10`으로 초기화한다.
3. 이후 새 Grill Me 승인 10건마다 하나의 병합 배치로 닫는다.
4. 병합 직전 GitHub 정본·Sheet·PR changed files·리뷰·CI·충돌·금지 경로를 적대적으로 재검증한다.
5. P0/P1 누락·충돌·권위 불일치가 있으면 병합하지 않는다.
6. 사전 감사 통과 후 원칙적으로 squash 병합한다.
7. 병합 후 main의 실제 SHA를 Sheet와 다음 작업 진입점에 다시 기록한다.

## 4. R1 Approved Core Decisions — Batch 01

R1 전체는 아직 완료되지 않았다. 아래 결정만 현재 승인 정본이며, 나머지 R1 질문과 성공·실패 기준은 후속 작업에서 계속 작성한다.

### `BS-CORE-20260802-01` — 피로도·날짜 진행은 핵심 불변

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / SYNCED`.
- 피로도는 광고성 대기벽이 아니라 한 명의 대장장이가 제한된 하루의 작업 우선순위를 정하는 핵심 리듬이다.
- 날짜는 세계 일정·의뢰 마감·시장·고객 재방문·토너먼트·전쟁·계절 사건을 연결하는 공통 시간축이다.
- 제거, 장식적 캘린더 축소, 사실상 무제한 반복 허용은 재승인이 필요하다.
- 정확한 피로도·행동 수·회복·일정 주기는 `RECOMMENDED_DEFAULT / TEST_VALUE`다.

### `BS-CORE-20260802-02` — 강화 주도 코어와 작품 역사 환류

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / SYNCED`.
- 가장 자주 반복되는 즉각 재미는 강화의 성공·실패와 멈춤·추가 도전 판단이다.
- 방문 고객 납품과 짧은 결과 이벤트는 강화 사이의 휴식·보상·세계 환류 구간이다.
- 장기 약속은 작품이 판매 후에도 소유자·사건·운명·연대기를 남기고 다음 제작 동기로 돌아오는 것이다.

### `BS-SET-20260802-01` — 다양한 작품 제작 동기와 세트 시스템

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / SYNCED`.
- 고객 역할·세계 일정·사건·관계가 무기·방어구·장신구 등 다양한 작품을 만들 이유를 제공한다.
- 세트는 개별 작품의 UID·제작 등급·강화 경로·소유자·운명·연대기를 보존하는 연결된 작품군이다.
- 세트 보너스가 개별 작품의 제작·강화 가치를 압도해서는 안 된다.

### `BS-SET-20260802-02` — 사건 연대기 기반 동적 세트

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / SYNCED`.
- 동일 세계 사건에 실제 납품·사용·기여한 작품들이 같은 사건 연대기 ID를 공유하면 하나의 연대기 세트가 된다.
- 사건 전 후보는 예정 세트이며 실제 기여가 확인된 뒤에만 역사적 세트가 된다.
- 동일 세계 일정의 반복을 전제로 하지 않는다.
- Canon: `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`.

### `BS-SET-20260802-03` — 연대기 세트 3층 보상

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / SYNCED`.
- 1층: 모든 상황에서 적용되는 작고 영구적인 범용 능력치 보정.
- 2층: 환경·위협·임무·제약·전술·사회 상황 태그가 유사한 새 사건의 추가 정보·선택지·전용 장면.
- 3층: 사건명·날짜·기여 작품·결과의 짧은 역사 요약과 선택형 상세 기록.
- 수치·누적 상한·태그 유사도는 `RECOMMENDED_DEFAULT / TEST_VALUE`다.

### `BS-SET-20260802-04` — 실패 사건도 연대기 세트 성립

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / SYNCED`.
- 성공·부분 성공·실패·참패와 무관하게 실제 사용·기여한 작품은 사건 연대기와 세트 자격을 얻는다.
- 결과에 따라 별칭·보정 성격·상황 태그·전용 장면·후속 의뢰가 달라진다.
- 실패했다고 실제 기여와 역사를 삭제하지 않지만 실패 파밍이 최적 성장 경로가 되어서는 안 된다.
- Canon: `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`.

## 5. Confirmed Product Decisions with Approval Evidence

다음은 기존 승인 증거가 복구된 제품 기획이다. 구현·검증 완료와는 별개다.

### `BS-ART-20260731-01` — Stylized Dark Forge

- `CONFIRMED_WITH_APPROVAL_EVIDENCE / SELECTIVE_DOMAIN_PROMOTION_PENDING`.
- 어두운 대장간의 무게감, 읽기 쉬운 장비, 따뜻한 국소 화광, 스타일라이즈드 2D, 장비가 시각적 주인공.

### `BS-MODAK-20260731-01` — Bright fire-spirit Modak

- `CONFIRMED_WITH_APPROVAL_EVIDENCE / SELECTIVE_DOMAIN_PROMOTION_PENDING`.
- 차분한 표정과 밝은 노랑·주황 불 정령 몸체. 숯 껍질 형태는 기본이 아님.

### `BS-MAIN-20260801-01` — Separate main menu

- `CONFIRMED_WITH_APPROVAL_EVIDENCE / IMPLEMENTATION_NOT_STARTED`.
- Continue·New Game·Settings와 저장 인식 Continue, 교체 경고를 가진 별도 Main Menu.

### `BS-SHELL-20260801-01` — Single BlacksmithApp shell

- `CONFIRMED_WITH_APPROVAL_EVIDENCE / IMPLEMENTATION_NOT_STARTED`.
- Main Menu 이후 한 `BlacksmithApp`이 캠페인 상태를 유지하고 View·Overlay가 탐색과 중단을 분리.

### `BS-GRADE-20260801-02` — Five craftsmanship grades

- `CONFIRMED_WITH_APPROVAL_EVIDENCE / DATA_MIGRATION_NOT_STARTED`.
- `보통 → 우수 → 명품 → 걸작 → 전설`; `양질` 제거.
- ID·분포·배율·마이그레이션 값은 R3 시험값.

### `BS-SAVE-20260801-01` — Save, Continue, and ResultEnvelope

- `CONFIRMED_WITH_APPROVAL_EVIDENCE / IMPLEMENTATION_NOT_STARTED`.
- 한 캠페인, 자동 백업 2개, 손상 복구, 안전한 New Game 교체, `AttemptIntent`, `ResultEnvelope`.
- Android process death와 사람 검증은 `NOT_RUN`.

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

이번 배치 병합 후 신규 Grill Me 승인 카운터: `0/10`.

R1은 아직 진행 중이다. 새로운 질문은 관련 분야 감사에서 실제 중요 충돌이 확인된 경우에만 한 건씩 연다.

## 9. History and Authority Boundaries

- Issue #79: 현재 총기획 Umbrella.
- PR #84: R0 복구와 R1 승인 배치 01을 병합하는 현재 PR.
- PR #81: `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`.
- Issue #60: `HISTORY_ONLY / SUPERSEDED` 후보.
- 과거 PoC PASS: `REFERENCE_IMPLEMENTATION`, 최신 제품 검증이 아님.

## 10. Synchronization Ledger

| Decision group | GitHub | Sheet | Status |
|---|---|---|---|
| `BS-OPS-20260802-01` | 이 파일·baseline·final report·PR #84 | `00·01·02·04·05·90·99` | `SYNCED` |
| R1 core and set `01~03` | R1 승인 원장·사건 연대기 정본 | `02·05·99` 동일 Decision ID | `SYNCED / READBACK_PASS` |
| `BS-SET-20260802-04` | Grill Me batch 01 정본 | `02!A40:M40`, `05!A26:J26`, `99!A41:H41` | `PREMERGE_READBACK_REQUIRED` |
| `BS-OPS-20260802-02` | Grill Me batch 01 정본 | `02!A41:M41`, `05!A27:J27`, `99!A42:H42` | `PREMERGE_READBACK_REQUIRED` |

## 11. Current Gates

```yaml
CANONICAL_RECOVERY_GATE: PASS
DECISION_AUTHORITY_GATE: PREMERGE_RECHECK
DECISION_SYNC_GATE: PREMERGE_RECHECK
PLANNING_COVERAGE_GATE: R1_IN_PROGRESS
GRILL_ME_DECISION_GATE: BATCH_01_APPROVED
PREMERGE_ADVERSARIAL_AUDIT_GATE: IN_PROGRESS
PLANNING_AND_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## 12. Next Planning Activity

1. PR #84 병합 전 GitHub·Sheet·PR·리뷰·CI·충돌 적대적 감사 완료.
2. 이상이 없으면 squash 병합.
3. main merge SHA와 Sheet를 재동기화하고 신규 Grill Me 카운터를 `0/10`으로 확정.
4. 별도 제품 구현 없이 R1의 남은 프로젝트 코어·플레이어 약속 기획을 계속한다.
