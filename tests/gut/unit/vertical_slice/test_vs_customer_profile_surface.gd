extends "res://addons/gut/test.gd"

const CUSTOMER_PROFILE_PATH := "res://scripts/vertical_slice/domain/vs_customer_profile.gd"
const NADIA_DATA_PATH := "res://data/vertical_slice/customers/nadia_venn.json"


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
