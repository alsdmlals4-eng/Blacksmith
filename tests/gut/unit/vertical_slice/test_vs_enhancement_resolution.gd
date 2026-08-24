extends "res://addons/gut/test.gd"

const ResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _item(level: int = 0, max_durability: int = 100):
	var item = ItemScript.new()
	item.uid = "BSI-fedcbafedcbafedcbafedcbafedcbafe"
	item.enhancement_level = level
	item.max_durability = max_durability
	item.current_durability = max_durability
	item.highest_checkpoint = 0
	if level >= 90:
		item.highest_checkpoint = 90
	elif level >= 60:
		item.highest_checkpoint = 60
	elif level >= 30:
		item.highest_checkpoint = 30
	elif level >= 10:
		item.highest_checkpoint = 10
	return item


func test_success_updates_level_checkpoint_and_clears_target_recovery() -> void:
	var resolver = ResolverScript.new()
	var item = _item(9, 100)
	item.enhancement_recovery_by_target = {"10": 2}
	var result = resolver.resolve_with_rolls(item, 10, {"success_roll_percent": 0.0})
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.highest_checkpoint, 10)
	assert_false(item.enhancement_recovery_by_target.has("10"))


func test_level_100_success_sets_terminal_lifecycle_fact() -> void:
	var resolver = ResolverScript.new()
	var item = _item(99, 100)
	var result = resolver.resolve_with_rolls(item, 100, {"success_roll_percent": 0.0})
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 100)
	assert_true(item.max_enhancement_reached)
	assert_eq(item.physical_state, "ACTIVE")


func test_failure_hold_increments_only_same_target_recovery() -> void:
	var resolver = ResolverScript.new()
	var item = _item(10, 100)
	var result = resolver.resolve_with_rolls(item, 11, {"success_roll_percent": 99.0, "failure_family_roll": 0})
	assert_eq(result["outcome"], "FAILURE")
	assert_eq(result["failure_family"], "HOLD")
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.enhancement_recovery_by_target.get("11"), 1)
	assert_eq(item.current_durability, 100)
	assert_eq(item.max_durability, 100)


func test_hard_guarantee_wins_even_against_high_success_roll() -> void:
	var resolver = ResolverScript.new()
	var item = _item(10, 100)
	item.enhancement_recovery_by_target = {"11": 4}
	var result = resolver.resolve_with_rolls(item, 11, {"success_roll_percent": 99.9})
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 11)
	assert_false(item.enhancement_recovery_by_target.has("11"))


func test_downgrade_is_max_one_level_and_never_below_checkpoint() -> void:
	var resolver = ResolverScript.new()
	var item = _item(15, 100)
	var result = resolver.resolve_with_rolls(item, 16, {"success_roll_percent": 99.0, "failure_family_roll": 50})
	assert_eq(result["failure_family"], "DOWNGRADE")
	assert_eq(item.enhancement_level, 14)
	assert_eq(item.highest_checkpoint, 10)

	var floor_item = _item(10, 100)
	var floor_result = resolver.resolve_with_rolls(floor_item, 11, {"success_roll_percent": 99.0, "failure_family_roll": 70})
	assert_eq(floor_result["failure_family"], "DOWNGRADE")
	assert_eq(floor_item.enhancement_level, 10)


func test_damage_changes_current_only_and_critical_owns_max_scar() -> void:
	var resolver = ResolverScript.new()
	var damaged = _item(10, 100)
	var damage_result = resolver.resolve_with_rolls(damaged, 11, {
		"success_roll_percent": 99.0, "failure_family_roll": 80, "current_loss": 6,
	})
	assert_eq(damage_result["failure_family"], "DAMAGE")
	assert_eq(damaged.current_durability, 94)
	assert_eq(damaged.max_durability, 100)

	var critical = _item(10, 100)
	var critical_result = resolver.resolve_with_rolls(critical, 11, {
		"success_roll_percent": 99.0, "failure_family_roll": 99,
		"current_loss": 12, "max_scar_loss": 2,
	})
	assert_eq(critical_result["failure_family"], "CRITICAL")
	assert_eq(critical.current_durability, 88)
	assert_eq(critical.max_durability, 98)


func test_zero_current_from_causal_failure_marks_physical_destroyed() -> void:
	var resolver = ResolverScript.new()
	var item = _item(30, 50)
	item.current_durability = 2
	var result = resolver.resolve_with_rolls(item, 31, {
		"success_roll_percent": 99.0, "failure_family_roll": 99,
		"current_loss": 10, "max_scar_loss": 4,
	})
	assert_eq(result["failure_family"], "CRITICAL")
	assert_eq(item.current_durability, 0)
	assert_eq(item.max_durability, 46)
	assert_eq(item.physical_state, "DESTROYED")
