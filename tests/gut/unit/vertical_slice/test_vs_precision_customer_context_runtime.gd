extends "res://addons/gut/test.gd"

const CONTEXT_PACKET_PATH := "res://scripts/vertical_slice/domain/vs_customer_context_packet.gd"
const CONTEXT_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_customer_context_resolver.gd"
const PRECISION_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd"
const ContextPacketScript = preload("res://scripts/vertical_slice/domain/vs_customer_context_packet.gd")
const ContextResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_customer_context_resolver.gd")
const CustomerProfileScript = preload("res://scripts/vertical_slice/domain/vs_customer_profile.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _script_has_method(script: Script, method_name: String) -> bool:
	for method in script.get_script_method_list():
		if str(method.get("name", "")) == method_name:
			return true
	return false


func _context(
	risk: int = 6,
	strength: int = 4,
	constitution: int = 6,
	proficiency: int = 2,
	required_function: String = ""
):
	var context = ContextPacketScript.new()
	context.customer_id = "SYNTHETIC_CUSTOMER"
	context.content_id = "SYNTHETIC_CONTENT"
	context.primary_need = "SAFE_RETURN"
	context.secondary_need = "RECOVERY_POSSIBILITY"
	context.known_context.append("RUINS")
	context.risk = risk
	context.strength = strength
	context.dexterity = 5
	context.constitution = constitution
	context.judgment = 5
	context.weapon_proficiency = proficiency
	context.related_ability = "CONSTITUTION"
	context.required_function_if_explicit = required_function
	context.relevant_precision_axes.append("WEIGHT")
	context.relevant_precision_axes.append("DURABILITY")
	return context


func _context_dict() -> Dictionary:
	return {
		"schema_version": 1,
		"customer_id": "SYNTHETIC_CUSTOMER",
		"content_id": "SYNTHETIC_CONTENT",
		"primary_need": "SAFE_RETURN",
		"secondary_need": "RECOVERY_POSSIBILITY",
		"known_context": ["RUINS"],
		"risk": 6,
		"strength": 4,
		"dexterity": 5,
		"constitution": 6,
		"judgment": 5,
		"weapon_proficiency": 2,
		"related_ability": "CONSTITUTION",
		"required_function_if_explicit": "",
		"relevant_precision_axes": ["WEIGHT", "DURABILITY"],
		"relevant_function_ids": [],
	}


func _customer(standing: String = "COMMON"):
	var customer = CustomerProfileScript.new()
	customer.customer_id = "SYNTHETIC_CUSTOMER"
	customer.public_standing_grade = standing
	return customer


func _item(weight: int = 40, enhancement: int = 10, function_ids: Array[String] = []):
	var item = ItemScript.new()
	item.weight_point = weight
	item.enhancement_level = enhancement
	item.highest_checkpoint = 10 if enhancement >= 10 else 0
	item.physical_state = "ACTIVE"
	for function_id in function_ids:
		item.functions.append(function_id)
	return item


func test_task4_runtime_surfaces_exist() -> void:
	assert_true(ResourceLoader.exists(CONTEXT_PACKET_PATH), "customer context packet must exist")
	assert_true(ResourceLoader.exists(CONTEXT_RESOLVER_PATH), "customer context resolver must exist")
	assert_true(ResourceLoader.exists(PRECISION_RESOLVER_PATH), "precision resolver must exist")


func test_context_packet_and_resolver_api_exist() -> void:
	var packet = load(CONTEXT_PACKET_PATH).new()
	var resolver = load(CONTEXT_RESOLVER_PATH).new()
	assert_true(packet.has_method("to_dict"), "context packet must serialize its external snapshot")
	assert_true(packet.has_method("maximum_load"), "context packet must expose the hard-load ceiling")
	assert_true(packet.has_method("related_ability_value"), "context packet must expose the selected contextual ability")
	assert_true(resolver.has_method("evaluate"), "context resolver must expose assignment evaluation")
	assert_true(resolver.has_method("enhancement_contribution_pp"), "context resolver must own Decision24 enhancement contribution")
	assert_true(resolver.has_method("proficiency_modifier_pp"), "context resolver must own proficiency mapping")


func test_context_numeric_primitives_match_decision24() -> void:
	var context = _context()
	var resolver = ContextResolverScript.new()
	assert_eq(context.maximum_load(), 40, "maximum load must be strength x 10")
	assert_eq(context.related_ability_value(), 6, "selected CONSTITUTION must resolve from the packet")
	assert_eq(resolver.enhancement_contribution_pp(0), 0)
	assert_eq(resolver.enhancement_contribution_pp(10), 3)
	assert_eq(resolver.enhancement_contribution_pp(60), 18)
	assert_eq(resolver.enhancement_contribution_pp(100), 30)
	assert_eq(resolver.proficiency_modifier_pp(0), -10)
	assert_eq(resolver.proficiency_modifier_pp(1), 0)
	assert_eq(resolver.proficiency_modifier_pp(2), 5)
	assert_eq(resolver.proficiency_modifier_pp(3), 10)


func test_allowed_assignment_is_53_percent_and_public_standing_is_neutral() -> void:
	var resolver = ContextResolverScript.new()
	var context = _context()
	var item = _item(40, 10)
	var common_result = resolver.evaluate(_customer("COMMON"), item, context)
	var legendary_result = resolver.evaluate(_customer("LEGENDARY"), item, context)
	for result in [common_result, legendary_result]:
		assert_eq(result.get("status", ""), "EVALUATED")
		assert_true(bool(result.get("assignment_allowed", false)))
		assert_true(bool(result.get("estimate_available", false)))
		assert_eq(int(result.get("risk_base", -1)), 40)
		assert_eq(int(result.get("enhancement_contribution_pp", -1)), 3)
		assert_eq(int(result.get("related_ability_modifier_pp", -1)), 5)
		assert_eq(int(result.get("proficiency_modifier_pp", -1)), 5)
		assert_eq(int(result.get("final_primary_estimate", -1)), 53)
		assert_false(result.has("fit_score"))
		assert_false(result.has("best"))
	assert_eq(common_result.get("final_primary_estimate", -1), legendary_result.get("final_primary_estimate", -2), "public standing must not alter the numeric estimate")


func test_overweight_hard_gate_blocks_before_estimate() -> void:
	var result = ContextResolverScript.new().evaluate(_customer(), _item(45, 10), _context())
	assert_eq(result.get("status", ""), "BLOCKED")
	assert_false(bool(result.get("assignment_allowed", true)))
	assert_eq(result.get("reason", ""), "OVERWEIGHT")
	assert_false(bool(result.get("estimate_available", true)))
	assert_false(result.has("final_primary_estimate"), "blocked assignments must not expose a misleading success estimate")


func test_unmet_related_ability_and_proficiency_one_produce_43_percent() -> void:
	var result = ContextResolverScript.new().evaluate(_customer(), _item(40, 10), _context(6, 4, 5, 1))
	assert_eq(result.get("status", ""), "EVALUATED")
	assert_eq(int(result.get("risk_base", -1)), 40)
	assert_eq(int(result.get("enhancement_contribution_pp", -1)), 3)
	assert_eq(int(result.get("related_ability_modifier_pp", -1)), 0)
	assert_eq(int(result.get("proficiency_modifier_pp", -1)), 0)
	assert_eq(int(result.get("final_primary_estimate", -1)), 43)


func test_explicit_required_function_is_a_hard_gate() -> void:
	var context = _context(6, 4, 6, 2, "ENVIRONMENTAL_SEALING")
	var missing = ContextResolverScript.new().evaluate(_customer(), _item(40, 10), context)
	assert_eq(missing.get("status", ""), "BLOCKED")
	assert_eq(missing.get("reason", ""), "REQUIRED_FUNCTION_MISSING")
	assert_false(missing.has("final_primary_estimate"))
	var present = ContextResolverScript.new().evaluate(_customer(), _item(40, 10, ["ENVIRONMENTAL_SEALING"]), context)
	assert_eq(present.get("status", ""), "EVALUATED")
	assert_eq(int(present.get("final_primary_estimate", -1)), 53)


func test_context_packet_from_dict_round_trips_external_snapshot() -> void:
	var packet_script: Script = load(CONTEXT_PACKET_PATH)
	var has_from_dict := _script_has_method(packet_script, "from_dict")
	assert_true(has_from_dict, "context packet must parse external numeric snapshots")
	if not has_from_dict:
		return
	var packet = packet_script.call("from_dict", _context_dict())
	assert_not_null(packet)
	if packet == null:
		return
	assert_true(packet.validation_errors.is_empty(), "approved synthetic context snapshot must validate")
	assert_eq(packet.to_dict(), _context_dict())
	assert_eq(packet.maximum_load(), 40)
	assert_eq(packet.related_ability_value(), 6)


func test_blocked_results_expose_assignment_block_reason_for_existing_task4_contract() -> void:
	var resolver = ContextResolverScript.new()
	var overweight = resolver.evaluate(_customer(), _item(45, 10), _context())
	assert_eq(overweight.get("assignment_block_reason", ""), "OVERWEIGHT")
	var function_context = _context(6, 4, 6, 2, "ENVIRONMENTAL_SEALING")
	var missing_function = resolver.evaluate(_customer(), _item(40, 10), function_context)
	assert_eq(missing_function.get("assignment_block_reason", ""), "REQUIRED_FUNCTION_MISSING")


func test_precision_selection_is_customer_context_independent_and_has_no_customer_bonus() -> void:
	var resolver = load(PRECISION_RESOLVER_PATH).new()
	assert_true(resolver.has_method("selection_preview"), "Decision37 precision resolver must expose selection preview")
	if not resolver.has_method("selection_preview"):
		return
	var item = _item(45, 9)
	var before_weight: int = int(item.weight_point)
	var light = resolver.selection_preview(item, 10, {
		"action": "ADD_TAG",
		"lineage_id": "EMBER_LINEAGE",
		"method_id": "LIGHTWEIGHTING",
	})
	assert_true(bool(light.get("allowed", false)))
	assert_eq(light.get("tag_id", ""), "TAG_EMBER_LIGHT")
	assert_eq(light.get("effect_axis", ""), "WEIGHT_POINT")
	assert_eq(int(light.get("effect_delta", 0)), -3)
	assert_eq(int(light.get("before_value", -1)), 45)
	assert_eq(int(light.get("after_value", -1)), 42)
	assert_eq(item.weight_point, before_weight, "precision preview must not mutate item weight")
	assert_false(light.has("customer_bonus_from_catalyst_selection_pp"))
	assert_false(light.has("context_relation"))


func test_precision_selection_respects_exact_entry_and_destroyed_item_eligibility() -> void:
	var resolver = load(PRECISION_RESOLVER_PATH).new()
	assert_true(resolver.has_method("selection_preview"), "Decision37 precision resolver must expose selection preview")
	if not resolver.has_method("selection_preview"):
		return
	var item = _item(30, 9)
	var selection := {"action": "ADD_TAG", "lineage_id": "ANVIL_LINEAGE", "method_id": "EDGE_REINFORCEMENT"}
	var valid = resolver.selection_preview(item, 10, selection)
	assert_true(bool(valid.get("allowed", false)))
	item.enhancement_level = 10
	var later = resolver.selection_preview(item, 11, selection)
	assert_false(bool(later.get("allowed", true)))
	assert_eq(later.get("reason", ""), "INVALID_PRECISION_ENTRY")
	item.enhancement_level = 9
	item.current_durability = 0
	item.physical_state = "DESTROYED"
	var destroyed = resolver.selection_preview(item, 10, selection)
	assert_false(bool(destroyed.get("allowed", true)))
	assert_eq(destroyed.get("reason", ""), "ITEM_DESTROYED")
