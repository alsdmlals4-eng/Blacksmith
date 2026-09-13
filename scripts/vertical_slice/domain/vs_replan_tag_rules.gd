# New blueprint ruleset only. Never reinterpret legacy CATALYST_AFFIX saves.
extends RefCounted

const RULESET_ID := "BLACKSMITH_REPLAN_TAGS_20260912"
const DISPLAY_NAMES_KO := {"BURST_OUTPUT":"격발", "SUSTAIN_OUTPUT":"견실", "BURST_HANDLING":"기민", "SUSTAIN_HANDLING":"균형"}
const AQUEDUCT_REQUIREMENTS := {
	"OUTPUT:BURST": {"content_id":"AQ01", "purpose":"파편을 막아 표식 회수", "success":"표식 회수", "failure":"접근 중단"},
	"HANDLING:BURST": {"content_id":"AQ02", "purpose":"바뀌는 방향을 엄호", "success":"표식 회수", "failure":"철수"},
	"OUTPUT:SUSTAIN": {"content_id":"AQ03", "purpose":"측량 동안 엄호", "success":"측량 완료", "failure":"엄호 중단"},
	"HANDLING:SUSTAIN": {"content_id":"AQ04", "purpose":"여러 지점 이동 엄호", "success":"측량 기록", "failure":"일부 철수"},
}
const WORLD_TRIALS := {
	"AQ": {"bucket":"aqueduct_trials", "record_type":"AQUEDUCT_TRIAL_V1", "title":"무너진 수로의 측량대", "profile":"LOW"},
	"DU": {"bucket":"duel_trials", "record_type":"DUEL_TRIAL_V1", "title":"콜로세움 결투", "profile":"MEDIUM"},
	"AR": {"bucket":"army_trials", "record_type":"ARMY_TRIAL_V1", "title":"전선 엄호", "profile":"HIGH"},
}
const WORLD_EQUIPMENT := {
	"AQ": ["iron_shield"],
	"DU": ["iron_sword", "iron_shield"],
	"AR": ["iron_sword", "iron_shield", "iron_bow", "iron_armor", "iron_helmet"],
}
const WORLD_PURPOSES := {
	"DU": {
		"OUTPUT:BURST":{"content_id":"DU01","purpose":"결정적 검격·막기","success":"결투 승리","failure":"패배 인정"},
		"HANDLING:BURST":{"content_id":"DU02","purpose":"빠른 대응·방향 조절","success":"결투 승리","failure":"패배 인정"},
		"OUTPUT:SUSTAIN":{"content_id":"DU03","purpose":"반복 공방의 성능","success":"결투 승리","failure":"패배 인정"},
		"HANDLING:SUSTAIN":{"content_id":"DU04","purpose":"안정적인 반복 취급","success":"결투 승리","failure":"패배 인정"},
	},
	"AR": {
		"OUTPUT:BURST":{"content_id":"AR01","purpose":"짧은 돌파·급박한 엄호","success":"목표 확보","failure":"철수"},
		"HANDLING:BURST":{"content_id":"AR02","purpose":"진형 변화에 빠른 대응","success":"목표 확보","failure":"철수"},
		"OUTPUT:SUSTAIN":{"content_id":"AR03","purpose":"통로·보급대 지속 엄호","success":"통로 유지","failure":"철수"},
		"HANDLING:SUSTAIN":{"content_id":"AR04","purpose":"긴 행군과 반복 진형 유지","success":"목적지 도착","failure":"행군 중단"},
	},
}

