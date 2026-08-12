class_name VSContentResultRecord
extends RefCounted

const SCHEMA_VERSION := 1
const RECORD_TYPE := "CONTENT_RESULT_V1"
const UID_PATTERN := "^BSI-[0-9a-f]{32}$"
const STATE_TOKEN_PATTERN := "^[A-Z0-9_]+$"
const REQUIRED_FIELDS := [
	"schema_version",
	"record_type",
	"event_id",
	"source_decision_id",
	"content_id",
	"customer_id",
	"occurred_at_game_day",
	"item_refs",
	"result_axes",
	"causal_reasons",
	"primary_next_action",
]
const ITEM_REF_REQUIRED_FIELDS := ["role", "uid"]
const ALLOWED_ITEM_ROLES := [
	"PRIMARY_ITEM",
	"BATCH_ITEM",
	"LEGACY_ITEM",
	"REPLACEMENT_ITEM",
]
const CONTENT_CONTRACTS := {
	"ADVENTURER_01": {
		"decision_id": "BS-CONTENT-20260811-01",
		"customer_id": "NADIA_VENN",
		"result_axes": [
			"EXPEDITION_RETURN_STATE",
			"RECOVERY_STATE",
			"ITEM_UID_LIFECYCLE_STATE",
		],
		"item_ref_policy": "SINGLE_PRIMARY_ITEM",
	},
	"ADVENTURER_02": {
		"decision_id": "BS-CONTENT-20260811-02",
		"customer_id": "TOREN_MARCH",
		"result_axes": [
			"JOURNEY_ARRIVAL_STATE",
			"ROUTE_EXPOSURE_STATE",
			"ITEM_UID_LIFECYCLE_STATE",
		],
		"item_ref_policy": "SINGLE_PRIMARY_ITEM",
	},
	"SOLDIER_01": {
		"decision_id": "BS-CONTENT-20260811-03",
		"customer_id": "MAREK_OLDEN",
		"result_axes": [
			"UNIT_MISSION_STATE",
			"STANDARD_ADOPTION_STATE",
			"BATCH_ITEM_LIFECYCLE_STATE",
		],
		"item_ref_policy": "BATCH_ITEMS_ONE_OR_MORE",
	},
	"COLLECTOR_01": {
		"decision_id": "BS-CONTENT-20260811-04",
		"customer_id": "ERSA_ROEN",
		"result_axes": [
			"EXHIBITION_RECEPTION_STATE",
			"EXHIBIT_THESIS_FIT_STATE",
			"ITEM_UID_PUBLIC_LEGACY_STATE",
		],
		"item_ref_policy": "SINGLE_PRIMARY_ITEM",
	},
	"GLADIATOR_01": {
		"decision_id": "BS-CONTENT-20260811-05",
		"customer_id": "CASSIA_BELLAN",
		"result_axes": [
			"ARENA_MATCH_STATE",
			"EQUIPMENT_CONTRIBUTION_STATE",
			"ITEM_UID_ARENA_LEGACY_STATE",
		],
		"item_ref_policy": "SINGLE_PRIMARY_ITEM",
	},
	"NOBLE_01": {
		"decision_id": "BS-CONTENT-20260811-06",
		"customer_id": "CEREMONIAL_NOBLE",
		"result_axes": [
			"CEREMONY_READINESS_STATE",
			"HEIRLOOM_TREATMENT_FIT_STATE",
			"ITEM_UID_DYNASTIC_LEGACY_STATE",
		],
		"item_ref_policy": "SINGLE_PRIMARY_ITEM",
	},
	"SOLDIER_02": {
		"decision_id": "BS-CONTENT-20260811-07",
		"customer_id": "LIANA_BERG",
		"result_axes": [
			"MISSION_DUTY_STATE",
			"COMMANDER_RETURN_STATE",
			"ITEM_UID_FIELD_LEGACY_STATE",
		],
		"item_ref_policy": "SINGLE_PRIMARY_ITEM",
	},
	"COLLECTOR_02": {
		"decision_id": "BS-CONTENT-20260811-08",
		"customer_id": "SEDRIC_VAEL",
		"result_axes": [
			"ARCHIVE_ACCESSION_STATE",
			"PROVENANCE_DOCUMENTATION_STATE",
			"ITEM_UID_CUSTODY_LEGACY_STATE",
		],
		"item_ref_policy": "SINGLE_PRIMARY_ITEM",
	},
	"GLADIATOR_02": {
		"decision_id": "BS-CONTENT-20260811-09",
		"customer_id": "KYLE_VAREN",
		"result_axes": [
			"VETERAN_RETURN_STATE",
			"EQUIPMENT_CONTINUITY_STATE",
			"ITEM_UID_LINEAGE_STATE",
		],
		"item_ref_policy": "LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT",
	},
}

