# Decision38 action-local recurring precision resolution and success-only effects.
extends "res://addons/gut/test.gd"

const PrecisionResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const TARGETS := [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


class MalformedCatalogResolver extends PrecisionResolverScript:
	var catalog_override: Dictionary = {}

	func _load_catalog() -> Dictionary:
		return catalog_override.duplicate(true)


func _item(level: int = 9, weight: int = 12):
	var item = ItemScript.new()
	item.uid = "BSI-0102030405060708090a0b0c0d0e0f10"
	item.enhancement_level = level
	item.highest_checkpoint = 10 if level >= 10 else 0
	item.raw_role_stat = 12
	item.weight_point = weight
	return item


func _add(lineage_id: String = "EMBER_LINEAGE", method_id: String = "EDGE_REINFORCEMENT") -> Dictionary:
	return {"action": "ADD_TAG", "lineage_id": lineage_id, "method_id": method_id}


func _upgrade(tag_id: String = "TAG_EMBER_EDGE") -> Dictionary:
	return {"action": "UPGRADE_TAG", "tag_id": tag_id}


func _seed(item, tag_id: String, stage: int = 1, milestones: Array[int] = [10]) -> void:
	item.catalyst_affix["tag_entries"] = [{
		"tag_id": tag_id,
		"stage": stage,
		"created_milestone": 10,
		"last_advanced_milestone": milestones.back(),
	}]
	item.used_precision_milestones.clear()
	for milestone in milestones:
		item.used_precision_milestones.append(milestone)


func test_every_catalog_target_requires_exact_entry_and_an_action_dictionary() -> void:
	var resolver = PrecisionResolverScript.new()
	for target in TARGETS:
		var item = _item(target - 1)
		var preview: Dictionary = resolver.selection_preview(item, target, _add())
		assert_true(bool(preview.get("allowed", false)), "target %d must accept ADD_TAG at exact entry" % target)
		assert_eq(preview.get("action", ""), "ADD_TAG")
		assert_eq(int(preview.get("target_level", -1)), target)
		assert_eq(item.catalyst_affix, ItemScript.empty_catalyst_affix(), "preview must not mutate catalog state")
		assert_eq(item.used_precision_milestones, [], "preview must not resolve milestones")

		item.enhancement_level = target
		var ordinary: Dictionary = resolver.selection_preview(item, target + 1, _add())
		assert_false(bool(ordinary.get("allowed", true)), "ordinary target %d must be blocked" % (target + 1))
		assert_eq(ordinary.get("reason", ""), "INVALID_PRECISION_ENTRY")


func test_first_target_only_allows_add_tag() -> void:
	var resolver = PrecisionResolverScript.new()
	var upgrade: Dictionary = resolver.selection_preview(_item(9), 10, _upgrade())
	assert_false(bool(upgrade.get("allowed", true)))
	assert_eq(upgrade.get("reason", ""), "PRECISION_ADD_REQUIRED")
	assert_true(bool(resolver.selection_preview(_item(9), 10, _add()).get("allowed", false)))


func test_later_target_adds_below_cap_and_rejects_duplicate_or_full_collection() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(19)
	_seed(item, "TAG_EMBER_EDGE")
	assert_true(bool(resolver.selection_preview(item, 20, _add("ANVIL_LINEAGE", "LIGHTWEIGHTING")).get("allowed", false)))

	var duplicate: Dictionary = resolver.selection_preview(item, 20, _add())
	assert_false(bool(duplicate.get("allowed", true)))
	assert_eq(duplicate.get("reason", ""), "DUPLICATE_PRECISION_TAG")

	item.catalyst_affix["tag_entries"] = [
		{"tag_id": "TAG_EMBER_EDGE", "stage": 1, "created_milestone": 10, "last_advanced_milestone": 10},
		{"tag_id": "TAG_EMBER_LIGHT", "stage": 1, "created_milestone": 20, "last_advanced_milestone": 20},
		{"tag_id": "TAG_ANVIL_EDGE", "stage": 1, "created_milestone": 30, "last_advanced_milestone": 30},
	]
	item.used_precision_milestones.clear()
	item.used_precision_milestones.append_array([10, 20, 30])
	item.enhancement_level = 39
	var full: Dictionary = resolver.selection_preview(item, 40, _add("ANVIL_LINEAGE", "LIGHTWEIGHTING"))
	assert_false(bool(full.get("allowed", true)))
	assert_eq(full.get("reason", ""), "PRECISION_TAG_CAP_REACHED")


func test_upgrade_applies_the_resolved_method_once_and_marks_only_target_twenty() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(19)
	_seed(item, "TAG_EMBER_EDGE")
	var raw_before: int = item.raw_role_stat
	var preview: Dictionary = resolver.selection_preview(item, 20, _upgrade())
	assert_true(bool(preview.get("allowed", false)))
	var result: Dictionary = resolver.apply_selection_success(item, 20, _upgrade())
	assert_true(bool(result.get("applied", false)))
	assert_eq(result.get("action", ""), "UPGRADE_TAG")
	assert_eq(int(result.get("stage_before", -1)), 1)
	assert_eq(int(result.get("stage_after", -1)), 2)
	assert_eq(item.raw_role_stat, raw_before + 3)
	assert_eq(item.used_precision_milestones, [10, 20])
	assert_eq(item.catalyst_affix["tag_entries"][0]["last_advanced_milestone"], 20)


func test_upgrade_advances_from_stage_one_to_four_then_blocks_mastered_tag() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(19)
	_seed(item, "TAG_EMBER_EDGE")
	for target in [20, 30, 40]:
		item.enhancement_level = target - 1
		var result: Dictionary = resolver.apply_selection_success(item, target, _upgrade())
		assert_true(bool(result.get("applied", false)))
	assert_eq(item.catalyst_affix["tag_entries"][0]["stage"], 4)
	item.enhancement_level = 49
	var mastered: Dictionary = resolver.selection_preview(item, 50, _upgrade())
	assert_false(bool(mastered.get("allowed", true)))
	assert_eq(mastered.get("reason", ""), "PRECISION_TAG_MASTERED")


func test_lightweighting_blocks_when_effect_would_have_zero_weight() -> void:
	var resolver = PrecisionResolverScript.new()
	var blocked: Dictionary = resolver.selection_preview(_item(9, 0), 10, _add("EMBER_LINEAGE", "LIGHTWEIGHTING"))
	assert_false(bool(blocked.get("allowed", true)))
	assert_eq(blocked.get("reason", ""), "PRECISION_EFFECT_UNAVAILABLE")


func test_success_only_mutates_once_and_preserves_non_precision_and_durability_fields() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(9)
	item.grade_affix = "GRADE_KEEP"
	item.chronicle_affix = "CHRONICLE_KEEP"
	item.current_durability = 3
	item.max_durability = 4
	item.base_max_durability = 5
	var before: Dictionary = item.to_dict()
	var malformed: Dictionary = resolver.apply_selection_success(item, 10, {"action": "ADD_TAG"})
	assert_false(bool(malformed.get("applied", true)))
	assert_eq(item.to_dict(), before, "blocked result must preserve full item snapshot")

	var success: Dictionary = resolver.apply_selection_success(item, 10, _add())
	assert_true(bool(success.get("applied", false)))
	assert_eq(item.grade_affix, "GRADE_KEEP")
	assert_eq(item.chronicle_affix, "CHRONICLE_KEEP")
	assert_eq(item.current_durability, 3)
	assert_eq(item.max_durability, 4)
	assert_eq(item.base_max_durability, 5)
	var after_success: Dictionary = item.to_dict()
	var repeated: Dictionary = resolver.apply_selection_success(item, 10, _add())
	assert_false(bool(repeated.get("applied", true)))
	assert_eq(item.to_dict(), after_success, "repeated resolver call must not reapply effect")


func test_malformed_tag_history_or_duplicate_resolved_milestone_fails_closed_without_mutation() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(19)
	_seed(item, "TAG_EMBER_EDGE")
	item.used_precision_milestones.append(10)
	var duplicate_snapshot: Dictionary = item.to_dict()
	var duplicate: Dictionary = resolver.apply_selection_success(item, 20, _upgrade())
	assert_false(bool(duplicate.get("applied", true)))
	assert_eq(duplicate.get("reason", ""), "INVALID_PRECISION_MILESTONE_STATE")
	assert_eq(item.to_dict(), duplicate_snapshot)

	item.used_precision_milestones.clear()
	item.used_precision_milestones.append(10)
	item.catalyst_affix["tag_entries"][0]["last_advanced_milestone"] = 20
	var orphaned_snapshot: Dictionary = item.to_dict()
	var orphaned: Dictionary = resolver.apply_selection_success(item, 20, _upgrade())
	assert_false(bool(orphaned.get("applied", true)))
	assert_eq(orphaned.get("reason", ""), "INVALID_PRECISION_MILESTONE_STATE")
	assert_eq(item.to_dict(), orphaned_snapshot)


func test_stage_three_history_without_a_complete_milestone_assignment_is_blocked_and_immutable() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(39)
	item.catalyst_affix["tag_entries"] = [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 3,
		"created_milestone": 10,
		"last_advanced_milestone": 20,
	}]
	item.used_precision_milestones.append_array([10, 20, 30])
	var snapshot: Dictionary = item.to_dict()

	var preview: Dictionary = resolver.selection_preview(item, 40, _add("ANVIL_LINEAGE", "LIGHTWEIGHTING"))
	assert_false(bool(preview.get("allowed", true)))
	assert_eq(preview.get("reason", ""), "INVALID_PRECISION_MILESTONE_STATE")
	var applied: Dictionary = resolver.apply_selection_success(item, 40, _add("ANVIL_LINEAGE", "LIGHTWEIGHTING"))
	assert_false(bool(applied.get("applied", true)))
	assert_eq(applied.get("reason", ""), "INVALID_PRECISION_MILESTONE_STATE")
	assert_eq(item.to_dict(), snapshot)


