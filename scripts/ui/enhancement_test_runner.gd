extends Control

const EnhancementScreenScript = preload("res://scripts/ui/special_enhancement_screen.gd")

var current_screen: Control


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_show_enhancement_test()


func _show_enhancement_test() -> void:
	if current_screen != null and is_instance_valid(current_screen):
		current_screen.queue_free()
	current_screen = EnhancementScreenScript.new()
	current_screen.configure_weapon({
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"quality_id": "TEST",
		"quality_label": "테스트용 철검",
		"quality_multiplier": 1.0,
	})
	current_screen.restart_requested.connect(_show_enhancement_test)
	current_screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(current_screen)
