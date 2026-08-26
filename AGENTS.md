# Blacksmith AI 작업 규칙

Blacksmith는 Android 세로형 Godot 제작 게임 프로젝트다. 현재 작업 상태는 `BS-OPS-20260825-08 / POSTMERGE_PLANNING / CUSTOMER_EVENT_DAMAGE_POLICY_NEXT / LIVING_GDD_HOME / ILLUSTRATED_WORKSHOP_BOOK`이며 `WORK_MODE: PLAN`이다. 일반 제품 구현은 `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`이고 현재 기획·문서·인수인계 작업이 그 Gate를 자동으로 열지 않는다.

현재 핵심 Decision은 `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03`이다. current product owner는 `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`, Decision28 exact curve owner는 `docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json`, Decision29 durability/repair owner는 `docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json`이다. 새 채팅 resume locator는 `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`다.

## 1. 권위 순서

1. 사용자의 최신 지시와 승인
2. `AGENTS.md`
3. `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md` — fresh-read cold-start locator
4. `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
5. `docs/decisions/BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md` + `docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json`
6. `docs/decisions/BS-DAMAGE-20260826-28_DAMAGE_PROBABILITY_CURVE.md` + `docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json`
7. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
8. `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`
9. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md` — `LEGACY_COMPATIBILITY_ROUTER`; 최신 override와 충돌하는 상단 역사 snapshot은 current authority가 아님
10. 2026-08-20/24 분야별 Canon·current registry — Decisions25~29/Art03과 같은 필드가 충돌하면 역사·부분대체 evidence
11. 실제 `code/data/Scene/Resource/tests`와 runtime evidence — 구현 사실은 증명하지만 PLAN Gate의 구현 drift가 최신 승인 기획을 덮어쓰지 않음
12. `NOTION_HUMAN_FACING_CANON`: 사람용 Project Home·Visual/Flow·비교표·에셋/Reference
13. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장
14. R2/R3 Game Bible·과거 PoC·구형 data/runtime
15. Google Sheet 등 `MIGRATION_ONLY_UNTIL_REMOVAL` compatibility 자료
16. 외부 벤치마크·과거 대화·AI 추론

현재 workspace routing:

- `Notion Project Home = HUMAN_PROJECT_HOME_IS_LIVING_GDD_VISUAL_DASHBOARD`
- `HUMAN_RELEVANT_PROJECT_OUTPUTS_VIEWABLE_FROM_HOME`
- `EXPLANATORY_VISUAL_GDD_BEFORE_DECORATIVE_ART`
- `Project Registry / System Record = AI_OPERATIONAL_SURFACE`
- `REPOSITORY_STRUCTURED_CANON` / `REPOSITORY_RUNTIME_TRUTH` = Markdown·JSON·game data·code·Scene/Resource·tests·CI/runtime truth
- Google Sheet = unique 미이관 자료와 same-ID compatibility mirror가 필요한 경우의 migration surface. 신규 기본 기획 작업공간이나 runtime 증거가 아니다.

`BS-OPS-20260825-03`에 따라 사람용 Home은 단순 링크 허브가 아니다. 게임 정체성 → 플레이 구조 → 핵심 시스템 → Flow → UI/Visual 방향 → 핵심 사람용 데이터 → 콘텐츠 맥락 → 사람용 구현 현실을 스크롤 안에서 직접 이해할 수 있어야 한다.

### 1.1 Human Home · Visual GDD 규칙

- current art-direction Decision은 `BS-ART-20260825-03`.
- `ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK`.
- `ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION`.
- 손그림 공방 노트, 종이·가죽·철·목재 물성, 따뜻한 공방 분위기, 현대적 판독 가능한 상호작용 계층을 사용한다.
- 기존 `STYLIZED_DARK_FORGE`/검정·금색 생성형 보드는 `LEGACY_VISUAL_REFERENCE_NOT_FINAL_STYLE_CANON`; 정보구조 참고 외 자동 재사용하지 않는다.
- 기존 8개 Visual GDD는 `INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD` reference이며 final style/runtime/release asset 승인이 아니다. old CURRENT/MAX 값·old MAX penalty·구형 precision·날짜별 강화 로그는 `SYSTEM_SEMANTICS_STALE`이다. Decision29이 숫자 내구도를 다시 도입했다고 해서 구형 수치/공식이 되살아나는 것은 아니다.
- 사용자가 제공한 예시 이미지는 `REFERENCE_ONLY_LAYOUT_DENSITY`이며 승인 Asset으로 승격하지 않는다.
- 사람에게 필요한 핵심 수치·규칙·밸런스 표를 AI Workspace에만 숨기지 않는다.
- `Asset Library row / Approved=true / Drive Source`는 `Notion Preview binary` 증거가 아니다.
- Notion server readback은 실제 client geometry/render 관찰을 대체하지 않는다.
- 대표 재생성은 current mechanic sync 뒤 `Main Menu / Enhancement Main(+1 + visible durability) / +9→+10 Precision Keyword / Durability·Repair·Structural Scar / Event-only Chronicle` 순으로 소수 화면부터 검증한다.

