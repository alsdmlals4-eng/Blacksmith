class_name PrecisionGauge
extends Control

var pointer_value: float = 0.0
var target_value: float = 0.5
var perfect_radius: float = 0.07
var good_radius: float = 0.18


func _ready() -> void:
	custom_minimum_size = Vector2(0.0, 72.0)
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func set_pointer(value: float) -> void:
	pointer_value = clampf(value, 0.0, 1.0)
	queue_redraw()


func configure(target: float, perfect: float, good: float) -> void:
	target_value = clampf(target, 0.0, 1.0)
	perfect_radius = maxf(perfect, 0.0)
	good_radius = maxf(good, perfect_radius)
	queue_redraw()


func _draw() -> void:
	var track := Rect2(Vector2(0.0, size.y * 0.32), Vector2(size.x, size.y * 0.36))
	draw_style_box(_style(Color("#20252d"), 12.0), track)

	var good_start := clampf(target_value - good_radius, 0.0, 1.0) * size.x
	var good_end := clampf(target_value + good_radius, 0.0, 1.0) * size.x
	var perfect_start := clampf(target_value - perfect_radius, 0.0, 1.0) * size.x
	var perfect_end := clampf(target_value + perfect_radius, 0.0, 1.0) * size.x

	draw_rect(Rect2(Vector2(good_start, track.position.y), Vector2(good_end - good_start, track.size.y)), Color("#b26d2f"))
	draw_rect(Rect2(Vector2(perfect_start, track.position.y), Vector2(perfect_end - perfect_start, track.size.y)), Color("#f2c14e"))

	var pointer_x := pointer_value * size.x
	var track_bottom := track.position.y + track.size.y
	draw_line(Vector2(pointer_x, track.position.y - 12.0), Vector2(pointer_x, track_bottom + 12.0), Color.WHITE, 6.0, true)
	draw_circle(Vector2(pointer_x, track.position.y - 12.0), 7.0, Color.WHITE)


func _style(color: Color, radius: float) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.corner_radius_top_left = int(radius)
	style.corner_radius_top_right = int(radius)
	style.corner_radius_bottom_left = int(radius)
	style.corner_radius_bottom_right = int(radius)
	return style
