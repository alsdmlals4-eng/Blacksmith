extends "res://addons/gut/test.gd"

const ADAPTER_PATH := "res://scripts/forging/canonical_first_item_input_adapter.gd"


func test_legacy_forge_grade_becomes_current_canonical_birth_input() -> void:
	assert_true(ResourceLoader.exists(ADAPTER_PATH), "forge boundary adapter must exist")
	if not ResourceLoader.exists(ADAPTER_PATH):
		return
	var adapter = load(ADAPTER_PATH).new()
	var input: Dictionary = adapter.to_canonical_input({
		"weapon_id": "iron_sword",
		"base_attack": 24,
		"craftsmanship_grade_id": "REFINED",
	})

	assert_eq(input.get("status", ""), "READY")
	assert_eq(input.get("crafting_grade", ""), "CRAFT_FINE")
	assert_eq(int(input.get("artistry", -1)), 5)
	assert_eq(int(input.get("base_attack", 0)), 24)


func test_unknown_legacy_forge_grade_fails_closed() -> void:
	if not ResourceLoader.exists(ADAPTER_PATH):
		assert_true(false, "forge boundary adapter must exist")
		return
	var input: Dictionary = load(ADAPTER_PATH).new().to_canonical_input({
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"craftsmanship_grade_id": "UNKNOWN",
	})
	assert_eq(input.get("status", ""), "BLOCKED")
	assert_eq(input.get("reason", ""), "UNSUPPORTED_LEGACY_CRAFTSMANSHIP_GRADE")


func test_completed_forge_result_uses_a_deterministic_current_grade() -> void:
	if not ResourceLoader.exists(ADAPTER_PATH):
		assert_true(false, "forge boundary adapter must exist")
		return
	var input: Dictionary = load(ADAPTER_PATH).new().to_canonical_input_from_completion({
		"weapon_id": "iron_sword",
		"base_attack": 22,
		"quality_id": "GOOD",
		"tap_count": 12,
		"fever_activation_count": 1,
		"fever_bonus_applied": true,
	})
	assert_eq(input.get("status", ""), "READY")
	assert_eq(input.get("crafting_grade", ""), "CRAFT_SUPERIOR")
	assert_eq(int(input.get("artistry", -1)), 3)
	assert_eq(int(input.get("tap_count", -1)), 12)
