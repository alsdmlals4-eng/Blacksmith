class_name EnhancementSession
extends RefCounted

signal changed(snapshot: Dictionary)
signal state_changed(new_state: int)
signal attempt_resolved(result: Dictionary)
signal completed(result: Dictionary)

enum State {
	READY,
	PRECISION,
	COMPLETE,
}

const DEFAULT_CONFIG := {
	"max_level": 100,
	"precision_interval": 10,
	"material_interval": 10,
	"base_success_by_target_level": {},
	"base_success_pattern_by_cycle_position": {
		"1": 0.98,
		"2": 0.95,
		"3": 0.92,
		"4": 0.89,
		"5": 0.86,
		"6": 0.83,
		"7": 0.80,
		"8": 0.77,
		"9": 0.74,
		"10": 0.68,
	},
	"decade_penalty": 0.025,
	"max_decade_penalty": 0.25,
	"minimum_base_success": 0.25,
	"milestones": [],
	"precision": {
		"speed": 0.9,
		"target": 0.5,
		"perfect_radius": 0.07,
		"good_radius": 0.18,
		"perfect_success_bonus": 0.2,
		"good_success_bonus": 0.1,
	},
	"pity": {
		"bonus_per_failure": 0.04,
		"max_bonus": 0.24,
	},
	"growth": {
		"base_attack": 10,
		"normal_rate": 0.08,
		"normal_rate_per_decade": 0.01,
		"special_rate": 0.20,
		"special_rate_per_decade": 0.02,
	},
	"economy": {
		"base_weapon_price": 100,
		"attack_price_scale": 12.0,
		"attack_price_exponent": 1.18,
		"level_price_scale": 4.0,
		"level_price_exponent": 1.65,
		"base_attempt_cost": 25,
		"attempt_cost_exponent": 1.55,
		"attempt_decade_multiplier": 0.22,
		"special_cost_multiplier": 2.4,
	},
	"risk": {
		"safe_until_level": 10,
		"destroy_start_level": 30,
		"special_downgrade_multiplier": 1.15,
		"special_destroy_multiplier": 1.25,
		"downgrade_ratio_by_decade": {},
		"destroy_ratio_by_decade": {},
		"downgrade_steps_by_decade": {},
	},
	"skills": {
		"balanced": {
			"name": "균형 단조",
			"description": "추가 보정 없이 기본 확률·비용·위험을 사용합니다.",
			"success_bonus": 0.0,
			"cost_multiplier": 1.0,
			"growth_multiplier": 1.0,
			"sale_value_bonus": 0.0,
			"downgrade_multiplier": 1.0,
			"destroy_multiplier": 1.0,
			"precision_bonus_multiplier": 1.0,
		},
	},
	"material_scoring": {
		"secondary_tag_weight": 2,
		"catalyst_tag_weight": 1,
	},
}

var config: Dictionary = {}
var material_by_id: Dictionary = {}
var affix_by_id: Dictionary = {}
var rng := RandomNumberGenerator.new()

var state: int = State.READY
var weapon_id: String = "iron_sword"
var base_weapon_name: String = "철검"
var enhancement_level: int = 0
var affixes: Array[Dictionary] = []
var selected_secondary_id: String = "whetstone"
var selected_catalyst_id: String = ""
var selected_skill_id: String = "balanced"
var precision_position: float = 0.0
var precision_direction: float = 1.0
var material_scores: Dictionary = {}
var lifetime_material_scores: Dictionary = {}
var last_secondary_tag: String = ""
var failure_streak: int = 0
var total_attempts: int = 0
var total_failures: int = 0
var total_spent: int = 0
var last_attempt: Dictionary = {}
var pending_roll_override: float = -1.0
var pending_attempt_cost: int = 0
var destroyed: bool = false

var base_attack: int = 10
var progression_attack: int = 10
var attack_history: Dictionary = {}
var value_bonus_total: float = 0.0
var value_bonus_history: Dictionary = {}
var catalyst_history: Array[Dictionary] = []


func _init(
	custom_config: Dictionary = {},
	materials: Array = [],
	affix_definitions: Array = [],
	weapon: Dictionary = {}
) -> void:
	config = DEFAULT_CONFIG.duplicate(true)
	_merge_config(custom_config)
	_index_materials(materials)
	_index_affixes(affix_definitions)
	weapon_id = str(weapon.get("weapon_id", "iron_sword"))
	base_weapon_name = str(weapon.get("weapon_name", "철검"))
	base_attack = int(weapon.get("base_attack", config.get("growth", {}).get("base_attack", 10)))
	progression_attack = base_attack
	attack_history["0"] = progression_attack
	value_bonus_history["0"] = 0.0
	rng.randomize()


