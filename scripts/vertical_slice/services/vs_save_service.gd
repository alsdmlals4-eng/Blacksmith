class_name VSSaveService
extends RefCounted

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const DEFAULT_SAVE_PATH := "user://blacksmith_vertical_slice_v3.json"
const LEGACY_V2_SAVE_PATH := "user://blacksmith_vertical_slice_v2.json"
const LEGACY_V1_SAVE_PATH := "user://blacksmith_vertical_slice_v1.json"

var save_path: String = DEFAULT_SAVE_PATH
var temp_path: String = DEFAULT_SAVE_PATH + ".tmp"
var backup_path: String = DEFAULT_SAVE_PATH + ".bak"
var legacy_v2_path: String = LEGACY_V2_SAVE_PATH
var legacy_v1_path: String = LEGACY_V1_SAVE_PATH


func _init(custom_save_path: String = DEFAULT_SAVE_PATH, custom_legacy_v2_path: String = "") -> void:
	save_path = custom_save_path
	temp_path = custom_save_path + ".tmp"
	backup_path = custom_save_path + ".bak"
	if not custom_legacy_v2_path.is_empty():
		legacy_v2_path = custom_legacy_v2_path
	elif custom_save_path == DEFAULT_SAVE_PATH:
		legacy_v2_path = LEGACY_V2_SAVE_PATH
	else:
		legacy_v2_path = ""
		legacy_v1_path = ""


func save_envelope(envelope) -> Error:
	if envelope == null:
		return ERR_INVALID_PARAMETER
	if not envelope.validation_errors.is_empty():
		return ERR_INVALID_DATA

	var serialized := JSON.stringify(envelope.to_dict(), "  ")
	var temp_file := FileAccess.open(temp_path, FileAccess.WRITE)
	if temp_file == null:
		return FileAccess.get_open_error()
	temp_file.store_string(serialized)
	temp_file.flush()
	temp_file.close()

	var verified_temp = _load_path(temp_path)
	if verified_temp == null or not verified_temp.validation_errors.is_empty():
		_remove_if_exists(temp_path)
		return ERR_INVALID_DATA

	if FileAccess.file_exists(save_path):
		_remove_if_exists(backup_path)
		var backup_error := _rename(save_path, backup_path)
		if backup_error != OK:
			_remove_if_exists(temp_path)
			return backup_error

	var promote_error := _rename(temp_path, save_path)
	if promote_error != OK:
		if FileAccess.file_exists(backup_path) and not FileAccess.file_exists(save_path):
			_rename(backup_path, save_path)
		_remove_if_exists(temp_path)
		return promote_error

	return OK


func replace_envelope_after_confirmation(envelope) -> Error:
	if envelope == null:
		return ERR_INVALID_PARAMETER
	if not envelope.validation_errors.is_empty():
		return ERR_INVALID_DATA

	var serialized := JSON.stringify(envelope.to_dict(), "  ")
	var temp_file := FileAccess.open(temp_path, FileAccess.WRITE)
	if temp_file == null:
		return FileAccess.get_open_error()
	temp_file.store_string(serialized)
	temp_file.flush()
	temp_file.close()

	var verified_temp = _load_path(temp_path)
	if verified_temp == null or not verified_temp.validation_errors.is_empty():
		_remove_if_exists(temp_path)
		return ERR_INVALID_DATA

	var primary = _load_path(save_path)
	var backup = _load_path(backup_path)
	var primary_valid: bool = primary != null and primary.validation_errors.is_empty()
	var backup_valid: bool = backup != null and backup.validation_errors.is_empty()

	if primary_valid:
		_remove_if_exists(backup_path)
		var rotate_error := _rename(save_path, backup_path)
		if rotate_error != OK:
			_remove_if_exists(temp_path)
			return rotate_error
	elif FileAccess.file_exists(save_path):
		var remove_error := _remove_if_exists(save_path)
		if remove_error != OK:
			_remove_if_exists(temp_path)
			return remove_error

	# A known-valid backup must survive replacement when the old primary is invalid.
	# The explicit New Game confirmation authorizes replacement of current V2 state,
	# not silent deletion/migration of the separate pre-release V1 file.
	var promote_error := _rename(temp_path, save_path)
	if promote_error != OK:
		_remove_if_exists(temp_path)
		return promote_error

	var committed = _load_path(save_path)
	if committed == null or not committed.validation_errors.is_empty():
		_remove_if_exists(save_path)
		if backup_valid and FileAccess.file_exists(backup_path):
			_rename(backup_path, save_path)
		return ERR_INVALID_DATA
	return OK


func load_envelope():
	var primary = _load_path(save_path)
	if primary != null and primary.validation_errors.is_empty():
		return primary

	var backup = _load_path(backup_path)
	if backup != null and backup.validation_errors.is_empty():
		backup.recovered_from_backup = true
		return backup

	var current_files_missing := (
		not FileAccess.file_exists(save_path)
		and not FileAccess.file_exists(backup_path)
	)
	if current_files_missing and not legacy_v2_path.is_empty() and FileAccess.file_exists(legacy_v2_path):
		return _load_path(legacy_v2_path)
	if current_files_missing and not legacy_v1_path.is_empty() and FileAccess.file_exists(legacy_v1_path):
		return _load_path(legacy_v1_path)

	if primary != null and not primary.validation_errors.is_empty():
		return primary
	if backup != null and not backup.validation_errors.is_empty():
		return backup

	var missing = SaveEnvelopeScript.new()
	missing.validation_errors.append("SAVE_NOT_FOUND")
	return missing


func _load_path(path: String):
	if not FileAccess.file_exists(path):
		return null
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return null
	var text := file.get_as_text()
	file.close()
	# JSON.parse_string() emits an engine error for expected corrupt-save fixtures,
	# which GUT correctly treats as an unexpected runtime error. Use the parser
	# object so corrupt pre-release/primary data is a normal validation result.
	var parser := JSON.new()
	var parse_error := parser.parse(text)
	if parse_error != OK or not parser.data is Dictionary:
		var invalid = SaveEnvelopeScript.new()
		invalid.validation_errors.append("INVALID_JSON")
		return invalid
	return SaveEnvelopeScript.from_dict(parser.data)


func _rename(from_path: String, to_path: String) -> Error:
	return DirAccess.rename_absolute(
		ProjectSettings.globalize_path(from_path),
		ProjectSettings.globalize_path(to_path)
	)


func _remove_if_exists(path: String) -> Error:
	if not FileAccess.file_exists(path):
		return OK
	return DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
