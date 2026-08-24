extends "res://addons/gut/test.gd"

const CONTEXT_PACKET_PATH := "res://scripts/vertical_slice/domain/vs_customer_context_packet.gd"
const CONTEXT_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_customer_context_resolver.gd"
const PRECISION_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd"


func test_task4_runtime_surfaces_exist() -> void:
	assert_true(ResourceLoader.exists(CONTEXT_PACKET_PATH), "customer context packet must exist")
	assert_true(ResourceLoader.exists(CONTEXT_RESOLVER_PATH), "customer context resolver must exist")
	assert_true(ResourceLoader.exists(PRECISION_RESOLVER_PATH), "precision resolver must exist")