func set_secondary_material(material_id: String) -> bool:
	if state != State.READY or not uses_materials_for_level(enhancement_level + 1):
		return false
	if not _material_supports_slot(material_id, "secondary"):
		return false
	selected_secondary_id = material_id
	_emit_changed()
	return true


func set_catalyst_material(material_id: String) -> bool:
	if state != State.READY or not uses_materials_for_level(enhancement_level + 1):
		return false
	if material_id != "" and not _material_supports_slot(material_id, "catalyst"):
		return false
	selected_catalyst_id = material_id
	_emit_changed()
	return true


func set_skill(skill_id: String) -> bool:
	if state != State.READY:
		return false
	var skills: Dictionary = config.get("skills", {})
	if not skills.has(skill_id):
		return false
	selected_skill_id = skill_id
	_emit_changed()
	return true


func begin_attempt(roll_override: float = -1.0) -> bool:
	if state != State.READY or enhancement_level >= int(config["max_level"]) or destroyed:
		return false
	var target_level := enhancement_level + 1
	total_attempts += 1
	pending_attempt_cost = calculate_attempt_cost()
	total_spent += pending_attempt_cost
	pending_roll_override = roll_override
	if uses_materials_for_level(target_level):
		_consume_material_traits()
	if requires_precision_for_level(target_level):
		state = State.PRECISION
		precision_position = 0.0
		precision_direction = 1.0
		state_changed.emit(state)
		_emit_changed()
	else:
		_resolve_attempt("ONE_CLICK", "원클릭 강화", 0.0)
	return true


func advance(delta: float) -> void:
	if delta <= 0.0 or state != State.PRECISION:
		return
	var precision: Dictionary = config["precision"]
	precision_position += precision_direction * float(precision["speed"]) * delta
	while precision_position > 1.0 or precision_position < 0.0:
		if precision_position > 1.0:
			precision_position = 2.0 - precision_position
			precision_direction = -1.0
		elif precision_position < 0.0:
			precision_position = -precision_position
			precision_direction = 1.0
	_emit_changed()


func finish_precision() -> Dictionary:
	if state != State.PRECISION:
		return {}
	var precision: Dictionary = config["precision"]
	var distance := absf(precision_position - float(precision["target"]))
	var quality_id := "STANDARD"
	var quality_label := "보통 정밀 강화"
	var success_bonus := 0.0
	if distance <= float(precision["perfect_radius"]):
		quality_id = "PERFECT"
		quality_label = "완벽한 정밀 강화"
		success_bonus = float(precision["perfect_success_bonus"])
	elif distance <= float(precision["good_radius"]):
		quality_id = "GOOD"
		quality_label = "좋은 정밀 강화"
		success_bonus = float(precision["good_success_bonus"])
	_resolve_attempt(quality_id, quality_label, success_bonus)
	return last_attempt.duplicate(true)


func requires_precision_for_level(target_level: int) -> bool:
	var interval := maxi(int(config.get("precision_interval", 10)), 1)
	return target_level > 0 and target_level % interval == 0


func uses_materials_for_level(target_level: int) -> bool:
	var interval := maxi(int(config.get("material_interval", 10)), 1)
	return target_level > 0 and target_level % interval == 0


func calculate_success_chance(precision_bonus: float = 0.0) -> float:
	var target_level := enhancement_level + 1
	var base_chance := _base_success_chance(target_level)
	var catalyst_bonus := _selected_catalyst_bonus() if uses_materials_for_level(target_level) else 0.0
	var skill := _selected_skill()
	var precision_multiplier := float(skill.get("precision_bonus_multiplier", 1.0))
	var skill_bonus := float(skill.get("success_bonus", 0.0))
	return clampf(
		base_chance + catalyst_bonus + _current_pity_bonus() + skill_bonus + precision_bonus * precision_multiplier,
		0.0,
		1.0
	)


func calculate_outcome_probabilities(precision_bonus: float = 0.0) -> Dictionary:
	var target_level := enhancement_level + 1
	var success := calculate_success_chance(precision_bonus)
	var failure := maxf(1.0 - success, 0.0)
	var destroy_conditional := _conditional_destroy_ratio(target_level)
	var downgrade_conditional := _conditional_downgrade_ratio(target_level)
	var destroy_chance := failure * destroy_conditional
	var downgrade_chance := failure * (1.0 - destroy_conditional) * downgrade_conditional
	var hold_chance := maxf(failure - destroy_chance - downgrade_chance, 0.0)
	return {
		"success": success,
		"hold": hold_chance,
		"downgrade": downgrade_chance,
		"destroy": destroy_chance,
		"downgrade_steps": _downgrade_steps(target_level),
	}


