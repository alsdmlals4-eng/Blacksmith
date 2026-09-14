class_name VSCommissionCatalog
extends RefCounted

const CATALOG_PATH := "res://data/vertical_slice/commission_catalog_v1.json"
const CATALOG_ID := "BLACKSMITH_COMMISSION_CATALOG_V1"
const DEFINITION_VERSION := 1
const EquipmentCatalogScript = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
const ReplanTagRulesScript = preload("res://scripts/vertical_slice/domain/vs_replan_tag_rules.gd")
const REQUIRED_FIELDS := [
	"definition_id",
	"version",
	"equipment_id",
	"min_level",
	"recommended_level",
	"purpose",
	"purpose_axis",
	"purpose_rhythm",
	"risk_profile",
	"funding_origin",
	"ownership_mode",
	"reward_policy_id",
	"return_policy",
]
const STRING_FIELDS := [
	"definition_id",
	"equipment_id",
	"purpose",
	"purpose_axis",
	"purpose_rhythm",
	"risk_profile",
	"funding_origin",
	"ownership_mode",
	"reward_policy_id",
	"return_policy",
]
const EXPECTED_DEFINITION_IDS := [
	"IRON_SWORD_BASIC_V1",
	"IRON_SWORD_PURPOSE_V1",
	"IRON_SHIELD_BASIC_V1",
	"IRON_SHIELD_PURPOSE_V1",
	"IRON_BOW_BASIC_V1",
	"IRON_BOW_PURPOSE_V1",
	"IRON_ARMOR_BASIC_V1",
	"IRON_ARMOR_PURPOSE_V1",
	"IRON_HELMET_BASIC_V1",
	"IRON_HELMET_PURPOSE_V1",
]
const REWARD_POLICIES := {
	"COMMISSION_ECONOMY_TRIAL_V1": {
		"policy_id": "COMMISSION_ECONOMY_TRIAL_V1",
		"gold": 400,
		"reinforcement_material": 2,
		"chosen_catalyst": 1,
		"bonus": 0,
		"balance_status": "TRIAL_NOT_FINAL",
	},
}


static func all() -> Array[Dictionary]:
	var file := FileAccess.open(CATALOG_PATH, FileAccess.READ)
	if file == null:
		return []
	var payload: Variant = JSON.parse_string(file.get_as_text())
	if not payload is Dictionary:
		return []
	if not _valid_payload_header(payload):
		return []
	var definitions: Array[Dictionary] = []
	var raw_definitions: Variant = payload.get("definitions", [])
	if not raw_definitions is Array:
		return []
	for definition in raw_definitions:
		if not definition is Dictionary:
			return []
		definitions.append(definition.duplicate(true))
	if not validate_catalog(definitions).is_empty():
		return []
	return definitions


static func by_id(definition_id: String) -> Dictionary:
	for definition in all():
		if str(definition.get("definition_id", "")) == definition_id:
			return definition
	return {}


