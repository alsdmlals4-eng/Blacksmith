# 현재 정본의 강화 성공·실패·손상 결과를 해석한다.
class_name VSEnhancementResolver
extends RefCounted

const PrecisionResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")
const CHECKPOINT_FLOORS := [10, 30, 60, 90]
const HARD_GUARANTEE_FAILURES := {"LEARN": 2, "BUILD_CONFIDENCE": 4, "FIRST_STOP_POINT": 4, "TENSION": 5, "HIGH_STAKES": 6, "MASTERY": 7}
const DAMAGE_ANCHORS := [{"target": 11, "percent": 5.0}, {"target": 30, "percent": 6.0}, {"target": 60, "percent": 7.0}, {"target": 90, "percent": 8.0}, {"target": 100, "percent": 10.0}]
const DURABILITY_MODIFIERS := {"NORMAL": {"success_delta_pp": 0.0, "damage_risk_multiplier": 1.0}, "MINOR": {"success_delta_pp": -3.0, "damage_risk_multiplier": 1.25}, "MAJOR": {"success_delta_pp": -7.0, "damage_risk_multiplier": 1.75}}


func band_for_target(target_level: int) -> String:
	if target_level <= 2 and target_level >= 1: return "LEARN"
	if target_level <= 10 and target_level >= 3: return "BUILD_CONFIDENCE"
	if target_level == 11: return "FIRST_STOP_POINT"
	if target_level <= 30 and target_level >= 12: return "TENSION"
	if target_level <= 60 and target_level >= 31: return "HIGH_STAKES"
	if target_level <= 100 and target_level >= 61: return "MASTERY"
	return "INVALID"


func base_success_percent(target_level: int) -> float:
	match target_level:
		1: return 100.0
		2: return 97.0
	if target_level >= 3 and target_level <= 10: return _linear(3, 95.0, 10, 86.0, target_level)
	if target_level == 11: return 82.0
	if target_level <= 30 and target_level >= 12: return _linear(12, 81.0, 30, 72.0, target_level)
	if target_level <= 60 and target_level >= 31: return _linear(31, 73.0, 60, 69.0, target_level)
	if target_level <= 100 and target_level >= 61: return _linear(61, 69.0, 100, 64.0, target_level)
	return 0.0


func gold_attempt_cost(target_level: int) -> int:
	if target_level < 1 or target_level > 100: return 0
	return int(round((12.0 * pow(float(target_level), 1.84)) / 10.0) * 10.0)


func reinforcement_units(target_level: int) -> int:
	return 0 if target_level < 1 or target_level > 100 else int(ceil(float(target_level) / 20.0))


func checkpoint_floor_for_level(level: int) -> int:
	var floor_value := 0
	for checkpoint in CHECKPOINT_FLOORS:
		if level >= checkpoint: floor_value = checkpoint
	return floor_value


func next_checkpoint_after(level: int) -> int:
	for checkpoint in CHECKPOINT_FLOORS:
		if checkpoint > level: return checkpoint
	return 100


func preview(item, target_level: int, precision_selection: Dictionary = {}) -> Dictionary:
	if item == null: return {"allowed": false, "reason": "MISSING_ITEM"}
	if str(item.physical_state) == "DESTROYED": return {"allowed": false, "reason": "ITEM_DESTROYED"}
	if int(item.enhancement_level) >= 100 or target_level > 100: return {"allowed": false, "reason": "MAX_ENHANCEMENT_TERMINAL"}
	if target_level != int(item.enhancement_level) + 1: return {"allowed": false, "reason": "TARGET_LEVEL_MISMATCH"}
	var band := band_for_target(target_level)
	if band == "INVALID": return {"allowed": false, "reason": "INVALID_TARGET_LEVEL"}
	var precision_tag_preview := {}
	if target_level == 10:
		precision_tag_preview = PrecisionResolverScript.new().selection_preview(item, target_level, precision_selection)
		if not bool(precision_tag_preview.get("allowed", false)):
			return {"allowed": false, "reason": str(precision_tag_preview.get("reason", "INVALID_PRECISION_SELECTION"))}
	var state := str(item.effective_durability_state())
	var modifier: Dictionary = DURABILITY_MODIFIERS.get(state, DURABILITY_MODIFIERS["NORMAL"])
	var recovery_failures := int(item.enhancement_recovery_by_target.get(str(target_level), 0))
	var guaranteed := recovery_failures >= int(HARD_GUARANTEE_FAILURES.get(band, 0))
	var base_success := base_success_percent(target_level)
	var recovery_soft_cap := maxf(95.0, base_success)
	var final_success := 100.0 if guaranteed else minf(recovery_soft_cap, base_success + float(modifier["success_delta_pp"]) + recovery_failures * 6)
	var final_damage := 0.0 if guaranteed else _damage_percent(target_level, state)
	var display_success := _round_half_up_one_decimal(final_success)
	var display_damage := _round_half_up_one_decimal(final_damage)
	return {"allowed": true, "reason": "", "target_level": target_level, "band": band, "effective_durability_state": state, "base_success_percent": base_success_percent(target_level), "recovery_failures": recovery_failures, "recovery_bonus_pp": recovery_failures * 6, "guaranteed": guaranteed, "final_success_percent": final_success, "final_damage_percent": final_damage, "display_outcomes": {"success_percent": display_success, "failed_damage_percent": display_damage, "failed_hold_percent": maxf(0.0, 100.0 - display_success - display_damage)}, "gold_cost": gold_attempt_cost(target_level), "reinforcement_units": reinforcement_units(target_level), "checkpoint_floor": checkpoint_floor_for_level(int(item.enhancement_level)), "next_checkpoint": next_checkpoint_after(int(item.enhancement_level)), "precision_tag_preview": precision_tag_preview}


