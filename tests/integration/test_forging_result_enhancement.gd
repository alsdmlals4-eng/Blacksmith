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
	await _test_fever_value_reaches_enhancement_and_storage()
	await _test_quality_value_survives_downgrade_restore()
	if failures.is_empty():
		print("Forging result enhancement integration tests PASSED (4 cases)")
		quit(0)
	for failure in failures:
		push_error(failure)
	quit(1)


func _test_perfect_quality_reaches_enhancement_and_storage() -> void:
	var perfect_screen = _new_screen(_forge_result(true))
	var standard_screen = _new_screen(_forge_result(false))
	await process_frame
	_expect(int(perfect_screen.session.raw_base_attack) == 10, "원본 공격력 10을 보존해야 합니다.")
	_expect(int(perfect_screen.session.base_attack) == 11, "완벽한 마감 공격력이 강화 세션에 전달되어야 합니다.")
	_expect(is_equal_approx(float(perfect_screen.session.value_bonus_total), 0.12), "완벽한 마감 가치 +12%가 판매가에 전달되어야 합니다.")
	_expect(
		int(perfect_screen.session.get_current_sale_price()) > int(standard_screen.session.get_current_sale_price()),
		"완벽한 마감의 실제 판매가는 보통 마감보다 높아야 합니다."
	)
	var record: Dictionary = perfect_screen.build_weapon_record()
	_expect(int(record.get("raw_base_attack", 0)) == 10, "보관 기록이 원본 공격력을 보존해야 합니다.")
	_expect(int(record.get("base_attack", 0)) == 11, "보관 기록이 품질 적용 공격력을 보존해야 합니다.")
	_expect(is_equal_approx(float(record.get("quality_attack_multiplier", 0.0)), 1.10), "보관 기록이 공격력 배율을 보존해야 합니다.")
	_expect(is_equal_approx(float(record.get("quality_value_multiplier", 0.0)), 1.12), "보관 기록이 가치 배율을 보존해야 합니다.")
	_expect(int(record.get("sale_price", 0)) == int(perfect_screen.session.get_current_sale_price()), "보관 판매가는 품질 적용 판매가와 같아야 합니다.")
	perfect_screen.queue_free()
	standard_screen.queue_free()
	await process_frame


func _test_standard_quality_stays_baseline() -> void:
	var screen = _new_screen(_forge_result(false))
	await process_frame
	_expect(int(screen.session.raw_base_attack) == 10, "자동 마감은 원본 공격력 10을 보존해야 합니다.")
	_expect(int(screen.session.base_attack) == 10, "자동 마감은 공격력 10을 유지해야 합니다.")
	_expect(is_zero_approx(float(screen.session.value_bonus_total)), "자동 마감은 가치 보너스를 만들면 안 됩니다.")
	var record: Dictionary = screen.build_weapon_record()
	_expect(is_equal_approx(float(record.get("quality_attack_multiplier", 0.0)), 1.0), "자동 마감 보관 기록의 공격력 배율은 1.0이어야 합니다.")
	_expect(is_equal_approx(float(record.get("quality_value_multiplier", 0.0)), 1.0), "자동 마감 보관 기록의 가치 배율은 1.0이어야 합니다.")
	screen.queue_free()
	await process_frame


func _test_fever_value_reaches_enhancement_and_storage() -> void:
	var fever_screen = _new_screen(_forge_result(false, true))
	var standard_screen = _new_screen(_forge_result(false, false))
	await process_frame
	_expect(is_equal_approx(float(fever_screen.session.fever_value_bonus), 0.05), "피버 제작 가치 +5%가 강화 세션에 전달되어야 합니다.")
	_expect(is_equal_approx(float(fever_screen.session.crafting_value_multiplier), 1.05), "피버 무기의 총 제작 가치 배율은 ×1.05여야 합니다.")
	_expect(bool(fever_screen.session.forging_completed_during_fever), "피버 중 제작 완료 기록이 강화 세션에 전달되어야 합니다.")
	_expect(int(fever_screen.session.get_current_sale_price()) > int(standard_screen.session.get_current_sale_price()), "피버 보너스 무기의 판매가는 무보너스 무기보다 높아야 합니다.")
	var record: Dictionary = fever_screen.build_weapon_record()
	_expect(is_equal_approx(float(record.get("fever_value_bonus", 0.0)), 0.05), "보관 기록이 피버 가치 +5%를 보존해야 합니다.")
	_expect(is_equal_approx(float(record.get("crafting_value_multiplier", 0.0)), 1.05), "보관 기록이 총 제작 가치 배율을 보존해야 합니다.")
	_expect(bool(record.get("forging_completed_during_fever", false)), "보관 기록이 피버 중 완성을 보존해야 합니다.")
	fever_screen.queue_free()
	standard_screen.queue_free()
	await process_frame


func _test_quality_value_survives_downgrade_restore() -> void:
	var screen = _new_screen(_forge_result(true, true))
	await process_frame
	_set_guaranteed_success(screen.session)
	for _level in range(9):
		screen._on_normal_pressed()
	_expect(screen.session.enhancement_level == 9, "품질 복원 테스트는 +9까지 성공해야 합니다.")
	_expect(screen.session.set_secondary_material("whetstone"), "+10 특수 강화에서 숫돌을 선택할 수 있어야 합니다.")
	screen._on_special_start_pressed()
	_expect(screen.session.state == 1, "+10 특수 강화가 정밀 판정 상태로 진입해야 합니다.")
	screen.session.precision_position = float(screen.session.config["precision"]["target"])
	screen._on_precision_pressed()
	screen._on_normal_pressed()
	_expect(screen.session.enhancement_level == 11, "단계 하락 검증 전에 +11에 도달해야 합니다.")

	screen.session.config["base_success_by_target_level"]["12"] = 0.0
	screen.session.config["risk"]["downgrade_ratio_by_decade"]["1"] = 1.0
	screen.session.config["risk"]["destroy_ratio_by_decade"]["1"] = 0.0
	var transaction: Dictionary = screen.workshop_resources.try_begin_attempt(screen.session, 0.5)
	_expect(bool(transaction.get("ok", false)), "+12 단계 하락 시도가 시작되어야 합니다.")
	_expect(screen.session.enhancement_level == 10, "단계 하락 결과는 +10이어야 합니다.")
	_expect(int(screen.session.base_attack) == 11, "단계 하락 후에도 완벽한 마감 기본 공격력을 유지해야 합니다.")
	_expect(is_equal_approx(float(screen.session.value_bonus_total), 0.17), "단계 하락 복원 뒤에도 완벽한 마감 +12%와 피버 +5%를 유지해야 합니다.")
	_expect(is_equal_approx(float(screen.session.fever_value_bonus), 0.05), "단계 하락 뒤에도 피버 가치 보너스를 유지해야 합니다.")
	screen.queue_free()
	await process_frame


func _forge_result(perfect: bool, with_fever: bool = false) -> Dictionary:
	var config := {"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0}
	if with_fever:
		config["fever_gain_base"] = 100.0
		config["fever_gain_rapid"] = 100.0
		config["fever_charge_max"] = 100.0
		config["fever_multiplier"] = 1.0
	var session = ForgingSessionScript.new(config)
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


func _set_guaranteed_success(session) -> void:
	var rates := {}
	for level in range(1, 101):
		rates[str(level)] = 1.0
	session.config["base_success_by_target_level"] = rates


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