func calculate_growth_gain(target_level: int = -1) -> int:
	if target_level < 0:
		target_level = enhancement_level + 1
	var growth: Dictionary = config.get("growth", {})
	var decade := maxi((target_level - 1) / 10, 0)
	var is_special := uses_materials_for_level(target_level)
	var rate := float(growth.get("normal_rate", 0.08)) + float(decade) * float(growth.get("normal_rate_per_decade", 0.01))
	if is_special:
		rate = float(growth.get("special_rate", 0.20)) + float(decade) * float(growth.get("special_rate_per_decade", 0.02))
	var multiplier := float(_selected_skill().get("growth_multiplier", 1.0))
	if is_special:
		multiplier *= float(_selected_catalyst().get("growth_multiplier", 1.0))
	return maxi(int(ceil(float(progression_attack) * rate * multiplier)), 1)


func calculate_attempt_cost() -> int:
	var target_level := enhancement_level + 1
	var economy: Dictionary = config.get("economy", {})
	var decade := maxi((target_level - 1) / 10, 0)
	var cost := float(economy.get("base_attempt_cost", 25))
	cost *= pow(float(target_level), float(economy.get("attempt_cost_exponent", 1.55)))
	cost *= 1.0 + float(decade) * float(economy.get("attempt_decade_multiplier", 0.22))
	if uses_materials_for_level(target_level):
		cost *= float(economy.get("special_cost_multiplier", 2.4))
		cost += float(_selected_secondary().get("price", 0))
		cost += float(_selected_catalyst().get("price", 0))
	cost *= float(_selected_skill().get("cost_multiplier", 1.0))
	return maxi(int(round(cost)), 1)


func get_current_final_attack() -> int:
	return _apply_affix_attack(progression_attack, affixes)


func get_current_sale_price() -> int:
	return _calculate_sale_price(enhancement_level, get_current_final_attack(), affixes, value_bonus_total)


func get_next_preview() -> Dictionary:
	if destroyed or enhancement_level >= int(config["max_level"]):
		return {}
	var target_level := enhancement_level + 1
	var gain := calculate_growth_gain(target_level)
	var next_progression_attack := progression_attack + gain
	var next_affixes := _preview_affixes_after_success(target_level)
	var next_final_attack := _apply_affix_attack(next_progression_attack, next_affixes)
	var next_value_bonus := value_bonus_total
	if uses_materials_for_level(target_level):
		next_value_bonus += float(_selected_catalyst().get("sale_value_bonus", 0.0))
		next_value_bonus += float(_selected_skill().get("sale_value_bonus", 0.0))
	var next_price := _calculate_sale_price(target_level, next_final_attack, next_affixes, next_value_bonus)
	return {
		"target_level": target_level,
		"growth_gain": gain,
		"growth_percent": float(gain) / maxf(float(progression_attack), 1.0),
		"progression_attack": next_progression_attack,
		"final_attack": next_final_attack,
		"sale_price": next_price,
		"sale_price_gain": next_price - get_current_sale_price(),
		"attempt_cost": calculate_attempt_cost(),
		"affixes": next_affixes,
		"value_bonus": next_value_bonus,
	}


func snapshot() -> Dictionary:
	var target_level := mini(enhancement_level + 1, int(config["max_level"]))
	return {
		"state": state,
		"weapon_id": weapon_id,
		"base_weapon_name": base_weapon_name,
		"display_name": get_display_name(),
		"enhancement_level": enhancement_level,
		"max_level": int(config["max_level"]),
		"progress_ratio": float(enhancement_level) / float(config["max_level"]),
		"target_level": target_level,
		"requires_precision": requires_precision_for_level(target_level),
		"uses_materials": uses_materials_for_level(target_level),
		"selected_secondary_id": selected_secondary_id,
		"selected_catalyst_id": selected_catalyst_id,
		"selected_skill_id": selected_skill_id,
		"selected_secondary": _selected_secondary().duplicate(true),
		"selected_catalyst": _selected_catalyst().duplicate(true),
		"selected_skill": _selected_skill().duplicate(true),
		"precision_position": precision_position,
		"base_success_chance": calculate_success_chance(),
		"outcome_probabilities": calculate_outcome_probabilities(),
		"failure_streak": failure_streak,
		"pity_bonus": _current_pity_bonus(),
		"material_scores": material_scores.duplicate(true),
		"lifetime_material_scores": lifetime_material_scores.duplicate(true),
		"milestone_preview": _get_milestone_preview(),
		"affixes": affixes.duplicate(true),
		"base_attack": base_attack,
		"progression_attack": progression_attack,
		"enhancement_bonus": progression_attack - base_attack,
		"final_attack": get_current_final_attack(),
		"sale_price": get_current_sale_price(),
		"attempt_cost": calculate_attempt_cost() if not destroyed and enhancement_level < int(config["max_level"]) else 0,
		"next_preview": get_next_preview(),
		"value_bonus_total": value_bonus_total,
		"catalyst_history": catalyst_history.duplicate(true),
		"total_attempts": total_attempts,
		"total_failures": total_failures,
		"total_spent": total_spent,
		"destroyed": destroyed,
		"last_attempt": last_attempt.duplicate(true),
	}


