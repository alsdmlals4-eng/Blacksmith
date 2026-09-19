extends "res://addons/gut/test.gd"

const CONTEXT_PACKET_PATH := "res://scripts/vertical_slice/domain/vs_customer_context_packet.gd"
const CONTEXT_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_customer_context_resolver.gd"
const PRECISION_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd"
const CustomerProfileScript = preload("res://scripts/vertical_slice/domain/vs_customer_profile.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _load_new(path: String):
	if not ResourceLoader.exists(path):
		return null
	var script = load(path)
	if script == null:
		return null
	return script.new()


func _customer(grade: String = "ELITE") -> VSCustomerProfile:
	return CustomerProfileScript.from_dict({
		"schema_version": 1,
		"customer_id": "TEST_CUSTOMER",
		"name": "테스트 고객",
		"role": "탐사대장",
		"public_epithet": "시험의 길잡이",
		"public_standing_grade": grade,
		"content_id": "TEST_CONTENT",
		"content_goal": "SURVIVAL_AND_RECOVERY",
		"numeric_capability_profile": "NON_CANONICAL_TEST_FIXTURE",
	})


func _context_dict() -> Dictionary:
	return {
		"schema_version": 1,
		"customer_id": "TEST_CUSTOMER",
		"content_id": "TEST_CONTENT",
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


func _context():
	var packet = _load_new(CONTEXT_PACKET_PATH)
	if packet == null:
		return null
	var script = load(CONTEXT_PACKET_PATH)
	return script.from_dict(_context_dict())


func _item(level: int = 10, weight: int = 30) -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-1234567890abcdef1234567890abcdef"
	item.birth_rng_seed = 12345
	item.primary_material_id = "iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.crafting_grade = "CRAFT_NORMAL"
	item.raw_role_stat = 5
	item.weight_point = weight
	item.enhancement_level = level
	item.highest_checkpoint = 10 if level >= 10 else 0
	return item


func test_task4_runtime_surfaces_exist() -> void:
	assert_true(ResourceLoader.exists(CONTEXT_PACKET_PATH), "customer context packet must exist")
	assert_true(ResourceLoader.exists(CONTEXT_RESOLVER_PATH), "customer context resolver must exist")
	assert_true(ResourceLoader.exists(PRECISION_RESOLVER_PATH), "precision resolver must exist")


func test_context_packet_uses_external_numeric_snapshot_without_claiming_nadia_values() -> void:
	var context = _context()
	assert_not_null(context)
	if context == null:
		return
	assert_true(context.validation_errors.is_empty())
	assert_eq(context.maximum_load(), 40)
	assert_eq(context.related_ability_value(), 6)
	assert_eq(context.primary_need, "SAFE_RETURN")
	assert_eq(context.secondary_need, "RECOVERY_POSSIBILITY")


func test_public_standing_grade_is_neutral_to_customer_success_math() -> void:
	var resolver = _load_new(CONTEXT_RESOLVER_PATH)
	var context = _context()
	assert_not_null(resolver)
	assert_not_null(context)
	if resolver == null or context == null:
		return
	var item = _item(10, 30)
	var common = resolver.evaluate(_customer("COMMON"), item, context)
	var legendary = resolver.evaluate(_customer("LEGENDARY"), item, context)
	assert_true(common["assignment_allowed"])
	assert_true(legendary["assignment_allowed"])
	assert_eq(common["final_primary_estimate"], 53)
	assert_eq(legendary["final_primary_estimate"], 53)
	assert_eq(common["final_primary_estimate"], legendary["final_primary_estimate"])
	assert_false(common.has("fit_score"))
	assert_false(common.has("best"))


func test_hard_load_gate_precedes_success_estimate() -> void:
	var resolver = _load_new(CONTEXT_RESOLVER_PATH)
	var context = _context()
	assert_not_null(resolver)
	assert_not_null(context)
	if resolver == null or context == null:
		return
	var overweight = resolver.evaluate(_customer(), _item(60, 45), context)
	assert_false(overweight["assignment_allowed"])
	assert_eq(overweight["assignment_block_reason"], "OVERWEIGHT")
	assert_eq(overweight["maximum_load"], 40)
	assert_eq(overweight["current_weight"], 45)
	assert_false(overweight["estimate_available"])
	assert_false(overweight.has("final_primary_estimate"))

	var within = resolver.evaluate(_customer(), _item(10, 40), context)
	assert_true(within["assignment_allowed"])
	assert_true(within["estimate_available"])
	assert_eq(within["final_primary_estimate"], 53)


func test_customer_success_budget_matches_decision24_without_hidden_softening() -> void:
	var resolver = _load_new(CONTEXT_RESOLVER_PATH)
	assert_not_null(resolver)
	if resolver == null:
		return
	assert_eq(resolver.enhancement_contribution_pp(0), 0)
	assert_eq(resolver.enhancement_contribution_pp(10), 3)
	assert_eq(resolver.enhancement_contribution_pp(60), 18)
	assert_eq(resolver.enhancement_contribution_pp(100), 30)
	assert_eq(resolver.proficiency_modifier_pp(0), -10)
	assert_eq(resolver.proficiency_modifier_pp(1), 0)
	assert_eq(resolver.proficiency_modifier_pp(2), 5)
	assert_eq(resolver.proficiency_modifier_pp(3), 10)

	var weak_context_dict := _context_dict()
	weak_context_dict["constitution"] = 5
	weak_context_dict["weapon_proficiency"] = 1
	var packet_script = load(CONTEXT_PACKET_PATH)
	var weak_context = packet_script.from_dict(weak_context_dict)
	var result = resolver.evaluate(_customer(), _item(10, 30), weak_context)
	assert_eq(result["risk_base"], 40)
	assert_eq(result["enhancement_contribution_pp"], 3)
	assert_eq(result["related_ability_modifier_pp"], 0)
	assert_eq(result["proficiency_modifier_pp"], 0)
	assert_eq(result["final_primary_estimate"], 43)


func test_explicit_required_function_is_a_hard_gate_not_a_hidden_bonus() -> void:
	var resolver = _load_new(CONTEXT_RESOLVER_PATH)
	assert_not_null(resolver)
	if resolver == null:
		return
	var context_dict := _context_dict()
	context_dict["required_function_if_explicit"] = "ENVIRONMENTAL_SEALING"
	var packet_script = load(CONTEXT_PACKET_PATH)
	var context = packet_script.from_dict(context_dict)
	var item = _item(10, 30)
	var blocked = resolver.evaluate(_customer(), item, context)
	assert_false(blocked["assignment_allowed"])
	assert_eq(blocked["assignment_block_reason"], "REQUIRED_FUNCTION_MISSING")
	item.functions = ["ENVIRONMENTAL_SEALING"]
	var allowed = resolver.evaluate(_customer(), item, context)
	assert_true(allowed["assignment_allowed"])
	assert_eq(allowed["final_primary_estimate"], 53)


func test_precision_preview_classifies_context_relation_without_catalyst_bonus() -> void:
	var resolver = _load_new(PRECISION_RESOLVER_PATH)
	var context = _context()
	assert_not_null(resolver)
	assert_not_null(context)
	if resolver == null or context == null:
		return
	var heavy = _item(10, 45)
	var light = resolver.preview(heavy, 10, "LIGHTWEIGHTING", "", context)
	assert_true(light["allowed"])
	assert_eq(light["output_lane"], "STAT_METHOD")
	assert_eq(light["changed_axis"], "CURRENT_WEIGHT")
	assert_eq(light["delta"], -5)
	assert_eq(light["result_weight"], 40)
	assert_eq(light["context_relation"], "GATE_CHANGE")

	var edge = resolver.preview(_item(10, 30), 10, "EDGE_REINFORCEMENT", "", context)
	assert_true(edge["allowed"])
	assert_eq(edge["context_relation"], "NOT_DIRECTLY_RELEVANT")

	var weight_up = resolver.preview(_item(10, 30), 10, "WEIGHTING", "", context)
	assert_true(weight_up["allowed"])
	assert_eq(weight_up["context_relation"], "TRADE_OFF")

	var art = resolver.preview(_item(10, 30), 10, "ARTISTIC_FINISH", "salamander_core", context)
	assert_true(art["allowed"])
	assert_eq(art["context_relation"], "NOT_DIRECTLY_RELEVANT")
	assert_eq(art["customer_bonus_from_catalyst_selection_pp"], 0)
	assert_false(art["customer_bonus_granted_by_catalyst_selection"])


func test_precision_preview_respects_milestone_and_item_eligibility() -> void:
	var resolver = _load_new(PRECISION_RESOLVER_PATH)
	var context = _context()
	assert_not_null(resolver)
	assert_not_null(context)
	if resolver == null or context == null:
		return
	var item = _item(9, 30)
	var not_reached = resolver.preview(item, 10, "EDGE_REINFORCEMENT", "", context)
	assert_false(not_reached["allowed"])
	assert_eq(not_reached["reason"], "MILESTONE_NOT_REACHED")
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	item.used_precision_milestones = [10]
	var used = resolver.preview(item, 10, "EDGE_REINFORCEMENT", "", context)
	assert_false(used["allowed"])
	assert_eq(used["reason"], "PRECISION_MILESTONE_ALREADY_USED")
	item.used_precision_milestones = []
	item.current_durability = 0
	item.physical_state = "DESTROYED"
	var destroyed = resolver.preview(item, 10, "EDGE_REINFORCEMENT", "", context)
	assert_false(destroyed["allowed"])
	assert_eq(destroyed["reason"], "ITEM_DESTROYED")
