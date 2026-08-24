class_name VSCustomerContextPacket
extends RefCounted

var schema_version := 1
var customer_id := ""
var content_id := ""
var primary_need := ""
var secondary_need := ""
var known_context: Array[String] = []
var risk := 0
var strength := 0
var dexterity := 0
var constitution := 0
var judgment := 0
var weapon_proficiency := 0
var related_ability := ""
var required_function_if_explicit := ""
var relevant_precision_axes: Array[String] = []
var relevant_function_ids: Array[String] = []


func to_dict() -> Dictionary:
	return {}


func maximum_load() -> int:
	return 0


func related_ability_value() -> int:
	return 0