## 2. 필수 작업 순서

```text
현재 권위·변경 경계 확인
→ PRE_WORK_RESEARCH_GATE
→ ADOPT / ADAPT / REJECT / DIFFERENTIATOR + 정본 충돌 + 적대 pre-check
→ brainstorming·적대적 검토
→ RED: 실패 계약 테스트 작성·의도한 실패 관측
→ GREEN: 최소 정본·구현 변경
→ REFACTOR: 중복·구형 참조 정리
→ exact-head 전체 검증
→ GitHub·Notion/repository destination readback
→ 같은 승인 범위는 재승인 없이 병합 / 새 planning conflict·scope expansion만 사용자 Decision
```

### PRE_WORK_RESEARCH_GATE

Decision `BS-OPS-20260811-02`.

- 게임 기획·콘텐츠·UX·경제·시장 포지셔닝: 직접/인접 유사작 2개 이상 + 현업/공식/1차 자료 2개 이상. 핵심 시스템·경제·출시·권리·접근성은 유사 사례 3개 이상 + 공식/1차 자료 2개 이상을 기본으로 한다.
- 기술·Godot·Android·GitHub·CI·tooling·performance: current 공식/1차 자료 1개 이상 + 유사 구현/추가 공식 자료 1개 이상과 버전 호환성을 확인한다.
- 저위험 maintenance는 현재 정본·최근 PR·공식 책임 원본을 다시 읽고 외부 비교가 무관하면 `BENCHMARK_NOT_APPLICABLE` 사유를 남긴다.
- 벤치마크의 수치·확률·경제·보상을 Blacksmith 정본으로 자동 역수입하지 않는다.

### 작업마다 TDD

```text
RED → GREEN → REFACTOR
```

테스트를 먼저 작성하고 의도한 RED를 실제 관측한다. 최소 변경으로 GREEN을 만든 뒤에만 정리한다. 문서·기획 변경도 기계 판독 계약 테스트로 보호한다.

## 3. 승인 배치와 조기 체크포인트

- 승인 10건은 최대 배치 크기다.
- `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT`에서는 조기 체크포인트를 허용한다.
- 같은 승인 범위는 exact technical validation 뒤 병합 재승인을 요구하지 않는다. 새 기획 충돌·범위 확장만 별도 사용자 Decision이 필요하다.
- 병합 뒤 main SHA와 필요한 Notion/repository destination을 다시 읽는다. Legacy Sheet는 migration/same-ID reconciliation 대상일 때만 갱신한다.

## 4. 현재 코어 보호

- PRIMARY CORE는 `강화의 긴장감 + DDD`; player question은 `STOP OR PUSH`.
- 작품은 UID·소유·손상·복원·사건·연대기를 유지한다.
- 일반 강화 성공은 항상 `SUCCESS_LEVEL_DELTA = +1`.
- `+9 -> +10 = PRECISION_ENHANCEMENT` 하나뿐이며 성공 시 플레이어용 `ITEM_KEYWORD` 하나, machine owner는 `CATALYST_AFFIX`. 네 번째 affix 슬롯 금지.
- machine slots는 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`.

### 4.1 Decision29 current durability authority

```text
BS-REPAIR-20260826-29
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
BASE_MAX_DURABILITY = immutable birth durability
0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
NORMAL = CURRENT_DURABILITY == MAX_DURABILITY
MINOR = 0.50 < CURRENT_DURABILITY / MAX_DURABILITY < 1.00
MAJOR = 0 < CURRENT_DURABILITY / MAX_DURABILITY <= 0.50
DESTROYED = CURRENT_DURABILITY == 0
CURRENT_MAX_AUTHORITY = SUPERSEDED = HISTORICAL_DECISION26_ONLY
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
```

숫자 CURRENT/MAX는 숨은 보조축이 아니라 **보이는 유일한 gameplay durability authority**다. 네 상태는 숫자에서 파생되는 player-facing view다.

`DAMAGE_EVENT_CURRENT_LOSS = 1`은 `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`다.

### 4.2 Decision28 target risk + Decision29 durability modifier

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
+11 5% / +30 6% / +60 7% / +90 8% / +100 10%
DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
```