func get_display_name() -> String:
	if destroyed:
		return "파괴된 %s" % base_weapon_name
	var names: Array[String] = []
	for index in range(affixes.size() - 1, -1, -1):
		var affix: Dictionary = affixes[index]
		names.append(str(affix.get("name", "")))
	var prefix := "%s " % " ".join(names) if not names.is_empty() else ""
	return "%s%s +%d" % [prefix, base_weapon_name, enhancement_level]


func _resolve_attempt(precision_id: String, precision_label: String, precision_bonus: float) -> void:
	var target_level := enhancement_level + 1
	var probabilities := calculate_outcome_probabilities(precision_bonus)
	var roll := pending_roll_override if pending_roll_override >= 0.0 else rng.randf()
	pending_roll_override = -1.0
	var success_limit := float(probabilities["success"])
	var destroy_limit := success_limit + float(probabilities["destroy"])
	var downgrade_limit := destroy_limit + float(probabilities["downgrade"])
	var outcome := "HOLD"
	if roll < success_limit:
		outcome = "SUCCESS"
	elif roll < destroy_limit:
		outcome = "DESTROY"
	elif roll < downgrade_limit:
		outcome = "DOWNGRADE"

	var previous_level := enhancement_level
	var growth_gain := 0
	var milestone := _milestone_for_level(target_level)
	var material_stage := uses_materials_for_level(target_level)
	var downgrade_steps := 0

	match outcome:
		"SUCCESS":
			growth_gain = calculate_growth_gain(target_level)
			progression_attack += growth_gain
			enhancement_level = target_level
			attack_history[str(enhancement_level)] = progression_attack
			failure_streak = 0
			if not milestone.is_empty():
				_apply_milestone(milestone)
			if material_stage:
				_apply_success_value_bonus(target_level)
			value_bonus_history[str(enhancement_level)] = value_bonus_total
		"DOWNGRADE":
			downgrade_steps = _downgrade_steps(target_level)
			enhancement_level = maxi(enhancement_level - downgrade_steps, 0)
			_restore_progress_to_level(enhancement_level)
			_rollback_affixes_to_level(enhancement_level)
			failure_streak += 1
			total_failures += 1
		"DESTROY":
			destroyed = true
			enhancement_level = 0
			progression_attack = 0
			affixes.clear()
			failure_streak += 1
			total_failures += 1
		_:
			failure_streak += 1
			total_failures += 1

	if outcome != "SUCCESS" and material_stage:
		material_scores.clear()
		last_secondary_tag = ""

	last_attempt = {
		"success": outcome == "SUCCESS",
		"outcome": outcome,
		"target_level": target_level,
		"previous_level": previous_level,
		"result_level": enhancement_level,
		"growth_gain": growth_gain,
		"downgrade_steps": downgrade_steps,
		"success_chance": float(probabilities["success"]),
		"hold_chance": float(probabilities["hold"]),
		"downgrade_chance": float(probabilities["downgrade"]),
		"destroy_chance": float(probabilities["destroy"]),
		"roll": roll,
		"precision_id": precision_id,
		"precision_label": precision_label,
		"precision_bonus": precision_bonus,
		"precision_required": requires_precision_for_level(target_level),
		"uses_materials": material_stage,
		"attempt_cost": pending_attempt_cost,
		"milestone": milestone.duplicate(true),
		"secondary_material_id": selected_secondary_id if material_stage else "",
		"catalyst_material_id": selected_catalyst_id if material_stage else "",
		"skill_id": selected_skill_id,
		"affixes": affixes.duplicate(true),
	}
	pending_attempt_cost = 0

	if destroyed or (outcome == "SUCCESS" and enhancement_level >= int(config["max_level"])):
		state = State.COMPLETE
		last_attempt["final_weapon"] = {
			"weapon_id": weapon_id,
			"weapon_name": get_display_name(),
			"enhancement_level": enhancement_level,
			"affixes": affixes.duplicate(true),
			"destroyed": destroyed,
			"final_attack": get_current_final_attack(),
			"sale_price": get_current_sale_price(),
		}
		state_changed.emit(state)
		attempt_resolved.emit(last_attempt.duplicate(true))
		completed.emit(last_attempt["final_weapon"].duplicate(true))
	else:
		state = State.READY
		state_changed.emit(state)
		attempt_resolved.emit(last_attempt.duplicate(true))
	_emit_changed()


