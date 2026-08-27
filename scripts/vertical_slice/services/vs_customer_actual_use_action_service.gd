# 고객 실제사용 이벤트를 저장 후보에서 해결하고 성공한 저장본만 반환한다.
class_name VSCustomerActualUseActionService
extends RefCounted

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const CustomerWorldEventResolverScript = preload(
	"res://scripts/vertical_slice/resolvers/vs_customer_world_event_resolver.gd"
)


func resolve_and_save_with_roll(
	envelope,
	item_uid: String,
	event: Dictionary,
	damage_roll_percent: float,
	save_service
) -> Dictionary:
	if save_service == null or not save_service.has_method("save_envelope"):
		return _blocked("INVALID_SAVE_SERVICE")
	if envelope == null or not envelope.has_method("to_dict"):
		return _blocked("INVALID_SAVE_ENVELOPE")

	var candidate = SaveEnvelopeScript.from_dict(envelope.to_dict())
	if candidate == null or not candidate.validation_errors.is_empty():
		return _blocked("INVALID_SAVE_ENVELOPE")

	var result: Dictionary = CustomerWorldEventResolverScript.new().resolve(
		candidate,
		item_uid,
		event.duplicate(true),
		damage_roll_percent
	)
	if str(result.get("status", "")) != "APPLIED":
		return result

	var save_error: Error = save_service.save_envelope(candidate)
	if save_error != OK:
		return _blocked("SAVE_FAILED:%d" % int(save_error))

	result["envelope"] = candidate
	return result


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
