extends "res://addons/gut/test.gd"

const Item = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const Envelope = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const Initializer = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Precision = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")
const Action = preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const Resources = preload("res://scripts/economy/workshop_resources.gd")

func test_aqueduct_prepared_save_resumes_with_independent_fixed_rolls_and_no_repeat_damage():
	var service = load("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd").new()
	assert_true(service.has_method("prepare_aqueduct_with_rolls"))
	if not service.has_method("prepare_aqueduct_with_rolls"):
		return
	for success in [true, false]:
		for damage in [true, false]:
			var envelope = Initializer.new().create_replan_candidate_envelope()
			var item = _item()
			var identity = load("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd").by_id("iron_shield")
			item.equipment_group = identity.equipment_group
			item.role_profile = identity.role_profile
			envelope.items_by_uid[item.uid] = item
			var save = load("res://scripts/vertical_slice/services/vs_save_service.gd").new("user://gut/aqueduct-transaction-%s-%s.json" % [success, damage])
			assert_eq(save.save_envelope(envelope), OK, "Explicitly initialize the isolated test run")
			var prepared = service.prepare_aqueduct_with_rolls(envelope, item.uid, "HANDLING", "BURST", [0.0 if success else 99.9, 0.0 if damage else 99.9], save)
			assert_eq(prepared.status, "PREPARED")
			assert_eq(item.current_durability, 5)
			var restored = save.load_envelope()
			var resolved = service.resolve_prepared_aqueduct(restored, item.uid, save)
			assert_eq(resolved.status, "APPLIED")
			assert_eq(resolved.record.mission_success, success)
			assert_eq(resolved.record.damage_applied, damage)
			var final_save = save.load_envelope()
			assert_eq(final_save.get_item(item.uid).current_durability, 4 if damage else 5)
			var repeated = service.resolve_prepared_aqueduct(final_save, item.uid, save)
			assert_eq(repeated.status, "ALREADY_RESOLVED")
			assert_eq(repeated.record, resolved.record)
			assert_eq(save.load_envelope().get_item(item.uid).current_durability, 4 if damage else 5)

func test_aqueduct_invalid_rolls_and_failed_commit_preserve_source():
	var service = load("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd").new()
	var envelope = _aqueduct_envelope()
	var uid = envelope.active_run.selected_item_uid
	var before = envelope.to_dict()
	var save = SaveBoundary.new()
	for rolls in [[true, 0], [-1, 0], [100, 0], [0], [NAN, 0]]:
		assert_eq(service.prepare_aqueduct_with_rolls(envelope, uid, "HANDLING", "BURST", rolls, save).status, "BLOCKED")
	assert_eq(save.calls, 0)
	var prepared = service.prepare_aqueduct_with_rolls(envelope, uid, "HANDLING", "BURST", [0, 0], save)
	save.error = ERR_CANT_CREATE
	assert_eq(service.resolve_prepared_aqueduct(prepared.envelope, uid, save).status, "BLOCKED")
	assert_eq(prepared.envelope.get_item(uid).current_durability, 5)
	assert_eq(prepared.envelope.active_run.aqueduct_trials[uid].phase, "PREPARED")
	assert_eq(envelope.to_dict(), before)
	var changed = Envelope.from_dict(prepared.envelope.to_dict())
	changed.get_item(uid).current_durability = 4
	assert_false(Envelope.from_dict(changed.to_dict()).validation_errors.is_empty(), "Pending item is reserved at the save boundary")
	assert_eq(service.resolve_prepared_aqueduct(changed, uid, SaveBoundary.new()).status, "BLOCKED")
	for field in ["schema_version", "ruleset_id", "rolls", "phase", "damage_percent"]:
		var corrupt = prepared.envelope.to_dict()
		corrupt.active_run.aqueduct_trials[uid][field] = null
		assert_false(Envelope.from_dict(corrupt).validation_errors.is_empty(), field)

func test_aqueduct_old_screen_cannot_reroll_an_already_saved_preparation():
	var service = load("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd").new()
	var envelope = _aqueduct_envelope()
	var uid = envelope.active_run.selected_item_uid
	var save = load("res://scripts/vertical_slice/services/vs_save_service.gd").new("user://gut/aqueduct-stale-screen.json")
	assert_eq(save.save_envelope(envelope), OK)
	var first = service.prepare_aqueduct_with_rolls(envelope, uid, "HANDLING", "BURST", [0, 0], save)
	var repeated = service.prepare_aqueduct_with_rolls(envelope, uid, "OUTPUT", "SUSTAIN", [99, 99], save)
	assert_eq(repeated.record, first.record, "Old in-memory screen must reuse the committed draw")
	var replacement = _aqueduct_envelope()
	assert_eq(save.save_envelope(replacement), OK, "Explicit new-game replacement")
	assert_eq(service.prepare_aqueduct_with_rolls(envelope, uid, "HANDLING", "BURST", [0, 0], save).status, "BLOCKED")
	assert_eq(save.load_envelope().active_run.run_id, replacement.active_run.run_id)

