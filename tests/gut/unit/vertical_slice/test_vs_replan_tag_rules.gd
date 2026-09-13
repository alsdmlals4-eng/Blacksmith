extends "res://addons/gut/test.gd"

func test_aqueduct_preview_separates_level_readiness_tag_support_and_cap():
	var rules = load(PATH).new()
	assert_true(rules.has_method("aqueduct_preview"), "Blueprint mission estimate must have a runtime consumer")
	if not rules.has_method("aqueduct_preview"):
		return
	var first = rules.aqueduct_preview("iron_shield", 10, {"BURST_HANDLING":1}, "HANDLING", "BURST")
	assert_true(first.ok)
	assert_eq(first.base_percent, 60.0)
	assert_eq(first.support_points, 3)
	assert_eq(first.success_percent, 63.0)
	assert_eq(rules.aqueduct_preview("iron_shield", 11, {"BURST_HANDLING":1}, "HANDLING", "BURST").success_percent, 63.5)
	var capped = rules.aqueduct_preview("iron_shield", 100, {"BURST_HANDLING":4,"SUSTAIN_HANDLING":4,"BURST_OUTPUT":2}, "HANDLING", "BURST")
	assert_eq(capped.base_percent, 80.0)
	assert_eq(capped.support_points, 16)
	assert_eq(capped.applied_support_percent, 15.0)
	assert_eq(capped.success_percent, 95.0)
	for level in [9, 10.5, true, 101]:
		assert_false(rules.aqueduct_preview("iron_shield", level, {}, "HANDLING", "BURST").ok)
	assert_false(rules.aqueduct_preview("iron_sword", 10, {"BURST_HANDLING":1}, "HANDLING", "BURST").ok)
	assert_false(rules.aqueduct_preview("iron_shield", 10, {"BURST_HANDLING":2}, "HANDLING", "BURST").ok)

const PATH := "res://scripts/vertical_slice/domain/vs_replan_tag_rules.gd"

func test_customer_choices_compare_benefit_even_when_catalyst_is_missing() -> void:
	var rules = load(PATH).new()
	assert_true(rules.has_method("customer_choices"), "Customer comparison is not connected to tag rules")
	if not rules.has_method("customer_choices"):
		return
	var tags := {"BURST_HANDLING": 1}
	var stock := {"fire_heart": 0, "earth_crystal": 2}
	var result = rules.customer_choices("iron_shield", 19, tags, stock, "HANDLING", "BURST")
	assert_true(result.ok)
	assert_eq(result.points_before, 3)
	assert_eq(result.choices.size(), 4)
	var upgrade: Dictionary = result.choices[2]
	assert_eq(upgrade.tag_id, "BURST_HANDLING")
	assert_false(upgrade.allowed)
	assert_eq(upgrade.reason, "INSUFFICIENT_CATALYST")
	assert_eq(upgrade.points_after, 6)
	assert_eq(upgrade.points_delta, 3)
	assert_eq(upgrade.catalyst_stock, 0)
	assert_eq(upgrade.catalyst_cost, 1)
	assert_true(result.choices[3].allowed)
	assert_eq(result.choices[3].points_after, 4)
	assert_eq(tags, {"BURST_HANDLING": 1})
	assert_eq(stock, {"fire_heart": 0, "earth_crystal": 2})

func test_customer_choices_do_not_offer_impossible_growth_or_invent_unknown_requirements() -> void:
	var rules = load(PATH).new()
	if not rules.has_method("customer_choices"):
		assert_true(false, "Customer comparison missing")
		return
	var result = rules.customer_choices("iron_shield", 49, {"BURST_OUTPUT": 4}, {"fire_heart": 1}, "OUTPUT", "BURST")
	assert_eq(result.choices[0].reason, "TAG_MASTERED")
	assert_false(result.choices[0].has("points_after"))
	assert_false(rules.customer_choices("iron_shield", 19, {}, {}, "UNKNOWN", "BURST").ok)
	assert_false(rules.customer_choices("iron_shield", 18, {}, {}, "OUTPUT", "BURST").ok)

func test_customer_choices_reject_malformed_stock_instead_of_claiming_it_is_spendable() -> void:
	var rules = load(PATH).new()
	if not rules.has_method("customer_choices"):
		assert_true(false, "Customer comparison missing")
		return
	for bad in [true, 1.5, -1, "1"]:
		assert_false(rules.customer_choices("iron_shield", 9, {}, {"fire_heart": bad}, "OUTPUT", "BURST").ok)

