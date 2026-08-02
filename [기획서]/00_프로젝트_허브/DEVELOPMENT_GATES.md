# Development Gates

## 1. 판정 원칙

- 문서 승인, 기획 완전성, 구현, 자동 테스트, 실제 렌더, Android, 접근성, 성능, 사람 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.
- 과거 PoC PASS는 해당 과거 코드 HEAD의 증거이며 최신 총기획·제품·플랫폼 PASS를 대신하지 않는다.
- 하나 이상의 중요 Gate가 `NOT_RUN`, `FAIL`, `BLOCKED`이면 전체 프로젝트 PASS를 주장하지 않는다.
- 제품 구현은 `PLANNING_AND_REVIEW_COMPLETE_GATE`가 닫힌 뒤 별도 승인 계약으로만 시작한다.

## 2. Current Gate Summary

```yaml
CURRENT_DECISION: BS-OPS-20260802-01
CURRENT_WORK_MODE: TOTAL_PLANNING
CANONICAL_RECOVERY_GATE: IN_PROGRESS
DECISION_AUTHORITY_GATE: IN_PROGRESS
DECISION_SYNC_GATE: IN_PROGRESS
PLANNING_COVERAGE_GATE: NOT_STARTED
GRILL_ME_DECISION_GATE: NOT_STARTED
ADVERSARIAL_FINAL_REVIEW_GATE: NOT_STARTED
USER_PLANNING_COMPLETE_GATE: BLOCKED
USER_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
PRODUCT_MAIN_AND_SHELL_GATE: NOT_IMPLEMENTED
SAVE_AND_RESULT_RECOVERY_GATE: NOT_IMPLEMENTED
LATEST_RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
PRODUCTION_GREENLIGHT_GATE: BLOCKED
```

## 3. R0 Canonical Recovery Gate

### 완료 조건

- [x] 현재 main·브랜치·PR·Decision ID 고정
- [x] 승인된 설계와 실행 계획 기록
- [x] 기준선·운영 Finding 기록
- [x] Root `CURRENT_CONFIRMED_DECISIONS.md` 생성
- [x] `AGENTS`, `START_HERE`, `ACTIVE_CONTEXT` 현행화
- [ ] `DOCUMENTATION_MAP`, `ROADMAP`, Registry 현행화
- [ ] Base Adapter·운영 Health 사실 교정
- [ ] Google Sheet 동일 Decision ID 동기화
- [ ] Issue #60·#79, PR #81·#84 권위 정리
- [ ] 최종 적대적 검토
- [ ] 콜드 스타트 검증
- [ ] exact-HEAD·보호 경로 diff 검증

### 차단 조건

- GitHub와 Sheet의 Decision ID·의미·Commit 불일치
- PR #81 또는 Issue #60이 현행 작업 권위로 해석됨
- 보호 제품 경로 변경
- Base v9.4와 과거 v9.3 이관이 동시에 활성 목표로 남음
- `NOT_RUN` Gate를 PASS로 요약함

현재 상태: `IN_PROGRESS`.

## 4. Decision Authority Gate

### 현행 원칙

- Root `CURRENT_CONFIRMED_DECISIONS.md`가 상태 진입점이다.
- 분야별 상세 계약은 등록된 단일 책임 원본이 가진다.
- Sheet의 `CURRENT`나 `USER_APPROVED` 문자열만으로 승인하지 않는다.
- 승인 증거, 분야 정본, GitHub Commit, Sheet 위치를 연결한다.
- 대체 결정은 `supersedes`와 `replaced_by`를 기록한다.

### 현재 판정

- `BS-OPS-20260802-01`: `APPROVED / GITHUB_RECORDED / SHEET_SYNC_PENDING`
- 승인 증거 확인 제품 Decision 6개: `CONFIRMED / SELECTIVE_PROMOTION_PENDING`
- 나머지 PR #81 상세 계약: `PROPOSED_REVIEW_REQUIRED` 또는 `RESEARCH_OR_TEST_REQUIRED`

현재 상태: `IN_PROGRESS`.

## 5. Decision Sync Gate

`SYNCED` 조건:

```text
같은 Decision ID
+ 같은 의미
+ 같은 상태
+ GitHub 책임 원본 경로
+ 정확한 GitHub Commit SHA
+ Google Sheet Tab·Range
+ 양쪽 재조회 성공
```

- GitHub만 기록: `PARTIAL_SYNC_BLOCKED`
- Sheet만 앞섬: `SYNC_CONFLICT`
- 중간 PR HEAD 사용: `FINAL_HEAD_RECHECK_REQUIRED`

현재 `BS-OPS-20260802-01`: `GITHUB_RECORDED / SHEET_SYNC_PENDING`.