func _aqueduct_envelope():
	var envelope = Initializer.new().create_replan_candidate_envelope()
	var item = _item()
	var identity = load("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd").by_id("iron_shield")
	item.equipment_group = identity.equipment_group
	item.role_profile = identity.role_profile
	envelope.items_by_uid[item.uid] = item
	envelope.active_run.selected_item_uid = item.uid
	return envelope

func test_stale_repair_cannot_erase_pending_or_resolved_aqueduct_record():
	for resolved in [false, true]:
		var envelope = _aqueduct_envelope()
		var uid = envelope.active_run.selected_item_uid
		envelope.get_item(uid).apply_damage_event()
		var save = load("res://scripts/vertical_slice/services/vs_save_service.gd").new("user://gut/aqueduct-stale-repair-%s.json" % resolved)
		assert_eq(save.save_envelope(envelope), OK)
		var service = load("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd").new()
		var prepared = service.prepare_aqueduct_with_rolls(envelope, uid, "HANDLING", "BURST", [0, 99], save)
		if resolved:
			service.resolve_prepared_aqueduct(prepared.envelope, uid, save)
		var before = save.load_envelope().to_dict()
		var stock = envelope.resource_snapshot()
		var resources = Resources.new(stock.gold, stock.material_stock)
		var maintenance = load("res://scripts/vertical_slice/services/vs_workshop_maintenance_service.gd").new()
		var result = maintenance.repair_and_save(envelope, uid, resources, save, {"quality_roll_percent":0.0,"scar_roll_percent":99.0})
		assert_eq(result.status, "BLOCKED")
		assert_eq(save.load_envelope().to_dict(), before)
		var enhanced = Action.new().resolve_and_save_with_rolls(envelope, uid, 20, {"success_roll_percent":0.0}, 1, resources, save, {"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912","tag_id":"BURST_HANDLING"})
		assert_eq(enhanced.outcome, "BLOCKED", "Stale enhancement also preserves event facts")
		assert_eq(save.load_envelope().to_dict(), before)

class SaveBoundary:
	extends RefCounted
	var error: Error = OK
	var calls := 0
	func save_envelope(candidate) -> Error:
		calls += 1
		var restored = Envelope.from_dict(JSON.parse_string(JSON.stringify(candidate.to_dict())))
		return error if restored.validation_errors.is_empty() else ERR_INVALID_DATA

class OldBackupReadback extends SaveBoundary:
	var old_envelope
	func load_envelope():
		return Envelope.from_dict(old_envelope.to_dict())

func test_aqueduct_commit_readback_rejects_previous_prepared_backup():
	var source = _aqueduct_envelope()
	var uid = source.active_run.selected_item_uid
	var service = load("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd").new()
	var prepared = service.prepare_aqueduct_with_rolls(source, uid, "HANDLING", "BURST", [0, 0], SaveBoundary.new())
	var backup = OldBackupReadback.new()
	backup.old_envelope = prepared.envelope
	var result = service.resolve_prepared_aqueduct(prepared.envelope, uid, backup)
	assert_eq(result.status, "BLOCKED")
	assert_eq(result.get("reason", ""), "AQUEDUCT_READBACK_FAILED")
	backup.old_envelope = source
	var missing_record = service.prepare_aqueduct_with_rolls(source, uid, "HANDLING", "BURST", [0, 0], backup)
	assert_eq(missing_record.status, "BLOCKED")
	assert_eq(missing_record.get("reason", ""), "AQUEDUCT_READBACK_FAILED")

func test_aqueduct_report_uses_saved_work_purpose_and_contribution_without_mutation():
	var service = load("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd").new()
	assert_true(service.has_method("aqueduct_report"))
	if not service.has_method("aqueduct_report"):
		return
	for case in [["OUTPUT","BURST","AQ01"],["HANDLING","BURST","AQ02"],["OUTPUT","SUSTAIN","AQ03"],["HANDLING","SUSTAIN","AQ04"]]:
		var source = _aqueduct_envelope()
		var uid = source.active_run.selected_item_uid
		var save = SaveBoundary.new()
		var prepared = service.prepare_aqueduct_with_rolls(source, uid, case[0], case[1], [0, 99], save)
		var report = service.aqueduct_report(prepared.record)
		assert_eq(report.content_id, case[2])
		assert_true(report.body.contains("대여"))
		var resolved = service.resolve_prepared_aqueduct(prepared.envelope, uid, save)
		var record_before = resolved.record.duplicate(true)
		var calls_before = save.calls
		resolved.envelope.get_item(uid).enhancement_level = 99
		var final_report = service.aqueduct_report(resolved.record)
		assert_true(final_report.body.contains("+19"))
		assert_true(final_report.body.contains("기민 I"))
		assert_true(final_report.body.contains("기본"))
		assert_true(final_report.body.contains("태그 기여"))
		assert_true(final_report.body.contains("반환"))
		assert_eq(resolved.record, record_before)
		assert_eq(save.calls, calls_before)

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
