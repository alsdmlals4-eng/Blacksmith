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


# Campaign repair commits durability and payment together; standalone probes stay pure to their old API.
func repair_and_save(envelope, item_uid: String, resources, save_service, rolls: Dictionary = {}, random_rolls: bool = false) -> Dictionary:
	if envelope == null or resources == null or save_service == null or not save_service.has_method("save_envelope"):
		return _blocked("MISSING_REPAIR_SAVE_CONTEXT")
	var envelope_script = load("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
	var candidate = envelope_script.from_dict(envelope.to_dict())
	if not candidate.validation_errors.is_empty() or resources.snapshot() != candidate.resource_snapshot():
		return _blocked("REPAIR_SAVE_DIVERGED")
	if envelope_script.pending_trial(candidate, item_uid):
		return _blocked("AQUEDUCT_PENDING")
	if save_service.has_method("load_envelope"):
		var disk = save_service.load_envelope()
		if disk == null or not disk.validation_errors.is_empty() or disk.active_run.run_id != candidate.active_run.run_id:
			return _blocked("REPAIR_SAVE_DIVERGED")
		if not envelope_script.serialized_equal([disk.active_run, disk.to_dict().items_by_uid, disk.resource_snapshot()], [candidate.active_run, candidate.to_dict().items_by_uid, candidate.resource_snapshot()]):
			return _blocked("REPAIR_SAVE_DIVERGED")
	var snapshot: Dictionary = candidate.resource_snapshot()
	var staged_resources = load("res://scripts/economy/workshop_resources.gd").new(int(snapshot.gold), snapshot.material_stock)
	var staged_item = candidate.get_item(item_uid)
	var result: Dictionary = try_repair(staged_item, staged_resources) if random_rolls else try_repair_with_rolls(staged_item, staged_resources, rolls)
	if result.get("status", "") != "APPLIED":
		return result
	candidate.workshop_resources = staged_resources.snapshot()
	var save_error: Error = save_service.save_envelope(candidate)
	if save_error != OK:
		return _blocked("REPAIR_SAVE_FAILED:%d" % int(save_error))
	resources.gold = staged_resources.gold
	resources.material_stock = staged_resources.material_stock.duplicate(true)
	resources.changed.emit(resources.snapshot())
	result.envelope = candidate
	return result


func try_overhaul(_item, _resources, _calendar = null) -> Dictionary:
	return _blocked("OVERHAUL_SUPERSEDED")


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
