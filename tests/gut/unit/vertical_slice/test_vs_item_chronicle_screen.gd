extends "res://addons/gut/test.gd"

const SCREEN_PATH := "res://scripts/vertical_slice/ui/vs_item_chronicle_screen.gd"
const ItemBirthServiceScript := preload("res://scripts/vertical_slice/services/vs_item_birth_service.gd")
const RunInitializerScript := preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const CustomerProfileScript := preload("res://scripts/vertical_slice/domain/vs_customer_profile.gd")
const NADIA_DATA_PATH := "res://data/vertical_slice/customers/nadia_venn.json"


func _item():
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	if str(birth.get("status", "")) != "APPLIED":
		return null
	return envelope.get_item(str(envelope.active_run["selected_item_uid"]))


func _nadia_actual_use_result(item_uid: String, damage_applied: bool = false) -> Dictionary:
	return {
		"event_id": "phase1-nadia-actual-use-%s" % item_uid,
		"content_id": "ADVENTURER_01",
		"customer_id": "NADIA_VENN",
		"item_refs": [{"role": "PRIMARY_ITEM", "uid": item_uid}],
		"durability_consequence": {
			"actual_item_use": true,
			"damage_applied": damage_applied,
			"before_current_durability": 5,
			"after_current_durability": 4 if damage_applied else 5,
			"before_max_durability": 5,
			"after_max_durability": 5,
			"repair_job_available": damage_applied,
		},
	}


func _entry_by_kind(entries: Array, kind: String) -> Dictionary:
	for entry in entries:
		if entry is Dictionary and str(entry.get("kind", "")) == kind:
			return entry
	return {}


func _nadia_profile():
	var file := FileAccess.open(NADIA_DATA_PATH, FileAccess.READ)
	if file == null:
		return null
	var raw: Variant = JSON.parse_string(file.get_as_text())
	return CustomerProfileScript.from_dict(raw) if raw is Dictionary else null


func test_item_chronicle_reads_existing_birth_and_saved_actual_use_facts_without_new_storage() -> void:
	assert_true(ResourceLoader.exists(SCREEN_PATH), "the approved Item Chronicle candidate needs a player-facing implementation")
	if not ResourceLoader.exists(SCREEN_PATH):
		return
	var item = _item()
	assert_not_null(item)
	if item == null:
		return
	var screen = load(SCREEN_PATH).new()
	add_child_autofree(screen)
	var saved_events := {"nadia": _nadia_actual_use_result(str(item.uid))}
	var profile = _nadia_profile()
	assert_not_null(profile)
	if profile == null:
		return
	assert_eq(screen.configure_item(item, saved_events, profile).get("status", ""), "APPLIED")
	var state: Dictionary = screen.view_state()
	assert_eq(state.get("item_uid", ""), str(item.uid))
	assert_false(_entry_by_kind(state.get("entries", []), "BIRTH").is_empty())
	var handoff_entry := _entry_by_kind(state.get("entries", []), "HANDOFF")
	assert_true(str(handoff_entry.get("text", "")).contains("나디아"))
	var actual_use_entry := _entry_by_kind(state.get("entries", []), "ACTUAL_USE")
	assert_true(str(actual_use_entry.get("text", "")).contains("손상 없음"))
	assert_true(screen.has_signal("workshop_requested"))
	var return_button := screen.get_node_or_null("ChronicleMargin/ChronicleLayout/WorkshopReturnButton") as Button
	assert_not_null(return_button)
	if return_button != null:
		assert_true(return_button.visible)
		assert_false(return_button.disabled)
		assert_gte(return_button.custom_minimum_size.y, 48.0)


func test_chronicle_keeps_a_matching_actual_use_fact_when_the_customer_has_no_loaded_profile() -> void:
	var item = _item()
	assert_not_null(item)
	if item == null:
		return
	var screen = load(SCREEN_PATH).new()
	add_child_autofree(screen)
	var unknown_customer_result := _nadia_actual_use_result(str(item.uid))
	unknown_customer_result["customer_id"] = "UNREGISTERED_CUSTOMER"
	assert_eq(screen.configure_item(item, {"unknown": unknown_customer_result}).get("status", ""), "APPLIED")
	var handoff_entry := _entry_by_kind(screen.view_state().get("entries", []), "HANDOFF")
	var actual_use_entry := _entry_by_kind(screen.view_state().get("entries", []), "ACTUAL_USE")
	assert_true(str(handoff_entry.get("text", "")).contains("고객"))
	assert_true(str(actual_use_entry.get("text", "")).contains("고객 실제 사용 결과"))