func world_preview(family: String, equipment_id: String, level: Variant, tags: Dictionary, axis: String, rhythm: String) -> Dictionary:
	if not WORLD_TRIALS.has(family):
		return {"ok":false, "reason":"UNKNOWN_WORLD_TRIAL"}
	if family == "AQ" and equipment_id != "iron_shield":
		return {"ok":false, "reason":"REQUIRES_SHIELD"}
	if equipment_id not in WORLD_EQUIPMENT[family]:
		return {"ok":false, "reason":"REQUIRES_SWORD_OR_SHIELD" if family == "DU" else "UNSUPPORTED_WORLD_EQUIPMENT"}
	# Reuse the established readiness calculation after checking actual equipment.
	var result := aqueduct_preview("iron_shield", level, tags, axis, rhythm)
	if result.ok:
		var definitions: Dictionary = AQUEDUCT_REQUIREMENTS if family == "AQ" else WORLD_PURPOSES[family]
		result.merge(definitions[axis + ":" + rhythm])
		result["profile"] = WORLD_TRIALS[family].profile
	return result

const TAGS := {
	"BURST_OUTPUT": ["OUTPUT", "BURST"],
	"SUSTAIN_OUTPUT": ["OUTPUT", "SUSTAIN"],
	"BURST_HANDLING": ["HANDLING", "BURST"],
	"SUSTAIN_HANDLING": ["HANDLING", "SUSTAIN"],
}

# Preview is pure: committing cost/result belongs to the save transaction owner.
func preview(equipment_id: String, level: int, tags: Dictionary, tag_id: String, inventory: Dictionary) -> Dictionary:
	if equipment_id not in ["iron_sword", "iron_shield", "iron_bow", "iron_armor", "iron_helmet"]:
		return {"ok": false, "reason": "UNKNOWN_EQUIPMENT"}
	if level < 9 or level > 99 or (level + 1) % 10 != 0:
		return {"ok": false, "reason": "INVALID_PRECISION_ENTRY"}
	var checked := support(tags, "OUTPUT", "BURST")
	if not checked.ok:
		return checked
	var spent_stages := 0
	for stage in tags.values():
		spent_stages += int(stage)
	if spent_stages != floori(float(level) / 10.0):
		return {"ok": false, "reason": "MILESTONE_STATE_MISMATCH"}
	if not TAGS.has(tag_id):
		return {"ok": false, "reason": "INVALID_SELECTION"}
	var stage_before := int(tags.get(tag_id, 0))
	if stage_before == 4:
		return {"ok": false, "reason": "TAG_MASTERED"}
	if stage_before == 0 and tags.size() >= 3:
		return {"ok": false, "reason": "TAG_CAP"}
	var catalyst_id := "fire_heart" if TAGS[tag_id][1] == "BURST" else "earth_crystal"
	var stock: Variant = inventory.get(catalyst_id, 0)
	if typeof(stock) != TYPE_INT or stock < 1:
		return {"ok": false, "reason": "INSUFFICIENT_CATALYST"}
	var after := tags.duplicate(true)
	after[tag_id] = stage_before + 1
	return {"ok": true, "reason": "OK", "ruleset_id": RULESET_ID,
		"target_level": level + 1, "tags_after": after,
		"action": "ADD_TAG" if stage_before == 0 else "UPGRADE_TAG",
		"catalyst_id": catalyst_id, "catalyst_cost": 1}

