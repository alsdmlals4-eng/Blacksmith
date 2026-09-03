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


func _precision_envelope(level: int = 9, tag_entries: Array = [], used_milestones: Array = []) -> VSSaveEnvelope:
	var envelope: VSSaveEnvelope = RunInitializerScript.new().create_candidate_envelope()
	var item := ItemScript.new()
	item.uid = "BSI-99999999999999999999999999999999"
	item.birth_rng_seed = 240810
	item.primary_material_id = "iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.raw_role_stat = 12
	item.weight_point = 2
	item.enhancement_level = level
	item.highest_checkpoint = 90 if level >= 90 else 60 if level >= 60 else 30 if level >= 30 else 10 if level >= 10 else 0
	item.base_max_durability = 5
	item.max_durability = 5
	item.current_durability = 5
	item.repair_job_available = false
	item.catalyst_affix["tag_entries"] = tag_entries.duplicate(true)
	for milestone in used_milestones:
		item.used_precision_milestones.append(int(milestone))
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
	var resources := ResourcesScript.new(20000, {
		"common_reinforcement_material": 30,
		"heart_of_flame": 64,
		"earth_crystal": 64,
	})
	envelope.workshop_resources = resources.snapshot()
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
		"catalyst_id": "HEART_OF_FLAME",
		"method_id": "EDGE_REINFORCEMENT",
	})
	assert_false(enhancement_button.disabled, "a valid first Tag selection unlocks the current +10 attempt")
	assert_true((screen.get_node("WorkshopScroll/WorkshopLayout/PrecisionPreviewLabel") as Label).text.contains("불의 심장 1개 소모"))
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
	assert_eq(reloaded.resource_snapshot()["material_stock"]["heart_of_flame"], 63)
	assert_eq(saved_item.used_precision_milestones, [10])
	var tag_entries: Array = saved_item.catalyst_affix.get("tag_entries", [])
	assert_eq(tag_entries.size(), 1)
	if not tag_entries.is_empty():
		assert_eq(str(tag_entries[0].get("tag_id", "")), "TAG_EMBER_EDGE")
		assert_eq(int(tag_entries[0].get("stage", 0)), 1)


func test_plus_19_to_plus_20_runtime_fixture_persists_tag_upgrade_and_derived_catalyst_charge_only_under_gut() -> void:
	var save_service := SaveServiceScript.new(FIXTURE_SAVE_PATH)

	var envelope := _precision_envelope(19, [{
		"tag_id": "TAG_ANVIL_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	assert_true(envelope.validation_errors.is_empty(), str(envelope.validation_errors))
	if not envelope.validation_errors.is_empty():
		return
	assert_eq(save_service.save_envelope(envelope), OK)

	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var resources := ResourcesScript.new(20000, {
		"common_reinforcement_material": 30,
		"heart_of_flame": 64,
		"earth_crystal": 64,
	})
	envelope.workshop_resources = resources.snapshot()
	screen.configure_context(
		envelope.get_item(str(envelope.active_run["selected_item_uid"])),
		resources,
		null,
		EnhancementActionServiceScript.new(),
		save_service,
		envelope
	)

	var upgrade_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button
	var tag_option := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTagOption") as OptionButton
	var enhancement_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementButton") as Button
	assert_not_null(upgrade_button)
	assert_not_null(tag_option)
	assert_not_null(enhancement_button)
	if upgrade_button == null or tag_option == null or enhancement_button == null:
		return
	assert_true(upgrade_button.visible)
	assert_false(upgrade_button.disabled)
	assert_true(enhancement_button.disabled)

	upgrade_button.pressed.emit()
	var anvil_tag_index := -1
	for index in range(tag_option.item_count):
		if str(tag_option.get_item_metadata(index)) == "TAG_ANVIL_EDGE":
			anvil_tag_index = index
			break
	assert_gte(anvil_tag_index, 0, "the visible +20 upgrade picker must include the stored tag")
	if anvil_tag_index < 0:
		return
	tag_option.select(anvil_tag_index)
	tag_option.item_selected.emit(anvil_tag_index)
	assert_false(enhancement_button.disabled, "a visible tag-upgrade selection unlocks the current +20 attempt")
	var preview := screen.get_node("WorkshopScroll/WorkshopLayout/PrecisionPreviewLabel") as Label
	assert_true(preview.text.contains("대지의 결정 1개 소모"))
	assert_true(preview.text.contains("단계 I → II"))

	var result: Dictionary = screen.request_enhancement_with_rolls({
		"success_roll_percent": 0.0,
		"damage_roll_percent": 99.0,
	})
	assert_eq(result.get("outcome", ""), "SUCCESS")
	assert_eq(result.get("precision_action", ""), "UPGRADE_TAG")
	assert_eq(result.get("precision_catalyst_id", ""), "EARTH_CRYSTAL")

	var reloaded = save_service.load_envelope()
	assert_true(reloaded.validation_errors.is_empty())
	var saved_item = reloaded.get_item("BSI-99999999999999999999999999999999")
	assert_not_null(saved_item)
	if saved_item == null:
		return
	assert_eq(saved_item.enhancement_level, 20)
	assert_eq(reloaded.resource_snapshot()["material_stock"]["earth_crystal"], 63)
	assert_eq(saved_item.used_precision_milestones, [10, 20])
	var saved_tag_entries: Array = saved_item.catalyst_affix.get("tag_entries", [])
	assert_eq(saved_tag_entries.size(), 1)
	if not saved_tag_entries.is_empty():
		assert_eq(str(saved_tag_entries[0].get("tag_id", "")), "TAG_ANVIL_EDGE")
		assert_eq(int(saved_tag_entries[0].get("stage", 0)), 2)
