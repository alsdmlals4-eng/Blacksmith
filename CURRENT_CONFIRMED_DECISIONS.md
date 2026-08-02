# Blacksmith Current Confirmed Decisions

> Current operating Decisions: `BS-OPS-20260802-01`, `BS-OPS-20260802-02`
>
> Status: `R0_RECOVERED / R1_IN_PROGRESS / GRILL_BATCH_01_MERGED / NEW_COUNTER_0_OF_10`
>
> Current branch: `main`
>
> Planning batch PR: `#84` — merge SHA `bd68c2dbf20592e84c1bebfdc83c4c925d010dbf`
>
> Postmerge sync PR: `#85` — sync SHA `338d256c7ffbf976473d04712ff9426f1e450d2c`
>
> Exact current main SHA authority: connected Google Sheet and Issue `#79`
>
> Product implementation: `BLOCKED`

## 1. Authority Rule

이 파일은 현재 Decision 상태의 루트 진입점이다. 상세 계약은 분야별 GitHub 정본이 가지며, 실제 구현 사실은 코드·Scene·Resource·data·tests가 가진다. Google Sheet는 연결된 `USER_FACING_GDD_WORKSPACE`이며 GitHub 정본을 독립적으로 덮어쓰지 않는다.

사용자 승인 기획, Draft, 실제 구현, 자동 테스트, Godot 런타임, Android·접근성·성능·사람 플레이 상태를 혼합하지 않는다.

## 2. Status Vocabulary

- `CONFIRMED_WITH_APPROVAL_EVIDENCE`: 원 사용자 승인 증거가 확인됨.
- `CONFIRMED_BY_LATEST_USER_DIRECTION`: 최신 사용자 지시로 승인됨.
- `RECOMMENDED_DEFAULT`: 변경 가능한 권장 상세값.
- `TEST_VALUE`: 검증이 필요한 시험값.
- `PROPOSED_REVIEW_REQUIRED`: 승인되지 않은 Draft.
- `USER_DECISION_REQUIRED`: 중요 충돌로 Grill Me가 필요한 상태.
- `RESEARCH_OR_TEST_REQUIRED`: 문서만으로 확정 불가.
- `REFERENCE_IMPLEMENTATION`: 기존 구현 사실이며 자동 기획 승인이 아님.
- `HISTORY_ONLY`: 현행 권위가 아닌 기록.

## 3. Current Operating Decisions

### `BS-OPS-20260802-01` — Planning-first canonical recovery

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 제품 구현보다 총기획과 정본 복구를 먼저 진행한다.
- 상세 수치와 기술값은 `RECOMMENDED_DEFAULT / TEST_VALUE`로 분리한다.
- 검증된 중요 충돌만 한 질문씩 Grill Me로 묻는다.
- 주요 승인 Decision은 GitHub와 Sheet에 같은 ID로 동기화한다.
- Android portrait mobile이 현재 플랫폼이다.
- 전체 기획·최종 적대적 검수·사용자 검수 전 제품 구현을 차단한다.

### `BS-OPS-20260802-02` — Grill Me 10건 단위 병합 운영

- Status: `APPROVED / BATCH_01_MERGED / ACTIVE_POLICY`.
- Canon: `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`.
- Completed batch: `BS-GRILL-BATCH-20260802-01`.
- Current new approval counter: `0/10`.

운영 계약:

1. 배치 01의 승인 질문 5건은 PR #84로 squash 병합 완료했다.
2. 이후 새 Grill Me 승인 10건을 한 병합 배치로 묶는다.
3. 10번째 승인 직후 GitHub 정본·Sheet·changed files·리뷰·CI·충돌·금지 경로를 적대적으로 재검증한다.
4. P0/P1 문제가 있으면 병합하지 않는다.
5. 통과 후 squash 병합하고 정확한 main SHA를 Sheet와 Issue #79에 기록한다.

## 4. R1 Approved Core Decisions — Batch 01

R1 전체는 아직 완료되지 않았다. 아래 결정은 main에 병합된 현재 승인 정본이다.

### `BS-CORE-20260802-01` — 피로도·날짜 진행은 핵심 불변

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 제한된 하루의 작업 우선순위와 세계 일정·의뢰·시장·고객·사건을 연결한다.
- 장식적 캘린더나 사실상 무제한 반복으로 축소하려면 재승인이 필요하다.
- 정확한 행동 수·회복·일정 주기는 `TEST_VALUE`다.

### `BS-CORE-20260802-02` — 강화 주도 코어와 작품 역사 환류

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 즉각적 메인 재미는 강화 성공·실패와 멈춤·추가 도전 판단이다.
- 방문 고객 납품과 짧은 결과 이벤트는 휴식·보상·세계 환류다.
- 작품은 판매 후에도 소유자·사건·운명·연대기를 남긴다.

### `BS-SET-20260802-01` — 다양한 작품 제작 동기와 세트

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 고객 역할·세계 일정·사건·관계가 무기·방어구·장신구 등 다양한 작품 제작 동기를 제공한다.
- 세트는 개별 작품의 UID·품질·강화·소유·운명·연대기를 보존한다.