func test_stage_three_history_with_a_complete_internal_milestone_assignment_is_allowed() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(39)
	item.catalyst_affix["tag_entries"] = [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 3,
		"created_milestone": 10,
		"last_advanced_milestone": 30,
	}]
	item.used_precision_milestones.append_array([10, 20, 30])

	var preview: Dictionary = resolver.selection_preview(item, 40, _add("ANVIL_LINEAGE", "LIGHTWEIGHTING"))
	assert_true(bool(preview.get("allowed", false)))
	assert_eq(preview.get("reason", ""), "OK")


func test_multiple_stage_three_entries_find_a_unique_complete_assignment() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(69)
	item.catalyst_affix["tag_entries"] = [
		{"tag_id": "TAG_EMBER_EDGE", "stage": 3, "created_milestone": 10, "last_advanced_milestone": 60},
		{"tag_id": "TAG_ANVIL_EDGE", "stage": 3, "created_milestone": 20, "last_advanced_milestone": 40},
	]
	item.used_precision_milestones.append_array([10, 20, 30, 40, 50, 60])

	var preview: Dictionary = resolver.selection_preview(item, 70, _upgrade("TAG_EMBER_EDGE"))
	assert_true(bool(preview.get("allowed", false)))
	assert_eq(preview.get("reason", ""), "OK")


