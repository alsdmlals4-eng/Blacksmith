# Blacksmith AI 작업 규칙

Blacksmith는 Google Play 출시를 우선하는 Android 세로형 Godot 게임 프로젝트다. 현재 단계는 **제품 구현이 아니라 총기획 작성·승인 배치 관리·정본 동기화**다.

## 1. 현재 작업 계약

```yaml
CURRENT_WORK_MODE: TOTAL_PLANNING
CURRENT_OPERATING_DECISIONS:
  - BS-OPS-20260802-01
  - BS-OPS-20260802-02
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
CURRENT_STAGE_STATUS: IN_PROGRESS / GRILL_BATCH_01_PREMERGE_AUDIT
CURRENT_BRANCH: agent/blacksmith-planning-canon-recovery
CURRENT_DRAFT_PR: 84
PRODUCT_IMPLEMENTATION: BLOCKED
PRIMARY_PLATFORM: ANDROID_PORTRAIT_MOBILE
PC: FUTURE_PLATFORM_CONSIDERATION
```

현재 제품 코드·Scene·런타임 데이터·에셋을 변경하지 않는다. 총기획, 적대적 최종 검수, 사용자 검수 완료 후에만 별도 Codex 구현 계약을 연다.

## 2. 사실·권한 우선순위

1. 사용자의 최신 지시와 승인
2. 이 문서와 보안·엔진·데이터 규칙
3. `CURRENT_CONFIRMED_DECISIONS.md`
4. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
5. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
6. 등록된 분야별 책임 원본
7. 실제 코드·data·Scene·Resource·assets·tests
8. `skills/PROJECT_BASE_ADAPTER.json`과 Base v9.4 운영 정본
9. Google Sheet·PDF·Dashboard 같은 연결 Surface와 파생본
10. 외부 벤치마크·과거 대화·AI 추론

GitHub가 기획 권위 원본이다. Google Sheet는 사용자용 기획·운영 Surface이며 같은 Decision ID·GitHub 경로·Commit을 기록한다.

## 3. 시작 순서

```text
AGENTS.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ docs/planning/CURRENT_R1_CANON_REGISTRY.json
→ [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md
→ DEVELOPMENT_GATES.md
→ ROADMAP.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ SKILL_REGISTRY.json
→ 현재 기획 Bundle·분야 정본
→ 필요한 실제 구현·데이터·테스트
```

PR #81은 `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`다. 전체 병합하거나 PR #81의 `CURRENT` 표기를 자동 승인으로 사용하지 않는다.

## 4. Work Mode와 Skill

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
- 병합 전 PR·Sheet·권위 문서 재검토

Skill은 Registry trigger에 따라 최소 집합만 선택한다. 전체 Skill 무차별 로드는 금지한다.

## 5. Grill Me와 병합 배치

Grill Me는 다음에만 한 질문씩 사용한다.

- 프로젝트 코어·플레이어 판타지·뾰족한 재미 변경
- 양립할 수 없는 주요 시스템·UX·콘텐츠 원칙
- 버티컬 슬라이스·본제작 범위 선택
- 주요 실패·파괴·복구·보상 의미 변경
- 기존 승인 Decision 대체
- 대안별 플레이 경험·제작 범위가 실질적으로 다른 경우

비대상:

- 저장소·Sheet에서 확인할 수 있는 사실
- 이미 승인된 결정
- 기술 세부·시험값
- 경로·상태·문서 오류
- 적대적 검토 전 막연한 취향 질문

병합 규칙 `BS-OPS-20260802-02`:

1. 이번 Grill Me 1~5는 PR #84에서 즉시 병합한다.
2. 병합 후 신규 승인 카운터를 `0/10`으로 초기화한다.
3. 이후 새 승인 10건마다 한 배치로 묶는다.
4. 10번째 승인 직후 GitHub·Sheet·PR changed files·리뷰·CI·충돌·금지 경로를 적대적으로 재검증한다.
5. P0/P1 문제 발생 시 병합을 중단한다.
6. 감사 통과 후 원칙적으로 squash 병합하고 main SHA를 재동기화한다.

