extends "res://addons/gut/test.gd"

const RecordScript = preload("res://scripts/vertical_slice/domain/vs_content_result_record.gd")

const UID_A := "BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
const UID_B := "BSI-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
const UID_C := "BSI-cccccccccccccccccccccccccccccccc"
const UID_D := "BSI-dddddddddddddddddddddddddddddddd"


func _nadia_record() -> Dictionary:
	return {
		"schema_version": 1,
		"record_type": "CONTENT_RESULT_V1",
		"event_id": "nadia-result-001",
		"source_decision_id": "BS-CONTENT-20260811-01",
		"content_id": "ADVENTURER_01",
		"customer_id": "NADIA_VENN",
		"occurred_at_game_day": 4,
		"item_refs": [
			{"role": "PRIMARY_ITEM", "uid": UID_A},
		],
		"result_axes": {
			"EXPEDITION_RETURN_STATE": "RETURNED",
			"RECOVERY_STATE": "PARTIAL_RECOVERY",
			"ITEM_UID_LIFECYCLE_STATE": "DAMAGED_RETURN",
		},
		"causal_reasons": ["LOAD_GATE_PASSED", "UTILITY_MATCHED"],
		"primary_next_action": "REPAIR_ITEM",
	}


func _marek_record() -> Dictionary:
	var value := _nadia_record()
	value["event_id"] = "marek-result-001"
	value["source_decision_id"] = "BS-CONTENT-20260811-03"
	value["content_id"] = "SOLDIER_01"
	value["customer_id"] = "MAREK_OLDEN"
	value["item_refs"] = [
		{"role": "BATCH_ITEM", "uid": UID_A},
		{"role": "BATCH_ITEM", "uid": UID_B},
	]
	value["result_axes"] = {
		"UNIT_MISSION_STATE": "COMPLETED",
		"STANDARD_ADOPTION_STATE": "CONDITIONAL",
		"BATCH_ITEM_LIFECYCLE_STATE": "MIXED_RETURN",
	}
	return value


func _kyle_record(with_replacement: bool = true) -> Dictionary:
	var value := _nadia_record()
	value["event_id"] = "kyle-result-001"
	value["source_decision_id"] = "BS-CONTENT-20260811-09"
	value["content_id"] = "GLADIATOR_02"
	value["customer_id"] = "KYLE_VAREN"
	value["item_refs"] = [
		{"role": "LEGACY_ITEM", "uid": UID_C},
	]
	if with_replacement:
		value["item_refs"].append(
			{"role": "REPLACEMENT_ITEM", "uid": UID_D}
		)
	value["result_axes"] = {
		"VETERAN_RETURN_STATE": "RETURNED",
		"EQUIPMENT_CONTINUITY_STATE": (
			"RETIRE_AND_REPLACE" if with_replacement else "KEEP_IN_SERVICE"
		),
		"ITEM_UID_LINEAGE_STATE": (
			"OLD_RETIRED_NEW_ASSIGNED" if with_replacement else "LEGACY_CONTINUES"
		),
	}
	return value


func test_valid_single_item_record_round_trips() -> void:
	var value := _nadia_record()
	var record = RecordScript.from_dict(value)
	assert_true(record.validation_errors.is_empty(), str(record.validation_errors))
	assert_eq(record.to_dict(), value)


func test_wrong_decision_and_customer_tuple_is_rejected() -> void:
	var value := _nadia_record()
	value["source_decision_id"] = "BS-CONTENT-20260811-02"
	value["customer_id"] = "TOREN_MARCH"
	var record = RecordScript.from_dict(value)
	assert_true(record.validation_errors.has("SOURCE_DECISION_MISMATCH"))
	assert_true(record.validation_errors.has("CUSTOMER_ID_MISMATCH"))


func test_wrong_axis_set_is_rejected() -> void:
	var value := _nadia_record()
	var axes: Dictionary = value["result_axes"]
	axes.erase("RECOVERY_STATE")
	axes["SCORE"] = "HIGH"
	var record = RecordScript.from_dict(value)
	assert_true(record.validation_errors.has("RESULT_AXIS_SET_MISMATCH"))


func test_result_axis_value_must_be_uppercase_token() -> void:
	var value := _nadia_record()
	value["result_axes"]["RECOVERY_STATE"] = "partial recovery"
	var record = RecordScript.from_dict(value)
	assert_true(record.validation_errors.has("INVALID_RESULT_AXIS_VALUE:RECOVERY_STATE"))


