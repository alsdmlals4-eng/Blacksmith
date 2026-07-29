# Blacksmith UX/UI Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Blacksmith의 재기획 Gate를 침범하지 않으면서 제작·강화·장비 비교 UX의 검증 가설, fixture, 사람 테스트 기준과 후속 Android 실행 조건을 고정한다.

**Architecture:** 현재 단계에서는 `PLANNING_ONLY_PROFILE`의 검증 계약만 작성한다. Issue #60에서 새 프로젝트 코어와 Vertical Slice가 승인된 뒤에만 기존 Godot 구현을 재사용 후보로 판정하고, 별도 구현 Issue에서 Android 런타임·실기기·사람 검증을 실행한다.

**Tech Stack:** GitHub Issues/Markdown, Godot 4.7.1·GDScript는 후속 승인 단계에서만 사용, Android 세로형 720×1280 기준.

## Global Constraints

- 최신 사용자 지시와 Issue #60의 `PLANNING_ONLY_PROFILE`이 우선한다.
- 새 프로젝트 코어·Vertical Slice 승인 전 제품 코드·Scene·data·asset을 변경하지 않는다.
- 기존 제작·강화·장비 생애 구현은 `REFERENCE_ONLY / REVALIDATION_REQUIRED`다.
- 공용 UX 기준은 Base `auditing-and-refining-ui-art`; 프로젝트 정본은 `docs/UX_UI_SYSTEM.md`다.
- HTML 기획 대시보드는 범위에서 제외한다.
- 미실행 검증은 `NOT_RUN` 또는 `HUMAN_NOT_RUN`으로 유지한다.

---

### Task 1: 권한과 기준선 고정

**Files:**
- Read: `AGENTS.md`
- Read: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Read: `docs/UX_UI_SYSTEM.md`
- Read: `docs/BASE_UX_UI_ADOPTION.md`
- Read: GitHub Issue `#60`

**Interfaces:**
- Consumes: 최신 사용자 결정, Issue #60 Gate, Base UX/UI 패턴.
- Produces: 검증 대상과 금지 범위가 명시된 Issue 본문.

- [ ] **Step 1:** Issue #60에서 현재 제품 단계, Work Mode, 구현 금지 조건을 인용한다.
- [ ] **Step 2:** 기존 제작·강화·장비 생애 UI를 `REFERENCE_ONLY`, 새 검증 계약을 `PROPOSED_ONLY`로 분리한다.
- [ ] **Step 3:** `docs/BASE_UX_UI_ADOPTION.md`의 Base main SHA를 검증 기준으로 기록한다.
- [ ] **Step 4:** 제품 파일 변경 없음과 HTML 대시보드 제외를 명시한다.

### Task 2: UX 검증 가설과 시나리오 정의

**Files:**
- Read: `docs/UX_UI_SYSTEM.md`
- Read: `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- Create after Gate approval: `docs/validation/BLACKSMITH_UX_UI_VALIDATION_PACKET.md`

**Interfaces:**
- Consumes: 제작·강화·비교·결과 복기 경험 약속.
- Produces: 후속 프로토타입과 사람 테스트가 공통으로 사용하는 6개 시나리오.

- [ ] **Step 1:** `제작 후보 선택 → 비용 비교 → 제작 → 결과 확인` 시나리오를 정의한다.
- [ ] **Step 2:** `희귀 재료를 사용하는 위험 강화 → 취소 또는 실행 → 손실/성과 복기` 시나리오를 정의한다.
- [ ] **Step 3:** 부족 재료, 인벤토리 가득 참, 잠금 상태의 원인·복구 행동 시나리오를 정의한다.
- [ ] **Step 4:** 현재 장비와 후보 장비를 같은 단위로 비교하고 장착·판매를 선택하는 시나리오를 정의한다.
- [ ] **Step 5:** 작은 화면·safe area·긴 한국어·최대 수치 fixture를 정의한다.
- [ ] **Step 6:** 복귀 플레이어가 최근 제작 결과와 다음 목표를 설명하는 시나리오를 정의한다.

### Task 3: 관찰 지표와 통과 기준 정의

**Files:**
- Create after Gate approval: `docs/validation/BLACKSMITH_UX_UI_VALIDATION_PACKET.md`
- Update after test: `docs/UX_UI_SYSTEM.md`

**Interfaces:**
- Consumes: Task 2 시나리오.
- Produces: `KEEP / AMPLIFY / CHANGE / REMOVE / RETEST` 판정 근거.

- [ ] **Step 1:** 각 시나리오에서 첫 행동까지 걸린 시간, 오입력, 뒤로가기, 설명 정확도를 기록한다.
- [ ] **Step 2:** 위험 강화 전 비용·성공 가능성·실패 손실을 세 항목 모두 설명해야 통과하도록 정한다.
- [ ] **Step 3:** 오류 상태에서 원인과 다음 행동을 도움 없이 찾은 비율을 기록한다.
- [ ] **Step 4:** 6명 중 5명 이상이 제작 결과와 장비 변화의 인과를 설명해야 통과하도록 정한다.
- [ ] **Step 5:** 세로 화면의 핵심 행동이 safe area 안에 있고 한 손 엄지 경로로 완주돼야 통과하도록 정한다.

### Task 4: 후속 Android 실행 Gate 정의

**Files:**
- Update after planning approval: `docs/DEVELOPMENT_GATES.md`
- Update after planning approval: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Create after planning approval: 별도 Codex Goal Issue

**Interfaces:**
- Consumes: 승인된 새 프로젝트 코어·Vertical Slice와 Task 2~3 계약.
- Produces: 제품 변경이 허용되는 별도 구현·검증 Issue.

- [ ] **Step 1:** Issue #60의 사용자 `검수 완료` 이전에는 Codex Build를 금지한다.
- [ ] **Step 2:** 승인 후 실제 UI Scene·Theme·View Data·Signal 소유자를 읽기 전용으로 조사한다.
- [ ] **Step 3:** 조사 결과를 기반으로 제품 변경과 테스트 변경을 별도 PR로 분리한다.
- [ ] **Step 4:** Godot parse/runtime, Android 실기기, 사람 이해, 접근성 사용자 증거를 독립 상태로 보고한다.

### Task 5: 검증과 보고

**Files:**
- Update after execution: `docs/UX_UI_SYSTEM.md`
- Update after execution: `docs/BASE_UX_UI_ADOPTION.md`
- Update after execution: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`

**Interfaces:**
- Consumes: 자동·기기·사람 증거.
- Produces: 다음 개발 결정과 Base 승격 후보.

- [ ] **Step 1:** 자동 검사, Android 실기기, 사람 이해, 접근성 사용자 결과를 합산하지 않고 별도로 기록한다.
- [ ] **Step 2:** 실행하지 않은 증거는 통과로 추정하지 않는다.
- [ ] **Step 3:** 공용 패턴 개선 후보와 Blacksmith 전용 수치·배치 결과를 분리한다.
- [ ] **Step 4:** 사용자 승인 없이 프로젝트 코어·강화 규칙·경제 수치를 변경하지 않는다.

## Verification Commands

계획 문서 PR에서는 다음만 실행한다.

```bash
python tools/check_archive_governance.py
python -m unittest tests.test_archive_retention_governance -v
python tools/audit_project_operating_system.py
```

후속 제품 검증은 별도 승인 Issue에서 Godot 4.7.1 import·parse, 대상 Scene smoke, Android 실기기와 사람 플레이를 실행한다.
