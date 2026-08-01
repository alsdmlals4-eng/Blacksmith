# Blacksmith 적용을 위한 Base 현행 Skill·작업 구조 분석

> Audit ID: `BS-BASE-AUDIT-20260801-01`
>
> 상태: `BASE_ANALYSIS_COMPLETE / PROJECT_INTEGRITY_CONFLICTS_OPEN`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN → REVIEW`
>
> 구현 권한: `NONE`
>
> Base latest main observed: `90ec6f33953f80f607d4e79f58cc2174eb178f73`
>
> Latest released project pin: Base v9.3 `30ca6c7b5f93521f0eb0eed42d01437cd43c50ae`

## 1. 조사 방식과 범위

Base가 선언한 콜드 스타트와 Registry 우선 원칙에 따라 다음 권위 층을 조사했다.

```text
Base README·START_HERE·AGENTS
→ OPERATING_MODEL·WORK_MODE_AND_SKILL_ROUTING·DOCUMENTATION_MAP
→ SKILL_REGISTRY·generated active Skill view·shared routes
→ Base release/version lock·v9.3 release contract·active v9 prompt
→ project adapter contract·project operating-contract generator/validator
→ 승인 결정·Google Sheets·기획 순서·적대적 검토·reference freshness 정책
→ Blacksmith adapter·snapshot·router·local Registry·Base adoption docs·health artifact
```

Base 자체의 정의에 따라 `전부 살펴본다`를 모든 Archive·Backup·보류 파일과 모든 Skill 본문을 무조건 메모리에 적재하는 방식으로 해석하지 않았다. 활성 Registry·권위 지도·현재 작업의 trigger에 따라 책임 원본, 활성 Skill 27개 메타데이터, 직접 소비자, 검증 도구와 Blacksmith 적용 파일을 선별했다.

직접 저장소 복제는 실행 환경 DNS 제한으로 실패했다. 따라서 GitHub 연결 검색·파일 조회로 확인 가능한 현재 main 파일을 사용했고, 전체 tracked inventory와 로컬 validator 실행은 `NOT_RUN`으로 남긴다.

## 2. Base 현행 버전과 권위 경계

### 2.1 세 층을 분리해야 한다

| 층 | 값 | 의미 |
|---|---|---|
| immutable Base release line | `v9.0.0` / `585a53a2…` | Base 자체의 최초 v9 릴리스 경계 |
| latest released project adapter line | `v9.3.0` / release `30ca6c7…` / evidence `462a86d…` | 프로젝트가 검증된 핀으로 채택 가능한 최신 릴리스 |
| latest Base main observed | `90ec6f3…` | v9.3 이후 변경과 v9.4 제안이 존재하는 최신 main, 프로젝트 핀으로 자동 사용 금지 |

`base-v9.3.lock.json`의 Registry raw-byte SHA-256은 `9847bb2b225c776ad7916930f0f48c490bc2a898bea8e02ea1fdd0e6caac60c1`이다.

현재 Base main의 generated active Skill view는 다른 Registry SHA를 가진다. 이는 릴리스 이후 Base가 계속 진화했음을 의미하며, 프로젝트는 최신 main Registry를 검증 릴리스처럼 직접 가져오면 안 된다.

### 2.2 v9.4 상태

Base latest main에는 판단 중심 AI 지시·컨텍스트 큐레이션·UI 모션 원칙 등의 v9.4 후보 제안이 `SUBMITTED`로 존재한다. 이는 활성 Base v9.3 릴리스가 아니며 Blacksmith 적용 범위에 자동 포함하지 않는다.

## 3. Base 작업 운영 구조

### 3.1 주 Work Mode

```text
PLAN
→ 요구·근거·설계·정본·작업 순서

BUILD
→ 승인된 범위 구현·단계별 테스트·롤백

