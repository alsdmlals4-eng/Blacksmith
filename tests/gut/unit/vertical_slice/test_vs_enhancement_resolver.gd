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


func _seeded_ember_item(level: int = 19) -> VSItem:
	var item := _item(level)
	item.catalyst_affix["tag_entries"] = [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}]
	item.used_precision_milestones = [10]
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
	assert_almost_eq(resolver.preview(_item(9), 10, _precision_add_ember())["final_damage_percent"], 0.0, 0.01)


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


func test_every_catalog_precision_target_requires_an_action_before_rolls() -> void:
	var resolver = _resolver()
	var item := _seeded_ember_item()
	var missing = resolver.preview(item, 20)
	assert_false(bool(missing.get("allowed", true)))
	assert_eq(missing.get("reason", ""), "INVALID_PRECISION_ACTION")
	assert_eq(item.enhancement_level, 19)
	assert_eq(item.catalyst_tag_entries().size(), 1)
	assert_eq(item.used_precision_milestones, [10])

	var selected = resolver.preview(item, 20, _precision_upgrade_ember())
	assert_true(bool(selected.get("allowed", false)))
	assert_eq(selected.get("precision_tag_preview", {}).get("tag_id", ""), "TAG_EMBER_EDGE")
	assert_eq(selected.get("precision_tag_preview", {}).get("effect_axis", ""), "RAW_ROLE_STAT")
	assert_eq(selected.get("precision_tag_preview", {}).get("effect_delta", 0), 3)
	assert_eq(selected.get("precision_tag_preview", {}).get("durability_delta", -1), 0)

	var ordinary := resolver.preview(_item(10), 11)
	assert_true(bool(ordinary.get("allowed", false)))
	assert_true((ordinary.get("precision_tag_preview", {}) as Dictionary).is_empty())


func test_plus_ten_success_applies_exact_tag_and_method_while_hold_writes_nothing() -> void:
	var resolver = _resolver()
	var item = _item(9)
	var before_raw := int(item.raw_role_stat)
	var held = resolver.resolve_with_rolls(item, 10, {
		"success_roll_percent": 99.0,
		"damage_roll_percent": -1.0,
	}, _precision_add_ember())
	assert_eq(held.get("outcome", ""), "FAILED_HOLD")
	assert_eq(item.enhancement_level, 9)
	assert_true(item.catalyst_tag_entries().is_empty())
	assert_eq(item.raw_role_stat, before_raw)

	var success = resolver.resolve_with_rolls(item, 10, {
		"success_roll_percent": 0.0,
		"damage_roll_percent": 0.0,
	}, _precision_add_ember())
	assert_eq(success.get("outcome", ""), "SUCCESS")
	assert_eq(success.get("precision_action", ""), "ADD_TAG")
	assert_eq(success.get("precision_tag_id", ""), "TAG_EMBER_EDGE")
	assert_eq(success.get("precision_stage_before", -1), 0)
	assert_eq(success.get("precision_stage_after", -1), 1)
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.catalyst_tag_entries()[0]["tag_id"], "TAG_EMBER_EDGE")
	assert_eq(item.used_precision_milestones, [10])
	assert_eq(item.raw_role_stat, before_raw + 3)


func test_plus_twenty_hold_and_damage_never_mutate_tag_growth() -> void:
	var resolver := _resolver()
	var held_item := _seeded_ember_item()
	var before_hold := held_item.to_dict()
	var held := resolver.resolve_with_rolls(held_item, 20, {
		"success_roll_percent": 99.0,
		"damage_roll_percent": 99.0,
	}, _precision_upgrade_ember())
	assert_eq(held.get("outcome", ""), "FAILED_HOLD")
	assert_eq(held_item.catalyst_affix, before_hold["catalyst_affix"])
	assert_eq(held_item.used_precision_milestones, before_hold["used_precision_milestones"])
	assert_eq(held_item.raw_role_stat, before_hold["raw_role_stat"])

	var damaged_item := _seeded_ember_item()
	var before_damage := damaged_item.to_dict()
	var damaged := resolver.resolve_with_rolls(damaged_item, 20, {
		"success_roll_percent": 99.0,
		"damage_roll_percent": 0.0,
	}, _precision_upgrade_ember())
	assert_eq(damaged.get("outcome", ""), "FAILED_DAMAGE")
	assert_eq(damaged_item.catalyst_affix, before_damage["catalyst_affix"])
	assert_eq(damaged_item.used_precision_milestones, before_damage["used_precision_milestones"])
	assert_eq(damaged_item.raw_role_stat, before_damage["raw_role_stat"])
	assert_eq(damaged_item.current_durability, int(before_damage["current_durability"]) - 1)


func _precision_add_ember() -> Dictionary:
	return {"action": "ADD_TAG", "catalyst_id": "HEART_OF_FLAME", "method_id": "EDGE_REINFORCEMENT"}


func _precision_upgrade_ember() -> Dictionary:
	return {"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"}
