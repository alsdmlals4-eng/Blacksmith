class_name VSWorkshopMaintenanceService
extends RefCounted

const REINFORCEMENT_MATERIAL_ID := "common_reinforcement_material"
const RepairResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")
const OverhaulResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_overhaul_resolver.gd")

var repair_resolver
var overhaul_resolver


func _init(repair = null, overhaul = null) -> void:
	repair_resolver = repair if repair != null else RepairResolverScript.new()
	overhaul_resolver = overhaul if overhaul != null else OverhaulResolverScript.new()


func try_repair(item, resources, calendar) -> Dictionary:
	return _try_apply(item, resources, calendar, repair_resolver)


func try_overhaul(item, resources, calendar) -> Dictionary:
	return _try_apply(item, resources, calendar, overhaul_resolver)


func _try_apply(item, resources, calendar, resolver) -> Dictionary:
	if item == null:
		return _blocked("MISSING_ITEM")
	if resources == null:
		return _blocked("MISSING_RESOURCES")
	if calendar == null:
		return _blocked("MISSING_CALENDAR")
	if resolver == null or not resolver.has_method("quote") or not resolver.has_method("apply"):
		return _blocked("INVALID_RESOLVER")
	if not resources.has_method("get_material_count"):
		return _blocked("INVALID_RESOURCES")

	var quote: Dictionary = resolver.quote(item)
	if not bool(quote.get("allowed", false)):
		return _blocked(str(quote.get("reason", "MAINTENANCE_NOT_ALLOWED")))

	var gold_cost := int(quote.get("gold_cost", 0))
	var reinforcement_units := int(quote.get("reinforcement_units", 0))
	var fatigue_cost := int(quote.get("fatigue_cost", 0))
	if int(resources.gold) < gold_cost:
		return _blocked("INSUFFICIENT_GOLD")
	if int(resources.get_material_count(REINFORCEMENT_MATERIAL_ID)) < reinforcement_units:
		return _blocked("INSUFFICIENT_REINFORCEMENT")
	if int(calendar.current_fatigue) < fatigue_cost:
		return _blocked("INSUFFICIENT_FATIGUE")

	var before_gold := int(resources.gold)
	var before_stock: Dictionary = resources.material_stock.duplicate(true)
	var before_fatigue := int(calendar.current_fatigue)

	resources.gold -= gold_cost
	resources.material_stock[REINFORCEMENT_MATERIAL_ID] = (
		int(resources.get_material_count(REINFORCEMENT_MATERIAL_ID)) - reinforcement_units
	)
	calendar.current_fatigue -= fatigue_cost

	var result: Dictionary = resolver.apply(item, gold_cost, reinforcement_units)
	if str(result.get("status", "")) != "APPLIED":
		resources.gold = before_gold
		resources.material_stock = before_stock
		calendar.current_fatigue = before_fatigue
		return result

	result["gold_cost"] = gold_cost
	result["reinforcement_units"] = reinforcement_units
	result["fatigue_cost"] = fatigue_cost
	resources.changed.emit(resources.snapshot())
	calendar.changed.emit(calendar.snapshot())
	return result


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
