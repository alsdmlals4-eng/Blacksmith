class_name WorkshopActionService
extends RefCounted

const STATUS_STARTED := "STARTED"
const STATUS_NO_FATIGUE := "NO_FATIGUE"
const STATUS_NO_GOLD := "NO_GOLD"
const STATUS_NO_MATERIAL := "NO_MATERIAL"
const STATUS_START_FAILED := "START_FAILED"

var calendar
var resources


func _init(workshop_calendar, workshop_resources) -> void:
	calendar = workshop_calendar
	resources = workshop_resources


func try_begin_forging(
	gold_cost: int,
	material_id: String,
	material_amount: int,
	begin_callable: Callable
) -> Dictionary:
	var fatigue_preview: Dictionary = calendar.preview_spend("forge")
	if not bool(fatigue_preview.get("ok", false)):
		return fatigue_preview
	if resources.gold < gold_cost:
		return {"ok": false, "status": STATUS_NO_GOLD, "missing_gold": gold_cost - resources.gold}
	if material_id != "" and resources.get_material_count(material_id) < material_amount:
		return {"ok": false, "status": STATUS_NO_MATERIAL, "material_id": material_id, "missing": material_amount - resources.get_material_count(material_id)}

	var before_gold: int = resources.gold
	var before_stock: Dictionary = resources.material_stock.duplicate(true)
	var before_fatigue: int = calendar.current_fatigue
	calendar.try_spend("forge")
	resources.gold -= gold_cost
	if material_id != "":
		resources.material_stock[material_id] = resources.get_material_count(material_id) - material_amount
	var started := bool(begin_callable.call()) if begin_callable.is_valid() else false
	if not started:
		resources.gold = before_gold
		resources.material_stock = before_stock
		calendar.current_fatigue = before_fatigue
		return {"ok": false, "status": STATUS_START_FAILED}
	return {"ok": true, "status": STATUS_STARTED, "fatigue_cost": fatigue_preview.get("cost", 0), "gold_cost": gold_cost}


func try_begin_enhancement(
	session,
	roll_override: float = -1.0,
	leap_roll_override: float = -1.0,
	allow_empty_secondary: bool = false
) -> Dictionary:
	if session == null:
		return {"ok": false, "status": STATUS_START_FAILED}
	var target_level := int(session.enhancement_level) + 1
	var action_id := "special_enhance" if bool(session.requires_precision_for_level(target_level)) else "normal_enhance"
	var fatigue_preview: Dictionary = calendar.preview_spend(action_id)
	if not bool(fatigue_preview.get("ok", false)):
		return fatigue_preview
	var resource_preview: Dictionary = resources.preview_attempt(session, allow_empty_secondary)
	if not bool(resource_preview.get("ok", false)):
		return resource_preview
	var before_fatigue: int = calendar.current_fatigue
	calendar.try_spend(action_id)
	var transaction: Dictionary = resources.try_begin_attempt(session, roll_override, leap_roll_override, allow_empty_secondary)
	if not bool(transaction.get("ok", false)):
		calendar.current_fatigue = before_fatigue
		return transaction
	transaction["fatigue_cost"] = int(fatigue_preview.get("cost", 0))
	transaction["action_id"] = action_id
	return transaction
