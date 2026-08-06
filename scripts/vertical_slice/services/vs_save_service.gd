class_name VSSaveService
extends RefCounted

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const DEFAULT_SAVE_PATH := "user://blacksmith_vertical_slice_v1.json"

var save_path: String = DEFAULT_SAVE_PATH
var temp_path: String = DEFAULT_SAVE_PATH + ".tmp"
var backup_path: String = DEFAULT_SAVE_PATH + ".bak"


func _init(custom_save_path: String = DEFAULT_SAVE_PATH) -> void:
	save_path = custom_save_path
	temp_path = custom_save_path + ".tmp"
	backup_path = custom_save_path + ".bak"


func save_envelope(envelope) -> Error:
	if envelope == null:
		return ERR_INVALID_PARAMETER
	var serialized: Dictionary = envelope.to_dict()
	var file := FileAccess.open(temp_path, FileAccess.WRITE)
	if file == null:
		return FileAccess.get_open_error()
	file.store_string(JSON.stringify(serialized, "  "))
	file.flush()
	file.close()

	var absolute_temp := ProjectSettings.globalize_path(temp_path)
	var absolute_save := ProjectSettings.globalize_path(save_path)
	var absolute_backup := ProjectSettings.globalize_path(backup_path)

	if FileAccess.file_exists(backup_path):
		var remove_backup_error := DirAccess.remove_absolute(absolute_backup)
		if remove_backup_error != OK:
			_cleanup_temp()
			return remove_backup_error

	var moved_primary_to_backup := false
	if FileAccess.file_exists(save_path):
		var backup_error := DirAccess.rename_absolute(absolute_save, absolute_backup)
		if backup_error != OK:
			_cleanup_temp()
			return backup_error
		moved_primary_to_backup = true

	var commit_error := DirAccess.rename_absolute(absolute_temp, absolute_save)
	if commit_error != OK:
		if moved_primary_to_backup and FileAccess.file_exists(backup_path):
			DirAccess.rename_absolute(absolute_backup, absolute_save)
		_cleanup_temp()
		return commit_error
	return OK


func load_envelope():
	if not FileAccess.file_exists(save_path):
		if FileAccess.file_exists(backup_path):
			var backup_only = _read_envelope(backup_path)
			if backup_only.validation_errors.is_empty():
				backup_only.recovered_from_backup = true
			return backup_only
		var missing = SaveEnvelopeScript.new()
		missing.validation_errors.append("SAVE_NOT_FOUND")
		return missing

	var primary = _read_envelope(save_path)
	if primary.validation_errors.is_empty():
		return primary
	if FileAccess.file_exists(backup_path):
		var backup = _read_envelope(backup_path)
		if backup.validation_errors.is_empty():
			backup.recovered_from_backup = true
			return backup
	return primary


func _read_envelope(path: String):
	var envelope = SaveEnvelopeScript.new()
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		envelope.validation_errors.append("SAVE_OPEN_ERROR:%d" % FileAccess.get_open_error())
		return envelope
	var source := file.get_as_text()
	file.close()
	var parsed: Variant = JSON.parse_string(source)
	if not parsed is Dictionary:
		envelope.validation_errors.append("SAVE_PARSE_ERROR")
		return envelope
	return SaveEnvelopeScript.from_dict(parsed)


func _cleanup_temp() -> void:
	if FileAccess.file_exists(temp_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(temp_path))
