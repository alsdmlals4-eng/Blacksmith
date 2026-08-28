# Blacksmith Visual GDD Asset Approval · 2026-08-25

- Status: `USER_APPROVED_VISUAL_GDD / HISTORICAL_INFORMATION_REFERENCE`
- User directive at creation: `승인 / 이후 그림체 재설계 필요`
- Work mode: `PLAN`
- Baseline main: `827ac4147cc58dba22a39b4a3f7babd8079cddff`
- Base main fresh-read at creation: `210ec78292fa12ed7563ba743b322dd36103ae4a`
- Historical art-direction Decision: `BS-ART-20260825-02`
- Current style owner: `BS-ART-20260825-03 / ILLUSTRATED_WORKSHOP_BOOK`
- Current image-delivery owner: `BS-ART-20260826-04 / ACTUAL_GAME_IMAGE_CONSUMER_GATE`
- Current status: `ART_STYLE_STATUS = HISTORICAL_REWORK_BRIDGE`
- Historical approval-time guard: `ART_STYLE_STATUS = REWORK_REQUIRED`
- Historical approval-time evidence: `APPROVED_REPRESENTATIVE_VISUAL = AVAILABLE / HISTORICAL_REFERENCE_ONLY`
- `STYLIZED_DARK_FORGE = LEGACY_VISUAL_REFERENCE_NOT_FINAL_STYLE_CANON`
- `APPROVED_VISUAL_SCOPE = INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD / HISTORICAL_ONLY`
- `EXISTING_VISUAL_GDD_8 = HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY`
- `FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED`
- `RUNTIME_VALIDATION = NOT_RUN`
- `PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- `GITHUB_MIGRATION_RECEIPT = docs/migration/BLACKSMITH_NOTION_TO_GITHUB_MIGRATION_20260828.md`
- `NOTION_SOURCE_STATUS = RETIRED_AFTER_ONE_TIME_READ_ONLY_MIGRATION`

## Current Decision04 override

The user has now clarified that Blacksmith image production is **not measured by explanatory sheets**. New images must have an actual game consumer.

```text
BS-ART-20260826-04
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
NEW_EXPLANATORY_GDD_SHEET_IMAGE_TARGET = FALSE
GENERATED_UI_SCREENSHOT_MOCKUP_AS_PRODUCT_ASSET = FALSE
FULL_FRAME_IMAGE_ALLOWED_ONLY_IF_RUNTIME_CONSUMES_FULL_FRAME = TRUE
PRIMARY_USE_GATE_REQUIRED = TRUE
NO_CONSUMER = CUT_OR_DEFER
```

Therefore this manifest is retained for identity/hash/provenance of the old eight Visual GDDs, but those images are **not templates or quota targets for future generation**.

## Approval meaning at the time

사용자가 2026-08-25 생성된 Blacksmith 설명형 Visual GDD 8개를 승인했다. 이 승인은 당시 **사람용 Living GDD / Visual Bible / 설계 판단용 정보 구조·레이아웃·설명 의도**에 대한 승인이다.

이후 Art03에서 `ILLUSTRATED_WORKSHOP_BOOK` 방향이 선택됐고, Decision04에서 신규 이미지 제작 기준은 actual game consumer로 좁혀졌다.

따라서 현재 의미:

```text
8 VISUAL GDDs = HISTORICAL INFORMATION / EXPLANATION REFERENCES
CURRENT GENERATED ART STYLE = NOT FINAL PRODUCT ASSET
NEW EXPLANATORY GDD SHEET IMAGE GENERATION = NOT A CURRENT TARGET
NEW IMAGE CANDIDATE -> ACTUAL GAME CONSUMER REQUIRED
```

Godot에 바로 투입되는 final runtime asset, 최종 UI texture, release asset, 접근성/device 검증 완료를 의미하지 않는다.

## Approved Visual GDD manifest · historical provenance

| Visual ID | Name | Generation ID | SHA-256 | Durable copy |
| --- | --- | --- | --- | --- |
| `BS-VIS-20260820-01` | 강화 메인 화면 Visual GDD | `f18d7a58-21b4-469c-b16e-2cbeaa22530b` | `2619843ad82c640e7038acd8a0687752f46326464444f0f24e062464e6cd7066` | Google Drive `16AcZRLJnl-Hexk0m1iLAWkufYGrysrZj` |
| `BS-VIS-20260820-02` | 강화 DDD 피드백 단계표 | `0f76cb2f-b5c0-45bf-b891-f814e5d14e16` | `606579edbc51f5a9454e4cf0f694e5f1ef4a40544488fda46512b46ed26175ce` | Google Drive `1eBmQG1uPGQcrrC7VlG_m2Kcj3RbxPvDm` |
| `BS-VIS-20260820-04` | 강화 긴장 Band 상태 매트릭스 | `d5a862ee-0bcf-4604-930e-23ffda4a9a48` | `b675de17a0a48b5719c6bb80a4e1bf39f7a7dea99583ba2a9923d5dbb8d0b028` | Google Drive `1UUTIvitHRMjW6NVCuzJthWd3U96ZXkw_` |
| `BS-VIS-20260820-05` | 첫 10분 DDD Storyboard | `7fa82021-aee3-49ad-84a5-01cbfb836202` | `3329e8b6c341b7482bf59afa00f652dcd930f138d78cbb2dfc04b56b67c4e84e` | Google Drive `1r0Xjfj-6iGA1yMfx4RQSUOMBLIYLkzbV` |
| `BS-VIS-20260820-06` | CURRENT/MAX 이중 내구도 Visual GDD | `e25e6e23-c370-46b0-b9d1-013f90794c93` | `378496097011ebfbcfe80d3611309825fed119f5bd5bbee272d149923aa6bb3f` | Google Drive `1w7Xam0CGO-KFUxsYXJnL75tbEXH7AUTm` |
| `BS-VIS-20260820-08` | MAX 구조 손상과 강화 페널티 비교 | `20e2d949-5bca-4f9d-b289-7ad26220efe1` | `8cb10166a354f13ee0117c279870bc76bb2f226a13e56e37005952aea329bdec` | Google Drive `1qDJ2Khz1I9L0FwdH-XFZ3Zf63CP0_CDp` |
| `BS-VIS-20260820-09` | 수리 판단 카드 Visual GDD | `66aed12c-f13c-41df-b6f5-027067898713` | `b683ae966b4ca4853c9efae7a49aeab1e9e769127f3ca540db276e2e2efda915` | Google Drive `11WVoZmI2If5zrRC0ydxsaDKro9tPR1qT` |
| `BS-VIS-20260824-10` | 정밀강화 → 고객 Context Visual GDD | `5c8090ff-898d-4a9f-80d9-4b36b3938fb6` | `c1831b39b7d48646bbd07224a301f6cbc6ede4f9da02c3e4cf6e5985f6067aa9` | Google Drive `17-UoaZsxSGPnLbJAhLHSqcfS6M-J941a` |

모든 8개 행은 당시 `USER_APPROVED_VISUAL_GDD`였지만 현재 future-generation 의미는 `HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY`다.

## Historical Art-direction override · `BS-ART-20260825-02`

당시 사용자 피드백을 다음과 같이 구현 가능한 디자인 문제로 정규화했다.

- generic AI-generated dark-fantasy / mobile-fantasy look가 강함
- 검정+금색 장식 프레임과 발광 테두리가 지나치게 균질함
- serif 제목·아이콘·패널 ornament가 프로젝트 고유성보다 먼저 읽힘
- 한 화면의 정보량과 장식 밀도가 높아 AI pitch-board 인상이 강함
- 장비와 대장간 물성은 유효하지만, 표현 방식이 독자적인 Blacksmith 시각 정체성으로 충분히 소유되지 않음

### 보존할 것

- 장비/작품이 시각적 주인공
- 대장간의 물성·열·마모·금속 질감
- 따뜻한 국소 화로광과 깊은 주변 명암
- 모바일에서 읽히는 상태·위험·선택 위계
- 색상 외 shape/icon/text의 중복 정보 채널

### 현재 추가 보호선

- UI 구조·정보 위계·상호작용 설계가 필요하면 structured/editable surface를 사용하고 설명용 screenshot raster를 제품 asset으로 만들지 않는다.
- full-frame art는 실제 runtime이 그 full frame을 소비할 때만 eligible하다.
- consumer가 없는 candidate는 `CUT / DEFER / REBRIEF`하며 역사 자료로 자동 전용하지 않는다.
- actual consumer candidate는 consumer metadata + Visual Requirement/Delete Test를 먼저 기록한다. 이 요건 뒤 candidate 생성은 사용자 사전승인 상태이며, 최종 방향/runtime 승격만 post-generation user lock을 요구한다.

## Shared guards

- 예시 이미지/외부 레퍼런스의 권리나 자산 자체를 승계하지 않는다.
- 8개 생성물은 historical project Visual GDD information reference로 보존한다.
- 생성 이미지 안의 세부 수치·문구는 current canon과 충돌할 경우 **시각 예시**가 우선권을 갖지 않는다.
- 이미지 속 예시 성공률·가격·단계값을 새 balance canon으로 자동 승격하지 않는다.
- 기존 8개 이미지의 art style을 후속 production asset의 스타일 기준으로 자동 복제하지 않는다.
- 실제 UI 구현 시 Human readability, Android portrait, accessibility, device/runtime 검증을 별도로 수행한다.
- `BS-VIS-20260820-03`, `07` 및 기타 미승인 Visual brief는 자동 승인되지 않는다.

## Storage and destination contract

- GitHub: 이 manifest와 `docs/migration/historical_notion_gdd/`가 old generated visual identity/hash/approval history의 현재 보존처다.
- Google Drive와 Notion은 과거 출처/provenance로만 남으며, 이후 read/write 또는 destination readback 대상이 아니다.
- current Art03 style + Decision04 actual-consumer rule은 GitHub GDD와 Visual Direction Lock Packet이 소유한다.
- Google Sheet: historical compatibility-only; active visual production workspace가 아니다.

## Evidence ceiling

`USER_APPROVED_VISUAL_GDD`는 과거 설명형 시각자료 승인 증거다. `BS-ART-20260826-04`는 신규 이미지 delivery policy만 승인하며 다음은 여전히 별도 검증이다.

- actual consumer requirement selection
- image generation
- final product asset / Godot import
- runtime screen match / actual runtime consumption
- Android device readability
- accessibility
- performance
- release asset rights ledger
- Human playtest
