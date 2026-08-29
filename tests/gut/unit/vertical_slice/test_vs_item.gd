extends "res://addons/gut/test.gd"

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const LedgerEntryScript = preload("res://scripts/vertical_slice/domain/vs_ledger_entry.gd")


func _make_item():
	var item = ItemScript.new()
	item.uid = "BSI-0123456789abcdef0123456789abcdef"
	item.birth_rng_seed = 712345
	item.primary_material_id = "iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.crafting_grade = "CRAFT_MASTERWORK"
	item.artistry = 7
	item.raw_role_stat = 15
	item.weight_point = 15
	item.function_capacity = 0
	item.functions.clear()
	item.grade_affix = "MASTERWORK_EDGE"
	item.chronicle_affix = ""
	item.enhancement_level = 0
	item.enhancement_failure_streak = 0
	item.used_precision_milestones.clear()
	item.damage_state = "INTACT"
	item.owner_id = "PLAYER"
	return item


func test_round_trip_preserves_birth_facts() -> void:
	var item = _make_item()
	var restored = ItemScript.from_dict(item.to_dict())
	assert_true(restored.validation_errors.is_empty(), "valid item produced validation errors")
	assert_eq(restored.uid, item.uid, "UID changed during round trip")
	assert_eq(restored.birth_rng_seed, item.birth_rng_seed, "birth RNG seed changed")
	assert_eq(restored.crafting_grade, item.crafting_grade, "crafting grade changed")
	assert_eq(restored.artistry, item.artistry, "artistry changed")
	assert_eq(restored.raw_role_stat, item.raw_role_stat, "raw role stat changed")


func test_round_trip_preserves_mutable_state() -> void:
	var item = _make_item()
	item.enhancement_level = 10
	item.enhancement_failure_streak = 2
	item.used_precision_milestones.assign([10])
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
	item.damage_state = "DAMAGED"
	item.owner_id = "customer_gladiator"
	var entry = LedgerEntryScript.create(
		1,
		"event-1",
		"ITEM_BORN",
		"BS-SAVE-20260806-01",
		"before",
		"after",
		1,
		{"grade": item.crafting_grade}
	)
	assert_eq(item.append_ledger_entry(entry.to_dict()), OK, "first ledger entry should append")
	var restored = ItemScript.from_dict(item.to_dict())
	assert_true(restored.validation_errors.is_empty(), "mutable state round trip produced errors")
	assert_eq(restored.enhancement_level, 10, "enhancement level changed")
	assert_eq(restored.used_precision_milestones, [10], "precision milestones changed")
	assert_eq(restored.catalyst_tag_entries()[0]["tag_id"], "TAG_EMBER_EDGE", "catalyst tag changed")
	assert_eq(restored.chronicle_affix, "ARENA_TESTED", "chronicle affix changed")
	assert_eq(restored.damage_state, "DAMAGED", "damage state changed")
	assert_eq(restored.owner_id, "customer_gladiator", "owner changed")
	assert_eq(restored.ledger.size(), 1, "ledger entry disappeared")
	assert_eq(restored.ledger[0]["occurred_at_game_day"], 1, "ledger day field changed")


func test_missing_birth_fact_is_reported() -> void:
	var value = _make_item().to_dict()
	value.erase("birth_rng_seed")
	var restored = ItemScript.from_dict(value)
	assert_true(
		restored.validation_errors.has("MISSING_REQUIRED_FIELD:birth_rng_seed"),
		"missing birth seed must be reported"
	)


func test_unsupported_grade_is_rejected() -> void:
	var value = _make_item().to_dict()
	value["crafting_grade"] = "RARE"
	var restored = ItemScript.from_dict(value)
	assert_true(
		restored.validation_errors.has("INVALID_CRAFTING_GRADE:RARE"),
		"legacy grade ID must be rejected"
	)


func test_ledger_sequence_is_append_only() -> void:
	var item = _make_item()
	var first = LedgerEntryScript.create(1, "event-1", "ITEM_BORN", "BS-SAVE-20260806-01", "", "a", 1, {})
	var duplicate_entry = LedgerEntryScript.create(1, "event-2", "ENHANCEMENT", "BS-ENHANCE-20260806-01", "a", "b", 1, {})
	var skipped = LedgerEntryScript.create(3, "event-3", "ENHANCEMENT", "BS-ENHANCE-20260806-01", "b", "c", 1, {})
	var second = LedgerEntryScript.create(2, "event-2", "ENHANCEMENT", "BS-ENHANCE-20260806-01", "a", "b", 1, {})
	assert_eq(item.append_ledger_entry(first.to_dict()), OK, "sequence 1 should append")
	assert_eq(item.append_ledger_entry(duplicate_entry.to_dict()), ERR_ALREADY_EXISTS, "duplicate sequence must fail")
	assert_eq(item.append_ledger_entry(skipped.to_dict()), ERR_INVALID_DATA, "skipped sequence must fail")
	assert_eq(item.append_ledger_entry(second.to_dict()), OK, "contiguous sequence 2 should append")
	assert_eq(item.ledger.size(), 2, "failed entries must not mutate ledger")


