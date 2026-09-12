extends "res://addons/gut/test.gd"

const Item = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const Envelope = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const Initializer = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Precision = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")

func _item():
	var item = Item.new()
	item.uid = "BSI-0123456789abcdef0123456789abcdef"
	item.primary_material_id = "iron"
	item.crafting_grade = "CRAFT_NORMAL"
	item.enhancement_level = 19
	item.highest_checkpoint = 10
	item.used_precision_milestones.assign([10])
	item.catalyst_affix = {"schema_version":2, "ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912", "tags":{"BURST_HANDLING":1}}
	return item

func test_new_tags_survive_real_envelope_json_round_trip_without_mutating_source():
	var envelope = Initializer.new().create_candidate_envelope()
	var item = _item()
	envelope.items_by_uid[item.uid] = item
	envelope.active_run["selected_item_uid"] = item.uid
	var before: Dictionary = envelope.to_dict()
	var restored = Envelope.from_dict(JSON.parse_string(JSON.stringify(before)))
	assert_eq(restored.validation_errors, [])
	assert_eq(restored.get_item(item.uid).catalyst_affix, item.catalyst_affix)
	assert_eq(envelope.to_dict(), before)

func test_unknown_mixed_and_fractional_tag_saves_fail_closed():
	for affix in [
		{"schema_version":2,"ruleset_id":"FUTURE_UNKNOWN","tags":{"BURST_HANDLING":1}},
		{"schema_version":2,"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912","tags":{"TAG_EMBER_EDGE":1}},
		{"schema_version":2,"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912","tags":{"BURST_HANDLING":1.5}},
		{"schema_version":2,"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912","tags":{"BURST_HANDLING":true}},
		{"schema_version":2,"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912","tags":{"BURST_HANDLING":2}},
	]:
		var raw: Dictionary = _item().to_dict()
		raw["catalyst_affix"] = affix
		assert_false(Item.from_dict(raw).validation_errors.is_empty())

func test_legacy_resolver_cannot_apply_old_effects_to_empty_new_ruleset():
	var item = _item()
	item.enhancement_level = 9
	item.used_precision_milestones.clear()
	item.catalyst_affix["tags"] = {}
	var result: Dictionary = Precision.new().selection_preview(item, 10, {})
	assert_eq(result.get("reason"), "PRECISION_RULESET_REQUIRES_NEW_RESOLVER")

func test_legacy_tag_save_is_not_converted_to_new_tags():
	var item = _item()
	item.catalyst_affix = {"schema_version":1,"tag_entries":[{"tag_id":"TAG_EMBER_EDGE","stage":1,"created_milestone":10,"last_advanced_milestone":10}],"initial_tag_backfill_pending":false,"unreadable_legacy_affix":""}
	var restored = Item.from_dict(JSON.parse_string(JSON.stringify(item.to_dict())))
	assert_eq(restored.validation_errors, [])
	assert_eq(restored.catalyst_affix, item.catalyst_affix)

func test_duplicate_fractional_and_boolean_milestones_are_not_normalized_into_valid_history():
	for milestones in [[10,10], [10.5], [true], [], [20]]:
		var raw: Dictionary = _item().to_dict()
		raw["used_precision_milestones"] = milestones
		assert_false(Item.from_dict(raw).validation_errors.is_empty())

func test_schema_one_cannot_smuggle_new_rule_identity_or_tags():
	var raw: Dictionary = _item().to_dict()
	raw["catalyst_affix"] = Item.empty_catalyst_affix()
	raw["catalyst_affix"]["ruleset_id"] = "BLACKSMITH_REPLAN_TAGS_20260912"
	assert_true(Item.from_dict(raw).validation_errors.has("MIXED_CATALYST_RULESET"))

func test_fractional_level_is_not_truncated_into_a_valid_replan_save():
	var raw: Dictionary = _item().to_dict()
	raw["enhancement_level"] = 19.5
	assert_false(Item.from_dict(raw).validation_errors.is_empty())
