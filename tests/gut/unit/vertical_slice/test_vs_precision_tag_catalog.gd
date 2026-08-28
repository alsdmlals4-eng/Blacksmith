# Decision37 정밀 태그 표가 현재 무기 소유권과 단일 적용 경계를 지키는지 검증한다.
extends "res://addons/gut/test.gd"

const PrecisionResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _item(level: int = 9) -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-0102030405060708090a0b0c0d0e0f10"
	item.enhancement_level = level
	item.highest_checkpoint = 10 if level >= 10 else 0
	item.raw_role_stat = 12
	item.weight_point = 2
	return item


func _ember_edge() -> Dictionary:
	return {"lineage_id": "EMBER_LINEAGE", "method_id": "EDGE_REINFORCEMENT"}


func _anvil_light() -> Dictionary:
	return {"lineage_id": "ANVIL_LINEAGE", "method_id": "LIGHTWEIGHTING"}


func test_selection_preview_blocks_missing_lineage_before_resolving_tag() -> void:
	var resolver = PrecisionResolverScript.new()
	assert_true(resolver.has_method("selection_preview"), "Decision37 requires a catalog-backed selection preview")
	if not resolver.has_method("selection_preview"):
		return
	var result: Dictionary = resolver.selection_preview(_item(), 10, {})
	assert_false(bool(result.get("allowed", true)))
	assert_eq(result.get("reason", ""), "MISSING_CATALYST_LINEAGE")


func test_selection_preview_resolves_exact_catalog_tag_and_effect() -> void:
	var resolver = PrecisionResolverScript.new()
	assert_true(resolver.has_method("selection_preview"), "Decision37 requires exact 2x2 catalog resolution")
	if not resolver.has_method("selection_preview"):
		return
	var edge: Dictionary = resolver.selection_preview(_item(), 10, _ember_edge())
	assert_true(bool(edge.get("allowed", false)))
	assert_eq(edge.get("tag_id", ""), "TAG_EMBER_EDGE")
	assert_eq(edge.get("tag_display_name_ko", ""), "불씨의 예리함")
	assert_eq(edge.get("effect_axis", ""), "RAW_ROLE_STAT")
	assert_eq(int(edge.get("effect_delta", 0)), 3)
	assert_eq(int(edge.get("before_value", -1)), 12)
	assert_eq(int(edge.get("after_value", -1)), 15)
	assert_eq(int(edge.get("durability_delta", -1)), 0)

	var light: Dictionary = resolver.selection_preview(_item(), 10, _anvil_light())
	assert_true(bool(light.get("allowed", false)))
	assert_eq(light.get("tag_id", ""), "TAG_ANVIL_LIGHT")
	assert_eq(light.get("tag_display_name_ko", ""), "모루의 가벼움")
	assert_eq(light.get("effect_axis", ""), "WEIGHT_POINT")
	assert_eq(int(light.get("effect_delta", 0)), -3)
	assert_eq(int(light.get("before_value", -1)), 2)
	assert_eq(int(light.get("after_value", -1)), 0)


func test_success_applies_only_one_tag_and_method_effect_without_other_affix_mutation() -> void:
	var resolver = PrecisionResolverScript.new()
	assert_true(resolver.has_method("apply_selection_success"), "Decision37 success must have one explicit application boundary")
	if not resolver.has_method("apply_selection_success"):
		return
	var item := _item()
	item.grade_affix = "GRADE_KEEP"
	item.chronicle_affix = "EVENT_KEEP"
	var result: Dictionary = resolver.apply_selection_success(item, _ember_edge())
	assert_true(bool(result.get("applied", false)))
	assert_eq(item.catalyst_affix, "TAG_EMBER_EDGE")
	assert_eq(item.raw_role_stat, 15)
	assert_eq(item.weight_point, 2)
	assert_eq(item.grade_affix, "GRADE_KEEP")
	assert_eq(item.chronicle_affix, "EVENT_KEEP")
	var second: Dictionary = resolver.apply_selection_success(item, _ember_edge())
	assert_false(bool(second.get("applied", true)))
	assert_eq(second.get("reason", ""), "CATALYST_AFFIX_ALREADY_RESOLVED")
	assert_eq(item.raw_role_stat, 15)


func test_placeholder_backfill_is_free_apply_once_and_fails_closed_for_unknown_affix() -> void:
	var resolver = PrecisionResolverScript.new()
	assert_true(resolver.has_method("backfill_placeholder"), "Decision37 placeholder migration needs a dedicated one-time boundary")
	if not resolver.has_method("backfill_placeholder"):
		return
	var placeholder := _item(10)
	placeholder.catalyst_affix = "PRECISION_KEYWORD_PENDING_CONTENT"
	var source_blocked: Dictionary = resolver.backfill_placeholder(placeholder, _anvil_light())
	assert_false(bool(source_blocked.get("applied", true)))
	assert_eq(source_blocked.get("reason", ""), "PRECISION_PLACEHOLDER_SOURCE_INELIGIBLE")
	assert_eq(placeholder.catalyst_affix, "PRECISION_KEYWORD_PENDING_CONTENT")
	var result: Dictionary = resolver.backfill_placeholder(placeholder, _anvil_light(), true)
	assert_true(bool(result.get("applied", false)))
	assert_eq(result.get("cost_or_roll", ""), "NONE")
	assert_eq(placeholder.catalyst_affix, "TAG_ANVIL_LIGHT")
	assert_eq(placeholder.weight_point, 0)
	var repeat: Dictionary = resolver.backfill_placeholder(placeholder, _anvil_light(), true)
	assert_false(bool(repeat.get("applied", true)))
	assert_eq(repeat.get("reason", ""), "CATALYST_AFFIX_ALREADY_RESOLVED")
	assert_eq(placeholder.weight_point, 0)

	var unknown := _item(10)
	unknown.catalyst_affix = "UNKNOWN_NONEMPTY_AFFIX"
	var unknown_result: Dictionary = resolver.backfill_placeholder(unknown, _ember_edge(), true)
	assert_false(bool(unknown_result.get("applied", true)))
	assert_eq(unknown_result.get("reason", ""), "CATALYST_AFFIX_UNKNOWN_FAIL_CLOSED")
	assert_eq(unknown.catalyst_affix, "UNKNOWN_NONEMPTY_AFFIX")
	assert_eq(unknown.raw_role_stat, 12)
