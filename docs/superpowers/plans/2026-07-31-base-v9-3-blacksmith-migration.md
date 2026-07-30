# Base v9.3 Blacksmith Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Blacksmith의 운영 계약을 Base v9.3·Vertical Slice v9로 정렬하고, 모바일 오프라인 플레이를 보존하는 `+50` 이상 작품 랭킹 서버 경계를 문서화한다.

**Architecture:** `skills/PROJECT_BASE_ADAPTER.json`을 단일 기계 판독 원본으로 두고 Project Registry·Snapshot·Compatibility view·Dashboard를 결정론적으로 파생한다. 서버 랭킹은 기존 프로젝트 Skill 3개에 책임을 분담하고 `FUTURE_SERVER_READY / NOT_IMPLEMENTED` 문서 계약으로만 추가한다.

**Tech Stack:** Markdown, JSON, Python `unittest`, GitHub Actions, Base v9.3 project operating contract, Google Sheets GDD workspace.

## Global Constraints

- 프로젝트: 블랙스미스(Blacksmith)
- 저장소: `alsdmlals4-eng/Blacksmith`
- 기준 main: `500a5a7960146ef229ae172cf9e127306d23f073`
- Base version: `9.3.0`
- Base release: `30ca6c7b5f93521f0eb0eed42d01437cd43c50ae`
- Base evidence: `462a86db192d23d0f386281a1eb54b0a8cbad62e`
- Base Registry SHA-256: `9847bb2b225c776ad7916930f0f48c490bc2a898bea8e02ea1fdd0e6caac60c1`
- GDD Sheet ID: `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`
- 플랫폼: Android 모바일 / 세로형 720×1280
- 보호 경로: `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`
- 서버·API·DB·로그인·랭킹 UI는 구현하지 않는다.

---

### Task 1: v9.3 실패 계약을 테스트로 고정

**Files:**
- Create: `tests/test_base_v9_3_migration_contract.py`
- Modify: `tests/test_base_v9_adoption.py`
- Modify: `tests/test_bca_visual_sheet_adoption.py`

**Interfaces:**
- Consumes: Base v9.3 lock identity와 프로젝트 경로
- Produces: 운영 문서·Adapter·서버 계약의 회귀 테스트

- [ ] **Step 1: 새 테스트에 v9.3 release/evidence/Registry hash 기대값을 작성한다.**
- [ ] **Step 2: `AGENTS.md`, `README.md`, `BASE_RULES_VERSION.md`에서 v8 활성 실행문과 `c987647...` 활성 핀이 없어야 함을 검사한다.**
- [ ] **Step 3: 미래 서버 계약에 `+50`, 등급, 수식어, 서버 권위, 오프라인 우선, `NOT_IMPLEMENTED`가 있어야 함을 검사한다.**
- [ ] **Step 4: Draft PR을 열어 현재 main 기반 테스트가 예상대로 실패하는지 확인한다.**
- [ ] **Step 5: 실패 원인이 v9.3 계약 미적용임을 기록한다.**

### Task 2: Base v9.3 Adapter와 파생본 정렬

