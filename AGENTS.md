# Blacksmith AI 작업 규칙

Blacksmith는 Google Play 출시를 우선하는 Android 세로형 Godot 게임 프로젝트다. 현재 단계는 **제품 구현이 아니라 총기획 작성·승인 배치 관리·정본 동기화**다.

## 1. 현재 작업 계약

```yaml
CURRENT_WORK_MODE: TOTAL_PLANNING
CURRENT_OPERATING_DECISIONS:
  - BS-OPS-20260802-01
  - BS-OPS-20260802-02
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
CURRENT_STAGE_STATUS: IN_PROGRESS / GRILL_BATCH_01_MERGED / NEW_COUNTER_0_OF_10
CURRENT_BRANCH: main
PLANNING_BATCH_PR: 84
PLANNING_BATCH_MERGE_SHA: bd68c2dbf20592e84c1bebfdc83c4c925d010dbf
POSTMERGE_SYNC_PR: 85
POSTMERGE_SYNC_SHA: 338d256c7ffbf976473d04712ff9426f1e450d2c
EXACT_CURRENT_MAIN_SHA_AUTHORITY: GOOGLE_SHEET_AND_ISSUE_79
PRODUCT_IMPLEMENTATION: BLOCKED
PRIMARY_PLATFORM: ANDROID_PORTRAIT_MOBILE
PC: FUTURE_PLATFORM_CONSIDERATION
```

## 2. 권위 우선순위

1. 사용자의 최신 지시와 승인
2. 이 문서
3. `CURRENT_CONFIRMED_DECISIONS.md`
4. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
5. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
6. 등록된 분야별 책임 원본
7. 실제 코드·data·Scene·Resource·assets·tests
8. `skills/PROJECT_BASE_ADAPTER.json`과 Base v9.4 운영 정본
9. 연결된 Google Sheet와 파생 Surface
10. 외부 벤치마크·과거 대화·AI 추론

GitHub가 기획 권위 원본이다. Google Sheet는 사용자용 GDD·Decision·Audit Surface이며 동일 Decision ID와 최종 main SHA를 기록한다.

## 3. 시작 순서

```text
AGENTS.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ docs/planning/CURRENT_R1_CANON_REGISTRY.json
→ START_HERE.md
→ ACTIVE_CONTEXT.md
→ DEVELOPMENT_GATES.md
→ ROADMAP.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ SKILL_REGISTRY.json
→ 현재 분야 정본
→ 실제 구현·data·tests
```

PR #81은 `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`, PR #84는 `MERGED / BATCH_01_CANON`, PR #85는 `MERGED / POSTMERGE_SYNC`다.

## 4. 작업 루프

```text
REVIEW
→ PLAN
→ 승인된 기획·문서 BUILD
→ REVIEW
```

필수 절차:

- 프로젝트 기준선과 보호 강점 복원
- brainstorming 후 설계
- 적대적 검토 `Attack → Validate Critique → Regression Recheck`
- 다단계 변경 전 계획
- 완료 주장 전 fresh verification
- 병합 전 GitHub·Sheet·PR·리뷰·CI·충돌 재검토

## 5. Grill Me와 병합 배치

Grill Me는 프로젝트 코어, 플레이어 판타지, 양립 불가능한 주요 시스템, 버티컬 슬라이스 범위, 실패·파괴·복구·보상 의미, 기존 승인 대체처럼 플레이 경험이 실질적으로 달라지는 중요 충돌에만 한 질문씩 사용한다.

`BS-OPS-20260802-02`:

1. Grill Me 배치 01의 승인 질문 5건은 PR #84로 squash 병합 완료했다.
2. 현재 신규 승인 카운터는 `0/10`이다.
3. 이후 새 승인 10건마다 한 배치로 묶는다.
4. 10번째 승인 직후 GitHub·Sheet·changed files·리뷰·CI·충돌·금지 경로를 적대적으로 재검증한다.
5. P0/P1 문제 발생 시 병합을 중단한다.
6. 감사 통과 후 squash 병합하고 최종 main SHA를 Sheet와 Issue #79에 기록한다.

## 6. 현재 승인된 R1 방향

- 피로도·날짜는 제한된 하루의 우선순위와 세계 일정을 연결하는 핵심 불변.
- 강화 성공·실패와 멈춤·추가 도전이 메인 반복 재미.
- 고객 납품·짧은 사건 결과는 강화 사이의 휴식·세계 환류.
- 고객 역할·세계 일정·사건·관계가 다양한 작품 제작 이유를 제공.
- 같은 사건에 실제 기여한 작품들이 사건 연대기 세트가 됨.
- 세트는 범용 보정 + 상황 태그 선택·장면 + 짧은 역사 기록을 제공.
- 성공·부분 성공·실패·참패 모두 실제 기여가 있으면 세트 성립.

상세 정본:

- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`

## 7. 보호 경계

현재 기획·문서 작업에서 변경 금지:

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

보호 대상:

- 한 명의 대장장이와 장비 한 점 중심 경험
- 직접 제작과 강화 위험 선택
- 일반 강화 입력당 결과 1회
- 장비 UID·소유권·운명·연대기
- 판매·인계 이후 세계 결과와 연대기 세트
- Android portrait·한 손 가독성
- 스타일라이즈드 다크 포지와 밝은 불 정령 모닥
- 미실행 검증을 PASS로 표시하지 않는 원칙

## 8. 기술·상태 기준

- Godot 4.7 / GDScript
- Android 세로형 모바일 우선
- 기준 뷰포트 720×1280, Expand 대응
- 현재 `project.godot` 실행 진입: `res://scenes/test/enhancement_test.tscn`
- 기존 PoC: `REFERENCE_IMPLEMENTATION`
- 최신 Main Menu·BlacksmithApp·Save·피로도·날짜·연대기 세트: 제품 구현 전

문서 존재 ≠ 사용자 승인 ≠ 구현 ≠ 검증 ≠ 출시 준비다.

## 9. Decision 동기화

```text
Decision ID
→ GitHub 분야 정본·Root 갱신
→ Commit·경로 기록
→ Google Sheet 동일 ID 반영
→ GitHub·Sheet 재조회
→ 의미·상태·Commit 일치 시 SYNCED
```

`PARTIAL_SYNC_BLOCKED` 또는 `SYNC_CONFLICT`이면 다음 주요 배치나 병합으로 진행하지 않는다.

## 10. 검증 상태

- 배치 01 premerge adversarial audit: `PASS`
- PR #84·#85 squash merge: `PASS`
- Google Sheet postmerge bounded readback: `PASS`
- Base v9 adoption·Python contracts·기존 Reference Godot contracts: `PASS`
- 최신 R1 제품 기능 구현: `BLOCKED`
- Android·접근성·성능·외부 사람 플레이: `NOT_RUN`

현재 전체 기획 완료와 Codex 준비는 `BLOCKED`이며 다음 활동은 R1 기획 계속이다.
