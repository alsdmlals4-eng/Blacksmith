class_name VSUidService
extends RefCounted

const UID_PATTERN := "^BSI-[0-9a-f]{32}$"
const MAX_ATTEMPTS := 128

var _crypto := Crypto.new()
var _uid_regex := RegEx.new()


func _init() -> void:
	_uid_regex.compile(UID_PATTERN)


func create_uid(existing_ids: Dictionary) -> String:
	for _attempt in range(MAX_ATTEMPTS):
		var random_bytes: PackedByteArray = _crypto.generate_random_bytes(16)
		var candidate := "BSI-" + random_bytes.hex_encode()
		if not existing_ids.has(candidate):
			return candidate
	return ""


func is_valid_uid(value: String) -> bool:
	return _uid_regex.search(value) != null
