class_name VSCustomerContextResolver
extends RefCounted


func evaluate(_customer, item, context) -> Dictionary:
	if item == null:
		return _blocked("MISSING_ITEM")
	if context == null:
		return _blocked("MISSING_CONTEXT")

	var maximum_load := int(context.maximum_load())
	var current_weight := int(item.weight_point)
	if current_weight > maximum_load:
		return _blocked("OVERWEIGHT", maximum_load, current_weight)

	var required_function := str(context.required_function_if_explicit)
	if not required_function.is_empty() and not item.functions.has(required_function):
		return _blocked("REQUIRED_FUNCTION_MISSING", maximum_load, current_weight)

	var risk_base := clampi(100 - int(context.risk) * 10, 5, 90)
	var enhancement_pp := enhancement_contribution_pp(int(item.enhancement_level))
	var related_ability_pp := 5 if int(context.related_ability_value()) >= int(context.risk) else 0
	var proficiency_pp := proficiency_modifier_pp(int(context.weapon_proficiency))
	var final_primary_estimate := clampi(
		risk_base + enhancement_pp + related_ability_pp + proficiency_pp,
		5,
		95
	)
	return {
		"status": "EVALUATED",
		"assignment_allowed": true,
		"reason": "OK",
		"estimate_available": true,
		"maximum_load": maximum_load,
		"current_weight": current_weight,
		"risk_base": risk_base,
		"enhancement_contribution_pp": enhancement_pp,
		"related_ability_modifier_pp": related_ability_pp,
		"proficiency_modifier_pp": proficiency_pp,
		"final_primary_estimate": final_primary_estimate,
	}


func enhancement_contribution_pp(enhancement_level: int) -> int:
	return roundi(0.30 * float(enhancement_level))


func proficiency_modifier_pp(proficiency_level: int) -> int:
	match proficiency_level:
		0:
			return -10
		1:
			return 0
		2:
			return 5
		3:
			return 10
		_:
			return 0


func _blocked(reason: String, maximum_load: int = 0, current_weight: int = 0) -> Dictionary:
	return {
		"status": "BLOCKED",
		"assignment_allowed": false,
		"reason": reason,
		"estimate_available": false,
		"maximum_load": maximum_load,
		"current_weight": current_weight,
	}
