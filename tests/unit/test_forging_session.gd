extends SceneTree

const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("ForgingSession tests PASSED (5 cases)")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)


func _run_tests() -> void:
	_test_precision_off_completes()
	_test_rapid_taps_start_fever()
	_test_precision_perfect_result()
	_test_quality_effect_values()
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
	_expect(int(session.result.get("raw_base_attack", 0)) == 10, "자동 마감은 원본 공격력 10을 보존해야 합니다.")
	_expect(int(session.result.get("base_attack", 0)) == 10, "자동 마감은 적용 공격력 10을 유지해야 합니다.")


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


func _test_quality_effect_values() -> void:
	var good_session = ForgingSessionScript.new({"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0})
	good_session.register_tap()
	good_session.precision_position = float(good_session.config["precision_target"]) + 0.10
	var good: Dictionary = good_session.finish_precision()
	_expect(good.get("quality_id") == "GOOD", "GOOD 범위는 좋은 마감이어야 합니다.")
	_expect(int(good.get("raw_base_attack", 0)) == 10, "좋은 마감은 원본 공격력 10을 보존해야 합니다.")
	_expect(int(good.get("base_attack", 0)) == 11, "좋은 마감의 10.5 공격력은 11로 반올림되어야 합니다.")
	_expect(is_equal_approx(float(good.get("quality_attack_multiplier", 0.0)), 1.05), "좋은 마감 공격력 배율은 1.05여야 합니다.")
	_expect(is_equal_approx(float(good.get("quality_value_multiplier", 0.0)), 1.05), "좋은 마감 가치 배율은 1.05여야 합니다.")

	var perfect_session = ForgingSessionScript.new({"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0})
	perfect_session.register_tap()
	perfect_session.precision_position = float(perfect_session.config["precision_target"])
	var perfect: Dictionary = perfect_session.finish_precision()
	_expect(int(perfect.get("raw_base_attack", 0)) == 10, "완벽한 마감은 원본 공격력 10을 보존해야 합니다.")
	_expect(int(perfect.get("base_attack", 0)) == 11, "완벽한 마감은 적용 공격력 11을 만들어야 합니다.")
	_expect(is_equal_approx(float(perfect.get("quality_attack_multiplier", 0.0)), 1.10), "완벽한 마감 공격력 배율은 1.10이어야 합니다.")
	_expect(is_equal_approx(float(perfect.get("quality_value_multiplier", 0.0)), 1.12), "완벽한 마감 가치 배율은 1.12여야 합니다.")


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
