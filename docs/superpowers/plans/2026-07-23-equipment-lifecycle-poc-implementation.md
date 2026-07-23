# Blacksmith 장비 생애 PoC 구현계획

> **에이전트 실행 요구사항:** 구현 시 `superpowers:subagent-driven-development`(권장) 또는 `superpowers:executing-plans`를 사용해 작업별로 실행한다. 모든 단계는 체크박스로 추적하며, 각 작업은 독립 테스트와 커밋으로 끝난다.

**목표:** 검투사 의뢰 확인부터 철검 제작, +5 납품 또는 +10 추가 도전, 수동 날짜 진행, 지연된 경기 결과, 영구 장비 이력, 같은 고객의 재방문까지 첫 장비 생애 PoC를 완성한다.

**아키텍처:** 확정 코어 계약을 구현보다 상위에 둔다. 날짜·피로도, 완성도, 고객 평가, 세계 장비 기록, 결과 판정을 각각 독립 도메인 모델로 분리한다. `GameFlowScreen`은 화면 라우팅만 담당하고, `EquipmentLifecyclePocController`가 시스템 간 상태 전이를 조정한다.

**기술 스택:** Godot 4.7.1 stable, GDScript, JSON 데이터 계약, Python 데이터 검증, Godot headless 테스트, Android 세로 UI.

## 전역 제약

- 강화 버튼 입력 한 번당 판정 한 번을 보존한다.
- 일반 강화와 +10 특수 강화를 분리한다.
- 기존 골드·재료 거래 의미를 보존한다.
- 사전조건 실패 시 골드·재료·피로도 어느 것도 차감하지 않는다.
- 날짜는 사용자가 직접 종료하며 작업 예약·자동 날짜 진행을 추가하지 않는다.
- 남은 피로도의 50%를 소수점 버림으로 이월하며 별도 상한을 두지 않는다.
- PoC는 `iron_sword`, 검투사 카일, +0~+10, 지연 경기 결과 1건만 지원한다.
- 난수는 결과 밴드를 바꾸지 않고 같은 밴드 안의 문장·보상 강도만 바꾼다.
- 기존 `quality_*` 필드는 호환 별칭으로 유지한다.
- 직원, 직접 전투, 시장 시뮬레이션, 전쟁, 관전, 베팅, 복원, 방어구, 악세서리, 저장 마이그레이션을 추가하지 않는다.
- 모든 작업은 Red→Green→Refactor 순서와 독립 커밋을 지킨다.

---

## 파일 구조

### 신규 데이터

- `data/progression/workshop_day_balance.json`: 기본 피로도, 이월률, 행동 비용.
- `data/crafting/craftsmanship_grades.json`: 영구 완성도 5등급과 정밀 결과별 분포.
- `data/customers/gladiator_poc.json`: 첫 의뢰와 재방문 의뢰.
- `data/world/gladiator_match_poc.json`: 결정 점수, 결과 밴드, 보상.

### 신규 도메인 코드

- `scripts/progression/workshop_calendar.gd`: 날짜·피로도 상태.
- `scripts/forging/craftsmanship_grade_resolver.gd`: 주입 가능한 난수로 완성도 판정.
- `scripts/customers/customer_contract.gd`: 납품 가능 여부와 적합도.
- `scripts/world/equipment_world_registry.gd`: 영구 장비 기록과 활동 집합.
- `scripts/world/world_activity_resolver.gd`: 결과 밴드·기여·미충족 조건.
- `scripts/poc/workshop_action_service.gd`: 골드·재료·피로도 원자 거래.
- `scripts/poc/equipment_lifecycle_poc_controller.gd`: 의뢰·납품·날짜·보고·재방문 상태 기계.
- `scripts/telemetry/poc_telemetry.gd`: 메모리 이벤트 로그와 JSON 내보내기.

### 신규 UI

- `scripts/ui/workshop_hud.gd`: 날짜, 피로도, 골드, 마감, 하루 종료.
- `scripts/ui/customer_contract_screen.gd`: 첫 의뢰·재방문 의뢰.
- `scripts/ui/world_report_screen.gd`: 설명 가능한 지연 결과.
- `scenes/test/equipment_lifecycle_poc.tscn`: PoC 화면 smoke test.

### 수정 파일

- `scripts/forging/forging_session.gd`
- `scripts/ui/forging_screen.gd`
- `scripts/ui/enhancement_screen.gd`
- `scripts/ui/game_flow_screen.gd`
- `tools/validate_game_data.py`
- `.github/workflows/godot-validation.yml`
- `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

---

## Task 1. 장비 생애 데이터 계약과 검증기

**파일**

- Create: `data/progression/workshop_day_balance.json`
- Create: `data/crafting/craftsmanship_grades.json`
- Create: `data/customers/gladiator_poc.json`
- Create: `data/world/gladiator_match_poc.json`
- Modify: `tools/validate_game_data.py`
- Create: `tests/test_lifecycle_data_contract.py`

**인터페이스**

- Produces: `validate_lifecycle_poc(errors: ValidationErrors) -> None`
- Produces: 이후 모든 작업이 소비하는 JSON 4종.

- [ ] **Step 1: 실패하는 데이터 계약 테스트 작성**

```python
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_game_data", ROOT / "tools" / "validate_game_data.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_lifecycle_data_is_valid() -> None:
    errors = MODULE.ValidationErrors()
    MODULE.validate_lifecycle_poc(errors)
    assert errors.items == []


