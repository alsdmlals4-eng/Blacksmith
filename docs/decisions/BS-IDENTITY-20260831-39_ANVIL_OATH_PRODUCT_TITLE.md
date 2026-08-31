# BS-IDENTITY-20260831-39 · ANVIL OATH / 모루의 서약 제품명

- 상태: `USER_APPROVED_CURRENT`
- 사용자 확정: `2026-08-31 KST`
- 현재 제품명: Korean primary `모루의 서약` / Latin title lockup `ANVIL OATH`
- 적용 상태: `MERGED_MAIN / MACHINE_VERIFIED / LIMITED_RUNTIME_VERIFIED`
- 법률·상표 상태: `NOT_RUN / NO_CLEARANCE_CLAIM`

## 결정과 역할

이 문서는 Blacksmith 프로젝트의 **제품명·표기·로고 소비처**만 소유한다.
게임의 강화, 태그, 내구도, 수리, 고객 사건, 저장 데이터, 장비 외형 규칙은
변경하지 않는다. 현재 통합 게임 의미는 계속
`docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`가 소유한다.

```text
PRODUCT_TITLE_KO = 모루의 서약
PRODUCT_TITLE_LATIN = ANVIL OATH
PRODUCT_TITLE_DISPLAY_ORDER = KOREAN_PRIMARY_WITH_LATIN_LOCKUP
CURRENT_TITLE_STATUS = USER_APPROVED_CURRENT
PUBLIC_BRAND_LEGAL_CLEARANCE = NOT_RUN
TITLE_TEXT_RUNTIME_STATUS = IMPLEMENTED_MACHINE_AND_RUNTIME_VERIFIED
LOGO_CANDIDATE_STATUS = USER_LOCKED_AO_LOGO_02
CANDIDATE_RUNTIME_PROMOTION = IMPLEMENTED_MACHINE_VERIFIED
LOGO_RUNTIME_ASSET = assets/ui/identity/anvil_oath_logo_ao02_v1.png
LOGO_RUNTIME_SLOT = MenuLayout/MenuTitleLogo
LOGO_SOURCE_SHA256 = 320BE3FC5530392E313E20B0A34375971A7A600754BF259B18DB2DA084E1F475
LOGO_SOURCE_DIMENSIONS = LANDSCAPE_TRANSPARENT_1672x941
LOGO_TEXT_FALLBACK = MenuTitleLabel_VISIBLE_ONLY_WHEN_LOGO_TEXTURE_IS_UNAVAILABLE
LOGO_RUNTIME_VISUAL_STATUS = LIMITED_RUNTIME_VERIFIED
LOGO_RUNTIME_VISUAL_EVIDENCE = HERA_EXACT_WORKTREE_720x1280_UI_TREE_SCREENSHOT_AND_ERROR_LOG_20260831
POSTMERGE_MAIN_SHA = 16e33b87b5c4880207466443b03beb3705ab8c57
PROTECTED_APPROVAL_STATUS = RETIRED_ON_POSTMERGE_BASELINE_CLOSURE
POSTMERGE_MAINTENANCE_RESEARCH = BENCHMARK_NOT_APPLICABLE_METADATA_ONLY
```

`대장간`은 장소·직업·행동을 뜻하는 일반 게임 언어로 남는다. 따라서
`대장간으로 돌아가기`, `새 대장간 시작`처럼 **제품명이 아닌** 화면 행동과
서사 문구에는 제목을 기계적으로 치환하지 않는다. 반대로 제품의 메인 제목,
사람용 GDD의 표제, 이후의 스토어·로고 표기는 위의 두 이름을 단일 원본으로
사용한다.

## 플레이어 약속

`모루의 서약`은 강화 수치만을 뜻하지 않는다. 플레이어는 하나의 작품을 만들고,
더 밀어붙일지 멈출지 판단하며, 정밀강화로 태그를 남기고, 손상과 수리를
감수한 뒤, 그 작품이 고객과 세계에 남기는 결과를 읽는다. 제목의 **서약**은
플레이어가 작품의 생애를 끝까지 책임지는 선택을, **모루**는 모든 다섯 장비
유형의 제작 기반을 뜻한다.