Decision28 anchors are 유지된다. Decision29 temporary state modifiers:

```text
NORMAL: success 0pp / new effect ×1.00 / damage risk ×1.00
MINOR:  success -3pp / new effect ×0.90 / damage risk ×1.25
MAJOR:  success -7pp / new effect ×0.75 / damage risk ×1.75
DURABILITY_MODIFIERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

Hard guarantee는 실제 100% 성공을 유지한다. 효과 배율은 새 ordinary enhancement effect에만 적용하고 기존 스탯·+1 레벨·+10 keyword cardinality를 줄이지 않는다.

```text
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, STATE)
= Decision28_base_probability(TARGET) * Decision29_state_multiplier(STATE)
```

모든 확률은 여전히 enhancement failure에 조건부다. `FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED`, `UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED`.

### 4.3 Repair / MAX scar

```text
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY
DESTROYED_REPAIR_ALLOWED = FALSE
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
MAX_DURABILITY_RECOVERY = NOT_APPROVED
```

임시 repair quality:

```text
EXCELLENT 20% -> post-scar MAX 100%
STANDARD  60% -> post-scar MAX 75%
POOR      20% -> post-scar MAX 50%
REPAIR_MINIMUM_CURRENT_GAIN_WHEN_POSSIBLE = 1
```

임시 MAX -1 scar chance:

```text
            +0~10  +11~30  +31~60  +61~90  +91~100
MINOR         10%      15%      20%      25%       30%
MAJOR         25%      30%      35%      40%       45%
MAX_SCAR_AMOUNT_ON_TRIGGER = -1
MAX_DURABILITY_FLOOR = 1
```

모든 상세 수치는 `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`. 수리비·재료비는 `NOT_FINAL / FOLLOWUP_REBASE_REQUIRED`이며 구형 CURRENT→MAX 수리비 공식과 `MAX +15 / cap60` 대수선은 fallback이 아니다.

### 4.4 Other current rules

- `CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE`; 구매/인계 자체는 damage가 아니다. 정확 event eligibility/probability는 후속 Gate.
- `ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE`; 제작·키워드·손상·MAX scar 수리·인계·세계 결과·파괴 등 의미 사건만 player Chronicle.
- 제작 등급은 `보통 / 우수 / 명품 / 걸작 / 전설`.
- 예술성은 단계명 없는 `1~10`, 전투력을 기본적으로 올리지 않는다.
- 보조재료 슬롯과 일반 수식어 A·B는 재도입하지 않는다.

## 5. 보호 경로

새 `기획 완료` 사용자 선언 전 변경 금지:

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

일반 제품 구현은 `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`. 현재 V2 runtime의 `current_durability/max_durability` 필드명이 Decision29와 유사해도 구현 증거가 아니다. 기존 resolver semantics는 여전히 `IMPLEMENTATION_DRIFT / HISTORICAL_RUNTIME_TRUTH`다.

## 6. 정본·구형 문서

- 한 질문에는 활성 책임 원본 하나만 둔다.
- `[대체됨] / [부분 대체됨] / [보류] / [폐기] / [역사 증거]`를 직접 표시한다.
- Decision26의 `CURRENT_MAX_AUTHORITY = SUPERSEDED`와 one-state-per-event는 Decision29에 의해 같은 필드에서 부분대체됐다.
- 구형 CURRENT/MAX 수치·MAX penalty·repair price·overhaul 공식은 Decision29이 아니다.
- 구형 `HOLD / DOWNGRADE / DAMAGE / CRITICAL` 비율은 Decision28/29 확률 또는 failure composition fallback이 아니다.
- `CURRENT_CONFIRMED_DECISIONS.md`는 역사 원장이다.
- PR #81은 `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT`.
- pre-existing PR #196은 `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`; 현재 PR과 흡수·수정·병합하지 않는다.

## 7. 완료 증거

- expected/exact HEAD 고정
- Base current owner/main 확인
- Python contracts + 관련 CI
- changed files·보호 경로 감사
- PR 댓글·인라인 스레드
- 필요한 Notion/repository destination readback
- Sheet가 실제 same-ID migration 대상일 때 provenance readback
- 미실행 runtime·Android·접근성·성능·사람 플레이는 `NOT_RUN`
- Notion server readback은 client 실제 렌더 관찰을 대체하지 않는다.

## 8. 플랫폼 출시·에셋 권리

출시·외부 자산·AI·외주 작업은 다음 프로젝트 증거를 읽는다.

- `docs/PLATFORM_RELEASE_AND_ASSET_RIGHTS_PROFILE.md`
- `docs/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- `docs/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`

