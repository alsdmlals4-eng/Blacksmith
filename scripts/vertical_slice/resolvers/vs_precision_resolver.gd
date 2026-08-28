# Decision37 정밀강화 태그 표를 읽고 무기 귀속 단일 적용을 해석한다.
class_name VSPrecisionResolver
extends RefCounted

const CATALOG_PATH := "res://docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json"
const PLACEHOLDER_AFFIX := "PRECISION_KEYWORD_PENDING_CONTENT"
const CATALYST_OWNER := "CATALYST_AFFIX"


func catalog() -> Dictionary:
	return _load_catalog().duplicate(true)


func selection_preview(item, target_level: int, selection: Dictionary) -> Dictionary:
	if item == null:
		return _blocked("MISSING_ITEM")
	if str(item.physical_state) == "DESTROYED":
		return _blocked("ITEM_DESTROYED")
	if int(item.enhancement_level) != 9 or target_level != 10:
		return _blocked("INVALID_PRECISION_ENTRY")
	if not str(item.catalyst_affix).is_empty():
		return _affix_block(item)
	var resolved := _resolve_selection(selection)
	if not bool(resolved.get("allowed", false)):
		return resolved
	return _preview_with_item(item, resolved)


func apply_selection_success(item, selection: Dictionary) -> Dictionary:
	var preview := selection_preview(item, 10, selection)
	if not bool(preview.get("allowed", false)):
		return _not_applied(str(preview.get("reason", "INVALID_PRECISION_SELECTION")))
	_apply_resolved_selection(item, preview)
	return {
		"applied": true,
		"reason": "OK",
		"tag_id": str(preview["tag_id"]),
		"effect_axis": str(preview["effect_axis"]),
		"effect_delta": int(preview["effect_delta"]),
		"durability_delta": int(preview["durability_delta"]),
	}


func backfill_preview(item, selection: Dictionary) -> Dictionary:
	if item == null:
		return _blocked("MISSING_ITEM")
	if int(item.enhancement_level) < 10:
		return _blocked("PLACEHOLDER_LEVEL_INELIGIBLE")
	var affix := str(item.catalyst_affix)
	if affix != PLACEHOLDER_AFFIX:
		var affix_block := _affix_backfill_block(affix)
		return _blocked(str(affix_block.get("reason", "PRECISION_PLACEHOLDER_NOT_FOUND")))
	var resolved := _resolve_selection(selection)
	if not bool(resolved.get("allowed", false)):
		return resolved
	return _preview_with_item(item, resolved)


func backfill_placeholder(item, selection: Dictionary) -> Dictionary:
	var preview := backfill_preview(item, selection)
	if not bool(preview.get("allowed", false)):
		return _not_applied(str(preview.get("reason", "INVALID_PRECISION_SELECTION")))
	_apply_resolved_selection(item, preview)
	return {
		"applied": true,
		"reason": "OK",
		"cost_or_roll": "NONE",
		"tag_id": str(preview["tag_id"]),
		"effect_axis": str(preview["effect_axis"]),
		"effect_delta": int(preview["effect_delta"]),
		"durability_delta": int(preview["durability_delta"]),
	}


