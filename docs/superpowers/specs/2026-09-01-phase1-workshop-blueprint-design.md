# 모루의 서약 — Phase 1 세로형 공방 블루프린트 설계

~~~
STATUS = USER_APPROVED_DIRECTION / WRITTEN_SPEC_REVIEW_PENDING
DESIGN_DATE = 2026-09-01
ARTIFACT_CLASS = IMPLEMENTATION_BLUEPRINT_CANDIDATE / NON_RUNTIME
SCOPE = CURRENT_CANON_MVP / PHASE_1_WORKSHOP_INFORMATION_ARCHITECTURE
NO_CANON_OWNER_REPLACEMENT = TRUE
NO_RUNTIME_OR_ASSET_PROMOTION = TRUE
TEXT_NATIVE_FLOW_MAP = MERMAID
GENERATED_UI_SCREENSHOT_AS_PRODUCT_ASSET = FALSE
WRITTEN_SPEC_USER_REVIEW_REQUIRED_BEFORE_IMPLEMENTATION = TRUE
~~~

## 1. 작업 전 문제와 목표

현재 세로 슬라이스에는 강화, 정밀강화, 내구도, 인계, 결과, 연대기를 연결하는
실제 코드와 승인된 이미지가 있다. 그러나 실제 화면의 정보가 긴 스크롤과 부분
제어에 흩어져 있어, 플레이어가 한 작품의 다음 행동을 아래 순서로 읽기 어렵다.

~~~text
무엇을 강화하는가?
→ 지금 시도하면 무엇을 얻거나 잃는가?
→ +10 단위에서 어떤 태그 행동과 촉매가 필요한가?
→ 이 작품이 고객의 실제 사용 뒤 어떻게 돌아오는가?
~~~

이 블루프린트의 목표는 새 경제나 새 그림을 추가하는 일이 아니라, 이미 승인된
STOP OR PUSH 코어를 Android 세로 화면에서 한 작품의 생애 흐름으로 보이게
정리하는 것이다. 제목은 사용자가 확정한 모루의 서약을 사용한다.

## 2. 정본 경계와 바꾸지 않는 규칙

이 문서는 화면·상태·자산의 소비 구조만 제안한다. 다음 제품 의미와 숫자를
소유하거나 대체하지 않는다.

| 질문 | 현행 정본 owner | 블루프린트에서의 처리 |
| --- | --- | --- |
| 강화의 핵심 질문과 Phase 1 범위 | BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md | STOP OR PUSH와 하나의 같은 UID 생애를 화면 흐름으로 표현 |
| 손상·수리·흉터 | Decisions 28/29/31 | 확률·수리비·durability 계산을 다시 계산하지 않고 service 출력만 표시 |
| 고객·세계 실제 사용 결과 | Decision 30 | 인계 자체는 손상을 만들지 않으며, 실제 사용 결과만 귀환 화면으로 표시 |
| 정밀 target·태그 행동 | Decisions 37/38 | PRECISION_TARGETS = [10,20,30,40,50,60,70,80,90,100], 최대 태그 3개, I–IV를 읽기 쉽게 배치 |
| 정밀 촉매의 이름·소모 | BS-ENHANCE-20260901-40 | 불의 심장 / 대지의 결정을 실제 소모 재료로 표시. 계보 선택으로 되돌리지 않음 |
| 시각 방향·이미지 승격 | Decisions 03/04 | ILLUSTRATED_WORKSHOP_BOOK, 실제 consumer, 사후 사용자 lock을 유지 |

~~~
NO_NEW_PRECISION_WORKSHOP_BACKGROUND = TRUE
NO_NEW_CATALYST_RASTER_ASSET = TRUE
NO_GRADE_VARIANT_EQUIPMENT_ART = TRUE
NO_NEW_GENERAL_INVENTORY_SCREEN = TRUE
NO_NEW_CUSTOMER_MANAGEMENT_OR_WAITING_LOOP = TRUE
NO_FAKE_DAMAGE_FOR_DEMONSTRATION = TRUE
~~~

NO_NEW_CATALYST_RASTER_ASSET = TRUE는 현재 Decision 40의 명시적 경계다.
촉매는 네이티브 텍스트·수량·비활성 상태로 충분히 판독되어야 한다. 실제 Android
관찰에서 그 상태가 읽히지 않는다는 증거가 생긴 경우에만, 별도 Visual Requirement와
사용자 lock을 거쳐 아이콘 후보를 다시 제안한다.

