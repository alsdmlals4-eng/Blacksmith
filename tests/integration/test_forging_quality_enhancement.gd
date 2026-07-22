extends SceneTree

const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")
const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")

var failures: Array[String] = []

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	await _test_perfect_quality_reaches_enhancement_and_storage()
	await _test_standard_quality_stays_baseline()
	if failures.is_empty():
		print("Forging quality enhancement integration tests PASSED (2 cases)")
		quit(0)
	for failure in failures:
		push_error(failure)
	quit(1)

func _test_perfect_quality_reaches_enhancement_and_storage() -> void:
	var result := _forge_result(true)
	var screen = _new_screen(result)
	await process_frame
	_expect(int(screen.session.raw_base_attack) == 10, "원본 공격력 10을 보존해야 합니다.")
	_expect(int(screen.session.base_attack) == 11, "완벽한 마감 공격력이 강화 세션에 전달되어야 합니다.")
	_expect(is_equal_approx(float(screen.session.value_bonus_total), 0.12), "완벽한 마감 가치 +12%가 판매가에 전달되어야 합니다.")
	var record: Dictionary = screen.build_weapon_record()
	_expect(int(record.get("raw_base_attack", 0)) == 10, "보관 기록이 원본 공격력을 보존해야 합니다.")
	_expect(int(record.get("base_attack", 0)) == 11, "보관 기록이 품질 적용 공격력을 보존해야 합니다.")
	_expect(is_equal_approx(float(record.get("quality_value_multiplier", 0.0)), 1.12), "보관 기록이 가치 배율을 보존해야 합니다.")
	screen.queue_free()
	await process_frame

func _test_standard_quality_stays_baseline() -> void:
	var result := _forge_result(false)
	var screen = _new_screen(result)
	await process_frame
	_expect(int(screen.session.base_attack) == 10, "자동 마감은 공격력 10을 유지해야 합니다.")
	_expect(is_zero_approx(float(screen.session.value_bonus_total)), "자동 마감은 가치 보너스를 만들면 안 됩니다.")
	screen.queue_free()
	await process_frame

func _forge_result(perfect: bool) -> Dictionary:
	var session = ForgingSessionScript.new({"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0})
	if not perfect:
		session.set_precision_enabled(false)
	session.register_tap()
	if perfect:
		session.precision_position = float(session.config["precision_target"])
		return session.finish_precision()
	return session.result.duplicate(true)

func _new_screen(result: Dictionary):
	var screen = EnhancementScreenScript.new()
	screen.configure_weapon(result)
	screen.set_workshop_resources(WorkshopResourcesScript.new(1000000, {"whetstone": 20}))
	get_root().add_child(screen)
	return screen

func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
