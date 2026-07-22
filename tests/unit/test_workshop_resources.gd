extends SceneTree

const EnhancementSessionScript = preload("res://scripts/enhancement/enhancement_session.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")

var failures: Array[String] = []
var base_config: Dictionary
var materials: Array
var affixes: Array
var milestones: Array


func _initialize() -> void:
	base_config = _read_json("res://data/crafting/enhancement_balance.json")
	materials = _read_json("res://data/crafting/materials.json").get("materials", [])
	affixes = _read_json("res://data/crafting/affixes.json").get("affixes", [])
	milestones = _read_json("res://data/crafting/enhancement_milestones.json").get("milestones", [])
	_run_tests()
	if failures.is_empty():
		print("WorkshopResources tests PASSED (6 cases)")
		quit(0)
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_normal_attempt_consumes_gold_only()
	_test_insufficient_gold_blocks_attempt()
	_test_special_attempt_consumes_selected_stock()
	_test_missing_material_blocks_without_spending()
	_test_empty_special_slots_are_allowed_for_auto_fallback()
	_test_invalid_state_does_not_charge_twice()


func _new_session(success: float = 1.0):
	var config := base_config.duplicate(true)
	config["milestones"] = milestones.duplicate(true)
	var rates := {}
	for level in range(1, 101):
		rates[str(level)] = success
	config["base_success_by_target_level"] = rates
	return EnhancementSessionScript.new(
		config,
		materials,
		affixes,
		{"weapon_id": "iron_sword", "weapon_name": "철검", "base_attack": 10}
	)


func _test_normal_attempt_consumes_gold_only() -> void:
	var session = _new_session()
	var resources = WorkshopResourcesScript.new(1000, {"whetstone": 2})
	var cost := int(session.calculate_attempt_cost())
	var transaction: Dictionary = resources.try_begin_attempt(session, 0.0)
	_expect(bool(transaction.get("ok", false)), "일반 강화는 자원이 충분하면 시작되어야 합니다.")
	_expect(resources.gold == 1000 - cost, "일반 강화 비용이 실제 보유 골드에서 차감되어야 합니다.")
	_expect(resources.get_material_count("whetstone") == 2, "일반 강화는 보조재료를 소비하면 안 됩니다.")
	_expect(session.enhancement_level == 1, "결제된 일반 강화가 실제 세션에 적용되어야 합니다.")


func _test_insufficient_gold_blocks_attempt() -> void:
	var session = _new_session()
	var resources = WorkshopResourcesScript.new(0, {})
	var transaction: Dictionary = resources.try_begin_attempt(session, 0.0)
	_expect(str(transaction.get("status", "")) == WorkshopResourcesScript.STATUS_NO_GOLD, "골드 부족 상태를 반환해야 합니다.")
	_expect(resources.gold == 0, "골드 부족 시 보유 골드가 변하면 안 됩니다.")
	_expect(session.total_attempts == 0 and session.enhancement_level == 0, "골드 부족 시 강화 판정을 시작하면 안 됩니다.")


func _test_special_attempt_consumes_selected_stock() -> void:
	var session = _new_session()
	for _level in range(9):
		session.begin_attempt(0.0)
	var resources = WorkshopResourcesScript.new(100000, {
		"whetstone": 1,
		"salamander_core": 1,
	})
	_expect(session.set_secondary_material("whetstone"), "+10에서 숫돌을 선택할 수 있어야 합니다.")
	_expect(session.set_catalyst_material("salamander_core"), "+10에서 촉매를 선택할 수 있어야 합니다.")
	var before_gold: int = int(resources.gold)
	var cost := int(session.calculate_attempt_cost())
	var transaction: Dictionary = resources.try_begin_attempt(session, 0.0)
	_expect(bool(transaction.get("ok", false)), "특수 강화는 골드와 재료가 충분하면 시작되어야 합니다.")
	_expect(resources.gold == before_gold - cost, "특수 강화 총 비용이 실제 골드에서 차감되어야 합니다.")
	_expect(resources.get_material_count("whetstone") == 0, "선택한 보조재료를 1개 소비해야 합니다.")
	_expect(resources.get_material_count("salamander_core") == 0, "선택한 촉매를 1개 소비해야 합니다.")
	_expect(session.state == EnhancementSessionScript.State.PRECISION, "결제 후 특수 강화 정밀 판정으로 진입해야 합니다.")


func _test_missing_material_blocks_without_spending() -> void:
	var session = _new_session()
	for _level in range(9):
		session.begin_attempt(0.0)
	var resources = WorkshopResourcesScript.new(100000, {"whetstone": 0})
	session.set_secondary_material("whetstone")
	var before_gold: int = int(resources.gold)
	var before_attempts: int = int(session.total_attempts)
	var transaction: Dictionary = resources.try_begin_attempt(session, 0.0)
	_expect(str(transaction.get("status", "")) == WorkshopResourcesScript.STATUS_NO_MATERIAL, "선택 재료가 없으면 재료 부족 상태를 반환해야 합니다.")
	_expect(str(transaction.get("material_id", "")) == "whetstone", "부족한 재료 ID를 반환해야 합니다.")
	_expect(resources.gold == before_gold, "재료 부족 시 골드를 차감하면 안 됩니다.")
	_expect(session.total_attempts == before_attempts, "재료 부족 시 강화 판정을 시작하면 안 됩니다.")


func _test_empty_special_slots_are_allowed_for_auto_fallback() -> void:
	var session = _new_session()
	for _level in range(9):
		session.begin_attempt(0.0)
	var resources = WorkshopResourcesScript.new(100000, {})
	_expect(session.set_secondary_material(""), "자동 fallback은 보조재료 슬롯을 비울 수 있어야 합니다.")
	_expect(session.set_catalyst_material(""), "자동 fallback은 촉매 슬롯을 비울 수 있어야 합니다.")
	var transaction: Dictionary = resources.try_begin_attempt(session, 0.0)
	_expect(bool(transaction.get("ok", false)), "자동 fallback의 무재료 특수 강화를 허용해야 합니다.")
	_expect(str(transaction.get("secondary_material_id", "missing")) == "", "무재료 특수 강화 기록은 빈 보조재료 ID여야 합니다.")


func _test_invalid_state_does_not_charge_twice() -> void:
	var session = _new_session()
	for _level in range(9):
		session.begin_attempt(0.0)
	var resources = WorkshopResourcesScript.new(100000, {"whetstone": 2})
	session.set_secondary_material("whetstone")
	var first: Dictionary = resources.try_begin_attempt(session, 0.0)
	_expect(bool(first.get("ok", false)), "첫 특수 강화 시도는 시작되어야 합니다.")
	var after_first_gold: int = int(resources.gold)
	var after_first_stock: int = resources.get_material_count("whetstone")
	var second: Dictionary = resources.try_begin_attempt(session, 0.0)
	_expect(str(second.get("status", "")) == WorkshopResourcesScript.STATUS_INVALID_STATE, "정밀 판정 중 중복 시작을 차단해야 합니다.")
	_expect(resources.gold == after_first_gold, "중복 시작 차단 시 골드를 추가 차감하면 안 됩니다.")
	_expect(resources.get_material_count("whetstone") == after_first_stock, "중복 시작 차단 시 재료를 추가 소비하면 안 됩니다.")


func _read_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		failures.append("%s 파일을 읽지 못했습니다." % path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
