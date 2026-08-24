class_name VSCustomerContextPacket
extends RefCounted

const SCHEMA_VERSION := 1
const RELATED_ABILITIES := ["STRENGTH", "DEXTERITY", "CONSTITUTION", "JUDGMENT"]
const REQUIRED_FIELDS := [
	"schema_version",
	"customer_id",
	"content_id",
	"primary_need",
	"secondary_need",
	"known_context",
	"risk",
	"strength",
	"dexterity",
	"constitution",
	"judgment",
	"weapon_proficiency",
	"related_ability",
	"required_function_if_explicit",
	"relevant_precision_axes",
	"relevant_function_ids",
]

var schema_version: int = SCHEMA_VERSION
var customer_id: String = ""
var content_id: String = ""
var primary_need: String = ""
var secondary_need: String = ""
var known_context: Array[String] = []
var risk: int = 0
var strength: int = 0
var dexterity: int = 0
var constitution: int = 0
var judgment: int = 0
var weapon_proficiency: int = 0
var related_ability: String = ""
var required_function_if_explicit: String = ""
var relevant_precision_axes: Array[String] = []
var relevant_function_ids: Array[String] = []
var validation_errors: Array[String] = []


static func from_dict(value: Dictionary) -> VSCustomerContextPacket:
	var packet := VSCustomerContextPacket.new()
	for field_name in REQUIRED_FIELDS:
		if not value.has(field_name):
			packet.validation_errors.append("MISSING_REQUIRED_FIELD:%s" % field_name)

	packet.schema_version = int(value.get("schema_version", 0))
	packet.customer_id = str(value.get("customer_id", ""))
	packet.content_id = str(value.get("content_id", ""))
	packet.primary_need = str(value.get("primary_need", ""))
	packet.secondary_need = str(value.get("secondary_need", ""))
	for entry in value.get("known_context", []):
		packet.known_context.append(str(entry))
	packet.risk = int(value.get("risk", 0))
	packet.strength = int(value.get("strength", 0))
	packet.dexterity = int(value.get("dexterity", 0))
	packet.constitution = int(value.get("constitution", 0))
	packet.judgment = int(value.get("judgment", 0))
	packet.weapon_proficiency = int(value.get("weapon_proficiency", 0))
	packet.related_ability = str(value.get("related_ability", ""))
	packet.required_function_if_explicit = str(value.get("required_function_if_explicit", ""))
	for entry in value.get("relevant_precision_axes", []):
		packet.relevant_precision_axes.append(str(entry))
	for entry in value.get("relevant_function_ids", []):
		packet.relevant_function_ids.append(str(entry))
	packet._validate_values()
	return packet


func to_dict() -> Dictionary:
	return {
		"schema_version": schema_version,
		"customer_id": customer_id,
		"content_id": content_id,
		"primary_need": primary_need,
		"secondary_need": secondary_need,
		"known_context": known_context.duplicate(),
		"risk": risk,
		"strength": strength,
		"dexterity": dexterity,
		"constitution": constitution,
		"judgment": judgment,
		"weapon_proficiency": weapon_proficiency,
		"related_ability": related_ability,
		"required_function_if_explicit": required_function_if_explicit,
		"relevant_precision_axes": relevant_precision_axes.duplicate(),
		"relevant_function_ids": relevant_function_ids.duplicate(),
	}


func maximum_load() -> int:
	return strength * 10


func related_ability_value() -> int:
	match related_ability:
		"STRENGTH":
			return strength
		"DEXTERITY":
			return dexterity
		"CONSTITUTION":
			return constitution
		"JUDGMENT":
			return judgment
		_:
			return 0


func _validate_values() -> void:
	if schema_version != SCHEMA_VERSION:
		validation_errors.append("UNSUPPORTED_CUSTOMER_CONTEXT_SCHEMA:%d" % schema_version)
	if customer_id.is_empty():
		validation_errors.append("MISSING_CUSTOMER_ID")
	if content_id.is_empty():
		validation_errors.append("MISSING_CONTENT_ID")
	if primary_need.is_empty():
		validation_errors.append("MISSING_PRIMARY_NEED")
	if secondary_need.is_empty():
		validation_errors.append("MISSING_SECONDARY_NEED")
	if not RELATED_ABILITIES.has(related_ability):
		validation_errors.append("INVALID_RELATED_ABILITY:%s" % related_ability)
	if weapon_proficiency < 0 or weapon_proficiency > 3:
		validation_errors.append("INVALID_WEAPON_PROFICIENCY:%d" % weapon_proficiency)