func test_reason_count_and_uniqueness_are_enforced() -> void:
	var too_few := _nadia_record()
	too_few["causal_reasons"] = ["ONE_REASON"]
	var too_few_record = RecordScript.from_dict(too_few)
	assert_true(too_few_record.validation_errors.has("INVALID_CAUSAL_REASON_COUNT"))

	var too_many := _nadia_record()
	too_many["causal_reasons"] = ["A", "B", "C", "D", "E"]
	var too_many_record = RecordScript.from_dict(too_many)
	assert_true(too_many_record.validation_errors.has("INVALID_CAUSAL_REASON_COUNT"))

	var duplicate_reasons := _nadia_record()
	duplicate_reasons["causal_reasons"] = ["SAME_REASON", "SAME_REASON"]
	var duplicate_record = RecordScript.from_dict(duplicate_reasons)
	assert_true(duplicate_record.validation_errors.has("DUPLICATE_CAUSAL_REASON"))


func test_primary_next_action_must_be_uppercase_token() -> void:
	var value := _nadia_record()
	value["primary_next_action"] = "repair item"
	var record = RecordScript.from_dict(value)
	assert_true(record.validation_errors.has("INVALID_PRIMARY_NEXT_ACTION"))


func test_invalid_uid_is_rejected() -> void:
	var value := _nadia_record()
	value["item_refs"][0]["uid"] = "bad-uid"
	var record = RecordScript.from_dict(value)
	assert_true(record.validation_errors.has("INVALID_ITEM_UID:bad-uid"))


func test_single_item_policy_requires_exact_primary_item() -> void:
	var missing := _nadia_record()
	missing["item_refs"] = []
	var missing_record = RecordScript.from_dict(missing)
	assert_true(missing_record.validation_errors.has("SINGLE_PRIMARY_ITEM_REQUIRED"))

	var wrong_role := _nadia_record()
	wrong_role["item_refs"][0]["role"] = "BATCH_ITEM"
	var wrong_role_record = RecordScript.from_dict(wrong_role)
	assert_true(wrong_role_record.validation_errors.has("SINGLE_PRIMARY_ITEM_REQUIRED"))


func test_batch_accepts_unique_items_and_rejects_duplicate_uid() -> void:
	var valid = RecordScript.from_dict(_marek_record())
	assert_true(valid.validation_errors.is_empty(), str(valid.validation_errors))

	var duplicate_batch := _marek_record()
	duplicate_batch["item_refs"][1]["uid"] = UID_A
	var duplicate_record = RecordScript.from_dict(duplicate_batch)
	assert_true(duplicate_record.validation_errors.has("DUPLICATE_ITEM_UID"))


func test_batch_requires_batch_roles() -> void:
	var value := _marek_record()
	value["item_refs"][1]["role"] = "PRIMARY_ITEM"
	var record = RecordScript.from_dict(value)
	assert_true(record.validation_errors.has("BATCH_ITEMS_ONE_OR_MORE_REQUIRED"))


func test_kyle_keep_and_distinct_replacement_are_valid() -> void:
	var keep = RecordScript.from_dict(_kyle_record(false))
	assert_true(keep.validation_errors.is_empty(), str(keep.validation_errors))

	var replace = RecordScript.from_dict(_kyle_record(true))
	assert_true(replace.validation_errors.is_empty(), str(replace.validation_errors))


func test_kyle_replacement_uid_must_differ_from_legacy_uid() -> void:
	var value := _kyle_record(true)
	value["item_refs"][1]["uid"] = UID_C
	var record = RecordScript.from_dict(value)
	assert_true(record.validation_errors.has("DUPLICATE_ITEM_UID"))


func test_kyle_requires_legacy_item_and_limits_replacement() -> void:
	var missing_legacy := _kyle_record(true)
	missing_legacy["item_refs"] = [
		{"role": "REPLACEMENT_ITEM", "uid": UID_D},
	]
	var missing_record = RecordScript.from_dict(missing_legacy)
	assert_true(
		missing_record.validation_errors.has(
			"LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT_REQUIRED"
		)
	)

	var extra_replacement := _kyle_record(true)
	extra_replacement["item_refs"].append(
		{"role": "REPLACEMENT_ITEM", "uid": UID_B}
	)
	var extra_record = RecordScript.from_dict(extra_replacement)
	assert_true(
		extra_record.validation_errors.has(
			"LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT_REQUIRED"
		)
	)


func test_unknown_record_and_item_ref_fields_are_rejected() -> void:
	var unknown_record := _nadia_record()
	unknown_record["total_score"] = 99
	var record = RecordScript.from_dict(unknown_record)
	assert_true(record.validation_errors.has("UNKNOWN_FIELD:total_score"))

	var unknown_ref := _nadia_record()
	unknown_ref["item_refs"][0]["history_transfer"] = true
	var ref_record = RecordScript.from_dict(unknown_ref)
	assert_true(ref_record.validation_errors.has("UNKNOWN_ITEM_REF_FIELD:history_transfer"))


func test_missing_required_field_is_reported() -> void:
	var value := _nadia_record()
	value.erase("primary_next_action")
	var record = RecordScript.from_dict(value)
	assert_true(
		record.validation_errors.has("MISSING_REQUIRED_FIELD:primary_next_action")
	)
