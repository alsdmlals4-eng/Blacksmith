# Blacksmith 시작 지점

## 프로젝트 보호 방향

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화의 위험 앞에서 멈출지 도전할지 선택하며, 제한된 하루와 세계 일정 속에서 그 작품이 다른 이의 손에서 쌓은 역사와 세계의 반응을 돌려받는 Android 세로형 제작 게임.

핵심 작품 기록 범위는 **장비의 출생·성장·소유·사건 기록**이다.

## 현재 상태

```yaml
CURRENT_OPERATING_DECISIONS:
  - BS-OPS-20260802-01
  - BS-OPS-20260802-02
WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
R1_STATUS: IN_PROGRESS / GRILL_BATCH_01_MERGED / NEW_COUNTER_0_OF_10
CORE_STATUS: CORE_CONFIRMED / R1_BATCH_01_MERGED
MAIN_BATCH_01_SHA: bd68c2dbf20592e84c1bebfdc83c4c925d010dbf
LAST_MERGED_PR: 84
PRODUCT_IMPLEMENTATION: BLOCKED
NEXT_ACTIVITY: CONTINUE_R1_PROJECT_CORE_AND_PLAYER_PROMISE
```

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
4. 이 문서
5. `ACTIVE_CONTEXT.md`
6. `DEVELOPMENT_GATES.md`
7. `ROADMAP.md`
8. `DESIGN_DOCUMENT_REGISTRY.json`
9. 현재 R1 분야 정본
10. 필요한 실제 구현·data·Scene·tests

## 현재 R1 승인 정본

- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`

승인·병합된 방향:

- 피로도·날짜 진행은 핵심 불변.
- 강화 성공·실패와 멈춤·추가 도전이 메인 반복 재미.
- 방문 고객 납품과 사건 결과는 휴식·세계 환류.
- 고객 역할·세계 일정이 다양한 작품 제작 이유를 제공.
- 실제 기여 작품이 같은 사건 연대기 세트로 성립.
- 세트는 범용 보정, 상황 태그 선택·전용 장면, 역사 기록을 제공.
- 실패·참패도 실제 기여가 있으면 연대기와 세트를 남긴다.

R1 전체 완료는 아니다. 타깃 플레이어·세일즈포인트·성공/실패 기준과 남은 중요 충돌을 계속 기획한다.

## 실제 구현 기준선

- 현재 `project.godot` 실행 진입은 `res://scenes/test/enhancement_test.tscn`이다.
- 기존 제작·강화·보관·장비 생애 PoC는 실제 구현 사실과 회귀 기준선이다.
- 최신 Main Menu·BlacksmithApp·Save·피로도·날짜·연대기 세트는 아직 제품 구현이 아니다.
- 최신 R1 제품 기능 기준 Android, 접근성, 성능, 사람 플레이는 `NOT_RUN`이다.

## Grill Me 병합 운영

- 배치 01의 승인 질문 5건은 PR #84로 squash 병합 완료했다.
- 현재 신규 승인 카운터는 `0/10`이다.
- 이후 새 승인 10건마다 GitHub·Sheet·PR·리뷰·CI·충돌·금지 경로를 다시 감사한다.
- P0/P1 문제가 있으면 병합하지 않는다.

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

- Issue #79: 총기획 Umbrella
- PR #84: `MERGED / R0_RECOVERY_AND_R1_BATCH_01_CANON`
- PR #81: `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`
- Issue #60과 PR #35: 역사 자료

## Historical CI compatibility evidence

아래 문자열은 기존 `check_project_core_alignment.py`와 과거 PoC 증거의 호환성을 위한 분류된 기록이다. 최신 R1 제품 구현 상태를 뜻하지 않는다.

- `CORE_CONFIRMED`: R1 코어 승인 배치가 기록됐다는 뜻이며 R1 전체 완료가 아니다.
- `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`: 과거 장비 생애 PoC HEAD에만 적용된 역사 상태. 최신 R1 runtime은 `NOT_RUN`이다.
- `ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED`: 과거 CI·PR 운영 기능의 증거 토큰.
- `#35`: 구형 PR 진입점의 역사 참조이며 최근 병합 PR은 #84다.

## 다음 작업

1. postmerge sync PR을 검증·병합해 현재 상태를 main에 고정한다.
2. 신규 Grill Me 카운터 `0/10`에서 R1의 남은 기획을 계속한다.
3. 제품 구현은 계속 차단한다.
