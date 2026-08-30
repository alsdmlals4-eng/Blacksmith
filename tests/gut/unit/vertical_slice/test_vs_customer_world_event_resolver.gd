extends "res://addons/gut/test.gd"

const RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_customer_world_event_resolver.gd"
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")

const ITEM_UID := "BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


func _item():
	var item = ItemScript.new()
	item.uid = ITEM_UID
	item.birth_rng_seed = 818181
	item.primary_material_id = "meteor_iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.crafting_grade = "CRAFT_LEGENDARY"
	item.artistry = 8
	item.raw_role_stat = 20
	item.weight_point = 20
	item.function_capacity = 1
	item.functions.assign(["ELEMENTAL_WARD_FIRE"])
	item.grade_affix = "LEGENDARY_EDGE"
	item.catalyst_affix = {
		"schema_version": 1,
		"tag_entries": [{
			"tag_id": "TAG_EMBER_EDGE",
			"stage": 1,
			"created_milestone": 10,
			"last_advanced_milestone": 10,
		}],
		"initial_tag_backfill_pending": false,
		"unreadable_legacy_affix": "",
	}
	item.chronicle_affix = "ARENA_TESTED"
	item.enhancement_level = 10
	item.used_precision_milestones.assign([10])
	item.highest_checkpoint = 10
	item.owner_id = "NADIA_VENN"
	return item


func _envelope():
	var envelope = SaveEnvelopeScript.new()
	envelope.saved_at_utc = "2026-08-27T00:00:00Z"
	envelope.active_run = {
		"run_id": "RUN-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
		"run_rng_seed": 998877,
		"current_day": 4,
		"resolved_events": {},
		"selected_item_uid": ITEM_UID,
	}
	assert_eq(envelope.add_item(_item()), OK)
	return envelope


func _nadia_result() -> Dictionary:
	return {
		"schema_version": 1,
		"record_type": "CONTENT_RESULT_V1",
		"event_id": "nadia-actual-use-001",
		"source_decision_id": "BS-CONTENT-20260811-01",
		"content_id": "ADVENTURER_01",
		"customer_id": "NADIA_VENN",
		"occurred_at_game_day": 4,
		"item_refs": [{"role": "PRIMARY_ITEM", "uid": ITEM_UID}],
		"result_axes": {
			"EXPEDITION_RETURN_STATE": "RETURNED",
			"RECOVERY_STATE": "PARTIAL_RECOVERY",
			"ITEM_UID_LIFECYCLE_STATE": "DAMAGED_RETURN",
		},
		"causal_reasons": ["LOAD_GATE_PASSED", "UTILITY_MATCHED"],
		"primary_next_action": "REPAIR_ITEM",
	}


func test_direct_actual_use_applies_one_current_damage_and_persists_same_uid_result() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "customer world event resolver must exist")
	if not ResourceLoader.exists(RESOLVER_PATH):
		return
	var resolver = load(RESOLVER_PATH).new()
	var envelope = _envelope()
	var item = envelope.get_item(ITEM_UID)
	var result: Dictionary = resolver.resolve(envelope, ITEM_UID, {
		"content_result": _nadia_result(),
		"actual_item_use": true,
		"damage_profile": "DIRECT",
		"damage_cause": "CAVE_IN_DIRECT_HIT",
	}, 100.0)
	assert_eq(result.get("status", ""), "APPLIED")
	assert_true(bool(result.get("damage_applied", false)))
	assert_eq(item.current_durability, 4)
	assert_eq(item.max_durability, 5, "actual-use damage must not scar MAX durability")
	assert_true(item.repair_job_available)
	assert_eq(
		envelope.active_run["resolved_events"].get("nadia-actual-use-001", {}).get("item_refs", []),
		[{"role": "PRIMARY_ITEM", "uid": ITEM_UID}],
		"persisted customer result must retain the same item UID"
	)
	assert_eq(
		envelope.active_run["resolved_events"].get("nadia-actual-use-001", {}).get("durability_consequence", {}),
		{
			"actual_item_use": true,
			"damage_applied": true,
			"damage_cause": "CAVE_IN_DIRECT_HIT",
			"declared_damage_profile": "DIRECT",
			"effective_damage_profile": "DIRECT",
			"before_current_durability": 5,
			"after_current_durability": 4,
			"before_max_durability": 5,
			"after_max_durability": 5,
			"repair_job_available": true,
		},
		"same-UID result must persist the factual durability consequence for a later result surface"
	)