func resolve_with_rolls(item, target_level: int, rolls: Dictionary, precision_selection: Dictionary = {}) -> Dictionary:
	var attempt := preview(item, target_level, precision_selection)
	if not bool(attempt.get("allowed", false)): return {"outcome": "BLOCKED", "reason": str(attempt.get("reason", "INVALID_ATTEMPT"))}
	if bool(attempt["guaranteed"]) or float(rolls.get("success_roll_percent", 0.0)) < float(attempt["final_success_percent"]):
		var precision_result := {}
		if target_level == 10:
			precision_result = PrecisionResolverScript.new().apply_selection_success(item, precision_selection)
			if not bool(precision_result.get("applied", false)):
				return {"outcome": "BLOCKED", "reason": str(precision_result.get("reason", "INVALID_PRECISION_SELECTION"))}
		_apply_success(item, target_level)
		return {"outcome": "SUCCESS", "target_level": target_level, "band": str(attempt["band"]), "precision_tag_id": str(precision_result.get("tag_id", "")), "precision_effect_axis": str(precision_result.get("effect_axis", "")), "precision_effect_delta": int(precision_result.get("effect_delta", 0))}
	var recovery_key := str(target_level)
	item.enhancement_recovery_by_target[recovery_key] = int(item.enhancement_recovery_by_target.get(recovery_key, 0)) + 1
	if float(rolls.get("damage_roll_percent", 100.0)) < float(attempt["final_damage_percent"]):
		item.apply_damage_event()
		return {"outcome": "FAILED_DAMAGE", "target_level": target_level, "recovery_failures": int(item.enhancement_recovery_by_target[recovery_key]), "physical_state": str(item.physical_state)}
	return {"outcome": "FAILED_HOLD", "target_level": target_level, "recovery_failures": int(item.enhancement_recovery_by_target[recovery_key]), "physical_state": str(item.physical_state)}


func _apply_success(item, target_level: int) -> void:
	item.enhancement_level = target_level
	if CHECKPOINT_FLOORS.has(target_level): item.highest_checkpoint = target_level
	item.enhancement_recovery_by_target.erase(str(target_level))
	if target_level == 100: item.max_enhancement_reached = true


func _damage_percent(target_level: int, state: String) -> float:
	if target_level <= 10: return 0.0
	return _base_damage_percent(target_level) * float(DURABILITY_MODIFIERS.get(state, DURABILITY_MODIFIERS["NORMAL"])["damage_risk_multiplier"])


func _base_damage_percent(target_level: int) -> float:
	for index in range(DAMAGE_ANCHORS.size() - 1):
		var left: Dictionary = DAMAGE_ANCHORS[index]
		var right: Dictionary = DAMAGE_ANCHORS[index + 1]
		if target_level >= int(left["target"]) and target_level <= int(right["target"]): return _linear(int(left["target"]), float(left["percent"]), int(right["target"]), float(right["percent"]), target_level)
	return 0.0


func _round_half_up_one_decimal(value: float) -> float:
	return floor(value * 10.0 + 0.5) / 10.0


func _linear(x0: int, y0: float, x1: int, y1: float, x: int) -> float:
	return y0 + (y1 - y0) * (float(x - x0) / float(x1 - x0))
