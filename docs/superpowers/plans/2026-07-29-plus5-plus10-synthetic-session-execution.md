# Plus Five / Plus Ten Synthetic Session Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to execute this plan task-by-task.

**Goal:** 교정된 `+5 납품 / +10 도전` Artifact를 합성 페르소나로 실행해 숫자 위계·경제 최적화·정보 공개 순서의 남은 위험을 잠정 판정한다.

**Architecture:** 실제 선택 Task와 독립 scripted 실패 Task를 계속 분리한다. 가상 선택은 비율이나 사람 행동으로 기록하지 않고 각 페르소나의 예상 해석·반례·신뢰도로만 기록한다.

**Tech Stack:** Markdown, Base Synthetic Tester Governance, Blacksmith 문서 CI

## Global Constraints

- `T6_AI_INFERENCE`, `human_validation: NOT_RUN`, `android_validation: NOT_RUN`을 유지한다.
- Scene, Script, 강화 JSON, 경제 수치, 제품 UI를 변경하지 않는다.
- 실제 선택률·애착·후회·매출 행동을 주장하지 않는다.

---

### Task 1: 합성 Case 실행

**Files:**
- Read: `docs/research/2026-07-29_SYNTHETIC_TESTER_STRUCTURE_ANALYSIS.md`
- Read: `docs/research/2026-07-29_PLUS5_PLUS10_SYNTHETIC_TESTER_REPORT.md`
- Read: `docs/superpowers/plans/2026-07-29-plus5-plus10-human-validation-artifact.md`
- Create: `docs/research/2026-07-29_PLUS5_PLUS10_SYNTHETIC_SESSION_EXECUTION.md`

- [ ] 초보·강화 숙련·성급·수집형·최적화 페르소나를 실행한다.
- [ ] 실제 선택과 scripted 실패 이해를 분리한다.
- [ ] `+10` 숫자 위계와 버튼 중립성, provenance 상세 카드 발견성을 공격한다.
- [ ] 경제 기대값은 `TEST_REQUIRED`로 유지한다.

### Task 2: 잠정 판정과 검증

- [ ] 결과를 `PROMISING_DIRECTION / ADAPT / REWORK / TEST_REQUIRED`로만 기록한다.
- [ ] 제품 UI·Android·경제 밸런스는 `NOT_RUN`으로 남긴다.
- [ ] 변경 파일을 계획·보고서 두 개로 제한한다.
- [ ] PR validation과 리뷰 스레드 확인 후 squash merge한다.