## 6. 현재 승인된 R1 방향

- 피로도·날짜는 제한된 하루의 우선순위와 세계 일정을 연결하는 핵심 불변.
- 강화 성공·실패와 멈춤·추가 도전이 메인 반복 재미.
- 고객 납품·짧은 사건 결과는 강화 사이의 휴식·세계 환류.
- 여러 종류의 작품은 고객 역할·세계 일정·사건·관계가 제작 이유를 제공.
- 같은 사건에 실제 기여한 작품들이 사건 연대기 세트가 됨.
- 세트는 범용 보정 + 상황 태그 선택·장면 + 짧은 역사 기록을 제공.
- 성공·부분 성공·실패·참패 모두 실제 기여가 있으면 연대기 세트 성립.

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

보호할 프로젝트 강점:

- 한 명의 대장장이와 장비 한 점 중심 경험
- 직접 제작과 강화 위험 선택
- 일반 강화 입력당 결과 1회
- 장비 UID·소유권·운명·연대기
- 판매·인계 이후 세계 결과와 연대기 세트
- 모바일에서 기억·비교 가능한 작품 정체성
- 스타일라이즈드 다크 포지와 밝은 불 정령 모닥
- 미실행 검증을 PASS로 표시하지 않는 원칙

승인 없이 추가·변경 금지:

- 직원·복수 대장장이 중심 운영
- 플레이어 직접 전투
- 생산 예약·대기열 중심 전환
- 일상적 수리 관리
- 승인 Decision 제거·대체
- PC 동시 출시 범위 확장
- 결제·광고·서버 구현

## 8. 기술 기준

- Godot 4.7 / GDScript
- Android 세로형 모바일 우선
- 기준 뷰포트 720×1280, 다양한 비율 Expand 대응
- 출시 빌드 목표 Android App Bundle
- 안전 영역·터치·작은 화면 가독성 우선
- 실제 Android 증거 전 모바일 검증 완료 금지

현재 `project.godot` 실행 진입은 `res://scenes/test/enhancement_test.tscn`이다. 승인된 Main Menu·BlacksmithApp·Save 계약은 아직 제품 구현이 아니다.

## 9. 정본과 상태 규칙

- 한 질문에는 활성 책임 원본 하나만 둔다.
- 서술 기획은 Markdown, ID·수치·관계·게임 데이터는 JSON이 책임진다.
- 실제 구현은 Scene·Script·Resource·data가 책임진다.
- 완료 증거는 정확한 현재 HEAD의 테스트·실행·캡처·프로파일·사람 검수가 책임진다.
- 문서 존재 ≠ 사용자 승인 ≠ 구현 ≠ 검증 ≠ 출시 준비.
- 과거 자동 검증은 해당 과거 HEAD의 증거일 뿐 최신 총기획 PASS가 아니다.
- 생성 호환 뷰는 generator 계약 없이 수동 편집하지 않는다.

## 10. Decision 즉시 동기화

```text
Decision ID 생성 또는 재사용
→ GitHub 분야 정본·CURRENT_CONFIRMED_DECISIONS 갱신
→ Commit과 경로 기록
→ 연결 Google Sheet에 같은 ID·상태·요약·경로·Commit 반영
→ GitHub와 Sheet 재조회
→ 의미·상태·Commit 일치 시 SYNCED
```

`PARTIAL_SYNC_BLOCKED` 또는 `SYNC_CONFLICT`이면 다음 주요 Bundle이나 병합으로 진행하지 않는다.

## 11. 검증 상태

검증은 독립적으로 기록한다.

- 문서·계약
- 정적·포맷
- 자동 테스트
- Godot import·런타임
- Android 실기기
- 접근성 사람 검토
- 성능
- 외부 플레이
- GitHub·Sheet readback

실행하지 못한 항목은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다. 하나의 PASS를 다른 계층으로 확대하지 않는다.

현재 전체 기획 완료와 Codex 준비는 `BLOCKED`다.