def test_grade_distribution_must_sum_to_one() -> None:
    data = MODULE.load_json(ROOT / "data" / "crafting" / "craftsmanship_grades.json")
    broken = copy.deepcopy(data)
    broken["precision_distributions"]["GOOD"]["REFINED"] = 0.99
    errors = MODULE.ValidationErrors()
    MODULE.validate_craftsmanship_grades(errors, broken)
    assert any("sum to 1" in item for item in errors.items)


def test_customer_affix_references_must_exist() -> None:
    customer = MODULE.load_json(ROOT / "data" / "customers" / "gladiator_poc.json")
    broken = copy.deepcopy(customer)
    broken["contracts"][0]["preferred_affix_ids"] = ["missing_affix"]
    affixes = MODULE.load_json(ROOT / "data" / "crafting" / "affixes.json")
    errors = MODULE.ValidationErrors()
    MODULE.validate_gladiator_contracts(errors, broken, affixes)
    assert any("unknown affix" in item for item in errors.items)
```

- [ ] **Step 2: 실패 확인**

```bash
python -m pytest tests/test_lifecycle_data_contract.py -q
```

Expected: 신규 데이터와 검증 함수가 없어 FAIL.

- [ ] **Step 3: 피로도 데이터 생성**

```json
{
  "schema_version": 1,
  "base_fatigue": 20,
  "carryover_ratio": 0.5,
  "action_costs": {
    "forge": 3,
    "normal_enhance": 1,
    "special_enhance": 3,
    "restore": 5
  }
}
```

- [ ] **Step 4: 완성도 데이터 생성**

```json
{
  "schema_version": 1,
  "grades": [
    {"id": "ROUGH", "label": "미숙한", "attack_multiplier": 0.98, "value_multiplier": 0.92, "world_score": 0},
    {"id": "STANDARD", "label": "평범한", "attack_multiplier": 1.0, "value_multiplier": 1.0, "world_score": 5},
    {"id": "REFINED", "label": "정교한", "attack_multiplier": 1.02, "value_multiplier": 1.05, "world_score": 10},
    {"id": "EXCELLENT", "label": "명품", "attack_multiplier": 1.04, "value_multiplier": 1.1, "world_score": 15},
    {"id": "MASTERPIECE", "label": "걸작", "attack_multiplier": 1.06, "value_multiplier": 1.15, "world_score": 20}
  ],
  "precision_distributions": {
    "STANDARD": {"ROUGH": 0.2, "STANDARD": 0.55, "REFINED": 0.22, "EXCELLENT": 0.03, "MASTERPIECE": 0.0},
    "GOOD": {"ROUGH": 0.05, "STANDARD": 0.4, "REFINED": 0.43, "EXCELLENT": 0.11, "MASTERPIECE": 0.01},
    "PERFECT": {"ROUGH": 0.0, "STANDARD": 0.15, "REFINED": 0.5, "EXCELLENT": 0.3, "MASTERPIECE": 0.05}
  }
}
```

- [ ] **Step 5: 검투사 의뢰 데이터 생성**

```json
{
  "schema_version": 1,
  "customer": {"id": "gladiator_kyle", "name": "검투사 카일"},
  "contracts": [
    {
      "id": "gladiator_kyle_first_sword",
      "kind": "FIRST",
      "requested_weapon_ids": ["iron_sword"],
      "required_level": 5,
      "stretch_level": 10,
      "preferred_affix_ids": ["sharp", "flaming"],
      "deadline_day_offset": 3,
      "report_delay_days": 1,
      "base_payment": 500,
      "immediate_fame": 1,
      "world_event_id": "gladiator_local_match"
    },
    {
      "id": "gladiator_kyle_follow_up",
      "kind": "FOLLOW_UP",
      "requested_weapon_ids": ["iron_sword"],
      "required_level": 5,
      "stretch_level": 10,
      "preferred_affix_ids": ["sharp", "flaming"],
      "deadline_day_offset": 4,
      "report_delay_days": 1,
      "base_payment": 650,
      "immediate_fame": 1,
      "world_event_id": "gladiator_local_match"
    }
  ]
}
```

- [ ] **Step 6: 경기 결과 데이터 생성**

```json
{
  "schema_version": 1,
  "events": [
    {
      "id": "gladiator_local_match",
      "active_record_limit": 6,
      "attack_threshold": 30,
      "contributions": {
        "required_level": 25,
        "stretch_level": 15,
        "preferred_affix": 25,
        "attack_threshold": 20
      },
      "bands": [
        {"id": "DEFEAT", "min_score": 0, "fame": 1, "relationship": 0, "gold_multiplier": 0.8},
        {"id": "WIN", "min_score": 40, "fame": 3, "relationship": 1, "gold_multiplier": 1.0},
        {"id": "DECISIVE_WIN", "min_score": 70, "fame": 6, "relationship": 2, "gold_multiplier": 1.15}
      ]
    }
  ]
}
```

- [ ] **Step 7: 검증기 구현**

`tools/validate_game_data.py`에 다음 책임을 추가한다.

```python
def validate_lifecycle_poc(errors: ValidationErrors) -> None:
    day = load_json(DATA_ROOT / "progression" / "workshop_day_balance.json")
    grades = load_json(DATA_ROOT / "crafting" / "craftsmanship_grades.json")
    customers = load_json(DATA_ROOT / "customers" / "gladiator_poc.json")
    world = load_json(DATA_ROOT / "world" / "gladiator_match_poc.json")
    affixes = load_json(DATA_ROOT / "crafting" / "affixes.json")
    validate_workshop_day_balance(errors, day)
    validate_craftsmanship_grades(errors, grades)
    validate_gladiator_contracts(errors, customers, affixes)
    validate_gladiator_world_event(errors, world, grades)
