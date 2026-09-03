class_name VSCustomerProfile
extends RefCounted

const SCHEMA_VERSION := 1
const PUBLIC_STANDING_GRADES := [
	"COMMON",
	"SKILLED",
	"ELITE",
	"RENOWNED",
	"LEGENDARY",
]
const PUBLIC_STANDING_LABELS_KO := {
	"COMMON": "일반",
	"SKILLED": "숙련",
	"ELITE": "정예",
	"RENOWNED": "명망",
	"LEGENDARY": "전설",
}
const CONTENT_GOAL_LABELS_KO := {
	"SURVIVAL_AND_RECOVERY": "생환과 회수를 위한 탐사",
}
const REQUIRED_FIELDS := [
	"schema_version",
	"customer_id",
	"name",
	"role",
	"public_epithet",
	"public_standing_grade",
	"content_id",
	"content_goal",
	"numeric_capability_profile",
]

var schema_version: int = SCHEMA_VERSION
var customer_id: String = ""
var name: String = ""
var role: String = ""
var public_epithet: String = ""
var public_standing_grade: String = "COMMON"
var content_id: String = ""
var content_goal: String = ""
# Identity/standing is intentionally separate from the customer's numeric
# capability source. Current Nadia numeric ability values are not invented here.
var numeric_capability_profile: String = "SEPARATE_CANON_SOURCE_REQUIRED"
var validation_errors: Array[String] = []


static func from_dict(value: Dictionary) -> VSCustomerProfile:
	var profile := VSCustomerProfile.new()
	for field_name in REQUIRED_FIELDS:
		if not value.has(field_name):
			profile.validation_errors.append("MISSING_REQUIRED_FIELD:%s" % field_name)

	profile.schema_version = int(value.get("schema_version", 0))
	profile.customer_id = str(value.get("customer_id", ""))
	profile.name = str(value.get("name", ""))
	profile.role = str(value.get("role", ""))
	profile.public_epithet = str(value.get("public_epithet", ""))
	profile.public_standing_grade = str(value.get("public_standing_grade", ""))
	profile.content_id = str(value.get("content_id", ""))
	profile.content_goal = str(value.get("content_goal", ""))
	profile.numeric_capability_profile = str(value.get("numeric_capability_profile", ""))
	profile._validate_values()
	return profile


func to_dict() -> Dictionary:
	return {
		"schema_version": schema_version,
		"customer_id": customer_id,
		"name": name,
		"role": role,
		"public_epithet": public_epithet,
		"public_standing_grade": public_standing_grade,
		"content_id": content_id,
		"content_goal": content_goal,
		"numeric_capability_profile": numeric_capability_profile,
	}


func public_standing_label_ko() -> String:
	return str(PUBLIC_STANDING_LABELS_KO.get(public_standing_grade, public_standing_grade))


func player_header_ko() -> String:
	var prefix := "[%s]" % public_standing_label_ko()
	if public_epithet.is_empty():
		return "%s %s" % [prefix, name]
	return "%s 「%s」 %s" % [prefix, public_epithet, name]


func work_request_summary_ko() -> String:
	return str(CONTENT_GOAL_LABELS_KO.get(content_goal, "기록된 의뢰"))


func _validate_values() -> void:
	if schema_version != SCHEMA_VERSION:
		validation_errors.append("UNSUPPORTED_CUSTOMER_PROFILE_SCHEMA:%d" % schema_version)
	if customer_id.is_empty():
		validation_errors.append("MISSING_CUSTOMER_ID")
	if name.is_empty():
		validation_errors.append("MISSING_CUSTOMER_NAME")
	if role.is_empty():
		validation_errors.append("MISSING_CUSTOMER_ROLE")
	if not PUBLIC_STANDING_GRADES.has(public_standing_grade):
		validation_errors.append("INVALID_PUBLIC_STANDING_GRADE:%s" % public_standing_grade)
	if content_id.is_empty():
		validation_errors.append("MISSING_CONTENT_ID")
	if content_goal.is_empty():
		validation_errors.append("MISSING_CONTENT_GOAL")
	if numeric_capability_profile.is_empty():
		validation_errors.append("MISSING_NUMERIC_CAPABILITY_PROFILE_SOURCE")
