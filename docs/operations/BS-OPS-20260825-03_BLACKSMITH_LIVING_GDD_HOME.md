# BS-OPS-20260825-03 — Blacksmith Living GDD Home

- Status: `APPROVED_CURRENT_OPERATIONAL_OVERRIDE`
- Approved by: user directive, 2026-08-25 KST
- Work mode: `PLAN`
- Product rule delta: `NONE`
- Baseline Blacksmith main: `187cc46a49bec8b4534f1b030a62fc607551bd3a`
- Base current main observed: `e3ee0fd5301b2f9631091e4df438f3eab996de77`
- Base owner: `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`
- Pre-existing PR #196: `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`

## Machine-readable decision

```text
BS-OPS-20260825-03
HUMAN_PROJECT_HOME_IS_LIVING_GDD_VISUAL_DASHBOARD
HUMAN_RELEVANT_PROJECT_OUTPUTS_VIEWABLE_FROM_HOME
PROJECT_HOME_TOP_VISUAL_GDD_REQUIRED
PROJECT_HOME_PROJECT_SPECIFIC_PRIORITY
EXPLANATORY_VISUAL_GDD_BEFORE_DECORATIVE_ART
FULL_GAME_FLOW_VISIBLE_ON_HOME
CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME
PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME
HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING
HOME_PROJECTION_IS_NOT_DUPLICATE_CANON
AI_WORKSPACE_DETAIL_COMPLETENESS_REQUIRED
HOME_DETAIL_AI_RUNTIME_TRACEABILITY_REQUIRED
STYLIZED_DARK_FORGE = CURRENT
APPROVED_REPRESENTATIVE_VISUAL = NOT_AVAILABLE
VISUAL_GDD_GAP = OPEN
EXAMPLE_IMAGES = REFERENCE_ONLY_LAYOUT_DENSITY
PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION
IMAGE_GENERATION = NOT_REQUESTED_NOT_RUN
```

## Decision

Blacksmith의 Notion `Project Home` 역할을 기존의 사람용 학습면에서 한 단계 강화하여 **Project Living GDD + Visual Dashboard**로 정의한다. Home은 단순 소개·링크 허브가 아니며, 다른 페이지를 먼저 열지 않아도 사람이 다음을 판단할 수 있어야 한다.

1. 무슨 게임을 만드는가.
2. 플레이어는 무엇을 반복하고 무엇을 고민하는가.
3. 실제로 어떤 시스템·화면·데이터를 만들어야 하는가.
4. 최종적으로 어떤 시각 언어로 보여야 하는가.
5. 현재 무엇이 구현됐고 무엇이 아직 검증되지 않았는가.

Home에 직접 노출할 사람용 정보는 축약을 이유로 AI Workspace로 밀어내지 않는다. 다만 raw schema, internal ID, PR/SHA/CI receipt, local path/port, 구현 로그와 같은 AI/운영 정보는 기존 Project Registry/System Record와 repository operational owner가 계속 소유한다.

## Existing-solution-first architecture

### ADOPT — rich Home projection + canonical linked views

- Home: 게임 정체성·Visual GDD·Flow·핵심 수치·사람용 구현 현실을 직접 보여준다.
- Detail Canon: 같은 내용을 더 깊이 비교·수정하는 사람용 owner다.
- canonical database: 큰 구조화 데이터는 Home에 복사하지 않고 project-filtered linked view로 노출한다.
- AI/System: machine detail, evidence, validation, handoff를 보존한다.
- GitHub: 구조화/runtime truth를 보존한다.

### REJECT — compact Home + link list

핵심 시스템·비주얼·수치가 상세 페이지 안에만 남아 첫 화면에서 게임을 판단할 수 없으므로 거부한다.

### REJECT — duplicate Home tables

Home 전용 복사본을 별도 관리하면 single owner와 drift 방지 원칙을 깨므로 거부한다.

### REJECT — new dashboard/tool

기존 Notion Home·Detail·System Record·canonical database로 목적을 달성할 수 있으므로 새 유료 도구나 병렬 dashboard를 만들지 않는다.

## Visual status gate

