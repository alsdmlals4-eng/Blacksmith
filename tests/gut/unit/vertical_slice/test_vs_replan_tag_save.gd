extends "res://addons/gut/test.gd"

const Item = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const Envelope = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const Initializer = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Precision = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")
const Action = preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const Resources = preload("res://scripts/economy/workshop_resources.gd")

class SaveBoundary:
	extends RefCounted
	var error: Error = OK
	var calls := 0
	func save_envelope(candidate) -> Error:
		calls += 1
		var restored = Envelope.from_dict(JSON.parse_string(JSON.stringify(candidate.to_dict())))
		return error if restored.validation_errors.is_empty() else ERR_INVALID_DATA

func test_new_precision_transaction_commits_growth_and_one_existing_catalyst_stock_unit():
	for success in [true, false]:
		var envelope = Initializer.new().create_candidate_envelope()
		var item = _item()
		envelope.items_by_uid[item.uid] = item
		var resources = Resources.new(20000, {"common_reinforcement_material":10, "heart_of_flame":2, "earth_crystal":2})
		envelope.workshop_resources = resources.snapshot()
		var save = SaveBoundary.new()
		var result = Action.new().resolve_and_save_with_rolls(envelope, item.uid, 20,
			{"success_roll_percent":0.0 if success else 99.9, "damage_roll_percent":100.0},
			1, resources, save, {"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912", "tag_id":"BURST_HANDLING"})
		assert_eq(result.outcome, "SUCCESS" if success else "FAILED_HOLD")
		assert_eq(save.calls, 1)
		assert_eq(resources.get_material_count("heart_of_flame"), 1)
		assert_eq(item.enhancement_level, 19, "Source envelope stays unchanged until caller adopts result")
		if result.has("envelope"):
			var saved = result.envelope.get_item(item.uid)
			assert_eq(saved.enhancement_level, 20 if success else 19)
			assert_eq(saved.catalyst_affix.tags.BURST_HANDLING, 2 if success else 1)
			assert_eq(saved.raw_role_stat, item.raw_role_stat)
			assert_eq(saved.weight_point, item.weight_point)
			var repeated = Action.new().resolve_and_save_with_rolls(result.envelope, item.uid, 20,
				{"success_roll_percent":0.0}, 1, resources, save,
				{"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912", "tag_id":"BURST_HANDLING"}) if success else {}
			if success:
				assert_eq(repeated.outcome, "BLOCKED")
				assert_eq(save.calls, 1)
				assert_eq(saved.ledger[-1].get("source_decision_id"), "BS-REPLAN-20260913-02")

func test_new_precision_accepts_all_five_equipment_identities_and_requires_real_stock():
	var catalog = load("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
	for entry in catalog.all():
		var envelope = Initializer.new().create_candidate_envelope()
		var item = _item()
		item.equipment_group = entry.equipment_group
		item.role_profile = entry.role_profile
		envelope.items_by_uid[item.uid] = item
		var resources = Resources.new(20000, {"common_reinforcement_material":10, "heart_of_flame":0, "earth_crystal":2})
		envelope.workshop_resources = resources.snapshot()
		var save = SaveBoundary.new()
		var blocked = Action.new().resolve_and_save_with_rolls(envelope, item.uid, 20,
			{"success_roll_percent":0.0}, 1, resources, save,
			{"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912", "tag_id":"BURST_HANDLING"})
		assert_eq(blocked.reason, "INSUFFICIENT_PRECISION_CATALYST")
		assert_eq(save.calls, 0)
		var result = Action.new().resolve_and_save_with_rolls(envelope, item.uid, 20,
			{"success_roll_percent":0.0}, 1, resources, save,
			{"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912", "tag_id":"SUSTAIN_HANDLING"})
		assert_eq(result.outcome, "SUCCESS", str(entry.equipment_id))
		assert_eq(resources.get_material_count("earth_crystal"), 1)

func test_new_precision_save_failure_and_empty_selection_do_not_spend_or_mutate():
	for empty in [true, false]:
		var envelope = Initializer.new().create_candidate_envelope()
		var item = _item()
		envelope.items_by_uid[item.uid] = item
		var resources = Resources.new(20000, {"common_reinforcement_material":10, "heart_of_flame":2, "earth_crystal":2})
		envelope.workshop_resources = resources.snapshot()
		var before: Dictionary = envelope.to_dict()
		var save = SaveBoundary.new()
		save.error = ERR_CANT_CREATE
		var selection := {} if empty else {"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912", "tag_id":"BURST_HANDLING"}
		var result = Action.new().resolve_and_save_with_rolls(envelope, item.uid, 20,
			{"success_roll_percent":0.0}, 1, resources, save, selection)
		assert_eq(result.outcome, "BLOCKED")
		assert_eq(save.calls, 0 if empty else 1)
		assert_eq(envelope.to_dict(), before)
		assert_eq(resources.snapshot(), envelope.resource_snapshot())

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