func test_precision_preview_adds_and_upgrades_without_spending_or_mutating() -> void:
	var rules = load(PATH).new()
	assert_true(rules.has_method("preview"), "Selection transaction preview missing")
	if not rules.has_method("preview"):
		return
	for equipment in ["iron_sword","iron_shield","iron_bow","iron_armor","iron_helmet"]:
		var result = rules.preview(equipment, 9, {}, "BURST_HANDLING", {"fire_heart":1})
		assert_true(result.ok)
		assert_eq(result.tags_after, {"BURST_HANDLING":1})
		assert_eq(result.catalyst_id, "fire_heart")
		assert_eq(result.catalyst_cost, 1)
	var tags := {"BURST_HANDLING":1}
	var inventory := {"fire_heart":2}
	var upgrade = rules.preview("iron_armor", 19, tags, "BURST_HANDLING", inventory)
	assert_eq(upgrade.tags_after, {"BURST_HANDLING":2})
	assert_eq(tags, {"BURST_HANDLING":1})
	assert_eq(inventory, {"fire_heart":2})

func test_precision_preview_blocks_invalid_boundary_resources_and_fourth_tag() -> void:
	var rules = load(PATH).new()
	if not rules.has_method("preview"):
		assert_true(false, "Selection transaction preview missing")
		return
	assert_false(rules.preview("iron_sword",8,{},"BURST_OUTPUT",{"fire_heart":1}).ok)
	assert_false(rules.preview("iron_sword",109,{},"BURST_OUTPUT",{"fire_heart":1}).ok)
	assert_false(rules.preview("iron_sword",9,{},"",{"fire_heart":1}).ok)
	assert_false(rules.preview("iron_sword",9,{},"BURST_OUTPUT",{}).ok)
	assert_false(rules.preview("iron_sword",9,{},"BURST_OUTPUT",{"fire_heart":true}).ok)
	assert_false(rules.preview("axe",9,{},"BURST_OUTPUT",{"fire_heart":1}).ok)
	assert_false(rules.preview("iron_sword",19,{},"BURST_OUTPUT",{"fire_heart":1}).ok)
	assert_eq(rules.preview("iron_sword",49,{"BURST_OUTPUT":4},"BURST_OUTPUT",{"fire_heart":1}).reason, "TAG_MASTERED")
	assert_false(rules.preview("iron_sword",39,{"BURST_OUTPUT":1,"SUSTAIN_OUTPUT":1,"BURST_HANDLING":1},"SUSTAIN_HANDLING",{"earth_crystal":1}).ok)

func test_all_reachable_tag_builds_have_a_next_choice_through_ten_milestones() -> void:
	var rules = load(PATH).new()
	var states: Array = [{}]
	for level in [9,19,29,39,49,59,69,79,89,99]:
		var next: Array = []
		for tags in states:
			var choices := 0
			for tag in ["BURST_OUTPUT","SUSTAIN_OUTPUT","BURST_HANDLING","SUSTAIN_HANDLING"]:
				var result = rules.preview("iron_helmet",level,tags,tag,{"fire_heart":1,"earth_crystal":1})
				if result.ok:
					choices += 1
					if not next.has(result.tags_after):
						next.append(result.tags_after)
			assert_gt(choices,0,"Reachable build must not dead-end with both catalysts available")
		states = next
	assert_eq(states.size(),24,"Ten milestones produce24valid final builds")

func test_new_rules_do_not_silently_read_legacy_tag_ids() -> void:
	assert_true(ResourceLoader.exists(PATH), "New ruleset required; old effect resolver is not equivalent")
	if not ResourceLoader.exists(PATH):
		return
	var rules = load(PATH).new()
	assert_false(rules.support({"LIGHTWEIGHT": 1}, "OUTPUT", "BURST").ok)
	assert_false(rules.support({"BURST_OUTPUT": 0}, "OUTPUT", "BURST").ok)
	assert_false(rules.support({"BURST_OUTPUT": 5}, "OUTPUT", "BURST").ok)
	assert_false(rules.support({"BURST_OUTPUT": 1.5}, "OUTPUT", "BURST").ok)

func test_suitability_matches_hand_calculated_blueprint_example() -> void:
	if not ResourceLoader.exists(PATH):
		assert_true(false, "New ruleset missing")
		return
	var rules = load(PATH).new()
	var tags := {"BURST_OUTPUT": 2, "SUSTAIN_OUTPUT": 1}
	assert_eq(rules.support(tags, "OUTPUT", "BURST").points, 7)
	assert_eq(rules.support(tags, "OUTPUT", "SUSTAIN").points, 5)
	assert_eq(rules.support(tags, "HANDLING", "BURST").points, 0)
	assert_eq(tags, {"BURST_OUTPUT": 2, "SUSTAIN_OUTPUT": 1}, "Preview must not mutate tags")

func test_four_tags_and_invalid_event_requirements_are_rejected() -> void:
	if not ResourceLoader.exists(PATH):
		assert_true(false, "New ruleset missing")
		return
	var rules = load(PATH).new()
	assert_false(rules.support({"BURST_OUTPUT":1,"SUSTAIN_OUTPUT":1,"BURST_HANDLING":1,"SUSTAIN_HANDLING":1}, "OUTPUT", "BURST").ok)
	assert_false(rules.support({}, "UNKNOWN", "BURST").ok)
	assert_false(rules.support({}, "OUTPUT", "UNKNOWN").ok)
	assert_eq(rules.support({}, "OUTPUT", "BURST").points, 0)