```

세부 검증은 다음을 강제한다.

- `base_fatigue`와 행동 비용은 양의 정수.
- `0 <= carryover_ratio < 1`.
- 등급 ID 중복 금지, 배율은 양수, 세계 점수는 0 이상.
- 정밀 결과별 분포 키가 등급 ID와 일치하고 합계가 `1.0 ± 1e-6`.
- 고객 무기·수식어·세계 이벤트 참조가 존재.
- 결과 밴드는 `min_score` 오름차순, 첫 밴드는 0.

- [ ] **Step 8: Green 확인**

```bash
python tools/validate_game_data.py
python -m pytest tests/test_lifecycle_data_contract.py -q
```

Expected: validator exit 0, pytest 3 passed.

- [ ] **Step 9: 커밋**

```bash
git add data/progression/workshop_day_balance.json data/crafting/craftsmanship_grades.json data/customers/gladiator_poc.json data/world/gladiator_match_poc.json tools/validate_game_data.py tests/test_lifecycle_data_contract.py
git commit -m "feat: add equipment lifecycle poc data contracts"
```

---

## Task 2. 날짜·피로도 모델

**파일**

- Create: `scripts/progression/workshop_calendar.gd`
- Create: `tests/unit/test_workshop_calendar.gd`

**인터페이스**

```gdscript
class_name WorkshopCalendar
func preview_spend(action_id: String) -> Dictionary
func try_spend(action_id: String) -> Dictionary
func refund(amount: int) -> void
func end_day() -> Dictionary
func snapshot() -> Dictionary
```

- [ ] **Step 1: 실패 테스트 작성**

```gdscript
extends SceneTree

const CalendarScript = preload("res://scripts/progression/workshop_calendar.gd")
var failures: Array[String] = []

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var calendar = CalendarScript.new({
        "base_fatigue": 20,
        "carryover_ratio": 0.5,
        "action_costs": {"forge": 3, "normal_enhance": 1, "special_enhance": 3}
    })
    _expect(calendar.try_spend("forge")["ok"], "제작 피로도를 소비해야 합니다.")
    _expect(calendar.remaining_fatigue == 17, "제작 뒤 피로도는 17이어야 합니다.")
    var day_result: Dictionary = calendar.end_day()
    _expect(day_result["carryover"] == 8, "17의 50% 버림은 8이어야 합니다.")
    _expect(calendar.day == 2, "날짜가 2일 차로 진행되어야 합니다.")
    _expect(calendar.remaining_fatigue == 28, "다음 날 피로도는 28이어야 합니다.")
    calendar.remaining_fatigue = 0
    var rejected: Dictionary = calendar.try_spend("normal_enhance")
    _expect(not rejected["ok"] and rejected["status"] == "NO_FATIGUE", "부족 시 차단해야 합니다.")
    if failures.is_empty():
        print("WorkshopCalendar tests PASSED (5 cases)")
        quit(0)
        return
    for item in failures:
        push_error(item)
    quit(1)

