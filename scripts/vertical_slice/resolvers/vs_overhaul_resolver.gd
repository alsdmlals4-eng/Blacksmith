class_name VSOverhaulResolver
extends RefCounted

const BASE_GOLD_COST := 750000
const REINFORCEMENT_UNITS := 20
const FATIGUE_COST := 5
const MAX_THRESHOLD := 40
const MAX_RECOVERY_CAP := 60
const MAX_RECOVERY_AMOUNT := 15
const REQUIRED_CHECKPOINT := 60
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
	if int(item.max_durability) > MAX_THRESHOLD:
		return _blocked("MAX_ABOVE_OVERHAUL_THRESHOLD")
	if int(item.highest_checkpoint) < REQUIRED_CHECKPOINT:
		return _blocked("CHECKPOINT_BELOW_60")
	if bool(item.overhaul_used):
		return _blocked("OVERHAUL_ALREADY_USED")

	var material_multiplier := float(MATERIAL_STRUCTURE_MULTIPLIERS[str(item.primary_material_id)])
	var gold_cost := int(round(float(BASE_GOLD_COST) * material_multiplier))
	var result_max := mini(MAX_RECOVERY_CAP, int(item.max_durability) + MAX_RECOVERY_AMOUNT)
	return {
		"allowed": true,
		"reason": "",
		"gold_cost": gold_cost,
		"reinforcement_units": REINFORCEMENT_UNITS,
		"fatigue_cost": FATIGUE_COST,
		"result_current": result_max,
		"result_max": result_max,
	}


func apply(item, available_gold: int, available_reinforcement: int) -> Dictionary:
	var overhaul_quote := quote(item)
	if not bool(overhaul_quote.get("allowed", false)):
		return {
			"status": "BLOCKED",
			"reason": str(overhaul_quote.get("reason", "OVERHAUL_NOT_ALLOWED")),
		}

	var gold_cost := int(overhaul_quote["gold_cost"])
	if available_gold < gold_cost:
		return {"status": "BLOCKED", "reason": "INSUFFICIENT_GOLD"}
	if available_reinforcement < REINFORCEMENT_UNITS:
		return {"status": "BLOCKED", "reason": "INSUFFICIENT_REINFORCEMENT"}

	item.max_durability = int(overhaul_quote["result_max"])
	item.current_durability = int(overhaul_quote["result_current"])
	item.overhaul_used = true
	return {
		"status": "APPLIED",
		"reason": "",
		"gold_cost": gold_cost,
		"reinforcement_units": REINFORCEMENT_UNITS,
		"fatigue_cost": FATIGUE_COST,
		"result_current": int(item.current_durability),
		"result_max": int(item.max_durability),
	}


func _blocked(reason: String) -> Dictionary:
	return {"allowed": false, "reason": reason}
