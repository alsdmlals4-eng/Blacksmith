# Blacksmith 시작 지점

## 프로젝트 보호 방향

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화의 위험 앞에서 멈출지 도전할지 선택하며, 제한된 하루와 세계 일정 속에서 그 작품이 다른 이의 손에서 쌓은 역사와 세계의 반응을 돌려받는 Android 세로형 제작 게임.

## 현재 상태

```yaml
CURRENT_OPERATING_DECISIONS:
  - BS-OPS-20260802-01
  - BS-OPS-20260802-02
WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
R1_STATUS: IN_PROGRESS / GRILL_BATCH_01_PREMERGE_AUDIT
BASE_MAIN: ac120fb146cea29bb5f8876682809f76779d86ad
BRANCH: agent/blacksmith-planning-canon-recovery
DRAFT_PR: 84
PLANNING_UMBRELLA: ISSUE_79
PR_81: REFERENCE_ONLY_SUPERSEDED_AS_MERGE_UNIT
BASE_RELEASE: 9.4.0_ADOPTED
GITHUB_SHEET_SYNC: PREMERGE_RECHECK
PRODUCT_IMPLEMENTATION: BLOCKED
NEXT_ACTIVITY: MERGE_BATCH_01_THEN_CONTINUE_R1
```

## 실제 구현 기준선

- 현재 `project.godot` 실행 진입은 `res://scenes/test/enhancement_test.tscn`이다.
- 기존 제작·강화·보관·장비 생애 PoC는 실제 구현 사실과 회귀 기준선이다.
- 승인된 Main Menu, `BlacksmithApp`, 최신 Save/ResultEnvelope, 피로도·날짜·연대기 세트는 아직 제품 구현이 아니다.
- 최신 총기획 기준 Godot runtime, Android 실기기, 접근성, 성능, 사람 플레이는 `NOT_RUN`이다.

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
4. 이 문서
5. `ACTIVE_CONTEXT.md`
6. `DEVELOPMENT_GATES.md`
7. `ROADMAP.md`
8. `DESIGN_DOCUMENT_REGISTRY.json` — 광역 R0 publication index
9. `SKILL_REGISTRY.json`
10. 현재 R1 분야 정본
11. 필요한 실제 코드·data·Scene·tests

## 현재 R1 승인 정본

- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`

승인된 핵심:

- 피로도·날짜 진행은 핵심 불변.
- 강화 성공·실패와 멈춤·추가 도전이 메인 반복 재미.
- 방문 고객 납품과 사건 결과는 휴식·세계 환류.
- 세계 일정과 고객 역할이 다양한 작품 제작 이유를 제공.
- 실제 기여 작품이 동일 사건 연대기 세트로 성립.
- 범용 보정 + 상황 태그 선택·전용 장면 + 역사 기록.
- 실패·참패도 실제 기여가 있으면 세트와 연대기를 남김.

R1 전체 완료는 아니다. 타깃 플레이어·세일즈포인트·성공/실패 기준·나머지 중요 충돌은 계속 기획한다.

## Grill Me 병합 운영

- 이번 승인 5건은 PR #84 사전 감사 후 즉시 squash 병합.
- 병합 후 신규 승인 카운터 `0/10`.
- 이후 새 승인 10건마다 GitHub·Sheet·PR·리뷰·CI·충돌·금지 경로를 적대적으로 재검증하고 병합.
- P0/P1 문제가 있으면 병합 금지.

## 현재 운영 규칙

- 기획 작성부터 진행한다.
- 상세 기술값·초기 수치는 `RECOMMENDED_DEFAULT / TEST_VALUE`로 제안한다.
- 중요 기획·검증된 충돌만 한 질문씩 Grill Me로 묻는다.
- 저장소나 Sheet에서 확인 가능한 사실과 승인 결정은 다시 묻지 않는다.
- 주요 승인 Decision은 GitHub와 Google Sheet에 같은 ID로 즉시 동기화한다.
- R8 사용자 검수 완료 전 제품 구현과 Codex Build를 시작하지 않는다.

## 보호 경로

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

## 권위 관계

```text
Issue #79 = 총기획 Umbrella
PR #84 = R0 복구 + R1 승인 배치 01 병합 PR
PR #81 = 선별 승격용 기획·승인 Evidence
Issue #60 = 과거 Base v6 재기획 이력
```

## 다음 작업

1. PR #84의 최종 사전 감사를 완료한다.
2. 통과 시 squash 병합하고 main SHA·Sheet·카운터를 재동기화한다.
3. 제품 구현 없이 R1의 남은 프로젝트 코어·플레이어 약속 기획을 계속한다.
