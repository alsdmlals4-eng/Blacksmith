class_name WorkshopCalendar
extends RefCounted

signal changed(snapshot: Dictionary)

const STATUS_OK := "OK"
const STATUS_NO_FATIGUE := "NO_FATIGUE"
const STATUS_UNKNOWN_ACTION := "UNKNOWN_ACTION"

const DEFAULT_CONFIG := {
	"base_fatigue": 20,
	"carryover_ratio": 0.5,
	"action_costs": {
		"forge": 3,
		"normal_enhance": 1,
		"special_enhance": 3,
		"restore": 5,
	},
}

var day: int = 1
var base_fatigue: int = 20
var current_fatigue: int = 20
var carryover: int = 0
var carryover_ratio: float = 0.5
var action_costs: Dictionary = {}


func _init(config: Dictionary = {}) -> void:
	var merged := DEFAULT_CONFIG.duplicate(true)
	for key in config:
		merged[key] = config[key]
	base_fatigue = maxi(int(merged.get("base_fatigue", 20)), 1)
	carryover_ratio = clampf(float(merged.get("carryover_ratio", 0.5)), 0.0, 1.0)
	action_costs = Dictionary(merged.get("action_costs", {})).duplicate(true)
	current_fatigue = base_fatigue


func preview_spend(action_id: String) -> Dictionary:
	if not action_costs.has(action_id):
		return {"ok": false, "status": STATUS_UNKNOWN_ACTION, "action_id": action_id}
	var cost := maxi(int(action_costs[action_id]), 0)
	if current_fatigue < cost:
		return {
			"ok": false,
			"status": STATUS_NO_FATIGUE,
			"action_id": action_id,
			"cost": cost,
			"available": current_fatigue,
			"missing": cost - current_fatigue,
		}
	return {
		"ok": true,
		"status": STATUS_OK,
		"action_id": action_id,
		"cost": cost,
		"available": current_fatigue,
	}


func try_spend(action_id: String) -> Dictionary:
	var preview := preview_spend(action_id)
	if not bool(preview.get("ok", false)):
		return preview
	current_fatigue -= int(preview.get("cost", 0))
	changed.emit(snapshot())
	return preview


func refund(amount: int) -> void:
	if amount <= 0:
		return
	current_fatigue += amount
	changed.emit(snapshot())


func end_day() -> Dictionary:
	carryover = int(floor(float(current_fatigue) * carryover_ratio))
	day += 1
	current_fatigue = base_fatigue + carryover
	changed.emit(snapshot())
	return snapshot()


func snapshot() -> Dictionary:
	return {
		"day": day,
		"current_fatigue": current_fatigue,
		"base_fatigue": base_fatigue,
		"carryover": carryover,
		"carryover_ratio": carryover_ratio,
		"action_costs": action_costs.duplicate(true),
	}