```text
PRESERVES_PRIMARY_CORE = ENHANCEMENT_TENSION_PLUS_DDD
PRESERVES_PLAYER_QUESTION = STOP_OR_PUSH
PRESERVES_PRECISION_TARGETS = [10,20,30,40,50,60,70,80,90,100]
PRESERVES_TAG_ACTION = ADD_OR_UPGRADE_ONE_TAG_ON_PRECISION_SUCCESS
PRESERVES_EQUIPMENT_TYPES = [SWORD, SHIELD, BOW, ARMOR, HELMET]
```

## 조사와 적대 검토

| 판정 | 근거 | 적용 또는 배제 |
| --- | --- | --- |
| `ADOPT` | [Moonlighter](https://moonlighterthegame.com/)의 짧은 고유명 중심 타이틀 | 장르·직업을 그대로 말하지 않고, 공방과 선택의 분위기를 담는 두 단어 제목을 채택한다. |
| `ADAPT` | [Shop Titans](https://playshoptitans.com/en/)의 짧은 모바일 표기 | 세로 모바일에서도 읽히는 `ANVIL OATH` 두 단어와 한국어 우선 표기를 사용한다. 이 게임의 상점·영웅 구조는 채택하지 않는다. |
| `ADAPT` | [Potion Permit](https://store.steampowered.com/app/1337760/Potion_Permit/)의 세계 내 역할·관습형 명명 | `서약`을 세계의 제작 관습과 플레이어의 책임으로 읽히게 하되, 치료사·허가증 설정은 가져오지 않는다. |
| `REJECT` | [Blacksmith: Ignite the Forge](https://store.steampowered.com/app/2651220/Blacksmith%3A_Ignite_the_Forge/)와 [Fantasy Blacksmith](https://store.steampowered.com/app/959520/Fantasy_Blacksmith/) | `Blacksmith`, `Fantasy`, `Forge` 중심의 일반명사 제목과 불꽃 부제는 시장 구분력이 낮고 이미 사용 중이므로 본제로 쓰지 않는다. |
| `RISK_RETAIN` | Fantasy Flight Games의 [Oath and Anvil](https://www.fantasyflightgames.com/en/ffg_blog/22241/original_content) | 단어 순서가 반대인 기존 판타지 카드게임 확장판이 있다. 정확한 독립 게임명 충돌은 이 1차 검색에서 확인되지 않았으나, 출시·스토어 공개 전 상표 및 국가별 스토어명 검토가 필요하다. |

`PUBLIC_BRAND_LEGAL_CLEARANCE = NOT_RUN`은 법적 위험이 없다는 뜻이 아니다. 이
결정은 현재 프로젝트 내부의 제품명·UI 표기 승인이고, 출시 가능성·등록
가능성·국가별 상표 충돌을 PASS로 만들지 않는다.

## 병합 후 운영 정리

제목 적용 PR #345는 `76b82967aacbef85484f9b0206d8194e09a9c9e3`으로 `main`에
병합됐다. 이 후속 정리는 그 정확한 병합 SHA를 보호 기준선으로 올리고, 해당
PR에만 유효했던 `PROJECT_PROTECTED_CHANGE_APPROVAL.json`을 폐기한다. 제품 규칙,
씬, 자산, 저장 구조, 경제 및 로고 후보 상태는 바꾸지 않는다. 이는 제품 설계나
시장·기술 선택이 없는 사후 운영 메타데이터 작업이므로 외부 벤치마크는
`BENCHMARK_NOT_APPLICABLE_METADATA_ONLY`다.

### AO-LOGO-02 승격의 병합 후 정리

`AO-LOGO-02` 실제 메뉴 로고 승격 PR #347은
`16e33b87b5c4880207466443b03beb3705ab8c57`으로 `main`에 병합됐다. 이 별도
운영 정리는 그 정확한 병합 SHA를 보호 기준선으로 채택하고, PR #347에만
유효했던 `PROJECT_PROTECTED_CHANGE_APPROVAL.json`을 폐기한다. 제품 이미지,
메뉴 구현, 저장 구조, 강화 규칙, 장비 자산 및 프로젝트 설정은 바꾸지 않는다.

## AO-LOGO-02 정식 승격

사용자는 2026-08-31 KST에 `AO-LOGO-02`를 실제 제품 로고로 확정했다. 이 승격은
사용자가 고른 후보 하나를 메인 메뉴의 **실제** 소비처에 연결하는 범위로 한정한다.
원본은 투명 PNG `1672×941`이며, 이전 `1600×640` 목표 비율과 다르므로 정본은
추정값을 유지하지 않고 실제 검증된 원본 규격을 기록한다. 런타임은
`VSMainMenu._ensure_product_logo()`가 `MenuLayout/MenuTitleLogo`를 만들어 비율을
보존해 표시한다. 이미 로컬화된 `MenuTitleLabel`은 로고 텍스처를 읽을 수 없을 때만
보이는 대체 표기로 남는다.

```text
SELECTED_LOGO_CANDIDATE = AO-LOGO-02
UNSELECTED_LOGO_CANDIDATES = [AO-LOGO-01, AO-LOGO-03]
ACTUAL_GAME_CONSUMER = MAIN_MENU_PRODUCT_TITLE_LOCKUP
RUNTIME_IMPLEMENTATION = DYNAMIC_TEXTURE_RECT_WITHOUT_TSCN_SERIALIZATION_MUTATION
TEXT_FALLBACK_POLICY = RETAIN_AND_SHOW_ONLY_IF_LOGO_TEXTURE_UNAVAILABLE
LEGAL_TRADEMARK_RELEASE_STATUS = NOT_RUN_NO_CLEARANCE_CLAIM
```

### 기존 해결책 우선 판정

| 항목 | 확인 결과 | 판정 |
| --- | --- | --- |
| 현재 UI 소비 경로 | `VSMainMenu`은 이미 `MenuIllustratedBackground`를 동적으로 바인딩하며, `MenuLayout`은 세로 `VBoxContainer`다. | `REUSE` |
| 엔진 기능 | [Godot 4.7 TextureRect](https://docs.godotengine.org/en/4.7/classes/class_texturerect.html)는 비율 보존·중앙 정렬 표시를 제공하고, [VBoxContainer](https://docs.godotengine.org/en/4.7/classes/class_vboxcontainer.html)는 자식의 최소 크기를 세로로 배치한다. | `REUSE` |
| 새 addon·플러그인 | 로고 한 장의 런타임 소비에 필요한 기능이 이미 있으므로 새 dependency·계정·비용·권한은 없다. | `REJECT_INSTALLATION` |

따라서 `TextureRect.EXPAND_IGNORE_SIZE`와 고정 180px 최소 높이,
`STRETCH_KEEP_ASPECT_CENTERED`를 사용했다. `VBoxContainer`의 실험적 자동 비율
최소 크기 모드는 피했다. 반대 측 검토에서 후보 원본의 `1672×941` 비율이 초기
`1600×640` 목표와 다름을 발견했고, 목표 값을 억지로 맞추지 않고 실제 원본 규격과
720×1280 runtime 관찰을 정본에 남겼다.

## 적용 경계

### 이번 제품명 통합에 포함

1. `scenes/vertical_slice/main_menu.tscn`의 `MenuTitleLabel` 제품 제목을
   `모루의 서약`으로 교체한다.
2. 사람용 GDD의 표제와 프로젝트의 현재 제품명 표기를 갱신하고, 생성 PDF를
   다시 만들어 정본 Markdown과 일치시킨다.
3. 제품명 표기 계약을 자동 검사한다. 검사는 제품 제목과 일반 장소·행동 문구를
   구분해야 하며, 저장 키·resource path·script class·기존 데이터 식별자를
   변경해서는 안 된다.
4. 사용자 잠금 뒤 `AO-LOGO-02`를 메인 메뉴의 `MenuTitleLogo` 소비처에 등록하고,
   로고 텍스처를 불러올 수 없을 때의 현지화 텍스트 대체 표기를 유지한다.

### 이번 범위에서 제외

- `project.godot`, 저장 키, UID, scene node 이름, resource path, script class,
  `BLACKSMITH_*` 기술 식별자, GitHub 저장소 이름 변경
- 강화 확률, 태그, 내구도, 수리, 경제, 고객 사건, 장비 외형 또는 장비 데이터 변경
- 제목 후보를 임의의 생성 이미지로 자동 대체하거나, 사용자 잠금 전 후보를
  runtime asset으로 승격하는 행위
- 스토어 등록, 상표 출원, 법률 자문 또는 출시 가능성 PASS 선언

## 로고 Visual Requirement

```text
consumer_id = MAIN_MENU_PRODUCT_TITLE_LOCKUP
consumer_surface = MAIN_MENU
runtime_asset_role = MenuTitleLogo TextureRect
primary_use = MAIN_MENU_PRODUCT_IDENTITY
implementation_owner_or_path = scripts/vertical_slice/ui/vs_main_menu.gd:_ensure_product_logo
target_aspect_resolution = USER_LOCKED_SOURCE_LANDSCAPE_TRANSPARENT_1672x941
state_family_requirement = DEFAULT_ONLY
fallback_if_unconsumed = RETAIN_LOCALIZED_MENUTITLELABEL_TEXT_FALLBACK
generation_status = USER_LOCKED_AO_LOGO_02
final_direction_lock = USER_CONFIRMED_2026-08-31_KST
```

아래 세 방향 후보 중 `AO-LOGO-02`만 사용자 잠금으로 정식 승격 대상이 됐다.
`AO-LOGO-01`과 `AO-LOGO-03`은 정본·runtime으로 승격하지 않은 후보로 남는다.

| 후보 | 방향 | 유지할 것 | 금지할 것 |
| --- | --- | --- | --- |
| `AO-LOGO-01` | 정통 판타지 | 얇은 원형 각인선, 손그림 공방 노트의 종이·철 질감, 우아한 세리프 | 참조 이미지의 깃털·원형 배치·정확한 글자 조합 복제, 검정·금색 다크 포지 스타일 |
| `AO-LOGO-02` | 균형형 | 읽기 쉬운 `ANVIL OATH`, 작은 모루 각인, 따뜻한 철·가죽·목재 물성 | 과도한 무기 실루엣, 다섯 장비 중 하나만 대표하는 구성 |
| `AO-LOGO-03` | 모바일 가독성형 | 큰 글자, 작은 화면에서도 읽히는 자간, 절제된 한 개의 표식 | 복잡한 테두리, 작은 장식문, UI 스크린샷처럼 보이는 가짜 제품 화면 |

## 검증 계약

```text
TITLE_CONTRACT_TEST = REQUIRED_BEFORE_UI_CHANGE
MENU_PRODUCT_TITLE_EXACT = 모루의 서약
GDD_PRODUCT_TITLE_EXACT = 모루의 서약
LATIN_LOCKUP_EXACT = ANVIL OATH
KEEP_GENERIC_WORKSHOP_COPY = TRUE
NO_SAVE_OR_MACHINE_IDENTIFIER_RENAME = TRUE
PDF_READBACK_AFTER_REGENERATION = REQUIRED
GODOT_PARSE_OR_GUT_TARGETED_CHECK = REQUIRED_AFTER_SCENE_CHANGE
ANDROID_ACCESSIBILITY_HUMAN_PLAY = NOT_RUN_UNLESS_OBSERVED
```

## 완료 상태

| 층위 | 상태 | 증거 |
| --- | --- | --- |
| 제목 방향 | `USER_APPROVED` | 2026-08-31 사용자 확정 |
| 정본 적용 | `SPECIFIED / MACHINE_VERIFIED` | 제목 계약, GDD/PDF readback |
| 메뉴 구현 | `IMPLEMENTED / MACHINE_VERIFIED` | 실제 Godot Editor + HiGodot로 `MenuTitleLabel` 저장 |
| 메뉴 런타임 | `LIMITED_RUNTIME_VERIFIED` | 720×1280 실행에서 제목·기존 한국어 행동·동적 배경 slot 확인; 사람 UX는 별도 |
| 로고 후보 | `AO-LOGO-01`/`03`만 `GENERATED_CANDIDATE` | 미선택 후보는 저장소·runtime 미승격 |
| 로고 최종 방향 | `USER_APPROVED / CANON_REGISTERED / IMPLEMENTED_MACHINE_VERIFIED / LIMITED_RUNTIME_VERIFIED` | 사용자 2026-08-31 `AO-LOGO-02` 확정, SHA·권리 기록·메뉴 동적 소비처·자동 계약, exact worktree 720×1280 UI tree·rendered screenshot·error log 관찰 |
| Android/접근성/사람 UX | `NOT_RUN` | 실제 기기·사람 관찰 전에는 PASS 불가 |
| 법률·상표·출시 | `NOT_RUN` | 별도 정식 검토 필요 |
