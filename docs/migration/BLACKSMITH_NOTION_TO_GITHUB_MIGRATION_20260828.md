# Blacksmith Notion → GitHub Migration Receipt · 2026-08-28

- Migration ID: `BS-OPS-20260828-35/NOTION-MIGRATION`
- Status: `COMPLETE / GITHUB_PATH_AND_HASH_VERIFIED`
- Source mode: `NOTION_READ_ONLY_ONE_TIME_SOURCE_MIGRATION`
- Future access: `NO_FUTURE_NOTION_READ_WRITE`
- Destination: this repository only
- Authority: `BS-OPS-20260828-35_GITHUB_ONLY_CANON_AND_IMAGE_EXECUTION_ROUTING.md`

## Purpose and boundary

사용자 지시에 따라 기존 Notion의 **구조와 유효한 작업물**을 GitHub 정본으로 이관했다. Notion은 이 이관 시점의 읽기 전용 출처일 뿐이며, 이 문서 이후에는 현재 사실 확인·문서 작성·동기화 대상으로 사용하지 않는다.

`CURRENT_MAPPED`는 현재 GitHub owner가 같은 의미를 소유한다는 뜻이다. 이미 현재 정본에 의해 대체된 규칙, 과거 수치표, 예전 상태 모델, 오래된 PR 수령증은 `OMITTED_STALE_DATA`로 보존 대상에서 제외했다. 이는 삭제가 아니라 현재 GitHub 정본에 재유입하지 않는다는 뜻이다.

```text
NOTION_READ_ONLY_ONE_TIME_SOURCE_MIGRATION = COMPLETE
NO_FUTURE_NOTION_READ_WRITE = TRUE
CURRENT_CANON_OWNER = GITHUB_REPOSITORY_ONLY
HISTORICAL_VISUAL_ARCHIVE = PRESERVED_NON_RUNTIME
OMITTED_STALE_DATA = NOT_IMPORTED_AS_CURRENT_TRUTH
```

## Structure and work-product map

| Notion source page | Source ID | Disposition | GitHub destination / ownership |
| --- | --- | --- | --- |
| Blacksmith Project Hub | `3c01b237-eb1c-8141-93ae-c528c4f3c40c` | `CURRENT_MAPPED` | `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md`; `exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf`; `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` (기술 추적) |
| Blacksmith Project Home | `3c41b237-eb1c-813f-a481-e415e3250d1c` | `CURRENT_MAPPED` | `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md`; `exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf`; `docs/planning/BLACKSMITH_HUMAN_GAME_FLOW_MAP_2026.md`; `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` (기술 추적) |
| Project System Record | `3c01b237-eb1c-81a1-8cd0-f8bc7eb2f420` | `CURRENT_MAPPED` | `AGENTS.md`; `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`; `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md` |
| Direction | `3c51b237-eb1c-81d7-80e0-d7e9fc704489` | `CURRENT_MAPPED` | `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`; `docs/decisions/BS-ENHANCE-20260828-34_WEAPON_KEYWORD_OWNERSHIP.md`; `docs/planning/BLACKSMITH_VISUAL_DIRECTION_LOCK_PACKET_20260828.md` |
| Flow | `3c01b237-eb1c-81a4-af26-c3057bfdcbbf` | `CURRENT_MAPPED` | `docs/planning/BLACKSMITH_HUMAN_GAME_FLOW_MAP_2026.md`; `docs/planning/PROJECT_CORE_SCENE_VISUAL_BOARD_20260828.md` |
| Core Systems | `3c11b237-eb1c-8143-baef-ecf4e697a258` | `CURRENT_MAPPED` | `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`; Decisions 28–32 JSON/decision owners |
| Enhancement / Economy | `3c51b237-eb1c-812b-8572-d6683dbfaf0a` | `CURRENT_MAPPED` | `docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json`; `docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json`; `docs/planning/BLACKSMITH_REPAIR_ECONOMY_REBASE_20260826.json` |
| Visual Bible | `3c01b237-eb1c-8147-abdf-fab51a8f9ad3` | `CURRENT_MAPPED` | `docs/planning/BLACKSMITH_VISUAL_DIRECTION_LOCK_PACKET_20260828.md`; `docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json`; `assets/ASSET_MANIFEST.json` |
| Visual UX Assets | `3c51b237-eb1c-81cf-b5c2-f25c9f14e9b3` | `CURRENT_MAPPED` | `docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json`; `assets/ASSET_MANIFEST.json` |
| Asset Library | `3c01b237-eb1c-817a-b257-cf6e2d299896` | `CURRENT_MAPPED` | `assets/ASSET_MANIFEST.json`; `docs/planning/BLACKSMITH_VISUAL_GDD_ASSET_APPROVAL_2026-08-25.md`; documentation archive below |
| Production / Handoff | `3c01b237-eb1c-8178-82e7-dd74ee265309` | `CURRENT_MAPPED` | `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`; `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` |
| Production Validation | `3c01b237-eb1c-810a-b307-eb2cb480b81a` | `CURRENT_MAPPED` | `docs/design/PROJECT_AI_PRODUCTION_SPEC.md`; `docs/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md` |
| Reference Benchmark | `3c01b237-eb1c-8139-a61fd9917994a726` | `CURRENT_MAPPED` | `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` § Appendix A; current research gate in `AGENTS.md` |
| Project Plan | `3c01b237-eb1c-8125-8e44-ed79bc638813` | `OMITTED_STALE_DATA` | Historic milestones and superseded numeric/system records are intentionally not re-imported. Current frontier is owned by the handoff and current decision files. |

