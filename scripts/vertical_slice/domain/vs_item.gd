class_name VSItem
extends RefCounted

const SCHEMA_VERSION := 4
const BASE_MAX_DURABILITY := 5
const LedgerEntryScript = preload("res://scripts/vertical_slice/domain/vs_ledger_entry.gd")
const REQUIRED_FIELDS := [
	"schema_version",
	"uid",
	"birth_rng_seed",
	"primary_material_id",
	"equipment_group",
	"role_profile",
	"crafting_grade",
	"artistry",
	"raw_role_stat",
	"weight_point",
	"function_capacity",
	"functions",
	"grade_affix",
	"catalyst_affix",
	"chronicle_affix",
	"enhancement_level",
	"enhancement_failure_streak",
	"used_precision_milestones",
	"damage_state",
	"owner_id",
	"ledger",
	"highest_checkpoint",
	"current_durability",
	"max_durability",
	"base_max_durability",
	"repair_job_available",
	"enhancement_recovery_by_target",
	"overhaul_used",
	"max_enhancement_reached",
	"physical_state",
]
const CRAFTING_GRADES := [
	"CRAFT_NORMAL",
	"CRAFT_SUPERIOR",
	"CRAFT_FINE",
	"CRAFT_MASTERWORK",
	"CRAFT_LEGENDARY",
]
const PRIMARY_MATERIAL_IDS := ["iron", "silver", "meteor_iron"]
const LEGACY_DAMAGE_STATES := ["INTACT", "DAMAGED", "BROKEN", "RESTORED"]
const PHYSICAL_STATES := ["ACTIVE", "DESTROYED"]
const CHECKPOINT_FLOORS := [0, 10, 30, 60, 90]
const PRECISION_MILESTONES := [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
const CATALYST_SCHEMA_VERSION := 1
const CATALYST_TAG_IDS := [
	"TAG_EMBER_EDGE",
	"TAG_EMBER_LIGHT",
	"TAG_ANVIL_EDGE",
	"TAG_ANVIL_LIGHT",
]
const PRECISION_PLACEHOLDER_AFFIX := "PRECISION_KEYWORD_PENDING_CONTENT"

var schema_version: int = SCHEMA_VERSION
var uid: String = ""
var birth_rng_seed: int = 0
var primary_material_id: String = ""
var equipment_group: String = "SWORD"
var role_profile: String = "PHYSICAL_WEAPON_ATTACK"
var crafting_grade: String = "CRAFT_NORMAL"
var artistry: int = 0
var raw_role_stat: int = 0
var weight_point: int = 0
var function_capacity: int = 0
var functions: Array[String] = []
var grade_affix: String = ""
var catalyst_affix: Dictionary = empty_catalyst_affix()
var chronicle_affix: String = ""
var enhancement_level: int = 0
var enhancement_failure_streak: int = 0
var used_precision_milestones: Array[int] = []
# Transitional pre-release compatibility field. Current durability authority is
# current_durability/max_durability + physical_state.
var damage_state: String = "INTACT"
var owner_id: String = "PLAYER"
var ledger: Array[Dictionary] = []
var highest_checkpoint: int = 0
var current_durability: int = BASE_MAX_DURABILITY
var max_durability: int = BASE_MAX_DURABILITY
var base_max_durability: int = BASE_MAX_DURABILITY
var repair_job_available: bool = false
var enhancement_recovery_by_target: Dictionary = {}
var overhaul_used: bool = false
var max_enhancement_reached: bool = false
var physical_state: String = "ACTIVE"
var validation_errors: Array[String] = []


static func from_dict(value: Dictionary) -> VSItem:
	var item := VSItem.new()
	var source_schema_version := int(value.get("schema_version", 0))
	for field_name in REQUIRED_FIELDS:
		if source_schema_version >= SCHEMA_VERSION and not value.has(field_name):
			item.validation_errors.append("MISSING_REQUIRED_FIELD:%s" % field_name)

	item.schema_version = SCHEMA_VERSION
	item.uid = str(value.get("uid", ""))
	item.birth_rng_seed = int(value.get("birth_rng_seed", -1))
	item.primary_material_id = str(value.get("primary_material_id", ""))
	item.equipment_group = str(value.get("equipment_group", ""))
	item.role_profile = str(value.get("role_profile", ""))
	item.crafting_grade = str(value.get("crafting_grade", ""))
	item.artistry = int(value.get("artistry", -1))
	item.raw_role_stat = int(value.get("raw_role_stat", -1))
	item.weight_point = int(value.get("weight_point", -1))
	item.function_capacity = int(value.get("function_capacity", -1))
	item.grade_affix = str(value.get("grade_affix", ""))
	item.chronicle_affix = str(value.get("chronicle_affix", ""))
	item.enhancement_level = int(value.get("enhancement_level", -1))
	item.enhancement_failure_streak = int(value.get("enhancement_failure_streak", -1))
	item.damage_state = str(value.get("damage_state", ""))
	item.owner_id = str(value.get("owner_id", ""))
	item.highest_checkpoint = int(value.get("highest_checkpoint", -1))
	item.current_durability = int(value.get("current_durability", -1))
	item.max_durability = int(value.get("max_durability", -1))
	item.base_max_durability = int(value.get("base_max_durability", BASE_MAX_DURABILITY))
	item.repair_job_available = bool(value.get("repair_job_available", false))
	item.overhaul_used = bool(value.get("overhaul_used", false))
	item.max_enhancement_reached = bool(value.get("max_enhancement_reached", false))
	item.physical_state = str(value.get("physical_state", ""))

	var raw_functions: Variant = value.get("functions", [])
	if raw_functions is Array:
		for function_id in raw_functions:
			item.functions.append(str(function_id))
	else:
		item.validation_errors.append("INVALID_FIELD_TYPE:functions")

	var raw_milestones: Variant = value.get("used_precision_milestones", [])
	if raw_milestones is Array:
		for milestone in raw_milestones:
			item.used_precision_milestones.append(int(milestone))
	else:
		item.validation_errors.append("INVALID_FIELD_TYPE:used_precision_milestones")

	var raw_catalyst_affix: Variant = value.get("catalyst_affix", "")
	if source_schema_version >= SCHEMA_VERSION:
		if raw_catalyst_affix is Dictionary:
			item.catalyst_affix = _normalize_catalyst_affix(raw_catalyst_affix)
		else:
			item.validation_errors.append("INVALID_FIELD_TYPE:catalyst_affix")
			item.catalyst_affix = _unreadable_catalyst_affix(str(raw_catalyst_affix))
	elif source_schema_version == 3 or source_schema_version == 2:
		item.catalyst_affix = _migrate_legacy_catalyst_affix(raw_catalyst_affix, item)
	else:
		item.catalyst_affix = _unreadable_catalyst_affix(str(raw_catalyst_affix))

	var raw_recovery: Variant = value.get("enhancement_recovery_by_target", {})
	if raw_recovery is Dictionary:
		item.enhancement_recovery_by_target = raw_recovery.duplicate(true)
	else:
		item.validation_errors.append("INVALID_FIELD_TYPE:enhancement_recovery_by_target")

	var raw_ledger: Variant = value.get("ledger", [])
	if raw_ledger is Array:
		var expected_sequence := 1
		for raw_entry in raw_ledger:
			if not raw_entry is Dictionary:
				item.validation_errors.append("INVALID_LEDGER_ENTRY_TYPE")
				continue
			var entry = LedgerEntryScript.from_dict(raw_entry)
			for error_code in entry.validation_errors:
				item.validation_errors.append("LEDGER:%s" % error_code)
			if entry.sequence != expected_sequence:
				item.validation_errors.append("NON_CONTIGUOUS_LEDGER_SEQUENCE:%d" % entry.sequence)
			expected_sequence += 1
			item.ledger.append(entry.to_dict())
	else:
		item.validation_errors.append("INVALID_FIELD_TYPE:ledger")

	if source_schema_version == 2:
		item._migrate_schema_v2_durability()
	elif source_schema_version != 3 and source_schema_version != SCHEMA_VERSION:
		item.validation_errors.append("UNSUPPORTED_ITEM_SCHEMA:%d" % source_schema_version)
	item._validate_values()
	return item


func to_dict() -> Dictionary:
	return {
		"schema_version": schema_version,
		"uid": uid,
		"birth_rng_seed": birth_rng_seed,
		"primary_material_id": primary_material_id,
		"equipment_group": equipment_group,
		"role_profile": role_profile,
		"crafting_grade": crafting_grade,
		"artistry": artistry,
		"raw_role_stat": raw_role_stat,
		"weight_point": weight_point,
		"function_capacity": function_capacity,
		"functions": functions.duplicate(),
		"grade_affix": grade_affix,
		"catalyst_affix": catalyst_affix.duplicate(true),
		"chronicle_affix": chronicle_affix,
		"enhancement_level": enhancement_level,
		"enhancement_failure_streak": enhancement_failure_streak,
		"used_precision_milestones": used_precision_milestones.duplicate(),
		"damage_state": damage_state,
		"owner_id": owner_id,
		"ledger": ledger.duplicate(true),
		"highest_checkpoint": highest_checkpoint,
		"current_durability": current_durability,
		"max_durability": max_durability,
		"base_max_durability": base_max_durability,
		"repair_job_available": repair_job_available,
		"enhancement_recovery_by_target": enhancement_recovery_by_target.duplicate(true),
		"overhaul_used": overhaul_used,
		"max_enhancement_reached": max_enhancement_reached,
		"physical_state": physical_state,
	}


func append_ledger_entry(entry_value: Dictionary) -> Error:
	var entry = LedgerEntryScript.from_dict(entry_value)
	if not entry.validation_errors.is_empty():
		return ERR_INVALID_DATA
	var expected_sequence := ledger.size() + 1
	if entry.sequence < expected_sequence:
		return ERR_ALREADY_EXISTS
	if entry.sequence != expected_sequence:
		return ERR_INVALID_DATA
	ledger.append(entry.to_dict())
	return OK


static func empty_catalyst_affix() -> Dictionary:
	return {
		"schema_version": CATALYST_SCHEMA_VERSION,
		"tag_entries": [],
		"initial_tag_backfill_pending": false,
		"unreadable_legacy_affix": "",
	}


func catalyst_tag_entries() -> Array[Dictionary]:
	var entries: Array[Dictionary] = []
	var raw_entries: Variant = catalyst_affix.get("tag_entries", [])
	if raw_entries is Array:
		for raw_entry in raw_entries:
			if raw_entry is Dictionary:
				entries.append(raw_entry.duplicate(true))
	return entries


func has_initial_tag_backfill_pending() -> bool:
	return bool(catalyst_affix.get("initial_tag_backfill_pending", false))


func has_unreadable_catalyst_affix() -> bool:
	return not str(catalyst_affix.get("unreadable_legacy_affix", "")).is_empty()


func precision_milestone_is_resolved(target_level: int) -> bool:
	return used_precision_milestones.has(target_level)


func _validate_values() -> void:
	var uid_regex := RegEx.new()
	uid_regex.compile("^BSI-[0-9a-f]{32}$")
	if uid_regex.search(uid) == null:
		validation_errors.append("INVALID_UID_FORMAT")
	if birth_rng_seed < 0:
		validation_errors.append("INVALID_BIRTH_RNG_SEED")
	if not PRIMARY_MATERIAL_IDS.has(primary_material_id):
		validation_errors.append("INVALID_PRIMARY_MATERIAL:%s" % primary_material_id)
	if equipment_group != "SWORD":
		validation_errors.append("INVALID_EQUIPMENT_GROUP:%s" % equipment_group)
	if role_profile != "PHYSICAL_WEAPON_ATTACK":
		validation_errors.append("INVALID_ROLE_PROFILE:%s" % role_profile)
	if not CRAFTING_GRADES.has(crafting_grade):
		validation_errors.append("INVALID_CRAFTING_GRADE:%s" % crafting_grade)
	if artistry < 0:
		validation_errors.append("NEGATIVE_ARTISTRY")
	if raw_role_stat < 0:
		validation_errors.append("NEGATIVE_RAW_ROLE_STAT")
	if weight_point < 0:
		validation_errors.append("NEGATIVE_WEIGHT_POINT")
	if function_capacity < 0:
		validation_errors.append("NEGATIVE_FUNCTION_CAPACITY")
	if enhancement_level < 0 or enhancement_level > 100:
		validation_errors.append("INVALID_ENHANCEMENT_LEVEL")
	if enhancement_failure_streak < 0:
		validation_errors.append("NEGATIVE_FAILURE_STREAK")
	for milestone in used_precision_milestones:
		if not PRECISION_MILESTONES.has(milestone):
			validation_errors.append("INVALID_PRECISION_MILESTONE:%d" % milestone)
	_validate_catalyst_affix()
	if not LEGACY_DAMAGE_STATES.has(damage_state):
		validation_errors.append("INVALID_DAMAGE_STATE:%s" % damage_state)
	if not CHECKPOINT_FLOORS.has(highest_checkpoint):
		validation_errors.append("INVALID_HIGHEST_CHECKPOINT:%d" % highest_checkpoint)
	if base_max_durability != BASE_MAX_DURABILITY:
		validation_errors.append("INVALID_BASE_MAX_DURABILITY")
	if current_durability < 0 or current_durability > base_max_durability:
		validation_errors.append("INVALID_CURRENT_DURABILITY")
	if max_durability < 1 or max_durability > base_max_durability:
		validation_errors.append("INVALID_MAX_DURABILITY")
	if current_durability > max_durability:
		validation_errors.append("CURRENT_EXCEEDS_MAX")
	if not PHYSICAL_STATES.has(physical_state):
		validation_errors.append("INVALID_PHYSICAL_STATE:%s" % physical_state)
	var has_zero_durability := current_durability == 0
	if has_zero_durability and physical_state != "DESTROYED":
		validation_errors.append("ZERO_DURABILITY_REQUIRES_DESTROYED")
	if physical_state == "DESTROYED" and not has_zero_durability:
		validation_errors.append("DESTROYED_REQUIRES_ZERO_DURABILITY")
	if enhancement_level == 100 and not max_enhancement_reached:
		validation_errors.append("LEVEL_100_REQUIRES_MAX_ENHANCEMENT_REACHED")
	if max_enhancement_reached and enhancement_level != 100:
		validation_errors.append("MAX_ENHANCEMENT_REACHED_REQUIRES_LEVEL_100")
	if owner_id.is_empty():
		validation_errors.append("MISSING_OWNER_ID")


func effective_durability_ratio() -> float:
	if current_durability <= 0 or max_durability <= 0 or base_max_durability <= 0:
		return 0.0
	return minf(
		float(current_durability) / float(max_durability),
		float(max_durability) / float(base_max_durability)
	)


func effective_durability_state() -> String:
	if current_durability == 0:
		return "DESTROYED"
	var ratio := effective_durability_ratio()
	if is_equal_approx(ratio, 1.0):
		return "NORMAL"
	if ratio > 0.5:
		return "MINOR"
	return "MAJOR"


func apply_damage_event() -> bool:
	if current_durability <= 0:
		return false
	current_durability = maxi(0, current_durability - 1)
	repair_job_available = true
	if current_durability == 0:
		physical_state = "DESTROYED"
	return true


func _migrate_schema_v2_durability() -> void:
	var legacy_current := current_durability
	var legacy_max := max_durability
	base_max_durability = BASE_MAX_DURABILITY
	max_durability = clampi(int(ceil(float(legacy_max) * 5.0 / 100.0)), 1, BASE_MAX_DURABILITY)
	if legacy_current <= 0:
		current_durability = 0
		physical_state = "DESTROYED"
	else:
		current_durability = clampi(
			int(ceil(float(legacy_current) * 5.0 / 100.0)),
			1,
			max_durability
		)
		repair_job_available = false


static func _normalize_catalyst_affix(value: Dictionary) -> Dictionary:
	var normalized := empty_catalyst_affix()
	normalized["schema_version"] = int(value.get("schema_version", 0))
	normalized["initial_tag_backfill_pending"] = bool(value.get("initial_tag_backfill_pending", false))
	normalized["unreadable_legacy_affix"] = str(value.get("unreadable_legacy_affix", ""))
	var raw_entries: Variant = value.get("tag_entries", [])
	if raw_entries is Array:
		var entries: Array = []
		for raw_entry in raw_entries:
			if raw_entry is Dictionary:
				entries.append({
					"tag_id": str(raw_entry.get("tag_id", "")),
					"stage": int(raw_entry.get("stage", -1)),
					"created_milestone": int(raw_entry.get("created_milestone", -1)),
					"last_advanced_milestone": int(raw_entry.get("last_advanced_milestone", -1)),
				})
			else:
				entries.append(raw_entry)
		normalized["tag_entries"] = entries
	else:
		normalized["tag_entries"] = raw_entries
	return normalized


static func _unreadable_catalyst_affix(source_value: String) -> Dictionary:
	var unreadable := empty_catalyst_affix()
	unreadable["unreadable_legacy_affix"] = source_value
	return unreadable


static func _migrate_legacy_catalyst_affix(raw_value: Variant, item: VSItem) -> Dictionary:
	var legacy_affix := str(raw_value)
	if legacy_affix.is_empty():
		return empty_catalyst_affix()
	if legacy_affix == PRECISION_PLACEHOLDER_AFFIX:
		var pending := empty_catalyst_affix()
		pending["initial_tag_backfill_pending"] = true
		return pending
	if CATALYST_TAG_IDS.has(legacy_affix) and item.enhancement_level >= 10:
		if not item.used_precision_milestones.has(10):
			item.used_precision_milestones.append(10)
		var migrated := empty_catalyst_affix()
		migrated["tag_entries"] = [{
			"tag_id": legacy_affix,
			"stage": 1,
			"created_milestone": 10,
			"last_advanced_milestone": 10,
		}]
		return migrated
	return _unreadable_catalyst_affix(legacy_affix)


func _validate_catalyst_affix() -> void:
	if int(catalyst_affix.get("schema_version", 0)) != CATALYST_SCHEMA_VERSION:
		validation_errors.append("INVALID_CATALYST_SCHEMA_VERSION")
	var raw_entries: Variant = catalyst_affix.get("tag_entries", null)
	if not raw_entries is Array:
		validation_errors.append("INVALID_FIELD_TYPE:catalyst_affix.tag_entries")
		return
	if raw_entries.size() > 3:
		validation_errors.append("TOO_MANY_CATALYST_TAGS")
	var seen_tag_ids: Dictionary = {}
	for raw_entry in raw_entries:
		if not raw_entry is Dictionary:
			validation_errors.append("INVALID_CATALYST_TAG_ENTRY_TYPE")
			continue
		var tag_id := str(raw_entry.get("tag_id", ""))
		var stage := int(raw_entry.get("stage", -1))
		var created_milestone := int(raw_entry.get("created_milestone", -1))
		var last_advanced_milestone := int(raw_entry.get("last_advanced_milestone", -1))
		if not CATALYST_TAG_IDS.has(tag_id):
			validation_errors.append("INVALID_CATALYST_TAG_ID:%s" % tag_id)
		if seen_tag_ids.has(tag_id):
			validation_errors.append("DUPLICATE_CATALYST_TAG:%s" % tag_id)
		seen_tag_ids[tag_id] = true
		if stage < 1 or stage > 4:
			validation_errors.append("INVALID_CATALYST_TAG_STAGE:%s:%d" % [tag_id, stage])
		if not PRECISION_MILESTONES.has(created_milestone):
			validation_errors.append("INVALID_CATALYST_CREATED_MILESTONE:%s:%d" % [tag_id, created_milestone])
		if not PRECISION_MILESTONES.has(last_advanced_milestone):
			validation_errors.append("INVALID_CATALYST_LAST_ADVANCE_MILESTONE:%s:%d" % [tag_id, last_advanced_milestone])
		if not used_precision_milestones.has(created_milestone):
			validation_errors.append("CATALYST_CREATED_NOT_USED:%s:%d" % [tag_id, created_milestone])
		if not used_precision_milestones.has(last_advanced_milestone):
			validation_errors.append("CATALYST_LAST_ADVANCE_NOT_USED:%s:%d" % [tag_id, last_advanced_milestone])
		if last_advanced_milestone < created_milestone:
			validation_errors.append("CATALYST_ADVANCE_BEFORE_CREATION:%s" % tag_id)
	if has_initial_tag_backfill_pending() and not raw_entries.is_empty():
		validation_errors.append("PENDING_CATALYST_HAS_TAG_ENTRIES")
	if has_unreadable_catalyst_affix() and not raw_entries.is_empty():
		validation_errors.append("UNREADABLE_CATALYST_HAS_TAG_ENTRIES")
