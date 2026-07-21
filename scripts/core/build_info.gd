class_name BuildInfo
extends RefCounted

const VERSION := "POC v0.3.1"
const CHANNEL := "main"
const BUILD_ID := "2026.07.21.1"


static func display_text() -> String:
	return "%s · %s · %s" % [VERSION, CHANNEL, BUILD_ID]
