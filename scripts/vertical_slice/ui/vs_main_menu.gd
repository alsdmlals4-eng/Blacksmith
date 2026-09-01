class_name VSMainMenu
extends Control

const SaveServiceScript = preload("res://scripts/vertical_slice/services/vs_save_service.gd")
const RunInitializerScript = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const FirstForgeCompletionServiceScript = preload("res://scripts/vertical_slice/services/vs_first_forge_completion_service.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")
const ForgingScreenScript = preload("res://scripts/ui/forging_screen.gd")
const AppScene = preload("res://scenes/vertical_slice/vertical_slice_app.tscn")
const MainMenuBackgroundTexture = preload("res://assets/ui/workshop/main_menu_dawn_background_v1.png")
const ProductLogoAssetPath := "res://assets/ui/identity/anvil_oath_logo_ao02_v1.png"
const ProductLogoMinimumHeight := 180.0

const STATUS_UNCHECKED := "UNCHECKED"
const STATUS_PRIMARY_OK := "PRIMARY_OK"
const STATUS_RECOVERED_BACKUP := "RECOVERED_BACKUP"
const STATUS_SAVE_UNAVAILABLE := "SAVE_UNAVAILABLE"

var continue_enabled := false
var save_status := STATUS_UNCHECKED
var campaign_ready := false
var settings_open := false

var _save_service = null
var _initializer_service = null
var _resources = null
var _completion_service = null
var _campaign_envelope = null
var _active_forge = null
var _active_app = null


func _ready() -> void:
	_ensure_flow_services()
	_ensure_illustrated_background()
	_ensure_product_logo()
	_connect_menu_actions()
	refresh_save_state()
	_refresh_menu_controls()


func configure_services(save_service, initializer_service) -> void:
	_save_service = save_service
	_initializer_service = initializer_service


func configure_flow_services(save_service, initializer_service, resources, completion_service) -> void:
	configure_services(save_service, initializer_service)
	_resources = resources
	_completion_service = completion_service


func refresh_save_state() -> void:
	continue_enabled = false
	save_status = STATUS_SAVE_UNAVAILABLE
	if _save_service == null or not _save_service.has_method("load_envelope"):
		return

	var envelope = _save_service.load_envelope()
	if envelope == null or not envelope.validation_errors.is_empty():
		return

	continue_enabled = true
	if envelope.recovered_from_backup:
		save_status = STATUS_RECOVERED_BACKUP
	else:
		save_status = STATUS_PRIMARY_OK


func new_game_requires_confirmation() -> bool:
	return continue_enabled


func start_new_game_after_confirmation():
	campaign_ready = false
	if _save_service == null or _initializer_service == null:
		return ERR_INVALID_PARAMETER
	if not _initializer_service.has_method("create_candidate_envelope"):
		return ERR_INVALID_PARAMETER
	if not _save_service.has_method("replace_envelope_after_confirmation"):
		return ERR_INVALID_PARAMETER

	var candidate = _initializer_service.create_candidate_envelope()
	if candidate == null or not candidate.validation_errors.is_empty():
		return ERR_INVALID_DATA

	var save_error = _save_service.replace_envelope_after_confirmation(candidate)
	campaign_ready = save_error == OK
	if campaign_ready:
		_campaign_envelope = candidate
		_restore_resources_from_envelope(candidate)
	return save_error


func set_settings_open(value: bool) -> void:
	settings_open = value


func player_facing_save_status() -> String:
	match save_status:
		STATUS_PRIMARY_OK:
			return "저장됨 · 이어하기 가능"
		STATUS_RECOVERED_BACKUP:
			return "백업 저장 복구됨 · 이어하기 가능"
		STATUS_SAVE_UNAVAILABLE:
			return "저장 파일 없음 · 새 대장간을 시작하세요"
		STATUS_UNCHECKED:
			return "저장 상태 확인 중"
		_:
			return save_status


func begin_first_forge(envelope) -> bool:
	if envelope == null or not envelope.validation_errors.is_empty():
		return false
	if not envelope.items_by_uid.is_empty() or not str(envelope.active_run.get("selected_item_uid", "")).is_empty():
		return false
	_ensure_flow_services()
	_campaign_envelope = envelope
	if not _restore_resources_from_envelope(envelope):
		_show_menu_message("공방 재화 정보를 불러올 수 없습니다.")
		return false
	_clear_active_surface()
	_set_menu_visible(false)
	_active_forge = ForgingScreenScript.new()
	_active_forge.ready.connect(_on_forge_screen_ready.bind(_active_forge), CONNECT_ONE_SHOT)
	add_child(_active_forge)
	return true


func apply_completed_first_forge_result(completed_forge_result: Dictionary) -> void:
	if _active_forge == null or _campaign_envelope == null:
		return
	var completion: Dictionary = _completion_service.complete_first_forge(
		_campaign_envelope,
		completed_forge_result,
		_save_service
	)
	if str(completion.get("status", "")) != "APPLIED":
		_show_menu_message("제작 저장 실패: %s" % str(completion.get("reason", "UNKNOWN")))
		return
	_campaign_envelope = completion.get("envelope", null)
	_clear_active_surface()
	_active_app = AppScene.instantiate()
	add_child(_active_app)
	if not _active_app.apply_first_forge_completion(completion, _resources, null, null, _save_service):
		_show_menu_message("작업대를 열 수 없습니다.")


