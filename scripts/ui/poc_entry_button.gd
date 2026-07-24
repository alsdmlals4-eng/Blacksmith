extends Button


func _ready() -> void:
	text = "장비 생애 PoC"
	custom_minimum_size = Vector2(190.0, 54.0)
	add_theme_font_size_override("font_size", 18)
	pressed.connect(_open_poc)


func _open_poc() -> void:
	get_tree().change_scene_to_file("res://scenes/test/equipment_lifecycle_poc.tscn")