필수 권리·계약·약관·플랫폼 답변이 미확인이면 `RELEASE_BLOCKED_UNVERIFIED`. 제품 구현 BLOCKED 상태와 실제 제출·법률 검토·최종 등급 미실행 상태를 바꾸지 않는다.

## 9. Godot·Godot AI·GUT·Hera 권위와 진입 Gate

### 9.1 Current host/runtime routing

현재 runtime/toolchain 선택은 사용자 제공 v4.8 r5.4와 최신 Base owner를 따른다.

- 프로젝트별 동일 Godot binary 복사본·전용 포트를 기본적으로 증식하지 않는다.
- shared approved exact Godot pin + shared approved Godot AI exact pin + provider fixed/default ports가 기본.
- 프로젝트 격리는 exact repository/worktree/project path + editor/session identity로 보장.
- 과거 Blacksmith 전용 `8006/9506`은 `HISTORICAL_ONLY / DO_NOT_REUSE_AS_DEFAULT`.
- current official version은 작업 시 upstream fresh-read와 safe-update/rollback/canary Gate를 거친다.

### 9.2 Historical authority / adoption records

- `HIGODOT_SOLE_AUTHORING_AUTHORITY`: `BS-HIGODOT-20260808-01` 사용자 승인으로 HiGodot은 Production Scene·Node·Resource·`project.godot` 설정의 단일 저작 권위로 활성화됐다.
- `GUT_SOLE_TEST_AUTHORITY`: GUT 9.7.1은 `BS-TEST-20260806-01` 및 postmerge closure에 따라 `FORMALLY_ADOPTED_ACTIVE`, GDScript 단위·통합 테스트 프레임워크 단일 권위다.
- `ENTRY_GATE_FAIL_CLOSED`: 결정 원장·미확정/감사·이미지 목록/검수·열린 PR exact HEAD 중 하나라도 누락/stale/schema drift이면 작업 진입을 차단한다.
- HiGodot current authority는 `FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY / USER_APPROVED_ACTIVE`; 당시 범위는 `TASK2_SCOPED_AUTHORING_ONLY`였으며 일반 제품 Gate를 열지 않는다.
- `.tscn`/Resource/`project.godot` 변경은 승인 production-authoring provenance가 있어야 하며 GitHub Contents API/직접 텍스트 치환으로 Godot 직렬화 surface를 우회하지 않는다.
- `BS-HERA-20260808-01`: `VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE` 역사 record.
- `BS-TOOLCHAIN-20260809-01`: Godot AI 3.1.3 역사 baseline, GUT editor plugin enabled, Hera enabled non-authoritative.
- `BS-TOOLCHAIN-20260811-02`: Godot AI 3.1.4 역사 current-version record; 새 작업의 최신 pin을 자동 결정하지 않는다.
- GUT runtime은 Git 추적 파일을 수정할 수 없고 HiGodot은 `tests/gut/**`, `.gutconfig.json`, `addons/gut/**`, JUnit 성공 결과를 수정할 수 없다. Hera authoring/mutation authority는 별도 승인 전 `NONE`.

## 10. 현재 프로젝트 총 작업지시문

- current task execution contract: `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.8-r5.4_SUPERSET_FINAL_20260826.md`
- `CURRENT_EXECUTION_CONTRACT_STATE: USER_SUPPLIED_V4_8_R5_4_SUPERSET_FINAL_CURRENT`
- previous `v4.8-r4` is `HISTORICAL_SUPERSEDED_BY_R5_4`.
- repository-tracked `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md` v4.5 r2는 `TRACKED_V4_5_R2_STALE_SUPERSEDED_DO_NOT_USE`.
- historical compatibility anchor: `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md` (`v4.5 r2`) — historical only.
- current operational override Decisions: `BS-OPS-20260825-08`, `BS-OPS-20260825-07`, `BS-ENHANCE-20260825-25`, `BS-DAMAGE-20260825-26`, `BS-DAMAGE-20260826-28`, `BS-REPAIR-20260826-29`, `BS-CHRONICLE-20260825-27`, `BS-ART-20260825-03`, `BS-OPS-20260825-03`, `BS-OPS-20260825-02`.
- 프로젝트 바인딩 historical Decision: `BS-OPS-20260811-01`.
- 선행 조사 Gate: `BS-OPS-20260811-02 / PRE_WORK_RESEARCH_GATE`.
- `PRODUCT_IMPLEMENTATION: BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`, `TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED` 유지.
