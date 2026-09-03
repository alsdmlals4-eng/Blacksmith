extends "res://addons/gut/test.gd"

const SCREEN_PATH := "res://scripts/vertical_slice/ui/vs_customer_handoff_screen.gd"
const PROFILE_PATH := "res://scripts/vertical_slice/domain/vs_customer_profile.gd"
const NADIA_DATA_PATH := "res://data/vertical_slice/customers/nadia_venn.json"


func _nadia_profile():
	var file := FileAccess.open(NADIA_DATA_PATH, FileAccess.READ)
	if file == null:
		return null
	var raw: Variant = JSON.parse_string(file.get_as_text())
	if not raw is Dictionary:
		return null
	return load(PROFILE_PATH).from_dict(raw)


func test_handoff_and_return_surface_use_the_registered_customer_profile() -> void:
	assert_true(ResourceLoader.exists(SCREEN_PATH))
	if not ResourceLoader.exists(SCREEN_PATH):
		return
	var profile = _nadia_profile()
	assert_not_null(profile)
	if profile == null:
		return
	var screen = load(SCREEN_PATH).new()
	add_child_autofree(screen)
	assert_eq(screen.configure_handoff("BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 10, profile).get("status", ""), "APPLIED")
	var handoff_state: Dictionary = screen.view_state()
	assert_eq(handoff_state.get("customer_header", ""), "[정예] 「유적의 길잡이」 나디아 벤")
	assert_eq(handoff_state.get("customer_context", ""), "유적 탐사대장 · 생환과 회수를 위한 탐사")
	assert_true(str(handoff_state.get("message", "")).contains("나디아 벤"))
	assert_eq(screen.configure_return_beat("BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", profile).get("status", ""), "APPLIED")
	assert_true(str(screen.view_state().get("message", "")).contains("나디아 벤"))


func test_handoff_refuses_a_missing_or_unvalidated_customer_profile() -> void:
	var screen = load(SCREEN_PATH).new()
	add_child_autofree(screen)
	assert_eq(
		screen.configure_handoff("BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 10, null),
		{"status": "BLOCKED", "reason": "INVALID_CUSTOMER_PROFILE"}
	)