static func validate_definition(definition: Dictionary) -> Array[String]:
	var errors: Array[String] = []
	for field_name in REQUIRED_FIELDS:
		if not definition.has(field_name):
			errors.append("MISSING_FIELD:%s" % field_name)
	for raw_field_name in definition.keys():
		var field_name := str(raw_field_name)
		if field_name not in REQUIRED_FIELDS:
			errors.append("UNKNOWN_FIELD:%s" % field_name)
	for field_name in STRING_FIELDS:
		if definition.has(field_name) and typeof(definition[field_name]) != TYPE_STRING:
			errors.append("INVALID_FIELD_TYPE:%s" % field_name)
	if not errors.is_empty():
		return errors

	var definition_id := str(definition.definition_id)
	var equipment_id := str(definition.equipment_id)
	var purpose := str(definition.purpose)
	var axis := str(definition.purpose_axis)
	var rhythm := str(definition.purpose_rhythm)
	var risk_profile := str(definition.risk_profile)
	var funding_origin := str(definition.funding_origin)
	var ownership_mode := str(definition.ownership_mode)
	var reward_policy_id := str(definition.reward_policy_id)
	var return_policy := str(definition.return_policy)

	if definition_id.strip_edges().is_empty():
		errors.append("EMPTY_DEFINITION_ID")
	if not _is_integral_number(definition.version) or int(definition.version) != DEFINITION_VERSION:
		errors.append("UNKNOWN_DEFINITION_VERSION:%s" % str(definition.version))
	if EquipmentCatalogScript.by_id(equipment_id).is_empty():
		errors.append("UNKNOWN_EQUIPMENT:%s" % equipment_id)
	if purpose.strip_edges().is_empty():
		errors.append("EMPTY_PURPOSE")
	for level_field in ["min_level", "recommended_level"]:
		var value: Variant = definition.get(level_field)
		if not _is_integral_number(value) or int(value) < 0:
			errors.append("INVALID_LEVEL:%s" % level_field)
	if axis not in ["NONE", "OUTPUT", "HANDLING"]:
		errors.append("UNKNOWN_PURPOSE_AXIS:%s" % axis)
	if rhythm not in ["NONE", "BURST", "SUSTAIN"]:
		errors.append("UNKNOWN_PURPOSE_RHYTHM:%s" % rhythm)
	if risk_profile not in ["NONE", "HIGH"]:
		errors.append("UNKNOWN_RISK_PROFILE:%s" % risk_profile)
	if funding_origin != "COMMISSION_ESCROW":
		errors.append("UNKNOWN_FUNDING_ORIGIN:%s" % funding_origin)
	if ownership_mode != "SALE":
		errors.append("UNKNOWN_OWNERSHIP_MODE:%s" % ownership_mode)
	if not REWARD_POLICIES.has(reward_policy_id):
		errors.append("UNKNOWN_REWARD_POLICY:%s" % reward_policy_id)
	if return_policy != "CUSTOMER":
		errors.append("UNKNOWN_RETURN_POLICY:%s" % return_policy)

	if _is_integral_number(definition.min_level) and _is_integral_number(definition.recommended_level):
		var min_level := int(definition.min_level)
		var recommended_level := int(definition.recommended_level)
		var basic_profile := axis == "NONE" and rhythm == "NONE"
		var purpose_profile := axis in ["OUTPUT", "HANDLING"] and rhythm in ["BURST", "SUSTAIN"]
		if not basic_profile and not purpose_profile:
			errors.append("INVALID_PURPOSE_PROFILE")
		elif basic_profile and (min_level != 0 or recommended_level != 0 or risk_profile != "NONE"):
			errors.append("INVALID_BASIC_PROFILE")
		elif purpose_profile and (min_level != 10 or recommended_level != 10 or risk_profile != "HIGH"):
			errors.append("INVALID_PURPOSE_PROFILE")
		if min_level > recommended_level:
			errors.append("MIN_LEVEL_ABOVE_RECOMMENDED")
		if not EquipmentCatalogScript.by_id(equipment_id).is_empty():
			var suffix := "BASIC_V1" if basic_profile else "PURPOSE_V1"
			var expected_id := "%s_%s" % [equipment_id.to_upper(), suffix]
			if definition_id != expected_id:
				errors.append("UNKNOWN_DEFINITION_ID:%s" % definition_id)
	return errors


static func validate_catalog(definitions: Array[Dictionary]) -> Array[String]:
	var errors: Array[String] = []
	var seen_ids: Dictionary = {}
	for definition in definitions:
		errors.append_array(validate_definition(definition))
		var definition_id: Variant = definition.get("definition_id", "")
		if typeof(definition_id) != TYPE_STRING or str(definition_id).is_empty():
			continue
		if seen_ids.has(definition_id):
			errors.append("DUPLICATE_DEFINITION_ID:%s" % definition_id)
		else:
			seen_ids[definition_id] = true
	for definition_id in EXPECTED_DEFINITION_IDS:
		if not seen_ids.has(definition_id):
			errors.append("MISSING_DEFINITION_ID:%s" % definition_id)
	return errors


