# Blacksmith License Ledger

> 상태: `INITIAL / NO_RELEASE_ASSET_LICENSE_APPROVAL`
>
> 기준일: `2026-08-01`
>
> 거버넌스: `BS-VISUAL-ASSET-GOV-20260801-01`

이 문서는 제품 후보 에셋·폰트·아이콘·오디오·외부 템플릿의 상업적 사용, 수정, 표기, 재배포 제한과 증거 위치를 기록한다. 법적 해석이 불명확하면 승인으로 추정하지 않는다.

## 현재 항목

| License ID | Asset/Family | Provider | License | Commercial | Modify | Attribution | Status | 증거·비고 |
|---|---|---|---|---|---|---|---|---|
| `BS-LIC-DIRECTION-001` | `BS-VIS-DIRECTION-DARK-FORGE-001` | 프로젝트 내부 기획 | 해당 없음 | 해당 없음 | 해당 없음 | 없음 | `REFERENCE_ONLY` | 방향 문서이며 배포 파일 아님 |
| `BS-LIC-MODAK-CONCEPT-001` | `BS-CHAR-MODAK-CONCEPT-001` | 대화 기반 생성 레퍼런스 | 제품 사용 권리 검토 전 | 미확정 | 미확정 | 미확정 | `REVIEW_REQUIRED` | 생성 이미지 원본·서비스 조건·후처리·실제 제품 사용 여부 미검토 |
| `BS-LIC-VISUAL-BOARD-001` | `BS-UI-VISUAL-BOARD-001` | 프로젝트 내부 기획 | 해당 없음 | 해당 없음 | 해당 없음 | 없음 | `REFERENCE_ONLY` | UI 방향 문서이며 배포 파일 아님 |

## 필수 필드

```text
license_entry_id
asset_id_or_asset_family
source_url_or_purchase_record
provider
license_name
license_version
commercial_use_allowed
modification_allowed
attribution_required
redistribution_restrictions
ai_training_or_generation_terms_reviewed
proof_location
reviewer
reviewed_at
status
notes
```

## 상태 정의

- `UNREVIEWED`
- `REVIEW_REQUIRED`
- `VERIFIED_FOR_PROJECT_USE`
- `ATTRIBUTION_REQUIRED`
- `BLOCKED`
- `EXPIRED_OR_REPLACED`
- `REFERENCE_ONLY`

## 릴리스 차단

다음 상태의 에셋은 제품 빌드·스토어 스크린샷·홍보물에 포함할 수 없다.

```text
UNREVIEWED
REVIEW_REQUIRED
BLOCKED
REFERENCE_ONLY
```

## 현재 판정

```text
VERIFIED_RELEASE_LICENSES: 0
ATTRIBUTION_FILES: NOT_CREATED
FONT_LICENSES: NOT_REVIEWED
ICON_LICENSES: NOT_REVIEWED
AUDIO_LICENSES: NOT_REVIEWED
EXTERNAL_TEMPLATE_LICENSES: NOT_REVIEWED
```
