# Plus5 Plus10 Synthetic Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `+5 납품 / +10 도전` 사람 검증 Artifact에서 후견 문구와 실제 선택·scripted 실패 혼합을 제거한다.

**Architecture:** 기존 PoC와 강화 JSON은 유지한다. 선택 Task는 중립 정보만 제공하고, scripted 실패 이해 Task는 참가자의 실제 선택과 분리된 별도 비교 장비로 실행한다.

**Tech Stack:** Markdown 연구 계약, 프로젝트 PR validation

## Global Constraints

- `human_validation: NOT_RUN`, `android_validation: NOT_RUN`, `implementation_authority: NONE` 유지.
- `scenes/**`, `scripts/**`, `data/**` 변경 금지.
- 경제 기대값은 별도 `TEST_REQUIRED`로 남긴다.

---

### Task 1: Artifact 교정

**Files:**
- Modify: `docs/superpowers/plans/2026-07-29-plus5-plus10-human-validation-artifact.md`

**Interfaces:**
- Consumes: `docs/research/2026-07-29_PLUS5_PLUS10_SYNTHETIC_TESTER_REPORT.md`
- Produces: 중립 선택 카드, 상세 이력 2단계, 독립 scripted failure task

- [ ] **Step 1:** current main·Base Governance metadata를 갱신한다.
- [ ] **Step 2:** “두 선택은 모두 유효하다” 문구를 baseline에서 제거한다.
- [ ] **Step 3:** 선택 화면과 제작 이력 상세를 2단계로 분리한다.
- [ ] **Step 4:** 실제 선택과 무관한 별도 비교 장비로 scripted failure task를 구성한다.
- [ ] **Step 5:** 버튼 위계 중립성과 actual/scripted 분리 필드를 기록 계약에 추가한다.

### Task 2: 검증과 병합

**Files:**
- Verify: branch diff
- Verify: PR validation

**Interfaces:**
- Consumes: Task 1 Artifact
- Produces: 문서 계약 통과 및 제품 경로 비침범 증거

- [ ] **Step 1:** 변경 파일이 계획과 Artifact에 한정되는지 확인한다.
- [ ] **Step 2:** PR validation 성공을 확인한다.
- [ ] **Step 3:** 미해결 리뷰 스레드가 없는지 확인한다.
- [ ] **Step 4:** 검증된 HEAD를 squash merge한다.