### Current approved style

`BS-ART-20260731-01`은 현재 `CURRENT`이며 Blacksmith 그림체는 이미 확정되어 있다.

- style key: `STYLIZED_DARK_FORGE`
- 어두운 대장간의 물성·무게감
- 장비가 시각적 주인공
- 따뜻한 국소 화로 조명
- stylized/simplified 2D game illustration
- iron/brass 중심 UI 언어
- 장식보다 강화 위험·보상·작품 상태의 판독을 우선

`BS-MODAK-20260731-01`의 마스코트 방향도 보존한다.

- 밝은 노랑·주황 불 정령
- 숯 껍질 몸체는 사용하지 않음
- dark detail은 보조 요소로 제한
- 항상 웃는 마스코트가 아니라 calm/curious/worried/joyful/surprised/sad/focused 감정 범위를 유지

### Representative visual gap

Sheet `72_이미지검수_승인로그`의 fresh readback은 `BS-REV-INIT / BLOCKED_IMAGE_NOT_GENERATED`뿐이며, `71_이미지기획_생성목록`의 P0/P1 시각자료도 PLANNED/BRIEF 단계다. 따라서 실제 승인 대표 Blacksmith 이미지 파일은 현재 존재하는 것으로 주장하지 않는다.

이번 대화에서 사용자가 제공한 이미지들은 **새 Blacksmith 승인 이미지가 아니라 정보 밀도·배치·Visual GDD 설명 수준의 reference**다. 첨부 예시를 Asset 승인으로 승격하거나 게임의 현재 그림체 정본을 덮어쓰지 않는다.

이미지 생성 요청도 없으므로 이 작업에서는 image generation을 실행하지 않는다.

## Home required scroll order

```text
01 · PROJECT NORTH STAR
→ 02 · HOW THE GAME WORKS
→ 03 · HOW IT SHOULD LOOK
→ 04 · CORE GAME DATA
→ 05 · CONTENT & DESIGN
→ 06 · DEVELOPMENT REALITY
→ 07 · DETAIL LIBRARY
```

### 01 · PROJECT NORTH STAR

- 한 문장 게임 판타지
- 핵심 판매 포인트 가설
- PRIMARY = 강화의 긴장감 + DDD
- SUPPORT = 정밀제작 / 고객·세계 인과 / UID·생애 / CURRENT·MAX 내구·수리 / 경제·하루 작업량
- Android portrait-first / PC future consideration
- 확정 Visual Style + `VISUAL_GDD_GAP`

### 02 · HOW THE GAME WORKS

Home에서 직접 다음 explanatory Visual GDD를 보여준다.

- Full Game Flow
- Core System Relationship
- One Item Lifecycle
- First 10 Minutes
- Nadia Causal Slice

대표 흐름:

`고객·세계 상황 → 목적·제약 → 제작/스펙/정밀 방향 → 강화 Preview → STOP/PUSH → 성공/손상/파괴 → 정확한 UID 인계 → 지연 고객·세계 결과 → 수리/대수선/Archive/후계 → 다음 필요`

직접 전투·탐험은 기본 proof surface로 새로 도입하지 않는다.

### 03 · HOW IT SHOULD LOOK

현재 승인 style rule을 Home에서 직접 볼 수 있게 하고, 다음 Visual GDD 요구를 우선 표시한다.

- 강화 메인 화면
- 강화 DDD Feedback Ladder
- CURRENT/MAX 상태
- 수리 판단 카드
- 첫 10분 Storyboard
- 정밀강화 → 고객 Context 카드

장식용 concept art보다 **EXPLANATORY_VISUAL_GDD_BEFORE_DECORATIVE_ART**를 우선한다.

### 04 · CORE GAME DATA

사람이 실제 기획 판단에 쓰는 현재 핵심 값은 상세 페이지에만 숨기지 않는다.

- 강화 경험 밴드와 성공률 test budget
- CURRENT/MAX 구조 상태 밴드와 penalty budget
- 일반 수리의 `CURRENT = MAX / MAX unchanged`
- 보강재·수리·대수선 anchor
- DESTROYED archive 규칙
- +100 terminal payoff

