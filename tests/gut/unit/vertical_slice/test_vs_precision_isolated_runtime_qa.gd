# 실제 플레이어 저장과 분리된 +9 -> +10 정밀강화 화면 QA 픽스처다.
extends "res://addons/gut/test.gd"

const SCREEN_SCENE := preload("res://scenes/vertical_slice/screens/vs_workshop_screen.tscn")
const ItemScript := preload("res://scripts/vertical_slice/domain/vs_item.gd")
const SaveEnvelopeScript := preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const ResourcesScript := preload("res://scripts/economy/workshop_resources.gd")
const RunInitializerScript := preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const EnhancementActionServiceScript := preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const SaveServiceScript := preload("res://scripts/vertical_slice/services/vs_save_service.gd")

# GUT policy allows only this disposable location.  It is removed before and
# after every test; the player-facing save path is never opened here.
const FIXTURE_SAVE_PATH := "user://gut/blacksmith_precision_runtime_qa_v4.json"


func before_each() -> void:
	assert_eq(
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("user://gut")),
		OK,
		"the isolated GUT fixture directory must exist before persistence"
	)
	_remove_fixture_files()


func after_each() -> void:
	_remove_fixture_files()
	for suffix in ["", ".tmp", ".bak"]:
		var path: String = FIXTURE_SAVE_PATH + suffix
		assert_false(FileAccess.file_exists(path), "the QA fixture must clean its disposable save file")


func _remove_fixture_files() -> void:
	for suffix in ["", ".tmp", ".bak"]:
		var path: String = FIXTURE_SAVE_PATH + suffix
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _precision_envelope() -> VSSaveEnvelope:
	var envelope: VSSaveEnvelope = RunInitializerScript.new().create_candidate_envelope()
	var item := ItemScript.new()
	item.uid = "BSI-99999999999999999999999999999999"
	item.birth_rng_seed = 240810
	item.primary_material_id = "iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.raw_role_stat = 12
	item.weight_point = 2
	item.enhancement_level = 9
	item.highest_checkpoint = 0
	item.base_max_durability = 5
	item.max_durability = 5
	item.current_durability = 5
	item.repair_job_available = false
	envelope.items_by_uid[item.uid] = item
	envelope.active_run["selected_item_uid"] = item.uid
	return SaveEnvelopeScript.from_dict(envelope.to_dict())


func test_plus_9_to_plus_10_runtime_fixture_persists_only_under_gut() -> void:
	var save_service := SaveServiceScript.new(FIXTURE_SAVE_PATH)
	assert_ne(save_service.save_path, SaveServiceScript.DEFAULT_SAVE_PATH)

	var envelope := _precision_envelope()
	assert_true(envelope.validation_errors.is_empty(), str(envelope.validation_errors))
	if not envelope.validation_errors.is_empty():
		return
	assert_eq(save_service.save_envelope(envelope), OK)
	assert_true(FileAccess.file_exists(FIXTURE_SAVE_PATH))

	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var resources := ResourcesScript.new(20000, {"common_reinforcement_material": 30})
	screen.configure_context(
		envelope.get_item(str(envelope.active_run["selected_item_uid"])),
		resources,
		null,
		EnhancementActionServiceScript.new(),
		save_service,
		envelope
	)

	var add_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button
	var enhancement_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementButton") as Button
	assert_not_null(add_button)
	assert_not_null(enhancement_button)
	if add_button == null or enhancement_button == null:
		return
	assert_eq(add_button.custom_minimum_size.y, 96.0, "the native +9 add-tag action keeps the 48 px portrait target at 2x scale")
	assert_eq(enhancement_button.custom_minimum_size.y, 112.0, "the primary enhancement action keeps the 56 px portrait target at 2x scale")
	assert_true(add_button.visible)
	assert_false(add_button.disabled)
	assert_true(enhancement_button.disabled)

	screen._on_precision_add_pressed()
	screen.set_precision_selection({
		"action": "ADD_TAG",
		"lineage_id": "EMBER_LINEAGE",
		"method_id": "EDGE_REINFORCEMENT",
	})
	assert_false(enhancement_button.disabled, "a valid first Tag selection unlocks the current +10 attempt")
	var result: Dictionary = screen.request_enhancement_with_rolls({
		"success_roll_percent": 0.0,
		"damage_roll_percent": 99.0,
	})
	assert_eq(result.get("outcome", ""), "SUCCESS")

	var reloaded = save_service.load_envelope()
	assert_true(reloaded.validation_errors.is_empty())
	var saved_item = reloaded.get_item("BSI-99999999999999999999999999999999")
	assert_not_null(saved_item)
	if saved_item == null:
		return
	assert_eq(saved_item.enhancement_level, 10)
	assert_eq(saved_item.used_precision_milestones, [10])
	var tag_entries: Array = saved_item.catalyst_affix.get("tag_entries", [])
	assert_eq(tag_entries.size(), 1)
	if not tag_entries.is_empty():
		assert_eq(str(tag_entries[0].get("tag_id", "")), "TAG_EMBER_EDGE")
		assert_eq(int(tag_entries[0].get("stage", 0)), 1)
