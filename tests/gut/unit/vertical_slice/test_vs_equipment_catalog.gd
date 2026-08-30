extends "res://addons/gut/test.gd"

const CatalogScript = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")


func test_catalog_exposes_exactly_five_ids_and_weapon_only_precision_eligibility() -> void:
	var entries: Array = CatalogScript.all()
	assert_eq(entries.size(), 5)
	var ids: Array[String] = []
	for entry in entries:
		ids.append(str(entry.get("equipment_id", "")))
	assert_eq(ids, ["iron_sword", "iron_shield", "iron_bow", "iron_armor", "iron_helmet"])
	assert_true(bool(CatalogScript.by_id("iron_sword").get("precision_tag_eligible", false)))
	assert_true(bool(CatalogScript.by_id("iron_shield").get("precision_tag_eligible", false)))
	assert_true(bool(CatalogScript.by_id("iron_bow").get("precision_tag_eligible", false)))
	assert_false(bool(CatalogScript.by_id("iron_armor").get("precision_tag_eligible", true)))
	assert_false(bool(CatalogScript.by_id("iron_helmet").get("precision_tag_eligible", true)))


func test_catalog_validates_each_group_profile_pair_without_accepting_crossed_pairs() -> void:
	assert_true(CatalogScript.is_valid_identity("SWORD", "PHYSICAL_WEAPON_ATTACK"))
	assert_true(CatalogScript.is_valid_identity("SHIELD", "PHYSICAL_WEAPON_GUARD"))
	assert_true(CatalogScript.is_valid_identity("BOW", "PHYSICAL_WEAPON_RANGED"))
	assert_true(CatalogScript.is_valid_identity("ARMOR", "ARMOR_BODY_DEFENSE"))
	assert_true(CatalogScript.is_valid_identity("HELMET", "ARMOR_HEAD_DEFENSE"))
	assert_false(CatalogScript.is_valid_identity("ARMOR", "PHYSICAL_WEAPON_ATTACK"))
	assert_true(CatalogScript.has_equipment_group("HELMET"))
	assert_false(CatalogScript.has_equipment_group("AXE"))