The machine-readable version is [`BLACKSMITH_NOTION_MIGRATION_MANIFEST_20260828.json`](BLACKSMITH_NOTION_MIGRATION_MANIFEST_20260828.json). It holds the full source-page list and exact binary hashes.

## Historical visual work preserved as binaries

The eight previously approved Visual GDD originals were downloaded from their Notion page attachments, then checked against the pre-existing GitHub approval manifest. They are now stored under `docs/migration/historical_notion_gdd/`, outside runtime asset paths.

| Visual ID | Repository copy | Preservation state |
| --- | --- | --- |
| `BS-VIS-20260820-01` | `docs/migration/historical_notion_gdd/BS-VIS-20260820-01_enhancement_main_visual_gdd.png` | `HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME` |
| `BS-VIS-20260820-02` | `docs/migration/historical_notion_gdd/BS-VIS-20260820-02_feedback_ladder_visual_gdd.png` | `HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME` |
| `BS-VIS-20260820-04` | `docs/migration/historical_notion_gdd/BS-VIS-20260820-04_tension_band_visual_gdd.png` | `HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME` |
| `BS-VIS-20260820-05` | `docs/migration/historical_notion_gdd/BS-VIS-20260820-05_first_ten_minutes_storyboard_visual_gdd.png` | `HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME` |
| `BS-VIS-20260820-06` | `docs/migration/historical_notion_gdd/BS-VIS-20260820-06_current_max_durability_visual_gdd.png` | `HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME` |
| `BS-VIS-20260820-08` | `docs/migration/historical_notion_gdd/BS-VIS-20260820-08_max_scar_visual_gdd.png` | `HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME` |
| `BS-VIS-20260820-09` | `docs/migration/historical_notion_gdd/BS-VIS-20260820-09_repair_decision_visual_gdd.png` | `HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME` |
| `BS-VIS-20260824-10` | `docs/migration/historical_notion_gdd/BS-VIS-20260824-10_precision_customer_visual_gdd.png` | `HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME` |

These files preserve historical information architecture, previous approval history, and provenance only. They are **not** current style canon, runtime texture candidates, current balance/UI truth, Human usability proof, or Player Experience proof. Their embedded numbers and generated pseudo-text must never override the current repository owner.

## Migration gap audit and readback

- `CURRENT_MAPPED`: all discovered Home, System Record, Direction, Flow, Core System, Economy, Visual Bible, Asset Library, Handoff, Validation, and Benchmark surfaces have a GitHub owner.
- `HISTORICAL_VISUAL_ARCHIVE`: all eight approved Visual GDD binary originals are local, hash-verified, and intentionally non-runtime.
- `OMITTED_STALE_DATA`: previous formula tables, old precision/milestone arrangements, dual-penalty state semantics, and PR receipts were not copied as current data because the user allowed obsolete data to remain out of the migration.
- `NO_FUTURE_NOTION_READ_WRITE`: source IDs are retained only for provenance lookup; no future workflow depends on a Notion page, URL, database, preview, or destination readback.

Exact destination and SHA-256 readback is enforced by `tests/check_github_only_notion_migration_contract.py`.
