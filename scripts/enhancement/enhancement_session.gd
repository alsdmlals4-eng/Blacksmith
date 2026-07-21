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
	"precision_interval": 5,
	"material_interval": 10,
	"base_success_by_target_level": {},
	"base_success_pattern_by_cycle_position": {
		"1": 0.98,
		"2": 0.95,
		"3": 0.92,
		"4": 0.89,
		"5": 0.76,
		"6": 0.88,
		"7": 0.85,
		"8": 0.82,
		"9": 0.79,
		"10": 0.68,
	},
	"decade_penalty": 0.02,
	"max_decade_penalty": 0.18,
	"minimum_base_success": 0.35,
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
		"bonus_per_failure": 0.05,
		"max_bonus": 0.2,
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
var precision_position: float = 0.0
var precision_direction: float = 1.0
var material_scores: Dictionary = {}
var lifetime_material_scores: Dictionary = {}
var last_secondary_tag: String = ""
var failure_streak: int = 0
var total_attempts: int = 0
var total_failures: int = 0
var last_attempt: Dictionary = {}
var pending_roll_override: float = -1.0


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


func begin_attempt(roll_override: float = -1.0) -> bool:
	if state != State.READY or enhancement_level >= int(config["max_level"]):
		return false

	var target_level := enhancement_level + 1
	total_attempts += 1
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
	var interval := maxi(int(config.get("precision_interval", 5)), 1)
	return target_level > 0 and target_level % interval == 0


func uses_materials_for_level(target_level: int) -> bool:
	var interval := maxi(int(config.get("material_interval", 10)), 1)
	return target_level > 0 and target_level % interval == 0


func calculate_success_chance(precision_bonus: float = 0.0) -> float:
	var target_level := enhancement_level + 1
	var base_chance := _base_success_chance(target_level)
	var catalyst_bonus := _selected_catalyst_bonus() if uses_materials_for_level(target_level) else 0.0
	var pity: Dictionary = config["pity"]
	var pity_bonus := minf(
		float(failure_streak) * float(pity["bonus_per_failure"]),
		float(pity["max_bonus"])
	)
	return clampf(base_chance + catalyst_bonus + pity_bonus + precision_bonus, 0.0, 1.0)


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
		"precision_position": precision_position,
		"base_success_chance": calculate_success_chance(),
		"failure_streak": failure_streak,
		"pity_bonus": _current_pity_bonus(),
		"material_scores": material_scores.duplicate(true),
		"lifetime_material_scores": lifetime_material_scores.duplicate(true),
		"milestone_preview": _get_milestone_preview(),
		"affixes": affixes.duplicate(true),
		"total_attempts": total_attempts,
		"total_failures": total_failures,
		"last_attempt": last_attempt.duplicate(true),
	}


func get_display_name() -> String:
	var names: Array[String] = []
	for index in range(affixes.size() - 1, -1, -1):
		var affix: Dictionary = affixes[index]
		names.append(str(affix.get("name", "")))
	var prefix := "%s " % " ".join(names) if not names.is_empty() else ""
	return "%s%s +%d" % [prefix, base_weapon_name, enhancement_level]


func _resolve_attempt(precision_id: String, precision_label: String, precision_bonus: float) -> void:
	var target_level := enhancement_level + 1
	var success_chance := calculate_success_chance(precision_bonus)
	var roll := pending_roll_override if pending_roll_override >= 0.0 else rng.randf()
	pending_roll_override = -1.0
	var success := roll < success_chance
	var milestone := _milestone_for_level(target_level)
	var material_stage := uses_materials_for_level(target_level)

	if success:
		enhancement_level = target_level
		failure_streak = 0
		if not milestone.is_empty():
			_apply_milestone(milestone)
	elif material_stage:
		# 실패한 +10 단위 시도는 재료 성질도 다시 선택할 수 있도록 되돌린다.
		material_scores.clear()
		last_secondary_tag = ""
		failure_streak += 1
		total_failures += 1
	else:
		failure_streak += 1
		total_failures += 1

	last_attempt = {
		"success": success,
		"target_level": target_level,
		"result_level": enhancement_level,
		"success_chance": success_chance,
		"roll": roll,
		"precision_id": precision_id,
		"precision_label": precision_label,
		"precision_bonus": precision_bonus,
		"precision_required": requires_precision_for_level(target_level),
		"uses_materials": material_stage,
		"milestone": milestone.duplicate(true),
		"secondary_material_id": selected_secondary_id if material_stage else "",
		"catalyst_material_id": selected_catalyst_id if material_stage else "",
		"affixes": affixes.duplicate(true),
	}

	if success and enhancement_level >= int(config["max_level"]):
		state = State.COMPLETE
		last_attempt["final_weapon"] = {
			"weapon_id": weapon_id,
			"weapon_name": get_display_name(),
			"enhancement_level": enhancement_level,
			"affixes": affixes.duplicate(true),
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
		float(completed_decades) * float(config.get("decade_penalty", 0.02)),
		float(config.get("max_decade_penalty", 0.18))
	)
	return maxf(base - penalty, float(config.get("minimum_base_success", 0.35)))


func _consume_material_traits() -> void:
	var scoring: Dictionary = config["material_scoring"]
	var secondary := _material(selected_secondary_id)
	for tag_value in secondary.get("affix_tags", []):
		var tag := str(tag_value)
		_add_material_score(material_scores, tag, int(scoring["secondary_tag_weight"]))
		_add_material_score(lifetime_material_scores, tag, int(scoring["secondary_tag_weight"]))
		last_secondary_tag = tag
	var catalyst := _material(selected_catalyst_id)
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
	var new_affix := {
		"id": preview["id"],
		"name": preview["name"],
		"slot": slot,
		"tier": 1,
		"material_tag": preview["material_tag"],
		"effects": preview.get("effects", {}).duplicate(true),
	}
	if slot - 1 < affixes.size():
		affixes[slot - 1] = new_affix
	else:
		affixes.append(new_affix)


func _upgrade_affix_slot(slot: int, tier_delta: int) -> void:
	var index := slot - 1
	if index < 0 or index >= affixes.size():
		return
	var affix: Dictionary = affixes[index]
	var definition: Dictionary = affix_by_id.get(str(affix.get("id", "")), {})
	var tiers: Dictionary = definition.get("tiers", {})
	var current_tier := int(affix.get("tier", 1))
	var target_tier := current_tier + maxi(tier_delta, 1)
	while target_tier > current_tier and not tiers.has(str(target_tier)):
		target_tier -= 1
	if target_tier <= current_tier:
		return
	affix["tier"] = target_tier
	affix["effects"] = tiers.get(str(target_tier), {}).duplicate(true)
	affixes[index] = affix


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
		preview["affix"] = affixes[index].duplicate(true) if index >= 0 and index < affixes.size() else {}
		preview["label"] = "수식어 강화"
	elif effect == "ASCEND_ALL":
		preview["label"] = "전체 수식어 최종 승급"
	return preview


func _get_leading_affix_preview(include_current_selection: bool = true, excluded_affix_ids: Array[String] = []) -> Dictionary:
	var scores := material_scores.duplicate(true)
	if include_current_selection:
		var secondary := _material(selected_secondary_id)
		for tag_value in secondary.get("affix_tags", []):
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


func _selected_catalyst_bonus() -> float:
	return float(_material(selected_catalyst_id).get("success_bonus", 0.0))


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
