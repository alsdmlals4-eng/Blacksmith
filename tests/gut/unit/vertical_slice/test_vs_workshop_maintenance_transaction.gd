extends "res://addons/gut/test.gd"

const SERVICE_PATH := "res://scripts/vertical_slice/services/vs_workshop_maintenance_service.gd"
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const RepairResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")
const OverhaulResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_overhaul_resolver.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")
const WorkshopCalendarScript = preload("res://scripts/progression/workshop_calendar.gd")

class FailingRepairResolver:
	extends RefCounted
	func quote(_item) -> Dictionary:
		return {"allowed": true, "gold_cost": 39, "reinforcement_units": 1}
	func apply(_item, _gold: int, _reinforcement: int) -> Dictionary:
		return {"status": "BLOCKED", "reason": "INJECTED_FAILURE"}


func _item(current: int = 3, maximum: int = 5) -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-abcdefabcdefabcdefabcdefabcdefab"
	item.primary_material_id = "iron"
	item.current_durability = current
	item.max_durability = maximum
	item.repair_job_available = true
	return item


func _resources(gold: int = 1000, reinforcement: int = 10):
	return WorkshopResourcesScript.new(gold, {"common_reinforcement_material": reinforcement})


func _service(repair_resolver = null):
	return load(SERVICE_PATH).new(repair_resolver if repair_resolver != null else RepairResolverScript.new(), OverhaulResolverScript.new())


func test_service_surface_exists() -> void:
	assert_true(ResourceLoader.exists(SERVICE_PATH))


func test_repair_success_spends_gold_and_one_reinforcement_without_calendar_cost() -> void:
	var item = _item()
	var resources = _resources()
	var calendar = WorkshopCalendarScript.new()
	calendar.current_fatigue = 1
	var result = _service().try_repair_with_rolls(item, resources, {"quality_roll_percent": 0.0, "scar_roll_percent": 99.0})
	assert_eq(result["status"], "APPLIED")
	assert_eq(item.current_durability, 5)
	assert_eq(resources.gold, 961)
	assert_eq(resources.get_material_count("common_reinforcement_material"), 9)
	assert_eq(calendar.current_fatigue, 1)


func test_repair_insufficient_material_is_fail_closed_without_any_mutation() -> void:
	var item = _item()
	var resources = _resources(1000, 0)
	var before_resources = resources.snapshot()
	var result = _service().try_repair_with_rolls(item, resources, {"quality_roll_percent": 0.0, "scar_roll_percent": 99.0})
	assert_eq(result["status"], "BLOCKED")
	assert_eq(result["reason"], "INSUFFICIENT_REINFORCEMENT")
	assert_eq(item.current_durability, 3)
	assert_true(item.repair_job_available)
	assert_eq(resources.snapshot(), before_resources)


func test_overhaul_is_not_a_maintenance_path_anymore() -> void:
	var result = _service().try_overhaul(_item(), _resources(), WorkshopCalendarScript.new())
	assert_eq(result["status"], "BLOCKED")
	assert_eq(result["reason"], "OVERHAUL_SUPERSEDED")


func test_downstream_apply_failure_rolls_back_resource_spend() -> void:
	var item = _item()
	var resources = _resources()
	var before_resources = resources.snapshot()
	var result = _service(FailingRepairResolver.new()).try_repair_with_rolls(item, resources, {})
	assert_eq(result["status"], "BLOCKED")
	assert_eq(result["reason"], "INJECTED_FAILURE")
	assert_eq(item.current_durability, 3)
	assert_eq(resources.snapshot(), before_resources)


func test_success_notifies_resource_consumers_once() -> void:
	var item = _item()
	var resources = _resources()
	var resource_events: Array = []
	resources.changed.connect(func(snapshot): resource_events.append(snapshot))
	var result = _service().try_repair_with_rolls(item, resources, {"quality_roll_percent": 0.0, "scar_roll_percent": 99.0})
	assert_eq(result["status"], "APPLIED")
	assert_eq(resource_events.size(), 1)
	if resource_events.size() == 1:
		assert_eq(resource_events[0], resources.snapshot())
