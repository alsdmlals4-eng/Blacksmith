# Blacksmith Asset Manifest

> 상태: `INITIAL_DIRECTION_ONLY / NO_RELEASE_ASSETS`
>
> 기준일: `2026-08-01`
>
> 거버넌스: `BS-VISUAL-ASSET-GOV-20260801-01`

이 문서는 제품에 사용하거나 사용할 후보 에셋의 ID·출처·용도·버전·검수 상태를 기록한다. 실제 런타임 파일이 없는 방향·레퍼런스도 누락시키지 않되 `REFERENCE_ONLY_NOT_SHIPPED`로 명확히 구분한다.

## 현재 항목

| Asset ID | 유형 | 이름 | 상태 | Source Type | 제품 경로 | License ID | 비고 |
|---|---|---|---|---|---|---|---|
| `BS-VIS-DIRECTION-DARK-FORGE-001` | art_direction | 스타일라이즈드 다크 포지 | `CONCEPT_DIRECTION_APPROVED` | `REFERENCE_ONLY_NOT_SHIPPED` | 없음 | `BS-LIC-DIRECTION-001` | 제품 그림체 방향. 단일 이미지 파일 아님 |
| `BS-CHAR-MODAK-CONCEPT-001` | character_concept | 밝은 불 정령 모닥 | `CONCEPT_DIRECTION_APPROVED` | `AI_GENERATED_OR_EDITED` | 없음 | `BS-LIC-MODAK-CONCEPT-001` | C안 표정+밝은 불 몸체. 대화 생성 이미지이며 제품 에셋 아님 |
| `BS-UI-VISUAL-BOARD-001` | ui_direction | 비주얼 상황 보드 v1 | `CONCEPT_DIRECTION_APPROVED` | `REFERENCE_ONLY_NOT_SHIPPED` | 없음 | `BS-LIC-VISUAL-BOARD-001` | 화면 문법 작업 기준. 수치·시스템 Placeholder 포함 |

## 제품 에셋 등록 조건

새 항목에는 최소 다음이 필요하다.

```text
asset_id
asset_type
display_name
status
canonical_decision_ids
source_type
source_reference
creator_or_provider
created_or_acquired_at
local_path
file_format
dimensions_or_duration
intended_usage
platform_scope
version
checksum
license_entry_id
modification_notes
review_evidence_ids
replacement_of
```

## 현재 판정

```text
RELEASE_APPROVED_ASSETS: 0
RUNTIME_INTEGRATED_ASSETS: 0
DEVICE_VERIFIED_ASSETS: 0
CONCEPT_DIRECTION_ENTRIES: 3
FINAL_PRODUCT_ASSET_CREATION: NOT_RUN
```
