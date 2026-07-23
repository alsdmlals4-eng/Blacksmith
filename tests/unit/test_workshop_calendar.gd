extends SceneTree

const WorkshopCalendarScript = preload("res://scripts/progression/workshop_calendar.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("WorkshopCalendar tests PASSED (5 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_action_costs()
	_test_no_fatigue_is_atomic()
	_test_end_day_carryover()
	_test_no_work_converges_below_double_base()
	_test_snapshot_separates_capacity_fields()


func _test_action_costs() -> void:
	var calendar = WorkshopCalendarScript.new()
	_expect(bool(calendar.try_spend("forge").get("ok", false)), "제작 피로도 3을 소비할 수 있어야 합니다.")
	_expect(calendar.current_fatigue == 17, "제작 뒤 피로도는 17이어야 합니다.")
	calendar.try_spend("normal_enhance")
	_expect(calendar.current_fatigue == 16, "일반 강화는 피로도 1이어야 합니다.")
	calendar.try_spend("special_enhance")
	_expect(calendar.current_fatigue == 13, "특수 강화는 피로도 3이어야 합니다.")


func _test_no_fatigue_is_atomic() -> void:
	var calendar = WorkshopCalendarScript.new()
	calendar.current_fatigue = 2
	var before := calendar.snapshot()
	var result: Dictionary = calendar.try_spend("forge")
	_expect(result.get("status") == WorkshopCalendarScript.STATUS_NO_FATIGUE, "피로도 부족은 NO_FATIGUE여야 합니다.")
	_expect(calendar.snapshot() == before, "피로도 부족 시 상태가 변하면 안 됩니다.")


func _test_end_day_carryover() -> void:
	var calendar = WorkshopCalendarScript.new()
	calendar.current_fatigue = 17
	calendar.end_day()
	_expect(calendar.day == 2, "하루 종료 뒤 2일차여야 합니다.")
	_expect(calendar.carryover == 8, "17의 50%는 소수점 버림으로 8이어야 합니다.")
	_expect(calendar.current_fatigue == 28, "다음 날 작업 가능량은 20+8=28이어야 합니다.")


func _test_no_work_converges_below_double_base() -> void:
	var calendar = WorkshopCalendarScript.new()
	for _index in range(20):
		calendar.end_day()
	_expect(calendar.current_fatigue < calendar.base_fatigue * 2, "무작업 이월은 기본 작업량의 두 배 미만에 수렴해야 합니다.")
	_expect(calendar.current_fatigue == 39, "기본 20과 50% 이월은 정수 버림으로 39에 수렴해야 합니다.")


func _test_snapshot_separates_capacity_fields() -> void:
	var calendar = WorkshopCalendarScript.new()
	calendar.current_fatigue = 28
	calendar.carryover = 8
	var value: Dictionary = calendar.snapshot()
	_expect(value.get("current_fatigue") == 28, "현재 작업 가능량을 별도 제공해야 합니다.")
	_expect(value.get("base_fatigue") == 20, "기본 일일량을 별도 제공해야 합니다.")
	_expect(value.get("carryover") == 8, "이월량을 별도 제공해야 합니다.")


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
