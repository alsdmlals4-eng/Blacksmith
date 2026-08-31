extends "res://addons/gut/test.gd"

const MAIN_MENU_PATH := "res://scripts/vertical_slice/ui/vs_main_menu.gd"
const MAIN_MENU_SCENE := preload("res://scenes/vertical_slice/main_menu.tscn")
const APPROVED_MAIN_MENU_BACKGROUND_PATH := "res://assets/ui/workshop/main_menu_dawn_background_v1.png"
const APPROVED_MAIN_MENU_LOGO_PATH := "res://assets/ui/identity/anvil_oath_logo_ao02_v1.png"


class FakeEnvelope:
	extends RefCounted
	var validation_errors: Array = []
	var recovered_from_backup := false


class FakeSaveService:
	extends RefCounted
	var envelope = null
	var replacement_error: Error = OK
	var replacement_calls := 0

	func load_envelope():
		return envelope

	func replace_envelope_after_confirmation(_candidate) -> Error:
		replacement_calls += 1
		return replacement_error


class FakeInitializerService:
	extends RefCounted
	var candidate = null
	var create_calls := 0

	func create_candidate_envelope():
		create_calls += 1
		return candidate


func _new_menu():
	if not ResourceLoader.exists(MAIN_MENU_PATH):
		return null
	var script = load(MAIN_MENU_PATH)
	if script == null:
		return null
	return script.new()


func _valid_envelope(recovered := false):
	var envelope := FakeEnvelope.new()
	envelope.recovered_from_backup = recovered
	return envelope


func _invalid_envelope(code := "SAVE_NOT_FOUND"):
	var envelope := FakeEnvelope.new()
	envelope.validation_errors.append(code)
	return envelope


func test_main_menu_surface_exists() -> void:
	assert_true(ResourceLoader.exists(MAIN_MENU_PATH), "Task 2 MainMenu logic must exist at the approved script path")


