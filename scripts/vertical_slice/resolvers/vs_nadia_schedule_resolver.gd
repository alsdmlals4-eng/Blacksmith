class_name VSNadiaScheduleResolver
extends RefCounted

const CustomerContextResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_customer_context_resolver.gd")


func handoff(customer, item, context) -> Dictionary:
	if customer == null:
		return _blocked("MISSING_CUSTOMER")
	if str(customer.customer_id) != "NADIA_VENN":
		return _blocked("CUSTOMER_NOT_NADIA")
	if item == null:
		return _blocked("MISSING_ITEM")
	if context == null:
		return _blocked("MISSING_CONTEXT")
	if not context.validation_errors.is_empty():
		return _blocked("INVALID_CONTEXT")
	if str(context.customer_id) != "NADIA_VENN" or str(context.content_id) != "ADVENTURER_01":
		return _blocked("CONTEXT_MISMATCH")
	if str(item.physical_state) == "DESTROYED":
		return _blocked("ITEM_DESTROYED")

	var assignment: Dictionary = CustomerContextResolverScript.new().evaluate(customer, item, context)
	if not bool(assignment.get("assignment_allowed", false)):
		return _blocked(str(assignment.get("reason", "ASSIGNMENT_BLOCKED")))

	return {
		"status": "HANDOFF_ACCEPTED",
		"customer_id": "NADIA_VENN",
		"content_id": "ADVENTURER_01",
		"assigned_uid": str(item.uid),
		"schedule_type": "PERSONAL_SCHEDULE",
		"initial_stage": "PREP_AND_ENTRY",
		"schedule_status": "ACTIVE",
		"result_available": false,
	}


func _blocked(reason: String) -> Dictionary:
	return {
		"status": "BLOCKED",
		"reason": reason,
		"result_available": false,
	}