# Adapter into the existing enhancement transaction; stock is checked by its owner.
func selection_preview(item, target_level: int, selection: Dictionary) -> Dictionary:
	if item == null:
		return {"allowed": false, "reason": "MISSING_ITEM"}
	var decoded := decode_saved_affix(item.catalyst_affix, item.enhancement_level, item.used_precision_milestones)
	if not decoded.ok:
		return {"allowed": false, "reason": decoded.reason}
	if str(selection.get("ruleset_id", "")) != RULESET_ID:
		return {"allowed": false, "reason": "INVALID_REPLAN_SELECTION"}
	if target_level != int(item.enhancement_level) + 1:
		return {"allowed": false, "reason": "TARGET_LEVEL_MISMATCH"}
	if str(item.physical_state) == "DESTROYED":
		return {"allowed": false, "reason": "ITEM_DESTROYED"}
	var identity: Dictionary = load("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd").by_item(item)
	var tag_id := str(selection.get("tag_id", ""))
	var checked := preview(str(identity.get("equipment_id", "")), int(item.enhancement_level),
		decoded.affix.tags, tag_id, {"fire_heart":1, "earth_crystal":1})
	if not checked.ok:
		return {"allowed": false, "reason": checked.reason}
	var fire: bool = checked.catalyst_id == "fire_heart"
	return {"allowed": true, "reason": "OK", "ruleset_id": RULESET_ID,
		"action": checked.action, "tag_id": tag_id, "tags_after": checked.tags_after,
		"stage_before": int(decoded.affix.tags.get(tag_id, 0)),
		"stage_after": int(checked.tags_after[tag_id]),
		"effect_axis": "EVENT_SUITABILITY", "effect_delta": 0,
		"precision_catalyst_id": checked.catalyst_id,
		"precision_catalyst_stock_key": "heart_of_flame" if fire else "earth_crystal",
		"precision_catalyst_display_name_ko": "불의 심장" if fire else "대지의 결정",
		"precision_catalyst_units": 1}

func apply_selection_success(item, target_level: int, selection: Dictionary) -> Dictionary:
	var result := selection_preview(item, target_level, selection)
	if not result.allowed:
		result["applied"] = false
		return result
	item.catalyst_affix["tags"] = result.tags_after.duplicate(true)
	item.used_precision_milestones.append(target_level)
	result["applied"] = true
	return result

# Read model for the workshop: hypothetical success is distinct from permission.
# No resources, item state or event probabilities are changed here.
func customer_choices(equipment_id: String, level: int, tags: Dictionary, inventory: Dictionary, axis: String, rhythm: String) -> Dictionary:
	var before := support(tags, axis, rhythm)
	if not before.ok:
		return before
	for catalyst in ["fire_heart", "earth_crystal"]:
		var stock: Variant = inventory.get(catalyst, 0)
		if typeof(stock) != TYPE_INT or stock < 0:
			return {"ok": false, "reason": "INVALID_CATALYST_STOCK"}
	var choices: Array = []
	for tag_id in TAGS:
		var available := preview(equipment_id, level, tags, tag_id, inventory)
		if available.reason in ["UNKNOWN_EQUIPMENT", "INVALID_PRECISION_ENTRY", "MILESTONE_STATE_MISMATCH"]:
			return available
		var catalyst_id := "fire_heart" if TAGS[tag_id][1] == "BURST" else "earth_crystal"
		var row := {"tag_id": tag_id, "allowed": available.ok, "reason": available.reason,
			"catalyst_id": catalyst_id, "catalyst_cost": 1,
			"catalyst_stock": int(inventory.get(catalyst_id, 0))}
		var hypothetical := available
		if available.reason == "INSUFFICIENT_CATALYST":
			var comparison_stock := inventory.duplicate(true)
			comparison_stock[catalyst_id] = 1
			hypothetical = preview(equipment_id, level, tags, tag_id, comparison_stock)
		if hypothetical.ok:
			var after := support(hypothetical.tags_after, axis, rhythm)
			row["points_after"] = after.points
			row["points_delta"] = int(after.points) - int(before.points)
			row["action"] = hypothetical.action
			row["stage_before"] = int(tags.get(tag_id, 0))
			row["stage_after"] = int(hypothetical.tags_after[tag_id])
		choices.append(row)
	return {"ok": true, "reason": "OK", "points_before": before.points,
		"axis": axis, "rhythm": rhythm, "choices": choices}

