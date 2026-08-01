# Blacksmith 비주얼 Placeholder·에셋·라이선스 거버넌스 정본

> Decision ID: `BS-VISUAL-ASSET-GOV-20260801-01`
>
> 상태: `USER_PREAPPROVED_RECOMMENDED / CANONICAL_DESIGN_COMPLETE`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 선행 결정: `BS-ART-20260731-01`, `BS-MODAK-20260731-01`, `BS-VISUAL-20260731-01`, `BS-MAIN-20260801-01`, `BS-SHELL-20260801-01`

## 1. 목적

비주얼 방향 승인, 콘셉트 이미지, 최종 제품 에셋, 라이선스 검증, 실제 화면 통합, 실기기 검증을 분리한다. 이미지에 등장한 임시 UI·수치·시스템이 게임 정본으로 승격되는 것을 막고, 모든 제품 에셋의 출처·권리·용도·버전·검수 증거를 추적한다.

## 2. 현재 승인 범위

### 승인됨

- 스타일라이즈드 다크 포지
- 장비가 시각적 주인공
- 어두운 대장간과 따뜻한 국소 화로 조명
- 철·황동 중심 UI 재질 문법
- 밝은 노랑·황금·주황 불 정령 모닥
- C안 기반 차분한 표정 7종
- 별도 메인 화면과 단일 제품 Shell
- 대장간 허브·작업·보관함·고객·결과 화면의 공통 방향

### 아직 승인되지 않음

- 최종 로고·배경·장비·캐릭터·아이콘·폰트 파일
- 실제 Android 화면의 모닥 크기·밝기·모션
- 최종 Theme Resource와 UI Scene
- 최종 오디오·효과음
- 외부 템플릿·에셋·폰트의 권리 적합성
- 실제 화면 시각 회귀 기준

## 3. Placeholder / NOT_CANON 목록

다음은 시안을 설명하기 위한 임시 요소이며 별도 Decision ID 없이는 구현하지 않는다.

```text
PLAYER_LEVEL
BLUE_GEM_OR_PREMIUM_CURRENCY
ENERGY_COUNTER
ACHIEVEMENTS
SHOP
DETAILED_CODEX_OR_GUIDE
SPECIAL_CRAFTING_AS_SEPARATE_SYSTEM
INVENTORY_128_OF_150
DIRECT_MARKET_EXPLORATION
DIRECT_ARENA_EXPLORATION_OR_COMBAT
IMAGE_DISPLAYED_PROBABILITIES
IMAGE_DISPLAYED_GOLD_MATERIAL_EQUIPMENT_VALUES
```

### 적용 규칙

- 작업지시문·와이어프레임·이미지 프롬프트에 `PLACEHOLDER / NOT_CANON` 태그를 유지한다.
- 구현 이슈·Codex Goal·데이터 JSON 생성 대상에서 제외한다.
- 승인 정본과 충돌하는 Placeholder는 최종 화면 사양에서 제거한다.
- 별도 시스템으로 승격할 때는 신규 Decision ID·영향 분석·Sheet 동기화를 요구한다.

## 4. 에셋 상태 모델

```text
PROPOSED
→ CONCEPT_DIRECTION_APPROVED
→ PRODUCTION_CANDIDATE
→ SOURCE_AND_LICENSE_VERIFIED
→ VISUAL_REVIEW_PASS
→ RUNTIME_INTEGRATED
→ DEVICE_VERIFIED
→ RELEASE_APPROVED

REJECTED / HISTORICAL / REPLACED
```

상태를 건너뛰지 않는다.

### 현재 상태

| 대상 | 상태 |
|---|---|
| 스타일라이즈드 다크 포지 | `CONCEPT_DIRECTION_APPROVED` |
| 모닥 밝은 불 정령 | `CONCEPT_DIRECTION_APPROVED` |
| 화면 보드 v1 | `CONCEPT_DIRECTION_APPROVED / WORKING_BASELINE` |
| 최종 제품 아트 | `NOT_CREATED_OR_NOT_REGISTERED` |
| 실제 화면 통합 | `NOT_RUN` |
| 실기기 검증 | `NOT_RUN` |
| 라이선스 검증 | `NOT_RUN` |

## 5. Asset Manifest 필수 필드

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

### Source Type

- `ORIGINAL_HANDMADE`
- `AI_GENERATED_OR_EDITED`
- `PURCHASED_ASSET`
- `OPEN_SOURCE_ASSET`
- `FONT`
- `REFERENCE_ONLY_NOT_SHIPPED`

`REFERENCE_ONLY_NOT_SHIPPED`는 제품 빌드에 포함할 수 없다.

## 6. License Ledger 필수 필드

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

### 상태

- `UNREVIEWED`
- `REVIEW_REQUIRED`
- `VERIFIED_FOR_PROJECT_USE`
- `ATTRIBUTION_REQUIRED`
- `BLOCKED`
- `EXPIRED_OR_REPLACED`

법적 판단이 불명확하면 `VERIFIED`로 추정하지 않고 `REVIEW_REQUIRED` 또는 `BLOCKED`로 둔다.

## 7. 파일·경로 규칙

권장 제품 경로:

```text
assets/art/environment/
assets/art/equipment/
assets/art/characters/
assets/art/modak/
assets/ui/icons/
assets/ui/backgrounds/
assets/ui/fonts/
assets/audio/bgm/
assets/audio/sfx/
```