### `BS-SET-20260802-02` — 사건 연대기 기반 동적 세트

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 같은 사건에 실제 납품·사용·기여한 작품들이 동일 사건 연대기 ID를 공유하면 세트가 된다.
- 사건 전 후보는 예정 세트이며 실제 기여 후에만 역사적 세트가 된다.
- 동일 세계 일정의 반복을 전제로 하지 않는다.

### `BS-SET-20260802-03` — 연대기 세트 3층 보상

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 1층: 작고 영구적인 범용 능력치 보정.
- 2층: 환경·위협·임무·제약·전술·사회 태그가 유사한 새 사건의 추가 정보·선택지·전용 장면.
- 3층: 사건명·날짜·기여 작품·결과의 짧은 역사 요약과 상세 기록.
- 수치·누적 상한·태그 유사도는 `TEST_VALUE`다.

### `BS-SET-20260802-04` — 실패 사건도 연대기 세트 성립

- Status: `APPROVED / SYNCED / MERGED_TO_MAIN`.
- 성공·부분 성공·실패·참패와 무관하게 실제 사용·기여한 작품은 연대기와 세트 자격을 얻는다.
- 결과에 따라 별칭·보정·태그·장면·후속 의뢰가 달라진다.
- 실패 파밍이 최적 성장 경로가 되어서는 안 된다.

상세 정본:

- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`

## 5. Confirmed Product Decisions with Approval Evidence

다음은 승인 기획이며 구현·검증 완료와 별개다.

- `BS-ART-20260731-01`: Stylized Dark Forge — `SELECTIVE_PROMOTION_PENDING`.
- `BS-MODAK-20260731-01`: Bright fire-spirit Modak — `SELECTIVE_PROMOTION_PENDING`.
- `BS-MAIN-20260801-01`: Separate main menu — `IMPLEMENTATION_NOT_STARTED`.
- `BS-SHELL-20260801-01`: Single BlacksmithApp — `IMPLEMENTATION_NOT_STARTED`.
- `BS-GRADE-20260801-02`: Five craftsmanship grades — `DATA_MIGRATION_NOT_STARTED`.
- `BS-SAVE-20260801-01`: Save·Continue·ResultEnvelope — `IMPLEMENTATION_NOT_STARTED`.

## 6. Protected Project Direction

- 한 명의 대장장이, 직원 경영이 아님.
- 직접 제작과 보이는 강화 위험 판단.
- 장비가 UID·정체성·소유자·운명·연대기를 가진 작품.
- 판매·납품 이후에도 세계 결과와 세트로 의미 유지.
- 플레이어 직접 전투는 현재 코어 활동이 아님.
- Android 세로형·한 손 가독성.
- 일반 강화 입력 1회는 결과 1회.
- 자동화는 정체성·정밀·파괴·재료·판매·소유·피로도·날짜 판단을 우회할 수 없음.

## 7. Current Open Decisions

현재 열린 Grill Me 질문: `0`.

신규 Grill Me 승인 카운터: `0/10`.

R1은 계속 진행 중이며 실제 중요 충돌이 확인된 경우에만 새 질문을 연다.

## 8. History and Authority Boundaries

- Issue #79: 총기획 Umbrella.
- PR #84: `MERGED / R0_RECOVERY_AND_R1_BATCH_01_CANON`.
- PR #85: `MERGED / POSTMERGE_STATE_SYNC`.
- PR #81: `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`.
- 과거 PoC PASS: `REFERENCE_IMPLEMENTATION`.

## 9. Synchronization Ledger

| Decision group | GitHub | Sheet | Status |
|---|---|---|---|
| `BS-OPS-20260802-01` | Root·baseline·report | `00·01·02·04·05·90·99` | `MERGED / SYNCED` |
| R1 core and set `01~04` | R1 승인 원장·세트 정본·배치 정본 | `02·05·99` | `MERGED / POSTMERGE_READBACK_PASS` |
| `BS-OPS-20260802-02` | 배치·병합 운영 정본 | `00·02·04·05·99` | `ACTIVE / POSTMERGE_READBACK_PASS` |
| exact current main SHA | GitHub main | Sheet `00·02·04·99` | `EXTERNAL_LEDGER_AUTHORITY` |

## 10. Current Gates

```yaml
CANONICAL_RECOVERY_GATE: PASS
DECISION_AUTHORITY_GATE: PASS
PREMERGE_ADVERSARIAL_AUDIT_GATE: PASS
BATCH_01_MERGE_GATE: PASS
POSTMERGE_SYNC_GATE: PASS
DECISION_SYNC_GATE: PASS
PLANNING_COVERAGE_GATE: R1_IN_PROGRESS
GRILL_ME_DECISION_GATE: NEW_COUNTER_0_OF_10
PLANNING_AND_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
NEW_R1_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## 11. Next Planning Activity

신규 Grill Me 카운터 `0/10`에서 R1의 남은 프로젝트 코어·플레이어 약속 기획을 계속한다. 별도 승인 전 제품 구현은 시작하지 않는다.