func _resolve_selection(selection: Dictionary) -> Dictionary:
	var lineage_id := str(selection.get("lineage_id", ""))
	if lineage_id.is_empty():
		return _blocked("MISSING_CATALYST_LINEAGE")
	var method_id := str(selection.get("method_id", ""))
	if method_id.is_empty():
		return _blocked("MISSING_PRECISION_METHOD")
	var catalog := _load_catalog()
	if catalog.is_empty():
		return _blocked("PRECISION_TAG_CATALOG_UNAVAILABLE")
	if str(catalog.get("machine_owner", "")) != CATALYST_OWNER:
		return _blocked("PRECISION_TAG_CATALOG_INVALID")
	var method := _entry_by_id(catalog.get("methods", []), method_id)
	if method.is_empty():
		return _blocked("INVALID_PRECISION_TAG_COMBINATION")
	if _entry_by_id(catalog.get("lineages", []), lineage_id).is_empty():
		return _blocked("INVALID_PRECISION_TAG_COMBINATION")
	for raw_tag in catalog.get("tags", []):
		if not raw_tag is Dictionary:
			continue
		var tag: Dictionary = raw_tag
		if str(tag.get("lineage_id", "")) == lineage_id and str(tag.get("method_id", "")) == method_id:
			if str(tag.get("machine_owner", "")) != CATALYST_OWNER:
				return _blocked("PRECISION_TAG_CATALOG_INVALID")
			var effect: Dictionary = method.get("effect", {})
			if effect.is_empty():
				return _blocked("PRECISION_TAG_CATALOG_INVALID")
			return {
				"allowed": true,
				"reason": "OK",
				"lineage_id": lineage_id,
				"method_id": method_id,
				"tag_id": str(tag.get("id", "")),
				"tag_display_name_ko": str(tag.get("display_name_ko", "")),
				"effect_axis": str(effect.get("axis", "")),
				"effect_delta": int(effect.get("delta", 0)),
				"durability_delta": int(catalog.get("mechanical_boundary", {}).get("durability_delta_in_first_catalog", 0)),
			}
	return _blocked("INVALID_PRECISION_TAG_COMBINATION")


func _preview_with_item(item, resolved: Dictionary) -> Dictionary:
	var axis := str(resolved.get("effect_axis", ""))
	var before_value := _axis_value(item, axis)
	var delta := int(resolved.get("effect_delta", 0))
	var after_value := maxi(0, before_value + delta) if axis == "WEIGHT_POINT" else before_value + delta
	var preview := resolved.duplicate(true)
	preview["before_value"] = before_value
	preview["after_value"] = after_value
	return preview


func _apply_resolved_selection(item, resolved: Dictionary) -> void:
	var axis := str(resolved.get("effect_axis", ""))
	var delta := int(resolved.get("effect_delta", 0))
	match axis:
		"RAW_ROLE_STAT":
			item.raw_role_stat = int(item.raw_role_stat) + delta
		"WEIGHT_POINT":
			item.weight_point = maxi(0, int(item.weight_point) + delta)
	item.catalyst_affix = str(resolved["tag_id"])


func _axis_value(item, axis: String) -> int:
	match axis:
		"RAW_ROLE_STAT":
			return int(item.raw_role_stat)
		"WEIGHT_POINT":
			return int(item.weight_point)
	return 0


func _load_catalog() -> Dictionary:
	var file := FileAccess.open(CATALOG_PATH, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func _entry_by_id(entries: Array, entry_id: String) -> Dictionary:
	for raw_entry in entries:
		if raw_entry is Dictionary and str(raw_entry.get("id", "")) == entry_id:
			return raw_entry
	return {}


func _affix_block(item) -> Dictionary:
	var affix := str(item.catalyst_affix)
	if affix == PLACEHOLDER_AFFIX:
		return _blocked("PRECISION_PLACEHOLDER_REQUIRES_BACKFILL")
	return _blocked("CATALYST_AFFIX_ALREADY_RESOLVED")


func _affix_backfill_block(affix: String) -> Dictionary:
	if affix.is_empty():
		return _not_applied("PRECISION_PLACEHOLDER_NOT_FOUND")
	if _is_known_tag(affix):
		return _not_applied("CATALYST_AFFIX_ALREADY_RESOLVED")
	return _not_applied("CATALYST_AFFIX_UNKNOWN_FAIL_CLOSED")


func _is_known_tag(tag_id: String) -> bool:
	for raw_tag in _load_catalog().get("tags", []):
		if raw_tag is Dictionary and str(raw_tag.get("id", "")) == tag_id:
			return true
	return false


func _blocked(reason: String) -> Dictionary:
	return {"allowed": false, "reason": reason}


func _not_applied(reason: String) -> Dictionary:
	return {"applied": false, "reason": reason}
