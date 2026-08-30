# Blacksmith Asset Rights and Provenance Record

> 자산마다 복사해 작성한다. 빈 Template은 실제 권리 증거가 아니다.

```yaml
asset_id:
category: MUSIC_SFX | FONT | CHARACTER_ILLUSTRATION | MODEL_3D_ANIMATION | PLUGIN_ASSET | OPEN_SOURCE_LIBRARY | AI_OUTPUT_MODEL_TERMS | OUTSOURCING_CONTRACT | VOICE_COMPOSER_TRANSLATOR_CONTRACT | OTHER
name:
project: BLACKSMITH
creation_route: OWNED_ORIGINAL | COMMISSIONED_ORIGINAL | LICENSED_THIRD_PARTY | OPEN_SOURCE | AI_GENERATED | REFERENCE_TO_ORIGINAL | MIXED_ROUTE
creator_or_vendor:
source_url_or_path:
source_checked_at:
acquired_or_created_at:
license_or_contract:
license_version_or_terms_date:
commercial_use: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
distribution_in_game_build: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
raw_source_redistribution: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
modification: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
attribution:
platform_or_territory_restrictions:
term_or_expiration:
seat_account_or_project_restrictions:
open_source_notice_or_source_obligation:
ai_model_service_version:
ai_account_or_plan:
ai_terms_checked_at:
ai_input_rights:
ai_output_terms:
ai_human_contribution_and_postprocessing:
contract_scope:
voice_clone_or_ai_training_rights:
reference_sources:
reference_brief:
forbidden_expression:
final_asset_record:
reference_similarity_status: PASS | REVISION_REQUIRED | BLOCKED_UNVERIFIED | NOT_APPLICABLE
shipping_and_marketing_usage:
proof_reference:
proof_hash:
secure_original_location:
redacted_excerpt:
reviewed_by:
reviewed_at:
status: APPROVED | CONDITIONAL | REJECTED | RELEASE_BLOCKED_UNVERIFIED | SUPERSEDED
notes:
```

`commercial_use`, `distribution_in_game_build`, `raw_source_redistribution`, `modification`은 서로 다른 권리다. 필요한 값이 `UNKNOWN`이거나 조건 충족 증거가 없으면 `RELEASE_BLOCKED_UNVERIFIED`다.

## Current asset record · ASSET-WORKSHOP-BACKGROUND-V2

```yaml
asset_id: ASSET-WORKSHOP-BACKGROUND-V2
category: OTHER
name: Workshop background v2
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI built-in image generation tool
source_url_or_path: assets/ui/workshop/workshop_enhancement_background_v2.png
acquired_or_created_at: 2026-08-28 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: NOT_REQUIRED
modification: UNKNOWN
ai_model_service_version: BUILT_IN_IMAGE_TOOL_UNVERSIONED
ai_input_rights: ORIGINAL_TEXT_BRIEF_ONLY; no third-party reference image used
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original production brief, selection, consumer mapping, and non-destructive runtime binding
reference_sources: Current Blacksmith art direction only; legacy v1 was not used as an image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, logos, runes, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-WORKSHOP-BACKGROUND-V2
reference_similarity_status: NOT_APPLICABLE
proof_hash: A3D305D28AEF0AABA374C7B435DC8ED0EA6F23F16A26BFA992D87682025382B5
status: RELEASE_BLOCKED_UNVERIFIED
notes: Project asset approval plus Workshop static and Main Menu dynamic runtime bindings are approved; release-rights review, Godot client render, Android readability, accessibility, and human visual review remain NOT_RUN.
```

## Current asset record · ASSET-WORKPIECE-DURABILITY-STATE-ATLAS-V1

