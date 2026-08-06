extends SceneTree

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const LedgerEntryScript = preload("res://scripts/vertical_slice/domain/vs_ledger_entry.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("VSItem tests PASSED (5 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_round_trip_preserves_birth_facts()
	_test_round_trip_preserves_mutable_state()
	_test_missing_birth_fact_is_reported()
	_test_unsupported_schema_is_reported()
	_test_ledger_sequence_is_append_only()


func _make_item():
	var item = ItemScript.new()
	item.uid = "BSI-0123456789abcdef0123456789abcdef"
	item.birth_rng_seed = 712345
	item.primary_material_id = "iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.crafting_grade = "MASTERWORK"
	item.artistry = 7
	item.raw_role_stat = 15
	item.weight_point = 10
	item.function_capacity = 1
	item.functions = ["DISPLAY_ATTACK"]
	item.grade_affix = "MASTERWORK_EDGE"
	item.catalyst_affix = ""
	item.chronicle_affix = ""
	item.enhancement_level = 0
	item.enhancement_failure_streak = 0
	item.used_precision_milestones = []
	item.damage_state = "INTACT"
	item.owner_id = "PLAYER"
	return item


func _test_round_trip_preserves_birth_facts() -> void:
	var item = _make_item()
	var restored = ItemScript.from_dict(item.to_dict())
	_expect(restored.validation_errors.is_empty(), "valid item produced validation errors")
	_expect(restored.uid == item.uid, "UID changed during round trip")
	_expect(restored.birth_rng_seed == item.birth_rng_seed, "birth RNG seed changed")
	_expect(restored.crafting_grade == item.crafting_grade, "crafting grade changed")
	_expect(restored.artistry == item.artistry, "artistry changed")
	_expect(restored.raw_role_stat == item.raw_role_stat, "raw role stat changed")


func _test_round_trip_preserves_mutable_state() -> void:
	var item = _make_item()
	item.enhancement_level = 10
	item.enhancement_failure_streak = 2
	item.used_precision_milestones = [10]
	item.catalyst_affix = "EMBER_TOUCHED"
	item.chronicle_affix = "ARENA_TESTED"
	item.damage_state = "DAMAGED"
	item.owner_id = "customer_gladiator"
	var entry = LedgerEntryScript.create(1, "event-1", "ITEM_BORN", "BS-VS-20260806-01", "before", "after", 1, {"grade": item.crafting_grade})
	_expect(item.append_ledger_entry(entry.to_dict()) == OK, "first ledger entry should append")
	var restored = ItemScript.from_dict(item.to_dict())
	_expect(restored.enhancement_level == 10, "enhancement level changed")
	_expect(restored.used_precision_milestones == [10], "precision milestones changed")
	_expect(restored.catalyst_affix == "EMBER_TOUCHED", "catalyst affix changed")
	_expect(restored.chronicle_affix == "ARENA_TESTED", "chronicle affix changed")
	_expect(restored.damage_state == "DAMAGED", "damage state changed")
	_expect(restored.owner_id == "customer_gladiator", "owner changed")
	_expect(restored.ledger.size() == 1, "ledger entry disappeared")


func _test_missing_birth_fact_is_reported() -> void:
	var value = _make_item().to_dict()
	value.erase("birth_rng_seed")
	var restored = ItemScript.from_dict(value)
	_expect(not restored.validation_errors.is_empty(), "missing birth seed must be reported")
	_expect(restored.validation_errors.has("MISSING_REQUIRED_FIELD:birth_rng_seed"), "missing seed error code absent")


func _test_unsupported_schema_is_reported() -> void:
	var value = _make_item().to_dict()
	value["schema_version"] = 99
	var restored = ItemScript.from_dict(value)
	_expect(restored.validation_errors.has("UNSUPPORTED_ITEM_SCHEMA:99"), "unsupported schema must be reported")


func _test_ledger_sequence_is_append_only() -> void:
	var item = _make_item()
	var first = LedgerEntryScript.create(1, "event-1", "ITEM_BORN", "BS-VS-20260806-01", "", "a", 1, {})
	var duplicate = LedgerEntryScript.create(1, "event-2", "ENHANCEMENT", "BS-ENHANCE-20260806-01", "a", "b", 1, {})
	var skipped = LedgerEntryScript.create(3, "event-3", "ENHANCEMENT", "BS-ENHANCE-20260806-01", "b", "c", 1, {})
	var second = LedgerEntryScript.create(2, "event-2", "ENHANCEMENT", "BS-ENHANCE-20260806-01", "a", "b", 1, {})
	_expect(item.append_ledger_entry(first.to_dict()) == OK, "sequence 1 should append")
	_expect(item.append_ledger_entry(duplicate.to_dict()) == ERR_ALREADY_EXISTS, "duplicate sequence must fail")
	_expect(item.append_ledger_entry(skipped.to_dict()) == ERR_INVALID_DATA, "skipped sequence must fail")
	_expect(item.append_ledger_entry(second.to_dict()) == OK, "contiguous sequence 2 should append")
	_expect(item.ledger.size() == 2, "failed entries must not mutate ledger")


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
