# Blacksmith AI 작업 규칙

Blacksmith는 Google Play 출시를 우선하는 Android 세로형 Godot 게임 프로젝트다. 현재 단계는 **제품 구현이 아니라 총기획 작성과 정본 복구**다.

## 1. 현재 작업 계약

```yaml
CURRENT_WORK_MODE: TOTAL_PLANNING
CURRENT_DECISION: BS-OPS-20260802-01
CURRENT_BRANCH: agent/blacksmith-planning-canon-recovery
CURRENT_DRAFT_PR: 84
PRODUCT_IMPLEMENTATION: BLOCKED
NEXT_PLANNING_BUNDLE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
PRIMARY_PLATFORM: ANDROID_PORTRAIT_MOBILE
PC: FUTURE_PLATFORM_CONSIDERATION
```

현재 제품 코드·Scene·런타임 데이터·에셋을 변경하지 않는다. 기획 작성, 적대적 검토, 사용자 기획 완료, 최종 검수, 사용자 검수 완료 뒤에만 별도 Codex 구현 계약을 연다.

## 2. 사실·권한 우선순위

1. 사용자의 최신 지시와 승인
2. 이 문서와 저장소 보안·엔진·데이터 규칙
3. `CURRENT_CONFIRMED_DECISIONS.md`
4. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`와 현행 Approval Bundle
5. 등록된 분야별 책임 원본
6. 실제 코드·데이터·Scene·Resource·에셋·테스트
7. `skills/PROJECT_BASE_ADAPTER.json`과 `docs/BASE_RULES_VERSION.md`
8. Base v9.4 현행 운영 정본과 등록된 Skill
9. Google Sheet·PDF·Dashboard 같은 연결 Surface와 파생본
10. 외부 벤치마크·과거 대화·AI 추론

GitHub가 기획 권위 원본이다. Google Sheet는 사용자용 기획·운영 Surface이며 같은 Decision ID와 GitHub 위치·Commit을 기록한다.

## 3. 시작 순서

```text
AGENTS.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ SKILL_REGISTRY.json
→ 현재 기획 Bundle·분야 정본
→ 실제 구현·데이터·테스트
```

PR #81은 `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`다. 전체 병합하거나 PR #81의 `CURRENT` 표기를 자동 승인으로 사용하지 않는다. 승인 증거와 현재 코어에 부합하는 항목만 별도 Bundle에서 선별 승격한다.

## 4. Work Mode와 Skill

현재 총기획 생명주기는 다음을 따른다.

```text
REVIEW
→ PLAN
→ 승인된 기획·문서 BUILD
→ REVIEW
```

필수 공통 절차:

- 프로젝트 기준선과 보호 강점 복원
- 적대적 검토 `Attack → Validate Critique → Regression Recheck`
- 주요 기획 개선 전 brainstorming
- 다단계 변경 전 writing-plans
- 완료 주장 전 verification-before-completion
- 주요 결과·PR 완료 전 code/document review

Skill은 `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`의 Trigger에 따라 최소 집합만 선택한다. 전체 Skill 무차별 로드는 금지한다.

## 5. Grill Me 규칙

다음에만 한 질문씩 Grill Me를 사용한다.

- 프로젝트 코어·플레이어 판타지·뾰족한 재미를 바꾸는 선택
- 양립할 수 없는 주요 시스템·UX·콘텐츠 원칙
- 버티컬 슬라이스·데모·본제작 범위를 다르게 만드는 선택
- 주요 실패·파괴·복구·보상 의미를 바꾸는 선택
- 기존 승인 Decision의 대체
- 대안별 플레이 경험·제작 범위가 실질적으로 다른 경우

금지:

- 저장소·Sheet에서 확인할 수 있는 사실 질문
- 이미 승인된 결정 재질문
- 기술 세부·시험값 질문
- 한 번에 여러 독립 결정 질문
- 적대적 검토 전 막연한 선호 인터뷰

상세 수치·기술 기본값·초기 밸런스값은 방향을 바꾸지 않는 범위에서 GPT 권장안을 사용하고 `RECOMMENDED_DEFAULT` 또는 `TEST_VALUE`로 기록한다.

## 6. 보호 경계

### 현재 기획·문서 작업에서 변경 금지

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

### 보호할 프로젝트 강점

- 한 명의 대장장이와 장비 한 점 중심 경험
- 직접 제작과 강화 위험 선택
- 일반 강화 입력당 결과 1회
- 장비 UID·소유권·운명·연대기
- 판매·인계 이후 세계 결과 환류
- 모바일에서 기억·비교 가능한 작품 정체성
- 스타일라이즈드 다크 포지와 밝은 불 정령 모닥
- 미실행 검증을 PASS로 표시하지 않는 원칙

### 승인 없이 추가·변경 금지

- 직원·복수 대장장이 중심 운영
- 플레이어 직접 전투
- 생산 예약·대기열 중심 전환
- 일상적 수리 관리
- 승인 결정 제거·대체
- PC 동시 출시 범위 확장
- 결제·광고·서버 구현

## 7. 기술 기준

- Godot 4.7 / GDScript
- Android 세로형 모바일 우선
- 기준 뷰포트 720×1280, 다양한 비율 Expand 대응
- 출시 빌드 목표 Android App Bundle
- 안전 영역·터치·작은 화면 가독성 우선
- 실제 Android 기기 증거 전 모바일 검증 완료 금지

현재 `project.godot`의 실행 진입은 `res://scenes/test/enhancement_test.tscn`이다. 이는 실제 구현 사실이며 승인된 별도 메인·단일 App Shell이 구현됐다는 뜻이 아니다.