```yaml
asset_id: ASSET-WORKPIECE-DURABILITY-STATE-ATLAS-V1
category: OTHER
name: Workpiece durability state atlas v1
project: BLACKSMITH
creation_route: AI_GENERATED
creation_date: 2026-08-28 KST
source_location: Built-in image generation artifact exec-b6622a40-8552-4cf3-86c3-355898d3540a; corrected opaque-background revision of the original state atlas
asset_path: assets/ui/workshop/workpiece_durability_state_atlas_v1.png
actual_consumer: VSWorkshopScreen / WorkshopLayout/WorkpieceDurabilityHero
consumer_surface: res://scenes/vertical_slice/screens/vs_workshop_screen.tscn
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original production brief, state-family selection, consumer mapping, and dynamic runtime atlas binding
reference_sources: Current Blacksmith art direction only; no third-party visual source was supplied as image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, logos, runes, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-WORKPIECE-DURABILITY-STATE-ATLAS-V1
reference_similarity_status: NOT_APPLICABLE
proof_hash: FA296911D634BF80F78DAF41A564A067BE3990C4FAB4988CFB8A5792573258FA
status: RELEASE_BLOCKED_UNVERIFIED
notes: Project asset approval and dynamic NORMAL/MINOR/MAJOR/DESTROYED runtime binding are approved; release-rights review, Godot client render, Android readability, accessibility, and human visual review remain NOT_RUN.
```

## Current asset record · ASSET-FIRST-FORGE-BACKGROUND-V1

```yaml
asset_id: ASSET-FIRST-FORGE-BACKGROUND-V1
category: OTHER
name: First forge background v1
project: BLACKSMITH
creation_route: AI_GENERATED
creation_date: 2026-08-28 KST
source_location: Built-in image generation artifact exec-db9184a2-a9e8-4265-81a6-8748ceb8b5e3
asset_path: assets/ui/workshop/first_forge_background_v1.png
actual_consumer: ForgingScreen / FirstForgeIllustratedBackground
consumer_surface: res://scripts/ui/forging_screen.gd
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original production brief, selection, consumer mapping, runtime binding, and readability-veil integration
reference_sources: Approved Blacksmith workshop background v2 only; no third-party visual source was supplied as image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, logos, runes, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-FIRST-FORGE-BACKGROUND-V1
reference_similarity_status: NOT_APPLICABLE
proof_hash: A575D0CDD0A8A487C74E12751647E959495E6182A374BB145B9AD98AF4E64954
status: RELEASE_BLOCKED_UNVERIFIED
notes: Project asset approval plus dynamic runtime binding and noninteractive readability veil are approved; release-rights review, Godot client render, Android readability, accessibility, and human visual review remain NOT_RUN.
```

## Current asset record · ASSET-ILLUSTRATED-WORKSHOP-BOOK-REFERENCE-V1

```yaml
asset_id: ASSET-ILLUSTRATED-WORKSHOP-BOOK-REFERENCE-V1
category: PRODUCTION_VISUAL_REFERENCE
name: Illustrated Workshop Book production reference v1
project: BLACKSMITH
creation_route: AI_GENERATED
creation_date: 2026-08-28 KST
source_location: Built-in image generation artifact exec-4515fbf7-2250-4f2b-a0fb-6350c5714c5b
asset_path: assets/visual_reference/illustrated_workshop_book_reference_v1.png
actual_consumer: NONE_BY_DESIGN
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original production brief, reference selection, and category boundary declaration
reference_sources: Current Blacksmith art direction plus project-owned v2 workshop and durability-atlas assets only
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, logos, runes, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-ILLUSTRATED-WORKSHOP-BOOK-REFERENCE-V1
reference_similarity_status: NOT_APPLICABLE
proof_hash: A05A3E3A30CEFA458305DABC1BA69A95AA71B580EAFDE6713B5A38C806051D1E
status: PRODUCTION_REFERENCE_APPROVED_NOT_RUNTIME
notes: May guide art production only. It is not a runtime or public marketing asset.
```

## Current asset record · ASSET-BLACKSMITH-KEY-ART-MASTER-V1

