# Blacksmith R2 체크포인트 004 Postmerge Closure

- 상태: `CLOSURE_PR107 / APPROVED_FOR_EXPECTED_HEAD_MERGE`
- 새 게임 Decision: `NONE`
- 제품 구현: `BLOCKED`

## 대상 Decision

- `BS-CRAFT-20260804-07`: 제작 등급 5단계와 출생 전설
- `BS-CRAFT-20260805-01`: 고정 설계 최대치 없는 숫자형 예술성

## Planning PR 병합 증거

```text
planning_pr: 106
planning_exact_head: 227b2dabf0d98832811415156e72f65d601332a9
planning_merge_sha: 789c73f38003f40dde5e9a99cd7dcb3ca03863f7
merge_method: SQUASH
github_readback: PASS
sheet_readback: PASS
```

병합 전 검증:

- Planning-first `91`: `PASS`
- Base `558`: `PASS`
- PR validation `1149`: `PASS`
- Python 전체 계약: `PASS`
- Godot 4.7.1 headless: `PASS`
- PR comments: `0`
- inline review threads: `0`
- changed protected product paths: `0`

## 폐쇄 상태

```text
R2_CHECKPOINT_004: MAIN_CANON
R2_BATCH_004: CLOSED_MERGED_PR106 / 2_OF_10
closure_reason: USER_APPROVED_EARLY_CHECKPOINT
R2_BATCH_005: ACTIVE / 0_OF_10
```

- 두 Decision의 ID와 계약 내용은 변경하지 않는다.
- `APPROVED_PENDING_MERGE` 상태만 `MERGED_PR106 / MAIN_CANON`으로 닫는다.
- 배치 005는 승인 Decision 없이 `0/10`으로 시작한다.
- 승인 10건은 계속 최대 배치 크기다.
- 제품 구현 Gate는 계속 `BLOCKED`다.

## 폐쇄 TDD

RED:

- commit `276f62d7477ab48521b814c17832ee24c4c6457f`
- PR validation `1150`: `EXPECTED_FAILURE`
- Base `559`: `PASS`
- 실패 원인: PR106 병합 뒤 정본·Registry가 배치 004 활성·pending 상태를 유지함

GREEN과 최종 exact-head 증거는 PR #107 CI가 완료된 후 PR 설명과 Sheet에 기록한다. Registry에는 자기참조를 피하기 위해 closure merge 전 `PENDING_EXPECTED_HEAD_MERGE`를 기록한다.

## 검증 경계

- focused closure/artistry/batch tests standalone: `NOT_RUN`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
- 현재 변경은 정본 상태·라우터·검증 도구에 한정
- 제품 코드·Scene·runtime data·asset 변경 없음
