# Decision38 catalog adapter. This is the sole normal-success mutation boundary for Catalyst Tags.
class_name VSPrecisionResolver
extends RefCounted

const CATALOG_PATH := "res://docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json"
const EquipmentCatalogScript = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
const CATALYST_OWNER := "CATALYST_AFFIX"
const PRECISION_TARGETS := [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
const MAX_ACTIVE_TAGS := 3
const MAX_TAG_STAGE := 4
const ACTION_ADD := "ADD_TAG"
const ACTION_UPGRADE := "UPGRADE_TAG"


func catalog() -> Dictionary:
	return _load_catalog().duplicate(true)


func selection_preview(item, target_level: int, selection: Dictionary) -> Dictionary:
	if item == null:
		return _blocked("MISSING_ITEM")
	if str(item.physical_state) == "DESTROYED":
		return _blocked("ITEM_DESTROYED")
	if not EquipmentCatalogScript.is_precision_tag_eligible(item):
		return _blocked("PRECISION_TAG_WEAPON_ONLY")
	var catalog_data := _load_catalog()
	if catalog_data.is_empty():
		return _blocked("PRECISION_TAG_CATALOG_UNAVAILABLE")
	if not _catalog_is_valid(catalog_data):
		return _blocked("PRECISION_TAG_CATALOG_INVALID")
	if not PRECISION_TARGETS.has(target_level) or int(item.enhancement_level) != target_level - 1:
		return _blocked("INVALID_PRECISION_ENTRY")
	if item.has_initial_tag_backfill_pending():
		return _blocked("PRECISION_INITIAL_TAG_BACKFILL_PENDING")
	if item.has_unreadable_catalyst_affix():
		return _blocked("CATALYST_AFFIX_UNKNOWN_FAIL_CLOSED")
	var entries: Array = item.catalyst_tag_entries()
	if not _entries_are_valid(entries, catalog_data):
		return _blocked("INVALID_CATALYST_TAG_STATE")
	if not _milestone_state_is_valid(item, entries):
		return _blocked("INVALID_PRECISION_MILESTONE_STATE")
	if item.precision_milestone_is_resolved(target_level):
		return _blocked("PRECISION_MILESTONE_ALREADY_RESOLVED")
	return _selection_preview_from_action(item, target_level, selection, entries, catalog_data)


func apply_selection_success(item, target_level: int, selection: Dictionary) -> Dictionary:
	var preview := selection_preview(item, target_level, selection)
	if not bool(preview.get("allowed", false)):
		return _not_applied(str(preview.get("reason", "INVALID_PRECISION_SELECTION")))
	_apply_growth(item, preview)
	var result := preview.duplicate(true)
	result["applied"] = true
	result["reason"] = "OK"
	return result


# Migration is deliberately separate from an enhancement attempt: no roll, cost, or effect replay.
func backfill_initial_tag(item, selection: Dictionary) -> Dictionary:
	if item == null:
		return _not_applied("MISSING_ITEM")
	if not EquipmentCatalogScript.is_precision_tag_eligible(item):
		return _not_applied("PRECISION_TAG_WEAPON_ONLY")
	if not item.has_initial_tag_backfill_pending():
		return _not_applied("PRECISION_INITIAL_TAG_BACKFILL_NOT_PENDING")
	if item.has_unreadable_catalyst_affix() or not item.catalyst_tag_entries().is_empty():
		return _not_applied("INVALID_CATALYST_TAG_STATE")
	if not _pending_backfill_milestone_state_is_valid(item):
		return _not_applied("INVALID_PRECISION_MILESTONE_STATE")
	if int(item.enhancement_level) < 10:
		return _not_applied("PLACEHOLDER_LEVEL_INELIGIBLE")
	var catalog_data := _load_catalog()
	if catalog_data.is_empty() or not _catalog_is_valid(catalog_data):
		return _not_applied("PRECISION_TAG_CATALOG_INVALID")
	var resolved := _resolve_add(selection, [], catalog_data)
	if not bool(resolved.get("allowed", false)):
		return _not_applied(str(resolved.get("reason", "INVALID_PRECISION_SELECTION")))
	item.catalyst_affix["tag_entries"] = [_seed_entry(resolved, 10)]
	item.catalyst_affix["initial_tag_backfill_pending"] = false
	if not item.used_precision_milestones.has(10):
		item.used_precision_milestones.append(10)
	var result := resolved.duplicate(true)
	result["applied"] = true
	result["reason"] = "OK"
	result["target_level"] = 10
	result["stage_before"] = 0
	result["stage_after"] = 1
	result["cost_or_roll"] = "NONE"
	return result


func _selection_preview_from_action(item, target_level: int, selection: Dictionary, entries: Array, catalog_data: Dictionary) -> Dictionary:
	var action := str(selection.get("action", ""))
	if action == ACTION_ADD:
		var add_preview := _resolve_add(selection, entries, catalog_data)
		if not bool(add_preview.get("allowed", false)):
			return add_preview
		return _preview_with_item(item, add_preview, target_level, 0, 1)
	if action == ACTION_UPGRADE:
		if target_level == 10:
			return _blocked("PRECISION_ADD_REQUIRED")
		var upgrade_preview := _resolve_upgrade(selection, entries, catalog_data)
		if not bool(upgrade_preview.get("allowed", false)):
			return upgrade_preview
		return _preview_with_item(item, upgrade_preview, target_level, int(upgrade_preview["stage_before"]), int(upgrade_preview["stage_after"]))
	return _blocked("INVALID_PRECISION_ACTION")


func _resolve_add(selection: Dictionary, entries: Array, catalog_data: Dictionary) -> Dictionary:
	if not _has_exact_keys(selection, ["action", "lineage_id", "method_id"]) or str(selection.get("action", "")) != ACTION_ADD:
		return _blocked("INVALID_PRECISION_ACTION")
	if entries.size() >= MAX_ACTIVE_TAGS:
		return _blocked("PRECISION_TAG_CAP_REACHED")
	var lineage_id := str(selection["lineage_id"])
	var method_id := str(selection["method_id"])
	if lineage_id.is_empty():
		return _blocked("MISSING_CATALYST_LINEAGE")
	if method_id.is_empty():
		return _blocked("MISSING_PRECISION_METHOD")
	var lineage := _entry_by_id(catalog_data["lineages"], lineage_id)
	var method := _entry_by_id(catalog_data["methods"], method_id)
	if lineage.is_empty() or method.is_empty():
		return _blocked("INVALID_PRECISION_TAG_COMBINATION")
	var tag := _tag_by_pair(catalog_data["tags"], lineage_id, method_id)
	if tag.is_empty():
		return _blocked("INVALID_PRECISION_TAG_COMBINATION")
	var tag_id := str(tag["id"])
	for entry in entries:
		if str(entry.get("tag_id", "")) == tag_id:
			return _blocked("DUPLICATE_PRECISION_TAG")
	if not _tag_is_compatible_with_entries(tag, entries, catalog_data):
		return _blocked("INCOMPATIBLE_PRECISION_TAG")
	return _resolved(tag, lineage, method, ACTION_ADD)


func _resolve_upgrade(selection: Dictionary, entries: Array, catalog_data: Dictionary) -> Dictionary:
	if not _has_exact_keys(selection, ["action", "tag_id"]) or str(selection.get("action", "")) != ACTION_UPGRADE:
		return _blocked("INVALID_PRECISION_ACTION")
	var tag_id := str(selection["tag_id"])
	if tag_id.is_empty():
		return _blocked("MISSING_PRECISION_TAG")
	var entry := _entry_by_tag_id(entries, tag_id)
	if entry.is_empty():
		return _blocked("INACTIVE_PRECISION_TAG")
	var stage := int(entry.get("stage", 0))
	if stage >= MAX_TAG_STAGE:
		return _blocked("PRECISION_TAG_MASTERED")
	var tag := _entry_by_id(catalog_data["tags"], tag_id)
	if tag.is_empty():
		return _blocked("INVALID_CATALYST_TAG_STATE")
	var lineage := _entry_by_id(catalog_data["lineages"], str(tag["lineage_id"]))
	var method := _entry_by_id(catalog_data["methods"], str(tag["method_id"]))
	if lineage.is_empty() or method.is_empty():
		return _blocked("PRECISION_TAG_CATALOG_INVALID")
	var resolved := _resolved(tag, lineage, method, ACTION_UPGRADE)
	resolved["stage_before"] = stage
	resolved["stage_after"] = stage + 1
	return resolved


func _resolved(tag: Dictionary, lineage: Dictionary, method: Dictionary, action: String) -> Dictionary:
	var effect: Dictionary = method["effect"]
	return {
		"allowed": true,
		"reason": "OK",
		"action": action,
		"tag_id": str(tag["id"]),
		"tag_display_name_ko": str(tag["display_name_ko"]),
		"lineage_id": str(lineage["id"]),
		"lineage_display_name_ko": str(lineage["display_name_ko"]),
		"method_id": str(method["id"]),
		"method_display_name_ko": str(method["display_name_ko"]),
		"effect_axis": str(effect["axis"]),
		"effect_delta": int(effect["delta"]),
		"durability_delta": int(effect["durability_delta"]),
	}


func _preview_with_item(item, resolved: Dictionary, target_level: int, stage_before: int, stage_after: int) -> Dictionary:
	var axis := str(resolved["effect_axis"])
	var before_value := _axis_value(item, axis)
	var delta := int(resolved["effect_delta"])
	if axis == "WEIGHT_POINT" and before_value <= 0:
		return _blocked("PRECISION_EFFECT_UNAVAILABLE")
	var preview := resolved.duplicate(true)
	preview["target_level"] = target_level
	preview["stage_before"] = stage_before
	preview["stage_after"] = stage_after
	preview["before_value"] = before_value
	preview["after_value"] = maxi(0, before_value + delta) if axis == "WEIGHT_POINT" else before_value + delta
	return preview


func _apply_growth(item, preview: Dictionary) -> void:
	var entries: Array = item.catalyst_affix["tag_entries"]
	if str(preview["action"]) == ACTION_ADD:
		entries.append(_seed_entry(preview, int(preview["target_level"])))
	else:
		_advance_entry(entries, str(preview["tag_id"]), int(preview["stage_after"]), int(preview["target_level"]))
	_apply_method_effect_once(item, preview)
	item.used_precision_milestones.append(int(preview["target_level"]))


func _seed_entry(preview: Dictionary, target_level: int) -> Dictionary:
	return {
		"tag_id": str(preview["tag_id"]),
		"stage": 1,
		"created_milestone": target_level,
		"last_advanced_milestone": target_level,
	}


func _advance_entry(entries: Array, tag_id: String, stage_after: int, target_level: int) -> void:
	for index in entries.size():
		var entry: Dictionary = entries[index]
		if str(entry.get("tag_id", "")) == tag_id:
			entry["stage"] = stage_after
			entry["last_advanced_milestone"] = target_level
			entries[index] = entry
			return


func _apply_method_effect_once(item, preview: Dictionary) -> void:
	match str(preview["effect_axis"]):
		"RAW_ROLE_STAT":
			item.raw_role_stat = int(item.raw_role_stat) + int(preview["effect_delta"])
		"WEIGHT_POINT":
			item.weight_point = maxi(0, int(item.weight_point) + int(preview["effect_delta"]))


func _axis_value(item, axis: String) -> int:
	match axis:
		"RAW_ROLE_STAT": return int(item.raw_role_stat)
		"WEIGHT_POINT": return int(item.weight_point)
	return 0


func _entries_are_valid(entries: Array, catalog_data: Dictionary) -> bool:
	if entries.size() > MAX_ACTIVE_TAGS:
		return false
	var seen: Dictionary = {}
	for entry in entries:
		if not entry is Dictionary:
			return false
		var tag_id := str(entry.get("tag_id", ""))
		if tag_id.is_empty() or seen.has(tag_id) or _entry_by_id(catalog_data["tags"], tag_id).is_empty():
			return false
		seen[tag_id] = true
		if int(entry.get("stage", 0)) < 1 or int(entry.get("stage", 0)) > MAX_TAG_STAGE:
			return false
		if not PRECISION_TARGETS.has(int(entry.get("created_milestone", -1))) or not PRECISION_TARGETS.has(int(entry.get("last_advanced_milestone", -1))):
			return false
	return true


func _milestone_state_is_valid(item, entries: Array) -> bool:
	var used_milestones: Array = []
	var used_lookup: Dictionary = {}
	for raw_milestone in item.used_precision_milestones:
		if typeof(raw_milestone) != TYPE_INT:
			return false
		var milestone: int = raw_milestone
		if not PRECISION_TARGETS.has(milestone) or milestone > int(item.enhancement_level) or used_lookup.has(milestone):
			return false
		used_lookup[milestone] = true
		used_milestones.append(milestone)
	var expected_action_count := 0
	var assigned_milestones: Dictionary = {}
	var internal_action_counts: Array = []
	for entry in entries:
		var stage := int(entry["stage"])
		var created := int(entry["created_milestone"])
		var last_advanced := int(entry["last_advanced_milestone"])
		if not used_lookup.has(created) or not used_lookup.has(last_advanced) or created > last_advanced:
			return false
		if (stage == 1 and created != last_advanced) or (stage > 1 and created == last_advanced):
			return false
		if assigned_milestones.has(created):
			return false
		assigned_milestones[created] = true
		if last_advanced != created:
			if assigned_milestones.has(last_advanced):
				return false
			assigned_milestones[last_advanced] = true
		expected_action_count += stage
		internal_action_counts.append(maxi(0, stage - 2))
	if expected_action_count != used_milestones.size():
		return false
	return _can_assign_all_internal_actions(used_milestones, entries, internal_action_counts, 0, assigned_milestones)


# Persisted entries retain only their first and latest action. Reconstruct a legal
# history by assigning each stage III/IV entry its required distinct inner actions.
func _can_assign_all_internal_actions(used_milestones: Array, entries: Array, internal_action_counts: Array, entry_index: int, assigned_milestones: Dictionary) -> bool:
	if entry_index >= entries.size():
		return assigned_milestones.size() == used_milestones.size()
	var required_internal_actions := int(internal_action_counts[entry_index])
	if required_internal_actions == 0:
		return _can_assign_all_internal_actions(used_milestones, entries, internal_action_counts, entry_index + 1, assigned_milestones)
	var entry: Dictionary = entries[entry_index]
	var created := int(entry["created_milestone"])
	var last_advanced := int(entry["last_advanced_milestone"])
	var candidates: Array = []
	for milestone in used_milestones:
		if milestone > created and milestone < last_advanced and not assigned_milestones.has(milestone):
			candidates.append(milestone)
	candidates.sort()
	return _assign_entry_internal_actions(candidates, 0, required_internal_actions, used_milestones, entries, internal_action_counts, entry_index, assigned_milestones)


func _assign_entry_internal_actions(candidates: Array, candidate_index: int, remaining_actions: int, used_milestones: Array, entries: Array, internal_action_counts: Array, entry_index: int, assigned_milestones: Dictionary) -> bool:
	if remaining_actions == 0:
		return _can_assign_all_internal_actions(used_milestones, entries, internal_action_counts, entry_index + 1, assigned_milestones)
	if candidates.size() - candidate_index < remaining_actions:
		return false
	for index in range(candidate_index, candidates.size()):
		var milestone := int(candidates[index])
		if assigned_milestones.has(milestone):
			continue
		assigned_milestones[milestone] = true
		if _assign_entry_internal_actions(candidates, index + 1, remaining_actions - 1, used_milestones, entries, internal_action_counts, entry_index, assigned_milestones):
			return true
		assigned_milestones.erase(milestone)
	return false


func _pending_backfill_milestone_state_is_valid(item) -> bool:
	if item.used_precision_milestones.is_empty():
		return true
	return item.used_precision_milestones.size() == 1 and item.used_precision_milestones[0] == 10 and int(item.enhancement_level) >= 10


func _tag_is_compatible_with_entries(tag: Dictionary, entries: Array, catalog_data: Dictionary) -> bool:
	var compatible_ids: Array = tag["compatible_tag_ids"]
	for entry in entries:
		var active_id := str(entry["tag_id"])
		var active_tag := _entry_by_id(catalog_data["tags"], active_id)
		if not compatible_ids.has(active_id) or not (active_tag.get("compatible_tag_ids", []) as Array).has(str(tag["id"])):
			return false
	return true


func _load_catalog() -> Dictionary:
	var file := FileAccess.open(CATALOG_PATH, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func _catalog_is_valid(catalog_data: Dictionary) -> bool:
	if int(catalog_data.get("schema_version", 0)) != 2 or str(catalog_data.get("machine_owner", "")) != CATALYST_OWNER:
		return false
	if str(catalog_data.get("source_decision_id", "")) != "BS-ENHANCE-20260830-38" or not _matches_precision_targets(catalog_data.get("precision_targets", [])):
		return false
	var growth: Variant = catalog_data.get("tag_growth", {})
	var boundary: Variant = catalog_data.get("mechanical_boundary", {})
	var flow: Variant = catalog_data.get("selection_flow", {})
	if not growth is Dictionary or not boundary is Dictionary or not flow is Dictionary:
		return false
	if int(growth.get("max_active_tags", 0)) != MAX_ACTIVE_TAGS or int(growth.get("max_stage", 0)) != MAX_TAG_STAGE:
		return false
	if int(boundary.get("durability_delta_in_first_catalog", -1)) != 0 or flow.get("actions", []) != [ACTION_ADD, ACTION_UPGRADE]:
		return false
	var lineages: Variant = catalog_data.get("lineages", [])
	var methods: Variant = catalog_data.get("methods", [])
	var tags: Variant = catalog_data.get("tags", [])
	if not lineages is Array or not methods is Array or not tags is Array or lineages.size() != 2 or methods.size() != 2 or tags.size() != 4:
		return false
	var lineage_ids: Dictionary = {}
	for lineage in lineages:
		if not lineage is Dictionary or str(lineage.get("id", "")).is_empty() or str(lineage.get("display_name_ko", "")).is_empty() or lineage_ids.has(str(lineage.get("id", ""))):
			return false
		lineage_ids[str(lineage["id"])] = true
	var method_ids: Dictionary = {}
	for method in methods:
		if not method is Dictionary or str(method.get("id", "")).is_empty() or str(method.get("display_name_ko", "")).is_empty() or method_ids.has(str(method.get("id", ""))):
			return false
		var effect: Variant = method.get("effect", {})
		if not effect is Dictionary or not ["RAW_ROLE_STAT", "WEIGHT_POINT"].has(str(effect.get("axis", ""))) or int(effect.get("delta", 0)) == 0 or int(effect.get("durability_delta", -1)) != 0:
			return false
		method_ids[str(method["id"])] = true
	var tag_ids: Dictionary = {}
	var tag_coordinates: Dictionary = {}
	for tag in tags:
		if not tag is Dictionary:
			return false
		var tag_id := str(tag.get("id", ""))
		var compatible: Variant = tag.get("compatible_tag_ids", [])
		var coordinate := "%s|%s" % [str(tag.get("lineage_id", "")), str(tag.get("method_id", ""))]
		if tag_id.is_empty() or str(tag.get("display_name_ko", "")).is_empty() or tag_ids.has(tag_id) or tag_coordinates.has(coordinate) or str(tag.get("machine_owner", "")) != CATALYST_OWNER or not lineage_ids.has(str(tag.get("lineage_id", ""))) or not method_ids.has(str(tag.get("method_id", ""))) or not compatible is Array or compatible.size() != 3:
			return false
		tag_ids[tag_id] = true
		tag_coordinates[coordinate] = true
	for tag in tags:
		var ids: Array = tag["compatible_tag_ids"]
		if ids.has(str(tag["id"])):
			return false
		for compatible_id in ids:
			var compatible_tag := _entry_by_id(tags, str(compatible_id))
			if compatible_tag.is_empty() or not (compatible_tag.get("compatible_tag_ids", []) as Array).has(str(tag["id"])):
				return false
	return true


func _has_exact_keys(value: Dictionary, expected_keys: Array) -> bool:
	if value.size() != expected_keys.size():
		return false
	for key in expected_keys:
		if not value.has(key):
			return false
	return true


func _matches_precision_targets(value: Variant) -> bool:
	if not value is Array or value.size() != PRECISION_TARGETS.size():
		return false
	for index in PRECISION_TARGETS.size():
		if int(value[index]) != PRECISION_TARGETS[index]:
			return false
	return true


func _entry_by_id(entries: Array, entry_id: String) -> Dictionary:
	for entry in entries:
		if entry is Dictionary and str(entry.get("id", "")) == entry_id:
			return entry
	return {}


func _entry_by_tag_id(entries: Array, tag_id: String) -> Dictionary:
	for entry in entries:
		if entry is Dictionary and str(entry.get("tag_id", "")) == tag_id:
			return entry
	return {}


func _tag_by_pair(tags: Array, lineage_id: String, method_id: String) -> Dictionary:
	for tag in tags:
		if tag is Dictionary and str(tag.get("lineage_id", "")) == lineage_id and str(tag.get("method_id", "")) == method_id:
			return tag
	return {}


func _blocked(reason: String) -> Dictionary:
	return {"allowed": false, "reason": reason}


func _not_applied(reason: String) -> Dictionary:
	return {"applied": false, "reason": reason}
