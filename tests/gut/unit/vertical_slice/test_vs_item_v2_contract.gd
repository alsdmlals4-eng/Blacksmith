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