var schema_version: int = SCHEMA_VERSION
var record_type: String = RECORD_TYPE
var event_id: String = ""
var source_decision_id: String = ""
var content_id: String = ""
var customer_id: String = ""
var occurred_at_game_day: int = 0
var item_refs: Array[Dictionary] = []
var result_axes: Dictionary = {}
var causal_reasons: Array[String] = []
var primary_next_action: String = ""
var validation_errors: Array[String] = []


static func from_dict(value: Dictionary) -> VSContentResultRecord:
	var record := VSContentResultRecord.new()
	for field_name in REQUIRED_FIELDS:
		if not value.has(field_name):
			record.validation_errors.append("MISSING_REQUIRED_FIELD:%s" % field_name)
	for raw_field_name in value.keys():
		var field_name := str(raw_field_name)
		if not REQUIRED_FIELDS.has(field_name):
			record.validation_errors.append("UNKNOWN_FIELD:%s" % field_name)

	record.schema_version = int(value.get("schema_version", 0))
	record.record_type = str(value.get("record_type", ""))
	record.event_id = str(value.get("event_id", ""))
	record.source_decision_id = str(value.get("source_decision_id", ""))
	record.content_id = str(value.get("content_id", ""))
	record.customer_id = str(value.get("customer_id", ""))
	record.occurred_at_game_day = int(value.get("occurred_at_game_day", 0))

	record._read_item_refs(value.get("item_refs", []))
	record._read_result_axes(value.get("result_axes", {}))
	record._read_causal_reasons(value.get("causal_reasons", []))

	var raw_next_action: Variant = value.get("primary_next_action", "")
	if raw_next_action is String:
		record.primary_next_action = raw_next_action
	else:
		record.validation_errors.append("INVALID_FIELD_TYPE:primary_next_action")
		record.primary_next_action = str(raw_next_action)

	record._validate_values()
	return record


func to_dict() -> Dictionary:
	return {
		"schema_version": schema_version,
		"record_type": record_type,
		"event_id": event_id,
		"source_decision_id": source_decision_id,
		"content_id": content_id,
		"customer_id": customer_id,
		"occurred_at_game_day": occurred_at_game_day,
		"item_refs": item_refs.duplicate(true),
		"result_axes": result_axes.duplicate(true),
		"causal_reasons": causal_reasons.duplicate(),
		"primary_next_action": primary_next_action,
	}


func _read_item_refs(raw_item_refs: Variant) -> void:
	if not raw_item_refs is Array:
		validation_errors.append("INVALID_FIELD_TYPE:item_refs")
		return

	for raw_item_ref in raw_item_refs:
		if not raw_item_ref is Dictionary:
			validation_errors.append("INVALID_ITEM_REF_TYPE")
			continue
		for field_name in ITEM_REF_REQUIRED_FIELDS:
			if not raw_item_ref.has(field_name):
				validation_errors.append("MISSING_ITEM_REF_FIELD:%s" % field_name)
		for raw_field_name in raw_item_ref.keys():
			var field_name := str(raw_field_name)
			if not ITEM_REF_REQUIRED_FIELDS.has(field_name):
				validation_errors.append("UNKNOWN_ITEM_REF_FIELD:%s" % field_name)

		var raw_role: Variant = raw_item_ref.get("role", "")
		var raw_uid: Variant = raw_item_ref.get("uid", "")
		if not raw_role is String:
			validation_errors.append("INVALID_ITEM_REF_FIELD_TYPE:role")
		if not raw_uid is String:
			validation_errors.append("INVALID_ITEM_REF_FIELD_TYPE:uid")
		item_refs.append({
			"role": str(raw_role),
			"uid": str(raw_uid),
		})


func _read_result_axes(raw_result_axes: Variant) -> void:
	if not raw_result_axes is Dictionary:
		validation_errors.append("INVALID_FIELD_TYPE:result_axes")
		return

	for raw_axis_name in raw_result_axes.keys():
		var axis_name := str(raw_axis_name)
		var raw_axis_value: Variant = raw_result_axes[raw_axis_name]
		if not raw_axis_value is String:
			validation_errors.append("INVALID_RESULT_AXIS_VALUE:%s" % axis_name)
		result_axes[axis_name] = str(raw_axis_value)


func _read_causal_reasons(raw_causal_reasons: Variant) -> void:
	if not raw_causal_reasons is Array:
		validation_errors.append("INVALID_FIELD_TYPE:causal_reasons")
		return

	for raw_reason in raw_causal_reasons:
		if not raw_reason is String:
			validation_errors.append("INVALID_CAUSAL_REASON:%s" % str(raw_reason))
		causal_reasons.append(str(raw_reason))


