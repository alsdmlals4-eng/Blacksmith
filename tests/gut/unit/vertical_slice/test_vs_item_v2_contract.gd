extends "res://addons/gut/test.gd"

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _make_v1_compatible_item():
	var item = ItemScript.new()
	item.uid = "BSI-0123456789abcdef0123456789abcdef"
	item.birth_rng_seed = 712345
	item.primary_material_id = "iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.crafting_grade = "CRAFT_MASTERWORK"
	item.artistry = 7
	item.raw_role_stat = 15
	item.weight_point = 15
	item.function_capacity = 0
	item.functions.clear()
	item.grade_affix = "MASTERWORK_EDGE"
	item.catalyst_affix = ""
	item.chronicle_affix = ""
	item.enhancement_level = 0
	item.enhancement_failure_streak = 0
	item.used_precision_milestones.clear()
	item.damage_state = "INTACT"
	item.owner_id = "PLAYER"
	return item


func test_current_canon_accepts_level_100_and_all_precision_milestones() -> void:
	var item = _make_v1_compatible_item()
	item.enhancement_level = 100
	item.used_precision_milestones.assign([10, 20, 30, 40, 50])
	item.highest_checkpoint = 90
	item.max_enhancement_reached = true
	var restored = ItemScript.from_dict(item.to_dict())
	assert_true(
		restored.validation_errors.is_empty(),
		"V2 item domain must accept +100 and precision milestones 10/20/30/40/50"
	)


func test_serialized_item_exposes_current_canon_lifecycle_fields() -> void:
	var serialized: Dictionary = _make_v1_compatible_item().to_dict()
	var required_v2_fields := [
		"highest_checkpoint",
		"current_durability",
		"max_durability",
		"enhancement_recovery_by_target",
		"overhaul_used",
		"max_enhancement_reached",
		"physical_state",
	]
	for field_name in required_v2_fields:
		assert_true(
			serialized.has(field_name),
			"V2 serialized item is missing required field: %s" % field_name
		)


func test_current_durability_cannot_exceed_max() -> void:
	var item = _make_v1_compatible_item()
	item.current_durability = 81
	item.max_durability = 80
	var restored = ItemScript.from_dict(item.to_dict())
	assert_true(
		restored.validation_errors.has("CURRENT_EXCEEDS_MAX"),
		"CURRENT must never exceed MAX"
	)


func test_zero_durability_requires_destroyed_state() -> void:
	var item = _make_v1_compatible_item()
	item.current_durability = 0
	item.max_durability = 70
	item.physical_state = "ACTIVE"
	var restored = ItemScript.from_dict(item.to_dict())
	assert_true(
		restored.validation_errors.has("ZERO_DURABILITY_REQUIRES_DESTROYED"),
		"CURRENT or MAX zero must be physical DESTROYED"
	)


func test_destroyed_state_requires_zero_durability_axis() -> void:
	var item = _make_v1_compatible_item()
	item.current_durability = 40
	item.max_durability = 70
	item.physical_state = "DESTROYED"
	var restored = ItemScript.from_dict(item.to_dict())
	assert_true(
		restored.validation_errors.has("DESTROYED_REQUIRES_ZERO_DURABILITY"),
		"physical destruction cannot come from a separate hidden destroy roll"
	)


func test_level_100_and_max_completion_fact_must_agree() -> void:
	var missing_fact = _make_v1_compatible_item()
	missing_fact.enhancement_level = 100
	missing_fact.highest_checkpoint = 90
	var restored_missing = ItemScript.from_dict(missing_fact.to_dict())
	assert_true(
		restored_missing.validation_errors.has("LEVEL_100_REQUIRES_MAX_ENHANCEMENT_REACHED"),
		"+100 must persist the terminal completion lifecycle fact"
	)

	var impossible_fact = _make_v1_compatible_item()
	impossible_fact.enhancement_level = 90
	impossible_fact.highest_checkpoint = 90
	impossible_fact.max_enhancement_reached = true
	var restored_impossible = ItemScript.from_dict(impossible_fact.to_dict())
	assert_true(
		restored_impossible.validation_errors.has("MAX_ENHANCEMENT_REACHED_REQUIRES_LEVEL_100"),
		"terminal completion fact cannot exist below +100"
	)