func test_main_menu_binds_the_approved_dawn_background_without_serializing_it_into_the_scene() -> void:
	assert_true(ResourceLoader.exists(APPROVED_MAIN_MENU_BACKGROUND_PATH), "approved main-menu illustration must be tracked before it can replace the runtime binding")
	if not ResourceLoader.exists(APPROVED_MAIN_MENU_BACKGROUND_PATH):
		return
	var menu = MAIN_MENU_SCENE.instantiate()
	add_child_autofree(menu)
	var background := menu.get_node_or_null("MenuIllustratedBackground") as TextureRect
	assert_not_null(background, "main menu must retain its existing dynamic illustration slot")
	if background == null:
		return
	assert_eq(background.texture.resource_path, APPROVED_MAIN_MENU_BACKGROUND_PATH)
	assert_eq(background.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(background.z_index, -1)
	assert_eq(background.expand_mode, TextureRect.EXPAND_IGNORE_SIZE)
	assert_eq(background.stretch_mode, TextureRect.STRETCH_KEEP_ASPECT_COVERED)
	assert_false(MAIN_MENU_SCENE.instantiate().get_node("MenuIllustratedBackground").texture.resource_path == APPROVED_MAIN_MENU_BACKGROUND_PATH, "the old serialized scene texture remains an unpromoted fallback")


func test_main_menu_binds_the_user_locked_ao_logo_before_its_text_fallback() -> void:
	assert_true(ResourceLoader.exists(APPROVED_MAIN_MENU_LOGO_PATH), "the user-locked AO-LOGO-02 must be tracked before runtime binding")
	if not ResourceLoader.exists(APPROVED_MAIN_MENU_LOGO_PATH):
		return
	var menu = MAIN_MENU_SCENE.instantiate()
	add_child_autofree(menu)
	var logo := menu.get_node_or_null("MenuLayout/MenuTitleLogo") as TextureRect
	var text_fallback := menu.get_node_or_null("MenuLayout/MenuTitleLabel") as Label
	assert_not_null(logo, "main menu must expose a concrete logo node above its text fallback")
	assert_not_null(text_fallback, "main menu must retain the localizable text fallback")
	if logo == null or text_fallback == null:
		return
	assert_eq(logo.texture.resource_path, APPROVED_MAIN_MENU_LOGO_PATH)
	assert_eq(logo.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(logo.expand_mode, TextureRect.EXPAND_IGNORE_SIZE)
	assert_eq(logo.stretch_mode, TextureRect.STRETCH_KEEP_ASPECT_CENTERED)
	assert_lt(logo.get_index(), text_fallback.get_index())
	assert_false(text_fallback.visible, "the text fallback must not duplicate the selected logo while the texture is available")


func test_main_menu_keeps_native_korean_touch_actions_over_the_approved_background() -> void:
	var menu = MAIN_MENU_SCENE.instantiate()
	add_child_autofree(menu)
	assert_eq(menu.get_node("MenuLayout/MenuTitleLabel").text, "모루의 서약")
	assert_eq(menu.get_node("MenuLayout/ContinueButton").text, "이어하기")
	assert_eq(menu.get_node("MenuLayout/NewGameButton").text, "새 대장간 시작")
	assert_eq(menu.get_node("MenuLayout/SettingsButton").text, "설정")
	assert_gte(menu.get_node("MenuLayout/NewGameButton").custom_minimum_size.y, 64.0)


func test_main_menu_localizes_player_facing_save_status() -> void:
	var menu = _new_menu()
	assert_not_null(menu)
	if menu == null:
		return
	menu.save_status = menu.STATUS_PRIMARY_OK
	assert_eq(menu.player_facing_save_status(), "저장됨 · 이어하기 가능")
	menu.save_status = menu.STATUS_SAVE_UNAVAILABLE
	assert_eq(menu.player_facing_save_status(), "저장 파일 없음 · 새 대장간을 시작하세요")
	menu.free()


func test_valid_primary_enables_continue() -> void:
	var menu = _new_menu()
	assert_true(menu != null, "MainMenu logic must load")
	if menu == null:
		return
	var save_service := FakeSaveService.new()
	save_service.envelope = _valid_envelope()
	menu.configure_services(save_service, FakeInitializerService.new())
	menu.refresh_save_state()
	assert_true(menu.continue_enabled, "valid primary save must enable Continue")
	assert_eq(menu.save_status, "PRIMARY_OK", "valid primary must expose PRIMARY_OK")
	menu.free()


func test_recovered_backup_enables_continue_with_explicit_status() -> void:
	var menu = _new_menu()
	assert_true(menu != null, "MainMenu logic must load")
	if menu == null:
		return
	var save_service := FakeSaveService.new()
	save_service.envelope = _valid_envelope(true)
	menu.configure_services(save_service, FakeInitializerService.new())
	menu.refresh_save_state()
	assert_true(menu.continue_enabled, "valid recovered backup must enable Continue")
	assert_eq(menu.save_status, "RECOVERED_BACKUP", "recovery must be explicit")
	menu.free()


func test_invalid_or_missing_save_disables_continue() -> void:
	var menu = _new_menu()
	assert_true(menu != null, "MainMenu logic must load")
	if menu == null:
		return
	var save_service := FakeSaveService.new()
	save_service.envelope = _invalid_envelope()
	menu.configure_services(save_service, FakeInitializerService.new())
	menu.refresh_save_state()
	assert_false(menu.continue_enabled, "missing or invalid save must disable Continue")
	assert_eq(menu.save_status, "SAVE_UNAVAILABLE", "unusable save must fail closed")
	assert_false(menu.new_game_requires_confirmation(), "no loadable save needs no destructive confirmation")
	menu.free()


func test_loadable_save_requires_new_game_confirmation() -> void:
	var menu = _new_menu()
	assert_true(menu != null, "MainMenu logic must load")
	if menu == null:
		return
	var save_service := FakeSaveService.new()
	save_service.envelope = _valid_envelope()
	menu.configure_services(save_service, FakeInitializerService.new())
	menu.refresh_save_state()
	assert_true(menu.new_game_requires_confirmation(), "loadable save must require destructive confirmation")
	menu.free()


func test_new_game_becomes_ready_only_after_successful_first_save() -> void:
	var menu = _new_menu()
	assert_true(menu != null, "MainMenu logic must load")
	if menu == null:
		return
	var save_service := FakeSaveService.new()
	save_service.envelope = _valid_envelope()
	var initializer := FakeInitializerService.new()
	initializer.candidate = _valid_envelope()
	menu.configure_services(save_service, initializer)
	var result = menu.start_new_game_after_confirmation()
	assert_eq(result, OK, "successful confirmed replacement must return OK")
	assert_eq(initializer.create_calls, 1, "initializer must create exactly one candidate")
	assert_eq(save_service.replacement_calls, 1, "save service must own confirmed replacement")
	assert_true(menu.campaign_ready, "campaign becomes ready only after first save succeeds")
	menu.free()


func test_first_save_failure_keeps_campaign_not_ready() -> void:
	var menu = _new_menu()
	assert_true(menu != null, "MainMenu logic must load")
	if menu == null:
		return
	var save_service := FakeSaveService.new()
	save_service.envelope = _valid_envelope()
	save_service.replacement_error = ERR_CANT_CREATE
	var initializer := FakeInitializerService.new()
	initializer.candidate = _valid_envelope()
	menu.configure_services(save_service, initializer)
	var result = menu.start_new_game_after_confirmation()
	assert_eq(result, ERR_CANT_CREATE, "save failure must propagate")
	assert_false(menu.campaign_ready, "failed first save must block campaign entry")
	menu.free()


func test_settings_toggle_is_inline_state_only() -> void:
	var menu = _new_menu()
	assert_true(menu != null, "MainMenu logic must load")
	if menu == null:
		return
	assert_false(menu.settings_open, "settings starts closed")
	menu.set_settings_open(true)
	assert_true(menu.settings_open, "settings opens inline")
	menu.set_settings_open(false)
	assert_false(menu.settings_open, "settings closes inline")
	menu.free()
