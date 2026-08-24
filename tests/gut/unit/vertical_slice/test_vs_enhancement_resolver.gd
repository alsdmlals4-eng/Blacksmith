extends "res://addons/gut/test.gd"

const RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd"
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _resolver():
	if not ResourceLoader.exists(RESOLVER_PATH):
		return null
	var script = load(RESOLVER_PATH)
	if script == null:
		return null
	return script.new()


func _item(level: int = 0, max_durability: int = 100):
	var item = ItemScript.new()
	item.uid = "BSI-abcdefabcdefabcdefabcdefabcdefab"
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


func test_resolver_surface_exists() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "current enhancement resolver must exist")


func test_target_level_maps_to_approved_experience_bands() -> void:
	var resolver = _resolver()
	assert_not_null(resolver)
	if resolver == null:
		return
	var cases := {
		1: "LEARN",
		2: "LEARN",
		3: "BUILD_CONFIDENCE",
		10: "BUILD_CONFIDENCE",
		11: "FIRST_STOP_POINT",
		12: "TENSION",
		30: "TENSION",
		31: "HIGH_STAKES",
		60: "HIGH_STAKES",
		61: "MASTERY",
		100: "MASTERY",
	}
	for target in cases:
		assert_eq(resolver.band_for_target(target), cases[target], "target %d band" % target)


func test_base_success_curve_matches_approved_representative_anchors() -> void:
	var resolver = _resolver()
	assert_not_null(resolver)
	if resolver == null:
		return
	var anchors := {
		1: 100.0,
		2: 97.0,
		3: 95.0,
		10: 86.0,
		11: 82.0,
		12: 81.0,
		20: 77.0,
		30: 72.0,
		31: 73.0,
		60: 69.0,
		61: 69.0,
		100: 64.0,
	}
	for target in anchors:
		assert_almost_eq(
			resolver.base_success_percent(target),
			anchors[target],
			0.01,
			"target %d base success" % target
		)


func test_attempt_cost_and_reinforcement_mapping_match_current_budget() -> void:
	var resolver = _resolver()
	assert_not_null(resolver)
	if resolver == null:
		return
	var gold_anchors := {1: 10, 2: 40, 10: 830, 11: 990, 20: 2970, 30: 6270, 60: 22440, 90: 47310, 100: 57440}
	for target in gold_anchors:
		assert_eq(resolver.gold_attempt_cost(target), gold_anchors[target], "target %d gold" % target)
	assert_eq(resolver.reinforcement_units(1), 1)
	assert_eq(resolver.reinforcement_units(20), 1)
	assert_eq(resolver.reinforcement_units(21), 2)
	assert_eq(resolver.reinforcement_units(40), 2)
	assert_eq(resolver.reinforcement_units(41), 3)
	assert_eq(resolver.reinforcement_units(60), 3)
	assert_eq(resolver.reinforcement_units(61), 4)
	assert_eq(resolver.reinforcement_units(80), 4)
	assert_eq(resolver.reinforcement_units(81), 5)
	assert_eq(resolver.reinforcement_units(100), 5)


func test_failure_family_table_is_conditional_on_failure_and_matches_decision13() -> void:
	var resolver = _resolver()
	assert_not_null(resolver)
	if resolver == null:
		return
	assert_eq(resolver.failure_family_ratio("LEARN"), {"HOLD": 100, "DOWNGRADE": 0, "DAMAGE": 0, "CRITICAL": 0})
	assert_eq(resolver.failure_family_ratio("BUILD_CONFIDENCE"), {"HOLD": 90, "DOWNGRADE": 0, "DAMAGE": 10, "CRITICAL": 0})
	assert_eq(resolver.failure_family_ratio("FIRST_STOP_POINT"), {"HOLD": 65, "DOWNGRADE": 10, "DAMAGE": 23, "CRITICAL": 2})
	assert_eq(resolver.failure_family_ratio("TENSION"), {"HOLD": 45, "DOWNGRADE": 10, "DAMAGE": 35, "CRITICAL": 10})
	assert_eq(resolver.failure_family_ratio("HIGH_STAKES"), {"HOLD": 30, "DOWNGRADE": 15, "DAMAGE": 39, "CRITICAL": 16})
	assert_eq(resolver.failure_family_ratio("MASTERY"), {"HOLD": 20, "DOWNGRADE": 20, "DAMAGE": 40, "CRITICAL": 20})


func test_max_durability_penalty_is_visible_in_final_success_preview() -> void:
	var resolver = _resolver()
	assert_not_null(resolver)
	if resolver == null:
		return
	var stable = resolver.preview(_item(10, 100), 11)
	var stressed = resolver.preview(_item(10, 70), 11)
	var damaged = resolver.preview(_item(10, 50), 11)
	var fractured = resolver.preview(_item(10, 30), 11)
	var critical = resolver.preview(_item(10, 10), 11)
	assert_eq(stable["max_penalty_pp"], 0)
	assert_eq(stressed["max_penalty_pp"], -3)
	assert_eq(damaged["max_penalty_pp"], -6)
	assert_eq(fractured["max_penalty_pp"], -10)
	assert_eq(critical["max_penalty_pp"], -15)
	assert_almost_eq(stable["final_success_percent"], 82.0, 0.01)
	assert_almost_eq(stressed["final_success_percent"], 79.0, 0.01)


func test_same_target_recovery_is_plus_six_pp_soft_capped_and_hard_guaranteed() -> void:
	var resolver = _resolver()
	assert_not_null(resolver)
	if resolver == null:
		return
	var item = _item(10, 100)
	item.enhancement_recovery_by_target = {"11": 1}
	var one_failure = resolver.preview(item, 11)
	assert_eq(one_failure["recovery_failures"], 1)
	assert_eq(one_failure["recovery_bonus_pp"], 6)
	assert_almost_eq(one_failure["final_success_percent"], 88.0, 0.01)
	assert_false(one_failure["guaranteed"])

	item.enhancement_recovery_by_target = {"11": 3}
	var soft_cap = resolver.preview(item, 11)
	assert_almost_eq(soft_cap["final_success_percent"], 95.0, 0.01)
	assert_false(soft_cap["guaranteed"])

	item.enhancement_recovery_by_target = {"11": 4}
	var guarantee = resolver.preview(item, 11)
	assert_true(guarantee["guaranteed"])
	assert_almost_eq(guarantee["final_success_percent"], 100.0, 0.01)


func test_preview_exposes_checkpoint_cost_material_and_no_plus_101() -> void:
	var resolver = _resolver()
	assert_not_null(resolver)
	if resolver == null:
		return
	var preview = resolver.preview(_item(10, 100), 11)
	assert_true(preview["allowed"])
	assert_eq(preview["target_level"], 11)
	assert_eq(preview["checkpoint_floor"], 10)
	assert_eq(preview["next_checkpoint"], 30)
	assert_eq(preview["gold_cost"], 990)
	assert_eq(preview["reinforcement_units"], 1)
	assert_eq(preview["band"], "FIRST_STOP_POINT")

	var at_max = _item(100, 100)
	at_max.max_enhancement_reached = true
	var beyond = resolver.preview(at_max, 101)
	assert_false(beyond["allowed"])
	assert_eq(beyond["reason"], "MAX_ENHANCEMENT_TERMINAL")