# Blueprint section21/22 trial estimate; no roll, reward, damage or save mutation.
func aqueduct_preview(equipment_id: String, level: Variant, tags: Dictionary, axis: String, rhythm: String) -> Dictionary:
	if equipment_id != "iron_shield":
		return {"ok": false, "reason": "REQUIRES_SHIELD"}
	if typeof(level) != TYPE_INT or level < 10 or level > 100:
		return {"ok": false, "reason": "INVALID_MISSION_LEVEL"}
	var checked := support(tags, axis, rhythm)
	if not checked.ok:
		return checked
	var stages := 0
	for stage in tags.values():
		stages += int(stage)
	if stages != floori(float(level) / 10.0):
		return {"ok": false, "reason": "MILESTONE_STATE_MISMATCH"}
	var base := clampf(60.0 + 0.5 * (float(level) - 10.0), 40.0, 80.0)
	var final := clampf(base + float(checked.points), 5.0, 95.0)
	return {"ok": true, "base_percent": base, "support_points": checked.points,
		"applied_support_percent": final - base, "success_percent": final,
		"trial_only": true, "reward": "NONE"}

# Nested save version keeps legacy tag effects separate. JSON whole-number floats
# are accepted only at this boundary, never booleans or fractional stages.
func decode_saved_affix(value: Dictionary, level: Variant, milestones: Array) -> Dictionary:
	if not (level is int or level is float) or not is_finite(float(level)) or float(level) != floor(float(level)):
		return {"ok": false, "reason": "INVALID_REPLAN_LEVEL"}
	if not (value.get("schema_version") is int or value.get("schema_version") is float) or value.get("schema_version") != 2:
		return {"ok": false, "reason": "INVALID_REPLAN_SCHEMA"}
	if not value.get("ruleset_id") is String or value.get("ruleset_id") != RULESET_ID:
		return {"ok": false, "reason": "UNKNOWN_REPLAN_RULESET"}
	if value.size() != 3 or not value.get("tags") is Dictionary:
		return {"ok": false, "reason": "INVALID_REPLAN_FIELDS"}
	var tags: Dictionary = {}
	var spent := 0
	for tag_id in value.tags:
		var stage: Variant = value.tags[tag_id]
		if not (stage is int or stage is float) or not is_finite(float(stage)) or float(stage) != floor(float(stage)) or stage < 1 or stage > 4:
			return {"ok": false, "reason": "INVALID_REPLAN_STAGE"}
		tags[tag_id] = int(stage)
		spent += int(stage)
	var checked := support(tags, "OUTPUT", "BURST")
	if not checked.ok:
		return checked
	if level < 0 or level > 100:
		return {"ok": false, "reason": "INVALID_REPLAN_LEVEL"}
	var count := floori(float(level) / 10.0)
	if spent != count or milestones.size() != count:
		return {"ok": false, "reason": "REPLAN_MILESTONE_MISMATCH"}
	for index in range(count):
		var milestone: Variant = milestones[index]
		if not (milestone is int or milestone is float) or milestone != (index + 1) * 10:
			return {"ok": false, "reason": "REPLAN_MILESTONE_MISMATCH"}
	return {"ok": true, "affix": {"schema_version": 2, "ruleset_id": RULESET_ID, "tags": tags}}

# Read-only suitability; does not change enhancement, damage, weight or repair.
func support(tags: Dictionary, axis: String, rhythm: String) -> Dictionary:
	if axis not in ["OUTPUT", "HANDLING"] or rhythm not in ["BURST", "SUSTAIN"]:
		return {"ok": false, "reason": "INVALID_REQUIREMENT", "points": 0}
	if tags.size() > 3:
		return {"ok": false, "reason": "TAG_CAP", "points": 0}
	var points := 0
	for tag_id in tags:
		if not TAGS.has(tag_id):
			return {"ok": false, "reason": "UNKNOWN_TAG", "points": 0}
		var stage: Variant = tags[tag_id]
		if typeof(stage) != TYPE_INT or stage < 1 or stage > 4:
			return {"ok": false, "reason": "INVALID_STAGE", "points": 0}
		var identity: Array = TAGS[tag_id]
		if identity[0] == axis:
			points += int(stage) * (3 if identity[1] == rhythm else 1)
	return {"ok": true, "reason": "OK", "points": points}
