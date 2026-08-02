# Blacksmith 시작 지점

## 프로젝트 보호 방향

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화의 위험 앞에서 멈출지 도전할지 선택하며, 그 작품이 다른 이의 손에서 쌓은 역사와 세계의 반응을 돌려받는 Android 세로형 제작 게임.

## 현재 상태

```yaml
CURRENT_DECISION: BS-OPS-20260802-01
WORK_MODE: TOTAL_PLANNING
R0_CANONICAL_RECOVERY: PASS_FOR_DRAFT_PR
BASE_MAIN: ac120fb146cea29bb5f8876682809f76779d86ad
BRANCH: agent/blacksmith-planning-canon-recovery
DRAFT_PR: 84
PLANNING_UMBRELLA: ISSUE_79
PR_81: REFERENCE_ONLY_SUPERSEDED_AS_MERGE_UNIT
ISSUE_60: HISTORY_ONLY_CANDIDATE
BASE_RELEASE: 9.4.0_ADOPTED
GITHUB_SHEET_SYNC: PASS
PRODUCT_IMPLEMENTATION: BLOCKED
NEXT_BUNDLE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
```

## 실제 구현 기준선

- 현재 `project.godot` 실행 진입은 `res://scenes/test/enhancement_test.tscn`이다.
- 기존 제작·강화·보관·장비 생애 PoC는 실제 구현 사실과 회귀 기준선으로 보존한다.
- 승인된 별도 Main Menu, 단일 `BlacksmithApp`, 최신 Save/ResultEnvelope는 아직 제품 구현이 아니다.
- 최신 총기획 기준 Godot runtime, Android 실기기, 접근성, 성능, 사람 플레이는 `NOT_RUN`이다.

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. 이 문서
4. `ACTIVE_CONTEXT.md`
5. `DOCUMENTATION_MAP.md`
6. `DEVELOPMENT_GATES.md`
7. `ROADMAP.md`
8. `DESIGN_DOCUMENT_REGISTRY.json`
9. `SKILL_REGISTRY.json`
10. `docs/operations/BS-OPS-20260802-01_FINAL_REPORT.md`
11. 현재 R1 기획 Bundle과 분야 정본
12. 필요한 실제 코드·데이터·Scene·테스트

## 현재 운영 규칙

- 기획 작성부터 진행한다.
- 상세 기술값·초기 수치는 `RECOMMENDED_DEFAULT` 또는 `TEST_VALUE`로 제안한다.
- 중요 기획·검증된 충돌만 한 질문씩 Grill Me로 묻는다.
- 저장소나 Sheet에서 확인할 수 있는 사실과 이미 승인된 결정은 다시 묻지 않는다.
- 주요 승인 Decision은 GitHub와 Google Sheet에 같은 ID로 즉시 동기화한다.
- R8 사용자 검수 완료 전 제품 구현과 Codex Build를 시작하지 않는다.

## 보호할 강점

- 한 명의 대장장이와 장비 한 점 중심 경험
- 직접 제작과 강화 위험 선택
- 일반 강화 입력당 결과 1회
- 장비 UID·소유권·운명·연대기
- 판매·인계 이후 세계 결과
- 모바일에서 읽을 수 있는 작품 정체성
- 스타일라이즈드 다크 포지와 밝은 불 정령 모닥
- 미실행 검증을 PASS로 표시하지 않음

총기획 중 변경 금지:

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

## 승인 증거가 확인된 제품 기획

- `BS-ART-20260731-01`
- `BS-MODAK-20260731-01`
- `BS-MAIN-20260801-01`
- `BS-SHELL-20260801-01`
- `BS-GRADE-20260801-02`
- `BS-SAVE-20260801-01`

기획 승인과 구현·검증 완료는 별개다.

## 권위 관계

```text
Issue #79 = 총기획 Umbrella
PR #84 = 현재 운영·정본 복구 Draft
PR #81 = 선별 승격용 기획·승인 Evidence
Issue #60 = 과거 Base v6 재기획 이력
```

## 다음 작업

`R1 Project Core and Player Promise`에서 타깃 플레이어, 플레이 상황, 플레이어 약속, 뾰족한 재미, 핵심 고민, 비타협 조건, 변경 가능한 외피, 제외 범위, 성공·실패 기준을 작성한다.

벤치마크와 반증을 함께 검토하고, 실제 중요한 충돌이 확인될 때만 한 건의 Grill Me를 연다.
