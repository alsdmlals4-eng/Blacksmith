# 현재 정본의 수리 결제와 결과 적용을 원자적으로 처리한다.
class_name VSWorkshopMaintenanceService
extends RefCounted

const REINFORCEMENT_MATERIAL_ID := "common_reinforcement_material"
const RepairResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")

var repair_resolver


func _init(repair = null, _overhaul = null) -> void:
	repair_resolver = repair if repair != null else RepairResolverScript.new()


func try_repair(item, resources, _calendar = null) -> Dictionary:
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	return try_repair_with_rolls(item, resources, {
		"quality_roll_percent": rng.randf_range(0.0, 100.0),
		"scar_roll_percent": rng.randf_range(0.0, 100.0),
	})


func try_repair_with_rolls(item, resources, rolls: Dictionary) -> Dictionary:
	if item == null: return _blocked("MISSING_ITEM")
	if resources == null or not resources.has_method("get_material_count"): return _blocked("INVALID_RESOURCES")
	if repair_resolver == null or not repair_resolver.has_method("quote"): return _blocked("INVALID_REPAIR_RESOLVER")
	var quote: Dictionary = repair_resolver.quote(item)
	if not bool(quote.get("allowed", false)): return _blocked(str(quote.get("reason", "REPAIR_NOT_ALLOWED")))
	var gold_cost := int(quote.get("gold_cost", 0))
	var reinforcement_units := int(quote.get("reinforcement_units", 0))
	if int(resources.gold) < gold_cost: return _blocked("INSUFFICIENT_GOLD")
	if int(resources.get_material_count(REINFORCEMENT_MATERIAL_ID)) < reinforcement_units: return _blocked("INSUFFICIENT_REINFORCEMENT")
	var before_gold := int(resources.gold)
	var before_stock: Dictionary = resources.material_stock.duplicate(true)
	resources.gold -= gold_cost
	resources.material_stock[REINFORCEMENT_MATERIAL_ID] = int(resources.get_material_count(REINFORCEMENT_MATERIAL_ID)) - reinforcement_units
	var result: Dictionary
	if repair_resolver.has_method("apply_with_rolls"):
		result = repair_resolver.apply_with_rolls(item, gold_cost, reinforcement_units, rolls.duplicate(true))
	else:
		result = repair_resolver.apply(item, gold_cost, reinforcement_units)
	if str(result.get("status", "")) != "APPLIED":
		resources.gold = before_gold
		resources.material_stock = before_stock
		return result
	result["gold_cost"] = gold_cost
	result["reinforcement_units"] = reinforcement_units
	resources.changed.emit(resources.snapshot())
	return result


func try_overhaul(_item, _resources, _calendar = null) -> Dictionary:
	return _blocked("OVERHAUL_SUPERSEDED")


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