- 파일명은 소문자 snake_case와 용도 suffix를 사용한다.
- 생성 원본·작업 파일과 런타임 최적화 파일을 구분한다.
- 런타임 파일만 Godot import 대상에 둔다.
- 외부 원본·구매 영수증·라이선스 증거를 제품 asset 폴더에 혼재시키지 않는다.
- 교체 에셋은 Manifest의 `replacement_of`로 연결하고 과거 항목을 삭제하지 않는다.

## 8. 모닥 제품 배치 규칙

### 역할

- 감정적 동반자·상태 반응
- 결과·위험·정답 예측 없음
- 성장·버프·재화 기능 없음
- 장비·확률·선택·결과 정보를 가리지 않음

### 권장 논리 크기 상한 — 720×1280 기준

| 화면 | 최대 바운딩 박스 | 용도 |
|---|---:|---|
| 메인·허브 | 160×160 | 환영·대기·상태 반응 |
| 단조·강화·고객 선택 | 112×112 | 보조 반응 |
| 결과·복구·경고 | 96×96 | 감정 보조, 정보 우선 |

실제 크기는 안전 영역·텍스트 크기·장비 영역을 기준으로 더 줄일 수 있다.

### 금지

- 주요 CTA 위 배치
- 장비 중앙 실루엣 위 배치
- 확률표·비용·정지 이유·ResultEnvelope 변화량 가림
- 텍스트 대비를 낮추는 과도한 bloom
- 항상 활짝 웃는 유아형 표현
- 감정 애니메이션 때문에 입력 지연 발생

## 9. 화면 시각 검수 세트

최소 Screenshot Baseline:

1. 별도 메인 — 저장 없음
2. 별도 메인 — 이어하기 가능
3. 저장 손상 복구
4. 대장간 허브
5. 단조 진행·정밀 마감
6. 강화 일반·선택 경계·+50 경로
7. 자동 강화 설정·정지
8. 보관함·장비 상세·연대기
9. 고객 Board·요청·인계
10. ResultEnvelope 일반·파괴·세계 결과
11. 설정·텍스트 확대·모션 감소
12. 오류·오프라인·저장 실패

### 검수 해상도

- 720×1280 기준
- 1080×2400 장형 Android
- 좌우·상하 cutout/safe inset 모의
- 텍스트 확대 단계
- reduced motion

## 10. 시각 검수 항목

```text
정보 위계
장비 시각 중심성
텍스트 대비
색상 외 상태 구분
48dp 터치 영역
안전 영역
긴 한국어 문자열
모닥 가림·밝기·표정
철·황동 문법 일관성
Placeholder 잔존
Asset ID·Manifest 연결
License 상태
```

### 통과 기준

- P0 정보 가림 0
- 48dp 미달 핵심 터치 0
- 색상만으로 구분하는 핵심 상태 0
- `PLACEHOLDER / NOT_CANON` 제품 화면 잔존 0
- Manifest 미등록 런타임 에셋 0
- License `UNREVIEWED/BLOCKED` 릴리스 에셋 0
- 모닥이 장비·결정 정보를 가리는 장면 0

## 11. AI 생성·편집 이미지 처리

- 대화에서 생성된 이미지는 자동으로 제품 에셋이 아니다.
- Manifest `AI_GENERATED_OR_EDITED` 또는 `REFERENCE_ONLY_NOT_SHIPPED`로 등록한다.
- 생성 시점, 사용한 지시문 요약, 편집 여부, 후처리, 승인 상태를 기록한다.
- 제품 후보는 원본 저장·해상도·투명 배경·압축·색공간·실제 화면 검수를 거친다.
- 특정 외부 작가의 고유 스타일을 직접 복제하는 지시를 제품 표준으로 사용하지 않는다.

## 12. 오디오 처리

BGM·SFX도 같은 Manifest와 License Ledger를 사용한다.

- 화면·상황별 의도
- loop 여부
- 길이·포맷·볼륨 기준
- 상업 이용·편집·표기 의무
- 진동·모션 감소와의 상호작용

오디오가 없다는 이유로 임시 파일을 릴리스 에셋으로 승격하지 않는다.

## 13. Google Sheet 역할

- `70_아트_오디오_에셋`: 아트·오디오 방향과 필요 자산군
- `71_이미지기획_생성목록`: 생성·제작 후보 Queue
- `72_이미지검수_승인로그`: 방향·후보·제품 검수 결과

GitHub Manifest·License Ledger가 상세 책임 원본이다. Sheet는 상태·요약·ID·링크를 보여주는 사용자 작업면이다.

## 14. 감사 판정

```text
BS-AUD-F10_PLACEHOLDER_TARGET: RESOLVED
BS-AUD-F23_MODAK_VALIDATION_CONTRACT: RESOLVED
BS-AUD-F24_ASSET_LICENSE_STRUCTURE: RESOLVED
BS-AUD-F25_SCREENSHOT_BASELINE_CONTRACT: RESOLVED
FINAL_PRODUCT_ASSETS: NOT_RUN
LICENSE_REVIEW: NOT_RUN
VISUAL_REGRESSION: NOT_RUN
DEVICE_VALIDATION: NOT_RUN
P0_P2_FINDING_COUNTS: 유지
```

## 15. 현재 Gate

```text
PLACEHOLDER_BOUNDARY: APPROVED
ASSET_STATUS_MODEL: APPROVED
ASSET_MANIFEST_SCHEMA: APPROVED
LICENSE_LEDGER_SCHEMA: APPROVED
MODAK_UI_LIMITS: APPROVED
SCREENSHOT_BASELINE_SET: APPROVED
FINAL_PRODUCT_ASSETS: NOT_RUN
PRODUCT_ASSET_INTEGRATION: BLOCKED
```