REVIEW
→ 적대적 공격·비판 검증·실제 증거·회귀 판정
```

한 시점에는 주 Work Mode 하나만 사용하고 복합 작업은 `PLAN → BUILD → REVIEW`로 전환한다.

### 3.2 자동 라우팅

```text
사용자 Prompt
→ 현재 단계·위험 판정
→ Work Mode 자동 선택
→ Skill Registry trigger 대조
→ 최소 Skill 자동 선택
→ 필요한 Skill Mode 선택
→ 실행·검증
→ Skill 실행 보고
```

주 책임 분야 Skill은 최대 1개이며 Foundation Skill은 필요한 경우에만 추가한다. 모든 Skill을 기본 로드하지 않는다.

### 3.3 공통 8단계 작업 루프

```text
BASELINE_RECOVERY
→ DUPLICATE_OMISSION_CONFLICT_AUDIT
→ EVIDENCE_PACK
→ APPROVAL_BUNDLE
→ CANONICAL_UPDATE
→ PROPAGATION_AUDIT
→ VALIDATION
→ GATE_CLOSE
```

차단 충돌이 있으면 새 기획·구현보다 복원·재동기화를 먼저 수행한다.

### 3.4 프로젝트 구현 연결

```text
GPT PLAN
→ 저장소·결정·Sheet 감사
→ 기획·데이터·UX·비-Godot 계약·마스터 계획

Codex PLAN
→ 최신 main의 실제 Godot 파일 읽기 전용 재검수

GPT
→ Codex Plan 검토·패키지 계약·READY_FOR_BUILD

Codex BUILD
→ 지정 Branch의 Godot 구현·테스트·Commit·Push

GPT REVIEW
→ diff·계약·테스트·회귀 검수

AGENT_MERGE_REQUIRED
→ 동일 HEAD·필수 검사·독립 검토·P0/P1 0일 때 병합
```

Blacksmith는 아직 P0/P1 Finding이 열려 있으므로 Codex BUILD와 병합 Gate를 열 수 없다.

## 4. Base 활성 Skill 구조

Base current main의 Registry-derived active Skill 수는 27개다. 수는 정책 목표가 아니라 관찰값이다.

### 4.1 Foundation·운영

1. `managing-project-intake-and-work-contract`
2. `managing-game-project-operating-system`
3. `evolving-project-discipline-skills`
4. `managing-design-documents`
5. `maintaining-project-context-and-handoff`

### 4.2 기획·코어·Vertical Slice

6. `analyzing-and-refining-game-concepts`
7. `designing-vertical-slices`
8. `identifying-project-core`
9. `establishing-project-core`
10. `governing-game-user-research-coverage`

### 4.3 아트·UX·자산

11. `designing-art-prompts-and-technique-cards`
12. `auditing-and-refining-ui-art`
13. `evaluating-godot-assets-and-plugins-before-creation`
14. `building-project-visual-dashboards`

### 4.4 검토·품질·유지보수

15. `reviewing-and-validating-project-changes`
16. `auditing-canonical-reference-freshness`
17. `running-adversarial-review-and-refinement`
18. `refactoring-with-contract-preservation`
19. `simplifying-skill-bodies`
20. `pruning-stale-and-nonfunctional-material`
21. `diagnosing-game-engine-runtime-failures`
22. `governing-legacy-retention-and-archives`

### 4.5 실행·Git·지식 환류

23. `orchestrating-deepseek-worktrees`
24. `managing-base-change-proposals`
25. `synchronizing-local-and-github-state`
26. `maintaining-long-running-task-continuity`
27. `creating-user-learning-notes`

이번 작업에서 직접 적용되는 핵심 조합은 다음이다.

```text
managing-project-intake-and-work-contract
+ managing-game-project-operating-system:audit
+ managing-design-documents:update
+ running-adversarial-review-and-refinement:repository-wide-audit
+ auditing-canonical-reference-freshness
+ reviewing-and-validating-project-changes:evidence-report
```

## 5. Base 공용 Skill과 프로젝트 Skill 경계

Base v9.1+ 어댑터 계약은 다음을 강제한다.

```text
Base 공용 절차·판단·품질 기준
→ Base가 단일 소유