func _validate_values() -> void:
	if schema_version != SCHEMA_VERSION:
		validation_errors.append("UNSUPPORTED_CONTENT_RESULT_SCHEMA:%d" % schema_version)
	if record_type != RECORD_TYPE:
		validation_errors.append("INVALID_RECORD_TYPE:%s" % record_type)
	if event_id.is_empty():
		validation_errors.append("MISSING_EVENT_ID")
	if occurred_at_game_day < 1:
		validation_errors.append("INVALID_OCCURRED_AT_GAME_DAY")

	var contract: Dictionary = CONTENT_CONTRACTS.get(content_id, {})
	if contract.is_empty():
		validation_errors.append("UNKNOWN_CONTENT_ID:%s" % content_id)
	else:
		if source_decision_id != str(contract["decision_id"]):
			validation_errors.append("SOURCE_DECISION_MISMATCH")
		if customer_id != str(contract["customer_id"]):
			validation_errors.append("CUSTOMER_ID_MISMATCH")
		_validate_result_axis_set(contract["result_axes"])
		_validate_item_ref_policy(str(contract["item_ref_policy"]))

	_validate_item_refs()
	_validate_result_axis_values()
	_validate_causal_reasons()
	if not _matches_token(primary_next_action):
		validation_errors.append("INVALID_PRIMARY_NEXT_ACTION")


func _validate_result_axis_set(expected_axes_value: Variant) -> void:
	var expected_axes: Array = []
	if expected_axes_value is Array:
		expected_axes = expected_axes_value.duplicate()
	var actual_axes: Array = result_axes.keys()
	expected_axes.sort()
	actual_axes.sort()
	if actual_axes != expected_axes:
		validation_errors.append("RESULT_AXIS_SET_MISMATCH")


func _validate_item_refs() -> void:
	var seen_uids := {}
	for item_ref in item_refs:
		var role := str(item_ref.get("role", ""))
		var uid := str(item_ref.get("uid", ""))
		if not ALLOWED_ITEM_ROLES.has(role):
			validation_errors.append("INVALID_ITEM_ROLE:%s" % role)
		if not _matches(UID_PATTERN, uid):
			validation_errors.append("INVALID_ITEM_UID:%s" % uid)
		if seen_uids.has(uid):
			validation_errors.append("DUPLICATE_ITEM_UID")
		else:
			seen_uids[uid] = true


func _validate_item_ref_policy(policy: String) -> void:
	match policy:
		"SINGLE_PRIMARY_ITEM":
			if item_refs.size() != 1 or str(item_refs[0].get("role", "")) != "PRIMARY_ITEM":
				validation_errors.append("SINGLE_PRIMARY_ITEM_REQUIRED")
		"BATCH_ITEMS_ONE_OR_MORE":
			var valid_batch := not item_refs.is_empty()
			for item_ref in item_refs:
				if str(item_ref.get("role", "")) != "BATCH_ITEM":
					valid_batch = false
			if not valid_batch:
				validation_errors.append("BATCH_ITEMS_ONE_OR_MORE_REQUIRED")
		"LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT":
			var legacy_count := 0
			var replacement_count := 0
			for item_ref in item_refs:
				match str(item_ref.get("role", "")):
					"LEGACY_ITEM":
						legacy_count += 1
					"REPLACEMENT_ITEM":
						replacement_count += 1
			if legacy_count != 1 or replacement_count > 1 or item_refs.size() != legacy_count + replacement_count:
				validation_errors.append("LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT_REQUIRED")
		_:
			validation_errors.append("UNKNOWN_ITEM_REF_POLICY:%s" % policy)


func _validate_result_axis_values() -> void:
	for axis_name in result_axes.keys():
		var axis_value := str(result_axes[axis_name])
		if not _matches_token(axis_value):
			var error_code := "INVALID_RESULT_AXIS_VALUE:%s" % str(axis_name)
			if not validation_errors.has(error_code):
				validation_errors.append(error_code)


func _validate_causal_reasons() -> void:
	if causal_reasons.size() < 2 or causal_reasons.size() > 4:
		validation_errors.append("INVALID_CAUSAL_REASON_COUNT")
	var seen_reasons := {}
	for reason in causal_reasons:
		if not _matches_token(reason):
			var error_code := "INVALID_CAUSAL_REASON:%s" % reason
			if not validation_errors.has(error_code):
				validation_errors.append(error_code)
		if seen_reasons.has(reason):
			validation_errors.append("DUPLICATE_CAUSAL_REASON")
		else:
			seen_reasons[reason] = true


static func _matches_token(value: String) -> bool:
	return _matches(STATE_TOKEN_PATTERN, value)


static func _matches(pattern: String, value: String) -> bool:
	var regex := RegEx.new()
	if regex.compile(pattern) != OK:
		return false
	return regex.search(value) != null