func test_handoff_without_actual_use_persists_result_but_never_damages() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "customer world event resolver must exist")
	if not ResourceLoader.exists(RESOLVER_PATH):
		return
	var resolver = load(RESOLVER_PATH).new()
	var envelope = _envelope()
	var item = envelope.get_item(ITEM_UID)
	var result: Dictionary = resolver.resolve(envelope, ITEM_UID, {
		"content_result": _nadia_result(),
		"actual_item_use": false,
		"damage_profile": "HIGH",
		"damage_cause": "HANDOFF_ONLY",
	}, 0.0)
	assert_eq(result.get("status", ""), "APPLIED")
	assert_false(bool(result.get("damage_applied", true)))
	assert_eq(result.get("effective_damage_profile", ""), "NONE")
	assert_eq(item.current_durability, 5)
	assert_eq(item.max_durability, 5)
	assert_false(item.repair_job_available)
	assert_true(envelope.active_run["resolved_events"].has("nadia-actual-use-001"))


func test_explicit_relevant_protection_reduces_only_one_probabilistic_profile_step() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "customer world event resolver must exist")
	if not ResourceLoader.exists(RESOLVER_PATH):
		return
	var resolver = load(RESOLVER_PATH).new()
	var envelope = _envelope()
	var item = envelope.get_item(ITEM_UID)
	item.functions.assign(["CAVE_IN_BRACING"])
	var event := {
		"content_result": _nadia_result(),
		"actual_item_use": true,
		"damage_profile": "MEDIUM",
		"damage_cause": "CAVE_IN_DEBRIS",
		"relevant_protection_function_id": "CAVE_IN_BRACING",
	}
	var result: Dictionary = resolver.resolve(envelope, ITEM_UID, event, 15.0)
	assert_eq(result.get("status", ""), "APPLIED")
	assert_eq(result.get("effective_damage_profile", ""), "LOW")
	assert_eq(float(result.get("damage_percent", -1.0)), 10.0)
	assert_false(bool(result.get("damage_applied", true)), "15% must miss the reduced 10% profile")
	assert_eq(item.current_durability, 5)


func test_major_state_multiplier_is_applied_before_one_damage_roll_and_duplicate_event_is_blocked() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "customer world event resolver must exist")
	if not ResourceLoader.exists(RESOLVER_PATH):
		return
	var resolver = load(RESOLVER_PATH).new()
	var envelope = _envelope()
	var item = envelope.get_item(ITEM_UID)
	item.current_durability = 2
	item.max_durability = 2
	var event := {
		"content_result": _nadia_result(),
		"actual_item_use": true,
		"damage_profile": "HIGH",
		"damage_cause": "CAVE_IN_DEBRIS",
	}
	var first: Dictionary = resolver.resolve(envelope, ITEM_UID, event, 69.0)
	assert_eq(first.get("status", ""), "APPLIED")
	assert_eq(float(first.get("damage_percent", -1.0)), 70.0)
	assert_true(bool(first.get("damage_applied", false)))
	assert_eq(item.current_durability, 1)
	assert_eq(item.max_durability, 2)
	var second: Dictionary = resolver.resolve(envelope, ITEM_UID, event, 0.0)
	assert_eq(second.get("status", ""), "BLOCKED")
	assert_eq(second.get("reason", ""), "EVENT_ALREADY_RESOLVED")
	assert_eq(item.current_durability, 1, "duplicate resolution must not consume another damage event")


