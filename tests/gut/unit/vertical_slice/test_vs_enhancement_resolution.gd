extends "res://addons/gut/test.gd"

const ResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _item(level: int = 0) -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-fedcbafedcbafedcbafedcbafedcbafe"
	item.enhancement_level = level
	item.highest_checkpoint = 10 if level >= 10 else 0
	return item


func test_success_updates_one_level_checkpoint_and_clears_only_target_recovery() -> void:
	var resolver = ResolverScript.new()
	var item = _item(9)
	item.enhancement_recovery_by_target = {"10": 2, "11": 1}
	var result = resolver.resolve_with_rolls(item, 10, {"success_roll_percent": 0.0})
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.highest_checkpoint, 10)
	assert_false(item.enhancement_recovery_by_target.has("10"))
	assert_eq(item.enhancement_recovery_by_target.get("11"), 1)
	assert_false(item.catalyst_affix.is_empty())


func test_level_100_success_sets_terminal_lifecycle_fact() -> void:
	var resolver = ResolverScript.new()
	var item = _item(99)
	var result = resolver.resolve_with_rolls(item, 100, {"success_roll_percent": 0.0})
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 100)
	assert_true(item.max_enhancement_reached)
	assert_eq(item.physical_state, "ACTIVE")


func test_failed_hold_increments_only_same_target_recovery() -> void:
	var resolver = ResolverScript.new()
	var item = _item(10)
	var result = resolver.resolve_with_rolls(item, 11, {"success_roll_percent": 99.0, "damage_roll_percent": 99.0})
	assert_eq(result["outcome"], "FAILED_HOLD")
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.enhancement_recovery_by_target.get("11"), 1)
	assert_eq(item.current_durability, 5)
	assert_eq(item.max_durability, 5)


func test_hard_guarantee_wins_even_against_high_success_roll() -> void:
	var resolver = ResolverScript.new()
	var item = _item(10)
	item.enhancement_recovery_by_target = {"11": 4}
	var result = resolver.resolve_with_rolls(item, 11, {"success_roll_percent": 99.9})
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 11)
	assert_false(item.enhancement_recovery_by_target.has("11"))


func test_failed_damage_keeps_level_and_opens_one_repair_job() -> void:
	var resolver = ResolverScript.new()
	var item = _item(10)
	var result = resolver.resolve_with_rolls(item, 11, {"success_roll_percent": 99.0, "damage_roll_percent": 0.0})
	assert_eq(result["outcome"], "FAILED_DAMAGE")
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.current_durability, 4)
	assert_eq(item.max_durability, 5)
	assert_true(item.repair_job_available)


func test_zero_current_from_damage_marks_physical_destroyed_without_max_scar() -> void:
	var resolver = ResolverScript.new()
	var item = _item(30)
	item.current_durability = 1
	var result = resolver.resolve_with_rolls(item, 31, {"success_roll_percent": 99.0, "damage_roll_percent": 0.0})
	assert_eq(result["outcome"], "FAILED_DAMAGE")
	assert_eq(item.current_durability, 0)
	assert_eq(item.max_durability, 5)
	assert_eq(item.physical_state, "DESTROYED")
