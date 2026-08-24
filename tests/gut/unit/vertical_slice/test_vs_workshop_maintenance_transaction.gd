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
		return {
			"allowed": true,
			"gold_cost": 100,
			"reinforcement_units": 2,
			"fatigue_cost": 2,
		}
	func apply(_item, _gold: int, _reinforcement: int) -> Dictionary:
		return {"status": "BLOCKED", "reason": "INJECTED_FAILURE"}


func _item(current: int = 50, maximum: int = 100, checkpoint: int = 30):
	var item = ItemScript.new()
	item.uid = "BSI-abcdefabcdefabcdefabcdefabcdefab"
	item.primary_material_id = "iron"
	item.equipment_group = "SWORD"
	item.current_durability = current
	item.max_durability = maximum
	item.highest_checkpoint = checkpoint
	item.physical_state = "ACTIVE"
	return item


func _resources(gold: int = 1000000, reinforcement: int = 99):
	return WorkshopResourcesScript.new(gold, {"common_reinforcement_material": reinforcement})


func _calendar(fatigue: int = 20):
	var calendar = WorkshopCalendarScript.new()
	calendar.current_fatigue = fatigue
	return calendar


func _service(repair_resolver = null, overhaul_resolver = null):
	if not ResourceLoader.exists(SERVICE_PATH):
		return null
	var script = load(SERVICE_PATH)
	if script == null:
		return null
	return script.new(
		repair_resolver if repair_resolver != null else RepairResolverScript.new(),
		overhaul_resolver if overhaul_resolver != null else OverhaulResolverScript.new()
	)


func test_service_surface_exists() -> void:
	assert_true(ResourceLoader.exists(SERVICE_PATH), "V2 maintenance transaction service must exist")


func test_repair_success_spends_gold_reinforcement_and_fatigue_with_item_change() -> void:
	var service = _service()
	assert_not_null(service)
	if service == null:
		return
	var item = _item(50, 100, 30)
	var resources = _resources(1000, 10)
	var calendar = _calendar(10)
	var quote = RepairResolverScript.new().quote(item)
	var result = service.try_repair(item, resources, calendar)
	assert_eq(result["status"], "APPLIED")
	assert_eq(item.current_durability, 100)
	assert_eq(item.max_durability, 100)
	assert_eq(resources.gold, 1000 - int(quote["gold_cost"]))
	assert_eq(resources.get_material_count("common_reinforcement_material"), 10 - int(quote["reinforcement_units"]))
	assert_eq(calendar.current_fatigue, 10 - int(quote["fatigue_cost"]))


func test_repair_insufficient_fatigue_is_fail_closed_without_any_mutation() -> void:
	var service = _service()
	assert_not_null(service)
	if service == null:
		return
	var item = _item(50, 100, 30)
	var resources = _resources(1000, 10)
	var calendar = _calendar(1)
	var before_resources = resources.snapshot()
	var result = service.try_repair(item, resources, calendar)
	assert_eq(result["status"], "BLOCKED")
	assert_eq(result["reason"], "INSUFFICIENT_FATIGUE")
	assert_eq(item.current_durability, 50)
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(calendar.current_fatigue, 1)


func test_repair_insufficient_material_is_fail_closed_without_any_mutation() -> void:
	var service = _service()
	assert_not_null(service)
	if service == null:
		return
	var item = _item(10, 100, 30)
	var resources = _resources(1000, 0)
	var calendar = _calendar(10)
	var before_resources = resources.snapshot()
	var result = service.try_repair(item, resources, calendar)
	assert_eq(result["status"], "BLOCKED")
	assert_eq(result["reason"], "INSUFFICIENT_REINFORCEMENT")
	assert_eq(item.current_durability, 10)
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(calendar.current_fatigue, 10)


func test_overhaul_success_spends_all_three_resources_and_marks_one_lifetime_use() -> void:
	var service = _service()
	assert_not_null(service)
	if service == null:
		return
	var item = _item(20, 40, 60)
	var resources = _resources(1000000, 25)
	var calendar = _calendar(10)
	var quote = OverhaulResolverScript.new().quote(item)
	var result = service.try_overhaul(item, resources, calendar)
	assert_eq(result["status"], "APPLIED")
	assert_eq(item.max_durability, 55)
	assert_eq(item.current_durability, 55)
	assert_true(item.overhaul_used)
	assert_eq(resources.gold, 1000000 - int(quote["gold_cost"]))
	assert_eq(resources.get_material_count("common_reinforcement_material"), 25 - int(quote["reinforcement_units"]))
	assert_eq(calendar.current_fatigue, 10 - int(quote["fatigue_cost"]))


func test_downstream_apply_failure_rolls_back_resource_and_fatigue_spend() -> void:
	var service = _service(FailingRepairResolver.new(), OverhaulResolverScript.new())
	assert_not_null(service)
	if service == null:
		return
	var item = _item(50, 100, 30)
	var resources = _resources(1000, 10)
	var calendar = _calendar(10)
	var before_resources = resources.snapshot()
	var result = service.try_repair(item, resources, calendar)
	assert_eq(result["status"], "BLOCKED")
	assert_eq(result["reason"], "INJECTED_FAILURE")
	assert_eq(item.current_durability, 50)
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(calendar.current_fatigue, 10)


func test_success_notifies_existing_resource_and_calendar_consumers_once() -> void:
	var service = _service()
	assert_not_null(service)
	if service == null:
		return
	var item = _item(50, 100, 30)
	var resources = _resources(1000, 10)
	var calendar = _calendar(10)
	var resource_events: Array = []
	var calendar_events: Array = []
	resources.changed.connect(func(snapshot): resource_events.append(snapshot))
	calendar.changed.connect(func(snapshot): calendar_events.append(snapshot))
	var result = service.try_repair(item, resources, calendar)
	assert_eq(result["status"], "APPLIED")
	assert_eq(resource_events.size(), 1, "successful maintenance must notify resource consumers once")
	assert_eq(calendar_events.size(), 1, "successful maintenance must notify calendar consumers once")
	if resource_events.size() == 1:
		assert_eq(resource_events[0], resources.snapshot())
	if calendar_events.size() == 1:
		assert_eq(calendar_events[0], calendar.snapshot())