func _v3_item(catalyst_affix: String, level: int, milestones: Array) -> Dictionary:
	var legacy: Dictionary = _make_item().to_dict()
	legacy["schema_version"] = 3
	legacy["catalyst_affix"] = catalyst_affix
	legacy["enhancement_level"] = level
	legacy["used_precision_milestones"] = milestones.duplicate()
	return legacy


func test_v4_empty_catalyst_record_round_trips_without_shared_mutation() -> void:
	var item = _make_item()
	var restored = ItemScript.from_dict(item.to_dict())
	assert_true(restored.validation_errors.is_empty(), str(restored.validation_errors))
	assert_eq(restored.schema_version, 4)
	assert_eq(restored.catalyst_tag_entries(), [])
	assert_false(restored.has_initial_tag_backfill_pending())
	assert_false(restored.has_unreadable_catalyst_affix())
	var entries: Array = []
	entries.assign(restored.catalyst_tag_entries())
	entries.append({"tag_id": "TAG_EMBER_EDGE"})
	assert_eq(restored.catalyst_tag_entries(), [], "helper must not expose mutable record storage")


func test_v4_multi_tag_record_round_trips_with_resolved_precision_milestones() -> void:
	var value: Dictionary = _make_item().to_dict()
	value["schema_version"] = 4
	value["enhancement_level"] = 20
	value["used_precision_milestones"] = [10, 20]
	value["catalyst_affix"] = {
		"schema_version": 1,
		"tag_entries": [
			{"tag_id": "TAG_EMBER_EDGE", "stage": 2, "created_milestone": 10, "last_advanced_milestone": 20},
			{"tag_id": "TAG_ANVIL_LIGHT", "stage": 1, "created_milestone": 20, "last_advanced_milestone": 20},
		],
		"initial_tag_backfill_pending": false,
		"unreadable_legacy_affix": "",
	}
	var restored = ItemScript.from_dict(value)
	assert_true(restored.validation_errors.is_empty(), str(restored.validation_errors))
	assert_eq(restored.catalyst_tag_entries().size(), 2)
	assert_true(restored.precision_milestone_is_resolved(10))
	assert_true(restored.precision_milestone_is_resolved(20))
	assert_false(restored.precision_milestone_is_resolved(30))
	assert_eq(restored.to_dict()["catalyst_affix"], value["catalyst_affix"])


func test_v3_known_tag_migrates_to_seed_without_reapplying_legacy_effect() -> void:
	var legacy := _v3_item("TAG_EMBER_EDGE", 10, [])
	var raw_role_stat_before := int(legacy["raw_role_stat"])
	var item = ItemScript.from_dict(legacy)
	assert_true(item.validation_errors.is_empty(), str(item.validation_errors))
	assert_eq(item.schema_version, 4)
	assert_eq(item.catalyst_tag_entries()[0]["stage"], 1)
	assert_eq(item.used_precision_milestones, [10])
	assert_eq(item.raw_role_stat, raw_role_stat_before)


func test_v3_placeholder_migrates_to_item_owned_pending_state() -> void:
	var item = ItemScript.from_dict(_v3_item("PRECISION_KEYWORD_PENDING_CONTENT", 10, [10]))
	assert_true(item.validation_errors.is_empty(), str(item.validation_errors))
	assert_true(item.has_initial_tag_backfill_pending())
	assert_eq(item.catalyst_tag_entries(), [])
	assert_false(item.has_unreadable_catalyst_affix())


func test_v3_unknown_nonempty_affix_is_preserved_as_unreadable_state() -> void:
	var item = ItemScript.from_dict(_v3_item("UNKNOWN_NONEMPTY_AFFIX", 10, [10]))
	assert_true(item.validation_errors.is_empty(), str(item.validation_errors))
	assert_true(item.has_unreadable_catalyst_affix())
	assert_eq(item.to_dict()["catalyst_affix"]["unreadable_legacy_affix"], "UNKNOWN_NONEMPTY_AFFIX")
	assert_eq(item.catalyst_tag_entries(), [])


func test_v4_invalid_tag_collection_is_rejected_without_becoming_empty() -> void:
	var value: Dictionary = _make_item().to_dict()
	value["schema_version"] = 4
	value["used_precision_milestones"] = [10]
	value["catalyst_affix"] = {
		"schema_version": 1,
		"tag_entries": [
			{"tag_id": "TAG_EMBER_EDGE", "stage": 0, "created_milestone": 10, "last_advanced_milestone": 10},
			{"tag_id": "TAG_EMBER_EDGE", "stage": 5, "created_milestone": 20, "last_advanced_milestone": 20},
		],
		"initial_tag_backfill_pending": false,
		"unreadable_legacy_affix": "",
	}
	var restored = ItemScript.from_dict(value)
	assert_true(restored.validation_errors.has("INVALID_CATALYST_TAG_STAGE:TAG_EMBER_EDGE:0"))
	assert_true(restored.validation_errors.has("INVALID_CATALYST_TAG_STAGE:TAG_EMBER_EDGE:5"))
	assert_true(restored.validation_errors.has("DUPLICATE_CATALYST_TAG:TAG_EMBER_EDGE"))
	assert_true(restored.validation_errors.has("CATALYST_LAST_ADVANCE_NOT_USED:TAG_EMBER_EDGE:20"))
	assert_eq(restored.catalyst_tag_entries().size(), 2, "invalid collection must remain inspectable")
