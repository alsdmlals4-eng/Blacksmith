extends SceneTree

const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")

var failures: Array[String] = []


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	await _test_manual_normal_uses_shared_resources()
	await _test_manual_special_consumes_stock_and_resyncs_selection()
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
	var before_gold: int = int(resources.gold)
	screen._on_normal_pressed()
	_expect(screen.session.enhancement_level == 1, "수동 일반 강화 버튼이 실제 강화 세션을 진행해야 합니다.")
	_expect(resources.gold == before_gold - cost, "수동 일반 강화 버튼이 공유 골드를 차감해야 합니다.")
	_expect(resources.get_material_count("whetstone") == 2, "수동 일반 강화는 보조재료를 소비하면 안 됩니다.")
	screen.queue_free()
	await process_frame


func _test_manual_special_consumes_stock_and_resyncs_selection() -> void:
	var resources = WorkshopResourcesScript.new(1000000, {
		"whetstone": 1,
		"flame_stone": 1,
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
	var before_gold: int = int(resources.gold)
	var cost := int(screen.session.calculate_attempt_cost())
	screen._on_special_start_pressed()
	_expect(screen.session.state == 1, "수동 특수 강화 시작 후 정밀 판정 상태여야 합니다.")
	_expect(resources.gold == before_gold - cost, "수동 특수 강화가 공유 골드를 차감해야 합니다.")
	_expect(resources.get_material_count("whetstone") == 0, "수동 특수 강화가 보조재료를 소비해야 합니다.")
	_expect(resources.get_material_count("salamander_core") == 0, "수동 특수 강화가 촉매를 소비해야 합니다.")
	_expect(str(screen.session.selected_secondary_id) == "whetstone", "정밀 판정 중 세션의 사용 재료 기록이 다른 재료로 바뀌면 안 됩니다.")

	screen.session.precision_position = float(screen.session.config["precision"]["target"])
	screen._on_precision_pressed()
	for _level in range(9):
		screen._on_normal_pressed()
	_expect(screen.session.enhancement_level == 19, "+20 특수 강화 직전까지 진행되어야 합니다.")
	_expect(str(screen.session.selected_secondary_id) == "flame_stone", "다음 특수 강화에서는 소진된 숫돌 대신 가용 화염석으로 선택을 동기화해야 합니다.")
	_expect(str(screen.session.selected_catalyst_id) == "", "소진된 촉매는 다음 특수 강화에서 사용하지 않음으로 동기화해야 합니다.")
	var selected_secondary := str(screen.secondary_select.get_item_metadata(screen.secondary_select.selected))
	var selected_catalyst := str(screen.catalyst_select.get_item_metadata(screen.catalyst_select.selected))
	_expect(selected_secondary == str(screen.session.selected_secondary_id), "보조재료 UI와 세션 선택이 일치해야 합니다.")
	_expect(selected_catalyst == str(screen.session.selected_catalyst_id), "촉매 UI와 세션 선택이 일치해야 합니다.")
	screen.queue_free()
	await process_frame


func _new_screen(resources):
	var screen = EnhancementScreenScript.new()
	screen.configure_weapon({
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"raw_base_attack": 10,
		"base_attack": 10,
		"quality_id": "TEST",
		"quality_label": "테스트",
		"quality_attack_multiplier": 1.0,
		"quality_value_multiplier": 1.0,
		"fever_value_bonus": 0.0,
		"fever_value_multiplier": 1.0,
		"crafting_value_multiplier": 1.0,
		"forging_completed_during_fever": false,
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
