# 첫 제작 완료를 저장 후보의 정본 작품과 작업대 선택 상태로 연결한다.
class_name VSFirstForgeCompletionService
extends RefCounted

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const ItemBirthServiceScript = preload("res://scripts/vertical_slice/services/vs_item_birth_service.gd")
const CanonicalInputAdapterScript = preload("res://scripts/forging/canonical_first_item_input_adapter.gd")

var _birth_service
var _input_adapter


func _init(birth_service = null, input_adapter = null) -> void:
	_birth_service = birth_service if birth_service != null else ItemBirthServiceScript.new()
	_input_adapter = input_adapter if input_adapter != null else CanonicalInputAdapterScript.new()


func complete_first_forge(envelope, completed_forge_result: Dictionary, save_service) -> Dictionary:
	if envelope == null or not envelope.validation_errors.is_empty():
		return _blocked("INVALID_ENVELOPE")
	if save_service == null or not save_service.has_method("save_envelope"):
		return _blocked("SAVE_SERVICE_UNAVAILABLE")
	var candidate = SaveEnvelopeScript.from_dict(envelope.to_dict())
	if candidate == null or not candidate.validation_errors.is_empty():
		return _blocked("INVALID_SAVE_CANDIDATE")
	var canonical_input: Dictionary = _input_adapter.to_canonical_input_from_completion(completed_forge_result)
	if str(canonical_input.get("status", "")) != "READY":
		return _blocked(str(canonical_input.get("reason", "INVALID_FORGE_RESULT")))
	canonical_input.erase("status")
	var birth: Dictionary = _birth_service.commit_first_forge(candidate, canonical_input)
	if str(birth.get("status", "")) != "APPLIED":
		return birth
	if save_service.save_envelope(candidate) != OK:
		return _blocked("SAVE_COMMIT_FAILED")
	return {
		"status": "APPLIED",
		"item_uid": str(birth.get("item_uid", "")),
		"item": birth.get("item", null),
		"envelope": candidate,
	}


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