func test_impossible_normal_history_is_blocked_and_immutable() -> void:
	var resolver = PrecisionResolverScript.new()
	var cases: Array = []

	var no_entries: VSItem = _item(19)
	no_entries.used_precision_milestones.append(10)
	cases.append(no_entries)

	var stage_four_one_action: VSItem = _item(19)
	_seed(stage_four_one_action, "TAG_EMBER_EDGE", 4)
	cases.append(stage_four_one_action)

	var reverse_history: VSItem = _item(19)
	_seed(reverse_history, "TAG_EMBER_EDGE", 2, [10, 20])
	reverse_history.catalyst_affix["tag_entries"][0]["created_milestone"] = 20
	reverse_history.catalyst_affix["tag_entries"][0]["last_advanced_milestone"] = 10
	cases.append(reverse_history)

	var future_action: VSItem = _item(19)
	future_action.catalyst_affix["tag_entries"] = [{
		"tag_id": "TAG_EMBER_EDGE", "stage": 1, "created_milestone": 30, "last_advanced_milestone": 30,
	}]
	future_action.used_precision_milestones.append(30)
	cases.append(future_action)

	var shared_seed_action: VSItem = _item(19)
	shared_seed_action.catalyst_affix["tag_entries"] = [
		{"tag_id": "TAG_EMBER_EDGE", "stage": 1, "created_milestone": 10, "last_advanced_milestone": 10},
		{"tag_id": "TAG_EMBER_LIGHT", "stage": 1, "created_milestone": 10, "last_advanced_milestone": 10},
	]
	shared_seed_action.used_precision_milestones.append_array([10, 20])
	cases.append(shared_seed_action)

	for item in cases:
		var snapshot: Dictionary = item.to_dict()
		var preview: Dictionary = resolver.selection_preview(item, 20, _upgrade())
		assert_false(bool(preview.get("allowed", true)))
		assert_eq(preview.get("reason", ""), "INVALID_PRECISION_MILESTONE_STATE")
		var applied: Dictionary = resolver.apply_selection_success(item, 20, _upgrade())
		assert_false(bool(applied.get("applied", true)))
		assert_eq(applied.get("reason", ""), "INVALID_PRECISION_MILESTONE_STATE")
		assert_eq(item.to_dict(), snapshot)


