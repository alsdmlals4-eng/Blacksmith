extends SceneTree

const CalendarScript = preload("res://scripts/progression/workshop_calendar.gd")
const ResourcesScript = preload("res://scripts/economy/workshop_resources.gd")
const ActionServiceScript = preload("res://scripts/poc/workshop_action_service.gd")

class FakeForgeStarter:
	extends RefCounted
	var should_start: bool = true
	func begin() -> bool:
		return should_start

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("Workshop action atomicity integration tests PASSED (4 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_no_fatigue_changes_nothing()
	_test_no_gold_changes_nothing()
	_test_no_material_changes_nothing()
	_test_start_failure_rolls_everything_back()


func _test_no_fatigue_changes_nothing() -> void:
	var calendar = CalendarScript.new()
	calendar.current_fatigue = 2
	var resources = ResourcesScript.new(100, {"iron": 1})
	var service = ActionServiceScript.new(calendar, resources)
	var before := _snapshot(calendar, resources)
	var result: Dictionary = service.try_begin_forging(10, "iron", 1, Callable(FakeForgeStarter.new(), "begin"))
	_expect(result.get("status") == CalendarScript.STATUS_NO_FATIGUE, "피로도 부족은 NO_FATIGUE여야 합니다.")
	_expect(_snapshot(calendar, resources) == before, "피로도 부족은 모든 자원을 보존해야 합니다.")


func _test_no_gold_changes_nothing() -> void:
	var calendar = CalendarScript.new()
	var resources = ResourcesScript.new(5, {"iron": 1})
	var service = ActionServiceScript.new(calendar, resources)
	var before := _snapshot(calendar, resources)
	var result: Dictionary = service.try_begin_forging(10, "iron", 1, Callable(FakeForgeStarter.new(), "begin"))
	_expect(result.get("status") == ActionServiceScript.STATUS_NO_GOLD, "골드 부족은 NO_GOLD여야 합니다.")
	_expect(_snapshot(calendar, resources) == before, "골드 부족은 모든 자원을 보존해야 합니다.")


func _test_no_material_changes_nothing() -> void:
	var calendar = CalendarScript.new()
	var resources = ResourcesScript.new(100, {"iron": 0})
	var service = ActionServiceScript.new(calendar, resources)
	var before := _snapshot(calendar, resources)
	var result: Dictionary = service.try_begin_forging(10, "iron", 1, Callable(FakeForgeStarter.new(), "begin"))
	_expect(result.get("status") == ActionServiceScript.STATUS_NO_MATERIAL, "재료 부족은 NO_MATERIAL이어야 합니다.")
	_expect(_snapshot(calendar, resources) == before, "재료 부족은 모든 자원을 보존해야 합니다.")


func _test_start_failure_rolls_everything_back() -> void:
	var calendar = CalendarScript.new()
	var resources = ResourcesScript.new(100, {"iron": 2})
	var service = ActionServiceScript.new(calendar, resources)
	var starter := FakeForgeStarter.new()
	starter.should_start = false
	var before := _snapshot(calendar, resources)
	var result: Dictionary = service.try_begin_forging(10, "iron", 1, Callable(starter, "begin"))
	_expect(result.get("status") == ActionServiceScript.STATUS_START_FAILED, "세션 시작 실패를 반환해야 합니다.")
	_expect(_snapshot(calendar, resources) == before, "세션 시작 실패는 골드·재료·피로도를 모두 복구해야 합니다.")


func _snapshot(calendar, resources) -> Dictionary:
	return {"fatigue": calendar.current_fatigue, "gold": resources.gold, "stock": resources.material_stock.duplicate(true)}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
