class_name VSMainMenu
extends Control

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


func configure_services(save_service, initializer_service) -> void:
	_save_service = save_service
	_initializer_service = initializer_service


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
	return save_error


func set_settings_open(value: bool) -> void:
	settings_open = value