func test_invalid_damage_roll_blocks_before_result_or_item_mutation() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "customer world event resolver must exist")
	if not ResourceLoader.exists(RESOLVER_PATH):
		return
	var resolver = load(RESOLVER_PATH).new()
	var envelope = _envelope()
	var item = envelope.get_item(ITEM_UID)
	var result: Dictionary = resolver.resolve(envelope, ITEM_UID, {
		"content_result": _nadia_result(),
		"actual_item_use": true,
		"damage_profile": "LOW",
		"damage_cause": "CAVE_IN_DEBRIS",
	}, -0.1)
	assert_eq(result.get("status", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "INVALID_DAMAGE_ROLL")
	assert_eq(item.current_durability, 5)
	assert_false(envelope.active_run["resolved_events"].has("nadia-actual-use-001"))


func test_non_dictionary_content_result_fails_closed_before_item_mutation() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "customer world event resolver must exist")
	if not ResourceLoader.exists(RESOLVER_PATH):
		return
	var resolver = load(RESOLVER_PATH).new()
	var envelope = _envelope()
	var item = envelope.get_item(ITEM_UID)
	var result: Dictionary = resolver.resolve(envelope, ITEM_UID, {
		"content_result": "not-a-record",
		"actual_item_use": true,
		"damage_profile": "LOW",
		"damage_cause": "CAVE_IN_DEBRIS",
	}, 0.0)
	assert_eq(result.get("status", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "INVALID_CONTENT_RESULT")
	assert_eq(item.current_durability, 5)
	assert_true(envelope.active_run["resolved_events"].is_empty())


func test_missing_resolved_events_or_invalid_envelope_blocks_before_item_mutation() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "customer world event resolver must exist")
	if not ResourceLoader.exists(RESOLVER_PATH):
		return
	var resolver = load(RESOLVER_PATH).new()
	var missing_events = _envelope()
	var missing_events_item = missing_events.get_item(ITEM_UID)
	missing_events.active_run.erase("resolved_events")
	var missing_result: Dictionary = resolver.resolve(missing_events, ITEM_UID, {
		"content_result": _nadia_result(),
		"actual_item_use": true,
		"damage_profile": "DIRECT",
		"damage_cause": "CAVE_IN_DIRECT_HIT",
	}, 0.0)
	assert_eq(missing_result.get("status", ""), "BLOCKED")
	assert_eq(missing_result.get("reason", ""), "INVALID_RESOLVED_EVENTS")
	assert_eq(missing_events_item.current_durability, 5)

	var invalid_envelope = _envelope()
	var invalid_item = invalid_envelope.get_item(ITEM_UID)
	invalid_envelope.validation_errors.append("MISSING_ACTIVE_RUN_FIELD:resolved_events")
	var invalid_result: Dictionary = resolver.resolve(invalid_envelope, ITEM_UID, {
		"content_result": _nadia_result(),
		"actual_item_use": true,
		"damage_profile": "DIRECT",
		"damage_cause": "CAVE_IN_DIRECT_HIT",
	}, 0.0)
	assert_eq(invalid_result.get("status", ""), "BLOCKED")
	assert_eq(invalid_result.get("reason", ""), "INVALID_ENVELOPE")
	assert_eq(invalid_item.current_durability, 5)


func test_non_finite_roll_and_non_string_damage_cause_fail_closed() -> void:
	assert_true(ResourceLoader.exists(RESOLVER_PATH), "customer world event resolver must exist")
	if not ResourceLoader.exists(RESOLVER_PATH):
		return
	var resolver = load(RESOLVER_PATH).new()
	var nan_envelope = _envelope()
	var nan_item = nan_envelope.get_item(ITEM_UID)
	var nan_result: Dictionary = resolver.resolve(nan_envelope, ITEM_UID, {
		"content_result": _nadia_result(),
		"actual_item_use": true,
		"damage_profile": "LOW",
		"damage_cause": "CAVE_IN_DEBRIS",
	}, NAN)
	assert_eq(nan_result.get("status", ""), "BLOCKED")
	assert_eq(nan_result.get("reason", ""), "INVALID_DAMAGE_ROLL")
	assert_eq(nan_item.current_durability, 5)

	var cause_envelope = _envelope()
	var cause_item = cause_envelope.get_item(ITEM_UID)
	var cause_result: Dictionary = resolver.resolve(cause_envelope, ITEM_UID, {
		"content_result": _nadia_result(),
		"actual_item_use": true,
		"damage_profile": "LOW",
		"damage_cause": 123,
	}, 0.0)
	assert_eq(cause_result.get("status", ""), "BLOCKED")
	assert_eq(cause_result.get("reason", ""), "INVALID_DAMAGE_CAUSE")
	assert_eq(cause_item.current_durability, 5)