```yaml
asset_id: ASSET-BLACKSMITH-KEY-ART-MASTER-V1
category: RELEASE_MARKETING_MASTER
name: Blacksmith key art master v1
project: BLACKSMITH
creation_route: AI_GENERATED
creation_date: 2026-08-28 KST
source_location: Built-in image generation artifact exec-dd7c69a3-5331-48e2-827c-5e14ed532d60
asset_path: assets/marketing/blacksmith_key_art_master_v1.png
actual_consumer: NONE_BY_DESIGN
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original production brief, selection, and release-category boundary declaration
reference_sources: Project-owned first-forge background only
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, logos, runes, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-BLACKSMITH-KEY-ART-MASTER-V1
reference_similarity_status: NOT_APPLICABLE
proof_hash: DBF22D182C8B38F752BA5564E644733EE44DEB9D2E51B0991A13F9A89D3515E3
status: RELEASE_DRAFT_NOT_PLATFORM_READY
notes: Master art only. It requires current platform specs, title treatment, rights review, and final review before any external use.
```

## Current asset record · ASSET-BLACKSMITH-APP-ICON-MASTER-V1

```yaml
asset_id: ASSET-BLACKSMITH-APP-ICON-MASTER-V1
category: RELEASE_MARKETING_MASTER
name: Blacksmith app icon master v1
project: BLACKSMITH
creation_route: AI_GENERATED
creation_date: 2026-08-28 KST
source_location: Built-in image generation artifact exec-1eee9e1d-7bd0-4fc3-85c4-9e6971b990ab
asset_path: assets/marketing/blacksmith_app_icon_master_v1.png
actual_consumer: NONE_BY_DESIGN
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original production brief, selection, and release-category boundary declaration
reference_sources: Project-owned durability state atlas only
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, logos, runes, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-BLACKSMITH-APP-ICON-MASTER-V1
reference_similarity_status: NOT_APPLICABLE
proof_hash: A014266240C5D1CF79646F7570056200E1C713B986C39E2C0D9917C66FABC1B0
status: RELEASE_DRAFT_NOT_PLATFORM_READY
notes: Square source master only. It requires current platform specs, safe-zone export, rights review, and final review before external use.
```

## Current asset record · ASSET-MAIN-MENU-DAWN-BACKGROUND-V1

```yaml
asset_id: ASSET-MAIN-MENU-DAWN-BACKGROUND-V1
category: OTHER
name: Main menu dawn background v1
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI ImageGen
source_url_or_path: assets/ui/workshop/main_menu_dawn_background_v1.png
acquired_or_created_at: 2026-08-30 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original brief, user selection, consumer mapping, and dynamic runtime binding
reference_sources: Current Blacksmith art direction only; no third-party image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, logos, watermarks, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-MAIN-MENU-DAWN-BACKGROUND-V1
proof_hash: 5870f6958135516b9d5f42f81e0d11e0724a5cbf27af9e3382f1de155a7f713a
status: RELEASE_BLOCKED_UNVERIFIED
notes: User 2026-08-30 approval; MenuIllustratedBackground dynamic binding is machine-verified. Godot client, Android, accessibility, human review, and release remain NOT_RUN or blocked.
```

## Historical retired asset record · ASSET-PRECISION-TAG-WORKSHOP-BACKGROUND-V1

```yaml
asset_id: ASSET-PRECISION-TAG-WORKSHOP-BACKGROUND-V1
category: OTHER
name: Precision tag workshop background v1
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI ImageGen
source_url_or_path: RETIRED_20260830 / former assets/ui/workshop/precision_tag_workshop_background_v1.png
acquired_or_created_at: 2026-08-30 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original brief, user selection, exact-target-only dynamic binding, and native-control preservation
reference_sources: Current Blacksmith art direction only; no third-party image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, numerals, logos, watermarks, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#retired_asset_records/ASSET-PRECISION-TAG-WORKSHOP-BACKGROUND-V1
proof_hash: 45679f660ad9fc24796e0080aded8474be6b0c462ae7bb2d58a91b6c0530ef32
status: SUPERSEDED
notes: User 2026-08-30 direction explicitly removes the dedicated Precision Workshop raster. Binding and repository file were retired; native tag-selection UX is the replacement consumer. This historical record does not approve a runtime asset. Godot client, Android, accessibility, human review, and release remain NOT_RUN or blocked.
```

## Current asset record · Five equipment identity illustrations v1

