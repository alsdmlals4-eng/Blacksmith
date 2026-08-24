extends "res://addons/gut/test.gd"

const CONTEXT_PACKET_PATH := "res://scripts/vertical_slice/domain/vs_customer_context_packet.gd"
const CONTEXT_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_customer_context_resolver.gd"
const PRECISION_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd"


func test_task4_runtime_surfaces_exist() -> void:
	assert_true(ResourceLoader.exists(CONTEXT_PACKET_PATH), "customer context packet must exist")
	assert_true(ResourceLoader.exists(CONTEXT_RESOLVER_PATH), "customer context resolver must exist")
	assert_true(ResourceLoader.exists(PRECISION_RESOLVER_PATH), "precision resolver must exist")


func test_context_packet_and_resolver_api_exist() -> void:
	var packet = load(CONTEXT_PACKET_PATH).new()
	var resolver = load(CONTEXT_RESOLVER_PATH).new()
	assert_true(packet.has_method("to_dict"), "context packet must serialize its external snapshot")
	assert_true(packet.has_method("maximum_load"), "context packet must expose the hard-load ceiling")
	assert_true(packet.has_method("related_ability_value"), "context packet must expose the selected contextual ability")
	assert_true(resolver.has_method("evaluate"), "context resolver must expose assignment evaluation")
	assert_true(resolver.has_method("enhancement_contribution_pp"), "context resolver must own Decision24 enhancement contribution")
	assert_true(resolver.has_method("proficiency_modifier_pp"), "context resolver must own proficiency mapping")
