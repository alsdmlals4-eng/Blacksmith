# 작업대 화면이 현재 정본 내구도·수리 상태를 표시하고 실행하는지 검증한다.
extends "res://addons/gut/test.gd"

const SCREEN_PATH := "res://scripts/vertical_slice/ui/vs_workshop_screen.gd"
const SCREEN_SCENE := preload("res://scenes/vertical_slice/screens/vs_workshop_screen.tscn")
const ItemScript := preload("res://scripts/vertical_slice/domain/vs_item.gd")
const ResourcesScript := preload("res://scripts/economy/workshop_resources.gd")


class TrackingMaintenanceService extends RefCounted:
	var random_repair_calls := 0
	var deterministic_repair_calls := 0


	func try_repair(_item, _resources, _calendar = null) -> Dictionary:
		random_repair_calls += 1
		return {"status": "BLOCKED", "reason": "TRACKED_RANDOM_REPAIR"}


	func try_repair_with_rolls(_item, _resources, _rolls: Dictionary) -> Dictionary:
		deterministic_repair_calls += 1
		return {"status": "BLOCKED", "reason": "TRACKED_DETERMINISTIC_REPAIR"}


func _item(current: int = 3, maximum: int = 5):
	var item = ItemScript.new()
	item.uid = "UI-ITEM-001"
	item.primary_material_id = "iron"
	item.enhancement_level = 11
	item.highest_checkpoint = 10
	item.base_max_durability = 5
	item.max_durability = maximum
	item.current_durability = current
	item.repair_job_available = true
	return item


func test_screen_exposes_current_durability_and_repair_quote() -> void:
	assert_true(ResourceLoader.exists(SCREEN_PATH), "Workshop screen controller must exist")
	if not ResourceLoader.exists(SCREEN_PATH):
		return
	var screen = load(SCREEN_PATH).new()
	screen.configure_context(_item(), ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	var state: Dictionary = screen.view_state()
	assert_eq(state["durability_text"], "3 / 5 / 5")
	assert_eq(state["durability_state"], "MINOR")
	assert_true(state["repair_allowed"])
	assert_eq(state["repair_gold_cost"], 39)
	assert_eq(state["repair_material_units"], 1)
	assert_eq(state.get("repair_quality_summary", ""), "예상 회복: 최상 100% / 표준 75% / 미흡 50%")
	assert_eq(state.get("repair_scar_summary", ""), "MAX 흉터 가능성: 10%")
	assert_eq(state.get("repair_job_summary", ""), "수리하면 다음 실제 손상 전까지 다시 수리할 수 없습니다")
	screen.free()


func test_screen_repair_refreshes_the_bound_item_and_disables_repeat_repair() -> void:
	if not ResourceLoader.exists(SCREEN_PATH):
		fail_test("Workshop screen controller must exist")
		return
	var item = _item()
	var resources = ResourcesScript.new(100, {"common_reinforcement_material": 1})
	var screen = load(SCREEN_PATH).new()
	screen.configure_context(item, resources)
	var result: Dictionary = screen.request_repair_with_rolls({"quality_roll_percent": 0.0, "scar_roll_percent": 99.0})
	assert_eq(result["status"], "APPLIED")
	assert_eq(item.current_durability, 5)
	assert_false(screen.view_state()["repair_allowed"])
	assert_eq(screen.view_state()["repair_reason"], "REPAIR_JOB_UNAVAILABLE")
	screen.free()


func test_screen_refreshes_visible_durability_after_an_enhancement_damage_event() -> void:
	var item = _item()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	assert_eq(screen.get_node("WorkshopLayout/DurabilityValueLabel").text, "3 / 5 / 5")
	item.apply_damage_event()
	screen.refresh_after_enhancement()
	assert_eq(screen.get_node("WorkshopLayout/DurabilityValueLabel").text, "2 / 5 / 5")
	assert_true(screen.get_node("WorkshopLayout/RepairButton").disabled == false)


func test_repair_button_uses_randomized_maintenance_path_not_test_rolls() -> void:
	var item = _item()
	var tracking_service = TrackingMaintenanceService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}), tracking_service)
	screen._on_repair_pressed()
	assert_eq(tracking_service.random_repair_calls, 1)
	assert_eq(tracking_service.deterministic_repair_calls, 0)
	assert_eq(screen.get_node("WorkshopLayout/RepairMessageLabel").text, "수리 불가: TRACKED_RANDOM_REPAIR")
