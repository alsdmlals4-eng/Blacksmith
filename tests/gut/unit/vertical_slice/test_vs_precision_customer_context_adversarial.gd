extends "res://addons/gut/test.gd"

const ContextPacketScript = preload("res://scripts/vertical_slice/domain/vs_customer_context_packet.gd")
const ContextResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_customer_context_resolver.gd")
const PrecisionResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")
const CustomerProfileScript = preload("res://scripts/vertical_slice/domain/vs_customer_profile.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const NADIA_PATH := "res://data/vertical_slice/customers/nadia_venn.json"


func _customer():
	var customer = CustomerProfileScript.new()
	customer.customer_id = "SYNTHETIC_CUSTOMER"
	customer.public_standing_grade = "COMMON"
	return customer


func _item(level: int = 10):
	var item = ItemScript.new()
	item.enhancement_level = level
	item.highest_checkpoint = 10 if level >= 10 else 0
	item.weight_point = 10
	item.physical_state = "ACTIVE"
	return item


func _valid_context(risk: int, ability: int, proficiency: int):
	var context = ContextPacketScript.new()
	context.customer_id = "SYNTHETIC_CUSTOMER"
	context.content_id = "SYNTHETIC_CONTENT"
	context.primary_need = "SAFE_RETURN"
	context.secondary_need = "RECOVERY_POSSIBILITY"
	context.risk = risk
	context.strength = 10
	context.constitution = ability
	context.weapon_proficiency = proficiency
	context.related_ability = "CONSTITUTION"
	return context


func test_invalid_external_context_fails_closed_in_customer_and_precision_resolvers() -> void:
	var invalid = ContextPacketScript.from_dict({})
	assert_false(invalid.validation_errors.is_empty(), "empty external context must be invalid")
	var evaluation = ContextResolverScript.new().evaluate(_customer(), _item(), invalid)
	assert_eq(evaluation.get("status", ""), "BLOCKED")
	assert_eq(evaluation.get("reason", ""), "INVALID_CONTEXT")
	assert_false(evaluation.has("final_primary_estimate"))
	var precision = PrecisionResolverScript.new().preview(_item(), 10, "EDGE_REINFORCEMENT", "", invalid)
	assert_false(bool(precision.get("allowed", true)))
	assert_eq(precision.get("reason", ""), "INVALID_CONTEXT")


func test_primary_estimate_respects_five_and_ninety_five_percent_clamps() -> void:
	var low = ContextResolverScript.new().evaluate(_customer(), _item(0), _valid_context(20, 0, 0))
	assert_eq(int(low.get("final_primary_estimate", -1)), 5)
	var high = ContextResolverScript.new().evaluate(_customer(), _item(100), _valid_context(0, 10, 3))
	assert_eq(int(high.get("final_primary_estimate", -1)), 95)


func test_precision_unknown_inputs_fail_closed() -> void:
	var resolver = PrecisionResolverScript.new()
	var context = _valid_context(5, 5, 1)
	var bad_milestone = resolver.preview(_item(10), 15, "EDGE_REINFORCEMENT", "", context)
	assert_false(bool(bad_milestone.get("allowed", true)))
	assert_eq(bad_milestone.get("reason", ""), "INVALID_PRECISION_MILESTONE")
	var retired_milestone = resolver.preview(_item(20), 20, "EDGE_REINFORCEMENT", "", context)
	assert_false(bool(retired_milestone.get("allowed", true)))
	assert_eq(retired_milestone.get("reason", ""), "INVALID_PRECISION_MILESTONE")
	var bad_method = resolver.preview(_item(10), 10, "UNKNOWN_METHOD", "", context)
	assert_false(bool(bad_method.get("allowed", true)))
	assert_eq(bad_method.get("reason", ""), "UNKNOWN_PRECISION_METHOD")


func test_nadia_product_data_still_refuses_unapproved_numeric_capability_invention() -> void:
	var file := FileAccess.open(NADIA_PATH, FileAccess.READ)
	assert_not_null(file, "Nadia product data must remain readable")
	if file == null:
		return
	var parsed = JSON.parse_string(file.get_as_text())
	assert_true(parsed is Dictionary, "Nadia data must parse as a dictionary")
	if not (parsed is Dictionary):
		return
	assert_eq(parsed.get("numeric_capability_profile", ""), "SEPARATE_CANON_SOURCE_REQUIRED")
	for forbidden in ["risk", "strength", "dexterity", "constitution", "judgment", "weapon_proficiency"]:
		assert_false(parsed.has(forbidden), "Task4 must not invent Nadia numeric capability: %s" % forbidden)
