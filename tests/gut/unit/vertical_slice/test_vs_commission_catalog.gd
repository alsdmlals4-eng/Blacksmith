extends "res://addons/gut/test.gd"

const CATALOG_PATH := "res://scripts/vertical_slice/domain/vs_commission_catalog.gd"
const EquipmentCatalogScript = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const ReplanTagRulesScript = preload("res://scripts/vertical_slice/domain/vs_replan_tag_rules.gd")

var CatalogScript: GDScript


func before_all() -> void:
	CatalogScript = load(CATALOG_PATH)


func test_catalog_script_and_required_api_exist() -> void:
	assert_not_null(CatalogScript, "Task 1 requires the commission catalog domain owner")
	if CatalogScript == null:
		return
	for method_name in ["all", "by_id", "validate_definition", "validate_catalog", "preview"]:
		assert_true(CatalogScript.has_method(method_name), "Missing API: %s" % method_name)


func test_catalog_exposes_fixed_basic_and_purpose_definition_for_each_equipment() -> void:
	if CatalogScript == null:
		pending("catalog script missing")
		return
	var definitions: Array[Dictionary] = CatalogScript.all()
	assert_eq(definitions.size(), 10)
	var expected_ids: Array[String] = []
	for equipment in EquipmentCatalogScript.all():
		var stem := str(equipment.equipment_id).to_upper()
		expected_ids.append("%s_BASIC_V1" % stem)
		expected_ids.append("%s_PURPOSE_V1" % stem)
	var actual_ids: Array[String] = []
	for definition in definitions:
		actual_ids.append(str(definition.definition_id))
	assert_eq(actual_ids, expected_ids)
	assert_true(CatalogScript.validate_catalog(definitions).is_empty())


func test_catalog_rejects_duplicate_ids_and_unknown_definition_lookup() -> void:
	if CatalogScript == null:
		pending("catalog script missing")
		return
	var definitions: Array[Dictionary] = CatalogScript.all()
	var duplicate := definitions.duplicate(true)
	duplicate.append(definitions[0].duplicate(true))
	assert_has(CatalogScript.validate_catalog(duplicate), "DUPLICATE_DEFINITION_ID:IRON_SWORD_BASIC_V1")
	var incomplete := definitions.duplicate(true)
	incomplete.pop_back()
	assert_has(CatalogScript.validate_catalog(incomplete), "MISSING_DEFINITION_ID:IRON_HELMET_PURPOSE_V1")
	assert_true(CatalogScript.by_id("UNKNOWN_DEFINITION").is_empty())


func test_definition_validation_fails_closed_for_unknown_or_malformed_values() -> void:
	if CatalogScript == null:
		pending("catalog script missing")
		return
	var valid: Dictionary = CatalogScript.by_id("IRON_SWORD_PURPOSE_V1")
	var cases := [
		["unknown equipment", "equipment_id", "iron_axe", "UNKNOWN_EQUIPMENT:iron_axe"],
		["empty purpose", "purpose", "", "EMPTY_PURPOSE"],
		["negative level", "min_level", -1, "INVALID_LEVEL:min_level"],
		["fractional level", "recommended_level", 10.5, "INVALID_LEVEL:recommended_level"],
		["unknown reward", "reward_policy_id", "UNKNOWN_REWARD", "UNKNOWN_REWARD_POLICY:UNKNOWN_REWARD"],
		["unknown ownership", "ownership_mode", "LOAN", "UNKNOWN_OWNERSHIP_MODE:LOAN"],
		["unknown funding", "funding_origin", "PLAYER", "UNKNOWN_FUNDING_ORIGIN:PLAYER"],
		["unknown return", "return_policy", "PLAYER", "UNKNOWN_RETURN_POLICY:PLAYER"],
		["unknown risk", "risk_profile", "EXTREME", "UNKNOWN_RISK_PROFILE:EXTREME"],
		["unknown version", "version", 2, "UNKNOWN_DEFINITION_VERSION:2"],
		["unknown axis", "purpose_axis", "POWER", "UNKNOWN_PURPOSE_AXIS:POWER"],
		["unknown rhythm", "purpose_rhythm", "RAPID", "UNKNOWN_PURPOSE_RHYTHM:RAPID"],
	]
	for row in cases:
		var malformed := valid.duplicate(true)
		malformed[row[1]] = row[2]
		assert_has(CatalogScript.validate_definition(malformed), row[3], row[0])
	var unknown_field := valid.duplicate(true)
	unknown_field["adaptive_tag_requirement"] = true
	assert_has(CatalogScript.validate_definition(unknown_field), "UNKNOWN_FIELD:adaptive_tag_requirement")


