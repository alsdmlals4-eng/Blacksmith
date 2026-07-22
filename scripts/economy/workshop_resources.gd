class_name WorkshopResources
extends RefCounted

signal changed(snapshot: Dictionary)

const STATUS_STARTED := "STARTED"
const STATUS_NO_GOLD := "NO_GOLD"
const STATUS_NO_MATERIAL := "NO_MATERIAL"
const STATUS_INVALID_SESSION := "INVALID_SESSION"
const STATUS_INVALID_STATE := "INVALID_STATE"
const STATUS_START_FAILED := "START_FAILED"

var gold: int = 0
var material_stock: Dictionary = {}


func _init(starting_gold: int = 0, starting_stock: Dictionary = {}) -> void:
	gold = maxi(starting_gold, 0)
	material_stock = starting_stock.duplicate(true)
	_normalize_stock()


func snapshot() -> Dictionary:
	return {
		"gold": gold,
		"material_stock": material_stock.duplicate(true),
	}


func get_material_count(material_id: String) -> int:
	if material_id == "":
		return 0
	return maxi(int(material_stock.get(material_id, 0)), 0)


func has_material(material_id: String, amount: int = 1) -> bool:
	if material_id == "":
		return true
	return get_material_count(material_id) >= maxi(amount, 0)


func available_material_id(material_id: String) -> String:
	return material_id if material_id != "" and has_material(material_id) else ""


func preview_attempt(session) -> Dictionary:
	if session == null or not session.has_method("begin_attempt") or not session.has_method("calculate_attempt_cost"):
		return {"ok": false, "status": STATUS_INVALID_SESSION}
	if int(session.state) != 0 or bool(session.destroyed) or int(session.enhancement_level) >= int(session.config.get("max_level", 100)):
		return {"ok": false, "status": STATUS_INVALID_STATE}

	var target_level := int(session.enhancement_level) + 1
	var is_special := bool(session.uses_materials_for_level(target_level))
	var secondary_id := str(session.selected_secondary_id) if is_special else ""
	var catalyst_id := str(session.selected_catalyst_id) if is_special else ""
	var cost := maxi(int(session.calculate_attempt_cost()), 0)

	if secondary_id != "" and not has_material(secondary_id):
		return {
			"ok": false,
			"status": STATUS_NO_MATERIAL,
			"slot": "secondary",
			"material_id": secondary_id,
			"cost": cost,
		}
	if catalyst_id != "" and not has_material(catalyst_id):
		return {
			"ok": false,
			"status": STATUS_NO_MATERIAL,
			"slot": "catalyst",
			"material_id": catalyst_id,
			"cost": cost,
		}
	if gold < cost:
		return {
			"ok": false,
			"status": STATUS_NO_GOLD,
			"cost": cost,
			"available_gold": gold,
			"missing_gold": cost - gold,
		}

	return {
		"ok": true,
		"status": STATUS_STARTED,
		"target_level": target_level,
		"cost": cost,
		"secondary_material_id": secondary_id,
		"catalyst_material_id": catalyst_id,
	}


func try_begin_attempt(session, roll_override: float = -1.0, leap_roll_override: float = -1.0) -> Dictionary:
	var transaction := preview_attempt(session)
	if not bool(transaction.get("ok", false)):
		return transaction

	var cost := int(transaction.get("cost", 0))
	var secondary_id := str(transaction.get("secondary_material_id", ""))
	var catalyst_id := str(transaction.get("catalyst_material_id", ""))
	gold -= cost
	_consume_material(secondary_id)
	_consume_material(catalyst_id)

	var started := bool(session.begin_attempt(roll_override, leap_roll_override))
	if not started:
		gold += cost
		_restore_material(secondary_id)
		_restore_material(catalyst_id)
		return {
			"ok": false,
			"status": STATUS_START_FAILED,
			"cost": cost,
		}

	_emit_changed()
	return transaction


func _consume_material(material_id: String) -> void:
	if material_id == "":
		return
	material_stock[material_id] = maxi(get_material_count(material_id) - 1, 0)


func _restore_material(material_id: String) -> void:
	if material_id == "":
		return
	material_stock[material_id] = get_material_count(material_id) + 1


func _normalize_stock() -> void:
	for key_value in material_stock.keys():
		material_stock[key_value] = maxi(int(material_stock[key_value]), 0)


func _emit_changed() -> void:
	changed.emit(snapshot())
