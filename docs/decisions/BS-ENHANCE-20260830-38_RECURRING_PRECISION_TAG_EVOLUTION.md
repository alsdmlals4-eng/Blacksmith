# BS-ENHANCE-20260830-38 · 반복 정밀강화 태그 진화

- 상태: `USER_APPROVED_CURRENT / CATALYST_RESOURCE_FIELDS_PARTIALLY_SUPERSEDED_BY_BS-ENHANCE-20260901-40`
- 현재 field owner: 정밀 cadence, 태그 collection cardinality/stage, V3→V4 migration disposition, tag-growth effect timing.
- 기계 catalog: `docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json` schema 3.

> [부분 대체됨] `lineage_id` 입력·`lineages` catalog·무재고/무소모 금지는 `BS-ENHANCE-20260901-40_CONSUMABLE_PRECISION_CATALYST_RESOURCES.md`가 소유한다. 이 Decision은 ten-target cadence, tag collection cardinality/stage, V3→V4 item migration disposition, growth effect timing을 계속 소유한다.

## 대체와 보존

| 기존 Decision | [대체됨] field | 현재 의미 |
| --- | --- | --- |
| Decision25 | `+9 -> +10` 단일 Precision, 하나의 Tag cardinality | `PRECISION_TARGETS=[10,20,30,40,50,60,70,80,90,100]`; 성공마다 태그 추가 또는 강화 하나 |
| Decision34 | `+10` 한 Tag만 기록 | 하나의 `CATALYST_AFFIX`가 최대 3 태그, I~IV stage를 소유 |
| Decision37 | target 10 only / 단일 문자열 / no new stored field | 첫 2×2 내용과 empty gate는 보존, V4 versioned record로 migration |

Decision28의 exact failure-damage curve, Decision29의 CURRENT/MAX/BASE_MAX durability authority 및 repair, Decision30의 actual-use world/customer damage policy는 변경하지 않는다. `SUCCESS_LEVEL_DELTA=+1`, `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`만 존재, `ITEM_KEYWORD_RECIPIENT=WEAPON_ITEM_ONLY`도 보존한다.

## 현재 행동 계약

`PRECISION_ENTRY = current_level == target - 1`, target은 catalog의 10개 exact 값이다. 성공은 `+1`과 아래 action 하나만 반영한다. 선택은 시도 로컬이며 hold, damage, blocked 뒤에는 저장되지 않는다.

| action | 입력 | 허용 | 성공 결과 |
| --- | --- | --- | --- |
| `ADD_TAG` | `{ "action": "ADD_TAG", "lineage_id": "EMBER_LINEAGE", "method_id": "EDGE_REINFORCEMENT" }` | 3개 미만, 새 compatible Tag | SEED I 추가, 해당 method effect 정확히 1회 |
| `UPGRADE_TAG` | `{ "action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE" }` | active tag I~III | 다음 stage, 해당 method effect 정확히 1회 |

첫 +10은 `ADD_TAG`만 가능하다. 3개 도달, duplicate Tag, IV 강화, target 외 시도, 누락/무효 선택, `LIGHTWEIGHTING`이 이미 0인 경우에는 cost/material/roll 전에 차단한다. 기본 선택, inventory/consumption, random, reroll, unrelated replacement는 금지한다.

## 효과와 migration

현재 첫 catalog는 `EDGE_REINFORCEMENT=RAW_ROLE_STAT +3`, `LIGHTWEIGHTING=WEIGHT_POINT -3 (floor 0)`, `DURABILITY_DELTA=0`만 허용한다. stage는 선택한 `tag_id`의 속성이며, 그 tag의 method effect가 해당 stage 상승 때 한 번 적용된 횟수를 읽기 좋게 나타낸다. 효과를 재계산하거나 배가하지 않는다.

| V3 입력 | V4 결과 |
| --- | --- |
| 빈 문자열 | 빈 tag collection |
| 알려진 단일 tag + level >=10 | SEED I, created milestone 10, used milestone 10; 기존 효과 재적용 금지 |
| `PRECISION_KEYWORD_PENDING_CONTENT` | initial-tag pending; 정정 전 후속 Precision 차단 |
| unknown nonempty | fail-closed unreadable state; 덮어쓰기/효과/재개 금지 |

## 조사·적대 검토·증거 ceiling

`ADOPT`: [Last Epoch 공식 Forging Potential](https://support.lastepoch.com/hc/en-us/articles/46361900702363-What-is-Forging-Potential)의 명시적 제작 상태 표현을, 별도 Forging Potential 자원 없이 tag stage/다음 target 표시에만 적용한다. `REJECT`: [Last Epoch 공식 Runes and Glyphs](https://support.lastepoch.com/hc/en-us/articles/46361877750043-Runes-and-Glyphs)의 무작위 affix 변경/reroll 성격은 채택하지 않는다. `ADAPT`: [Android 공식 natural input guidance](https://developer.android.com/games/develop/multiplatform/enable-natural-input-on-all-form-factors)의 입력 적합성 원칙을 two-step, 큰 native control에만 적용한다. 이 출처의 수치·균형 값은 import하지 않는다. `REJECT`: forging-potential 자원과 10회 무한 누적. 적대 검토는 fourth affix, 확률/내구도/repair 변경, default selection, duplicate effect, V3 double-apply를 차단한다.

자동 계약은 catalog/owner 정합성 증거일 뿐 Godot runtime, Android, accessibility, performance, simulation, human playtest는 `NOT_RUN`이다.
