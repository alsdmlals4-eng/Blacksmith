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
	"max_level": 5,
	"base_success_by_target_level": {
		"1": 1.0,
		"2": 0.9,
		"3": 0.8,
		"4": 0.7,
		"5": 0.6,
	},
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
var precision_enabled: bool = true
var precision_position: float = 0.0
var precision_direction: float = 1.0
var material_scores: Dictionary = {}
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
	if state != State.READY or not _material_supports_slot(material_id, "secondary"):
		return false
	selected_secondary_id = material_id
	_emit_changed()
	return true


func set_catalyst_material(material_id: String) -> bool:
	if state != State.READY:
		return false
	if material_id != "" and not _material_supports_slot(material_id, "catalyst"):
		return false
	selected_catalyst_id = material_id
	_emit_changed()
	return true


func set_precision_enabled(enabled: bool) -> void:
	if state != State.READY:
		return
	precision_enabled = enabled
	_emit_changed()


func begin_attempt(roll_override: float = -1.0) -> bool:
	if state != State.READY or enhancement_level >= int(config["max_level"]):
		return false

	total_attempts += 1
	pending_roll_override = roll_override
	_consume_material_traits()

	if precision_enabled:
		state = State.PRECISION
		precision_position = 0.0
		precision_direction = 1.0
		state_changed.emit(state)
		_emit_changed()
	else:
		_resolve_attempt("STANDARD", "자동 강화", 0.0)
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
	var quality_label := "보통 판정"
	var success_bonus := 0.0

	if distance <= float(precision["perfect_radius"]):
		quality_id = "PERFECT"
		quality_label = "완벽한 강화"
		success_bonus = float(precision["perfect_success_bonus"])
	elif distance <= float(precision["good_radius"]):
		quality_id = "GOOD"
		quality_label = "좋은 강화"
		success_bonus = float(precision["good_success_bonus"])

	_resolve_attempt(quality_id, quality_label, success_bonus)
	return last_attempt.duplicate(true)


func calculate_success_chance(precision_bonus: float = 0.0) -> float:
	var target_level := enhancement_level + 1
	var base_table: Dictionary = config["base_success_by_target_level"]
	var base_chance := float(base_table.get(str(target_level), 0.0))
	var catalyst_bonus := _selected_catalyst_bonus()
	var pity: Dictionary = config["pity"]
	var pity_bonus := minf(
		float(failure_streak) * float(pity["bonus_per_failure"]),
		float(pity["max_bonus"])
	)
	return clampf(base_chance + catalyst_bonus + pity_bonus + precision_bonus, 0.0, 1.0)


func snapshot() -> Dictionary:
	var preview := _get_leading_affix_preview()
	return {
		"state": state,
		"weapon_id": weapon_id,
		"base_weapon_name": base_weapon_name,
		"display_name": get_display_name(),
		"enhancement_level": enhancement_level,
		"max_level": int(config["max_level"]),
		"progress_ratio": float(enhancement_level) / float(config["max_level"]),
		"target_level": mini(enhancement_level + 1, int(config["max_level"])),
		"selected_secondary_id": selected_secondary_id,
		"selected_catalyst_id": selected_catalyst_id,
		"precision_enabled": precision_enabled,
		"precision_position": precision_position,
		"base_success_chance": calculate_success_chance(),
		"failure_streak": failure_streak,
		"pity_bonus": _current_pity_bonus(),
		"material_scores": material_scores.duplicate(true),
		"leading_affix": preview,
		"affixes": affixes.duplicate(true),
		"total_attempts": total_attempts,
		"total_failures": total_failures,
		"last_attempt": last_attempt.duplicate(true),
	}


func get_display_name() -> String:
	var prefix := ""
	if not affixes.is_empty():
		prefix = "%s " % str(affixes[0].get("name", ""))
	return "%s%s +%d" % [prefix, base_weapon_name, enhancement_level]


func _resolve_attempt(precision_id: String, precision_label: String, precision_bonus: float) -> void:
	var target_level := enhancement_level + 1
	var success_chance := calculate_success_chance(precision_bonus)
	var roll := pending_roll_override if pending_roll_override >= 0.0 else rng.randf()
	pending_roll_override = -1.0
	var success := roll < success_chance

	if success:
		enhancement_level = target_level
		failure_streak = 0
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
		"secondary_material_id": selected_secondary_id,
		"catalyst_material_id": selected_catalyst_id,
	}

	if success and enhancement_level >= int(config["max_level"]):
		_apply_first_affix()
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


func _consume_material_traits() -> void:
	var scoring: Dictionary = config["material_scoring"]
	var secondary := _material(selected_secondary_id)
	for tag in secondary.get("affix_tags", []):
		_add_material_score(str(tag), int(scoring["secondary_tag_weight"]))
		last_secondary_tag = str(tag)

	var catalyst := _material(selected_catalyst_id)
	for tag in catalyst.get("affix_tags", []):
		_add_material_score(str(tag), int(scoring["catalyst_tag_weight"]))


func _apply_first_affix() -> void:
	var preview := _get_leading_affix_preview(false)
	if preview.is_empty():
		return
	affixes = [{
		"id": preview["id"],
		"name": preview["name"],
		"tier": 1,
		"material_tag": preview["material_tag"],
		"effects": preview.get("effects", {}).duplicate(true),
	}]


func _get_leading_affix_preview(include_current_selection: bool = true) -> Dictionary:
	var scores := material_scores.duplicate(true)
	if include_current_selection and scores.is_empty():
		var secondary := _material(selected_secondary_id)
		for tag in secondary.get("affix_tags", []):
			scores[str(tag)] = int(scores.get(str(tag), 0)) + 1

	var best_tag := ""
	var best_score := -1
	for tag_value in scores:
		var tag := str(tag_value)
		if not _has_affix_for_tag(tag):
			continue
		var score := int(scores[tag])
		if score > best_score or (score == best_score and tag == last_secondary_tag):
			best_tag = tag
			best_score = score

	if best_tag == "":
		best_tag = _first_affix_tag_for_material(selected_secondary_id)
	return _affix_preview_for_tag(best_tag)


func _affix_preview_for_tag(tag: String) -> Dictionary:
	for affix_id_value in affix_by_id:
		var definition: Dictionary = affix_by_id[affix_id_value]
		if tag in definition.get("material_tags", []):
			var tiers: Dictionary = definition.get("tiers", {})
			return {
				"id": str(definition.get("id", "")),
				"name": str(definition.get("name", "")),
				"material_tag": tag,
				"effects": tiers.get("1", {}).duplicate(true),
			}
	return {}


func _selected_catalyst_bonus() -> float:
	return float(_material(selected_catalyst_id).get("success_bonus", 0.0))


func _current_pity_bonus() -> float:
	var pity: Dictionary = config["pity"]
	return minf(
		float(failure_streak) * float(pity["bonus_per_failure"]),
		float(pity["max_bonus"])
	)


func _add_material_score(tag: String, amount: int) -> void:
	material_scores[tag] = int(material_scores.get(tag, 0)) + amount


func _material(material_id: String) -> Dictionary:
	return material_by_id.get(material_id, {})


func _material_supports_slot(material_id: String, slot: String) -> bool:
	return slot in _material(material_id).get("slot_types", [])


func _first_affix_tag_for_material(material_id: String) -> String:
	var tags: Array = _material(material_id).get("affix_tags", [])
	return str(tags[0]) if not tags.is_empty() else ""


func _has_affix_for_tag(tag: String) -> bool:
	return not _affix_preview_for_tag(tag).is_empty()


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