func _base_success_chance(target_level: int) -> float:
	var explicit: Dictionary = config.get("base_success_by_target_level", {})
	if explicit.has(str(target_level)):
		return float(explicit[str(target_level)])
	var pattern: Dictionary = config.get("base_success_pattern_by_cycle_position", {})
	var cycle_position := ((target_level - 1) % 10) + 1
	var base := float(pattern.get(str(cycle_position), 0.5))
	var completed_decades := maxi((target_level - 1) / 10, 0)
	var penalty := minf(
		float(completed_decades) * float(config.get("decade_penalty", 0.025)),
		float(config.get("max_decade_penalty", 0.25))
	)
	return maxf(base - penalty, float(config.get("minimum_base_success", 0.25)))


func _conditional_downgrade_ratio(target_level: int) -> float:
	var risk: Dictionary = config.get("risk", {})
	if target_level <= int(risk.get("safe_until_level", 10)):
		return 0.0
	var decade := maxi((target_level - 1) / 10, 0)
	var ratios: Dictionary = risk.get("downgrade_ratio_by_decade", {})
	var ratio := float(ratios.get(str(decade), 0.0))
	if uses_materials_for_level(target_level):
		ratio *= float(risk.get("special_downgrade_multiplier", 1.0))
	ratio *= float(_selected_skill().get("downgrade_multiplier", 1.0))
	if uses_materials_for_level(target_level):
		ratio *= float(_selected_catalyst().get("downgrade_multiplier", 1.0))
	return clampf(ratio, 0.0, 1.0)


func _conditional_destroy_ratio(target_level: int) -> float:
	var risk: Dictionary = config.get("risk", {})
	if target_level < int(risk.get("destroy_start_level", 30)):
		return 0.0
	var decade := maxi((target_level - 1) / 10, 0)
	var ratios: Dictionary = risk.get("destroy_ratio_by_decade", {})
	var ratio := float(ratios.get(str(decade), 0.0))
	if uses_materials_for_level(target_level):
		ratio *= float(risk.get("special_destroy_multiplier", 1.0))
	ratio *= float(_selected_skill().get("destroy_multiplier", 1.0))
	if uses_materials_for_level(target_level):
		ratio *= float(_selected_catalyst().get("destroy_multiplier", 1.0))
	return clampf(ratio, 0.0, 1.0)


func _downgrade_steps(target_level: int) -> int:
	var risk: Dictionary = config.get("risk", {})
	var decade := maxi((target_level - 1) / 10, 0)
	var values: Dictionary = risk.get("downgrade_steps_by_decade", {})
	return maxi(int(values.get(str(decade), 1)), 1)


func _calculate_sale_price(level: int, final_attack: int, affix_list: Array, value_bonus: float) -> int:
	if destroyed:
		return 0
	var economy: Dictionary = config.get("economy", {})
	var price := float(economy.get("base_weapon_price", 100))
	price += pow(maxf(float(final_attack), 1.0), float(economy.get("attack_price_exponent", 1.18))) * float(economy.get("attack_price_scale", 12.0))
	price += pow(maxf(float(level), 0.0), float(economy.get("level_price_exponent", 1.65))) * float(economy.get("level_price_scale", 4.0))
	price += _affix_flat_value(affix_list)
	price *= 1.0 + maxf(value_bonus, 0.0)
	return maxi(int(round(price)), 0)


func _affix_flat_value(affix_list: Array) -> float:
	var value := 0.0
	for affix_value in affix_list:
		if affix_value is not Dictionary:
			continue
		var affix: Dictionary = affix_value
		var effects: Dictionary = affix.get("effects", {})
		value += float(affix.get("tier", 1)) * 60.0
		value += float(effects.get("fire_damage", 0)) * 22.0
		value += float(effects.get("special_trigger_chance", 0.0)) * 1800.0
	return value


