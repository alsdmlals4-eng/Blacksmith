# BS-ART-20260826-04 · Actual Game Image Consumer Gate

- Date: `2026-08-26 KST`
- User approval: `우린 '설명용 시트'가 아니라 실제 게임 소비처가 있는 이미지 기준으로 만든다.`
- Status: `USER_APPROVED_PROJECT_VISUAL_DELIVERY_CANON`
- Parent art direction: `BS-ART-20260825-03 / ILLUSTRATED_WORKSHOP_BOOK`
- Base policy adaptation: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Work Mode: `PLAN`
- Image generation in this Decision: `NOT_RUN`

## 1. Core rule

Blacksmith의 신규 이미지 제작 기준은 **설명 자료가 아니라 실제 게임 소비처**다.

```text
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
NEW_EXPLANATORY_GDD_SHEET_IMAGE_TARGET = FALSE
NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE
PRIMARY_USE_GATE_REQUIRED = TRUE
NO_CONSUMER = CUT_OR_DEFER
```

기존 Notion Mermaid/표/텍스트 설명은 기획 커뮤니케이션에 계속 사용할 수 있다. 그러나 이를 다시 한 장짜리 생성 이미지로 만들어 "Visual GDD" 수량을 늘리는 작업은 신규 이미지 제작 목표가 아니다.

## 2. What counts as an actual game consumer

이미지 자체가 실제 제품의 특정 slot에서 소비될 수 있어야 한다.

예시 category:

```text
SCREEN_BACKGROUND
EVENT_ILLUSTRATION
ITEM_PORTRAIT_OR_ICON
CUSTOMER_PORTRAIT_OR_EVENT_VIGNETTE
UI_ORNAMENT_OR_FRAME
STATE_VARIANT_ASSET
FULL_FRAME_STATIC_ART_IF_RUNTIME_CONSUMES_IT_AS_FULL_FRAME
```

반대로 아래는 실제 게임 소비처가 아니다.

```text
standalone explanation board
text-heavy GDD sheet rendered as image
fake gameplay screenshot created only to explain layout
comparison sheet whose only consumer is Notion review
concept collage with no mapped product slot
```

## 3. Generated UI mockup boundary

```text
GENERATED_UI_SCREENSHOT_MOCKUP_AS_PRODUCT_ASSET = FALSE
UI_LAYOUT_PROTOTYPE_IS_NOT_GENERATED_RASTER_ASSET = TRUE
```

UI 구조·정보 위계·상호작용 배치는 Notion Flow, structured screen spec, Figma/Godot 등 **편집 가능한 구조 표현**에서 설계한다. 생성형 이미지로 만든 가짜 screenshot은 layout discussion reference일 수는 있어도 제품 asset으로 승격하지 않는다.

화면 전체를 이미지로 생성하는 것은 예외적으로 다음 조건에서만 허용한다.

```text
FULL_FRAME_IMAGE_ALLOWED_ONLY_IF_RUNTIME_CONSUMES_FULL_FRAME = TRUE
```

예: 메인 메뉴가 실제로 한 장의 full-screen background illustration을 소비하도록 설계된 경우 그 background 자체는 eligible하다. 반대로 버튼·수치·텍스트까지 합성한 screenshot은 실제 UI consumer asset이 아니다.

## 4. Required consumer metadata

새 이미지 brief가 생성 Gate에 들어가기 전에 최소 다음 필드를 가진다.

```text
consumer_id
consumer_surface
runtime_asset_role
primary_use
implementation_owner_or_path
target_aspect_resolution
state_family_requirement
fallback_if_unconsumed
```

의미:

- `consumer_id`: 어떤 실제 UI/flow/runtime slot이 쓰는가.
- `consumer_surface`: Main Menu / Enhancement / Repair / Customer Result / Chronicle 등 실제 화면·상태 owner.
- `runtime_asset_role`: background / portrait / icon / event illustration / ornament / state asset 등.
- `primary_use`: 이 이미지가 플레이 중 무엇을 전달하는가.
- `implementation_owner_or_path`: 현재 계획된 screen owner 또는 향후 `res://` 승격 target. runtime blocked 단계에서는 owner locator만 있어도 되며 거짓 구현 경로를 만들지 않는다.
- `target_aspect_resolution`: 실제 소비처 요구에 맞춘 비율/해상도 계약.
- `state_family_requirement`: normal/damaged/selected/disabled처럼 실제 consumer가 상태군을 요구하는지 여부.
- `fallback_if_unconsumed`: 소비처가 사라지면 `CUT / DEFER / REBRIEF`; 설명 자료로 자동 전용하지 않는다.

## 5. Primary Use Gate

Base의 `Primary Use Gate`를 Blacksmith에서 필수화한다.

```text
PRIMARY_USE_GATE_REQUIRED = TRUE
candidate image
-> exact consumer exists
-> requirement / aspect / crop / alpha / state family checked
-> image conversation approval gate
-> exactly approved generation scope
-> review
-> primary-use success before reuse harvest
```

재사용 가능성을 이유로 consumer 없는 이미지를 먼저 만들지 않는다.