현재 Canon이 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE` 또는 `TUNABLE_BASELINE_TEST_PRESET / NOT_FINAL`로 분류한 수치를 Home에서도 `TEST_BUDGET_NOT_FINAL`로 표시한다.

### 05 · CONTENT & DESIGN

Nadia starter-order 대표 인과를 보여주되 정답 recipe나 direct adventure를 새로 만들지 않는다. 고객/세계 콘텐츠는 강화 선택의 이유와 같은 UID 작품 결과를 돌려주는 SUPPORT다.

### 06 · DEVELOPMENT REALITY

사람이 이해할 수준으로만 표시한다.

- current planning reopened / PLAN
- 새 `기획 완료` 선언 전 제품 구현 Gate 닫힘
- 과거 구현 존재와 현재 whole-game experience 검증을 구분
- Human/Android/accessibility/final visual validation의 실제 미실행 상태

raw SHA/CI/port/local path는 Home에 노출하지 않는다.

### 07 · DETAIL LIBRARY

Direction / Enhancement / Visual / Production / Reference 상세 owner로 drill-down한다. 이 링크들은 깊이 보기용이며 Home의 핵심 이해를 대신하지 않는다.

## Canonical linked-view rule

가능하면 다음 현재 canonical data source를 Home에 project-filtered linked view로 연결한다.

1. `CORE SYSTEM · Master`: Blacksmith + `CONFIRMED` rows.
2. `ASSET LIBRARY · Master`: Blacksmith + `Approved=true` visual rows.

현재 approved visual view가 비어 있어도 placeholder/reference 이미지를 억지로 채우지 않는다. 빈 상태는 `VISUAL_GDD_GAP` 증거로 취급한다.

## Benchmark / professional-practice review

Fresh 2026-08-25 research was used only for information-architecture validation.

- Game Developer, `The Modern Game Design Document`: visual flow/system diagrams and living, focused design documentation principle → `ADOPT`.
- Machinations, game design/system economy documentation guidance: system inputs/rules/outputs and concrete values must be inspectable → `ADAPT` to Home core-data projection.
- commercial visual-GDD/dashboard products → connected visual structure is referenceable, but new paid tooling is `REJECT` because existing Notion surfaces already satisfy the need.

External examples do not override Blacksmith canon and no benchmark visual is copied into a product asset.

## Implementation Reality Gate

Verified in this planning task:

- Base current Home policy owner discovery: `VERIFIED`
- Blacksmith current repository/Notion/Sheet authority discovery: `VERIFIED`
- current art-style Decision existence: `VERIFIED`
- approved representative visual absence in Sheet approval log: `VERIFIED`
- repository contract/PR/CI effects: only after exact-head readback
- Notion page/view mutation: only after server readback

Not verified unless separately observed:

- Notion client-side geometry/rendering: `NOT_RUN`
- Human usability/player fun: `NOT_RUN`
- Android device: `NOT_RUN`
- accessibility: `NOT_RUN`
- final approved visual: `NOT_AVAILABLE`

## Adversarial review targets

1. Home이 다시 링크 허브로 축소되는가.
2. 사람에게 필요한 data가 AI Workspace로 숨겨지는가.
3. Home projection이 독립 canon 복제본으로 drift하는가.
4. 예시 이미지를 승인 Blacksmith art로 오인하는가.
5. test budget을 final balance로 과장하는가.
6. 과거 구현을 current whole-game PASS로 오인하는가.
7. broad management scope가 reinforcement tension + item biography를 밀어내는가.
8. raw AI/technical metadata가 Home을 오염하는가.

## Revisit conditions

다음 중 하나가 실제로 발생할 때만 이 routing을 재검토한다.

- 현재 Home만으로 게임의 플레이·Visual·핵심 data를 판단할 수 없음
- canonical linked view가 사람용 판단을 실질적으로 방해함
- 새 승인 대표 Visual이 생겨 `VISUAL_GDD_GAP`이 닫힘
- current core가 강화 긴장감 + DDD에서 변경됨
- Human test가 Home의 설명과 실제 플레이 경험이 다르다고 증명함