func _apply_affix_attack(attack_value: int, affix_list: Array) -> int:
	var attack_percent := 0.0
	for affix_value in affix_list:
		if affix_value is Dictionary:
			var effects: Dictionary = affix_value.get("effects", {})
			attack_percent += float(effects.get("attack_percent", 0.0))
	return int(round(float(attack_value) * (1.0 + attack_percent)))


func _apply_success_value_bonus(level: int) -> void:
	var catalyst := _selected_catalyst()
	var bonus := float(catalyst.get("sale_value_bonus", 0.0))
	bonus += float(_selected_skill().get("sale_value_bonus", 0.0))
	value_bonus_total += bonus
	if selected_catalyst_id != "":
		catalyst_history.append({
			"level": level,
			"id": selected_catalyst_id,
			"name": str(catalyst.get("name", selected_catalyst_id)),
			"price": int(catalyst.get("price", 0)),
			"value_bonus": bonus,
			"description": str(catalyst.get("description", "")),
		})


func _restore_progress_to_level(level: int) -> void:
	progression_attack = int(attack_history.get(str(level), base_attack))
	value_bonus_total = float(value_bonus_history.get(str(level), 0.0))
	var attack_keys := attack_history.keys()
	for key_value in attack_keys:
		if int(key_value) > level:
			attack_history.erase(key_value)
	var value_keys := value_bonus_history.keys()
	for key_value in value_keys:
		if int(key_value) > level:
			value_bonus_history.erase(key_value)
	var retained: Array[Dictionary] = []
	for entry_value in catalyst_history:
		if entry_value is Dictionary and int(entry_value.get("level", 0)) <= level:
			retained.append(entry_value)
	catalyst_history = retained


func _rollback_affixes_to_level(level: int) -> void:
	var allowed_slots := 0
	if level >= 50:
		allowed_slots = 3
	elif level >= 30:
		allowed_slots = 2
	elif level >= 10:
		allowed_slots = 1
	while affixes.size() > allowed_slots:
		affixes.pop_back()
	for index in range(affixes.size()):
		var slot := index + 1
		var allowed_tier := _allowed_affix_tier(slot, level)
		var affix: Dictionary = affixes[index]
		affix["tier"] = allowed_tier
		var definition: Dictionary = affix_by_id.get(str(affix.get("id", "")), {})
		var tiers: Dictionary = definition.get("tiers", {})
		affix["effects"] = tiers.get(str(allowed_tier), {}).duplicate(true)
		affixes[index] = affix


func _allowed_affix_tier(slot: int, level: int) -> int:
	var tier := 1
	match slot:
		1:
			if level >= 20: tier = 2
			if level >= 70: tier = 3
			if level >= 100: tier = 4
		2:
			if level >= 40: tier = 2
			if level >= 80: tier = 3
			if level >= 100: tier = 4
		3:
			if level >= 60: tier = 2
			if level >= 90: tier = 3
			if level >= 100: tier = 4
	return tier


func _preview_affixes_after_success(target_level: int) -> Array[Dictionary]:
	var preview: Array[Dictionary] = []
	for value in affixes:
		if value is Dictionary:
			preview.append(value.duplicate(true))
	var milestone := _milestone_for_level(target_level)
	if milestone.is_empty():
		return preview
	var effect := str(milestone.get("effect", ""))
	var slot := int(milestone.get("slot", 1))
	match effect:
		"ADD_AFFIX":
			var excluded: Array[String] = []
			for existing in preview:
				excluded.append(str(existing.get("id", "")))
			var candidate := _get_leading_affix_preview(true, excluded)
			if candidate.is_empty():
				candidate = _first_available_affix_preview(excluded)
			if not candidate.is_empty():
				var new_affix := candidate.duplicate(true)
				new_affix["slot"] = slot
				new_affix["tier"] = 1
				if slot - 1 < preview.size():
					preview[slot - 1] = new_affix
				else:
					preview.append(new_affix)
		"UPGRADE_AFFIX":
			var index := slot - 1
			if index >= 0 and index < preview.size():
				preview[index] = _preview_upgraded_affix(preview[index], int(milestone.get("tier_delta", 1)))
		"ASCEND_ALL":
			for index in range(preview.size()):
				preview[index] = _preview_upgraded_affix(preview[index], int(milestone.get("tier_delta", 1)))
	return preview