func test_all_definitions_share_explicit_trial_reward_and_customer_sale_defaults() -> void:
	if CatalogScript == null:
		pending("catalog script missing")
		return
	for definition in CatalogScript.all():
		assert_eq(definition.version, 1)
		assert_eq(definition.funding_origin, "COMMISSION_ESCROW")
		assert_eq(definition.ownership_mode, "SALE")
		assert_eq(definition.reward_policy_id, "COMMISSION_ECONOMY_TRIAL_V1")
		assert_eq(definition.return_policy, "CUSTOMER")
		var view: Dictionary = CatalogScript.preview(definition, _item_for(definition))
		assert_eq(view.reward, {
			"policy_id": "COMMISSION_ECONOMY_TRIAL_V1",
			"gold": 400,
			"reinforcement_material": 2,
			"chosen_catalyst": 1,
			"bonus": 0,
			"balance_status": "TRIAL_NOT_FINAL",
		})
		assert_eq(view.ownership, {
			"funding_origin": "COMMISSION_ESCROW",
			"ownership_mode": "SALE",
			"return_policy": "CUSTOMER",
		})


func test_basic_preview_requires_no_tag_and_purpose_preview_recommends_fixed_existing_tag() -> void:
	if CatalogScript == null:
		pending("catalog script missing")
		return
	for equipment in EquipmentCatalogScript.all():
		var stem := str(equipment.equipment_id).to_upper()
		var basic: Dictionary = CatalogScript.by_id("%s_BASIC_V1" % stem)
		var basic_view: Dictionary = CatalogScript.preview(basic, _item_for(basic))
		assert_true(basic_view.allowed)
		assert_false(basic_view.purpose.tag_required)
		assert_eq(basic_view.purpose.recommended_tag_id, "")
		var purpose: Dictionary = CatalogScript.by_id("%s_PURPOSE_V1" % stem)
		var purpose_view: Dictionary = CatalogScript.preview(purpose, _item_for(purpose))
		assert_true(purpose_view.allowed)
		assert_false(purpose_view.purpose.tag_required, "Recommendations never become adaptive requirements")
		var tag_id := str(purpose_view.purpose.recommended_tag_id)
		assert_true(ReplanTagRulesScript.TAGS.has(tag_id))
		assert_eq(ReplanTagRulesScript.TAGS[tag_id], [purpose.purpose_axis, purpose.purpose_rhythm])
		assert_eq(purpose_view.purpose.recommended_tag_name, ReplanTagRulesScript.DISPLAY_NAMES_KO[tag_id])
		assert_true(str(purpose_view.purpose.recommendation).contains("추천"))


func test_preview_uses_equipment_catalog_name_and_reports_mismatch_and_level_shortage() -> void:
	if CatalogScript == null:
		pending("catalog script missing")
		return
	var definition: Dictionary = CatalogScript.by_id("IRON_BOW_PURPOSE_V1")
	var eligible: VSItem = _item_for(definition)
	var eligible_view: Dictionary = CatalogScript.preview(definition, eligible)
	assert_eq(eligible_view.keys(), ["allowed", "reasons", "equipment_name", "min_level", "recommended_level", "purpose", "reward", "ownership"])
	assert_eq(eligible_view.equipment_name, EquipmentCatalogScript.by_id("iron_bow").display_name_ko)
	assert_true(eligible_view.allowed)
	assert_true(eligible_view.reasons.is_empty())
	var wrong_equipment: VSItem = _item_for(CatalogScript.by_id("IRON_SWORD_PURPOSE_V1"))
	var mismatch: Dictionary = CatalogScript.preview(definition, wrong_equipment)
	assert_false(mismatch.allowed)
	assert_has(mismatch.reasons, "EQUIPMENT_MISMATCH")
	eligible.enhancement_level = 9
	var under_level: Dictionary = CatalogScript.preview(definition, eligible)
	assert_false(under_level.allowed)
	assert_has(under_level.reasons, "LEVEL_BELOW_MINIMUM")


func test_preview_and_repeated_lookup_are_pure_and_deterministic() -> void:
	if CatalogScript == null:
		pending("catalog script missing")
		return
	var definition: Dictionary = CatalogScript.by_id("IRON_SHIELD_PURPOSE_V1")
	var definition_before := definition.duplicate(true)
	var item: VSItem = _item_for(definition)
	item.catalyst_affix = {"schema_version": 2, "ruleset_id": ReplanTagRulesScript.RULESET_ID, "tags": {"BURST_OUTPUT": 1}}
	item.used_precision_milestones = [10]
	var item_before: Dictionary = item.to_dict()
	var first: Dictionary = CatalogScript.preview(definition, item)
	var second: Dictionary = CatalogScript.preview(CatalogScript.by_id("IRON_SHIELD_PURPOSE_V1"), item)
	assert_eq(first, second)
	assert_eq(item.to_dict(), item_before)
	assert_eq(definition, definition_before)
	assert_eq(CatalogScript.by_id("IRON_SHIELD_PURPOSE_V1"), definition_before)


func _item_for(definition: Dictionary) -> VSItem:
	var item: VSItem = ItemScript.new()
	var equipment: Dictionary = EquipmentCatalogScript.by_id(str(definition.get("equipment_id", "")))
	item.equipment_group = str(equipment.get("equipment_group", ""))
	item.role_profile = str(equipment.get("role_profile", ""))
	item.enhancement_level = int(definition.get("min_level", 0))
	return item
