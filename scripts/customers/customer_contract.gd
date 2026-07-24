class_name CustomerContract
extends RefCounted

const STATUS_OK := "OK"
const STATUS_WRONG_EQUIPMENT := "WRONG_EQUIPMENT"
const STATUS_DESTROYED := "DESTROYED"
const STATUS_REQUIREMENT_NOT_MET := "REQUIREMENT_NOT_MET"
const STATUS_DEADLINE_EXPIRED := "DEADLINE_EXPIRED"

var config: Dictionary = {}
var activity_config: Dictionary = {}
var accepted_day: int = 1


func _init(contract_config: Dictionary = {}, result_config: Dictionary = {}, start_day: int = 1) -> void:
	config = contract_config.duplicate(true)
	activity_config = result_config.duplicate(true)
	accepted_day = maxi(start_day, 1)


func can_deliver(equipment: Dictionary, day: int) -> Dictionary:
	var missing: Array[String] = []
	if str(equipment.get("weapon_id", equipment.get("equipment_id", ""))) != str(config.get("equipment_id", "iron_sword")):
		missing.append(STATUS_WRONG_EQUIPMENT)
	if bool(equipment.get("destroyed", false)) or str(equipment.get("lifecycle_state", "")) == "BROKEN_OR_LOST":
		missing.append(STATUS_DESTROYED)
	if int(equipment.get("enhancement_level", 0)) < int(config.get("required_level", 5)):
		missing.append(STATUS_REQUIREMENT_NOT_MET)
	if remaining_days(day) < 0:
		missing.append(STATUS_DEADLINE_EXPIRED)
	return {
		"ok": missing.is_empty(),
		"status": STATUS_OK if missing.is_empty() else missing[0],
		"missing_conditions": missing,
		"remaining_days": remaining_days(day),
	}


func evaluate_fit(equipment: Dictionary) -> Dictionary:
	var weights: Dictionary = activity_config.get("score_weights", {})
	var level := int(equipment.get("enhancement_level", 0))
	var affix_ids := _affix_ids(equipment.get("affixes", []))
	var contributions := {
		"required_level": int(weights.get("required_level", 0)) if level >= int(config.get("required_level", 5)) else 0,
		"stretch_level": int(weights.get("stretch_level", 0)) if level >= int(config.get("stretch_level", 10)) else 0,
		"preferred_affix": int(weights.get("preferred_affix", 0)) if _has_preferred_affix(affix_ids) else 0,
		"grade": int(Dictionary(activity_config.get("grade_scores", {})).get(str(equipment.get("craftsmanship_grade_id", "STANDARD")), 0)),
		"attack": int(weights.get("attack", 0)) if int(equipment.get("progression_attack", equipment.get("base_attack", 0))) >= int(weights.get("attack_threshold", 20)) else 0,
	}
	var score := 0
	for value in contributions.values():
		score += int(value)
	var band_id := _band_for_score(score)
	return {
		"score": score,
		"band_id": band_id,
		"contributions": contributions,
		"effective_choices": _effective_choices(contributions),
		"missing_conditions": _missing_fit_conditions(contributions),
	}


func remaining_days(day: int) -> int:
	return accepted_day + int(config.get("deadline_days", 3)) - day


func _band_for_score(score: int) -> String:
	var selected := ""
	for band_value in activity_config.get("result_bands", []):
		var band: Dictionary = band_value
		if score >= int(band.get("minimum_score", 0)):
			selected = str(band.get("id", ""))
	return selected


func _has_preferred_affix(affix_ids: Array[String]) -> bool:
	for preferred in config.get("preferred_affix_ids", []):
		if affix_ids.has(str(preferred)):
			return true
	return false


func _affix_ids(values: Array) -> Array[String]:
	var ids: Array[String] = []
	for value in values:
		if value is Dictionary:
			ids.append(str(value.get("id", value.get("affix_id", ""))))
		else:
			ids.append(str(value))
	return ids


func _effective_choices(contributions: Dictionary) -> Array[String]:
	var result: Array[String] = []
	for key in contributions:
		if int(contributions[key]) > 0:
			result.append(str(key))
	return result


func _missing_fit_conditions(contributions: Dictionary) -> Array[String]:
	var result: Array[String] = []
	for key in contributions:
		if int(contributions[key]) <= 0:
			result.append(str(key))
	return result
