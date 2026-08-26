# 현재 정본 내구도·수리 및 강화 실패 결과를 검증한다.
# 현재 정본 내구도·수리 런타임 계약을 검증한다.
extends "res://addons/gut/test.gd"

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const EnhancementResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd")
const RepairResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")
const EnhancementActionServiceScript = preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const WorkshopMaintenanceServiceScript = preload("res://scripts/vertical_slice/services/vs_workshop_maintenance_service.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")


func _item(current: int = 5, maximum: int = 5, level: int = 10):
	var item = ItemScript.new()
	item.uid = "BSI-00112233445566778899aabbccddeeff"
	item.primary_material_id = "iron"
	item.enhancement_level = level
	item.highest_checkpoint = 10 if level < 30 else 30
	item.base_max_durability = 5
	item.max_durability = maximum
	item.current_durability = current
	item.physical_state = "DESTROYED" if current == 0 else "ACTIVE"
	item.repair_job_available = false
	return item


func test_effective_state_uses_the_worse_current_or_structural_ratio() -> void:
	var item = _item(4, 4)
	assert_eq(item.effective_durability_state(), "MINOR")
	item.current_durability = 2
	assert_eq(item.effective_durability_state(), "MAJOR")
	item.current_durability = 0
	assert_eq(item.effective_durability_state(), "DESTROYED")


func test_failure_is_hold_or_damage_without_downgrade_or_critical() -> void:
	var resolver = EnhancementResolverScript.new()
	var safe_item = _item(5, 5, 10)
	var safe_result: Dictionary = resolver.resolve_with_rolls(
		safe_item,
		11,
		{"success_roll_percent": 99.0, "damage_roll_percent": 99.0}
	)
	assert_eq(safe_result["outcome"], "FAILED_HOLD")
	assert_eq(safe_item.enhancement_level, 10)
	assert_eq(safe_item.current_durability, 5)

	var damaged_item = _item(5, 5, 10)
	var damaged_result: Dictionary = resolver.resolve_with_rolls(
		damaged_item,
		11,
		{"success_roll_percent": 99.0, "damage_roll_percent": 0.0}
	)
	assert_eq(damaged_result["outcome"], "FAILED_DAMAGE")
	assert_eq(damaged_item.enhancement_level, 10)
	assert_eq(damaged_item.current_durability, 4)
	assert_true(damaged_item.repair_job_available)


func test_preview_exposes_exact_final_outcomes_that_display_to_100_percent() -> void:
	var resolver = EnhancementResolverScript.new()
	var preview: Dictionary = resolver.preview(_item(4, 5, 10), 11)
	assert_almost_eq(preview["final_success_percent"], 79.0, 0.01)
	assert_almost_eq(preview["final_damage_percent"], 6.25, 0.01)
	assert_eq(preview["display_outcomes"], {
		"success_percent": 79.0,
		"failed_damage_percent": 6.3,
		"failed_hold_percent": 14.7,
	})


func test_same_target_recovery_offsets_durability_penalty_before_soft_cap() -> void:
	var item = _item(4, 5, 10)
	item.enhancement_recovery_by_target = {"11": 1}
	var one_failure: Dictionary = EnhancementResolverScript.new().preview(item, 11)
	assert_almost_eq(one_failure["final_success_percent"], 85.0, 0.01)
	item.enhancement_recovery_by_target = {"11": 3}
	var soft_cap: Dictionary = EnhancementResolverScript.new().preview(item, 11)
	assert_almost_eq(soft_cap["final_success_percent"], 95.0, 0.01)


func test_repair_requires_one_damage_job_and_uses_base_max_r_band_quote() -> void:
	var resolver = RepairResolverScript.new()
	var item = _item(3, 5, 10)
	assert_eq(resolver.quote(item)["reason"], "REPAIR_JOB_UNAVAILABLE")
	item.repair_job_available = true
	var quote: Dictionary = resolver.quote(item)
	assert_true(quote["allowed"])
	assert_eq(quote["gold_cost"], 39)
	assert_eq(quote["reinforcement_units"], 1)
	assert_eq(quote["base_max"], 5)


func test_repair_consumes_the_job_and_skips_a_scar_that_blocks_positive_gain() -> void:
	var resolver = RepairResolverScript.new()
	var item = _item(1, 2, 10)
	item.repair_job_available = true
	var quote: Dictionary = resolver.quote(item)
	var result: Dictionary = resolver.apply_with_rolls(
		item,
		int(quote["gold_cost"]),
		1,
		{"quality_roll_percent": 99.0, "scar_roll_percent": 0.0}
	)
	assert_eq(result["status"], "APPLIED")
	assert_true(result["scar_skipped"])
	assert_eq(item.max_durability, 2)
	assert_eq(item.current_durability, 2)
	assert_false(item.repair_job_available)
	assert_eq(resolver.quote(item)["reason"], "REPAIR_JOB_UNAVAILABLE")


func test_action_service_preserves_current_canon_damage_and_archives_destruction() -> void:
	var item = _item(1, 5, 10)
	var envelope = SaveEnvelopeScript.new()
	envelope.items_by_uid[item.uid] = item
	var result: Dictionary = EnhancementActionServiceScript.new().resolve_with_rolls(
		envelope,
		item.uid,
		11,
		{"success_roll_percent": 99.0, "damage_roll_percent": 0.0},
		1
	)
	assert_eq(result["outcome"], "FAILED_DAMAGE")
	assert_eq(item.current_durability, 0)
	assert_eq(item.base_max_durability, 5)
	assert_true(item.repair_job_available)
	assert_true(result["destroyed_history_archived"])
	if envelope.destroyed_history_by_uid.has(item.uid):
		assert_eq(envelope.destroyed_history_by_uid[item.uid]["direct_cause"], "ENHANCEMENT_DAMAGE")


func test_maintenance_spends_only_gold_and_one_reinforcement_for_repair() -> void:
	var item = _item(3, 5, 10)
	item.repair_job_available = true
	var resources = WorkshopResourcesScript.new(100, {"common_reinforcement_material": 1})
	var result: Dictionary = WorkshopMaintenanceServiceScript.new().try_repair_with_rolls(
		item,
		resources,
		{"quality_roll_percent": 0.0, "scar_roll_percent": 99.0}
	)
	assert_eq(result["status"], "APPLIED")
	assert_eq(resources.gold, 61)
	assert_eq(resources.get_material_count("common_reinforcement_material"), 0)
	assert_eq(item.current_durability, 5)
	assert_false(result.has("fatigue_cost"))