## 6. Planning Coverage Gate

운영 복구 후 다음 Bundle 순서로 닫는다.

1. R1 프로젝트 코어·플레이어 약속
2. R2 Core·Session·Meta Loop
3. R3 제작·강화·작품 정체성·실패·저장
4. R4 고객·세계 환류·장비 연대기
5. R5 경제·성장·장기 목표
6. R6 모바일 UX·접근성·아트·오디오
7. R7 버티컬 슬라이스·데이터·마이그레이션·검증·제작 계획
8. R8 최종 적대적 검토·사용자 검수

각 Bundle은 다음을 포함한다.

```text
현재 승인
→ 실제 구현
→ 공백·충돌
→ 벤치마크·Evidence
→ 권장안과 반증
→ 상세값 RECOMMENDED_DEFAULT/TEST_VALUE
→ 중요 충돌만 Grill Me
→ 정본·소비자·Sheet 동기화
→ Regression Recheck
```

현재 상태: `NOT_STARTED`.

## 7. Grill Me Decision Gate

Grill Me 대상:

- 프로젝트 코어·플레이어 판타지·뾰족한 재미
- 양립 불가능한 주요 시스템·UX·콘텐츠 원칙
- Vertical Slice·데모·본제작 범위
- 주요 실패·파괴·복구·보상 의미
- 기존 승인 Decision 대체
- 플레이 경험·제작 범위가 실질적으로 다른 대안

Grill Me 비대상:

- 저장소·Sheet에서 확인 가능한 사실
- 이미 승인된 동일 결정
- 기술 세부·시험값
- 단순 경로·상태·문서 오류
- 근거가 없는 막연한 취향 질문

현재 검증된 열린 질문: `0`.
현재 상태: `NOT_STARTED`.

## 8. Historical Implementation Baseline

기존 제작·강화·보관·장비 생애 PoC는 실제 구현 사실과 회귀 기준선으로 보존한다.

- 역사적 자동 검증: 해당 당시 코드 HEAD에서 실행됨
- 최신 total-planning 기준 재검증: `NOT_RUN`
- 최신 제품 Main/Shell/Save: `NOT_IMPLEMENTED`
- Android·사람·성능: `NOT_RUN`

이 영역의 상태는 `REFERENCE_IMPLEMENTATION`, 전체 프로젝트 판정은 `INCOMPLETE`다.

## 9. Product Implementation Gate

다음이 모두 닫혀야 Codex 구현 계약을 만들 수 있다.

- [ ] 모든 R1~R7 기획 Coverage가 허용 상태로 닫힘
- [ ] 미해결 `MUST_FIX` 0 또는 사용자 승인 보류 조건 존재
- [ ] 필요한 Grill Me 완료
- [ ] GitHub·Sheet 주요 Decision `SYNCED`
- [ ] 사용자 `기획 완료`
- [ ] 적대적 최종 검수 완료
- [ ] 사용자 `검수 완료`
- [ ] 구현 범위·제외·수용 기준·테스트·롤백 확정
- [ ] 실제 구현 기준선·보호 경로 기록

현재 상태: `BLOCKED`.

## 10. Product and Platform Validation

| Gate | 상태 | 필요한 증거 |
|---|---|---|
| Latest static/contract validation | `NOT_RUN` | current final HEAD validator output |
| Godot import/parse | `NOT_RUN` | current final HEAD import and parse |
| Main and representative Scene smoke | `NOT_RUN` | latest approved product entry and flows |
| Save/load/process-death | `NOT_RUN` | atomic save/recovery tests and Android interruption |
| Android device | `NOT_RUN` | build, install, safe area, touch, back, lifecycle |
| Accessibility | `NOT_RUN` | non-color information, text size, alternative input, human review |
| Performance | `NOT_RUN` | representative and worst-scene profile |
| Human playtest | `NOT_RUN` | task completion, comprehension, fatigue, player choices |
| Build/package | `NOT_RUN` | clean build, package, install, launch, exit |

문서 복구는 위 검증을 통과시키지 않는다.

## 11. Completion Rules

### R0 완료

```yaml
CANONICAL_RECOVERY_GATE: PASS
DECISION_SYNC_GATE: PASS
PLANNING_COVERAGE_GATE: NOT_STARTED
PLANNING_AND_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
```

### 전체 기획 완료

R1~R7 Coverage, 중요 Decision, 동기화, 적대적 검토, 사용자 검수가 닫혀야 한다.

### Demo 완료

승인된 범위의 실제 구현, 자동 검증, Android, 접근성, 성능, 사람 플레이, Build·패키징 증거가 있어야 한다. 문서와 과거 PoC PASS만으로 Demo Ready를 선언하지 않는다.