## 6. Existing Visual GDD 8

```text
EXISTING_VISUAL_GDD_8 = HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY
```

기존 8장은 다음 용도로만 보존한다.

- 과거 정보구조 비교
- 설명 위계 reference
- 이전 승인/검수 provenance

다음으로 자동 승격하지 않는다.

```text
PRODUCT_RUNTIME_ASSET
FINAL_GAME_SCREEN
NEW_IMAGE_BATCH_TEMPLATE
ART_STYLE_CANON_SOURCE
```

기존 이미지 안의 old CURRENT/MAX 값, 구형 precision cadence, 날짜형 Chronicle 등 stale system semantics도 계속 runtime/current canon이 아니다.

## 7. Current candidate consumer pass

현재 시스템 정리 후 이미지 제작을 바로 시작하지 않는다. 먼저 **실제 소비처 requirement pass**를 한다.

```text
ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS
```

이미 current planning에서 존재하는 화면군은 소비처 후보 locator일 뿐 자동 생성 목록이 아니다.

```text
MAIN_MENU
ENHANCEMENT_MAIN
PRECISION_+9_TO_+10
DURABILITY_REPAIR
CUSTOMER_WORLD_RESULT
ITEM_CHRONICLE
```

각 후보마다 실제 이미지가 필요한지 Delete Test를 통과해야 한다. UI/vector/structured layout으로 충분하면 생성 이미지를 만들지 않는다.

```text
AUTOMATIC_GENERATION_FROM_CANDIDATE_CONSUMER_LIST = FALSE
```

## 8. Notion visual responsibility

Notion은 사람용 현재 그림을 소유하지만, 이것이 설명용 raster sheet 생산을 요구하지 않는다.

```text
NOTION_EXPLANATORY_DIAGRAM_MAY_USE_STRUCTURED_FLOW_NOT_GENERATED_SHEET = TRUE
```

Home/Flow/Core에서 Mermaid, 표, 텍스트를 사용해 시스템을 설명할 수 있다. 실제 게임 이미지가 존재하고 승인되면 Visual Bible/Asset record는 **그 이미지의 실제 consumer와 usage**를 표시한다.

## 9. Image conversation gate remains mandatory

이 Decision은 future requirement 기준을 승인한 것이지 이미지 생성 명령이 아니다.

```text
IMAGE_GENERATION_REQUIRES_SEPARATE_CONVERSATION_APPROVAL_GATE = TRUE
NO_AUTOMATIC_IMAGE_CHAIN = TRUE
```

따라서 consumer requirement가 확정되어도 사용자가 해당 이미지 brief를 승인하기 전 자동 생성하지 않는다.

## 10. Relation to current art direction

`BS-ART-20260825-03`의 그림체 선택은 유지한다.

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
```

Decision04는 **무엇을 이미지로 만들 것인가 / 어디서 실제 소비될 것인가**를 좁히는 delivery Gate이며, Art03의 스타일 방향을 대체하지 않는다.

## 11. Base policy disposition

Base current image policy already requires:

```text
current Project canon / stage / consumer
Visual Requirement Gate
Primary Use Gate
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
```

Blacksmith project override:

- `ADOPT`: consumer-first requirement, Primary Use Gate, state-family/engine-consumption metadata.
- `ADAPT`: Blacksmith 신규 생성 이미지는 실제 game consumer가 필수.
- `REJECT`: 설명용 sheet 숫자를 늘리기 위한 image generation.
- `REJECT`: fake screenshot을 그대로 product asset으로 취급.
- `DIFFERENTIATOR`: 생성 이미지도 특정 작품/고객/event/공방 화면에서 실제 플레이 의미를 가져야 한다.

## 12. Adversarial review contract

### Loop 1 — 설명이 필요하면 이미지로 만들어야 하나?
No. 시스템 설명은 structured text/flow/table로 충분할 수 있다.

### Loop 2 — UI screenshot mockup은 소비처인가?
No. screenshot 자체를 runtime이 쓰지 않는다면 product asset consumer가 아니다.

### Loop 3 — full-screen art는 금지인가?
No. runtime이 실제 full-frame background/static art로 소비하면 eligible하다.

### Loop 4 — 기존 Visual GDD 8은 삭제하나?
No. history/reference로 보존한다. 신규 generation target만 바뀐다.

### Loop 5 — screen 이름이 있으면 자동 생성하나?
No. consumer candidate -> Visual Requirement/Delete Test -> 별도 image conversation approval 순서다.

### Loop 6 — consumer가 사라진 이미지는 Notion 설명 자료로 자동 전용하나?
No. `CUT / DEFER / REBRIEF`가 기본이다.

## 13. Evidence ceiling

```text
VISUAL_DELIVERY_POLICY = USER_APPROVED / BS-ART-20260826-04
IMAGE_GENERATION = NOT_RUN
ACTUAL_RUNTIME_CONSUMPTION = NOT_RUN
PROJECT_ASSET_APPROVAL = NOT_GRANTED_BY_THIS_DECISION
ART_DIRECTION = BS-ART-20260825-03 / USER_APPROVED_DIRECTION
```
