extends SceneTree

const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")

var failures: Array[String] = []


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	await _test_manual_normal_uses_shared_resources()
	await _test_manual_special_consumes_stock()
	if failures.is_empty():
		print("Manual enhancement economy integration tests PASSED (2 cases)")
		quit(0)
	for failure in failures:
		push_error(failure)
	quit(1)


func _test_manual_normal_uses_shared_resources() -> void:
	var resources = WorkshopResourcesScript.new(100000, {"whetstone": 2})
	var screen = _new_screen(resources)
	await process_frame
	_set_guaranteed_success(screen.session)
	var cost := int(screen.session.calculate_attempt_cost())
	var before_gold := resources.gold
	screen._on_normal_pressed()
	_expect(screen.session.enhancement_level == 1, "수동 일반 강화 버튼이 실제 강화 세션을 진행해야 합니다.")
	_expect(resources.gold == before_gold - cost, "수동 일반 강화 버튼이 공유 골드를 차감해야 합니다.")
	_expect(resources.get_material_count("whetstone") == 2, "수동 일반 강화는 보조재료를 소비하면 안 됩니다.")
	screen.queue_free()
	await process_frame


func _test_manual_special_consumes_stock() -> void:
	var resources = WorkshopResourcesScript.new(1000000, {
		"whetstone": 1,
		"salamander_core": 1,
	})
	var screen = _new_screen(resources)
	await process_frame
	_set_guaranteed_success(screen.session)
	for _level in range(9):
		screen._on_normal_pressed()
	_expect(screen.session.enhancement_level == 9, "수동 일반 강화로 +9까지 진행되어야 합니다.")
	_expect(screen.session.set_secondary_material("whetstone"), "+10에서 숫돌을 선택할 수 있어야 합니다.")
	_expect(screen.session.set_catalyst_material("salamander_core"), "+10에서 촉매를 선택할 수 있어야 합니다.")
	var before_gold := resources.gold
	var cost := int(screen.session.calculate_attempt_cost())
	screen._on_special_start_pressed()
	_expect(screen.session.state == 1, "수동 특수 강화 시작 후 정밀 판정 상태여야 합니다.")
	_expect(resources.gold == before_gold - cost, "수동 특수 강화가 공유 골드를 차감해야 합니다.")
	_expect(resources.get_material_count("whetstone") == 0, "수동 특수 강화가 보조재료를 소비해야 합니다.")
	_expect(resources.get_material_count("salamander_core") == 0, "수동 특수 강화가 촉매를 소비해야 합니다.")
	screen.queue_free()
	await process_frame


func _new_screen(resources):
	var screen = EnhancementScreenScript.new()
	screen.configure_weapon({
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"base_attack": 10,
		"quality_id": "TEST",
		"quality_label": "테스트",
		"quality_multiplier": 1.0,
	})
	screen.set_workshop_resources(resources)
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
