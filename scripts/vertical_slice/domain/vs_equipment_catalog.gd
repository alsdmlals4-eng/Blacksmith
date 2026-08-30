# The single current source for selectable first-forge equipment identity and visual consumers.
class_name VSEquipmentCatalog
extends RefCounted

const CATALOG_PATH := "res://data/vertical_slice/vertical_slice_equipment_catalog_20260830.json"

static var _cached_payload: Dictionary = {}


static func all() -> Array[Dictionary]:
	var entries: Array[Dictionary] = []
	var raw_entries: Variant = _payload().get("equipment", [])
	if raw_entries is Array:
		for raw_entry in raw_entries:
			if raw_entry is Dictionary:
				entries.append(raw_entry.duplicate(true))
	return entries


static func by_id(equipment_id: String) -> Dictionary:
	for entry in all():
		if str(entry.get("equipment_id", "")) == equipment_id:
			return entry
	return {}


static func by_identity(equipment_group: String, role_profile: String) -> Dictionary:
	for entry in all():
		if str(entry.get("equipment_group", "")) == equipment_group and str(entry.get("role_profile", "")) == role_profile:
			return entry
	return {}


static func by_item(item) -> Dictionary:
	if item == null:
		return {}
	return by_identity(str(item.equipment_group), str(item.role_profile))


static func has_equipment_group(equipment_group: String) -> bool:
	for entry in all():
		if str(entry.get("equipment_group", "")) == equipment_group:
			return true
	return false


static func is_valid_identity(equipment_group: String, role_profile: String) -> bool:
	return not by_identity(equipment_group, role_profile).is_empty()


static func is_precision_tag_eligible(item) -> bool:
	return bool(by_item(item).get("precision_tag_eligible", false))


static func _payload() -> Dictionary:
	if not _cached_payload.is_empty():
		return _cached_payload
	var file := FileAccess.open(CATALOG_PATH, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary:
		return {}
	_cached_payload = parsed.duplicate(true)
	return _cached_payload