func test_malformed_catalog_display_or_duplicate_coordinates_blocks_before_display_resolution() -> void:
	var baseline := PrecisionResolverScript.new().catalog()
	for malformed_catalog in [
		_catalog_without_method_display(baseline),
		_catalog_without_tag_display(baseline),
		_catalog_with_duplicate_tag_coordinate(baseline),
	]:
		var resolver := MalformedCatalogResolver.new()
		resolver.catalog_override = malformed_catalog
		var item = _item(9)
		var snapshot: Dictionary = item.to_dict()
		var preview: Dictionary = resolver.selection_preview(item, 10, _add())
		assert_false(bool(preview.get("allowed", true)))
		assert_eq(preview.get("reason", ""), "PRECISION_TAG_CATALOG_INVALID")
		var applied: Dictionary = resolver.apply_selection_success(item, 10, _add())
		assert_false(bool(applied.get("applied", true)))
		assert_eq(applied.get("reason", ""), "PRECISION_TAG_CATALOG_INVALID")
		assert_eq(item.to_dict(), snapshot)


func _catalog_without_method_display(catalog_data: Dictionary) -> Dictionary:
	var malformed := catalog_data.duplicate(true)
	malformed["methods"][0].erase("display_name_ko")
	return malformed


func _catalog_without_tag_display(catalog_data: Dictionary) -> Dictionary:
	var malformed := catalog_data.duplicate(true)
	malformed["tags"][0]["display_name_ko"] = ""
	return malformed


func _catalog_with_duplicate_tag_coordinate(catalog_data: Dictionary) -> Dictionary:
	var malformed := catalog_data.duplicate(true)
	malformed["tags"][1]["lineage_id"] = malformed["tags"][0]["lineage_id"]
	malformed["tags"][1]["method_id"] = malformed["tags"][0]["method_id"]
	return malformed


func test_pending_initial_backfill_is_no_cost_seed_transition_without_effect_reapplication() -> void:
	var resolver = PrecisionResolverScript.new()
	var item = _item(10)
	item.catalyst_affix["initial_tag_backfill_pending"] = true
	var raw_before: int = item.raw_role_stat
	var result: Dictionary = resolver.backfill_initial_tag(item, _add("ANVIL_LINEAGE", "EDGE_REINFORCEMENT"))
	assert_true(bool(result.get("applied", false)))
	assert_eq(result.get("cost_or_roll", ""), "NONE")
	assert_eq(item.raw_role_stat, raw_before, "migration must not reapply an already-owned effect")
	assert_eq(item.used_precision_milestones, [10])
	assert_eq(item.catalyst_affix["tag_entries"], [{
		"tag_id": "TAG_ANVIL_EDGE", "stage": 1, "created_milestone": 10, "last_advanced_milestone": 10,
	}])
	assert_false(bool(item.catalyst_affix["initial_tag_backfill_pending"]))
	var snapshot: Dictionary = item.to_dict()
	assert_false(bool(resolver.backfill_initial_tag(item, _add("ANVIL_LINEAGE", "EDGE_REINFORCEMENT")).get("applied", true)))
	assert_eq(item.to_dict(), snapshot)
