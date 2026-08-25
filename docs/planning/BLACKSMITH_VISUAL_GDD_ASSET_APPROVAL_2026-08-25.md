# Blacksmith Visual GDD Asset Approval · 2026-08-25

- Status: `USER_APPROVED_VISUAL_GDD`
- User directive: `좋아 승인`
- Work mode: `PLAN`
- Baseline main: `256f7ca04ccb258cbd308c7b85250a60c690cdbb`
- Base main fresh-read: `3c3376845b9a1b7921a4260aa6259cd61533ffc4`
- `STYLIZED_DARK_FORGE = CURRENT`
- `APPROVED_REPRESENTATIVE_VISUAL = AVAILABLE`
- `FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED`
- `RUNTIME_VALIDATION = NOT_RUN`
- `PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## Approval meaning

사용자가 2026-08-25 생성된 6개 Blacksmith 설명형 Visual GDD를 승인했다. 이 승인은 **사람용 Living GDD / Visual Bible / 설계 판단용 대표 시각자료**로서의 승인이다. Godot에 바로 투입되는 final runtime asset, 최종 UI texture, release asset, 접근성/device 검증 완료를 의미하지 않는다.

## Approved Visual GDD manifest

| Visual ID | Name | Generation ID | SHA-256 | Durable copy |
| --- | --- | --- | --- | --- |
| `BS-VIS-20260820-01` | 강화 메인 화면 Visual GDD | `f18d7a58-21b4-469c-b16e-2cbeaa22530b` | `2619843ad82c640e7038acd8a0687752f46326464444f0f24e062464e6cd7066` | Google Drive `16AcZRLJnl-Hexk0m1iLAWkufYGrysrZj` |
| `BS-VIS-20260820-02` | 강화 DDD 피드백 단계표 | `0f76cb2f-b5c0-45bf-b891-f814e5d14e16` | `606579edbc51f5a9454e4cf0f694e5f1ef4a40544488fda46512b46ed26175ce` | Google Drive `1eBmQG1uPGQcrrC7VlG_m2Kcj3RbxPvDm` |
| `BS-VIS-20260820-05` | 첫 10분 DDD Storyboard | `7fa82021-aee3-49ad-84a5-01cbfb836202` | `3329e8b6c341b7482bf59afa00f652dcd930f138d78cbb2dfc04b56b67c4e84e` | Google Drive `1r0Xjfj-6iGA1yMfx4RQSUOMBLIYLkzbV` |
| `BS-VIS-20260820-06` | CURRENT/MAX 이중 내구도 Visual GDD | `e25e6e23-c370-46b0-b9d1-013f90794c93` | `378496097011ebfbcfe80d3611309825fed119f5bd5bbee272d149923aa6bb3f` | Google Drive `1w7Xam0CGO-KFUxsYXJnL75tbEXH7AUTm` |
| `BS-VIS-20260820-09` | 수리 판단 카드 Visual GDD | `66aed12c-f13c-41df-b6f5-027067898713` | `b683ae966b4ca4853c9efae7a49aeab1e9e769127f3ca540db276e2e2efda915` | Google Drive `11WVoZmI2If5zrRC0ydxsaDKro9tPR1qT` |
| `BS-VIS-20260824-10` | 정밀강화 → 고객 Context Visual GDD | `5c8090ff-898d-4a9f-80d9-4b36b3938fb6` | `c1831b39b7d48646bbd07224a301f6cbc6ede4f9da02c3e4cf6e5985f6067aa9` | Google Drive `17-UoaZsxSGPnLbJAhLHSqcfS6M-J941a` |

모든 6개 행의 승인 상태는 `USER_APPROVED_VISUAL_GDD`다.

## Shared guards

- 예시 이미지/외부 레퍼런스의 권리나 자산 자체를 승계하지 않는다.
- 생성물은 `STYLIZED_DARK_FORGE` 방향을 설명하는 internal project Visual GDD로 사용한다.
- 생성 이미지 안의 세부 수치·문구는 current canon과 충돌할 경우 **시각 예시**가 우선권을 갖지 않는다. 실제 수치 정본은 current Canon/structured data가 우선한다.
- 이미지 속 예시 성공률·가격·단계값을 새 balance canon으로 자동 승격하지 않는다.
- 실제 UI 구현 시 Human readability, Android portrait, accessibility, device/runtime 검증을 별도로 수행한다.
- `BS-VIS-20260820-03`, `04`, `07`, `08` 및 기타 미승인 Visual brief는 자동 승인되지 않는다.

## Storage and destination contract

- GitHub: 이 manifest가 생성물 identity/hash/approval 범위의 structured canon이다.
- Google Drive: 6개 PNG의 durable binary copy를 보관한다.
- Notion Asset Library: 동일 6개 Visual ID를 `Approved=true / Status=APPROVED / Decision=ADOPT`의 **Visual GDD reference asset**으로 등록한다.
- Notion Human Home: 승인 Visual 보유 상태와 Visual Bible/Asset Library를 사람이 볼 수 있게 반영한다.
- Google Sheet: 기존 동일 Visual ID의 승인/검수 행을 최종 승인 상태로 갱신한다.

## Evidence ceiling

`USER_APPROVED_VISUAL_GDD`는 사용자의 시각자료 승인 증거다. 다음은 여전히 별도 검증이다.

- final product asset / Godot import
- runtime screen match
- Android device readability
- accessibility
- performance
- release asset rights ledger
- Human playtest