static func preview(definition: Dictionary, item) -> Dictionary:
	var validation_errors := validate_definition(definition)
	var equipment := EquipmentCatalogScript.by_id(str(definition.get("equipment_id", "")))
	var reasons: Array[String] = validation_errors.duplicate()
	if validation_errors.is_empty():
		if item == null:
			reasons.append("MISSING_ITEM")
		else:
			var item_equipment: Dictionary = EquipmentCatalogScript.by_item(item)
			if str(item_equipment.get("equipment_id", "")) != str(definition.equipment_id):
				reasons.append("EQUIPMENT_MISMATCH")
			if int(item.enhancement_level) < int(definition.min_level):
				reasons.append("LEVEL_BELOW_MINIMUM")
	var purpose_view := _purpose_view(definition)
	var reward_policy_id := str(definition.get("reward_policy_id", ""))
	var reward: Dictionary = REWARD_POLICIES.get(reward_policy_id, {}).duplicate(true)
	var ownership := {
		"funding_origin": str(definition.get("funding_origin", "")),
		"ownership_mode": str(definition.get("ownership_mode", "")),
		"return_policy": str(definition.get("return_policy", "")),
	}
	return {
		"allowed": reasons.is_empty(),
		"reasons": reasons,
		"equipment_name": str(equipment.get("display_name_ko", "")),
		"min_level": int(definition.get("min_level", 0)) if _is_integral_number(definition.get("min_level")) else 0,
		"recommended_level": int(definition.get("recommended_level", 0)) if _is_integral_number(definition.get("recommended_level")) else 0,
		"purpose": purpose_view,
		"reward": reward,
		"ownership": ownership,
	}


static func _valid_payload_header(payload: Dictionary) -> bool:
	if payload.size() != 3:
		return false
	if not _is_integral_number(payload.get("schema_version")) or int(payload.schema_version) != 1:
		return false
	if typeof(payload.get("catalog_id")) != TYPE_STRING or str(payload.catalog_id) != CATALOG_ID:
		return false
	return payload.has("definitions")


static func _purpose_view(definition: Dictionary) -> Dictionary:
	var axis := str(definition.get("purpose_axis", "NONE"))
	var rhythm := str(definition.get("purpose_rhythm", "NONE"))
	var tag_id := _recommended_tag_id(axis, rhythm)
	var tag_name := str(ReplanTagRulesScript.DISPLAY_NAMES_KO.get(tag_id, ""))
	var recommendation := "태그 없이 +0 제작으로 수행하는 기본 의뢰입니다."
	if not tag_id.is_empty():
		recommendation = "%s 태그를 추천합니다. %s·%s 목적 적합도를 높이지만 필수 조건은 아닙니다." % [
			tag_name,
			"성능" if axis == "OUTPUT" else "취급",
			"순간" if rhythm == "BURST" else "지속",
		]
	return {
		"description": str(definition.get("purpose", "")),
		"axis": axis,
		"rhythm": rhythm,
		"risk_profile": str(definition.get("risk_profile", "")),
		"tag_required": false,
		"recommended_tag_id": tag_id,
		"recommended_tag_name": tag_name,
		"recommendation": recommendation,
	}


static func _recommended_tag_id(axis: String, rhythm: String) -> String:
	for tag_id in ReplanTagRulesScript.TAGS:
		var identity: Array = ReplanTagRulesScript.TAGS[tag_id]
		if identity == [axis, rhythm]:
			return str(tag_id)
	return ""


static func _is_integral_number(value: Variant) -> bool:
	if typeof(value) not in [TYPE_INT, TYPE_FLOAT]:
		return false
	return is_finite(float(value)) and float(value) == floor(float(value))