func _preview_upgraded_affix(affix: Dictionary, tier_delta: int) -> Dictionary:
	var result := affix.duplicate(true)
	var definition: Dictionary = affix_by_id.get(str(result.get("id", "")), {})
	var tiers: Dictionary = definition.get("tiers", {})
	var current_tier := int(result.get("tier", 1))
	var target_tier := current_tier + maxi(tier_delta, 1)
	while target_tier > current_tier and not tiers.has(str(target_tier)):
		target_tier -= 1
	result["tier"] = target_tier
	result["effects"] = tiers.get(str(target_tier), {}).duplicate(true)
	return result


func _consume_material_traits() -> void:
	var scoring: Dictionary = config["material_scoring"]
	var secondary := _selected_secondary()
	for tag_value in secondary.get("affix_tags", []):
		var tag := str(tag_value)
		_add_material_score(material_scores, tag, int(scoring["secondary_tag_weight"]))
		_add_material_score(lifetime_material_scores, tag, int(scoring["secondary_tag_weight"]))
		last_secondary_tag = tag
	var catalyst := _selected_catalyst()
	for tag_value in catalyst.get("affix_tags", []):
		var tag := str(tag_value)
		_add_material_score(material_scores, tag, int(scoring["catalyst_tag_weight"]))
		_add_material_score(lifetime_material_scores, tag, int(scoring["catalyst_tag_weight"]))


func _apply_milestone(milestone: Dictionary) -> void:
	var effect := str(milestone.get("effect", ""))
	var slot := int(milestone.get("slot", 1))
	match effect:
		"ADD_AFFIX":
			_add_affix_to_slot(slot)
		"UPGRADE_AFFIX":
			_upgrade_affix_slot(slot, int(milestone.get("tier_delta", 1)))
		"ASCEND_ALL":
			for affix_index in range(affixes.size()):
				_upgrade_affix_slot(affix_index + 1, int(milestone.get("tier_delta", 1)))
	material_scores.clear()
	last_secondary_tag = ""


func _add_affix_to_slot(slot: int) -> void:
	var excluded_ids: Array[String] = []
	for affix_value in affixes:
		var existing: Dictionary = affix_value
		excluded_ids.append(str(existing.get("id", "")))
	var preview := _get_leading_affix_preview(false, excluded_ids)
	if preview.is_empty():
		preview = _first_available_affix_preview(excluded_ids)
	if preview.is_empty():
		return
	var new_affix := preview.duplicate(true)
	new_affix["slot"] = slot
	new_affix["tier"] = 1
	if slot - 1 < affixes.size():
		affixes[slot - 1] = new_affix
	else:
		affixes.append(new_affix)


func _upgrade_affix_slot(slot: int, tier_delta: int) -> void:
	var index := slot - 1
	if index < 0 or index >= affixes.size():
		return
	affixes[index] = _preview_upgraded_affix(affixes[index], tier_delta)


func _get_milestone_preview() -> Dictionary:
	var milestone := _next_milestone()
	if milestone.is_empty():
		return {}
	var effect := str(milestone.get("effect", ""))
	var slot := int(milestone.get("slot", 1))
	var preview := milestone.duplicate(true)
	preview["label"] = "재료 이정표"
	if effect == "ADD_AFFIX":
		var excluded_ids: Array[String] = []
		for affix_value in affixes:
			var existing: Dictionary = affix_value
			excluded_ids.append(str(existing.get("id", "")))
		var affix_preview := _get_leading_affix_preview(true, excluded_ids)
		if affix_preview.is_empty():
			affix_preview = _first_available_affix_preview(excluded_ids)
		preview["affix"] = affix_preview
		preview["label"] = "수식어 추가"
	elif effect == "UPGRADE_AFFIX":
		var index := slot - 1
		var current_affix: Dictionary = {}
		if index >= 0 and index < affixes.size():
			current_affix = affixes[index].duplicate(true)
		preview["affix"] = _preview_upgraded_affix(current_affix, int(milestone.get("tier_delta", 1))) if not current_affix.is_empty() else {}
		preview["label"] = "수식어 강화"
	elif effect == "ASCEND_ALL":
		preview["label"] = "전체 수식어 최종 승급"
	return preview


