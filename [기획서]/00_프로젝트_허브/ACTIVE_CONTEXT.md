# Active Context

- 갱신일: `2026-08-02 15:06 KST`
- Work Mode: `TOTAL_PLANNING`
- 현재 운영 Decisions: `BS-OPS-20260802-01`, `BS-OPS-20260802-02`
- 기준 main: `ac120fb146cea29bb5f8876682809f76779d86ad`
- 현재 브랜치: `agent/blacksmith-planning-canon-recovery`
- 현재 Draft PR: `#84`
- 기획 Umbrella: Issue `#79`
- 현재 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE`
- 현재 상태: `IN_PROGRESS / GRILL_BATCH_01_PREMERGE_AUDIT`
- 제품 구현: `BLOCKED`

## 현재 판정

| 영역 | 상태 |
|---|---|
| Base release adoption | `9.4.0 / COMPLETE` |
| R0 운영·정본 복구 | `PASS_FOR_DRAFT_PR` |
| Root current decisions | `UPDATED_FOR_R1_BATCH_01` |
| Current R1 canon overlay | `CREATED` |
| Google Sheet binding/readback | `PREMERGE_RECHECK` |
| Issue·PR authority | `PASS` |
| PR #81 | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |
| 기획 Coverage | `R1 IN_PROGRESS` |
| Grill Me batch 01 | `5 APPROVED / MERGE_REQUESTED` |
| 다음 Grill Me counter | `0/10 AFTER_MERGE` |
| Codex 구현 | `BLOCKED_BY_PLANNING_GATE` |
| Runtime against latest planning | `NOT_RUN` |
| Android 실기기 | `NOT_RUN` |
| 접근성 사람 검토 | `NOT_RUN` |
| 성능 | `NOT_RUN` |
| 외부 플레이테스트 | `NOT_RUN` |

## 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 안에서 작품을 직접 만들고, 강화의 위험 앞에서 멈출지 도전할지 선택하며, 그 작품이 고객과 세계 사건에서 남긴 역사와 반응을 돌려받는 Android 세로형 제작 게임.

현재 승인된 위계:

```text
직접 제작
→ 강화 성공·실패와 멈춤·추가 도전
→ 피로도에 따른 오늘의 작업 우선순위
→ 고객 판매·납품
→ 짧은 세계 사건 결과
→ 작품의 소유·운명·연대기·세트 확인
→ 새로운 작품과 더 높은 강화에 도전
```

## R1 승인 배치 01

| Decision | 확정 내용 |
|---|---|
| `BS-CORE-20260802-01` | 피로도·날짜 진행은 핵심 불변 |
| `BS-CORE-20260802-02` | 강화가 메인, 고객·세계 환류는 휴식과 장기 약속 |
| `BS-SET-20260802-01` | 고객·일정·사건이 다양한 작품과 세트 제작 동기 제공 |
| `BS-SET-20260802-02` | 동일 사건에 실제 기여한 작품이 연대기 세트 성립 |
| `BS-SET-20260802-03` | 범용 보정 + 상황 태그 선택·장면 + 역사 기록 |
| `BS-SET-20260802-04` | 실패·참패도 실제 기여가 있으면 연대기 세트 성립 |

상세 정본:

- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`

## 사건 연대기 세트

```text
세계 일정 공개
→ 역할 확인
→ 고유 작품 제작·강화·납품
→ 사건 결과와 실제 기여 확인
→ 공통 사건 연대기 ID
→ 연대기 세트 성립
→ 범용 보정·상황 태그·역사 요약
→ 유사한 새 사건의 추가 선택지·전용 장면·후속 의뢰
```

- 동일한 세계 일정은 반복되지 않는다.
- 성공 여부와 세트 성립은 분리한다.
- 실패해도 실제 기여가 있으면 기록과 세트가 남는다.
- 보정 수치·누적 상한·태그 유사도·기여 임계치는 `RECOMMENDED_DEFAULT / TEST_VALUE`다.

## 승인 증거가 확인된 기존 제품 기획

- `BS-ART-20260731-01`
- `BS-MODAK-20260731-01`
- `BS-MAIN-20260801-01`
- `BS-SHELL-20260801-01`
- `BS-GRADE-20260801-02`
- `BS-SAVE-20260801-01`

이들은 승인 기획이며 제품 구현·런타임·기기 검증 완료가 아니다.

## 실제 구현 사실

현재 `project.godot`:

```text
run/main_scene="res://scenes/test/enhancement_test.tscn"
```

기존 제작·강화·보관·장비 생애 PoC는 `REFERENCE_IMPLEMENTATION`이다. 최신 피로도·날짜·연대기 세트·Main/Shell/Save 계약의 구현 완료를 의미하지 않는다.

## 보호 경로

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

현재 PR changed files 기준 보호 제품 경로 변경은 `0`이다.

## Grill Me 병합 운영

`BS-OPS-20260802-02`:

1. 이번 누적 5건은 PR #84에서 즉시 병합한다.
2. 병합 후 신규 승인 카운터 `0/10`.
3. 이후 새 승인 10건마다 GitHub·Sheet·PR·리뷰·CI·충돌·금지 경로를 재검증한다.
4. P0/P1 문제가 있으면 병합하지 않는다.
5. 통과 시 squash 병합하고 main SHA를 재동기화한다.

## 현재 사전 감사

확인 완료:

- PR open·mergeable
- branch behind `0`
- changed files는 운영·기획·문서·어댑터 범위
- 보호 제품 경로 변경 `0`
- PR conversation comment `0`

수정 중 발견 사항:

- 루트와 Hub 문서의 `R1 NOT_STARTED` 상태가 최신 승인과 충돌
- PR 본문에 최신 두 Decision 누락
- Current R1 분야 정본의 별도 Registry 필요

위 항목을 정합화한 뒤 Sheet·PR·CI·리뷰를 다시 읽고 병합 판정을 내린다.

## 검증 상한

- 로컬 GitHub checkout/static validator: `BLOCKED_UNVERIFIED` — container DNS 실패
- Godot runtime: `NOT_RUN`
- Android: `NOT_RUN`
- accessibility human: `NOT_RUN`
- performance: `NOT_RUN`
- external playtest: `NOT_RUN`

## 다음 작업

1. current-facing 문서와 Sheet의 최신 Decision·HEAD를 정합화한다.
2. PR changed files·전체 diff·리뷰·CI·mergeability를 재검증한다.
3. P0/P1이 0이면 PR #84를 squash 병합한다.
4. main SHA와 Sheet를 동기화하고 Grill Me 카운터를 `0/10`으로 확정한다.
5. 제품 구현 없이 R1의 남은 기획을 계속한다.
