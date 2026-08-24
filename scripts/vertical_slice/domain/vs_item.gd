class_name VSItem
extends RefCounted

const SCHEMA_VERSION := 2
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
const PRECISION_MILESTONES := [10, 20, 30, 40, 50]

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
var catalyst_affix: String = ""
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
var current_durability: int = 100
var max_durability: int = 100
var enhancement_recovery_by_target: Dictionary = {}
var overhaul_used: bool = false
var max_enhancement_reached: bool = false
var physical_state: String = "ACTIVE"
var validation_errors: Array[String] = []


static func from_dict(value: Dictionary) -> VSItem:
	var item := VSItem.new()
	for field_name in REQUIRED_FIELDS:
		if not value.has(field_name):
			item.validation_errors.append("MISSING_REQUIRED_FIELD:%s" % field_name)

	item.schema_version = int(value.get("schema_version", 0))
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
	item.catalyst_affix = str(value.get("catalyst_affix", ""))
	item.chronicle_affix = str(value.get("chronicle_affix", ""))
	item.enhancement_level = int(value.get("enhancement_level", -1))
	item.enhancement_failure_streak = int(value.get("enhancement_failure_streak", -1))
	item.damage_state = str(value.get("damage_state", ""))
	item.owner_id = str(value.get("owner_id", ""))
	item.highest_checkpoint = int(value.get("highest_checkpoint", -1))
	item.current_durability = int(value.get("current_durability", -1))
	item.max_durability = int(value.get("max_durability", -1))
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
		"catalyst_affix": catalyst_affix,
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


func _validate_values() -> void:
	if schema_version != SCHEMA_VERSION:
		validation_errors.append("UNSUPPORTED_ITEM_SCHEMA:%d" % schema_version)
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
	if not LEGACY_DAMAGE_STATES.has(damage_state):
		validation_errors.append("INVALID_DAMAGE_STATE:%s" % damage_state)
	if not CHECKPOINT_FLOORS.has(highest_checkpoint):
		validation_errors.append("INVALID_HIGHEST_CHECKPOINT:%d" % highest_checkpoint)
	if current_durability < 0 or current_durability > 100:
		validation_errors.append("INVALID_CURRENT_DURABILITY")
	if max_durability < 0 or max_durability > 100:
		validation_errors.append("INVALID_MAX_DURABILITY")
	if current_durability > max_durability:
		validation_errors.append("CURRENT_EXCEEDS_MAX")
	if not PHYSICAL_STATES.has(physical_state):
		validation_errors.append("INVALID_PHYSICAL_STATE:%s" % physical_state)
	var has_zero_durability := current_durability == 0 or max_durability == 0
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
