class_name VSPrecisionResolver
extends RefCounted

const PRECISION_MILESTONES := [10]
const METHOD_OUTPUTS := {
	"EDGE_REINFORCEMENT": {
		"output_lane": "STAT_METHOD",
		"changed_axis": "ATTACK",
		"delta": 5,
	},
	"SHOCK_ABSORPTION": {
		"output_lane": "STAT_METHOD",
		"changed_axis": "DEFENSE",
		"delta": 5,
	},
	"BALANCE_TUNING": {
		"output_lane": "STAT_METHOD",
		"changed_axis": "HANDLING",
		"delta": 5,
	},
	"ARTISTIC_FINISH": {
		"output_lane": "STAT_METHOD",
		"changed_axis": "ARTISTRY",
		"delta": 5,
	},
	"LIGHTWEIGHTING": {
		"output_lane": "STAT_METHOD",
		"changed_axis": "CURRENT_WEIGHT",
		"delta": -5,
	},
	"WEIGHTING": {
		"output_lane": "STAT_METHOD",
		"changed_axis": "CURRENT_WEIGHT",
		"delta": 5,
	},
	"ENVIRONMENTAL_TREATMENT": {
		"output_lane": "FUNCTION_REWORK",
		"changed_axis": "FUNCTION",
		"delta": 0,
	},
}


func preview(item, milestone: int, method_id: String, catalyst_id: String, context) -> Dictionary:
	if item == null:
		return _blocked("MISSING_ITEM")
	if context == null:
		return _blocked("MISSING_CONTEXT")
	if not context.validation_errors.is_empty():
		return _blocked("INVALID_CONTEXT")
	if str(item.physical_state) == "DESTROYED":
		return _blocked("ITEM_DESTROYED")
	if not PRECISION_MILESTONES.has(milestone):
		return _blocked("INVALID_PRECISION_MILESTONE")
	if int(item.enhancement_level) < milestone:
		return _blocked("MILESTONE_NOT_REACHED")
	if item.used_precision_milestones.has(milestone):
		return _blocked("PRECISION_MILESTONE_ALREADY_USED")
	if not METHOD_OUTPUTS.has(method_id):
		return _blocked("UNKNOWN_PRECISION_METHOD")

	var method: Dictionary = METHOD_OUTPUTS[method_id]
	var delta := int(method["delta"])
	var current_weight := int(item.weight_point)
	var result_weight := current_weight
	if str(method["changed_axis"]) == "CURRENT_WEIGHT":
		result_weight = maxi(0, current_weight + delta)

	return {
		"allowed": true,
		"reason": "OK",
		"milestone": milestone,
		"method_id": method_id,
		"output_lane": str(method["output_lane"]),
		"changed_axis": str(method["changed_axis"]),
		"delta": delta,
		"result_weight": result_weight,
		"context_relation": _context_relation(method_id, current_weight, result_weight, context),
		"catalyst_id": catalyst_id,
		"customer_bonus_from_catalyst_selection_pp": 0,
		"customer_bonus_granted_by_catalyst_selection": false,
	}


func _context_relation(method_id: String, current_weight: int, result_weight: int, context) -> String:
	if method_id == "LIGHTWEIGHTING":
		var maximum_load := int(context.maximum_load())
		if current_weight > maximum_load and result_weight <= maximum_load:
			return "GATE_CHANGE"
		if context.relevant_precision_axes.has("WEIGHT"):
			return "DIRECTLY_RELEVANT"
	if method_id == "WEIGHTING" and context.relevant_precision_axes.has("WEIGHT"):
		return "TRADE_OFF"
	return "NOT_DIRECTLY_RELEVANT"


func _blocked(reason: String) -> Dictionary:
	return {
		"allowed": false,
		"reason": reason,
		"customer_bonus_from_catalyst_selection_pp": 0,
		"customer_bonus_granted_by_catalyst_selection": false,
	}
