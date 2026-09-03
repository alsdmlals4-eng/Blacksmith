# 현재 구현된 고객 프로필을 명시적 ID로만 읽는다. 파일 탐색이나 신규 고객 추론은 하지 않는다.
class_name VSCustomerProfileRepository
extends RefCounted

const CustomerProfileScript = preload("res://scripts/vertical_slice/domain/vs_customer_profile.gd")
const CUSTOMER_PROFILE_PATHS := {
	"NADIA_VENN": "res://data/vertical_slice/customers/nadia_venn.json",
}


func load_profile(customer_id: String) -> Dictionary:
	var profile_path: String = str(CUSTOMER_PROFILE_PATHS.get(customer_id, ""))
	if profile_path.is_empty():
		return _blocked("UNKNOWN_CUSTOMER_ID")
	var file := FileAccess.open(profile_path, FileAccess.READ)
	if file == null:
		return _blocked("CUSTOMER_PROFILE_UNREADABLE")
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary:
		return _blocked("INVALID_CUSTOMER_PROFILE_DATA")
	var profile = CustomerProfileScript.from_dict(parsed)
	if profile == null or not profile.validation_errors.is_empty() or profile.customer_id != customer_id:
		return _blocked("INVALID_CUSTOMER_PROFILE")
	return {"status": "APPLIED", "profile": profile}


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