## 8. 정본과 상태 규칙

- 한 질문에는 활성 책임 원본 하나만 둔다.
- 서술 기획은 Markdown, ID·수치·관계·게임 데이터는 JSON이 책임진다.
- 실제 구현은 Scene·Script·Resource·데이터가 책임진다.
- 완료 증거는 정확한 현재 HEAD의 테스트·실행·캡처·프로파일·사람 검수가 책임진다.
- 문서 존재 ≠ 사용자 승인 ≠ 구현 ≠ 검증 ≠ 출시 준비.
- 과거 자동 검증은 해당 과거 코드 HEAD의 증거일 뿐 최신 총기획의 PASS가 아니다.
- 생성 호환 뷰는 generator 계약 없이 수동 편집하지 않는다.

## 9. Decision 즉시 동기화

주요 변경이나 사용자 승인이 발생하면 같은 작업 흐름에서 수행한다.

```text
Decision ID 생성 또는 재사용
→ GitHub 분야 정본·CURRENT_CONFIRMED_DECISIONS·Plan 갱신
→ Commit과 경로 기록
→ 연결 Google Sheet에 같은 ID·상태·요약·경로·Commit 반영
→ GitHub와 Sheet 재조회
→ 의미·상태·Commit 일치 시 SYNCED
```

`PARTIAL_SYNC_BLOCKED` 또는 `SYNC_CONFLICT`이면 다음 주요 기획 Bundle로 진행하지 않는다.

## 10. 검증 상태

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

## 11. 완료 조건

운영 복구 완료에는 다음이 필요하다.

- 현재 Decision·단계·PR·다음 작업을 저장소만으로 찾을 수 있음
- Base v9.4와 프로젝트 운영 상태가 분리돼 정확히 기록됨
- PR #81·Issue #60의 역사/참조 경계가 명확함
- GitHub와 Sheet가 `BS-OPS-20260802-01`로 일치함
- 제품 보호 경로 변경 0
- 적대적 검토에서 미해결 운영 `MUST_FIX` 0

전체 기획 완료와 Codex 준비는 별도 Gate다. 현재는 `BLOCKED`다.