func _expect(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
```

- [ ] **Step 2: Red 확인**

```bash
./godot --headless --path . --script res://tests/unit/test_workshop_calendar.gd
```

Expected: 스크립트가 없어 FAIL.

- [ ] **Step 3: 최소 구현**

```gdscript
class_name WorkshopCalendar
extends RefCounted

signal changed(snapshot: Dictionary)

var day: int = 1
var base_fatigue: int = 20
var carryover_ratio: float = 0.5
var action_costs: Dictionary = {}
var remaining_fatigue: int = 20

func _init(config: Dictionary = {}) -> void:
    base_fatigue = maxi(int(config.get("base_fatigue", 20)), 1)
    carryover_ratio = clampf(float(config.get("carryover_ratio", 0.5)), 0.0, 0.999999)
    action_costs = config.get("action_costs", {}).duplicate(true)
    remaining_fatigue = base_fatigue

func preview_spend(action_id: String) -> Dictionary:
    var cost := maxi(int(action_costs.get(action_id, 0)), 0)
    if cost <= 0:
        return {"ok": false, "status": "INVALID_ACTION", "cost": cost}
    if remaining_fatigue < cost:
        return {"ok": false, "status": "NO_FATIGUE", "cost": cost, "missing": cost - remaining_fatigue}
    return {"ok": true, "status": "READY", "cost": cost}

func try_spend(action_id: String) -> Dictionary:
    var preview := preview_spend(action_id)
    if not bool(preview.get("ok", false)):
        return preview
    remaining_fatigue -= int(preview["cost"])
    changed.emit(snapshot())
    return preview

func refund(amount: int) -> void:
    remaining_fatigue += maxi(amount, 0)
    changed.emit(snapshot())

func end_day() -> Dictionary:
    var unused := remaining_fatigue
    var carryover := int(floor(float(unused) * carryover_ratio))
    day += 1
    remaining_fatigue = base_fatigue + carryover
    var result := {"day": day, "unused_fatigue": unused, "carryover": carryover, "remaining_fatigue": remaining_fatigue}
    changed.emit(snapshot())
    return result

func snapshot() -> Dictionary:
    return {"day": day, "base_fatigue": base_fatigue, "remaining_fatigue": remaining_fatigue, "carryover_ratio": carryover_ratio}
```

- [ ] **Step 4: Green 확인·커밋**

```bash
./godot --headless --path . --script res://tests/unit/test_workshop_calendar.gd
git add scripts/progression/workshop_calendar.gd tests/unit/test_workshop_calendar.gd
git commit -m "feat: add workshop day and fatigue model"
```

Expected: `WorkshopCalendar tests PASSED (5 cases)`.

---

## Task 3. 정밀 결과와 영구 완성도 분리

**파일**

- Create: `scripts/forging/craftsmanship_grade_resolver.gd`
- Modify: `scripts/forging/forging_session.gd`
- Modify: `scripts/ui/forging_screen.gd`
- Modify: `tests/unit/test_forging_session.gd`
- Modify: `tests/integration/test_forging_quality_enhancement.gd`

**인터페이스**

```gdscript
class_name CraftsmanshipGradeResolver
func resolve(precision_result_id: String, roll: float) -> Dictionary
```

- [ ] **Step 1: 판정기·호환 필드 실패 테스트 추가**

테스트는 다음을 고정한다.

- `GOOD`, roll `0.06` → `STANDARD`.
- `GOOD`, roll `0.50` → `REFINED`.
- 결과에 `precision_result_id`와 `craftsmanship_grade_id`가 동시에 존재.
- `quality_id`는 `craftsmanship_grade_id`와 같고 기존 강화 화면이 읽을 수 있음.

- [ ] **Step 2: 판정기 구현**

```gdscript
class_name CraftsmanshipGradeResolver
extends RefCounted

var grades_by_id: Dictionary = {}
var distributions: Dictionary = {}

func _init(data: Dictionary) -> void:
    for grade_value in data.get("grades", []):
        var grade: Dictionary = grade_value
        grades_by_id[str(grade.get("id", ""))] = grade.duplicate(true)
    distributions = data.get("precision_distributions", {}).duplicate(true)

func resolve(precision_result_id: String, roll: float) -> Dictionary:
    var distribution: Dictionary = distributions.get(precision_result_id, distributions.get("STANDARD", {}))
    var cursor := 0.0
    var clamped_roll := clampf(roll, 0.0, 0.999999)
    for grade_id in ["ROUGH", "STANDARD", "REFINED", "EXCELLENT", "MASTERPIECE"]:
        cursor += float(distribution.get(grade_id, 0.0))
        if clamped_roll < cursor:
            return grades_by_id.get(grade_id, {}).duplicate(true)
    return grades_by_id.get("MASTERPIECE", {}).duplicate(true)
```

- [ ] **Step 3: `ForgingSession` 결과 계약 변경**

`finish_precision()`은 정밀 결과를 계산한 뒤 판정기로 완성도를 선택한다. `_complete()` 결과에 다음 필드를 추가한다.

```gdscript
"precision_result_id": precision_id,
"precision_result_label": precision_label,
"craftsmanship_grade_id": grade_id,
"craftsmanship_grade_label": grade_label,
"craftsmanship_attack_multiplier": grade_attack_multiplier,
"craftsmanship_value_multiplier": grade_value_multiplier,
"quality_id": grade_id,
"quality_label": grade_label,
"quality_attack_multiplier": grade_attack_multiplier,
"quality_value_multiplier": grade_value_multiplier,
```

`quality_*`는 별도 계산이 아니라 완성도 필드의 호환 별칭이어야 한다.

- [ ] **Step 4: UI 문구 분리**

`forging_screen.gd`의 결과 패널은 다음 두 줄을 별도로 표시한다.

```text
마감 정타: 좋은 정타
영구 완성도: 정교한
```

- [ ] **Step 5: 회귀 실행·커밋**

```bash
./godot --headless --path . --script res://tests/unit/test_forging_session.gd
./godot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd
git add scripts/forging/craftsmanship_grade_resolver.gd scripts/forging/forging_session.gd scripts/ui/forging_screen.gd tests/unit/test_forging_session.gd tests/integration/test_forging_quality_enhancement.gd
git commit -m "feat: separate precision result and craftsmanship grade"
```

Expected: 기존 강화·보관 전달 회귀와 새 용어 계약 모두 PASS.

---

## Task 4. 고객 의뢰와 납품 적합도

**파일**

- Create: `scripts/customers/customer_contract.gd`
- Create: `tests/unit/test_customer_contract.gd`

**인터페이스**

```gdscript
class_name CustomerContract
func can_deliver(equipment: Dictionary, current_day: int) -> Dictionary
func evaluate_fit(equipment: Dictionary) -> Dictionary
func remaining_days(current_day: int) -> int
```

- [ ] **Step 1: 실패 테스트 작성**

필수 사례:

1. 철검 +4 → `LEVEL_TOO_LOW`.
2. 철검 +5, 기한 이내 → 납품 가능.
3. +10, `sharp` 보유 → stretch·preferred contribution 포함.
4. 기한 초과 → `DEADLINE_EXPIRED`.
5. 다른 무기 ID → `WEAPON_NOT_REQUESTED`.

- [ ] **Step 2: 구현**

```gdscript
class_name CustomerContract
extends RefCounted

var data: Dictionary = {}
var accepted_day: int = 1
var deadline_day: int = 1

func _init(contract_data: Dictionary, start_day: int) -> void:
    data = contract_data.duplicate(true)
    accepted_day = start_day
    deadline_day = start_day + int(data.get("deadline_day_offset", 0))

func remaining_days(current_day: int) -> int:
    return deadline_day - current_day

func can_deliver(equipment: Dictionary, current_day: int) -> Dictionary:
    var missing: Array[Dictionary] = []
    if current_day > deadline_day:
        missing.append({"id": "DEADLINE_EXPIRED", "label": "의뢰 기한 초과"})
    if str(equipment.get("weapon_id", "")) not in data.get("requested_weapon_ids", []):
        missing.append({"id": "WEAPON_NOT_REQUESTED", "label": "요청하지 않은 장비"})
    if int(equipment.get("enhancement_level", 0)) < int(data.get("required_level", 0)):
        missing.append({"id": "LEVEL_TOO_LOW", "label": "요구 강화 미달"})
    if bool(equipment.get("destroyed", false)):
        missing.append({"id": "DESTROYED", "label": "파괴된 장비"})
    return {"ok": missing.is_empty(), "missing_conditions": missing, "deadline_day": deadline_day}
```

`evaluate_fit()`은 required, stretch, preferred affix, grade, attack를 개별 기여 항목으로 반환한다.

- [ ] **Step 3: 테스트·커밋**

```bash
./godot --headless --path . --script res://tests/unit/test_customer_contract.gd
git add scripts/customers/customer_contract.gd tests/unit/test_customer_contract.gd
git commit -m "feat: add gladiator delivery contract"
```

---

## Task 5. 세계 장비 기록과 결정적 결과 판정

**파일**

- Create: `scripts/world/equipment_world_registry.gd`
- Create: `scripts/world/world_activity_resolver.gd`
- Create: `tests/unit/test_equipment_world_registry.gd`
- Create: `tests/unit/test_world_activity_resolver.gd`

**인터페이스**

```gdscript
class_name EquipmentWorldRegistry
func deliver(equipment: Dictionary, owner: Dictionary, delivered_day: int, report_day: int) -> Dictionary
func due_records(current_day: int) -> Array[Dictionary]
func apply_result(world_record_id: String, result: Dictionary, day: int) -> bool
func mark_report_opened(world_record_id: String, day: int) -> bool

class_name WorldActivityResolver
func resolve(equipment: Dictionary, contract: Dictionary, event_data: Dictionary, detail_roll: float = 0.5) -> Dictionary
```

- [ ] **Step 1: 실패 테스트 작성**

결과 판정 사례:

- +5, 정교한, 공격 기준 충족, 선호 수식어 없음 → 55점 `WIN`.
- +10, 선호 수식어, 명품, 공격 기준 충족 → 75점 이상 `DECISIVE_WIN`.
- detail roll 0.1과 0.9는 `outcome_band`가 같아야 함.
- 세계 기록은 납품·경기·보고 열람 이력을 순서대로 보존.
- 활동 장비 7번째 등록 시 가장 오래된 비대표 기록만 `ARCHIVED`.

- [ ] **Step 2: 결과 판정 구현**

```gdscript
class_name WorldActivityResolver
extends RefCounted

func resolve(equipment: Dictionary, contract: Dictionary, event_data: Dictionary, detail_roll: float = 0.5) -> Dictionary:
    var score := 0
    var contributions: Array[Dictionary] = []
    var missing: Array[Dictionary] = []
    var level := int(equipment.get("enhancement_level", 0))
    _score_condition(level >= int(contract.get("required_level", 5)), "REQUIRED_LEVEL", "+5 요구 조건 충족", int(event_data["contributions"]["required_level"]), contributions, missing, score)
    score = _sum_scores(contributions)
    if level >= int(contract.get("stretch_level", 10)):
        contributions.append({"id": "STRETCH_LEVEL", "label": "+10 추가 목표 충족", "score": int(event_data["contributions"]["stretch_level"])})
    else:
        missing.append({"id": "STRETCH_LEVEL", "label": "+10 추가 강화 미도달"})
    if _has_preferred_affix(equipment, contract.get("preferred_affix_ids", [])):
        contributions.append({"id": "PREFERRED_AFFIX", "label": "선호 수식어 보유", "score": int(event_data["contributions"]["preferred_affix"])})
    else:
        missing.append({"id": "PREFERRED_AFFIX", "label": "선호 수식어 없음"})
    contributions.append({"id": "GRADE", "label": str(equipment.get("craftsmanship_grade_label", "평범한")), "score": int(equipment.get("craftsmanship_world_score", 5))})
    if int(equipment.get("final_attack", 0)) >= int(event_data.get("attack_threshold", 30)):
        contributions.append({"id": "ATTACK", "label": "기준 공격력 충족", "score": int(event_data["contributions"]["attack_threshold"])})
    else:
        missing.append({"id": "ATTACK", "label": "기준 공격력 미달"})
    score = _sum_scores(contributions)
    var band := _select_band(score, event_data.get("bands", []))
    return {
        "outcome_band": str(band.get("id", "DEFEAT")),
        "score": score,
        "contributions": contributions,
        "missing_conditions": missing,
        "fame_reward": int(band.get("fame", 0)),
        "relationship_delta": int(band.get("relationship", 0)),
        "detail_roll": clampf(detail_roll, 0.0, 0.999999)
    }
```

보조 함수는 점수 합계, 선호 수식어 탐색, 밴드 선택만 담당하며 난수로 밴드를 변경하지 않는다.

- [ ] **Step 3: Registry 구현**

상태 전이는 다음으로 제한한다.

```text
ACTIVE → RESULT_READY → REPORT_OPENED → ARCHIVED
ACTIVE → ARCHIVED
```

각 기록은 `equipment_record`, `owner_id`, `status`, `delivered_day`, `next_event_day`, `history`, `result`를 소유한다.

- [ ] **Step 4: 테스트·커밋**

```bash
./godot --headless --path . --script res://tests/unit/test_world_activity_resolver.gd
./godot --headless --path . --script res://tests/unit/test_equipment_world_registry.gd
git add scripts/world/equipment_world_registry.gd scripts/world/world_activity_resolver.gd tests/unit/test_equipment_world_registry.gd tests/unit/test_world_activity_resolver.gd
git commit -m "feat: add persistent equipment world results"
```

---

## Task 6. 원자 거래와 생애 컨트롤러

**파일**

- Create: `scripts/poc/workshop_action_service.gd`
- Create: `scripts/poc/equipment_lifecycle_poc_controller.gd`
- Create: `tests/integration/test_workshop_action_atomicity.gd`
- Create: `tests/integration/test_equipment_lifecycle_controller.gd`

**인터페이스**

```gdscript
class_name WorkshopActionService
func try_begin_enhancement(session, resources, calendar, action_id: String, roll_override: float = -1.0, leap_roll_override: float = -1.0) -> Dictionary

class_name EquipmentLifecyclePocController
func deliver(equipment: Dictionary) -> Dictionary
func end_day() -> Dictionary
func open_report(world_record_id: String) -> Dictionary
func snapshot() -> Dictionary
```

- [ ] **Step 1: 원자성 실패 테스트**

다음을 각각 검증한다.

- 피로도 부족: 골드·재료·피로도 불변.
- 골드 부족: 피로도·재료 불변.
- 재료 부족: 골드·피로도 불변.
- `session.begin_attempt()` 실패: 선차감 자원 전부 환불.
- 성공 시작: 기존 WorkshopResources 거래와 피로도 모두 한 번만 차감.

- [ ] **Step 2: Action Service 구현**

```gdscript
class_name WorkshopActionService
extends RefCounted

func try_begin_enhancement(session, resources, calendar, action_id: String, roll_override: float = -1.0, leap_roll_override: float = -1.0) -> Dictionary:
    var fatigue_preview: Dictionary = calendar.preview_spend(action_id)
    if not bool(fatigue_preview.get("ok", false)):
        return fatigue_preview
    var resource_preview: Dictionary = resources.preview_attempt(session)
    if not bool(resource_preview.get("ok", false)):
        return resource_preview
    var fatigue_result: Dictionary = calendar.try_spend(action_id)
    if not bool(fatigue_result.get("ok", false)):
        return fatigue_result
    var transaction: Dictionary = resources.try_begin_attempt(session, roll_override, leap_roll_override)
    if not bool(transaction.get("ok", false)):
        calendar.refund(int(fatigue_result.get("cost", 0)))
        return transaction
    transaction["fatigue_cost"] = int(fatigue_result.get("cost", 0))
    transaction["fatigue_after"] = calendar.remaining_fatigue
    return transaction
```

특수 강화의 빈 보조재료 fallback은 수동 PoC에서 허용하지 않는다.

- [ ] **Step 3: 컨트롤러 구현**

컨트롤러 상태:

```gdscript
enum State { CONTRACT, WORKSHOP, REPORT_READY, FOLLOW_UP }
```

`deliver()`는 적합도 확인 → 기본 대금·즉시 명성 → 세계 기록 생성 순서로 실행한다. 실패 시 어떤 상태도 변경하지 않는다. `end_day()`는 Calendar를 진행하고 due record를 결과 판정한 뒤 `REPORT_READY`로 전환한다. `open_report()`는 세계 명성·관계를 적용하고 재방문을 해금한다.

- [ ] **Step 4: 테스트·커밋**

```bash
./godot --headless --path . --script res://tests/integration/test_workshop_action_atomicity.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_controller.gd
git add scripts/poc/workshop_action_service.gd scripts/poc/equipment_lifecycle_poc_controller.gd tests/integration/test_workshop_action_atomicity.gd tests/integration/test_equipment_lifecycle_controller.gd
git commit -m "feat: coordinate atomic lifecycle actions"
```

---

## Task 7. PoC 행동 로그

**파일**

- Create: `scripts/telemetry/poc_telemetry.gd`
- Create: `tests/unit/test_poc_telemetry.gd`

**인터페이스**

```gdscript
class_name PocTelemetry
func record(event_name: String, payload: Dictionary) -> void
func events_named(event_name: String) -> Array[Dictionary]
func export_json() -> String
func clear() -> void
```

- [ ] **Step 1: 실패 테스트 작성**

필수 이벤트 이름과 필드가 누락되면 테스트가 실패해야 한다. 이벤트 순서와 deep copy를 검증한다.

- [ ] **Step 2: 구현**

```gdscript
class_name PocTelemetry
extends RefCounted

var events: Array[Dictionary] = []
var sequence: int = 0

func record(event_name: String, payload: Dictionary) -> void:
    sequence += 1
    events.append({"sequence": sequence, "event": event_name, "payload": payload.duplicate(true)})

func events_named(event_name: String) -> Array[Dictionary]:
    var matches: Array[Dictionary] = []
    for entry in events:
        if str(entry.get("event", "")) == event_name:
            matches.append(entry.duplicate(true))
    return matches

func export_json() -> String:
    return JSON.stringify(events, "  ")

func clear() -> void:
    events.clear()
    sequence = 0
```

- [ ] **Step 3: 테스트·커밋**

```bash
./godot --headless --path . --script res://tests/unit/test_poc_telemetry.gd
git add scripts/telemetry/poc_telemetry.gd tests/unit/test_poc_telemetry.gd
git commit -m "feat: add lifecycle poc telemetry"
```

---

## Task 8. 세로 UI와 기존 흐름 통합

**파일**

- Create: `scripts/ui/workshop_hud.gd`
- Create: `scripts/ui/customer_contract_screen.gd`
- Create: `scripts/ui/world_report_screen.gd`
- Create: `scenes/test/equipment_lifecycle_poc.tscn`
- Modify: `scripts/ui/enhancement_screen.gd`
- Modify: `scripts/ui/game_flow_screen.gd`
- Modify: `scenes/main/main.tscn`

**인터페이스**

- `WorkshopHud`: `day_end_requested` signal, `refresh(snapshot)`.
- `CustomerContractScreen`: `contract_accepted`, `workshop_requested` signals.
- `WorldReportScreen`: `report_acknowledged(world_record_id)` signal.

- [ ] **Step 1: 계약 화면 구현**

기본 화면에 고객명, 요청 무기, +5 필수, +10 선택 목표, 선호 수식어, 마감일, 대금만 표시한다. 주 행동 버튼은 `의뢰 수락` 하나다.

- [ ] **Step 2: HUD 구현**

HUD는 날짜, `남은 피로도 / 기본 피로도`, 골드, 남은 기한, `하루 마치기`를 표시한다. 색상 외에 텍스트로 부족 상태를 병기한다.

- [ ] **Step 3: 결과 보고 화면 구현**

보고 화면은 다음 순서로 표시한다.

1. 결과 밴드.
2. 효과가 있었던 선택.
3. 부족했던 조건.
4. 장비 이력 추가 내용.
5. 명성·관계 변화.
6. `보고서 확인` 버튼.

자동 닫힘을 사용하지 않는다.

- [ ] **Step 4: EnhancementScreen을 Action Service로 전환**

```gdscript
var action_id := "special_enhance" if session.uses_materials_for_level(session.enhancement_level + 1) else "normal_enhance"
var transaction: Dictionary = workshop_action_service.try_begin_enhancement(
    session,
    workshop_resources,
    workshop_calendar,
    action_id
)
```

`NO_FATIGUE`이면 부족량을 표시하고 현재 시도 버튼을 비활성화한다. 날짜는 자동 진행하지 않는다.

- [ ] **Step 5: GameFlowScreen 얇게 분리**

초기 화면은 `_show_contract()`로 변경한다. 다음 객체를 로드·생성한다.

```gdscript
calendar = WorkshopCalendarScript.new(day_balance)
world_registry = EquipmentWorldRegistryScript.new(int(match_event.get("active_record_limit", 6)))
contract = CustomerContractScript.new(first_contract_data, calendar.day)
telemetry = PocTelemetryScript.new()
controller = EquipmentLifecyclePocControllerScript.new(
    calendar,
    workshop_resources,
    contract,
    customer_data,
    world_registry,
    WorldActivityResolverScript.new(),
    match_event
)
action_service = WorkshopActionServiceScript.new()
```

화면 전환 외의 날짜·결과·재방문 판정은 컨트롤러에 위임한다.

- [ ] **Step 6: 보관함 납품 버튼**

적합 장비에 `검투사에게 납품` 버튼을 추가한다. `controller.deliver()`가 성공했을 때만 보관함에서 제거하고 `poc_equipment_delivered`를 기록한다.

- [ ] **Step 7: Smoke 테스트**

```bash
./godot --headless --editor --path . --quit
./godot --headless --path . res://scenes/main/main.tscn --quit-after 2
./godot --headless --path . res://scenes/test/equipment_lifecycle_poc.tscn --quit-after 2
```

Expected: 모두 exit 0, `SCRIPT ERROR`, `Parse Error`, `Compile Error`, `ERROR:` 없음.

- [ ] **Step 8: 커밋**

```bash
git add scripts/ui/workshop_hud.gd scripts/ui/customer_contract_screen.gd scripts/ui/world_report_screen.gd scripts/ui/enhancement_screen.gd scripts/ui/game_flow_screen.gd scenes/test/equipment_lifecycle_poc.tscn scenes/main/main.tscn
git commit -m "feat: add equipment lifecycle poc screens"
```

---

## Task 9. 전체 생애 통합 테스트·CI·정본 동기화

**파일**

- Create: `tests/integration/test_equipment_lifecycle_poc.gd`
- Modify: `.github/workflows/godot-validation.yml`
- Modify: `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

- [ ] **Step 1: 결정적 E2E 테스트 작성**

```text
첫 의뢰 수락
→ REFINED 철검 생성
→ 제작 피로도 소비
→ +1~+5 성공 고정
→ +5에서 보관·납품
→ 하루 종료
→ WIN 판정
→ 보고서 열기
→ 영구 장비 이력 확인
→ 재방문 해금 확인
```

필수 assertion:

- 제작 3, 일반 강화당 1의 피로도 차감.
- 납품 대금 500과 즉시 명성 1.
- 하루 종료 후 50% 이월.
- 결과 밴드 `WIN`.
- 기여와 미충족 조건 배열 존재.
- 보고서 열람 후 세계 명성·관계 적용.
- 납품·경기 이력이 세계 기록에 유지.
- 재방문 의뢰 해금.

- [ ] **Step 2: E2E Red/Green 실행**

```bash
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_poc.gd
```

Expected: `Equipment lifecycle PoC integration tests PASSED`, exit 0.

- [ ] **Step 3: CI에 신규 테스트 등록**

`.github/workflows/godot-validation.yml`에 다음 명령과 각각의 PASS marker·process status 검사를 추가한다.

```bash
./godot --headless --path . --script res://tests/unit/test_workshop_calendar.gd
./godot --headless --path . --script res://tests/unit/test_customer_contract.gd
./godot --headless --path . --script res://tests/unit/test_world_activity_resolver.gd
./godot --headless --path . --script res://tests/unit/test_equipment_world_registry.gd
./godot --headless --path . --script res://tests/unit/test_poc_telemetry.gd
./godot --headless --path . --script res://tests/integration/test_workshop_action_atomicity.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_controller.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_poc.gd
```

- [ ] **Step 4: 전체 로컬 검증**

```bash
python tests/check_no_merge_conflicts.py
python tools/validate_game_data.py
python -m pytest tests/test_lifecycle_data_contract.py -q
./godot --headless --editor --path . --quit
./godot --headless --path . res://scenes/test/enhancement_test.tscn --quit-after 2
./godot --headless --path . res://scenes/test/equipment_lifecycle_poc.tscn --quit-after 2
./godot --headless --path . res://scenes/main/main.tscn --quit-after 2
./godot --headless --path . --script res://tests/unit/test_forging_session.gd
./godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
./godot --headless --path . --script res://tests/unit/test_workshop_resources.gd
./godot --headless --path . --script res://tests/unit/test_workshop_calendar.gd
./godot --headless --path . --script res://tests/unit/test_customer_contract.gd
./godot --headless --path . --script res://tests/unit/test_world_activity_resolver.gd
./godot --headless --path . --script res://tests/unit/test_equipment_world_registry.gd
./godot --headless --path . --script res://tests/unit/test_poc_telemetry.gd
./godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd
./godot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd
./godot --headless --path . --script res://tests/integration/test_workshop_action_atomicity.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_controller.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_poc.gd
```

Expected: 모든 명령 exit 0. 하나라도 실패하면 구현 완료를 선언하지 않는다.

- [ ] **Step 5: 정본 동기화**

- Game Bible에는 실제 구현된 동작만 기록한다.
- Active Context에는 정확한 테스트 수와 Workflow run ID를 기록한다.
- Development Gates에는 증거가 있는 게이트만 PASS로 변경한다.
- Android 실기기, 접근성, 시각 검수, 성능, 외부 플레이테스트는 증거 전까지 `NOT_RUN`.
- 통합 명세와 구현계획을 Design Document Registry에 등록한다.

- [ ] **Step 6: 사람 검증 게이트**

1. 720×1280 세로 UI와 좁은 Android viewport 검수.
2. 터치 영역·스크롤·색상 외 정보 전달 검수.
3. 개발자 설명 없는 내부 콜드 스타트 1회.
4. 외부 플레이어 5명 세션.

수집 행동 지표:

- +5에서 멈춘 비율과 +10을 선택한 이유.
- 결과 보고 자발적 열람.
- 결과 원인 2개 이상 회상.
- 낮은 완성도 즉시 폐기율.
- 날짜만 넘긴 비율.
- 재방문 후 새 제작 시작 여부.

- [ ] **Step 7: 커밋**

```bash
git add tests/integration/test_equipment_lifecycle_poc.gd .github/workflows/godot-validation.yml "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md" "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md" "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md" "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
git commit -m "test: verify complete equipment lifecycle poc"
```

---

## 계획 자체 검토

### 명세 커버리지

- 코어 정체성과 뾰족한 재미: Tasks 3, 4, 5, 8, 9.
- 영구 완성도: Task 3.
- +5 납품 대 +10 추가 도전: Tasks 4, 5, 8, 9.
- 피로도와 50% 이월: Tasks 1, 2, 6, 8, 9.
- 자원 원자성: Task 6.
- 지연 결과와 세계 이력: Tasks 5, 6, 8, 9.
- 설명 가능한 인과성: Task 5와 Task 8 보고 UI.
- 재방문 고객: Tasks 6, 8, 9.
- 텔레메트리와 반증 가능한 플레이테스트: Tasks 7, 9.
- 기존 회귀와 CI: Task 9.

### 명칭 일관성

- `WorkshopCalendar`: `preview_spend`, `try_spend`, `refund`, `end_day`.
- `CustomerContract`: `can_deliver`, `evaluate_fit`.
- `EquipmentWorldRegistry`: `deliver`, `due_records`, `apply_result`, `mark_report_opened`.
- `WorldActivityResolver`: `resolve`.
- `WorkshopActionService`: `try_begin_enhancement`.
- `EquipmentLifecyclePocController`: `deliver`, `end_day`, `open_report`.
- 결과 필드: `outcome_band`, `contributions`, `missing_conditions`.

### 범위 검토

각 Task는 독립 테스트와 커밋을 갖는다. 두 번째 고객, 두 번째 사건, +11 이상, 저장 마이그레이션, 자동 단조 정책 변경은 이 계획 밖이다.

## 실행 순서

1. 전체 PR 스택 `#31 → #32 → #33`을 병합하거나 해당 head에서 격리 worktree를 만든다.
2. Tasks 1~9를 순서대로 실행한다.
3. 각 Task의 diff와 테스트 증거를 검토한 뒤 다음 Task로 진행한다.
4. 전체 검증 명령이 통과한 뒤에만 구현 PR을 연다.
5. 세로 UI와 내부 콜드 스타트 검토 전까지 구현 PR을 Draft로 유지한다.