These five objects share one approved production brief and the same two runtime consumers, but retain individual file and hash identities in the asset manifest. The locked 1254×1254 PNG source bytes remain provenance-hashed; the runtime import applies a 512px lossless 2D/no-mipmap ceiling for the 96px first-forge card and the 156px Workshop hero. They are identity illustrations only: names, role values, Precision eligibility, costs, probabilities, durability, controls, and outcomes remain native Godot UI. Android memory and visual-quality observation remain `NOT_RUN`.

```yaml
asset_id: ASSET-EQUIPMENT-IRON-SWORD-CARD-V1
category: OTHER
name: Iron sword identity illustration v1
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI ImageGen
source_url_or_path: assets/ui/equipment/iron_sword_card_v1.png
acquired_or_created_at: 2026-08-30 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original isolated-object brief, user lock, exact consumer mapping, and noninteractive dynamic binding
reference_sources: Current Blacksmith ILLUSTRATED_WORKSHOP_BOOK direction only; no third-party image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, numerals, logos, watermarks, UI screenshot, or combat outcome
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-EQUIPMENT-IRON-SWORD-CARD-V1
proof_hash: bbed060e8ac115d51a0ee83bbe285127d292f3cbd4d2b633ef4df2f4258db5cc
status: RELEASE_BLOCKED_UNVERIFIED
notes: User 2026-08-30 runtime-promotion lock. First-forge choice and Workshop identity binding are machine-verified; Godot client, Android, accessibility, human visual review, and release rights remain NOT_RUN or blocked.
```

```yaml
asset_id: ASSET-EQUIPMENT-IRON-SHIELD-CARD-V1
category: OTHER
name: Iron shield identity illustration v1
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI ImageGen
source_url_or_path: assets/ui/equipment/iron_shield_card_v1.png
acquired_or_created_at: 2026-08-30 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original isolated-object brief, user lock, exact consumer mapping, and noninteractive dynamic binding
reference_sources: Current Blacksmith ILLUSTRATED_WORKSHOP_BOOK direction only; no third-party image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, numerals, logos, watermarks, UI screenshot, or combat outcome
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-EQUIPMENT-IRON-SHIELD-CARD-V1
proof_hash: f3c02be3a6a9d375ffb816a4101a124bf7bb86aa97951cb0c0f9c6c98094de0c
status: RELEASE_BLOCKED_UNVERIFIED
notes: User 2026-08-30 runtime-promotion lock. First-forge choice and Workshop identity binding are machine-verified; Godot client, Android, accessibility, human visual review, and release rights remain NOT_RUN or blocked.
```

```yaml
asset_id: ASSET-EQUIPMENT-IRON-BOW-CARD-V1
category: OTHER
name: Iron bow identity illustration v1
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI ImageGen
source_url_or_path: assets/ui/equipment/iron_bow_card_v1.png
acquired_or_created_at: 2026-08-30 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original isolated-object brief, user lock, exact consumer mapping, and noninteractive dynamic binding
reference_sources: Current Blacksmith ILLUSTRATED_WORKSHOP_BOOK direction only; no third-party image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, numerals, logos, watermarks, UI screenshot, or combat outcome
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-EQUIPMENT-IRON-BOW-CARD-V1
proof_hash: 3f7c013553ed71d8821eb83c90f7bcabd90f72b1849701e0fd340e08e8d75f1f
status: RELEASE_BLOCKED_UNVERIFIED
notes: User 2026-08-30 runtime-promotion lock. First-forge choice and Workshop identity binding are machine-verified; Godot client, Android, accessibility, human visual review, and release rights remain NOT_RUN or blocked.
```

```yaml
asset_id: ASSET-EQUIPMENT-IRON-ARMOR-CARD-V1
category: OTHER
name: Iron armor identity illustration v1
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI ImageGen
source_url_or_path: assets/ui/equipment/iron_armor_card_v1.png
acquired_or_created_at: 2026-08-30 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original isolated-object brief, user lock, exact consumer mapping, and noninteractive dynamic binding
reference_sources: Current Blacksmith ILLUSTRATED_WORKSHOP_BOOK direction only; no third-party image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, numerals, logos, watermarks, UI screenshot, or combat outcome
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-EQUIPMENT-IRON-ARMOR-CARD-V1
proof_hash: d4c0b9db933c9fe351575cf793412e22ead9b234590cb8ab60d3a82fcb554cc2
status: RELEASE_BLOCKED_UNVERIFIED
notes: User 2026-08-30 runtime-promotion lock. First-forge choice and Workshop identity binding are machine-verified; Godot client, Android, accessibility, human visual review, and release rights remain NOT_RUN or blocked.
```