프로젝트 경로·정본·엔진·플랫폼·검증기
→ PROJECT_BASE_ADAPTER.json

세계관·코어 규칙·실제 데이터·프로젝트 고유 제작 절차
→ 프로젝트 로컬 Skill
```

- Base 공용 Skill 본문을 프로젝트에 복제하지 않는다.
- Canonical adapter는 `skills/PROJECT_BASE_ADAPTER.json`이다.
- `PROJECT_BASE_SKILL_ADAPTER.json`, `BASE_V9_ADAPTER.json`, `PROJECT_PATH_ADAPTER.json`은 생성 호환 뷰이며 수동 편집 금지다.
- `PROJECT_SKILL_SNAPSHOT.json`, router, health artifact는 adapter와 Registry에서 결정론적으로 생성한다.
- 프로젝트 변경은 `tools/project_operating_contract.py`와 검증된 릴리스 핀을 통해 수행한다.
- Base main 최신본을 직접 참조하지 않고 release commit·evidence commit·Registry hash를 함께 고정한다.

## 6. Base의 현재 프로젝트 GDD Sheet 계약

프로젝트 Sheet의 역할은 `USER_FACING_GDD_WORKSPACE`다.

```text
GitHub 정본·실제 구현
↔ Google Sheet 사용자 작업면
```

- Sheet는 상세 정본과 구현 사실을 대체하지 않는다.
- Sheet-only 변경은 `PROPOSED_SHEET_CHANGE`다.
- `02_현재_확정결정`만 CURRENT 결정을 보유해야 한다.
- SUPERSEDED·전체 이력은 `99_변경이력`으로 이동한다.
- 주요 Decision은 GitHub 정본·Commit·Sheet를 같은 ID로 갱신하고 재조회한다.
- 한 화면 요약, 흐름·관계·와이어프레임, 핵심 수치, 정본 링크 순서로 구성한다.
- HTML Dashboard는 사용자가 명시하거나 기존 유지보수일 때만 사용한다.

## 7. Blacksmith 현행 적용 대조

### BASE-F01 — Canonical adapter가 v9.1에 고정됨

현재 `skills/PROJECT_BASE_ADAPTER.json`은 다음을 기록한다.

```text
version: 9.1.0
release_commit: 3c158f52…
release_evidence_commit: dd20ad38…
```

반면 최신 Blacksmith 기획 문서는 Base v9.3 release commit `30ca6c7…`을 적용 기준처럼 기록한다. 문서 선언과 실제 실행 어댑터가 다르다.

**판정:** `MUST_FIX / PROJECT_OPERATING_INTEGRITY`

### BASE-F02 — protected baseline이 현재 main과 불일치

Adapter protected baseline:

```text
4b465ae92a48c1bd7e222b86234dafb507d242dc
```

감사한 Blacksmith main:

```text
500a5a7960146ef229ae172cf9e127306d23f073
```

Base validator는 표준 로컬 검증에서 `refs/remotes/origin/main`이 adapter baseline commit과 정확히 같아야 한다. 현재 값은 정적으로 불일치한다. 따라서 실제 validator 실행 시 fail-closed할 가능성이 높으며, 실행 전까지 `STATIC_CONFLICT / VALIDATOR_NOT_RUN`으로 판정한다.

**판정:** `MUST_FIX / BLOCKS_SHARED_ROUTE_EXECUTION`

### BASE-F03 — Sheet 상태가 서로 충돌

- Canonical adapter: `gdd_sheet.sync_status = NOT_CONFIGURED`
- 프로젝트 Registry·Workbook·실제 연결 상태: `PROJECT_SHEET_CONFIGURED`
- 실제 Sheet: `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`

Application Binding의 입력이 서로 다르므로 실행 경로가 어떤 상태를 믿어야 하는지 불명확하다.

**판정:** `MUST_FIX / CONFLICTING_SOURCE`

### BASE-F04 — Base 기준 문서가 구형

`docs/BASE_RULES_VERSION.md`는 다음을 동시에 주장한다.

- 기준 commit `c987647…`
- Base 활성 기능 25개
- 활성 Prompt v8
- Sheet configured

현재 Base 구조는 Registry-derived active Skill 27개와 active v9 prompt를 사용한다. 또한 canonical adapter의 v9.1 핀과도 일치하지 않는다.

**판정:** `MUST_FIX / STALE_REFERENCE`

### BASE-F05 — Adoption Profile의 핀이 별도로 남음

`docs/BASE_ADOPTION_PROFILE.json`은 Base commit `41a2058…`, shared extension commit `6a224e4…`를 기록한다. Canonical adapter, Base rules doc, local Registry가 각각 다른 commit을 주장한다.

**판정:** `MUST_FIX / DUPLICATE_ACTIVE_SOURCE`

### BASE-F06 — Project Registry provenance drift

프로젝트 Registry의 `base_integration.commit`은 `c987647…`이며 canonical adapter의 release commit `3c158f5…`와 다르다. Registry의 local Skill 3개 구조 자체는 유효하지만 Base provenance가 일치하지 않는다.

**판정:** `MUST_FIX / MISSING_PROPAGATION`

### BASE-F07 — Snapshot·Router는 v9.1로 생성됨

- `PROJECT_SKILL_SNAPSHOT.json`: v9.1 adapter의 Registry hash와 route를 사용
- `.agents/skills/blacksmith-workflow-router/SKILL.md`: `verified v9.1 operating contracts`

이 둘은 현재 adapter와는 일치하지만, Blacksmith 기획 문서의 v9.3 선언과 불일치한다. 수동 수정이 아니라 adapter migration 뒤 재생성해야 한다.

**판정:** `MUST_FIX / GENERATED_DERIVATIVE_STALE_RELATIVE_TO_TARGET`

### BASE-F08 — CURRENT_CONFIRMED_DECISIONS 안정 진입점 부재

Base current contract는 현재 승인 결정을 복원하는 `CURRENT_CONFIRMED_DECISIONS.md`를 프로젝트 필수 진입점으로 사용한다. Blacksmith는 기능상 유사한 `BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`를 가지고 있지만 안정 표준 경로 또는 adapter role binding이 없다.

**권장:** 상세 정본을 복제하지 않는 얇은 `CURRENT_CONFIRMED_DECISIONS.md`를 생성하거나, Base adapter가 현행 결정 인덱스를 명시적으로 그 역할에 바인딩하도록 한다.

**판정:** `SHOULD_FIX / COLD_START_DISCOVERABILITY`

### BASE-F09 — Health artifact의 PASS가 현재 drift를 반영하지 않음

`docs/PROJECT_OPERATING_HEALTH.json`은:

```text
integrity_verdict: PASS_WITH_NOT_RUN_GATES
operating_maturity: OM-L0
static/runtime/device/accessibility/human: NOT_RUN
```

하지만 operating evidence가 비어 있고 현재 adapter·baseline·Sheet drift가 반영되지 않았다. 재생성 전에는 현재 PASS 증거로 사용하지 않는다.

**판정:** `MUST_FIX / DERIVATIVE_STALE`

### BASE-F10 — Sheet의 CURRENT 원장에 역사 결정이 혼재

현재 `02_현재_확정결정`에는 `SUPERSEDED` 제작 등급 결정이 남아 있다. Base current Sheet 정책은 `02`를 CURRENT 전용으로, 역사·대체 관계는 `99_변경이력`으로 분리한다.

데이터 손실을 막기 위해 즉시 삭제하지 않고 전체 Sheet 감사에서 이동·호환 정책을 정한다.

**판정:** `SHOULD_FIX / LEGACY_RECONCILIATION_REQUIRED`

### BASE-F11 — Base latest main을 직접 채택하면 안 됨

Base current main `90ec6f3…`에는 v9.4 제안이 포함돼 있지만 릴리스 핀은 아니다. Blacksmith migration target은 현재 시점에서 **검증된 v9.3 release/evidence pin**이어야 한다.

**판정:** `KEEP_GUARDRAIL / NO_DIRECT_MAIN_PIN`

## 8. 권장 목표 구조

```text
Base release target
├─ version: 9.3.0
├─ release_commit: 30ca6c7b5f93521f0eb0eed42d01437cd43c50ae
├─ release_evidence_commit: 462a86db192d23d0f386281a1eb54b0a8cbad62e
└─ registry_sha256: 9847bb2b225c776ad7916930f0f48c490bc2a898bea8e02ea1fdd0e6caac60c1

