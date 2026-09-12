# New blueprint ruleset only. Never reinterpret legacy CATALYST_AFFIX saves.
extends RefCounted

const RULESET_ID := "BLACKSMITH_REPLAN_TAGS_20260912"
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