func has_active_first_forge() -> bool:
	return _active_forge != null and is_instance_valid(_active_forge)


func has_active_workshop() -> bool:
	return _active_app != null and is_instance_valid(_active_app)


func current_selected_item_uid() -> String:
	if _campaign_envelope == null:
		return ""
	return str(_campaign_envelope.active_run.get("selected_item_uid", ""))


func _ensure_flow_services() -> void:
	if _save_service == null:
		_save_service = SaveServiceScript.new()
	if _initializer_service == null:
		_initializer_service = RunInitializerScript.new()
	if _resources == null:
		_resources = WorkshopResourcesScript.new()
	if _completion_service == null:
		_completion_service = FirstForgeCompletionServiceScript.new()


func _restore_resources_from_envelope(envelope) -> bool:
	if envelope == null or not envelope.has_method("resource_snapshot"):
		return false
	var snapshot: Variant = envelope.resource_snapshot()
	if not snapshot is Dictionary:
		return false
	var material_stock: Variant = snapshot.get("material_stock", null)
	if not material_stock is Dictionary:
		return false
	var gold: Variant = snapshot.get("gold", null)
	if not gold is int or int(gold) < 0:
		return false
	_resources = WorkshopResourcesScript.new(int(gold), material_stock.duplicate(true))
	return true


func _connect_menu_actions() -> void:
	var new_game_button := get_node_or_null("MenuLayout/NewGameButton")
	if new_game_button != null and not new_game_button.pressed.is_connected(_on_new_game_pressed):
		new_game_button.pressed.connect(_on_new_game_pressed)
	var continue_button := get_node_or_null("MenuLayout/ContinueButton")
	if continue_button != null and not continue_button.pressed.is_connected(_on_continue_pressed):
		continue_button.pressed.connect(_on_continue_pressed)


func _on_new_game_pressed() -> void:
	if new_game_requires_confirmation():
		_show_menu_message("기존 저장이 있어 새 게임 시작 전 확인이 필요합니다.")
		return
	if start_new_game_after_confirmation() != OK:
		_show_menu_message("새 게임을 시작하지 못했습니다.")
		return
	begin_first_forge(_campaign_envelope)


func _on_continue_pressed() -> void:
	var envelope = _save_service.load_envelope()
	if envelope == null or not envelope.validation_errors.is_empty():
		_show_menu_message("이전 저장을 불러올 수 없습니다.")
		return
	_campaign_envelope = envelope
	if not _restore_resources_from_envelope(envelope):
		_show_menu_message("공방 재화 정보를 불러올 수 없습니다.")
		return
	if str(envelope.active_run.get("selected_item_uid", "")).is_empty():
		begin_first_forge(envelope)
		return
	_clear_active_surface()
	_set_menu_visible(false)
	_active_app = AppScene.instantiate()
	add_child(_active_app)
	if not _active_app.configure_campaign(envelope, _resources, null, null, _save_service):
		_show_menu_message("작업대를 열 수 없습니다.")


func _on_forge_screen_ready(forge_screen) -> void:
	if forge_screen != _active_forge or forge_screen.session == null:
		return
	if not forge_screen.session.completed.is_connected(apply_completed_first_forge_result):
		forge_screen.session.completed.connect(apply_completed_first_forge_result)


func _clear_active_surface() -> void:
	for surface in [_active_forge, _active_app]:
		if surface != null and is_instance_valid(surface):
			remove_child(surface)
			surface.queue_free()
	_active_forge = null
	_active_app = null


func _show_menu_message(message: String) -> void:
	_clear_active_surface()
	_set_menu_visible(true)
	save_status = message
	_refresh_menu_controls()


func _set_menu_visible(should_show_menu: bool) -> void:
	var layout := get_node_or_null("MenuLayout")
	if layout != null:
		layout.visible = should_show_menu
	var settings_overlay := get_node_or_null("SettingsOverlay")
	if settings_overlay != null:
		settings_overlay.visible = should_show_menu and settings_open


func _refresh_menu_controls() -> void:
	var status_label := get_node_or_null("MenuLayout/SaveStatusLabel")
	if status_label != null:
		status_label.text = player_facing_save_status()
	var continue_button := get_node_or_null("MenuLayout/ContinueButton")
	if continue_button != null:
		continue_button.disabled = not continue_enabled


func _ensure_illustrated_background() -> void:
	var background := get_node_or_null("MenuIllustratedBackground") as TextureRect
	if background == null:
		return
	background.texture = MainMenuBackgroundTexture


func _ensure_product_logo() -> void:
	var menu_layout := get_node_or_null("MenuLayout") as VBoxContainer
	var text_fallback := get_node_or_null("MenuLayout/MenuTitleLabel") as Label
	if menu_layout == null or text_fallback == null:
		return

	var product_logo_texture := load(ProductLogoAssetPath) as Texture2D
	if product_logo_texture == null:
		text_fallback.visible = true
		return

	var logo := menu_layout.get_node_or_null("MenuTitleLogo") as TextureRect
	if logo == null:
		logo = TextureRect.new()
		logo.name = "MenuTitleLogo"
		logo.mouse_filter = Control.MOUSE_FILTER_IGNORE
		logo.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		logo.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		logo.custom_minimum_size = Vector2(0.0, ProductLogoMinimumHeight)
		logo.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		menu_layout.add_child(logo)
		menu_layout.move_child(logo, text_fallback.get_index())

	logo.texture = product_logo_texture
	text_fallback.visible = false