func _get_leading_affix_preview(include_current_selection: bool = true, excluded_affix_ids: Array[String] = []) -> Dictionary:
	var scores := material_scores.duplicate(true)
	if include_current_selection:
		var secondary := _selected_secondary()
		for tag_value in secondary.get("affix_tags", []):
			var tag := str(tag_value)
			scores[tag] = int(scores.get(tag, 0)) + 1
		var catalyst := _selected_catalyst()
		for tag_value in catalyst.get("affix_tags", []):
			var tag := str(tag_value)
			scores[tag] = int(scores.get(tag, 0)) + 1
	var best_tag := ""
	var best_score := -1
	for tag_value in scores:
		var tag := str(tag_value)
		var preview := _affix_preview_for_tag(tag)
		if preview.is_empty() or str(preview.get("id", "")) in excluded_affix_ids:
			continue
		var score := int(scores[tag])
		if score > best_score or (score == best_score and tag == last_secondary_tag):
			best_tag = tag
			best_score = score
	if best_tag == "":
		var fallback := _affix_preview_for_tag(_first_affix_tag_for_material(selected_secondary_id))
		if not fallback.is_empty() and str(fallback.get("id", "")) not in excluded_affix_ids:
			return fallback
		return {}
	return _affix_preview_for_tag(best_tag)


func _first_available_affix_preview(excluded_affix_ids: Array[String]) -> Dictionary:
	for affix_id_value in affix_by_id:
		var definition: Dictionary = affix_by_id[affix_id_value]
		var affix_id := str(definition.get("id", ""))
		if affix_id in excluded_affix_ids:
			continue
		var tags: Array = definition.get("material_tags", [])
		if not tags.is_empty():
			return _affix_preview_for_tag(str(tags[0]))
	return {}


func _affix_preview_for_tag(tag: String) -> Dictionary:
	for affix_id_value in affix_by_id:
		var definition: Dictionary = affix_by_id[affix_id_value]
		if tag in definition.get("material_tags", []):
			var tiers: Dictionary = definition.get("tiers", {})
			return {
				"id": str(definition.get("id", "")),
				"name": str(definition.get("name", "")),
				"material_tag": tag,
				"tier": 1,
				"effects": tiers.get("1", {}).duplicate(true),
			}
	return {}


func _milestone_for_level(level: int) -> Dictionary:
	for item_value in config.get("milestones", []):
		if item_value is Dictionary:
			var item: Dictionary = item_value
			if int(item.get("level", -1)) == level:
				return item
	return {}


func _next_milestone() -> Dictionary:
	for item_value in config.get("milestones", []):
		if item_value is Dictionary:
			var item: Dictionary = item_value
			if int(item.get("level", 0)) > enhancement_level:
				return item
	return {}


func _selected_secondary() -> Dictionary:
	return _material(selected_secondary_id)


func _selected_catalyst() -> Dictionary:
	return _material(selected_catalyst_id)


func _selected_skill() -> Dictionary:
	var skills: Dictionary = config.get("skills", {})
	return skills.get(selected_skill_id, skills.get("balanced", {}))


func _selected_catalyst_bonus() -> float:
	return float(_selected_catalyst().get("success_bonus", 0.0))


func _current_pity_bonus() -> float:
	var pity: Dictionary = config["pity"]
	return minf(float(failure_streak) * float(pity["bonus_per_failure"]), float(pity["max_bonus"]))


func _add_material_score(target: Dictionary, tag: String, amount: int) -> void:
	target[tag] = int(target.get(tag, 0)) + amount


func _material(material_id: String) -> Dictionary:
	return material_by_id.get(material_id, {})


func _material_supports_slot(material_id: String, slot: String) -> bool:
	return slot in _material(material_id).get("slot_types", [])


func _first_affix_tag_for_material(material_id: String) -> String:
	var tags: Array = _material(material_id).get("affix_tags", [])
	return str(tags[0]) if not tags.is_empty() else ""


func _index_materials(materials: Array) -> void:
	material_by_id.clear()
	for item_value in materials:
		if item_value is Dictionary:
			var item: Dictionary = item_value
			material_by_id[str(item.get("id", ""))] = item.duplicate(true)


func _index_affixes(definitions: Array) -> void:
	affix_by_id.clear()
	for item_value in definitions:
		if item_value is Dictionary:
			var item: Dictionary = item_value
			affix_by_id[str(item.get("id", ""))] = item.duplicate(true)


func _merge_config(custom_config: Dictionary) -> void:
	for key_value in custom_config:
		var key := str(key_value)
		if config.get(key) is Dictionary and custom_config[key_value] is Dictionary:
			var nested: Dictionary = config[key]
			for nested_key in custom_config[key_value]:
				nested[nested_key] = custom_config[key_value][nested_key]
		else:
			config[key] = custom_config[key_value]


func _emit_changed() -> void:
	changed.emit(snapshot())
