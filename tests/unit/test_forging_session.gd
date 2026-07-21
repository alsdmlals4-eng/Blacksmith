extends SceneTree

const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("ForgingSession tests PASSED (4 cases)")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)


func _run_tests() -> void:
	_test_precision_off_completes()
	_test_rapid_taps_start_fever()
	_test_precision_perfect_result()
	_test_reset_clears_session()


func _test_precision_off_completes() -> void:
	var session = ForgingSessionScript.new({
		"target_progress": 10.0,
		"tap_power": 10.0,
		"auto_work_per_second": 0.0,
	})
	session.set_precision_enabled(false)
	session.register_tap()
	_expect(session.state == ForgingSessionScript.State.COMPLETE, "정밀작업 OFF에서 제작이 즉시 완료되어야 합니다.")
	_expect(session.result.get("quality_id") == "STANDARD", "자동 마감은 STANDARD 결과여야 합니다.")


func _test_rapid_taps_start_fever() -> void:
	var session = ForgingSessionScript.new({
		"target_progress": 1000.0,
		"tap_power": 10.0,
		"auto_work_per_second": 0.0,
		"rapid_tap_window_seconds": 1.0,
		"fever_gain_base": 50.0,
		"fever_gain_rapid": 50.0,
		"fever_charge_max": 100.0,
		"fever_decay_per_second": 0.0,
		"fever_multiplier": 2.0,
	})
	session.register_tap()
	session.advance(0.1)
	session.register_tap()
	_expect(session.is_fever_active(), "빠른 연속 터치가 피버를 발동해야 합니다.")
	var before: float = session.progress
	session.register_tap()
	_expect(is_equal_approx(session.progress - before, 20.0), "피버 중 터치 작업량에 배율이 적용되어야 합니다.")


func _test_precision_perfect_result() -> void:
	var session = ForgingSessionScript.new({
		"target_progress": 1.0,
		"tap_power": 1.0,
		"auto_work_per_second": 0.0,
	})
	session.set_precision_enabled(true)
	session.register_tap()
	_expect(session.state == ForgingSessionScript.State.FINISHING, "정밀작업 ON이면 제작 완료 후 마감 상태로 진입해야 합니다.")
	session.precision_position = float(session.config["precision_target"])
	var result: Dictionary = session.finish_precision()
	_expect(result.get("quality_id") == "PERFECT", "정중앙 마감은 PERFECT 결과여야 합니다.")


func _test_reset_clears_session() -> void:
	var session = ForgingSessionScript.new({
		"target_progress": 10.0,
		"tap_power": 5.0,
		"auto_work_per_second": 0.0,
	})
	session.register_tap()
	session.reset()
	_expect(session.state == ForgingSessionScript.State.FORGING, "reset 후 제작 상태로 돌아와야 합니다.")
	_expect(is_zero_approx(session.progress), "reset 후 제작 진행도가 0이어야 합니다.")
	_expect(session.tap_count == 0, "reset 후 터치 횟수가 0이어야 합니다.")


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
