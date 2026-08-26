extends "res://addons/gut/test.gd"

const RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd"
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _resolver() -> VSEnhancementResolver:
	return load(RESOLVER_PATH).new()


func _item(level: int = 10, current: int = 5, maximum: int = 5) -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-abcdefabcdefabcdefabcdefabcdefab"
	item.enhancement_level = level
	item.highest_checkpoint = 10 if level >= 10 else 0
	item.current_durability = current
	item.max_durability = maximum
	return item


func test_resolver_surface_and_target_bands_exist() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH))
	var resolver = _resolver()
	assert_eq(resolver.band_for_target(1), "LEARN")
	assert_eq(resolver.band_for_target(11), "FIRST_STOP_POINT")
	assert_eq(resolver.band_for_target(30), "TENSION")
	assert_eq(resolver.band_for_target(60), "HIGH_STAKES")
	assert_eq(resolver.band_for_target(100), "MASTERY")


func test_base_success_and_attempt_budget_remain_explicit_test_inputs() -> void:
	var resolver = _resolver()
	assert_almost_eq(resolver.base_success_percent(11), 82.0, 0.01)
	assert_almost_eq(resolver.base_success_percent(30), 72.0, 0.01)
	assert_eq(resolver.gold_attempt_cost(11), 990)
	assert_eq(resolver.reinforcement_units(11), 1)
	assert_eq(resolver.reinforcement_units(81), 5)


func test_damage_curve_is_failure_conditional_and_uses_effective_state_multiplier() -> void:
	var resolver = _resolver()
	var normal = resolver.preview(_item(10, 5, 5), 11)
	var minor = resolver.preview(_item(10, 4, 5), 11)
	var major = resolver.preview(_item(10, 2, 5), 11)
	assert_almost_eq(normal["final_damage_percent"], 5.0, 0.01)
	assert_almost_eq(minor["final_damage_percent"], 6.25, 0.01)
	assert_almost_eq(major["final_damage_percent"], 8.75, 0.01)
	assert_almost_eq(resolver.preview(_item(9), 10)["final_damage_percent"], 0.0, 0.01)


func test_preview_displays_only_success_damage_and_hold_that_sum_to_100() -> void:
	var preview = _resolver().preview(_item(10, 4, 5), 11)
	assert_eq(preview["display_outcomes"], {
		"success_percent": 79.0,
		"failed_damage_percent": 6.3,
		"failed_hold_percent": 14.7,
	})


func test_same_target_recovery_is_plus_six_pp_soft_capped_and_hard_guaranteed() -> void:
	var resolver = _resolver()
	var item = _item()
	item.enhancement_recovery_by_target = {"11": 1}
	assert_almost_eq(resolver.preview(item, 11)["final_success_percent"], 88.0, 0.01)
	item.enhancement_recovery_by_target = {"11": 3}
	assert_almost_eq(resolver.preview(item, 11)["final_success_percent"], 95.0, 0.01)
	item.enhancement_recovery_by_target = {"11": 4}
	var guarantee = resolver.preview(item, 11)
	assert_true(guarantee["guaranteed"])
	assert_almost_eq(guarantee["final_success_percent"], 100.0, 0.01)


func test_preview_exposes_checkpoint_cost_material_and_no_plus_101() -> void:
	var resolver = _resolver()
	var preview = resolver.preview(_item(), 11)
	assert_true(preview["allowed"])
	assert_eq(preview["checkpoint_floor"], 10)
	assert_eq(preview["next_checkpoint"], 30)
	assert_eq(preview["gold_cost"], 990)
	var at_max = _item(100)
	at_max.max_enhancement_reached = true
	var beyond = resolver.preview(at_max, 101)
	assert_false(beyond["allowed"])
	assert_eq(beyond["reason"], "MAX_ENHANCEMENT_TERMINAL")