**Files:**
- Modify: `skills/PROJECT_BASE_ADAPTER.json`
- Modify: `skills/PROJECT_SKILL_SNAPSHOT.json`
- Modify: `skills/BASE_V9_ADAPTER.json`
- Modify: `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- Modify: `docs/PROJECT_OPERATING_DASHBOARD.html`
- Modify: `docs/PROJECT_OPERATING_HEALTH.json`

**Interfaces:**
- Consumes: Base v9.3 lock, Project Registry raw-byte hash, Workbook evidence hash
- Produces: v9.3 release identity와 6개 effective route의 결정론적 운영 뷰

- [ ] **Step 1: Adapter `base_release`를 v9.3 lock 값으로 교체한다.**
- [ ] **Step 2: Base Registry hash를 lock의 `9847bb...`로 교체한다.**
- [ ] **Step 3: 실제 Sheet를 `CURRENT`로 기록하고 Workbook 문서를 Sheet evidence로 연결한다.**
- [ ] **Step 4: Project Registry·Adapter raw-byte hash를 계산한다.**
- [ ] **Step 5: Snapshot·Compatibility view·Dashboard를 정렬된 키와 LF 개행으로 재생성한다.**

### Task 3: 프로젝트 Skill과 Registry에 서버 대비 책임 추가

**Files:**
- Modify: `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`
- Modify: `skills/game-design/SKILL.md`
- Modify: `skills/engineering/SKILL.md`
- Modify: `skills/qa/SKILL.md`
- Create: `docs/planning/BLACKSMITH_HIGH_GRADE_RANKING_SERVER_CONTRACT.md`

**Interfaces:**
- Consumes: 사용자 요구 `+50 이상 작품 랭킹`, 등급·수식어 비교
- Produces: 게임 디자인·엔지니어링·QA의 분리된 후속 책임

- [ ] **Step 1: Game Design에 공개 비교 경험·등록 조건·시즌 가설 모드를 추가한다.**
- [ ] **Step 2: Engineering에 API 계약·오프라인 큐·idempotency·버전 경계 모드를 추가한다.**
- [ ] **Step 3: QA에 서버 권위·부정 등록·개인정보·삭제·호환성 검토 모드를 추가한다.**
- [ ] **Step 4: 랭킹 계약 문서에 공개 Payload 최소화와 클라이언트 비신뢰 원칙을 기록한다.**
- [ ] **Step 5: 서버 구현 상태를 `NOT_IMPLEMENTED`로 고정한다.**

### Task 4: 활성 운영 문서와 Vertical Slice v9 계약 정렬

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: `docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md`
- Create: `docs/operations/BLACKSMITH_VERTICAL_SLICE_V9_APPLICATION.md`
- Create: `docs/operations/BLACKSMITH_V9_RECONCILIATION_PACKET.md`

**Interfaces:**
- Consumes: Adapter·Issue #79·v9 실행문
- Produces: 콜드 스타트와 감사에서 사용하는 현행 권한 설명

- [ ] **Step 1: v8 활성 문구를 v9.3·v9 실행문으로 교체한다.**
- [ ] **Step 2: v6~v8을 `LEGACY_REFERENCE_ALLOWED / SUPERSEDED_COMPATIBILITY`로 기록한다.**
- [ ] **Step 3: Application Binding에 저장소·Sheet·보호 경로·Skill 3개를 고정한다.**
- [ ] **Step 4: Reconciliation Packet에 현재 Finding·Critical Gate·Sheet 동기화 순서를 기록한다.**
- [ ] **Step 5: Workbook에 서버 랭킹이 후속 계획이며 GitHub 병합 후 Sheet를 갱신한다고 기록한다.**

### Task 5: GitHub Issue 권한 정렬

**Files:**
- GitHub Issue #60
- GitHub Issue #69
- GitHub Issue #79

**Interfaces:**
- Consumes: 최신 사용자 지시와 v9.3 Application Binding
- Produces: v6 전용 실행 권한이 제거된 추적 구조

- [ ] **Step 1: #60 제목·서두·권한 모델을 Base v9.3·Vertical Slice v9로 갱신한다.**
- [ ] **Step 2: 기존 v6 재기획 기록은 요구사항 추적 입력으로 보존한다.**
- [ ] **Step 3: #69의 상위 Gate와 프로필을 v9 조건부 프로필로 갱신한다.**
- [ ] **Step 4: #79에 PR·CI·병합·Sheet 결과를 기록한다.**

### Task 6: PR 검증과 병합

**Files:**
- All changed files in the PR

**Interfaces:**
- Consumes: Task 1~5 결과
- Produces: 검증된 `main` 운영 계약

- [ ] **Step 1: PR changed filenames를 전수 확인해 보호 경로가 없는지 검사한다.**
- [ ] **Step 2: PR validation과 Base adoption workflow 결과를 확인한다.**
- [ ] **Step 3: 실패 로그가 있으면 계약·hash·파생본을 최소 수정한다.**
- [ ] **Step 4: 성공한 head SHA를 고정해 squash merge한다.**
- [ ] **Step 5: 병합된 main 파일과 commit을 재조회한다.**

### Task 7: 병합 후 Google Sheet 동기화

**Files:**
- Google Sheet `00_프로젝트_허브`
- Google Sheet `01_작업순서`
- Google Sheet `04_누락_충돌_감사`
- Google Sheet `05_GDD_요약`
- Google Sheet `80_데모_버티컬슬라이스_플레이테스트`
- Google Sheet `90_본제작_출시_사업`
- Google Sheet `99_변경이력`

**Interfaces:**
- Consumes: 병합된 main SHA와 v9.3 계약
- Produces: GitHub main과 일치하는 사용자 GDD 작업면

- [ ] **Step 1: 대상 셀을 다시 읽고 기존 사용자 변경을 보존한다.**
- [ ] **Step 2: Base SHA·실행문·Issue·상태·서버 후속 계획을 허용 탭에 기록한다.**
- [ ] **Step 3: `80_데모_버티컬슬라이스_플레이테스트!B2`의 `#ERROR!`를 일반 문자열로 교정한다.**
- [ ] **Step 4: 변경 셀을 재조회해 값·수식·상태를 검증한다.**
- [ ] **Step 5: #79와 변경이력 탭에 최종 동기화 증거를 기록한다.**

## Plan self-review

- Spec coverage: Base v9.3, v9 실행문, Adapter 파생본, Skill 3개, 서버 대비, Issue, PR, Sheet를 모두 Task에 연결함.
- Placeholder scan: `TBD`, `TODO`, 구현 미정 지시 없음. 서버 기능은 의도적으로 `NOT_IMPLEMENTED`이며 후속 결정 목록이 명시됨.
- Type consistency: release/evidence/hash·Sheet ID·상태 이름을 설계 문서와 동일하게 사용함.