Blacksmith
├─ skills/PROJECT_BASE_ADAPTER.json             # canonical generated input/result
├─ skills/PROJECT_SKILL_SNAPSHOT.json           # generated
├─ .agents/skills/blacksmith-workflow-router/   # generated
├─ docs/PROJECT_OPERATING_HEALTH.json            # generated
├─ docs/PROJECT_OPERATING_DASHBOARD.html         # 선택적 generated artifact, 사용자 기본 작업면 아님
├─ [기획서]/00_프로젝트_허브/SKILL_REGISTRY.json # 프로젝트 로컬 3 Skill
├─ CURRENT_CONFIRMED_DECISIONS.md 또는 명시적 role binding
└─ configured GDD Sheet binding
```

## 9. 안전한 보완 순서

```text
1. Blacksmith main·열린 PR·Sheet 최신 상태 고정
2. v9.3 release/evidence/Registry hash 검증
3. 현행 adapter·legacy input·protected paths 인벤토리
4. PROJECT_BASE_ADAPTER migration input 생성
5. tools/project_operating_contract.py로 adapter·snapshot·router·health 재생성
6. 호환 뷰를 직접 편집하지 않고 generator output으로만 갱신
7. Base rules·adoption profile·local Registry provenance·Documentation Map 갱신
8. Sheet configured binding과 CURRENT_CONFIRMED_DECISIONS 역할 연결
9. operating-contract validator·reference freshness·tests 실행
10. 적대적 검토와 콜드 스타트 검증
```

로컬 Base checkout과 validator 실행 환경이 없으므로 이번 단계에서는 migration 파일을 수동 작성하지 않는다. Base 분석 정본과 변경 계획만 확정한다.

## 10. 영향과 기존 감사 연결

기존 `BS-AUD-F12`의 “Base v8·v9.1·v9.3 동시 활성”은 이 분석으로 구체화됐다.

```text
BS-AUD-F12
→ BASE-F01~F09
```

새로운 게임 설계 P0를 추가하지 않는다. 다만 Base shared route를 사용하거나 Codex 구현 인계를 열기 전 반드시 해결해야 하는 **운영 무결성 차단**으로 취급한다.

## 11. 현재 판정

```text
BASE_LATEST_MAIN_OBSERVED: 90ec6f33953f80f607d4e79f58cc2174eb178f73
BASE_LATEST_RELEASED_PROJECT_LINE: 9.3.0
BASE_V9_3_RELEASE_COMMIT: 30ca6c7b5f93521f0eb0eed42d01437cd43c50ae
BASE_V9_3_EVIDENCE_COMMIT: 462a86db192d23d0f386281a1eb54b0a8cbad62e
BASE_V9_4_PROPOSALS: NOT_RELEASED
BASE_ACTIVE_SKILLS_CURRENT_MAIN: 27

BLACKSMITH_CANONICAL_ADAPTER_VERSION: 9.1.0
BLACKSMITH_ADAPTER_TARGET_DECLARATION: CONFLICTING_V9_3_DOCS
BLACKSMITH_PROTECTED_BASELINE: STALE_RELATIVE_TO_MAIN
BLACKSMITH_SHEET_BINDING: CONFLICTING_SOURCE
BLACKSMITH_OPERATING_HEALTH: REGENERATION_REQUIRED

BASE_ANALYSIS: COMPLETE
PROJECT_MIGRATION_DESIGN: REQUIRED
PROJECT_MIGRATION_EXECUTION: NOT_RUN
LOCAL_VALIDATOR: NOT_RUN
PRODUCT_CODE_CHANGE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
