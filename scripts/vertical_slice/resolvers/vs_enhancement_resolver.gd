class_name VSEnhancementResolver
extends RefCounted

const CHECKPOINT_FLOORS := [10, 30, 60, 90]
const HARD_GUARANTEE_FAILURES := {
	"LEARN": 2,
	"BUILD_CONFIDENCE": 4,
	"FIRST_STOP_POINT": 4,
	"TENSION": 5,
	"HIGH_STAKES": 6,
	"MASTERY": 7,
}
const FAILURE_FAMILY_RATIOS := {
	"LEARN": {"HOLD": 100, "DOWNGRADE": 0, "DAMAGE": 0, "CRITICAL": 0},
	"BUILD_CONFIDENCE": {"HOLD": 90, "DOWNGRADE": 0, "DAMAGE": 10, "CRITICAL": 0},
	"FIRST_STOP_POINT": {"HOLD": 65, "DOWNGRADE": 10, "DAMAGE": 23, "CRITICAL": 2},
	"TENSION": {"HOLD": 45, "DOWNGRADE": 10, "DAMAGE": 35, "CRITICAL": 10},
	"HIGH_STAKES": {"HOLD": 30, "DOWNGRADE": 15, "DAMAGE": 39, "CRITICAL": 16},
	"MASTERY": {"HOLD": 20, "DOWNGRADE": 20, "DAMAGE": 40, "CRITICAL": 20},
}


func band_for_target(target_level: int) -> String:
	if target_level >= 1 and target_level <= 2:
		return "LEARN"
	if target_level >= 3 and target_level <= 10:
		return "BUILD_CONFIDENCE"
	if target_level == 11:
		return "FIRST_STOP_POINT"
	if target_level >= 12 and target_level <= 30:
		return "TENSION"
	if target_level >= 31 and target_level <= 60:
		return "HIGH_STAKES"
	if target_level >= 61 and target_level <= 100:
		return "MASTERY"
	return "INVALID"


func base_success_percent(target_level: int) -> float:
	match target_level:
		1:
			return 100.0
		2:
			return 97.0
	if target_level >= 3 and target_level <= 10:
		return _linear(3, 95.0, 10, 86.0, target_level)
	if target_level == 11:
		return 82.0
	if target_level >= 12 and target_level <= 30:
		return _linear(12, 81.0, 30, 72.0, target_level)
	if target_level >= 31 and target_level <= 60:
		return _linear(31, 73.0, 60, 69.0, target_level)
	if target_level >= 61 and target_level <= 100:
		return _linear(61, 69.0, 100, 64.0, target_level)
	return 0.0


func gold_attempt_cost(target_level: int) -> int:
	if target_level < 1 or target_level > 100:
		return 0
	var raw_cost := 12.0 * pow(float(target_level), 1.84)
	return int(round(raw_cost / 10.0) * 10.0)


func reinforcement_units(target_level: int) -> int:
	if target_level < 1 or target_level > 100:
		return 0
	return int(ceil(float(target_level) / 20.0))


func failure_family_ratio(band: String) -> Dictionary:
	return FAILURE_FAMILY_RATIOS.get(band, {}).duplicate(true)


func max_durability_penalty_pp(max_durability: int) -> int:
	if max_durability >= 81:
		return 0
	if max_durability >= 61:
		return -3
	if max_durability >= 41:
		return -6
	if max_durability >= 21:
		return -10
	if max_durability >= 1:
		return -15
	return 0


func checkpoint_floor_for_level(level: int) -> int:
	var floor_value := 0
	for checkpoint in CHECKPOINT_FLOORS:
		if level >= checkpoint:
			floor_value = checkpoint
	return floor_value


func next_checkpoint_after(level: int) -> int:
	for checkpoint in CHECKPOINT_FLOORS:
		if checkpoint > level:
			return checkpoint
	return 100


func preview(item, target_level: int) -> Dictionary:
	if item == null:
		return {"allowed": false, "reason": "MISSING_ITEM"}
	if str(item.physical_state) == "DESTROYED":
		return {"allowed": false, "reason": "ITEM_DESTROYED"}
	if int(item.enhancement_level) >= 100 or target_level > 100:
		return {"allowed": false, "reason": "MAX_ENHANCEMENT_TERMINAL"}
	if target_level != int(item.enhancement_level) + 1:
		return {"allowed": false, "reason": "TARGET_LEVEL_MISMATCH"}

	var band := band_for_target(target_level)
	if band == "INVALID":
		return {"allowed": false, "reason": "INVALID_TARGET_LEVEL"}

	var recovery_failures := int(item.enhancement_recovery_by_target.get(str(target_level), 0))
	var recovery_bonus_pp := recovery_failures * 6
	var hard_guarantee_count := int(HARD_GUARANTEE_FAILURES.get(band, 0))
	var guaranteed := hard_guarantee_count > 0 and recovery_failures >= hard_guarantee_count
	var max_penalty_pp := max_durability_penalty_pp(int(item.max_durability))
	var final_success_percent: float = 100.0 if guaranteed else minf(
		95.0,
		base_success_percent(target_level) + float(recovery_bonus_pp + max_penalty_pp)
	)

	return {
		"allowed": true,
		"reason": "",
		"target_level": target_level,
		"band": band,
		"base_success_percent": base_success_percent(target_level),
		"max_penalty_pp": max_penalty_pp,
		"recovery_failures": recovery_failures,
		"recovery_bonus_pp": recovery_bonus_pp,
		"guaranteed": guaranteed,
		"final_success_percent": final_success_percent,
		"gold_cost": gold_attempt_cost(target_level),
		"reinforcement_units": reinforcement_units(target_level),
		"checkpoint_floor": checkpoint_floor_for_level(int(item.enhancement_level)),
		"next_checkpoint": next_checkpoint_after(int(item.enhancement_level)),
		"failure_family_ratio": failure_family_ratio(band),
	}


func _linear(x0: int, y0: float, x1: int, y1: float, x: int) -> float:
	var t := float(x - x0) / float(x1 - x0)
	return y0 + (y1 - y0) * t