```yaml
asset_id: ASSET-EQUIPMENT-IRON-HELMET-CARD-V1
category: OTHER
name: Iron helmet identity illustration v1
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI ImageGen
source_url_or_path: assets/ui/equipment/iron_helmet_card_v1.png
acquired_or_created_at: 2026-08-30 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original isolated-object brief, user lock, exact consumer mapping, and noninteractive dynamic binding
reference_sources: Current Blacksmith ILLUSTRATED_WORKSHOP_BOOK direction only; no third-party image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, numerals, logos, watermarks, UI screenshot, or combat outcome
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-EQUIPMENT-IRON-HELMET-CARD-V1
proof_hash: 90cebb815fdc77b0076b7bab1eca00e1f7be791378d45dd2880f8b8ebe610cfb
status: RELEASE_BLOCKED_UNVERIFIED
notes: User 2026-08-30 runtime-promotion lock. First-forge choice and Workshop identity binding are machine-verified; Godot client, Android, accessibility, human visual review, and release rights remain NOT_RUN or blocked.
```

## Current asset record · ASSET-CUSTOMER-RESULT-RETURN-ILLUSTRATION-V1

```yaml
asset_id: ASSET-CUSTOMER-RESULT-RETURN-ILLUSTRATION-V1
category: OTHER
name: Customer result return illustration v1
project: BLACKSMITH
creation_route: AI_GENERATED
creator_or_vendor: OpenAI ImageGen
source_url_or_path: assets/ui/workshop/customer_result_return_illustration_v1.png
acquired_or_created_at: 2026-08-30 KST
commercial_use: UNKNOWN
distribution_in_game_build: UNKNOWN
raw_source_redistribution: UNKNOWN
modification: UNKNOWN
ai_output_terms: RELEASE_BLOCKED_UNVERIFIED_PENDING_CURRENT_TERMS_REVIEW
ai_human_contribution_and_postprocessing: Original brief, user selection, valid-saved-result-only dynamic binding, and native factual text preservation
reference_sources: Current Blacksmith art direction only; no third-party image input
forbidden_expression: copied game imagery, identifiable third-party visual identity, text, numerical durability display, logos, watermarks, or UI screenshot
final_asset_record: assets/ASSET_MANIFEST.json#ASSET-CUSTOMER-RESULT-RETURN-ILLUSTRATION-V1
proof_hash: 716ce4dd4c6c4bdf48255c4b10aef906573d1113b331d20304e4f75f6e74eca1
status: RELEASE_BLOCKED_UNVERIFIED
notes: User 2026-08-30 approval; valid-result illustration plus readability veil is machine-verified. Godot client, Android, accessibility, human review, and release remain NOT_RUN or blocked.
```

## Reference-to-original

```yaml
reference_only_input_excluded_from_build:
functional_or_general_principles_extracted:
identifiable_expression_removed:
project_specific_canon_applied:
independent_working_files:
comparison_set:
reviewer:
reviewed_at:
reference_similarity_status:
```

기능·정보 위계·상호작용·일반 형태·재질·주파수·타이밍·성능 원리만 분석한다. tracing, overpaint, sample·멜로디·리프·보컬 재사용, mesh·texture·rig·animation clip·font glyph 추출, 특정 작가·성우·실존 인물 모사, 원본 AI 변환을 독립 제작으로 인정하지 않는다.

공개 저장소에는 원계약서, 신분증, 서명, 주소, 계좌·결제·세금·개인정보를 넣지 않는다. 접근 통제된 보관소의 `secure_original_location`, 최소 metadata, hash와 적법하게 가린 발췌만 기록한다.
