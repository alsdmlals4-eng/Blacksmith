class_name VSRepairResolver
extends RefCounted

const SWORD_BASE_REPAIR_GOLD := 800
const SETUP_FRACTION := 0.05
const VARIABLE_FRACTION := 0.65
const FATIGUE_COST := 2
const MATERIAL_STRUCTURE_MULTIPLIERS := {
	"iron": 1.00,
	"silver": 1.20,
	"meteor_iron": 1.50,
}


func quote(item) -> Dictionary:
	if item == null:
		return _blocked("MISSING_ITEM")
	if str(item.physical_state) == "DESTROYED" or int(item.current_durability) <= 0 or int(item.max_durability) <= 0:
		return _blocked("ITEM_DESTROYED")
	if str(item.equipment_group) != "SWORD":
		return _blocked("UNSUPPORTED_EQUIPMENT_GROUP")
	if not MATERIAL_STRUCTURE_MULTIPLIERS.has(str(item.primary_material_id)):
		return _blocked("UNSUPPORTED_PRIMARY_MATERIAL")

	var current := int(item.current_durability)
	var maximum := int(item.max_durability)
	if current >= maximum:
		return _blocked("NO_CURRENT_DAMAGE")

	var missing := maximum - current
	var material_multiplier := float(MATERIAL_STRUCTURE_MULTIPLIERS[str(item.primary_material_id)])
	var secured_multiplier := _secured_band_multiplier(int(item.highest_checkpoint))
	var reference_cost := float(SWORD_BASE_REPAIR_GOLD) * material_multiplier * secured_multiplier
	var burden_fraction := SETUP_FRACTION + VARIABLE_FRACTION * (float(missing) / 100.0)
	var gold_cost := int(round(reference_cost * burden_fraction))
	var reinforcement_units := maxi(1, int(ceil(float(missing) / 25.0)))

	return {
		"allowed": true,
		"reason": "",
		"missing_current": missing,
		"gold_cost": gold_cost,
		"reinforcement_units": reinforcement_units,
		"fatigue_cost": FATIGUE_COST,
		"result_current": maximum,
		"result_max": maximum,
	}


func apply(item, available_gold: int, available_reinforcement: int) -> Dictionary:
	var repair_quote := quote(item)
	if not bool(repair_quote.get("allowed", false)):
		return {
			"status": "BLOCKED",
			"reason": str(repair_quote.get("reason", "REPAIR_NOT_ALLOWED")),
		}

	var gold_cost := int(repair_quote["gold_cost"])
	var reinforcement_units := int(repair_quote["reinforcement_units"])
	if available_gold < gold_cost:
		return {"status": "BLOCKED", "reason": "INSUFFICIENT_GOLD"}
	if available_reinforcement < reinforcement_units:
		return {"status": "BLOCKED", "reason": "INSUFFICIENT_REINFORCEMENT"}

	item.current_durability = int(repair_quote["result_current"])
	return {
		"status": "APPLIED",
		"reason": "",
		"gold_cost": gold_cost,
		"reinforcement_units": reinforcement_units,
		"fatigue_cost": FATIGUE_COST,
		"result_current": int(item.current_durability),
		"result_max": int(item.max_durability),
	}


func _secured_band_multiplier(highest_checkpoint: int) -> float:
	if highest_checkpoint >= 90:
		return 3.00
	if highest_checkpoint >= 60:
		return 2.25
	if highest_checkpoint >= 30:
		return 1.25
	if highest_checkpoint >= 10:
		return 1.10
	return 1.00


func _blocked(reason: String) -> Dictionary:
	return {"allowed": false, "reason": reason}