## 3. 조사·비교와 채택 판단

조사는 2026-09-01 KST에 공식 제품 페이지와 공식 Godot 문서를 기준으로
진행했다. 아래의 수치·경제·등급 구조는 Blacksmith로 자동 이식하지 않는다.

| 비교 대상 | 관찰한 강점 | 판단 | 모루의 서약 적용 |
| --- | --- | --- | --- |
| [Blacksmith Master](https://store.steampowered.com/app/2292800/Blacksmith_Master/) | 자원부터 제작·판매까지의 공방 목적성이 분명함 | REJECT | 채굴·직원·물류 운영으로 확장하지 않음. 한 작품의 판단을 우선 |
| [Anvil Saga](https://store.steampowered.com/app/1587540/Anvil_Saga/) | 고객·사건·대화가 대장장이의 결정을 맥락화 | ADAPT | 인계 후 실제 사용 결과와 연대기로 작품 맥락을 되돌림. 다중 세력 운영은 제외 |
| [Forge Ahead](https://apps.apple.com/us/app/forge-ahead-be-a-blacksmith/id1485491919) | 모바일에서 조작 직후 결과가 보이는 짧은 리듬 | ADOPT | 일반 강화 버튼 바로 아래에 결과·다음 선택을 배치. 탭 수익·idle loop는 제외 |
| [Blacksmith of the Sand Kingdom](https://www.kemco.jp/game/sandkingdom/en/index.html) | 만든 장비가 사용·보유·판매의 목적과 연결됨 | ADAPT | 장비 UID가 고객 실제 사용 결과까지 이어짐. 파티 RPG·탐험으로 넓히지 않음 |
| [While the Iron's Hot](https://www.humblegames.com/games/whiletheironshot/) | 제작 결과가 세계의 다음 행동과 연결됨 | ADAPT | 고객·세계 결과는 작품 연대기의 의미 사건으로만 기록. 탐험 퍼즐 loop는 제외 |
| [Potion Craft](https://store.steampowered.com/app/1210320/Potion_Craft_Alchemist_Simulator/) | 따뜻한 손그림 공방 테두리와 중앙 결정 영역의 대비 | ADOPT | 기존 공방 배경은 주변의 물성을, 중앙 Panel은 수치·버튼의 판독성을 담당 |
| [Godot Container 가이드](https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html) | Container가 세로형 반응형 레이아웃의 크기·배치를 소유 | ADOPT | MarginContainer → ScrollContainer → VBoxContainer가 화면 폭·안전 여백을 소유 |
| [Godot Theme 레퍼런스](https://docs.godotengine.org/en/stable/classes/class_theme.html) | 반복되는 Control override보다 Theme의 일관된 역할 분리 | ADOPT | 상태색·버튼·패널 역할은 중앙 Theme로, 도메인 결과는 presenter text로 분리 |

### 적대적 사전 검토

| 위험 또는 반대 질문 | 판정 | 설계 방어 |
| --- | --- | --- |
| 한 화면에 모든 정보를 넣으면 더 답답해지지 않는가? | 유효한 위험 | 선택 전에는 현재 작품·다음 시도·다음 목적지만 보이고, 태그·수리·연대기는 조건 충족 시만 열림 |
| 촉매를 계보 버튼처럼 보이게 만들 위험은? | 차단 필요 | 불의 심장 ×1, 대지의 결정 ×1은 수량을 가진 재료로만 표시. tag upgrade에서는 필요 촉매를 자동 해석해 read-only로 표시 |
| 등급이 달라질 때 장비 외형도 바꾸게 되는가? | 금지 | 동일 장비 종류의 identity art는 V2 투명 장비 그림 하나를 유지. 강화·태그는 프레임, 배지, 텍스트, 상태 atlas로 표현 |
| 새 촉매 그림이 없어도 판독 가능한가? | 아직 runtime 증거 없음 | 현 단계에서는 native text-first. Android 실기기 관찰이 NOT_RUN이므로 아이콘 생성으로 성급히 보완하지 않음 |
| 정밀 전용 배경을 다시 만들면 멋있어지지 않는가? | 정본과 충돌 | 현행 NO_NEW_PRECISION_WORKSHOP_BACKGROUND를 유지하고 공방 배경 안의 네이티브 UX로 해결 |

## 4. Phase 1 플로우 맵

이 지도는 문서에 남는 편집 가능한 구조 정보다. raster flow image가 아니며 게임
asset도 아니다.

~~~mermaid
flowchart TD
    A["메인 메뉴\n모루의 서약"] --> B["첫 제작\n장비 종류 선택"]
    B --> C["공방: 같은 UID 작품\n장비 정체성·레벨·상태"]
    C --> D{"다음 target"}
    D -->|"일반 target"| E["일반 강화\n성공 / 실패·유지 / 실패·손상"]
    E --> C
    D -->|"+5"| F["제작 리듬 표식\n연출만, 새 태그 없음"]
    F --> C
    D -->|"+10 단위"| G["정밀 패널\n태그 추가 또는 강화"]
    G --> H{"사전 조건"}
    H -->|"선택·Gold·보강재·촉매 충족"| I["정밀 시도\n원자적 결제 후 해소"]
    H -->|"부족 또는 미선택"| G
    I --> C
    C -->|"손상 뒤 repair job 가능"| J["수리 패널\n현재/MAX/BASE_MAX 표시"]
    J --> C
    C -->|"인계"| K["고객 실제 사용\n인계 자체는 손상 없음"]
    K --> L["결과 귀환\n고객/세계 결과와 상태"]
    L --> M["작품 연대기\n의미 사건만"]
    M --> C
~~~

### 상태 전이 경계

| 화면 상태 | 화면이 하는 일 | 화면이 하지 않는 일 |
| --- | --- | --- |
| 일반 강화 준비 | target·성공·실패 유지·손상 확률, 비용, CTA 표시 | 확률을 재계산하거나 실패 결과를 임의 변경하지 않음 |
| 정밀 태그 추가 | 촉매·방식·미리보기·비용을 명시하고 시도 전 blocker 표시 | 무작위 태그, reroll, 네 번째 affix를 만들지 않음 |
| 정밀 태그 강화 | 선택 태그가 요구하는 촉매를 자동 표시 | 다른 촉매로 우회하거나 촉매 선택을 중복 요구하지 않음 |
| 손상 수리 | derived condition 및 수리 가능 여부를 표시 | destroyed 수리 허용, MAX 회복, 수리비 곡선 수정 |
| 인계/결과 | 같은 UID의 실제 사용 결과와 다음 선택 표시 | 인계만으로 손상을 가짜로 만들거나 고객 관리 loop 생성 |

## 5. 세로 화면 와이어프레임

### 5.1 공통 화면 뼈대

~~~text
┌─────────────────────────────────┐
│ [모루의 서약 로고]       [설정] │
│─────────────────────────────────│
│ 안전 여백 / ScrollContainer      │
│  └ VBoxContainer                 │
│     1. 현재 작품 identity        │
│     2. 지금의 판단                │
│     3. 조건부 세부 패널           │
│     4. 다음 목적지                │
└─────────────────────────────────┘
~~~

로고·배경·장비 그림은 장식용으로 화면을 차지하지 않는다. 공방 배경은 주변의
종이·가죽·철·목재 분위기를 담당하고, 중앙 PanelContainer가 상호작용과 숫자를
충분한 대비로 책임진다.

### 5.2 메인 메뉴와 첫 제작

~~~text
┌─────────────────────────────────┐
│          모루의 서약             │
│  [기존 main_menu_dawn 배경]      │
│                                 │
│      “한 번 더 벼릴 것인가?”     │
│                                 │
│       [새 작품 만들기]           │
│       [이전 공방 계속하기]       │
└─────────────────────────────────┘

새 작품 만들기
┌─────────────────────────────────┐
│ 장비를 고르세요                  │
│ [검] [방패] [활]                 │
│ [갑옷] [투구]                    │
│  투명 V2 장비 identity art       │
│  → 제작 확정                     │
└─────────────────────────────────┘
~~~

장비 선택은 실제 이미지가 도움이 되는 소비처다. 이미 사용자 lock을 받은 다섯
V2 투명 장비 그림을 그대로 쓴다. 장비 등급에 따라 같은 종류의 그림을 바꾸지
않는다.

### 5.3 공방 — 기본 강화 상태

~~~text
┌─────────────────────────────────┐
│ < 공방                   작품 연대 │
│ [검 identity art]  이름 / UID     │
│ +12  보통 · 예리함 II              │
│ 현재 4 / 최대 5 / 출생 5           │
│ 상태: 경미 손상                    │
│─────────────────────────────────│
│ 다음: +13                          │
│ 성공 72.0% | 실패·유지 22.0%       │
│ 실패·손상 6.0%                     │
│ 비용: Gold · 보강재                │
│          [일반 강화 시도]          │
│─────────────────────────────────│
│ [손상 수리]             [인계]    │
└─────────────────────────────────┘
~~~

핵심 CTA는 한 화면에서 하나다. 조건 충족 전에는 구매·상점·새 아이템을 찾게
하지 않고, 왜 막혔는지를 CTA 가까이에 설명한다. +5는 짧은 제작 리듬 표식이며,
새 태그 선택으로 보이지 않게 한다.

### 5.4 정밀강화 — +10 단위 패널

~~~text
┌─────────────────────────────────┐
│ 정밀강화 +20                      │
│ 태그 행동  [태그 추가] [태그 강화]│
│─────────────────────────────────│
│ 태그 추가                         │
│ 정밀 촉매                         │
│ [불의 심장 · 보유 63]             │
│ [대지의 결정 · 보유 64]           │
│ 정밀 방식  [날 세우기] [경량 담금]│
│ 결과: 불의 심장 · 예리함 I         │
│ 비용: Gold · 보강재 · 촉매 ×1     │
│          [정밀강화 시도]          │
│─────────────────────────────────│
│ 태그 강화일 때                    │
│ [기존 태그 선택]                  │
│ 필요 촉매: 불의 심장 ×1 (자동)    │
│ 결과: 예리함 I → II               │
└─────────────────────────────────┘
~~~

첫 +9 → +10은 태그 추가만 허용한다. 이후 +20 … +100은 유효한 태그 추가
또는 기존 I–III 태그 강화가 된다. 장비가 검·방패·활이 아니면 정밀 패널은
이유를 보이고 시도를 열지 않는다. native Control만 사용하며 정밀 전용 그림,
촉매 아이콘, full-frame fake screenshot은 사용하지 않는다.

### 5.5 결과 귀환·수리·연대기

~~~text
┌─────────────────────────────────┐
│ 나디아의 실제 사용 결과           │
│ [같은 검 identity + 필요시 상태]  │
│ 결과: 임무 성공 / 손상: 없음      │
│ [공방으로 돌아가기]               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 수리                              │
│ 현재 2 / 최대 4 / 출생 5          │
│ 상태: 중대 손상                   │
│ 비용과 가능한 결과                │
│ [수리 시작]                       │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 작품 연대기                       │
│ 제작 · +10 태그 · 손상 · 수리     │
│ 인계 · 세계 결과 · 파괴만         │
│ [공방으로 돌아가기]               │
└─────────────────────────────────┘
~~~

결과 귀환에는 기존 customer_result_return_illustration_v1을, 실제 손상
상태가 생긴 경우에만 기존 durability state atlas를 조건부로 사용한다. routine
강화 로그를 연대기에 모두 쌓지 않는다.

## 6. UI 구조와 구현 소유 경로

| UI 역할 | 예상 Godot 구조 | 도메인 소유자 | 구현 경계 |
| --- | --- | --- | --- |
| 안전 여백·세로 흐름 | MarginContainer → ScrollContainer → VBoxContainer | scene / Theme | Container가 배치와 반응형 크기를 소유 |
| 작품 identity hero | TextureRect + labels | equipment catalog / workshop presenter | V2 투명 장비 art, UID, 레벨, 태그 읽기 |
| 강화 판단 카드 | native PanelContainer, labels, CTA | enhancement action/result presenter | resolver의 확률·비용·해소 결과를 그대로 표시 |
| 정밀 패널 | native action/tags/catalyst/method controls | scripts/vertical_slice/ui/vs_workshop_screen.gd | ADD_TAG/UPGRADE_TAG 입력을 action service에 전달 |
| 촉매 수량·부족 | label, disabled CTA, local error text | material_stock, Decision 40 resolver | 아이템명·×1·부족 사유를 표시 |
| 수리 카드 | condition labels, job CTA | repair resolver | CURRENT/MAX/BASE_MAX를 표시하고 새 계산은 하지 않음 |
| 인계·결과·연대기 | transition CTA / result panel | customer/world and chronicle services | 같은 UID의 의미 사건을 읽기 전용으로 보여 줌 |

후속 구현은 기존 scenes/vertical_slice/screens/vs_workshop_screen.tscn과
scripts/vertical_slice/ui/vs_workshop_screen.gd를 우선 소비처로 사용한다.
새 scene·background·addon으로 갈라지지 않는다. 동적 native control을 정리할
때에도 tag/catalyst 선택의 안정 ID는 visible text가 아니라 현행 catalog ID로
전달한다.

## 7. 자산·UI 제작 판단

| 화면 소비처 | 사용할 자산 또는 UI | 현재 상태 | 이번 블루프린트 판단 |
| --- | --- | --- | --- |
| 메인 메뉴 | anvil_oath_logo_ao02_v1.png, main_menu_dawn_background_v1.png | 승인·구현됨 | REUSE |
| 첫 제작·공방 identity | 검·방패·활·갑옷·투구 V2 투명 PNG | 5종 모두 승인·구현됨 | REUSE |
| 공방 배경 | workshop_enhancement_background_v2.png | 승인·소비처 있음 | REUSE |
| 실제 손상 상태 | workpiece_durability_state_atlas_v1.png | 승인·조건부 소비처 있음 | REUSE_ONLY_WHEN_DAMAGED |
| 고객 결과 | customer_result_return_illustration_v1.png | 승인·구현됨 | REUSE |
| 정밀강화 | native labels/buttons/disabled states | Decision 40 경계 | BUILD_NONE |
| 촉매 아이콘 | 없음 | actual readability 증거 없음 | DEFER |
| 정밀 전용 배경 | retired | 사용자가 이미 UX-only로 결정 | DO_NOT_RECREATE |

따라서 이번 단계에서 새 raster 이미지, generated mockup, SVG 대체 그래픽,
third-party UI/addon은 만들지 않는다. 이는 자산을 비워 두는 것이 아니라,
각 화면이 이미 가진 실제 consumer와 승인된 이미지로 먼저 완성도를 확보하는
선택이다.

## 8. 구현 전 수용 계약과 증거 한계

서면 설계가 승인되면 다음 순서로 구현 plan을 작성한다.

1. 작은 contract test에서 정밀 target, 촉매 명칭, 태그 행동, asset reuse/retirement
   경계를 먼저 RED로 관찰한다.
2. Theme·Container·workshop native control을 최소 변경으로 정리하고, 기존
   resolver/service 결과를 presenter에 연결한다.
3. blocked/normal/precision/repair/handoff-return 상태를 GUT·Python contract로
   검증한다.
4. Blacksmith의 실제 Godot runtime을 열어 portrait 화면을 capture하고, 실제
   Blacksmith process와 scene identity를 증명한다.
5. branch exact-head 검증, GitHub PR, CI, merge 승인 경로, main readback을 수행한다.

현재 이 문서가 주장하는 증거 ceiling은 아래와 같다.

~~~
repository_blueprint_contract = PENDING_LOCAL_MACHINE_VALIDATION
godot_runtime = NOT_RUN
android_device = NOT_RUN
accessibility = NOT_RUN
performance = NOT_RUN
human_player_experience = NOT_RUN
release = NOT_RUN
~~~

Android의 한 손 도달성, 글자 판독성, 촉매 표현의 충분성, 강화의 재미는 실제
capture와 사람 플레이 전에는 PASS가 아니다.

## 9. 서면 검토 뒤의 작업 단위

사용자가 이 서면 블루프린트를 검토·확정한 뒤에만 writing-plans 단계로
들어간다. 그 plan은 다음을 하나의 exact-head 구현 단위로 쪼갠다.

1. Workshop 화면 계층과 Theme 역할 정리.
2. 일반 강화와 +5 제작 리듬의 명확한 결과 표현.
3. +10 단위 태그 추가·강화의 native precision 패널.
4. 촉매 수량·부족·원자적 소모 결과의 text-first 상태.
5. repair, handoff-return, chronicle의 같은 UID 귀환 흐름.
6. 실제 portrait capture와 GitHub destination readback.

새 촉매 이미지는 이 목록의 선행 조건이 아니다. 이후 runtime evidence가
텍스트만으로 실제 판독 실패를 보일 때만 NEEDED → BRIEF_READY →
GENERATED_CANDIDATE → USER_APPROVED의 별도 경로를 시작한다.
