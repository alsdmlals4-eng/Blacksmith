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
