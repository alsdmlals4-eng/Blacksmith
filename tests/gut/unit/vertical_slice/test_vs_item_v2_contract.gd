extends "res://addons/gut/test.gd"

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _item() -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-0123456789abcdef0123456789abcdef"
	item.birth_rng_seed = 712345
	item.primary_material_id = "iron"
	item.crafting_grade = "CRAFT_MASTERWORK"
	item.artistry = 7
	item.raw_role_stat = 15
	item.weight_point = 15
	item.grade_affix = "MASTERWORK_EDGE"
	return item


func test_current_item_serializes_five_slot_durability_and_repair_job() -> void:
	var serialized: Dictionary = _item().to_dict()
	assert_eq(serialized["schema_version"], 3)
	assert_eq(serialized["base_max_durability"], 5)
	assert_eq(serialized["current_durability"], 5)
	assert_eq(serialized["max_durability"], 5)
	assert_true(serialized.has("repair_job_available"))


func test_v2_item_migrates_to_current_five_slot_authority() -> void:
	var legacy: Dictionary = _item().to_dict()
	legacy["schema_version"] = 2
	legacy.erase("base_max_durability")
	legacy.erase("repair_job_available")
	legacy["current_durability"] = 80
	legacy["max_durability"] = 100
	var restored = ItemScript.from_dict(legacy)
	assert_true(restored.validation_errors.is_empty())
	assert_eq(restored.schema_version, 3)
	assert_eq(restored.base_max_durability, 5)
	assert_eq(restored.current_durability, 4)
	assert_eq(restored.max_durability, 5)
	assert_false(restored.repair_job_available)


func test_only_plus_10_is_a_valid_precision_milestone() -> void:
	var item = _item()
	item.used_precision_milestones.assign([10])
	assert_true(ItemScript.from_dict(item.to_dict()).validation_errors.is_empty())
	item.used_precision_milestones.assign([20])
	assert_true(ItemScript.from_dict(item.to_dict()).validation_errors.has("INVALID_PRECISION_MILESTONE:20"))


func test_current_and_max_invariants_remain_fail_closed() -> void:
	var item = _item()
	item.current_durability = 5
	item.max_durability = 4
	assert_true(ItemScript.from_dict(item.to_dict()).validation_errors.has("CURRENT_EXCEEDS_MAX"))
	item = _item()
	item.current_durability = 0
	assert_true(ItemScript.from_dict(item.to_dict()).validation_errors.has("ZERO_DURABILITY_REQUIRES_DESTROYED"))
