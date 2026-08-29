# BS-ENHANCE-20260830-38 · 반복 정밀강화 태그 진화

- 상태: `USER_APPROVED_CURRENT`
- 현재 field owner: 정밀 cadence, 태그 collection cardinality/stage, V3→V4 migration disposition, tag-growth effect timing.
- 기계 catalog: `docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json` schema 2.

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

현재 첫 catalog는 `EDGE_REINFORCEMENT=RAW_ROLE_STAT +3`, `LIGHTWEIGHTING=WEIGHT_POINT -3 (floor 0)`, `DURABILITY_DELTA=0`만 허용한다. stage는 선택한 method의 적용 횟수이며 효과를 재계산하거나 배가하지 않는다.

| V3 입력 | V4 결과 |
| --- | --- |
| 빈 문자열 | 빈 tag collection |
| 알려진 단일 tag + level >=10 | SEED I, created milestone 10, used milestone 10; 기존 효과 재적용 금지 |
| `PRECISION_KEYWORD_PENDING_CONTENT` | initial-tag pending; 정정 전 후속 Precision 차단 |
| unknown nonempty | fail-closed unreadable state; 덮어쓰기/효과/재개 금지 |

## 조사·적대 검토·증거 ceiling

`ADOPT`: 지속 제작 상태를 명시적으로 보여 주는 제작 게임의 누적 선택. `ADAPT`: Android two-step large native control. `REJECT`: forging-potential 자원, random affix reroll, 10회 무한 누적. 적대 검토는 fourth affix, 확률/내구도/repair 변경, default selection, duplicate effect, V3 double-apply를 차단한다.

자동 계약은 catalog/owner 정합성 증거일 뿐 Godot runtime, Android, accessibility, performance, simulation, human playtest는 `NOT_RUN`이다.
