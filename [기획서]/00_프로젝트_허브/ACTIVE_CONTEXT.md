# Active Context

- 갱신일: `2026-08-02 15:06 KST`
- Work Mode: `TOTAL_PLANNING`
- 현재 운영 Decisions: `BS-OPS-20260802-01`, `BS-OPS-20260802-02`
- 기준 main: `ac120fb146cea29bb5f8876682809f76779d86ad`
- 현재 브랜치: `agent/blacksmith-planning-canon-recovery`
- 현재 Draft PR: `#84`
- 기획 Umbrella: Issue `#79`
- 현재 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE`
- 현재 상태: `CORE_CONFIRMED / CORE_RECORDED / R1_IN_PROGRESS / GRILL_BATCH_01_PREMERGE_AUDIT`
- 제품 구현: `BLOCKED`

## 현재 판정

| 영역 | 상태 |
|---|---|
| Base release adoption | `9.4.0 / COMPLETE` |
| R0 운영·정본 복구 | `PASS_FOR_DRAFT_PR` |
| Root current decisions | `UPDATED_FOR_R1_BATCH_01` |
| Current R1 canon overlay | `CREATED` |
| Google Sheet binding/readback | `PREMERGE_RECHECK` |
| PR #81 | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |
| 기획 Coverage | `R1 IN_PROGRESS` |
| Grill Me batch 01 | `5 APPROVED / MERGE_REQUESTED` |
| 병합 후 Grill Me counter | `0/10` |
| Codex 구현 | `BLOCKED_BY_PLANNING_GATE` |
| Runtime against latest planning | `NOT_RUN` |
| Android·접근성·성능·사람 플레이 | `NOT_RUN` |

## 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 안에서 작품을 직접 만들고, 강화의 위험 앞에서 멈출지 도전할지 선택하며, 그 작품이 고객과 세계 사건에서 남긴 역사와 반응을 돌려받는 Android 세로형 제작 게임.

```text
직접 제작
→ 강화 성공·실패와 멈춤·추가 도전
→ 피로도에 따른 오늘의 작업 우선순위
→ 고객 판매·납품
→ 짧은 세계 사건 결과
→ 작품의 소유·운명·연대기·세트 확인
→ 새로운 작품과 더 높은 강화
```

## R1 승인 배치 01

| Decision | 확정 내용 |
|---|---|
| `BS-CORE-20260802-01` | 피로도·날짜 진행 핵심 불변 |
| `BS-CORE-20260802-02` | 강화가 메인, 고객·세계 환류는 휴식과 장기 약속 |
| `BS-SET-20260802-01` | 다양한 작품과 세트 제작 동기 |
| `BS-SET-20260802-02` | 실제 기여 작품의 사건 연대기 세트 |
| `BS-SET-20260802-03` | 범용 보정 + 상황 태그 + 역사 기록 |
| `BS-SET-20260802-04` | 실패·참패도 실제 기여 시 세트 성립 |

상세 정본:

- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`

## 실제 구현 사실

- 현재 실행 진입: `res://scenes/test/enhancement_test.tscn`
- 기존 장비 생애 PoC 범위: `docs/MVP-003_SCOPE.md`
- 기존 제작·강화·보관·장비 생애 PoC는 `REFERENCE_IMPLEMENTATION`이다.
- 최신 피로도·날짜·연대기 세트·Main/Shell/Save는 아직 구현되지 않았다.

### 과거 강화 데이터 책임 원본

다음 경로는 기존 강화 PoC 구현 데이터의 책임 원본이다. 현행 R1에서 수치가 승인됐다는 뜻은 아니며 R3/R5에서 재검토한다.

- 강화 실패·하락·파괴·재료 소비·연속 실패 보정과 위험 분포: `data/crafting/enhancement_balance.json`
- +10 단위 이정표·특수 강화·수식어 성장 구간: `data/crafting/enhancement_milestones.json`
- `enhancement_milestones.json`은 실패 정책을 소유하지 않으며 실패·위험 계약은 `enhancement_balance.json`이 소유한다.

## 과거 PoC 필수 사실 — 분류된 호환 증거

아래 문자열은 Base 운영·제작 품질 감사가 요구하는 과거 구현 계약이다. 현행 R1 설계의 수치 확정이나 최신 구현 완료를 뜻하지 않는다.

- 최신 역사 PoC 배지: `POC v0.6.4 · main · 2026.07.23.1`.
- 제작 품질 단위 검증 기록: `제작 모델 7건`.
- 제작 결과·강화 연계 검증 기록: `통합 6건`.
- `POC v`: 기존 장비 한 점의 생애 PoC 버전 계열을 가리키는 역사 토큰.
- `자동 단조`: 기존 PoC 반복 보조 기능. 현행 R1에서는 피로도·날짜·강화 판단 우회 여부를 R3/R5에서 재검토한다.
- `+11`: 과거 강화 경계·회귀 검사의 대표 구간 토큰.
- `+30`: 과거 장기 강화 경계·회귀 검사의 대표 구간 토큰.
- `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`: 과거 PoC HEAD에만 적용. 최신 R1 runtime은 `NOT_RUN`.
- `ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED`: 과거 Actions·자동 PR 기능 증거. 현재 check 결과는 HEAD별로 별도 조회한다.
- `PR validation #468`: 과거 검증 실행 참조. 현재 PR #84 check와 동일하지 않다.

## Grill Me 병합 운영

`BS-OPS-20260802-02`:

1. 이번 승인 질문 5건은 PR #84에서 즉시 병합한다.
2. 병합 후 신규 승인 카운터 `0/10`.
3. 이후 새 승인 10건마다 GitHub·Sheet·PR·리뷰·CI·충돌·금지 경로를 재검증한다.
4. P0/P1 문제가 있으면 병합하지 않는다.
5. 통과 시 squash 병합하고 main SHA를 재동기화한다.

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

## 병합 전 감사 현황

수정 완료:

- Root·Hub의 stale R1 상태
- Current R1 canon overlay 부재
- PR 본문 최신 Decision 누락
- core alignment exact-token 누락
- QA Registry mode와 Skill 본문 불일치
- 과거 PoC 필수 assertion·제작 품질 증거 분류 누락
- 강화 실패·위험과 이정표 책임 원본 표기 누락
- PR #81 역사 경로 포인터 누락

잔여 확인:

- 새 HEAD 전체 CI
- Sheet 최신 HEAD bounded readback
- 리뷰·mergeability·expected HEAD

## 검증 상한

- local checkout/static validator: `BLOCKED_UNVERIFIED` — container DNS 실패
- GitHub Actions: 현재 HEAD별로 별도 검증
- 최신 R1 기능 runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## 다음 작업

1. 새 HEAD의 Actions를 재검증한다.
2. Sheet·PR·리뷰·mergeability를 다시 읽는다.
3. P0/P1이 0이면 PR #84를 squash 병합한다.
4. main SHA와 Sheet를 동기화하고 카운터를 `0/10`으로 확정한다.
5. 제품 구현 없이 R1의 남은 기획을 계속한다.
