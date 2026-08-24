extends "res://addons/gut/test.gd"

const CUSTOMER_PROFILE_PATH := "res://scripts/vertical_slice/domain/vs_customer_profile.gd"
const NADIA_DATA_PATH := "res://data/vertical_slice/customers/nadia_venn.json"


func _profile_script():
	if not ResourceLoader.exists(CUSTOMER_PROFILE_PATH):
		return null
	return load(CUSTOMER_PROFILE_PATH)


func _load_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	assert_not_null(file, "customer data must be readable")
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	assert_true(parsed is Dictionary, "customer data must parse as a dictionary")
	if parsed is Dictionary:
		return parsed
	return {}


func test_customer_profile_runtime_surface_exists() -> void:
	assert_true(
		ResourceLoader.exists(CUSTOMER_PROFILE_PATH),
		"visitor standing requires a current V2 customer profile domain model"
	)


func test_nadia_v2_customer_data_exists() -> void:
	assert_true(
		FileAccess.file_exists(NADIA_DATA_PATH),
		"Nadia starter visitor must have current V2 customer data"
	)


func test_nadia_identity_standing_and_epithet_round_trip() -> void:
	var script = _profile_script()
	assert_not_null(script, "customer profile script must load")
	if script == null:
		return
	var profile = script.from_dict(_load_json(NADIA_DATA_PATH))
	assert_true(profile.validation_errors.is_empty(), "Nadia visitor profile must validate")
	assert_eq(profile.customer_id, "NADIA_VENN")
	assert_eq(profile.name, "나디아 벤")
	assert_eq(profile.role, "유적 탐사대장")
	assert_eq(profile.public_epithet, "유적의 길잡이")
	assert_eq(profile.public_standing_grade, "ELITE")
	assert_eq(profile.public_standing_label_ko(), "정예")
	assert_eq(profile.player_header_ko(), "[정예] 「유적의 길잡이」 나디아 벤")
	assert_eq(script.from_dict(profile.to_dict()).to_dict(), profile.to_dict())


func test_only_five_public_standing_grades_are_accepted() -> void:
	var script = _profile_script()
	assert_not_null(script, "customer profile script must load")
	if script == null:
		return
	var base_data := _load_json(NADIA_DATA_PATH)
	for grade in ["COMMON", "SKILLED", "ELITE", "RENOWNED", "LEGENDARY"]:
		var candidate := base_data.duplicate(true)
		candidate["public_standing_grade"] = grade
		var profile = script.from_dict(candidate)
		assert_true(profile.validation_errors.is_empty(), "approved standing must validate: %s" % grade)


func test_unknown_public_standing_grade_fails_closed() -> void:
	var script = _profile_script()
	assert_not_null(script, "customer profile script must load")
	if script == null:
		return
	var candidate := _load_json(NADIA_DATA_PATH)
	candidate["public_standing_grade"] = "MYTHIC_POWER_9000"
	var profile = script.from_dict(candidate)
	assert_true(
		profile.validation_errors.has("INVALID_PUBLIC_STANDING_GRADE:MYTHIC_POWER_9000"),
		"visitor standing must be an explicit five-tier public label, not an arbitrary power tier"
	)


func test_generic_visitor_may_have_no_epithet_but_named_profile_keeps_explicit_field() -> void:
	var script = _profile_script()
	assert_not_null(script, "customer profile script must load")
	if script == null:
		return
	var candidate := _load_json(NADIA_DATA_PATH)
	candidate["customer_id"] = "GENERIC_VISITOR_FIXTURE"
	candidate["name"] = "방문객"
	candidate["public_epithet"] = ""
	var profile = script.from_dict(candidate)
	assert_true(profile.validation_errors.is_empty(), "generic visitor may intentionally have no epithet")
	assert_eq(profile.player_header_ko(), "[정예] 방문객")
